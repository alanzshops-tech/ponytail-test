#!/usr/bin/env python3
"""Misst, was die Variantenauswahl auf einer Produktseite dem Besucher zeigt.

Warum es dieses Werkzeug gibt
-----------------------------
Am 22.11.2026 ergab eine Abfrage aller 96 aktiven Produkte, dass viele
Optionswerte unverarbeitet vom Lieferanten durchgereicht werden:
"Farbe: default" auf elf Produkten, "Attribute: RSPF4MBCSPM0MX1YEV0" auf
drei, englische Optionsnamen ("Color", "Size") auf vier. Die Admin-API
sagt aber nicht, ob der Besucher das auch *sieht* -- Dawn blendet eine
Auswahl aus, wenn ein Produkt nur die Standardvariante hat. Ob eine
Korrektur in der API also an der Oberflaeche ankommt, ist eine Frage an
die ausgelieferte Seite, nicht an die API.

Die Regel aus CLAUDE.md
-----------------------
"Ein Selektor, der zu viel faengt, ist kein Messgeraet." Deshalb prueft
dieses Skript sich zuerst selbst: Es braucht einen Positivfall, auf dem
eine Auswahl stehen MUSS, und einen Negativfall, auf dem keine stehen
darf. Schlaegt eine der beiden Proben fehl, faellt kein Urteil ueber die
restlichen Seiten -- dann ist das Messgeraet kaputt, nicht der Shop.

Aufruf
------
    python3 scripts/optionen.py                      # Eichung + alle Produkte der Sitemap
    python3 scripts/optionen.py --pfade a b c        # nur diese Produktpfade
    python3 scripts/optionen.py --selbsttest         # nur die Eichung, ohne Netz

Ergebnis: OPTIONEN.md an der Wurzel, daten/optionen-<datum>.json.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import gzip
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

SHOP = "https://www.homeeins.de"
KOPF = {"User-Agent": "homeeins-optionencheck/1.0 (+Messung des eigenen Shops)"}

# Eichung. Der Positivfall hat sechs echte Farben, der Negativfall nur die
# Standardvariante. Beide Erwartungen stehen hier als Zahl, nicht als
# Gefuehl, damit ein Fehlschlag auffaellt.
POSITIVFALL = "/products/schuhbank-kompakt-62cm-sitzpolster"
NEGATIVFALL = "/products/raumteiler-japanisch-4-teilig-holz"

# Werte, die kein Mensch so in einen Shop schreiben wuerde: Platzhalter und
# Lieferanten-Artikelnummern. Der Vergleich laeuft auf dem kleingeschriebenen
# Wert, damit "Default" und "default" beide treffen.
PLATZHALTER = {"default", "default title", "title", "-", "n/a", "none", "standard"}
ARTIKELNUMMER = re.compile(r"^[A-Z0-9]{12,}$")
ENGLISCHE_NAMEN = {"color", "colour", "size", "material", "style", "attribute", "attributes"}


def _holen(url: str, versuche: int = 3) -> str:
    """Laedt eine Seite als Text. Gibt bei dauerhaftem Fehler eine Ausnahme."""
    letzter: Exception | None = None
    for n in range(versuche):
        try:
            anfrage = urllib.request.Request(url, headers=KOPF)
            with urllib.request.urlopen(anfrage, timeout=30) as antwort:
                rohdaten = antwort.read()
                if antwort.headers.get("Content-Encoding") == "gzip":
                    rohdaten = gzip.decompress(rohdaten)
                return rohdaten.decode("utf-8", "replace")
        except Exception as fehler:  # noqa: BLE001 -- Netzfehler sind erwartbar
            letzter = fehler
            time.sleep(1.5 * (n + 1))
    raise RuntimeError(f"{url} nicht erreichbar: {letzter}")


def optionen_aus_json(seite: str) -> list[dict]:
    """Liest die Optionen aus dem Produkt-JSON, das Dawn in die Seite legt.

    Dawn rendert fuer die Variantenauswahl ein <script type="application/json">
    mit der Produktstruktur. Das ist genauer als ein Regex auf die sichtbaren
    Labels, weil dort auch die Optionsnamen stehen.
    """
    gefunden: list[dict] = []
    for treffer in re.finditer(
        r'<script[^>]+type="application/json"[^>]*>(.*?)</script>', seite, re.S
    ):
        try:
            daten = json.loads(treffer.group(1))
        except Exception:  # noqa: BLE001 -- nicht jedes JSON-Script ist das Produkt
            continue
        if isinstance(daten, dict) and "options_with_values" in daten:
            for option in daten["options_with_values"]:
                gefunden.append(
                    {
                        "name": option.get("name", ""),
                        "werte": [
                            w.get("name", "") if isinstance(w, dict) else str(w)
                            for w in option.get("values", [])
                        ],
                    }
                )
    return gefunden


def auswahl_sichtbar(seite: str) -> bool:
    """Sagt, ob Dawn eine Variantenauswahl ausliefert.

    Dawn setzt variant-selects bzw. variant-radios nur, wenn das Produkt mehr
    als die Standardvariante hat. Beides wird geprueft, weil die Einstellung
    'Als Knoepfe' die zweite Form erzeugt.
    """
    return ("<variant-selects" in seite) or ("<variant-radios" in seite)


def befunde(name: str, werte: list[str]) -> list[str]:
    """Welche Maengel ein einzelner Optionsname mit seinen Werten hat."""
    liste: list[str] = []
    if name.strip().lower() in ENGLISCHE_NAMEN and name.strip().lower() != "attribute":
        liste.append(f"englischer Optionsname: {name!r}")
    if name.strip().lower() in {"attribute", "attributes"}:
        liste.append(f"unverarbeiteter Optionsname: {name!r}")
    for wert in werte:
        kurz = wert.strip()
        if kurz.lower() in PLATZHALTER:
            liste.append(f"Platzhalter als Wert: {name!r} = {wert!r}")
        elif ARTIKELNUMMER.match(kurz):
            liste.append(f"Lieferanten-Artikelnummer als Wert: {name!r} = {wert!r}")
        elif kurz.lower() == name.strip().lower():
            liste.append(f"Wert gleich Optionsname: {name!r} = {wert!r}")
    return liste


def selbsttest() -> list[str]:
    """Prueft die Urteilsfunktion gegen bekannte Faelle, ohne Netz.

    Ohne diesen Test wuerde ein zu breiter Vergleich unbemerkt alles oder
    nichts melden. Jede Zeile hier ist ein Fall, der schon vorgekommen ist.
    """
    fehler: list[str] = []

    def erwarte(bedingung: bool, was: str) -> None:
        if not bedingung:
            fehler.append(was)

    # Muss treffen.
    erwarte(befunde("Farbe", ["default"]), "Platzhalter 'default' nicht erkannt")
    erwarte(
        befunde("Attribute", ["RSPF4MBCSPM0MX1YEV0"]),
        "Lieferanten-Artikelnummer nicht erkannt",
    )
    erwarte(befunde("Color", ["BLACK"]), "englischer Optionsname 'Color' nicht erkannt")
    erwarte(befunde("Material", ["Material"]), "Wert gleich Optionsname nicht erkannt")

    # Darf nicht treffen. Das ist die Haelfte, die bisher dreimal gefehlt hat.
    erwarte(not befunde("Farbe", ["Betongrau", "Weiß"]), "echte Farben falsch gemeldet")
    erwarte(not befunde("Größe", ["70 x 30 x 135 cm"]), "echtes Maß falsch gemeldet")
    erwarte(
        not befunde("Farbe", ["Grau mit Pfotenmuster"]),
        "echter zusammengesetzter Farbwert falsch gemeldet",
    )
    erwarte(
        not befunde("Modell", ["Willing HeatFlex Pro"]),
        "Modellname mit Leerzeichen falsch als Artikelnummer gemeldet",
    )
    # 'Title'/'Default Title' ist Shopifys Standardvariante. Sie ist kein
    # Mangel, weil Dawn sie gar nicht anzeigt -- sie darf nur dann gemeldet
    # werden, wenn die Auswahl trotzdem sichtbar ist. Deshalb wird dieser
    # Fall nicht hier, sondern in pruefen() entschieden.
    erwarte(
        bool(befunde("Title", ["Default Title"])),
        "Standardvariante wird von befunde() nicht als auffaellig gemeldet "
        "(pruefen() muss sie abhaengig von der Sichtbarkeit verwerfen)",
    )

    # Sichtbarkeits-Erkennung gegen beide Formen und einen Negativfall.
    erwarte(auswahl_sichtbar('<variant-selects id="x">'), "variant-selects nicht erkannt")
    erwarte(auswahl_sichtbar('<variant-radios id="x">'), "variant-radios nicht erkannt")
    erwarte(
        not auswahl_sichtbar("<p>Farbe: Betongrau</p>"),
        "Fließtext falsch als Variantenauswahl erkannt",
    )
    return fehler


def pruefen(pfad: str) -> dict:
    """Misst eine Produktseite."""
    seite = _holen(SHOP + pfad)
    sichtbar = auswahl_sichtbar(seite)
    optionen = optionen_aus_json(seite)
    maengel: list[str] = []
    if sichtbar:
        for option in optionen:
            maengel.extend(befunde(option["name"], option["werte"]))
    return {
        "pfad": pfad,
        "auswahl_sichtbar": sichtbar,
        "optionen": optionen,
        "maengel": maengel,
    }


def eichen() -> tuple[bool, list[str]]:
    """Positiv- und Negativprobe am echten Shop."""
    meldungen: list[str] = []
    ok = True

    positiv = pruefen(POSITIVFALL)
    if not positiv["auswahl_sichtbar"]:
        ok = False
        meldungen.append(
            f"Positivprobe fehlgeschlagen: {POSITIVFALL} zeigt keine Auswahl, "
            "obwohl das Produkt sechs Farben hat."
        )
    else:
        meldungen.append(f"Positivprobe bestanden: {POSITIVFALL} zeigt eine Auswahl.")

    negativ = pruefen(NEGATIVFALL)
    if negativ["auswahl_sichtbar"]:
        ok = False
        meldungen.append(
            f"Negativprobe fehlgeschlagen: {NEGATIVFALL} zeigt eine Auswahl, "
            "obwohl das Produkt nur die Standardvariante hat."
        )
    else:
        meldungen.append(
            f"Negativprobe bestanden: {NEGATIVFALL} zeigt keine Auswahl."
        )

    return ok, meldungen


def produktpfade() -> list[str]:
    """Alle Produktpfade aus der Produkt-Sitemap."""
    pfade: list[str] = []
    index = _holen(f"{SHOP}/sitemap.xml")
    for adresse in re.findall(r"<loc>([^<]+sitemap_products[^<]+)</loc>", index):
        teil = _holen(adresse)
        for seite in re.findall(r"<loc>([^<]+/products/[^<]+)</loc>", teil):
            pfad = seite.split(SHOP, 1)[-1] if SHOP in seite else seite
            if pfad.startswith("/products/") and pfad not in pfade:
                pfade.append(pfad)
    return pfade


def bericht(eichmeldungen: list[str], ergebnisse: list[dict]) -> str:
    heute = _dt.date.today().strftime("%d.%m.%Y")
    mit_mangel = [e for e in ergebnisse if e["maengel"]]
    zeilen = [
        "# Variantenauswahl, wie der Besucher sie sieht",
        "",
        f"Gemessen am {heute} an der ausgelieferten Seite, nicht an der "
        "Admin-API. Erzeugt von `scripts/optionen.py`.",
        "",
        "## Eichung",
        "",
    ]
    zeilen += [f"- {m}" for m in eichmeldungen]
    zeilen += [
        "",
        "## Ergebnis",
        "",
        f"- Produktseiten gemessen: **{len(ergebnisse)}**",
        f"- davon mit sichtbarer Variantenauswahl: "
        f"**{sum(1 for e in ergebnisse if e['auswahl_sichtbar'])}**",
        f"- davon mit auffaelligen Optionswerten: **{len(mit_mangel)}**",
        "",
    ]
    if mit_mangel:
        zeilen += ["## Die auffaelligen Seiten", ""]
        for eintrag in mit_mangel:
            zeilen.append(f"### `{eintrag['pfad']}`")
            for mangel in eintrag["maengel"]:
                zeilen.append(f"- {mangel}")
            zeilen.append("")
    else:
        zeilen += [
            "Keine auffaelligen Optionswerte auf einer Seite mit sichtbarer "
            "Auswahl. Das ist nur dann eine gute Nachricht, wenn die Eichung "
            "oben bestanden hat.",
            "",
        ]
    return "\n".join(zeilen)


def main(argv: list[str] | None = None) -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--pfade", nargs="*", help="nur diese Produktpfade messen")
    zerleger.add_argument(
        "--selbsttest", action="store_true", help="nur die Eichung der Urteilsfunktion"
    )
    argumente = zerleger.parse_args(argv)

    fehler = selbsttest()
    if fehler:
        print("Selbsttest fehlgeschlagen:", file=sys.stderr)
        for f in fehler:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"Selbsttest bestanden ({len(PLATZHALTER)} Platzhalter, 4 Positiv-, 5 Negativfaelle).")
    if argumente.selbsttest:
        return 0

    eichung_ok, eichmeldungen = eichen()
    for meldung in eichmeldungen:
        print(meldung)
    if not eichung_ok:
        print(
            "Abgelehnt: Die Eichung am echten Shop ist fehlgeschlagen. Ohne sie "
            "ist jedes Urteil ueber die anderen Seiten wertlos.",
            file=sys.stderr,
        )
        return 2

    pfade = argumente.pfade or produktpfade()
    print(f"{len(pfade)} Produktseiten werden gemessen.")
    ergebnisse: list[dict] = []
    for nummer, pfad in enumerate(pfade, 1):
        try:
            ergebnisse.append(pruefen(pfad))
        except Exception as f:  # noqa: BLE001
            ergebnisse.append(
                {"pfad": pfad, "auswahl_sichtbar": None, "optionen": [], "maengel": [], "fehler": str(f)}
            )
        if nummer % 10 == 0:
            print(f"  {nummer}/{len(pfade)}")
        time.sleep(0.4)

    wurzel = pathlib.Path(__file__).resolve().parent.parent
    (wurzel / "OPTIONEN.md").write_text(
        bericht(eichmeldungen, ergebnisse), encoding="utf-8"
    )
    daten = wurzel / "daten"
    daten.mkdir(exist_ok=True)
    datum = _dt.date.today().isoformat()
    (daten / f"optionen-{datum}.json").write_text(
        json.dumps(
            {"eichung": eichmeldungen, "produkte": ergebnisse},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    mit_mangel = sum(1 for e in ergebnisse if e["maengel"])
    print(f"OPTIONEN.md geschrieben. {mit_mangel} Seiten mit auffaelligen Werten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
