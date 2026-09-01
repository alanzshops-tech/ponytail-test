#!/usr/bin/env python3
"""abfolge.py — misst die Reihenfolge, nicht die Güte der einzelnen Szene.

Der Vorwurf, den dieses Gerät prüfen soll: *Die einzelnen Kapitel sind
gut. Das Problem ist die Abfolge.* Im Bereich 36–45 laufe immer dasselbe
Muster — berufliches Problem, Gespräch, Dokument, Sitzung, neue
Information, Reaktion —, und der Leser wisse irgendwann, wie der Roman
funktioniert.

Kein vorhandenes Werkzeug kann das sehen. `romantik.py` zählt Berührung
je Kapitel, `prosa.py` misst Sätze, `manier.py` sucht Gussformen. Alle
drei bewerten **Stellen**. Gleichförmigkeit ist aber keine Eigenschaft
einer Stelle, sondern einer Folge: Drei gute Sachszenen hintereinander
sind drei gute Szenen und trotzdem ein Problem.

**Zwei Messungen, und die erste hat sich als die falsche erwiesen.**

1. *Dichte und Lauflänge.* Wie viele sachliche Szenen folgen ohne eine
   private dazwischen? Ergebnis: 36–45 hat die **kürzesten** Ketten und
   den **höchsten** Privatanteil im ganzen Buch. Das war richtig
   gerechnet und ging an der Frage vorbei — beanstandet war nicht, wie
   viel Sachliches vorkommt, sondern dass man den Ablauf vorhersagen
   kann.

2. *Die Eröffnungsformel.* Vorhersagbarkeit fängt beim ersten Satz an.
   In K01–10 kommen Menschen zur Tür herein (*„Sabine Reinhardt kam um
   achtzehn Uhr dreißig durch meine Tür"*). In K36–45 beginnt das
   Kapitel mit einem Datum und oft mit einem Dokument als Subjekt
   (*„Die Bekanntmachung ist am zweiten April herausgegangen"*). Das
   ist der messbare Unterschied — 70 gegen 30 Prozent.

Beide Messungen bleiben stehen, auch die widerlegte: Wer später fragt,
ob es an der Dichte liegt, soll die Antwort finden, ohne sie neu
herzuleiten.

Der Bezugsrahmen: Verglichen wird gegen die Blöcke, die als tragend
gelten — 1–10 („starker Sog") und 11–35 („funktionieren gut"). Eine
Zahl für 36–45 allein sagt nichts.

Kalibriert an den zwei Kapiteln, deren Verfahrensdichte in Phase 1 von
Hand nachgerechnet wurde: **K13 = 15,1** (höchste, muss SACH sein) und
**K17 = 1,0** (niedrigste, darf nicht SACH sein).

Aufruf:
    python3 scripts/abfolge.py --selbsttest
    python3 scripts/abfolge.py --buch buch2
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chronik import DATUM_WORT                 # noqa: E402
from manier import szenen                      # noqa: E402
from romantik import BERUEHRUNG, SEHNSUCHT     # noqa: E402

# Verfahren, Dokument, Sitzung. Nur Begriffe, die ohne Kontext
# eindeutig aus der Amtswelt stammen -- "Termin" und "Frage" stehen
# bewusst NICHT hier, die kommen auch am Küchentisch vor.
SACHLICH = re.compile(
    r"\b(Vergabe\w*|Verfahren\w*|Gutachten\w*|Gutachter\w*|Bescheid\w*|"
    r"Antrag\w*|Anträge\w*|Frist\w*|Akte\w*|Aktenvermerk\w*|Vermerk\w*|"
    r"Protokoll\w*|Sitzung\w*|Beirat\w*|Vorlage\w*|Ziffer\w*|"
    r"Paragraf\w*|Widerspruch\w*|Widersprüche\w*|Auflage\w*|"
    r"Behörde\w*|Vergabekammer\w*|Anwalt|Anwälte\w*|Kanzlei\w*|"
    r"Anlage\w*|Schriftsatz\w*|Stellungnahme\w*|Beschluss\w*|"
    r"Genehmigung\w*|Zuständigkeit\w*|Ausschreibung\w*|Bieter\w*|"
    r"Auftraggeber\w*|Messreihe\w*|Baustopp\w*|Denkmalschutz\w*|"
    r"Aufenthaltserlaubnis\w*|Ausländerbehörde\w*|Niederschrift\w*|"
    r"Unterlagen|zugeleitet|gegengezeichnet|beantragt|erteilt)", re.I)

# Das Private im engeren Sinn. Die ersten beiden Muster stammen aus
# romantik.py, sind also schon kalibriert.
ORT_PRIVAT = re.compile(
    r"\b(Bett\b|Schlafzimmer|Küchentisch|Küchenboden|Sofa\b|Badezimmer|"
    r"Wanne\w*|aufgewacht|eingeschlafen|Frühstück\w*|zugedeckt|"
    r"Decke\b|Kissen\b|barfuß|Bademantel)", re.I)

# Treffer je 100 Wörter, ab dem eine Szene als sachlich bzw. privat
# gilt. An K13/K17 geeicht, siehe selbsttest().
SCHWELLE = 0.8

DOKSUBJEKT = re.compile(
    r"^(?:Die|Der|Das)\s+(Bekanntmachung|Angebote?|Beschlussvorlage|"
    r"Vorlage|Beirat|Bescheid|Antrag|Frist|Akte|Sitzung|Vergabe\w*|"
    r"Gutachten|Protokoll|Schreiben|Brief|Unterlagen|Widerspruch|"
    r"Auflage|Termin)")
WOCHENTAG = re.compile(r"\b(Montag|Dienstag|Mittwoch|Donnerstag|Freitag|"
                       r"Samstag|Sonntag)\b")

BLOECKE = [("K01-10  starker Sog", 1, 10),
           ("K11-35  funktioniert", 11, 35),
           ("K36-45  beanstandet", 36, 45),
           ("K46-64  Schluss", 46, 64)]


def dichte(rx, text: str) -> float:
    return 100.0 * len(rx.findall(text)) / max(1, len(text.split()))


def privatwert(text: str) -> float:
    return (dichte(BERUEHRUNG, text) + dichte(SEHNSUCHT, text)
            + dichte(ORT_PRIVAT, text))


def typ(text: str) -> str:
    """SACH, PRIVAT oder NEUTRAL."""
    s, p = dichte(SACHLICH, text), privatwert(text)
    if s >= SCHWELLE and s > p:
        return "SACH"
    if p >= SCHWELLE and p > s:
        return "PRIVAT"
    return "NEUTRAL"


def szenentypen(text: str) -> list[str]:
    return [typ("\n\n".join(s)) for s in szenen(text)]


def laeufe(folge: list[str]) -> list[int]:
    """Ketten aus SACH ohne PRIVAT dazwischen.

    NEUTRAL unterbricht nicht: Eine Szene ohne Amtsdeutsch und ohne
    Berührung ist keine Erholung von der Sachlichkeit, sie ist nur keine
    Sachszene. Genau darum geht der Vorwurf -- es fehlt das ausdrücklich
    Private zwischen den Vorgängen.
    """
    aus, lauf = [], 0
    for t in folge:
        if t == "SACH":
            lauf += 1
        elif t == "PRIVAT":
            if lauf:
                aus.append(lauf)
            lauf = 0
    if lauf:
        aus.append(lauf)
    return aus


def erster_satz(text: str) -> str:
    t = re.sub(r"^#.*$", "", text, flags=re.M).strip()
    return re.split(r"(?<=[.!?“])\s", " ".join(t.split()))[0]


def eroeffnung(text: str) -> tuple[bool, bool]:
    """(beginnt mit einem Datum, Dokument als Subjekt)"""
    s = erster_satz(text)
    return (bool(DATUM_WORT.search(s)) or bool(WOCHENTAG.search(s)),
            bool(DOKSUBJEKT.match(s)))


def selbsttest(buch: str = "buch2") -> None:
    fehler = []
    ordner = Path(buch)

    if ordner.exists():
        k13 = (ordner / "kapitel-13.md").read_text(encoding="utf-8")
        k17 = (ordner / "kapitel-17.md").read_text(encoding="utf-8")
        d13, d17 = dichte(SACHLICH, k13), dichte(SACHLICH, k17)
        if not d13 > d17 * 3:
            fehler.append(f"K13 ({d13:.2f}) muss deutlich sachlicher sein "
                          f"als K17 ({d17:.2f})")
        if typ(k13) != "SACH":
            fehler.append(f"K13 nicht als SACH erkannt: {typ(k13)}")
        if typ(k17) == "SACH":
            fehler.append("K17 fälschlich als SACH erkannt")

    privat = ("Sie hat die Hand auf meinen Nacken gelegt, und wir sind "
              "im Bett liegen geblieben, bis es hell war.")
    if typ(privat) != "PRIVAT":
        fehler.append(f"Privatfall nicht erkannt: {typ(privat)}")
    sach = ("Der Bescheid der Vergabekammer kam mit vierzehn Auflagen, "
            "und der Anwalt hat eine Stellungnahme zur Akte gereicht.")
    if typ(sach) != "SACH":
        fehler.append(f"Sachfall nicht erkannt: {typ(sach)}")
    neutral = ("Er ist die Treppe hinuntergegangen und hat unten kurz "
               "gewartet, weil der Regen stärker geworden war.")
    if typ(neutral) != "NEUTRAL":
        fehler.append(f"Neutralfall falsch: {typ(neutral)}")

    if laeufe(["SACH", "SACH", "PRIVAT", "SACH"]) != [2, 1]:
        fehler.append("Lauflängen falsch gerechnet")
    if laeufe(["SACH", "NEUTRAL", "SACH"]) != [2]:
        fehler.append("NEUTRAL darf die Kette nicht unterbrechen")

    # Eroeffnungsformel: je ein echter Positiv- und Negativfall.
    if eroeffnung("# X\n\nDie Bekanntmachung ist am zweiten April "
                  "herausgegangen, elf Seiten.") != (True, True):
        fehler.append("Eröffnung mit Datum+Dokument nicht erkannt")
    if eroeffnung("# X\n\nEin Riss ist harmlos, solange er sich nicht "
                  "bewegt.") != (False, False):
        fehler.append("Eröffnungsmuster fängt zu viel")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  bestanden (K13/K17 aus Phase 1; gestellter Privat-, Sach- "
          "und Neutralfall; Lauflängen; Eröffnung positiv und negativ).")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--buch", default="buch2")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    selbsttest(a.buch)
    if a.selbsttest:
        return

    ordner = Path(a.buch)
    je_kapitel = {}
    for f in sorted(ordner.glob("kapitel-*.md")):
        nr = int(re.search(r"(\d+)", f.name).group(1))
        t = f.read_text(encoding="utf-8")
        je_kapitel[nr] = (szenentypen(t), dichte(SACHLICH, t),
                          privatwert(t), eroeffnung(t))

    print("\n=== Szenentypen je Kapitel (S=sachlich, P=privat, ·=neutral) "
          "===\n")
    for nr in sorted(je_kapitel):
        ty, ds, dp, _ = je_kapitel[nr]
        bild = "".join({"SACH": "S", "PRIVAT": "P"}.get(x, "·") for x in ty)
        print(f"  K{nr:02d}  {bild:<14s}  sachlich {ds:5.2f}  privat {dp:5.2f}")

    print("\n=== Messung 1: Ketten sachlicher Szenen (widerlegt den "
          "Vorwurf) ===\n")
    for name, von, bis in BLOECKE:
        teil = []
        for nr in range(von, bis + 1):
            if nr in je_kapitel:
                teil += je_kapitel[nr][0]
        lf = laeufe(teil)
        sach = 100 * sum(1 for x in teil if x == "SACH") / max(1, len(teil))
        pri = 100 * sum(1 for x in teil if x == "PRIVAT") / max(1, len(teil))
        print(f"  {name:24s} längste Kette {max(lf) if lf else 0:2d} | "
              f"sachlich {sach:4.1f} % | privat {pri:4.1f} %")

    print("\n=== Messung 2: Eröffnungsformel (bestätigt ihn) ===\n")
    for name, von, bis in BLOECKE:
        dat = dok = n = 0
        for nr in range(von, bis + 1):
            if nr not in je_kapitel:
                continue
            n += 1
            d, k = je_kapitel[nr][3]
            dat += d
            dok += k
        print(f"  {name:24s} Datum im 1. Satz {dat:2d}/{n:2d} = "
              f"{100*dat/max(1,n):3.0f} % | Dokument als Subjekt "
              f"{dok:2d}/{n:2d} = {100*dok/max(1,n):3.0f} %")

    print("\n=== Kapitel in 36-45, die mit Datum oder Dokument öffnen ===\n")
    for nr in range(36, 46):
        if nr not in je_kapitel:
            continue
        d, k = je_kapitel[nr][3]
        if d or k:
            s = erster_satz((ordner / f"kapitel-{nr:02d}.md")
                            .read_text(encoding="utf-8"))
            marke = ("Dokument+Datum" if d and k else
                     "Dokument" if k else "Datum")
            print(f"  K{nr:02d} [{marke:14s}] {s[:88]}")


if __name__ == "__main__":
    main()
