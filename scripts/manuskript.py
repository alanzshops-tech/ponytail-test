#!/usr/bin/env python3
"""
manuskript.py — setzt Vorspann, Kapitel und Nachspann zu einer Datei
zusammen und zählt nach.

Wozu: Bei KDP wird eine Datei hochgeladen, nicht dreißig. Die von Hand
zusammenzukopieren ist genau die Art Arbeit, bei der ein Kapitel
verschwindet und es niemandem auffällt. Deshalb baut das hier die Datei
jedes Mal neu aus den Einzelteilen und meldet, was drin ist.

Die Prüfungen sind nicht Zierrat, sondern die Fehler, die dabei
tatsächlich passieren:
  * Lücke in der Kapitelnummerierung (1, 2, 4 …)
  * doppelte Kapitelnummer
  * Kapitel ohne Überschrift
  * Perspektivwechsel gebrochen (zweimal hintereinander dieselbe Figur)
  * Platzhalter in eckigen Klammern, die noch im Text stehen

Aufruf:
    python3 scripts/manuskript.py
    python3 scripts/manuskript.py --autor "Marie Falk"
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime, time
from pathlib import Path

BUCH = Path(__file__).resolve().parent.parent / "buch"


def woerter(text: str) -> int:
    return len(text.split())


def kapitel_lesen() -> list[tuple[int, Path, str]]:
    raus = []
    for p in sorted(BUCH.glob("kapitel-*.md")):
        m = re.search(r"kapitel-(\d+)", p.name)
        if not m:
            continue
        raus.append((int(m.group(1)), p, p.read_text(encoding="utf-8")))
    return raus


def platzhalter(text: str) -> list[str]:
    """Findet [PLATZHALTER] in eckigen Klammern.

    Markdown-Links werden ausgelassen — aber nicht daran, dass der
    Klammerinhalt mit http anfaengt: Bei `[Link](http://x)` steht das
    http hinter der Klammer, nicht darin. Der Selbsttest hat genau das
    gefunden. Erkannt wird der Link deshalb an der runden Klammer, die
    direkt folgt.
    """
    return [" ".join(t.split())[:60]
            for t in re.findall(r"\[([A-ZÄÖÜ][^\]]{2,80})\](?!\()", text,
                                re.S)]


def selbsttest() -> bool:
    """Ein Pruefwerkzeug, das nie etwas findet, sieht genauso aus wie
    ein sauberes Manuskript. Am 15.08.2026 meldete dieses hier 'Keine
    Beanstandungen', waehrend neun Platzhalter im Vorspann standen --
    nicht weil die Erkennung falsch war, sondern weil sie auf den
    Vorspann gar nicht angewendet wurde. Seitdem: erst pruefen, ob das
    Pruefen prueft."""
    ok = True

    fund = platzhalter("Text mit [VORNAME NACHNAME] darin.")
    print(f"  Platzhalter, Positivfall: {fund}")
    if fund != ["VORNAME NACHNAME"]:
        print("  FEHLGESCHLAGEN: bekannter Platzhalter nicht gefunden.")
        ok = False

    sauber = platzhalter("Ein [Link](http://x) und ein Satz.")
    print(f"  Platzhalter, Negativfall: {sauber}")
    if sauber:
        print("  FEHLGESCHLAGEN: sauberer Text meldet einen Platzhalter.")
        ok = False

    gebrochen = [(1, Path("a.md"), "# Kapitel 1 — Leni\n"),
                 (2, Path("b.md"), "# Kapitel 2 — Leni\n")]
    k = pruefen(gebrochen)
    print(f"  Perspektive, Positivfall: {len(k)} Beanstandung(en)")
    if not any("Perspektivwechsel" in x for x in k):
        print("  FEHLGESCHLAGEN: zweimal Leni wurde nicht bemerkt.")
        ok = False

    heil = [(1, Path("a.md"), "# Kapitel 1 — Leni\n"),
            (2, Path("b.md"), "# Kapitel 2 — Jonas\n")]
    if any("Perspektivwechsel" in x for x in pruefen(heil)):
        print("  FEHLGESCHLAGEN: sauberer Wechsel wird beanstandet.")
        ok = False

    luecke = [(1, Path("a.md"), "# Kapitel 1 — Leni\n"),
              (3, Path("c.md"), "# Kapitel 3 — Leni\n")]
    if not any("Fehlende Kapitel" in x for x in pruefen(luecke)):
        print("  FEHLGESCHLAGEN: Luecke in der Nummerierung nicht bemerkt.")
        ok = False

    print("  Selbsttest bestanden." if ok else "  Selbsttest FEHLGESCHLAGEN.")
    return ok


def pruefen(kapitel: list[tuple[int, Path, str]]) -> list[str]:
    klagen = []
    nummern = [n for n, _, _ in kapitel]

    if not nummern:
        return ["Keine Kapitel gefunden."]
    doppelt = {n for n in nummern if nummern.count(n) > 1}
    if doppelt:
        klagen.append(f"Doppelte Kapitelnummern: {sorted(doppelt)}")
    luecken = [n for n in range(1, max(nummern) + 1) if n not in nummern]
    if luecken:
        klagen.append(f"Fehlende Kapitel: {luecken}")

    letzte_figur = None
    for n, p, text in kapitel:
        kopf = text.lstrip().split("\n", 1)[0]
        if not kopf.startswith("# "):
            klagen.append(f"{p.name}: keine Überschrift in der ersten Zeile")
            continue
        m = re.search(r"—\s*(\w+)", kopf)
        figur = m.group(1) if m else None
        if figur and figur == letzte_figur:
            klagen.append(
                f"Kapitel {n}: zweimal hintereinander {figur} — der "
                f"Perspektivwechsel ist gebrochen")
        letzte_figur = figur

        for treffer in platzhalter(text):
            klagen.append(f"{p.name}: Platzhalter [{treffer}]")

    # Vorspann und Nachspann mitpruefen. Genau dort stehen die
    # Platzhalter, die vor dem Hochladen ersetzt werden muessen --
    # Impressum, Autorenname, Jahr. Sie hier auszulassen war der Fehler,
    # der "Keine Beanstandungen" ausgab, obwohl neun offen waren.
    for name in ("00-vorspann.md", "99-nachspann.md"):
        datei = BUCH / name
        if not datei.exists():
            klagen.append(f"{name} fehlt")
            continue
        for treffer in platzhalter(datei.read_text(encoding="utf-8")):
            klagen.append(f"{name}: Platzhalter [{treffer}]")
    return klagen


CSS = """
body { font-family: serif; line-height: 1.5; margin: 0 6%; }
h1 { font-size: 1.5em; text-align: center; margin: 2.5em 0 1.5em;
     font-weight: normal; letter-spacing: 0.08em; }
