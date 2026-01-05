# 🎵 KlangKiste PWA (v67 Stable)

**Die smarte DIY "Toniebox" fürs Handy – 100% AI-Generated Code.**

Dieses Projekt ist eine kinderfreundliche Musik-Player-App, die alte Smartphones in sichere, werbefreie Abspielgeräte verwandelt. Sie läuft als **Progressive Web App (PWA)** komplett offline im Browser.

> 🤖 **Made with Gemini:** Dieses gesamte Projekt (HTML, CSS, JavaScript Logik, Datenbank-Struktur) wurde vollständig durch **Google Gemini 3 Pro** erstellt und analysiert. Es ist ein Experiment, wie weit KI-gestützte Entwicklung ohne manuelles Coden gehen kann.

---

## ✨ Neue Funktionen in v67

* 💾 **Auto-Save & Smart Resume:** Die App speichert nun **alle 5 Sekunden** automatisch den Fortschritt. Wird die App versehentlich geschlossen oder stürzt ab, öffnet sie beim nächsten Start sofort das letzte Hörspiel an der exakten Stelle.
* ⚡ **Performance-Boost (Admin):**
    * **Kein Flackern mehr:** Die Liste der gespeicherten Tags lädt nun butterweich.
    * **Sofort-Aktion:** Das Verstecken/Anzeigen von Hörbüchern (Auge-Icon) passiert nun verzögerungsfrei.
    * **Auto-Scroll:** Ein Klick auf den Stift (Bearbeiten) scrollt nun zuverlässig und weich zum Eingabeformular hoch.
* 🖥️ **Vollbild-Logik:** Der Kinder-Modus aktiviert den Vollbildmodus nun zuverlässiger (auch auf iOS), sobald der Bildschirm das erste Mal berührt wird.
* ⚙️ **Optimierte Standards:** Für neue Nutzer sind "Bunte Knöpfe", "Display anlassen" und "Eco-Modus" nun standardmäßig aktiviert.
* 🎨 **Design:** Verbesserte Lesbarkeit der "Versteckt"-Badges (weißer Hintergrund) und Hinweistexte bei Massen-Aktionen.

---

## 📸 Vorschau

Die App ist in zwei Bereiche unterteilt: Den geschützten **Eltern-Modus** (Verwaltung) und den kindersicheren **Player-Modus**.

### 👶 Kinder-Modus & Bibliothek

Hier spielen die Kinder. Große Bilder, keine Text-Menüs, einfache Bedienung.

| **Der Player (Neu: Rewind)** | **Die Bibliothek** |
|:---:|:---:|
| <img src="docs/screenshots/kid-mode1.png" width="200"> | <img src="docs/screenshots/library_grid.png" width="200"> |
| *Große Steuerung & Cover* | *Visuelles Stöbern & Filtern* |

| **Info-Overlay** | **Details & Dauer** |
|:---:|:---:|
| <img src="docs/screenshots/library_info.png" width="200"> | <img src="docs/screenshots/kid-mode2.png" width="200"> |
| *Beschreibung & Alter* | *Einfacher Player* |

### 🔧 Eltern-Modus & Statistik

Verwaltung der Inhalte und Einsicht in das Nutzungsverhalten.

| **Verwaltung** | **Statistik (Neu)** |
|:---:|:---:|
| <img src="docs/screenshots/parent-mode.png" width="200"> | <img src="docs/screenshots/stats_view.png" width="200"> |
| *Tags anlernen & Import* | *Hörverhalten & Fortschritt (✅)* |

---

# 📲 Installation (Android)

Die App muss nicht über den Play Store geladen werden, sondern wird direkt über den Browser installiert.

1. Öffne **Chrome** auf deinem Android-Smartphone.
2. Rufe die Webseite auf: **https://basecore.github.io/klangkiste/**
3. **Warte kurz (bis zu 30 Sekunden):** Oft erscheint am unteren Bildschirmrand automatisch ein Hinweis „KlangKiste zum Startbildschirm hinzufügen".
4. Falls nicht, folge diesen Schritten:

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

## 📖 Bedienung

### 1. Musik hinzufügen

Die App unterstützt mehrere Wege:

* **A) Online-Beispiele (Neu):**
    Lade mit einem Klick vorbereitete KI-generierte Hörspiele direkt vom Server (siehe unten).
* **B) Massen-Import (Empfohlen):**
    Erstelle Ordner mit MP3s und Covern am PC und lade sie über „Massen-Import" hoch. **Tipp:** Wenn du unser Python-Tool (siehe unten) mit den TAF-Dateien nutzt, wird eine `klangkiste.json` erstellt. Wähle diese Datei und den Ordner aus – dann sind alle Titel, Cover und Texte sofort perfekt gesetzt!
* **C) Manuell anlernen:**
    Gehe auf „Neuen Tag anlernen", wähle Audio & Bild und fülle im Menü **„📝 Erweiterte Infos"** Details wie Beschreibung und Alter aus.

### 2. NFC Tags nutzen (Optional)

Wenn dein Android-Gerät NFC hat:
1. Gehe auf „Tag scannen & speichern".
2. Halte eine NFC-Karte oder Figur an das Handy.
3. Die Musik ist nun mit diesem Tag verknüpft. Im Kinder-Modus startet sie sofort beim Auflegen.

### 3. Statistik ansehen

