#!/usr/bin/env python3
"""manier.py — findet zwei Manierismen, die man beim Lesen nicht sieht.

Beide Muster sind einzeln jedes Mal gut. Sie fallen erst als Menge auf,
und deshalb ist ein Suchlauf hier ehrlicher als ein Urteil: Wer 64
Kapitel liest, gewoehnt sich an die eigene Bauweise nach dem dritten.

**Muster 1 — der Schlusssatz-Reflex.** Eine Szene endet nicht mit dem
letzten Ereignis, sondern mit einem kurzen Satz, der das Ereignis
deutet. *„Das andere ist eine Zeichnung."* *„Beides. Immer beides."*
Das ist die Stimme des Buches. Wenn es aber jede Szene macht, tragen
die grossen Saetze nichts mehr.

**Muster 2 — der Aphorismus bei Nebenfiguren.** Zwoelf Figuren
formulieren nach derselben Gussform: *X ist nicht Y, sondern Z* /
*Das ist A, kein B* / *Der Unterschied zwischen ... ist ...*.

Der Bezugsrahmen -- ohne den eine Messung keine ist:

  Das Geraet zaehlt Gussformen, nicht Qualitaet. Ein Treffer ist kein
  Fehler. Er ist eine Stelle, an der jemand von Hand entscheiden muss,
  ob diese Figur an dieser Stelle deuten darf. Wendland, Sabine und
  Dr. Brandt sind im Roman ausdruecklich als Deutende angelegt; bei
  ihnen ist die Gussform Absicht.

Aufruf:
    python3 scripts/manier.py --buch buch2
    python3 scripts/manier.py --selbsttest
"""

import argparse
import pathlib
import re
import sys

# Muster 1: kurzer Deutungssatz am Szenenende, ohne woertliche Rede.
#
# Der Trennschaerfe wegen zwei Bedingungen statt einer Wortliste. Die
# erste Fassung suchte nach "das ist|das war|beides|..." und fand den
# eigenen Positivfall nicht -- "Das andere ist eine Zeichnung" enthaelt
# keine dieser Zeichenketten. Eine Wortliste, die aus der Erinnerung
# geschrieben ist, misst die Erinnerung.
#
# Stattdessen: der Satz beginnt mit einem Demonstrativpronomen, und er
# ist kurz. Das Pronomen von seinem Artikel zu trennen erledigt die
# deutsche Rechtschreibung -- "Das Fenster war offen" (Artikel, danach
# gross) ist kein Deutungssatz, "Das andere ist eine Zeichnung"
# (Pronomen, danach klein) ist einer.
# Gesucht ist nicht "kurzer Schlussabsatz" -- 59 von 399 Szenen enden
# kurz, und die meisten davon enden auf einer Handlung ("Er hat
# aufgelegt.", "Ich bin hingefahren."), die genau richtig ist. Gesucht
# ist die Zweiteilung: Ereignissatz, dann ein kurzer Satz, der auf das
# Ereignis zurueckzeigt und es deutet. Nur bei dieser Form ist der
# Eingriff definiert -- letzten Satz streichen, vorletzten behalten.
KURZ = 10                              # Woerter im Deutungssatz

RUECKBEZUG = re.compile(
    r"^(?:"
    r"(?:Das|Es|Dies)\s+(?![A-ZÄÖÜ])"  # Pronomen, kein Artikel
    r"|Beides\b|Dasselbe\b|Dieselbe\b|Derselbe\b"
    r"|Deshalb\b|Darum\b|Genau das\b|Und das\b|Nicht das\b"
    r"|Immer\b|Weil\b|Ich merke\b|Ich fand\b|Ich habe es\b"
    r")")


def saetze(absatz: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", absatz.strip())
            if s.strip()]


def deutungsschluss(absatz: str) -> tuple[str, str] | None:
    """(Ereignissatz, Deutungssatz) -- oder None."""
    a = " ".join(absatz.split())
    if a[:1] in ("„", ">", "*", "#"):   # Dialog, Zitat, Auszeichnung
        return None
    ss = saetze(a)
    if len(ss) < 2:
        return None
    letzt = ss[-1]
    # Ein Satz, der auf " endet, steht in woertlicher Rede -- der
    # Satztrenner hat innerhalb eines Zitats geschnitten. K29 und K56
    # sind genau so falsch in die erste Liste geraten.
    if letzt.endswith(("“", "”", '"')) or "„" in letzt:
        return None
    if len(letzt.split()) <= KURZ and RUECKBEZUG.match(letzt):
        return ss[-2], letzt
    return None

