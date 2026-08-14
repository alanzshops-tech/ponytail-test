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


def suche(seite, host: str, begriff: str, anzahl: int) -> list[dict]:
    """Liest die Trefferliste. Nur was auf der Seite steht, nichts geraten."""
    from urllib.parse import quote_plus
    # i=digital-text schraenkt auf den Kindle-Shop ein.
    url = f"https://{host}/s?k={quote_plus(begriff)}&i=digital-text"
    seite.goto(url, wait_until="domcontentloaded", timeout=45000)
    seite.wait_for_timeout(2500)

    treffer = seite.evaluate("""() => {
      const raus = [];
      const karten = document.querySelectorAll('[data-component-type="s-search-result"]');
      for (const k of karten) {
        const asin = k.getAttribute('data-asin') || '';
        if (!asin) continue;
        const t = k.querySelector('h2 span, h2 a span');
        const preis = k.querySelector('.a-price .a-offscreen');
        const bew = k.querySelector('[aria-label*="Bewertungen"], [aria-label*="ratings"], .s-underline-text');
        const sterne = k.querySelector('[aria-label*="von 5"], [aria-label*="out of 5"]');
        const gesponsert = !!k.querySelector('[aria-label*="Gesponsert"], [aria-label*="Sponsored"]')
          || /Gesponsert|Sponsored/.test(k.textContent.slice(0, 400));
        raus.push({
          asin,
          titel: t ? t.textContent.trim() : '',
          preis_text: preis ? preis.textContent.trim() : '',
          bewertungen_text: bew ? bew.textContent.trim() : '',
          sterne_text: sterne ? (sterne.getAttribute('aria-label') || '') : '',
          gesponsert
        });
      }
      return raus;
    }""")

    aus = []
    for t in treffer[:anzahl]:
        t["preis"] = preis_aus(t.pop("preis_text", ""))
        t["bewertungen"] = zahl_aus(t.pop("bewertungen_text", ""))
        m = re.search(r"([\d,.]+)", t.pop("sterne_text", "") or "")
        t["sterne"] = preis_aus(m.group(1)) if m else None
        aus.append(t)
    return aus


def bsr_holen(seite, host: str, asin: str, muster: str) -> int | None:
    """BSR steht nur auf der Produktseite, nicht in der Trefferliste."""
    seite.goto(f"https://{host}/dp/{asin}", wait_until="domcontentloaded",
               timeout=45000)
    seite.wait_for_timeout(1800)
    text = seite.evaluate("() => document.body.innerText")
    m = re.search(muster, text)
    return zahl_aus(m.group(1)) if m else None


def eine_nische(seite, markt: dict, begriff: str, titel: int, details: int,
                a: float, b: float, pause: float) -> dict:
    ergebnis: dict = {"begriff": begriff, "markt": markt["host"]}
    try:
        liste = suche(seite, markt["host"], begriff, titel)
    except Exception as e:
        ergebnis["fehler"] = f"Suche fehlgeschlagen: {str(e)[:160]}"
        return ergebnis

    if not liste:
        # Leeres Ergebnis ist kein Befund. Entweder blockiert Amazon oder
        # der Selektor passt nicht mehr -- beides muss auffallen.
        ergebnis["fehler"] = ("Keine Treffer gelesen. Entweder blockiert "
                              "Amazon den Abruf oder die Seitenstruktur hat "
                              "sich geaendert. NICHT als 'keine Konkurrenz' "
                              "deuten.")
        return ergebnis

    organisch = [t for t in liste if not t["gesponsert"]]
    ergebnis["titel_gelesen"] = len(liste)
    ergebnis["davon_gesponsert"] = len(liste) - len(organisch)

    for t in organisch[:details]:
        try:
            t["bsr"] = bsr_holen(seite, markt["host"], t["asin"],
                                 markt["bsr_muster"])
        except Exception:
            t["bsr"] = None
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
         "Bewertungen Median | Preis Median | im 70-%-Fenster | gesponsert |",
         "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for e in ergebnisse:
        if e.get("fehler"):
            z.append(f"| {e['begriff']} | {e['markt']} | FEHLER | – | – | – "
                     f"| – | – | – |")
            continue
        z.append(
            f"| {e['begriff']} | {e['markt']} | {e['bsr_median'] or '–'} "
            f"| {e['bsr_bester'] or '–'} "
            f"| {e['verkaeufe_tag_geschaetzt'] or '–'} "
            f"| {e['bewertungen_median'] if e['bewertungen_median'] is not None else '–'} "
            f"| {e['preis_median'] or '–'} "
            f"| {e['im_70_prozent_fenster']}/{e['titel_gelesen']} "
            f"| {e['davon_gesponsert']}/{e['titel_gelesen']} |")

    fehler = [e for e in ergebnisse if e.get("fehler")]
    if fehler:
        z += ["", "## Fehlgeschlagen", ""]
        for e in fehler:
            z.append(f"- **{e['begriff']}** — {e['fehler']}")

    z += ["", "## Wie zu lesen", "",
          "- **BSR Median niedrig** = viel Nachfrage in dieser Nische.",
          "- **Bewertungen Median niedrig** = die Führenden sitzen locker, "
          "ein neuer Titel kann aufschließen. Hohe Werte heißen: dort steht "
          "jemand seit Jahren.",
          "- **Viele gesponserte Treffer** = die Suche wird beworben, "
          "organisch sichtbar zu werden ist teurer.",
          "- **im 70-%-Fenster** = wie viele Titel zwischen 2,99 und 9,99 € "
          "liegen. Weit darüber heißt: Der Markt trägt höhere Preise, aber "
          "die Tantieme fällt auf 35 %.",
          "",
          "Die beste Nische hat **niedrigen BSR bei niedrigen "
          "Bewertungszahlen**. Das ist Nachfrage ohne festsitzende "
          "Platzhirsche.", ""]
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
    Path("KDP-NISCHEN.md").write_text(bericht(ergebnisse, a, b),
                                      encoding="utf-8")
    print(f"\ngeschrieben: KDP-NISCHEN.md, {ordner / 'kdp-nischen.json'}")


if __name__ == "__main__":
    main()
