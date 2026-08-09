#!/usr/bin/env python3
"""
gsc.py — holt die Google-Search-Console-Daten für homeeins.de.

Wozu: Bis jetzt kannte ich die Suchleistung nur aus einem Screenshot. Die
Search-Console-API ist kostenlos und braucht kein Abrechnungskonto — damit
kann ich wöchentlich selbst nachsehen, statt zu fragen.

Was abgefragt wird:
  - Tagesverlauf (Klicks, Impressionen, CTR, Position)
  - Suchanfragen mit Position und CTR
  - Seiten
  - Geräte

Die interessante Auswertung ist nicht die Top-Liste, sondern:
  - Anfragen auf Position 5-20 mit Impressionen  -> echte Reichweite
  - Seiten mit Impressionen, aber null Klicks    -> Snippet-Problem
  - Vergleich mit der Vorperiode                 -> wirkt, was wir tun?

Zugang, in dieser Reihenfolge:
  1. Application Default Credentials — im Workflow von
     google-github-actions/auth per Workload Identity Federation gesetzt.
     Kein Schlüssel, nur ein kurzlebiges Token. Bevorzugter Weg.
  2. Dienstkonto-JSON in GSC_SERVICE_ACCOUNT_JSON, falls jemand doch mit
     einer Schlüsseldatei arbeitet.
Fehlt beides, bricht das Skript nicht ab, sondern erklärt die Einrichtung.

Aufruf:
    python3 scripts/gsc.py --property sc-domain:homeeins.de --out daten
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# Search-Console-Daten sind zwei bis drei Tage verzögert. Ohne diesen
# Versatz sieht der letzte Tag künstlich schwach aus.
VERZUG_TAGE = 3
ZEITRAUM_TAGE = 28

EINRICHTUNG = """
Keine Zugangsdaten gefunden — weder Application Default Credentials noch
GSC_SERVICE_ACCOUNT_JSON.

Vorgesehen ist Workload Identity Federation: GitHub Actions weist sich
direkt bei Google aus, es existiert kein Schluessel. Dafuer braucht es
einmalig in der Google Cloud Shell:

  gcloud services enable iamcredentials.googleapis.com sts.googleapis.com

  gcloud iam workload-identity-pools create github --location=global

  gcloud iam workload-identity-pools providers create-oidc github-provider \\
    --location=global --workload-identity-pool=github \\
    --issuer-uri="https://token.actions.githubusercontent.com" \\
    --attribute-mapping="google.subject=assertion.sub,\\
attribute.repository=assertion.repository,\\
attribute.repository_owner=assertion.repository_owner" \\
    --attribute-condition="assertion.repository_owner=='alanzshops-tech'"

  gcloud iam service-accounts add-iam-policy-binding <DIENSTKONTO-MAIL> \\
    --role=roles/iam.workloadIdentityUser \\
    --member="principalSet://iam.googleapis.com/projects/<PROJEKTNUMMER>\\
/locations/global/workloadIdentityPools/github/attribute.repository/\\
alanzshops-tech/ponytail-test"

