#!/usr/bin/env python3
"""
cover.py — misst, wie die Cover in einer Buchnische tatsächlich aussehen.

Wozu: Vor einem eigenen Cover steht immer derselbe Rat — „schau dir an,
was in deiner Nische funktioniert". Das ist eine Anweisung ohne
Messgerät. Dieses Skript baut es: Es holt die Cover der Spitzentitel aus
den gemessenen Nischen, legt sie als Kontaktbogen nebeneinander und misst
je Cover das, was ohne Interpretation messbar ist.

Was gemessen wird (und nur das):
  * Seitenverhältnis und Auflösung
  * Mittlere Helligkeit, Kontrast (Streuung), Sättigung
  * Die fünf häufigsten Farben mit Flächenanteil
  * In welchem waagerechten Fünftel die meiste Kantenenergie sitzt
    — das ist der Ort des Titelblocks, siehe Kalibrierung unten

Was NICHT gemessen wird: ob ein Mensch abgebildet ist, welche Schriftart
verwendet wird, ob die Stimmung „warm" ist. Dafür gibt es kein
verlässliches Messgerät in zwanzig Zeilen, und ein unzuverlässiges wäre
schlimmer als keins. Diese Fragen beantwortet der Kontaktbogen, den ein
Mensch (oder ein Modell mit Augen) ansieht.

**Kalibrierung.** Die Kantenenergie je Band ist der einzige Wert hier,
der etwas behauptet, das nicht direkt in der Datei steht. Deshalb prüft
`--selbsttest` ihn gegen einen bekannten Positiv- und einen bekannten
Negativfall, bevor er zum ersten Mal auf echte Daten losgelassen wird:
ein Bild mit einem Textblock oben (muss Band 1 finden) und eine glatte
Fläche ohne Text (darf kein Band deutlich herausheben). Ohne bestandenen
Selbsttest bricht der Lauf ab.

**Zur Nutzung.** Amazons Nutzungsbedingungen untersagen automatisierten
Zugriff. Wie `kdp_nischen.py` ist dieses Skript bewusst kleinvolumig und
nur lesend, mit Pausen. Die Cover werden angesehen und vermessen, nicht
weiterverwendet — sie sind urheberrechtlich geschützt und gehören nicht
in ein Produkt.

Aufruf:
    python3 scripts/cover.py --selbsttest
    python3 scripts/cover.py --begriffe "geheimes baby liebesroman" \\
        "milliardär liebesroman" --markt de --anzahl 12
"""

from __future__ import annotations

import argparse
import colorsys
import io
import json
import random
import re
import sys
import time
from datetime import date
from pathlib import Path
from statistics import median

from PIL import Image, ImageDraw, ImageFilter, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kdp_nischen import MARKTPLAETZE, consent_wegklicken  # noqa: E402

BAENDER = 5
MARKER = ('<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf '
          'erhalten -->')


# ---------------------------------------------------------------- Messung

def kantenband(bild: Image.Image) -> list[float]:
    """Kantenenergie je waagerechtem Fünftel, normiert auf Summe 1.

    Schrift erzeugt auf kleiner Skala sehr viele Kanten. Ein Foto oder
    ein Farbverlauf erzeugt wenige. Wo auf einem Cover der Titel steht,
    steigt dieser Wert deshalb deutlich an.
    """
    g = bild.convert("L").resize((300, 450))
    kanten = g.filter(ImageFilter.FIND_EDGES)
    # FIND_EDGES lässt am Bildrand einen Artefaktstreifen stehen: gemessen
    # 42 bzw. 193 in der ersten und letzten Zeile, 117 in den Randspalten,
    # gegen 0,3 bis 1,3 im Inneren. Ohne diesen Schnitt meldete der
    # Selbsttest auf einer glatten Fläche eine Textzone im untersten Band.
    kanten = kanten.crop((4, 4, kanten.width - 4, kanten.height - 4))
    h = kanten.height // BAENDER
    werte = []
    for i in range(BAENDER):
        streifen = kanten.crop((0, i * h, kanten.width, (i + 1) * h))
        werte.append(ImageStat.Stat(streifen).mean[0])
    summe = sum(werte) or 1.0
    return [w / summe for w in werte]


