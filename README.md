# 🎵 Jukebox NFC - Die DIY Toniebox-Alternative "To Go"

Willkommen bei der **Jukebox NFC**! Dies ist eine webbasierte, kinderfreundliche Musik-App, die dein Android-Smartphone in einen NFC-gesteuerten Hörspiel-Player verwandelt.

Perfekt für den Urlaub, die Autofahrt oder einfach als günstige und flexible Alternative zur Toniebox – gesteuert über normale NFC-Tags oder Sticker.

## ✨ Was ist das? ("Vibe Coding" Story)

Dieses Projekt ist ein Experiment in **"Vibe Coding"**.
Ich habe **keine einzige Zeile Code selbst geschrieben**. Die gesamte App – von der NFC-Logik über das Design bis hin zur Datenbank – wurde vollständig durch Dialoge mit **Google Gemini (Model 2.0 Flash)** erstellt.

Es ist der Beweis, dass man mit der richtigen Idee und einer starken KI funktionierende, nützliche Software bauen kann, ohne selbst programmieren zu müssen.

## ⚠️ WICHTIGE HINWEISE (Bitte zuerst lesen!)

Bevor du startest, beachte bitte diese zwei technischen Einschränkungen:

1.  **❌ Keine Original Tonie-Figuren:**
    Diese App funktioniert **NICHT** mit originalen Tonie-Figuren. Die Chips in den Tonies sind verschlüsselt und können von normalen Smartphones nicht korrekt als eindeutige ID ausgelesen werden.
    *Lösung:* Nutze günstige **NTAG213 oder NTAG215** Sticker/Karten (Cent-Artikel bei Amazon/eBay) und klebe sie unter eigene Figuren oder auf Karten.

2.  **❌ Kein automatischer Stopp beim Wegnehmen:**
    Die Funktion "Musik stopp, wenn Figur weg" (wie bei der echten Box) ist technisch im Browser leider unzuverlässig. Web-Browser auf Handys erlauben kein dauerhaftes, energiesparendes Scannen im Millisekundentakt.
    *Lösung:* Die App hat große, kinderleichte "Pause"- und "Stopp"-Buttons.

## 🚀 Features

* **100% Kostenlos & Werbefrei:** Läuft direkt im Browser.
* **Offline-Fähig (PWA):** Kann als "App" auf dem Startbildschirm installiert werden und funktioniert danach auch ohne Internet (sofern die Audio-Dateien im Cache sind oder lokal verwaltet werden).
* **Kinder-Modus:** Große Buttons, gesperrtes Menü, keine Gefahr, etwas zu löschen.
* **Playlist-Support:** Unterstützt Hörbücher mit vielen Kapiteln (CD 1, CD 2...). Die App spielt sie nacheinander ab.
* **Merk-Funktion:** Die App merkt sich pro Figur exakt, wo das Kind aufgehört hat (z.B. Track 5, Minute 3:12).
* **Smart Backup:** Exportiere deine Datenbank. Beim Handywechsel kannst du deine MP3-Sammlung einfach neu auswählen, und die App verknüpft alles automatisch wieder (Smart Repair).

## 🛠️ Installation & Nutzung

### Voraussetzungen
* Ein **Android Smartphone** mit NFC.
* Der **Chrome Browser** (oder ein Chromium-basierter Browser).
* Eigene MP3-Dateien deiner Hörspiele.
* Leere NFC-Tags (NTAG213/215).

### Schritt 1: App Installieren
1.  Öffne die Webseite auf deinem Handy: `https://basecore.github.io/jukebox/` (bzw. dein Link).
2.  Tippe oben rechts auf das Menü (3 Punkte).
3.  Wähle **"App installieren"** oder **"Zum Startbildschirm zufügen"**.
4.  Starte die App nun über das neue Icon auf deinem Homescreen (sie startet im Vollbild).

### Schritt 2: Eltern-Modus (Einrichten)
1.  Du landest im Eltern-Menü.
2.  Wähle unter "Neuen Tag anlernen" deine **Audio-Dateien** aus.
3.  Wähle optional ein **Cover-Bild**.
4.  Gib dem Ganzen einen **Namen** (z.B. "Benjamin Blümchen").
5.  Klicke auf **"Tag scannen & speichern"**.
6.  Halte deinen leeren NFC-Tag an die Rückseite des Handys.
7.  *Ping!* Fertig.

### Schritt 3: Kinder-Modus
1.  Klicke oben auf den großen grünen Button **"▶ ZUM KINDER-MODUS"**.
2.  Übergib das Handy dem Kind.
3.  Sobald ein angelernter Tag an das Handy gehalten wird, beginnt die Musik zu spielen!

*Um zurück in den Eltern-Modus zu kommen: Tippe **5x schnell** in die obere rechte Ecke des Bildschirms.*

## 🔒 Datenschutz
Alles passiert **lokal auf deinem Gerät**.
* Die Datenbank (IndexedDB) liegt in deinem Browser-Speicher.
* Es werden keine MP3s auf fremde Server hochgeladen.
* Es gibt kein Tracking.

---

*Viel Spaß mit deiner DIY Jukebox!*
*Created by **Sebastian Rößer** with the help of **Google Gemini**.*
