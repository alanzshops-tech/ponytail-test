#!/usr/bin/env python3
"""
gesamtscan.py — wertet den Unlighthouse-Lauf aus.

Warum ein zweites Lighthouse: Das bisherige misst sechs Seiten, die ich
selbst ausgesucht habe. Unlighthouse (MIT, harlan-zw) läuft über den
ganzen Shop und fasst gleichartige Seiten zu Mustern zusammen — es prüft
also nicht 146 Produktseiten einzeln, sondern eine Stichprobe je
Seitentyp. Damit finde ich systematische Fehler statt der Fehler auf den
Seiten, an die ich zufällig gedacht habe.

Das Schema der Ausgabedatei kenne ich nicht auswendig. Deshalb sucht
dieses Skript die Datei, beschreibt beim ersten Lauf ihren Aufbau im
Bericht und wertet defensiv aus. Eine Auswertung, die bei unbekanntem
Aufbau still nichts meldet, wäre schlimmer als gar keine.

Aufruf:
    python3 scripts/gesamtscan.py --ordner .unlighthouse
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

FELDER_SCORE = ("performance", "accessibility", "best-practices", "seo")


def datei_finden(ordner: Path) -> Path | None:
    kandidaten = sorted(ordner.rglob("*.json"), key=lambda p: -p.stat().st_size)
    for p in kandidaten:
        if "ci-result" in p.name or "report" in p.name:
            return p
    return kandidaten[0] if kandidaten else None


def zeilen_aus(d) -> list[dict]:
    """Findet die Liste der Seitenergebnisse, egal wie sie verschachtelt
    ist. Gesucht wird nach Einträgen, die einen Pfad und Scores haben."""
    gefunden: list[dict] = []

    def wandern(x):
        if isinstance(x, dict):
            pfad = x.get("path") or x.get("route") or x.get("url")
            scores = x.get("categories") or x.get("score") or x.get("scores")
            if pfad and scores:
                gefunden.append(x)
            for v in x.values():
                wandern(v)
        elif isinstance(x, list):
            for v in x:
                wandern(v)

    wandern(d)
    return gefunden


def score(eintrag: dict, name: str):
    c = eintrag.get("categories")
    if isinstance(c, dict):
        v = c.get(name)
        if isinstance(v, dict):
            v = v.get("score")
        if isinstance(v, (int, float)):
            return round(v * 100) if v <= 1 else round(v)
    s = eintrag.get("score")
    if name == "performance" and isinstance(s, (int, float)):
        return round(s * 100) if s <= 1 else round(s)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ordner", default=".unlighthouse")
    a = ap.parse_args()
    ordner = Path(a.ordner)

    z = ["# Gesamtscan", "", f"Stand: {date.today()}", "",
         "Gemessen mit **Unlighthouse** (MIT) — Google Lighthouse über den "
         "ganzen Shop statt über sechs handverlesene Seiten. Gleichartige "
         "Seiten werden zu Mustern zusammengefasst, es läuft also eine "
         "Stichprobe je Seitentyp.", ""]

    datei = datei_finden(ordner) if ordner.exists() else None
    if not datei:
        z += ["Keine Ergebnisdatei gefunden. Der Lauf ist entweder "
              "fehlgeschlagen oder hat woanders geschrieben.", ""]
        Path("GESAMTSCAN.md").write_text("\n".join(z) + "\n", encoding="utf-8")
        print("Keine Ergebnisdatei.")
        return

    d = json.loads(datei.read_text(encoding="utf-8"))
    eintraege = zeilen_aus(d)
    z += [f"Quelle: `{datei}` ({datei.stat().st_size} Bytes), "
          f"{len(eintraege)} Seitenergebnisse.", ""]

    if not eintraege:
        # Aufbau offenlegen statt schweigen — beim nächsten Lauf ist die
        # Auswertung dann richtig statt still leer.
        z += ["Der Aufbau der Datei ist unbekannt. Oberste Ebene:", "",
              "```", json.dumps(d, ensure_ascii=False)[:1200], "```", ""]
        Path("GESAMTSCAN.md").write_text("\n".join(z) + "\n", encoding="utf-8")
        print("Aufbau unbekannt, im Bericht dokumentiert.")
        return

    z += ["| Seite | Tempo | Barrierefreiheit | Praxis | SEO |",
          "|---|---:|---:|---:|---:|"]
    schlecht = []
    for e in sorted(eintraege, key=lambda x: str(x.get("path") or x.get("route") or x.get("url"))):
        pfad = str(e.get("path") or e.get("route") or e.get("url"))[:60]
        werte = [score(e, f) for f in FELDER_SCORE]
        z.append("| " + pfad + " | " +
                 " | ".join("–" if v is None else str(v) for v in werte) + " |")
        p = werte[0]
        if p is not None and p < 50:
            schlecht.append((pfad, p))
    z.append("")

    for name, i in zip(("Tempo", "Barrierefreiheit", "Praxis", "SEO"), range(4)):
        werte = [score(e, FELDER_SCORE[i]) for e in eintraege]
        werte = [v for v in werte if v is not None]
        if werte:
            werte.sort()
            z.append(f"- **{name}**: Median {werte[len(werte)//2]}, "
                     f"schlechtester {werte[0]}, bester {werte[-1]} "
                     f"({len(werte)} Seiten)")
    z.append("")
    if schlecht:
        z += ["## Unter 50 beim Tempo", ""]
        z += [f"- `{p}` — {v}" for p, v in sorted(schlecht, key=lambda x: x[1])]
        z.append("")
    # Der erste Lauf zeigte auf 34 Seiten fast durchgehend dieselbe
    # Praxis-Note. Gleiche Zahl überall heißt: eine gemeinsame Ursache,
    # nicht 34 einzelne. ci-result.json (auch mit --reporter jsonExpanded)
    # enthält aber nur die Kategorien-Scores, keine einzelnen Prüfpunkte —
    # nachgeprüft im Quellcode von @unlighthouse/core (reportJsonExpanded
    # reduziert jeden Report auf categories + eine feste Metrik-Liste).
    # Die vollen Lighthouse-Berichte je Seite liegen aber trotzdem auf der
    # Platte, unter <ausgabe>/**/lighthouse.json — dort stehen die
    # einzelnen Audits mit Score. Die werden hier zusätzlich gelesen, ohne
    # sie zu committen (nur die Zusammenfassung landet im Bericht).
    durchgefallen: dict[str, dict[str, dict]] = {f: {} for f in FELDER_SCORE}
    lh_dateien = list(ordner.rglob("lighthouse.json")) if ordner.exists() else []
    lh_gelesen = 0
    for p in lh_dateien:
        try:
            lh = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        kategorien = lh.get("categories")
        audits_alle = lh.get("audits")
        if not isinstance(kategorien, dict) or not isinstance(audits_alle, dict):
            continue
        lh_gelesen += 1
        for kat_id in FELDER_SCORE:
            kat = kategorien.get(kat_id)
            if not isinstance(kat, dict):
                continue
            for ref in kat.get("auditRefs") or []:
                aid = ref.get("id") if isinstance(ref, dict) else None
                if not aid:
                    continue
                av = audits_alle.get(aid)
                if not isinstance(av, dict):
                    continue
                s = av.get("score")
                # scoreDisplayMode "notApplicable"/"informative" liefern
                # score: null — das ist kein Durchfallen, sondern "trifft
                # nicht zu". Nur echte Zahlenwerte unter 0.9 zählen.
                if isinstance(s, (int, float)) and not isinstance(s, bool) and s < 0.9:
                    eintrag = durchgefallen[kat_id].setdefault(
                        aid, {"titel": av.get("title", aid), "seiten": 0})
                    eintrag["seiten"] += 1

    if lh_gelesen == 0:
        z += ["## Prüfpunkte, die auf vielen Seiten durchfallen", "",
              f"Keine `lighthouse.json`-Dateien unter `{ordner}` gefunden — "
              "nur die Kategorien-Scores oben sind belastbar, welche "
              "einzelnen Prüfpunkte dahinterstecken bleibt offen. Das ist "
              "ein leeres Ergebnis, kein \"kein Problem\".", ""]
    else:
        for kat_id, titel in zip(FELDER_SCORE,
                                  ("Tempo", "Barrierefreiheit", "Praxis", "SEO")):
            kat_durchgefallen = durchgefallen[kat_id]
            if not kat_durchgefallen:
                continue
            z += [f"## {titel}: Prüfpunkte, die auf vielen Seiten durchfallen "
                  f"({lh_gelesen} Berichte gelesen)", "",
                  "| Prüfpunkt | betroffene Seiten |", "|---|---:|"]
            for aid, v in sorted(kat_durchgefallen.items(),
                                 key=lambda x: -x[1]["seiten"])[:20]:
                z.append(f"| {v['titel']} (`{aid}`) | {v['seiten']} von "
                         f"{lh_gelesen} |")
            z.append("")

    z += ["Skala 0–100. Google nennt ab 90 gut, unter 50 schlecht. Der "
          "Wert schwankt zwischen Läufen um einige Punkte — belastbar ist "
          "der Trend über mehrere Wochen, nicht die einzelne Zahl.", ""]

    Path("GESAMTSCAN.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    print(f"GESAMTSCAN.md geschrieben — {len(eintraege)} Seiten")


if __name__ == "__main__":
    main()
