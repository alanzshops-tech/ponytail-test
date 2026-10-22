#!/usr/bin/env python3
"""Eigennamen auf Schreibvarianten pruefen.

Ein Buch mit vierzig Nebenfiguren verliert Namen. Nicht laut -- es
schreibt Sarrazin einmal Sarazin, und niemand merkt es beim Lesen,
weil das Auge den Namen aus dem Zusammenhang ergaenzt. Genau dafuer
ist ein Messgeraet da.

Der Bezugsrahmen -- ohne den eine Messung keine ist:

  Geprueft wird *nicht* jedes grossgeschriebene Wort. Im Deutschen
  sind alle Substantive gross, ein Abstandsvergleich ueber den ganzen
  Wortschatz meldet "Wand/Hand", "Mann/Mama", "Boden/Boten" und
  ersaeuft den einen echten Treffer in achtzig falschen. Ein Selektor,
  der zu viel faengt, ist kein Messgeraet.

  Geprueft wird stattdessen ein umgrenzter Bestand: Woerter, die im
  Text hinter einer Anrede stehen (Frau, Herr, Herrn, Dr., Familie)
  oder in der Figurenbibel des Projekts vorkommen. Das sind sicher
  Eigennamen. Jede Fundstelle im ganzen Buch wird dann gegen diesen
  Bestand gehalten: Ein Wort mit Abstand 1 zu einem bekannten Namen,
  das selbst kein bekannter Name ist, ist ein Verdacht.

Aufruf:
    python3 scripts/namen.py --buch buch2
    python3 scripts/namen.py --selbsttest
"""

import argparse
import pathlib
import re
import sys
from collections import Counter

# "Frau" ist im Deutschen zweierlei: Anrede und Ehefrau. Die erste
# Fassung hat deshalb "Nimmt Ihre Frau Zucker in den Kaffee?" als Figur
# namens Zucker gelesen, dazu Fotos, Miete und Vorwuerfe. Ein Selektor,
# der zu viel faengt, ist kein Messgeraet: Vor der Anrede darf kein
# Begleiter stehen, der sie zur Ehefrau macht.
BEGLEITER = {
    "ihre", "ihrer", "ihrem", "ihren", "meine", "meiner", "meinem",
    "deine", "deiner", "deinem", "seine", "seiner", "seinem",
    "unsere", "unserer", "die", "der", "den", "dieser", "diese",
    "eine", "einer", "einem",
}
ANREDE = re.compile(
    r"(?:(?P<davor>[A-Za-zÄÖÜäöüß]+)\s+)?"
    r"\b(?:Frau|Herr|Herrn|Familie)\s+(?:Dr\.\s+)?"
    r"(?P<name>[A-ZÄÖÜ][a-zäöüß]+)")
WORT = re.compile(r"\b[A-ZÄÖÜ][a-zäöüß]{3,}\b")

# Woerter, die hinter einer Anrede stehen koennen, ohne Name zu sein.
KEINE_NAMEN = {
    "Doktor", "Professor", "Kollege", "Kollegin", "Anwalt", "Anwaeltin",
    "Nachbarin", "Nachbar", "Mutter", "Vater", "Tochter", "Sohn",
}

# Vornamen kommen nie hinter einer Anrede vor und muessen deshalb von
# Hand gepflegt werden. Wer eine Figur einfuehrt, traegt sie hier nach.
VORNAMEN = {
    "Amira", "Theo", "Jonas", "Leni", "Selin", "Bastian", "Niklas",
    "Emil", "Sabine", "Marlene", "Nadia", "Karim", "Ernst",
}


def abstand(a: str, b: str) -> int:
    """Levenshtein, kurz gehalten -- die Woerter sind hoechstens 20 Zeichen."""
    if a == b:
        return 0
    vor = list(range(len(b) + 1))
    for i, za in enumerate(a, 1):
        jetzt = [i]
        for j, zb in enumerate(b, 1):
            jetzt.append(min(vor[j] + 1, jetzt[j - 1] + 1,
                             vor[j - 1] + (za != zb)))
        vor = jetzt
    return vor[-1]


