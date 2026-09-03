#!/usr/bin/env python3
"""
stichprobe.py — wie viele Besucher ein A/B-Test wirklich braucht.

Der Grund für dieses Skript: „Wissenschaftlich" heißt im E-Commerce
zuerst *Stichprobenrechnung*, nicht Werkzeugauswahl. Wer einen Test nach
200 Besuchern abbricht, weil eine Variante vorn liegt, misst Rauschen und
nennt es Erkenntnis. Das ist der häufigste Fehler der Branche, und er
kostet mehr als jedes fehlende Werkzeug.

Die Formel ist die übliche Näherung für den Vergleich zweier Anteile,
zweiseitig, mit Stetigkeitskorrektur weggelassen:

    n je Gruppe = (z(1-α/2)·√(2·p̄·(1-p̄)) + z(1-β)·√(p₁q₁ + p₂q₂))² / (p₂-p₁)²

Ausgegeben wird zusätzlich, wie lange das bei einer gegebenen Zahl von
Besuchern je Tag dauert — die Zahl, die die Entscheidung trifft.

Aufruf:
    python3 scripts/stichprobe.py --basis 2 --hebung 20 --besucher-tag 50
    python3 scripts/stichprobe.py --basis 2 --hebung 20 --besucher-tag 0
"""

from __future__ import annotations

import argparse
import math

# Normalquantile. Ohne scipy, damit das Skript überall läuft.
Z = {0.80: 0.8416, 0.90: 1.2816, 0.95: 1.6449, 0.975: 1.9600, 0.99: 2.3263}


def n_je_gruppe(p1: float, p2: float, alpha: float = 0.05,
                power: float = 0.80) -> int:
    z_a = Z[round(1 - alpha / 2, 3)]
    z_b = Z[power]
    pq = p1 * (1 - p1) + p2 * (1 - p2)
    pm = (p1 + p2) / 2
    zaehler = (z_a * math.sqrt(2 * pm * (1 - pm)) + z_b * math.sqrt(pq)) ** 2
    return math.ceil(zaehler / (p2 - p1) ** 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", type=float, default=2.0,
                    help="heutige Conversion in Prozent")
    ap.add_argument("--hebung", type=float, default=20.0,
                    help="gesuchte relative Verbesserung in Prozent")
    ap.add_argument("--besucher-tag", type=float, default=0.0,
                    dest="besucher_tag")
    ap.add_argument("--power", type=float, default=0.80)
    ap.add_argument("--alpha", type=float, default=0.05)
    a = ap.parse_args()

    p1 = a.basis / 100
    p2 = p1 * (1 + a.hebung / 100)
    n = n_je_gruppe(p1, p2, a.alpha, a.power)
    gesamt = 2 * n

    print(f"Ausgangs-Conversion   {a.basis:g} %")
    print(f"Gesuchte Verbesserung {a.hebung:g} % relativ "
          f"(also auf {p2 * 100:.2f} %)")
    print(f"Signifikanz {(1 - a.alpha) * 100:g} %, Trennschärfe "
          f"{a.power * 100:g} %\n")
    print(f"  Besucher je Variante : {n:,}".replace(",", "."))
    print(f"  Besucher insgesamt   : {gesamt:,}".replace(",", "."))

    if a.besucher_tag > 0:
        tage = gesamt / a.besucher_tag
        print(f"\nBei {a.besucher_tag:g} Besuchern am Tag: "
              f"**{tage:.0f} Tage** ({tage / 30.4:.1f} Monate)")
        if tage > 60:
            print("\nÜber zwei Monate. In der Zeit ändern sich Saison, "
                  "Sortiment und Werbung — der Test misst dann nicht mehr "
                  "nur die Variante. Bei so wenig Verkehr sind gemessene "
                  "Mängel (Tempo, Fehler, Lesbarkeit) die bessere "
                  "Entscheidungsgrundlage als ein A/B-Test.")
    else:
        print("\nOhne Besucher ist kein Test möglich. Jede Aussage über "
              "Conversion bleibt bis dahin eine Hypothese aus der "
              "Fachliteratur — brauchbar, aber nicht belegt.")

    print("\nZum Vergleich, gleiche Ausgangslage:")
    for h in (5, 10, 20, 50, 100):
        m = n_je_gruppe(p1, p1 * (1 + h / 100), a.alpha, a.power)
        zeile = f"  +{h:3d} % relativ -> {2 * m:>10,} Besucher".replace(",", ".")
        if a.besucher_tag > 0:
            zeile += f"  ({2 * m / a.besucher_tag / 30.4:>6.1f} Monate)"
        print(zeile)


if __name__ == "__main__":
    main()