def hauptfarben(bild: Image.Image, anzahl: int = 5) -> list[dict]:
    """Die häufigsten Farben mit Flächenanteil, über eine adaptive
    Palette. Kein k-means, keine zusätzliche Abhängigkeit."""
    klein = bild.convert("RGB").resize((160, 240))
    p = klein.convert("P", palette=Image.Palette.ADAPTIVE, colors=anzahl)
    palette = p.getpalette() or []
    gesamt = klein.width * klein.height
    raus = []
    for zahl, index in sorted(p.getcolors() or [], reverse=True)[:anzahl]:
        r, g, b = palette[index * 3:index * 3 + 3]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        raus.append({
            "hex": f"#{r:02x}{g:02x}{b:02x}",
            "anteil": round(zahl / gesamt, 3),
            "ton": round(h * 360),
            "saettigung": round(s, 2),
            "helligkeit": round(v, 2),
        })
    return raus


def messen(bild: Image.Image) -> dict:
    rgb = bild.convert("RGB")
    grau = rgb.convert("L")
    st = ImageStat.Stat(grau)
    hsv = rgb.convert("HSV")
    baender = kantenband(rgb)
    return {
        "breite": rgb.width,
        "hoehe": rgb.height,
        "verhaeltnis": round(rgb.height / rgb.width, 3) if rgb.width else None,
        "helligkeit": round(st.mean[0], 1),
        "kontrast": round(st.stddev[0], 1),
        "saettigung": round(ImageStat.Stat(hsv).mean[1], 1),
        "kantenbaender": [round(b, 3) for b in baender],
        "textzone": baender.index(max(baender)) + 1,
        "farben": hauptfarben(rgb),
    }


# ----------------------------------------------------------- Kalibrierung

def _probe_text_oben() -> Image.Image:
    """Positivfall: großer Textblock im oberen Fünftel, sonst glatt."""
    b = Image.new("RGB", (600, 900), (40, 60, 90))
    d = ImageDraw.Draw(b)
    for y in range(30, 150, 22):
        for x in range(40, 560, 14):
            d.rectangle([x, y, x + 9, y + 15], fill=(240, 235, 225))
    return b


def _probe_ohne_text() -> Image.Image:
    """Negativfall: reiner senkrechter Verlauf, nirgends Schrift."""
    b = Image.new("RGB", (600, 900))
    d = ImageDraw.Draw(b)
    for y in range(900):
        t = y / 899
        d.line([(0, y), (600, y)],
               fill=(int(30 + 180 * t), int(40 + 150 * t), int(80 + 90 * t)))
    return b


def _probe_text_unten_auf_rauschen() -> Image.Image:
    """Der harte Fall: Schrift im vierten Fünftel über einem unruhigen
    Hintergrund. Ein Cover ist nie eine glatte Fläche — wenn die Messung
    nur auf ruhigem Grund funktioniert, ist sie für echte Cover nutzlos."""
    zufall = random.Random(7)
    b = Image.new("RGB", (600, 900))
    px = b.load()
    for y in range(900):
        for x in range(0, 600, 3):
            t = zufall.randint(60, 200)
            for dx in range(3):
                px[x + dx, y] = (t, int(t * 0.7), int(t * 0.5))
    d = ImageDraw.Draw(b)
    for y in range(580, 700, 22):
        for x in range(40, 560, 14):
            d.rectangle([x, y, x + 9, y + 15], fill=(255, 255, 255))
    return b


