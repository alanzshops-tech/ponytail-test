#!/usr/bin/env python3
"""
trends.py — holt Google-Trends-Daten für die Suchbegriffe aus trends.config.json.

Wozu: Die Beitragsplanung hing bisher an meiner Einschätzung, was saisonal
passt ("Feuerschale im August, Gewichtsdecke im Herbst"). Das ist geraten.
Google Trends zeigt die tatsächliche Nachfragekurve in Deutschland — und
verschiebt damit die Planung von Bauchgefühl auf Messwerte.

Ausgabe:
  daten/trends-JJJJ-MM-TT.json   Rohdaten, versioniert als Zeitreihe
  daten/trends-aktuell.json      immer der letzte Stand
  TRENDS.md                      lesbare Auswertung

Grenzen, die man kennen muss:
  - Die Werte sind Indexwerte von 0 bis 100, keine Suchvolumina. 100 ist der
    Höchstwert INNERHALB einer Abfragegruppe im Zeitraum. Begriffe aus
    verschiedenen Gruppen sind deshalb nicht vergleichbar.
  - Google drosselt die inoffizielle Schnittstelle (HTTP 429). Das Skript
    wartet und wiederholt; scheitert eine Gruppe endgültig, wird das im
    Bericht vermerkt statt stillschweigend weggelassen.

Aufruf:
    python3 scripts/trends.py --config trends.config.json --out daten
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import date
from pathlib import Path

# Wie oft eine Gruppe wiederholt wird, bevor sie als fehlgeschlagen gilt,
# und wie lange dazwischen gewartet wird (Google drosselt aggressiv).
VERSUCHE = 4
WARTEN_START = 20
WARTEN_ZWISCHEN_GRUPPEN = 12

# Fehler, die durch Warten nie verschwinden: falsche Signatur, fehlendes
# Modul, kaputte Konfiguration. Der erste Lauf hat neun Minuten damit
# verbracht, einen TypeError dreimal zu wiederholen. Solche Fehler brechen
# die Gruppe sofort ab, statt die Wiederholungen zu verbrauchen.
DAUERHAFT = (TypeError, AttributeError, ImportError, NameError, KeyError)


def klient(sprache: str = "de-DE"):
    from pytrends.request import TrendReq
    # Bewusst OHNE retries/backoff_factor: pytrends baut daraus ein
    # urllib3-Retry mit dem Argument method_whitelist, das in urllib3 2.0
    # entfernt wurde -> TypeError bei jedem Aufruf. Wiederholungen macht
    # ohnehin die Schleife in main(), eine Ebene höher.
    #
    # Ohne Browser-Kennung antwortet Google deutlich häufiger mit 429.
    return TrendReq(
        hl=sprache,
        tz=-60,
        timeout=(10, 30),
        requests_args={"headers": {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/126.0 Safari/537.36"),
            "Accept-Language": "de-DE,de;q=0.9",
        }},
    )


def gruppe_holen(py, begriffe: list[str], zeitraum: str, region: str) -> dict:
    """Eine Gruppe abfragen: Verlauf plus aufsteigende Suchanfragen."""
    py.build_payload(begriffe, timeframe=zeitraum, geo=region)

    verlauf_df = py.interest_over_time()
    verlauf: dict[str, list] = {}
    if verlauf_df is not None and not verlauf_df.empty:
        # isPartial markiert die laufende, noch unvollständige Periode.
        if "isPartial" in verlauf_df.columns:
            verlauf_df = verlauf_df[~verlauf_df["isPartial"]]
        for b in begriffe:
            if b in verlauf_df.columns:
                verlauf[b] = [
                    {"datum": str(i.date()), "wert": int(v)}
                    for i, v in verlauf_df[b].items()
                ]

    # Aufsteigende verwandte Suchanfragen: die beste Quelle für Begriffe,
    # auf die noch niemand optimiert.
    steigend: dict[str, list] = {}
    try:
        verwandt = py.related_queries() or {}
        for b in begriffe:
            eintrag = (verwandt.get(b) or {}).get("rising")
            if eintrag is not None and not eintrag.empty:
                steigend[b] = [
                    {"anfrage": r["query"], "zuwachs": int(r["value"])}
                    for _, r in eintrag.head(5).iterrows()
                ]
    except Exception as e:                                   # noqa: BLE001
        print(f"    verwandte Anfragen nicht verfügbar: {e}")

    return {"verlauf": verlauf, "steigend": steigend}


def auswerten(verlauf: list[dict]) -> dict:
    """Kennzahlen je Begriff: aktueller Stand, Jahresmittel, Saisonhoch."""
    werte = [p["wert"] for p in verlauf]
    if not werte:
        return {}
    jetzt = werte[-1]
    mittel = statistics.mean(werte)
    hoch = max(werte)
    hoch_datum = verlauf[werte.index(hoch)]["datum"]
    # Vergleich mit vor rund drei Monaten (Wochenwerte -> 13 Schritte).
    zurueck = werte[-14] if len(werte) >= 14 else werte[0]
    return {
        "jetzt": jetzt,
        "jahresmittel": round(mittel, 1),
        "hoechstwert": hoch,
        "hoch_am": hoch_datum,
        "gegen_jahresmittel_prozent": round((jetzt - mittel) / mittel * 100)
        if mittel else 0,
        "gegen_vor_3_monaten_prozent": round((jetzt - zurueck) / zurueck * 100)
        if zurueck else 0,
    }


def einordnen(k: dict) -> str:
    """Kurzurteil für die Planung."""
    if not k:
        return "keine Daten"
    gegen_mittel = k["gegen_jahresmittel_prozent"]
    trend = k["gegen_vor_3_monaten_prozent"]
    if gegen_mittel >= 20 and trend >= 10:
        return "Hochsaison, jetzt bewerben"
    if trend >= 25:
        return "steigt deutlich"
    if gegen_mittel <= -25 and trend <= -10:
        return "Nebensaison, zurückstellen"
    if trend <= -25:
        return "fällt deutlich"
    return "stabil"


def bericht(daten: dict) -> str:
    z = [f"# Google Trends — homeeins", "",
         f"Stand: {daten['stand']} · Region: {daten['region']} · "
         f"Zeitraum: {daten['zeitraum']}", "",
         "Indexwerte 0–100, **nur innerhalb einer Gruppe vergleichbar**. "
         "100 = Höchstwert der jeweiligen Gruppe im Zeitraum.", ""]

    for g in daten["gruppen"]:
        z.append(f"## {g['name']}")
        z.append("")
        if g.get("fehler"):
            z.append(f"> Abfrage fehlgeschlagen: {g['fehler']}")
            z.append("")
            continue
        z.append("| Begriff | Jetzt | Jahresmittel | Saisonhoch | vs. 3 Mon. | Einordnung |")
        z.append("|---|---:|---:|---|---:|---|")
        reihen = []
        for begriff, kw in g["kennzahlen"].items():
            if not kw:
                continue
            reihen.append((kw["gegen_jahresmittel_prozent"], begriff, kw))
        for _, begriff, kw in sorted(reihen, reverse=True):
            z.append(
                f"| {begriff} | {kw['jetzt']} | {kw['jahresmittel']} | "
                f"{kw['hoechstwert']} am {kw['hoch_am']} | "
                f"{kw['gegen_vor_3_monaten_prozent']:+d} % | {einordnen(kw)} |")
        z.append("")

        steigend = {b: v for b, v in g.get("steigend", {}).items() if v}
        if steigend:
            z.append("**Aufsteigende Suchanfragen** — Begriffe mit wachsender "
                     "Nachfrage, oft noch wenig umkämpft:")
            z.append("")
            for begriff, liste in steigend.items():
                treffer = ", ".join(
                    f"{e['anfrage']} (+{e['zuwachs']} %)" for e in liste)
                z.append(f"- *{begriff}*: {treffer}")
            z.append("")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="trends.config.json")
    ap.add_argument("--out", default="daten")
    a = ap.parse_args()

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8"))
    region, zeitraum = cfg.get("region", "DE"), cfg.get("zeitraum", "today 12-m")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    py = klient()
    ergebnis = {"stand": str(date.today()), "region": region,
                "zeitraum": zeitraum, "gruppen": []}
    fehlgeschlagen = 0

    for i, gruppe in enumerate(cfg["gruppen"]):
        begriffe = gruppe["begriffe"][:5]
        print(f"\n=== {gruppe['name']}: {', '.join(begriffe)} ===")
        eintrag = {"name": gruppe["name"], "begriffe": begriffe}

        for versuch in range(1, VERSUCHE + 1):
            try:
                roh = gruppe_holen(py, begriffe, zeitraum, region)
                eintrag.update(roh)
                eintrag["kennzahlen"] = {
                    b: auswerten(v) for b, v in roh["verlauf"].items()}
                for b, k in eintrag["kennzahlen"].items():
                    if k:
                        print(f"  {b}: jetzt {k['jetzt']}, "
                              f"Mittel {k['jahresmittel']}, {einordnen(k)}")
                break
            except DAUERHAFT as e:
                print(f"  Dauerhafter Fehler, keine Wiederholung: "
                      f"{type(e).__name__}: {e}")
                eintrag["fehler"] = f"{type(e).__name__}: {e}"[:200]
                fehlgeschlagen += 1
                break
            except Exception as e:                            # noqa: BLE001
                wartezeit = WARTEN_START * versuch
                print(f"  Versuch {versuch}/{VERSUCHE} fehlgeschlagen: {e}")
                if versuch == VERSUCHE:
                    eintrag["fehler"] = str(e)[:200]
                    fehlgeschlagen += 1
                else:
                    print(f"  warte {wartezeit}s ...")
                    time.sleep(wartezeit)

        ergebnis["gruppen"].append(eintrag)
        if i < len(cfg["gruppen"]) - 1:
            time.sleep(WARTEN_ZWISCHEN_GRUPPEN)

    text = json.dumps(ergebnis, ensure_ascii=False, indent=2)
    (out / f"trends-{ergebnis['stand']}.json").write_text(text, encoding="utf-8")
    (out / "trends-aktuell.json").write_text(text, encoding="utf-8")
    Path("TRENDS.md").write_text(bericht(ergebnis), encoding="utf-8")

    gesamt = len(cfg["gruppen"])
    print(f"\nFertig: {gesamt - fehlgeschlagen}/{gesamt} Gruppen abgefragt")
    # Nur abbrechen, wenn gar nichts durchkam - Teilergebnisse sind brauchbar.
    if fehlgeschlagen == gesamt:
        sys.exit("Keine einzige Gruppe erfolgreich - vermutlich gedrosselt.")


if __name__ == "__main__":
    main()
