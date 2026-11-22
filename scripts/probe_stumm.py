"""Gegenprobe: darf ein Reel ohne Sprecher durchrutschen?

Vorgeschichte, 10.08.2026: im Matrix-Job fuer "gewichtsdecke" scheiterten
alle vier deutschen Piper-Stimmen. make_reels.py hat eine WARNUNG gedruckt,
weitergerendert und mit Rueckgabewert 0 geendet. Das Video ging als
"success" durch -- nur Musik, kein Sprecher. Gefunden hat es erst die
Tonpruefung im naechsten Job: Uebereinstimmung 0.00, Spitzenpegel -8.2 dB
statt der ueblichen -1.5 dB, und Whisper "erkannte" im stummen Ton den
Untertitel-Rest "Copyright WDR 2020".

Ein stummes Reel ist bei dieser Strecke kein abgeschwaechtes Ergebnis,
sondern Ausschuss. Deshalb bricht der Renderer jetzt hart ab -- und laesst
sich nur mit --ohne-stimme ausdruecklich umstimmen. Beide Richtungen
werden hier geprueft; eine Sperre, die man nicht auch absichtlich oeffnen
kann, wird sonst irgendwann umgangen.

Der Netzzugang wird ueber einen toten Proxy gekappt, damit der
Stimm-Download zwangslaeufig scheitert.

Lauf: python3 scripts/probe_stumm.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CFG = {"produkte": [{
    "name": "testprodukt", "hook": "Test", "preis": "1 EUR",
    "stimmung": "ruhig",
    "sprecher": "Dies ist ein Sprechertext, also erwarte ich Sprachausgabe.",
    "bilder": ["https://example.invalid/bild.jpg"],
}]}

# Toter Proxy: jeder Download scheitert, egal welcher.
UMGEBUNG = {"PATH": "/usr/bin:/bin", "PIP_NO_INDEX": "1",
            "HTTP_PROXY": "http://127.0.0.1:1",
            "HTTPS_PROXY": "http://127.0.0.1:1"}

WURZEL = Path(__file__).parent.parent


def main() -> int:
    fehler = 0
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        (t / "cfg.json").write_text(json.dumps(CFG), encoding="utf-8")
        umg = {**UMGEBUNG, "HOME": str(t)}

        for name, extra, soll_abbruch in (
            ("ohne Schalter: muss abbrechen", [], True),
            ("mit --ohne-stimme: muss weitermachen", ["--ohne-stimme"], False),
        ):
            r = subprocess.run(
                [sys.executable, "scripts/make_reels.py",
                 "--config", str(t / "cfg.json"),
                 "--out", str(t / "out")] + extra,
                capture_output=True, text=True, env=umg, cwd=WURZEL)
            aus = r.stdout + r.stderr
            # An der Stimmsperre abgebrochen -- nicht irgendwo sonst.
            abgebrochen = ("keine Piper-Stimme verfügbar" in aus
                           and r.returncode != 0)
            # Sperre passiert. Dass der Lauf danach trotzdem scheitert
            # (Bilddownload ohne Netz), ist hier egal und erwartet.
            weiter = "stumme Reels sind angefordert" in aus
            ok = abgebrochen if soll_abbruch else weiter
            if not ok:
                fehler += 1
                print(f"FEHLER  {name}")
                print("   ---", aus.strip()[-400:])
            else:
                print(f"OK      {name}")
    print(f"\nFehlschlaege: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
