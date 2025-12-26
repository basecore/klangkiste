# 🎵 Jukebox PWA (v62 Stats)

**Die smarte DIY "Toniebox" fürs Handy – 100% AI-Generated Code.**

Dieses Projekt ist eine kinderfreundliche Musik-Player-App, die alte Smartphones in sichere, werbefreie Abspielgeräte verwandelt. Sie läuft als **Progressive Web App (PWA)** komplett offline im Browser.

> 🤖 **Made with Gemini:** Dieses gesamte Projekt (HTML, CSS, JavaScript Logik, Datenbank-Struktur) wurde vollständig durch **Google Gemini 3 Pro** erstellt und analysiert. Es ist ein Experiment, wie weit KI-gestützte Entwicklung ohne manuelles Coden gehen kann.

---

## ✨ Neue Funktionen in v62

* 📊 **Detaillierte Eltern-Statistik:** Ein neues Dashboard zeigt genau an:
    * Hördauer (Heute / Woche / Gesamt).
    * Die Top 5 Lieblings-Hörspiele.
    * Tageszeit-Heatmap (Wann wird gehört?).
    * Anzahl der Interaktionen (NFC-Scans, Umdrehen).
* 🛠️ **Bugfixes:**
    * Das seitliche "Wackeln" des Bildschirms im Kinder-Modus wurde behoben.
    * Lange Dateinamen im Editor werden nun korrekt umgebrochen.
* 💾 **Datenbank Upgrade:** Automatische Migration auf DB-Version 2 für das Event-Logging.

---

## 📸 Screenshots

### 👶 Der Kinder-Modus
Große Bilder, keine komplizierten Menüs. Die Steuerung ist kindersicher.

| **Der Player** | **Die Bibliothek** |
|:---:|:---:|
| <img src="docs/screenshots/kid-mode1.png" width="180"> | <img src="docs/screenshots/library_grid.png" width="180"> |
| *Große Tasten & Cover* | *Visuelles Stöbern* |

### 🔧 Der Eltern-Modus
Nur durch einen Trick ("Secret Knock") erreichbar. Hier verwaltest du Inhalte und prüfst die Nutzung.

| **Verwaltung** | **Statistik (Neu)** |
|:---:|:---:|
| <img src="docs/screenshots/parent-mode.png" width="180"> | <img src="docs/screenshots/stats_view.png" width="180"> |
| *Tags anlernen & Import* | *Hörverhalten analysieren* |

---

## 🚀 Installation

Da es eine PWA ist, gibt es keinen App-Store-Download. Die App läuft lokal auf deinem Gerät.

1.  **Hosting:** Lade die Dateien (`index.html`, `sw.js`, `manifest.json`, `assets/`) auf einen Webspace (https erforderlich) oder starte einen lokalen Server.
2.  **Öffnen:** Rufe die URL im **Chrome (Android)** oder **Safari (iOS)** auf.
3.  **Installieren:**
    * **Android:** Tippe auf das Menü (3 Punkte) -> "Zum Startbildschirm hinzufügen" (oder "App installieren").
    * **iOS:** Tippe auf "Teilen" -> "Zum Home-Bildschirm".
4.  **Starten:** Öffne die neue App auf dem Homescreen. Sie läuft nun im Vollbild ohne Browser-Leiste.

---

## 📖 Bedienung

### 1. Musik importieren
* **Massen-Import (Empfohlen):** Klicke auf "📂 Massen-Import" und wähle einen Ordner mit Unterordnern (MP3s + Bilder) aus. Die App erkennt Zusammenhänge automatisch.
* **Einzeln:** Nutze "🎵 Tag bearbeiten", lade eine Audio-Datei und ein Bild hoch.

### 2. NFC Tags nutzen (Optional)
Wenn dein Android-Gerät NFC hat:
1.  Gehe auf "Tag scannen & speichern".
2.  Halte eine NFC-Karte oder Figur an das Handy.
3.  Die Musik ist nun mit diesem Tag verknüpft. Im Kinder-Modus startet sie sofort beim Auflegen.

### 3. Statistik ansehen
Klicke im Eltern-Modus oben rechts auf den Button **"📊 Statistik"**. Hier siehst du, was dein Kind wann und wie lange hört.

### 4. Kinder-Modus verlassen
Es gibt keinen sichtbaren "Zurück"-Button, damit Kinder die App nicht versehentlich schließen.
➡️ **Tippe 5x schnell hintereinander in die obere rechte Ecke des Bildschirms, um das Passwort-Feld zu umgehen und zum Eltern-Modus zurückzukehren.**

---

## 📂 Dateistruktur

* `index.html` - Der gesamte Quellcode der Anwendung (Logik & Design).
* `sw.js` - Der Service Worker für die Offline-Funktionalität.
* `manifest.json` - Konfiguration für das App-Icon und den Vollbild-Modus.
* `assets/` - Ordner für Icons und Test-Sounds.

---

## 🔒 Datenschutz & Sicherheit

* **Lokal:** Alle Daten (Datenbank, Bilder, Statistiken) werden in der `IndexedDB` deines Browsers gespeichert. Nichts wird in eine Cloud hochgeladen.
* **Offline:** Nach dem ersten Laden funktioniert die App komplett ohne Internet.
* **WakeLock:** Die App verhindert, dass das Display ausgeht, während ein Hörspiel läuft.

---

**Projekt erstellt mit Google Gemini 3 Pro.**
