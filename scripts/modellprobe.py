"""Taugen die billigen Modelle fuer Produkttexte? Gemessen, nicht geraten.

Die Frage ist nicht "klingt es gut" -- das laesst sich nachlesen. Die
Frage ist, ob ein Modell Tatsachen erfindet und ob es die Regeln dieses
Ladens einhaelt. Beides ist zaehlbar:

  ERFUNDENE ZAHLEN  Jede Zahl im Text, die nicht in der Aufgabe stand.
                    Bei Moebeln ist das der teuerste Fehler: "waschbar
                    bei 60 Grad" oder "3 cm dick" steht sonst als
                    Zusicherung im Shop, ohne dass es jemand geprueft hat.
  DARK PATTERNS     Erfundene Knappheit, Streichpreise, "X Leute sehen
                    sich das an". In der EU verboten (Omnibus-Richtlinie,
                    § 5b UWG). Ein Modell, das sowas von selbst
                    dazuschreibt, ist fuer diesen Shop unbrauchbar.
  DEUTSCH           Englische Reste sind der haeufigste Ausfall billiger
                    Modelle bei deutschen Aufgaben.
  LAENGE, DAUER, KOSTEN

Die Aufgaben stehen fest in daten/modellprobe-aufgaben.json -- ein
wechselnder Text waere kein Vergleich.

Laeuft auf dem Runner; die Arbeitsumgebung erreicht openrouter.ai nicht.

    python3 scripts/modellprobe.py --modelle a,b,c
"""
from __future__ import annotations

import argparse
import json
import re
import time
from datetime import date
from pathlib import Path

import openrouter as o

AUFTRAG = (
    "Du schreibst für einen deutschen Online-Shop für Wohnaccessoires.\n"
    "Schreibe eine Produktbeschreibung von 60 bis 90 Wörtern.\n\n"
    "Regeln:\n"
    "- Nur Tatsachen aus den Angaben unten. Erfinde keine Maße, Gewichte, "
    "Materialien, Temperaturen oder Prozentwerte.\n"
    "- Keine Knappheit, keine Streichpreise, keine Bewertungen, keine "
    "Behauptungen über andere Käufer.\n"
    "- Sachlicher deutscher Fließtext, keine Aufzählung, keine Überschrift.\n\n"
    "Angaben:\n{angaben}"
)

# Muster fuer verbotene Werbemaschen. Jedes einzelne ist unten in
# probe_modellprobe.py gegen einen Treffer- UND einen Nicht-Treffer-Fall
# geprueft -- ein Muster wie "nur noch" allein wuerde "nur noch besser"
# faelschlich fangen, und genau solche Selektoren haben in diesem Projekt
# schon dreimal falsche Befunde erzeugt.
MASCHEN = {
    "Knappheit": r"nur noch \d+|nur \d+ (?:Stück|Exemplare)|letzte[nr]? \d+",
    "Zeitdruck": r"nur (?:heute|jetzt)|Angebot endet|noch \d+ Stunden",
    "Streichpreis": r"statt \d+[,.]\d{2}|UVP \d|ehemals \d+[,.]\d{2}",
    "Publikum": r"\d+ (?:Personen|Leute|Kunden) (?:sehen|schauen|kauften)",
    "Rang": r"\bBestseller\b|beliebtestes? Produkt|Nummer 1",
}

# Englische Woerter, die in einem deutschen Produkttext nichts verloren
# haben. Bewusst nur eindeutige -- "Set" und "Design" sind im Deutschen
# gebraeuchlich und stehen deshalb nicht drin.
ENGLISCH = r"\b(?:the|and|with|your|our|for|this|that|from|comfort|soft|quality|features?|perfect|premium quality)\b"

# Ausgeplaudertes Denken. Nemotron 3 Ultra lieferte am 10.08.2026 seinen
# kompletten Gedankengang als Produkttext aus -- "The user wants...",
# "Constraints:", "Drafting:", dann eine Wortzaehlung, bis das
# Token-Budget alle war. Das ist ein eigener Ausfall und gehoert nicht
# unter "erfundene Zahlen" einsortiert: dort hat es die Zahl aufgeblaeht
# und schlimmer ausgesehen, als es war.
GEDANKEN = r"(?:the user (?:wants|asked)|constraints?:|drafting:|word count|let me (?:think|draft|write)|I (?:need|should|will) (?:to )?(?:write|draft|check)|here'?s? (?:my|the) (?:draft|response))"


