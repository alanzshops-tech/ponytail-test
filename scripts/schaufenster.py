#!/usr/bin/env python3
"""schaufenster.py — misst, was der Leser *vor* dem Kauf sieht.

Zwei verschiedene Qualitäten: Ein Roman kann gut sein und sich trotzdem
schlecht verkaufen, weil außerhalb des Buches niemand erkennt, was das
Besondere ist. Dieses Gerät misst nur das Äußere — Titel, Untertitel,
Genrezeile auf dem Cover, Klappentext — und nur zwei Dinge daran:

**1. Wie lange braucht der Leser bis zur Prämisse?**

Die Prämisse dieses Buches ist nicht *Denkmalpflege, Behörde, Familie,
Bauprojekt*. Sie ist: **die beiden sind schon verheiratet und müssen
erst lernen, eine Ehe zu sein.** Gemessen wird, an welcher Wortstelle
das zum ersten Mal steht — und ob es noch vor Amazons Abschnitt
„mehr lesen" steht. Auf dem Handy sind das rund 200 Zeichen; was
danach kommt, sieht nur, wer schon interessiert ist.

**2. Verschenkte Keyword-Felder.**

KDP durchsucht Titel und Untertitel ohnehin. Ein Keyword, dessen Wörter
dort schon stehen, ist ein verschenktes von sieben Feldern. Der Bericht
`buch2/KDP-LAUNCH-2.md` nennt zwei solche Fehler, die beim ersten
Aufschreiben passiert sind — gefunden von einem Prüfskript, das nie
gespeichert wurde. Deshalb steht es jetzt hier.

Der Bezugsrahmen: Ein Treffer ist kein Fehler. Eine Kollision kann
gewollt sein, und eine spät stehende Prämisse ist bei einem
Reihenband weniger schlimm als bei einem Einzeltitel. Das Gerät zeigt
Zahlen, die Entscheidung bleibt beim Menschen.

Aufruf:
    python3 scripts/schaufenster.py --selbsttest
    python3 scripts/schaufenster.py --buch buch2
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Amazons Vorschau auf dem Handy, bevor "mehr lesen" kommt. Gerundet
# und bewusst knapp gewählt -- lieber zu streng als zu großzügig.
VORSCHAU_ZEICHEN = 200

# Die Prämisse in ihren Formulierungen. Verlangt wird die Verbindung
# aus "schon verheiratet" UND "muss sich noch zeigen/beweisen/lernen" --
# das blosse Wort "Ehe" ist keine Prämisse, sondern ein Etikett, und
# davon hat die Nische genug.
SCHON_VERHEIRATET = re.compile(
    r"\b(sind verheiratet|seit \w+ Monaten verheiratet|längst verheiratet|"
    r"schon verheiratet|heimlich geheiratet|in Kopenhagen geheiratet|"
    r"verheiratet\b(?=[\s\S]{0,60}\b(nie|noch nie|niemand)\b))", re.I)
MUSS_SICH_ZEIGEN = re.compile(
    r"\b(noch nie miteinander|waren noch nie|beweisen|lernen|"
    r"zum ersten Mal|nie gelebt|zusammenwohnen|echt ist)\b", re.I)


def wortstelle(text: str, rx) -> int | None:
    """An welchem Wort steht der erste Treffer? None = kommt nicht vor."""
    m = rx.search(text)
    if not m:
        return None
    return len(text[:m.start()].split()) + 1


def praemisse(text: str) -> tuple[int | None, int | None]:
    return (wortstelle(text, SCHON_VERHEIRATET),
            wortstelle(text, MUSS_SICH_ZEIGEN))


def in_vorschau(text: str, rx) -> bool:
    return bool(rx.search(text[:VORSCHAU_ZEICHEN]))


def kollisionen(keywords: list[str], titel: str, untertitel: str) -> dict:
    """Welche Keyword-Wörter stehen schon in Titel oder Untertitel?"""
    gesperrt = set(re.findall(r"\w+", (titel + " " + untertitel).lower()))
    aus = {}
    for k in keywords:
        treffer = [w for w in re.findall(r"\w+", k.lower())
                   if w in gesperrt]
        if treffer:
            aus[k] = treffer
    return aus


def beschreibung_messen(text: str) -> dict:
    """Struktur einer Amazon-Beschreibung.

    Was hier gemessen wird, entscheidet nicht ueber Qualitaet -- ob eine
    Beschreibung Lust macht, ist keine Zahl. Messbar ist nur, was auf
    dem Handy ueberhaupt ankommt, bevor "mehr lesen" den Rest abschneidet,
    und wie schwer die ersten Saetze zu lesen sind.

    **Kein Bezugsrahmen aus der Nische.** Fuer Cover und Titel liegen 36
    bzw. 30 gemessene Konkurrenztitel vor, fuer Beschreibungen nicht.
    Die Werte hier sind deshalb nur untereinander vergleichbar --
    Fassung A gegen Fassung B --, nicht gegen den Markt.
    """
    absaetze = [" ".join(a.split()) for a in text.split("\n\n") if a.strip()]
    sichtbar = text[:VORSCHAU_ZEICHEN]
    erster = absaetze[0] if absaetze else ""
    saetze = [s for s in re.split(r"(?<=[.!?])\s+", erster) if s.strip()]
    return {
        "zeichen": len(text),
        "absaetze": len(absaetze),
        "laengster_absatz": max((len(a.split()) for a in absaetze), default=0),
        "erster_satz_woerter": len(saetze[0].split()) if saetze else 0,
        "in_vorschau": sichtbar,
        "stake_in_vorschau": bool(re.search(
            r"Behörde|Frist|beweisen|Montag|ausreisen|prüft", sichtbar, re.I)),
        "zusage": bool(re.search(
            r"Happy End|abgeschlossen|kein Cliffhanger|ohne explizite",
            text, re.I)),
    }


def selbsttest() -> None:
    fehler = []

    # Positivfall: der aktuelle Klappentextanfang. Beide Hälften der
    # Prämisse müssen ganz vorn stehen.
    gut = "Sie sind verheiratet. Sie waren noch nie miteinander aus."
    a, b = praemisse(gut)
    if a is None or a > 3:
        fehler.append(f"'schon verheiratet' nicht am Anfang gefunden: {a}")
    if b is None or b > 10:
        fehler.append(f"'muss sich zeigen' nicht am Anfang gefunden: {b}")

    # Negativfall: die Aufzählung, die genau das nicht leistet.
    schlecht = "Eine geheime Ehe, eine Frist und eine Familie, die alles regelt"
    a, b = praemisse(schlecht)
    if a is not None:
        fehler.append(f"Aufzählung fälschlich als Prämisse erkannt: {a}")

    # Ueber den Satzpunkt hinweg: "Verheiratet. Und nie zusammen aus."
    # ist die Praemisse in zwei Saetzen. Die erste Fassung des Musters
    # hat sie nicht gesehen, weil sie am Punkt abgebrochen hat.
    if praemisse("Verheiratet. Und nie zusammen aus.")[0] is None:
        fehler.append("Praemisse ueber Satzgrenze nicht erkannt")

    # Das blosse Etikett darf nicht reichen.
    if praemisse("Geheime Ehe · Familiengeheimnis")[0] is not None:
        fehler.append("Etikett 'Geheime Ehe' als Prämisse gezählt")

    # Kollisionen, Positiv- und Negativfall aus dem echten Bericht.
    k = kollisionen(["scheinehe liebesroman", "hamburg speicherstadt roman"],
                    "Was er nie gefragt hat",
                    "Eine geheime Ehe, eine Frist und eine Familie – "
                    "Liebesroman (Die Reinhardt-Brüder 2)")
    if "scheinehe liebesroman" not in k:
        fehler.append("bekannte Kollision 'liebesroman' nicht gefunden")
    if "hamburg speicherstadt roman" in k:
        fehler.append("sauberes Keyword fälschlich als Kollision gemeldet")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  bestanden (Klappentextanfang positiv, Aufzählung und Etikett "
          "negativ, Kollision positiv und negativ).")


def klappentext(buch: str) -> str:
    t = Path("scripts/manuskript.py").read_text(encoding="utf-8")
    m = re.search(r'"' + buch[-1] + r'":\s*"""(.*?)"""', t, re.S)
    return m.group(1) if m else ""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--buch", default="buch2")
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--untertitel", default=None,
                   help="Fassung durchrechnen, ohne sie einzubauen")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return

    kdp = Path(a.buch) / "KDP-LAUNCH-2.md"
    text = kdp.read_text(encoding="utf-8") if kdp.exists() else ""
    titel = "Was er nie gefragt hat"
    m = re.search(r"\*\*Im KDP-Feld \[E\]:\*\*\n> (.+)", text)
    untertitel = a.untertitel or (m.group(1) if m else "")
    m = re.search(r"\*\*Auf dem Cover:\*\* (.+)", text)
    coverzeile = m.group(1) if m else ""
    kt = klappentext(a.buch)

    print("\n=== Wie lange braucht der Leser bis zur Prämisse? ===\n")
    flaechen = [("Titel", titel), ("Untertitel", untertitel),
                ("Cover-Genrezeile", coverzeile), ("Klappentext", kt)]
    for name, t in flaechen:
        if not t:
            continue
        av, mz = praemisse(t)
        s1 = f"Wort {av}" if av else "fehlt"
        s2 = f"Wort {mz}" if mz else "fehlt"
        vor = ("ja" if in_vorschau(t, SCHON_VERHEIRATET) else "nein")
        print(f"  {name:18s} 'schon verheiratet': {s1:9s} | "
              f"'muss sich zeigen': {s2:9s} | in den ersten "
              f"{VORSCHAU_ZEICHEN} Zeichen: {vor}")

    kws = re.findall(r"\|\s*\d\s*\|\s*`([^`]+)`", text)
    if kws:
        print(f"\n=== Keyword-Kollisionen mit Titel + Untertitel ===\n")
        print(f"  Untertitel: {untertitel}\n")
        koll = kollisionen(kws, titel, untertitel)
        for k in kws:
            if k in koll:
                print(f"  VERSCHENKT  {k:40s} -> {', '.join(koll[k])}")
            else:
                print(f"  frei        {k}")
        print(f"\n  {len(koll)} von {len(kws)} Feldern verschenkt.")


if __name__ == "__main__":
    main()
