# 🎵 Klangkiste (v69 - Performance Edition)

Ein offline Hörbuch-Player für Kinder, der komplett im Browser läuft. Keine Cloud, kein Tracking, keine Werbung. Ideal für alte Smartphones (Upcycling), die als "Toniebox-Alternative" genutzt werden sollen.

**Version:** v69
**Update-Fokus:** Stabilität für große Bibliotheken (>100 Hörbücher) und ältere Geräte (z.B. Galaxy S8+).

---

## ✨ Neue Features in v69

Diese Version wurde massiv optimiert, um Abstürze (Memory Leaks) bei vielen Cover-Bildern zu verhindern.

### 🚀 1. Performance & Stabilität
* **Standard Listen-Ansicht:** Der Admin-Bereich startet jetzt standardmäßig in einer reinen Text-Liste. Cover-Bilder werden nicht geladen, um den Arbeitsspeicher (RAM) zu schonen.
* **Ansicht umschaltbar:** Du kannst im Admin-Bereich jederzeit zwischen "📋 Liste" (schnell) und "🖼️ Raster" (mit Bildern) wechseln.
* **Asynchrones Laden:** Wenn Bilder angezeigt werden, nutzen sie `decoding="async"`, damit das Scrollen nicht ruckelt.

### 🛡️ 2. Sicherheits-Sperre (Locking)
* **Keine "Race Conditions" mehr:** Wenn die Datenbank arbeitet (z.B. beim Speichern oder Massen-Verstecken), wird die Oberfläche gesperrt.
* **Visuelles Feedback:** Ein Status-Text am unteren Rand zeigt genau an, was passiert ("Verarbeite Eintrag 5 von 100...").
* **Verhinderter Absturz:** Buttons werden grau/inaktiv, damit man nicht versehentlich Aktionen doppelt auslöst oder den Modus wechselt, während im Hintergrund geschrieben wird.

### ⚡ 3. Optimierte Massen-Steuerung
* **"Alle verstecken / Alle anzeigen":** Diese Funktion lädt die Seite nicht mehr neu. Stattdessen werden nur die kleinen Symbole (Auge/Verbotszeichen) live ausgetauscht. Das verhindert, dass der Browser bei >100 Einträgen einfriert.

---

## 🛠️ Installation

Die Klangkiste ist eine **Single-File-Application**. Es ist keine Installation nötig.

1.  Lade die Datei `index.html` auf dein Android-Gerät.
2.  Öffne die Datei mit **Google Chrome** oder **Samsung Internet**.
3.  Öffne das Browser-Menü und wähle **"Zum Startbildschirm hinzufügen"**.
4.  Starte die App nun über das neue Icon auf dem Homescreen (sie läuft jetzt im Vollbild-Modus).

---

## 📖 Bedienung

### Admin-Modus (Eltern)
Hier verwaltest du die Hörbücher.

* **Hinzufügen:** Wähle MP3-Dateien und (optional) ein Cover-Bild. Gib einen Namen und eine ID (für NFC) ein.
* **Bibliothek (Gespeicherte Tags):**
    * Nutze die **Listenansicht**, um schnell zu löschen oder die Sichtbarkeit zu ändern.
    * Nutze die **Massen-Steuerung**, um z.B. alle Weihnachtslieder auf einmal zu verstecken.
* **Backup:** Du kannst die Datenbank (Metadaten) als JSON exportieren und wieder importieren. *(Hinweis: Audio-Dateien werden aus Browser-Sicherheitsgründen oft nicht im JSON-Export unterstützt, nur die Texte/Einstellungen).*

### Kinder-Modus
Dies ist die sichere Umgebung für das Kind.

* Es werden nur Hörbücher angezeigt, die **nicht versteckt** sind.
* **Bedienung:** Großes Cover anklicken = Abspielen.
* **Player:** Einfache Steuerung (Start/Stop, Vor/Zurück).
* **Schutz:** Um den Kinder-Modus zu verlassen, muss man in die obere rechte Ecke (unsichtbarer Button) klicken oder lange drücken und die **PIN** eingeben.

---

## ⚙️ Technische Hinweise

* **Datenbank:** Nutzt `IndexedDB` im Browser. Daten bleiben auch beim Schließen des Tabs erhalten.
* **Speicherplatz:** Hängt vom freien Speicher deines Geräts ab. Der Browser kann mehrere Gigabyte verwalten.
* **Reset:** Falls gar nichts mehr geht: Einstellungen -> "Datenbank löschen" setzt die App komplett zurück.

---

## 📝 Changelog History

### v69 (Aktuell)
* [Fix] Massen-Steuerung ("Alle verstecken") stürzt nicht mehr ab (DOM-Update statt Reload).
* [Feature] Sicherheits-Variable `isProcessingDatabase` eingeführt, um parallele Zugriffe zu blockieren.
* [Feature] Umschalter für Listen- vs. Rasteransicht im Admin-Bereich.
* [Tweak] Bilder werden im Admin-Bereich standardmäßig ausgeblendet (RAM-Schutz).

### v68 und älter
* Grundfunktionen: Audio-Player, NFC-Feld, Cover-Upload.
* Einführung des PIN-Schutzes.
* Einführung der "Verstecken"-Funktion.
