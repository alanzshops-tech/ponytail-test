#!/usr/bin/env python3
"""
aufzeichnen.py — nimmt echte CJ-Antworten auf, damit Tests gegen die
Wirklichkeit laufen statt gegen meine Vorstellung davon.

Anlass: An einem Tag sechs falsche Annahmen über diese API — Währung,
Bestandsbezug, ein Kategoriefeld, das nur mit Zusatzparameter kommt, eine
Stichwortsuche, die vorhandene Artikel nicht findet, eine Fracht von null,
die echt war. Jede einzelne hatte einen grünen Test daneben stehen. Die
Tests prüften handgeschriebene Attrappen, also genau die Annahmen, die
falsch waren.

VCR.py löst das: Der Runner nimmt echte Antworten auf, das Repository
trägt sie, die Tests spielen sie ab. Eine Attrappe kann sich irren, eine
Aufzeichnung nicht.

GEHEIMNISSE: In den Aufnahmen stehen sonst Schlüssel und Token. Beides
wird vor dem Schreiben geschwärzt — im Anfragekopf, im Anfragekörper und
in der Antwort. Anschließend wird jede Kassette gegengelesen. Findet die
Prüfung noch etwas, wird die Datei gelöscht statt committet.

Aufruf (nur auf dem Runner, CJ_API_KEY muss gesetzt sein):
    python3 scripts/aufzeichnen.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cj                                                  # noqa: E402

ORDNER = Path("kassetten")
PLATZHALTER = "GESCHWAERZT"

# Kopfzeilen, die niemals in eine Datei gehören.
KOEPFE = ["CJ-Access-Token", "Authorization", "Cookie", "Set-Cookie"]

# Felder, die in Anfrage oder Antwort geschwärzt werden.
FELDER = ["apiKey", "accessToken", "refreshToken", "openId"]


def anfrage_saeubern(anfrage):
    if anfrage.body:
        roh = anfrage.body
        text = roh.decode("utf-8", "replace") if isinstance(roh, bytes) else str(roh)
        try:
            leib = json.loads(text)
        except ValueError:
            return anfrage
        geaendert = False
        for f in FELDER:
            if isinstance(leib, dict) and f in leib:
                leib[f] = PLATZHALTER
                geaendert = True
        if geaendert:
            anfrage.body = json.dumps(leib).encode()
    return anfrage


def antwort_saeubern(antwort):
    koerper = antwort.get("body", {}).get("string")
    if not koerper:
        return antwort
    text = koerper.decode("utf-8", "replace") if isinstance(koerper, bytes) else koerper
    for f in FELDER:
        # Ersetzt den Wert hinter dem Feldnamen, egal wie lang er ist.
        text = re.sub(rf'("{f}"\s*:\s*)"[^"]*"', rf'\1"{PLATZHALTER}"', text)
    antwort["body"]["string"] = text.encode() if isinstance(koerper, bytes) else text
    return antwort


def pruefen(datei: Path, schluessel: str) -> list[str]:
    """Liest die fertige Kassette gegen. Ein Filter, der nicht geprüft
    wird, ist eine Hoffnung."""
    text = datei.read_text(encoding="utf-8", errors="replace")
    funde = []
    if schluessel and schluessel in text:
        funde.append("der API-Schlüssel steht im Klartext")
    for f in FELDER:
        for m in re.finditer(rf'"{f}"\s*:\s*"([^"]*)"', text):
            if m.group(1) != PLATZHALTER:
                funde.append(f"{f} nicht geschwärzt")
                break
    for k in KOEPFE:
        if re.search(rf'{k}.{{0,4}}\n?\s*-\s*(?!{PLATZHALTER})\S{{20,}}',
                     text, re.I):
            funde.append(f"Kopfzeile {k} enthält noch einen Wert")
    return funde


def main() -> None:
    schluessel = os.environ.get("CJ_API_KEY", "").strip()
    if not schluessel:
        print(cj.ANLEITUNG)
        return

    import vcr
    band = vcr.VCR(
        cassette_library_dir=str(ORDNER),
        record_mode="all",              # immer frisch aufnehmen
        filter_headers=KOEPFE,
        before_record_request=anfrage_saeubern,
        before_record_response=antwort_saeubern,
        decode_compressed_response=True,
    )
    ORDNER.mkdir(exist_ok=True)

    with band.use_cassette("cj_anmeldung.yaml"):
        token = cj.token_holen(schluessel)
    print("  Anmeldung aufgezeichnet")

    with band.use_cassette("cj_lagerliste.yaml"):
        cj.lager_pruefen(token)

    with band.use_cassette("cj_liste.yaml"):
        treffer, gesamt = cj.suchen(token, "*", {"mindestbestand": 1,
                                                 "seiten": 1})
    print(f"  Trefferliste aufgezeichnet: {len(treffer)} Artikel, "
          f"{gesamt} laut CJ")

    if treffer:
        import marge
        sku = treffer[0]["sku"]
        with band.use_cassette("cj_bestand.yaml"):
            de, welt, name = marge.bestand_de(token, sku)
        print(f"  Bestandsabfrage aufgezeichnet: {sku} -> DE {de}, welt {welt}")

    fehler = False
    for datei in sorted(ORDNER.glob("*.yaml")):
        funde = pruefen(datei, schluessel)
        if funde:
            datei.unlink()
            print(f"  {datei.name}: GELÖSCHT — {'; '.join(funde)}")
            fehler = True
        else:
            print(f"  {datei.name}: sauber ({datei.stat().st_size} Bytes)")
    if fehler:
        sys.exit("Mindestens eine Kassette enthielt Zugangsdaten. "
                 "Nichts davon darf committet werden.")
    print(f"\n{len(list(ORDNER.glob('*.yaml')))} Kassetten in {ORDNER}/")


if __name__ == "__main__":
    main()
