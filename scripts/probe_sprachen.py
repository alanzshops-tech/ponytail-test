"""Gegenprobe fuer den Kopfdaten-Parser in sprachen.py.

Der Parser ersetzt einen Regex, weil Regexe auf HTML in diesem
Repository schon dreimal zu viel gefangen haben. Diese Probe stellt
genau die Faelle nach, an denen ein Regex scheitern wuerde -- wenn der
Parser sie besteht, ist der Austausch etwas wert, sonst ist er nur
anders falsch.

Positivfaelle:
  - Attributreihenfolge umgedreht: <link href=... rel="canonical">
  - rel mit mehreren Werten: rel="alternate stylesheet" (kein hreflang)
  - Grossschreibung: REL="CANONICAL"
  - x-default wird als hreflang mitgenommen

Negativfaelle (duerfen NICHT gefunden werden):
  - rel="canonical" als Text in einem <script>
  - ein <link rel="canonical"> NACH </head> -- gehoert nicht zum Kopf
  - <link rel="alternate"> ohne hreflang (RSS-Feed)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sprachen import Kopfdaten, bericht  # noqa: E402

HTML = """<!doctype html>
<html lang="en">
<head>
  <link href="https://x.de/en/p/a" REL="CANONICAL">
  <link rel="alternate" hreflang="de-DE" href="https://x.de/p/a">
  <link rel="alternate" hreflang="X-Default" href="https://x.de/p/a">
  <link rel="alternate" type="application/rss+xml" href="https://x.de/feed">
  <link rel="alternate stylesheet" href="https://x.de/dunkel.css">
  <script>
    var falle = '<link rel="canonical" href="https://boese.example/">';
    if (a < b) { console.log('rel="alternate" hreflang="fr"'); }
  </script>
</head>
<body>
  <link rel="canonical" href="https://zu-spaet.example/">
</body></html>
"""

k = Kopfdaten()
k.feed(HTML)

assert k.lang == "en", k.lang
assert k.canonical == "https://x.de/en/p/a", f"Canonical: {k.canonical!r}"
assert "boese" not in k.canonical, "Skript-Inhalt gefangen"
assert "zu-spaet" not in k.canonical, "Link nach </head> gefangen"

hl = sorted(a["hreflang"] for a in k.alternates)
assert hl == ["de-de", "x-default"], f"hreflang-Liste: {hl}"
assert all("feed" not in a["href"] for a in k.alternates), "RSS mitgezaehlt"
assert all("dunkel" not in a["href"] for a in k.alternates), "Stylesheet"
assert all(a["hreflang"] != "fr" for a in k.alternates), "Skript-Inhalt"

# Negativfall als Ganzes: eine Seite voellig ohne Auszeichnung darf
# leere Werte liefern, nicht zufaellig etwas aus dem Rumpf aufsammeln.
leer = Kopfdaten()
leer.feed("<html><head><title>nichts</title></head>"
          "<body><a href='/de'>Deutsch</a></body></html>")
assert leer.canonical == "" and leer.alternates == [] and leer.lang == ""

# Und der Bericht muss "nicht abgerufen" von "abgerufen, aber nichts
# gefunden" unterscheiden. Sonst liest sich ein Netzfehler wie ein
# Befund ueber den Shop -- der Fehler, der hier am teuersten waere.
b = bericht({"stand": "2026-08-11", "seiten": [
    {"url": "https://x.de/tot", "status": 0, "abgerufen": False},
]})
assert "Nicht abgerufen" in b and "kein Kontakt" in b, b
assert "kein Befund über den Shop" in b, "Netzfehler als Befund ausgegeben"

b2 = bericht({"stand": "2026-08-11", "seiten": [
    {"url": "https://x.de/p", "status": 200, "abgerufen": True, "lang": "de",
     "canonical": "https://x.de/p", "alternates": [], "gegenprobe": []},
]})
assert "ohne jede hreflang-Angabe" in b2
assert "sich selbst" in b2, "Selbstverweis nicht erkannt"
assert "Nicht abgerufen" not in b2, "Abschnitt faelschlich erzeugt"

print("Attributreihenfolge, Mehrfach-rel, Skriptfalle, Rumpf-Link, "
      "Leerfall und Berichtstrennung bestanden.")
