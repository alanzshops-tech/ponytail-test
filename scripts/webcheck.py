#!/usr/bin/env python3
"""
webcheck.py — fotografiert den Shop und misst, was Besucher erleben.

Warum: Über Design lässt sich nicht urteilen, ohne die Seite gesehen zu
haben, und über Ladezeit nicht ohne Messung. Aus der abgeschotteten
Arbeitsumgebung ist beides unmöglich — der Runner kann beides.

Was entsteht:
  bilder/<seite>-mobil.jpg     390 px breit, wie ein iPhone
  bilder/<seite>-desktop.jpg   1440 px breit
  daten/webcheck-aktuell.json  Messwerte je Seite

Gemessen wird, was ohne Besucherstrom aussagekräftig ist: Ladezeit bis
zum größten sichtbaren Element, Seitengewicht, Zahl der Anfragen, Größe
der Bilder, Anzahl blockierender Skripte. Alles Mängel, keine Hypothesen
— für Hypothesen bräuchte man Besucher, und die gibt es noch nicht.

Aufruf:
    python3 scripts/webcheck.py --urls urls-shop.txt
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlsplit

# Ein iPhone 14 ist 390 Punkte breit, ein üblicher Laptop 1440. Zwischen
# beiden liegt der Unterschied, an dem die meisten Shops scheitern.
GERAETE = {
    "mobil":   {"viewport": {"width": 390, "height": 844},
                "device_scale_factor": 2, "is_mobile": True,
                "has_touch": True},
    "desktop": {"viewport": {"width": 1440, "height": 900},
                "device_scale_factor": 1, "is_mobile": False},
}


def name_aus(url: str) -> str:
    pfad = urlsplit(url).path.strip("/") or "startseite"
    return re.sub(r"[^A-Za-z0-9]+", "-", pfad)[:60].strip("-")


def eine_seite(browser, url: str, geraet: str, bilder: Path,
               praefix: str = "") -> dict:
    from playwright.sync_api import Error as PWError

    ctx = browser.new_context(locale="de-DE", **GERAETE[geraet])
    seite = ctx.new_page()

    anfragen: list[dict] = []
    seite.on("response", lambda r: anfragen.append(
        {"url": r.url, "status": r.status,
         "typ": (r.request.resource_type or ""),
         "groesse": int(r.headers.get("content-length") or 0)}))

    messwerte: dict = {"geraet": geraet, "url": url}
    try:
        antwort = seite.goto(url, wait_until="load", timeout=60000)
        messwerte["status"] = antwort.status if antwort else 0
        seite.wait_for_timeout(3000)          # Nachladen abwarten
    except PWError as e:
        messwerte["fehler"] = str(e)[:200]
        ctx.close()
        return messwerte

    # Cookie-Dialog wegklicken. Ohne das liegt er ueber dem Hero und
    # jede Kontrastmessung dort misst den Dialog statt der Seite --
    # genau so war die erste Nachher-Aufnahme am 14.08.2026 unbrauchbar.
    # "Ablehnen" statt "Akzeptieren": Wir wollen die Seite sehen, nicht
    # in ihrem Namen einwilligen.
    messwerte["cookie_dialog"] = "nicht gefunden"
    for beschriftung in ("Ablehnen", "Alle ablehnen", "Decline",
                         "Akzeptieren", "Alle akzeptieren"):
        try:
            knopf = seite.get_by_role("button", name=beschriftung, exact=False)
            if knopf.count() and knopf.first.is_visible(timeout=1500):
                knopf.first.click(timeout=3000)
                seite.wait_for_timeout(900)
                messwerte["cookie_dialog"] = f"geschlossen via '{beschriftung}'"
                break
        except PWError:
            continue
        except Exception:
            continue

    # Kennzahlen direkt aus dem Browser, nicht geschätzt.
    messwerte.update(seite.evaluate("""() => {
      const n = performance.getEntriesByType('navigation')[0] || {};
      const lcpEintraege = performance.getEntriesByType('largest-contentful-paint');
      const fcp = performance.getEntriesByName('first-contentful-paint')[0];
      return {
        ms_bis_erste_anzeige: Math.round(fcp ? fcp.startTime : 0),
        ms_bis_groesstes_element: Math.round(
          lcpEintraege.length ? lcpEintraege[lcpEintraege.length - 1].startTime : 0),
        ms_bis_fertig: Math.round(n.loadEventEnd || 0),
        dom_knoten: document.getElementsByTagName('*').length,
        bilder_gesamt: document.images.length,
        bilder_ohne_alt: [...document.images].filter(i => !i.alt).length,
        h1_anzahl: document.querySelectorAll('h1').length,
        formulare: document.querySelectorAll('form').length,
        seitenhoehe: Math.round(document.body.scrollHeight),
      };
    }"""))

    # Waagerechtes Scrollen ist auf dem Handy der häufigste Layoutfehler.
    messwerte["waagerecht_scrollbar"] = seite.evaluate(
        "() => document.documentElement.scrollWidth > window.innerWidth + 2")

    nach_typ: dict[str, list[int]] = {}
    for a in anfragen:
        nach_typ.setdefault(a["typ"] or "sonstiges", []).append(a["groesse"])
    messwerte["anfragen"] = len(anfragen)
    messwerte["gewicht_kb"] = round(
        sum(a["groesse"] for a in anfragen) / 1024)
    messwerte["nach_typ_kb"] = {
        t: round(sum(g) / 1024) for t, g in sorted(
            nach_typ.items(), key=lambda x: -sum(x[1]))}
    messwerte["fehlerhafte_anfragen"] = [
        a["url"][:110] for a in anfragen if a["status"] >= 400][:8]

    # Nach Absender gruppieren. Erst das zeigt, welche App wie viel kostet
    # — "1260 kB Skripte" ist eine Zahl, "davon 400 kB von einem
    # Bewertungs-Widget" ist eine Entscheidungsgrundlage.
    eigen = urlsplit(url).netloc
    nach_host: dict[str, dict] = defaultdict(
        lambda: {"anfragen": 0, "kb": 0})
    for a in anfragen:
        h = urlsplit(a["url"]).netloc or "(inline)"
        nach_host[h]["anfragen"] += 1
        nach_host[h]["kb"] += a["groesse"] / 1024
    messwerte["nach_host"] = [
        {"host": h, "eigen": h.endswith(eigen) or "shopify" in h,
         "anfragen": v["anfragen"], "kb": round(v["kb"])}
        for h, v in sorted(nach_host.items(),
                           key=lambda x: -x[1]["anfragen"])]
    fremd = [x for x in messwerte["nach_host"] if not x["eigen"]]
    messwerte["fremde_hosts"] = len(fremd)
    messwerte["fremde_anfragen"] = sum(x["anfragen"] for x in fremd)
    messwerte["fremde_kb"] = sum(x["kb"] for x in fremd)

    bilder.mkdir(parents=True, exist_ok=True)
    ziel = bilder / f"{praefix}{name_aus(url)}-{geraet}.jpg"
    # Ganze Seite, damit auch der Bereich unterhalb des Falzes zu sehen
    # ist. Qualität 72 reicht zum Beurteilen und hält das Repo klein.
    seite.screenshot(path=str(ziel), full_page=True, type="jpeg", quality=72)
    messwerte["bild"] = str(ziel)
    messwerte["bild_kb"] = round(ziel.stat().st_size / 1024)
    ctx.close()
    return messwerte


def bericht(daten: dict) -> str:
    z = ["# Shop-Messung", "", f"Stand: {daten['stand']}", "",
         "Gemessen mit einem echten Browser auf dem Runner, Sprache "
         "de-DE. **Mobil** entspricht einem iPhone (390 px), "
         "**Desktop** einem Laptop (1440 px).", "",
         "> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests "
         "bräuchte es Besucher — die Zahlen hier gelten auch ohne.", "",
         "| Seite | Gerät | Status | Erste Anzeige | Größtes Element | "
         "Gewicht | Anfragen | Höhe | Querscroll |",
         "|---|---|---:|---:|---:|---:|---:|---:|:-:|"]
    for m in daten["seiten"]:
        if m.get("fehler"):
            z.append(f"| {urlsplit(m['url']).path or '/'} | {m['geraet']} "
                     f"| FEHLER | – | – | – | – | – | – |")
            continue
        z.append(
            f"| {urlsplit(m['url']).path or '/'} | {m['geraet']} "
            f"| {m.get('status','?')} | {m.get('ms_bis_erste_anzeige',0)} ms "
            f"| {m.get('ms_bis_groesstes_element',0)} ms "
            f"| {m.get('gewicht_kb',0)} kB | {m.get('anfragen',0)} "
            f"| {m.get('seitenhoehe',0)} px "
            f"| {'JA' if m.get('waagerecht_scrollbar') else '–'} |")
    z += ["", "Richtwerte von Google: Das größte Element sollte nach "
          "**2500 ms** stehen, alles darüber gilt als verbesserungswürdig. "
          "Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.", ""]

    z += ["## Was schwer wiegt", ""]
    for m in daten["seiten"]:
        if m.get("fehler") or m["geraet"] != "mobil":
            continue
        teile = ", ".join(f"{t} {kb} kB" for t, kb in
                          list(m.get("nach_typ_kb", {}).items())[:6])
        z.append(f"- `{urlsplit(m['url']).path or '/'}` — {teile}")
    z.append("")

    probleme = []
    for m in daten["seiten"]:
        p = urlsplit(m["url"]).path or "/"
        if m.get("waagerecht_scrollbar"):
            probleme.append(f"`{p}` ({m['geraet']}) lässt sich seitwärts "
                            f"scrollen — Layout läuft über")
        if m.get("h1_anzahl", 1) != 1:
            probleme.append(f"`{p}` hat {m.get('h1_anzahl')} H1-Überschriften "
                            f"statt einer")
        if m.get("bilder_ohne_alt"):
            probleme.append(f"`{p}` ({m['geraet']}): "
                            f"{m['bilder_ohne_alt']} von "
                            f"{m.get('bilder_gesamt')} Bildern ohne Alt-Text")
        for f in m.get("fehlerhafte_anfragen", []):
            probleme.append(f"`{p}` lädt etwas, das fehlschlägt: {f}")
    if probleme:
        z += ["## Befunde", ""] + [f"- {x}" for x in dict.fromkeys(probleme)] + [""]

    z += ["## Woher die Anfragen kommen", "",
          "Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de "
          "und nicht von Shopify selbst — also Apps und Dienste Dritter.", ""]
    for m in daten["seiten"]:
        if m.get("fehler") or m["geraet"] != "mobil" or not m["url"].endswith(".de/"):
            continue
        z += [f"Insgesamt {m['anfragen']} Anfragen, davon "
              f"**{m.get('fremde_anfragen', 0)} von {m.get('fremde_hosts', 0)} "
              f"fremden Servern** mit {m.get('fremde_kb', 0)} kB.", "",
              "| Absender | Anfragen | kB | eigen |", "|---|---:|---:|:-:|"]
        for h in m.get("nach_host", [])[:22]:
            z.append(f"| {h['host'][:46]} | {h['anfragen']} | {h['kb']} "
                     f"| {'ja' if h['eigen'] else '**nein**'} |")
        z.append("")

    z += ["## Bilder", "",
          "Vollständige Seitenfotos liegen in `bilder/`.", ""]
    for m in daten["seiten"]:
        if m.get("bild"):
            z.append(f"- `{m['bild']}` ({m['bild_kb']} kB)")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls-shop.txt")
    ap.add_argument("--bilder", default="bilder")
    # Vorschau-URLs haben keinen Pfad und hiessen sonst alle
    # "startseite" -- damit wuerde eine Nachher-Aufnahme die
    # Vorher-Aufnahme ueberschreiben und der Vergleich waere weg.
    ap.add_argument("--praefix", default="")
    ap.add_argument("--out", default="daten")
    a = ap.parse_args()

    adressen = [z.strip() for z in Path(a.urls).read_text(encoding="utf-8")
                .splitlines() if z.strip() and not z.startswith("#")]
    from playwright.sync_api import sync_playwright

    ergebnis = {"stand": str(date.today()), "seiten": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--no-sandbox"])
        for url in adressen:
            for geraet in GERAETE:
                print(f"  {geraet:8s} {url}")
                m = eine_seite(browser, url, geraet, Path(a.bilder), a.praefix)
                if m.get("fehler"):
                    print(f"           FEHLER: {m['fehler'][:90]}")
                else:
                    print(f"           {m['ms_bis_groesstes_element']} ms, "
                          f"{m['gewicht_kb']} kB, {m['anfragen']} Anfragen")
                ergebnis["seiten"].append(m)
        browser.close()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "webcheck-aktuell.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("WEBSITE.md").write_text(bericht(ergebnis), encoding="utf-8")
    print(f"\n{len(ergebnis['seiten'])} Messungen, Bericht in WEBSITE.md")


if __name__ == "__main__":
    main()