def bestand(texte: list[str], zusatz: set[str]) -> set[str]:
    namen = set(zusatz) | VORNAMEN
    for t in texte:
        for m in ANREDE.finditer(t):
            davor = (m.group("davor") or "").lower()
            if davor in BEGLEITER:
                continue          # "Ihre Frau Zucker" ist keine Figur Zucker
            w = m.group("name")
            if w not in KEINE_NAMEN:
                namen.add(w)
    return namen


def pruefen(texte: list[str], namen: set[str]) -> list[tuple[str, str, int]]:
    """Jedes Wort im Text gegen den Namensbestand. Abstand 1 = Verdacht."""
    zaehler = Counter()
    for t in texte:
        zaehler.update(WORT.findall(t))

    verdacht = []
    for wort, anzahl in zaehler.items():
        if wort in namen:
            continue
        # Beugungen sind keine Varianten: Sarrazins, Haddads.
        if wort[:-1] in namen and wort.endswith(("s", "n")):
            continue
        for name in namen:
            if abs(len(wort) - len(name)) <= 1 and abstand(wort, name) == 1:
                verdacht.append((wort, name, anzahl))
                break
    return sorted(verdacht)


def selbsttest() -> None:
    """Ein eingebauter Tippfehler muss auffallen, sauberer Text nicht."""
    fehler = []

    sauber = ("Frau Sarrazin hat genickt. Herr Adamczyk schwieg. "
              "Sarrazin sah auf. Adamczyk zog die Schuhe an. "
              "Die Wand war kalt, die Hand auch, und der Mann ging.")
    namen = bestand([sauber], set()) - VORNAMEN
    if namen != {"Sarrazin", "Adamczyk"}:
        fehler.append(f"Bestand falsch erkannt: {sorted(namen)}")

    # Der Fall, an dem die erste Fassung gescheitert ist.
    ehefrau = ("Nimmt Ihre Frau Zucker in den Kaffee? Deine Frau Miete "
               "zahlt, und in dieser Familie Vorwürfe abgelegt werden.")
    falsch = bestand([ehefrau], set()) - VORNAMEN
    if falsch:
        fehler.append(f"Ehefrau als Figur gelesen: {sorted(falsch)}")

    # Positivfall dazu: die echte Anrede muss weiter greifen, auch mit Titel.
    if "Sarrazin" not in bestand(["Frau Dr. Sarrazin kam herein."], set()):
        fehler.append("Anrede mit Titel wird nicht erkannt.")
    treffer = pruefen([sauber], namen)
    if treffer:
        fehler.append(f"Falscher Alarm auf sauberem Text: {treffer}")

    kaputt = sauber + " Sarazin hat es anders geschrieben."
    treffer = pruefen([kaputt], namen)
    if not any(w == "Sarazin" for w, _, _ in treffer):
        fehler.append("Der eingebaute Tippfehler Sarazin wurde nicht gefunden.")

    # Negativfall: eine Beugung ist keine Variante.
    treffer = pruefen(["Frau Sarrazin kam. Sarrazins Akte lag da."],
                      {"Sarrazin"})
    if treffer:
        fehler.append(f"Beugung faelschlich gemeldet: {treffer}")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if not fehler:
        print("  Selbsttest bestanden (Positivfall, Negativfall, Beugung).")
    else:
        sys.exit(1)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--buch", default="buch2")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return

    ordner = pathlib.Path(a.buch)
    dateien = sorted(ordner.glob("kapitel-*.md"))
    texte = [d.read_text(encoding="utf-8") for d in dateien]

    projekt = ordner / "PROJEKT.md"
    zusatz = set()
    if projekt.exists():
        zusatz = {m.group("name") for m in
                  ANREDE.finditer(projekt.read_text(encoding="utf-8"))}

    namen = bestand(texte, zusatz)
    print(f"\n{a.buch}: {len(dateien)} Kapitel, "
          f"{len(namen)} Eigennamen im Bestand.")

    treffer = pruefen(texte, namen)
    if not treffer:
        print("Keine Schreibvarianten gefunden.")
        return

    print(f"\n{len(treffer)} Verdachtsfaelle "
          f"(Wort — aehnlich zu — wie oft im Buch):")
    for wort, name, anzahl in treffer:
        print(f"  {wort:20s} ~ {name:20s} {anzahl}x")
    print("\nJeder Treffer ist von Hand zu entscheiden. Ein Wort, das kein "
          "Name ist, kann zufaellig einen Buchstaben Abstand haben.")


if __name__ == "__main__":
    main()
