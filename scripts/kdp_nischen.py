#!/usr/bin/env python3
"""
kdp_nischen.py — misst Nachfrage und Wettbewerb für Buchnischen auf Amazon.

Wozu: Jede Quelle zu KDP sagt „Nische mit hoher Nachfrage und niedriger
Konkurrenz suchen". Das ist eine Anweisung ohne Messgerät. Dieses Skript
liefert die Zahlen dazu — je Suchbegriff:

  * Bestseller-Rang der Spitzentitel  (beobachtbar, direkt vergleichbar)
  * Zahl der Bewertungen der Führenden (wie fest sitzen sie?)
  * Preisniveau  (liegt es im 2,99–9,99-Fenster für 70 % Tantiemen?)
  * Anteil bezahlter Platzierungen  (wie umkämpft ist die Suche?)

**Zur Nutzung:** Amazons Nutzungsbedingungen untersagen automatisierten
Zugriff. Dieses Skript ist bewusst kleinvolumig und nur lesend, mit
Pausen zwischen den Abrufen. Es ersetzt kein bezahltes Werkzeug wie
Publisher Rocket, das dafür lizenziert ist. Wer regelmäßig und in Menge
misst, sollte dorthin wechseln.

**Zur Aussagekraft:** Der Bestseller-Rang (BSR) ist eine echte, von
Amazon veröffentlichte Zahl und **innerhalb desselben Marktplatzes direkt
vergleichbar** — niedriger heißt mehr Verkäufe. Die Umrechnung in
Stückzahlen ist dagegen eine Schätzung mit kategorieabhängigen
Konstanten. Deshalb steht hier der BSR im Vordergrund und die Schätzung
nur daneben, mit sichtbaren Konstanten.

Aufruf:
    python3 scripts/kdp_nischen.py --begriffe "milliardär liebesroman" \\
        "enemies to lovers" --markt de --titel 10 --details 5
"""

from __future__ import annotations

import argparse
import json
import random
import re
import time
from datetime import date
from pathlib import Path
from statistics import median

MARKTPLAETZE = {
    "de": {"host": "www.amazon.de", "sprache": "de-DE",
           "bsr_muster": r"Nr\.\s*([\d.]+)\s*in\s*(?:Kindle-Shop|Bücher)"},
    "com": {"host": "www.amazon.com", "sprache": "en-US",
            "bsr_muster": r"#([\d,]+)\s*in\s*(?:Kindle Store|Books)"},
}

# Umrechnung BSR -> geschaetzte Tagesverkaeufe: taeglich = A * BSR^(-B).
# Diese Konstanten sind aus oeffentlich kursierenden Kalibrierungen fuer
# den Kindle-Shop uebernommen und NICHT selbst validiert. Sie dienen der
# Groessenordnung, nicht der Buchhaltung. Ueber --konstanten aenderbar.
A_STANDARD, B_STANDARD = 100_000.0, 0.85

# Der Bericht wird bei jedem Lauf neu geschrieben. Von Hand ergaenzte
# Auswertungen gingen dabei verloren -- am 14.08.2026 knapp verhindert.
# Alles unterhalb dieser Zeile wird uebernommen.
MARKER = '<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->'


def zahl_aus(text: str) -> int | None:
    """'1.234' oder '1,234' -> 1234. Beide Tausendertrennzeichen, weil
    amazon.de und amazon.com sich unterscheiden."""
    if not text:
        return None
    sauber = re.sub(r"[^\d]", "", text)
    return int(sauber) if sauber else None


def preis_aus(text: str) -> float | None:
    """'9,99 €' oder '$4.99' -> float. Deutsches Komma beachten."""
    if not text:
        return None
    t = re.sub(r"[^\d,.]", "", text)
    if not t:
        return None
    # Deutsches Format: letztes Komma ist das Dezimaltrennzeichen.
    if "," in t and (t.rfind(",") > t.rfind(".")):
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def geschaetzte_verkaeufe(bsr: int, a: float, b: float) -> float:
    if bsr <= 0:
        return 0.0
    return round(a * (bsr ** -b), 2)


