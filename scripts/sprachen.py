#!/usr/bin/env python3
"""
sprachen.py — misst Canonical und hreflang der Sprachfassungen.

Anlass: In den Search-Console-Daten vom 11.08.2026 landen sieben
deutsche Suchanfragen ("tischkicker klappbar", "kickertisch klappbar",
"tischfussball klappbar" ...) samt und sonders auf der ENGLISCHEN
Produkt-URL, Position 46 bis 65. Keine einzige auf der deutschen. Und
bei "couchtisch hochglanz schwarz" stehen beide Fassungen desselben
Produkts nebeneinander in derselben Ergebnisliste.

Zwei Ursachen kommen dafuer in Frage, und sie verlangen
entgegengesetzte Reparaturen:

  a) hreflang fehlt oder ist nicht wechselseitig -> Google weiss nicht,
     dass die beiden Seiten dieselbe Sache in zwei Sprachen sind, und
     waehlt selbst. Reparatur: Auszeichnung ergaenzen.
  b) hreflang stimmt, aber das Canonical der englischen Seite zeigt auf
     sich selbst, waehrend die deutsche Fassung schwaecher verlinkt ist
     -> Google hat sich fuer die falsche entschieden. Reparatur liegt
     woanders.

Ohne Messung ist nicht zu unterscheiden, welche. Deshalb dieses Skript.

Gemessen wird je Adresse:
  - Status und Zieladresse nach Weiterleitungen
  - <html lang>
  - <link rel="canonical">
  - alle <link rel="alternate" hreflang=...>, inklusive x-default
  - Wechselseitigkeit: verweist die genannte Gegenseite zurueck?

Kein Regex auf dem HTML. Die Attributreihenfolge ist nicht garantiert
(<link href=... rel=...> ist genauso gueltig wie umgekehrt), und ein
Muster wie rel="canonical" trifft auch in einem <script> zu. Beides ist
in diesem Repository schon dreimal danebengegangen -- siehe CLAUDE.md,
"Ein Selektor, der zu viel faengt, ist kein Messgeraet."

Aufruf:
    python3 scripts/sprachen.py --urls urls-sprachen.txt
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

KOPF = {"User-Agent": "homeeins-sprachpruefung/1.0 (+github.com/"
                      "alanzshops-tech/ponytail-test)"}
ZEITLIMIT = 20


class Kopfdaten(HTMLParser):
    """Liest lang, canonical und die hreflang-Verweise aus dem <head>.

    Nur <link>- und <html>-Elemente ausserhalb von <script>/<style>
    zaehlen. Beim schliessenden </head> ist Schluss -- was danach kommt,
    ist Seiteninhalt und gehoert nicht zur Auszeichnung.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.canonical = ""
        self.alternates: list[dict] = []
        self._fertig = False

    def handle_starttag(self, tag, attrs):
        if self._fertig:
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "link":
            # rel kann mehrere Werte tragen: rel="alternate stylesheet".
            rel = {w.lower() for w in a.get("rel", "").split()}
            href = a.get("href", "")
            if "canonical" in rel and href and not self.canonical:
                self.canonical = href
            if "alternate" in rel and a.get("hreflang") and href:
                self.alternates.append(
                    {"hreflang": a["hreflang"].lower(), "href": href})

    def handle_endtag(self, tag):
        if tag == "head":
            self._fertig = True


