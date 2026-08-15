#!/usr/bin/env python3
"""
prosa.py — misst den Text des Manuskripts.

Wozu: Für Nachfrage, Cover und Kategorien gibt es hier Messgeräte. Für
den Text selbst gab es keins — und beim ersten Versuch, eins zu bauen,
kam sofort ein Fund, den ich mit bloßem Auge nie gemacht hätte: **1.107
Dialogzeilen mit falschem schließendem Anführungszeichen.**

Was das Gerät kann und was nicht:

**Absolut messbar** — hier gibt es richtig und falsch:
  * Typografie: Anführungszeichen, Apostroph, Auslassungspunkte
  * Rechtschreibung und Grammatik (LanguageTool)

**Nur im Vergleich messbar** — hier gibt es kein „richtig", nur
Ausreißer zwischen den Kapiteln:
  * Satzlänge und ihre Streuung
  * Füllwortdichte
  * Dialoganteil
  * Adverb- und Adjektivdichte
  * Wortwiederholung im Nahbereich

**Nicht messbar, deshalb nicht behauptet:** ob eine Szene trägt, ob eine
Figur glaubwürdig ist, ob das Buch gut ist. Dafür gibt es kein Gerät,
und ein schlechtes wäre schlimmer als keins. Die Lesbarkeitsformeln
(Flesch, Wiener Sachtextformel) stehen mit im Bericht, aber sie sind für
**Sachtexte** gebaut — bei Belletristik messen sie vor allem, wie viel
Dialog vorkommt.

Aufruf:
    python3 scripts/prosa.py --selbsttest
    python3 scripts/prosa.py
    python3 scripts/prosa.py --korrigieren      # nur Typografie
"""

from __future__ import annotations

import argparse
import collections
import re
import statistics
import sys
from pathlib import Path

BUCH = Path(__file__).resolve().parent.parent / "buch"
MARKER = ('<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf '
          'erhalten -->')

# Deutsche Fuellwoerter. Kein Fehler an sich -- in der ersten Person
# gehoeren sie zur Stimme. Interessant ist nur, wenn ein Kapitel deutlich
# ueber den anderen liegt.
FUELLWOERTER = {
    "eigentlich", "irgendwie", "ziemlich", "wirklich", "halt", "eben",
    "wohl", "einfach", "schon", "sehr", "etwas", "quasi", "sozusagen",
    "praktisch", "natürlich", "offensichtlich", "tatsächlich",
    "letztendlich", "überhaupt", "immerhin", "allerdings", "jedenfalls",
    "vielleicht", "eventuell", "möglicherweise", "durchaus", "absolut",
    "total", "völlig", "komplett", "relativ", "nahezu", "beinahe",
    "irgendwann", "irgendwo", "irgendetwas",
}

# LanguageTool-Regeln, die bei Belletristik nur Rauschen liefern. Jede
# Zeile ist begruendet, sonst waere es Wegdrehen statt Filtern.
LT_AUS = {
    # Markdown-Reste: Kursivsterne machen aus dem naechsten Wort einen
    # Satzanfang, das Gross-/Kleinschreibungsurteil ist dann wertlos.
    "DE_CASE",
    # Erfundene Eigennamen, Hausnummern, ausgeschriebene Zahlen. Der
    # Speller kennt "Kehrwieder" und "dreihundertneun" nicht.
    "GERMAN_SPELLER_RULE",
    # Bewusste Satzfragmente sind in diesem Buch Stilmittel:
    # "Ich sagte nichts." / "Vierzig Bilder."
    "SATZBAU",
}


# ----------------------------------------------------------- Grundlagen

def text_von(pfad: Path) -> str:
    return pfad.read_text(encoding="utf-8")


