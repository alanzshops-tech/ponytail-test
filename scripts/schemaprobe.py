#!/usr/bin/env python3
"""
schemaprobe.py — prüft strukturierte Daten (JSON-LD) auf Produktseiten.

Warum: Recherche (13.08.2026) zu Shopify-SEO 2026 zeigt wiederholt
denselben Befund — vollständiges Product-Schema (GTIN, Brand,
aggregateRating, Review) soll die Klickrate in der Google-Suche
messbar erhöhen, Standard-Themes liefern oft nur ein unvollständiges
Grundgerüst. Ob das bei Homeeins/Dawn zutrifft, war bisher nicht
gemessen — nur vermutet.

Rein lesend. Ändert nichts am Theme (Regel 2 in CLAUDE.md: nie in
Dawns Dateien schreiben). Liefert nur die Diagnose, damit eine
Ergänzung — falls nötig — gezielt und geprüft in `custom-liquid`
passieren kann, nicht geraten.

Aufruf:
    python3 scripts/schemaprobe.py --urls url1 url2 ...
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


def name_aus(url: str) -> str:
    pfad = urlsplit(url).path.strip("/") or "seite"
    return re.sub(r"[^A-Za-z0-9]+", "-", pfad)[:60].strip("-")


def schema_pruefen(browser, url: str) -> dict:
    from playwright.sync_api import Error as PWError

    ctx = browser.new_context(locale="de-DE")
    seite = ctx.new_page()
    ergebnis: dict = {"url": url}
    try:
        seite.goto(url, wait_until="load", timeout=60000)
        seite.wait_for_timeout(1500)
    except PWError as e:
        ergebnis["fehler"] = str(e)[:200]
        ctx.close()
        return ergebnis

    bloecke = seite.eval_on_selector_all(
        'script[type="application/ld+json"]',
        "els => els.map(e => e.textContent)")
    ctx.close()

    ergebnis["anzahl_bloecke"] = len(bloecke)
    geparst = []
    for roh in bloecke:
        try:
            geparst.append(json.loads(roh))
        except (json.JSONDecodeError, TypeError):
            geparst.append({"_parsefehler": True, "_roh_laenge": len(roh or "")})
    ergebnis["bloecke"] = geparst

    # Product-Block(e) heraussuchen, auch wenn @graph verschachtelt ist.
    def wandern(x, sammlung):
        if isinstance(x, dict):
            t = x.get("@type")
            typen = t if isinstance(t, list) else [t]
            if any(str(ty).lower() == "product" for ty in typen if ty):
                sammlung.append(x)
            for v in x.values():
                wandern(v, sammlung)
        elif isinstance(x, list):
            for v in x:
                wandern(v, sammlung)

    produkte = []
    for b in geparst:
        wandern(b, produkte)
    ergebnis["product_bloecke"] = len(produkte)

    if produkte:
        p = produkte[0]
        FELDER = ("gtin", "gtin8", "gtin12", "gtin13", "gtin14", "mpn",
                  "brand", "sku", "aggregateRating", "review", "offers",
                  "image", "description")
        vorhanden = {f: (f in p and p[f] not in (None, "", [])) for f in FELDER}
        ergebnis["product_felder"] = vorhanden
        # offers.price/availability separat, weil oft das Einzige, was
        # Dawn von sich aus mitliefert -- damit lässt sich unterscheiden
        # zwischen "nichts da" und "nur das Nötigste da".
        offers = p.get("offers")
        if isinstance(offers, list):
            offers = offers[0] if offers else {}
        if isinstance(offers, dict):
            ergebnis["offers_felder"] = {
                "price": bool(offers.get("price")),
                "availability": bool(offers.get("availability")),
                "priceCurrency": bool(offers.get("priceCurrency")),
            }
    return ergebnis


def bericht(ergebnisse: list[dict]) -> str:
    z = ["# Schemaprobe — strukturierte Daten (JSON-LD)", "",
         "Rein lesend geprüft, keine Theme-Änderung. Prüft, ob und wie "
         "vollständig Product-Schema auf Produktseiten steht — das "
         "beeinflusst laut Recherche die Klickrate in der Google-Suche, "
         "unabhängig vom Ranking selbst.", ""]

    for e in ergebnisse:
        z.append(f"## {e['url']}")
        z.append("")
        if e.get("fehler"):
            z.append(f"Seite nicht ladbar: {e['fehler']}")
            z.append("")
            continue
        z.append(f"{e['anzahl_bloecke']} `application/ld+json`-Block(e) "
                 f"gefunden, davon {e['product_bloecke']} mit "
                 f"`@type: Product`.")
        z.append("")
        if e["product_bloecke"] == 0:
            z.append("**Kein Product-Schema gefunden.** Das ist ein "
                     "leeres Ergebnis, kein bestätigtes \"nichts da\" — "
                     "möglich, dass es dynamisch nach dem gemessenen "
                     "Zeitpunkt nachlädt. Mit einer Seite gegenprüfen, "
                     "die sicher ein Schema haben sollte, bevor das als "
                     "Befund gilt.")
            z.append("")
            continue
        felder = e.get("product_felder", {})
        z.append("| Feld | vorhanden |")
        z.append("|---|---|")
        for f, v in felder.items():
            z.append(f"| `{f}` | {'✅' if v else '❌'} |")
        z.append("")
        if e.get("offers_felder"):
            z.append("`offers`-Unterfelder: " + ", ".join(
                f"`{k}` {'✅' if v else '❌'}"
                for k, v in e["offers_felder"].items()))
            z.append("")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", nargs="+", required=True)
    ap.add_argument("--out", default="daten")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright

    ergebnisse = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for url in a.urls:
            print(f"Prüfe {url} ...")
            ergebnisse.append(schema_pruefen(browser, url))
        browser.close()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "schemaprobe.json").write_text(
        json.dumps(ergebnisse, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("SCHEMAPROBE.md").write_text(bericht(ergebnisse), encoding="utf-8")
    print("SCHEMAPROBE.md geschrieben")


if __name__ == "__main__":
    main()
