"""Gegenprobe fuer die Auswertung in openrouter.py.

Die Arbeitsumgebung erreicht openrouter.ai nicht, der echte Aufruf laeuft
erst auf dem Runner. Was sich hier trotzdem pruefen laesst: dass aus einer
Antwort ein richtiger Bericht wird -- und vor allem, dass ein Fehlschlag
auch als Fehlschlag im Bericht steht und nicht stillschweigend als leere
Tabelle durchgeht. Ein gruener Lauf mit "HTTP 401" im Bericht waere die
schlechteste aller Rueckmeldungen.

Lauf: python3 scripts/probe_openrouter.py
"""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "openrouter", Path(__file__).parent / "openrouter.py")
o = importlib.util.module_from_spec(spec)
sys.argv = ["probe"]
spec.loader.exec_module(o)

GUT = {
    "stand": "2026-08-10",
    # Kein "label" mehr: das Feld enthaelt bei OpenRouter den maskierten
    # Schluessel und wird vor dem Bericht herausgefiltert.
    "schluessel": {"data": {"limit": 5, "usage": 0.12,
                            "limit_remaining": 4.88,
                            "is_free_tier": False}},
    "guthaben": {"data": {"total_credits": 5, "total_usage": 0.12}},
    "modelle": [
        {"id": "teuer/gross", "name": "Gross", "kontext": 200000,
         "preis_eingabe": 15.0, "preis_ausgabe": 75.0},
        {"id": "billig/klein", "name": "Klein", "kontext": 32000,
         "preis_eingabe": 0.05, "preis_ausgabe": 0.2},
        {"id": "gratis/modell", "name": "Gratis", "kontext": 8000,
         "preis_eingabe": 0.0, "preis_ausgabe": 0.0},
    ],
    "kostenlos": ["gratis/modell"],
    "guenstigstes": "billig/klein",
    "probe": {"modell": "billig/klein", "antwort": "Ein Hundesofa ist ...",
              "verbrauch": {"total_tokens": 42}},
}

SCHLECHT = {
    "stand": "2026-08-10",
    "schluessel": {"fehler": "HTTP 401",
                   "text": '{"error":{"message":"No auth credentials found"}}'},
    "guthaben": {"fehler": "HTTP 401", "text": "..."},
    "modelle": [],
    "probe": {"modell": "billig/klein", "fehler": "HTTP 402",
              "text": '{"error":{"message":"Insufficient credits"}}'},
}


