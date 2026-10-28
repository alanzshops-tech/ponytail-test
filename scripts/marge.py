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

Und am Ende die Umsatzsteuer — hier lag ich falsch. Ich habe pauschal
19 Prozent aufgeschlagen. Homeeins ist aber Kleinunternehmer nach § 19
UStG; das steht wörtlich im Impressum („Umsatzsteuerbefreit
(Kleinunternehmerregelung)") und in den AGB unter 4.1 („Umsatzsteuer
fällt nicht an"). Auch Shopify führt den Shop mit taxesIncluded = false
und ohne Steuersatz. Es gibt also kein Netto und kein Brutto, sondern
einen Preis. Der Aufschlag hat die empfohlenen Preise 19 Prozent zu hoch
gemacht — nicht gefährlich, aber teurer als nötig gegenüber dem
Wettbewerb.

    Einstand = (Einkauf + Versand) × Kurs
    VK       = Einstand × Faktor × (1 + Steuersatz)

Steuersatz ist voreingestellt 0. Wer die Kleinunternehmergrenze
überschreitet (seit 2025: 25.000 € Vorjahr / 100.000 € laufendes Jahr),
rechnet mit --ust 19 weiter.

Ein zweiter Punkt gehört dazu: Als Kleinunternehmer gibt es keinen
Vorsteuerabzug. Was CJ an Steuer berechnet, bleibt Kosten und steckt
bereits im Einkaufspreis — deshalb ist er hier voll angesetzt.

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

# Kleinunternehmer nach § 19 UStG — siehe Impressum und AGB 4.1.
# Kein Aufschlag, solange sich daran nichts ändert.
UST_VOREINSTELLUNG = 0.0
EZB = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


def bestand_de(token: str, sku: str) -> tuple[int, int, str]:
    """Bestand je Lagerhaus. Gibt (Deutschland, weltweit, Lagername).

    Die Trefferliste liefert warehouseInventoryNum — ohne Angabe, ob das
    der deutsche oder der weltweite Bestand ist. Das Beispiel in der
    Dokumentation zeigt China mit 777.566 neben US mit 36, also ist die
    Summe global. Wer daraus deutschen Bestand liest, plant mit Ware, die
    in Yiwu liegt."""
    time.sleep(TAKT)
    a = anfrage("product/stock/queryBySku", token=token, params={"sku": sku})
    if not a.get("result"):
        return 0, 0, ""
    lager = a.get("data") or []
    de = next((w for w in lager if w.get("countryCode") == "DE"), None)
    welt = sum(int(w.get("totalInventoryNum") or 0) for w in lager)
    if not de:
        return 0, welt, ""
    # cjInventoryNum ist die Ware, die wirklich im CJ-Lager steht.
    # totalInventoryNum zaehlt Fabrikbestand mit, der erst anreisen muss.
    return (int(de.get("cjInventoryNum") or 0), welt,
            de.get("areaEn", "Germany Warehouse"))


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
    # CJ liefert Preise in der Waehrung des Kontos. Die Dokumentation nennt
    # nur bei der Fracht ausdruecklich USD. Wer hier falsch liegt, verfehlt
    # den Faktor um den Wechselkurs — deshalb steht die Annahme im Bericht.
    ap.add_argument("--waehrung", choices=["EUR", "USD"], default="EUR")
    ap.add_argument("--ust", type=float, default=UST_VOREINSTELLUNG,
                    help="Umsatzsteuersatz in Prozent. Voreinstellung 0 — "
                         "Homeeins ist Kleinunternehmer nach § 19 UStG.")
    a = ap.parse_args()

    schluessel = os.environ.get("CJ_API_KEY", "").strip()
    if not schluessel:
        print(ANLEITUNG)
        return

    if a.waehrung == "USD":
        kurs, kursdatum = kurs_usd_eur()
        print(f"CJ-Preise in USD · EZB-Kurs vom {kursdatum}: "
              f"1 USD = {kurs:.4f} EUR")
    else:
        kurs, kursdatum = 1.0, "keine Umrechnung"
        print("CJ-Preise in EUR laut Kontoeinstellung — keine Umrechnung")
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
        de_stk, welt_stk, lagername = bestand_de(token, p["sku"])
        einkauf = preis(v)
        einstand = (einkauf + fracht) * kurs
        netto = einstand * a.faktor
        verkauf = netto * (1 + a.ust / 100)
        zeilen.append({
            "nische": p["nische"], "name": p["name"], "sku": p["sku"],
            "gelistet_von": p["gelistet_von"],
            "bestand_liste": p["bestand"],
            "bestand_de": de_stk, "bestand_welt": welt_stk,
            "lager": lagername,
            "einkauf_usd": round(einkauf, 2), "fracht_usd": round(fracht, 2),
            "einstand_eur": round(einstand, 2),
            "vk_ohne_steuer": round(netto, 2), "vk": round(verkauf, 2),
            "versandart": traeger, "laufzeit": dauer,
            "versand_inklusive": p.get("versand_inklusive"),
            "versandoptionen": optionen,
        })
        print(f"  {p['nische'][:22]:<24} EK {einkauf:6.2f} + Fracht "
              f"{fracht:5.2f} -> VK {verkauf:7.2f} EUR "
              f"| DE {de_stk:>5} von weltweit {welt_stk}")
        if len(zeilen) <= 3:
            print(f"      Versandoptionen laut CJ: {optionen}")

    ergebnis = {"stand": str(date.today()), "faktor": a.faktor,
                "kurs_usd_eur": round(kurs, 4), "kursdatum": kursdatum,
                "umsatzsteuer_prozent": a.ust, "zeilen": zeilen}
    Path("daten").mkdir(exist_ok=True)
    Path("daten/marge-aktuell.json").write_text(
        json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")

    waehrungszeile = (f"Preise in EUR laut Kontoeinstellung"
                      if a.waehrung == "EUR" else
                      f"Preise in USD · EZB-Kurs vom {kursdatum}: "
                      f"1 USD = {kurs:.4f} EUR")
    z = [f"# Verkaufspreise bei Faktor {a.faktor:g}", "",
         f"Stand {ergebnis['stand']} · {waehrungszeile} · "
         f"Umsatzsteuer {a.ust:g} %", "",
         "**Bestand DE** ist der Bestand im deutschen CJ-Lager, einzeln "
         "je Artikel abgefragt. Die Zahl aus der Trefferliste zählt alle "
         "Lager weltweit zusammen und taugt für die Planung nicht.", "",
         "CJ rechnet in Dollar. **Einstand** ist Einkauf plus Fracht in "
         "Euro; wo CJ den Versand im Preis führt (Spalte *frei*), ist die "
         "Fracht null. "
         + ("Der Shop ist Kleinunternehmer nach § 19 UStG — keine "
          "Umsatzsteuer, also kein Netto und kein Brutto. **VK** ist der "
          "Preis, der im Shop steht." if a.ust == 0 else
          f"Auf den Faktor kommen {a.ust:g} % Umsatzsteuer; **VK** ist der "
          f"Preis, der im Shop steht."), "",
         "| Nische | Artikel | Einkauf | Fracht | frei | Einstand € | "
         "**VK €** | Bestand DE | weltweit | Händler | Laufzeit |",
         "|---|---|---:|---:|:-:|---:|---:|---:|---:|---:|---|"]
    # Ohne Ware in Deutschland ist der Preis egal — solche Zeilen nach
    # unten, nicht heimlich weglassen.
    for r in sorted(zeilen, key=lambda x: (x["bestand_de"] == 0, x["vk"])):
        frei = {1: "ja", 0: "nein"}.get(r.get("versand_inklusive"), "?")
        z.append(f"| {r['nische']} | {r['name'][:44]} | {r['einkauf_usd']} "
                 f"| {r['fracht_usd']} | {frei} "
                 f"| {r['einstand_eur']} "
                 f"| **{r['vk']}** | {r['bestand_de']} "
                 f"| {r['bestand_welt']} | {r['gelistet_von']} "
                 f"| {r['laufzeit'] or '—'} |")
    z += ["", "Die Fracht ist für **ein** Stück nach Deutschland gerechnet. "
          "Bei zwei Artikeln in einer Bestellung sinkt sie je Stück — der "
          "Faktor wird dann besser, nicht schlechter.", ""]
    Path("MARGE.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    print(f"\nMARGE.md geschrieben — {len(zeilen)} Artikel gerechnet")


if __name__ == "__main__":
    main()
