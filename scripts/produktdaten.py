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
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cj import TAKT, anfrage, token_holen, ANLEITUNG          # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skus", required=True, help="SKUs, Komma-getrennt")
    ap.add_argument("--out", default="daten/produkte-roh.json")
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

    p = Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2),
                 encoding="utf-8")
    print(f"\n{len(skus)} Produkte roh gespeichert in {p}")


if __name__ == "__main__":
    main()
