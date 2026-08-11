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
  - Seite + Anfrage zusammen (welche Anfrage gehört zu welcher Seite)
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


MIN_IMPR = 5   # Schwelle, ab der eine Zeile als belastbar gilt


def anfragen_je_seite(d: dict, seiten: list[dict]) -> list[str]:
    """Welche Suchanfrage gehoert zu welcher Seite.

    Ohne diese Zuordnung laesst sich ein Snippet nur raten: man sieht,
    dass eine Seite auf Position 2 steht und null Klicks bekommt, aber
    nicht, worauf sie steht. Title und Description muessen zur Anfrage
    passen, nicht zum Produkt.

    Der Bezugsrahmen ist hier besonders wichtig. Die Kombination
    page+query verliert alle anonymisierten Anfragen -- eine Seite mit 28
    Impressionen kann in dieser Abfrage mit 4 auftauchen. Deshalb steht
    bei jeder Seite, wieviel von ihren Impressionen ueberhaupt sichtbar
    ist. Und deshalb wird "keine Anfrage sichtbar" ausdruecklich als
    Ergebnis ausgewiesen und nicht stillschweigend uebersprungen: es ist
    ein anderer Befund als "keine Daten geholt".
    """
    if "seiten_anfragen" not in d:
        return []                    # aeltere Datei, Abfrage gab es noch nicht
    if not seiten:
        return []

    nach_seite: dict[str, list[dict]] = {}
    for r in d["seiten_anfragen"]:
        nach_seite.setdefault(r["page"], []).append(r)

    z = ["## Wonach diese Seiten gefunden werden", "",
         "Ohne die Anfrage ist jede Snippet-Änderung geraten. "
         "Die Kombination Seite+Anfrage zeigt nur die nicht anonymisierten "
         "Anfragen — die Spalte „sichtbar“ sagt, auf wieviel der "
         "Impressionen sich die Zeilen darunter überhaupt stützen.", ""]

    for p in sorted(seiten, key=lambda x: -x["impressionen"]):
        treffer = sorted(nach_seite.get(p["page"], []),
                         key=lambda x: -x["impressionen"])
        sichtbar = sum(t["impressionen"] for t in treffer)
        anteil = round(sichtbar / p["impressionen"] * 100) if p["impressionen"] else 0
        z.append(f"### {p['page']}")
        z.append("")
        z.append(f"Position {p['position']}, {p['impressionen']} Impressionen, "
                 f"0 Klicks. Über Anfragen sichtbar: {sichtbar} ({anteil} %).")
        if "/en/" in p["page"] or p["page"].rstrip("/").endswith("/en"):
            z.append("")
            z.append("> Abgeschaltete Sprachfassung. Seit dem 09.08.2026 "
                     "antwortet `/en/` mit 404 oder leitet auf die deutsche "
                     "Seite um — hier ist **nichts zu optimieren**. Steht "
                     "diese Zeile in einem Bericht, dessen Zeitraum vor dem "
                     "09.08.2026 endet, beschreibt sie einen bereits "
                     "behobenen Zustand.")
        z.append("")
        if treffer:
            z.append("| Anfrage | Impressionen | Position |")
            z.append("|---|---:|---:|")
            for t in treffer[:10]:
                z.append(f"| {t['query']} | {t['impressionen']} "
                         f"| {t['position']} |")
        else:
            z.append("Keine einzige Anfrage sichtbar — alle Impressionen "
                     "dieser Seite sind anonymisiert. Für diese Seite lässt "
                     "sich das Snippet **nicht** datengestützt schreiben.")
        z.append("")
    return z


