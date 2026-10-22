#!/usr/bin/env python3
"""
coverbau.py — setzt die Typografie auf ein Coverbild und misst das
Ergebnis gegen die Konkurrenz.

Wozu: `cover.py` hat gemessen, wie die 36 Spitzentitel der Nische
aussehen (`COVER.md`). Dieses Skript setzt genau das um — und prüft
danach, ob es getroffen hat. Ein Cover, das nur „gut aussieht", ist eine
Behauptung.

Was es macht:
  1. Bild auf 1600 × 2560 bringen (KDP-Norm, Verhältnis 1,6).
  2. Einen Verlauf von unten einblenden, **so tief wie nötig** — die
     Deckkraft wird hochgedreht, bis der Titelkontrast das Ziel erreicht.
     Nicht geschätzt: gemessen, mit demselben WCAG-Rechenweg wie
     `kontrast.py`.
  3. Reihenzeile oben, Titel im unteren Mitteldrittel, Genre-Zeile und
     Autorname darunter — die Anordnung aus der Messung.
  4. Drei Dateien ausgeben: fertiges Cover, transparente Schrift-Ebene
     (für ein anderes Bild) und die Miniaturprobe.
  5. Das Ergebnis gegen die Nischen-Mediane halten.

**Die Miniaturprobe ist der eigentliche Test.** Auf dem Handy ist ein
Cover in der Trefferliste rund 160 Pixel hoch. Was dort nicht lesbar ist,
existiert nicht.

Aufruf:
    python3 scripts/coverbau.py --bild cover/roh/mann.png \\
        --autor "Vorname Nachname"
    python3 scripts/coverbau.py --platzhalter      # ohne eigenes Bild
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kontrast import kontrast  # noqa: E402

BREITE, HOEHE = 1600, 2560
SCHRIFTEN = Path(__file__).resolve().parent.parent / "schriften"

GOLD = (200, 160, 106)
WEISS = (255, 255, 255)

# Zielkontrast. AA verlangt 4,5 für normalen Text. Hier steht 7,0, weil
# das Cover als 160-Pixel-Miniatur gelesen wird und dabei jedes Detail
# verschwimmt -- der Puffer ist Absicht, nicht Übererfüllung.
ZIEL_KONTRAST = 7.0

# Nischen-Mediane aus COVER.md, Lauf vom 15.08.2026, 36 Cover.
VERGLEICH = {
    "helligkeit": (55.8, 64.5),
    "saettigung": (94.5, 119.7),
    "verhaeltnis": (1.45, 1.61),
}


def schrift(name: str, groesse: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(SCHRIFTEN / name), groesse)


def breite_gesperrt(zeichnung, text: str, font, sperrung: int) -> int:
    if not text:
        return 0
    summe = sum(zeichnung.textlength(z, font=font) for z in text)
    return int(summe + sperrung * (len(text) - 1))


def gesperrt(zeichnung, mitte_x: int, y: int, text: str, font,
             farbe, sperrung: int) -> None:
    """PIL kann keine Laufweite. Also Zeichen für Zeichen. Ohne Sperrung
    sehen Versalien wie zusammengeschoben aus — auf allen 36 gemessenen
    Covern sind die kleinen Zeilen weit gesperrt."""
    x = mitte_x - breite_gesperrt(zeichnung, text, font, sperrung) / 2
    for z in text:
        zeichnung.text((x, y), z, font=font, fill=farbe)
        x += zeichnung.textlength(z, font=font) + sperrung


def passend(zeichnung, text: str, datei: str, zielbreite: int,
            sperrung: int = 0) -> ImageFont.FreeTypeFont:
    """Größte Schriftgröße, die noch in die Zielbreite passt."""
    klein, gross = 10, 400
    while klein < gross:
        mitte = (klein + gross + 1) // 2
        f = schrift(datei, mitte)
        if breite_gesperrt(zeichnung, text, f, sperrung) <= zielbreite:
            klein = mitte
        else:
            gross = mitte - 1
    return schrift(datei, klein)


def einpassen(bild: Image.Image, zoom: float = 1.0) -> Image.Image:
    """Auf 1600x2560 bringen, oben verankert — das Gesicht sitzt oben,
    beschnitten wird unten.

    `zoom` > 1 schneidet enger. Das ist kein Schoenheitsregler: Wenn ein
    heller Bildteil genau im Titelband liegt (bei Band 2 ein offenes
    weisses Hemd), rutscht er durch engeren Schnitt darunter, und der
    Titel steht wieder auf dunklem Grund. Ein Verlauf kann das nicht --
    er muesste die Stelle um 65 Prozent abdunkeln und wuerde damit die
    halbe untere Bildhaelfte flachdruecken. Nachgerechnet am 01.09.2026.
    """
    bild = bild.convert("RGB")
    faktor = max(BREITE / bild.width, HOEHE / bild.height) * zoom
    neu = bild.resize((max(BREITE, int(bild.width * faktor)),
                       max(HOEHE, int(bild.height * faktor))),
                      Image.LANCZOS)
    links = (neu.width - BREITE) // 2
    return neu.crop((links, 0, links + BREITE, HOEHE))


def verlauf(deckkraft: float, ab: float = 0.42) -> Image.Image:
    """Schwarzer Verlauf von unten. `ab` ist die Höhe, ab der er
    einsetzt."""
    ebene = Image.new("L", (1, HOEHE), 0)
    p = ebene.load()
    start = int(HOEHE * ab)
    for y in range(start, HOEHE):
        t = (y - start) / max(1, HOEHE - start)
        p[0, y] = int(255 * deckkraft * (t ** 1.4))
    return ebene.resize((BREITE, HOEHE))


def mittlere_farbe(bild: Image.Image, kasten) -> tuple[int, int, int]:
    aus = bild.crop(kasten).resize((1, 1), Image.BOX)
    return aus.getpixel((0, 0))


# Kachelgroesse fuer die Suche nach der hellsten Stelle. 80x40 ist grob
# eine Buchstabenflaeche der Versalzeile -- kleiner misst Rauschen,
# groesser verwischt wieder zum Mittelwert.
KACHEL = (80, 40)


def hellste_farbe(bild: Image.Image, kasten) -> tuple[int, int, int]:
    """Die hellste Kachel im Titelkasten, nicht sein Mittelwert.

    Warum: Am 01.09.2026 lief der Titel von Band 2 ueber ein weisses
    Hemd. Der Mittelwert unter dem Titel war (67,64,65) und meldete
    10,25:1 -- bestanden. An der Stelle, wo das Hemd sass, standen aber
    (254,254,254), also 1,01:1 gegen weisse Schrift: weiss auf weiss,
    unlesbar. Der Verlauf blieb deshalb bei Deckkraft 0,00 stehen.

    Ein Mittelwert kann einen hellen Fleck nicht sehen, und genau der
    macht Schrift unlesbar. Gemessen wird deshalb der schlechteste
    Fall, nicht der durchschnittliche.
    """
    aus = bild.crop(kasten).convert("RGB")
    kb, kh = KACHEL
    # Maximumsuche: Startwert muss unter jeder echten Helligkeit liegen.
    # Stand hier zuerst auf 1e9 -- dann greift die Bedingung nie und die
    # Funktion gab immer (0,0,0) zurueck, also den bestmoeglichen Wert.
    # Ein Messgeraet, das im Fehlerfall "alles in Ordnung" sagt, ist das
    # gefaehrlichste von allen. Gefunden hat es der Kalibrierlauf.
    schlimmst, hellste = -1.0, (0, 0, 0)
    for x in range(0, max(1, aus.width - kb + 1), kb):
        for y in range(0, max(1, aus.height - kh + 1), kh):
            f = aus.crop((x, y, x + kb, y + kh)).resize((1, 1),
                                                        Image.BOX)
            f = f.getpixel((0, 0))
            helligkeit = 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]
            if helligkeit < schlimmst:
                continue
            schlimmst, hellste = helligkeit, f
    return hellste


def unter_der_schrift(hintergrund: Image.Image, ebene: Image.Image,
                      schwelle: float = 4.5) -> tuple[float, float]:
    """Kontrast dort, wo die Buchstaben wirklich stehen.

    Der Mittelwert unter dem Titelkasten sagt nichts darueber, ob ein
    einzelner Buchstabe auf einem hellen Fleck sitzt; die hellste Kachel
    im ganzen Band sagt zu viel, weil die Schrift das Band nur zu einem
    Bruchteil bedeckt. Gemessen wird deshalb die Deckungsflaeche der
    Glyphen selbst, leicht aufgeweitet, damit auch der Rand zaehlt.

    Rueckgabe: (Anteil der Schriftflaeche unter `schwelle`, schlechtester
    Einzelwert). Das ist eine Warnung, keine Abnahme -- der bekannte
    Positivfall Band 1 liegt bei rund 15 Prozent und funktioniert.
    """
    a = ebene.getchannel("A").filter(ImageFilter.MaxFilter(9))
    hg = hintergrund.convert("RGB")
    pa, ph = a.load(), hg.load()
    schlecht = gesamt = 0
    schlimmst = 99.0
    for y in range(0, a.height, 3):
        for x in range(0, a.width, 3):
            if pa[x, y] < 128:
                continue
            gesamt += 1
            k = kontrast(WEISS, ph[x, y])
            schlimmst = min(schlimmst, k)
            if k < schwelle:
                schlecht += 1
    return schlecht / max(1, gesamt), schlimmst


def platzhalterbild() -> Image.Image:
    """Ein neutraler Stellvertreter, damit man die Schrift beurteilen
    kann, wenn noch kein Bild da ist. Das ist ausdrücklich KEIN
    Coverbild — es steht auch so drauf."""
    b = Image.new("RGB", (BREITE, HOEHE), (10, 10, 12))
    d = ImageDraw.Draw(b)
    for y in range(HOEHE):
        t = y / HOEHE
        warm = int(90 * max(0.0, 1 - abs(t - 0.22) * 3.2))
        kalt = int(46 * max(0.0, 1 - abs(t - 0.30) * 2.6))
        d.line([(0, y), (BREITE, y)],
               fill=(14 + warm, 12 + int(warm * 0.55) + int(kalt * 0.35),
                     16 + int(warm * 0.3) + kalt))
    f = schrift("Cormorant-SemiBold.ttf", 46)
    gesperrt(d, BREITE // 2, 300, "PLATZHALTER — KEIN COVERBILD", f,
             (150, 140, 130), 6)
    return b


def bauen(bild: Image.Image, texte: dict, zoom: float = 1.0) -> tuple[Image.Image, Image.Image, dict]:
    grund = einpassen(bild, zoom)
    mess = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    # --- Schriftgrößen, alle von der Bildbreite abgeleitet -----------
    rand = int(BREITE * 0.08)
    innen = BREITE - 2 * rand

    f_caps = passend(mess, texte["titel_caps"], "Cinzel-Black.ttf",
                     int(innen * 0.98))
    f_script = schrift("GreatVibes.ttf", int(f_caps.size * 0.78))
    f_reihe = passend(mess, texte["reihe"], "Cinzel-SemiBold.ttf",
                      int(innen * 0.78), sperrung=9)
    f_genre = passend(mess, texte["genre"].upper(),
                      "Cormorant-SemiBold.ttf", int(innen * 0.86),
                      sperrung=6)
    f_autor = passend(mess, texte["autor"].upper(), "Cinzel-SemiBold.ttf",
                      int(innen * 0.62), sperrung=10)

    # --- Senkrechte Anordnung ---------------------------------------
    # Titel ins untere Mitteldrittel: gemessene Textzone ist Band 4
    # von 5, also 60 bis 80 Prozent der Höhe.
    y_script = int(HOEHE * 0.615)
    y_caps = y_script + int(f_script.size * 0.92)
    y_genre = y_caps + int(f_caps.size * 1.30)
    y_autor = int(HOEHE * 0.915)
    y_reihe = int(HOEHE * 0.045)

    titelkasten = (rand, y_script, BREITE - rand,
                   y_genre + int(f_genre.size * 1.6))

    # --- Verlauf so tief wie nötig, nicht wie geplant ----------------
    diagnose = []
    gewaehlt, endkontrast, hintergrund = 0.0, 0.0, (0, 0, 0)
    for schritt in range(0, 21):
        d = schritt * 0.05
        probe = Image.composite(Image.new("RGB", (BREITE, HOEHE), (0, 0, 0)),
                                grund, verlauf(d))
        # Der Verlauf laeuft weiterhin nach dem Mittelwert. Die
        # Kachelsuche als Steuergroesse war falsch: Sie verlangt, dass
        # das ganze Titelband dunkel ist, aber die Schrift bedeckt es
        # nur zu einem Bruchteil. Damit ist auch Band 1 durchgefallen --
        # ein veroeffentlichtes Cover, das nachweislich funktioniert.
        # Ein Selektor, der den bekannten Positivfall verwirft, ist kein
        # Messgeraet. Die strenge Messung steht jetzt als Warnung unter
        # dem Ergebnis, siehe unter_der_schrift().
        hg = mittlere_farbe(probe, titelkasten)
        k = kontrast(WEISS, hg)
        diagnose.append({"deckkraft": round(d, 2), "kontrast": round(k, 2)})
        gewaehlt, endkontrast, hintergrund = d, k, hg
        if k >= ZIEL_KONTRAST:
            break

    leinwand = Image.composite(Image.new("RGB", (BREITE, HOEHE), (0, 0, 0)),
                               grund, verlauf(gewaehlt))
    # Oben ein kurzer Verlauf, damit die Reihenzeile immer trägt.
    oben = Image.new("L", (BREITE, HOEHE), 0)
    do = ImageDraw.Draw(oben)
    for y in range(int(HOEHE * 0.16)):
        do.line([(0, y), (BREITE, y)],
                fill=int(150 * (1 - y / (HOEHE * 0.16))))
    leinwand = Image.composite(Image.new("RGB", (BREITE, HOEHE), (0, 0, 0)),
                               leinwand, oben)

    # --- Schrift auf eine eigene, durchsichtige Ebene ----------------
    ebene = Image.new("RGBA", (BREITE, HOEHE), (0, 0, 0, 0))
    z = ImageDraw.Draw(ebene)
    m = BREITE // 2

    gesperrt(z, m, y_reihe, texte["reihe"], f_reihe, GOLD + (255,), 9)
    z.text((m, y_script), texte["titel_script"], font=f_script,
           fill=WEISS + (255,), anchor="ma")
    gesperrt(z, m, y_caps, texte["titel_caps"], f_caps, WEISS + (255,), 0)
    gesperrt(z, m, y_genre, texte["genre"].upper(), f_genre, GOLD + (255,), 6)

    if texte.get("band"):
        # Cinzel, nicht Cormorant: Cormorant setzt Ziffern als
        # Mediävalziffern, die "1" wird dann so klein wie ein
        # Kleinbuchstabe und sieht neben BAND aus wie ein Versehen.
        f_band = schrift("Cinzel-SemiBold.ttf", int(f_genre.size * 0.78))
        gesperrt(z, m, y_genre + int(f_genre.size * 1.80), texte["band"],
                 f_band, GOLD + (255,), 8)

    linie_y = y_autor - int(f_autor.size * 0.75)
    z.line([(m - innen * 0.16, linie_y), (m + innen * 0.16, linie_y)],
           fill=GOLD + (170,), width=3)
    gesperrt(z, m, y_autor, texte["autor"].upper(), f_autor,
             WEISS + (255,), 10)

    fertig = Image.alpha_composite(leinwand.convert("RGBA"), ebene)

    werte = {
        "verlauf_deckkraft": round(gewaehlt, 2),
        "titelkontrast": round(endkontrast, 2),
        "hintergrund_unter_titel": "#%02x%02x%02x" % hintergrund,
        "ziel": ZIEL_KONTRAST,
        "bestanden": endkontrast >= ZIEL_KONTRAST,
        "verlauf_diagnose": diagnose,
        "gold_auf_grund": round(kontrast(GOLD, hintergrund), 2),
    }
    werte["ohne_text"] = leinwand
    return fertig.convert("RGB"), ebene, werte


def miniaturprobe(cover: Image.Image) -> Image.Image:
    """160 Pixel Höhe ist die Größe in der Amazon-Trefferliste auf dem
    Handy. Daneben dieselbe Miniatur dreifach vergrößert, damit man
    sieht, was übrig bleibt — nicht was man zu sehen glaubt."""
    klein = cover.resize((int(160 * BREITE / HOEHE), 160), Image.LANCZOS)
    lupe = klein.resize((klein.width * 3, klein.height * 3), Image.NEAREST)
    rand = 40
    f = schrift("Cormorant-SemiBold.ttf", 30)
    blatt = Image.new("RGB",
                      (klein.width + lupe.width + rand * 3,
                       lupe.height + rand * 2 + 50), (245, 245, 245))
    blatt.paste(klein, (rand, rand + (lupe.height - klein.height) // 2))
    blatt.paste(lupe, (rand * 2 + klein.width, rand))
    d = ImageDraw.Draw(blatt)
    unten = blatt.height - rand + 4
    d.text((rand + klein.width // 2, unten), "160 px", font=f,
           fill=(40, 40, 40), anchor="ma")
    d.text((rand * 2 + klein.width + lupe.width // 2, unten),
           "dieselbe Miniatur, dreifach vergrößert — mehr sieht "
           "niemand", font=f, fill=(40, 40, 40), anchor="ma")
    return blatt


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--bild", help="Coverbild ohne Text")
    p.add_argument("--platzhalter", action="store_true",
                   help="ohne eigenes Bild bauen, nur zur Beurteilung "
                        "der Schrift")
    p.add_argument("--reihe", default="DIE REINHARDT-BRÜDER")
    p.add_argument("--titel-script", default="Sein bestgehütetes")
    p.add_argument("--titel-caps", default="GEHEIMNIS")
    p.add_argument("--genre", default="Ein Geheimes-Baby-Liebesroman")
    p.add_argument("--band", default="BAND 1")
    p.add_argument("--autor", default="DEIN AUTORENNAME")
    p.add_argument("--ordner", default="cover/fertig")
    # Helligkeit und Saettigung sind Regler auf das Hintergrundbild, keine
    # Neugestaltung. Band 1 hat die Saettigung am 15.08.2026 von Hand um
    # Faktor 1,35 hochgezogen, weil sie unter dem Nischenband lag -- das
    # stand danach nirgends und war beim naechsten Band nicht wiederholbar.
    # Seit dem 24.08.2026 stehen beide hier, damit der Wert im Aufruf steht
    # und die Messung darunter zeigt, ob er gereicht hat.
    p.add_argument("--zoom", type=float, default=1.0,
                   help="enger schneiden; >1 vergroessert das Gesicht und "
                        "schiebt helle Bildteile unter das Titelband")
    p.add_argument("--helligkeit", type=float, default=1.0,
                   help="Faktor auf die Helligkeit des Hintergrundbildes "
                        "(1.0 = unveraendert)")
    p.add_argument("--saettigung", type=float, default=1.0,
                   help="Faktor auf die Saettigung des Hintergrundbildes")
    args = p.parse_args()

    if args.bild:
        bild = Image.open(args.bild)
        quelle = args.bild
    elif args.platzhalter:
        bild = platzhalterbild()
        quelle = "(Platzhalter)"
    else:
        p.error("entweder --bild oder --platzhalter")

    if args.helligkeit != 1.0 or args.saettigung != 1.0:
        from PIL import ImageEnhance
        bild = bild.convert("RGB")
        if args.helligkeit != 1.0:
            bild = ImageEnhance.Brightness(bild).enhance(args.helligkeit)
        if args.saettigung != 1.0:
            bild = ImageEnhance.Color(bild).enhance(args.saettigung)
        print(f"Regler: Helligkeit x{args.helligkeit}, "
              f"Saettigung x{args.saettigung}")

    texte = {"reihe": args.reihe, "titel_script": args.titel_script,
             "titel_caps": args.titel_caps, "genre": args.genre,
             "band": args.band, "autor": args.autor}

    cover, ebene, werte = bauen(bild, texte, args.zoom)

    ziel = Path(args.ordner)
    ziel.mkdir(parents=True, exist_ok=True)
    cover.save(ziel / "cover.jpg", quality=92)
    ebene.save(ziel / "schrift-ebene.png")
    miniaturprobe(cover).save(ziel / "miniaturprobe.png")

    print(f"Quelle: {quelle}")
    print(f"Format: {BREITE} x {HOEHE}  (Verhältnis "
          f"{HOEHE / BREITE:.2f}, KDP-Norm 1.60)")
    print("\nVerlauf, hochgedreht bis der Titel trägt:")
    for d in werte["verlauf_diagnose"]:
        print(f"  Deckkraft {d['deckkraft']:.2f} -> Kontrast "
              f"{d['kontrast']:.2f}")
    print(f"\nGewählt: {werte['verlauf_deckkraft']:.2f}")
    print(f"Grund unter dem Titel: {werte['hintergrund_unter_titel']}")
    print(f"Weiß auf Grund: {werte['titelkontrast']}:1  "
          f"(Ziel {ZIEL_KONTRAST}) -> "
          f"{'bestanden' if werte['bestanden'] else 'DURCHGEFALLEN'}")
    print(f"Gold auf Grund: {werte['gold_auf_grund']}:1  "
          f"(AA für große Schrift: 3.0)")

    # Zusaetzlich dort messen, wo die Buchstaben wirklich stehen. Der
    # Mittelwert oben kann einen hellen Fleck unter einem einzelnen
    # Wort nicht sehen. Bezugsgroesse: Band 1 liegt bei rund 15 %.
    anteil, mini = unter_der_schrift(werte["ohne_text"], ebene)
    print(f"Unter der Schrift: {100*anteil:.1f} % der Glyphenfläche "
          f"unter 4.5:1, schlechteste Stelle {mini:.2f}:1")
    if anteil > 0.20:
        print("  WARNUNG: deutlich mehr als bei Band 1 (rund 15 %). "
              "Ein heller Bildteil liegt unter dem Titel.")

    # Gegen die Nische halten -- mit demselben Messgerät wie die 36.
    try:
        from cover import messen
        m = messen(cover)
        print("\nGegen die 36 gemessenen Cover:")
        for feld, (lo, hi) in VERGLEICH.items():
            w = m[feld]
            lage = "im Bereich" if lo <= w <= hi else "AUSSERHALB"
            print(f"  {feld:12s} {w:>7} | Nische {lo}–{hi} | {lage}")
        print(f"  Textzone     {m['textzone']:>7} | Nische 4 "
              f"(unteres Mitteldrittel)")
    except Exception as e:
        print(f"\nVergleich nicht möglich: {str(e)[:120]}")

    print(f"\nGeschrieben: {ziel}/cover.jpg, {ziel}/schrift-ebene.png, "
          f"{ziel}/miniaturprobe.png")


if __name__ == "__main__":
    main()