def consent_wegklicken(seite) -> str:
    """Amazon zeigt beim ersten Aufruf eine Cookie-Abfrage, die die
    Trefferliste verdeckt. Beim Lauf vom 14.08.2026 scheiterten dadurch
    die ersten sechs von acht Begriffen -- die letzten beiden kamen nur
    durch, weil die Huerde bis dahin von selbst weg war. Positionsabhaengig,
    also kein Zufall."""
    for text in ("Alle akzeptieren", "Accept all", "Alle Cookies akzeptieren",
                 "Nur erforderliche Cookies", "Weiter shoppen",
                 "Continue shopping", "Accept Cookies", "Dismiss"):
        try:
            k = seite.get_by_role("button", name=text, exact=False)
            if k.count() and k.first.is_visible(timeout=1200):
                k.first.click(timeout=2500)
                seite.wait_for_timeout(1200)
                return f"geschlossen via '{text}'"
        except Exception:
            continue
    # Amazon nutzt teils <input type=submit> statt <button>.
    for sel in ("#sp-cc-accept", 'input[name="accept"]',
                'input[data-cel-widget="sp-cc-accept"]'):
        try:
            if seite.locator(sel).count():
                seite.locator(sel).first.click(timeout=2500)
                seite.wait_for_timeout(1200)
                return f"geschlossen via {sel}"
        except Exception:
            continue
    return "nicht gefunden"


def suche(seite, host: str, begriff: str, anzahl: int) -> list[dict]:
    """Liest die Trefferliste. Nur was auf der Seite steht, nichts geraten."""
    from urllib.parse import quote_plus
    # i=digital-text schraenkt auf den Kindle-Shop ein.
    url = f"https://{host}/s?k={quote_plus(begriff)}&i=digital-text"
    seite.goto(url, wait_until="domcontentloaded", timeout=45000)
    seite.wait_for_timeout(2000)
    consent_wegklicken(seite)
    seite.wait_for_timeout(1200)

    treffer = seite.evaluate("""() => {
      const raus = [];
      const karten = document.querySelectorAll('[data-component-type="s-search-result"]');
      for (const k of karten) {
        const asin = k.getAttribute('data-asin') || '';
        if (!asin) continue;
        const t = k.querySelector('h2 span, h2 a span');
        const preis = k.querySelector('.a-price .a-offscreen');
        // Bewertungszahl: Der frueher genutzte Selektor .s-underline-text
        // greift nicht mehr. Robuster ist, im Kartentext nach der Zahl in
        // Klammern oder vor "Bewertungen"/"ratings" zu suchen.
        let bewText = '';
        const bewEl = k.querySelector('[aria-label$="Bewertungen"], [aria-label$="ratings"], a[href*="#customerReviews"] span');
        if (bewEl) bewText = bewEl.getAttribute('aria-label') || bewEl.textContent || '';
        if (!/\d/.test(bewText)) {
          const m = k.textContent.match(/([\d.,]+)\s*(?:Bewertungen|Sternebewertungen|ratings)/);
          if (m) bewText = m[1];
        }
        const sterne = k.querySelector('[aria-label*="von 5"], [aria-label*="out of 5"]');
        // Amazon markiert bezahlte Treffer unterschiedlich: mal per
        // aria-label, mal als eigenes Element, mal nur als Text. Der
        // vorige Selektor sah nur die ersten 400 Zeichen und traf nie --
        // alle sechs Nischen meldeten exakt 0, was kein Befund sein kann.
        const gesponsert =
          !!k.querySelector('[aria-label*="Gesponsert"], [aria-label*="Sponsored"], '
            + '[data-component-type="sp-sponsored-result"], .puis-sponsored-label-text, '
            + 's-sponsored-label-info-icon, .s-sponsored-label-text')
          || /\bGesponsert\b|\bSponsored\b/.test(k.textContent);
        raus.push({
          asin,
          titel: t ? t.textContent.trim() : '',
          preis_text: preis ? preis.textContent.trim() : '',
          bewertungen_text: bewText.trim(),
          sterne_text: sterne ? (sterne.getAttribute('aria-label') || '') : '',
          gesponsert
        });
      }
      return raus;
    }""")

    aus = []
    for t in treffer[:anzahl]:
        p = preis_aus(t.pop("preis_text", ""))
        # 0,00 heisst bei Amazon in aller Regel Kindle Unlimited, nicht
        # "kostenlos zu haben". Als Preis gewertet zieht es den Median
        # nach unten und taeuscht ein billiges Marktsegment vor.
        t["kindle_unlimited"] = (p == 0.0)
        t["preis"] = None if (p is None or p == 0.0) else p
        t["bewertungen"] = zahl_aus(t.pop("bewertungen_text", ""))
        m = re.search(r"([\d,.]+)", t.pop("sterne_text", "") or "")
        t["sterne"] = preis_aus(m.group(1)) if m else None
        aus.append(t)
    return aus


