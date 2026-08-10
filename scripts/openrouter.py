"""OpenRouter: Zugang pruefen und eine echte Antwort holen.

OpenRouter ist ein Vermittler. Eine Adresse, ein Schluessel, dahinter die
Modelle vieler Anbieter. Die Schnittstelle ist OpenAI-kompatibel.

Alles hier ist am Paket @openrouter/sdk 1.2.18 (Apache-2.0) nachgesehen,
nicht aus einer Anleitung uebernommen:

    Basis            https://openrouter.ai/api/v1
    Anmeldung        Authorization: Bearer <Schluessel>
    Endpunkte        /key /credits /models /chat/completions /generation

Kein SDK noetig, urllib reicht -- eine Abhaengigkeit weniger, die altern
kann.

DER SCHLUESSEL steht in der Umgebungsvariablen OPENROUTER_API_KEY und
nirgends sonst. Nicht im Repository, nicht in einem Befehl, nicht in der
Ausgabe. Das Skript zeigt nur seine Laenge.

DIE ARBEITSUMGEBUNG ERREICHT OPENROUTER NICHT. Nur GitHub, PyPI und npm.
Dieses Skript laeuft auf dem Runner, das Ergebnis kommt als Commit
zurueck -- so wie jedes andere Werkzeug hier.

    python3 scripts/openrouter.py --pruefen
    python3 scripts/openrouter.py --fragen "Ein Satz ueber Hundesofas."
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

BASIS = "https://openrouter.ai/api/v1"
# OpenRouter bittet um diese beiden Kopfzeilen, damit Aufrufe zuordenbar
# sind. Sie sind freiwillig und enthalten nichts Geheimes.
HERKUNFT = "https://www.homeeins.de"
TITEL = "Homeeins Werkzeuge"


def schluessel() -> str:
    s = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not s:
        sys.exit("OPENROUTER_API_KEY fehlt. Gehoert in die GitHub Secrets, "
                 "nicht in eine Datei.")
    return s


def rufen(pfad: str, last: dict | None = None, zeit: int = 90) -> dict:
    """Ein Aufruf. Gibt bei einem Fehler den Text des Dienstes zurueck --
    „HTTP 401" allein sagt nicht, ob der Schluessel falsch ist oder das
    Guthaben leer."""
    kopf = {
        "Authorization": f"Bearer {schluessel()}",
        "Content-Type": "application/json",
        "HTTP-Referer": HERKUNFT,
        "X-Title": TITEL,
    }
    daten = json.dumps(last).encode() if last is not None else None
    anfrage = urllib.request.Request(f"{BASIS}{pfad}", data=daten,
                                     headers=kopf,
                                     method="POST" if daten else "GET")
    try:
        with urllib.request.urlopen(anfrage, timeout=zeit) as a:
            return json.loads(a.read().decode())
    except urllib.error.HTTPError as e:
        text = e.read().decode(errors="replace")[:400]
        return {"fehler": f"HTTP {e.code}", "text": text}
    except Exception as e:                                       # noqa: BLE001
        return {"fehler": str(e)[:200]}


def preis(m: dict) -> tuple[float, float]:
    """Preise kommen als Zeichenkette in Dollar je Token. Umgerechnet auf
    eine Million Token, sonst liest man Nullen."""
    p = m.get("pricing") or {}
    def z(w: str) -> float:
        try:
            return float(p.get(w) or 0) * 1_000_000
        except (TypeError, ValueError):
            return 0.0
    return z("prompt"), z("completion")


def guenstigstes(modelle: list[dict]) -> dict | None:
    """Das billigste Modell, das ueberhaupt etwas kostet -- ein kostenloses
    waere fuer einen Verbindungstest zwar schoen, ist aber oft ueberlastet
    und beweist dann nichts."""
    mit = [(sum(preis(m)), m) for m in modelle if sum(preis(m)) > 0]
    return min(mit, key=lambda x: x[0])[1] if mit else None


def pruefen() -> dict:
    d: dict = {"stand": str(date.today())}
    s = schluessel()
    print(f"Schluessel vorhanden, {len(s)} Zeichen.")

    d["schluessel"] = rufen("/key")
    d["guthaben"] = rufen("/credits")

    modelle = rufen("/models")
    liste = modelle.get("data") if isinstance(modelle, dict) else None
    if not isinstance(liste, list):
        d["modelle_fehler"] = modelle
        d["modelle"] = []
    else:
        d["modelle"] = [
            {"id": m.get("id"), "name": m.get("name"),
             "kontext": m.get("context_length"),
             "preis_eingabe": round(preis(m)[0], 4),
             "preis_ausgabe": round(preis(m)[1], 4)}
            for m in liste
        ]
        d["kostenlos"] = [m["id"] for m in d["modelle"]
                          if m["preis_eingabe"] == 0 and m["preis_ausgabe"] == 0]
        g = guenstigstes(liste)
        d["guenstigstes"] = g.get("id") if g else None
    return d


def fragen(text: str, modell: str | None = None) -> dict:
    """Ein echter Rundlauf. Ohne den ist „Zugang funktioniert" nur eine
    Behauptung ueber /key -- lesen darf ein Schluessel oft auch dann, wenn
    das Guthaben fuer eine Antwort nicht reicht."""
    if not modell:
        m = rufen("/models")
        liste = m.get("data") if isinstance(m, dict) else None
        if not isinstance(liste, list):
            return {"fehler": "Modelliste nicht lesbar", "roh": m}
        g = guenstigstes(liste)
        if not g:
            return {"fehler": "Kein Modell mit Preis gefunden"}
        modell = g.get("id")
    print(f"Modell: {modell}")
    a = rufen("/chat/completions", {
        "model": modell,
        "messages": [{"role": "user", "content": text}],
        "max_tokens": 200,
    })
    if "fehler" in a:
        return {"modell": modell, **a}
    wahl = (a.get("choices") or [{}])[0]
    return {
        "modell": modell,
        "antwort": ((wahl.get("message") or {}).get("content") or "").strip(),
        "verbrauch": a.get("usage"),
    }


def bericht(d: dict) -> str:
    z = [f"# OpenRouter — Stand {d.get('stand', '')}", "",
         "Zugang zu vielen Modellen über eine Adresse. Erhoben auf dem",
         "Runner; die Arbeitsumgebung erreicht openrouter.ai nicht.", ""]

    k = d.get("schluessel") or {}
    kd = k.get("data") if isinstance(k, dict) else None
    z += ["## Schlüssel", ""]
    if "fehler" in k:
        z += [f"**Fehlgeschlagen: {k['fehler']}**", "", "```", k.get("text", ""),
              "```", "",
              "HTTP 401 heißt falscher oder fehlender Schlüssel, 402 heißt",
              "Guthaben leer. Der Text oben sagt, welches von beidem.", ""]
    elif isinstance(kd, dict):
        z += ["| Angabe | Wert |", "|---|---|"]
        for feld, name in (("label", "Bezeichnung"), ("limit", "Grenze"),
                           ("usage", "verbraucht"),
                           ("limit_remaining", "verbleibend"),
                           ("is_free_tier", "Gratisstufe")):
            if feld in kd:
                z.append(f"| {name} | {kd[feld]} |")
        z.append("")

    g = d.get("guthaben") or {}
    gd = g.get("data") if isinstance(g, dict) else None
    if isinstance(gd, dict):
        z += ["## Guthaben", "", "| Angabe | Wert |", "|---|---|"]
        for feld, name in (("total_credits", "eingezahlt"),
                           ("total_usage", "verbraucht")):
            if feld in gd:
                z.append(f"| {name} | {gd[feld]} |")
        z.append("")

    mod = d.get("modelle") or []
    z += ["## Modelle", ""]
    if not mod:
        z += ["Keine Liste erhalten.", ""]
    else:
        frei = d.get("kostenlos") or []
        z += [f"**{len(mod)} Modelle erreichbar**, davon {len(frei)} ohne "
              "Kosten.", "",
              "Die zehn günstigsten mit Preis. Beträge in US-Dollar je",
              "Million Token — Eingabe ist, was hingeschickt wird, Ausgabe,",
              "was zurückkommt.", "",
              "| Modell | Kontext | Eingabe | Ausgabe |", "|---|---:|---:|---:|"]
        bezahlt = sorted(
            (m for m in mod if m["preis_eingabe"] + m["preis_ausgabe"] > 0),
            key=lambda m: m["preis_eingabe"] + m["preis_ausgabe"])
        for m in bezahlt[:10]:
            z.append(f"| `{m['id']}` | {m['kontext'] or '–'} "
                     f"| {m['preis_eingabe']:.4f} $ | {m['preis_ausgabe']:.4f} $ |")
        z.append("")
        if frei:
            z += ["Ohne Kosten, die ersten zehn:", "",
                  ", ".join(f"`{i}`" for i in frei[:10]), "",
                  "Kostenlose Modelle sind gedrosselt und oft überlastet. Für",
                  "eine Messung taugen sie nicht — ein Fehlschlag sagt dann",
                  "nichts über den Zugang.", ""]

    p = d.get("probe")
    if p:
        z += ["## Rundlauf", ""]
        if "fehler" in p:
            z += [f"**Fehlgeschlagen: {p['fehler']}**", "",
                  "```", str(p.get("text") or p.get("roh") or "")[:500], "```", ""]
        else:
            z += [f"Modell `{p.get('modell')}`, Verbrauch "
                  f"`{p.get('verbrauch')}`.", "", "```", p.get("antwort", ""),
                  "```", "",
                  "Erst das beweist den Zugang. `/key` zu lesen gelingt auch",
                  "einem Schlüssel, dessen Guthaben für keine Antwort reicht.",
                  ""]
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefen", action="store_true",
                    help="Schlüssel, Guthaben und Modellliste abfragen")
    ap.add_argument("--fragen", metavar="TEXT",
                    help="einen echten Rundlauf machen")
    ap.add_argument("--modell", help="Modell für --fragen; sonst das günstigste")
    ap.add_argument("--bericht", default="OPENROUTER.md")
    ap.add_argument("--json", default="daten/openrouter.json")
    a = ap.parse_args()

    if not a.pruefen and not a.fragen:
        ap.error("Nichts zu tun: --pruefen oder --fragen angeben.")

    d = pruefen() if a.pruefen else {"stand": str(date.today())}
    if a.fragen:
        d["probe"] = fragen(a.fragen, a.modell)

    Path(a.json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json).write_text(json.dumps(d, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    Path(a.bericht).write_text(bericht(d), encoding="utf-8")
    print(f"Geschrieben: {a.bericht}, {a.json}")

    # Rot werden, wenn der Zugang nicht steht -- ein gruener Lauf mit
    # „HTTP 401" im Bericht waere die schlechteste aller Rueckmeldungen.
    schlecht = [x for x in (d.get("schluessel"), d.get("probe"))
                if isinstance(x, dict) and "fehler" in x]
    if schlecht:
        sys.exit(f"Zugang steht nicht: {schlecht[0]['fehler']}")


if __name__ == "__main__":
    main()
