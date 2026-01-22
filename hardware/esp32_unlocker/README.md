# 📟 ESP32 Tonie Unlocker & Diagnostic Tool

Ein Standalone-Tool zum Analysieren von Tonie-Figuren, Deaktivieren des Privacy-Mode (bei Kreativ-Tonies) und Auslesen der echten UIDs für die KlangKiste.

![PCB Setup](img/pcb_setup.jpg)
*(Füge hier deine Bilder vom Aufbau ein)*

## ✨ Funktionen (Firmware V11.3)
1.  **Privacy Unlock:** Entfernt die Sperre von neuen Kreativ-Tonies automatisch.
2.  **Deep Scan:** Liest Block 4 des NFC-Tags, um zwischen "Original", "Custom" und "Locked" zu unterscheiden.
3.  **Display:** Zeigt UID und Status auf einem OLED-Display an (2-Seiten-Ansicht).
4.  **Hardware Check:** Prüft beim Start, ob der PN5180 korrekt verkabelt ist.

---

## 🛠️ Hardware & Verkabelung

### Komponenten
* **ESP32-C3** (SuperMini oder DevKit)
* **PN5180** NFC Modul (Besser Reichweite als RC522, ISO15693 Support)
* **SSD1306** OLED Display (0.96" I2C)

### Verdrahtung (Wiring Diagram)

| ESP32-C3 Pin | PN5180 Pin | OLED Display |
| :--- | :--- | :--- |
| **3.3V** | 3.3V | VCC |
| **GND** | GND | GND |
| **GPIO 1** | RST | - |
| **GPIO 8** | NSS (SS) | - |
| **GPIO 2** | MOSI | - |
| **GPIO 3** | MISO | - |
| **GPIO 4** | SCK | - |
| **GPIO 10** | BUSY | - |
| **GPIO 5** | - | SDA |
| **GPIO 6** | - | SCL |

![Wiring](img/wiring.jpg)

---

## 💻 Software Installation

Die Firmware muss mit der **Arduino IDE** (Version 2.3.7 empfohlen) geflasht werden.

### ⚠️ WICHTIG: Versionen beachten!
Neuere Versionen des ESP32-Board-Pakets führen zu Fehlern. Bitte exakt diese Versionen nutzen:

1.  **Board Manager:**
    * Installiere `esp32 by Espressif Systems`.
    * Wähle **Version 2.0.17** aus (Nicht 3.0+!).
2.  **Bibliotheken (Library Manager):**
    * `Adafruit SSD1306`
    * `Adafruit GFX Library`
    * `Adafruit BusIO`
3.  **NFC Bibliothek:**
    * Lade die **[PN5180-Library von ATrappmann](https://github.com/ATrappmann/PN5180-Library)** als ZIP herunter.
    * Importiere sie in Arduino: *Sketch -> Bibliothek einbinden -> .ZIP Bibliothek hinzufügen*.

### 🔧 Der "Bibliotheks-Hack" (Zwingend erforderlich)
Damit der Unlock-Befehl gesendet werden darf, muss eine geschützte Funktion in der Bibliothek freigeschaltet werden:

1.  Navigiere zu deinem Arduino Bibliotheks-Ordner (Dokumente/Arduino/libraries/PN5180...).
2.  Öffne die Datei `src/PN5180ISO15693.h` mit einem Texteditor.
3.  Suche die Zeile `class PN5180ISO15693 {`.
4.  Suche darunter `private:`.
5.  **Ändere `private:` zu `public:`.**
6.  Speichern.

### ⚙️ Arduino IDE Einstellungen (Tools)
* **Board:** ESP32C3 Dev Module
* **USB CDC On Boot:** Enabled (Wichtig für Serial Monitor!)
* **CPU Frequency:** 160MHz (WiFi)
* **Flash Mode:** QIO
* **Flash Frequency:** 80MHz
* **Partition Scheme:** Default 4MB with spiffs
* **Upload Speed:** 921600

---

## 📄 Firmware Code (V11.3)

Kopiere diesen Code in deinen Sketch (`.ino` Datei):

```cpp
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <PN5180ISO15693.h>

// ================================================================
// EINSTELLUNGEN
// ================================================================
#define FIRMWARE_VERSION "V11.3 (Final)"
#define BUILD_DATE       "2026-01-22" 

// Display Setup (128x64)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_SDA 5
#define OLED_SCL 6
#define OLED_ADDRESS 0x3C

// Offset (28px links), damit Gehäuse den Text nicht verdeckt
#define X_OFF 28  
#define Y_OFF 24

// NFC Hardware (ESP32-C3 Pins)
#define PN5180_RST  1   
#define PN5180_BUSY 10
#define PN5180_SS   8   
#define PN5180_MOSI 2
#define PN5180_MISO 3
#define PN5180_SCK  4

// Das geheime Tonie-Passwort
const uint8_t toniePass[] = {0x5B, 0x6E, 0xFD, 0x7F};

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ================================================================
// LOGIK KLASSE (Erbt von der Lib, um Commands zu senden)
// ================================================================
class TonieNFC : public PN5180ISO15693 {
  public:
    using PN5180ISO15693::PN5180ISO15693;

    // Führt den Unlock durch (Privacy Mode deaktivieren)
    bool unlockTonie() {
      uint8_t cmdGetRnd[] = {0x02, 0xB2, 0x04}; 
      uint8_t resp[16]; uint8_t *respPtr = resp; 
      
      // 1. Zufallszahl vom Tag holen
      ISO15693ErrorCode rc = issueISO15693Command(cmdGetRnd, sizeof(cmdGetRnd), &respPtr);
      if (rc != ISO15693_EC_OK) return false;

      // 2. Passwort berechnen (XOR mit Zufallszahl)
      uint8_t rnd1 = respPtr[1]; uint8_t rnd2 = respPtr[2];
      uint8_t xorPW[4];
      xorPW[0] = toniePass[0] ^ rnd1; xorPW[1] = toniePass[1] ^ rnd2;
      xorPW[2] = toniePass[2] ^ rnd1; xorPW[3] = toniePass[3] ^ rnd2;
      
      // 3. Unlock senden
      uint8_t cmdUnlock[] = {0x02, 0xB3, 0x04, 0x04, xorPW[0], xorPW[1], xorPW[2], xorPW[3]};
      return (issueISO15693Command(cmdUnlock, sizeof(cmdUnlock), &respPtr) == ISO15693_EC_OK);
    }
};

TonieNFC nfc(PN5180_SS, PN5180_BUSY, PN5180_RST);

// ================================================================
// HELFER FUNKTIONEN
// ================================================================

// Formatiert UID mit Doppelpunkten: E0:04:03...
String getFormattedUID(uint8_t* uid) {
  String s = "";
  for (int i = 7; i >= 0; i--) {
    if (uid[i] < 0x10) s += "0";
    s += String(uid[i], HEX);
    if (i > 0) s += ":"; 
  }
  s.toUpperCase();
  return s;
}

// Zeigt eine "Seite" auf dem Display an
void showPage(String l1, String l2, String l3) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(X_OFF + 2, Y_OFF + 2);  display.println(l1);
  display.setCursor(X_OFF + 2, Y_OFF + 14); display.println(l2);
  display.setCursor(X_OFF + 2, Y_OFF + 26); display.println(l3);
  
  display.display();
}

// ================================================================
// SETUP
// ================================================================
void setup() {
  Serial.begin(115200);
  delay(1000); 

  // Display Init
  Wire.begin(OLED_SDA, OLED_SCL); 
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
     Serial.println("Display Error");
  }
  
  showPage("System Start", FIRMWARE_VERSION, BUILD_DATE);
  delay(2000);

  // NFC Init
  SPI.begin(PN5180_SCK, PN5180_MISO, PN5180_MOSI, PN5180_SS);
  nfc.begin(); 
  nfc.reset();
  
  // Hardware Check
  uint8_t productVersion[2];
  nfc.readEEprom(PRODUCT_VERSION, productVersion, 2);
  if (productVersion[1] == 0xFF || productVersion[1] == 0x00) {
      showPage("HARDWARE", "FEHLER!", "Kabel checken");
      while(1) delay(100); 
  }
  
  nfc.setupRF(); // HF Feld einschalten
  showPage("Bereit", "Warte auf", "Figur...");
}

// ================================================================
// LOOP
// ================================================================
void loop() {
  
  // 1. UNLOCK VERSUCH (Blindfeuer)
  bool unlockSent = nfc.unlockTonie();
  if(unlockSent) delay(5); 

  // 2. SCAN
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  
  if (rc == ISO15693_EC_OK) {
    Serial.println(F("TAG GEFUNDEN"));
    showPage("Gefunden!", "Lese...", "Daten...");

    // 3. VALIDIERUNG: Können wir Block 4 lesen?
    // Das bestätigt, ob der Privacy Mode wirklich aus ist.
    uint8_t data[4];
    ISO15693ErrorCode readRC = nfc.readSingleBlock(uid, 4, data, 4);

    if (readRC == ISO15693_EC_OK) {
        // --- TAG IST OFFEN (UNLOCKED) ---
        uint32_t audioID = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
        
        String typeLine = "Typ: Original";
        String idLine = "(Standard)";
        
        if (audioID > 0) {
            typeLine = "Typ: Custom";
            idLine = "ID: " + String(audioID);
        }

        // SEITE 1: Status & Typ (2,5 Sek)
        showPage("UNLOCKED!", typeLine, idLine);
        delay(2500); 

        // SEITE 2: Seriennummer groß (5,0 Sek)
        String fullUID = getFormattedUID(uid); 
        String part1 = fullUID.substring(0, 12); // Erste Hälfte
        String part2 = fullUID.substring(12);    // Zweite Hälfte
        
        showPage("SerialNr.:", part1, part2);
        delay(5000);

    } else {
        // --- FEHLER: TAG IST GESPERRT (LOCKED) ---
        showPage("LOCKED!", "Privacy Mode", "Aktiv!");
        delay(2500);
        
        // Zeige trotzdem UID zur Diagnose
        String fullUID = getFormattedUID(uid);
        String part1 = fullUID.substring(0, 12);
        String part2 = fullUID.substring(12);
        showPage("SerialNr.:", part1, part2);
        delay(5000);
    }
    
    // Reset für nächsten Scan
    showPage("Bereit", "Warte auf", "Figur...");
    nfc.reset();
    nfc.setupRF();
  }
  
  delay(50);
}