# Oberkategorien, die bei jedem Titel stehen und nichts unterscheiden.
# Interessant sind nur die Unterkategorien darunter -- die entscheiden
# ueber das Bestseller-Abzeichen.
OBERKATEGORIEN = ("Kindle-Shop", "Bücher", "Kindle Store", "Books",
                  "Kindle eBooks", "eBook Kindle")


# Zwischen Beschriftung und Wert stehen auf Amazon unsichtbare
# Richtungszeichen (U+200E/U+200F) und ein Doppelpunkt. Deshalb wird
# nicht auf ": " geprueft, sondern auf "irgendwas Kurzes ohne Ziffern".
# Amazon setzt an dieser Stelle mal einen normalen Bindestrich, mal
# einen geschuetzten (U+2011) und mal ein Leerzeichen. Der Selbsttest
# hat den geschuetzten gefunden -- mit nur "[- ]" lieferte
# "Print\u2011Ausgabe" kein Ergebnis, und das haette im Bericht wie
# "keine Angabe" ausgesehen.
BINDE = r"[-\u2010\u2011\u2012\u2013\u00ad ]"
SEITEN_MUSTER = (
    rf"Seitenzahl der Print{BINDE}Ausgabe[^\d]{{0,25}}([\d.,]+)",
    rf"Print{BINDE}length[^\d]{{0,25}}([\d.,]+)",
    r"L(?:ä|ae)nge[^\d]{0,25}([\d.,]+)\s*Seiten",
)


def seitenzahl(text: str) -> int | None:
    """Umfang eines Kindle-Titels in Druckseiten.

    Warum ueberhaupt: Die Zahl, nach der bei Kindle Unlimited bezahlt
    wird (KENPC), veroeffentlicht Amazon nicht. Die Seitenzahl der
    Print-Ausgabe steht dagegen auf fast jeder Produktseite und ist der
    beste oeffentliche Anhaltspunkt fuer die Laenge.
    """
    for muster in SEITEN_MUSTER:
        m = re.search(muster, text, re.I)
        if m:
            n = zahl_aus(m.group(1))
            # Unter 20 und ueber 2000 Seiten ist kein Liebesroman,
            # sondern ein Lesefehler.
            if n and 20 <= n <= 2000:
                return n
    return None


# --- Hitzegrad -------------------------------------------------------
#
# Wozu: Fuer Band 1 stand die Frage offen, ob ein Liebesroman dieser
# Nische eine Liebesszene braucht. Die Antwort war bis zum 16.08.2026
# eine Vermutung. Deutsche Romance-Titel schreiben den Grad fast immer
# selbst auf die Produktseite -- als Spice-Angabe, als Warnhinweis oder
# als ausdrueckliches "ohne explizite Szenen". Das laesst sich zaehlen.
#
# Die Muster sind absichtlich mehrwortig. "heiss" allein faengt
# "Heisshunger", "es heisst" und "heiss begehrt"; genau diese Sorte
# Fehlgriff hat in diesem Repository schon dreimal einen Bericht
# verdorben. Deshalb steht unten ein Negativfall, der treffen wuerde,
# wenn jemand die Muster wieder aufweicht.