def selbsttest() -> bool:
    """Prüft die Kantenband-Messung gegen bekannten Positiv- und
    Negativfall. Ohne diesen Test ist 'Textzone 3' eine Behauptung."""
    ok = True

    pos = kantenband(_probe_text_oben())
    zone = pos.index(max(pos)) + 1
    print(f"  Positivfall (Text oben):  Bänder {[round(x, 3) for x in pos]} "
          f"-> Zone {zone}")
    if zone != 1:
        print("  FEHLGESCHLAGEN: Textblock oben wurde nicht in Band 1 "
              "gefunden.")
        ok = False
    if max(pos) < 0.35:
        print(f"  FEHLGESCHLAGEN: Ausschlag zu schwach ({max(pos):.3f} < "
              "0.35) — das Gerät erkennt Schrift nicht deutlich genug.")
        ok = False

    neg = kantenband(_probe_ohne_text())
    print(f"  Negativfall (kein Text):  Bänder {[round(x, 3) for x in neg]} "
          f"-> Spanne {max(neg) - min(neg):.3f}")
    if max(neg) - min(neg) > 0.08:
        print("  FEHLGESCHLAGEN: glatte Fläche erzeugt einen Ausschlag. "
              "Der Wert misst dann nicht Schrift.")
        ok = False

    hart = kantenband(_probe_text_unten_auf_rauschen())
    zone_h = hart.index(max(hart)) + 1
    print(f"  Harter Fall (Text Band 4 auf Rauschen): "
          f"Bänder {[round(x, 3) for x in hart]} -> Zone {zone_h}")
    if zone_h != 4:
        print("  FEHLGESCHLAGEN: Schrift über unruhigem Grund wird nicht "
              "gefunden. Auf echten Covern ist der Grund immer unruhig.")
        ok = False

    print("  Selbsttest bestanden." if ok else "  Selbsttest FEHLGESCHLAGEN.")
    return ok


# -------------------------------------------------------------- Beschaffung

def gross(url: str) -> str:
    """Amazon-Thumbnails tragen die Größe im Dateinamen:
    ..._AC_UY218_SEARCH_.jpg -> ..._SL500_.jpg"""
    return re.sub(r"\._[A-Za-z0-9_,]+_\.", "._SL500_.", url)


def treffer_mit_covern(seite, host: str, begriff: str, anzahl: int) -> list[dict]:
    from urllib.parse import quote_plus
    url = f"https://{host}/s?k={quote_plus(begriff)}&i=digital-text"
    seite.goto(url, wait_until="domcontentloaded", timeout=45000)
    seite.wait_for_timeout(2000)
    consent_wegklicken(seite)
    seite.wait_for_timeout(1200)

    roh = seite.evaluate("""() => {
      const raus = [];
      for (const k of document.querySelectorAll('[data-asin]')) {
        const asin = k.getAttribute('data-asin');
        if (!asin) continue;
        const bild = k.querySelector('img.s-image');
        if (!bild || !bild.src) continue;
        const t = k.querySelector('h2 span, h2 a span');
        const gesponsert =
          !!k.querySelector('[aria-label*="Gesponsert"], [aria-label*="Sponsored"], '
            + '[data-component-type="sp-sponsored-result"], .puis-sponsored-label-text, '
            + '.s-sponsored-label-text')
          || /\\bGesponsert\\b|\\bSponsored\\b/.test(k.textContent);
        raus.push({asin, titel: t ? t.textContent.trim() : '',
                   bild: bild.src, gesponsert});
      }
      return raus;
    }""")

    organisch = [t for t in roh if not t["gesponsert"]]
    return organisch[:anzahl]


def holen(seite, url: str) -> bytes | None:
    """Über den Browserkontext laden, nicht über requests — dieselbe
    Sitzung, dieselben Kopfzeilen, keine zweite Spur."""
    try:
        antwort = seite.context.request.get(url, timeout=30000)
        return antwort.body() if antwort.ok else None
    except Exception:
        return None


