#!/usr/bin/env python3
"""
seiten_check.py — prüft, was Google von homeeins.de ausgeliefert bekommt.

Anlass: Die Search Console zeigt zehn Seiten auf Position 1 bis 5 mit null
Klicks, darunter mehrere unter /en/. Die Stichprobe ergab ein gespaltenes
Bild: Produkt-URLs unter /en/ leiten sauber auf die deutsche Fassung um,
/en/collections/gartenmobel dagegen antwortet mit 200, deklariert
lang="en", zeigt deutschen Text und erklärt sich selbst zur kanonischen
Adresse. Damit konkurriert eine zweite URL mit der echten Seite.

Offen war nur: betrifft das zwei Seiten oder zweihundert? Diese Frage
beantwortet der Sitemap-Modus. Er liest die Sitemap, prüft jede deutsche
Adresse und dazu ihre /en/-Entsprechung und zählt aus, welches Muster wie
oft vorkommt.

Zwei Betriebsarten:
    python3 scripts/seiten_check.py --urls urls.txt          # Stichprobe
    python3 scripts/seiten_check.py --sitemap https://...    # vollständig

Warum das auf dem Runner läuft und nicht hier: Die Arbeitsumgebung erreicht
nur GitHub und PyPI. Der Shop ist von hier aus unsichtbar — unabhängig
davon, welche Bibliothek die Anfrage stellt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

WEITERLEITUNG = (301, 302, 303, 307, 308)

# Attributwert in beliebiger Schreibweise: "wert", 'wert' oder wert.
# Shopify liefert doppelte Anführungszeichen, aber das ist eine Annahme
# über fremdes HTML, die ich von hier aus nicht nachprüfen kann — und eine
# fehlende Canonical-Angabe zu melden, die in Wahrheit nur anders
# geschrieben ist, wäre der teuerste Fehler dieses Skripts.
W = r"""["']?([^"'>\s]+)["']?"""
QC = r"""["']?canonical["']?"""

# Sechs gleichzeitige Abrufe. Shopify verträgt deutlich mehr, aber ein
# vollständiger Lauf über rund 200 Adressen ist damit in gut einer Minute
# durch — schneller zu sein bringt nichts und fällt nur unangenehm auf.
PARALLEL = 6

# Funktionswörter trennen Sprachen zuverlässiger als Inhaltswörter, weil
# Produktnamen oft in beiden Sprachen gleich sind ("Rattan", "Design").
DE = re.compile(r"\b(und|oder|mit|für|nicht|dein|deine|das|die|der|ist|"
                r"auch|bei|aus|wird|kann|sich|mehr)\b", re.I)
EN = re.compile(r"\b(and|or|with|for|not|your|the|is|also|from|will|can|"
                r"more|this|that)\b", re.I)


def holen(url: str, folgen: bool = True):
    """Seite laden. Gibt (Status, Endadresse, HTML) zurück."""
    class Stopp(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    bauer = urllib.request.build_opener(*([] if folgen else [Stopp]))
    anfrage = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "de-DE,de;q=0.9"})
    try:
        with bauer.open(anfrage, timeout=25) as a:
            return a.status, a.url, a.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", url), ""
    except Exception as e:                                    # noqa: BLE001
        return 0, str(e), ""


def kopfdaten(html: str) -> dict:
    def eins(muster):
        t = re.search(muster, html, re.I | re.S)
        return unescape(t.group(1).strip()) if t else ""

    hreflang = [(m.group(1), m.group(2)) for m in re.finditer(
        rf'<link[^>]+hreflang={W}[^>]+href={W}', html, re.I)]
    # Skripte und Stile raus, sonst zählt die Heuristik JavaScript mit.
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    de, en = len(DE.findall(text)), len(EN.findall(text))
    # Schwelle bewusst niedrig: Auf echten Produktseiten liegen die Werte
    # im dreistelligen Bereich. Acht genuegt, um Rauschen auszuschliessen,
    # ohne ein eindeutiges Signal auf duennen Seiten zu verwerfen.
    if de + en < 8:
        sprache = "zu wenig Text"
    else:
        sprache = "Deutsch" if de > en * 1.3 else (
            "Englisch" if en > de * 1.3 else "gemischt")
    return {
        "lang_attribut": eins(rf'<html[^>]+\blang={W}'),
        "titel": eins(r"<title[^>]*>(.*?)</title>"),
        "canonical": eins(rf'<link[^>]+rel={QC}[^>]+href={W}')
                     or eins(rf'<link[^>]+href={W}[^>]+rel={QC}'),
        "hreflang": hreflang,
        "de_woerter": de,
        "en_woerter": en,
        "textsprache": f"{sprache} (de {de} / en {en})",
        "sprache": sprache,
    }


