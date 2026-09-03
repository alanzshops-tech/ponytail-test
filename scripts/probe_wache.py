"""Gegenprobe fuer die Live-Theme-Sperre in aufraeumen.yml.

Der Workflow loescht Dateien aus einem Theme. Die Sperre davor ist das
Einzige, was zwischen einem Tippfehler und einem leeren Live-Shop steht --
also muss sie selbst geprueft werden, und zwar gegen einen Fall, der
durchgehen MUSS, und einen, der abbrechen MUSS.

Vorgeschichte: bis zum 10.08.2026 stand die Nummer des Live-Themes fest im
Workflow. Sie zeigte auf 182664626499, das laengst nicht mehr
veroeffentlicht war. Die Sperre schuetzte das falsche Theme und haette das
echte freigegeben. Eine Sperre, die von Hand nachgezogen werden muss, ist
keine.

Lauf: python3 scripts/probe_wache.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).parent.parent / ".github/workflows/aufraeumen.yml"

# Der Pruefling wird aus dem Workflow gezogen, nicht hier abgeschrieben --
# eine Kopie wuerde bald etwas anderes pruefen als das, was wirklich laeuft.
w = yaml.safe_load(WORKFLOW.read_text())
skript = None
for s in w["jobs"]["aufraeumen"]["steps"]:
    if s.get("name", "").startswith("Ist das Ziel"):
        skript = s["run"].split("python3 - \"$THEME\" <<'PY'\n", 1)[1] \
                         .rsplit("\nPY", 1)[0]
if not skript:
    sys.exit("Der Schritt 'Ist das Ziel ...' fehlt im Workflow.")

ECHT = [
    {"id": 182665347395, "name": "Live", "role": "main"},
    {"id": 182664790339, "name": "Sandbox Ausbau", "role": "unpublished"},
    {"id": 182664626499, "name": "Umbau Conversion", "role": "unpublished"},
]

FAELLE = [
    # (Name, Inhalt von themen.json, Ziel-ID, soll durchgehen?)
    ("Ziel unveroeffentlicht (Normalfall)", {"themes": ECHT},
     "182664790339", True),
    ("Ziel IST das Live-Theme", {"themes": ECHT},
     "182665347395", False),
    # Genau der Fall, den die alte feste Nummer falsch herum behandelt hat.
    ("frueher fest gesperrte Nummer, heute unveroeffentlicht", {"themes": ECHT},
     "182664626499", True),
    ("Liste als blanke Liste statt unter 'themes'", ECHT,
     "182664790339", True),
    ("Feld 'live' statt 'role'",
     {"themes": [{"id": 1, "live": True}, {"id": 2, "live": False}]},
     "1", False),
    # Beide folgenden muessen abbrechen: eine Sperre, die bei unklarer
    # Lage durchwinkt, ist schlimmer als keine.
    ("kein Live-Theme erkennbar",
     {"themes": [{"id": 1, "role": "unpublished"}]}, "1", False),
    ("Ausgabe unlesbar", None, "182664790339", False),
]


def main() -> int:
    fehler = 0
    with tempfile.TemporaryDirectory() as ordner:
        pfad = Path(ordner)
        (pfad / "wache.py").write_text(skript)
        for name, inhalt, ziel, soll in FAELLE:
            (pfad / "themen.json").write_text(
                "Kein JSON, sondern eine CLI-Fehlermeldung" if inhalt is None
                else json.dumps(inhalt))
            p = subprocess.run([sys.executable, "wache.py", ziel],
                               cwd=pfad, capture_output=True, text=True)
            ging = p.returncode == 0
            if ging != soll:
                fehler += 1
            print(f"{'OK ' if ging == soll else 'FEHLER'}  {name:<52} "
                  f"erwartet={'durch' if soll else 'Abbruch':<8} "
                  f"tatsaechlich={'durch' if ging else 'Abbruch'}")
    print(f"\nFehlschlaege: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
