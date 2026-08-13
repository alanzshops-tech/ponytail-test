#!/usr/bin/env python3
"""
produktdaten.py — holt alles zu einer Handvoll SKUs und legt es roh ab.

Bewusst ohne Auswahl: Es wird die vollständige Antwort gespeichert, nicht
die Felder, die ich für wichtig halte. Heute habe ich sechsmal danebe
gelegen, welches Feld was bedeutet — threeCategoryName kam nur mit
Zusatzparameter, totalVerifiedInventory war größer als der Bestand,
currency ist leer. Wer vorsortiert, verliert genau die Felder, deren
Bedeutung er noch nicht kennt.

Ausgabe: daten/produkte-roh.json

Aufruf:
    python3 scripts/produktdaten.py --skus CJJT2782337,CJJT2782055
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cj import TAKT, anfrage, token_holen, ANLEITUNG          # noqa: E402


FENSTER = 524288          # 512 KB -- Lieferantenfotos tragen oft ein
                          # eingebettetes Vorschaubild und ein Farbprofil
                          # vor dem eigentlichen SOF-Marker; 64 KB reichten
                          # bei CJs Bildern gemessen nicht (13.08.2026,
                          # kein Fehler, der SOF-Marker lag einfach dahinter).


def bildgroesse(url: str) -> tuple[int, int] | None:
    """Echte Pixelmaße eines JPEG/PNG. Meldet ehrlich, WARUM eine Messung
    scheitert, statt still None zurückzugeben -- eine Größe, die nicht
    gemessen werden konnte, ist etwas anderes als eine Größe, die belegt
    kleiner als empfohlen ist."""
    try:
        req = urllib.request.Request(url, headers={"Range": f"bytes=0-{FENSTER - 1}"})
        with urllib.request.urlopen(req, timeout=30) as a:
            kopf = a.read(FENSTER)
            gesamt = a.headers.get("Content-Range", "").split("/")[-1] \
                or a.headers.get("Content-Length", "?")
    except Exception as e:                                    # noqa: BLE001
        print(f"    Bildkopf nicht ladbar: {e}")
        return None

    if kopf[:2] != b"\xff\xd8" and kopf[:8] != b"\x89PNG\r\n\x1a\n":
        print(f"    kein bekanntes Bildformat, erste Bytes: {kopf[:12].hex()}, "
              f"Dateigröße laut Server: {gesamt}")
        return None

    if kopf[:8] == b"\x89PNG\r\n\x1a\n":                        # PNG
        breite, hoehe = struct.unpack(">II", kopf[16:24])
        return breite, hoehe

    i = 2                                                       # JPEG
    try:
        while i < len(kopf) - 9:
            if kopf[i] != 0xFF:
                i += 1
                continue
            marker = kopf[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                hoehe, breite = struct.unpack(">HH", kopf[i + 5:i + 9])
                return breite, hoehe
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            segment_laenge = struct.unpack(">H", kopf[i + 2:i + 4])[0]
            i += 2 + segment_laenge
    except struct.error:
        pass
    print(f"    SOF-Marker nicht innerhalb von {len(kopf)} geladenen Bytes "
          f"gefunden, Dateigröße laut Server: {gesamt}")
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skus", required=True, help="SKUs, Komma-getrennt")
    ap.add_argument("--out", default="daten/produkte-roh.json")
    ap.add_argument("--bildgroessen", action="store_true",
                    help="Echte Pixelmaße der productImage-URLs mitmessen")
    a = ap.parse_args()

    schluessel = os.environ.get("CJ_API_KEY", "").strip()
    if not schluessel:
        print(ANLEITUNG)
        return

    token = token_holen(schluessel)
    skus = [s.strip() for s in a.skus.split(",") if s.strip()]
    ergebnis = {"stand": str(date.today()), "produkte": {}}

    for sku in skus:
        print(f"\n=== {sku} ===")
        time.sleep(TAKT)
        detail = anfrage("product/query", token=token, params={
            "productSku": sku, "countryCode": "DE",
            # Beschreibung und Bestand mitliefern lassen — beide fehlen
            # sonst, genau wie die Kategorie ohne enable_category.
            "features": "enable_description,enable_inventory"})
        time.sleep(TAKT)
        lager = anfrage("product/stock/queryBySku", token=token,
                        params={"sku": sku})
        ergebnis["produkte"][sku] = {"detail": detail, "lager": lager}
        d = (detail.get("data") or {})
        print(f"  {d.get('productNameEn', '(kein Name)')[:70]}")
        print(f"  Felder in der Antwort: {sorted(d.keys())}")
        v = d.get("variants") or []
        print(f"  {len(v)} Varianten"
              + (f", Felder: {sorted(v[0].keys())}" if v else ""))

        if a.bildgroessen:
            bilder = d.get("productImageSet") or d.get("productImage") or []
            groessen = {}
            for url in bilder:
                time.sleep(0.3)
                g = bildgroesse(url)
                groessen[url] = {"breite": g[0], "hoehe": g[1]} if g else None
                anzeige = f"{g[0]}x{g[1]}" if g else "nicht messbar"
                print(f"    {anzeige}  {url}")
            ergebnis["produkte"][sku]["bildgroessen"] = groessen

    p = Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print(f"\n{len(skus)} Produkte roh gespeichert in {p}")


if __name__ == "__main__":
    main()