# ---------------------------------------------------------------- Stichprobe

def pruefen(url: str) -> None:
    print(f"\n=== {url} ===")
    status, ziel, _ = holen(url, folgen=False)
    if status in WEITERLEITUNG:
        print(f"  {status} Weiterleitung -> {ziel}")
    status, endziel, html = holen(url)
    print(f"  Status {status}, gelandet bei: {endziel}")
    if not html:
        print("  kein HTML erhalten")
        return
    k = kopfdaten(html)
    print(f"  html lang   : {k['lang_attribut'] or '—'}")
    print(f"  Titel       : {k['titel'][:80]}")
    print(f"  Canonical   : {k['canonical'] or '—'}")
    print(f"  Textsprache : {k['textsprache']}")
    if k["hreflang"]:
        print("  hreflang    :")
        for sp, ziel_url in k["hreflang"][:8]:
            print(f"      {sp:<8} {ziel_url}")
    else:
        print("  hreflang    : keine")


# ------------------------------------------------------------------ Sitemap

def sitemap_lesen(url: str, tiefe: int = 0) -> list[str]:
    """Sitemap oder Sitemap-Index rekursiv auflösen."""
    if tiefe > 3:                       # Schutz vor zirkulären Verweisen
        return []
    status, _, xml = holen(url)
    if status != 200 or not xml:
        print(f"  Sitemap nicht lesbar: {url} (Status {status})",
              file=sys.stderr)
        return []
    try:
        wurzel = ET.fromstring(xml)
    except ET.ParseError as e:
        print(f"  Sitemap unlesbar: {url} ({e})", file=sys.stderr)
        return []

    # Namensraum abstreifen: Shopify liefert sitemaps.org-XML, aber der
    # Präfix ist nicht garantiert. Auf den lokalen Namen zu prüfen ist
    # robuster als ihn fest zu verdrahten.
    def lokal(el):
        return el.tag.rsplit("}", 1)[-1]

    adressen: list[str] = []
    for kind in wurzel:
        name = lokal(kind)
        ort = next((e.text.strip() for e in kind
                    if lokal(e) == "loc" and e.text), None)
        if not ort:
            continue
        if name == "sitemap":
            print(f"  -> Untersitemap {ort}")
            adressen += sitemap_lesen(ort, tiefe + 1)
        elif name == "url":
            adressen.append(ort)
    return adressen


def gattung(url: str) -> str:
    pfad = urlsplit(url).path
    for stueck, name in (("/products/", "Produkte"),
                         ("/collections/", "Kollektionen"),
                         ("/blogs/", "Blog"),
                         ("/pages/", "Seiten")):
        if stueck in pfad:
            return name
    return "Start und Sonstiges"


def en_variante(url: str) -> str:
    """https://host/products/x  ->  https://host/en/products/x"""
    t = urlsplit(url)
    return urlunsplit((t.scheme, t.netloc, "/en" + t.path, t.query, ""))


def ohne_schraegstrich(url: str) -> str:
    t = urlsplit(url)
    return urlunsplit((t.scheme, t.netloc, t.path.rstrip("/"), "", ""))


def abrufen(url: str, ist_en: bool) -> dict:
    """Eine Adresse prüfen. Nur EIN Abruf, ohne Weiterleitungen zu folgen —
    bei einer Weiterleitung interessiert das Ziel, nicht dessen Inhalt."""
    status, ziel, html = holen(url, folgen=False)
    e = {"url": url, "ist_en": ist_en, "status": status, "ziel": ziel,
         "gattung": gattung(url)}
    if status == 200 and html:
        k = kopfdaten(html)
        e["hreflang_anzahl"] = len(k.pop("hreflang"))
        e.update(k)
    e["befund"] = urteil(e)
    return e


