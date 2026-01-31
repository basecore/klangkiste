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
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- KONFIGURATION ---
VERSION = "22.0 (Sub-Series & Multi-M3U)"
AUTHOR = "KlangKiste ARD Importer"
DEFAULT_START_URL = "https://www.ardaudiothek.de/rubrik/fuer-kinder/urn:ard:page:36c12c1321f8895a/"
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
"""

class ARDImporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"📺 {AUTHOR} - v{VERSION}")
        self.root.geometry("1600x900")
        self.root.configure(bg=COLOR_BG)

        self.items_map = {}
        self.export_path = os.path.join(os.getcwd(), "klangkiste_ard_content")
        self.stop_scan = False

        self.setup_ui()

    def setup_ui(self):
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True)

        self.tab_import = tk.Frame(self.nb, bg=COLOR_BG)
        self.nb.add(self.tab_import, text=" 📥 Hörbuch & Podcast Importer ")

        self.tab_info = tk.Frame(self.nb, bg="white")
        self.nb.add(self.tab_info, text=" ℹ️ Info ")
        self.setup_info_tab()

        header = tk.Frame(self.tab_import, bg=COLOR_HEADER, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="ARD Audiothek Importer", fg="white", bg=COLOR_HEADER, font=("Arial", 24, "bold")).pack()
        tk.Label(header, text=f"Für Podcasts & Hörspiele | v{VERSION}", fg="#cbd5e1", bg=COLOR_HEADER, font=("Arial", 11)).pack()

        tool_frame = tk.Frame(self.tab_import, bg=COLOR_BG, pady=10, padx=20)
        tool_frame.pack(fill="x")

        tk.Label(tool_frame, text="URL:", bg=COLOR_BG, font=("Arial", 10, "bold")).pack(side="left")
        self.url_entry = tk.Entry(tool_frame, width=50)
        self.url_entry.insert(0, DEFAULT_START_URL)
        self.url_entry.pack(side="left", padx=5)

        tk.Button(tool_frame, text="▶ Starten", command=self.start_scan_thread, bg="#27ae60", fg="white",
                  font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=5)
        tk.Button(tool_frame, text="⏹ STOPP", command=self.stop_process, bg="#c0392b", fg="white",
                  font=("Arial", 10, "bold"), padx=15).pack(side="left", padx=5)

        tk.Label(tool_frame, text="    Zielordner:", bg=COLOR_BG).pack(side="left", padx=5)
        self.path_entry = tk.Entry(tool_frame, width=30)
        self.path_entry.insert(0, self.export_path)
        self.path_entry.pack(side="left", padx=5)
        tk.Button(tool_frame, text="📂", command=self.choose_path).pack(side="left")

        content = tk.Frame(self.tab_import, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=20, pady=5)

        left_frame = tk.Frame(content, bg="white")
        left_frame.pack(side="left", fill="both", expand=True)

        cols = ('Status', 'Alter', 'Datum', 'Titel', 'Dauer', 'Podcast', 'Sender', 'Rubrik')
        self.tree = ttk.Treeview(left_frame, columns=cols, show='headings', selectmode="extended")

        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_tree(c, False))

        self.tree.column('Status', width=80, anchor="center")
        self.tree.column('Alter', width=50, anchor="center")
        self.tree.column('Datum', width=80, anchor="center")
        self.tree.column('Titel', width=350)
        self.tree.column('Dauer', width=60, anchor="center")
        self.tree.column('Podcast', width=200)
        self.tree.column('Sender', width=120)
        self.tree.column('Rubrik', width=120)

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        sb = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        self.preview_panel = tk.Frame(content, bg="white", width=420, bd=1, relief="ridge")
        self.preview_panel.pack(side="right", fill="both", padx=(15, 0))
        self.preview_panel.pack_propagate(False)

        self.prev_img_label = tk.Label(self.preview_panel, bg="white", text="") 
        self.prev_img_label.pack(pady=20)

        self.details_text = tk.Text(self.preview_panel, bg="white", font=("Arial", 10), relief="flat", wrap="word",
                                    state="disabled", height=20)
        self.details_text.pack(fill="both", expand=True, padx=20, pady=10)

        footer = tk.Frame(self.tab_import, bg=COLOR_BG, pady=15, padx=20)
        footer.pack(fill="x", side="bottom")

        self.status_var = tk.StringVar(value="Bereit.")
        tk.Label(footer, textvariable=self.status_var, bg=COLOR_BG, fg="#555", font=("Arial", 11, "italic")).pack(side="left")

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

    def clean_filename(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:100]

    def clean_text(self, soup_element):
        if not soup_element: return ""
        text = soup_element.get_text(separator=" ")
        return " ".join(text.split())

    # --- HELPER: Datum parsen für Sortierung ---
    def get_date_obj(self, date_str):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except:
            return datetime.min

    # --- FORMATIERUNG ---
    def format_title_numbering(self, title):
        if not title: return ""
        title = title.strip()
        
        # Erkennt: "Titel der Unterserie (1/4): Episodentitel"
        match = re.search(r'^(.*?)\s*\((\d+)/(\d+)\)(.*)', title)
        if match:
            sub_series = match.group(1).strip()
            current = int(match.group(2))
            total = int(match.group(3))
            rest = match.group(4).strip()
            
            # Wenn rest mit : beginnt, entfernen
            if rest.startswith(":") or rest.startswith("-"):
                rest = rest[1:].strip()
            
            # Format: (01/04) SubSerie: Titel
            prefix = f"({current:02d}/{total:02d})"
            
            if sub_series:
                return f"{prefix} {sub_series}: {rest}" if rest else f"{prefix} {sub_series}"
            return f"{prefix} {rest}"
            
        return title

    # --- SORTIERUNG ---
    def sort_tree(self, col, reverse):
        l = [(self.tree.set(k, col), self.tree.set(k, 'Titel'), k) for k in self.tree.get_children('')]
        
        def get_title_sort_key(full_title):
            # Sortiert erst nach Text, dann nach (x/y)
            m = re.match(r'^\((\d+)/(\d+)\)\s*(.+)', full_title)
            if m:
                curr = int(m.group(1))
                total = int(m.group(2))
                text = m.group(3).strip().lower()
                return (text, total, curr)
            return (full_title.lower(), 0, 0)

        try:
            l.sort(key=lambda t: (datetime.strptime(t[0], "%d.%m.%Y"), t[1]), reverse=reverse)
        except ValueError:
            try:
                l.sort(key=lambda t: (int(re.sub(r'\D', '', t[0])), t[1]), reverse=reverse)
            except:
                l.sort(key=lambda t: (t[0].lower(), get_title_sort_key(t[1])), reverse=reverse)

        for index, (val, title, k) in enumerate(l):
            self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    # --- ALTERSERKENNUNG ---
    def parse_age(self, text):
        if not text: return 0
        text = text.lower()
        
        match = re.search(r'empfohlen\s*ab\s*(\d{1,2})', text)
        if match:
             age = int(match.group(1))
             if age <= 20: return age

        match = re.search(r'(?:ab|von|für)\s*(?:kinder)?\s*(?:ab|von)?\s*(\d{1,2})(?:[\s\-]*(?:bis|oder)?[\s\-]*\d{1,2})?\s*jahren?', text)
        if match:
            age = int(match.group(1))
            if age <= 20: return age 

        match = re.search(r'^(\d{1,2})\s+jahre', text)
        if match:
            age = int(match.group(1))
            if age <= 20: return age
        return 0

    def start_scan_thread(self):
        self.stop_scan = False
        self.items_map = {}
        for i in self.tree.get_children(): self.tree.delete(i)
        self.btn_download.config(state="disabled")
        threading.Thread(target=self.scan_logic, daemon=True).start()

    def get_links_from_url(self, url):
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            text = r.text
            soup = BeautifulSoup(text, 'html.parser')
            
            h1 = soup.find('h1')
            page_title = self.clean_text(h1) if h1 else ""

            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                link_title = self.clean_text(a) or "Lade Titel..."

                if "/episode/" in href:
                    urn_match = re.search(r'(urn:ard:episode:[a-zA-Z0-9]+)', href)
                    if urn_match:
                        urn = urn_match.group(1)
                        links.append({"urn": urn, "href": href, "type": "audio", "title": link_title})
                elif "/sendung/" in href or "/sammlung/" in href or "/rubrik/" in href:
                    links.append({"href": href, "type": "collection", "title": link_title})

            return links, page_title
        except Exception as e:
            print(f"Error fetching links: {e}")
            return [], ""

    def scan_logic(self):
        start_url = self.url_entry.get().strip()
        self.status_var.set(f"🔍 Scanne Start-URL...")

        processed_urns = set()
        items_todo = {}
        collections_to_scan = []
        
        root_links, root_title = self.get_links_from_url(start_url)
        generic_titles = ["Für Kinder", "Hauptseite", "Startseite", root_title]

        for l in root_links:
            if l['type'] == 'audio':
                if l['urn'] not in processed_urns:
                    items_todo[l['urn']] = {"title": l['title'], "source": root_title, "age": 0, "href": l['href']}
                    processed_urns.add(l['urn'])
            elif l['type'] == 'collection':
                collections_to_scan.append(l)

        for col in collections_to_scan:
            if self.stop_scan: break
            full_url = BASE_DOMAIN + col['href'] if col['href'].startswith("/") else col['href']
            if full_url == start_url: continue
            self.root.after(0, lambda t=col['title']: self.status_var.set(f"📖 Scanne Container: {t}..."))
            sub_links, page_title = self.get_links_from_url(full_url)
            inherited_age = self.parse_age(page_title)
            for l in sub_links:
                if l['type'] == 'audio':
                    if l['urn'] not in processed_urns:
                        items_todo[l['urn']] = {
                            "title": l['title'], "source": page_title, "age": inherited_age, "href": l['href']
                        }
                        processed_urns.add(l['urn'])

        queue_list = list(items_todo.items())
        total = len(queue_list)
        
        if total == 0:
            self.root.after(0, lambda: messagebox.showinfo("Info", "Keine Audio-Episoden gefunden."))
            self.root.after(0, lambda: self.status_var.set("Keine Ergebnisse."))
            self.root.after(0, lambda: self.btn_download.config(state="normal"))
            return

        self.root.after(0, lambda: self.status_var.set(f"💡 {total} Einträge gefunden. Starte Detail-Analyse..."))

        for i, (urn, meta) in enumerate(queue_list):
            if self.stop_scan: break
            iid = urn.split(":")[-1]
            self.root.after(0, self.add_placeholder_item, iid, meta['title'], meta['source'])
            self.analyze_item(urn, meta, iid, i + 1, total)
            time.sleep(0.01)

        if not self.stop_scan:
            self.root.after(0, lambda: self.status_var.set("🔄 Synchronisiere Altersempfehlungen..."))
            self.apply_age_groups(generic_titles)

        msg = "🛑 Abgebrochen." if self.stop_scan else f"✅ Fertig. {total} Episoden geladen."
        self.root.after(0, lambda: self.status_var.set(msg))
        self.root.after(0, lambda: self.btn_download.config(state="normal"))

    def apply_age_groups(self, generic_titles):
        groups = {}
        for iid, data in self.items_map.items():
            src = data.get('source_label', '')
            if not src: continue
            if src not in groups: groups[src] = []
            groups[src].append(iid)

        for source, iids in groups.items():
            if source in generic_titles or "Für Kinder" in source: continue
            found_age = 0
            for iid in iids:
                if self.items_map[iid]['age'] > 0:
                    found_age = self.items_map[iid]['age']
                    break 
            if found_age > 0:
                updates_made = False
                for iid in iids:
                    if self.items_map[iid]['age'] == 0:
                        self.items_map[iid]['age'] = found_age
                        updates_made = True
                if updates_made:
                    self.root.after(0, self.refresh_tree_ages, iids, found_age)

    def refresh_tree_ages(self, iids, age):
        age_str = f"{age}+"
        for iid in iids:
            if self.tree.exists(iid):
                self.tree.set(iid, "Alter", age_str)

    def add_placeholder_item(self, iid, title, source):
        if not self.tree.exists(iid):
            self.tree.insert('', 'end', iid=iid, values=("⏳ Lade...", "-", "-", title, "-", "-", "-", "-"))

    def analyze_item(self, urn, meta, iid, current_idx, total):
        if current_idx % 5 == 0:
            self.root.after(0, lambda: self.status_var.set(f"Analysiere {current_idx}/{total}: {meta['title']}"))

        web_url = BASE_DOMAIN + meta['href'] if meta['href'].startswith("/") else meta['href']
        data = self.fetch_full_details_html(web_url, urn)

        if data:
            if data['age'] == 0 and meta['age'] > 0: data['age'] = meta['age']
            if meta['source'] and meta['source'] != "Hauptseite":
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
            self.tree.set(iid, "Datum", data.get('datum', '-'))
            self.tree.set(iid, "Titel", data['title'])
            self.tree.set(iid, "Dauer", f"{mins}m")
            self.tree.set(iid, "Podcast", data.get('podcast', '-'))
            self.tree.set(iid, "Sender", data.get('sender', '-'))
            self.tree.set(iid, "Rubrik", data.get('rubrik', '-'))

    def fetch_full_details_html(self, url, urn):
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            if r.status_code != 200: return None

            soup = BeautifulSoup(r.text, 'html.parser')
            meta_info = {"datum": "-", "rubrik": "-", "sender": "-", "podcast": "-"}
            
            def get_meta_value(soup, label_text):
                try:
                    label_span = soup.find('span', string=label_text)
                    if not label_span: return "-"
                    value_div = label_span.find_parent('div').find_next_sibling('div')
                    if not value_div: return "-"
                    return self.clean_text(value_div)
                except: return "-"

            meta_info["datum"] = get_meta_value(soup, "Erscheinungsdatum")
            meta_info["rubrik"] = get_meta_value(soup, "Rubrik")
            meta_info["sender"] = get_meta_value(soup, "Sender")
            meta_info["podcast"] = get_meta_value(soup, "Podcast")

            script = soup.find('script', id='__NEXT_DATA__')
            if not script: return None

            json_data = json.loads(script.string)
            try:
                base = json_data['props']['pageProps']['initialData']['data']
                core = base.get('item') or base.get('programSet')
            except: return None
            if not core: return None

            title = core.get('title', 'Unbekannt')
            title = self.format_title_numbering(title)

            summary = core.get('description', '') 
            if not summary: summary = core.get('synopsis', '')
            
            program_info = core.get('program', {})
            source_label = program_info.get('title', 'ARD Audiothek')
            
            if meta_info["podcast"] == "-" and source_label: 
                meta_info["podcast"] = source_label

            image_obj = core.get('image', {})
            img_url = image_obj.get('url1X1')
            if not img_url:
                img_url = image_obj.get('src') or image_obj.get('url')
            if img_url:
                if "{width}" in img_url: img_url = img_url.replace("{width}", "1200")
                elif "?w=" in img_url: img_url = re.sub(r'w=\d+', 'w=1200', img_url)
                elif "&w=" in img_url: img_url = re.sub(r'w=\d+', 'w=1200', img_url)

            age = self.parse_age(title + " " + summary)
            
            tracks = []
            def extract_best_audio(audios_list):
                best = sorted([a for a in audios_list if a.get('downloadUrl')], key=lambda x: x.get('downloadUrl'), reverse=True)
                if best: return best[0]['downloadUrl']
                best_fallback = sorted([a for a in audios_list if a.get('url')], key=lambda x: x.get('url'), reverse=True)
                if best_fallback:
                    fb = best_fallback[0]['url']
                    if ".mp3" in fb: return fb
                    return fb
                return None

            if 'items' in core and 'nodes' in core['items']:
                for node in core['items']['nodes']:
                    t_title = node.get('title', 'Track')
                    dl_url = extract_best_audio(node.get('audios', []))
                    if dl_url:
                        tracks.append({"title": t_title, "url": dl_url, "duration": node.get('duration', 0)})

            elif 'audios' in core:
                dl_url = extract_best_audio(core.get('audios', []))
                if dl_url:
                    tracks.append({"title": title, "url": dl_url, "duration": core.get('duration', 0)})

            if not tracks: return None
            total_duration = sum(t['duration'] for t in tracks)
            id_clean = urn.split(":")[-1]

            return {
                "id": id_clean, "title": title, "summary": summary, "image_url": img_url,
                "tracks": tracks, "duration": total_duration, "age": age, "source_label": source_label,
                "datum": meta_info["datum"], "rubrik": meta_info["rubrik"],
                "sender": meta_info["sender"], "podcast": meta_info["podcast"]
            }
        except: return None

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        iid = sel[0]
        if iid not in self.items_map: return
        item = self.items_map[iid]

        self.details_text.config(state="normal")
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', f"📖 {item['title']}\n")
        self.details_text.insert('end', f"🎙 Podcast: {item['podcast']} | 📡 {item['sender']}\n")
        self.details_text.insert('end', f"📅 {item['datum']} | 📂 {item['rubrik']}\n")
        self.details_text.insert('end', f"👶 Alter: ab {item['age']} J. | ⏱ {int(item['duration'] / 60)}m\n\n")
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
        except: pass

    def start_download_thread(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Info", "Nichts ausgewählt.")
        self.stop_scan = False
        self.btn_download.config(state="disabled", text="⏳ Lade...")
        iids = list(sel)
        threading.Thread(target=self.download_logic, args=(iids,), daemon=True).start()

    # --- HAUPTLOGIK: DOWNLOAD (MIT SUB-SERIES GRUPPIERUNG) ---
    def download_logic(self, iids):
        if not os.path.exists(self.export_path): os.makedirs(self.export_path)
        json_file = os.path.join(self.export_path, "klangkiste_ard.json")
        json_entries = []
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_entries = json.load(f)
            except: pass
        existing_ids = [e['tagId'] for e in json_entries]

        # 1. Gruppierung
        # Wir versuchen, eine "Unter-Serie" zu erkennen.
        # Format im Titel: "(01/04) Unterserie: Titel" oder "(01/04) Unterserie - Titel"
        grouped_items = {}
        
        for iid in iids:
            if iid not in self.items_map: continue
            item = self.items_map[iid]
            
            raw_cast = item.get('podcast', '-')
            if not raw_cast or raw_cast == "-":
                raw_cast = "Unknown_Collection_" + iid
            
            # --- SUB-SERIES ERKENNUNG ---
            # Wir extrahieren den Teil VOR dem Doppelpunkt oder dem Titel, wenn er in (x/y) steht
            sub_series_name = raw_cast # Standard ist Podcast Name
            
            m = re.match(r'^\((\d+)/(\d+)\)\s*(.+)', item['title'])
            if m:
                # Titel hat Nummerierung. Wir schauen, was danach kommt.
                rest = m.group(3).strip()
                # Oft ist es "Unterserie: Episodentitel"
                if ":" in rest:
                    parts = rest.split(":", 1)
                    potential_sub = parts[0].strip()
                    # Wenn der Teil vor dem Doppelpunkt nicht zu lang ist, ist es wohl der Serienname
                    if len(potential_sub) < 50:
                        sub_series_name = f"{raw_cast} - {potential_sub}"
                
                # Manchmal ist es auch nur "Unterserie Teil 1" -> schwer zu trennen ohne Doppelpunkt
                # Wir belassen es bei Doppelpunkt-Logik oder expliziter Nummerierung als Indikator
            
            # Gruppieren nach (SubSeriesName, ImageURL)
            group_key = (sub_series_name, item.get('image_url', ''))
            
            if group_key not in grouped_items:
                grouped_items[group_key] = []
            grouped_items[group_key].append(item)

        # 2. Verarbeitung
        for key, items in grouped_items.items():
            if self.stop_scan: break
            series_name = key[0] # Das ist jetzt entweder "Podcast" oder "Podcast - Unterserie"
            
            # Entscheidung: Zusammenfassen wenn > 1
            is_series = len(items) > 1 and "Unknown_Collection_" not in series_name

            # Sortieren
            try:
                has_numbers = any(re.match(r'^\s*\((\d+)/(\d+)\)', x['title']) for x in items)
                if has_numbers:
                    def sort_num(i):
                        m = re.match(r'^\s*\((\d+)/(\d+)\)', i['title'])
                        return int(m.group(1)) if m else 9999
                    items.sort(key=sort_num)
                else:
                    items.sort(key=lambda x: self.get_date_obj(x.get('datum', '')))
            except: pass

            if is_series:
                # --- SERIEN MODUS ---
                self.root.after(0, lambda pn=series_name: self.status_var.set(f"📦 Verarbeite: {pn}"))
                
                # Name bereinigen
                clean_series_name = self.clean_filename(series_name)
                # Falls zu lang, kürzen
                if len(clean_series_name) > 100: clean_series_name = clean_series_name[:100]
                
                first_item = items[0]
                safe_title = clean_series_name
                cover_filename = f"{safe_title}.jpg"
                cover_path = os.path.join(self.export_path, cover_filename)
                
                if first_item['image_url']:
                    try:
                        r = requests.get(first_item['image_url'], verify=False)
                        with open(cover_path, 'wb') as f: f.write(r.content)
                    except: pass

                all_files = []
                total_duration = 0
                
                for idx, ep in enumerate(items):
                    if self.stop_scan: break
                    
                    # Titel säubern (Nummerierung entfernen, da wir eigene machen oder sortiert haben)
                    # Wir wollen "Titel" haben. Wenn "(01/04) Sub: Titel", dann nur "Titel"
                    ep_clean_title = self.clean_filename(ep['title'])
                    
                    # Versuche, den reinen Episodentitel zu extrahieren
                    m_title = re.match(r'^\(\d+/\d+\)\s*.*?:?\s*(.*)', ep['title'])
                    if m_title:
                        ep_clean_title = self.clean_filename(m_title.group(1))

                    # Präfix
                    match_num = re.match(r'^\s*\((\d+)/\d+\)', ep['title'])
                    if match_num:
                        prefix = f"{int(match_num.group(1)):02d}"
                    else:
                        d_obj = self.get_date_obj(ep.get('datum', ''))
                        if d_obj != datetime.min: prefix = d_obj.strftime("%Y-%m-%d")
                        else: prefix = f"{idx+1:02d}"

                    for t_i, track in enumerate(ep['tracks']):
                        fname = f"{safe_title} - {prefix} - {ep_clean_title}.mp3"
                        if len(ep['tracks']) > 1:
                            fname = f"{safe_title} - {prefix} - {ep_clean_title} ({t_i+1}).mp3"
                        
                        fpath = os.path.join(self.export_path, fname)
                        if not os.path.exists(fpath):
                            try:
                                r = requests.get(track['url'], stream=True, verify=False, timeout=30)
                                with open(fpath, 'wb') as f:
                                    for chunk in r.iter_content(chunk_size=65536): f.write(chunk)
                            except: pass
                        all_files.append(fname)
                        total_duration += track.get('duration', 0)

                with open(os.path.join(self.export_path, f"{safe_title}.m3u"), "w", encoding="utf-8") as f:
                    for fn in all_files: f.write(fn + "\n")

                tag_id = f"ard_series_{self.clean_filename(series_name)}"
                tags = ["ARD", "Kinder", "Serie"]
                if first_item['podcast'] != "-": tags.append(first_item['podcast'])
                # Sender etc.
                
                entry = {
                    "tagId": tag_id, "name": series_name, 
                    "playlistFileNames": all_files,
                    "imageFileName": cover_filename,
                    "meta": {
                        "description": f"Sammlung: {series_name}.\nEnthält {len(items)} Episoden.\n\n{first_item['summary'][:300]}...",
                        "age_recommendation": first_item['age'],
                        "genre": "Podcast-Serie", "runtime": int(total_duration / 60),
                        "series": first_item['podcast'],
                        "released_at": first_item['datum'],
                        "station": first_item['sender'],
                        "category": first_item['rubrik']
                    },
                    "tags": tags, "filter_age": first_item['age']
                }
                
                if tag_id not in existing_ids:
                    json_entries.append(entry)
                    existing_ids.append(tag_id)

            else:
                # --- EINZEL MODUS ---
                for item in items:
                    self.root.after(0, lambda t=item['title']: self.status_var.set(f"⬇️ Lade Einzel: {t}"))
                    
                    raw_podcast = item.get('podcast', '-')
                    clean_cast = ""
                    if raw_podcast and raw_podcast != "-":
                        parts = re.split(r'\s+[-–]\s+', raw_podcast)
                        clean_cast = self.clean_filename(parts[0])

                    safe_title = self.clean_filename(item['title'])
                    if clean_cast:
                        if safe_title.lower().startswith(clean_cast.lower()): base_name = safe_title
                        else: base_name = f"{clean_cast} - {safe_title}"
                    else:
                        base_name = safe_title
                    
                    if len(base_name) > 150: base_name = base_name[:150]

                    cover_filename = f"{base_name}.jpg"
                    cover_path = os.path.join(self.export_path, cover_filename)
                    if item['image_url']:
                        try:
                            r = requests.get(item['image_url'], verify=False)
                            with open(cover_path, 'wb') as f: f.write(r.content)
                        except: pass

                    file_names = []
                    for t_idx, track in enumerate(item['tracks']):
                        if self.stop_scan: break
                        fname = f"{base_name}.mp3" if len(item['tracks']) == 1 else f"{base_name} - {t_idx + 1:02d}.mp3"
                        fpath = os.path.join(self.export_path, fname)
                        if not os.path.exists(fpath):
                            try:
                                r = requests.get(track['url'], stream=True, verify=False, timeout=30)
                                with open(fpath, 'wb') as f:
                                    for chunk in r.iter_content(chunk_size=65536): f.write(chunk)
                            except: pass
                        file_names.append(fname)

                    with open(os.path.join(self.export_path, f"{base_name}.m3u"), "w", encoding="utf-8") as f:
                        for fn in file_names: f.write(fn + "\n")

                    tag_id = f"ard_{item['id']}"
                    tags = ["ARD", "Kinder"]
                    if item['podcast'] != "-": tags.append(item['podcast'])
                    
                    entry = {
                        "tagId": tag_id, "name": item['title'], "playlistFileNames": file_names,
                        "imageFileName": cover_filename,
                        "meta": {
                            "description": item['summary'][:400], "age_recommendation": item['age'],
                            "genre": "Podcast/Hörspiel", "runtime": int(item['duration'] / 60), 
                            "series": item['podcast'], "released_at": item['datum'],
                            "station": item['sender'], "category": item['rubrik']
                        },
                        "tags": tags, "filter_age": item['age']
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
