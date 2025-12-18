# 🎵 Jukebox PWA (v31) - DIY "Toniebox" für das Handy

Eine kinderfreundliche Musik-Player-App, die als Progressive Web App (PWA) direkt im Browser läuft. Sie ermöglicht es, Musik und Hörspiele über **NFC-Tags** (wie bei einer Toniebox) zu starten. Ideal, um alten Smartphones neues Leben als Kinder-Abspielgerät einzuhauchen.

## ✨ Neu in Version 31 (Cue Support)
* **📜 Kapitel-Unterstützung (.cue):** Du kannst jetzt beim Anlernen optional eine `.cue` Datei hochladen.
* **⏭️ Kapitel-Skip:** Wenn ein Hörspiel Kapitel hat, erscheint im Kinder-Modus ein zusätzlicher Button, um direkt zum nächsten Kapitel/Track zu springen.
* **📝 Titel-Anzeige:** Statt "Teil 1" wird der echte Name des aktuellen Kapitels (z.B. *"Benjamin kauft ein"*) angezeigt.

## 🚀 Alle Features im Überblick
* **🔋 Eco-Mode:** Handy aufs Display legen -> Bildschirm aus (spart Strom), Musik läuft weiter.
* **🔊 Lautstärke-Limit:** Eltern legen ein Maximum fest. Der Regler für Kinder skaliert relativ dazu (Logarithmisch für natürliches Hörempfinden).
* **💡 Screen Wake Lock:** Verhindert zuverlässig, dass das Handy in den Sperrbildschirm geht (nutzt Video-Trick).
* **NFC-Steuerung:** Musik durch Auflegen von Figuren/Karten starten.
* **Offline-Fähig:** Speichert Musik und Cover direkt im Browser (IndexedDB).

## 🛠️ Installation & Voraussetzungen

### Benötigte Hardware
1.  **Android Smartphone** mit NFC (empfohlen).
2.  **NFC-Tags** (NTAG213, NTAG215 oder NTAG216).
3.  Optional: Bluetooth-Lautsprecher.

### Software-Setup (Hosting)
Damit Sensoren (Eco-Modus) und NFC funktionieren, **MUSS** die App über einen Server laufen (`http://` oder `https://`).

**Option A: Lokal auf dem Handy (Offline / Empfohlen)**
1.  Erstelle einen Ordner `Jukebox` auf dem Handy und kopiere alle Dateien (`index.html`, `manifest.json`, Icons...) hinein.
2.  Installiere eine Webserver-App (z.B. *"Web Server for Chrome"* oder *"Simple HTTP Server"*).
3.  Starte den Server und öffne die Adresse (z.B. `http://127.0.0.1:8080`) in **Chrome**.

**Option B: Online (GitHub Pages)**
1.  Lade die Dateien in ein GitHub Repository hoch und aktiviere "GitHub Pages".
2.  Öffne die URL auf dem Handy.

### PWA Installation
Öffne die URL in Chrome -> Menü -> **"Zum Startbildschirm hinzufügen"** oder **"App installieren"**.

## 📖 Bedienungsanleitung

### 1. Musik hinzufügen (mit Kapiteln)
1.  Klicke auf **"Neuen Tag anlernen"**.
2.  Wähle die MP3-Datei bei `1. Audio Datei`.
3.  **(Neu)** Wähle die passende `.cue` Datei bei `2. Cue-Datei` (optional).
4.  Wähle ein Cover und vergib einen Namen.
5.  Klicke auf **"📡 Tag scannen & speichern"** und halte den NFC-Tag an.

### 2. Einstellungen (WICHTIG!)
* Stelle die **physischen Lautstärke-Tasten** am Handy auf **100%**.
* Nutze den Regler in der App ("Maximale Lautstärke"), um das Limit für das Kind zu setzen.
* Aktiviere **"Display anlassen"**, damit das Cover sichtbar bleibt.

### 3. Kinder-Modus verlassen
Es gibt keinen sichtbaren "Zurück"-Button.
➡️ **Tippe 5x schnell hintereinander in die obere rechte Ecke des Bildschirms.**

## 📂 Dateistruktur
* `index.html` - Der komplette Code.
* `manifest.json` - App-Konfiguration.
* `sw.js` - Service Worker (für Offline-Support).
* `icon.png` - App Icon.

## ⚠️ Hinweise
* **iOS/iPhone:** WebNFC wird nicht unterstützt. Die App läuft als Player, aber Tags scannen geht nur mit Android. Für den Eco-Modus Button "iOS Sensoren" drücken.
* **Browser-Daten:** Lösche niemals die Browser-Daten ("Webseitendaten"), sonst ist die angelernte Musik weg! Mache Backups.

## 👨‍💻 Credits
Entwickelt von Sebastian Rößer.
Ein Open-Source Projekt für Eltern.
