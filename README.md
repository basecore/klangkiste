# 🎵 Jukebox PWA (v28) - DIY "Toniebox" für das Handy

Eine kinderfreundliche Musik-Player-App, die als Progressive Web App (PWA) direkt im Browser läuft. Sie ermöglicht es, Musik und Hörspiele über **NFC-Tags** (wie bei einer Toniebox) zu starten. Ideal, um alten Smartphones neues Leben als Kinder-Abspielgerät einzuhauchen.

Entwickelt als lokale Lösung ohne Cloud-Zwang, ohne Tracking und komplett kostenlos.

## ✨ Neu in Version 28 (Volume Fix)
* **🔊 Intelligente Lautstärkebegrenzung:** Der Lautstärkebalken im Kinder-Modus skaliert jetzt relativ zum Eltern-Limit.
    * *Beispiel:* Wenn du das Limit auf 50% setzt, entspricht "Vollgas" im Kinder-Modus genau diesen 50%. Das Kind kann also fein regeln, aber niemals lauter machen, als du erlaubt hast.
* **⚠️ Hardware-Warnung:** Ein Hinweis erinnert daran, die physischen Lautstärketasten des Handys auf Maximum zu stellen, damit die App die Kontrolle übernehmen kann.
* **🔋 Robuster Eco-Modus:** Verbesserte Erkennung beim Umdrehen des Handys (Display aus), auch auf älteren Geräten.
* **💡 Screen Wake Lock:** Verhindert zuverlässig, dass das Handy in den Sperrbildschirm geht, während Musik läuft.

## 🚀 Funktionen
* **NFC-Steuerung:** Musik durch Auflegen von Figuren/Karten starten.
* **Kinder-Modus:**
    * Große, bunte Tasten.
    * Gesperrte Einstellungen.
    * Geheimer Ausweg (5x Tippen).
* **Eltern-Bereich:**
    * Tags anlernen & verwalten.
    * **Test-Ton-Button:** Zum schnellen Prüfen der Maximallautstärke.
    * Schlaf-Timer (Fade-out).
    * Design anpassen (Hintergrundbild oder Farbe).
    * Datenbank Backup & Restore.
* **Offline-Fähig:** Speichert Musik und Cover direkt im Browser (IndexedDB).

## 🛠️ Installation & Voraussetzungen

### Benötigte Hardware
1.  **Android Smartphone** mit NFC (empfohlen).
2.  **NFC-Tags** (NTAG213, NTAG215 oder NTAG216) – z.B. Sticker, Karten oder Schlüsselanhänger.
3.  Optional: Bluetooth-Lautsprecher für besseren Klang.

### Software-Setup (Hosting)
Damit Sensoren (Eco-Modus) und NFC funktionieren, **MUSS** die App über einen Server laufen. Einfaches Öffnen der Datei (`file://`) reicht oft nicht!

**Option A: Lokal auf dem Handy (Offline / Empfohlen)**
1.  Erstelle einen Ordner `Jukebox` auf dem Handy und kopiere alle Dateien (`index.html`, `manifest.json`, Icons...) hinein.
2.  Installiere eine simple Webserver-App aus dem PlayStore (z.B. *"Web Server for Chrome"* oder *"Simple HTTP Server"*).
3.  Starte den Server in der App und öffne die angezeigte Adresse (meist `http://127.0.0.1:8080`) in **Chrome**.

**Option B: Online (GitHub Pages)**
1.  Lade die Dateien in ein GitHub Repository hoch.
2.  Aktiviere "GitHub Pages" in den Einstellungen.
3.  Öffne die URL (`https://dein-name.github.io/...`) auf dem Handy.

### PWA Installation (App-Feeling)
1.  Öffne die URL in **Chrome** auf dem Android-Gerät.
2.  Tippe auf das Menü (3 Punkte) -> **"Zum Startbildschirm hinzufügen"** oder **"App installieren"**.
3.  Starte die App nun über das Icon auf dem Homescreen (Vollbild, ohne Adressleiste).

## 📖 Bedienungsanleitung

### 1. Lautstärke einstellen (WICHTIG!)
1.  Stelle sicher, dass die **physischen Lautstärke-Tasten** am Handy auf **100% (Maximum)** stehen.
2.  Gehe in die App-Einstellungen (Eltern-Modus).
3.  Schiebe den Regler "Maximale Lautstärke" auf das gewünschte Limit (z.B. 40%).
4.  Drücke auf **"🔊 Test-Ton spielen"**, um zu hören, wie laut es maximal wird.

### 2. Musik hinzufügen
1.  Klicke auf **"Neuen Tag anlernen"**.
2.  Wähle Audio-Dateien und (optional) ein Bild.
3.  Vergib einen Namen.
4.  Klicke auf **"📡 Tag scannen & speichern"** und halte den NFC-Tag an.

### 3. Eco-Modus nutzen
1.  Aktiviere in den Einstellungen **"Stromsparen beim Umdrehen"**.
2.  Starte Musik im Kinder-Modus.
3.  Lege das Handy mit dem **Display nach unten** auf den Tisch.
4.  Der Bildschirm wird schwarz (spart Strom), die Musik läuft weiter, das Handy sperrt sich nicht.

### 4. Kinder-Modus verlassen
Es gibt keinen sichtbaren "Zurück"-Button.
➡️ **Tippe 5x schnell hintereinander in die obere rechte Ecke des Bildschirms.**

## 📂 Dateistruktur

* `index.html` - Der komplette Code der App (Logic & Design).
* `manifest.json` - Konfiguration für die Installation als App.
* `sw.js` - Service Worker (für Offline-Support, muss im selben Ordner liegen).
* `icon.png` - App Icon.

## ⚠️ Hinweise
* **iOS/iPhone:** Unterstützt *Web NFC* noch nicht. Die App kann als Player genutzt werden, aber Tags scannen geht nur mit Android. Für den Eco-Modus auf dem iPhone muss der Button "iOS Sensoren aktivieren" gedrückt werden.
* **Datenverlust:** Wenn du die "Browserdaten löschst", ist die Musik weg! Nutze regelmäßig die **Backup-Funktion** in den Einstellungen.

## 👨‍💻 Credits
Entwickelt von Sebastian Rößer.
Ein Open-Source Projekt für Eltern, die die Kontrolle über ihre Audiodaten behalten wollen.
