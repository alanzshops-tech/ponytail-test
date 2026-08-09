#!/usr/bin/env python3
"""
kaufprobe.py — zwei Fragen, die man nur im Browser beantworten kann.

1. Sieht die umgebaute Startseite (Theme-Kopie) richtig aus, oder habe
   ich beim Kürzen etwas zerschossen?
2. Kann ein Kunde bei Homeeins tatsächlich einkaufen — Produktseite,
   In-den-Warenkorb, Warenkorb, Kasse?

Zu 2: Der Lauf legt Ware in den Korb und ruft die Kasse auf. Er bezahlt
nichts und schließt nichts ab. Es entsteht ein abgebrochener Warenkorb
im Shopify-Adminbereich, sonst nichts. Als Adresse wird eine erkennbare
Testadresse verwendet, als E-Mail eine Adresse auf example.com — diese
Domain ist genau dafür reserviert und nimmt keine Post an.

Warum überhaupt: Der Shop hat 2026 null Bestellungen. Dafür gibt es zwei
mögliche Gründe — niemand kommt, oder niemand kann. Das sind völlig
verschiedene Probleme, und man unterscheidet sie nur, indem man es
selbst versucht.

Aufruf:
    python3 scripts/kaufprobe.py --theme 182664626499
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SHOP = "https://www.homeeins.de"

# Produkte für die Probe. Eines aus dem Bestand, eines von den beiden,
# die ich selbst angelegt habe — bei denen hatte ich schon einmal
# unverkäufliche Varianten übersehen.
PRODUKTE = [
    ("bestand", "/products/vorratsbehaelter-luftdicht-schwarz"),
    ("selbst",  "/products/led-taschenlampe-aufladbar-zoom-warnlicht"),
]

TESTADRESSE = {
    "email": "kaufprobe-test@example.com",
    "firstName": "Test",
    "lastName": "Kaufprobe",
    "address1": "Musterstraße 1",
    "postalCode": "10115",
    "city": "Berlin",
}

# Wonach in der Kasse gesucht wird. Die FAQ, die ich geschrieben habe,
# nennt sechs Zahlarten — diese Liste prüft, ob das stimmt.
#
# „Rechnung" stand hier schon einmal und war ein Fehlalarm: Die Kasse
# enthält die Zeile „Lieferadresse als Rechnungsadresse verwenden".
# Genau derselbe Fehler wie neulich mit „Ausverkauft". Deshalb jetzt
# Wortgrenzen und ein ausdrücklicher Ausschluss.
ZAHLARTEN = ["PayPal", "Klarna", "Apple Pay", "Google Pay", "Shop Pay",
             "Kreditkarte", "Visa", "Mastercard", "SEPA", "Lastschrift",
             "Sofort", "Amazon Pay", "Nachnahme", "Vorkasse",
             "Banküberweisung", "iDEAL", "Bancontact",
             r"Rechnung(?!sadresse)"]


def zahlarten_finden(text: str) -> list[str]:
    return [z.split("(")[0] for z in ZAHLARTEN
            if re.search(rf"\b{z}", text)]

# Namen, die aus der Startseite verschwinden mussten.
ERFUNDEN = ["Anna M.", "Thomas B.", "Sarah K.", "Michael S.", "Laura F.",
            "Jan W.", "Elena N.", "Markus L.", "Sophie R.", "Peter H.",
            "David K.", "Zufriedene Kundinnen", "14-Tage"]

GERAETE = {
    "mobil":   {"viewport": {"width": 390, "height": 844},
                "device_scale_factor": 2, "is_mobile": True,
                "has_touch": True},
    "desktop": {"viewport": {"width": 1440, "height": 900},
                "device_scale_factor": 1, "is_mobile": False},
}


def foto(seite, ziel: Path, ganz: bool = True) -> int:
    ziel.parent.mkdir(parents=True, exist_ok=True)
    seite.screenshot(path=str(ziel), full_page=ganz, type="jpeg", quality=72)
    return round(ziel.stat().st_size / 1024)


# ---------------------------------------------------------------- Teil 1

def vorschau_pruefen(browser, theme_id: str, bilder: Path) -> dict:
    """Die Theme-Kopie ansehen. Erst ein Bild beweist, dass eine
    Vorlage nicht nur gültiges JSON ist, sondern auch etwas anzeigt."""
    url = f"{SHOP}/?preview_theme_id={theme_id}"
    ergebnis: dict = {"url": url, "theme_id": theme_id}

    for geraet in GERAETE:
        ctx = browser.new_context(locale="de-DE", **GERAETE[geraet])
        seite = ctx.new_page()
        fehlerhaft: list[str] = []
        seite.on("response", lambda r: fehlerhaft.append(f"{r.status} {r.url[:110]}")
                 if r.status >= 400 else None)
        try:
            seite.goto(url, wait_until="load", timeout=60000)
            seite.wait_for_timeout(3500)
        except Exception as e:                                   # noqa: BLE001
            ergebnis[f"{geraet}_fehler"] = str(e)[:200]
            ctx.close()
            continue

        text = seite.inner_text("body")
        ergebnis[f"{geraet}_bild"] = str(bilder / f"vorschau-{geraet}.jpg")
        ergebnis[f"{geraet}_bild_kb"] = foto(
            seite, bilder / f"vorschau-{geraet}.jpg")
        ergebnis[f"{geraet}_hoehe"] = seite.evaluate(
            "() => Math.round(document.body.scrollHeight)")
        ergebnis[f"{geraet}_querscroll"] = seite.evaluate(
            "() => document.documentElement.scrollWidth > window.innerWidth + 2")
        ergebnis[f"{geraet}_fehlerhafte_anfragen"] = fehlerhaft[:10]

        if geraet == "mobil":
            ergebnis["gefundene_faelschungen"] = [
                n for n in ERFUNDEN if n in text]
            # Bilder, die zwar im HTML stehen, aber nicht geladen haben —
            # der häufigste Schaden nach einem Umbau.
            ergebnis["bilder_kaputt"] = seite.evaluate("""() =>
              [...document.images]
                .filter(i => i.complete && i.naturalWidth === 0)
                .map(i => (i.currentSrc || i.src || '').slice(0, 110))
                .slice(0, 10)""")
            ergebnis["bilder_gesamt"] = seite.evaluate(
                "() => document.images.length")
            # Erwartete Bausteine. Fehlt einer, ist beim Kürzen etwas
            # verlorengegangen.
            for name, muster in [
                    ("banner", "Mach Schluss mit Chaos"),
                    ("vertrauenszeile", "Kostenlose Lieferung"),
                    ("bestseller", "Bestseller"),
                    ("zahlungslogos", "Sicher bezahlen mit"),
                    ("kategorien", "Kategorien"),
                    ("faq", "Häufige Fragen")]:
                ergebnis[f"hat_{name}"] = muster in text
            # Nur innerhalb der Bestseller-Reihe zählen. Der erste Lauf
            # zählte über die ganze Seite und meldete 28 Kacheln, wo acht
            # eingestellt sind — die Karussell- und Kategoriekacheln waren
            # mitgezählt. Eine Zahl ohne Bezugsrahmen ist keine Messung.
            ergebnis["produktkacheln"] = seite.evaluate(
                """() => {
                  const s = document.querySelector(
                    '#shopify-section-featured_collection');
                  return s ? s.querySelectorAll('.card__heading').length : -1;
                }""")
            # Das Karussell oben und die Kategoriekacheln unten zeigen
            # womöglich dasselbe. Zweimal dieselbe Navigation auf einer
            # Seite kostet Platz — aber erst die Zählung entscheidet das,
            # nicht mein Eindruck vom Screenshot.
            ergebnis["karussell"] = seite.evaluate("""() => {
              const s = document.querySelector(
                '#shopify-section-175490368314e073b7');
              if (!s) return null;
              return [...new Set([...s.querySelectorAll('a')]
                .map(a => (a.innerText || a.title || '').trim())
                .filter(Boolean))];
            }""")
            ergebnis["kategoriekacheln"] = seite.evaluate("""() => {
              const s = document.querySelector(
                '#shopify-section-collection_list_Xm8GYP');
              if (!s) return null;
              return [...new Set([...s.querySelectorAll('a')]
                .map(a => (a.innerText || '').trim()).filter(Boolean))];
            }""")

            ergebnis["leere_abschnitte"] = seite.evaluate("""() =>
              [...document.querySelectorAll('.shopify-section')]
                .filter(s => s.innerText.trim().length === 0 &&
                             s.querySelectorAll('img,svg,video').length === 0)
                .map(s => s.id || '(ohne id)')""")
        ctx.close()
    return ergebnis


# ---------------------------------------------------------------- Teil 2

def in_den_korb(seite) -> tuple[bool, str]:
    """Den Kaufknopf drücken wie ein Kunde. Mehrere Bauweisen, weil
    Themes den Knopf unterschiedlich benennen."""
    for wahl in ["product-form button[name='add']",
                 "form[action*='/cart/add'] button[type='submit']",
                 "button[name='add']",
                 ".product-form__submit"]:
        knopf = seite.locator(wahl).first
        try:
            if knopf.count() == 0 or not knopf.is_visible():
                continue
            if knopf.is_disabled():
                return False, f"Knopf '{wahl}' ist ausgegraut"
            knopf.click(timeout=15000)
            seite.wait_for_timeout(3500)
            return True, wahl
        except Exception as e:                                   # noqa: BLE001
            return False, f"{wahl}: {str(e)[:120]}"
    return False, "kein Kaufknopf gefunden"


def korb_inhalt(seite) -> dict:
    """Der Warenkorb aus Shopifys eigener Schnittstelle, nicht aus dem
    Seitentext geraten."""
    return seite.evaluate("""async () => {
      const r = await fetch('/cart.js', {headers: {'Accept': 'application/json'}});
      const c = await r.json();
      return {anzahl: c.item_count, summe: c.total_price, waehrung: c.currency,
              posten: (c.items || []).map(i => i.title + ' ×' + i.quantity)};
    }""")


def produkt_probe(browser, pfad: str, marke: str, bilder: Path) -> dict:
    ctx = browser.new_context(locale="de-DE", **GERAETE["mobil"])
    seite = ctx.new_page()
    p: dict = {"pfad": pfad, "herkunft": marke}
    try:
        antwort = seite.goto(SHOP + pfad, wait_until="load", timeout=60000)
        p["status"] = antwort.status if antwort else 0
        seite.wait_for_timeout(2500)
        text = seite.inner_text("body")
        p["ausverkauft_sichtbar"] = bool(
            re.search(r"\bAusverkauft\b|\bNicht verfügbar\b", text))
        p["preis_sichtbar"] = bool(re.search(r"\d+[,.]\d{2}\s*€|€\s*\d+", text))
        p["mwst_hinweis"] = "MwSt" in text or "Mwst" in text
        p["bild_produktseite"] = str(bilder / f"kauf-1-produkt-{marke}.jpg")
        foto(seite, bilder / f"kauf-1-produkt-{marke}.jpg")

        p["geklickt"], p["knopf"] = in_den_korb(seite)
        p["korb_nach_klick"] = korb_inhalt(seite)

        seite.goto(SHOP + "/cart", wait_until="load", timeout=60000)
        seite.wait_for_timeout(2000)
        p["bild_warenkorb"] = str(bilder / f"kauf-2-korb-{marke}.jpg")
        foto(seite, bilder / f"kauf-2-korb-{marke}.jpg")
        korbtext = seite.inner_text("body")
        p["korb_leer_text"] = ("leer" in korbtext.lower()[:2000])
        p["kasse_knopf"] = seite.locator(
            "button[name='checkout'], input[name='checkout'], "
            "a[href*='/checkout']").count()
    except Exception as e:                                       # noqa: BLE001
        p["fehler"] = str(e)[:250]
    ctx.close()
    return p


def kasse_probe(browser, pfad: str, bilder: Path) -> dict:
    """Bis zur Bezahlseite, nicht weiter. Hier zeigt sich, ob ein
    Versandtarif greift und welche Zahlarten wirklich angeboten werden."""
    ctx = browser.new_context(locale="de-DE", **GERAETE["mobil"])
    seite = ctx.new_page()
    k: dict = {}
    try:
        seite.goto(SHOP + pfad, wait_until="load", timeout=60000)
        seite.wait_for_timeout(2000)
        in_den_korb(seite)
        k["korb"] = korb_inhalt(seite)

        antwort = seite.goto(SHOP + "/checkout", wait_until="load",
                             timeout=60000)
        k["status"] = antwort.status if antwort else 0
        k["url"] = seite.url
        seite.wait_for_timeout(4000)
        k["bild_kasse_leer"] = str(bilder / "kauf-3-kasse.jpg")
        foto(seite, bilder / "kauf-3-kasse.jpg")

        text = seite.inner_text("body")
        k["zahlarten_vor_adresse"] = zahlarten_finden(text)
        k["erreichbar"] = "checkout" in seite.url or "Bezahlen" in text

        # ZUERST das Land. Der erste Lauf lief vom Runner aus, also aus den
        # USA — die Kasse stand auf „Vereinigte Staaten", rechnete
        # Auslandsversand und zeigte womöglich andere Zahlarten. Wer den
        # deutschen Kaufweg prüfen will, muss Deutschland einstellen.
        k["land_vorher"] = seite.evaluate(
            """() => { const s = document.querySelector(
                 "select[name='countryCode']"); return s ? s.value : null; }""")
        try:
            seite.select_option("select[name='countryCode']", "DE",
                                timeout=10000)
            seite.wait_for_timeout(4000)
            k["land_gesetzt"] = "DE"
        except Exception as e:                                   # noqa: BLE001
            k["land_gesetzt"] = f"fehlgeschlagen: {str(e)[:110]}"

        # Testadresse eintragen, damit Versand und Zahlung berechnet werden.
        gefuellt = []
        for feld, wert in TESTADRESSE.items():
            for wahl in (f"input[name='{feld}']", f"input#{feld}"):
                el = seite.locator(wahl).first
                try:
                    if el.count() and el.is_visible():
                        el.fill(wert, timeout=8000)
                        gefuellt.append(feld)
                        break
                except Exception:                                # noqa: BLE001
                    continue
        k["felder_gefuellt"] = gefuellt
        seite.wait_for_timeout(6000)

        text2 = seite.inner_text("body")
        k["zahlarten_nach_adresse"] = zahlarten_finden(text2)
        # Der Zahlungsabschnitt für sich, damit die Namen aus der Liste
        # stammen und nicht aus irgendeinem Fließtext daneben.
        k["zahlungsabschnitt"] = seite.evaluate("""() => {
          const abschnitte = [...document.querySelectorAll('section, div')]
            .filter(e => /^Zahlung\\b/.test(e.innerText || ''));
          if (!abschnitte.length) return null;
          const e = abschnitte[abschnitte.length - 1];
          return (e.innerText || '').slice(0, 900);
        }""")
        k["gesamt"] = seite.evaluate("""() => {
          const m = (document.body.innerText || '')
            .match(/Gesamt[\\s\\S]{0,80}?([\\d.]+,\\d{2}\\s*€)/);
          return m ? m[1] : null;
        }""")
        k["versandhinweis"] = [
            z.strip() for z in text2.splitlines()
            if re.search(r"Versand|Lieferung|Kostenlos", z)][:6]
        k["fehlermeldungen"] = [
            z.strip() for z in text2.splitlines()
            if re.search(r"nicht verfügbar|nicht möglich|Fehler|"
                         r"keine Versandart|liefern wir nicht", z, re.I)][:8]
        k["bezahlknopf"] = seite.locator(
            "button#checkout-pay-button, button[type='submit']").count()
        k["bild_kasse_gefuellt"] = str(bilder / "kauf-4-kasse-adresse.jpg")
        foto(seite, bilder / "kauf-4-kasse-adresse.jpg")
    except Exception as e:                                       # noqa: BLE001
        k["fehler"] = str(e)[:250]
    ctx.close()
    return k


# ---------------------------------------------------------------- Bericht

def bericht(d: dict) -> str:
    v = d["vorschau"]
    z = ["# Kaufprobe und Sichtprüfung", "",
         f"Stand: {d['stand']}", "",
         "Zwei Fragen, beide nur im Browser beantwortbar: Sieht die "
         "umgebaute Startseite richtig aus, und kann man einkaufen?", "",
         "## 1. Die Theme-Kopie", "",
         f"Vorschau: `{v['url']}`", ""]

    faelsch = v.get("gefundene_faelschungen", [])
    z.append(f"- Erfundene Bewertungen im sichtbaren Text: "
             f"**{'noch da: ' + ', '.join(faelsch) if faelsch else 'keine'}**")
    for name, beschr in [("banner", "Banner mit Überschrift"),
                         ("vertrauenszeile", "Vertrauenszeile"),
                         ("bestseller", "Bestseller-Reihe"),
                         ("zahlungslogos", "Zahlungslogos"),
                         ("kategorien", "Kategoriekacheln"),
                         ("faq", "FAQ")]:
        z.append(f"- {beschr}: {'ja' if v.get(f'hat_{name}') else '**FEHLT**'}")
    z += [f"- Produktkacheln gezählt: {v.get('produktkacheln', '?')}",
          f"- Bilder auf der Seite: {v.get('bilder_gesamt', '?')}, "
          f"davon nicht geladen: "
          f"{len(v.get('bilder_kaputt', [])) or 'keine'}"]
    for b in v.get("bilder_kaputt", []):
        z.append(f"    - kaputt: {b}")
    for g in ("mobil", "desktop"):
        z.append(f"- {g}: {v.get(f'{g}_hoehe', '?')} px hoch, Querscroll "
                 f"{'JA' if v.get(f'{g}_querscroll') else 'nein'}")
    kar = v.get("karussell") or []
    kat = v.get("kategoriekacheln") or []
    doppelt = sorted(set(kar) & set(kat))
    z += [f"- Karussell oben: {', '.join(kar) or '–'}",
          f"- Kategoriekacheln unten: {', '.join(kat) or '–'}",
          f"- **Doppelt auf einer Seite: "
          f"{', '.join(doppelt) if doppelt else 'nichts'}**"]
    leer = v.get("leere_abschnitte", [])
    z.append(f"- Leere Abschnitte: {', '.join(leer) if leer else 'keine'}")
    for g in ("mobil", "desktop"):
        for f in v.get(f"{g}_fehlerhafte_anfragen", []):
            z.append(f"- Fehlerhafte Anfrage ({g}): {f}")
    z += ["", f"Bilder: `{v.get('mobil_bild')}`, `{v.get('desktop_bild')}`", ""]

    z += ["## 2. Kann man einkaufen?", ""]
    for p in d["produkte"]:
        z += [f"### `{p['pfad']}` ({p['herkunft']})", ""]
        if p.get("fehler"):
            z += [f"- FEHLER: {p['fehler']}", ""]
            continue
        korb = p.get("korb_nach_klick", {})
        z += [f"- Seite geladen: HTTP {p.get('status')}",
              f"- Preis sichtbar: {'ja' if p.get('preis_sichtbar') else '**nein**'}"
              f", MwSt-Hinweis: {'ja' if p.get('mwst_hinweis') else '**nein**'}",
              f"- „Ausverkauft\" sichtbar: "
              f"{'ja' if p.get('ausverkauft_sichtbar') else 'nein'}",
              f"- Kaufknopf gedrückt: "
              f"{'ja (' + str(p.get('knopf')) + ')' if p.get('geklickt') else '**nein — ' + str(p.get('knopf')) + '**'}",
              f"- Warenkorb danach: **{korb.get('anzahl', '?')} Artikel**, "
              f"{(korb.get('summe') or 0) / 100:.2f} {korb.get('waehrung', '')}",
              f"- Posten: {', '.join(korb.get('posten', [])) or '–'}",
              f"- Kasse-Knopf im Warenkorb: {p.get('kasse_knopf', 0)}", ""]

    k = d["kasse"]
    z += ["### Die Kasse", ""]
    if k.get("fehler"):
        z += [f"- FEHLER: {k['fehler']}", ""]
    else:
        z += [f"- Kasse erreichbar: "
              f"{'**ja**' if k.get('erreichbar') else '**NEIN**'} "
              f"(HTTP {k.get('status')})",
              f"- Land voreingestellt: `{k.get('land_vorher')}`, "
              f"umgestellt auf: `{k.get('land_gesetzt')}`",
              f"- Adresse: {', '.join(k.get('felder_gefuellt', [])) or 'keine Felder gefunden'}",
              f"- Gesamtpreis in der Kasse: **{k.get('gesamt') or '?'}**",
              f"- Zahlarten vor Adresseingabe: "
              f"{', '.join(k.get('zahlarten_vor_adresse', [])) or '–'}",
              f"- Zahlarten nach Adresseingabe: "
              f"**{', '.join(k.get('zahlarten_nach_adresse', [])) or 'keine erkannt'}**"]
        for f in k.get("fehlermeldungen", []):
            z.append(f"- Meldung in der Kasse: „{f}\"")
        for s in k.get("versandhinweis", []):
            z.append(f"- Versandzeile: „{s}\"")
        if k.get("zahlungsabschnitt"):
            z += ["", "Der Zahlungsabschnitt im Wortlaut:", "",
                  "```", k["zahlungsabschnitt"].strip(), "```"]
        z += ["", "Es wurde nichts bezahlt und nichts bestellt. Im "
              "Adminbereich erscheint ein abgebrochener Warenkorb auf "
              f"`{TESTADRESSE['email']}` — das ist der Beleg des Tests.", ""]
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", required=True, help="ID der Theme-Kopie")
    ap.add_argument("--bilder", default="bilder")
    a = ap.parse_args()

    from playwright.sync_api import sync_playwright
    bilder = Path(a.bilder)
    d = {"stand": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--no-sandbox"])
        print("Theme-Vorschau …")
        d["vorschau"] = vorschau_pruefen(browser, a.theme, bilder)
        d["produkte"] = []
        for marke, pfad in PRODUKTE:
            print(f"Kaufprobe {pfad} …")
            d["produkte"].append(produkt_probe(browser, pfad, marke, bilder))
        print("Kasse …")
        d["kasse"] = kasse_probe(browser, PRODUKTE[0][1], bilder)
        browser.close()

    Path("daten").mkdir(exist_ok=True)
    Path("daten/kaufprobe.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("KAUFPROBE.md").write_text(bericht(d), encoding="utf-8")
    print("\nBericht in KAUFPROBE.md")


if __name__ == "__main__":
    main()
