#!/usr/bin/env python3
"""
seiten_check.py — prüft URLs des Shops auf das, was Google sieht.

Anlass: Die Search Console zeigt zehn Seiten auf Position 1 bis 5 mit null
Klicks, darunter mehrere unter /en/. Ob dort Englisch oder Deutsch steht,
welche URL sich als kanonisch bezeichnet und was hreflang behauptet, lässt
sich nur am ausgelieferten HTML feststellen — nicht in der Admin-API.

Geprüft wird je URL:
  - Status und Weiterleitungskette
  - <html lang>, <title>, Canonical, hreflang
  - Sprache des Fließtextes (Heuristik über Funktionswörter)

Aufruf:
    python3 scripts/seiten_check.py --urls urls.txt
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from html import unescape

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

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

    bauer = urllib.request.build_opener(
        *( [] if folgen else [Stopp] ))
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
        r'<link[^>]+hreflang="([^"]+)"[^>]+href="([^"]+)"', html, re.I)]
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
        "lang_attribut": eins(r'<html[^>]+lang="([^"]+)"'),
        "titel": eins(r"<title[^>]*>(.*?)</title>"),
        "canonical": eins(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"'),
        "hreflang": hreflang,
        "textsprache": f"{sprache} (de {de} / en {en})",
    }


def pruefen(url: str) -> None:
    print(f"\n=== {url} ===")
    status, ziel, _ = holen(url, folgen=False)
    if status in (301, 302, 303, 307, 308):
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", required=True,
                    help="Datei mit einer URL je Zeile")
    a = ap.parse_args()
    zeilen = [z.strip() for z in open(a.urls, encoding="utf-8")
              if z.strip() and not z.startswith("#")]
    if not zeilen:
        sys.exit("Keine URLs angegeben")
    for u in zeilen:
        pruefen(u)
    print(f"\n{len(zeilen)} URLs geprüft")


if __name__ == "__main__":
    main()
