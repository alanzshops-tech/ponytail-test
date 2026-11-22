#!/usr/bin/env python3
"""
themecheck.py — wertet `shopify theme check --output json` aus.

Theme Check ist Shopifys eigener Linter für Liquid. Er prüft Dinge, die
kein Screenshot zeigt: nicht verwendete Snippets, fehlende Übersetzungen,
teure Schleifen, veraltete Filter, ungültige Schemata.

Bis heute ging das nicht, weil das Theme nicht als Dateien vorlag. Mit
dem Theme-Access-Token holt der Runner es und prüft es.

Aufruf:
    python3 scripts/themecheck.py --json daten/themecheck.json --pfad theme/live
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path

RANG = {"error": 0, "crash": 0, "warning": 1, "suggestion": 2,
        "style": 3, "info": 4}


def befunde(d) -> list[dict]:
    """Theme Check liefert eine Liste je Datei mit `offenses`. Der Aufbau
    kann sich ändern — deshalb defensiv suchen statt fest annehmen."""
    aus = []

    def wandern(x, datei=None):
        if isinstance(x, dict):
            pfad = x.get("path") or x.get("relativePath") or datei
            for o in (x.get("offenses") or []):
                if isinstance(o, dict):
                    aus.append({**o, "datei": o.get("path") or pfad})
            for v in x.values():
                wandern(v, pfad)
        elif isinstance(x, list):
            for v in x:
                wandern(v, datei)

    wandern(d)
    return aus


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="daten/themecheck.json")
    ap.add_argument("--pfad", default="theme/live")
    a = ap.parse_args()

    z = ["# Theme Check", "", f"Stand: {date.today()}", "",
         "Shopifys eigener Linter für Liquid, gelaufen über `"
         f"{a.pfad}`. Prüft, was kein Screenshot zeigt: ungültige "
         "Schemata, fehlende Übersetzungen, veraltete Filter, tote "
         "Snippets, teure Schleifen.", ""]

    p = Path(a.json)
    if not p.exists() or not p.stat().st_size:
        z += ["Keine Ergebnisdatei. Entweder ist der Lauf fehlgeschlagen "
              "oder der Token greift nicht — beides steht im Protokoll "
              "des Workflows.", ""]
        Path("THEMECHECK.md").write_text("\n".join(z) + "\n", encoding="utf-8")
        print("Keine Ergebnisdatei.")
        return

    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as e:
        z += [f"Ergebnisdatei ist kein gültiges JSON: {e}", ""]
        Path("THEMECHECK.md").write_text("\n".join(z) + "\n", encoding="utf-8")
        return

    offen = befunde(d)
    dateien = len(list(Path(a.pfad).rglob("*"))) if Path(a.pfad).exists() else 0
    z += [f"{dateien} Dateien im Theme, **{len(offen)} Befunde**.", ""]

    if not offen:
        z += ["Keine Beanstandungen. Das ist bei einem nahezu "
              "unveränderten Dawn zu erwarten — und genau deshalb ein "
              "brauchbarer Ausgangswert: Ab jetzt fällt jede neue "
              "Beanstandung auf.", ""]
        Path("THEMECHECK.md").write_text("\n".join(z) + "\n", encoding="utf-8")
        print("0 Befunde")
        return

    nach_regel = Counter(o.get("check") or o.get("rule") or "?" for o in offen)
    nach_schwere = Counter((o.get("severity") or "?") for o in offen)
    z += ["| Schwere | Anzahl |", "|---|---:|"]
    for s, n in sorted(nach_schwere.items(), key=lambda x: RANG.get(str(x[0]), 9)):
        z.append(f"| {s} | {n} |")
    z += ["", "## Nach Regel", "", "| Regel | Fälle |", "|---|---:|"]
    for regel, n in nach_rege_sorted(nach_regel):
        z.append(f"| `{regel}` | {n} |")

    z += ["", "## Die ersten 25 im Einzelnen", "",
          "| Datei | Zeile | Regel | Meldung |", "|---|---:|---|---|"]
    for o in sorted(offen, key=lambda x: RANG.get(str(x.get("severity")), 9))[:25]:
        datei = str(o.get("datei") or "?").replace(a.pfad + "/", "")
        zeile = (o.get("start_row") or o.get("startRow")
                 or (o.get("start") or {}).get("line") or "?")
        z.append(f"| `{datei}` | {zeile} | `{o.get('check') or o.get('rule')}` "
                 f"| {str(o.get('message', ''))[:90]} |")
    z.append("")

    Path("THEMECHECK.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    print(f"THEMECHECK.md — {len(offen)} Befunde")


def nach_rege_sorted(c: Counter):
    return sorted(c.items(), key=lambda x: -x[1])


if __name__ == "__main__":
    main()