HITZE_EXPLIZIT = (
    r"\bexplizit(?:e|en|er)\s+(?:Szenen|Liebesszenen|Darstellung)",
    r"\bSpice[- ]?(?:Level|Grad|Faktor)",
    r"[\U0001F336]",                       # Chilischote
    r"\bab\s?18\b|\b18\+",
    r"\bSexszenen?\b",
    r"\berotische(?:r|n|s)?\s+(?:Roman|Liebesroman|Szenen|Momente)",
    r"\bsteamy\b",
    r"\bprickelnde(?:r|n|s)?\s+Erotik",
)

HITZE_GESCHLOSSEN = (
    r"\bohne\s+explizite",
    r"\bkeine\s+expliziten",
    r"\bclosed[- ]door\b",
    r"\bnicht\s+explizit\b",
    r"\bohne\s+Erotik\b",
)

HITZE_DAZWISCHEN = (
    r"\bprickelnd(?:e|er|en|es)?\b(?!\s+Erotik)",
    r"\bknistert?\b|\bKnistern\b",
    r"\bsinnlich(?:e|er|en|es)?\b",
    r"\bleidenschaftlich(?:e|er|en|es)?\b",
)

HITZE_KATEGORIEN = ("Erotik", "Erotische", "Erotisch")


def hitze(text: str, kategorien: list[tuple[int, str]] | None = None) -> str:
    """explizit | geschlossen | dazwischen | keine Angabe.

    Reihenfolge mit Absicht: Wer "ohne explizite Szenen" schreibt, sagt
    ausdruecklich, dass es geschlossen ist -- und wuerde sonst vom
    Explizit-Muster gefangen, weil das Wort dort vorkommt.
    """
    if kategorien:
        for _, name in kategorien:
            if any(name.startswith(k) for k in HITZE_KATEGORIEN):
                return "explizit"
    for muster in HITZE_GESCHLOSSEN:
        if re.search(muster, text, re.I):
            return "geschlossen"
    for muster in HITZE_EXPLIZIT:
        if re.search(muster, text, re.I):
            return "explizit"
    for muster in HITZE_DAZWISCHEN:
        if re.search(muster, text, re.I):
            return "dazwischen"
    return "keine Angabe"


def hitze_selbsttest() -> None:
    """Ohne diesen Test ist 'keine Angabe' nicht von 'Muster kaputt' zu
    unterscheiden."""
    faelle = [
        ("Spice-Level: 3 von 5. Enthaelt explizite Szenen.", "explizit"),
        ("Ein Liebesroman ohne explizite Szenen.", "geschlossen"),
        ("Zwischen den beiden knistert es von der ersten Seite an.",
         "dazwischen"),
        # Der Negativfall. Jedes dieser Woerter hat ein Muster schon
        # einmal faelschlich ausgeloest.
        ("Es heisst, der Roman sei heiss begehrt. Sie hatte Heisshunger "
         "und 18 Kapitel vor sich. Ein Buch ab 1899.", "keine Angabe"),
    ]
    for text, erwartet in faelle:
        ist = hitze(text)
        zeichen = "ok " if ist == erwartet else "FEHLER"
        print(f"  {zeichen} {ist:<13} <- {text[:52]!r}")
        if ist != erwartet:
            sys.exit(f"Hitze-Selbsttest fehlgeschlagen: {erwartet} erwartet.")
    if hitze("", [(4, "Erotische Literatur")]) != "explizit":
        sys.exit("Hitze-Selbsttest: Kategorie nicht erkannt.")
    print("  ok  Kategorie 'Erotische Literatur' zaehlt als explizit")