def bericht(d: dict) -> str:
    a, b = d["aktuell"], d["vorher"]
    q_impr = sum(q["impressionen"] for q in d["anfragen"])
    p_impr = sum(p["impressionen"] for p in d["seiten"])

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

    # Diese Lücke ist kein Nebenschauplatz. Google verschweigt seltene
    # Anfragen aus Datenschutzgründen. Die Kennzahlen oben stammen aus der
    # Anfragen-Dimension und beschreiben deshalb nur einen Ausschnitt -
    # meist den schlechteren, weil Markensuchen anonymisiert werden.
    if p_impr > q_impr:
        z += [f"> **{p_impr - q_impr} von {p_impr} Impressionen sind "
              f"anonymisiert.** Über Suchanfragen sichtbar: {q_impr}. "
              f"Über Seiten sichtbar: {p_impr}. Die Kennzahlen oben stammen "
              f"aus der Anfragen-Dimension und zeigen daher nur den "
              f"sichtbaren Rest — die Durchschnittsposition ist dadurch "
              f"schlechter, als die Domain tatsächlich steht.", ""]

    # Wichtigster Abschnitt: Seiten, die vorn stehen und trotzdem nicht
    # geklickt werden. Rankings sind da, es hakt am Snippet oder an der
    # Absicht dahinter - das ist behebbar, anders als fehlende Autoritaet.
    vorn = [p for p in d["seiten"]
            if p["position"] <= 5 and p["impressionen"] >= MIN_IMPR]
    ungenutzt = [p for p in vorn if p["klicks"] == 0]
    z.append("## Seiten auf Position 1–5")
    z.append("")
    if vorn:
        z.append(f"{len(vorn)} Seiten stehen weit vorn, "
                 f"{len(ungenutzt)} davon ohne einen einzigen Klick. "
                 f"Wo Ranking da ist und Klicks fehlen, liegt es am "
                 f"Snippet, an der Sprache oder an der Suchabsicht — "
                 f"nicht an fehlender Autorität.")
        z.append("")
        z.append("| Seite | Position | Impressionen | Klicks |")
        z.append("|---|---:|---:|---:|")
        for p in sorted(vorn, key=lambda x: -x["impressionen"])[:20]:
            z.append(f"| {p['page']} | {p['position']} | "
                     f"{p['impressionen']} | {p['klicks']} |")
    else:
        z.append(f"Keine Seite mit mindestens {MIN_IMPR} Impressionen steht "
                 f"unter Position 5.")
    z.append("")
    z += anfragen_je_seite(d, ungenutzt)

    chancen = [q for q in d["anfragen"]
               if 5 <= q["position"] <= 20 and q["impressionen"] >= MIN_IMPR]
    knapp = [q for q in d["anfragen"]
             if 5 <= q["position"] <= 20 and q["impressionen"] < MIN_IMPR]
    z.append("## Anfragen auf Position 5–20")
    z.append("")
    if chancen:
        z.append("Hier ist Reichweite da, aber die erste Seite fehlt knapp.")
        z.append("")
        z.append("| Anfrage | Position | Impressionen | Klicks | CTR |")
        z.append("|---|---:|---:|---:|---:|")
        for q in sorted(chancen, key=lambda x: -x["impressionen"])[:20]:
            z.append(f"| {q['query']} | {q['position']} | {q['impressionen']} "
                     f"| {q['klicks']} | {q['ctr']} % |")
    else:
        z.append(f"Keine mit mindestens {MIN_IMPR} Impressionen.")
    if knapp:
        # Nicht verschweigen: unterhalb der Schwelle steht oft das, woraus
        # sich morgen etwas entwickelt.
        namen = ", ".join(f"{q['query']} ({q['position']})"
                          for q in sorted(knapp, key=lambda x: x["position"])[:8])
        z.append("")
        z.append(f"Unterhalb der Schwelle, mit weniger als {MIN_IMPR} "
                 f"Impressionen: {namen}")
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
            and p["impressionen"] >= 10 and p["position"] > 5]
    if tote:
        z.append("## Weiter hinten, ohne Klicks")
        z.append("")
        z.append("Werden gefunden, aber nicht angeklickt — hier vermutlich "
                 "schlicht wegen der Position.")
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

    # Ein 403 ist kein Absturz, sondern eine fehlende Freigabe. Mit
    # Traceback sucht man an der falschen Stelle.
    from googleapiclient.errors import HttpError
    try:
        _ = abfragen(api, a.property, start, ende, ["date"], limit=1)
    except HttpError as e:
        if e.resp.status in (401, 403):
            sys.exit(
                f"Kein Zugriff auf {a.property} (HTTP {e.resp.status}).\n"
                f"Das Dienstkonto weist sich korrekt aus, ist in der Search "
                f"Console aber nicht als Nutzer eingetragen.\n"
                f"search.google.com/search-console -> Einstellungen -> "
                f"Nutzer und Berechtigungen -> Nutzer hinzufügen "
                f"('Eingeschränkt' genügt).")
        raise

    anfragen = abfragen(api, a.property, start, ende, ["query"])
    seiten = abfragen(api, a.property, start, ende, ["page"])
    # Die Kombination beantwortet die einzige Frage, die zaehlt, wenn ein
    # Snippet umgeschrieben werden soll: worauf steht diese Seite? Ein
    # hoeheres Limit als sonst, weil jede Seite mehrere Anfragen hat.
    seiten_anfragen = abfragen(api, a.property, start, ende,
                               ["page", "query"], limit=2500)
    geraete = abfragen(api, a.property, start, ende, ["device"])
    verlauf = abfragen(api, a.property, start, ende, ["date"], limit=100)
    v_anfragen = abfragen(api, a.property, v_start, v_ende, ["query"])

    daten = {
        "stand": str(date.today()), "property": a.property,
        "start": str(start), "ende": str(ende),
        "aktuell": summe(anfragen), "vorher": summe(v_anfragen),
        "anfragen": anfragen, "seiten": seiten,
        "seiten_anfragen": seiten_anfragen,
        "geraete": geraete, "verlauf": verlauf,
    }

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    (out / f"gsc-{daten['stand']}.json").write_text(text, encoding="utf-8")
    (out / "gsc-aktuell.json").write_text(text, encoding="utf-8")
    Path("GSC.md").write_text(bericht(daten), encoding="utf-8")

    s = daten["aktuell"]
    print(f"{len(anfragen)} Anfragen, {len(seiten)} Seiten, "
          f"{len(seiten_anfragen)} Seite+Anfrage-Paare. "
          f"{s['klicks']} Klicks, {s['impressionen']} Impressionen, "
          f"Ø Position {s['position']}")
    if len(seiten_anfragen) >= 2500:
        print("WARNUNG: Zeilenlimit erreicht, die Zuordnung ist "
              "unvollstaendig. Limit erhoehen.")


if __name__ == "__main__":
    main()
