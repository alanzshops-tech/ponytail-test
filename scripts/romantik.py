#!/usr/bin/env python3
"""
romantik.py — misst, wo im Buch die beiden zusammen sind und wo nicht.

Wozu: Ein Liebesroman lebt davon, dass die zwei Hauptfiguren im selben
Raum stehen. Alles andere — Bank, Beirat, Gutachten — ist Beiwerk. Beim
Lesen merkt man nicht, dass zwischen Kapitel 46 und 51 sechs Kapitel
liegen, in denen kaum etwas zwischen ihnen passiert; man merkt nur, dass
es zaeh wird. Von Hand ist das nicht zu zaehlen, ohne sich zu verzaehlen.

Gemessen wird pro Kapitel:

  Szene    Steht die andere Hauptfigur mit im Raum? Erkannt daran, dass
           ihr Name in der Naehe einer Dialogzeile steht — nicht daran,
           dass er ueberhaupt vorkommt. "Ich habe an Jonas gedacht" ist
           keine gemeinsame Szene.
  Beruehr  Koerperliche Naehe: Hand, Arm, Schulter, Haut, Kuss.
  Sehnen   Blick, Naehe, Wollen, Vermissen.
  Konflikt Streit, Vorwurf, Rueckzug.

Die Zahlen sind rohe Trefferzahlen, keine Quoten — die Kapitel sind
mit 850 bis 1980 Woertern aehnlich lang genug, dass eine Normierung
nichts aendern wuerde. Die Wortzahl steht daneben, damit man es
nachpruefen kann.

Grenze des Geraets: Kapitel 1 zeigt null gemeinsame Szenen, obwohl er am
Ende darin steht. Sie kennt seinen Namen zu diesem Zeitpunkt noch nicht
und nennt ihn nie. Das ist der einzige bekannte Fehltreffer; alle
anderen Nullen sind von Hand nachgesehen.

    python3 scripts/romantik.py --selbsttest
    python3 scripts/romantik.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BUCH = Path(__file__).resolve().parent.parent / "buch"

# Nur Wortstaemme, die ohne Kontext eindeutig sind. "nah" faengt
# "nahm" — deshalb steht hier nicht "nah", sondern die Formen einzeln.
BERUEHRUNG = re.compile(
    r"\b(berühr\w*|angefasst|festgehalten|umarm\w*|Umarmung|küss\w*|Kuss|"
    r"Hand\b|Hände|Handgelenk|Finger\w*|Arm\b|Arme\b|Schulter\w*|"
    r"Haut\b|Wange\w*|Nacken|Haar\w*|Lippen|Stirn\b)", re.I)

SEHNSUCHT = re.compile(
    r"\b(angesehen|ansah|Blick\w*|angeschaut|gesehen hat, wie|"
    r"vermisst\w*|gefehlt hat|nah\b|näher|Nähe\b|dicht\b|"
    r"gewollt|wollte ihn|wollte sie|wollte, dass er|wollte, dass sie|"
    r"gerochen|Geruch\b|Atem\b|geatmet)", re.I)

KONFLIKT = re.compile(
    r"\b(geschrien|geschrie\w*|angeschrien|Vorwurf|vorgeworfen|"
    r"rausgeworfen|geh\b|Verschwinde|gestritten|Streit\b|wütend|"
    r"Wut\b|zugemacht|weggegangen|gegangen ist|aufgelegt|"
    r"nicht mehr angerufen|hasse|verlogen|betrogen|belogen)", re.I)

DIALOG = re.compile(r"^\s*[„»]", re.M)


def kapitelnummer(p: Path) -> int:
    return int(re.match(r"kapitel-(\d+)\.md$", p.name).group(1))


def perspektive(text: str) -> str:
    m = re.search(r"^#.*—\s*(\w+)", text, re.M)
    return m.group(1) if m else "?"


def fliesstext(text: str) -> str:
    zeilen = [z for z in text.splitlines()
              if not z.startswith("#") and z.strip() != "---"]
    return "\n".join(zeilen)


# Die beiden nennen einander nicht beim selben Namen. Er sagt
# "Marlene", sie sagt "Jonas" oder "Reinhardt", Behoerden sagen "Frau
# Voss". Ein Selektor mit nur einem Namen fand in *jedem* Jonas-Kapitel
# null gemeinsame Szenen — ein leeres Ergebnis, das offensichtlich falsch
# war. Am 16.08.2026 korrigiert.
#
# Band 2 am 24.08.2026 dazugekommen. Nachschlag erfolgt ueber die
# Perspektive, und die vier Namen sind ueber beide Baende eindeutig, also
# braucht es keine zweite Tabelle. Zwei Fallen dabei:
#
#   * "Reinhardt" darf bei Amira NICHT drinstehen. In Band 2 heissen so
#     vier Brueder, die Mutter und die Firma; in Theos eigenen Kapiteln
#     stuende der Nachname in fast jedem Absatz und wuerde jede Sitzung
#     ueber Rothenburgsort als Liebesszene zaehlen.
#   * "Herr Reinhardt" ist ebenfalls unbrauchbar — die Behoerde nennt in
#     Kapitel 23 und 24 beide Ehepartner so, und Wendland meint damit in
#     Kapitel 22 mal Jonas und mal Theo.
#
# Uebrig bleibt der Vorname, plus die Behoerdenanrede fuer sie, die
# eindeutig ist.
NAMEN = {
    "Leni":  ("Jonas", "Reinhardt"),
    "Jonas": ("Marlene", "Leni", "Frau Voss"),
    "Amira": ("Theo",),
    "Theo":  ("Amira", "Frau Haddad"),
}


def gemeinsame_szene(text: str, namen) -> int:
    """Absaetze, in denen der andere neben einer Dialogzeile steht.

    Der Name allein reicht nicht: In fast jedem Leni-Kapitel kommt
    "Jonas" vor, weil sie an ihn denkt. Gezaehlt wird nur, wo er
    spricht oder wo jemand mit ihm spricht — also wo sein Name und
    eine Dialogzeile im selben Absatzblock stehen.
    """
    treffer = 0
    bloecke = re.split(r"\n\s*---\s*\n", text)
    for b in bloecke:
        absaetze = re.split(r"\n\s*\n", b)
        for i, a in enumerate(absaetze):
            if not any(n in a for n in namen):
                continue
            # Mit Zeilenumbruch verbinden, nicht mit Leerzeichen: das
            # Dialogmuster prueft den Zeilenanfang. Am 16.08.2026 im
            # Selbsttest aufgefallen — der Positivfall fiel durch.
            umfeld = "\n\n".join(absaetze[max(0, i - 2):i + 3])
            if DIALOG.search(umfeld):
                treffer += 1
    return treffer


def selbsttest() -> None:
    """Jedes Muster gegen einen Fall, der treffen muss, und einen, der nicht darf."""
    fehler = []

    # Beruehrung: darf "nahm" nicht als Naehe zaehlen, muss "Hand" fangen.
    if not BERUEHRUNG.search("Er hat meine Hand genommen."):
        fehler.append("Beruehrung findet 'Hand' nicht.")
    if BERUEHRUNG.search("Sie nahm den Ordner und ging zur Tür."):
        fehler.append("Beruehrung faengt einen Satz ohne Koerperkontakt.")

    # Konflikt: "gegangen ist" ja, "gegangen war einkaufen" nein.
    if not KONFLIKT.search("Ich habe ihn angeschrien."):
        fehler.append("Konflikt findet 'angeschrien' nicht.")
    if KONFLIKT.search("Der Ofen braucht vierzig Minuten."):
        fehler.append("Konflikt faengt einen Satz ohne Streit.")

    # Gemeinsame Szene: Name plus Dialog ja, Name im Gedanken nein.
    ja = ('Jonas stand in der Tür.\n\n„Ich wollte nicht stören.“\n')
    nein = ('Ich habe an Jonas gedacht, den ganzen Nachmittag,\n'
            'während ich Teig ausgerollt habe.\n')
    if gemeinsame_szene(ja, ("Jonas",)) < 1:
        fehler.append("Gemeinsame Szene wird nicht erkannt.")
    if gemeinsame_szene(nein, ("Jonas",)) > 0:
        fehler.append("Ein Gedanke an ihn gilt als gemeinsame Szene.")

    # Band 2: derselbe Test mit dem anderen Paar, plus der Negativfall,
    # wegen dem "Reinhardt" nicht in Amiras Namensliste steht.
    ja2 = ('Theo stand am Herd.\n\n„Ich habe ihn falsch gemacht.“\n')
    nein2 = ('Ich habe den ganzen Nachmittag an Theo gedacht,\n'
             'waehrend ich die Ostwand vermessen habe.\n')
    if gemeinsame_szene(ja2, NAMEN["Amira"]) < 1:
        fehler.append("Band 2: gemeinsame Szene wird nicht erkannt.")
    if gemeinsame_szene(nein2, NAMEN["Amira"]) > 0:
        fehler.append("Band 2: ein Gedanke gilt als gemeinsame Szene.")
    sitzung = ('Wendland hat die Mappe zugemacht.\n\n'
               '„Die Reinhardt Immobilien klagt.“\n')
    if gemeinsame_szene(sitzung, NAMEN["Amira"]) > 0:
        fehler.append("Band 2: eine Sitzung ueber die Firma zaehlt als "
                      "gemeinsame Szene — 'Reinhardt' steht in der Liste.")

    for f in fehler:
        print(f"  FEHLER: {f}")
    if fehler:
        sys.exit("Selbsttest nicht bestanden — die Zahlen unten waeren wertlos.")
    print("  Selbsttest bestanden (je ein Positiv- und ein Negativfall "
          "pro Muster).")


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selbsttest", action="store_true")
    ap.add_argument("--csv", action="store_true")
    ap.add_argument("--buch", default="buch",
                    help="Ordner mit Kapiteln (zweiter Band: --buch buch2 "
                         "-- NAMEN oben im Skript muss dafuer erst auf "
                         "Amira/Theo umgestellt werden)")
    a = ap.parse_args()

    global BUCH
    BUCH = Path(a.buch)

    print("Selbsttest:")
    selbsttest()
    if a.selbsttest:
        return

    dateien = sorted(BUCH.glob("kapitel-*.md"), key=kapitelnummer)
    zeilen = []
    for p in dateien:
        roh = p.read_text(encoding="utf-8")
        pov = perspektive(roh)
        anderer = NAMEN.get(pov, ("Jonas",))
        t = fliesstext(roh)
        w = len(t.split())
        zeilen.append({
            "nr": kapitelnummer(p),
            "pov": pov,
            "woerter": w,
            "szene": gemeinsame_szene(t, anderer),
            "beruehr": len(BERUEHRUNG.findall(t)),
            "sehnen": len(SEHNSUCHT.findall(t)),
            "konflikt": len(KONFLIKT.findall(t)),
        })

    if a.csv:
        print("nr;pov;woerter;szene;beruehr;sehnen;konflikt")
        for z in zeilen:
            print(";".join(str(z[k]) for k in
                           ("nr", "pov", "woerter", "szene", "beruehr",
                            "sehnen", "konflikt")))
        return

    gesamt = sum(z["woerter"] for z in zeilen)
    print(f"\n{len(zeilen)} Kapitel, {gesamt} Woerter.\n")
    print("  Nr  POV    Woerter  Szene  Beruehr  Sehnen  Konflikt   Pos.")
    for z in zeilen:
        bis = sum(x["woerter"] for x in zeilen if x["nr"] <= z["nr"])
        pos = 100 * bis / gesamt
        mark = "  <-- ohne gemeinsame Szene" if z["szene"] == 0 else ""
        print(f"  {z['nr']:>2}  {z['pov']:<5}  {z['woerter']:>6}  "
              f"{z['szene']:>5}  {z['beruehr']:>7}  {z['sehnen']:>6}  "
              f"{z['konflikt']:>8}   {pos:>4.0f}%{mark}")

    ohne = [z["nr"] for z in zeilen if z["szene"] == 0]
    print(f"\nKapitel ohne gemeinsame Szene: {len(ohne)} von {len(zeilen)}")
    print("  " + ", ".join(str(n) for n in ohne))

    # Laengste Strecke ohne gemeinsame Szene — das ist die Stelle, an
    # der eine Leserin das Buch weglegt.
    lauf, best, start, beststart = 0, 0, 0, 0
    for z in zeilen:
        if z["szene"] == 0:
            if lauf == 0:
                start = z["nr"]
            lauf += 1
            if lauf > best:
                best, beststart = lauf, start
        else:
            lauf = 0
    print(f"\nLaengste Strecke ohne gemeinsame Szene: {best} Kapitel "
          f"(ab Kapitel {beststart}).")


if __name__ == "__main__":
    main()
