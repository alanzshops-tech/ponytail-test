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


# Gegenprobe. Beim ersten brauchbaren Lauf meldeten beide Modelle bei
# allen vier Kapiteln "ABBRUCH: keine". Das kann heissen, dass die
# Kapitel tragen -- oder dass Modelle hoeflich sind. Ohne einen Text,
# von dem feststeht, dass er schlecht ist, laesst sich das nicht
# unterscheiden. Dieser hier haeuft absichtlich, was in dieser Nische
# zum Weglegen fuehrt: Klischee, Perspektivsprung mitten im Absatz,
# Erklaerbaer, Widerspruch in zwei Saetzen.
KONTROLLTEXT = """Marlene war eine wunderschöne junge Frau mit langen
blonden Haaren, die im Wind wehten wie goldene Fäden aus reinstem
Sonnenlicht. Sie war 32 Jahre alt und arbeitete als Konditorin, was
bedeutet, dass sie Kuchen und Torten herstellte, ein Beruf, den man in
Deutschland in einer dreijährigen Ausbildung erlernt.

„Oh nein", dachte sie. Jonas dachte im selben Moment, dass sie
wunderschön war, und Marlene wusste, dass er das dachte, obwohl sie es
nicht wissen konnte.

Ihre Haare waren übrigens dunkelbraun.

Jonas Reinhardt war Milliardär. Er hatte viele Milliarden Euro, was
sehr viel Geld ist. Er stieg aus seinem teuren Auto, das sehr teuer
war, und ging auf sie zu.

„Hallo", sagte er lächelnd mit einem Lächeln.

„Hallo", sagte sie und ihr Herz machte einen Sprung, denn sie war
verliebt, obwohl sie ihn gerade zum allerersten Mal sah und ihn seit
zwei Jahren kannte.

Es war Liebe auf den ersten Blick, und beide wussten es sofort, und
alles würde von nun an für immer gut werden, und sie lebten glücklich
bis ans Ende ihrer Tage, aber das ist eine andere Geschichte."""


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


def modelle_aufloesen(muster: list[str],
                      max_preis: float = 20.0) -> list[list[str]]:
    """Modell-IDs nicht raten, sondern aus der Liste holen. Ein geratener
    Name scheitert erst auf dem Runner und kostet einen ganzen Lauf."""
    m = rufen("/models")
    liste = m.get("data") if isinstance(m, dict) else None
    if not isinstance(liste, list):
        raise RuntimeError(f"Modelliste nicht lesbar: {str(m)[:150]}")
    def kosten(x):
        p_ = x.get("pricing") or {}
        try:
            return (float(p_.get("prompt") or 0)
                    + float(p_.get("completion") or 0))
        except (TypeError, ValueError):
            return 0.0

    raus = []
    for p in muster:
        treffer = [x for x in liste
                   if p.lower() in (x.get("id") or "").lower()
                   and "image" not in (x.get("id") or "")
                   # Varianten hinter dem Doppelpunkt (:batch, :free,
                   # :extended) verhalten sich anders. Der erste Lauf griff
                   # google/gemini-2.5-flash-lite:batch, und die Antwort kam
                   # ohne Inhalt zurueck.
                   and ":" not in (x.get("id") or "")
                   and kosten(x) > 0]
        if not treffer:
            print(f"  kein Modell zu „{p}“ gefunden")
            continue
        # Das TEUERSTE der Familie, nicht das billigste. Der erste Lauf
        # waehlte nach Preis aufwaerts und landete bei gpt-oss-20b -- ein
        # kleines Modell soll hier nicht urteilen. Innerhalb eines
        # Anbieters ist der Preis der beste verfuegbare Anhaltspunkt fuer
        # Leistung; ein Feld dafuer gibt es in der Liste nicht.
        treffer.sort(key=kosten, reverse=True)
        bezahlbar = [x for x in treffer
                     if kosten(x) * 1e6 <= max_preis] or treffer[-1:]
        kandidaten = [x["id"] for x in bezahlbar[:3]]
        raus.append(kandidaten)
        print(f"  „{p}“ -> " + ", ".join(
            f"{x['id']} ({kosten(x) * 1e6:.1f} USD/Mio.)"
            for x in bezahlbar[:3]))
    return raus


