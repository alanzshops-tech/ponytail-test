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
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_music  # noqa: E402

# Piper-Stimmen in Wunschreihenfolge. Die erste, die sich laden lässt,
# wird genommen — der Katalog ändert sich gelegentlich, deshalb mehrere.
STIMMEN = [
    "de_DE-thorsten-high",
    "de_DE-thorsten-medium",
    "de_DE-ramona-low",
    "de_DE-kerstin-low",
]

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


def clip_rendern(ff: str, bild: Path, ziel: Path, sekunden: float) -> Path:
    """Stufe 1: ein Standbild zu einem Clip mit langsamer Zoomfahrt."""
    vw, vh = int(BREITE * VORSKALIERUNG), int(HOEHE * VORSKALIERUNG)
    frames = int(sekunden * FPS)
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
         "-loop", "1", "-framerate", str(FPS), "-t", str(sekunden), "-i", str(bild),
         "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
         "-r", str(FPS), str(ziel)],
        check=True)
    return ziel


def zusammenfuegen(ff: str, clips: list[Path], hook: str, preis: str,
                   ziel: Path, font: str | None, textfaehig: bool,
                   sek_pro_bild: float, musik: Path | None = None,
                   stimme: Path | None = None) -> Path:
    """Stufe 2: Clips überblenden, Text drauflegen, Ton mischen."""
    n = len(clips)
    teile, letzte = [], "0"
    offset = sek_pro_bild - UEBERBLENDUNG
    for i in range(1, n):
        neu = f"x{i}"
        teile.append(f"[{letzte}][{i}]xfade=transition=fade:"
                     f"duration={UEBERBLENDUNG}:offset={offset:.3f}[{neu}]")
        letzte = neu
        offset += sek_pro_bild - UEBERBLENDUNG

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

    dauer = n * sek_pro_bild - (n - 1) * UEBERBLENDUNG

    cmd = [ff, "-y", "-loglevel", "error", "-stats"]
    for c in clips:
        cmd += ["-i", str(c)]

    # Tonspur zusammenstellen. Instagram lehnt Reels ohne Audiostream ab,
    # deshalb gibt es immer eine – notfalls Stille.
    ton_idx, ton_filter = [], []
    if musik:
        cmd += ["-i", str(musik)]
        ton_idx.append(len(clips) + len(ton_idx))
        ton_filter.append(f"[{ton_idx[-1]}:a]volume=0.62[mus]")
    if stimme:
        cmd += ["-i", str(stimme)]
        ton_idx.append(len(clips) + len(ton_idx))
        # Sprache auf volle Laenge bringen und leicht anheben.
        # Mit Musik wird die Spur zweimal gebraucht (als Sidechain-Ausloeser
        # und als Tonspur im Mix). Ein Filter-Ausgang darf in FFmpeg aber nur
        # EINMAL verbraucht werden – deshalb asplit. Ohne Musik entfaellt das,
        # denn ein unbenutzter Ausgang wuerde den Graphen ungueltig machen.
        basis = (f"[{ton_idx[-1]}:a]apad,atrim=0:{dauer:.3f},volume=1.5")
        ton_filter.append(
            f"{basis},asplit=2[spr1][spr2]" if musik else f"{basis}[spr]")

    if musik and stimme:
        # Musik unter der Sprache absenken (Sidechain-Ducking), dann
        # auf einheitliche Lautheit bringen.
        ton_filter.append(
            # ratio 6 hat die Musik unter der Sprache komplett verschwinden
            # lassen. 3 senkt sie hörbar ab, ohne sie wegzudrücken.
            "[mus][spr1]sidechaincompress=threshold=0.08:ratio=3:attack=25:"
            "release=450[musduck]")
        ton_filter.append("[musduck][spr2]amix=inputs=2:duration=first:"
                          "normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    elif stimme:
        ton_filter.append("[spr]loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    elif musik:
        ton_filter.append("[mus]loudnorm=I=-18:TP=-1.5:LRA=11[a]")
    else:
        cmd += ["-f", "lavfi", "-i",
                "anullsrc=channel_layout=stereo:sample_rate=44100"]
        ton_filter.append(f"[{len(clips)}:a]anull[a]")

    # Dauer explizit setzen: -shortest greift nicht auf Filter-Ausgaben, und
    # eine endlose Tonquelle wuerde das Video sonst massiv verlaengern.
    cmd += ["-filter_complex", ";".join(teile + ton_filter),
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
            "-t", f"{dauer:.3f}", "-movflags", "+faststart", str(ziel)]
    subprocess.run(cmd, check=True)
    return ziel


def wav_dauer(p: Path) -> float:
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def stimme_holen(ordner: Path) -> Path | None:
    """Lädt die erste verfügbare deutsche Piper-Stimme herunter."""
    ordner.mkdir(parents=True, exist_ok=True)
    for name in STIMMEN:
        onnx = ordner / f"{name}.onnx"
        if onnx.is_file():
            return onnx
        r = subprocess.run(
            [sys.executable, "-m", "piper.download_voices",
             "--download-dir", str(ordner), name],
            capture_output=True, text=True)
        if r.returncode == 0 and onnx.is_file():
            print(f"  Stimme: {name}")
            return onnx
        print(f"  Stimme {name} nicht verfügbar ({r.stderr.strip()[:90]})")
    return None


def sprechen(text: str, modell: Path, ziel: Path) -> Path | None:
    """Erzeugt die Sprachausgabe. length-scale 1.05 = minimal langsamer,
    das wirkt ruhiger und passt besser zu Wohn-Themen."""
    r = subprocess.run(
        [sys.executable, "-m", "piper", "-m", str(modell),
         "-f", str(ziel), "--length-scale", "1.05", "--sentence-silence", "0.35"],
        input=text, capture_output=True, text=True)
    if r.returncode != 0 or not ziel.is_file():
        print(f"  Sprachausgabe fehlgeschlagen: {r.stderr.strip()[:200]}")
        return None
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

    # Stimme einmal fuer alle Produkte laden.
    braucht_stimme = any(p.get("sprecher") for p in produkte)
    modell = stimme_holen(tmp / "stimmen") if braucht_stimme else None
    if braucht_stimme and not modell:
        print("WARNUNG: Keine Piper-Stimme verfügbar – Reels ohne Sprachausgabe.")

    for prod in produkte:
        name = prod["name"]
        print(f"\n=== {name} ===")
        wd = tmp / name
        if wd.exists():
            shutil.rmtree(wd)
        wd.mkdir(parents=True)

        n = len(prod["bilder"])

        # Sprachausgabe zuerst: ihre Länge bestimmt das Tempo der Bildfolge,
        # damit der Text nicht abgeschnitten wird.
        stimme = None
        sprecher_text = prod.get("sprecher", "").strip()
        if sprecher_text and modell:
            stimme = sprechen(sprecher_text, modell, wd / "stimme.wav")
            if stimme:
                print(f"  Sprachausgabe: {wav_dauer(stimme):.1f}s")

        sek_pro_bild = SEK_PRO_BILD
        if stimme:
            noetig = wav_dauer(stimme) + 1.2 + (n - 1) * UEBERBLENDUNG
            sek_pro_bild = max(SEK_PRO_BILD, min(6.0, noetig / n))
        dauer = n * sek_pro_bild - (n - 1) * UEBERBLENDUNG
        print(f"  Bildtakt: {sek_pro_bild:.2f}s -> Reel {dauer:.1f}s")

        clips = []
        for i, url in enumerate(prod["bilder"], 1):
            bild = laden(url, wd / f"{i:02d}.jpg")
            clip = clip_rendern(ff, bild, wd / f"c{i:02d}.mp4", sek_pro_bild)
            print(f"  [{i}/{n}] Clip {clip.stat().st_size//1024} KB")
            clips.append(clip)

        musik = None
        if prod.get("musik", True):
            musik = make_music.schreiben(
                make_music.erzeuge(dauer, prod.get("stimmung", "ruhig")),
                wd / "musik.wav")

        ziel = out / f"{name}.mp4"
        zusammenfuegen(ff, clips, prod.get("hook", ""), prod.get("preis", ""),
                       ziel, font, textfaehig, sek_pro_bild, musik, stimme)
        print(f"  fertig: {ziel} ({ziel.stat().st_size//1024} KB, {dauer:.1f}s)")

        url = zu_cloudinary(ziel, f"homeeins/reels/{name}")
        if url:
            print(f"  online: {url}")
        ergebnisse.append({
            "name": name, "datei": str(ziel), "url": url,
            "hook": prod.get("hook", ""), "preis": prod.get("preis", ""),
            "dauer_s": round(dauer, 1), "mit_text": bool(textfaehig and font),
            "mit_stimme": bool(stimme), "mit_musik": bool(musik),
        })

    (out / "reels.json").write_text(
        json.dumps(ergebnisse, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)

    print(f"\nFertig: {len(ergebnisse)} Reels")
    for e in ergebnisse:
        print(f"  {e['name']}: {e['url'] or e['datei']}")


if __name__ == "__main__":
    main()