def kontaktbogen(bilder: list[tuple[str, Image.Image]], spalten: int = 6,
                 zellbreite: int = 220) -> Image.Image:
    """Alle Cover einer Nische nebeneinander, nummeriert. Das ist der
    Teil, den ein Mensch ansieht — die Zahlen oben ersetzen das nicht."""
    zellhoehe = int(zellbreite * 1.6)
    beschriftung = 22
    zeilen = max(1, (len(bilder) + spalten - 1) // spalten)
    blatt = Image.new("RGB",
                      (spalten * zellbreite,
                       zeilen * (zellhoehe + beschriftung)),
                      (255, 255, 255))
    d = ImageDraw.Draw(blatt)
    for i, (name, bild) in enumerate(bilder):
        sp, ze = i % spalten, i // spalten
        x, y = sp * zellbreite, ze * (zellhoehe + beschriftung)
        k = bild.convert("RGB").copy()
        k.thumbnail((zellbreite - 8, zellhoehe - 8))
        blatt.paste(k, (x + (zellbreite - k.width) // 2, y + 4))
        d.text((x + 6, y + zellhoehe + 4), name[:34], fill=(20, 20, 20))
    return blatt


# ------------------------------------------------------------------ Bericht

def bericht(nischen: list[dict]) -> str:
    z = ["# Cover in den gemessenen Nischen", "",
         f"Stand: {date.today().isoformat()}", "",
         "Gemessen an den Cover-Bildern der organischen Spitzentitel auf "
         "den öffentlichen Amazon-Trefferlisten. Gemessen wird nur, was "
         "ohne Deutung in der Bilddatei steht: Format, Helligkeit, "
         "Kontrast, Sättigung, Farbanteile und die Lage der "
         "Kantenenergie. **Ob ein Mensch abgebildet ist, welche Schrift "
         "verwendet wird und welche Stimmung entsteht, wird hier nicht "
         "gemessen** — dafür liegen die Kontaktbögen in `cover/`.", "",
         "Die Spalte **Textzone** sagt, in welchem waagerechten Fünftel "
         "die meiste Kantenenergie sitzt; dort steht in aller Regel der "
         "Titel. Die Messung ist gegen einen Positiv- und einen "
         "Negativfall kalibriert (`--selbsttest`).", "",
         "| Nische | Cover | Verhältnis | Helligkeit | Kontrast | "
         "Sättigung | Textzone (Median) | Kontaktbogen |",
         "|---|---:|---:|---:|---:|---:|---:|---|"]
    for n in nischen:
        if n.get("fehler"):
            z.append(f"| {n['begriff']} | FEHLER | – | – | – | – | – | – |")
            continue
        c = n["cover"]
        if not c:
            z.append(f"| {n['begriff']} | 0 | – | – | – | – | – | – |")
            continue

        def m(feld):
            w = [x[feld] for x in c if x.get(feld) is not None]
            return round(median(w), 1) if w else "–"

        z.append(
            f"| {n['begriff']} | {len(c)} | {m('verhaeltnis')} "
            f"| {m('helligkeit')} | {m('kontrast')} | {m('saettigung')} "
            f"| {m('textzone')} | `{n['kontaktbogen']}` |")

    z += ["", "## Farbwelt je Nische", "",
          "Die häufigsten Farben aller gemessenen Cover einer Nische, nach "
          "Gesamtfläche. Das ist der Farbraum, in dem ein neues Cover "
          "auffallen oder sich einfügen muss.", ""]
    for n in nischen:
        if n.get("fehler") or not n.get("cover"):
            continue
        eimer: dict[str, float] = {}
        for c in n["cover"]:
            for f in c["farben"]:
                # Auf 32er-Raster runden, sonst zählt jede Nuance einzeln.
                r, g, b = (int(f["hex"][i:i + 2], 16) for i in (1, 3, 5))
                schluessel = (f"#{r // 32 * 32:02x}{g // 32 * 32:02x}"
                              f"{b // 32 * 32:02x}")
                eimer[schluessel] = eimer.get(schluessel, 0) + f["anteil"]
        gesamt = sum(eimer.values()) or 1
        oben = sorted(eimer.items(), key=lambda x: -x[1])[:8]
        z.append(f"**{n['begriff']}** — "
                 + ", ".join(f"`{k}` {v / gesamt:.0%}" for k, v in oben))
        z.append("")

    z += ["## Grenzen dieser Messung", "",
          "- **Die Stichprobe ist die erste Trefferseite**, nicht die "
          "Bestsellerliste. Wer oben steht, steht dort auch wegen "
          "Suchbegriff-Treffern.",
          "- **Cover werden als Miniatur ausgeliefert** (500 px). Feine "
          "Typografie ist darin nicht beurteilbar — auf dem Handy sieht "
          "die Kundin allerdings auch nur eine Miniatur.",
          "- **Die Kantenmessung findet Schrift, nicht Titel.** Ein "
          "detailreiches Foto im selben Band verschiebt den Wert.",
          "- Die Cover sind urheberrechtlich geschützt. Sie liegen hier "
          "zur Messung, nicht zur Verwendung.", "",
          MARKER, ""]
    return "\n".join(z)


def bericht_schreiben(text: str, pfad: Path) -> None:
    """Handnotizen unterhalb des Markers überleben jeden Lauf."""
    alt = pfad.read_text(encoding="utf-8") if pfad.exists() else ""
    schwanz = ""
    if MARKER in alt:
        schwanz = alt.split(MARKER, 1)[1]
    pfad.write_text(text + schwanz, encoding="utf-8")


# --------------------------------------------------------------------- main

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--begriffe", nargs="*", default=[])
    p.add_argument("--markt", choices=sorted(MARKTPLAETZE), default="de")
    p.add_argument("--anzahl", type=int, default=12,
                   help="Cover je Nische")
    p.add_argument("--ordner", default="cover")
    p.add_argument("--bericht", default="COVER.md")
    p.add_argument("--pause", type=float, default=2.0)
    p.add_argument("--selbsttest", action="store_true",
                   help="nur die Kalibrierung laufen lassen")
    args = p.parse_args()

    print("Kalibrierung der Kantenband-Messung:")
    if not selbsttest():
        sys.exit(2)
    if args.selbsttest:
        return
    if not args.begriffe:
        print("Keine Begriffe angegeben.")
        return

    markt = MARKTPLAETZE[args.markt]
    ziel = Path(args.ordner)
    ziel.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    nischen = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--no-sandbox"])
        kontext = browser.new_context(
            locale=markt["sprache"],
            viewport={"width": 1400, "height": 1000},
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0 Safari/537.36"))
        seite = kontext.new_page()

        for begriff in args.begriffe:
            print(f"\n=== {begriff} ===", flush=True)
            eintrag: dict = {"begriff": begriff, "markt": markt["host"],
                             "cover": []}
            try:
                treffer = treffer_mit_covern(seite, markt["host"], begriff,
                                             args.anzahl)
            except Exception as e:
                eintrag["fehler"] = f"Suche fehlgeschlagen: {str(e)[:160]}"
                nischen.append(eintrag)
                continue

            if not treffer:
                # Leeres Ergebnis ist kein Befund.
                eintrag["fehler"] = ("Keine Treffer gelesen. NICHT als "
                                     "'keine Cover' deuten.")
                try:
                    eintrag["seitentitel"] = seite.title()
                except Exception:
                    pass
                nischen.append(eintrag)
                continue

            kurz = re.sub(r"[^a-z0-9]+", "-", begriff.lower()).strip("-")
            unterordner = ziel / kurz
            unterordner.mkdir(parents=True, exist_ok=True)
            bilder = []

            for i, t in enumerate(treffer, 1):
                daten = holen(seite, gross(t["bild"]))
                if not daten:
                    print(f"  {i:2d} {t['asin']}  Bild nicht ladbar")
                    continue
                try:
                    bild = Image.open(io.BytesIO(daten))
                    bild.load()
                except Exception:
                    print(f"  {i:2d} {t['asin']}  Bild nicht lesbar")
                    continue
                datei = unterordner / f"{i:02d}-{t['asin']}.jpg"
                bild.convert("RGB").save(datei, quality=88)
                werte = messen(bild)
                werte.update(asin=t["asin"], titel=t["titel"],
                             datei=str(datei))
                eintrag["cover"].append(werte)
                bilder.append((f"{i:02d} {t['titel'][:30]}", bild))
                print(f"  {i:2d} {t['asin']}  {werte['breite']}x"
                      f"{werte['hoehe']}  hell {werte['helligkeit']}  "
                      f"Textzone {werte['textzone']}", flush=True)
                time.sleep(args.pause * random.uniform(0.5, 1.2))

            if bilder:
                bogen = ziel / f"kontaktbogen-{kurz}.png"
                kontaktbogen(bilder).save(bogen)
                eintrag["kontaktbogen"] = str(bogen)
                print(f"  Kontaktbogen: {bogen}")
            nischen.append(eintrag)
            time.sleep(args.pause * 2)

        browser.close()

    Path("daten").mkdir(exist_ok=True)
    Path("daten/cover.json").write_text(
        json.dumps(nischen, ensure_ascii=False, indent=2), encoding="utf-8")
    bericht_schreiben(bericht(nischen), Path(args.bericht))
    print(f"\nGeschrieben: {args.bericht}, daten/cover.json, {args.ordner}/")


if __name__ == "__main__":
    main()