h2 { font-size: 1.15em; text-align: center; margin: 2em 0 1em;
     font-weight: normal; }
p { text-indent: 1.2em; margin: 0; text-align: justify; }
p:first-of-type, h1 + p, h2 + p, hr + p { text-indent: 0; }
hr { border: 0; text-align: center; margin: 1.6em 0; }
/* Das Trennzeichen steht als echtes Zeichen da, nicht als CSS-Escape.
   Bis zum 19.08.2026 stand hier content: "\\2042" -- gemeint war das
   Asterism U+2042. Python hat \\204 aber als Oktalzahl gelesen, also
   als Steuerzeichen U+0084, und die 2 blieb als Ziffer stehen. Im
   Lesegeraet stand an allen 471 Szenenwechseln ein Kaestchen und eine
   2. Als "diese 2 irritiert" gemeldet. epubcheck.py prueft seitdem
   auch das Stylesheet auf Steuerzeichen. */
hr:after { content: "⁂"; }
blockquote { font-style: italic; margin: 1.2em 2em; }
blockquote p { text-indent: 0; }
"""


REIHE = "Die Reinhardt-Brüder"

# Namen, die im Impressum stehen muessen und sonst nirgends. dc:creator
# ist der Name, der im Laden steht; am 31.08.2026 stand dort der
# Klarname, weil ein Bau mit --autor "Alan Lorenz" aufgerufen worden
# war. Der Vorgabewert war richtig, der Aufruf nicht -- und ein
# Werkzeug, bei dem ein falscher Aufruf den Klarname in tausend
# verkaufte Dateien schreibt, ist falsch gebaut. Jetzt bricht es ab.
KLARNAMEN = {"Alan Lorenz", "Alan Lorenz GbR"}

# Der Klappentext in dc:description ist nicht dasselbe Feld wie die
# Produktbeschreibung bei KDP -- die wird im Formular eingegeben. Hier
# steht er fuer Lesegeraete, Kataloge und jeden Haendler, der die Datei
# selbst ausliest. Beide sollten denselben Text tragen; die abgenommene
# Fassung steht in buch2/KDP-LAUNCH-2.md.
KLAPPENTEXT = {
    "2": """Sie sind verheiratet. Sie waren noch nie miteinander aus.

