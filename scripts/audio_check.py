#!/usr/bin/env python3
"""
audio_check.py — prüft die Tonspur der fertigen Reels, ohne sie zu hören.

Hintergrund: Ein Fehler im Musikbett (alles unter 400 Hz, praktisch unhörbar)
ist beim reinen Betrachten des Videos nicht aufgefallen und wäre fast in vier
geplante Posts gegangen. Gefunden wurde er erst auf einem Spektrogramm. Dieses
Skript macht daraus einen festen Prüfschritt:

  1. Wellenform und Spektrogramm als PNG  — sichtbar statt hörbar
  2. Spracherkennung (faster-whisper)     — kommt der Text verständlich an?
  3. Lautheit (volumedetect)              — nicht zu leise, nicht übersteuert
  4. Musikbett-Regressionstest            — genug Energie oberhalb 500 Hz

Beendet sich mit Code 1, wenn eine harte Grenze reißt. Fehlt whisper oder
scheitert der Modell-Download, wird nur gewarnt: der Renderlauf soll daran
nicht scheitern.

Aufruf:
    python3 scripts/audio_check.py --dist dist --config reels.config.json
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_music  # noqa: E402

# Verständlichkeit der Sprachausgabe, gemessen als Wortähnlichkeit zwischen
# Vorlage und Transkript. Unter 0.55 ist etwas grundsätzlich kaputt (falsche
# Stimme, abgeschnittene Spur); zwischen 0.55 und 0.75 lohnt ein Blick.
WARN_TEXT = 0.75
FEHLER_TEXT = 0.55

# Lautheit des fertigen Reels in dBFS. loudnorm zielt auf I=-16 LUFS, das
# entspricht grob einem mean_volume um -20 dBFS.
MIN_MEAN_DB = -26.0
MAX_MEAN_DB = -12.0
MAX_PEAK_DB = -0.5

# Musikbett: Abstand zwischen Gesamtpegel und Pegel oberhalb 800 Hz.
# Gemessen am selben Bett vor und nach dem Fix: defekt 24.0 dB, repariert
# 14.7 dB. 18 dB liegt dazwischen. Bei 500 Hz trennen die beiden Fassungen
# sich zu wenig (16.4 gegen 10.3), deshalb 800.
HOCHPASS_HZ = 800
MAX_DUMPFHEIT_DB = 18.0

# Whisper schreibt Zahlen als Ziffern, die Vorlage schreibt sie aus. Ohne
# diese Angleichung sinkt die Ähnlichkeit grundlos.
ZAHLEN = {
    "110": "hundertzehn", "50": "fünfzig", "100": "hundert",
    "10": "zehn", "20": "zwanzig", "30": "dreißig", "40": "vierzig",
    "60": "sechzig", "70": "siebzig", "80": "achtzig", "90": "neunzig",
    "3": "drei", "2": "zwei", "1": "ein",
}


def lauf(cmd: list[str]) -> str:
    """FFmpeg aufrufen und stderr zurückgeben (dort stehen die Messwerte)."""
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stderr + p.stdout


def pegel(ff: str, quelle: Path, filter_: str = "") -> tuple[float, float]:
    """mean_volume und max_volume in dBFS, optional nach einem Filter."""
    af = f"{filter_},volumedetect" if filter_ else "volumedetect"
    text = lauf([ff, "-hide_banner", "-i", str(quelle), "-af", af,
                 "-f", "null", "-"])
    mean = max_ = float("nan")
    for zeile in text.splitlines():
        if "mean_volume:" in zeile:
            mean = float(zeile.split("mean_volume:")[1].split("dB")[0])
        elif "max_volume:" in zeile:
            max_ = float(zeile.split("max_volume:")[1].split("dB")[0])
    return mean, max_


def bilder(ff: str, quelle: Path, qa: Path, name: str) -> list[Path]:
    """Wellenform und Spektrogramm als PNG. Das sind die Artefakte, an denen
    sich Tonprobleme ansehen lassen, ohne etwas abzuspielen."""
    welle = qa / f"{name}.welle.png"
    spek = qa / f"{name}.spektrum.png"
    lauf([ff, "-y", "-hide_banner", "-i", str(quelle), "-filter_complex",
          "showwavespic=s=1600x400:colors=white", "-frames:v", "1", str(welle)])
    lauf([ff, "-y", "-hide_banner", "-i", str(quelle), "-lavfi",
          "showspectrumpic=s=1600x800:legend=1", "-frames:v", "1", str(spek)])
    return [p for p in (welle, spek) if p.exists()]


def normalisieren(text: str) -> list[str]:
    text = text.lower()
    for ziffer, wort in ZAHLEN.items():
        text = re.sub(rf"\b{ziffer}\b", wort, text)
    text = re.sub(r"[^a-zäöüß ]+", " ", text)
    return text.split()


def aehnlichkeit(soll: str, ist: str) -> float:
    return difflib.SequenceMatcher(
        None, normalisieren(soll), normalisieren(ist)).ratio()


def transkribieren(modellname: str):
    """Whisper-Modell laden. Gibt None zurück, wenn das nicht möglich ist —
    in einer Umgebung ohne Netzzugang ist das der Normalfall."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("  HINWEIS: faster-whisper nicht installiert, "
              "Spracherkennung übersprungen")
        return None
    try:
        return WhisperModel(modellname, device="cpu", compute_type="int8")
    except Exception as e:                                  # noqa: BLE001
        print(f"  HINWEIS: Whisper-Modell nicht ladbar ({e}), übersprungen")
        return None