def urteil(e: dict) -> str:
    """Kurzurteil. Grossbuchstaben am Anfang = Handlungsbedarf."""
    st = e["status"]
    if st == 0:
        return "nicht erreichbar"
    if st in WEITERLEITUNG:
        return "leitet weiter"
    if st == 404:
        # Unter /en/ ist 404 unschoen, aber harmlos: nichts wird indexiert.
        return "404" if e["ist_en"] else "FEHLER 404 auf deutscher Adresse"
    if st != 200:
        return f"FEHLER HTTP {st}"

    eigen = ohne_schraegstrich(e.get("canonical", "")) == ohne_schraegstrich(e["url"])
    deutsch = e.get("sprache") == "Deutsch"
    lang_en = e.get("lang_attribut", "").lower().startswith("en")

    if e["ist_en"]:
        if eigen and deutsch:
            return "FEHLER deutscher Inhalt unter /en/, kanonisch auf sich selbst"
        if eigen:
            return "WARNUNG /en/ erklaert sich selbst zur kanonischen Adresse"
        if lang_en and deutsch:
            return "WARNUNG lang=en, Text deutsch"
        if not e.get("canonical"):
            return "WARNUNG kein Canonical"
        return "ok (verweist auf die deutsche Fassung)"

    if not e.get("canonical"):
        return "WARNUNG kein Canonical"
    if not eigen:
        return f"WARNUNG Canonical zeigt woanders hin: {e['canonical']}"
    return "ok"


def bericht(daten: dict) -> str:
    eintraege = daten["eintraege"]
    en = [e for e in eintraege if e["ist_en"]]
    de = [e for e in eintraege if not e["ist_en"]]
    kaputt = [e for e in en if e["befund"].startswith("FEHLER")]
    warn = [e for e in en if e["befund"].startswith("WARNUNG")]
    de_prob = [e for e in de if not e["befund"].startswith("ok")]

    z = ["# Seitenprüfung — homeeins.de", "",
         f"Stand: {daten['stand']} · Quelle: {daten['sitemap']}", "",
         f"{len(de)} deutsche Adressen aus der Sitemap, dazu je die "
         f"/en/-Entsprechung geprüft ({len(eintraege)} Abrufe).", ""]

    if kaputt:
        n = len(kaputt)
        z += [f"## {n} /en/-{'Adresse' if n == 1 else 'Adressen'} "
              f"{'konkurriert' if n == 1 else 'konkurrieren'} mit der "
              f"deutschen Seite", "",
              "Diese Adressen antworten mit 200, zeigen deutschen Text "
              "und erklären sich **selbst** zur kanonischen Adresse. Damit "
              "sieht Google zwei gleichwertige Seiten mit demselben Inhalt "
              "und muss raten, welche gemeint ist.", ""]
        for e in sorted(kaputt, key=lambda x: x["url"]):
            z.append(f"- `{urlsplit(e['url']).path}` — {e.get('titel','')[:70]}")
        z.append("")
    else:
        z += ["## Keine selbstkanonischen /en/-Seiten gefunden", "",
              "Alle geprüften /en/-Adressen leiten weiter, laufen ins 404 "
              "oder verweisen kanonisch auf die deutsche Fassung.", ""]

    if warn:
        z += [f"## {len(warn)} weitere /en/-Auffälligkeiten", ""]
        for e in sorted(warn, key=lambda x: x["url"])[:40]:
            z.append(f"- `{urlsplit(e['url']).path}` — {e['befund']}")
        if len(warn) > 40:
            z.append(f"- … und {len(warn) - 40} weitere")
        z.append("")

    if de_prob:
        z += [f"## {len(de_prob)} Auffälligkeiten auf deutschen Adressen", ""]
        for e in sorted(de_prob, key=lambda x: x["url"])[:40]:
            z.append(f"- `{urlsplit(e['url']).path}` — {e['befund']}")
        if len(de_prob) > 40:
            z.append(f"- … und {len(de_prob) - 40} weitere")
        z.append("")

    z += ["## Verteilung nach Gattung", "",
          "| Gattung | deutsch | /en/ leitet weiter | /en/ 404 | /en/ Problem |",
          "|---|---:|---:|---:|---:|"]
    for g in sorted({e["gattung"] for e in eintraege}):
        d = sum(1 for e in de if e["gattung"] == g)
        w = sum(1 for e in en if e["gattung"] == g
                and e["befund"] == "leitet weiter")
        v = sum(1 for e in en if e["gattung"] == g and e["befund"] == "404")
        p = sum(1 for e in en if e["gattung"] == g
                and e["befund"].startswith(("FEHLER", "WARNUNG")))
        z.append(f"| {g} | {d} | {w} | {v} | {p} |")
    z.append("")

    z += ["## Alle Befunde gezählt", "",
          "| Befund | Anzahl |", "|---|---:|"]
    for befund, n in Counter(e["befund"] for e in eintraege).most_common():
        z.append(f"| {befund} | {n} |")
    return "\n".join(z) + "\n"