Kopenhagen, März 2025: eine Standesbeamtin, ein Zeuge, den sie sich von
der Straße geholt haben, und zwei Menschen, die beschließen, es
niemandem zu erzählen. Amira Haddad begutachtet historische
Bausubstanz und schreibt gerade für die Firma seiner Familie — eine Ehe
darin wäre ein Angriffspunkt. Theo Reinhardt will zum ersten Mal etwas
haben, das niemand besichtigt.

Vierzehn Monate später steht die Ausländerbehörde vor der Tür. Keine
gemeinsame Adresse, kein gemeinsames Konto, sieben Fotos. Am Montag um
elf sitzen die beiden in getrennten Räumen und sollen beweisen, dass
ihre Ehe echt ist.

Sie ist echt. Sie ist nur nie gelebt worden.

Was jetzt kommt, machen sie zum ersten Mal: zusammenwohnen. Sich
streiten, wo jemand zusieht. Seine Bücher zwischen ihre stellen. Und
irgendwann klingelt er unten an einer Haustür, an der sein eigener Name
steht, weil sie einmal im Leben hören will, dass jemand für sie
klingelt.

Band 2 der Reihe „Die Reinhardt-Brüder". In sich abgeschlossen, mit
Happy End — kein Cliffhanger für dieses Paar. Emotional und sinnlich,
ohne explizite Szenen.""",
}

# Fuenf bis sieben Schlagworte, aus den gemessenen Nischen und nicht
# geraten (buch2/KDP-LAUNCH-2.md, Lauf vom 31.08.2026). dc:subject ist
# nicht das KDP-Keyword-Feld -- die sieben Keywords stehen dort und
# duerfen sich mit Titel und Untertitel nicht doppeln; hier gilt diese
# Regel nicht.
SCHLAGWORTE = [
    "Liebesroman",
    "Familiengeheimnis",
    "Geheime Ehe",
    "Zeitgenössischer Liebesroman",
    "Familiensaga",
    "Hamburg",
    "Deutschsprachige Gegenwartsliteratur",
]


def sortiername(name: str) -> str:
    """"Jule Norden" -> "Norden, Jule". Fuer dc:creator/file-as."""
    teile = name.split()
    return f"{teile[-1]}, {' '.join(teile[:-1])}" if len(teile) > 1 else name


def metadaten(band: str) -> list[tuple[str, str]]:
    m = [("publisher", "Alan Lorenz GbR"), ("date", "2026")]
    if band in KLAPPENTEXT:
        m.append(("description", KLAPPENTEXT[band]))
    m += [("subject", s) for s in SCHLAGWORTE]
    return m


def epub_bauen(kapitel, vorspann: str, nachspann: str, titel: str,
               autor: str, ziel: Path, coverbild: Path | None) -> None:
    """KDP nimmt DOCX, EPUB oder KPF — kein Markdown. Ohne diesen
    Schritt ist das Manuskript keine hochladbare Datei."""
    import markdown as md
    from ebooklib import epub

    buch = epub.EpubBook()
    # Die Kennung muss sich aendern, wenn sich der Inhalt aendert.
    # Bis zum 18.08.2026 stand hier nur der Titel -- jede neue Fassung
    # trug damit dieselbe Kennung, und Lesegeraete erkennen Buecher
    # genau daran. Wer eine aeltere Fassung importiert hatte, bekam die
    # neue nicht zu sehen: gleiche Kennung, also dasselbe Buch. Drei Mal
    # als "steht immer noch das Alte drin" gemeldet, bevor es aufgefallen
    # ist.
    #
    # Aus dem Inhalt gebildet, nicht zufaellig: gleicher Text gibt
    # dieselbe Kennung, der Bau bleibt reproduzierbar.
    #
    # Die Regel dazu lautet: **Alles, was in die Datei geht, geht in die
    # Kennung.** Sie ist zweimal gebrochen worden, jedes Mal eine Ebene
    # tiefer, und jedes Mal hat es dieselbe Meldung ausgeloest.
    #
    #   18.08.2026  Das Umschlagbild fehlte im Hash. Nur das Bild wurde
    #               getauscht, der Text blieb gleich -- gleiche Kennung,
    #               also fuer das Lesegeraet dasselbe Buch, also der
    #               alte Umschlag.
    #   31.08.2026  Klappentext, Verlag, Schlagworte und die
    #               Reihenangabe kamen dazu -- alle vier stehen in
    #               content.opf, also gehoeren sie in die Kennung.
    #   19.08.2026  Das Stylesheet fehlte im Hash. Behoben wurde eine
    #               kaputte Zeile CSS, Text und Bild blieben gleich --
    #               wieder gleiche Kennung, wieder die alte Fassung.
    #
    # Wer hier eine neue Zutat einbaut -- Schriftart, zweites Bild,
    # Nachwort --, traegt sie in diese Liste ein.
    import hashlib
    h = hashlib.sha256()
    band = "2" if BUCH.name.endswith("2") else "1"
    for teil in ([titel, autor, vorspann, nachspann, CSS, REIHE]
                 + [w for _, w in metadaten(band)]
                 + [t for _, _, t in kapitel]):
        h.update(teil.encode("utf-8"))
    if coverbild and coverbild.exists():
        h.update(coverbild.read_bytes())
    kennung = h.hexdigest()[:12]
    # Das Praefix kommt aus dem Buchordner, nicht aus einer festen
    # Zeichenkette. Bis zum 24.08.2026 stand hier "reinhardt-1-", und
    # Band 2 trug damit eine Kennung, die ihn als Band 1 auswies. Die
    # Buecher waren trotzdem unterscheidbar, weil der Hash sich
    # unterscheidet -- aufgefallen ist es erst, als beide Kennungen
    # nebeneinander ausgegeben wurden.
    buch.set_identifier(f"reinhardt-{band}-{kennung}")
    buch.set_title(titel)
    buch.set_language("de")
    # file_as und role sind nicht Zierrat: Ohne file-as sortieren
    # Lesegeraete und Bibliothekskataloge nach dem Vornamen, ohne role
    # steht nicht in der Datei, dass diese Person die Verfasserin ist
    # und nicht Herausgeberin oder Uebersetzerin.
    if autor in KLARNAMEN:
        raise SystemExit(
            f"dc:creator waere '{autor}' -- ein Klarname aus dem "
            f"Impressum. Er gehoert nicht in die Metadaten. Pseudonym "
            f"verwenden (Vorgabewert: Jule Norden).")
    buch.add_author(autor, file_as=sortiername(autor), role="aut")

    for name, wert in metadaten(band):
        buch.add_metadata("DC", name, wert)

    # Reihen-Metadaten nach EPUB 3.2. Amazon und Kobo bauen daraus die
    # Serienseite; ohne sie stehen die Baende als Einzeltitel da.
    buch.add_metadata(None, "meta", REIHE,
                      {"property": "belongs-to-collection", "id": "serie"})
    buch.add_metadata(None, "meta", "series",
                      {"refines": "#serie", "property": "collection-type"})
    buch.add_metadata(None, "meta", band,
                      {"refines": "#serie", "property": "group-position"})

    stil = epub.EpubItem(uid="stil", file_name="style.css",
                         media_type="text/css", content=CSS)
    buch.add_item(stil)

    if coverbild and coverbild.exists():
        buch.set_cover("cover.jpg", coverbild.read_bytes())

    def seite(name: str, kopf: str, text: str):
        k = epub.EpubHtml(title=kopf, file_name=name, lang="de")
        k.content = md.markdown(text, extensions=["extra"])
        k.add_item(stil)
        buch.add_item(k)
        return k

    seiten = [seite("vorspann.xhtml", "Titel", vorspann)]
    for n, _, text in kapitel:
        kopf = text.lstrip().split("\n", 1)[0].lstrip("# ").strip()
        seiten.append(seite(f"kap{n:02d}.xhtml", kopf, text))
    seiten.append(seite("nachspann.xhtml", "Die Reinhardt-Brüder",
                        nachspann))

    buch.toc = tuple(seiten)

    # Startposition. Ohne diese Angabe oeffnet der Kindle auf der ersten
    # Seite der Datei, und "Blick ins Buch" bei Amazon faengt dort an.
    # Das kostet in einer Leseprobe von zehn Prozent die ersten Seiten
    # fuer Titelei und Hinweise. Mit guide/landmarks vom Typ
    # "text" bzw. "bodymatter" faengt beides bei Kapitel 1 an.
    erstes_kapitel = seiten[1].file_name if len(seiten) > 1 else "vorspann.xhtml"
    buch.guide = [{"type": "text", "href": erstes_kapitel,
                   "title": "Anfang"}]
    # Der Cover-Eintrag nur, wenn es auch ein Cover gibt. Er stand hier
    # bis zum 24.08.2026 fest verdrahtet, weil Band 1 immer eins hatte.
    # Der erste Bau von Band 2 lief ohne, und die fertige Datei trug
    # danach im Verzeichnis einen Verweis auf eine cover.xhtml, die es
    # nicht gab -- ein toter Link, gefunden von epubcheck.py, nicht beim
    # Lesen.
    if coverbild and coverbild.exists():
        buch.guide.insert(0, {"type": "cover", "href": "cover.xhtml",
                              "title": "Cover"})

    buch.add_item(epub.EpubNcx())
    buch.add_item(epub.EpubNav())
    # Die Umschlagseite gehoert in den spine, auch wenn sie nicht
    # mitgelesen wird (is_linear=False). Bis zum 31.08.2026 stand sie
    # nur im Manifest, waehrend die Landmarks in nav.xhtml auf sie
    # zeigten -- und EPUB 3.3 verlangt, dass jedes Nav-Ziel ein
    # spine-Eintrag ist. Der offizielle epubcheck von W3C meldet das als
    # RSC-011; der hauseigene epubcheck.py hat es nicht gesehen, weil er
    # auf tote Verweise prueft und cover.xhtml ja existiert. Der Fehler
    # steckte in jeder bisher gebauten Datei, in beiden Baenden.
    umschlagseite = [buch.get_item_with_id("cover")] if coverbild \
        and coverbild.exists() else []
    buch.spine = umschlagseite + ["nav"] + seiten
    # ebooklib stempelt sonst die aktuelle Uhrzeit in content.opf. Dann
    # unterscheidet sich jede neu gebaute EPUB von der alten, obwohl kein
    # Wort anders ist, und `git status` meldet eine Aenderung, die keine
    # ist. Ueber die mtime-Option nur das Datum setzen -- am selben Tag
    # zweimal gebaut ergibt Byte fuer Byte dieselbe Datei.
    #
    # Nicht ueber add_metadata: dcterms:modified darf laut EPUB-3-Spec
    # genau einmal vorkommen. ebooklib filtert Doubletten nur im
    # OPF-Namensraum heraus, ein selbst hinzugefuegter Eintrag landet
    # zusaetzlich in der Datei. Genau das war beim ersten Versuch der
    # Fall -- zwei Zeitstempel in content.opf.
    heute = datetime.combine(date.today(), time.min)
    epub.write_epub(str(ziel), buch, {"mtime": heute})
    zip_normalisieren(ziel)


def zip_normalisieren(datei: Path) -> None:
    """Schreibt das EPUB-Archiv mit festen Eintragszeitstempeln neu.

    Auch nach der mtime-Option blieb die Datei zwischen zwei Laeufen
    verschieden: Der Inhalt war Byte fuer Byte gleich, aber alle 38
    ZIP-Eintraege trugen die Uhrzeit des Laufs. Fuer eine Binaerdatei im
    Repository heisst das: jeder Neubau erzeugt einen Diff, und die
    Historie waechst um 240 kB, ohne dass ein Wort anders ist.

    Die EPUB-Regel dabei: `mimetype` muss der erste Eintrag sein und
    unkomprimiert gespeichert werden, sonst erkennen manche Lesegeraete
    das Paket nicht.
    """
    import shutil
    import tempfile
    import zipfile

    fest = (2000, 1, 1, 0, 0, 0)
    quelle = zipfile.ZipFile(datei)
    eintraege = quelle.infolist()
    reihenfolge = ([e for e in eintraege if e.filename == "mimetype"]
                   + [e for e in eintraege if e.filename != "mimetype"])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp:
        pfad = tmp.name
    with zipfile.ZipFile(pfad, "w") as neu_zip:
        for e in reihenfolge:
            daten = quelle.read(e.filename)
            info = zipfile.ZipInfo(e.filename, date_time=fest)
            if e.filename == "mimetype":
                info.compress_type = zipfile.ZIP_STORED
            else:
                info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = e.external_attr
            neu_zip.writestr(info, daten)
    quelle.close()
    shutil.move(pfad, datei)


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--autor", default=None,
                   help="ersetzt [AUTORENNAME] im Vorspann")
    p.add_argument("--buch", default="buch",
                   help="Ordner mit Kapiteln, Vor- und Nachspann "
                        "(zweiter Band: --buch buch2)")
    # Ohne Angabe richten sich Ziel, EPUB und Titel nach --buch. Vorher
    # standen hier feste Band-1-Werte: Ein Lauf mit --buch buch2 und
    # ohne die anderen drei Schalter hat am 01.09.2026 den Text von
    # Band 2 in buch/manuskript.md und buch/reinhardt-1.epub
    # geschrieben, unter dem Titel von Band 1. Dieselbe Bauart hatte
    # prosa.py schon einmal, mit demselben Ergebnis. Ein Werkzeug, das
    # man vollstaendig aufrufen muss, damit es nichts kaputtmacht, ist
    # falsch gebaut -- der Vorgabewert muss dem Buch folgen.
    p.add_argument("--ziel", default=None)
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--epub", default=None,
                   help="Zieldatei für die EPUB (leer = überspringen)")
    # Auch das Cover richtet sich nach --buch. Diese Vorgabe ist beim
    # Umbau am 01.09.2026 uebersehen worden: --ziel, --epub und --titel
    # sind mitgezogen, --cover blieb auf Band 1 stehen. Ergebnis war,
    # dass die fertige Band-2-EPUB das Cover von Band 1 getragen hat --
    # im Paket nachgewiesen, gleiche Pruefsumme. Vierte Stelle dieser
    # Bauart nach prosa.py, --ziel/--epub/--titel.
    p.add_argument("--cover", default=None)
    p.add_argument("--titel", default=None)
    args = p.parse_args()

    global BUCH
    BUCH = Path(args.buch)

    zweiter = BUCH.name.endswith("2")
    if args.ziel is None:
        args.ziel = str(BUCH / "manuskript.md")
    if args.epub is None:
        args.epub = str(BUCH / ("Was-er-nie-gefragt-hat_v2.epub" if zweiter
                                else "reinhardt-1.epub"))
    if args.titel is None:
        args.titel = ("Was er nie gefragt hat" if zweiter
                      else "Was ich dir nie gesagt habe")
    if args.cover is None:
        args.cover = ("cover/band2/cover.jpg" if zweiter
                      else "cover/fertig/cover.jpg")

    print("Kalibrierung der Pruefungen:")
    if not selbsttest():
        raise SystemExit(2)
    if args.selbsttest:
        return
    print()

    kapitel = kapitel_lesen()
    klagen = pruefen(kapitel)

    vorspann = (BUCH / "00-vorspann.md").read_text(encoding="utf-8")
    nachspann = (BUCH / "99-nachspann.md").read_text(encoding="utf-8")
    # Die Zeile "# Vorspann" und der HTML-Kommentar sind Arbeitsnotizen
    # und gehoeren nicht ins Buch.
    vorspann = re.sub(r"^# (Vorspann|Nachspann)\n+<!--.*?-->\n+", "",
                      vorspann, flags=re.S)
    nachspann = re.sub(r"^# (Vorspann|Nachspann)\n+<!--.*?-->\n+", "",
                       nachspann, flags=re.S)
    if args.autor:
        vorspann = vorspann.replace("[AUTORENNAME]", args.autor)

    teile = [vorspann.rstrip(), ""]
    for _, _, text in kapitel:
        teile += [text.rstrip(), "", "---", ""]
    teile += [nachspann.rstrip(), ""]

    ganz = "\n".join(teile)
    ziel = Path(args.ziel)
    ziel.write_text(ganz, encoding="utf-8")

    roh = sum(woerter(t) for _, _, t in kapitel)
    print(f"{len(kapitel)} Kapitel, {roh:,} Wörter Fließtext, "
          f"{woerter(ganz):,} Wörter gesamt".replace(",", "."))
    print(f"Geschrieben: {ziel}")

    kurz = [(n, woerter(t)) for n, _, t in kapitel if woerter(t) < 900]
    if kurz:
        print("\nKapitel unter 900 Wörtern: "
              + ", ".join(f"{n} ({w})" for n, w in kurz))

    if args.epub:
        try:
            epub_bauen(kapitel, vorspann, nachspann, args.titel,
                       # Ohne --autor stand hier bis zum 16.08.2026
                       # "[AUTORENNAME]" in den EPUB-Metadaten -- im
                       # Vorspann und auf dem Umschlag steht der Name
                       # laengst, nur das Feld, das KDP ausliest, war
                       # leer. Die Platzhalterpruefung sieht nur den
                       # Text, nicht die Metadaten.
                       args.autor or "Jule Norden", Path(args.epub),
                       Path(args.cover) if args.cover else None)
            groesse = Path(args.epub).stat().st_size / 1024
            print(f"Geschrieben: {args.epub} ({groesse:.0f} kB, "
                  f"{len(kapitel) + 2} Abschnitte)")
        except Exception as e:
            # Bis zum 16.08.2026 wurde hier nur gedruckt und danach
            # trotzdem "Keine Beanstandungen" gemeldet. Ein Lauf ohne
            # markdown-Modul sah aus wie ein sauberer Lauf, und die
            # EPUB im Ordner war stillschweigend die alte.
            print(f"EPUB fehlgeschlagen: {str(e)[:200]}")
            klagen.append(f"EPUB nicht gebaut: {str(e)[:120]}")

    if klagen:
        print(f"\n{len(klagen)} Beanstandung(en):")
        for k in klagen:
            print(f"  - {k}")
    else:
        print("\nKeine Beanstandungen.")


if __name__ == "__main__":
    main()
