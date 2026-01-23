# 🎵 KlangKiste PWA (V77 SD-Card Link Edition)

**Die smarte DIY "Toniebox" fürs Handy – Jetzt mit SD-Karten Streaming!**

Dieses Projekt ist eine kinderfreundliche Musik-Player-App, die alte Smartphones in sichere, werbefreie Abspielgeräte verwandelt. Sie läuft als **Progressive Web App (PWA)** komplett offline im Browser.

> 🤖 **Made with Gemini:** Dieses gesamte Projekt (HTML, CSS, JavaScript Logik, Datenbank-Struktur) wurde vollständig durch **Google Gemini 3 Pro** erstellt und analysiert. Es ist ein Experiment, wie weit KI-gestützte Entwicklung ohne manuelles Coden gehen kann.

---

## ✨ Neu in v77: Der SD-Card Link (Speicher-Retter)

Das größte Problem von Web-Apps auf Android wurde gelöst: **Der Speicherplatz.**
Bisher wurden alle Hörbücher in den internen Browser-Speicher *kopiert*. Bei großen Sammlungen (z.B. 10 GB auf der SD-Karte) war der interne Speicher schnell voll und der Import brach ab.

### 🔗 SD-Karte / Ordner verknüpfen (File System Access API)
Anstatt Dateien zu kopieren, bittet die App nun um Erlaubnis, direkt auf den Ordner zugreifen zu dürfen.
* **Null Speicherverbrauch:** Die MP3s bleiben auf der SD-Karte. Die App speichert in ihrer Datenbank nur einen "Wegweiser" (Link).
* **Blitzschnell:** Da keine Daten kopiert werden müssen, sind 100 Hörbücher in wenigen Sekunden importiert.
* **Voraussetzung:** Benötigt einen modernen Browser (Empfohlen: **Google Chrome** auf Android).

---

## 🚀 Wichtige Funktionen aus v76

### 📂 Smart Folder Erkennung
Die App erkennt automatisch Ordnerstrukturen.
* `Hörspiele/Benjamin Blümchen/01.mp3` -> Wird automatisch Album "Benjamin Blümchen".
* Bilder im Ordner werden automatisch als Cover erkannt.

### ⚡ Admin Listen-Ansicht
Für Eltern mit großen Sammlungen (500+ Alben) gibt es im Admin-Bereich nun eine umschaltbare Listen-Ansicht für maximale Performance auf alten Geräten.

---

## 📸 Vorschau

Die App ist in zwei Bereiche unterteilt: Den geschützten **Eltern-Modus** (Verwaltung) und den kindersicheren **Player-Modus**.

### 👶 Kinder-Modus & Bibliothek

Hier spielen die Kinder. Große Bilder, keine Text-Menüs, einfache Bedienung.

| **Der Player** | **Die Bibliothek** |
|:---:|:---:|
| <img src="docs/screenshots/kid-mode1.png" width="200"> | <img src="docs/screenshots/library_grid.png" width="200"> |
| *Große Steuerung & Cover* | *Visuelles Stöbern & Filtern* |

| **Info-Overlay** | **Details & Dauer** |
|:---:|:---:|
| <img src="docs/screenshots/library_info.png" width="200"> | <img src="docs/screenshots/kid-mode2.png" width="200"> |
| *Beschreibung & Alter* | *Einfacher Player* |

### 🔧 Eltern-Modus & Statistik

Verwaltung der Inhalte und Einsicht in das Nutzungsverhalten.

| **Verwaltung** | **Statistik** |
|:---:|:---:|
| <img src="docs/screenshots/parent-mode.png" width="200"> | <img src="docs/screenshots/stats_view.png" width="200"> |
| *Smart Folder & Tags* | *Timeline & Fortschritt (✅)* |

---

## 🌍 Direkt im Browser nutzen (Ohne Installation)

Du musst die App nicht zwingend installieren. Du kannst sie auch einfach direkt als Webseite verwenden:

👉 **[https://basecore.github.io/klangkiste/](https://basecore.github.io/klangkiste/)**

**Hinweis:** Die App funktioniert auch so vollumfänglich und speichert deine Datenbank im Browser. Deine Daten bleiben erhalten, **solange du deine Browser-Daten (Cache/Webseitendaten) nicht löschst**.

---

# 📲 Installation (Android)

Die App muss nicht über den Play Store geladen werden, sondern wird direkt über den Browser installiert.

1.  Öffne **Chrome** auf deinem Android-Smartphone.
2.  Rufe die Webseite auf: **https://basecore.github.io/klangkiste/**
3.  **Warte kurz (bis zu 30 Sekunden):** Oft erscheint am unteren Bildschirmrand automatisch ein Hinweis „KlangKiste zum Startbildschirm hinzufügen".
4.  Falls nicht, folge diesen Schritten:

| **1. Menü öffnen** | **2. Installieren** |
|:---:|:---:|
| <img src="docs/screenshots/install-app1.png" width="200"> | <img src="docs/screenshots/install-app2.png" width="200"> |
| *Tippe oben rechts auf die 3 Punkte* | *Wähle „App installieren"* |

| **3. Bestätigen** | **4. Widget platzieren** |
|:---:|:---:|
| <img src="docs/screenshots/install-app3.png" width="200"> | <img src="docs/screenshots/install-app4.png" width="200"> |
| *Klicke auf „Installieren"* | *Automatisch oder ziehen* |

*(iOS Nutzer verwenden Safari → Teilen → Zum Home-Bildschirm)*

---

## 📖 Bedienung & Musik hinzufügen

### 1. Musik importieren (Empfohlener Weg)

* **A) 🔗 SD-Karte / Ordner verknüpfen (Neu in V77):**
    Dies ist die beste Methode für große Sammlungen auf SD-Karten. Die Dateien werden **nicht kopiert**, sondern direkt gestreamt.
    * Wähle deinen "Hörspiele"-Ordner auf der SD-Karte.
    * Chrome fragt um Erlaubnis -> Bestätigen.
    * Fertig! Gigabytes an Musik in Sekunden verfügbar.

### 2. Alternative Import-Wege (Klassisch)

* **B) Ordner-Struktur Import (Kopieren):**
    Wie Methode A, aber die Dateien werden physisch in den internen Speicher der App kopiert. Gut für kleine Sammlungen, wenn die SD-Karte oft gewechselt wird.
* **C) Massen-Import (Dateien):**
    Für lose MP3s oder wenn du unser Python-Tool nutzt (`klangkiste.json`). Kopiert Dateien in den App-Speicher.
* **D) Manuell anlernen:**
    Gehe auf „Neuen Tag anlernen", wähle Audio & Bild einzeln und fülle Details wie Beschreibung und Alter aus.

### 3. Backups & Restore

* **Sichern:** Klicke auf **"Datenbank exportieren"**. Dies speichert eine Datei (`klangkiste_full_backup_DATUM.json`), die all deine Fortschritte, Einstellungen und Statistiken enthält.
* **Wiederherstellen:** Lade diese Datei über **"Datenbank laden"**. Wenn du Methode A (Verknüpfung) genutzt hast, musst du danach eventuell den Ordnerpfad einmal neu bestätigen.

### 4. NFC Tags nutzen (Optional)

Wenn dein Android-Gerät NFC hat:
1.  Gehe auf „Tag scannen & speichern".
2.  Halte eine NFC-Karte oder Figur an das Handy.
3.  Die Musik ist nun mit diesem Tag verknüpft. Im Kinder-Modus startet sie sofort beim Auflegen.

### 5. Kinder-Modus verlassen

Es gibt keinen sichtbaren „Zurück"-Button, damit Kinder die App nicht versehentlich schließen.
➡️ **Tippe 5× schnell hintereinander in die obere rechte Ecke des Bildschirms, um in den Eltern-Modus zurückzukehren.**

---

## 🚀 Schnellstart mit Beispielen

