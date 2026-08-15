#!/usr/bin/env python3
"""
einschieben.py — neue Kapitel einfügen und alles neu durchnummerieren.

Wozu: Ein Kapitel in der Mitte einzufügen heißt, alle folgenden
umzubenennen und in jeder Datei die Überschrift zu ändern. Von Hand ist
das die Sorte Arbeit, bei der genau ein Kapitel die falsche Nummer
bekommt und es niemandem auffällt — und in diesem Buch hängt an der
Nummer auch noch der Perspektivwechsel Leni/Jonas.

Neue Kapitel heißen `kapitel-<NN><buchstabe>.md` und werden hinter
`kapitel-<NN>.md` einsortiert: `kapitel-08a.md` und `kapitel-08b.md`
kommen also hinter Kapitel 8, in dieser Reihenfolge.

Das Skript benennt um, schreibt die Überschriften neu und prüft danach,
ob die Perspektive noch abwechselt. Stimmt sie nicht, wird nichts
geschrieben.

    python3 scripts/einschieben.py --probe   # nur zeigen, was passiert
    python3 scripts/einschieben.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BUCH = Path(__file__).resolve().parent.parent / "buch"


def sortierschluessel(p: Path) -> tuple[int, str]:
    m = re.match(r"kapitel-(\d+)([a-z]?)\.md$", p.name)
    if not m:
        raise ValueError(p.name)
    return int(m.group(1)), m.group(2)


def figur(text: str) -> str | None:
    kopf = text.lstrip().split("\n", 1)[0]
    m = re.search(r"—\s*(\w+)", kopf)
    return m.group(1) if m else None


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--probe", action="store_true",
                   help="nur anzeigen, nichts schreiben")
    args = p.parse_args()

    dateien = sorted(BUCH.glob("kapitel-*.md"), key=sortierschluessel)
    if not dateien:
        sys.exit("Keine Kapitel gefunden.")

    plan = []
    for neu_nr, alt in enumerate(dateien, start=1):
        text = alt.read_text(encoding="utf-8")
        f = figur(text)
        plan.append({"alt": alt, "neu_nr": neu_nr, "figur": f,
                     "text": text})

    # Perspektivwechsel pruefen, BEVOR irgendetwas umbenannt wird.
    klagen = []
    for i in range(1, len(plan)):
        a, b = plan[i - 1]["figur"], plan[i]["figur"]
        if a and b and a == b:
            klagen.append(f"Kapitel {plan[i]['neu_nr']} "
                          f"({plan[i]['alt'].name}): zweimal {b} "
                          f"hintereinander")
        if not b:
            klagen.append(f"{plan[i]['alt'].name}: keine Figur in der "
                          f"Überschrift erkennbar")

    breite = max(len(x["alt"].name) for x in plan)
    for x in plan:
        ziel = f"kapitel-{x['neu_nr']:02d}.md"
        marke = "  " if x["alt"].name == ziel else "->"
        print(f"  {x['alt'].name:<{breite}} {marke} {ziel:<14} "
              f"{x['figur']}")

    if klagen:
        print(f"\n{len(klagen)} Beanstandung(en) — es wird nichts "
              f"geschrieben:")
        for k in klagen:
            print(f"  - {k}")
        sys.exit(2)
    print("\nPerspektivwechsel in Ordnung.")

    if args.probe:
        return

    # Erst alles auf Zwischennamen, sonst überschreibt kapitel-09a.md
    # beim Umbenennen die noch nicht verschobene kapitel-10.md.
    for x in plan:
        zwischen = BUCH / f"_um_{x['neu_nr']:03d}.md"
        neuer_kopf = re.sub(r"^#\s*Kapitel\s*\d+",
                            f"# Kapitel {x['neu_nr']}",
                            x["text"], count=1)
        zwischen.write_text(neuer_kopf, encoding="utf-8")
        x["alt"].unlink()

    for x in plan:
        (BUCH / f"_um_{x['neu_nr']:03d}.md").rename(
            BUCH / f"kapitel-{x['neu_nr']:02d}.md")

    print(f"{len(plan)} Kapitel neu durchnummeriert.")


if __name__ == "__main__":
    main()