def eine_frage(kapitel: str, kandidaten: list[str]) -> dict:
    """Der Reihe nach durchprobieren, bis eins antwortet.

    Ein einzelner Modellname reicht nicht. Beim ersten Lauf lieferte
    `gpt-5.5-pro` nur Denk-Token und lief in die Laengenbegrenzung
    (finish_reason: length, content: None), und
    `claude-opus-4.7-fast` antwortete mit HTTP 400, weil diese Variante
    einen Parameter nicht kennt. Beides sind Eigenschaften des Modells,
    keine Ausfaelle -- also weiterziehen statt scheitern.
    """
    letzter = {}
    for modell in kandidaten:
        last = {
            "model": modell,
            "messages": [{"role": "user", "content": AUFGABE + kapitel}],
            # 400 Token waren zu wenig: Denkmodelle verbrauchen sie,
            # bevor eine einzige Zeile Antwort entsteht.
            "max_tokens": 2000,
            "temperature": 0.2,
            # Ausfuehrliches Nachdenken bringt hier nichts -- gefragt ist
            # eine Leseerfahrung, kein Beweis.
            "reasoning": {"effort": "low"},
        }
        a = rufen("/chat/completions", last, zeit=180)
        e = _antwort_auspacken(a)
        e["modell"] = modell
        if "fehler" not in e:
            return e
        print(f"    {modell}: {e['fehler']}")
        letzter = e
    return letzter or {"fehler": "kein Kandidat"}