Ausserdem muss die E-Mail des Dienstkontos in der Search Console unter
Einstellungen -> Nutzer und Berechtigungen als Nutzer eingetragen sein
("Eingeschraenkt" genuegt).
"""


def dienst():
    """Zugang holen. Erst ADC (Workload Identity Federation), dann als
    Rueckfallebene eine Schluesseldatei aus der Umgebung.

    Die Google-Bibliotheken werden bewusst erst importiert, wenn
    Zugangsdaten vorliegen. Sonst bekaeme jemand ohne installierte
    Abhaengigkeiten einen Traceback statt der Einrichtungsanleitung."""
    zugang = None
    quelle = ""

    roh = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if roh:
        try:
            info = json.loads(roh)
        except ValueError as e:
            sys.exit(f"GSC_SERVICE_ACCOUNT_JSON ist kein gültiges JSON: {e}")
        from google.oauth2 import service_account
        zugang = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES)
        quelle = "Dienstkonto-Schlüssel aus der Umgebung"
    else:
        try:
            import google.auth
            from google.auth.exceptions import DefaultCredentialsError
        except ImportError:
            print(EINRICHTUNG)
            return None
        try:
            zugang, _ = google.auth.default(scopes=SCOPES)
            quelle = "Application Default Credentials (Workload Identity)"
        except DefaultCredentialsError:
            print(EINRICHTUNG)
            return None

    from googleapiclient.discovery import build
    print(f"Zugang über: {quelle}")
    # cache_discovery=False vermeidet eine Warnung ohne beschreibbaren Cache.
    return build("searchconsole", "v1", credentials=zugang,
                 cache_discovery=False)


def abfragen(api, property_url: str, start: date, ende: date,
             dimensionen: list[str], limit: int = 500) -> list[dict]:
    rumpf = {
        "startDate": start.isoformat(),
        "endDate": ende.isoformat(),
        "dimensions": dimensionen,
        "rowLimit": limit,
    }
    antwort = api.searchanalytics().query(
        siteUrl=property_url, body=rumpf).execute()
    zeilen = []
    for r in antwort.get("rows", []):
        eintrag = {d: k for d, k in zip(dimensionen, r.get("keys", []))}
        eintrag.update({
            "klicks": r.get("clicks", 0),
            "impressionen": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1),
        })
        zeilen.append(eintrag)
    return zeilen


def summe(zeilen: list[dict]) -> dict:
    k = sum(z["klicks"] for z in zeilen)
    i = sum(z["impressionen"] for z in zeilen)
    # Position gewichtet nach Impressionen mitteln - ein einfacher
    # Durchschnitt ueber Zeilen waere verzerrt.
    pos = (sum(z["position"] * z["impressionen"] for z in zeilen) / i) if i else 0
    return {"klicks": k, "impressionen": i,
            "ctr": round(k / i * 100, 2) if i else 0,
            "position": round(pos, 1)}


def veraenderung(jetzt: float, vorher: float) -> str:
    if not vorher:
        return "neu" if jetzt else "–"
    p = round((jetzt - vorher) / vorher * 100)
    return f"{p:+d} %"


def bericht(d: dict) -> str:
    a, b = d["aktuell"], d["vorher"]
    z = ["# Google Search Console — homeeins", "",
         f"Zeitraum: {d['start']} bis {d['ende']} "
         f"({ZEITRAUM_TAGE} Tage) · Vergleich mit den {ZEITRAUM_TAGE} Tagen davor",
         "",
         "| | Aktuell | Vorher | Veränderung |",
         "|---|---:|---:|---:|",
         f"| Klicks | {a['klicks']} | {b['klicks']} | "
         f"{veraenderung(a['klicks'], b['klicks'])} |",
         f"| Impressionen | {a['impressionen']} | {b['impressionen']} | "
         f"{veraenderung(a['impressionen'], b['impressionen'])} |",
         f"| CTR | {a['ctr']} % | {b['ctr']} % | |",
         f"| Ø Position | {a['position']} | {b['position']} | |", ""]

    chancen = [q for q in d["anfragen"]
               if 5 <= q["position"] <= 20 and q["impressionen"] >= 5]
    z.append("## Anfragen auf Position 5–20")
    z.append("")
    if chancen:
        z.append("Hier ist Reichweite da, aber die erste Seite fehlt knapp. "
                 "Der wirksamste Hebel im ganzen Bericht.")
        z.append("")
        z.append("| Anfrage | Position | Impressionen | Klicks | CTR |")
        z.append("|---|---:|---:|---:|---:|")
        for q in sorted(chancen, key=lambda x: -x["impressionen"])[:20]:
            z.append(f"| {q['query']} | {q['position']} | {q['impressionen']} "
                     f"| {q['klicks']} | {q['ctr']} % |")
    else:
        z.append("Keine. Alles steht entweder sehr weit vorn oder jenseits "
                 "von Position 20 — bei einer neuen Domain der Normalfall.")
    z.append("")

    z.append("## Meiste Impressionen")
    z.append("")
    z.append("| Anfrage | Impressionen | Klicks | Position |")
    z.append("|---|---:|---:|---:|")
    for q in sorted(d["anfragen"], key=lambda x: -x["impressionen"])[:25]:
        z.append(f"| {q['query']} | {q['impressionen']} | {q['klicks']} "
                 f"| {q['position']} |")
    z.append("")

    tote = [p for p in d["seiten"] if p["klicks"] == 0
            and p["impressionen"] >= 10]
    if tote:
        z.append("## Seiten mit Impressionen, aber ohne Klicks")
        z.append("")
        z.append("Werden gefunden, aber nicht angeklickt: entweder zu weit "
                 "hinten oder Titel und Beschreibung überzeugen nicht.")
        z.append("")
        z.append("| Seite | Impressionen | Position |")
        z.append("|---|---:|---:|")
        for p in sorted(tote, key=lambda x: -x["impressionen"])[:15]:
            z.append(f"| {p['page']} | {p['impressionen']} | {p['position']} |")
        z.append("")

    if d.get("geraete"):
        z.append("## Geräte")
        z.append("")
        z.append("| Gerät | Klicks | Impressionen | CTR | Position |")
        z.append("|---|---:|---:|---:|---:|")
        for g in d["geraete"]:
            z.append(f"| {g['device']} | {g['klicks']} | {g['impressionen']} "
                     f"| {g['ctr']} % | {g['position']} |")
        z.append("")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--property", default="sc-domain:homeeins.de")
    ap.add_argument("--out", default="daten")
    ap.add_argument("--tage", type=int, default=ZEITRAUM_TAGE)
    a = ap.parse_args()

    api = dienst()
    if api is None:
        # Kein Abbruch: Der Workflow soll nicht rot sein, nur weil die
        # Zugangsdaten noch fehlen. Die Anleitung steht oben im Log.
        return

    ende = date.today() - timedelta(days=VERZUG_TAGE)
    start = ende - timedelta(days=a.tage - 1)
    v_ende = start - timedelta(days=1)
    v_start = v_ende - timedelta(days=a.tage - 1)

    print(f"Zeitraum {start} bis {ende}, Vergleich {v_start} bis {v_ende}")

    anfragen = abfragen(api, a.property, start, ende, ["query"])
    seiten = abfragen(api, a.property, start, ende, ["page"])
    geraete = abfragen(api, a.property, start, ende, ["device"])
    verlauf = abfragen(api, a.property, start, ende, ["date"], limit=100)
    v_anfragen = abfragen(api, a.property, v_start, v_ende, ["query"])

    daten = {
        "stand": str(date.today()), "property": a.property,
        "start": str(start), "ende": str(ende),
        "aktuell": summe(anfragen), "vorher": summe(v_anfragen),
        "anfragen": anfragen, "seiten": seiten,
        "geraete": geraete, "verlauf": verlauf,
    }

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    (out / f"gsc-{daten['stand']}.json").write_text(text, encoding="utf-8")
    (out / "gsc-aktuell.json").write_text(text, encoding="utf-8")
    Path("GSC.md").write_text(bericht(daten), encoding="utf-8")

    s = daten["aktuell"]
    print(f"{len(anfragen)} Anfragen, {len(seiten)} Seiten. "
          f"{s['klicks']} Klicks, {s['impressionen']} Impressionen, "
          f"Ø Position {s['position']}")


if __name__ == "__main__":
    main()
