#!/usr/bin/env python3
"""
zoomprobe.py — funktioniert Bild-Zoom auf dem Handy wirklich?

PRODUKTBILDER.md nennt das als einen der am leichtesten übersehenen
Mängel: Baymard misst, dass rund 40 % der Shops weder Pinch- noch
Doppeltipp-Zoom auf Produktbildern unterstützen. Ein Screenshot beweist
das nicht — nur ein echter Tap im Browser zeigt, ob etwas passiert.

Zwei getrennte Fragen:
  1. Erlaubt das Viewport-Meta-Tag Pinch-Zoom überhaupt (technische
     Grundvoraussetzung, unabhängig vom Theme)?
  2. Öffnet ein Tap auf das Hauptbild eine vergrößerte Ansicht (Dawns
     eigener Zoom-Mechanismus)?

Ein "kein Unterschied nach dem Tap" ist ein Fund, kein Fehlschlag des
Skripts -- deshalb wird der Zustand vorher UND nachher festgehalten,
nicht nur ein Ja/Nein geraten.

Aufruf:
    python3 scripts/zoomprobe.py --pfad /products/led-taschenlampe-aufladbar-zoom-warnlicht
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SHOP = "https://www.homeeins.de"

GERAET = {"viewport": {"width": 390, "height": 844},
          "device_scale_factor": 2, "is_mobile": True, "has_touch": True}


def foto(seite, ziel: Path) -> int:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    seite.screenshot(path=str(ziel), type="jpeg", quality=80)
    return round(ziel.stat().st_size / 1024)


def zoom_pruefen(browser, pfad: str, bilder: Path) -> dict:
    ctx = browser.new_context(locale="de-DE", **GERAET)
    seite = ctx.new_page()
    d: dict = {"pfad": pfad}
    try:
        seite.goto(SHOP + pfad, wait_until="load", timeout=60000)
        seite.wait_for_timeout(2500)

        # Zusatzfrage, unabhaengig vom Zoom-Thema: welche App blendet den
        # "Vertrag widerrufen"-Button ein? Sucht das Element ueber seinen
        # Text, geht dann den Elternpfad hoch bis zu einem Knoten mit
        # erkennbaren Merkmalen (id, class, data-*), und listet alle
        # Skript-Adressen, die nicht von shopify.com selbst stammen --
        # eine davon ist fast immer die Herkunft der App.
        d["widerruf_button"] = seite.evaluate("""() => {
          const alle = [...document.querySelectorAll('button, a, div, span')];
          const treffer = alle.find(
            el => (el.textContent || '').trim() === 'Vertrag widerrufen'
                  && el.children.length === 0);
          if (!treffer) return {gefunden: false};

          const pfad = [];
          let el = treffer;
          for (let i = 0; i < 6 && el; i++) {
            pfad.push({
              tag: el.tagName,
              id: el.id || null,
              klassen: el.className && typeof el.className === 'string'
                ? el.className : null,
              data_attribute: [...el.attributes]
                .filter(a => a.name.startsWith('data-'))
                .map(a => `${a.name}="${a.value}"`.slice(0, 120)),
            });
            el = el.parentElement;
          }

          const fremdeSkripte = [...document.querySelectorAll('script[src]')]
            .map(s => s.src)
            .filter(src => src && !src.includes('cdn.shopify.com')
                         && !src.includes('shopifycloud.com')
                         && !src.includes('homeeins.de'));

          return {gefunden: true, elternpfad: pfad,
                  fremde_skripte: [...new Set(fremdeSkripte)].slice(0, 15)};
        }""")

        # Frage 1: erlaubt das Meta-Tag Pinch-Zoom ueberhaupt?
        meta = seite.evaluate("""() => {
          const m = document.querySelector('meta[name="viewport"]');
          return m ? m.getAttribute('content') : null;
        }""")
        d["viewport_meta"] = meta
        inhalt = (meta or "").replace(" ", "")
        d["user_scalable_no"] = "user-scalable=no" in inhalt
        d["maximum_scale_1"] = "maximum-scale=1" in inhalt or "maximum-scale=1.0" in inhalt
        d["pinch_zoom_technisch_moeglich"] = not (
            d["user_scalable_no"] or d["maximum_scale_1"])

        # Ausgangszustand: Anzahl Bild-Elemente, groesstes Bild, ob ein
        # <dialog>/Modal offen ist.
        vorher = seite.evaluate("""() => ({
          bilder: document.images.length,
          dialoge_offen: [...document.querySelectorAll('dialog')]
            .filter(el => el.open).length,
          scrollHoehe: document.body.scrollHeight,
        })""")
        d["vorher"] = vorher
        d["bild_vorher"] = str(bilder / "zoomprobe-1-vorher.jpg")
        foto(seite, bilder / "zoomprobe-1-vorher.jpg")

        # Frage 2: Tap auf das Hauptbild -- Dawns eigener Mechanismus.
        # Mehrere moegliche Bauweisen, weil Themes das unterschiedlich
        # umsetzen (Zoom-Icon, klickbares Bild, eigener Button).
        haupt = None
        for wahl in [".product__media img", ".product-media-container img",
                     "[id^='MediaGallery'] img", "product-media-gallery img"]:
            loc = seite.locator(wahl).first
            if loc.count() and loc.is_visible():
                haupt = loc
                d["bild_selektor"] = wahl
                break
        if haupt is None:
            d["fehler"] = "kein Produktbild-Element gefunden"
            ctx.close()
            return d

        try:
            haupt.tap(timeout=8000)
        except Exception as e:                                   # noqa: BLE001
            d["tap_fehler"] = str(e)[:200]
        seite.wait_for_timeout(1500)

        nachher = seite.evaluate("""() => ({
          bilder: document.images.length,
          dialoge_offen: [...document.querySelectorAll('dialog')]
            .filter(el => el.open).length,
          scrollHoehe: document.body.scrollHeight,
        })""")
        d["nachher"] = nachher
        d["bild_nachher"] = str(bilder / "zoomprobe-2-nach-tap.jpg")
        foto(seite, bilder / "zoomprobe-2-nach-tap.jpg")

        # Groesster sichtbarer Unterschied: hat sich ueberhaupt etwas
        # veraendert? Ein offener Dialog ist der eindeutigste Beleg.
        d["dialog_geoeffnet"] = nachher["dialoge_offen"] > vorher["dialoge_offen"]
        d["seite_veraendert"] = nachher != vorher

        # Doppeltipp als zweiter, unabhaengiger Versuch -- manche Themes
        # reagieren nur darauf, nicht auf einfaches Tippen.
        try:
            haupt.dblclick(timeout=8000)
            seite.wait_for_timeout(1500)
        except Exception as e:                                   # noqa: BLE001
            d["doppeltipp_fehler"] = str(e)[:200]
        nach_doppeltipp = seite.evaluate("""() => ({
          dialoge_offen: [...document.querySelectorAll('dialog')]
            .filter(el => el.open).length,
        })""")
        d["dialog_nach_doppeltipp"] = (
            nach_doppeltipp["dialoge_offen"] > vorher["dialoge_offen"])
        d["bild_nach_doppeltipp"] = str(bilder / "zoomprobe-3-doppeltipp.jpg")
        foto(seite, bilder / "zoomprobe-3-doppeltipp.jpg")

    except Exception as e:                                       # noqa: BLE001
        d["fehler"] = str(e)[:250]
    ctx.close()
    return d


def bericht(d: dict) -> str:
    z = ["# Zoomprobe — funktioniert Bild-Zoom auf dem Handy?", "",
         f"Seite: `{d.get('pfad')}`", "",
         "Gemessen, nicht angenommen: zwei unabhängige Fragen, jede mit "
         "Screenshot als Beleg.", "", "## 0. Herkunft des \"Vertrag "
         "widerrufen\"-Buttons", ""]
    wb = d.get("widerruf_button") or {}
    if not wb.get("gefunden"):
        z += ["Button auf dieser Seite nicht gefunden (Text stimmt "
              "nicht exakt überein oder er lädt verzögert nach).", ""]
    else:
        z.append("Elternpfad vom Button nach oben, bis zu 6 Ebenen:")
        z.append("")
        for i, e in enumerate(wb.get("elternpfad", [])):
            merkmale = []
            if e.get("id"):
                merkmale.append(f"id=\"{e['id']}\"")
            if e.get("klassen"):
                merkmale.append(f"class=\"{e['klassen']}\"")
            merkmale += e.get("data_attribute") or []
            z.append(f"{i}. `<{e['tag'].lower()}>` "
                     f"{' '.join(merkmale) if merkmale else '(keine Merkmale)'}")
        fremde = wb.get("fremde_skripte") or []
        z += ["", f"**Fremde Skript-Adressen auf der Seite** "
              f"({len(fremde)}, ohne shopify.com/homeeins.de selbst):", ""]
        if fremde:
            z += [f"- `{s}`" for s in fremde]
        else:
            z.append("keine gefunden — der Button stammt dann vermutlich "
                     "aus einem Theme-Abschnitt oder einer Shopify-eigenen "
                     "App (z. B. Shopify Subscriptions), nicht von einem "
                     "externen Anbieter.")
        z.append("")
    if d.get("fehler"):
        z += [f"**Fehlgeschlagen: {d['fehler']}**", ""]
        return "\n".join(z) + "\n"

    z += ["## 1. Erlaubt das Viewport-Meta-Tag Pinch-Zoom?", "",
         f"`{d.get('viewport_meta') or '(kein viewport-Meta-Tag gefunden)'}`",
         ""]

    moeglich = d.get("pinch_zoom_technisch_moeglich")
    z.append(f"**Pinch-Zoom technisch möglich: "
             f"{'ja' if moeglich else 'NEIN — durch das Meta-Tag blockiert'}**")
    if not moeglich:
        z.append("Das Meta-Tag verbietet Skalieren "
                 f"(`user-scalable=no`: {d.get('user_scalable_no')}, "
                 f"`maximum-scale=1`: {d.get('maximum_scale_1')}) — damit "
                 "kann niemand mit den Fingern hineinzoomen, unabhängig "
                 "vom Theme.")
    z.append("")

    z += ["## 2. Öffnet ein Tap auf das Bild eine vergrößerte Ansicht?", ""]
    z.append(f"Bild-Selektor gefunden: `{d.get('bild_selektor', '—')}`")
    z.append(f"**Dialog/Modal nach einfachem Tap geöffnet: "
             f"{'ja' if d.get('dialog_geoeffnet') else 'nein'}**")
    z.append(f"**Dialog/Modal nach Doppeltipp geöffnet: "
             f"{'ja' if d.get('dialog_nach_doppeltipp') else 'nein'}**")
    z.append(f"Seitenzustand hat sich nach dem Tap überhaupt verändert: "
             f"{'ja' if d.get('seite_veraendert') else 'nein'}")
    if d.get("tap_fehler"):
        z.append(f"Tap-Fehler: {d['tap_fehler']}")
    if d.get("doppeltipp_fehler"):
        z.append(f"Doppeltipp-Fehler: {d['doppeltipp_fehler']}")
    z += ["", f"Screenshots: `{d.get('bild_vorher')}`, "
          f"`{d.get('bild_nachher')}`, `{d.get('bild_nach_doppeltipp')}`", ""]

    z += ["## Einordnung", ""]
    if not moeglich:
        z.append("Ergebnis eindeutig: Zoom ist blockiert, bevor die Frage "
                 "nach Dawns eigenem Mechanismus überhaupt relevant wird.")
    elif d.get("dialog_geoeffnet") or d.get("dialog_nach_doppeltipp"):
        z.append("Ein Tap öffnet eine größere Ansicht — Zoom funktioniert "
                 "über Dawns eigenen Mechanismus.")
    else:
        z.append("Weder Tap noch Doppeltipp haben ein Modal geöffnet, und "
                 "das Meta-Tag blockiert nicht. Das ist kein Beweis, dass "
                 "gar kein Zoom existiert — es kann auch ein anderer "
                 "Auslöser sein (z. B. ein eigenes Zoom-Symbol), der hier "
                 "nicht gefunden wurde. Die Screenshots vorher/nachher "
                 "zeigen den tatsächlichen Zustand.")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pfad", required=True)
    ap.add_argument("--bilder", default="bilder")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright
    bilder = Path(a.bilder)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--no-sandbox"])
        d = zoom_pruefen(browser, a.pfad, bilder)
        browser.close()

    Path("daten").mkdir(exist_ok=True)
    Path("daten/zoomprobe.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("ZOOMPROBE.md").write_text(bericht(d), encoding="utf-8")
    print("Bericht in ZOOMPROBE.md")


if __name__ == "__main__":
    main()