# Muster 2: die drei Gussformen des Aphorismus in woertlicher Rede.
APHORISMUS = [
    ("nicht-sondern", re.compile(
        r"„[^“]{0,200}?\bist nicht\b[^“]{0,120}?\bsondern\b[^“]{0,120}“")),
    ("A-kein-B", re.compile(
        r"„[^“]{0,200}?\bist (?:ein|eine)\b[^“]{0,60}?,\s*kein[e]?\b[^“]{0,80}“")),
    # Dieselbe Gussform andersherum: "ist keine X, das ist ein Y".
    # Marlenes Satz in K48 ist so gebaut und ist der ersten Fassung
    # deshalb entgangen -- gefunden nur, weil ich ihre Redebeitraege
    # danach von Hand durchgesehen habe. Ein Muster, das man nur in
    # einer Richtung sucht, misst die Richtung.
    ("kein-B-sondern-A", re.compile(
        r"„[^“]{0,200}?\bist kein[e]?\b[^“]{0,80}?,\s*(?:das ist|sondern)\s"
        r"(?:ein|eine)\b[^“]{0,80}“")),
    ("Unterschied", re.compile(
        r"„[^“]{0,200}?\bUnterschied zwischen\b[^“]{0,160}“")),
    # Die gnomische Form: "Wer X, tut Y" / "Leute, die X, tun Y" --
    # ein Satz ueber die Menschen im Allgemeinen, mitten im Gespraech.
    # Die vier Gussformen oben haben sie nicht erfasst, und deshalb war
    # der erste Befund ("Nebenfiguren aphorisieren nicht") falsch:
    # Brandt in K03, Adamczyk in K19 und Marlene in K04 sprechen so.
    # Gefunden nur, weil der Phase-1-Bericht diese Saetze zitiert und
    # das Geraet sie nicht wiedergefunden hat.
    # Erste Fassung fing 15 Treffer, davon 10 gewoehnliche Fragen
    # ("Wer kauft ein?", "Wer steht morgens zuerst auf?"). Die Form
    # braucht beides: Nebensatz mit Komma, und einen Aussagesatz --
    # kein Fragezeichen. "Man kann/muss/darf" ist ganz raus, das ist
    # normale Rede.
    ("gnomisch", re.compile(
        r"(?:Wer\s+\w+(?:\s+\w+){0,4},\s|Leute,\s+die\s|Jemand,\s+der\s)"
        r"[^“„?]{0,120}?\.")),
    ("das-ist-etwas-anderes", re.compile(
        r"„[^“]{0,200}?\bDas ist (?:etwas|was) anderes\b[^“]{0,120}“")),
]

DEUTENDE = {"Wendland", "Sabine", "Brandt"}   # duerfen deuten, per Anlage


def szenen(text: str) -> list[list[str]]:
    """Kapitel in Szenen zerlegen; Szenen sind durch --- getrennt."""
    ohne_kopf = re.sub(r"^#.*$", "", text, flags=re.M)
    roh = re.split(r"^\s*---\s*$", ohne_kopf, flags=re.M)
    aus = []
    for s in roh:
        absaetze = [a.strip() for a in s.split("\n\n") if a.strip()]
        if absaetze:
            aus.append(absaetze)
    return aus


def schlusssaetze(text: str) -> list[tuple[str, str]]:
    paare = (deutungsschluss(s[-1]) for s in szenen(text))
    return [p for p in paare if p]


def aphorismen(text: str) -> list[tuple[str, str]]:
    flach = " ".join(text.split())
    aus = []
    for name, rx in APHORISMUS:
        for m in rx.finditer(flach):
            aus.append((name, m.group(0)))
    return aus


