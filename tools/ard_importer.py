import sys
import subprocess
import importlib.util
import os
import time
import json
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from io import BytesIO
import webbrowser


# --- 1. AUTOMATISCHE INSTALLATION ---
def install_and_import(package, import_name):
    if importlib.util.find_spec(import_name) is None:
        print(f"🔧 Installiere: {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            print(f"❌ Fehler: {e}")
            sys.exit(1)


required_packages = [("requests", "requests"), ("Pillow", "PIL"), ("beautifulsoup4", "bs4"), ("urllib3", "urllib3")]
for pkg, imp in required_packages: install_and_import(pkg, imp)

# --- 2. IMPORTS ---
import requests
import urllib3
from PIL import Image, ImageTk, ImageOps
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFIGURATION ---
VERSION = "10.0 (Instant & Square)"
AUTHOR = "KlangKiste ARD Importer"
START_URL = "https://www.ardaudiothek.de/rubrik/fuer-kinder/urn:ard:page:36c12c1321f8895a/"
BASE_DOMAIN = "https://www.ardaudiothek.de"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

COLOR_HEADER = "#003480"
COLOR_BTN = "#004eb3"
COLOR_BG = "#f0f4f8"

LEGAL_TEXT = """=== DISCLAIMER ===
Dies ist ein privates Hilfsprogramm. Keine Verbindung zur ARD.

=== NUTZUNG ===
Nur für private Sicherungskopien (Privatkopie § 53 UrhG).
Kein Verkauf, keine Verbreitung.

Quelle: https://www.ardaudiothek.de/"""


class ARDImporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"📺 {AUTHOR} - v{VERSION}")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLOR_BG)

        self.items_map = {}  # Speichert Details zu IIDs
        self.export_path = os.path.join(os.getcwd(), "klangkiste_ard_content")
        self.stop_scan = False
        self.sort_reverse = False
        self.last_sort_col = ""

        self.setup_ui()
        self.root.after(1000, self.start_scan_thread)

    def setup_ui(self):
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True)

        self.tab_import = tk.Frame(self.nb, bg=COLOR_BG)
        self.nb.add(self.tab_import, text=" 📥 Hörbuch Importer ")

        self.tab_info = tk.Frame(self.nb, bg="white")
        self.nb.add(self.tab_info, text=" ℹ️ Info ")
        self.setup_info_tab()

        header = tk.Frame(self.tab_import, bg=COLOR_HEADER, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="ARD Audiothek Importer", fg="white", bg=COLOR_HEADER, font=("Arial", 24, "bold")).pack()
        tk.Label(header, text=f"Für KlangKiste | v{VERSION} | url1X1 Fix", fg="#cbd5e1", bg=COLOR_HEADER,
                 font=("Arial", 11)).pack()

        tool_frame = tk.Frame(self.tab_import, bg=COLOR_BG, pady=10, padx=20)
        tool_frame.pack(fill="x")

        tk.Button(tool_frame, text="▶ Neu Scannen", command=self.start_scan_thread, bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=5)
        tk.Button(tool_frame, text="⏹ STOPP", command=self.stop_process, bg="#c0392b", fg="white",
                  font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=5)

        tk.Label(tool_frame, text="   Zielordner:", bg=COLOR_BG).pack(side="left", padx=5)
        self.path_entry = tk.Entry(tool_frame, width=50)
        self.path_entry.insert(0, self.export_path)
        self.path_entry.pack(side="left", padx=5)
        tk.Button(tool_frame, text="📂", command=self.choose_path).pack(side="left")

        content = tk.Frame(self.tab_import, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=20, pady=5)

        left_frame = tk.Frame(content, bg="white")
        left_frame.pack(side="left", fill="both", expand=True)

        cols = ('Status', 'Alter', 'Titel', 'Tracks', 'Dauer', 'Quelle')
        self.tree = ttk.Treeview(left_frame, columns=cols, show='headings', selectmode="extended")

        self.tree.heading('Status', text='Status')
        self.tree.heading('Alter', text='👶 Alter')
        self.tree.heading('Titel', text='Titel')
        self.tree.heading('Tracks', text='Tracks')
        self.tree.heading('Dauer', text='Dauer')
        self.tree.heading('Quelle', text='Sammlung')

        self.tree.column('Status', width=100, anchor="center")
        self.tree.column('Alter', width=60, anchor="center")
        self.tree.column('Titel', width=450)
        self.tree.column('Tracks', width=60, anchor="center")
        self.tree.column('Dauer', width=80, anchor="center")
        self.tree.column('Quelle', width=200)

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        sb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        self.preview_panel = tk.Frame(content, bg="white", width=420, bd=1, relief="ridge")
        self.preview_panel.pack(side="right", fill="both", padx=(15, 0))
        self.preview_panel.pack_propagate(False)

        self.prev_img_label = tk.Label(self.preview_panel, bg="white", text="Bitte wählen...")
        self.prev_img_label.pack(pady=20)

        self.details_text = tk.Text(self.preview_panel, bg="white", font=("Arial", 10), relief="flat", wrap="word",
                                    state="disabled", height=20)
        self.details_text.pack(fill="both", expand=True, padx=20, pady=10)

        footer = tk.Frame(self.tab_import, bg=COLOR_BG, pady=15, padx=20)
        footer.pack(fill="x", side="bottom")

        self.status_var = tk.StringVar(value="Bereit.")
        tk.Label(footer, textvariable=self.status_var, bg=COLOR_BG, fg="#555", font=("Arial", 11, "italic")).pack(
            side="left")

        self.btn_download = tk.Button(footer, text="🚀 AUSWAHL HERUNTERLADEN", bg=COLOR_BTN, fg="white",
                                      font=("Arial", 14, "bold"), padx=30, pady=10, command=self.start_download_thread)
        self.btn_download.pack(side="right")

    def setup_info_tab(self):
        container = tk.Frame(self.tab_info, bg="white", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        text_widget = tk.Text(container, font=("Arial", 11), bg="#f9f9f9", relief="flat", wrap="word", height=20)
        text_widget.insert("1.0", LEGAL_TEXT)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)

    def choose_path(self):
        p = filedialog.askdirectory()
        if p:
            self.export_path = p
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, p)

    def stop_process(self):
        self.stop_scan = True
        self.status_var.set("🛑 Vorgang wird angehalten...")

    def sort_tree(self, col, reverse):
        # Einfache Sortierung
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: int(re.sub(r'\D', '', t[0])), reverse=reverse)
        except:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l): self.tree.move(k, '', index)

    def clean_filename(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:100]

    def parse_age(self, text):
        if not text: return 0
        text = text.lower()
        # "ab 4-5 jahren" -> nimmt 4
        match = re.search(r'(?:ab|von|für)\s*(?:kinder)?\s*(?:ab|von)?\s*(\d+)', text)
        if match: return int(match.group(1))
        # "4 jahre" am Anfang
        match = re.search(r'^(\d+)\s+jahr', text)
        if match: return int(match.group(1))
        return 0

    # --- SCAN ENGINE (Queue Based) ---
    def start_scan_thread(self):
        self.stop_scan = False
        self.items_map = {}
        for i in self.tree.get_children(): self.tree.delete(i)
        self.btn_download.config(state="disabled")
        threading.Thread(target=self.scan_logic, daemon=True).start()

    def get_links_from_url(self, url):
        """Liest HTML und extrahiert Links (Audio & Sammlungen)."""
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            text = r.text
            soup = BeautifulSoup(text, 'html.parser')
            page_title = soup.find('h1').get_text().strip() if soup.find('h1') else ""

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']

                # Typ 1: Hörbuch / Sendung / Episode
                if "/sendung/" in href or "/episode/" in href:
                    urn_match = re.search(r'(urn:ard:(?:show|episode):[a-zA-Z0-9]+)', href)
                    if urn_match:
                        urn = urn_match.group(1)
                        title = a.get_text().strip() or "Lade Titel..."
                        links.append({"urn": urn, "href": href, "type": "audio", "title": title})

                # Typ 2: Sammlung / Rubrik
                elif "/sammlung/" in href or "/rubrik/" in href:
                    links.append({"href": href, "type": "collection", "title": a.get_text().strip()})

            return links, page_title
        except:
            return [], ""

    def scan_logic(self):
        self.status_var.set(f"🔍 Scanne Hauptseite...")

        # Wir nutzen ein Set für verarbeitete URNs, um Duplikate zu vermeiden
        processed_urns = set()

        # Liste aller gefundenen Items (noch nicht detailliert)
        # Struktur: { urn: { title, source, age_hint, href } }
        items_todo = {}
        collections_to_scan = []

        # 1. Hauptseite scannen
        links, _ = self.get_links_from_url(START_URL)

        # Sortieren: Audio vs Sammlung
        for l in links:
            if l['type'] == 'audio':
                if l['urn'] not in processed_urns:
                    items_todo[l['urn']] = {"title": l['title'], "source": "Hauptseite", "age": 0, "href": l['href']}
                    processed_urns.add(l['urn'])
            elif l['type'] == 'collection':
                collections_to_scan.append(l)

        # 2. Sammlungen scannen (Ebene 1)
        for col in collections_to_scan:
            if self.stop_scan: break

            full_url = BASE_DOMAIN + col['href'] if col['href'].startswith("/") else col['href']
            self.root.after(0, lambda t=col['title']: self.status_var.set(f"📖 Scanne: {t}..."))

            sub_links, page_title = self.get_links_from_url(full_url)
            inherited_age = self.parse_age(page_title)

            for l in sub_links:
                if l['type'] == 'audio':
                    if l['urn'] not in processed_urns:
                        items_todo[l['urn']] = {"title": l['title'], "source": page_title, "age": inherited_age,
                                                "href": l['href']}
                        processed_urns.add(l['urn'])

        # 3. GUI füllen (SOFORT)
        queue_list = list(items_todo.items())
        total = len(queue_list)
        self.root.after(0, lambda: self.status_var.set(f"💡 {total} Einträge gefunden. Starte Detail-Analyse..."))

        for i, (urn, meta) in enumerate(queue_list):
            if self.stop_scan: break

            iid = urn.split(":")[-1]
            # Platzhalter in GUI
            self.root.after(0, self.add_placeholder_item, iid, meta['title'], meta['source'])

            # Detail Analyse starten
            self.analyze_item(urn, meta, iid, i + 1, total)

            time.sleep(0.01)  # Kurz warten für GUI

        msg = "🛑 Abgebrochen." if self.stop_scan else f"✅ Fertig. {total} Hörbücher geladen."
        self.root.after(0, lambda: self.status_var.set(msg))
        self.root.after(0, lambda: self.btn_download.config(state="normal"))

    def add_placeholder_item(self, iid, title, source):
        if not self.tree.exists(iid):
            self.tree.insert('', 'end', iid=iid, values=("⏳ Lade...", "-", title, "-", "-", source))

    def analyze_item(self, urn, meta, iid, current_idx, total):
        if current_idx % 5 == 0:
            self.root.after(0, lambda: self.status_var.set(f"Analysiere {current_idx}/{total}: {meta['title']}"))

        # URL bauen (Fallback falls meta href unvollständig)
        web_url = BASE_DOMAIN + meta['href'] if meta['href'].startswith("/") else meta['href']

        # Details laden (Mit __NEXT_DATA__ Parsing!)
        data = self.fetch_full_details_html(web_url, urn)

        if data:
            # Alter mergen
            if data['age'] == 0 and meta['age'] > 0: data['age'] = meta['age']
            data['source_label'] = meta['source']

            self.items_map[iid] = data
            self.root.after(0, self.update_tree_item, iid, data)
        else:
            self.root.after(0, lambda: self.tree.set(iid, "Status", "❌ Fehler"))

    def update_tree_item(self, iid, data):
        if self.tree.exists(iid):
            mins = int(data['duration'] / 60)
            age = f"{data['age']}+" if data['age'] > 0 else "-"
            self.tree.set(iid, "Status", "✅ Bereit")
            self.tree.set(iid, "Alter", age)
            self.tree.set(iid, "Titel", data['title'])
            self.tree.set(iid, "Tracks", len(data['tracks']))
            self.tree.set(iid, "Dauer", f"{mins}m")

    # --- HTML PARSER MIT JSON EXTRAKTION ---
    def fetch_full_details_html(self, url, urn):
        """Lädt die Webseite und parst __NEXT_DATA__ JSON."""
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            if r.status_code != 200: return None

            soup = BeautifulSoup(r.text, 'html.parser')

            # JSON Data Block suchen
            script = soup.find('script', id='__NEXT_DATA__')
            if not script: return None

            json_data = json.loads(script.string)

            # Pfad zu den Daten finden (variiert je nach Seitentyp)
            try:
                base = json_data['props']['pageProps']['initialData']['data']
                core = base.get('item') or base.get('programSet')
            except:
                return None

            if not core: return None

            # Daten extrahieren
            title = core.get('title', 'Unbekannt')
            summary = core.get('description', '')  # Beschreibung steht oft hier
            if not summary: summary = core.get('synopsis', '')

            # 1:1 Bild finden (url1X1)
            image_obj = core.get('image', {})
            img_url = image_obj.get('url1X1')  # DAS IST DAS QUADRATISCHE BILD!
            if not img_url:
                img_url = image_obj.get('src') or image_obj.get('url')

            # Qualität hochsetzen
            if img_url:
                if "{width}" in img_url:
                    img_url = img_url.replace("{width}", "1200")
                elif "?w=" in img_url:
                    img_url = re.sub(r'w=\d+', 'w=1200', img_url)
                elif "&w=" in img_url:
                    img_url = re.sub(r'w=\d+', 'w=1200', img_url)

            # Alter aus Text
            age = self.parse_age(title + " " + summary)

            # Tracks finden
            tracks = []

            # Fall A: Serie
            if 'items' in core and 'nodes' in core['items']:
                for node in core['items']['nodes']:
                    t_title = node.get('title', 'Track')
                    audios = node.get('audios', [])
                    best = sorted([a for a in audios if a.get('downloadUrl')], key=lambda x: x.get('downloadUrl'),
                                  reverse=True)
                    if best:
                        tracks.append(
                            {"title": t_title, "url": best[0]['downloadUrl'], "duration": node.get('duration', 0)})

            # Fall B: Einzel-Episode
            elif 'audios' in core:
                audios = core.get('audios', [])
                best = sorted([a for a in audios if a.get('downloadUrl')], key=lambda x: x.get('downloadUrl'),
                              reverse=True)
                if best:
                    tracks.append({"title": title, "url": best[0]['downloadUrl'], "duration": core.get('duration', 0)})

            # Wenn keine Tracks gefunden wurden, aber es eine Serie ist,
            # könnte man rekursiv laden. Aber hier belassen wir es bei der HTML Analyse für Speed.

            if not tracks: return None

            total_duration = sum(t['duration'] for t in tracks)
            id_clean = urn.split(":")[-1]

            return {
                "id": id_clean,
                "title": title,
                "summary": summary,
                "image_url": img_url,
                "tracks": tracks,
                "duration": total_duration,
                "age": age
            }

        except Exception as e:
            # print(e)
            return None

    # --- VORSCHAU ---
    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]

        if iid not in self.items_map: return
        item = self.items_map[iid]

        self.details_text.config(state="normal")
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', f"📖 {item['title']}\n")
        self.details_text.insert('end', f"👶 Alter: ab {item['age']} J.\n")
        self.details_text.insert('end', f"📂 {item['source_label']} | ⏱ {int(item['duration'] / 60)}m\n\n")
        self.details_text.insert('end', item['summary'])
        self.details_text.config(state="disabled")

        threading.Thread(target=self.load_preview_image, args=(item['image_url'],), daemon=True).start()

    def load_preview_image(self, url):
        if not url: return
        try:
            r = requests.get(url, verify=False, timeout=5)
            img = Image.open(BytesIO(r.content))
            img.thumbnail((380, 380), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.root.after(0, lambda: self.prev_img_label.config(image=photo, text=""))
            self.prev_img_label.image = photo
        except:
            pass

    # --- DOWNLOAD ---
    def start_download_thread(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Info", "Nichts ausgewählt.")
        self.stop_scan = False
        self.btn_download.config(state="disabled", text="⏳ Lade...")

        iids = list(sel)
        threading.Thread(target=self.download_logic, args=(iids,), daemon=True).start()

    def download_logic(self, iids):
        if not os.path.exists(self.export_path): os.makedirs(self.export_path)
        json_file = os.path.join(self.export_path, "klangkiste_ard.json")
        json_entries = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_entries = json.load(f)
            except:
                pass
        existing_ids = [e['tagId'] for e in json_entries]

        count = 0
        for iid in iids:
            if self.stop_scan: break
            if iid not in self.items_map: continue

            item = self.items_map[iid]
            count += 1
            self.root.after(0, lambda t=item['title']: self.status_var.set(f"⬇️ Lade ({count}/{len(iids)}): {t}"))

            safe_title = self.clean_filename(item['title'])

            # Cover (Original speichern)
            cover_filename = f"{safe_title}.jpg"
            cover_path = os.path.join(self.export_path, cover_filename)
            if item['image_url']:
                try:
                    r = requests.get(item['image_url'], verify=False)
                    with open(cover_path, 'wb') as f:
                        f.write(r.content)
                except:
                    pass

            # Tracks
            file_names = []
            for t_idx, track in enumerate(item['tracks']):
                if self.stop_scan: break
                fname = f"{safe_title}.mp3" if len(item['tracks']) == 1 else f"{safe_title} - {t_idx + 1:02d}.mp3"
                fpath = os.path.join(self.export_path, fname)
                if not os.path.exists(fpath):
                    try:
                        r = requests.get(track['url'], stream=True, verify=False, timeout=30)
                        with open(fpath, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=65536): f.write(chunk)
                    except:
                        pass
                file_names.append(fname)

            # M3U
            with open(os.path.join(self.export_path, f"{safe_title}.m3u"), "w", encoding="utf-8") as f:
                for fn in file_names: f.write(fn + "\n")

            # JSON
            tag_id = f"ard_{item['id']}"
            entry = {
                "tagId": tag_id,
                "name": item['title'],
                "playlistFileNames": file_names,
                "imageFileName": cover_filename,
                "meta": {
                    "description": item['summary'][:400],
                    "age_recommendation": item['age'],
                    "genre": "Hörspiel",
                    "runtime": int(item['duration'] / 60),
                    "series": "ARD Audiothek"
                },
                "tags": ["ARD", "Kinder", item['source_label']],
                "filter_age": item['age']
            }
            if tag_id not in existing_ids:
                json_entries.append(entry)
                existing_ids.append(tag_id)

            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_entries, f, indent=4, ensure_ascii=False)

        self.root.after(0, lambda: self.status_var.set("✅ Fertig!"))
        self.root.after(0, lambda: self.btn_download.config(state="normal", text="🚀 AUSWAHL HERUNTERLADEN"))
        if not self.stop_scan: self.root.after(0, self.open_explorer)

    def open_explorer(self):
        messagebox.showinfo("Fertig", f"Dateien in:\n{self.export_path}")
        subprocess.Popen(f'explorer "{os.path.normpath(self.export_path)}"')


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ARDImporterGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Fehler: {e}")
        input("Enter...")
