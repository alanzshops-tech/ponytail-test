#!/usr/bin/env python3
"""
marge.py — rechnet aus, welcher Verkaufspreis den Faktor trägt.

Der Einkaufspreis ist nicht der Einstandspreis. Zwischen beiden liegen
zwei Posten, die eine Faktor-Rechnung sonst still auffrisst:

  Versand   CJ berechnet ihn getrennt, auch aus dem deutschen Lager.
            Bei einem Artikel für 23 Dollar sind 6 Dollar Fracht keine
            Nebensache, sondern ein Viertel des Einkaufs.

  Währung   CJ rechnet in US-Dollar. Der Kurs kommt von der EZB, nicht
            aus einer Schätzung.

Und am Ende steht die Umsatzsteuer: Ein Verkaufspreis im Shop ist brutto,
die Faktor-Rechnung gehört auf den Nettopreis. Wer 19 Prozent vergisst,
verfehlt seinen eigenen Faktor um ein Fünftel.

    Einstand  = (Einkauf + Versand) × Kurs
    VK netto  = Einstand × Faktor
    VK brutto = VK netto × 1,19

Aufruf:
    python3 scripts/marge.py --faktor 2.5
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cj import TAKT, anfrage, token_holen, ANLEITUNG      # noqa: E402

UST = 1.19          # Deutschland, Regelsteuersatz
EZB = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def kurs_usd_eur() -> tuple[float, str]:
    """Tageskurs der EZB. Gibt (EUR je USD, Datum) zurück."""
    with urllib.request.urlopen(EZB, timeout=30) as a:
        baum = ET.fromstring(a.read())
    datum, usd = "", 0.0
    for el in baum.iter():
        name = el.tag.rsplit("}", 1)[-1]
        if name == "Cube" and el.get("time"):
            datum = el.get("time")
        if name == "Cube" and el.get("currency") == "USD":
            usd = float(el.get("rate"))
    if not usd:
        raise SystemExit("Kein USD-Kurs in den EZB-Daten gefunden.")
    # Die EZB notiert USD je Euro. Gebraucht wird die Gegenrichtung.
    return 1 / usd, datum


def varianten(token: str, sku: str) -> list[dict]:
    time.sleep(TAKT)
    a = anfrage("product/query", token=token,
                params={"productSku": sku, "countryCode": "DE"})
    if not a.get("result"):
        return []
    d = a.get("data") or {}
    return d.get("variants") or []


def versand(token: str, vid: str) -> tuple[float, str, str, list]:
    """Fracht innerhalb Deutschlands für ein Stück.

    Gibt alle Optionen mit zurück. Der erste Lauf meldete bei 44 von 46
    Artikeln exakt 0,00 — entweder ist Versand aus dem deutschen Lager
    tatsächlich frei, oder die Antwort enthält eine Null-Option, die das
    Minimum verzerrt. Ohne die Liste lässt sich das nicht auseinander-
    halten, und ein zu niedriger Einstandspreis ruiniert jede
    Faktor-Rechnung."""
    time.sleep(TAKT)
    a = anfrage("logistic/freightCalculate", token=token, daten={
        "startCountryCode": "DE", "endCountryCode": "DE",
        "products": [{"quantity": 1, "vid": vid}]})
    if not a.get("result"):
        return 0.0, "", "", [{"fehler": a.get("message", "")[:80]}]
    liste = a.get("data") or []
    optionen = [{"name": x.get("logisticName", ""),
                 "preis": x.get("logisticPrice"),
                 "dauer": x.get("logisticAging", "")} for x in liste]
    if not liste:
        return 0.0, "", "", optionen
    # Nur Optionen mit echtem Preis. Eine Null ist kein Angebot, sondern
    # meistens ein Platzhalter.
    echte = [x for x in liste if float(x.get("logisticPrice") or 0) > 0]
    beste = min(echte or liste,
                key=lambda x: float(x.get("logisticPrice") or 999))
    return (float(beste.get("logisticPrice") or 0),
            beste.get("logisticName", ""), beste.get("logisticAging", ""),
            optionen)


def kandidaten(cj: Path, nischen: Path, je_nische: int) -> list[dict]:
    """Je Nische die Artikel mit den wenigsten Mitbewerbern."""
    artikel, gesehen = [], set()
    for s in json.loads(cj.read_text(encoding="utf-8"))["suchen"]:
        for p in s["treffer"]:
            if p["sku"] not in gesehen:
                gesehen.add(p["sku"])
                artikel.append(p)
    cfg = json.loads(nischen.read_text(encoding="utf-8"))
    aus = []
    for n in cfg["nischen"]:
        passend = [p for p in artikel if re.search(n["muster"], p["name"], re.I)]
        passend.sort(key=lambda p: (p["gelistet_von"], -p["bestand"]))
        for p in passend[:je_nische]:
            aus.append({**p, "nische": n["name"]})
    # Ein Artikel kann in zwei Nischen passen — nur einmal rechnen.
    einmal, sku_gesehen = [], set()
    for p in aus:
        if p["sku"] not in sku_gesehen:
            sku_gesehen.add(p["sku"])
            einmal.append(p)
    return einmal


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--faktor", type=float, default=2.5)
    ap.add_argument("--cj", default="daten/cj-aktuell.json")
    ap.add_argument("--nischen", default="nischen.config.json")
    ap.add_argument("--je-nische", type=int, default=2, dest="je_nische")
    a = ap.parse_args()

    schluessel = os.environ.get("CJ_API_KEY", "").strip()
    if not schluessel:
        print(ANLEITUNG)
        return

    kurs, kursdatum = kurs_usd_eur()
    print(f"EZB-Kurs vom {kursdatum}: 1 USD = {kurs:.4f} EUR")
    token = token_holen(schluessel)
    liste = kandidaten(Path(a.cj), Path(a.nischen), a.je_nische)
    print(f"{len(liste)} Kandidaten werden gerechnet\n")

    zeilen = []
    for p in liste:
        vs = varianten(token, p["sku"])
        if not vs:
            print(f"  {p['sku']}: keine Varianten abrufbar")
            continue
        # Die günstigste Variante ist der beste Fall für den Faktor.
        def preis(v):
            try:
                return float(v.get("variantSellPrice") or v.get("sellPrice") or 0)
            except (TypeError, ValueError):
                return 0.0
        v = min((x for x in vs if preis(x) > 0), key=preis, default=None)
        if not v:
            print(f"  {p['sku']}: kein Preis in den Varianten")
            continue
        vid = v.get("vid") or v.get("variantId") or ""
        fracht, traeger, dauer, optionen = (versand(token, vid) if vid
                                            else (0.0, "", "", []))
        einkauf = preis(v)
        einstand = (einkauf + fracht) * kurs
        netto = einstand * a.faktor
        zeilen.append({
            "nische": p["nische"], "name": p["name"], "sku": p["sku"],
            "gelistet_von": p["gelistet_von"], "bestand": p["bestand"],
            "einkauf_usd": round(einkauf, 2), "fracht_usd": round(fracht, 2),
            "einstand_eur": round(einstand, 2),
            "vk_netto": round(netto, 2), "vk_brutto": round(netto * UST, 2),
            "versandart": traeger, "laufzeit": dauer,
            "versand_inklusive": p.get("versand_inklusive"),
            "versandoptionen": optionen,
        })
        print(f"  {p['nische'][:22]:<24} Einkauf ${einkauf:6.2f} + Fracht "
              f"${fracht:5.2f} -> VK brutto {netto * UST:7.2f} EUR")
        if len(zeilen) <= 3:
            print(f"      Versandoptionen laut CJ: {optionen}")

    ergebnis = {"stand": str(date.today()), "faktor": a.faktor,
                "kurs_usd_eur": round(kurs, 4), "kursdatum": kursdatum,
                "umsatzsteuer": UST, "zeilen": zeilen}
    Path("daten").mkdir(exist_ok=True)
    Path("daten/marge-aktuell.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")

    z = [f"# Verkaufspreise bei Faktor {a.faktor:g}", "",
         f"Stand {ergebnis['stand']} · EZB-Kurs vom {kursdatum}: "
         f"1 USD = {kurs:.4f} EUR · Umsatzsteuer 19 %", "",
         "CJ rechnet in Dollar. **Einstand** ist Einkauf plus Fracht in "
         "Euro; wo CJ den Versand im Preis führt (Spalte *frei*), ist die "
         "Fracht null. "
         f"Der Faktor liegt auf dem **Nettopreis**; die Bruttospalte ist "
         f"das, was im Shop steht.", "",
         "| Nische | Artikel | Einkauf $ | Fracht $ | frei | Einstand € | "
         "VK netto € | **VK brutto €** | Händler | Laufzeit |",
         "|---|---|---:|---:|:-:|---:|---:|---:|---:|---|"]
    for r in sorted(zeilen, key=lambda x: x["vk_brutto"]):
        frei = {1: "ja", 0: "nein"}.get(r.get("versand_inklusive"), "?")
        z.append(f"| {r['nische']} | {r['name'][:44]} | {r['einkauf_usd']} "
                 f"| {r['fracht_usd']} | {frei} "
                 f"| {r['einstand_eur']} | {r['vk_netto']} "
                 f"| **{r['vk_brutto']}** | {r['gelistet_von']} "
                 f"| {r['laufzeit'] or '—'} |")
    z += ["", "Die Fracht ist für **ein** Stück nach Deutschland gerechnet. "
          "Bei zwei Artikeln in einer Bestellung sinkt sie je Stück — der "
          "Faktor wird dann besser, nicht schlechter.", ""]
    Path("MARGE.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    print(f"\nMARGE.md geschrieben — {len(zeilen)} Artikel gerechnet")


if __name__ == "__main__":
    main()
