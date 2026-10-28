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
    #
    # Die Zahl allein genuegt nicht. '[class*="loox"]' faengt auch
    # leere Platzhalter-Container, und beide Produktseiten meldeten
    # exakt 7 -- ein gleichfoermiger Wert ueber alle Faelle war hier
    # schon dreimal ein defekter Selektor. Deshalb kommt zu jedem
    # Treffer die Klasse und der sichtbare Text mit; erst daran laesst
    # sich entscheiden, ob dort eine Bewertung steht oder eine leere
    # Huelle.
    gefunden = seite.evaluate(
        """() => {
            const sel = ['[class*="loox"]', '[class*="jdgm"]',
                         '[class*="star-rating"]', '[class*="rating"]'];
            const raus = [];
            const gesehen = new Set();
            for (const s of sel) {
                for (const el of document.querySelectorAll(s)) {
                    if (gesehen.has(el)) continue;
                    gesehen.add(el);
                    const r = el.getBoundingClientRect();
                    if (r.width <= 0 || r.height <= 0) continue;
                    raus.push({
                        klasse: (el.className || '').toString().slice(0, 70),
                        text: (el.innerText || '').trim().slice(0, 40),
                        breite: Math.round(r.width),
                        hoehe: Math.round(r.height)});
                }
            }
            return raus;
        }""")
    ergebnis["sterne_sichtbar"] = len(gefunden)
    ergebnis["sterne_treffer"] = gefunden[:12]
    # "Mit Text" war als Mass untauglich. Der erste Lauf meldete sieben
    # Treffer mit Text und loeste die Warnung aus -- der Text lautete
    # "Be the first to write a review". Ein ehrlich leeres Widget ist
    # das Gegenteil eines Verstosses, und die Warnung stand trotzdem
    # da. Ein Messgeraet, das den sauberen Fall anschwaerzt, ist so
    # schaedlich wie eines, das den schmutzigen durchlaesst.
    #
    # Gezaehlt wird jetzt, was eine BEWERTUNG belegt: ein Sternzeichen
    # oder eine Zahl in der Form 4,8 bzw. 4.8 -- und ausdruecklich
    # nicht, wenn der Text sagt, dass es keine Bewertungen gibt.
    leer = re.compile(
        r"be the first|no reviews|noch keine|keine bewertungen|"
        r"schreibe die erste|write a review", re.I)
    bewertet = re.compile(r"[★⭐]|\b\d[.,]\d\b")
    ergebnis["bewertungen_angezeigt"] = sum(
        1 for g in gefunden
        if bewertet.search(g["text"]) and not leer.search(g["text"]))
    ergebnis["leer_gemeldet"] = sum(
        1 for g in gefunden if leer.search(g["text"]))
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
        angezeigt = e.get("bewertungen_angezeigt", 0)
        leer_n = e.get("leer_gemeldet", 0)
        z.append(f"**Sichtbare Bewertungs-Elemente:** {sterne} · "
                 f"davon mit angezeigter Bewertung: {angezeigt} · "
                 f"ausdrücklich \"noch keine\": {leer_n}")
        treffer = e.get("sterne_treffer") or []
        if treffer:
            z.append("")
            z.append("| Klasse | Text | Größe |")
            z.append("|---|---|---|")
            for g in treffer:
                txt = (g["text"] or "—").replace("|", "/").replace("\n", " ")
                z.append(f"| `{g['klasse']}` | {txt} | "
                         f"{g['breite']}×{g['hoehe']} |")
        if angezeigt:
            z.append("")
            z.append("> **Es werden Bewertungen angezeigt.** Das ist nur "
                     "dann in Ordnung, wenn echte Kaeufer dahinterstehen. "
                     "Bewertungen ohne Kaeufer sind nach Anhang zu "
                     "Paragraf 3 Abs. 3 Nr. 23b/23c UWG verboten "
                     "(CLAUDE.md, Regel 3). Dieses Geraet sieht nur die "
                     "Anzeige -- ob die Bewertungen echt sind, kann es "
                     "nicht sagen.")
        elif leer_n:
            z.append("")
            z.append("> Das Widget meldet ausdruecklich, dass es noch "
                     "keine Bewertungen gibt. Das ist der saubere Fall.")
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
