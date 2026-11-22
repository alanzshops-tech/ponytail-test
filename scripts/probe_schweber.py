"""Gegenprobe fuer den Schatten-Durchgriff im Widerruf-Detektor.

Positivfall: ein fester Knopf mit dem Wort "widerrufen" INNERHALB einer
shadowRoot -- genau die Lage, die der alte Detektor uebersehen hat.
Zweiter Knopf im hellen DOM, damit sichtbar wird, dass der alte Code
ueberhaupt etwas findet und der Unterschied wirklich am Schatten liegt.
"""
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

QUELLE = (Path(__file__).parent / "pruefstand.py").read_text()
# Den JS-Block aus dem Skript ziehen, statt ihn hier abzuschreiben --
# eine Kopie wuerde bald etwas anderes pruefen als das Original.
m = re.search(r'm\["widerruf"\] = seite\.evaluate\("""(.*?)"""\)', QUELLE, re.S)
if not m:
    sys.exit("JS-Block nicht gefunden")
NEU = m.group(1)
# Der alte Stand: flaches querySelectorAll ohne Schatten-Abstieg.
ALT = re.sub(
    r"const alle = \[\];\n(.*?)\}\)\(document, 0\);",
    "const alle = [...document.querySelectorAll('*')];",
    NEU, flags=re.S)
assert "e.shadowRoot" not in ALT, "Rueckbau misslungen"

SEITE = """
<!doctype html><meta charset=utf-8><body style="height:2000px">
  <div id="hell" style="position:fixed;right:20px;bottom:20px;
       width:120px;height:40px;background:#eee">TrustedSite</div>
  <div id="wirt"></div>
  <script>
    const w = document.getElementById('wirt').attachShadow({mode:'open'});
    w.innerHTML = '<div class="revoq-floating" style="position:fixed;' +
      'right:20px;bottom:20px;width:170px;height:40px;background:#111;' +
      'color:#fff">Vertrag widerrufen</div>';
  </script>
</body>
"""

# Negativfall: echte Verschachtelung. Ein fester Kasten mit einem festen
# Kind darin darf EINE Zeile ergeben, nicht zwei -- und keine
# Ueberlappung. Sonst waere der Umbau nur ein anderer Fehler.
VERSCHACHTELT = """
<!doctype html><meta charset=utf-8><body style="height:2000px">
  <div id="huelle" style="position:fixed;right:20px;bottom:20px;
       width:170px;height:60px;background:#111">
    <span id="kind" style="position:fixed;right:30px;bottom:30px;
          width:40px;height:40px;background:#f00"></span>
  </div>
</body>
"""

with sync_playwright() as p:
    # In der abgeschotteten Arbeitsumgebung liegt ein vorinstallierter
    # Chromium unter einer festen Nummer (z.B. chromium-1194). Das
    # pip-Paket "playwright" wird unabhaengig davon aktualisiert und sucht
    # dann eine neuere Revision, die hier gar nicht heruntergeladen ist --
    # Absturz mit "Executable doesn't exist". Deshalb der stabile Symlink
    # /opt/pw-browsers/chromium, der immer auf die tatsaechlich
    # installierte Version zeigt. Auf dem Runner gibt es diesen Pfad
    # nicht; CHROMIUM zeigt es dort um, sonst faellt es auf Playwrights
    # eigene Wahl zurueck.
    pfad = os.environ.get("CHROMIUM") or (
        "/opt/pw-browsers/chromium"
        if os.path.exists("/opt/pw-browsers/chromium") else None)
    b = p.chromium.launch(**({"executable_path": pfad} if pfad else {}))
    s = b.new_context(viewport={"width": 390, "height": 844}).new_page()
    s.set_content(SEITE)
    for name, js in (("alt", ALT), ("neu", NEU)):
        r = s.evaluate(js)
        print(f"{name}: treffer={r['elemente']} "
              f"schwebend_mit_text={r['schwebend_mit_text']} "
              f"schweber={[x['kennung'] for x in r['schweber']]} "
              f"ueberlappungen={r['ueberlappungen']}")
    s.set_content(VERSCHACHTELT)
    r = s.evaluate(NEU)
    print(f"verschachtelt: schweber={[x['kennung'] for x in r['schweber']]} "
          f"ueberlappungen={r['ueberlappungen']}")
    assert [x["kennung"] for x in r["schweber"]] == ["huelle"], "Kind mitgezaehlt"
    assert not r["ueberlappungen"], "Kind als Ueberlappung gemeldet"
    print("Negativfall bestanden.")
    b.close()