def _antwort_auspacken(a: dict) -> dict:
    if "fehler" in a:
        return {"fehler": a["fehler"], "text": a.get("text", "")[:200]}
    try:
        inhalt = a["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return {"fehler": "Antwort ohne Inhalt", "roh": str(a)[:200]}
    # content kann None sein -- bei Batch-Varianten und bei Modellen, die
    # nur reasoning liefern. Der erste Lauf ist genau daran abgestuerzt,
    # weil das None ungeprueft in re.search ging.
    if not inhalt or not inhalt.strip():
        return {"fehler": "Antwort mit leerem Inhalt",
                "roh": str(a.get("choices"))[:200]}
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
            kosten: float, kontrolle: dict | None = None) -> str:
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

    if kontrolle is not None:
        erkannt = []
        for m, a in (kontrolle.get("antworten") or {}).items():
            w = ((a or {}).get("gelesen") or {}).get("ABBRUCH") or {}
            erkannt.append((m, bool(w.get("zitat"))))
        z += ["## Gegenprobe", "",
              "Ein absichtlich schlechter Text (Klischee, "
              "Perspektivsprung, Erklärbär, Widerspruch in zwei Sätzen) "
              "geht bei jedem Lauf mit durch. Winken die Modelle ihn "
              "durch, ist jedes „kein Abbruch“ bei den echten Kapiteln "
              "wertlos.", ""]
        for m, ok_ in erkannt:
            z.append(f"- `{m.split('/')[-1]}`: "
                     + ("**Abbruchstelle genannt** — die Frage "
                        "funktioniert" if ok_
                        else "**durchgewunken** — die Frage misst nichts"))
        if erkannt and not any(o for _, o in erkannt):
            z += ["", "> ⚠️ Keins der Modelle hat den schlechten Text "
                  "beanstandet. Die Spalte „Wo abgebrochen würde“ unten "
                  "ist damit kein Befund, sondern Höflichkeit."]
        z.append("")

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
    p.add_argument("--buch", default="buch",
                   help="Ordner mit Kapiteln (zweiter Band: --buch buch2)")
    # Ohne Angabe richtet sich der Bericht nach dem Buch. Ein fester
    # Vorgabewert hat am 31.08.2026 bei prosa.py den Bericht von
    # Band 1 mit den Zahlen von Band 2 ueberschrieben; derselbe
    # Fehler waere hier moeglich gewesen.
    p.add_argument("--bericht", default=None)
    p.add_argument("--max-preis", type=float, default=20.0,
                   help="USD je Mio. Token, Obergrenze")
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--ohne-kontrolle", action="store_true",
                   help="Gegenprobe überspringen")
    args = p.parse_args()

    global BUCH
    BUCH = Path(args.buch)
    if args.bericht is None:
        args.bericht = ("LEKTORAT.md" if BUCH.name == "buch"
                        else str(BUCH / "LEKTORAT.md"))

    print("Kalibrierung:")
    if not selbsttest():
        raise SystemExit(2)
    if args.selbsttest:
        return

    if not args.kapitel:
        print("Keine Kapitel angegeben.")
        return

    print("\nModelle auflösen:")
    modelle = modelle_aufloesen(args.modelle, args.max_preis)
    if not modelle:
        raise SystemExit("Kein Modell aufgelöst.")
    benutzt: list[str] = []

    ergebnisse, kosten = [], 0.0

    # Gegenprobe zuerst: Wenn die Modelle diesen Text durchwinken, ist
    # jedes "ABBRUCH: keine" bei den echten Kapiteln wertlos.
    kontrolle = {"kapitel": 0, "antworten": {}}
    if not args.ohne_kontrolle:
        print("\nGegenprobe (absichtlich schlechter Text) …", flush=True)
        for kandidaten in modelle:
            a = eine_frage(KONTROLLTEXT, kandidaten)
            m = a.get("modell", kandidaten[0])
            if "fehler" in a:
                print(f"  {m}: {a['fehler']}")
                kontrolle["antworten"][m] = a
                continue
            kosten += float(a.get("kosten") or 0)
            gelesen = antwort_lesen(a["text"])
            for wert in gelesen.values():
                wert["belegt"] = belegt(wert.get("zitat"), KONTROLLTEXT)
            kontrolle["antworten"][m] = {"text": a["text"],
                                         "gelesen": gelesen}
            w = gelesen.get("ABBRUCH") or {}
            print(f"  {m}: ABBRUCH "
                  + (f"„{w['zitat'][:45]}“" if w.get("zitat") else "keine"))
            if m not in benutzt:
                benutzt.append(m)

    for n in args.kapitel:
        f = BUCH / f"kapitel-{n:02d}.md"
        if not f.exists():
            print(f"Kapitel {n} fehlt.")
            continue
        text = re.sub(r"^#.*$", "", f.read_text(encoding="utf-8"),
                      flags=re.M).strip()
        eintrag = {"kapitel": n, "antworten": {}}
        for kandidaten in modelle:
            m = kandidaten[0]
            print(f"\nKapitel {n} an {m} …", flush=True)
            a = eine_frage(text, kandidaten)
            m = a.get("modell", m)
            if "fehler" in a:
                print(f"  Fehler: {a['fehler']}")
                eintrag["antworten"][m] = a
                continue
            kosten += float(a.get("kosten") or 0)
            gelesen = antwort_lesen(a["text"])
            for feld, wert in gelesen.items():
                wert["belegt"] = belegt(wert.get("zitat"), text)
            eintrag["antworten"][m] = {"text": a["text"], "gelesen": gelesen}
            if m not in benutzt:
                benutzt.append(m)
            for feld in ("ABBRUCH", "UNKLAR", "STARK"):
                w = gelesen.get(feld)
                if w and w.get("zitat"):
                    print(f"  {feld}: „{w['zitat'][:50]}“ "
                          f"[{'belegt' if w['belegt'] else 'ERFUNDEN'}]")
                elif w:
                    print(f"  {feld}: keine")
        ergebnisse.append(eintrag)

    Path("daten").mkdir(exist_ok=True)
    # Auch die Rohdaten je Buch, sonst ueberschreibt der Lauf ueber Band 2
    # die Antworten zu Band 1.
    rohdaten = ("daten/lektorat.json" if BUCH.name == "buch"
                else f"daten/lektorat-{BUCH.name}.json")
    Path(rohdaten).write_text(
        json.dumps(ergebnisse, ensure_ascii=False, indent=2),
        encoding="utf-8")

    ziel = Path(args.bericht)
    alt = ziel.read_text(encoding="utf-8") if ziel.exists() else ""
    schwanz = alt.split(MARKER, 1)[1] if MARKER in alt else ""
    ziel.write_text(bericht(ergebnisse, benutzt or [k[0] for k in modelle],
                            kosten,
                            None if args.ohne_kontrolle else kontrolle)
                    + schwanz,
                    encoding="utf-8")
    print(f"\nGeschrieben: {ziel} · Kosten {kosten:.4f} USD")


if __name__ == "__main__":
    main()
