#!/usr/bin/env python3
"""
lektorat.py — lässt fremde Modelle die Kapitel lesen und prüft nach, ob
sie sie wirklich gelesen haben.

Wozu: `prosa.py` sagt selbst, dass es nicht messen kann, ob eine Szene
trägt. Ich kann das auch nicht — mein Urteil über meine eigene Prosa ist
als Prüfung wertlos. Ein fremdes Modell ist für genau diese Lücke ein
Messgerät. Aber nur, wenn man ihm nicht glaubt, sondern nachrechnet.

**Der Trick: Es muss wörtlich zitieren.** Jede Antwort enthält Zitate
aus dem Kapitel, und dieses Skript prüft für jedes einzelne, ob es
tatsächlich im Text steht. Ein erfundenes Zitat heißt: Das Modell hat
das Kapitel nicht gelesen, sondern etwas Plausibles gesagt. Die Quote
der belegten Zitate steht im Bericht — sie ist die Kalibrierung dieses
Geräts.

**Zwei Modelle, nicht eins.** Wenn zwei unabhängige Modelle dieselbe
Stelle nennen, ist das ein Befund. Wenn sie nichts gemeinsam haben, ist
das Gerät Rauschen, und der Bericht sagt das.

Gefragt wird nichts, was nicht beantwortbar ist. Nicht „ist das gut",
sondern: Wo würdest du aufhören zu lesen. Das hat eine Stelle, und die
Stelle lässt sich zitieren.

Aufruf (läuft auf dem Runner, die Arbeitsumgebung erreicht OpenRouter
nicht):
    python3 scripts/lektorat.py --kapitel 1 2 3 --modelle openai google
    python3 scripts/lektorat.py --selbsttest
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from openrouter import rufen  # noqa: E402

BUCH = Path(__file__).resolve().parent.parent / "buch"
MARKER = ('<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf '
          'erhalten -->')

AUFGABE = """Du liest ein Kapitel aus einem deutschen Liebesroman
(Zeitgenössisch, Reihe „Die Reinhardt-Brüder"). Du bist eine erfahrene
Leserin dieser Nische, keine Lektorin — du sagst, was beim Lesen
passiert, nicht was Regeln verlangen.

Antworte in genau diesem Format, drei Zeilen, sonst nichts:

ABBRUCH: "wörtliches Zitat aus dem Kapitel, 5 bis 12 Wörter" — Grund in einem Satz
UNKLAR: "wörtliches Zitat aus dem Kapitel, 5 bis 12 Wörter" — was daran unklar ist
STARK: "wörtliches Zitat aus dem Kapitel, 5 bis 12 Wörter"

ABBRUCH ist die erste Stelle, an der du das Buch weglegen oder
querlesen würdest. Gibt es keine, schreibe: ABBRUCH: keine
UNKLAR ist eine Stelle, die beim ersten Lesen nicht verständlich ist.
Gibt es keine, schreibe: UNKLAR: keine

Die Zitate müssen **wörtlich** aus dem Kapitel stammen, Zeichen für
Zeichen. Erfinde nichts.

Hier ist das Kapitel:

"""


def normal(t: str) -> str:
    """Vergleichsform: Leerraum vereinheitlichen, typografische
    Sonderzeichen angleichen. Ohne das scheitert der Beleg an einem
    Zeilenumbruch mitten im Zitat."""
    t = t.replace("„", '"').replace("“", '"').replace("’", "'")
    t = t.replace("—", "-").replace("–", "-").replace("…", "...")
    return " ".join(t.split()).lower()


def antwort_lesen(text: str) -> dict:
    raus = {}
    for feld in ("ABBRUCH", "UNKLAR", "STARK"):
        m = re.search(rf"{feld}\s*:\s*(.+?)(?=\n[A-ZÄÖÜ]+\s*:|\Z)",
                      text, re.S)
        if not m:
            continue
        roh = " ".join(m.group(1).split())
        if roh.lower().startswith("keine"):
            raus[feld] = {"zitat": None, "grund": None}
            continue
        z = re.search(r'["„»](.+?)["“«]', roh)
        g = re.split(r"\s+[—–-]\s+", roh, maxsplit=1)
        raus[feld] = {"zitat": z.group(1) if z else None,
                      "grund": g[1] if len(g) > 1 else None}
    return raus


def belegt(zitat: str | None, kapitel: str) -> bool | None:
    """None = kein Zitat angegeben. True = steht wirklich im Text."""
    if not zitat:
        return None
    return normal(zitat) in normal(kapitel)


def modelle_aufloesen(muster: list[str]) -> list[str]:
    """Modell-IDs nicht raten, sondern aus der Liste holen. Ein geratener
    Name scheitert erst auf dem Runner und kostet einen ganzen Lauf."""
    m = rufen("/models")
    liste = m.get("data") if isinstance(m, dict) else None
    if not isinstance(liste, list):
        raise RuntimeError(f"Modelliste nicht lesbar: {str(m)[:150]}")
    raus = []
    for p in muster:
        treffer = [x for x in liste
                   if p.lower() in (x.get("id") or "").lower()
                   and "image" not in (x.get("id") or "")
                   and "free" not in (x.get("id") or "")]
        if not treffer:
            print(f"  kein Modell zu „{p}“ gefunden")
            continue
        # Das jeweils guenstigste, damit ein Durchgang bezahlbar bleibt.
        def kosten(x):
            p_ = x.get("pricing") or {}
            try:
                return float(p_.get("prompt") or 0) + float(p_.get("completion") or 0)
            except (TypeError, ValueError):
                return 9e9
        treffer.sort(key=kosten)
        raus.append(treffer[0]["id"])
        print(f"  „{p}“ -> {treffer[0]['id']}")
    return raus


def eine_frage(kapitel: str, modell: str) -> dict:
    last = {"model": modell,
            "messages": [{"role": "user", "content": AUFGABE + kapitel}],
            "max_tokens": 400, "temperature": 0.2}
    a = rufen("/chat/completions", last, zeit=120)
    if "fehler" in a:
        return {"fehler": a["fehler"], "text": a.get("text", "")[:200]}
    try:
        inhalt = a["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return {"fehler": "Antwort ohne Inhalt", "roh": str(a)[:200]}
    kosten = ((a.get("usage") or {}).get("cost")
              or (a.get("usage") or {}).get("total_cost") or 0)
    return {"text": inhalt, "kosten": kosten}


# --------------------------------------------------------- Kalibrierung

def selbsttest() -> bool:
    ok = True
    kapitel = ('Er sah sie an. „Nicht heute", sagte sie. „Bitte." '
               'Draußen ging jemand mit einem Hund vorbei.')

    gut = antwort_lesen(
        'ABBRUCH: "Nicht heute, sagte sie" — zu wenig Widerstand\n'
        'UNKLAR: keine\n'
        'STARK: "Draußen ging jemand mit einem Hund vorbei"')
    print(f"  Format gelesen: {sorted(gut)}")
    if sorted(gut) != ["ABBRUCH", "STARK", "UNKLAR"]:
        print("  FEHLGESCHLAGEN: Format nicht erkannt.")
        ok = False
    if gut.get("UNKLAR", {}).get("zitat") is not None:
        print("  FEHLGESCHLAGEN: 'keine' nicht als leer erkannt.")
        ok = False

    echt = belegt(gut["STARK"]["zitat"], kapitel)
    erfunden = belegt("Sie warf die Tasse gegen die Wand", kapitel)
    print(f"  Beleg: echtes Zitat {echt}, erfundenes Zitat {erfunden}")
    if not (echt is True and erfunden is False):
        print("  FEHLGESCHLAGEN: Zitatprüfung unbrauchbar.")
        ok = False

    # Der harte Fall: richtiges Zitat, aber mit Zeilenumbruch und
    # typografischen Anfuehrungszeichen -- muss trotzdem als belegt
    # gelten, sonst meldet das Geraet lauter Falschtreffer.
    hart = belegt('„Nicht heute“, sagte sie',
                  'Er sah sie an. „Nicht heute“,\nsagte sie. „Bitte."')
    print(f"  Beleg über Zeilenumbruch hinweg: {hart}")
    if hart is not True:
        print("  FEHLGESCHLAGEN: Umbruch oder Sonderzeichen brechen den "
              "Beleg.")
        ok = False

    print("  Selbsttest bestanden." if ok else "  Selbsttest FEHLGESCHLAGEN.")
    return ok


# --------------------------------------------------------------- Bericht

def bericht(ergebnisse: list[dict], modelle: list[str],
            kosten: float) -> str:
    z = ["# Lektorat durch fremde Modelle", "",
         f"Stand: {date.today().isoformat()} · Modelle: "
         + ", ".join(f"`{m}`" for m in modelle)
         + f" · Kosten: {kosten:.4f} USD", "",
         "Gefragt wurde nichts, was nicht beantwortbar ist — nicht „ist "
         "das gut“, sondern: **wo würdest du aufhören zu lesen**. Das hat "
         "eine Stelle, und die Stelle muss wörtlich zitiert werden.", "",
         "**Jedes Zitat ist gegen den Kapiteltext geprüft.** Ein "
         "erfundenes Zitat heißt: Das Modell hat nicht gelesen, sondern "
         "etwas Plausibles gesagt. Die Belegquote unten ist die "
         "Kalibrierung dieses Geräts — liegt sie niedrig, ist der ganze "
         "Bericht wertlos.", ""]

    gesamt = beleg_ok = 0
    for e in ergebnisse:
        for m in modelle:
            a = e["antworten"].get(m, {})
            for feld in ("ABBRUCH", "UNKLAR", "STARK"):
                f = (a.get("gelesen") or {}).get(feld)
                if f and f.get("zitat"):
                    gesamt += 1
                    beleg_ok += 1 if f.get("belegt") else 0
    quote = round(100 * beleg_ok / gesamt, 1) if gesamt else 0.0
    z += [f"**Belegquote: {beleg_ok} von {gesamt} Zitaten "
          f"({quote} %) stehen wirklich im Text.**", ""]
    if quote < 70 and gesamt:
        z += ["> ⚠️ Unter 70 %. Die Modelle erfinden zu viel — die "
              "Befunde unten sind nicht belastbar.", ""]

    z += ["## Wo abgebrochen würde", "",
          "| Kap. | Modell | Stelle | Grund | belegt |",
          "|---:|---|---|---|:--:|"]
    for e in ergebnisse:
        for m in modelle:
            f = ((e["antworten"].get(m) or {}).get("gelesen")
                 or {}).get("ABBRUCH")
            if not f:
                continue
            if not f.get("zitat"):
                z.append(f"| {e['kapitel']} | `{m.split('/')[-1]}` | "
                         f"*keine* | – | – |")
                continue
            z.append(f"| {e['kapitel']} | `{m.split('/')[-1]}` | "
                     f"„{f['zitat'][:60]}“ | {(f.get('grund') or '–')[:70]} "
                     f"| {'ja' if f.get('belegt') else '**NEIN**'} |")

    z += ["", "## Was unklar bleibt", "",
          "| Kap. | Modell | Stelle | Was | belegt |", "|---:|---|---|---|:--:|"]
    for e in ergebnisse:
        for m in modelle:
            f = ((e["antworten"].get(m) or {}).get("gelesen")
                 or {}).get("UNKLAR")
            if not f or not f.get("zitat"):
                continue
            z.append(f"| {e['kapitel']} | `{m.split('/')[-1]}` | "
                     f"„{f['zitat'][:60]}“ | {(f.get('grund') or '–')[:70]} "
                     f"| {'ja' if f.get('belegt') else '**NEIN**'} |")

    z += ["", "## Übereinstimmung der Modelle", "",
          "Wenn zwei unabhängige Modelle dieselbe Stelle nennen, ist das "
          "ein Befund. Nennen sie nie dieselbe, misst das Gerät Rauschen.",
          ""]
    einig = 0
    for e in ergebnisse:
        stellen = []
        for m in modelle:
            f = ((e["antworten"].get(m) or {}).get("gelesen")
                 or {}).get("ABBRUCH")
            if f and f.get("zitat") and f.get("belegt"):
                stellen.append(normal(f["zitat"]))
        gleich = len(stellen) > 1 and any(
            a in b or b in a for a in stellen for b in stellen if a != b)
        if gleich:
            einig += 1
        z.append(f"- Kapitel {e['kapitel']}: "
                 + ("**dieselbe Stelle**" if gleich
                    else "verschiedene Stellen" if len(stellen) > 1
                    else "nur ein Modell mit Beleg"))
    z += ["", f"**{einig} von {len(ergebnisse)} Kapiteln mit "
          f"übereinstimmendem Abbruchpunkt.**", "", MARKER, ""]
    return "\n".join(z)


def main() -> None:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kapitel", nargs="*", type=int, default=[])
    p.add_argument("--modelle", nargs="*",
                   default=["openai/gpt", "google/gemini"])
    p.add_argument("--bericht", default="LEKTORAT.md")
    p.add_argument("--selbsttest", action="store_true")
    args = p.parse_args()

    print("Kalibrierung:")
    if not selbsttest():
        raise SystemExit(2)
    if args.selbsttest:
        return

    if not args.kapitel:
        print("Keine Kapitel angegeben.")
        return

    print("\nModelle auflösen:")
    modelle = modelle_aufloesen(args.modelle)
    if not modelle:
        raise SystemExit("Kein Modell aufgelöst.")

    ergebnisse, kosten = [], 0.0
    for n in args.kapitel:
        f = BUCH / f"kapitel-{n:02d}.md"
        if not f.exists():
            print(f"Kapitel {n} fehlt.")
            continue
        text = re.sub(r"^#.*$", "", f.read_text(encoding="utf-8"),
                      flags=re.M).strip()
        eintrag = {"kapitel": n, "antworten": {}}
        for m in modelle:
            print(f"\nKapitel {n} an {m} …", flush=True)
            a = eine_frage(text, m)
            if "fehler" in a:
                print(f"  Fehler: {a['fehler']}")
                eintrag["antworten"][m] = a
                continue
            kosten += float(a.get("kosten") or 0)
            gelesen = antwort_lesen(a["text"])
            for feld, wert in gelesen.items():
                wert["belegt"] = belegt(wert.get("zitat"), text)
            eintrag["antworten"][m] = {"text": a["text"], "gelesen": gelesen}
            for feld in ("ABBRUCH", "UNKLAR", "STARK"):
                w = gelesen.get(feld)
                if w and w.get("zitat"):
                    print(f"  {feld}: „{w['zitat'][:50]}“ "
                          f"[{'belegt' if w['belegt'] else 'ERFUNDEN'}]")
                elif w:
                    print(f"  {feld}: keine")
        ergebnisse.append(eintrag)

    Path("daten").mkdir(exist_ok=True)
    Path("daten/lektorat.json").write_text(
        json.dumps(ergebnisse, ensure_ascii=False, indent=2),
        encoding="utf-8")

    ziel = Path(args.bericht)
    alt = ziel.read_text(encoding="utf-8") if ziel.exists() else ""
    schwanz = alt.split(MARKER, 1)[1] if MARKER in alt else ""
    ziel.write_text(bericht(ergebnisse, modelle, kosten) + schwanz,
                    encoding="utf-8")
    print(f"\nGeschrieben: {ziel} · Kosten {kosten:.4f} USD")


if __name__ == "__main__":
    main()