def selbsttest() -> None:
    fehler = []

    # Muster 1, Positivfaelle: zwei echte Szenenschluesse aus dem Buch.
    positive = [
        "Er hat nicht widersprochen. Das war das Schlimmste daran.",
        "Ich habe das gemerkt. Ich merke so etwas inzwischen sofort.",
    ]
    for pos in positive:
        if len(schlusssaetze("Text.\n\n---\n\nVorher.\n\n" + pos)) != 1:
            fehler.append(f"Deutungsmuster findet den Positivfall nicht: "
                          f"{pos!r}")

    # Muster 1, Negativfaelle -- jeder steht fuer einen Fehlgriff, den
    # das Geraet schon gemacht hat:
    #   1. Handlungsschluss. Kurz, aber richtig; darf nicht weg.
    #   2. "Das" als Artikel, nicht als Pronomen (Grossschreibung).
    #   3. Einsaetzer -- da gibt es keinen vorletzten Satz zu behalten,
    #      der Eingriff waere also gar nicht definiert.
    #   4. Deutung innerhalb woertlicher Rede: der Satztrenner schneidet
    #      im Zitat. So sind K29 und K56 in die erste Liste geraten.
    negative = [
        "Sie ist gegangen. Er hat die Tür zugemacht und ist in die "
        "Küche gegangen.",
        "Er hat sie angesehen. Das Fenster war offen.",
        "Das war das Schlimmste daran.",
        "Und ich habe gesagt: „Ich weiß. Das macht es für dich besser "
        "und für mich nicht.“",
    ]
    for neg in negative:
        if schlusssaetze("Text.\n\n---\n\nVorher.\n\n" + neg):
            fehler.append(f"Deutungsmuster faengt zu viel: {neg!r}")

    # Muster 2, Positivfall.
    p2 = ("„Der Unterschied zwischen einem Fehler und einem Skandal ist "
          "nicht der Fehler.“")
    if not aphorismen(p2):
        fehler.append("Aphorismusmuster findet den Positivfall nicht.")

    # Muster 2, Negativfall: gewoehnliche Rede mit 'nicht' und 'sondern'.
    n2 = "„Ich komme nicht Dienstag, sondern Donnerstag“, sagte sie."
    if aphorismen(n2):
        fehler.append(f"Aphorismusmuster faengt zu viel: {aphorismen(n2)}")

    # Muster 2, gnomische Form -- echte Saetze aus dem Buch gegen die
    # Fragen, die die erste Fassung mitgenommen hat.
    for p in ("„Wer lügt, bereitet sich vor.“",
              "„Wer mittags misst, misst das Wetter.“",
              "„Leute, die etwas vorspielen, legen die Dinge des "
              "anderen in die Mitte.“"):
        if not aphorismen(p):
            fehler.append(f"Gnomisches Muster findet nicht: {p!r}")
    for n in ("„Wer steht morgens zuerst auf?“", "„Wer kauft ein?“",
              "„Wer hat dir das beigebracht?“", "„Wer weiß es sonst?“",
              "„Man kann Satzungen ändern.“", "„Wer da gewohnt hat.“"):
        if aphorismen(n):
            fehler.append(f"Gnomisches Muster faengt zu viel: {n!r}")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  Selbsttest bestanden (Muster 1: 2 Positiv-, 4 Negativfaelle; "
          "Muster 2: 4 Positiv-, 7 Negativfaelle).")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--buch", default="buch2")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return

    dateien = sorted(pathlib.Path(a.buch).glob("kapitel-*.md"))
    szenen_gesamt = deut = 0
    print("\n=== Muster 1: Ereignissatz + Deutungssatz am Szenenende ===\n")
    for f in dateien:
        nr = int(re.search(r"(\d+)", f.name).group(1))
        t = f.read_text(encoding="utf-8")
        szenen_gesamt += len(szenen(t))
        for vorher, letzt in schlusssaetze(t):
            deut += 1
            print(f"K{nr:02d}  … {vorher[-60:]}")
            print(f"     streichbar: {letzt}")
    print(f"\n{deut} von {szenen_gesamt} Szenen "
          f"({100*deut/szenen_gesamt:.0f} %).")

    print(f"\n=== Muster 2: Aphorismus-Gussformen in woertlicher Rede ===\n")
    n = 0
    for f in dateien:
        nr = int(re.search(r"(\d+)", f.name).group(1))
        for form, satz in aphorismen(f.read_text(encoding="utf-8")):
            n += 1
            print(f"K{nr:02d} [{form}] {satz[:115]}")
    print(f"\n{n} Treffer. Wendland, Sabine und Dr. Brandt duerfen deuten "
          f"(so angelegt) — bei allen anderen ist jeder Treffer eine "
          f"Entscheidung.")


if __name__ == "__main__":
    main()