def bsr_holen(seite, host: str, asin: str,
              muster: str) -> tuple[int | None, list[tuple[int, str]],
                                     int | None, str]:
    """BSR und Kategorien stehen nur auf der Produktseite.

    Amazon listet dort untereinander:
        Nr. 1.234 in Kindle-Shop
        Nr. 12 in Zeitgenössische Liebesromane
        Nr. 34 in Liebesromane (Kindle-Shop)

    Die erste Zeile ist der Gesamtrang, die darunter sind die
    Kategorien, in denen ein Titel ein Abzeichen bekommen kann.
    """
    seite.goto(f"https://{host}/dp/{asin}", wait_until="domcontentloaded",
               timeout=45000)
    seite.wait_for_timeout(1800)
    text = seite.evaluate("() => document.body.innerText")

    m = re.search(muster, text)
    bsr = zahl_aus(m.group(1)) if m else None

    umfang = seitenzahl(text)

    kategorien = []
    for rang, name in re.findall(
            r"(?:Nr\.|#)\s*([\d.,]+)\s+in\s+([^\n(]{3,70})", text):
        name = name.strip().rstrip(".,")
        if any(name.startswith(o) for o in OBERKATEGORIEN):
            continue
        r = zahl_aus(rang)
        if r:
            kategorien.append((r, name))
    return bsr, kategorien[:4], umfang, hitze(text, kategorien)


def eine_nische(seite, markt: dict, begriff: str, titel: int, details: int,
                a: float, b: float, pause: float) -> dict:
    ergebnis: dict = {"begriff": begriff, "markt": markt["host"]}
    try:
        liste = suche(seite, markt["host"], begriff, titel)
    except Exception as e:
        ergebnis["fehler"] = f"Suche fehlgeschlagen: {str(e)[:160]}"
        return ergebnis

    if not liste:
        # Ein Fehlversuch kann an der Consent-Huerde liegen. Einmal neu.
        time.sleep(3)
        try:
            liste = suche(seite, markt["host"], begriff, titel)
        except Exception:
            liste = []
    if not liste:
        # Leeres Ergebnis ist kein Befund. Entweder blockiert Amazon oder
        # der Selektor passt nicht mehr -- beides muss auffallen.
        # Ohne Diagnose sehen CAPTCHA, Consent-Variante und geaenderte
        # Seitenstruktur im Bericht identisch aus. Am 14.08.2026 scheiterten
        # acht .com-Begriffe, und die Ursache war aus dem Bericht nicht
        # erkennbar.
        try:
            titel = seite.title()
            text = " ".join(
                seite.evaluate("() => document.body.innerText")[:220].split())
        except Exception:
            titel, text = "(nicht lesbar)", "(nicht lesbar)"
        ergebnis["fehler"] = ("Keine Treffer gelesen. NICHT als 'keine "
                              "Konkurrenz' deuten.")
        ergebnis["seitentitel"] = titel
        ergebnis["seitenanfang"] = text
        return ergebnis

    organisch = [t for t in liste if not t["gesponsert"]]
    ergebnis["titel_gelesen"] = len(liste)
    ergebnis["davon_gesponsert"] = len(liste) - len(organisch)

    for t in organisch[:details]:
        try:
            (t["bsr"], t["kategorien"], t["seiten"],
             t["hitze"]) = bsr_holen(
                seite, markt["host"], t["asin"], markt["bsr_muster"])
        except Exception:
            t["bsr"], t["kategorien"], t["seiten"] = None, [], None
            t["hitze"] = "nicht gelesen"
        time.sleep(pause + random.uniform(0, pause))

    bsrs = [t["bsr"] for t in organisch[:details] if t.get("bsr")]
    preise = [t["preis"] for t in liste if t.get("preis")]
    bews = [t["bewertungen"] for t in organisch[:details]
            if t.get("bewertungen") is not None]

    ergebnis["titel"] = liste
    ergebnis["bsr_werte"] = bsrs
    ergebnis["bsr_median"] = int(median(bsrs)) if bsrs else None
    ergebnis["bsr_bester"] = min(bsrs) if bsrs else None
    ergebnis["verkaeufe_tag_geschaetzt"] = (
        geschaetzte_verkaeufe(int(median(bsrs)), a, b) if bsrs else None)
    ergebnis["bewertungen_median"] = int(median(bews)) if bews else None
    ergebnis["preis_median"] = round(median(preise), 2) if preise else None
    ergebnis["kindle_unlimited"] = sum(
        1 for t in liste if t.get("kindle_unlimited"))
    seiten = [t["seiten"] for t in organisch[:details] if t.get("seiten")]
    ergebnis["seiten_werte"] = sorted(seiten)
    ergebnis["seiten_median"] = int(median(seiten)) if seiten else None

    ergebnis["hitze"] = [t.get("hitze", "nicht gelesen")
                         for t in organisch[:details]]

    zaehler: dict[str, list[int]] = {}
    for t in organisch[:details]:
        for rang, name in t.get("kategorien", []):
            zaehler.setdefault(name, []).append(rang)
    ergebnis["kategorien"] = sorted(
        ({"name": n, "titel": len(r), "rang_bester": min(r)}
         for n, r in zaehler.items()),
        key=lambda x: (-x["titel"], x["rang_bester"]))
    ergebnis["im_70_prozent_fenster"] = (
        sum(1 for p in preise if 2.99 <= p <= 9.99) if preise else 0)
    return ergebnis