def zahlen(text: str) -> set[str]:
    """Zahlen normalisiert, damit 5,0 und 5.0 und 5 dasselbe sind."""
    roh = re.findall(r"\d+(?:[.,]\d+)?", text)
    aus = set()
    for z in roh:
        w = z.replace(",", ".")
        try:
            f = float(w)
        except ValueError:
            continue
        aus.add(str(int(f)) if f == int(f) else str(f))
    return aus


def erfundene_zahlen(antwort: str, angaben: str) -> list[str]:
    """Zahlen im Text, die in der Aufgabe nicht vorkamen.

    Ein- und zweistellige Zaehlzahlen bleiben aussen vor: "zwei Körbe"
    oder "in 3 Größen" sind Formulierung, keine Zusicherung. Gefaehrlich
    sind Masse, Gewichte, Temperaturen und Prozente -- die stehen sonst
    als Eigenschaft im Shop, ohne dass sie jemand geprueft hat.
    """
    drin = zahlen(angaben)
    return sorted(z for z in zahlen(antwort)
                  if z not in drin and float(z) > 10)


def maschen(text: str) -> list[str]:
    return [name for name, m in MASCHEN.items()
            if re.search(m, text, re.I)]


def englisch(text: str) -> list[str]:
    return sorted({w.lower() for w in re.findall(ENGLISCH, text, re.I)})


def gedanken(text: str) -> list[str]:
    return sorted({t.lower() for t in re.findall(GEDANKEN, text, re.I)})


def messen(antwort: str, angaben: str) -> dict:
    geplaudert = gedanken(antwort)
    return {
        "woerter": len(antwort.split()),
        # Plaudert das Modell sein Denken aus, sind die Zahlen darin
        # Wortzaehlerei und zitierte Vorgaben, keine erfundenen
        # Produktangaben. Getrennt ausweisen, statt eine Zahl zu melden,
        # die schlimmer klingt, als sie ist.
        "erfundene_zahlen": [] if geplaudert else erfundene_zahlen(antwort, angaben),
        "gedanken_im_text": geplaudert,
        "maschen": maschen(antwort),
        "englisch": englisch(antwort),
    }


def angaben_text(a: dict) -> str:
    return (f"Titel: {a['titel']}\n"
            f"Kategorie: {a['art']}\n"
            f"Schlagworte: {', '.join(a['schlagworte'])}\n"
            f"Preis: {a['preis']}\n"
            f"Varianten: {'; '.join(a['varianten'])}")


def einen(modell: str, a: dict, denken: str | None = None) -> dict:
    angaben = angaben_text(a)
    last = {
        "model": modell,
        "messages": [{"role": "user",
                      "content": AUFTRAG.format(angaben=angaben)}],
        "max_tokens": 400,
    }
    # `reasoning.effort` kennt laut @openrouter/sdk die Stufen none,
    # minimal, low, medium, high, max, xhigh. Ohne Angabe entscheidet das
    # Modell -- und ein Reasoning-Modell denkt dann sichtbar. Genau das
    # ist am 10.08.2026 passiert, weil ich den Schalter nicht kannte.
    if denken:
        last["reasoning"] = {"effort": denken}
    start = time.time()
    r = o.rufen("/chat/completions", last)
    dauer = round(time.time() - start, 1)
    if "fehler" in r:
        return {"aufgabe": a["kennung"], "fehler": r["fehler"],
                "text": (r.get("text") or "")[:160], "dauer": dauer}
    wahl = (r.get("choices") or [{}])[0]
    inhalt = ((wahl.get("message") or {}).get("content") or "").strip()
    if not inhalt:
        return {"aufgabe": a["kennung"], "fehler": "leere Antwort",
                "dauer": dauer}
    v = r.get("usage") or {}
    return {"aufgabe": a["kennung"], "antwort": inhalt, "dauer": dauer,
            "kosten": v.get("cost"), "token": v.get("total_tokens"),
            **messen(inhalt, angaben)}