def crawl(sitemap: str, limit: int, out: Path) -> int:
    print(f"Sitemap lesen: {sitemap}")
    roh = sitemap_lesen(sitemap)
    # Adressen, die die Sitemap schon selbst unter /en/ führt, kämen sonst
    # doppelt vor — einmal als Fund, einmal als abgeleitete Variante.
    deutsch = sorted({u for u in roh if "/en/" not in urlsplit(u).path})
    if not deutsch:
        sys.exit("Sitemap enthielt keine brauchbaren Adressen.")
    if limit:
        deutsch = deutsch[:limit]
    print(f"{len(roh)} Adressen in der Sitemap, {len(deutsch)} deutsche "
          f"werden geprüft (dazu je die /en/-Fassung)")

    auftraege = [(u, False) for u in deutsch] + \
                [(en_variante(u), True) for u in deutsch]

    eintraege: list[dict] = []
    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        for i, e in enumerate(pool.map(lambda a: abrufen(*a), auftraege), 1):
            eintraege.append(e)
            if i % 25 == 0 or i == len(auftraege):
                print(f"  {i}/{len(auftraege)} abgerufen")

    daten = {"stand": str(date.today()), "sitemap": sitemap,
             "eintraege": eintraege}
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    (out / f"seiten-{daten['stand']}.json").write_text(text, encoding="utf-8")
    (out / "seiten-aktuell.json").write_text(text, encoding="utf-8")
    Path("SEITEN.md").write_text(bericht(daten), encoding="utf-8")

    kaputt = [e for e in eintraege
              if e["ist_en"] and e["befund"].startswith("FEHLER")]
    print(f"\nFertig. {len(kaputt)} /en/-Adressen konkurrieren mit ihrer "
          f"deutschen Fassung. Bericht in SEITEN.md")
    # Bewusst kein Abbruch: Der Befund ist das Ergebnis, kein Fehlschlag.
    # Ein roter Lauf würde die Zahl verstecken, statt sie zu zeigen.
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", help="Datei mit einer URL je Zeile (Stichprobe)")
    ap.add_argument("--sitemap", help="Sitemap-Adresse (vollständiger Lauf)")
    ap.add_argument("--out", default="daten")
    ap.add_argument("--limit", type=int, default=0,
                    help="nur die ersten N Adressen (zum Ausprobieren)")
    a = ap.parse_args()

    if a.sitemap:
        sys.exit(crawl(a.sitemap, a.limit, Path(a.out)))

    if not a.urls:
        sys.exit("Entweder --urls oder --sitemap angeben.")
    zeilen = [z.strip() for z in open(a.urls, encoding="utf-8")
              if z.strip() and not z.startswith("#")]
    if not zeilen:
        sys.exit("Keine URLs angegeben")
    for u in zeilen:
        pruefen(u)
    print(f"\n{len(zeilen)} URLs geprüft")


if __name__ == "__main__":
    main()