def musikbett_pruefen(ff: str, qa: Path, stimmungen: list[str]) -> list[str]:
    """Regressionstest für den Bassbrumm-Fehler: Das Bett wird neu erzeugt und
    gemessen, ob oberhalb 800 Hz überhaupt etwas ankommt."""
    fehler = []
    for stimmung in stimmungen:
        wav = qa / f"bett-{stimmung}.wav"
        make_music.schreiben(make_music.erzeuge(8.0, stimmung), wav)
        gesamt, _ = pegel(ff, wav)
        hoch, _ = pegel(ff, wav, f"highpass=f={HOCHPASS_HZ}")
        abstand = gesamt - hoch
        zustand = "ok" if abstand <= MAX_DUMPFHEIT_DB else "ZU DUMPF"
        print(f"  Bett '{stimmung}': gesamt {gesamt:.1f} dB, "
              f">{HOCHPASS_HZ} Hz {hoch:.1f} dB, "
              f"Abstand {abstand:.1f} dB — {zustand}")
        lauf([ff, "-y", "-hide_banner", "-i", str(wav), "-lavfi",
              "showspectrumpic=s=1200x600:legend=1", "-frames:v", "1",
              str(qa / f"bett-{stimmung}.spektrum.png")])
        if abstand > MAX_DUMPFHEIT_DB:
            fehler.append(
                f"Musikbett '{stimmung}' ist zu dumpf: {abstand:.1f} dB "
                f"Abstand über {HOCHPASS_HZ} Hz, erlaubt sind "
                f"{MAX_DUMPFHEIT_DB}")
        wav.unlink(missing_ok=True)
    return fehler


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--config", default="reels.config.json")
    ap.add_argument("--qa", default="")
    ap.add_argument("--modell", default="small",
                    help="Whisper-Modell: tiny, base, small, medium")
    ap.add_argument("--ffmpeg", default="ffmpeg")
    a = ap.parse_args()

    dist = Path(a.dist)
    qa = Path(a.qa) if a.qa else dist / "qa"
    qa.mkdir(parents=True, exist_ok=True)

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    texte = {p["name"]: p.get("sprecher", "") for p in cfg["produkte"]}
    stimmungen = sorted({p.get("stimmung", "ruhig") for p in cfg["produkte"]})

    videos = sorted(dist.glob("*.mp4"))
    if not videos:
        sys.exit(f"Keine MP4s in {dist}")

    print("=== Musikbett ===")
    fehler = musikbett_pruefen(a.ffmpeg, qa, stimmungen)

    modell = transkribieren(a.modell)

    for video in videos:
        name = video.stem
        print(f"\n=== {name} ===")
        erzeugt = bilder(a.ffmpeg, video, qa, name)
        print(f"  Bilder: {', '.join(p.name for p in erzeugt) or 'keine'}")

        mean, spitze = pegel(a.ffmpeg, video)
        print(f"  Pegel: mean {mean:.1f} dB, max {spitze:.1f} dB")
        if not MIN_MEAN_DB <= mean <= MAX_MEAN_DB:
            fehler.append(f"{name}: Pegel {mean:.1f} dB außerhalb "
                          f"{MIN_MEAN_DB}..{MAX_MEAN_DB} dB")
        if spitze > MAX_PEAK_DB:
            fehler.append(f"{name}: Spitze {spitze:.1f} dB, übersteuert")

        soll = texte.get(name, "")
        if modell and soll:
            teile, _ = modell.transcribe(str(video), language="de",
                                         beam_size=5)
            ist = " ".join(t.text for t in teile).strip()
            wert = aehnlichkeit(soll, ist)
            print(f"  Erkannt: {ist}")
            print(f"  Übereinstimmung: {wert:.2f}")
            if wert < FEHLER_TEXT:
                fehler.append(f"{name}: Sprachausgabe unverständlich "
                              f"({wert:.2f} < {FEHLER_TEXT})")
            elif wert < WARN_TEXT:
                print(f"  WARNUNG: unter {WARN_TEXT}, bitte anhören")

    print("\n=== Ergebnis ===")
    if fehler:
        for f in fehler:
            print(f"  FEHLER: {f}")
        sys.exit(1)
    print("  Alle Tonprüfungen bestanden")


if __name__ == "__main__":
    main()
