#!/usr/bin/env python3
"""
make_reels.py — baut aus Shopify-Produktfotos vertikale 9:16-Reels.

Gedacht für einen GitHub-Actions-Runner: der hat freien Netzzugang und kann
die Bilder von der Shopify-CDN laden. Gerendert wird lokal mit FFmpeg, es
wird also kein kostenpflichtiger Video-API-Dienst gebraucht.

Zweistufiges Rendern, und zwar mit Absicht:
  Stufe 1  jedes Bild einzeln zu einem Clip mit Ken-Burns-Zoomfahrt
  Stufe 2  die Clips per xfade überblenden, Text drauf, stille Tonspur dazu

Der Umweg über Zwischendateien ist nötig, weil `zoompan` keine verwertbare
Bildratenangabe weitergibt und `xfade` dann mit
"The inputs needs to be a constant frame rate; current rate of 1/0" abbricht.
Über Dateien stimmen die Metadaten.

Aufruf:
    python3 scripts/make_reels.py --config reels.config.json --out dist
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# --- Reel-Parameter ---------------------------------------------------------
# 2 s pro Bild entspricht der Empfehlung aus der Recherche (1,5–2,5 s).
BREITE, HOEHE = 1080, 1920
FPS = 30
SEK_PRO_BILD = 2.0
UEBERBLENDUNG = 0.5
ZOOM_MAX = 1.12
# Vorskalierung: nur so viel Reserve, wie der Zoom braucht. Größer kostet
# überproportional Rechenzeit, ohne sichtbar besser zu werden.
VORSKALIERUNG = 1.25

SCHRIFT_KANDIDATEN = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def schriftart() -> str | None:
    for p in SCHRIFT_KANDIDATEN:
        if Path(p).is_file():
            return p
    return None


def ffmpeg_pfad() -> str:
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        sys.exit("FFmpeg fehlt. Auf Ubuntu: sudo apt-get install -y ffmpeg")


def kann_drawtext(ff: str) -> bool:
    """Manche FFmpeg-Builds (z. B. das pip-Paket) sind ohne libfreetype gebaut."""
    try:
        out = subprocess.run([ff, "-hide_banner", "-filters"],
                             capture_output=True, text=True, timeout=60).stdout
        return " drawtext " in out
    except Exception:
        return False


def laden(url: str, ziel: Path) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": "homeeins-reels/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r, open(ziel, "wb") as f:
        shutil.copyfileobj(r, f)
    if ziel.stat().st_size < 1024:
        sys.exit(f"Bild leer oder zu klein: {url}")
    return ziel


def dt_escape(s: str) -> str:
    """Escaping für den drawtext-Filter."""
    for a, b in [("\\", r"\\"), (":", r"\:"), ("'", r"\'"),
                 ("%", r"\%"), (",", r"\,"), ("[", r"\["), ("]", r"\]")]:
        s = s.replace(a, b)
    return s


def clip_rendern(ff: str, bild: Path, ziel: Path) -> Path:
    """Stufe 1: ein Standbild zu einem Clip mit langsamer Zoomfahrt."""
    vw, vh = int(BREITE * VORSKALIERUNG), int(HOEHE * VORSKALIERUNG)
    frames = int(SEK_PRO_BILD * FPS)
    schritt = (ZOOM_MAX - 1) / frames
    vf = (
        f"scale={vw}:{vh}:force_original_aspect_ratio=increase,crop={vw}:{vh},"
        f"zoompan=z='min(zoom+{schritt:.6f},{ZOOM_MAX})':d={frames}"
        f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":s={BREITE}x{HOEHE}:fps={FPS},"
        f"setsar=1,format=yuv420p"
    )
    subprocess.run(
        [ff, "-y", "-loglevel", "error",
         "-loop", "1", "-framerate", str(FPS), "-t", str(SEK_PRO_BILD), "-i", str(bild),
         "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
         "-r", str(FPS), str(ziel)],
        check=True)
    return ziel


def zusammenfuegen(ff: str, clips: list[Path], hook: str, preis: str,
                   ziel: Path, font: str | None, textfaehig: bool) -> Path:
    """Stufe 2: Clips überblenden, Text drauflegen, stille Tonspur anhängen."""
    n = len(clips)
    teile, letzte = [], "0"
    offset = SEK_PRO_BILD - UEBERBLENDUNG
    for i in range(1, n):
        neu = f"x{i}"
        teile.append(f"[{letzte}][{i}]xfade=transition=fade:"
                     f"duration={UEBERBLENDUNG}:offset={offset:.3f}[{neu}]")
        letzte = neu
        offset += SEK_PRO_BILD - UEBERBLENDUNG

    kette = f"[{letzte}]"
    if textfaehig and font and (hook or preis):
        if hook:
            kette += (f"drawtext=fontfile='{font}':text='{dt_escape(hook)}'"
                      f":fontcolor=white:fontsize=64:line_spacing=14"
                      f":borderw=4:bordercolor=black@0.55"
                      f":x=(w-text_w)/2:y=170,")
        if preis:
            kette += (f"drawtext=fontfile='{font}':text='{dt_escape(preis)}'"
                      f":fontcolor=white:fontsize=58"
                      f":box=1:boxcolor=black@0.60:boxborderw=26"
                      f":x=(w-text_w)/2:y=h-300,")
    kette += "format=yuv420p[v]"
    teile.append(kette)

    cmd = [ff, "-y", "-loglevel", "error", "-stats"]
    for c in clips:
        cmd += ["-i", str(c)]
    # Instagram lehnt Reels ohne Audiostream ab -> stille Tonspur.
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    # Dauer explizit setzen. -shortest greift hier nicht, weil anullsrc endlos
    # laeuft und die Videospur aus dem Filtergraph kein Input-Ende meldet –
    # ohne -t kommt ein 123-Sekunden-Video heraus statt eines 5-Sekunden-Reels.
    dauer = n * SEK_PRO_BILD - (n - 1) * UEBERBLENDUNG
    cmd += ["-filter_complex", ";".join(teile),
            "-map", "[v]", "-map", f"{n}:a",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
            "-t", f"{dauer:.3f}", "-movflags", "+faststart", str(ziel)]
    subprocess.run(cmd, check=True)
    return ziel


def zu_cloudinary(datei: Path, public_id: str) -> str | None:
    cloud = os.environ.get("CLOUDINARY_CLOUD_NAME")
    key = os.environ.get("CLOUDINARY_API_KEY")
    secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not all([cloud, key, secret]):
        print("  (keine Cloudinary-Zugangsdaten – Upload übersprungen)")
        return None
    try:
        import requests
    except ImportError:
        print("  (requests fehlt – Upload übersprungen)")
        return None

    ts = int(time.time())
    p = {"public_id": public_id, "timestamp": ts,
         "overwrite": "true", "invalidate": "true"}
    roh = "&".join(f"{k}={p[k]}" for k in sorted(p))
    p["signature"] = hashlib.sha1((roh + secret).encode()).hexdigest()
    p["api_key"] = key

    with open(datei, "rb") as f:
        r = requests.post(f"https://api.cloudinary.com/v1_1/{cloud}/video/upload",
                          data=p, files={"file": f}, timeout=900)
    if r.status_code >= 400:
        print(f"  Cloudinary-Fehler {r.status_code}: {r.text[:300]}")
        return None
    return r.json().get("secure_url")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="reels.config.json")
    ap.add_argument("--out", default="dist")
    ap.add_argument("--nur", help="Nur dieses Produkt rendern (Feld 'name')")
    a = ap.parse_args()

    ff = ffmpeg_pfad()
    font = schriftart()
    textfaehig = kann_drawtext(ff)
    print(f"FFmpeg: {ff}")
    print(f"Schrift: {font or 'KEINE GEFUNDEN'}")
    if not textfaehig:
        print("WARNUNG: Dieses FFmpeg kann kein drawtext (ohne libfreetype gebaut).")
        print("         Reels werden ohne Textebenen gerendert.")
        print("         Abhilfe: sudo apt-get install -y ffmpeg")

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    produkte = cfg["produkte"]
    if a.nur:
        produkte = [p for p in produkte if p["name"] == a.nur]
        if not produkte:
            sys.exit(f"Kein Produkt mit name={a.nur}")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tmp = Path(".reel-tmp")
    ergebnisse = []

    for prod in produkte:
        name = prod["name"]
        print(f"\n=== {name} ===")
        wd = tmp / name
        if wd.exists():
            shutil.rmtree(wd)
        wd.mkdir(parents=True)

        clips = []
        for i, url in enumerate(prod["bilder"], 1):
            bild = laden(url, wd / f"{i:02d}.jpg")
            clip = clip_rendern(ff, bild, wd / f"c{i:02d}.mp4")
            print(f"  [{i}/{len(prod['bilder'])}] Clip {clip.stat().st_size//1024} KB")
            clips.append(clip)

        ziel = out / f"{name}.mp4"
        zusammenfuegen(ff, clips, prod.get("hook", ""), prod.get("preis", ""),
                       ziel, font, textfaehig)
        dauer = len(clips) * SEK_PRO_BILD - (len(clips) - 1) * UEBERBLENDUNG
        print(f"  fertig: {ziel} ({ziel.stat().st_size//1024} KB, ~{dauer:.1f}s)")

        url = zu_cloudinary(ziel, f"homeeins/reels/{name}")
        if url:
            print(f"  online: {url}")
        ergebnisse.append({
            "name": name, "datei": str(ziel), "url": url,
            "hook": prod.get("hook", ""), "preis": prod.get("preis", ""),
            "dauer_s": round(dauer, 1), "mit_text": bool(textfaehig and font),
        })

    (out / "reels.json").write_text(
        json.dumps(ergebnisse, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)

    print(f"\nFertig: {len(ergebnisse)} Reels")
    for e in ergebnisse:
        print(f"  {e['name']}: {e['url'] or e['datei']}")


if __name__ == "__main__":
    main()
