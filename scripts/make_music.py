#!/usr/bin/env python3
"""
make_music.py — erzeugt ein ruhiges Ambient-Bett als WAV.

Warum selbst erzeugen statt einen fertigen Track nehmen: Auch CC0-Musik wird
von Metas Audioerkennung regelmäßig fälschlich markiert, weil Dritte dieselbe
Aufnahme registriert haben. Selbst erzeugte Klänge haben keinen Rechteinhaber
und lösen keinen Treffer aus.

Klanglich bewusst zurückhaltend: weiche Flächen, langsamer Wechsel, viel
Tiefpass. Das Bett soll unter der Sprachausgabe liegen, nicht auffallen.

Aufruf:
    python3 scripts/make_music.py --sekunden 8 --ziel bett.wav --stimmung ruhig
"""

from __future__ import annotations

import argparse
import math
import struct
import wave
from pathlib import Path

RATE = 44100

# Akkordfolgen als Frequenzen (Grundton, Terz, Quinte, Oktave).
# "ruhig" = Moll-lastig und warm, "hell" = Dur, offener.
STIMMUNGEN = {
    "ruhig": [
        (146.83, 174.61, 220.00, 293.66),   # d-moll
        (130.81, 155.56, 196.00, 261.63),   # c-moll-ish
        (174.61, 220.00, 261.63, 349.23),   # F-Dur
        (130.81, 164.81, 196.00, 261.63),   # C-Dur
    ],
    "hell": [
        (174.61, 220.00, 261.63, 349.23),   # F-Dur
        (196.00, 246.94, 293.66, 392.00),   # G-Dur
        (220.00, 277.18, 329.63, 440.00),   # A-Dur
        (174.61, 220.00, 261.63, 349.23),   # F-Dur
    ],
}


def tiefpass(x: list[float], alpha: float) -> list[float]:
    """Einfacher Einpol-Tiefpass. Nimmt den Flächen die Härte."""
    y, vorher = [], 0.0
    for v in x:
        vorher += alpha * (v - vorher)
        y.append(vorher)
    return y


def erzeuge(sekunden: float, stimmung: str = "ruhig") -> list[float]:
    akkorde = STIMMUNGEN.get(stimmung, STIMMUNGEN["ruhig"])
    n = int(sekunden * RATE)
    pro_akkord = max(1, n // len(akkorde))
    out = [0.0] * n

    for idx, akkord in enumerate(akkorde):
        start = idx * pro_akkord
        ende = min(n, start + pro_akkord)
        laenge = ende - start
        if laenge <= 0:
            break
        # Weiche Hüllkurve: langsam auf, langsam ab, damit nichts klickt.
        for i in range(laenge):
            t = i / RATE
            pos = i / laenge
            huelle = math.sin(math.pi * pos) ** 1.5
            wert = 0.0
            for k, f in enumerate(akkord):
                # Leichte Verstimmung erzeugt Schwebung -> weniger steril.
                schwebung = 1.0 + (0.0013 * (k - 1.5))
                amp = 0.30 / (k + 1.4)
                wert += amp * math.sin(2 * math.pi * f * schwebung * t)
                # Sehr leise Oktave darüber gibt Glanz.
                wert += (amp * 0.16) * math.sin(2 * math.pi * f * 2 * schwebung * t)
            out[start + i] += wert * huelle

    # Akkorde ineinander laufen lassen (grobes Crossfade über die Grenzen).
    out = tiefpass(out, 0.16)

    # Gesamthüllkurve: erste und letzte halbe Sekunde ein- und ausblenden.
    rand = int(0.5 * RATE)
    for i in range(min(rand, n)):
        out[i] *= i / rand
        out[n - 1 - i] *= i / rand

    # Normalisieren auf angenehmen Pegel. Bewusst leise, es ist ein Bett.
    spitze = max((abs(v) for v in out), default=1.0) or 1.0
    ziel = 0.28
    return [v / spitze * ziel for v in out]


def schreiben(samples: list[float], ziel: Path) -> Path:
    with wave.open(str(ziel), "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        rahmen = bytearray()
        for v in samples:
            s = int(max(-1.0, min(1.0, v)) * 32767)
            rahmen += struct.pack("<hh", s, s)
        w.writeframes(bytes(rahmen))
    return ziel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sekunden", type=float, required=True)
    ap.add_argument("--ziel", required=True)
    ap.add_argument("--stimmung", default="ruhig", choices=sorted(STIMMUNGEN))
    a = ap.parse_args()
    p = schreiben(erzeuge(a.sekunden, a.stimmung), Path(a.ziel))
    print(f"{p} ({p.stat().st_size//1024} KB, {a.sekunden}s, {a.stimmung})")


if __name__ == "__main__":
    main()
