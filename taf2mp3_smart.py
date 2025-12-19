import os
import subprocess
import glob
import json
import hashlib
import requests
import shutil
import sys
import struct

# --- KONFIGURATION ---
SOURCE_DIR = "."         
OUTPUT_DIR = "mp3_converted"
JSON_FILE = "tonies.json"
HEADER_SIZE = 4096       
OPUS_SAMPLE_RATE = 48000.0

# ==========================================
# TEIL 1: DIE NEUE, ROBUSTE TECHNIK (CUE)
# ==========================================

def read_varint(data, offset):
    """Liest einen Protobuf-Wert Byte für Byte."""
    value = 0
    shift = 0
    curr = offset
    while True:
        if curr >= len(data): raise ValueError("EOF")
        byte = data[curr]
        curr += 1
        value |= (byte & 0x7f) << shift
        if not (byte & 0x80): break
        shift += 7
    return value, curr

def get_real_chapters_robust(filepath):
    """
    Sucht 'aggressiv' nach der Kapitelliste im Header.
    Findet auch Kapitel, wenn der Header unsauber ist.
    """
    best_chapters = []
    try:
        with open(filepath, "rb") as f:
            data = f.read(HEADER_SIZE)
            
            # Wir suchen überall nach dem Byte 0x22 (Kennung für Kapitel-Liste)
            for i in range(len(data) - 2):
                if data[i] == 0x22:
                    try:
                        length = data[i+1]
                        start = i + 2
                        end = start + length
                        if end > len(data): continue
                        
                        temp = []
                        curr = start
                        while curr < end:
                            val, curr = read_varint(data, curr)
                            temp.append(val)
                        
                        # Plausibilitäts-Check: Sind es mehr Tracks als vorher gefunden?
                        # Und sind sie sortiert? (Track 2 kommt nach Track 1)
                        if len(temp) > len(best_chapters):
                            if all(temp[j] <= temp[j+1] for j in range(len(temp)-1)):
                                best_chapters = temp
                    except: continue
    except: pass

    # Kapitel 0 ist immer der Start
    return sorted(list(set([0] + best_chapters)))

def scan_ogg_times(filepath):
    """Scannt die Audio-Daten nach exakten Zeitstempeln."""
    page_map = {}
    try:
        with open(filepath, "rb") as f:
            f.seek(HEADER_SIZE)
            file_size = os.fstat(f.fileno()).st_size
            
            while f.tell() < file_size:
                # Sync suchen (falls Datenmüll dazwischen ist)
                pos = f.tell()
                sig = f.read(4)
                if sig != b'OggS':
                    if not sig: break
                    f.seek(pos + 1)
                    continue
                
                head = f.read(23)
                if len(head) < 23: break
                
                # Header auspacken
                data = struct.unpack("<BBQLLLB", head)
                granule = data[2] # Zeit
                seq = data[4]     # Page Nummer
                n_segs = data[6]
                
                # Inhalt überspringen
                seg_table = f.read(n_segs)
                body_size = sum(seg_table)
                f.seek(body_size, 1)
                
                page_map[seq] = granule
    except: pass
    return page_map

