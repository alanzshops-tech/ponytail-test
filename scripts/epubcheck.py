#!/usr/bin/env python3
"""
epubcheck.py — prueft die fertige EPUB auf das, woran Uploads scheitern.

Wozu: `manuskript.py` baut die Datei und weiss, was hineingehoert. Es
weiss aber nicht, ob dabei etwas kaputtgegangen ist. Genau das ist am
16.08.2026 passiert: Der EPUB-Bau schlug still fehl, im Ordner lag die
alte Datei, und der Autor stand als `[AUTORENNAME]` in den Metadaten.
Gemerkt hat das kein Skript, sondern ein Zufall.

Geprueft wird die fertige Datei, nicht die Quelle. Das ist der ganze
Punkt: Was hier durchfaellt, faellt auch bei Amazon durch oder sieht auf
einem Kindle falsch aus.

  Reihenfolge   Spine gegen Kapitelnummern, Luecken
  Verzeichnis   nav und NCX vorhanden, vollstaendig, gleiche Reihenfolge
  Ueberschrift  jedes Kapitel genau eine h1
  Leer          kein Kapitel unter 200 Woertern
  Doppelt       keine zwei Abschnitte mit gleicher Ueberschrift/Anfang
  Links         jeder interne Verweis zeigt auf eine vorhandene Datei
  Platzhalter   keine eckigen Platzhalter, kein TODO, kein HTML-Kommentar
  Metadaten     Titel, Autor, Sprache, Kennung gesetzt und ohne Platzhalter
  Cover         als Bild vorhanden und als Cover ausgezeichnet
  Zeichen       keine Steuerzeichen in Text, Stylesheet oder Metadaten

    python3 scripts/epubcheck.py --selbsttest
    python3 scripts/epubcheck.py buch/reinhardt-1_KDP_final.epub
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# "[" allein waere zu grob -- in Prosa kommen eckige Klammern vor.
PLATZHALTER = re.compile(
    r"\[(AUTORENNAME|VORNAME|NACHNAME|TITEL|PLATZHALTER|TBD|XXX)[^\]]*\]"
    r"|\bTODO\b|\bFIXME\b|\bLEKTORAT\b|<!--", re.I)

KAPITEL = re.compile(r"kap(\d+)\.xhtml$")

# Zeichen, die niemand gesetzt hat und die ein Lesegeraet als Kaestchen
# malt: C0-Steuerzeichen (ohne Tab, Zeilenumbruch, Wagenruecklauf),
# C1-Steuerzeichen U+0080-U+009F und das Ersatzzeichen U+FFFD.
#
# Gebaut am 19.08.2026, nachdem in der fertigen Datei an jedem
# Szenenwechsel ein Kaestchen und eine 2 stand. Ursache war eine Zeile
# CSS: content: "\2042" in einem Python-String. Python las \204 als
# Oktalzahl, machte U+0084 daraus und liess die 2 als Ziffer stehen.
# Beide Werkzeuge, die es haette sehen muessen, sahen nur den Prosatext
# und nie das Stylesheet.
#
# Absichtlich eng: Gedankenstrich, Anfuehrungszeichen und das Asterism
# sind normale Zeichen und duerfen nicht anschlagen.
STEUERZEICHEN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f�]")

# Geprueft wird jede Textdatei im Paket, nicht nur die Kapitel. Das
# Stylesheet gehoert dazu -- dort stand der Fehler.
TEXTDATEI = (".xhtml", ".html", ".css", ".opf", ".ncx", ".xml")


def text_aus(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())


def pruefe(pfad: Path) -> list[str]:
    klagen: list[str] = []
    z = zipfile.ZipFile(pfad)
    namen = z.namelist()

    if "mimetype" not in namen:
        klagen.append("mimetype fehlt")
    elif z.read("mimetype").strip() != b"application/epub+zip":
        klagen.append("mimetype hat den falschen Inhalt")
    if "META-INF/container.xml" not in namen:
        klagen.append("META-INF/container.xml fehlt")

    opf = next((n for n in namen if n.endswith(".opf")), None)
    if not opf:
        return klagen + ["keine OPF-Datei — das ist keine EPUB"]
    baum = ET.fromstring(z.read(opf))
    ns = {"o": "http://www.idpf.org/2007/opf",
          "d": "http://purl.org/dc/elements/1.1/"}

    # --- Metadaten ---------------------------------------------------
    for feld, name in [("title", "Titel"), ("creator", "Autor"),
                       ("language", "Sprache"), ("identifier", "Kennung")]:
        e = baum.find(f".//d:{feld}", ns)
        wert = (e.text or "").strip() if e is not None else ""
        if not wert:
            klagen.append(f"Metadaten: {name} fehlt oder ist leer")
        elif PLATZHALTER.search(wert):
            klagen.append(f"Metadaten: {name} ist ein Platzhalter ({wert!r})")

    # --- Cover -------------------------------------------------------
    manifest = {i.get("id"): i for i in baum.findall(".//o:item", ns)}
    hat_bild = any(
        i.get("media-type", "").startswith("image/")
        and "cover" in ((i.get("id") or "") + (i.get("href") or "")).lower()
        for i in manifest.values())
    if not hat_bild:
        klagen.append("kein Coverbild im Manifest")
    elif (baum.find(".//o:meta[@name='cover']", ns) is None
          and not any("cover-image" in (i.get("properties") or "")
                      for i in manifest.values())):
        klagen.append("Coverbild ist nicht als Cover ausgezeichnet")

    # --- Spine -------------------------------------------------------
    ordner = opf.rsplit("/", 1)[0] + "/" if "/" in opf else ""
    spine = []
    for ref in baum.findall(".//o:itemref", ns):
        i = manifest.get(ref.get("idref"))
        if i is None:
            klagen.append(f"Spine verweist auf unbekannte id "
                          f"{ref.get('idref')!r}")
            continue
        spine.append(ordner + i.get("href"))

    fehlend = [s for s in spine if s not in namen]
    if fehlend:
        klagen.append(f"Spine verweist auf fehlende Dateien: {fehlend[:3]}")

    nummern = [int(m.group(1)) for s in spine if (m := KAPITEL.search(s))]
    if nummern != sorted(nummern):
        klagen.append("Kapitel stehen im Spine nicht in Reihenfolge")
    elif nummern:
        luecken = [n for n in range(nummern[0], nummern[-1] + 1)
                   if n not in nummern]
        if luecken:
            klagen.append(f"Luecken in der Kapitelfolge: {luecken}")

    # --- Abschnitte ---------------------------------------------------
    titel_gesehen: dict[str, str] = {}
    anfang_gesehen: dict[str, str] = {}
    for s in spine:
        if s not in namen:
            continue
        roh = z.read(s).decode("utf-8", "ignore")
        txt = text_aus(roh)
        # Nur echte Kapitel auf Ueberschrift und Laenge pruefen. Beim
        # ersten Lauf gegen die echte Datei hat dieses Geraet nav.xhtml
        # und den 140 Woerter langen Vorspann angeklagt -- beides richtig
        # so im Buch, falsch im Pruefer.
        ist_kapitel = bool(KAPITEL.search(s))

        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", roh, re.S)
        if ist_kapitel and len(h1) != 1:
            klagen.append(f"{s}: {len(h1)} h1-Ueberschriften (erwartet 1)")
        if ist_kapitel and len(txt.split()) < 200:
            klagen.append(f"{s}: nur {len(txt.split())} Woerter — "
                          f"leerer oder abgebrochener Abschnitt")

        if h1:
            t = text_aus(h1[0])
            if t in titel_gesehen:
                klagen.append(f"{s}: gleiche Ueberschrift wie "
                              f"{titel_gesehen[t]} ({t!r})")
            titel_gesehen[t] = s
        kern = txt[:400]
        if kern and kern in anfang_gesehen:
            klagen.append(f"{s}: gleicher Anfang wie {anfang_gesehen[kern]}")
        anfang_gesehen[kern] = s

        for m in PLATZHALTER.finditer(txt):
            klagen.append(f"{s}: Platzhalter {m.group(0)[:40]!r}")

        for ziel in re.findall(r'href="([^"#]+)', roh):
            if ziel.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            if ordner + ziel not in namen and ziel not in namen:
                klagen.append(f"{s}: toter Verweis auf {ziel!r}")

    # --- Zeichen --------------------------------------------------------
    for n in namen:
        if not n.lower().endswith(TEXTDATEI):
            continue
        inhalt = z.read(n).decode("utf-8", "replace")
        treffer = list(STEUERZEICHEN.finditer(inhalt))
        if treffer:
            stellen = ", ".join(
                f"U+{ord(t.group(0)):04X} bei {t.start()}"
                for t in treffer[:3])
            mehr = f" und {len(treffer)-3} weitere" if len(treffer) > 3 else ""
            klagen.append(f"{n}: Steuerzeichen im Text ({stellen}{mehr}) — "
                          f"das Lesegeraet malt dafuer ein Kaestchen")

    # --- Inhaltsverzeichnis --------------------------------------------
    nav = next((n for n in namen if n.endswith("nav.xhtml")), None)
    if not nav:
        klagen.append("nav.xhtml fehlt (EPUB 3 braucht es)")
    if not any(n.endswith(".ncx") for n in namen):
        klagen.append("NCX fehlt (aeltere Kindle-Geraete brauchen es)")
    if nav:
        roh = z.read(nav).decode("utf-8", "ignore")
        # Nur der toc-Block. nav.xhtml enthaelt danach die Landmarks, und
        # die verweisen absichtlich ein zweites Mal auf Kapitel 1 -- das
        # ist kein doppelter Eintrag, sondern die Startposition.
        m = re.search(r'<nav[^>]*epub:type="toc".*?</nav>', roh, re.S)
        ziele = re.findall(r'href="([^"#]+)', m.group(0) if m else roh)
        im_nav = [t.rsplit("/", 1)[-1] for t in ziele if KAPITEL.search(t)]
        im_buch = [s.rsplit("/", 1)[-1] for s in spine if KAPITEL.search(s)]
        if len(im_nav) != len(im_buch):
            klagen.append(f"Verzeichnis listet {len(im_nav)} Kapitel, "
                          f"das Buch hat {len(im_buch)}")
        elif im_nav != im_buch:
            klagen.append("Verzeichnis und Buch haben andere Reihenfolgen")
    return klagen


def selbsttest() -> None:
    """Ein kaputtes Buch muss durchfallen, ein sauberes nicht.

    Ohne diesen Test heisst „keine Beanstandungen" nur, dass das Skript
    gelaufen ist.
    """
    import tempfile
    ordner = Path(tempfile.mkdtemp())

    def bauen(ziel: Path, kaputt: bool) -> None:
        lang = " wort" * 300
        with zipfile.ZipFile(ziel, "w") as z:
            z.writestr("mimetype", "application/epub+zip")
            z.writestr("META-INF/container.xml", "<container/>")
            autor = "[AUTORENNAME]" if kaputt else "Eine Autorin"
            z.writestr("EPUB/buch.opf", f"""<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0">
 <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>Ein Titel</dc:title><dc:creator>{autor}</dc:creator>
  <dc:language>de</dc:language><dc:identifier>x1</dc:identifier>
  <meta name="cover" content="cv"/>
 </metadata>
 <manifest>
  <item id="cv" href="cover.jpg" media-type="image/jpeg"/>
  <item id="st" href="style.css" media-type="text/css"/>
  <item id="k1" href="kap01.xhtml" media-type="application/xhtml+xml"/>
  <item id="k2" href="kap02.xhtml" media-type="application/xhtml+xml"/>
  <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml"/>
  <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
 </manifest>
 <spine><itemref idref="k1"/><itemref idref="k2"/></spine>
