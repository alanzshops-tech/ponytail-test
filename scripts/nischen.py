#!/usr/bin/env python3
"""
nischen.py — führt Nachfrage und Angebot zusammen.

Die beiden Hälften lagen bisher getrennt im Repo: TRENDS.md sagt, wonach
in Deutschland gesucht wird, CJ.md sagt, was im deutschen Lager liegt.
Erst zusammen beantworten sie die Frage, die zählt — welche Nische lohnt
sich, und wann.

Zwei Kennzahlen entscheiden:

  Jahresmittel   Wie groß die Nische überhaupt ist. Ein Begriff mit
                 Mittel 3 hat keine Nachfrage, egal wie schön das
                 Produkt ist. Nur innerhalb einer Abfragegruppe
                 vergleichbar — die Gruppe steht deshalb im Bericht.

  Saisonfaktor   Höchstwert geteilt durch Jahresmittel. Bei 1,3 läuft es
                 das ganze Jahr gleichmäßig. Ab etwa 1,8 ist es
                 Saisonware: Der Einkauf muss dann vor dem Hoch stehen,
                 nicht mittendrin.

Angebot kommt aus dem CJ-Lauf: Artikelzahl, Bestand und vor allem, von
wie vielen Händlern die Artikel schon geführt werden.

Aufruf:
    python3 scripts/nischen.py
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
from pathlib import Path

MONATE = {1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai",
          6: "Juni", 7: "Juli", 8: "August", 9: "September",
          10: "Oktober", 11: "November", 12: "Dezember"}

# Ab hier gilt eine Nische als Saisonware. Der Wert ist gesetzt, nicht
# gemessen: Bei 1,8 liegt das Hoch fast doppelt so hoch wie der
# Jahresschnitt, und das ist die Schwelle, ab der der Einkaufszeitpunkt
# über das Ergebnis entscheidet.
SAISON_AB = 1.8


def trends_lesen(pfad: Path) -> dict:
    d = json.loads(pfad.read_text(encoding="utf-8"))
    aus: dict[str, dict] = {}
    for g in d["gruppen"]:
        if g.get("fehler"):
            continue
        for begriff, k in (g.get("kennzahlen") or {}).items():
            if not k:
                continue
            verlauf = g["verlauf"].get(begriff, [])
            monate = collections.defaultdict(list)
            for punkt in verlauf:
                monate[int(punkt["datum"][5:7])].append(punkt["wert"])
            mittel_monat = {m: statistics.mean(w) for m, w in monate.items()}
            hoch_monat = max(mittel_monat, key=mittel_monat.get) if mittel_monat else 0
            mittel = k["jahresmittel"] or 0.01
            aus[begriff] = {
                "gruppe": g["name"],
                "jetzt": k["jetzt"],
                "mittel": k["jahresmittel"],
                "hoch": k["hoechstwert"],
                "saisonfaktor": round(k["hoechstwert"] / mittel, 2),
                "hoch_monat": MONATE.get(hoch_monat, "—"),
                "trend_3m": k["gegen_vor_3_monaten_prozent"],
                "monatsmittel": {m: round(v, 1) for m, v in sorted(mittel_monat.items())},
            }
    return aus


def cj_lesen(pfad: Path) -> list[dict]:
    d = json.loads(pfad.read_text(encoding="utf-8"))
    alle: list[dict] = []
    gesehen = set()
    for s in d["suchen"]:
        for p in s["treffer"]:
            # Derselbe Artikel taucht bei mehreren Suchbegriffen auf.
            if p["sku"] in gesehen:
                continue
            gesehen.add(p["sku"])
            alle.append(p)
    return alle


def urteil(n: dict) -> str:
    if n["mittel"] < 8:
        return "zu klein"
    if n["saisonfaktor"] >= SAISON_AB:
        return f"Saison ({n['hoch_monat']})"
    return "ganzjährig"


def bericht(nischen: list[dict], stand_t: str, stand_c: str) -> str:
    z = ["# Nischen — Nachfrage trifft deutsches Lager", "",
         f"Trends-Stand {stand_t} · CJ-Stand {stand_c}", "",
         "**Jahresmittel** zeigt die Größe der Nische, **Saisonfaktor** "
         "das Verhältnis von Hoch zu Durchschnitt. Ab 1,8 ist es "
         "Saisonware — dann entscheidet der Einkaufszeitpunkt mit.", "",
         "> Indexwerte sind **nur innerhalb einer Abfragegruppe** "
         "vergleichbar. Die Gruppe steht in der letzten Spalte. Wer "
         "Zahlen aus verschiedenen Gruppen gegeneinanderstellt, "
         "vergleicht Äpfel mit Birnen.", ""]

    mit = [n for n in nischen if n["cj_artikel"] > 0 and n["mittel"] is not None]
    ganzjahr = sorted((n for n in mit if urteil(n) == "ganzjährig"),
                      key=lambda n: -n["mittel"])
    saison = sorted((n for n in mit if urteil(n).startswith("Saison")),
                    key=lambda n: -n["mittel"])
    klein = [n for n in mit if urteil(n) == "zu klein"]
    ohne = [n for n in nischen if n["cj_artikel"] == 0]

    def tabelle(titel: str, reihen: list[dict], extra: str = "") -> None:
        if not reihen:
            return
        z.append(f"## {titel}")
        z.append("")
        if extra:
            # extend statt "+=" — eine Zuweisung würde z hier zu einer
            # lokalen Variablen machen und die äußere verdecken.
            z.extend([extra, ""])
        z.append("| Nische | Mittel | Saison­faktor | Hoch im | vs. 3 Mon. "
                 "| Artikel im DE-Lager | Bestand | Ø Händler | Gruppe |")
        z.append("|---|---:|---:|---|---:|---:|---:|---:|---|")
        for n in reihen:
            z.append(f"| {n['name']} | {n['mittel']} | {n['saisonfaktor']} "
                     f"| {n['hoch_monat']} | {n['trend_3m']:+d} % "
                     f"| {n['cj_artikel']} | {n['cj_bestand']} "
                     f"| {n['cj_gelistet']} | {n['gruppe']} |")
        z.append("")

    tabelle("Ganzjährig", ganzjahr,
            "Laufen das ganze Jahr durch. Kein Einkaufsdruck, dafür "
            "planbarer Umsatz.")
    tabelle("Saisonware", saison,
            "Das Hoch liegt deutlich über dem Schnitt. Die Ware muss "
            "**vor** dem genannten Monat im Shop stehen, nicht darin.")

    if klein:
        z += ["## Zu kleine Nachfrage", "",
              "Jahresmittel unter 8 — die Kurve liegt fast das ganze Jahr "
              "nahe null. Verfügbarkeit im Lager ändert daran nichts.", "",
              ", ".join(f"{n['name']} ({n['mittel']})" for n in klein), ""]
    if ohne:
        z += ["## Nachfrage da, aber nichts im deutschen Lager", "",
              ", ".join(f"{n['name']} ({n['mittel']})"
                        for n in sorted(ohne, key=lambda x: -(x['mittel'] or 0))
                        if n["mittel"]), ""]

    # Die Verlaufszeile macht die Saisonform sichtbar. Eine Zahl sagt
    # "Hoch im Dezember", dreizehn Zahlen zeigen, wie steil es dahin geht.
    z += ["## Verlauf über zwölf Monate", "",
          "Monatsmittel des Indexwerts, jeweils innerhalb der Gruppe.", "",
          "```"]
    for n in ganzjahr + saison:
        reihe = " ".join(f"{n['monatsmittel'].get(m, 0):4.0f}" for m in range(1, 13))
        z.append(f"{n['name'][:24]:<24} {reihe}")
    z += ["", f"{'':<24} {'  Jan  Feb  Mär  Apr  Mai  Jun  Jul  Aug  Sep  Okt  Nov  Dez'}",
          "```", ""]
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="nischen.config.json")
    ap.add_argument("--trends", default="daten/trends-aktuell.json")
    ap.add_argument("--cj", default="daten/cj-aktuell.json")
    a = ap.parse_args()

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    t = trends_lesen(Path(a.trends))
    artikel = cj_lesen(Path(a.cj))
    print(f"{len(t)} Suchbegriffe mit Kennzahlen, {len(artikel)} Artikel im Lager")

    nischen = []
    for eintrag in cfg["nischen"]:
        passend = [p for p in artikel
                   if re.search(eintrag["muster"], p["name"], re.I)]
        kennz = t.get(eintrag["begriff"], {})
        if not kennz:
            print(f"  ohne Trends-Daten: {eintrag['begriff']}")
        nischen.append({
            "name": eintrag["name"],
            "begriff": eintrag["begriff"],
            "gruppe": kennz.get("gruppe", "—"),
            "mittel": kennz.get("mittel"),
            "saisonfaktor": kennz.get("saisonfaktor", 0),
            "hoch_monat": kennz.get("hoch_monat", "—"),
            "trend_3m": kennz.get("trend_3m", 0),
            "monatsmittel": kennz.get("monatsmittel", {}),
            "cj_artikel": len(passend),
            "cj_bestand": sum(p["bestand"] for p in passend),
            "cj_gelistet": round(statistics.mean(
                [p["gelistet_von"] for p in passend]), 1) if passend else 0,
        })

    stand_t = json.loads(Path(a.trends).read_text(encoding="utf-8"))["stand"]
    stand_c = json.loads(Path(a.cj).read_text(encoding="utf-8"))["stand"]
    Path("NISCHEN.md").write_text(bericht(nischen, stand_t, stand_c),
                                  encoding="utf-8")
    mit = sum(1 for n in nischen if n["cj_artikel"] and (n["mittel"] or 0) >= 8)
    print(f"NISCHEN.md geschrieben — {mit} von {len(nischen)} Nischen haben "
          f"sowohl Nachfrage als auch Ware im deutschen Lager")


if __name__ == "__main__":
    main()