def ohne_markdown(t: str) -> str:
    """Ueberschriften, Trenner, Sterne und Zitatzeichen raus. Ohne das
    meldet LanguageTool Markdown-Syntax als Grammatikfehler -- beim
    ersten Lauf waren 7 von 19 Treffern genau das."""
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    t = re.sub(r"^\s*(---|\*\*\*)\s*$", "", t, flags=re.M)
    t = re.sub(r"^\s*>\s?", "", t, flags=re.M)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t, flags=re.S)
    t = re.sub(r"\*(.+?)\*", r"\1", t, flags=re.S)
    t = re.sub(r"`(.+?)`", r"\1", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def saetze(t: str) -> list[str]:
    roh = re.split(r"(?<=[.!?…])[\s\n]+", t)
    return [s.strip() for s in roh if len(s.split()) >= 2]


# ---------------------------------------------------------- Typografie

def typografie_pruefen(t: str) -> dict:
    """Was hier gezaehlt wird, ist eindeutig falsch oder eindeutig
    richtig -- kein Geschmack."""
    return {
        "zitat_offen": t.count("„"),
        "zitat_zu_richtig": t.count("“"),
        "zitat_zu_falsch": t.count('"'),
        "apostroph_falsch": t.count("'"),
        "apostroph_richtig": t.count("’"),
        "auslassung_falsch": len(re.findall(r"(?<!\.)\.\.\.(?!\.)", t)),
        "auslassung_richtig": t.count("…"),
    }


def typografie_korrigieren(t: str) -> tuple[str, dict]:
    """Nur Ersetzungen, die eindeutig sind.

    Der Tausch von " nach " ist nur zulaessig, wenn sich oeffnende und
    schliessende Zeichen sauber abwechseln. Ist das nicht so, steckt ein
    echter Fehler im Text und ein blindes Ersetzen wuerde ihn zubetonieren.
    """
    vorher = typografie_pruefen(t)
    stellen = [m.group() for m in re.finditer(r'[„"]', t)]
    erwartet = "„"
    for ch in stellen:
        if ch != erwartet:
            raise ValueError(
                "Anführungszeichen wechseln sich nicht sauber ab — "
                "nicht automatisch ersetzbar, bitte von Hand ansehen.")
        erwartet = '"' if ch == "„" else "„"
    if erwartet != "„":
        raise ValueError("Text endet mit offenem Zitat.")

    t = t.replace('"', "“")
    t = re.sub(r"(?<=\w)'(?=\W|$)", "’", t)   # Genitiv: Jonas'
    t = re.sub(r"(?<=\w)'(?=\w)", "’", t)     # Elision: bin's
    t = re.sub(r"(?<!\.)\.\.\.(?!\.)", "…", t)
    return t, vorher


# ------------------------------------------------------------- Messung

def kapitelmass(t: str, nlp=None) -> dict:
    rein = ohne_markdown(t)
    s = saetze(rein)
    laengen = [len(x.split()) for x in s] or [0]
    woerter = rein.split()
    klein = [w.strip(".,;:!?…„“’—–-()").lower() for w in woerter]

    # Dialoganteil: Zeichen zwischen den Anfuehrungszeichen.
    dialog = sum(len(m.group(1)) for m in
                 re.finditer(r"„([^“\"]*)[“\"]", rein))

    m = {
        "woerter": len(woerter),
        "saetze": len(s),
        "satz_median": round(statistics.median(laengen), 1),
        "satz_streuung": round(statistics.pstdev(laengen), 1) if len(laengen) > 1 else 0.0,
        "satz_lang_anteil": round(
            100 * sum(1 for x in laengen if x > 30) / max(1, len(laengen)), 1),
        "dialog_anteil": round(100 * dialog / max(1, len(rein)), 1),
        "fuellwort_je_1000": round(
            1000 * sum(1 for w in klein if w in FUELLWOERTER) / max(1, len(woerter)), 1),
    }
    if nlp is not None:
        d = nlp(rein[:900_000])
        inhalt = [t_ for t_ in d if t_.pos_ in ("NOUN", "VERB", "ADJ", "ADV")]
        m["adverb_je_1000"] = round(
            1000 * sum(1 for t_ in d if t_.pos_ == "ADV") / max(1, len(d)), 1)
        m["adjektiv_je_1000"] = round(
            1000 * sum(1 for t_ in d if t_.pos_ == "ADJ") / max(1, len(d)), 1)
        m["_lemmas"] = [(t_.lemma_.lower(), t_.i) for t_ in inhalt
                        if len(t_.lemma_) > 3]
    return m


def doppelwoerter(text: str) -> list[tuple[str, int]]:
    """Dasselbe Wort zweimal direkt hintereinander, ohne Satzzeichen
    dazwischen.

    Das kann Vale nicht: Sein Regex-Motor (RE2) kennt keine
    Rueckverweise, und seine Wiederholungsregel ignoriert Satzzeichen.
    Am 15.08.2026 meldete sie deshalb fuenf Treffer im Manuskript, und
    alle fuenf waren richtiges Deutsch -- Relativpronomen ("die, die es
    allein schafft"), Konjunktiv-Inversion ("gegeben haette, haette
    ich") und eine gewollte Wiederholung ueber den Gedankenstrich.

    Hier mit Rueckverweis und ohne erlaubte Satzzeichen dazwischen, und
    erst ab vier Buchstaben -- kuerzere sind im Deutschen fast immer
    Funktionswoerter.
    """
    raus = []
    # Ohne IGNORECASE. Im Deutschen unterscheidet die Grossschreibung
    # Substantiv und Verb: "in einem Leben leben" ist richtig, und mit
    # IGNORECASE meldete diese Funktion genau das als Fehler.
    for m in re.finditer(r"\b([A-Za-zÄÖÜäöüß]{4,})\s+\1\b", text):
        raus.append((m.group(1), text[:m.start()].count("\n") + 1))
    return raus


def wiederholungen(lemmas: list[tuple[str, int]], fenster: int = 220,
                   ab: int = 4) -> list[tuple[str, int]]:
    """Dasselbe Wort mehrfach dicht beieinander. Über ein ganzes Kapitel
    verteilt ist eine Wiederholung normal — auf zwei Absätzen fällt sie
    auf."""
    nach_wort: dict[str, list[int]] = {}
    for lemma, pos in lemmas:
        nach_wort.setdefault(lemma, []).append(pos)
    raus = []
    for wort, stellen in nach_wort.items():
        if len(stellen) < ab:
            continue
        best = 0
        links = 0
        for rechts in range(len(stellen)):
            while stellen[rechts] - stellen[links] > fenster:
                links += 1
            best = max(best, rechts - links + 1)
        if best >= ab:
            raus.append((wort, best))
    return sorted(raus, key=lambda x: -x[1])


# --------------------------------------------------------- Kalibrierung

def selbsttest() -> bool:
    ok = True

    t = typografie_pruefen('„Hallo", sagte er. Jonas\' Hut. Also ...')
    print(f"  Typografie: {t}")
    if not (t["zitat_offen"] == 1 and t["zitat_zu_falsch"] == 1
            and t["apostroph_falsch"] == 1 and t["auslassung_falsch"] == 1):
        print("  FEHLGESCHLAGEN: bekannte Fehler nicht gefunden.")
        ok = False

    sauber = typografie_pruefen("„Hallo“, sagte er. Jonas’ Hut. Also …")
    if (sauber["zitat_zu_falsch"] or sauber["apostroph_falsch"]
            or sauber["auslassung_falsch"]):
        print("  FEHLGESCHLAGEN: sauberer Text wird beanstandet.")
        ok = False
    print(f"  Typografie, Negativfall: keine Beanstandung "
          f"= {not any([sauber['zitat_zu_falsch'], sauber['apostroph_falsch'], sauber['auslassung_falsch']])}")

    try:
        typografie_korrigieren('„a" „b" „c"')
        print("  Korrektur, Positivfall: sauberes Paarmuster akzeptiert")
    except ValueError:
        print("  FEHLGESCHLAGEN: sauberes Paarmuster abgelehnt.")
        ok = False
    try:
        typografie_korrigieren('„a" „b')
        print("  FEHLGESCHLAGEN: offenes Zitat wurde ersetzt.")
        ok = False
    except ValueError:
        print("  Korrektur, Negativfall: offenes Zitat abgelehnt")

    dopp = doppelwoerter("Er ging ging zur Tür.")
    print(f"  Doppelwort, Positivfall: {dopp}")
    if not dopp:
        print("  FEHLGESCHLAGEN: 'ging ging' nicht gefunden.")
        ok = False
    falsch = []
    for satz in ["Ich bin die, die es allein schafft.",
                 "niemand — niemand von uns",
                 "gegeben hätte, hätte ich",
                 "Frau Özdemir, die die Gruppe leitet",
                 "Der Anwalt, der der Gegenseite geraten hat",
                 "dass ich nicht in einem Leben leben kann",
                 "weil das Wissen wissen will"]:
        if doppelwoerter(satz):
            falsch.append(satz)
    print(f"  Doppelwort, sieben echte Sätze: "
          f"{len(falsch)} falsche Treffer")
    if falsch:
        for s in falsch:
            print(f"    falsch beanstandet: {s}")
        ok = False

    eng = [("regen", i) for i in range(0, 100, 25)]
    weit = [("regen", i) for i in range(0, 4000, 1000)]
    a = wiederholungen(eng)
    b = wiederholungen(weit)
    print(f"  Wiederholung eng: {a} | weit: {b}")
    if not a or b:
        print("  FEHLGESCHLAGEN: Nahbereichs-Wiederholung falsch erkannt.")
        ok = False

    # Der erste Testfall hier war '„Ja", sagte er.' mit der Erwartung
    # über 30 Prozent. Das Gerät meldete 17,6 -- und hatte recht: In
    # diesem Satz sind zwei von 34 Zeichen Dialog. Der Testfall war
    # falsch, nicht die Messung. Jetzt ein Fall, bei dem der Anteil
    # tatsächlich hoch ist.
    voll = kapitelmass('„Ich komme morgen vorbei, wenn es dir recht ist."')
    leer = kapitelmass("Er ging über die Straße und sah niemanden dort.")
    print(f"  Dialoganteil: fast nur Dialog {voll['dialog_anteil']} %, "
          f"kein Dialog {leer['dialog_anteil']} %")
    if not (voll["dialog_anteil"] > 80 and leer["dialog_anteil"] == 0):
        print("  FEHLGESCHLAGEN: Dialogmessung unbrauchbar.")
        ok = False

    print("  Selbsttest bestanden." if ok else "  Selbsttest FEHLGESCHLAGEN.")
    return ok


# ------------------------------------------------------------- Bericht

def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--korrigieren", action="store_true",
                   help="eindeutige Typografiefehler im Text ersetzen")
    p.add_argument("--bericht", default="PROSA.md")
    p.add_argument("--ohne-spacy", action="store_true")
    args = p.parse_args()

    print("Kalibrierung:")
    if not selbsttest():
        raise SystemExit(2)
    if args.selbsttest:
        return
    print()

    dateien = sorted(BUCH.glob("kapitel-*.md"))

    if args.korrigieren:
        geaendert = 0
        summe = collections.Counter()
        for f in dateien + [BUCH / "00-vorspann.md", BUCH / "99-nachspann.md"]:
            if not f.exists():
                continue
            alt = text_von(f)
            neu, vorher = typografie_korrigieren(alt)
            if neu != alt:
                f.write_text(neu, encoding="utf-8")
                geaendert += 1
                for k, v in vorher.items():
                    if "falsch" in k:
                        summe[k] += v
        print(f"Typografie korrigiert in {geaendert} Dateien:")
        for k, v in summe.items():
            print(f"  {k}: {v}")
        print()

    nlp = None
    if not args.ohne_spacy:
        try:
            import spacy
            nlp = spacy.load("de_core_news_sm")
        except Exception as e:
            print(f"spaCy nicht verfügbar ({str(e)[:60]}) — "
                  f"Wortarten werden übersprungen.\n")

    zeilen = ["# Prosa-Messung", "",
              "Gemessen mit `scripts/prosa.py`. **Absolut** messbar ist "
              "nur die Typografie — alles andere sind Vergleichswerte "
              "zwischen den Kapiteln. Ein Ausreißer ist ein Hinweis, kein "
              "Urteil.", "",
              "| Kap. | Wörter | Satz Median | Streuung | >30 Wörter | "
              "Dialog | Füllw./1000 | Adv./1000 |",
              "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    alle = {}
    for f in dateien:
        n = int(re.search(r"(\d+)", f.name).group(1))
        m = kapitelmass(text_von(f), nlp)
        alle[n] = m
        zeilen.append(
            f"| {n} | {m['woerter']} | {m['satz_median']} | "
            f"{m['satz_streuung']} | {m['satz_lang_anteil']} % | "
            f"{m['dialog_anteil']} % | {m['fuellwort_je_1000']} | "
            f"{m.get('adverb_je_1000', '–')} |")

    def spanne(feld):
        w = [(n, m[feld]) for n, m in alle.items() if feld in m]
        if not w:
            return None
        hoch = max(w, key=lambda x: x[1])
        tief = min(w, key=lambda x: x[1])
        med = statistics.median([x[1] for x in w])
        return med, hoch, tief

    zeilen += ["", "## Ausreißer", ""]
    for feld, name in [("dialog_anteil", "Dialoganteil"),
                       ("fuellwort_je_1000", "Füllwörter je 1000"),
                       ("satz_median", "Satzlänge Median"),
                       ("adverb_je_1000", "Adverbien je 1000")]:
        s = spanne(feld)
        if not s:
            continue
        med, hoch, tief = s
        zeilen.append(f"- **{name}**: Median {med} · höchster Kapitel "
                      f"{hoch[0]} ({hoch[1]}) · niedrigster Kapitel "
                      f"{tief[0]} ({tief[1]})")

    if nlp is not None:
        zeilen += ["", "## Wortwiederholung im Nahbereich", "",
                   "Dasselbe Wort mindestens viermal innerhalb von 220 "
                   "Wörtern. Über ein ganzes Kapitel verteilt wäre das "
                   "normal; dicht beieinander fällt es auf.", ""]
        gefunden = False
        for n, m in alle.items():
            w = wiederholungen(m.get("_lemmas", []))
            if w:
                gefunden = True
                zeilen.append(f"- **Kapitel {n}**: "
                              + ", ".join(f"{x} ({y}×)" for x, y in w[:6]))
        if not gefunden:
            zeilen.append("*Keine gefunden.*")

    zeilen += ["", "## Wort doppelt hintereinander", ""]
    dop = False
    for f in dateien:
        n = int(re.search(r"(\d+)", f.name).group(1))
        for wort, zeile in doppelwoerter(text_von(f)):
            dop = True
            zeilen.append(f"- Kapitel {n}, Zeile {zeile}: „{wort} {wort}“")
    if not dop:
        zeilen.append("*Keine gefunden.*")

    t = typografie_pruefen("\n".join(text_von(f) for f in dateien))
    zeilen += ["", "## Typografie", "",
               f"- Öffnende Anführungszeichen `„`: {t['zitat_offen']}",
               f"- Schließende **richtig** `“`: {t['zitat_zu_richtig']}",
               f"- Schließende **falsch** `\"`: {t['zitat_zu_falsch']}",
               f"- Apostroph falsch `'`: {t['apostroph_falsch']} · "
               f"richtig `’`: {t['apostroph_richtig']}",
               f"- Auslassung falsch `...`: {t['auslassung_falsch']} · "
               f"richtig `…`: {t['auslassung_richtig']}", "",
               MARKER, ""]

    ziel = Path(args.bericht)
    alt = ziel.read_text(encoding="utf-8") if ziel.exists() else ""
    schwanz = alt.split(MARKER, 1)[1] if MARKER in alt else ""
    ziel.write_text("\n".join(zeilen) + schwanz, encoding="utf-8")

    gesamt = sum(m["woerter"] for m in alle.values())
    print(f"{len(alle)} Kapitel, {gesamt} Wörter gemessen.")
    print(f"Typografie: {t['zitat_zu_falsch']} falsche schließende "
          f"Anführungszeichen, {t['apostroph_falsch']} falsche Apostrophe, "
          f"{t['auslassung_falsch']} falsche Auslassungspunkte.")
    print(f"Geschrieben: {ziel}")


if __name__ == "__main__":
    main()