def bericht(ergebnisse: list[dict], a: float, b: float) -> str:
    z = ["# KDP-Nischen", "", f"Stand: {date.today().isoformat()}", "",
         "Gemessen auf den öffentlichen Amazon-Trefferlisten und "
         "Produktseiten. **Der Bestseller-Rang (BSR) ist die belastbare "
         "Zahl** — innerhalb desselben Marktplatzes direkt vergleichbar, "
         "niedriger heißt mehr Verkäufe. Die Umrechnung in Stückzahlen ist "
         "eine Schätzung.", "",
         f"Verwendete Konstanten: `täglich = {a:g} × BSR^-{b:g}`. "
         "Öffentlich kursierende Kalibrierung, **nicht selbst validiert** — "
         "gut für Größenordnungen, nicht für Planung.", "",
         "| Nische | Markt | BSR Median | BSR bester | Verk./Tag (gesch.) | "
         "Bewertungen Median | Preis Median | im 70-%-Fenster | in KU | "
         "gesponsert |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for e in ergebnisse:
        if e.get("fehler"):
            z.append(f"| {e['begriff']} | {e['markt']} | FEHLER | – | – | – "
                     f"| – | – | – | – |")
            continue
        z.append(
            f"| {e['begriff']} | {e['markt']} | {e['bsr_median'] or '–'} "
            f"| {e['bsr_bester'] or '–'} "
            f"| {e['verkaeufe_tag_geschaetzt'] or '–'} "
            f"| {e['bewertungen_median'] if e['bewertungen_median'] is not None else '–'} "
            f"| {e['preis_median'] or '–'} "
            f"| {e['im_70_prozent_fenster']}/{e['titel_gelesen']} "
            f"| {e.get('kindle_unlimited', 0)}/{e['titel_gelesen']} "
            f"| {e['davon_gesponsert']}/{e['titel_gelesen']} |")

    fehler = [e for e in ergebnisse if e.get("fehler")]
    if fehler:
        z += ["", "## Fehlgeschlagen", ""]
        for e in fehler:
            z.append(f"- **{e['begriff']}** — {e['fehler']}")
            if e.get("seitentitel"):
                z.append(f"  - Seitentitel: `{e['seitentitel']}`")
                z.append(f"  - Seitenanfang: `{e.get('seitenanfang','')[:180]}`")

    # --- Hitzegrad
    stufen = ("explizit", "dazwischen", "geschlossen", "keine Angabe")
    z += ["", "## Hitzegrad der Spitzentitel", "",
          "Wie explizit die gemessenen Titel selbst angeben zu sein — "
          "aus Beschreibung, Warnhinweisen und Kategorien der "
          "Produktseite. Deutsche Romance-Titel schreiben das fast immer "
          "selbst hin. **Was ohne Angabe bleibt, ist nicht "
          "„geschlossen“, sondern ungemessen.**", "",
          "| Nische | " + " | ".join(stufen) + " |",
          "|---|" + "---:|" * len(stufen)]
    gesamt = {s: 0 for s in stufen}
    for e in ergebnisse:
        if e.get("fehler"):
            continue
        zaehl = {s: 0 for s in stufen}
        for h in e.get("hitze", []):
            if h in zaehl:
                zaehl[h] += 1
                gesamt[h] += 1
        z.append(f"| {e['begriff']} | "
                 + " | ".join(str(zaehl[s]) for s in stufen) + " |")
    z.append("| **gesamt** | "
             + " | ".join(f"**{gesamt[s]}**" for s in stufen) + " |")

    z += ["", "## Wie zu lesen", "",
          "- **BSR Median niedrig** = viel Nachfrage in dieser Nische.",
          "- **Bewertungen Median niedrig** = die Führenden sitzen locker, "
          "ein neuer Titel kann aufschließen. Hohe Werte heißen: dort steht "
          "jemand seit Jahren.",
          "- **Viele gesponserte Treffer** = die Suche wird beworben, "
          "organisch sichtbar zu werden ist teurer.",
          "- **in KU** = wie viele Titel bei Kindle Unlimited liegen (Preis "
          "0,00 €). Hoher Anteil heißt: In dieser Nische wird gelesen, nicht "
          "gekauft — Einnahmen kommen dann über Seitenaufrufe, nicht über "
          "Tantiemen je Verkauf.",
          "- **im 70-%-Fenster** = wie viele Titel zwischen 2,99 und 9,99 € "
          "liegen. Weit darüber heißt: Der Markt trägt höhere Preise, aber "
          "die Tantieme fällt auf 35 %.",
          "",
          "Die beste Nische hat **niedrigen BSR bei niedrigen "
          "Bewertungszahlen**. Das ist Nachfrage ohne festsitzende "
          "Platzhirsche.", ""]

    # Die Titel im Wortlaut. Bisher wurden sie gelesen und wieder
    # weggeworfen, und deshalb war jede Aussage ueber Titelmuster
    # ("Nennt man den Trope im Untertitel?") eine Vermutung. Sie stehen
    # jetzt da, damit man sie auszaehlen kann statt sie zu erinnern.
    z += ["## Die Spitzentitel im Wortlaut", "",
          "Ungekuerzt, in der Reihenfolge der Trefferliste. Wer daraus "
          "Titelmuster ableitet, kann sie hier nachzaehlen.", ""]
    for e in ergebnisse:
        if e.get("fehler"):
            continue
        z.append(f"**{e['begriff']}**", )
        z.append("")
        namen = [(t.get("titel") or "").strip()
                 for t in (e.get("titel") or [])]
        for i, name in enumerate([n for n in namen if n], 1):
            z.append(f"{i}. {name}")
        z.append("")

    z += ["## Wie lang sind die Spitzentitel?", "",
          "Die Zahl, nach der Kindle Unlimited bezahlt (KENPC), "
          "veröffentlicht Amazon nicht. Die **Seitenzahl der "
          "Print-Ausgabe** steht dagegen auf fast jeder Produktseite und "
          "ist der beste öffentliche Anhaltspunkt. Als grobe Umrechnung "
          "für deutsche Belletristik: **rund 250 Wörter je Druckseite** — "
          "das ist eine Faustregel, keine Messung, und deshalb steht die "
          "Seitenzahl daneben.", "",
          "| Nische | Titel mit Angabe | Seiten Median | Spanne | "
          "≈ Wörter (×250) |",
          "|---|---:|---:|---|---:|"]
    for e in ergebnisse:
        if e.get("fehler"):
            continue
        w = e.get("seiten_werte") or []
        if not w:
            z.append(f"| {e['begriff']} | 0 | – | – | – |")
            continue
        m = e["seiten_median"]
        z.append(f"| {e['begriff']} | {len(w)} | {m} | {min(w)}–{max(w)} "
                 f"| {m * 250:,} |".replace(",", "."))
    z.append("")

    z += ["## Kategorien der Spitzentitel", "",
          "In welchen Unterkategorien die gemessenen Titel stehen und auf "
          "welchem Rang der beste von ihnen dort liegt. Das ist die Liste, "
          "aus der bei KDP die drei Kategorien gewählt werden. Die "
          "Oberkategorien (Kindle-Shop, Bücher) sind ausgelassen, weil sie "
          "bei jedem Titel stehen und nichts unterscheiden.", "",
          "**Ein niedriger bester Rang heißt: dort ist es eng.** Eine "
          "Kategorie, in der der beste gemessene Titel auf Rang 40 steht, "
          "ist leichter zu erreichen als eine, in der er auf Rang 2 steht.",
          ""]
    leer = True
    for e in ergebnisse:
        if e.get("fehler") or not e.get("kategorien"):
            continue
        leer = False
        z += [f"**{e['begriff']}**", "",
              "| Kategorie | Titel darin | bester Rang |",
              "|---|---:|---:|"]
        for k in e["kategorien"][:8]:
            z.append(f"| {k['name']} | {k['titel']} | {k['rang_bester']} |")
        z.append("")
    if leer:
        z += ["*Keine Kategorien gelesen. Das heißt nicht, dass es keine "
              "gibt — entweder wurde keine Produktseite erreicht oder das "
              "Muster passt nicht mehr.*", ""]
    return "\n".join(z)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--begriffe", nargs="+", required=True)
    ap.add_argument("--markt", default="de", choices=sorted(MARKTPLAETZE))
    ap.add_argument("--titel", type=int, default=10,
                    help="Wie viele Treffer je Begriff lesen")
    ap.add_argument("--details", type=int, default=5,
                    help="Fuer wie viele davon die Produktseite oeffnen (BSR)")
    ap.add_argument("--pause", type=float, default=2.0,
                    help="Grundpause zwischen Produktseiten in Sekunden")
    ap.add_argument("--konstanten", default=f"{A_STANDARD},{B_STANDARD}")
    ap.add_argument("--out", default="daten")
    a_arg = ap.parse_args()

    a, b = (float(x) for x in a_arg.konstanten.split(","))
    markt = MARKTPLAETZE[a_arg.markt]

    from playwright.sync_api import sync_playwright

    ergebnisse = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(
            locale=markt["sprache"],
            viewport={"width": 1440, "height": 900},
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"))
        seite = ctx.new_page()

        # Aufwaermen: Beim Lauf vom 14.08.2026 scheiterten zweimal
        # ausgerechnet die ERSTEN Begriffe -- die Sitzung hatte noch keine
        # Cookies, und die Consent-Abfrage verdeckte die Trefferliste. Ein
        # Besuch der Startseite vorweg setzt sie, bevor gemessen wird.
        try:
            seite.goto(f"https://{markt['host']}/",
                       wait_until="domcontentloaded", timeout=45000)
            seite.wait_for_timeout(2000)
            print(f"Aufwaermen: Consent {consent_wegklicken(seite)}", flush=True)
            seite.wait_for_timeout(1500)
        except Exception as e:
            print(f"Aufwaermen fehlgeschlagen: {str(e)[:120]}", flush=True)

        # Erst das Messgeraet pruefen, dann messen. Ein kaputtes
        # Hitze-Muster liefert lauter "keine Angabe" und sieht im
        # Bericht aus wie ein Befund.
        print("Hitze-Selbsttest:", flush=True)
        hitze_selbsttest()

        for begriff in a_arg.begriffe:
            print(f"messe: {begriff} ({markt['host']}) ...", flush=True)
            ergebnisse.append(eine_nische(seite, markt, begriff, a_arg.titel,
                                          a_arg.details, a, b, a_arg.pause))
            time.sleep(a_arg.pause * 2)
        browser.close()

    ordner = Path(a_arg.out)
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / "kdp-nischen.json").write_text(
        json.dumps(ergebnisse, indent=2, ensure_ascii=False), encoding="utf-8")
    ziel = Path("KDP-NISCHEN.md")
    handnotizen = ""
    if ziel.exists():
        alt = ziel.read_text(encoding="utf-8")
        if MARKER in alt:
            handnotizen = "\n" + MARKER + alt.split(MARKER, 1)[1]
            print("Handnotizen uebernommen "
                  f"({len(handnotizen)} Zeichen)")
    ziel.write_text(bericht(ergebnisse, a, b) + handnotizen, encoding="utf-8")
    print(f"\ngeschrieben: KDP-NISCHEN.md, {ordner / 'kdp-nischen.json'}")


if __name__ == "__main__":
    main()
