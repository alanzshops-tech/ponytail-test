#!/usr/bin/env python3
"""
dopplung.py — findet Szenen, die zweimal erzählt werden.

Wozu: Das Buch wechselt kapitelweise die Perspektive, und an einigen
Stellen erzählen beide Figuren denselben Abend. Das ist Absicht und es
trägt — solange es die Ausnahme bleibt. Wird es zur Gewohnheit, liest
man dieselbe Szene ein zweites Mal und legt das Buch weg, und bei Kindle
Unlimited wird nach gelesenen Seiten bezahlt.

Von Hand ist das nicht zu finden: Die Dopplungen stehen nicht
nebeneinander, sie sind umformuliert, und beim Lesen des zweiten
Kapitels hat man das erste nicht mehr Satz für Satz im Kopf.

Gemessen wird auf Absatzebene mit difflib. Verglichen werden nur Absätze
aus *verschiedenen* Kapiteln; eine Wiederholung im selben Kapitel ist
ein Stilmittel.

    python3 scripts/dopplung.py --selbsttest
    python3 scripts/dopplung.py --schwelle 0.55
"""

from __future__ import annotations

import argparse
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

BUCH = Path(__file__).resolve().parent.parent / "buch"


def kapitelnummer(p: Path) -> int:
    return int(re.match(r"kapitel-(\d+)\.md$", p.name).group(1))


def absaetze(text: str) -> list[str]:
    """Absätze ohne Überschrift, Trenner und Kurzzeilen.

    Unter zwölf Wörtern ist ein Absatz meistens eine Dialogzeile
    ("Ja.", "Ich weiß."). Die wiederholen sich in jedem Roman und sind
    kein Befund — sie würden den Bericht mit Rauschen füllen.
    """
    raus = []
    for a in re.split(r"\n\s*\n", text):
        a = a.strip()
        if not a or a.startswith("#") or a == "---":
            continue
        if len(a.split()) < 12:
            continue
        raus.append(" ".join(a.split()))
    return raus


def normalisieren(s: str) -> str:
    """Auf den Wortkern reduzieren.

    Satzzeichen und Kursive unterscheiden die beiden Fassungen oft
    stärker als der Inhalt. Und die Perspektive wechselt: "sagte ich"
    wird zu "sagte er". Deshalb fliegen die Pronomen raus — sonst findet
    das Gerät genau die Dopplungen nicht, um die es geht.
    """
    s = s.lower()
    s = re.sub(r"[^a-zäöüß ]", " ", s)
    weg = {"ich", "er", "sie", "mir", "mich", "ihm", "ihn", "ihr",
           "mein", "meine", "meinen", "sein", "seine", "seinen",
           "und", "der", "die", "das", "ein", "eine", "einen", "dem",
           "den", "hat", "habe", "war", "ist", "es", "in", "zu", "auf"}
    return " ".join(w for w in s.split() if w not in weg)


def paare(kapitel: dict[int, list[str]], schwelle: float,
          abstand: int) -> list[tuple]:
    treffer = []
    nummern = sorted(kapitel)
    for i, a in enumerate(nummern):
        for b in nummern[i + 1:]:
            if b - a > abstand:
                continue
            for pa in kapitel[a]:
                na = normalisieren(pa)
                if len(na.split()) < 8:
                    continue
                sa = set(na.split())
                for pb in kapitel[b]:
                    nb = normalisieren(pb)
                    if len(nb.split()) < 8:
                        continue
                    sb = set(nb.split())
                    # Vorfilter: ohne gemeinsame Wortmenge lohnt der
                    # teure Vergleich nicht.
                    if len(sa & sb) / max(len(sa | sb), 1) < schwelle * 0.6:
                        continue
                    q = SequenceMatcher(None, na, nb).ratio()
                    if q >= schwelle:
                        treffer.append((q, a, b, pa, pb))
    return sorted(treffer, reverse=True, key=lambda x: x[0])


def selbsttest() -> None:
    """Positiv- und Negativfall, sonst ist 'nichts gefunden' kein Befund."""
    a = ("Er hat ihn falsch gehalten, zu hoch, zu fest, mit einer Hand am "
         "Hinterkopf, so wie man einen Neugeborenen haelt.")
    b = ("Ich habe ihn falsch gehalten, zu hoch, zu fest, mit einer Hand "
         "am Hinterkopf, so wie man Neugeborene haelt.")
    c = ("Der Ofen braucht vierzig Minuten, bis die linke Seite so heiss "
         "ist wie die rechte, und er wird es nie ganz.")
    q_ab = SequenceMatcher(None, normalisieren(a), normalisieren(b)).ratio()
    q_ac = SequenceMatcher(None, normalisieren(a), normalisieren(c)).ratio()
    print(f"  Positivfall (dieselbe Szene, andere Perspektive): {q_ab:.2f}")
    print(f"  Negativfall (zwei fremde Absaetze):               {q_ac:.2f}")
    if q_ab < 0.75:
        sys.exit("Selbsttest: die bekannte Dopplung wird nicht erkannt.")
    if q_ac > 0.40:
        sys.exit("Selbsttest: fremde Absaetze gelten als Dopplung.")
    print("  Selbsttest bestanden.")


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schwelle", type=float, default=0.55)
    ap.add_argument("--abstand", type=int, default=4,
                    help="nur Kapitel vergleichen, die hoechstens so weit "
                         "auseinanderliegen")
    ap.add_argument("--selbsttest", action="store_true")
    ap.add_argument("--buch", default="buch",
                    help="Ordner mit Kapiteln (zweiter Band: --buch buch2)")
    a = ap.parse_args()

    global BUCH
    BUCH = Path(a.buch)

    print("Selbsttest:")
    selbsttest()
    if a.selbsttest:
        return

    kapitel = {}
    for p in sorted(BUCH.glob("kapitel-*.md"), key=kapitelnummer):
        kapitel[kapitelnummer(p)] = absaetze(p.read_text(encoding="utf-8"))
    print(f"\n{len(kapitel)} Kapitel, "
          f"{sum(len(v) for v in kapitel.values())} Absaetze.\n")

    t = paare(kapitel, a.schwelle, a.abstand)
    if not t:
        print("Keine Dopplungen ueber der Schwelle.")
        return

    print(f"{len(t)} Absatzpaare ab Aehnlichkeit {a.schwelle}:\n")
    for q, ka, kb, pa, pb in t:
        print(f"  {q:.2f}  Kapitel {ka} und {kb}")
        print(f"        {ka}: {pa[:110]}")
        print(f"        {kb}: {pb[:110]}\n")

    zaehler: dict[tuple[int, int], int] = {}
    for q, ka, kb, _, _ in t:
        zaehler[(ka, kb)] = zaehler.get((ka, kb), 0) + 1
    print("Kapitelpaare nach Anzahl doppelter Absaetze:")
    for (ka, kb), n in sorted(zaehler.items(), key=lambda x: -x[1]):
        print(f"  Kapitel {ka:>2} und {kb:>2}: {n}")


if __name__ == "__main__":
    main()
