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
Die Farben in der Tabelle sind Vorschläge (Standard Regenbogen-Kabel), um Verwechslungen zu vermeiden.

**⚠️ WICHTIG:** Das Display ist auf diesem Board intern bereits an GPIO 5 & 6 angeschlossen. Diese Pins nicht nutzen! Das PN5180 läuft auf **3.3V** (5V zerstört es!).



| ESP32-C3 Pin | PN5180 Pin | Funktion | Farbe (Kabel) |
| :--- | :--- | :--- | :--- |
| **3.3V** | **3.3V** | Stromversorgung | 🔴 **Rot** |
| **GND** | **GND** | Masse | ⚫ **Schwarz** |
| **GPIO 1** | **RST** | Reset | 🟡 **Gelb** |
| **GPIO 8** | **NSS** | Chip Select | 🟠 **Orange** |
| **GPIO 2** | **MOSI** | SPI Data Out | 🟢 **Grün** |
| **GPIO 3** | **MISO** | SPI Data In | 🔵 **Blau** |
| **GPIO 4** | **SCK** | SPI Clock | 🟣 **Lila** |
| **GPIO 10** | **BUSY** | Status Signal | ⚪ **Weiß/Grau** |

---

## 📺 Display-Anzeigen (Was passiert wann?)

Die Firmware V11.3 nutzt ein intelligentes 2-Seiten-System, um auf dem winzigen Display alle Infos anzuzeigen.

### 1. Start & Diagnose
Direkt nach dem Einstecken prüft der ESP32, ob der NFC-Reader antwortet.

| Status | Zeile 1 | Zeile 2 | Zeile 3 |
| :--- | :--- | :--- | :--- |
| **Boot** | `System Start` | `V11.3 (Final)` | `2026-01-22` |
| **Check OK** | `NFC OK` | `Chip: v3.5` | `Bereit.` |
| **Fehler** | `HARDWARE` | `FEHLER!` | `Kabel checken` |

### 2. Leerlauf (Warten)
Das Gerät ist bereit zum Scannen.
```text
Bereit
Warte auf
Figur...