def holen(url: str) -> tuple[int, str, str]:
    """(Status, Zieladresse, Text). Status 0 heisst: gar nicht erreicht."""
    req = urllib.request.Request(url, headers=KOPF)
    try:
        with urllib.request.urlopen(req, timeout=ZEITLIMIT) as a:
            roh = a.read(600_000)
            zeichen = a.headers.get_content_charset() or "utf-8"
            return a.status, a.geturl(), roh.decode(zeichen, "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:                      # DNS, TLS, Zeitueberschreitung
        print(f"  nicht erreichbar: {type(e).__name__}: {e}", file=sys.stderr)
        return 0, url, ""


def lesen(url: str) -> dict:
    status, ziel, text = holen(url)
    e = {"url": url, "status": status, "ziel": ziel,
         "weitergeleitet": ziel.split("?")[0] != url.split("?")[0]}
    if not text:
        e["abgerufen"] = False
        return e
    k = Kopfdaten()
    k.feed(text)
    e.update({"abgerufen": True, "lang": k.lang, "canonical": k.canonical,
              "alternates": k.alternates})
    return e


def wechselseitig(eintraege: list[dict]) -> None:
    """Prueft je Seite, ob die genannten Gegenseiten zurueckverweisen.

    Eine einseitige hreflang-Angabe ist fuer Google wertlos -- sie muss
    von beiden Seiten kommen. Genau das ist der Fehler, der zwei
    Sprachfassungen gegeneinander antreten laesst.
    """
    zwischenspeicher: dict[str, dict] = {e["url"]: e for e in eintraege}
    for e in eintraege:
        if not e.get("abgerufen"):
            continue
        prueflauf = []
        for alt in e["alternates"]:
            ziel = alt["href"]
            if ziel not in zwischenspeicher:
                zwischenspeicher[ziel] = lesen(ziel)
            g = zwischenspeicher[ziel]
            zurueck = any(
                a["href"].split("?")[0] == e["url"].split("?")[0]
                for a in g.get("alternates", []))
            prueflauf.append({"hreflang": alt["hreflang"], "href": ziel,
                              "erreichbar": g.get("abgerufen", False),
                              "status": g.get("status", 0),
                              "verweist_zurueck": zurueck})
        e["gegenprobe"] = prueflauf


def bericht(daten: dict) -> str:
    z = ["# Sprachfassungen — Canonical und hreflang", "",
         f"Stand: {daten['stand']} · {len(daten['seiten'])} Adressen", "",
         "Anlass ist ein gemessener Befund, kein Verdacht: sieben deutsche "
         "Suchanfragen landen auf der englischen Produkt-URL, keine auf der "
         "deutschen (`GSC.md`, 11.08.2026). Hier steht, ob die Auszeichnung "
         "das erklärt.", ""]

    nicht_da = [s for s in daten["seiten"] if not s.get("abgerufen")]
    if nicht_da:
        z += ["## Nicht abgerufen", "",
              "Diese Adressen sagen nichts aus — weder im Guten noch im "
              "Schlechten. Sie fehlen in allen Zahlen unten.", "",
              "| Adresse | Status |", "|---|---:|"]
        z += [f"| {s['url']} | {s['status'] or 'kein Kontakt'} |"
              for s in nicht_da]
        z.append("")

    da = [s for s in daten["seiten"] if s.get("abgerufen")]
    if not da:
        z += ["Keine einzige Adresse abgerufen. Das ist ein Netzproblem, "
              "kein Befund über den Shop."]
        return "\n".join(z) + "\n"

    ohne = [s for s in da if not s["alternates"]]
    z += ["## Überblick", "",
          f"{len(da)} Adressen abgerufen. "
          f"{len(ohne)} davon **ohne jede hreflang-Angabe**.", ""]
    z += ["| Adresse | lang | hreflang | Canonical zeigt auf |",
          "|---|---|---:|---|"]
    for s in da:
        c = s["canonical"] or "—"
        eigen = c.split("?")[0] == s["url"].split("?")[0]
        z.append(f"| {s['url']} | {s['lang'] or '—'} | "
                 f"{len(s['alternates'])} | "
                 f"{'sich selbst' if eigen else c} |")
    z.append("")

    z += ["## Wechselseitigkeit", "",
          "Eine hreflang-Angabe wirkt nur, wenn die Gegenseite "
          "zurückverweist. Einseitige Angaben ignoriert Google.", ""]
    einseitig = 0
    for s in da:
        if not s.get("gegenprobe"):
            z.append(f"**{s['url']}** — keine Alternativen angegeben.")
            z.append("")
            continue
        z.append(f"**{s['url']}**")
        z.append("")
        z.append("| hreflang | Ziel | erreichbar | verweist zurück |")
        z.append("|---|---|:-:|:-:|")
        for g in s["gegenprobe"]:
            if not g["verweist_zurueck"]:
                einseitig += 1
            erreichbar = "ja" if g["erreichbar"] else f"nein ({g['status']})"
            zurueck = "ja" if g["verweist_zurueck"] else "**nein**"
            z.append(f"| {g['hreflang']} | {g['href']} | "
                     f"{erreichbar} | {zurueck} |")
        z.append("")
    z += [f"Einseitige Angaben insgesamt: **{einseitig}**.", ""]
    return "\n".join(z) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls-sprachen.txt")
    ap.add_argument("--out", default="daten")
    a = ap.parse_args()

    zeilen = [z.strip() for z in Path(a.urls).read_text().splitlines()]
    urls = [z for z in zeilen if z and not z.startswith("#")]
    if not urls:
        sys.exit(f"{a.urls} enthält keine Adressen.")

    seiten = []
    for u in urls:
        print(f"lese {u}")
        seiten.append(lesen(u))
    wechselseitig(seiten)

    daten = {"stand": str(date.today()), "seiten": seiten}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "sprachen-aktuell.json").write_text(
        json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("SPRACHEN.md").write_text(bericht(daten), encoding="utf-8")

    erreicht = sum(1 for s in seiten if s.get("abgerufen"))
    print(f"{erreicht} von {len(seiten)} Adressen abgerufen.")
    if not erreicht:
        sys.exit("Keine einzige Adresse abgerufen — das ist kein Befund.")


if __name__ == "__main__":
    main()
