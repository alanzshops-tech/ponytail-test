#!/usr/bin/env python3
"""chronik.py — prueft die Zeitachse, nicht den Wochentag.

`kalender.py` prueft, ob "am achtzehnten Mai, einem Montag" stimmt. Das
kann es nur, wo ein Wochentag dabeisteht: **12 von 142 Datumsangaben**
in Band 2. Die anderen 130 meldet es ehrlich als "nicht pruefbar" — und
genau darin sass der Heiligabend-Fehler ein halbes Jahr lang, weil in
Kapitel 32 kein Wochentag steht.

Diese 130 Angaben sind aber pruefbar, nur anders: **Die Kapitel laufen
in der Zeit vorwaerts.** Ein Datum in Kapitel 30 darf nicht vor einem
Datum in Kapitel 20 liegen. Wo es das tut, ist entweder das Datum
falsch, die Jahrestafel falsch, oder es ist eine Rueckblende — und
Rueckblenden erkennt man daran, dass sie es sagen.

Der Bezugsrahmen — ohne den eine Messung keine ist:

  Gemessen wird die *Reihenfolge*, nicht die Wahrheit. Ein Treffer sagt
  nicht "dieses Datum ist falsch", sondern "diese zwei Angaben koennen
  nicht beide stimmen". Welche der beiden nachgibt, entscheidet ein
  Mensch am Text.

Zweite Pruefung: **Zeitspannen.** "seit vierzehn Monaten", "vor drei
Jahren", "achtundzwanzig Jahre". Das Buch hat davon vier Sorten, und
drei davon sind schon einmal eingefroren, waehrend die Handlung
weiterlief (die "fuenfzehn Monate" von K12 bis K24, Wendlands
"vierunddreissig Jahre", die "achtundzwanzig Jahre" in K44/K58/K63).
Eine Zahl, die stillsteht, waehrend der Kalender laeuft, ist der
haeufigste inhaltliche Fehler in diesem Buch gewesen.

Aufruf:
    python3 scripts/chronik.py --selbsttest
    python3 scripts/chronik.py --buch buch2
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kalender import JAHR, MONAT, TAG, kapitelnummer, jahr_fuer  # noqa: E402

MONATE = "|".join(MONAT)
TAGWORT = r"[a-zäöüß]+(?:sten|ten)"

# "am achtzehnten Mai", "im Mai 2027", "am 4. August"
DATUM_WORT = re.compile(rf"\b[Aa]m (?P<tag>{TAGWORT})\s+(?P<monat>{MONATE})\b"
                        r"(?:\s+(?P<jahr>(?:19|20)\d{2}))?")
DATUM_ZIFFER = re.compile(r"\b(?P<tag>\d{1,2})\.\s*(?P<monat>\d{1,2})\."
                          r"(?P<jahr>(?:19|20)\d{2})\b")

# Eine Rueckblende sagt es. Aber sie sagt es in *ihrem* Teilsatz, nicht
# irgendwo im Satz: In K46 steht "Wir haben am achtundzwanzigsten
# November ... in einem Hotelzimmer gestanden, weil das Hotel von
# damals abgerissen worden ist". Das "damals" gehoert zum Hotel, nicht
# zum Datum -- die satzweite Suche hat deshalb das echte Szenendatum
# verworfen und ein Datum aus einem Konditionalsatz zum spaetesten des
# Kapitels gemacht. Gesucht wird jetzt im Fenster *vor* dem Datum, bis
# zum naechsten Komma.
RUECKBLENDE = re.compile(
    r"\b(damals|vorletzt\w*|im Jahr zuvor|ein Jahr (?:zuvor|davor)|"
    r"letztes Jahr|im letzten|seinerzeit|frueher|früher|"
    r"(?:19|20)\d{2})\b", re.I)

# Ein Datum im Konjunktiv ist kein Szenendatum: "Dann haette ich am
# neunten Juni abgesagt" beschreibt, was *nicht* passiert ist.
KONJUNKTIV = re.compile(
    r"\b(hätte|hätten|wäre|wären|würde|würden|sollte|müsste|"
    r"könnte|wenn ich|wenn du|wenn er|wenn sie)\b", re.I)


def teilsatz_vor(text: str, i: int, weite: int = 60) -> str:
    """Bis zu `weite` Zeichen vor dem Datum, hoechstens bis zum Satzanfang.

    Nur rueckwaerts, und das ist der Punkt. "Damals, am dritten Juni"
    markiert das Datum; das "damals" in K46 steht *hinter* dem Datum und
    gehoert zu einem anderen Satzglied. Ein Fenster bis zum letzten
    Komma war zu eng (bei "Damals," faellt der Marker gerade heraus),
    ein ganzer Satz zu weit. Beide Faelle stehen im Selbsttest.
    """
    a = max(0, i - weite)
    schnitt = max(text.rfind(".", a, i), text.rfind("\n", a, i))
    return text[schnitt + 1 if schnitt >= 0 else a: i]

ZAHLWORT = {
    "einem": 1, "einer": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5,
    "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11,
    "zwölf": 12, "dreizehn": 13, "vierzehn": 14, "fünfzehn": 15,
    "sechzehn": 16, "siebzehn": 17, "achtzehn": 18, "neunzehn": 19,
    "zwanzig": 20, "einundzwanzig": 21, "zweiundzwanzig": 22,
    "dreiundzwanzig": 23, "vierundzwanzig": 24, "fünfundzwanzig": 25,
    "sechsundzwanzig": 26, "siebenundzwanzig": 27, "achtundzwanzig": 28,
    "neunundzwanzig": 29, "dreißig": 30, "einunddreißig": 31,
    "zweiunddreißig": 32, "dreiunddreißig": 33, "vierunddreißig": 34,
}
SPANNE = re.compile(
    r"\b(?:seit|vor|seit über|seit fast)\s+(?P<zahl>" +
    "|".join(sorted(ZAHLWORT, key=len, reverse=True)) +
    r")\s+(?P<einheit>Monaten|Monate|Jahren|Jahre|Wochen)\b", re.I)


def datum_treffer(text: str, jahr: int):
    """Alle Datumsangaben eines Kapitels als (datum, zitat, rueckblende)."""
    aus = []
    for m in DATUM_WORT.finditer(text):
        tag = TAG.get(m.group("tag"))
        monat = MONAT.get(m.group("monat"))
        if not tag or not monat:
            continue
        j = int(m.group("jahr")) if m.group("jahr") else jahr
        vor = teilsatz_vor(text, m.start())
        # Nennt das Datum sein Jahr selbst und ist es nicht das Jahr des
        # Kapitels, dann wird zurueckverwiesen -- "am vierzehnten Maerz
        # 2025" ist in K52 die Hochzeit in Kopenhagen, keine Szene. Der
        # Jahresmarker steht hier *hinter* den Datumswoertern und faellt
        # deshalb nicht ins Rueckwaertsfenster.
        kein_szenendatum = bool(RUECKBLENDE.search(vor)) or \
            bool(KONJUNKTIV.search(vor)) or j != jahr
        try:
            aus.append((date(j, monat, tag), m.group(0), kein_szenendatum))
        except ValueError:
            aus.append((None, m.group(0), False))      # 31. Februar o. ae.
    return aus


def satz_um(text: str, i: int) -> str:
    a = text.rfind(".", 0, i) + 1
    b = text.find(".", i)
    return text[a: b if b > 0 else len(text)]


def spannen(text: str):
    for m in SPANNE.finditer(text):
        n = ZAHLWORT[m.group("zahl").lower()]
        yield n, m.group("einheit").lower(), m.group(0)


def selbsttest() -> None:
    fehler = []

    # Datumserkennung, Positiv- und Negativfall.
    t = datum_treffer("Sie kam am achtzehnten Mai zurück.", 2026)
    if not t or t[0][0] != date(2026, 5, 18):
        fehler.append(f"Datum nicht erkannt: {t}")
    if datum_treffer("Sie kam am Morgen zurück.", 2026):
        fehler.append("Datumsmuster faengt zu viel.")

    # Jahreszahl im Satz schlaegt die Tafel.
    t = datum_treffer("Er hat am dritten Juni 2019 angefangen.", 2026)
    if not t or t[0][0] != date(2019, 6, 3):
        fehler.append(f"Jahreszahl im Satz ignoriert: {t}")

    # Rueckblende wird als solche erkannt -- sonst meldet jede
    # Erinnerung einen Reihenfolgefehler.
    t = datum_treffer("Damals, am dritten Juni, war das anders.", 2026)
    if not t or not t[0][2]:
        fehler.append(f"Rueckblende nicht erkannt: {t}")
    t = datum_treffer("Sie kam am dritten Juni und blieb.", 2026)
    if t and t[0][2]:
        fehler.append("Rueckblendenmuster faengt zu viel.")

    # Die beiden Faelle aus K46, an denen die satzweite Suche
    # gescheitert ist -- ein "damals" in einem anderen Teilsatz darf
    # das Szenendatum nicht verwerfen, ein Konjunktiv muss es.
    t = datum_treffer("Wir haben am achtundzwanzigsten November dort "
                      "gestanden, weil das Hotel von damals abgerissen "
                      "worden ist.", 2027)
    if not t or t[0][2]:
        fehler.append(f"'damals' im Nebensatz verwirft das Datum: {t}")
    t = datum_treffer("Dann hätte ich am neunten Juni abgesagt.", 2027)
    if not t or not t[0][2]:
        fehler.append(f"Konjunktivdatum nicht als solches erkannt: {t}")

    # Eigenes Jahr, das nicht das Kapiteljahr ist: Rueckverweis.
    t = datum_treffer("Wir haben am vierzehnten März 2025 geheiratet.", 2028)
    if not t or not t[0][2]:
        fehler.append(f"Fremdes Jahr nicht als Rueckverweis erkannt: {t}")
    t = datum_treffer("Wir sind am vierzehnten März 2028 hingefahren.", 2028)
    if not t or t[0][2]:
        fehler.append(f"Eigenes Jahr faelschlich als Rueckverweis: {t}")

    # Ungueltiges Datum faellt auf.
    t = datum_treffer("Am einunddreißigsten Februar kam die Post.", 2026)
    if not t or t[0][0] is not None:
        fehler.append(f"Ungueltiges Datum nicht gemeldet: {t}")

    # Zeitspannen, Positiv- und Negativfall.
    s = list(spannen("Sie sind seit vierzehn Monaten verheiratet."))
    if s != [(14, "monaten", "seit vierzehn Monaten")]:
        fehler.append(f"Spanne nicht erkannt: {s}")
    if list(spannen("Sie sind seit Monaten verheiratet.")):
        fehler.append("Spannenmuster faengt zu viel.")

    # Die Reihenfolgepruefung selbst, an einem gestellten Fall.
    kap = {10: [(date(2026, 5, 1), "am ersten Mai", False)],
           20: [(date(2026, 3, 1), "am ersten März", False)]}
    if not reihenfolge(kap):
        fehler.append("Reihenfolgepruefung meldet den Rueckschritt nicht.")
    # Blosser Rueckverweis darf NICHT melden: K20 spielt spaeter und
    # nennt nebenbei ein frueheres Datum. Genau diese zehn Faelle hat
    # die erste Fassung faelschlich gezaehlt.
    kap = {10: [(date(2026, 3, 1), "am ersten März", False)],
           20: [(date(2026, 2, 1), "am ersten Februar", False),
                (date(2026, 5, 1), "am ersten Mai", False)]}
    if reihenfolge(kap):
        fehler.append("Rueckverweis wird faelschlich als Zeitsprung "
                      "gezaehlt.")
    kap = {10: [(date(2026, 3, 1), "am ersten März", False)],
           20: [(date(2026, 5, 1), "am ersten Mai", False)]}
    if reihenfolge(kap):
        fehler.append("Reihenfolgepruefung meldet eine saubere Achse.")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  Selbsttest bestanden (Datum, Jahr im Satz, Rueckblende, "
          "ungueltiges Datum, Spanne, Reihenfolge — je Positiv "
          "und Negativ).")


def reihenfolge(kapitel: dict) -> list:
    """Laeuft die Erzaehlzeit vorwaerts?

    Gemessen wird das **spaeteste** Datum je Kapitel, nicht das
    frueheste. Grund: Ein Kapitel nennt staendig zurueckliegende Daten
    ("zu meinem Bruder, am achten Mai"), ohne dort zu spielen. Die
    erste Fassung nahm das frueheste Datum und meldete deshalb 14
    Stellen, von denen 10 blosse Rueckverweise waren -- ein Selektor,
    der jede Erinnerung als Zeitsprung zaehlt, misst nicht die
    Zeitachse, sondern die Erzaehlweise.

    Bleibt der Rest: echte Rueckschritte. Auch die sind nicht
    zwangslaeufig Fehler -- die Kapitel wechseln die Perspektive, und
    zwei Blickwinkel auf dieselbe Woche duerfen sich ueberlappen.
    Deshalb ist die Ueberlappung mit ausgewiesen und nicht als
    Beanstandung gezaehlt.
    """
    klagen, hoechst, woher = [], None, None
    for nr in sorted(kapitel):
        echte = [(d, z) for d, z, rueck in kapitel[nr] if d and not rueck]
        if not echte:
            continue
        groesst = max(echte)
        if hoechst and groesst[0] < hoechst:
            klagen.append((nr, groesst[1], groesst[0], woher, hoechst,
                           (hoechst - groesst[0]).days))
        if hoechst is None or groesst[0] > hoechst:
            hoechst, woher = groesst[0], nr
    return klagen


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--buch", default="buch2")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return

    ordner = Path(a.buch)
    kapitel, ungueltig, alle_spannen = {}, [], []
    ohne_jahr = []
    for f in sorted(ordner.glob("kapitel-*.md")):
        nr = kapitelnummer(f)
        jahr = jahr_fuer(ordner.name, nr)
        if jahr is None:
            ohne_jahr.append(nr)
            continue
        t = f.read_text(encoding="utf-8")
        treffer = datum_treffer(t, jahr)
        kapitel[nr] = treffer
        ungueltig += [(nr, z) for d, z, _ in treffer if d is None]
        alle_spannen += [(nr, n, e, z) for n, e, z in spannen(t)]

    gesamt = sum(len(v) for v in kapitel.values())
    rueck = sum(1 for v in kapitel.values() for _, _, r in v if r)
    print(f"\n{gesamt} Datumsangaben in {len(kapitel)} Kapiteln erfasst "
          f"({rueck} als Rückblende ausgenommen).")
    if ohne_jahr:
        print(f"WARNUNG: kein Jahr in der Tafel für Kapitel {ohne_jahr}")

    print("\n=== Ungültige Kalenderdaten ===")
    for nr, z in ungueltig:
        print(f"  K{nr:02d}  {z}")
    print("  keine" if not ungueltig else "")

    print("\n=== Zeitachse: Datum liegt vor einem früheren Kapitel ===")
    klagen = reihenfolge(kapitel)
    for nr, zitat, d, vor_nr, vor_d, tage in klagen:
        print(f"  K{nr:02d}  spielt bis {d} ({zitat!r}) — K{vor_nr:02d} "
              f"stand schon bei {vor_d}, also {tage} Tage zurück")
    print("  keine" if not klagen else "")

    # Eine Jahresangabe zeigt auf ein Ankerjahr: Kapiteljahr minus n.
    # Meint dieselbe Angabe in zwei Kapiteln dieselbe Sache, muss das
    # Ankerjahr gleich bleiben -- waechst das Kapiteljahr und die Zahl
    # nicht mit, wandert der Anker, und das ist der Fehler. So sind
    # gefunden worden: K39 ("das Haus seit drei Jahren", Auftrag aber
    # August 2023) und K62 (Bastian "seit sieben Jahren", gegangen aber
    # 2019 -- im selben Kapitel dreimal gesagt).
    #
    # Automatisch entscheiden laesst sich das nicht: Dieselbe Zahl
    # meint oft verschiedene Dinge (Amiras Wohnung seit 2019 und Theos
    # Wohnung seit 2020 sind beide "sieben Jahre", nur in
    # verschiedenen Kapiteln). Das Geraet legt die Ankerjahre
    # nebeneinander; welche zusammengehoeren, sieht ein Mensch.
    print(f"\n=== Zeitspannen: Ankerjahre ({len(alle_spannen)} Angaben) ===")
    nach_zahl = {}
    for nr, n, e, z in alle_spannen:
        if not e.startswith("jahr"):
            continue
        anker = jahr_fuer(ordner.name, nr) - n
        nach_zahl.setdefault(n, []).append((nr, anker))
    for n, paare in sorted(nach_zahl.items()):
        anker = sorted({a for _, a in paare})
        if len(paare) < 2:
            continue
        streit = "  <-- Anker wandert" if len(anker) > 1 else ""
        orte = " ".join(f"K{nr}->{a}" for nr, a in sorted(paare))
        print(f"  {n:2d} Jahre: {orte}{streit}")

    print(f"\n{len(klagen) + len(ungueltig)} Beanstandungen.")


if __name__ == "__main__":
    main()
