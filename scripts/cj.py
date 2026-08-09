#!/usr/bin/env python3
"""
cj.py — durchsucht den CJ-Dropshipping-Katalog, nur Lager Deutschland.

Warum über die API und nicht über die Webseite: cjdropshipping.com
verlangt bei Listen- und Suchseiten eine Captcha-Prüfung ("Human
verification"). Das ist Absicht des Anbieters und wird hier nicht
umgangen. Die offizielle API ist der vorgesehene Weg und kann mehr:
Sie filtert direkt nach Lagerland und geprüftem Bestand.

Was die API liefert, das ein Katalogblick nicht hergibt:
  warehouseInventoryNum   Bestand
  totalVerifiedInventory  davon geprüft
  listedNum               wie viele Händler den Artikel schon führen
  deliveryCycle           Bearbeitungszeit in Tagen

listedNum ist die interessanteste Zahl. Ein Artikel mit viel Bestand und
wenigen Listungen ist entweder eine Lücke oder ein Ladenhüter — beides
muss man wissen, bevor man einkauft.

Geheimnisse: Es wird ausschließlich CJ_API_KEY aus der Umgebung gelesen.
Weder der Schlüssel noch das Token werden ausgegeben oder gespeichert.

Aufruf:
    python3 scripts/cj.py --config cj.config.json --out daten
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

BASIS = "https://developers.cjdropshipping.com/api2.0/v1"

# Die API erlaubt eine Anfrage je Sekunde (QPS = 1). Etwas Puffer, damit
# ein langsamer Runner nicht in die Drosselung läuft.
TAKT = 1.3

ANLEITUNG = """
Es fehlt das Secret CJ_API_KEY. Der Lauf bricht deshalb nicht ab —
hier steht, wie es eingerichtet wird:

1. Bei CJ anmelden und den Schlüssel erzeugen:
   https://www.cjdropshipping.com/my.html#/authorize/API
   Der Schlüssel sieht aus wie:  CJUserNum@api@xxxxxxxx

2. Im Repository unter
   Settings -> Secrets and variables -> Actions -> New repository secret
   Name:  CJ_API_KEY
   Wert:  der Schlüssel aus Schritt 1