def main() -> int:
    fehler = 0

    b = o.bericht(GUT)
    for muss in ("4.88", "billig/klein", "0.0500 $", "gratis/modell",
                 "Ein Hundesofa ist", "3 Modelle erreichbar"):
        if muss not in b:
            print(f"FEHLER  Erfolgsfall: '{muss}' fehlt im Bericht"); fehler += 1
    # Das teure Modell muss zwar auftauchen, aber hinter dem billigen.
    if b.index("billig/klein") > b.index("teuer/gross"):
        print("FEHLER  Erfolgsfall: nicht nach Preis sortiert"); fehler += 1
    if not fehler:
        print("OK      Erfolgsfall: Schluessel, Preise, Sortierung, Antwort")

    v = fehler
    b2 = o.bericht(SCHLECHT)
    for muss in ("HTTP 401", "No auth credentials", "HTTP 402",
                 "Insufficient credits", "Fehlgeschlagen"):
        if muss not in b2:
            print(f"FEHLER  Fehlerfall: '{muss}' fehlt im Bericht"); fehler += 1
    # Der Fehlerfall darf nicht wie ein Erfolg aussehen.
    if "Modelle erreichbar" in b2:
        print("FEHLER  Fehlerfall: meldet trotzdem erreichbare Modelle")
        fehler += 1
    if fehler == v:
        print("OK      Fehlerfall: 401 und 402 stehen samt Grund im Bericht")

    # Preisumrechnung: Dollar je Token -> Dollar je Million Token.
    v = fehler
    e, a = o.preis({"pricing": {"prompt": "0.0000005", "completion": "0.0000015"}})
    if round(e, 4) != 0.5 or round(a, 4) != 1.5:
        print(f"FEHLER  Preis falsch umgerechnet: {e}, {a}"); fehler += 1
    # Kaputte Angaben duerfen nicht abstuerzen, sondern muessen 0 ergeben.
    if o.preis({"pricing": {"prompt": None, "completion": "keine Zahl"}}) != (0.0, 0.0):
        print("FEHLER  kaputte Preisangabe nicht abgefangen"); fehler += 1
    if o.preis({}) != (0.0, 0.0):
        print("FEHLER  fehlende Preisangabe nicht abgefangen"); fehler += 1
    if fehler == v:
        print("OK      Preisumrechnung, auch bei fehlenden und kaputten Werten")

    # Der Fall, der am 10.08.2026 wirklich passiert ist: OpenRouters
    # /key liefert unter "label" den maskierten Schluessel, nicht einen
    # selbstgewaehlten Namen. Er stand danach im oeffentlichen Repository.
    # Geprueft wird mit der echten Antwortform, samt Feldern, die es damals
    # gab -- und mit einem erfundenen neuen Feld, denn eine Positivliste
    # ist nur dann eine, wenn sie Unbekanntes ebenfalls aussperrt.
    v = fehler
    echt = {"data": {
        "label": "sk-or-v1-cc8...4b5",
        "creator_user_id": "user_12345",
        "irgendein_neues_feld": "kann morgen dazukommen",
        "limit": None, "usage": 0, "is_free_tier": True,
    }}
    sauber = o.ohne_geheimnis(echt)
    uebrig = set(sauber["data"])
    for verboten in ("label", "creator_user_id", "irgendein_neues_feld"):
        if verboten in uebrig:
            print(f"FEHLER  Geheimnisfilter laesst '{verboten}' durch")
            fehler += 1
    for noetig in ("limit", "usage", "is_free_tier"):
        if noetig not in uebrig:
            print(f"FEHLER  Geheimnisfilter verschluckt '{noetig}'")
            fehler += 1
    # Und das Ganze bis in den Bericht hinein, nicht nur im Filter.
    if "sk-or-v1" in o.bericht({"stand": "x", "schluessel": echt}):
        print("FEHLER  Schluesselfragment steht im Bericht"); fehler += 1
    # Ein Fehlerobjekt ohne "data" muss unveraendert durchgehen.
    if o.ohne_geheimnis({"fehler": "HTTP 401"}) != {"fehler": "HTTP 401"}:
        print("FEHLER  Fehlerobjekt wurde veraendert"); fehler += 1
    if fehler == v:
        print("OK      Geheimnisfilter: label, Konto-ID und unbekannte "
              "Felder bleiben draussen")

    # Modellwahl fuer den Rundlauf. Der Schluessel vom 10.08.2026 hatte
    # null Guthaben; die urspruengliche Wahl nahm trotzdem das guenstigste
    # BEZAHLTE Modell und waere zuverlaessig an HTTP 402 gescheitert --
    # was wie ein kaputter Zugang ausgesehen haette.
    v = fehler
    liste = [
        {"id": "teuer/gross", "context_length": 200000,
         "pricing": {"prompt": "0.000015", "completion": "0.000075"}},
        {"id": "billig/klein", "context_length": 32000,
         "pricing": {"prompt": "0.00000005", "completion": "0.0000002"}},
        {"id": "gratis/gross", "context_length": 128000,
         "pricing": {"prompt": "0", "completion": "0"}},
        {"id": "gratis/winzig", "context_length": 4096,
         "pricing": {"prompt": "0", "completion": "0"}},
    ]
    mit = o.anwaerter(liste, guthaben=True)
    if not mit or mit[0] != "billig/klein":
        print(f"FEHLER  mit Guthaben nicht das billigste bezahlte: {mit}")
        fehler += 1
    if "gratis/gross" in mit:
        print("FEHLER  mit Guthaben ein Gratismodell vorgeschlagen"); fehler += 1

    ohne = o.anwaerter(liste, guthaben=False)
    if [x for x in ohne if x.startswith(("teuer/", "billig/"))]:
        print(f"FEHLER  ohne Guthaben ein bezahltes Modell vorgeschlagen: {ohne}")
        fehler += 1
    if ohne[:1] != ["gratis/gross"]:
        print(f"FEHLER  ohne Guthaben nicht das groesste Gratismodell zuerst: {ohne}")
        fehler += 1
    # Mehrere Anwaerter, sonst haengt das Ergebnis an einem gedrosselten
    # fremden Server.
    if len(ohne) < 2:
        print("FEHLER  nur ein Anwaerter ohne Guthaben"); fehler += 1
    if o.anwaerter([], guthaben=False) != []:
        print("FEHLER  leere Modelliste nicht abgefangen"); fehler += 1
    if fehler == v:
        print("OK      Modellwahl: mit Guthaben bezahlt, ohne Guthaben gratis, "
              "mehrere Anwaerter")

    # Fehlversuche muessen auch bei Erfolg im Bericht stehen.
    v = fehler
    b3 = o.bericht({"stand": "x", "modelle": [], "probe": {
        "modell": "gratis/gross", "auswahl": "Gratisstufe",
        "antwort": "Ein Satz.", "verbrauch": {"total_tokens": 9},
        "versuche": [{"modell": "gratis/winzig", "fehler": "HTTP 429",
                      "text": "rate limited"}]}})
    for muss in ("Davor abgelehnt", "gratis/winzig", "HTTP 429", "Ein Satz."):
        if muss not in b3:
            print(f"FEHLER  Fehlversuche fehlen im Bericht: '{muss}'"); fehler += 1
    if fehler == v:
        print("OK      Fehlversuche stehen auch bei Erfolg im Bericht")

    # Modalitaetsfilter. Der echte Fall: google/lyria-3-* sind
    # Musikmodelle, standen aber vorn und gaben HTTP 502.
    v = fehler
    faelle = [
        ("Sprachmodell", {"architecture": {"input_modalities": ["text"],
                                           "output_modalities": ["text"]}}, True),
        ("Musikmodell", {"architecture": {"input_modalities": ["text"],
                                          "output_modalities": ["audio"]}}, False),
        ("Bildgenerator", {"architecture": {"input_modalities": ["text"],
                                            "output_modalities": ["image"]}}, False),
        ("Modell mit Bildeingabe, Textausgabe",
         {"architecture": {"input_modalities": ["text", "image"],
                           "output_modalities": ["text"]}}, True),
        # Fehlt die Angabe, lieber zulassen als stillschweigend verwerfen.
        ("ohne architecture", {}, True),
        ("architecture leer", {"architecture": {}}, True),
    ]
    for name, m, soll in faelle:
        if o.schreibt_text(m) != soll:
            print(f"FEHLER  Modalitaet/{name}: erwartet {soll}"); fehler += 1
    # Und in der Auswahl: das Musikmodell darf trotz groesstem Kontext
    # nicht vorgeschlagen werden.
    liste = [
        {"id": "musik/gross", "context_length": 999999,
         "pricing": {"prompt": "0", "completion": "0"},
         "architecture": {"input_modalities": ["text"],
                          "output_modalities": ["audio"]}},
        {"id": "sprache/klein", "context_length": 8000,
         "pricing": {"prompt": "0", "completion": "0"},
         "architecture": {"input_modalities": ["text"],
                          "output_modalities": ["text"]}},
    ]
    if o.anwaerter(liste, guthaben=False) != ["sprache/klein"]:
        print(f"FEHLER  Musikmodell trotzdem vorgeschlagen: "
              f"{o.anwaerter(liste, guthaben=False)}")
        fehler += 1
    if fehler == v:
        print("OK      Modalitaetsfilter: Musik und Bild raus, Text bleibt")

    # Bildfaehige Modelle. Anlass: statt eines lokal zu installierenden
    # Bildwerkzeugs (kein GPU hier, Gewichte ausserhalb GitHub/PyPI/npm
    # nicht erreichbar) erst pruefen, was OpenRouter selbst kann.
    v = fehler
    faelle_bild = [
        ("Bildausgabe", {"architecture": {"input_modalities": ["text", "image"],
                                          "output_modalities": ["image"]}}, True),
        ("nur Text", {"architecture": {"input_modalities": ["text"],
                                       "output_modalities": ["text"]}}, False),
        ("ohne architecture", {}, False),
    ]
    for name, m, soll in faelle_bild:
        if o.gibt_bild_aus(m) != soll:
            print(f"FEHLER  Bildfilter/{name}: erwartet {soll}"); fehler += 1
    if fehler == v:
        print("OK      Bildfilter: nur echte output_modalities=image zaehlt")

    # Der Fall vom 12.08.2026: "openrouter/auto" hat Preis "-1" je Token
    # (variabler Tarif eines Routers, kein echter Preis). Hochgerechnet
    # auf eine Million Token wurde daraus -1.000.000 $, und das Modell
    # stand als "guenstigstes" ganz oben in der Bildmodell-Liste.
    v = fehler
    auto_router = {"id": "openrouter/auto", "context_length": 999999,
                   "pricing": {"prompt": "-1", "completion": "-1"},
                   "architecture": {"input_modalities": ["text", "image"],
                                    "output_modalities": ["text", "image"]}}
    e, a = o.preis(auto_router)
    if not (e < 0 and a < 0):
        print("FEHLER  Testaufbau: negativer Preis kommt nicht mehr zustande "
              "-- pruefe, ob dieser Fall noch zutrifft"); fehler += 1
    if o.gibt_bild_aus(auto_router) is not True:
        print("FEHLER  Router mit Bildausgabe wird nicht als bildfaehig "
              "erkannt"); fehler += 1
    echt_bild = {"id": "bild/echt", "context_length": 8000,
                 "pricing": {"prompt": "0.000001", "completion": "0.000002"},
                 "architecture": {"input_modalities": ["text"],
                                  "output_modalities": ["image"]}}
    gefiltert = [m for m in [auto_router, echt_bild]
                if o.gibt_bild_aus(m) and sum(o.preis(m)) >= 0]
    if [m["id"] for m in gefiltert] != ["bild/echt"]:
        print(f"FEHLER  Router mit Negativpreis nicht ausgefiltert: "
              f"{[m['id'] for m in gefiltert]}"); fehler += 1
    if fehler == v:
        print("OK      Router mit variablem (negativem) Preis fliegt aus "
              "der Bildmodell-Liste, echtes Bildmodell bleibt")

    # Bericht muss den Leerfall ausdruecklich benennen, nicht stillschweigend
    # weglassen -- "nichts gefunden" ist ein Ergebnis, kein fehlender
    # Abschnitt.
    v = fehler
    b4 = o.bericht({"stand": "x", "modelle": [
        {"id": "text/eins", "name": "Eins", "kontext": 8000,
         "preis_eingabe": 0.1, "preis_ausgabe": 0.2}], "bild_modelle": []})
    if "Bildfähige Modelle" not in b4 or "Keins gefunden" not in b4:
        print("FEHLER  Leerfall bei Bildmodellen nicht ausgewiesen"); fehler += 1
    b5 = o.bericht({"stand": "x", "modelle": [
        {"id": "bild/eins", "name": "Bild", "kontext": 8000,
         "preis_eingabe": 1.0, "preis_ausgabe": 2.0}],
        "bild_modelle": [{"id": "bild/eins", "name": "Bild",
                          "rein": ["text", "image"], "raus": ["image"],
                          "preis_eingabe": 1.0, "preis_ausgabe": 2.0}]})
    for muss in ("bild/eins", "1 von 1 Modellen", "text, image"):
        if muss not in b5:
            print(f"FEHLER  Erfolgsfall Bildmodelle: '{muss}' fehlt"); fehler += 1
    if fehler == v:
        print("OK      Bildmodelle im Bericht: Leerfall und Erfolgsfall getrennt")

    print(f"\nFehlschlaege: {fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
