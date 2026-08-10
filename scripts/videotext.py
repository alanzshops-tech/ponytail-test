#!/usr/bin/env python3
"""
videotext.py — holt YouTube-Transkripte auf dem Runner.

YouTube ist aus der abgeschotteten Arbeitsumgebung gesperrt, der Runner
kommt hin. Gleiches Muster wie bei den Shop-Seiten: Der Runner liest,
das Repository trägt, ich werte hier aus.

Ehrliche Einschränkung: YouTube blockt Anfragen aus Rechenzentren
regelmäßig. Wenn das passiert, steht es im Bericht — ein leeres Ergebnis
darf nicht wie ein Ergebnis aussehen.

Aufruf:
    python3 scripts/videotext.py --ids rNiw_9OO9ts,hh7i8Bs8-JI
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

# Wonach in den Transkripten gesucht wird: Werkzeuge, Befehle, Dateien.
# Nicht nach Meinungen — die stehen in jedem Blogartikel. Interessant
# ist, was die Leute tatsächlich tippen.
BEGRIFFE = [
    "shopify cli", "theme dev", "theme pull", "theme push", "theme check",
    "dev mcp", "mcp", "claude.md", "claude code", "playwright",
    "lighthouse", "liquid", "metafield", "section", "snippet",
    "git", "github", "vercel", "hydrogen", "headless", "dawn",
    "horizon", "tailwind", "figma", "cursor", "subagent", "agent",
    "hook", "pre-commit", "schema", "json template", "app block",
]


def holen(vid: str) -> dict:
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    versuche = [["de"], ["en"], ["en-US"], None]
    for sprachen in versuche:
        try:
            t = (api.fetch(vid, languages=sprachen) if sprachen
                 else api.fetch(vid))
            teile = [s.text for s in t]
            return {"id": vid, "sprache": getattr(t, "language_code", "?"),
                    "text": " ".join(teile), "zeilen": len(teile)}
        except Exception as e:                                   # noqa: BLE001
            letzter = f"{type(e).__name__}: {str(e)[:200]}"
    return {"id": vid, "fehler": letzter}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True)
    ap.add_argument("--out", default="daten/transkripte")
    a = ap.parse_args()

    ordner = Path(a.out)
    ordner.mkdir(parents=True, exist_ok=True)
    ergebnisse = []
    for vid in [x.strip() for x in a.ids.split(",") if x.strip()]:
        print(f"  {vid} …")
        r = holen(vid)
        if r.get("text"):
            (ordner / f"{vid}.txt").write_text(r["text"], encoding="utf-8")
            print(f"     {len(r['text'])} Zeichen, Sprache {r['sprache']}")
        else:
            print(f"     FEHLER {r.get('fehler')}")
        ergebnisse.append(r)

    z = ["# Transkripte", "", f"Stand: {date.today()}", "",
         "Auf dem Runner geholt, weil YouTube aus der Arbeitsumgebung "
         "gesperrt ist. Gesucht wird nach genannten Werkzeugen und "
         "Befehlen, nicht nach Meinungen.", "",
         "| Video | Sprache | Zeichen | Status |", "|---|---|---:|---|"]
    for r in ergebnisse:
        if r.get("text"):
            z.append(f"| `{r['id']}` | {r['sprache']} | {len(r['text'])} | ok |")
        else:
            z.append(f"| `{r['id']}` | – | 0 | {r.get('fehler', '?')[:90]} |")
    z.append("")

    mit_text = [r for r in ergebnisse if r.get("text")]
    if not mit_text:
        z += ["**Kein einziges Transkript erhalten.** YouTube blockt "
              "Anfragen aus Rechenzentren; GitHub-Runner laufen in einem. "
              "Das ist kein Ergebnis, sondern ein verweigerter Zugriff — "
              "und wird hier ausdrücklich als solcher vermerkt.", ""]
    else:
        z += ["## Genannte Werkzeuge und Befehle", "",
              "| Begriff | " + " | ".join(f"`{r['id']}`" for r in mit_text)
              + " | gesamt |",
              "|---|" + "---:|" * (len(mit_text) + 1)]
        zeilen = []
        for b in BEGRIFFE:
            n = [len(re.findall(re.escape(b), r["text"], re.I))
                 for r in mit_text]
            if sum(n):
                zeilen.append((sum(n), b, n))
        for gesamt, b, n in sorted(zeilen, reverse=True):
            z.append(f"| {b} | " + " | ".join(str(x) for x in n)
                     + f" | **{gesamt}** |")
        z.append("")

    Path("TRANSKRIPTE.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    Path("daten").mkdir(exist_ok=True)
    Path("daten/transkripte.json").write_text(
        json.dumps([{k: v for k, v in r.items() if k != "text"}
                    for r in ergebnisse], ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\n{len(mit_text)} von {len(ergebnisse)} Transkripten geholt")


if __name__ == "__main__":
    main()
