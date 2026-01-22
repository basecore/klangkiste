#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <PN5180ISO15693.h>

// ================================================================
// EINSTELLUNGEN
// ================================================================
#define FIRMWARE_VERSION "V11.3 (2-Pages)"
#define BUILD_DATE       "2026-01-22" 

// Display Setup (ABRobot ESP32-C3 internal wiring)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_SDA 5
#define OLED_SCL 6
#define OLED_ADDRESS 0x3C

// Offset (28px links), damit Gehäuse den Text nicht verdeckt
#define X_OFF 28  
#define Y_OFF 24

// NFC Hardware
#define PN5180_RST  1   
#define PN5180_BUSY 10
#define PN5180_SS   8   
#define PN5180_MOSI 2
#define PN5180_MISO 3
#define PN5180_SCK  4

// ================================================================
// SICHERHEITSEINSTELLUNGEN
// ================================================================
// check for ICODE-SLIX2 password protected tag
// put your privacy password here, e.g.:
// https://de.ifixit.com/Antworten/Ansehen/513422/nfc+Chips+f%C3%BCr+tonies+kaufen
//
// default factory password for ICODE-SLIX2 is {0x0F, 0x0F, 0x0F, 0x0F}
//
const uint8_t toniePass[] = {0x00, 0x00, 0x00, 0x00}; // <--- HIER ANPASSEN!

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ================================================================
// LOGIK KLASSE
// ================================================================
class TonieNFC : public PN5180ISO15693 {
  public:
    using PN5180ISO15693::PN5180ISO15693;

    bool unlockTonie() {
      uint8_t cmdGetRnd[] = {0x02, 0xB2, 0x04}; 
      uint8_t resp[16]; uint8_t *respPtr = resp; 
      
      ISO15693ErrorCode rc = issueISO15693Command(cmdGetRnd, sizeof(cmdGetRnd), &respPtr);
      if (rc != ISO15693_EC_OK) return false;

      uint8_t rnd1 = respPtr[1]; uint8_t rnd2 = respPtr[2];
      uint8_t xorPW[4];
      xorPW[0] = toniePass[0] ^ rnd1; xorPW[1] = toniePass[1] ^ rnd2;
      xorPW[2] = toniePass[2] ^ rnd1; xorPW[3] = toniePass[3] ^ rnd2;
      
      uint8_t cmdUnlock[] = {0x02, 0xB3, 0x04, 0x04, xorPW[0], xorPW[1], xorPW[2], xorPW[3]};
      return (issueISO15693Command(cmdUnlock, sizeof(cmdUnlock), &respPtr) == ISO15693_EC_OK);
    }
};

TonieNFC nfc(PN5180_SS, PN5180_BUSY, PN5180_RST);

// ================================================================
// HELFER FUNKTIONEN
// ================================================================

// Erzeugt den langen String mit Doppelpunkten: E0:04:03...
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

  // Display
  Wire.begin(OLED_SDA, OLED_SCL); 
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS);
  
  showPage("Tonie Reader", FIRMWARE_VERSION, BUILD_DATE);
  delay(2000);

  // NFC
  SPI.begin(PN5180_SCK, PN5180_MISO, PN5180_MOSI, PN5180_SS);
  nfc.begin(); nfc.reset();
  
  uint8_t productVersion[2];
  nfc.readEEprom(PRODUCT_VERSION, productVersion, 2);
  if (productVersion[1] == 0xFF) {
      showPage("HARDWARE", "FEHLER!", "Kabel checken");
      while(1) delay(100); 
  }
  
  nfc.setupRF(); 
  showPage("Bereit", "Warte auf", "Figur...");
}

// ================================================================
// LOOP
// ================================================================
void loop() {
  
  // 1. UNLOCK
  bool unlockSent = nfc.unlockTonie();
  if(unlockSent) delay(5); 

  // 2. SCAN
  uint8_t uid[8];
  ISO15693ErrorCode rc = nfc.getInventory(uid);
  
  if (rc == ISO15693_EC_OK) {
    Serial.println(F("TAG GEFUNDEN"));
    showPage("Gefunden!", "Lese...", "Daten...");

    // 3. READ BLOCK 4 (Check Privacy)
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
        
        // Seite 2: Trotzdem UID anzeigen
        String fullUID = getFormattedUID(uid);
        String part1 = fullUID.substring(0, 12);
        String part2 = fullUID.substring(12);
        showPage("SerialNr.:", part1, part2);
        delay(5000);
    }
    
    // Reset
    showPage("Bereit", "Warte auf", "Figur...");
    nfc.reset();
    nfc.setupRF();
  }
  
  delay(50);
}
