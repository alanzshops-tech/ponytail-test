#!/usr/bin/env python3
"""
bilder_holen.py — lädt eine Liste von Bild-URLs in einen Ordner.

Wozu: Die Arbeitsumgebung erreicht cdn.shopify.com nicht (nur GitHub,
PyPI, npm). Der Runner schon. Für alles, wofür ich ein Shopify-Bild
tatsächlich sehen oder weiterverarbeiten muss (Qualität prüfen, an
OpenRouter zur Bearbeitung schicken, dem Nutzer zum Download geben),
muss es erst hierher.

Aufruf:
    python3 scripts/bilder_holen.py --urls URL1 URL2 --ordner bilder/produktfotos/xyz
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlsplit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", nargs="+", required=True)
    ap.add_argument("--ordner", required=True)
    a = ap.parse_args()

    import requests

    ordner = Path(a.ordner)
    ordner.mkdir(parents=True, exist_ok=True)

    for i, url in enumerate(a.urls, start=1):
        name = Path(urlsplit(url).path).name or f"bild-{i}.jpg"
        ziel = ordner / f"{i:02d}-{name}"
        antwort = requests.get(url, timeout=30)
        antwort.raise_for_status()
        ziel.write_bytes(antwort.content)
        print(f"{ziel} ({len(antwort.content)} Bytes)")


if __name__ == "__main__":
    main()