Du möchtest die App sofort testen? Wir haben Beispiel-Hörspiele vorbereitet.

### ⚡ Methode 1: Direkt in der App laden
1.  Öffne den Bereich **„📂 Datenbank“** im Eltern-Modus.
2.  Klicke auf den blauen Button **„☁️ Beispiele direkt laden (Online)“**.
3.  Bestätige den Download. Fertig!

<img src="docs/screenshots/import-online.png" width="400" alt="Screenshot des Online Import Buttons">

> **⚠️ Hinweis zu den Beispielen:** Die enthaltenen Hörbücher wurden testweise mit der **KI Suno 4.5** generiert. Sie dienen rein zu Testzwecken.

---

## 🪄 Das Python-Tool: TAF zu KlangKiste

Hast du **eigene Tonie-Dateien (.taf)**? Du kannst diese mit dem beiliegenden Skript `taf_klangkiste_final.py` (im Ordner `tools/`) vollautomatisch für die App konvertieren.

**Das Script erledigt alles:**
1.  Wandelt `.taf` (Tonie-Format) in `.mp3` um (inkl. Kapitelmarken in einer `.cue` Datei).
2.  Lädt das **Original-Cover** herunter.
3.  Holt **Metadaten** (Beschreibungstext, Altersempfehlung, Genre) von der Tonie-Website.
4.  Erstellt eine perfekte `klangkiste.json` für den Import.

### Anleitung für PC/Mac

1.  **Vorbereitung:**
    * Installiere [Python](https://www.python.org/)
    * Installiere [FFmpeg](https://ffmpeg.org/) (muss im System-Pfad sein)

2.  **Dateien ablegen:**
    * Kopiere das Script `taf_klangkiste_final.py` und deine `.taf`-Dateien in einen gemeinsamen Ordner

3.  **Abhängigkeiten installieren:**
    Öffne ein Terminal in dem Ordner und führe aus:
    ```bash
    pip install requests beautifulsoup4 playwright
    playwright install
    ```

4.  **Script starten:**
    ```bash
    python taf_klangkiste_final.py
    ```

5.  **Ergebnis:**
    Es entsteht ein Ordner `klangkiste_output`. Diesen Ordner kannst du nun direkt über **„📂 Massen-Import"** in die App laden!

---

## 📂 Dateistruktur

* `index.html` – Der gesamte Quellcode der Anwendung (Logik & Design, v77)
* `sw.js` – Der Service Worker für die Offline-Funktionalität
* `manifest.json` – Konfiguration für das App-Icon und den Vollbild-Modus
* `assets/` – Ordner für Icons und Test-Sounds
* `example/` – Beispieldateien (MP3s, PNGs, `klangkiste.json`) für schnellen Start
* `tools/` – Enthält das Python-Script für den Import von Tonie-Dateien
* `docs/screenshots/` – Screenshots für diese Anleitung

---

## 📟 Hardware: Der ESP32 Unlocker

Du möchtest **Tonie-Figuren einfach entsperren** ohne die "Klopf-Methode" anwenden zu müssen oder die **exakte UID auslesen**, um sie in der App zu nutzen?
Wir haben ein DIY-Diagnose-Tool auf Basis eines ESP32 und PN5180 entwickelt.

👉 **[Hier geht es zur Hardware-Dokumentation & Bauanleitung](hardware/esp32_unlocker/README.md)**

* **Funktionen:** Privacy Mode deaktivieren, Audio-ID auslesen, Chip-Diagnose.
* **Kosten:** < 15€
* **Kein Bluetooth nötig:** Arbeitet als Standalone-Tool.

---

## 🔗 Projekt & Support

* 🏠 **Projekt:** https://github.com/basecore/klangkiste
* 🐛 **Fehler melden:** https://github.com/basecore/klangkiste/issues

## 👨‍💻 Credits

Entwickelt von Sebastian Rößer mit Unterstützung von **Google Gemini 3 Pro**.
Version 77 „SD-Card Link Edition".
