# 📟 ESP32 Tonie Unlocker (ABRobot Edition)

Ein kostengünstiges (< 10€) Standalone-Tool zum Analysieren von Tonie-Figuren, Deaktivieren des Privacy-Modes (bei Kreativ-Tonies) und Auslesen der echten UIDs für die KlangKiste.

Basierend auf dem extrem kompakten **ESP32-C3 SuperMini mit integriertem 0.42" OLED**.

![Project Teaser](../../docs/screenshots/hardware_teaser.jpg)
*(Platzhalter für dein Foto vom fertigen Aufbau)*

## 📸 Projekt-Übersicht

| **Komponente** | **Beschreibung** |
| :--- | :--- |
| **Ziel** | Privacy Unlock & UID Auslesen (Block 4 Check) |
| **Firmware** | [Esp32_Tonie_Unlocker.ino](Esp32_Tonie_Unlocker.ino) |
| **Bibliothek** | [PN5180-Library von ATrappmann](https://github.com/ATrappmann/PN5180-Library) |

---

## 💰 Einkaufsliste (Bill of Materials)

Preise basierend auf AliExpress (Stand: Jan 2026).

| Komponente | Details | Preis ca. |
| :--- | :--- | :--- |
| **ESP32-C3 OLED** | "ESP32-C3 SuperMini Development Board 0.42 inch OLED" | **2,60 €** |
| **NFC Reader** | "PN5180 NFC RF Sensor ISO15693" (Rot oder Grün) | **5,02 €** |
| **Kabel** | "Dupont Jumper Wire 10cm Female-to-Female" | **1,30 €** |
| **Gesamt** | | **~ 8,92 €** |

---

## 🛠️ Verkabelung (Wiring)

Wir nutzen handelsübliche **Female-to-Female (Buchse-zu-Buchse)** Jumper-Kabel.
**Achtung:** NSS (Chip Select) liegt bei dieser Konfiguration auf **GPIO 8**!

| PN5180 Pin | ESP32-C3 Pin | Farbe (Dein Setup) | Funktion |
| :--- | :--- | :--- | :--- |
| **5V** | **5V** | 🔴 **Rot** | Strom für Antenne (Optional) |
| **3.3V** | **3.3V** | 🟠 **Orange** | Strom für Logik |
| **GND** | **GND** | ⚫ **Schwarz** | Masse |
| **RST** | **GPIO 1** | 🟣 **Lila** | Reset |
| **NSS** | **GPIO 8** | 🔘 **Grau** | Chip Select |
| **MOSI** | **GPIO 2** | 🔵 **Blau** | Daten zum PN5180 |
| **MISO** | **GPIO 3** | 🟡 **Gelb** | Daten vom PN5180 |
| **SCK** | **GPIO 4** | 🟢 **Grün** | Takt |
| **BUSY** | **GPIO 10** | ⚪ **Weiß** | Status |

> **Hinweis zum 5V Pin:** Da dein PN5180 Modul einen 5V Pin hat, kannst du diesen an den 5V (VBUS) des ESP32 anschließen, um die Antennenleistung zu stärken. Die Datenleitungen (MOSI, MISO etc.) bleiben dabei sicher auf 3.3V.

---

## 📺 Display-Anzeigen (Logik)

Die Firmware **V11.3** nutzt ein intelligentes 2-Seiten-System, um auf dem winzigen Display alle Infos anzuzeigen.

### 1. Start & Diagnose
Direkt nach dem Einstecken prüft der ESP32, ob der NFC-Reader antwortet.

| Status | Zeile 1 | Zeile 2 | Zeile 3 |
| :--- | :--- | :--- | :--- |
| **Boot** | `System Start` | `V11.3 (Custom)` | `2026-01-22` |
| **Check OK** | `NFC OK` | `Chip: v3.5` | `Bereit.` |
| **Fehler** | `HARDWARE` | `FEHLER!` | `Kabel checken` |

### 2. Leerlauf (Warten)
Das Gerät ist bereit zum Scannen.
```text
Bereit
Warte auf
Figur...
```

### 3. Figur erkannt (Szenarien)
Wenn eine Figur aufgelegt wird, versucht das Tool sie zu entsperren und liest den Speicher.

**✅ Szenario A: Kreativ-Tonie (Unlock erfolgreich)**
Zeigt an, dass die Figur "offen" ist und welche Audio-ID sie hat (für Custom Content).

*Seite 1 (2,5 Sek):*
```text
UNLOCKED!
Typ: Custom
ID: 21161870
```
*Seite 2 (5,0 Sek - Die lange Seriennummer):*
```text
SerialNr.:
E0:04:03:50:
1B:5A:0F:C5
```

**✅ Szenario B: Original-Tonie / Standard Tag**
Zeigt an, dass der Tag lesbar ist, aber keinen Custom-Inhalt hat.

*Seite 1:*
```text
UNLOCKED!
Typ: Original
(Standard)
```

**❌ Szenario C: Gesperrt (Privacy Mode aktiv)**
Konnte trotz Unlock-Versuch nicht gelesen werden (falsches Passwort oder defekt).

*Seite 1:*
```text
LOCKED!
Privacy Mode
Aktiv!
```

---

## 💻 Software Installation

### 1. Arduino IDE Setup
* **Version:** Arduino IDE 2.3.7 (oder neuer)
* **Board Manager URL:** `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
* **Installiertes Paket:** `esp32 by Espressif Systems`
    * ⚠️ **WICHTIG:** Wähle **Version 2.0.17**! (Version 3.x verursacht SPI-Fehler).

### 2. Board Einstellungen (Tools Menü)
* **Board:** `ESP32C3 Dev Module`
* **USB CDC On Boot:** `Enabled` (Zwingend nötig für Serial Monitor!)
* **CPU Frequency:** `160MHz (WiFi)`
* **Flash Mode:** `QIO`
* **Flash Frequency:** `80MHz`
* **Partition Scheme:** `Default 4MB with spiffs`
* **Upload Speed:** `921600`

### 3. Bibliotheken
Installiere folgende Bibliotheken über den Library Manager oder Import:

1.  `Adafruit SSD1306` (Display)
2.  `Adafruit GFX Library` (Grafik)
3.  `Adafruit BusIO`
4.  **PN5180 Library:**
    * Download: [ATrappmann/PN5180-Library](https://github.com/ATrappmann/PN5180-Library) (Code -> Download ZIP)
    * Import: `Sketch` -> `Bibliothek einbinden` -> `.ZIP Bibliothek hinzufügen`

### 🔧 Der "Privacy Hack" (Zwingend erforderlich!)
Damit der ESP32 den Befehl zum Entsperren des Privacy-Modes senden darf, müssen wir eine Sicherheitsstufe in der Bibliothek entfernen.

1.  Gehe in deinen Arduino Ordner: `Dokumente/Arduino/libraries/PN5180-Library-master/src/`
2.  Öffne die Datei `PN5180ISO15693.h` mit einem Texteditor.
3.  Suche die Zeile `class PN5180ISO15693 {`.
4.  Suche direkt darunter das Wort `private:`.
5.  Ändere es in `public:`.
6.  Speichern.

> **Grund:** Die Funktion `issueISO15693Command` ist normalerweise versteckt, wir brauchen sie aber für den Unlock-Befehl.

### 📄 Firmware flashen

1.  Öffne die Datei `Esp32_Tonie_Unlocker.ino` aus diesem Repository.
2.  **Passwort setzen (Wichtig):**
    Suche im Code nach dem Abschnitt `SICHERHEITSEINSTELLUNGEN`. Du musst dort das Passwort für den ICODE-SLIX2 (Privacy Mode) eintragen. Ohne das korrekte Passwort können Kreativ-Tonies nicht entsperrt werden.

    ```cpp
    // ================================================================
    // SICHERHEITSEINSTELLUNGEN
    // ================================================================
    // check for ICODE-SLIX2 password protected tag
    // put your privacy password here, e.g.:
    // [https://de.ifixit.com/Antworten/Ansehen/513422/nfc+Chips+f%C3%BCr+tonies+kaufen](https://de.ifixit.com/Antworten/Ansehen/513422/nfc+Chips+f%C3%BCr+tonies+kaufen)
    //
    // default factory password for ICODE-SLIX2 is {0x0F, 0x0F, 0x0F, 0x0F}
    const uint8_t toniePass[] = {0x00, 0x00, 0x00, 0x00}; // <-- Hier dein PW eintragen!
    ```

3.  Schließe den ESP32-C3 per USB-C an.
4.  Wähle den richtigen COM-Port und klicke auf **Upload**.
