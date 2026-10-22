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
        antwort = seite.goto(url, wait_until="load", timeout=60000)
        seite.wait_for_timeout(1500)
    except PWError as e:
        ergebnis["fehler"] = str(e)[:200]
        ctx.close()
        return ergebnis

    # Ohne diese drei Angaben sieht eine 404-Seite im Bericht genauso
    # aus wie eine Produktseite ohne Schema: beides "0 Bloecke". Am
    # 22.10.2026 fiel die Messung von 3 Bloecken auf 0, und ohne
    # Statuscode und Titel liess sich nicht entscheiden, ob der Shop
    # sich geaendert hat oder die Messung. CLAUDE.md: Leeres Ergebnis
    # ist kein bestaetigtes Nichts.
    ergebnis["status"] = antwort.status if antwort else None
    ergebnis["titel"] = (seite.title() or "")[:120]
    ergebnis["textanfang"] = (seite.inner_text("body") or "")[:200].replace(
        "\n", " ")

    bloecke = seite.eval_on_selector_all(
        'script[type="application/ld+json"]',
        "els => els.map(e => e.textContent)")

    # Welche Bewertungs-App laedt hier, und zeigt sie Sterne?
    #
    # Der Anlass steht in CLAUDE.md: Judge.me lieferte aggregateRating
    # weiter, nachdem die Sterne-Metafelder geloescht waren. Das JSON-LD
    # allein beantwortet die Frage also nicht -- es sagt, was Google
    # sieht, nicht, welche App es hineingeschrieben hat und was der
    # Besucher sieht. Bei einem Laden mit sieben Bestellungen in drei
    # Jahren ist beides zu pruefen: Bewertungen ohne Kaeufer sind nicht
    # nur unschoen, sondern nach Anhang zu Paragraf 3 Abs. 3 Nr. 23b/23c
    # UWG verboten.
    #
    # Gemessen wird die Herkunft der Skripte, nicht geraten: jede
    # fremde Skriptadresse auf der Seite, gefiltert auf die bekannten
    # Anbieter.
    apps = seite.eval_on_selector_all(
        "script[src]",
        "els => els.map(e => e.src)")
    ergebnis["bewertungs_apps"] = sorted({
        name for name, marke in (("Loox", "loox.io"),
                                 ("Judge.me", "judge.me"),
                                 ("Yotpo", "yotpo.com"),
                                 ("Stamped", "stamped.io"),
                                 ("Okendo", "okendo.io"))
        if any(marke in (s or "") for s in apps)})
    ergebnis["fremde_skripte"] = sorted({
        urlsplit(s).netloc for s in apps if s
        and urlsplit(s).netloc
        and "homeeins.de" not in urlsplit(s).netloc
        and "shopify" not in urlsplit(s).netloc})

    # Sichtbare Sterne. Ein Widget, das bei null Bewertungen trotzdem
    # Sterne malt, ist genau der Fall, der hier schon einmal auftrat.
    ergebnis["sterne_sichtbar"] = seite.evaluate(
        """() => {
            const sel = ['.loox-rating', '[class*="loox"]',
                         '.jdgm-star', '[class*="jdgm"]',
                         '[class*="star-rating"]'];
            let n = 0;
            for (const s of sel) {
                for (const el of document.querySelectorAll(s)) {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) n++;
                }
            }
            return n;
        }""")
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
        if e.get("status") is not None:
            z.append(f"HTTP {e['status']} · Titel: „{e.get('titel')}“")
            z.append("")
        if e.get("fehler"):
            z.append(f"Seite nicht ladbar: {e['fehler']}")
            z.append("")
            continue
        z.append(f"{e['anzahl_bloecke']} `application/ld+json`-Block(e) "
                 f"gefunden, davon {e['product_bloecke']} mit "
                 f"`@type: Product`.")
        z.append("")

        apps = e.get("bewertungs_apps", [])
        sterne = e.get("sterne_sichtbar")
        z.append("**Bewertungs-Apps auf der Seite:** "
                 + (", ".join(apps) if apps else "keine erkannt"))
        if len(apps) > 1:
            z.append("")
            z.append("> **Zwei Bewertungs-Apps gleichzeitig.** Doppeltes "
                     "Markup, und bei Judge.me ist belegt, dass sie "
                     "`aggregateRating` weitergeliefert hat, nachdem die "
                     "Daten geloescht waren (CLAUDE.md). Eine davon "
                     "gehoert deinstalliert, nicht nur deaktiviert.")
        z.append("")
        z.append(f"**Sichtbare Sterne-Elemente:** {sterne}")
        if sterne:
            z.append("")
            z.append("> Sterne sind sichtbar. Das ist nur dann in "
                     "Ordnung, wenn echte Kaeuferbewertungen dahinter "
                     "stehen. Bewertungen ohne Kaeufer sind nach Anhang "
                     "zu Paragraf 3 Abs. 3 Nr. 23b/23c UWG verboten "
                     "(CLAUDE.md, Regel 3). Dieses Geraet zaehlt nur "
                     "Elemente -- ob die Bewertungen echt sind, kann es "
                     "nicht sagen.")
        fremd = e.get("fremde_skripte", [])
        if fremd:
            z.append("")
            z.append(f"Fremde Skript-Hosts ({len(fremd)}): "
                     + ", ".join(f"`{h}`" for h in fremd))
        z.append("")
        if e["product_bloecke"] == 0:
            z.append("**Kein Product-Schema gefunden.** Das ist ein "
                     "leeres Ergebnis, kein bestätigtes \"nichts da\" — "
                     "möglich, dass es dynamisch nach dem gemessenen "
                     "Zeitpunkt nachlädt. Mit einer Seite gegenprüfen, "
                     "die sicher ein Schema haben sollte, bevor das als "
                     "Befund gilt.")
            z.append("")
            z.append(f"Seitenanfang zur Einordnung: "
                     f"„{e.get('textanfang', '')}“")
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