def granule_to_cue(granule):
    """Rechnet Samples in CUE-Zeit um."""
    seconds = granule / OPUS_SAMPLE_RATE
    m = int(seconds // 60)
    s = int(seconds % 60)
    f = int((seconds - int(seconds)) * 75)
    return f"{m:02d}:{s:02d}:{f:02d}"

# ==========================================
# TEIL 2: HELFER & UI (WIE IM ALTEN SKRIPT)
# ==========================================

def show_header():
    print("=" * 70)
    print("TAF 2 MP3 COMPLETE (Mit Auto-CUE)".center(70))
    print("=" * 70)

def load_json_db(path):
    print(f"📂 Lade Datenbank: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        db = {}
        for entry in data:
            pic = entry.get('pic')
            if not pic: continue
            for h in entry.get('hash', []):
                db[h.lower()] = {
                    'pic': pic,
                    'title': entry.get('title', 'Unknown'),
                    'series': entry.get('series', ''),
                    'tracks': entry.get('tracks', [])
                }
        print(f"✓ {len(db)} Einträge geladen.")
        print()
        return db
    except:
        print("⚠️  tonies.json nicht gefunden oder fehlerhaft. Mache ohne Metadaten weiter.")
        print()
        return {}

def get_hash(path):
    s = hashlib.sha1()
    try:
        with open(path, 'rb') as f:
            f.seek(HEADER_SIZE)
            while True:
                d = f.read(65536)
                if not d: break
                s.update(d)
        return s.hexdigest().lower()
    except: return None

def download_cover(url, target):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(target, 'wb') as f: f.write(r.content)
            return True
    except: pass
    return False

def clean_filename(name):
    return "".join([c if c.isalnum() or c in " .-_()" else "_" for c in name]).strip()

# ==========================================
# TEIL 3: HAUPTPROGRAMM
# ==========================================

def main():
    show_header()
    
    # 1. Dateien suchen & Anzeigen
    taf_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.taf")))
    
    if not taf_files:
        print("✗ Keine .taf Dateien gefunden!")
        input("Enter zum Beenden...")
        return

    print("📁 Gefundene Dateien:")
    for i, f in enumerate(taf_files, 1):
        size = os.path.getsize(f) / (1024*1024)
        print(f"  {i}. {os.path.basename(f)} ({size:.1f} MB)")
    print()
    print(f"Gesamt: {len(taf_files)} Dateien.")
    print("-" * 70)
    
    input("Drücken Sie Enter zum Starten...")
    print()

    # 2. Datenbank laden
    db = load_json_db(JSON_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 3. Verarbeitungsschleife
    for i, taf_path in enumerate(taf_files, 1):
        filename = os.path.basename(taf_path)
        base_name = os.path.splitext(filename)[0]
        mp3_out = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
        
        print(f"[{i}/{len(taf_files)}] Bearbeite: {filename}")
        
        # A) Metadaten holen
        sys.stdout.write("  🔎 Suche Infos... ")
        sys.stdout.flush()
        file_hash = get_hash(taf_path)
        meta = db.get(file_hash, {})
        
        title = meta.get('title', base_name)
        series = meta.get('series', title)
        track_names = meta.get('tracks', [])
        
        print(f"Found: {title}")
        
        # B) Cover laden
        cover_tmp = "temp_cover.jpg"
        has_cover = False
        if meta.get('pic'):
            if download_cover(meta['pic'], cover_tmp):
                has_cover = True

        # C) MP3 Konvertierung
        if not os.path.exists(mp3_out):
            sys.stdout.write("  🎵 Konvertiere Audio... ")
            sys.stdout.flush()
            try:
                with open(taf_path, "rb") as f:
                    f.seek(HEADER_SIZE)
                    audio_data = f.read()
                
                cmd = ['ffmpeg', '-y', '-f', 'ogg', '-i', 'pipe:0']
                
                if has_cover:
                    cmd += ['-i', cover_tmp, '-map', '0:0', '-map', '1:0', 
                            '-c:v', 'copy', '-id3v2_version', '3', 
                            '-metadata:s:v', 'title="Cover"', '-metadata:s:v', 'comment="Front"']
                
                cmd += ['-c:a', 'libmp3lame', '-q:a', '2', 
                        '-metadata', f'title={title}', 
                        '-metadata', f'artist={series}', 
                        mp3_out]
                
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                proc.communicate(input=audio_data)
                print("✓ Done")
            except Exception as e:
                print(f"✗ Fehler: {e}")
        else:
            print("  ⏭️  MP3 existiert schon.")

        # D) CUE Sheet (DIE MAGIE)
        sys.stdout.write("  ✂️  Erstelle Kapitel (Robust Scan)... ")
        sys.stdout.flush()
        
        # 1. Kapitel-Liste finden (Brute Force)
        chapters = get_real_chapters_robust(taf_path)
        
        if chapters and len(chapters) > 1:
            # 2. Zeiten aus OGG holen
            page_map = scan_ogg_times(taf_path)
            
            clean_title = clean_filename(title)
            cue_path = os.path.join(OUTPUT_DIR, f"{clean_title}.cue")
            
            # Cover auch kopieren
            if has_cover:
                shutil.copy(cover_tmp, os.path.join(OUTPUT_DIR, f"{clean_title}.jpg"))

            try:
                with open(cue_path, "w", encoding="utf-8") as f:
                    f.write(f'REM CREATED BY TAF2MP3 COMPLETE\n')
                    f.write(f'TITLE "{title}"\n')
                    f.write(f'PERFORMER "{series}"\n')
                    f.write(f'FILE "{os.path.basename(mp3_out)}" MP3\n')
                    
                    track_no = 1
                    for page_idx in chapters:
                        # Zeit ermitteln
                        time_str = "00:00:00"
                        if page_idx > 0:
                            prev = page_idx - 1
                            # Falls Lücke in Pages, rückwärts suchen
                            tries = 100
                            while prev >= 0 and prev not in page_map and tries > 0:
                                prev -= 1; tries -= 1
                            
                            if prev in page_map:
                                time_str = granule_to_cue(page_map[prev])
                        
                        # Name ermitteln
                        t_name = f"Chapter {track_no}"
                        if track_no <= len(track_names):
                            t_name = track_names[track_no-1]
                            
                        f.write(f'  TRACK {track_no:02d} AUDIO\n')
                        f.write(f'    TITLE "{t_name}"\n')
                        f.write(f'    INDEX 01 {time_str}\n')
                        track_no += 1
                        
                print(f"✓ ({len(chapters)} Tracks)")
            except Exception as e:
                print(f"✗ Fehler CUE: {e}")
        else:
            print("✗ Keine Kapitel im Header gefunden.")

        # Cleanup
        if os.path.exists(cover_tmp): os.remove(cover_tmp)
        print()

    print("=" * 70)
    print("Fertig! Alle Dateien wurden verarbeitet.")
    print(f"Ordner: {os.path.abspath(OUTPUT_DIR)}")
    input("Drücken Sie Enter zum Beenden...")

if __name__ == "__main__":
    main()
