#!/usr/bin/env python3
"""
pruefstand.py — misst, was gutes Design ausmacht, statt darüber zu reden.

Drei Werkzeuge, alle quelloffen, alle ohne Konto:

  axe-core       Deque Systems, MPL-2.0. Der Prüfer, den auch Lighthouse
                 und Google benutzen. Findet Kontraste unter dem Grenzwert,
                 Knöpfe ohne Beschriftung, kaputte Überschriftenfolgen —
                 also genau die Dinge, die eine Seite billig wirken lassen,
                 lange bevor jemand sagen kann warum.

  Pixelvergleich Pillow. Vor jeder Änderung ein Foto, nach jeder Änderung
                 ein Foto, Differenz in Prozent. Wer eine Zeile CSS ändert
                 und drei Seiten weiter etwas zerschießt, merkt das sonst
                 erst durch einen Kunden, den es nie gab.

  Textmaß       Zeilenlänge, Schriftgröße, Kontrast der Fließtexte. Die
                 drei Zahlen, an denen Lesbarkeit hängt.

Barrierefreiheit ist für Homeeins keine Pflicht — das BFSG nimmt
Kleinstunternehmen (unter 10 Beschäftigte UND unter 2 Mio. Umsatz) für
Dienstleistungen ausdrücklich aus. Es bleibt trotzdem sinnvoll: Dieselben
Befunde sind Bedienbarkeitsfehler, und Google bewertet sie mit.

Aufruf:
    python3 scripts/pruefstand.py --urls urls-shop.txt
    python3 scripts/pruefstand.py --urls urls-shop.txt --grundlinie
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

GERAETE = {
    "mobil":   {"viewport": {"width": 390, "height": 844},
                "device_scale_factor": 2, "is_mobile": True,
                "has_touch": True},
    "desktop": {"viewport": {"width": 1440, "height": 900},
                "device_scale_factor": 1, "is_mobile": False},
}

# axe kennt vier Schweregrade. Nur die oberen zwei sind es wert, dass
# jemand seine Zeit darauf verwendet.
SCHWER = ("critical", "serious")


def name_aus(url: str) -> str:
    import re
    pfad = urlsplit(url).path.strip("/") or "startseite"
    return re.sub(r"[^A-Za-z0-9]+", "-", pfad)[:60].strip("-")


def axe_quelle() -> str:
    """axe-core als Datei, nicht aus einem CDN — sonst hängt die Messung
    an einem fremden Server und liefert bei Ausfall stillschweigend
    weniger Befunde."""
    for p in (Path("node_modules/axe-core/axe.min.js"),
              Path("/usr/lib/node_modules/axe-core/axe.min.js")):
        if p.exists():
            return p.read_text(encoding="utf-8")
    raise SystemExit("axe-core fehlt. Vorher: npm install axe-core")


def eine_seite(browser, url: str, geraet: str, axe_js: str,
               bilder: Path) -> dict:
    ctx = browser.new_context(locale="de-DE", **GERAETE[geraet])
    seite = ctx.new_page()
    m: dict = {"url": url, "geraet": geraet}
    try:
        seite.goto(url, wait_until="load", timeout=60000)
        seite.wait_for_timeout(3000)
    except Exception as e:                                       # noqa: BLE001
        m["fehler"] = str(e)[:200]
        ctx.close()
        return m

    seite.add_script_tag(content=axe_js)
    bericht = seite.evaluate("""async () => {
      const r = await axe.run(document, {
        resultTypes: ['violations'],
        runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}
      });
      return r.violations.map(v => ({
        id: v.id, impact: v.impact, help: v.help, anzahl: v.nodes.length,
        beispiel: (v.nodes[0] && v.nodes[0].html || '').slice(0, 160)
      }));
    }""")
    m["verstoesse"] = bericht
    m["schwer"] = sum(v["anzahl"] for v in bericht
                      if v.get("impact") in SCHWER)
    m["leicht"] = sum(v["anzahl"] for v in bericht
                      if v.get("impact") not in SCHWER)

    # Bewertungen. Am 9.8.2026 standen elf erfundene auf der Startseite
    # und 26 als Sterne-Metafelder auf fünf Produkten. Die Metafelder
    # sind gelöscht — ob das Judge.me-Widget noch etwas anzeigt, sieht
    # man nur im Browser, weil es seine Daten aus der App holt und
    # nicht aus Shopify.
    m["bewertungen"] = seite.evaluate("""() => {
      const txt = document.body.innerText || '';
      // Nur sichtbare Widgets, keine Script-Tags. Der erste Lauf griff
      // sich Judge.mes Einstellungs-Script und zitierte JSON statt
      // Bewertungen — ein Selektor, der zu viel fängt, ist kein Messgerät.
      const widget = [...document.querySelectorAll(
        '.jdgm-widget, .jdgm-rev-widget, .jdgm-widget-actions-wrapper')]
        .find(e => e.tagName !== 'SCRIPT' && e.offsetParent !== null) || null;
      const treffer = (r) => (txt.match(r) || []).length;
      return {
        widget_da: !!widget,
        widget_text: widget ? (widget.innerText || '').trim().slice(0, 300) : null,
        sterne_symbole: treffer(/★|⭐/g),
        wort_bewertung: treffer(/\\bBewertung(en)?\\b/g),
        wort_rezension: treffer(/\\bRezension(en)?\\b/g),
        wort_sterne: treffer(/\\bSterne?\\b/g),
        // Strukturdaten sind die Stelle, an der Google Sterne abgreift.
        preise_mit_eur: (txt.match(/\d,\d{2}\s*EUR/g) || []).length,
        preise_gesamt: (txt.match(/\d,\d{2}\s*(?:€|EUR)/g) || []).length,
        aggregate_rating: [...document.querySelectorAll(
            'script[type="application/ld+json"]')]
          .map(s => s.textContent || '')
          .filter(t => t.includes('aggregateRating')).length
      };
    }""")

    # Widerrufsbutton der App „Revoq EU Widerrufsbutton". Breit gesucht,
    # weil ich den Selektor der App nicht kenne — dafür wird derselbe
    # Detektor gegen das Live-Theme gehalten, wo der Knopf aus ist.
    # Ein Fund ohne Gegentest wäre kein Beweis.
    m["widerruf"] = seite.evaluate("""() => {
      const alle = [...document.querySelectorAll('*')];
      const passt = (e) => {
        const s = ((e.className && e.className.baseVal !== undefined
                    ? e.className.baseVal : e.className) || '') + ' ' + (e.id || '');
        return /revoq|widerruf/i.test(s);
      };
      const treffer = alle.filter(passt);
      const sichtbar = treffer.filter(e => e.offsetParent !== null
        || getComputedStyle(e).position === 'fixed');
      const fest = alle.filter(e => {
        const c = getComputedStyle(e);
        return c.position === 'fixed' && (e.innerText || '').match(/Widerruf/i);
      });
      return {
        elemente: treffer.length,
        sichtbar: sichtbar.length,
        schwebend_mit_text: fest.length,
        beispiel: treffer.length
          ? (treffer[0].outerHTML || '').slice(0, 180) : null,
        skripte: [...document.querySelectorAll('script[src]')]
          .map(s => s.src).filter(u => /revoq/i.test(u)).slice(0, 3)
      };
    }""")

    # Lesbarkeit: die drei Zahlen, an denen Fließtext steht oder fällt.
    m["text"] = seite.evaluate("""() => {
      const abs = [...document.querySelectorAll('p, li')]
        .filter(e => (e.innerText || '').trim().length > 60);
      if (!abs.length) return null;
      const px = e => parseFloat(getComputedStyle(e).fontSize);
      const zeichen = e => {
        const b = e.getBoundingClientRect().width;
        return Math.round(b / (px(e) * 0.5));   // ~0,5 em je Zeichen
      };
      const groessen = abs.map(px).sort((a, b) => a - b);
      const laengen = abs.map(zeichen).sort((a, b) => a - b);
      const med = a => a[Math.floor(a.length / 2)];
      return {absaetze: abs.length,
              schriftgroesse_median: med(groessen),
              zu_klein: groessen.filter(g => g < 16).length,
              zeilenlaenge_median: med(laengen),
              zu_breit: laengen.filter(l => l > 80).length};
    }""")

    bilder.mkdir(parents=True, exist_ok=True)
    ziel = bilder / f"{name_aus(url)}-{geraet}.png"
    seite.screenshot(path=str(ziel), full_page=True)
    m["bild"] = str(ziel)
    ctx.close()
    return m


def vergleichen(neu: Path, alt: Path) -> dict | None:
    """Zwei Aufnahmen derselben Seite. Gibt den Anteil geänderter Pixel."""
    if not alt.exists():
        return None
    from PIL import Image, ImageChops
    a, b = Image.open(alt).convert("RGB"), Image.open(neu).convert("RGB")
    if a.size != b.size:
        # Andere Höhe heißt: Es ist etwas dazugekommen oder weggefallen.
        # Das ist ein Befund, kein Fehler der Messung.
        return {"groesse_alt": a.size, "groesse_neu": b.size,
                "anteil": None, "hinweis": "Seitenhöhe hat sich geändert"}
    diff = ImageChops.difference(a, b).convert("L")
    geaendert = sum(1 for p in diff.getdata() if p > 12)
    return {"groesse_alt": a.size, "groesse_neu": b.size,
            "anteil": round(100 * geaendert / (a.size[0] * a.size[1]), 3)}


def bericht(d: dict) -> str:
    z = ["# Prüfstand", "", f"Stand: {d['stand']}", "",
         "Gemessen mit **axe-core** (Deque, MPL-2.0) gegen WCAG 2.1 AA, "
         "dazu Lesbarkeitsmaße und ein Pixelvergleich gegen die letzte "
         "Grundlinie.", "",
         "> Barrierefreiheit ist für Homeeins keine gesetzliche Pflicht — "
         "das BFSG nimmt Kleinstunternehmen für Dienstleistungen aus. "
         "Die Befunde sind trotzdem echte Bedienfehler.", "",
         "| Seite | Gerät | schwer | leicht | Schrift | Zeilenlänge | "
         "Pixel geändert |", "|---|---|---:|---:|---:|---:|---:|"]
    for m in d["seiten"]:
        p = urlsplit(m["url"]).path or "/"
        if m.get("fehler"):
            z.append(f"| {p} | {m['geraet']} | FEHLER | – | – | – | – |")
            continue
        t = m.get("text") or {}
        v = m.get("vergleich")
        pix = ("–" if not v else
               (v.get("hinweis") or f"{v.get('anteil')} %"))
        z.append(f"| {p} | {m['geraet']} | **{m.get('schwer', 0)}** "
                 f"| {m.get('leicht', 0)} "
                 f"| {t.get('schriftgroesse_median', '–')} px "
                 f"| {t.get('zeilenlaenge_median', '–')} Z. | {pix} |")
    z += ["", "Richtwerte: Fließtext ab **16 px**, Zeilen **45–80 Zeichen**. "
          "Längere Zeilen verliert das Auge beim Rücksprung.", ""]

    z += ["## Widerrufsbutton", "",
          "| Seite | Elemente | sichtbar | schwebend m. Text | Skripte |",
          "|---|---:|---:|---:|---:|"]
    for m in d["seiten"]:
        if m.get("fehler") or m["geraet"] != "mobil":
            continue
        w = m.get("widerruf") or {}
        z.append(f"| {urlsplit(m['url']).path or '/'} | {w.get('elemente', 0)} "
                 f"| {w.get('sichtbar', 0)} | {w.get('schwebend_mit_text', 0)} "
                 f"| {len(w.get('skripte') or [])} |")
    bsp = next((m["widerruf"]["beispiel"] for m in d["seiten"]
                if (m.get("widerruf") or {}).get("beispiel")), None)
    if bsp:
        z += ["", "Erstes gefundenes Element:", "", "```", bsp, "```"]
    z += ["", "Derselbe Detektor läuft gegen das veröffentlichte Theme, wo "
          "der Knopf abgeschaltet ist. Nur wenn er dort **null** meldet und "
          "in der Sandbox mehr, ist der Fund ein Beweis.", "",
          "## Preisschreibweise", "",
          "| Seite | Preise | davon mit „EUR\" |", "|---|---:|---:|"]
    for m in d["seiten"]:
        if m.get("fehler") or m["geraet"] != "mobil":
            continue
        b = m.get("bewertungen") or {}
        z.append(f"| {urlsplit(m['url']).path or '/'} "
                 f"| {b.get('preise_gesamt', 0)} | {b.get('preise_mit_eur', 0)} |")
    z += ["", "Deutsche Schreibweise ist „124,99 €\" — Zahl vorn, Zeichen "
          "hinten, ohne Währungskürzel. Das Kürzel schaltet ein Haken im "
          "Theme ab; die Stellung des Zeichens ist eine Shop-Einstellung.",
          "", "## Bewertungen auf der Live-Seite", "",
          "| Seite | Judge.me-Widget | ★-Symbole | „Bewertung\" | "
          "„Sterne\" | aggregateRating |", "|---|:-:|---:|---:|---:|---:|"]
    for m in d["seiten"]:
        if m.get("fehler") or m["geraet"] != "mobil":
            continue
        b = m.get("bewertungen") or {}
        z.append(f"| {urlsplit(m['url']).path or '/'} "
                 f"| {'ja' if b.get('widget_da') else '–'} "
                 f"| {b.get('sterne_symbole', 0)} "
                 f"| {b.get('wort_bewertung', 0)} "
                 f"| {b.get('wort_sterne', 0)} "
                 f"| {b.get('aggregate_rating', 0)} |")
    for m in d["seiten"]:
        b = m.get("bewertungen") or {}
        if m["geraet"] == "mobil" and b.get("widget_text"):
            z += ["", f"Widget-Inhalt auf `{urlsplit(m['url']).path}`:", "",
                  "```", b["widget_text"], "```"]
    z += ["", "**aggregateRating** ist die Stelle, an der Google Sterne für "
          "die Trefferliste abgreift. Steht dort etwas ohne echte Käufe, "
          "wirbt der Shop auch außerhalb der eigenen Seite mit Erfundenem.",
          ""]

    # Verstöße zusammenfassen, nicht je Seite wiederholen.
    gesamt: dict[str, dict] = {}
    for m in d["seiten"]:
        for v in m.get("verstoesse", []):
            e = gesamt.setdefault(v["id"], {**v, "anzahl": 0, "seiten": set()})
            e["anzahl"] += v["anzahl"]
            e["seiten"].add(urlsplit(m["url"]).path or "/")
    if gesamt:
        z += ["## Befunde, nach Häufigkeit", "",
              "| Regel | Schwere | Fälle | betroffen |", "|---|---|---:|---|"]
        for v in sorted(gesamt.values(),
                        key=lambda x: (x.get("impact") not in SCHWER,
                                       -x["anzahl"])):
            z.append(f"| {v['help']} | {v.get('impact')} | {v['anzahl']} "
                     f"| {', '.join(sorted(v['seiten']))} |")
        z += ["", "Beispiele:", ""]
        for v in list(sorted(gesamt.values(), key=lambda x: -x["anzahl"]))[:5]:
            z.append(f"- `{v['id']}` — `{v['beispiel']}`")
        z.append("")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls-shop.txt")
    ap.add_argument("--bilder", default="bilder/pruefstand")
    ap.add_argument("--grundlinie", action="store_true",
                    help="aktuelle Aufnahmen als neue Vergleichsbasis "
                         "ablegen statt zu vergleichen")
    a = ap.parse_args()

    adressen = [z.strip() for z in Path(a.urls).read_text(encoding="utf-8")
                .splitlines() if z.strip() and not z.startswith("#")]
    axe_js = axe_quelle()
    from playwright.sync_api import sync_playwright

    bilder, basis = Path(a.bilder), Path(a.bilder) / "grundlinie"
    d = {"stand": str(date.today()), "seiten": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--no-sandbox"])
        for url in adressen:
            for geraet in GERAETE:
                print(f"  {geraet:8s} {url}")
                m = eine_seite(browser, url, geraet, axe_js, bilder)
                if not m.get("fehler"):
                    alt = basis / Path(m["bild"]).name
                    m["vergleich"] = vergleichen(Path(m["bild"]), alt)
                    print(f"           {m['schwer']} schwer, "
                          f"{m['leicht']} leicht"
                          + (f", {m['vergleich']['anteil']} % Pixel anders"
                             if m.get("vergleich")
                             and m["vergleich"].get("anteil") is not None
                             else ""))
                d["seiten"].append(m)
        browser.close()

    if a.grundlinie:
        import shutil
        basis.mkdir(parents=True, exist_ok=True)
        for m in d["seiten"]:
            if m.get("bild"):
                shutil.copy(m["bild"], basis / Path(m["bild"]).name)
        print(f"\nGrundlinie erneuert: {len(list(basis.glob('*.png')))} Bilder")

    Path("daten").mkdir(exist_ok=True)
    Path("daten/pruefstand.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8")
    Path("PRUEFSTAND.md").write_text(bericht(d), encoding="utf-8")
    print("\nBericht in PRUEFSTAND.md")


if __name__ == "__main__":
    main()