def bericht(d: dict) -> str:
    z = [f"# Modellvergleich für Produkttexte — Stand {d['stand']}", "",
         "Dieselben drei echten Produkte an jedes Modell, derselbe Auftrag.",
         "Gemessen wird nicht, ob es schön klingt, sondern ob es Tatsachen",
         "erfindet und die Regeln des Ladens einhält.", "",
         "**Erfundene Zahlen** sind der teure Fehler: eine Zahl über 10, die",
         "in den Angaben nicht vorkam, steht danach als Zusicherung im Shop",
         "— „waschbar bei 60 Grad“, „3 cm dick“ — ohne dass sie jemand",
         "geprüft hat. Kleine Zählzahlen bleiben außen vor, die sind",
         "Formulierung.", "",
         "**Denken im Text** ist ein eigener Ausfall, kein erfundener",
         "Fakt: ein Reasoning-Modell ohne gesetztes `reasoning.effort`",
         "liefert seinen Gedankengang als Produkttext aus. Die Zahlen darin",
         "sind Wortzählerei, keine Zusicherungen — deshalb getrennt gezählt.",
         "",
         "| Modell | Läufe | Fehler | Wörter ⌀ | erfundene Zahlen "
         "| Denken im Text | Maschen | englische Reste | Dauer ⌀ | Kosten |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for m, laeufe in d["modelle"].items():
        gut = [x for x in laeufe if "antwort" in x]
        schlecht = len(laeufe) - len(gut)
        if not gut:
            z.append(f"| `{m}` | {len(laeufe)} | **{schlecht}** | – | – | – "
                     f"| – | – | – | – |")
            continue
        wo = sum(x["woerter"] for x in gut) / len(gut)
        zahl = sum(len(x["erfundene_zahlen"]) for x in gut)
        mas = sum(len(x["maschen"]) for x in gut)
        eng = sum(len(x["englisch"]) for x in gut)
        ged = sum(1 for x in gut if x.get("gedanken_im_text"))
        dau = sum(x["dauer"] for x in gut) / len(gut)
        kos = sum(x.get("kosten") or 0 for x in gut)
        z.append(f"| `{m}` | {len(laeufe)} | {schlecht} | {wo:.0f} "
                 f"| {zahl} | {ged} | {mas} | {eng} | {dau:.1f} s "
                 f"| {kos:.6f} $ |")
    z.append("")

    for m, laeufe in d["modelle"].items():
        z += [f"## {m}", ""]
        for x in laeufe:
            z.append(f"**{x['aufgabe']}** — {x['dauer']} s")
            if "fehler" in x:
                z += ["", f"Fehlgeschlagen: {x['fehler']} {x.get('text', '')}",
                      ""]
                continue
            hin = []
            if x["erfundene_zahlen"]:
                hin.append("erfundene Zahlen: " + ", ".join(x["erfundene_zahlen"]))
            if x.get("gedanken_im_text"):
                hin.append("Denken im Text: "
                           + ", ".join(x["gedanken_im_text"]))
            if x["maschen"]:
                hin.append("Maschen: " + ", ".join(x["maschen"]))
            if x["englisch"]:
                hin.append("englisch: " + ", ".join(x["englisch"]))
            z += ["", "```", x["antwort"], "```", ""]
            z.append(("**Befund:** " + "; ".join(hin)) if hin
                     else "Befund: nichts zu beanstanden.")
            z.append("")
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelle", required=True,
                    help="Komma-getrennte Modell-IDs. Ein Anhang "
                         "@none/@minimal/@low usw. setzt reasoning.effort "
                         "fuer dieses Modell, z. B. nvidia/foo:free@none")
    ap.add_argument("--aufgaben", default="daten/modellprobe-aufgaben.json")
    ap.add_argument("--bericht", default="MODELLPROBE.md")
    ap.add_argument("--json", default="daten/modellprobe.json")
    a = ap.parse_args()

    aufgaben = json.loads(Path(a.aufgaben).read_text(encoding="utf-8"))["aufgaben"]
    d = {"stand": str(date.today()), "modelle": {}}
    for eintrag in [x.strip() for x in a.modelle.split(",") if x.strip()]:
        # "modell@none" heisst: dasselbe Modell, aber ohne sichtbares
        # Denken. So laesst sich beides im selben Lauf nebeneinander
        # stellen, statt zwei Laeufe zu vergleichen, zwischen denen sich
        # die Drosselung geaendert haben kann.
        m, _, denken = eintrag.partition("@")
        print(f"\n=== {eintrag} ===")
        d["modelle"][eintrag] = []
        for auf in aufgaben:
            r = einen(m, auf, denken or None)
            d["modelle"][eintrag].append(r)
            print(f"  {auf['kennung']:<16} "
                  + (f"FEHLER {r['fehler']}" if "fehler" in r
                     else f"{r['woerter']} Wörter, {r['dauer']} s, "
                          f"{len(r['erfundene_zahlen'])} erfundene Zahlen"))

    Path(a.json).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json).write_text(json.dumps(d, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    Path(a.bericht).write_text(bericht(d), encoding="utf-8")
    print(f"\nGeschrieben: {a.bericht}, {a.json}")


if __name__ == "__main__":
    main()
