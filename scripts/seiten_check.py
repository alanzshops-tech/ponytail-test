#!/usr/bin/env python3
"""
seiten_check.py — prüft, was Google von homeeins.de ausgeliefert bekommt.

Anlass: Die Search Console zeigt zehn Seiten auf Position 1 bis 5 mit null
Klicks, darunter mehrere unter /en/. Die Stichprobe ergab ein gespaltenes
Bild: Produkt-URLs unter /en/ leiten sauber auf die deutsche Fassung um,
/en/collections/gartenmobel dagegen antwortet mit 200, deklariert
lang="en", zeigt deutschen Text und erklärt sich selbst zur kanonischen
Adresse. Damit konkurriert eine zweite URL mit der echten Seite.

Offen war nur: betrifft das zwei Seiten oder zweihundert? Diese Frage
beantwortet der Sitemap-Modus. Er liest die Sitemap, prüft jede deutsche
Adresse und dazu ihre /en/-Entsprechung und zählt aus, welches Muster wie
oft vorkommt.

Zwei Betriebsarten:
    python3 scripts/seiten_check.py --urls urls.txt          # Stichprobe
    python3 scripts/seiten_check.py --sitemap https://...    # vollständig

Warum das auf dem Runner läuft und nicht hier: Die Arbeitsumgebung erreicht
nur GitHub und PyPI. Der Shop ist von hier aus unsichtbar — unabhängig
davon, welche Bibliothek die Anfrage stellt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import time
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

WEITERLEITUNG = (301, 302, 303, 307, 308)

# Attributwert in beliebiger Schreibweise: "wert", 'wert' oder wert.
# Shopify liefert doppelte Anführungszeichen, aber das ist eine Annahme
# über fremdes HTML, die ich von hier aus nicht nachprüfen kann — und eine
# fehlende Canonical-Angabe zu melden, die in Wahrheit nur anders
# geschrieben ist, wäre der teuerste Fehler dieses Skripts.
W = r"""["']?([^"'>\s]+)["']?"""
QC = r"""["']?canonical["']?"""

# Sequenziell, mit Pause. Der erste vollständige Lauf holte mit sechs
# parallelen Verbindungen 263 von 304 Adressen als HTTP 429 — Shopify
# drosselt deutlich früher als erwartet. Ein Crawl, der gedrosselt wird,
# liefert kein schnelles Ergebnis, sondern gar keins.
PAUSE_START = 1.0      # Sekunden zwischen zwei Abrufen
PAUSE_MAX = 8.0
VERSUCHE = 4           # je Adresse, bei 429

# Funktionswörter trennen Sprachen zuverlässiger als Inhaltswörter, weil
# Produktnamen oft in beiden Sprachen gleich sind ("Rattan", "Design").
DE = re.compile(r"\b(und|oder|mit|für|nicht|dein|deine|das|die|der|ist|"
                r"auch|bei|aus|wird|kann|sich|mehr)\b", re.I)
EN = re.compile(r"\b(and|or|with|for|not|your|the|is|also|from|will|can|"
                r"more|this|that)\b", re.I)


def holen(url: str, folgen: bool = True):
    """Seite laden. Gibt (Status, Endadresse, HTML, Wartehinweis) zurück.

    Der Wartehinweis ist der Retry-After-Wert in Sekunden, sonst 0."""
    class Stopp(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    bauer = urllib.request.build_opener(*([] if folgen else [Stopp]))
    anfrage = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Language": "de-DE,de;q=0.9"})
    try:
        with bauer.open(anfrage, timeout=25) as a:
            return a.status, a.url, a.read().decode("utf-8", "replace"), 0
    except urllib.error.HTTPError as e:
        try:
            warte = int(e.headers.get("Retry-After") or 0)
        except ValueError:                    # auch ein Datum ist erlaubt
            warte = 10
        return e.code, e.headers.get("Location", url), "", warte
    except Exception as e:                                    # noqa: BLE001
        return 0, str(e), "", 0


class Bremse:
    """Hält das Tempo und zieht an, sobald der Shop drosselt.

    Die Pause wächst bei jedem 429 und sinkt nach erfolgreichen Abrufen
    langsam wieder — so tastet sich der Lauf an das erlaubte Tempo heran,
    statt pauschal langsam zu sein oder pauschal zu schnell."""

    def __init__(self) -> None:
        self.pause = PAUSE_START
        self.gedrosselt = 0
        self.gut_in_folge = 0

    def abrufen(self, url: str, folgen: bool = False):
        for versuch in range(1, VERSUCHE + 1):
            time.sleep(self.pause)
            status, ziel, html, warte = holen(url, folgen)
            if status != 429:
                self.gut_in_folge += 1
                if self.gut_in_folge >= 20 and self.pause > PAUSE_START:
                    self.pause = max(PAUSE_START, self.pause / 1.5)
                    self.gut_in_folge = 0
                return status, ziel, html
            self.gedrosselt += 1
            self.gut_in_folge = 0
            self.pause = min(PAUSE_MAX, self.pause * 2)
            ruhe = max(warte, self.pause * versuch)
            print(f"    429 bei {url} — warte {ruhe:.0f}s "
                  f"(Versuch {versuch}/{VERSUCHE}, Takt jetzt {self.pause:.1f}s)")
            time.sleep(ruhe)
        return 429, url, ""


def kopfdaten(html: str) -> dict:
    def eins(muster):
        t = re.search(muster, html, re.I | re.S)
        return unescape(t.group(1).strip()) if t else ""

    hreflang = [(m.group(1), m.group(2)) for m in re.finditer(
        rf'<link[^>]+hreflang={W}[^>]+href={W}', html, re.I)]
    # Skripte und Stile raus, sonst zählt die Heuristik JavaScript mit.
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    de, en = len(DE.findall(text)), len(EN.findall(text))
    # Schwelle bewusst niedrig: Auf echten Produktseiten liegen die Werte
    # im dreistelligen Bereich. Acht genuegt, um Rauschen auszuschliessen,
    # ohne ein eindeutiges Signal auf duennen Seiten zu verwerfen.
    if de + en < 8:
        sprache = "zu wenig Text"
    else:
        sprache = "Deutsch" if de > en * 1.3 else (
            "Englisch" if en > de * 1.3 else "gemischt")
    return {
        "lang_attribut": eins(rf'<html[^>]+\blang={W}'),
        "titel": eins(r"<title[^>]*>(.*?)</title>"),
        "canonical": eins(rf'<link[^>]+rel={QC}[^>]+href={W}')
                     or eins(rf'<link[^>]+href={W}[^>]+rel={QC}'),
        "hreflang": hreflang,
        "de_woerter": de,
        "en_woerter": en,
        "textsprache": f"{sprache} (de {de} / en {en})",
        "sprache": sprache,
    }


# ---------------------------------------------------------------- Stichprobe

def pruefen(url: str) -> None:
    print(f"\n=== {url} ===")
    status, ziel, _, _ = holen(url, folgen=False)
    if status in WEITERLEITUNG:
        print(f"  {status} Weiterleitung -> {ziel}")
    status, endziel, html, _ = holen(url)
    print(f"  Status {status}, gelandet bei: {endziel}")
    if not html:
        print("  kein HTML erhalten")
        return
    k = kopfdaten(html)
    print(f"  html lang   : {k['lang_attribut'] or '—'}")
    print(f"  Titel       : {k['titel'][:80]}")
    print(f"  Canonical   : {k['canonical'] or '—'}")
    print(f"  Textsprache : {k['textsprache']}")
    if k["hreflang"]:
        print("  hreflang    :")
        for sp, ziel_url in k["hreflang"][:8]:
            print(f"      {sp:<8} {ziel_url}")
    else:
        print("  hreflang    : keine")


# ------------------------------------------------------------------ Sitemap

def sitemap_lesen(url: str, tiefe: int = 0) -> list[str]:
    """Sitemap oder Sitemap-Index rekursiv auflösen."""
    if tiefe > 3:                       # Schutz vor zirkulären Verweisen
        return []
    status, _, xml, _ = holen(url)
    if status != 200 or not xml:
        print(f"  Sitemap nicht lesbar: {url} (Status {status})",
              file=sys.stderr)
        return []
    try:
        wurzel = ET.fromstring(xml)
    except ET.ParseError as e:
        print(f"  Sitemap unlesbar: {url} ({e})", file=sys.stderr)
        return []

    # Namensraum abstreifen: Shopify liefert sitemaps.org-XML, aber der
    # Präfix ist nicht garantiert. Auf den lokalen Namen zu prüfen ist
    # robuster als ihn fest zu verdrahten.
    def lokal(el):
        return el.tag.rsplit("}", 1)[-1]

    adressen: list[str] = []
    for kind in wurzel:
        name = lokal(kind)
        ort = next((e.text.strip() for e in kind
                    if lokal(e) == "loc" and e.text), None)
        if not ort:
            continue
        if name == "sitemap":
            print(f"  -> Untersitemap {ort}")
            adressen += sitemap_lesen(ort, tiefe + 1)
        elif name == "url":
            adressen.append(ort)
    return adressen


def gattung(url: str) -> str:
    pfad = urlsplit(url).path
    for stueck, name in (("/products/", "Produkte"),
                         ("/collections/", "Kollektionen"),
                         ("/blogs/", "Blog"),
                         ("/pages/", "Seiten")):
        if stueck in pfad:
            return name
    return "Start und Sonstiges"


def en_variante(url: str) -> str:
    """https://host/products/x  ->  https://host/en/products/x"""
    t = urlsplit(url)
    return urlunsplit((t.scheme, t.netloc, "/en" + t.path, t.query, ""))


def ohne_schraegstrich(url: str) -> str:
    t = urlsplit(url)
    return urlunsplit((t.scheme, t.netloc, t.path.rstrip("/"), "", ""))


def abrufen(bremse: "Bremse", url: str, ist_en: bool) -> dict:
    """Eine Adresse prüfen. Nur EIN Abruf, ohne Weiterleitungen zu folgen —
    bei einer Weiterleitung interessiert das Ziel, nicht dessen Inhalt."""
    status, ziel, html = bremse.abrufen(url, folgen=False)
    e = {"url": url, "ist_en": ist_en, "status": status, "ziel": ziel,
         "gattung": gattung(url)}
    if status == 200 and html:
        k = kopfdaten(html)
        e["hreflang_anzahl"] = len(k.pop("hreflang"))
        e.update(k)
    e["code"], e["befund"] = urteil(e)
    return e


# Jeder Befund bekommt einen Code. Der erste vollständige Lauf hat gezeigt,
# warum: Die Auswertung filterte über den Text ("beginnt mit FEHLER"), und
# damit landeten 263 gedrosselte Abrufe in der Liste der Seiten, die mit
# ihrer deutschen Fassung konkurrieren. Die Überschrift meldete 152
# Duplikate, wo in Wahrheit kein einziges HTML angekommen war. Ein Code
# kann nicht versehentlich zu einem anderen passen.
def urteil(e: dict) -> tuple[str, str]:
    st = e["status"]
    if st == 0:
        return "unerreichbar", "nicht erreichbar"
    if st == 429:
        return "gedrosselt", "gedrosselt (429), nicht geprüft"
    if st in WEITERLEITUNG:
        return "weiterleitung", f"leitet weiter -> {e['ziel']}"
    if st == 404:
        # Unter /en/ ist 404 unschoen, aber harmlos: nichts wird indexiert.
        return ("en_404", "404") if e["ist_en"] else \
               ("de_404", "404 auf deutscher Adresse")
    if st != 200:
        return "http_fehler", f"HTTP {st}"

    eigen = ohne_schraegstrich(e.get("canonical", "")) == ohne_schraegstrich(e["url"])
    deutsch = e.get("sprache") == "Deutsch"
    lang_en = e.get("lang_attribut", "").lower().startswith("en")

    if e["ist_en"]:
        if eigen and deutsch:
            return "duplikat", ("deutscher Inhalt unter /en/, kanonisch "
                                "auf sich selbst")
        if eigen:
            return "en_selbstkanonisch", "/en/ erklärt sich selbst zur kanonischen Adresse"
        if lang_en and deutsch:
            return "en_lang_falsch", "lang=en, Text deutsch"
        if not e.get("canonical"):
            return "kein_canonical", "kein Canonical"
        return "en_ok", "ok (verweist auf die deutsche Fassung)"

    if not e.get("canonical"):
        return "kein_canonical", "kein Canonical"
    if not eigen:
        return "canonical_fremd", f"Canonical zeigt woanders hin: {e['canonical']}"
    return "ok", "ok"


# Codes, die Handlungsbedarf bedeuten — getrennt von denen, die nur sagen,
# dass die Prüfung nicht stattgefunden hat.
PROBLEM = {"duplikat", "en_selbstkanonisch", "en_lang_falsch",
           "kein_canonical", "canonical_fremd", "de_404", "http_fehler"}
UNGEPRUEFT = {"gedrosselt", "unerreichbar"}


def liste(z: list[str], eintraege: list[dict], max_zeilen: int = 40) -> None:
    for e in sorted(eintraege, key=lambda x: x["url"])[:max_zeilen]:
        titel = f" — {e['titel'][:60]}" if e.get("titel") else ""
        z.append(f"- `{urlsplit(e['url']).path}` — {e['befund']}{titel}")
    if len(eintraege) > max_zeilen:
        z.append(f"- … und {len(eintraege) - max_zeilen} weitere")
    z.append("")


def bericht(daten: dict) -> str:
    eintraege = daten["eintraege"]
    en = [e for e in eintraege if e["ist_en"]]
    de = [e for e in eintraege if not e["ist_en"]]
    ungeprueft = [e for e in eintraege if e["code"] in UNGEPRUEFT]
    dupl = [e for e in en if e["code"] == "duplikat"]
    en_warn = [e for e in en if e["code"] in PROBLEM and e["code"] != "duplikat"]
    de_prob = [e for e in de if e["code"] in PROBLEM]

    z = ["# Seitenprüfung — homeeins.de", "",
         f"Stand: {daten['stand']} · Quelle: {daten['sitemap']}", "",
         f"{len(de)} deutsche Adressen aus der Sitemap, dazu je die "
         f"/en/-Entsprechung ({len(eintraege)} Abrufe).", ""]

    # Zuerst die Belastbarkeit, dann der Befund. Ein Bericht, der die
    # Luecke verschweigt, ist schlimmer als gar keiner: Er liest sich
    # vollstaendig.
    if ungeprueft:
        anteil = round(len(ungeprueft) / len(eintraege) * 100)
        z += [f"> **{len(ungeprueft)} von {len(eintraege)} Abrufen ({anteil} %) "
              f"kamen nicht durch** — gedrosselt oder nicht erreichbar. "
              f"Die Zahlen unten beziehen sich nur auf die "
              f"{len(eintraege) - len(ungeprueft)} tatsächlich gelesenen "
              f"Seiten.", ""]
        if anteil > 25:
            z += ["> Bei dieser Ausfallquote ist der Lauf **nicht "
                  "aussagekräftig**. Er sollte langsamer wiederholt werden.", ""]

    n = len(dupl)
    if dupl:
        z += [f"## {n} /en/-{'Adresse' if n == 1 else 'Adressen'} "
              f"{'konkurriert' if n == 1 else 'konkurrieren'} mit der "
              f"deutschen Seite", "",
              "Diese Adressen antworten mit 200, zeigen deutschen Text "
              "und erklären sich **selbst** zur kanonischen Adresse. Damit "
              "sieht Google zwei gleichwertige Seiten mit demselben Inhalt "
              "und muss raten, welche gemeint ist.", ""]
        liste(z, dupl, 60)
    else:
        z += ["## Keine selbstkanonischen /en/-Seiten unter den gelesenen "
              "Adressen", "",
              "Alle geprüften /en/-Adressen leiten weiter, laufen ins 404 "
              "oder verweisen kanonisch auf die deutsche Fassung.", ""]

    if en_warn:
        z += [f"## {len(en_warn)} weitere /en/-Auffälligkeiten", ""]
        liste(z, en_warn)

    if de_prob:
        z += [f"## {len(de_prob)} Auffälligkeiten auf deutschen Adressen", ""]
        liste(z, de_prob)

    z += ["## Verteilung nach Gattung", "",
          "| Gattung | deutsch | /en/ leitet weiter | /en/ 404 | "
          "/en/ Duplikat | nicht geprüft |",
          "|---|---:|---:|---:|---:|---:|"]
    for g in sorted({e["gattung"] for e in eintraege}):
        def zaehl(menge, *codes):
            return sum(1 for e in menge
                       if e["gattung"] == g and e["code"] in codes)
        z.append(f"| {g} | {sum(1 for e in de if e['gattung'] == g)} "
                 f"| {zaehl(en, 'weiterleitung')} | {zaehl(en, 'en_404')} "
                 f"| {zaehl(en, 'duplikat')} "
                 f"| {zaehl(eintraege, *UNGEPRUEFT)} |")
    z.append("")

    # Gezählt wird über den Code, nicht über den Befundtext. Der Text
    # enthält bei Weiterleitungen das Ziel und ist damit für jede Adresse
    # verschieden — die Tabelle hätte sonst 97 Zeilen mit je einer Eins.
    z += ["## Alle Befunde gezählt", "",
          "| Befund | Anzahl |", "|---|---:|"]
    namen = {"ok": "ok", "en_ok": "/en/ verweist auf die deutsche Fassung",
             "weiterleitung": "leitet weiter", "en_404": "/en/ 404",
             "de_404": "404 auf deutscher Adresse",
             "duplikat": "deutscher Inhalt unter /en/, kanonisch auf sich selbst",
             "en_selbstkanonisch": "/en/ kanonisch auf sich selbst",
             "en_lang_falsch": "lang=en, Text deutsch",
             "kein_canonical": "kein Canonical",
             "canonical_fremd": "Canonical zeigt woanders hin",
             "gedrosselt": "gedrosselt (429)", "unerreichbar": "nicht erreichbar",
             "http_fehler": "sonstiger HTTP-Fehler"}
    for code, anzahl in Counter(e["code"] for e in eintraege).most_common():
        z.append(f"| {namen.get(code, code)} | {anzahl} |")
    return "\n".join(z) + "\n"


def crawl(sitemap: str, limit: int, out: Path) -> int:
    print(f"Sitemap lesen: {sitemap}")
    roh = sitemap_lesen(sitemap)
    # Adressen, die die Sitemap schon selbst unter /en/ führt, kämen sonst
    # doppelt vor — einmal als Fund, einmal als abgeleitete Variante.
    deutsch = sorted({u for u in roh if "/en/" not in urlsplit(u).path})
    if not deutsch:
        sys.exit("Sitemap enthielt keine brauchbaren Adressen.")
    if limit:
        deutsch = deutsch[:limit]
    print(f"{len(roh)} Adressen in der Sitemap, {len(deutsch)} deutsche "
          f"werden geprüft (dazu je die /en/-Fassung)")

    auftraege = [(u, False) for u in deutsch] + \
                [(en_variante(u), True) for u in deutsch]

    bremse = Bremse()
    eintraege: list[dict] = []
    for i, (u, ist_en) in enumerate(auftraege, 1):
        eintraege.append(abrufen(bremse, u, ist_en))
        if i % 25 == 0 or i == len(auftraege):
            print(f"  {i}/{len(auftraege)} abgerufen "
                  f"(Takt {bremse.pause:.1f}s, {bremse.gedrosselt}x gedrosselt)")

    daten = {"stand": str(date.today()), "sitemap": sitemap,
             "eintraege": eintraege}
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(daten, ensure_ascii=False, indent=2)
    (out / f"seiten-{daten['stand']}.json").write_text(text, encoding="utf-8")
    (out / "seiten-aktuell.json").write_text(text, encoding="utf-8")
    Path("SEITEN.md").write_text(bericht(daten), encoding="utf-8")

    dupl = sum(1 for e in eintraege if e["code"] == "duplikat")
    fehlt = sum(1 for e in eintraege if e["code"] in UNGEPRUEFT)
    print(f"\nFertig. {dupl} /en/-Adressen konkurrieren mit ihrer deutschen "
          f"Fassung, {fehlt} Abrufe kamen nicht durch. Bericht in SEITEN.md")
    # Bewusst kein Abbruch: Der Befund ist das Ergebnis, kein Fehlschlag.
    # Ein roter Lauf würde die Zahl verstecken, statt sie zu zeigen.
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", help="Datei mit einer URL je Zeile (Stichprobe)")
    ap.add_argument("--sitemap", help="Sitemap-Adresse (vollständiger Lauf)")
    ap.add_argument("--out", default="daten")
    ap.add_argument("--limit", type=int, default=0,
                    help="nur die ersten N Adressen (zum Ausprobieren)")
    # Der Bericht soll sich ohne neuen Crawl neu erzeugen lassen. Sonst
    # verleitet jede Verbesserung an der Darstellung zu einem weiteren
    # Lauf gegen den Shop.
    ap.add_argument("--bericht-aus", dest="bericht_aus",
                    help="SEITEN.md aus einer vorhandenen JSON neu schreiben")
    a = ap.parse_args()

    if a.bericht_aus:
        daten = json.loads(Path(a.bericht_aus).read_text(encoding="utf-8"))
        Path("SEITEN.md").write_text(bericht(daten), encoding="utf-8")
        print(f"SEITEN.md aus {a.bericht_aus} neu geschrieben "
              f"({len(daten['eintraege'])} Einträge)")
        return

    if a.sitemap:
        sys.exit(crawl(a.sitemap, a.limit, Path(a.out)))

    if not a.urls:
        sys.exit("Entweder --urls oder --sitemap angeben.")
    zeilen = [z.strip() for z in open(a.urls, encoding="utf-8")
              if z.strip() and not z.startswith("#")]
    if not zeilen:
        sys.exit("Keine URLs angegeben")
    for u in zeilen:
        pruefen(u)
    print(f"\n{len(zeilen)} URLs geprüft")


if __name__ == "__main__":
    main()
