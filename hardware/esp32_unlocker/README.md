# 📟 ESP32 Tonie Unlocker (ABRobot Edition)

Ein kompaktes Standalone-Tool zum Analysieren von Tonie-Figuren und Deaktivieren des Privacy-Modes. Basierend auf dem **ESP32-C3 mit integriertem OLED**.

## ✨ Funktionen (Firmware V11.3)
* **All-in-One:** Sehr kompakt durch integriertes Display.
* **Privacy Unlock:** Entfernt die Sperre von neuen Kreativ-Tonies (Passwort erforderlich, siehe Code).
* **Deep Scan:** Zeigt "Original" vs. "Custom" und die echte UID an.
* **Safety:** Nutzt nur 3.3V Logik (NFC-Reader freundlich).

---

## 🛠️ Hardware Setup

### Komponenten
1.  **Board:** ESP32-C3 mit 0.42" OLED (z.B. ABRobot / SuperMini OLED).
2.  **NFC:** PN5180 Modul.
3.  **Kabel:** 8x Jumper Wires (Female-to-Female).

### Verkabelung (Pinout)

Da das Display intern verdrahtet ist (SDA=5, SCL=6), muss nur der NFC-Reader angeschlossen werden:

| ESP32-C3 Pin | PN5180 Pin | Funktion |
| :--- | :--- | :--- |
| **3.3V** | 3.3V | VCC |
| **GND** | GND | GND |
| **GPIO 1** | RST | Reset |
| **GPIO 8** | NSS | Chip Select |
| **GPIO 2** | MOSI | SPI MOSI |
| **GPIO 3** | MISO | SPI MISO |
| **GPIO 4** | SCK | SPI Clock |
| **GPIO 10** | BUSY | Busy Signal |

> **Hinweis:** Die Pins GPIO 5, 6, 7 und 9 werden beim Booten oder vom Display genutzt und sollten für den NFC Reader vermieden werden. Unsere Belegung oben berücksichtigt das.

---

## 💻 Software Installation

### 1. Arduino IDE Setup
* **Board Manager URL:** `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
* **Board Auswahl:** `ESP32C3 Dev Module`
* **WICHTIG:** Version **2.0.17** des `esp32` Pakets nutzen! (Nicht 3.x)

### 2. Einstellungen (Tools Menü)
* **USB CDC On Boot:** `Enabled` (Sonst kein Serial Monitor!)
* **Flash Mode:** `QIO`
* **Partition Scheme:** `Default 4MB with spiffs`

### 3. Bibliotheken
Installiere folgende Libs:
* `Adafruit SSD1306`
* `Adafruit GFX Library`
* `PN5180 Library` von *ATrappmann*: [GitHub Link](https://github.com/ATrappmann/PN5180-Library) (als ZIP importieren).

**⚠️ Library Hack (Wichtig!):**
Öffne die Datei `src/PN5180ISO15693.h` in der installierten PN5180-Bibliothek und ändere `private:` zu `public:` um den Unlock-Befehl freizuschalten.

---

## 📄 Firmware

Lade die Datei [`Esp32_Tonie_Unlocker.ino`](Esp32_Tonie_Unlocker.ino) auf das Board.
**Achtung:** Du musst im Code das Passwort für den Privacy-Mode selbst eintragen (siehe Kommentar im Code).