Den Schlüssel nirgends sonst einfügen — nicht in eine Datei im
Repository, nicht in eine Nachricht. Als Secret ist er in den Logs
automatisch geschwärzt.
"""


def anfrage(pfad: str, token: str | None = None,
            daten: dict | None = None, params: dict | None = None) -> dict:
    url = f"{BASIS}/{pfad}"
    if params:
        # None-Werte raus, sonst landet "None" als Text in der Abfrage.
        sauber = {k: v for k, v in params.items() if v is not None}
        url += "?" + urllib.parse.urlencode(sauber)
    kopf = {"Content-Type": "application/json"}
    if token:
        kopf["CJ-Access-Token"] = token
    leib = json.dumps(daten).encode() if daten is not None else None
    r = urllib.request.Request(url, data=leib, headers=kopf,
                               method="POST" if daten is not None else "GET")
    try:
        with urllib.request.urlopen(r, timeout=40) as a:
            return json.loads(a.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        leib_text = e.read().decode("utf-8", "replace")[:300]
        # Die Fehlermeldung kann den Schlüssel zurückspiegeln. Nicht
        # weiterreichen, sonst steht er im Log.
        raise SystemExit(f"CJ antwortete mit HTTP {e.code}. "
                         f"Antwort (gekürzt, ohne Zugangsdaten): "
                         f"{leib_text[:120]}") from None


def token_holen(schluessel: str) -> str:
    a = anfrage("authentication/getAccessToken", daten={"apiKey": schluessel})
    if not a.get("result"):
        raise SystemExit(f"Anmeldung fehlgeschlagen: {a.get('message')}")
    return a["data"]["accessToken"]


def lager_pruefen(token: str) -> bool:
    """Gibt es das deutsche Lager überhaupt? Einmal nachsehen ist besser
    als bei jeder leeren Trefferliste zu rätseln."""
    a = anfrage("product/globalWarehouseList", token=token)
    lager = a.get("data") or []
    namen = [(w.get("countryCode"), w.get("areaEn")) for w in lager
             if isinstance(w, dict)]
    de = [n for n in namen if n[0] == "DE"]
    print(f"  {len(namen)} Lager verfügbar, Deutschland: "
          f"{de[0][1] if de else 'NICHT gefunden'}")
    return bool(de)


def suchen(token: str, begriff: str, cfg: dict) -> list[dict]:
    time.sleep(TAKT)
    a = anfrage("product/listV2", token=token, params={
        "keyWord": begriff,
        "countryCode": "DE",              # nur mit Bestand in Deutschland
        "verifiedWarehouse": 1,           # nur geprüfter Bestand
        "startWarehouseInventory": cfg.get("mindestbestand", 20),
        "startSellPrice": cfg.get("preis_von"),
        "endSellPrice": cfg.get("preis_bis"),
        "size": cfg.get("treffer", 40),
        "page": 1,
        "orderBy": 4,                     # nach Bestand sortieren
        "sort": "desc",
    })
    if not a.get("result"):
        print(f"    Abfrage fehlgeschlagen: {a.get('message')}")
        return []
    treffer: list[dict] = []
    # data.content ist eine Liste, jeder Eintrag trägt eine productList.
    for block in (a.get("data", {}).get("content") or []):
        for p in (block.get("productList") or []):
            treffer.append({
                "name": p.get("nameEn", ""),
                "sku": p.get("sku", ""),
                "preis": p.get("sellPrice"),
                "preis_aktion": p.get("nowPrice"),
                "bestand": p.get("warehouseInventoryNum", 0),
                "bestand_geprueft": p.get("totalVerifiedInventory", 0),
                "gelistet_von": p.get("listedNum", 0),
                "bearbeitung_tage": p.get("deliveryCycle", ""),
                "kategorie": p.get("threeCategoryName", ""),
                "bild": p.get("bigImage", ""),
                "id": p.get("id", ""),
            })
    return treffer


def bericht(daten: dict) -> str:
    z = ["# CJ Dropshipping — Lager Deutschland", "",
         f"Stand: {daten['stand']} · nur Artikel mit geprüftem Bestand in "
         f"Deutschland", "",
         "**gelistet von** zeigt, wie viele CJ-Händler den Artikel bereits "
         "führen. Wenige Listungen bei viel Bestand heißt Lücke *oder* "
         "Ladenhüter — die Zahl allein entscheidet nichts.", "",
         "Preise wie von CJ geliefert. Die Währung hängt an der "
         "Kontoeinstellung, das bitte einmal gegenprüfen.", ""]

    for eintrag in daten["suchen"]:
        treffer = eintrag["treffer"]
        z.append(f"## {eintrag['begriff']} — {len(treffer)} Treffer")
        z.append("")
        if not treffer:
            z += ["Nichts mit geprüftem Bestand im deutschen Lager.", ""]
            continue
        z.append("| Artikel | Preis | Bestand DE | gelistet von | Bearb. | SKU |")
        z.append("|---|---:|---:|---:|---|---|")
        for p in sorted(treffer, key=lambda x: -x["bestand"])[:20]:
            z.append(f"| {p['name'][:58]} | {p['preis']} | {p['bestand']} "
                     f"| {p['gelistet_von']} | {p['bearbeitung_tage']} "
                     f"| `{p['sku']}` |")
        z.append("")
        wenig = [p for p in treffer
                 if p["gelistet_von"] <= 5 and p["bestand"] >= 50]
        if wenig:
            z += [f"**Viel Bestand, kaum gelistet ({len(wenig)}):** "
                  + ", ".join(f"{p['name'][:40]} ({p['gelistet_von']}×)"
                              for p in wenig[:8]), ""]
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="cj.config.json")
    ap.add_argument("--out", default="daten")
    # Ersetzt die Begriffe aus der Konfiguration, ohne sie zu überschreiben.
    # Der Wert kommt aus einer Workflow-Eingabe und wird deshalb als
    # Argument übergeben, nicht in eine Shell-Zeile eingesetzt.
    ap.add_argument("--begriffe",
                    help="Suchbegriffe, Komma-getrennt (statt Konfiguration)")
    a = ap.parse_args()

    schluessel = os.environ.get("CJ_API_KEY", "").strip()
    if not schluessel:
        print(ANLEITUNG)
        return                      # bewusst grün: nichts ist kaputt

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    if a.begriffe:
        cfg["begriffe"] = [b.strip() for b in a.begriffe.split(",") if b.strip()]
        print(f"Begriffe aus dem Aufruf: {', '.join(cfg['begriffe'])}")
    if not cfg.get("begriffe"):
        sys.exit("Keine Suchbegriffe angegeben.")
    print("Bei CJ anmelden ...")
    token = token_holen(schluessel)
    print("  angemeldet")
    time.sleep(TAKT)
    if not lager_pruefen(token):
        sys.exit("Kein deutsches Lager in der Lagerliste — Abbruch, bevor "
                 "leere Ergebnisse als 'nichts gefunden' missverstanden "
                 "werden.")

    ergebnis = {"stand": str(date.today()), "suchen": []}
    for begriff in cfg["begriffe"]:
        print(f"\n=== {begriff} ===")
        treffer = suchen(token, begriff, cfg)
        print(f"  {len(treffer)} Artikel mit geprüftem Bestand in DE")
        ergebnis["suchen"].append({"begriff": begriff, "treffer": treffer})

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(ergebnis, ensure_ascii=False, indent=2)
    (out / f"cj-{ergebnis['stand']}.json").write_text(text, encoding="utf-8")
    (out / "cj-aktuell.json").write_text(text, encoding="utf-8")
    Path("CJ.md").write_text(bericht(ergebnis), encoding="utf-8")

    gesamt = sum(len(s["treffer"]) for s in ergebnis["suchen"])
    print(f"\nFertig: {gesamt} Artikel über {len(cfg['begriffe'])} Suchen. "
          f"Bericht in CJ.md")


if __name__ == "__main__":
    main()