</package>""")
            z.writestr("EPUB/cover.jpg", b"\xff\xd8\xff")
            # Negativfall fuer die Zeichenpruefung: Das saubere
            # Stylesheet enthaelt Asterism, Gedankenstrich und deutsche
            # Anfuehrungszeichen. Schlaegt der Pruefer hier an, ist er
            # zu grob. Der Kaputtfall traegt genau den Fehler vom
            # 19.08.2026: aus "\2042" wurde U+0084 plus die Ziffer 2.
            z.writestr("EPUB/style.css",
                       'hr:after { content: "\x842"; }\n' if kaputt else
                       'hr:after { content: "⁂"; }\n'
                       '/* Gedankenstrich — und „Anfuehrung" */\n')
            z.writestr("EPUB/kap01.xhtml",
                       f"<html><body><h1>Eins</h1><p>{lang}</p></body></html>")
            if kaputt:
                z.writestr("EPUB/kap02.xhtml",
                           '<html><body><h1>Eins</h1><h1>Noch eins</h1>'
                           '<p>kurz</p><a href="gibtsnicht.xhtml">x</a>'
                           "</body></html>")
            else:
                z.writestr("EPUB/kap02.xhtml",
                           f"<html><body><h1>Zwei</h1><p>anders{lang}"
                           f"</p></body></html>")
            z.writestr("EPUB/nav.xhtml",
                       '<html><body><nav epub:type="toc">'
                       '<a href="kap01.xhtml">1</a>'
                       '<a href="kap02.xhtml">2</a></nav>'
                       '<nav epub:type="landmarks">'
                       '<a href="kap01.xhtml">Anfang</a></nav></body></html>')
            z.writestr("EPUB/toc.ncx", "<ncx/>")

    gut, schlecht = ordner / "gut.epub", ordner / "schlecht.epub"
    bauen(gut, False)
    bauen(schlecht, True)
    k_gut, k_schlecht = pruefe(gut), pruefe(schlecht)
    print(f"  Sauberes Buch: {len(k_gut)} Beanstandung(en) — erwartet 0")
    for k in k_gut:
        print(f"      {k}")
    print(f"  Kaputtes Buch: {len(k_schlecht)} Beanstandung(en) — "
          f"erwartet mindestens 4")
    if k_gut:
        sys.exit("Selbsttest: ein sauberes Buch faellt durch.")
    if len(k_schlecht) < 4:
        sys.exit("Selbsttest: ein kaputtes Buch kommt durch.")
    print("  Selbsttest bestanden (Landmarks gelten nicht als Dopplung).")


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("datei", nargs="?")
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args()

    print("Selbsttest:")
    selbsttest()
    if a.selbsttest:
        return
    if not a.datei:
        sys.exit("Keine Datei angegeben.")

    pfad = Path(a.datei)
    print(f"\nGeprueft: {pfad} ({pfad.stat().st_size/1024:.0f} kB)\n")
    klagen = pruefe(pfad)
    if not klagen:
        print("Keine Beanstandungen.")
        return
    print(f"{len(klagen)} Beanstandung(en):")
    for k in klagen:
        print(f"  - {k}")
    sys.exit(1)


if __name__ == "__main__":
    main()
