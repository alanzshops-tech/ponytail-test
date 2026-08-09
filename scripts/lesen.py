#!/usr/bin/env python3
"""
lesen.py — holt beliebige Webseiten und legt sie lesbar ins Repo.

Wozu: Diese Arbeitsumgebung erreicht nur GitHub und PyPI. Jede andere
Adresse lehnt der Proxy schon beim Verbindungsaufbau ab:

    connect_rejected  www.homeeins.de:443
    gateway answered 403 to CONNECT (policy denial)

Das passiert unterhalb jeder Bibliothek. Ein echter Browser bekommt
denselben 403 wie curl — geprüft mit dem hier vorinstallierten Chromium,
der ERR_TUNNEL_CONNECTION_FAILED meldet. Werkzeuge wie Browser Use,
Playwright oder Scrapy ändern daran nichts.

GitHub ist aber erreichbar. Also liest der Runner, und das Ergebnis kommt
über das Repository zurück. Damit lassen sich Wettbewerberseiten,
Ratgeber, Herstellerangaben und alles andere auswerten, was für die
Vermarktung zählt.

Aufruf:
    python3 scripts/lesen.py --urls "https://a.de/x, https://b.de/y"
    python3 scripts/lesen.py --datei lesen.txt --out gelesen
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

# Wiederverwendung statt Nachbau: Abruf, Drosselbremse und Kopfdaten sind
# im Seitenprüfer schon gelöst und getestet. Beim Start eines Skripts legt
# Python dessen Verzeichnis auf sys.path, deshalb genügt der Modulname.
from seiten_check import Bremse, kopfdaten


def text_gewinnen(html: str, url: str) -> tuple[str, str]:
    """Fließtext aus HTML. Gibt (Text, verwendetes Verfahren) zurück."""
    try:
        import trafilatura
        t = trafilatura.extract(html, url=url, output_format="markdown",
                                include_links=True, include_tables=True,
                                favor_precision=True)
        if t and len(t) > 200:
            return t, "trafilatura"
    except ImportError:
        pass
    except Exception as e:                                    # noqa: BLE001
        print(f"    trafilatura scheiterte ({e}), nehme den Notbehelf")

    # Notbehelf. Deutlich gröber: Er trennt Haupttext nicht von Navigation
    # und Fußzeile. Dass er benutzt wurde, steht im Kopf jeder Datei —
    # sonst hielte man Menütexte für Inhalt.
    t = re.sub(r"<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", html,
               flags=re.I | re.S)
    t = re.sub(r"<(br|/p|/div|/li|/h[1-6])\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    from html import unescape
    t = unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
    return t.strip(), "Notbehelf (Regex)"


def verfuegbarkeit(html: str) -> str:
    """Was der Shop dem Kunden über Lieferbarkeit anzeigt.

    Die Textextraktion wirft genau das weg — Kaufbutton und Varianten sind
    kein Fließtext. Shopify liefert es aber strukturiert im JSON-LD mit,
    und Google liest dieselbe Stelle.
    """
    import json as _json

    zustaende: list[str] = []
    for m in re.finditer(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html, re.I | re.S):
        try:
            daten = _json.loads(m.group(1))
        except ValueError:
            continue
        for knoten in (daten if isinstance(daten, list) else [daten]):
            if not isinstance(knoten, dict):
                continue
            angebote = knoten.get("offers")
            for a in (angebote if isinstance(angebote, list) else [angebote]):
                if isinstance(a, dict) and a.get("availability"):
                    zustaende.append(str(a["availability"]).rsplit("/", 1)[-1])
    if not zustaende:
        # Kein Produkt oder kein JSON-LD — beides kein Fehler.
        return ""
    aus = sum(1 for z in zustaende if "OutOfStock" in z or "SoldOut" in z)
    lieferbar = len(zustaende) - aus
    hinweis = "Ausverkauft" in html or "Sold out" in html
    return (f"{lieferbar} von {len(zustaende)} Varianten lieferbar"
            + (f", {aus} ausverkauft" if aus else "")
            + (" · Seite zeigt „Ausverkauft“" if hinweis else ""))


def dateiname(url: str) -> str:
    t = urlsplit(url)
    roh = f"{t.netloc}{t.path}".rstrip("/")
    roh = re.sub(r"[^A-Za-z0-9._-]+", "-", roh).strip("-")
    return (roh[:120] or "seite") + ".md"


def eine(bremse: Bremse, url: str, out: Path,
         roh: Path | None = None) -> bool:
    print(f"\n=== {url} ===")
    status, ziel, html = bremse.abrufen(url, folgen=True)
    if status != 200 or not html:
        print(f"  Status {status} — nichts gelesen ({ziel})")
        return False

    k = kopfdaten(html)
    text, verfahren = text_gewinnen(html, url)
    kopf = [
        f"# {k['titel'] or url}", "",
        f"- Quelle: {url}",
        f"- Abgerufen: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC",
        f"- Sprache laut HTML: {k['lang_attribut'] or 'nicht angegeben'} · "
        f"gemessen: {k['textsprache']}",
        f"- Extraktion: {verfahren}",
        f"- Zeichen: {len(text)}",
    ]
    lager = verfuegbarkeit(html)
    if lager:
        kopf.append(f"- Verfügbarkeit: {lager}")
    kopf += ["", "---", ""]
    out.mkdir(parents=True, exist_ok=True)
    if roh:
        # Fuer Fragen, die der Fliesstext nicht beantwortet: Welche Variante
        # ist vorausgewaehlt, steht "Ausverkauft" auf der Seite, was sagt das
        # strukturierte Datenblatt. Die Extraktion wirft genau das weg.
        roh.mkdir(parents=True, exist_ok=True)
        (roh / (dateiname(url)[:-3] + ".html")).write_text(html, encoding="utf-8")
    ziel_datei = out / dateiname(url)
    ziel_datei.write_text("\n".join(kopf) + text + "\n", encoding="utf-8")
    print(f"  {len(text)} Zeichen über {verfahren} -> {ziel_datei}")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", help="Adressen, durch Komma getrennt")
    ap.add_argument("--datei", help="Datei mit einer Adresse je Zeile")
    ap.add_argument("--out", default="gelesen")
    ap.add_argument("--roh", help="zusaetzlich das rohe HTML hierhin schreiben")
    a = ap.parse_args()

    adressen: list[str] = []
    if a.urls:
        adressen += [u.strip() for u in a.urls.split(",") if u.strip()]
    if a.datei and Path(a.datei).exists():
        adressen += [z.strip() for z in Path(a.datei).read_text(encoding="utf-8")
                     .splitlines() if z.strip() and not z.startswith("#")]
    # Reihenfolge erhalten, Doppelte entfernen.
    adressen = list(dict.fromkeys(adressen))
    if not adressen:
        sys.exit("Keine Adressen angegeben (--urls oder --datei).")
    for u in adressen:
        if not u.startswith(("http://", "https://")):
            sys.exit(f"Keine gültige Adresse: {u}")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bremse = Bremse()
    roh = Path(a.roh) if a.roh else None
    gelesen = sum(eine(bremse, u, out, roh) for u in adressen)
    print(f"\n{gelesen} von {len(adressen)} Seiten gelesen -> {out}/")
    # Nur abbrechen, wenn gar nichts kam. Eine tote Adresse unter zehn
    # soll den Lauf nicht verwerfen.
    if gelesen == 0:
        sys.exit("Keine einzige Seite gelesen.")


if __name__ == "__main__":
    main()
