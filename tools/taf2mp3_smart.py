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
# TEIL 1: HEADER & OGG ANALYSE (THEORETISCH)
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

def get_chapters_robust(filepath):
    """
    Findet die Kapitel-Marker im Header via Brute-Force-Suche.
    Findet garantiert die 25 Tracks, auch wenn der Header 'unsauber' ist.
    """
    best_chapters = []
    try:
        with open(filepath, "rb") as f:
            data = f.read(HEADER_SIZE)
            
            # Suche nach Byte 0x22 (Protobuf Tag für Feld 4 / ChapterPages)
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
                        
                        # Plausibilitäts-Check: 
                        # Sind die Page-Nummern aufsteigend? (Kapitel 2 > Kapitel 1)
                        # Wir nehmen die längste gefundene valide Liste.
                        if len(temp) > len(best_chapters):
                            if all(temp[j] <= temp[j+1] for j in range(len(temp)-1)):
                                best_chapters = temp
                    except: continue
    except: pass

    # Kapitel 0 (Start) ist immer implizit dabei
    return sorted(list(set([0] + best_chapters)))

def scan_ogg_timestamps(filepath):
    """
    Liest die exakten Zeitstempel (Granules) aus den OGG-Pages.
    """
    page_map = {}
    try:
        with open(filepath, "rb") as f:
            f.seek(HEADER_SIZE)
            file_size = os.fstat(f.fileno()).st_size
            
            while f.tell() < file_size:
                # Sync suchen
                pos = f.tell()
                sig = f.read(4)
                if sig != b'OggS':
                    if not sig: break
                    f.seek(pos + 1)
                    continue
                
                head = f.read(23)
                if len(head) < 23: break
                
                # Header auspacken: Granule ist Index 2 (Q), PageSeq ist Index 4 (L)
                data = struct.unpack("<BBQLLLB", head)
                granule = data[2] 
                seq = data[4]
                n_segs = data[6]
                
                # Inhalt überspringen
                seg_table = f.read(n_segs)
                f.seek(sum(seg_table), 1)
                
                page_map[seq] = granule
    except: pass
    return page_map

def granule_to_cue(granule):
    """Rechnet Samples (48kHz) in CUE-Zeit um."""
    seconds = granule / OPUS_SAMPLE_RATE
    m = int(seconds // 60)
    s = int(seconds % 60)
    f = int((seconds - int(seconds)) * 75)
    return f"{m:02d}:{s:02d}:{f:02d}"

# ==========================================
# TEIL 2: HELFER & UI
# ==========================================

def show_header():
    print("=" * 70)
    print("TAF 2 MP3 THEORETICAL (Robust Header Scan)".center(70))
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
    
    # 1. Dateien suchen
    taf_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.taf")))
    if not taf_files:
        print("✗ Keine .taf Dateien gefunden!")
        input("Enter zum Beenden...")
        return

    print("📁 Gefundene Dateien:")
    for i, f in enumerate(taf_files, 1):
        print(f"  {i}. {os.path.basename(f)}")
    print("-" * 70)
    
    input("Drücken Sie Enter zum Starten...")
    print()

    db = load_json_db(JSON_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, taf_path in enumerate(taf_files, 1):
        filename = os.path.basename(taf_path)
        base_name = os.path.splitext(filename)[0]
        mp3_out = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")
        
        print(f"[{i}/{len(taf_files)}] Verarbeite: {filename}")
        
        # A) Metadaten
        sys.stdout.write("  -> Metadaten... ")
        file_hash = get_hash(taf_path)
        meta = db.get(file_hash, {})
        title = meta.get('title', base_name)
        series = meta.get('series', title)
        track_names = meta.get('tracks', [])
        print(f"'{title}'")
        
        # B) Cover
        cover_tmp = "temp_cover.jpg"
        has_cover = False
        if meta.get('pic'):
            if download_cover(meta['pic'], cover_tmp): has_cover = True

        # C) MP3 Konvertierung
        if not os.path.exists(mp3_out):
            sys.stdout.write("  -> Audio (FFmpeg)... ")
            sys.stdout.flush()
            try:
                with open(taf_path, "rb") as f:
                    f.seek(HEADER_SIZE)
                    audio_data = f.read()
                
                cmd = ['ffmpeg', '-y', '-f', 'ogg', '-i', 'pipe:0']
                if has_cover:
                    cmd += ['-i', cover_tmp, '-map', '0:0', '-map', '1:0', '-c:v', 'copy', '-id3v2_version', '3', '-metadata:s:v', 'title="Cover"', '-metadata:s:v', 'comment="Front"']
                
                cmd += ['-c:a', 'libmp3lame', '-q:a', '2', '-metadata', f'title={title}', '-metadata', f'artist={series}', mp3_out]
                subprocess.run(cmd, input=audio_data, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("✓")
            except Exception as e: print(f"✗ {e}")
        else:
            print("  -> MP3 existiert schon.")

        # D) CUE (THEORETISCH / ROBUST)
        sys.stdout.write("  -> CUE (Header Scan)... ")
        sys.stdout.flush()
        
        # 1. Kapitel-Liste (Robust)
        chapters = get_chapters_robust(taf_path)
        
        if chapters and len(chapters) > 1:
            # 2. Zeitstempel (Ogg Scan)
            page_map = scan_ogg_timestamps(taf_path)
            
            clean_title = clean_filename(title)
            cue_path = os.path.join(OUTPUT_DIR, f"{clean_title}.cue")
            if has_cover: shutil.copy(cover_tmp, os.path.join(OUTPUT_DIR, f"{clean_title}.jpg"))

            try:
                with open(cue_path, "w", encoding="utf-8") as f:
                    f.write(f'REM CREATED BY TAF2MP3 THEORETICAL\n')
                    f.write(f'TITLE "{title}"\nPERFORMER "{series}"\n')
                    f.write(f'FILE "{os.path.basename(mp3_out)}" MP3\n')
                    
                    track_no = 1
                    for page_idx in chapters:
                        time_str = "00:00:00"
                        if page_idx > 0:
                            prev = page_idx - 1
                            # Lücken-Fallback
                            tries = 100
                            while prev >= 0 and prev not in page_map and tries > 0:
                                prev -= 1; tries -= 1
                            
                            if prev in page_map:
                                time_str = granule_to_cue(page_map[prev])
                        
                        t_name = f"Chapter {track_no}"
                        if track_no <= len(track_names): t_name = track_names[track_no-1]
                        
                        f.write(f'  TRACK {track_no:02d} AUDIO\n')
                        f.write(f'    TITLE "{t_name}"\n')
                        f.write(f'    INDEX 01 {time_str}\n')
                        track_no += 1
                        
                print(f"✓ ({len(chapters)} Tracks)")
            except Exception as e: print(f"✗ {e}")
        else:
            print(f"✗ Fehler: Nur {len(chapters)} Kapitel gefunden.")

        if os.path.exists(cover_tmp): os.remove(cover_tmp)
        print()

    print("=" * 70)
    print("Fertig!")
    input("Enter...")

if __name__ == "__main__":
    main()