Klicke im Eltern-Modus oben rechts auf den Button **„📊 Statistik"**. Hier siehst du, was dein Kind wann und wie lange hört und welche Hörspiele bereits **vollständig (✅)** gehört wurden.

### 4. Kinder-Modus verlassen

Es gibt keinen sichtbaren „Zurück"-Button, damit Kinder die App nicht versehentlich schließen.
➡️ **Tippe 5× schnell hintereinander in die obere rechte Ecke des Bildschirms, um in den Eltern-Modus zurückzukehren.**

---

## 🚀 Schnellstart mit Beispielen

Du möchtest die App sofort testen? Wir haben Beispiel-Hörspiele vorbereitet (inkl. Cover & Metadaten).

### ⚡ Methode 1: Direkt in der App laden (Empfohlen)

Du musst nichts manuell herunterladen! Die App holt sich die Dateien direkt vom Server.

1. Öffne den Bereich **„📂 Datenbank“** im Eltern-Modus.
2. Klicke auf den blauen Button **„☁️ Beispiele direkt laden (Online)“**.
3. Bestätige den Download. Fertig! 🎉

<img src="docs/screenshots/import-online.png" width="400" alt="Screenshot des Online Import Buttons">

> **⚠️ Hinweis zu den Beispielen:** > Die enthaltenen Hörbücher wurden testweise mit der **KI Suno 4.5** generiert. Sie dienen rein zu Testzwecken der App-Funktionen.  
> **Bitte beachten:** Die Geschichten, Betonung und Aussprache sind experimentell ("KI-generiert") und entsprechen qualitativ nicht echten, professionellen Hörbüchern.

### 📥 Methode 2: Manuell herunterladen (für Offline-Installationen)

Falls du die Dateien lieber selbst auf dem Handy haben möchtest:

1. Gehe auf https://github.com/basecore/klangkiste
2. Klicke auf den grünen **„Code"**-Button -> **„Download ZIP"**
3. Entpacke die Datei.
4. Gehe in der App auf **„📂 Massen-Import"**.
5. Wähle im Ordner `example/` die Datei `klangkiste.json` und die MP3/PNG Dateien aus.

### Was ist in den Beispielen enthalten?

| Titel | Genre | Alter | Laufzeit |
|-------|-------|-------|----------|
| Die drei Schneeflocken der Freundschaft – Das Hörspiel | Hörspiel | 4+ | 5 Min |
| Schneeflocken – Das Lied | Musik | 3+ | 4 Min |
| Wusel in der Werkstatt | Hörspiel | 4+ | 1 Min |

Die `klangkiste.json` definiert alle Metadaten: Seriennamen, Episodentitel, ausführliche Beschreibungen, Genre, Altersempfehlung, Sprache und passende Tags (Freundschaft, Winter, Abenteuer, Humor).

---

## 🪄 Das Python-Tool: TAF zu KlangKiste

Hast du **eigene Tonie-Dateien (.taf)**? Du kannst diese mit dem beiliegenden Skript `taf_klangkiste_final.py` (im Ordner `tools/`) vollautomatisch für die App konvertieren.

**Das Script erledigt alles:**
1. Wandelt `.taf` (Tonie-Format) in `.mp3` um (inkl. Kapitelmarken in einer `.cue` Datei).
2. Lädt das **Original-Cover** herunter.
3. Holt **Metadaten** (Beschreibungstext, Altersempfehlung, Genre) von der Tonie-Website.
4. Erstellt eine perfekte `klangkiste.json` für den Import.

### Anleitung für PC/Mac

1. **Vorbereitung:**
    * Installiere [Python](https://www.python.org/)
    * Installiere [FFmpeg](https://ffmpeg.org/) (muss im System-Pfad sein)

2. **Dateien ablegen:**
    * Kopiere das Script `taf_klangkiste_final.py` und deine `.taf`-Dateien in einen gemeinsamen Ordner

3. **Abhängigkeiten installieren:**
    Öffne ein Terminal in dem Ordner und führe aus:
    ```
    pip install requests beautifulsoup4 playwright
    playwright install
    ```

4. **Script starten:**
    ```
    python taf_klangkiste_final.py
    ```

5. **Ergebnis:**
    Es entsteht ein Ordner `klangkiste_output`. Diesen Ordner kannst du nun direkt über **„📂 Massen-Import"** in die App laden!

---

## 📂 Dateistruktur

* `index.html` – Der gesamte Quellcode der Anwendung (Logik & Design, v67)
* `sw.js` – Der Service Worker für die Offline-Funktionalität (Cache v66)
* `manifest.json` – Konfiguration für das App-Icon und den Vollbild-Modus
* `assets/` – Ordner für Icons und Test-Sounds
* `example/` – Beispieldateien (MP3s, PNGs, `klangkiste.json`) für schnellen Start
* `tools/` – Enthält das Python-Script für den Import von Tonie-Dateien
* `docs/screenshots/` – Screenshots für diese Anleitung

---

## 🔗 Projekt & Support

* 🏠 **Projekt:** https://github.com/basecore/klangkiste
* 🐛 **Fehler melden:** https://github.com/basecore/klangkiste/issues

## 👨‍💻 Credits

Entwickelt von Sebastian Rößer mit Unterstützung von **Google Gemini 3 Pro**.  
Version 67 „Auto-Save Edition".
