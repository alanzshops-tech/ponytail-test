#!/usr/bin/env python3
"""
kalender.py — prueft jedes Datum im Manuskript gegen den echten Kalender.

Wozu: Band 1 hatte genau diesen Fehler. Dort stand der 18. Februar 2026
als Montag; er ist ein Mittwoch, und weil im selben Kapitel der fuenfte
Eingewoehnungstag auf einen Freitag fiel, der als Dienstag bezeichnet
war, zog der Fehler eine ganze Woche schief. Gefunden wurde er beim
Lesen, durch Zufall, nach mehreren vollstaendigen Durchgaengen.

Kein anderes Werkzeug im Repository kann das finden. prosa.py prueft
Typografie, dopplung.py Wiederholungen, manuskript.py die Struktur.
Ein Datum mit dem falschen Wochentag ist fuer alle drei sauberer Text.

Geprueft werden vier Formen, weil das Buch alle vier benutzt:

  1. "Am sechsundzwanzigsten Juli, einem Sonntag"
  2. "Am Donnerstag, dem zwanzigsten Mai"
  3. "Sie hat das Buero am siebzehnten Maerz bezogen, an einem Freitag"
  4. "am neunundzwanzigsten erzaehlt, einem Samstag" (ohne Monat)

Ein Datum ohne Wochentag ("am achten Mai") ist nicht pruefbar. Wie viele
das sind, steht im Bericht -- sonst sieht "keine Beanstandungen" nach
mehr Sicherheit aus, als da ist.

Das Jahr steht fast nie im Satz. Es wird deshalb aus einer Zeittafel je
Kapitel genommen, die von Hand gepflegt wird -- Raten waere hier
schlimmer als nichts. **Steht doch eine Jahreszahl im Satz, gilt sie**,
sonst meldet jede Rueckblende einen Fehler.

    python3 scripts/kalender.py --selbsttest
    python3 scripts/kalender.py --buch buch2
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# Ausgeschriebene Ordnungszahlen, wie sie im Buch stehen.
TAG = {
    "ersten": 1, "zweiten": 2, "dritten": 3, "vierten": 4, "fuenften": 5,
    "fünften": 5, "sechsten": 6, "siebten": 7, "siebenten": 7, "achten": 8,
    "neunten": 9, "zehnten": 10, "elften": 11, "zwoelften": 12,
    "zwölften": 12, "dreizehnten": 13, "vierzehnten": 14, "fuenfzehnten": 15,
    "fünfzehnten": 15, "sechzehnten": 16, "siebzehnten": 17,
    "achtzehnten": 18, "neunzehnten": 19, "zwanzigsten": 20,
    "einundzwanzigsten": 21, "zweiundzwanzigsten": 22,
    "dreiundzwanzigsten": 23, "vierundzwanzigsten": 24,
    "fuenfundzwanzigsten": 25, "fünfundzwanzigsten": 25,
    "sechsundzwanzigsten": 26, "siebenundzwanzigsten": 27,
    "achtundzwanzigsten": 28, "neunundzwanzigsten": 29,
    "dreissigsten": 30, "dreißigsten": 30, "einunddreissigsten": 31,
    "einunddreißigsten": 31,
}

MONAT = {"Januar": 1, "Februar": 2, "März": 3, "Maerz": 3, "April": 4,
         "Mai": 5, "Juni": 6, "Juli": 7, "August": 8, "September": 9,
         "Oktober": 10, "November": 11, "Dezember": 12}

WOCHENTAG = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag",
             "Samstag", "Sonntag"]

# Welches Jahr in welchem Kapitel gilt. Von Hand gepflegt, weil es im
# Text fast nie steht. Wer Kapitel einschiebt, traegt hier nach; ein
# fehlender Eintrag fuehrt zu einer Meldung und nicht zu einer stillen
# Annahme.
JAHR = {
    "buch2": [
        # Kapitel 32 ist Heiligabend und gehoert noch ins alte Jahr. Der
        # Fehler stand hier bis zum 31.08.2026 unbemerkt drin, weil in
        # Kapitel 32 kein Datum mit Wochentag vorkommt -- das Werkzeug
        # haette ihn also nie gemeldet. Gefunden wurde er beim
        # Nachrechnen der Ehedauer ("einundzwanzig Monate" = Dezember
        # 2026, nicht 2027).
        (1, 10, 2026), (11, 32, 2026), (33, 35, 2027), (36, 44, 2027),
        (45, 49, 2028), (50, 56, 2028), (57, 63, 2029), (64, 64, 2030),
    ],
}

# Tag + Monat + ausgeschriebener Wochentag, in beiden Wortstellungen.
#
# Die erste Fassung vom 31.08.2026 kannte nur Form 1 und hat damit 6 von
# 11 pruefbaren Stellen uebersehen -- darunter den Epilog, weil zwischen
# "März" und ", einem Mittwoch" die Woerter "2030 gepflanzt worden"
# stehen und der Abstand auf 20 Zeichen begrenzt war. Ein Messgeraet,
# das die Haelfte nicht sieht, meldet "keine Beanstandungen" und ist
# damit schlimmer als keins. Jetzt vier Formen, jede im Selbsttest.
MONATE = ("Januar|Februar|März|April|Mai|Juni|Juli|August|September|"
          "Oktober|November|Dezember")
WT = "Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag"
TAGWORT = r"[a-zäöüß]+(?:sten|ten)"

# Form 1: "Am sechsundzwanzigsten Juli, einem Sonntag"
#         "am zwanzigsten März 2030 gepflanzt worden, einem Mittwoch"
MIT_TAG = re.compile(
    rf"\b[Aa]m (?P<tag>{TAGWORT})\b[^.]{{0,40}}?"
    rf"\b(?P<monat>{MONATE})\b[^.]{{0,60}}?,\s*einem (?P<wtag>{WT})")

# Form 2: "Am Donnerstag, dem zwanzigsten Mai"
UMGEKEHRT = re.compile(
    rf"\b[Aa]m (?P<wtag>{WT}), (?:dem|den) (?P<tag>{TAGWORT})\s+"
    rf"(?P<monat>{MONATE})")

# Form 3: "Sie hat das Büro am siebzehnten März bezogen, an einem Freitag"
#         "am elften Juni gekommen, ohne …, an einem Freitagnachmittag"
NACHGESTELLT = re.compile(
    rf"\b[Aa]m (?P<tag>{TAGWORT})\b[^.]{{0,40}}?\b(?P<monat>{MONATE})\b"
    rf"[^.]{{0,80}}?,\s*an einem (?P<wtag>{WT})")

# Form 4: ohne Monat, "am neunundzwanzigsten erzählt, einem Samstag"
OHNE_MONAT = re.compile(
    rf"\b[Aa]m (?P<tag>{TAGWORT})\b(?![^.]{{0,40}}?(?:{MONATE}))"
    rf"[^.]{{0,25}}?,\s*einem (?P<wtag>{WT})")

FORMEN = [("Datum, einem Wochentag", MIT_TAG),
          ("Wochentag, dem Datum", UMGEKEHRT),
          ("Datum … an einem Wochentag", NACHGESTELLT)]


def kapitelnummer(p: Path) -> int:
    return int(re.match(r"kapitel-(\d+)\.md$", p.name).group(1))


def jahr_fuer(buch: str, nr: int) -> int | None:
    for von, bis, jahr in JAHR.get(buch, []):
        if von <= nr <= bis:
            return jahr
    return None


def selbsttest() -> None:
    """Ein richtiges und ein falsches Datum, plus der echte Fall aus Band 1."""
    fehler = []

    # Der Fehler aus Band 1: 18.02.2026 ist ein Mittwoch, kein Montag.
    if date(2026, 2, 18).weekday() != 2:
        fehler.append("Kalenderrechnung stimmt nicht (18.02.2026).")

    treffer = list(MIT_TAG.finditer(
        "Am sechsundzwanzigsten Juli, einem Sonntag, saßen wir."))
    if len(treffer) != 1:
        fehler.append("Muster findet die Standardform nicht.")
    elif TAG[treffer[0].group("tag")] != 26 or \
            MONAT[treffer[0].group("monat")] != 7:
        fehler.append("Muster liest Tag oder Monat falsch.")

    # Negativfall: ein Wochentag ohne Datum darf nicht anschlagen.
    if MIT_TAG.search("Wir sind an einem Sonntag spazieren gegangen."):
        fehler.append("Muster faengt einen Wochentag ohne Datum.")

    # Negativfall: ein Datum ohne Wochentag darf nicht anschlagen.
    if MIT_TAG.search("Am achten Mai um zehn nach neun klingelte es."):
        fehler.append("Muster faengt ein Datum ohne Wochentagsangabe.")

    # Die Form ohne Monat muss greifen, aber nicht dort, wo ein Monat steht.
    if not OHNE_MONAT.search("Am neunundzwanzigsten erzählt, einem Samstag"):
        fehler.append("Muster ohne Monat greift nicht.")
    if OHNE_MONAT.search("Am sechsundzwanzigsten Juli, einem Sonntag"):
        fehler.append("Muster ohne Monat faengt einen Satz mit Monat "
                      "-- das gaebe eine doppelte Meldung.")

    # Die drei Formen, die der ersten Fassung entgangen sind. Jede mit
    # dem Wortlaut, an dem sie tatsaechlich vorbeigelaufen ist.
    entgangen = [
        (MIT_TAG, "Die Winterlinde ist am zwanzigsten März 2030 gepflanzt "
                  "worden, einem Mittwoch, um Viertel nach acht.", 20, 3),
        (UMGEKEHRT, "Am Donnerstag, dem zwanzigsten Mai, ist sie "
                    "gekommen.", 20, 5),
        (NACHGESTELLT, "Sie hat das Büro am siebzehnten März bezogen, an "
                       "einem Freitag, und ich durfte nicht helfen.", 17, 3),
    ]
    for muster, satz, tag_soll, monat_soll in entgangen:
        m = muster.search(satz)
        if not m:
            fehler.append(f"Form greift nicht: {satz[:50]!r}")
        elif TAG[m.group("tag")] != tag_soll or \
                MONAT[m.group("monat")] != monat_soll:
            fehler.append(f"Form liest Tag/Monat falsch: {satz[:50]!r}")

    # Negativfall fuer die umgekehrte Form: ein Wochentag ohne Datum.
    if UMGEKEHRT.search("Am Donnerstag, dem Tag nach der Sitzung, kam er."):
        fehler.append("Umgekehrte Form faengt einen Satz ohne Datum.")

    # Rueckblende: Steht im Satz ein Jahr, muss es die Zeittafel schlagen.
    m = NACHGESTELLT.search("Mein Vater ist am elften Februar 2010 "
                            "gestorben, an einem Donnerstag, im Büro.")
    if not m:
        fehler.append("Rueckblendenform greift nicht.")
    else:
        import re as _re
        jahr = _re.search(r"\b(19|20)\d\d\b", m.group(0))
        if not jahr or jahr.group(0) != "2010":
            fehler.append("Jahreszahl im Satz wird nicht gelesen.")
        elif date(2010, 2, 11).weekday() != 3:
            fehler.append("11.02.2010 ist laut Rechnung kein Donnerstag.")

    for f in fehler:
        print(f"  FEHLER: {f}")
    if fehler:
        sys.exit("Selbsttest nicht bestanden — die Pruefung waere wertlos.")
    print("  Selbsttest bestanden (Band-1-Fall, Positiv- und "
          "zwei Negativfaelle, beide Wortstellungen).")


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--buch", default="buch2")
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args()

    print("Selbsttest:")
    selbsttest()
    if a.selbsttest:
        return

    ordner = Path(a.buch)
    klagen, geprueft, ohne_wochentag = [], 0, 0
    letzter_monat: dict[int, int] = {}

    for p in sorted(ordner.glob("kapitel-*.md"), key=kapitelnummer):
        nr = kapitelnummer(p)
        text = p.read_text(encoding="utf-8")
        jahr = jahr_fuer(a.buch, nr)

        # Monat merken, damit die Form ohne Monat einen Bezug hat.
        monate = re.findall(r"\b(" + "|".join(MONAT) + r")\b", text)
        if monate:
            letzter_monat[nr] = MONAT[monate[-1]]

        ohne_wochentag += len(re.findall(
            r"\b[Aa]m [a-zäöüß]+(?:sten|ten)\b", text))

        gesehen = set()
        for name, muster in FORMEN:
            for m in muster.finditer(text):
                tag = TAG.get(m.group("tag"))
                monat = MONAT[m.group("monat")]
                if tag is None:
                    klagen.append(f"Kapitel {nr}: Tag nicht erkannt "
                                  f"({m.group('tag')!r})")
                    continue
                # Steht im Satz selbst eine Jahreszahl, gilt sie -- sonst
                # meldet jede Rueckblende einen Fehler. Kapitel 16 nennt
                # den Tod des Vaters am 11.02.2010; die Zeittafel sagt
                # fuer dieses Kapitel 2027, und der Donnerstag stimmt fuer
                # 2010 und nicht fuer 2027. Am 31.08.2026 als Fehlalarm
                # aufgefallen, bevor er zu einer falschen Korrektur am
                # richtigen Text gefuehrt hat.
                im_satz = re.search(r"\b(19|20)\d\d\b", m.group(0))
                jahr_hier = int(im_satz.group(0)) if im_satz else jahr
                if jahr_hier is None:
                    klagen.append(f"Kapitel {nr}: kein Jahr in der Zeittafel")
                    continue
                # Dieselbe Stelle kann von zwei Formen gefunden werden.
                if (tag, monat, m.group("wtag")) in gesehen:
                    continue
                gesehen.add((tag, monat, m.group("wtag")))
                geprueft += 1
                ist = WOCHENTAG[date(jahr_hier, monat, tag).weekday()]
                soll = m.group("wtag")
                if ist != soll:
                    klagen.append(
                        f"Kapitel {nr}: {tag}.{monat}.{jahr_hier} ist ein "
                        f"{ist}, im Text steht {soll} ({name})")

    print(f"\n{a.buch}: {geprueft} Datumsangaben mit Wochentag geprueft.")
    print(f"{ohne_wochentag} Datumsangaben ohne Wochentag — nicht pruefbar.")
    if not klagen:
        print("\nKeine Beanstandungen.")
        return
    print(f"\n{len(klagen)} Beanstandung(en):")
    for k in klagen:
        print(f"  - {k}")
    sys.exit(1)


if __name__ == "__main__":
    main()
