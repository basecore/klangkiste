import os
import json
import requests
import datetime
import urllib3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from io import BytesIO
import threading
import subprocess
import re
import html
import webbrowser
import random
import time
from bs4 import BeautifulSoup

# SSL & Header Setup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}

VERSION = "4.2"
LAST_UPDATE = "27.01.2026"
AUTHOR = "KlangKiste Magic Importer"
LOGO_URL = "https://www.ohrka.de/templates/public/img/logo.png"

RANDOM_COLORS = [
    (46, 204, 113), (52, 152, 219), (155, 89, 182),
    (231, 76, 60), (241, 196, 15), (230, 126, 34), (26, 188, 156),
    (142, 68, 173), (22, 160, 133), (44, 62, 80)
]


class ImporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"🚀 {AUTHOR} - OHRKA Edition - v{VERSION}")
        self.root.geometry("1300x950")
        self.root.configure(bg="#f4f7f6")

        self.books = []
        self.sort_reverse = {"ID": False, "Alter": False, "Titel": False, "Likes": True}
        self.export_path = os.path.join(os.getcwd(), "ohrka_export")
        self.logo_data = self.fetch_logo()

        self.setup_ui()
        threading.Thread(target=self.load_all_sources, daemon=True).start()

    def fetch_logo(self):
        try:
            r = requests.get(LOGO_URL, verify=False, timeout=10)
            return r.content if r.status_code == 200 else None
        except:
            return None

    def open_url(self, url):
        webbrowser.open_new(url)

    def setup_ui(self):
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True)

        self.tab_import = tk.Frame(self.nb, bg="#f4f7f6")
        self.nb.add(self.tab_import, text=" 📥 Hörbuch Importer ")

        self.tab_info = tk.Frame(self.nb, bg="white")
        self.nb.add(self.tab_info, text=" ℹ️ Über OHRKA ")
        self.setup_info_tab()

        header = tk.Frame(self.tab_import, bg="#2ecc71", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🎨 KlangKiste Magic Import", fg="white", bg="#2ecc71", font=("Arial", 26, "bold")).pack()
        tk.Label(header, text=f"Fan-Projekt für OHRKA.de | v{VERSION} | Stand: {LAST_UPDATE}", fg="#eefcf1",
                 bg="#2ecc71", font=("Arial", 12, "italic")).pack()

        footer_parent = tk.Frame(self.tab_import, bg="#f4f7f6", pady=10)
        footer_parent.pack(fill="x", side="bottom", padx=20)

        status_line = tk.Frame(footer_parent, bg="#f4f7f6")
        status_line.pack(fill="x")
        self.status_var = tk.StringVar(value="🔍 Suche läuft...")
        tk.Label(status_line, textvariable=self.status_var, bg="#f4f7f6", fg="#7f8c8d",
                 font=("Arial", 12, "italic")).pack(side="left")
        self.sync_var = tk.StringVar(value="")
        tk.Label(status_line, textvariable=self.sync_var, bg="#f4f7f6", fg="#e67e22", font=("Arial", 12, "bold")).pack(
            side="left", padx=30)

        self.btn_go = tk.Button(footer_parent, text="🚀 AUSWAHL HERUNTERLADEN", bg="#e67e22", fg="white",
                                font=("Arial", 16, "bold"), relief="flat", command=self.start_download, padx=50,
                                pady=15)
        self.btn_go.pack(side="right", pady=(10, 0))

        tool_frame = tk.Frame(self.tab_import, bg="#f4f7f6", pady=10)
        tool_frame.pack(fill="x", padx=20)
        tk.Label(tool_frame, text="Filter:", bg="#f4f7f6", font=("Arial", 14, "bold")).pack(side="left")
        self.age_filter = ttk.Combobox(tool_frame, values=["Alle", "3+", "5+", "8+", "10+", "12+"], state="readonly",
                                       font=("Arial", 12), width=10)
        self.age_filter.current(0)
        self.age_filter.pack(side="left", padx=10)
        self.age_filter.bind("<<ComboboxSelected>>", self.refresh_list)
        self.path_entry = tk.Entry(tool_frame, font=("Arial", 12))
        self.path_entry.insert(0, self.export_path)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10)
        tk.Button(tool_frame, text="Pfad", command=self.choose_path, bg="#3498db", fg="white", relief="flat",
                  font=("Arial", 12, "bold")).pack(side="left")

        content = tk.Frame(self.tab_import, bg="#f4f7f6")
        content.pack(fill="both", expand=True, padx=20, pady=5)
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=35)
        self.tree = ttk.Treeview(table_frame, columns=('ID', 'Alter', 'Titel', 'Likes'), show='headings',
                                 selectmode="extended")
        self.tree.heading('ID', text='Nr.', command=lambda: self.sort_column("ID"))
        self.tree.heading('Alter', text='👶 Alter', command=lambda: self.sort_column("Alter"))
        self.tree.heading('Titel', text='📖 Titel', command=lambda: self.sort_column("Titel"))
        self.tree.heading('Likes', text='❤️', command=lambda: self.sort_column("Likes"))
        self.tree.column('ID', width=60, anchor="center")
        self.tree.column('Alter', width=100, anchor="center")
        self.tree.column('Titel', width=500)
        self.tree.column('Likes', width=100, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        self.preview_panel = tk.Frame(content, bg="#ffffff", width=450, bd=1, relief="ridge")
        self.preview_panel.pack(side="right", fill="both", padx=(15, 0))
        self.prev_label = tk.Label(self.preview_panel, bg="white")
        self.prev_label.pack(pady=25)
        self.details_text = tk.Text(self.preview_panel, bg="white", font=("Arial", 12), relief="flat", wrap="word",
                                    state="disabled")
        self.details_text.pack(fill="both", expand=True, padx=20, pady=15)

    def setup_info_tab(self):
        container = tk.Frame(self.tab_info, bg="white", padx=40, pady=40)
        container.pack(fill="both", expand=True)
        tk.Label(container, text="Was ist OHRKA?", font=("Arial", 22, "bold"), bg="white", fg="#2ecc71").pack(
            anchor="w")
        info_text = (
            "OHRKA e.V. ist ein gemeinnütziges Netzwerk, das hochwertigste Hörabenteuer für Kinder "
            "kostenlos, werbefrei und ohne Anmeldung zur Verfügung stellt.\n\n"
            "WICHTIG: Dieses Tool ist KEIN offizielles Produkt von OHRKA e.V.\n\n"
            "Bitte unterstütze OHRKA e.V. mit einer Spende!"
        )
        tk.Label(container, text=info_text, font=("Arial", 13), bg="white", wraplength=800, justify="left",
                 pady=20).pack(anchor="w")
        btn_frame = tk.Frame(container, bg="white")
        btn_frame.pack(fill="x", pady=20)
        tk.Button(btn_frame, text="🌐 Website", command=lambda: self.open_url("https://www.ohrka.de"), bg="#3498db",
                  fg="white", font=("Arial", 12, "bold"), padx=20, pady=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="❤️ Spenden",
                  command=lambda: self.open_url("https://www.ohrka.de/ueber-ohrka/spenden-fuer-ohrka"), bg="#e67e22",
                  fg="white", font=("Arial", 12, "bold"), padx=20, pady=10).pack(side="left", padx=10)

    def refresh_list(self, event=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        f = self.age_filter.get()
        for i, b in enumerate(self.books):
            if f == "Alle" or f == b['age']:
                l = b['likes'] if b['likes'] > 0 else "⏳"
                self.tree.insert('', 'end', values=(i + 1, b['age'], b['title'], l), iid=i)

    def sort_column(self, col):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        if col in ["ID", "Likes"]:
            data.sort(key=lambda x: int(re.sub(r'\D', '', str(x[0])) or 0), reverse=self.sort_reverse[col])
        else:
            data.sort(reverse=self.sort_reverse[col])
        for index, item in enumerate(data): self.tree.move(item[1], '', index)
        self.sort_reverse[col] = not self.sort_reverse[col]

    def choose_path(self):
        p = filedialog.askdirectory()
        if p: self.export_path = p; self.path_entry.delete(0, tk.END); self.path_entry.insert(0, p)

    def load_all_sources(self):
        self.books = []
        urls = ["https://www.ohrka.de/suchen",
                "https://www.ohrka.de/ueber-ohrka/alle-hoerabenteuer",
                "https://www.ohrka.de/ueber-ohrka/100-neue-ohrka-maerchen"]

        for url in urls:
            try:
                res = requests.get(url, verify=False, headers=HEADERS, timeout=15)
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, 'html.parser')

                for teaser in soup.find_all('div', class_='teaser'):
                    link = teaser.find_parent('a') or teaser.find('a')
                    if not link or not link.get('href'): continue

                    href = link['href']
                    full_url = "https://www.ohrka.de" + href if not href.startswith('http') else href

                    if any(x['url'] == full_url for x in self.books): continue

                    icon_url = None
                    img_div = teaser.find('div', class_='teaserImageIcon')
                    if img_div:
                        img = img_div.find('img')
                        if img and img.get('src'):
                            icon_url = "https://www.ohrka.de" + img['src'] if not img['src'].startswith('http') else \
                            img['src']

                    text_div = teaser.find('div', class_='teaserText')
                    if not text_div: continue

                    # Titel extrahieren
                    title = "Unbekannt"
                    h3 = text_div.find('h3')
                    if h3:
                        title_text = h3.find(string=True, recursive=False)
                        if title_text:
                            title = title_text.strip()
                        else:
                            full_h3 = h3.get_text()
                            ratings = h3.find('span', class_='ratings')
                            if ratings:
                                title = full_h3.replace(ratings.get_text(), "").strip()
                            else:
                                title = full_h3.strip()

                    # Likes
                    likes = 0
                    ratings_span = text_div.find('span', class_='ratings')
                    if ratings_span:
                        try:
                            likes = int(re.sub(r'\D', '', ratings_span.get_text()))
                        except:
                            pass

                    # Beschreibung
                    desc = ""
                    p_tag = text_div.find('p')
                    if p_tag:
                        desc = html.unescape(p_tag.get_text().strip())

                    self.books.append({
                        "title": title,
                        "url": full_url,
                        "age": "⏳",
                        "runtime": "⏳",
                        "likes": likes,
                        "chapters": [],
                        "desc": desc,
                        "icon_url_source": icon_url,
                        "icon_data": None
                    })

            except Exception as e:
                print(f"Fehler beim Laden von {url}: {e}")

        self.root.after(0, self.refresh_list)
        self.status_var.set(f"✅ {len(self.books)} Geschichten gefunden.")
        threading.Thread(target=self.pre_scan_all, daemon=True).start()

    def fetch_full_details(self, book_obj):
        try:
            res = requests.get(book_obj['url'], verify=False, timeout=10, headers=HEADERS)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'html.parser')

            dur = "⏳"
            dur_m = re.search(r'(\d{1,2}:\d{2}:\d{2})', res.text)
            if dur_m: dur = dur_m.group(1)

            chapters = []
            chap_m = re.search(r'var mp3SoundInfos = (\{.*?\});', res.text)
            if chap_m:
                try:
                    raw_chap = json.loads(chap_m.group(1).replace('\\/', '/'))
                    for k in sorted(raw_chap.keys(), key=int):
                        chapters.append({"idx": k, "start": int(raw_chap[k]["start"])})
                except:
                    pass

            age = "⏳"
            age_m = re.search(r'(\d+)_pl\.png', res.text)
            if age_m: age = f"{age_m.group(1)}+"

            icon_data = None
            if book_obj.get('icon_url_source'):
                try:
                    ir = requests.get(book_obj['icon_url_source'], verify=False, timeout=5)
                    if ir.status_code == 200:
                        icon_data = ir.content
                except:
                    pass

            return age, dur, chapters, icon_data
        except:
            return "⏳", "⏳", [], None

    def pre_scan_all(self):
        for i, b in enumerate(self.books):
            age, dur, chaps, ic_data = self.fetch_full_details(b)
            b.update({"age": age, "runtime": dur, "chapters": chaps, "icon_data": ic_data})
            self.root.after(0, lambda idx=i, book=b: self.tree.item(idx, values=(
                idx + 1, book['age'], book['title'], book['likes'] if book['likes'] > 0 else "⏳")))
            self.sync_var.set(f"⏳ Sync Details: {i + 1}/{len(self.books)}")
        self.sync_var.set("✅ Daten synchronisiert")

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        idx = int(sel[0])
        b = self.books[idx]
        self.update_preview_text(
            f"📖 {b['title']}\n👶 Alter: {b['age']}\n⏱ Dauer: {b['runtime']}\n❤️ Likes: {b['likes']}\n\n{b.get('desc', '')}")
        cover = self.generate_sq_cover(self.logo_data, b['title'], b.get('icon_data'))
        if cover:
            cover.thumbnail((380, 380))
            photo = ImageTk.PhotoImage(cover)
            self.prev_label.config(image=photo)
            self.prev_label.image = photo

    def update_preview_text(self, text):
        self.details_text.config(state="normal")
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert('1.0', text)
        self.details_text.config(state="disabled")

    def generate_sq_cover(self, logo_raw, title, specific_icon_raw=None):
        canvas = Image.new("RGB", (600, 600), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)

        # 1. Logo RIESIG
        if logo_raw:
            try:
                logo = Image.open(BytesIO(logo_raw)).convert("RGBA")
                target_w = 580
                ratio = target_w / logo.width
                target_h = int(logo.height * ratio)
                logo = logo.resize((target_w, target_h), Image.LANCZOS)
                canvas.paste(logo, ((600 - logo.width) // 2, 20), logo)
            except:
                pass

        # 2. Icon 250px
        if specific_icon_raw:
            try:
                spec_icon = Image.open(BytesIO(specific_icon_raw)).convert("RGBA")
                target_w = 250
                ratio = target_w / spec_icon.width
                target_h = int(spec_icon.height * ratio)
                if target_h > 250:
                    target_h = 250
                    ratio = target_h / spec_icon.height
                    target_w = int(spec_icon.width * ratio)
                spec_icon = spec_icon.resize((target_w, target_h), Image.LANCZOS)
                canvas.paste(spec_icon, ((600 - spec_icon.width) // 2, 250), spec_icon)
            except:
                pass

        try:
            font = ImageFont.truetype("arial.ttf", 52)
        except:
            font = ImageFont.load_default()

        words = title.split()
        raw_lines = []
        cur = ""
        for w in words:
            if draw.textbbox((0, 0), cur + w, font=font)[2] < 560:
                cur += w + " "
            else:
                raw_lines.append(cur.strip())
                cur = w + " "
        raw_lines.append(cur.strip())

        final_lines = []
        if len(raw_lines) > 2:
            final_lines.append(raw_lines[0])
            line2 = raw_lines[1]
            while draw.textbbox((0, 0), line2 + "...", font=font)[2] > 560 and len(line2) > 1:
                line2 = line2[:-1]
            final_lines.append(line2.strip() + "...")
        else:
            final_lines = [l for l in raw_lines if l]

        bg_color = random.choice(RANDOM_COLORS)
        line_height = 60
        padding = 30
        bh = len(final_lines) * line_height + padding
        draw.rectangle([0, 600 - bh, 600, 600], fill=bg_color)
        y = 600 - bh + (padding // 2) - 5

        for l in final_lines:
            text_w = draw.textbbox((0, 0), l, font=font)[2]
            draw.text(((600 - text_w) // 2, y), l, font=font, fill="white")
            y += line_height

        return canvas

    def start_download(self):
        sel = self.tree.selection()
        if not sel: return
        threading.Thread(target=self.download_loop, args=([int(i) for i in sel],), daemon=True).start()

    def download_loop(self, indices):
        path = self.path_entry.get()
        audio_dir = os.path.join(path, "audio")
        os.makedirs(audio_dir, exist_ok=True)
        results = []
        for idx in indices:
            b = self.books[idx]
            self.status_var.set(f"📥 Lade: {b['title']}...")
            entry = self.proc_file(b, audio_dir)
            if entry:
                results.append(entry)
                self.save_json(path, results)
        self.status_var.set("✅ Fertig!")
        messagebox.showinfo("Fertig", f"Exportiert nach:\n{path}")
        subprocess.Popen(f'explorer "{os.path.normpath(path)}"')

    def proc_file(self, b, folder):
        try:
            res = requests.get(b['url'], verify=False, headers=HEADERS, timeout=15)
            mp3_match = re.search(r'href="([^"]+\.mp3)"', res.text)
            if not mp3_match: return None
            mp3_url = mp3_match.group(1)
            if not mp3_url.startswith('http'): mp3_url = "https://www.ohrka.de" + mp3_url

            safe = "".join([c for c in b['title'] if c.isalnum() or c in (' ', '-', '_')]).strip()

            with open(os.path.join(folder, f"{safe}.mp3"), 'wb') as f:
                f.write(requests.get(mp3_url, verify=False, timeout=60).content)

            # Optimiertes Speichern (kleinere Dateigröße)
            self.generate_sq_cover(self.logo_data, b['title'], b.get('icon_data')).save(
                os.path.join(folder, f"{safe}.jpg"), "JPEG", quality=70, optimize=True)

            if b['chapters']:
                with open(os.path.join(folder, f"{safe}.cue"), 'w', encoding='utf-8') as c:
                    c.write(f'FILE "{safe}.mp3" MP3\n')
                    for ch in b['chapters']:
                        m, s = divmod(ch['start'], 60)
                        c.write(
                            f'  TRACK {int(ch["idx"]):02d} AUDIO\n    TITLE "Kapitel {ch["idx"]}"\n    INDEX 01 {m:02d}:{s:02d}:00\n')

            rt = 0
            if ":" in str(b['runtime']):
                parts = b['runtime'].split(":")
                if len(parts) >= 2:
                    rt = int(parts[0]) * 60 + int(parts[1])
            else:
                rt = int(re.sub(r'\D', '', str(b['runtime'])) or 0)

            return {
                "tagId": f"ohr_{int(time.time())}_{os.urandom(2).hex()}",
                "name": b['title'],
                "playlistFileNames": [f"{safe}.mp3"],
                "imageFileName": f"{safe}.jpg",
                "meta": {
                    "series": b['title'].split("-")[0].strip(),
                    "episode": "Hörbuch",
                    "description": b['desc'],
                    "age_recommendation": int(re.sub(r'\D', '', b['age']) or 0),
                    "genre": "Hörspiel",
                    "language": "Deutsch",
                    "runtime": rt
                },
                "tags": ["Ohrka", "Hörspiel", "Kostenlos"],
                "filter_age": int(re.sub(r'\D', '', b['age']) or 0),
                "downloadUrl": mp3_url  # Wichtig für die App!
            }
        except:
            return None

    def save_json(self, path, data):
        j_p = os.path.join(path, "klangkiste.json")
        cur = []
        if os.path.exists(j_p):
            try:
                with open(j_p, 'r', encoding='utf-8') as f:
                    cur = json.load(f)
            except:
                pass

        for d in data:
            exists = False
            for i, e in enumerate(cur):
                if e['name'] == d['name']:
                    cur[i] = d
                    exists = True
                    break
            if not exists: cur.append(d)

        with open(j_p, 'w', encoding='utf-8') as f:
            json.dump(cur, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImporterGUI(root)
    root.mainloop()
