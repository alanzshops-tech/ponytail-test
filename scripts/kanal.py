#!/usr/bin/env python3
"""Zustandsverwaltung für den YouTube-Kanal.

Warum SQLite und nicht JSON: Die Produktion laeuft parallel (die
Reels-Matrix rendert zwoelf Jobs gleichzeitig). Zwei Jobs, die
gleichzeitig dieselbe JSON-Datei schreiben, verlieren einen Stand --
lautlos. SQLite hat dafuer Transaktionen.

Warum nur die Standardbibliothek: make_reels.py braucht Piper,
audio_check.py braucht faster-whisper -- beides schwere Pakete, die nur
auf dem Runner stehen. Die Zustandsverwaltung muss aber ueberall
laufen, auch in der abgeschotteten Arbeitsumgebung, sonst laesst sie
sich nicht pruefen.

Der Ablauf ist eine Kette, kein freies Feld:

    thema -> bewertet -> skript -> geprueft -> gerendert
          -> ton_ok -> entwurf -> freigegeben -> geplant -> veroeffentlicht

Ein Schritt darf nur auf seinen Nachfolger. Das ist der Kern der
Sicherheitsregel aus Phase 4: Wer die Faktenpruefung nicht bestanden
hat, kann nicht gerendert werden, und wer die Tonpruefung nicht
bestanden hat, kann nicht hochgeladen werden -- nicht aus Disziplin,
sondern weil die Datenbank es ablehnt.

'gescheitert' ist von jedem Schritt aus erreichbar und traegt immer
einen Grund.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_STANDARD = Path("daten/kanal.sqlite")

# Die Kette. Reihenfolge ist bedeutsam: Der Index bestimmt, was als
# naechster Schritt erlaubt ist.
KETTE = (
    "thema",          # Idee erfasst, Quellen dabei
    "bewertet",       # Nachfrage/Originalitaet/Kosten bewertet
    "skript",         # Sprechertext und Szenenplan liegen vor
    "geprueft",       # Fakten geprueft, unsichere Aussagen markiert
    "gerendert",      # MP4 existiert
    "ton_ok",         # audio_check.py bestanden
    "entwurf",        # als privat/Entwurf hochgeladen
    "freigegeben",    # Mensch hat zugestimmt
    "geplant",        # Termin steht
    "veroeffentlicht",
)
GESCHEITERT = "gescheitert"

SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    schluessel  TEXT    NOT NULL UNIQUE,
    titel       TEXT    NOT NULL,
    nische      TEXT    NOT NULL DEFAULT 'nachgemessen',
    status      TEXT    NOT NULL DEFAULT 'thema',
    angelegt    TEXT    NOT NULL,
    geaendert   TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS quellen (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id  INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    url       TEXT    NOT NULL,
    behauptung TEXT   NOT NULL,
    stufe     TEXT    NOT NULL DEFAULT 'ungeprueft',
    notiz     TEXT    NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS verlauf (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id  INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    von       TEXT    NOT NULL,
    nach      TEXT    NOT NULL,
    wann      TEXT    NOT NULL,
    notiz     TEXT    NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS kosten (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id  INTEGER NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    posten    TEXT    NOT NULL,
    betrag_usd REAL   NOT NULL,
    wann      TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
"""

# Belegstufen fuer Quellen -- dieselbe Unterscheidung wie in den
# Berichten dieses Projekts. 'unbelegt' darf nicht in ein Skript.
STUFEN = ("belegt", "geschaetzt", "unbelegt", "ungeprueft")


def jetzt() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def oeffnen(pfad: Path = DB_STANDARD) -> sqlite3.Connection:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(pfad)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA)
    return db


def anlegen(db: sqlite3.Connection, schluessel: str, titel: str,
            nische: str = "nachgemessen") -> int:
    t = jetzt()
    cur = db.execute(
        "INSERT INTO videos (schluessel, titel, nische, status, angelegt,"
        " geaendert) VALUES (?, ?, ?, 'thema', ?, ?)",
        (schluessel, titel, nische, t, t))
    db.execute("INSERT INTO verlauf (video_id, von, nach, wann, notiz)"
               " VALUES (?, '', 'thema', ?, 'angelegt')", (cur.lastrowid, t))
    db.commit()
    return cur.lastrowid


def erlaubt(von: str, nach: str) -> bool:
    """Nur ein Schritt vorwaerts -- oder scheitern."""
    if nach == GESCHEITERT:
        return von != GESCHEITERT
    if von == GESCHEITERT or von not in KETTE or nach not in KETTE:
        return False
    return KETTE.index(nach) == KETTE.index(von) + 1


def weiter(db: sqlite3.Connection, schluessel: str, nach: str,
           notiz: str = "") -> str:
    zeile = db.execute("SELECT id, status FROM videos WHERE schluessel = ?",
                       (schluessel,)).fetchone()
    if zeile is None:
        raise KeyError(f"Kein Video mit Schlüssel {schluessel!r}")
    von = zeile["status"]
    if not erlaubt(von, nach):
        raise ValueError(
            f"Übergang {von!r} -> {nach!r} ist nicht erlaubt. "
            f"Erlaubt wäre: "
            f"{KETTE[KETTE.index(von) + 1] if von in KETTE and KETTE.index(von) + 1 < len(KETTE) else '— (Ende)'}"
            f" oder {GESCHEITERT!r}.")
    if nach == GESCHEITERT and not notiz.strip():
        raise ValueError("Ein Fehlschlag braucht einen Grund (--notiz).")
    t = jetzt()
    db.execute("UPDATE videos SET status = ?, geaendert = ? WHERE id = ?",
               (nach, t, zeile["id"]))
    db.execute("INSERT INTO verlauf (video_id, von, nach, wann, notiz)"
               " VALUES (?, ?, ?, ?, ?)", (zeile["id"], von, nach, t, notiz))
    db.commit()
    return f"{schluessel}: {von} → {nach}"


def quelle_zu(db: sqlite3.Connection, schluessel: str, url: str,
              behauptung: str, stufe: str = "ungeprueft",
              notiz: str = "") -> None:
    if stufe not in STUFEN:
        raise ValueError(f"Unbekannte Belegstufe {stufe!r}. Möglich: {STUFEN}")
    zeile = db.execute("SELECT id FROM videos WHERE schluessel = ?",
                       (schluessel,)).fetchone()
    if zeile is None:
        raise KeyError(f"Kein Video mit Schlüssel {schluessel!r}")
    db.execute("INSERT INTO quellen (video_id, url, behauptung, stufe, notiz)"
               " VALUES (?, ?, ?, ?, ?)",
               (zeile["id"], url, behauptung, stufe, notiz))
    db.commit()


def unbelegte(db: sqlite3.Connection, schluessel: str) -> list[sqlite3.Row]:
    """Behauptungen, die ein Skript blockieren müssen."""
    return db.execute(
        "SELECT q.behauptung, q.stufe FROM quellen q JOIN videos v"
        " ON v.id = q.video_id WHERE v.schluessel = ?"
        " AND q.stufe IN ('unbelegt', 'ungeprueft')", (schluessel,)).fetchall()


def kosten_zu(db: sqlite3.Connection, schluessel: str, posten: str,
              betrag_usd: float) -> None:
    zeile = db.execute("SELECT id FROM videos WHERE schluessel = ?",
                       (schluessel,)).fetchone()
    if zeile is None:
        raise KeyError(f"Kein Video mit Schlüssel {schluessel!r}")
    db.execute("INSERT INTO kosten (video_id, posten, betrag_usd, wann)"
               " VALUES (?, ?, ?, ?)",
               (zeile["id"], posten, betrag_usd, jetzt()))
    db.commit()


def uebersicht(db: sqlite3.Connection) -> str:
    zeilen = db.execute(
        "SELECT v.schluessel, v.status, v.titel,"
        " (SELECT ROUND(SUM(betrag_usd), 4) FROM kosten k"
        "  WHERE k.video_id = v.id) AS usd"
        " FROM videos v ORDER BY v.geaendert DESC").fetchall()
    if not zeilen:
        return "Noch keine Videos erfasst."
    breite = max(len(z["schluessel"]) for z in zeilen)
    aus = [f"{'Schlüssel'.ljust(breite)}  {'Status'.ljust(15)} Kosten  Titel"]
    for z in zeilen:
        usd = f"{z['usd']:.2f}$" if z["usd"] else "  —  "
        aus.append(f"{z['schluessel'].ljust(breite)}  "
                   f"{z['status'].ljust(15)} {usd:>6}  {z['titel'][:50]}")
    return "\n".join(aus)


# ----------------------------------------------------------- Selbsttest

def selbsttest() -> int:
    """Prueft die Kette in BEIDE Richtungen.

    Ein Test, der nur zeigt, dass der erlaubte Weg funktioniert, ist
    kein Test der Schranke. Die Schranke ist der Zweck dieser Datei:
    Sie soll verhindern, dass ein ungeprueftes Video hochgeladen wird.
    """
    import tempfile
    fehler: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        db = oeffnen(Path(tmp) / "t.sqlite")
        anlegen(db, "probe-1", "Testvideo")

        # Der erlaubte Weg muss ganz durchlaufen.
        for i in range(1, len(KETTE)):
            try:
                weiter(db, "probe-1", KETTE[i], "selbsttest")
            except Exception as e:                      # noqa: BLE001
                fehler.append(f"Erlaubter Schritt → {KETTE[i]} scheitert: {e}")
                break
        else:
            z = db.execute("SELECT status FROM videos WHERE schluessel='probe-1'"
                           ).fetchone()
            if z["status"] != KETTE[-1]:
                fehler.append(f"Endstatus ist {z['status']}, erwartet {KETTE[-1]}")

        # Und jetzt die Gegenprobe: Jedes Ueberspringen muss scheitern.
        # Ohne diesen Block waere die Schranke nicht geprueft, sondern
        # nur der Glueckspfad.
        anlegen(db, "probe-2", "Testvideo 2")
        verbotene = [
            ("thema", "gerendert", "Rendern ohne Skript"),
            ("thema", "veroeffentlicht", "Direkt veröffentlichen"),
            ("thema", "entwurf", "Upload ohne Tonprüfung"),
            ("thema", "thema", "Stillstand"),
        ]
        for _, nach, was in verbotene:
            try:
                weiter(db, "probe-2", nach, "darf nicht gehen")
                fehler.append(f"Verbotener Schritt wurde erlaubt: {was}")
            except ValueError:
                pass

        # Rueckwaerts muss ebenfalls scheitern.
        weiter(db, "probe-2", "bewertet", "ok")
        try:
            weiter(db, "probe-2", "thema", "zurück")
            fehler.append("Rückwärts wurde erlaubt")
        except ValueError:
            pass

        # Scheitern braucht einen Grund.
        try:
            weiter(db, "probe-2", GESCHEITERT, "")
            fehler.append("Fehlschlag ohne Grund wurde angenommen")
        except ValueError:
            pass
        weiter(db, "probe-2", GESCHEITERT, "Faktenprüfung nicht bestanden")

        # Aus 'gescheitert' fuehrt kein Weg zurueck in die Kette.
        try:
            weiter(db, "probe-2", "skript", "wiederbeleben")
            fehler.append("Aus 'gescheitert' wurde weitergegangen")
        except ValueError:
            pass

        # Quellen: unbelegte Behauptungen muessen auffindbar sein.
        quelle_zu(db, "probe-1", "https://example.org/a", "Zahl A", "belegt")
        quelle_zu(db, "probe-1", "", "Zahl B", "unbelegt", "kein Nachweis")
        offen = unbelegte(db, "probe-1")
        if len(offen) != 1 or offen[0]["behauptung"] != "Zahl B":
            fehler.append(f"Unbelegte Behauptungen falsch erkannt: {offen}")
        try:
            quelle_zu(db, "probe-1", "u", "x", "sehr sicher")
            fehler.append("Unbekannte Belegstufe wurde angenommen")
        except ValueError:
            pass

        # Positivprobe: Ein belegter Eintrag darf NICHT als offen gelten.
        # Ein Melder, der alles meldet, ist so nutzlos wie keiner.
        quelle_zu(db, "probe-1", "https://example.org/c", "Zahl C", "belegt")
        if any(o["behauptung"] == "Zahl C" for o in unbelegte(db, "probe-1")):
            fehler.append("Belegte Behauptung fälschlich als offen gemeldet")

        kosten_zu(db, "probe-1", "skript", 0.03)
        kosten_zu(db, "probe-1", "bilder", 0.30)
        if "0.33$" not in uebersicht(db):
            fehler.append(f"Kostensumme falsch:\n{uebersicht(db)}")

        db.close()

    if fehler:
        print("Selbsttest:")
        for f in fehler:
            print(f"  FEHLER: {f}")
        return 1
    print("Selbsttest: bestanden (Kette vorwärts; Überspringen, Rückwärts, "
          "Wiederbelebung und Fehlschlag-ohne-Grund werden abgelehnt; "
          "unbelegte Quellen erkannt, belegte nicht fälschlich gemeldet; "
          "Kostensumme stimmt).")
    print("  NICHT geprüft: ob ein Video wirklich hochgeladen wird — dafür "
          "fehlt hier das Netz.")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--db", type=Path, default=DB_STANDARD)
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--anlegen", nargs=2, metavar=("SCHLÜSSEL", "TITEL"))
    p.add_argument("--weiter", nargs=2, metavar=("SCHLÜSSEL", "STATUS"))
    p.add_argument("--quelle", nargs=3,
                   metavar=("SCHLÜSSEL", "URL", "BEHAUPTUNG"))
    p.add_argument("--stufe", default="ungeprueft", choices=STUFEN)
    p.add_argument("--kosten", nargs=3, metavar=("SCHLÜSSEL", "POSTEN", "USD"))
    p.add_argument("--notiz", default="")
    p.add_argument("--offen", metavar="SCHLÜSSEL",
                   help="Unbelegte Behauptungen eines Videos zeigen")
    p.add_argument("--liste", action="store_true")
    a = p.parse_args()

    if a.selbsttest:
        raise SystemExit(selbsttest())

    try:
        ausfuehren(a)
    except (ValueError, KeyError) as e:
        # Eine abgelehnte Statusaenderung ist der Normalfall dieses
        # Werkzeugs, kein Absturz. Ein Stacktrace an dieser Stelle
        # sieht aus wie ein Defekt und verdeckt die eigentliche
        # Meldung -- beim ersten Testlauf am 28.10.2026 genau so
        # passiert.
        raise SystemExit(f"Abgelehnt: {e.args[0] if e.args else e}")


def ausfuehren(a: argparse.Namespace) -> None:
    db = oeffnen(a.db)
    if a.anlegen:
        anlegen(db, *a.anlegen)
        print(f"angelegt: {a.anlegen[0]}")
    if a.weiter:
        print(weiter(db, a.weiter[0], a.weiter[1], a.notiz))
    if a.quelle:
        quelle_zu(db, a.quelle[0], a.quelle[1], a.quelle[2], a.stufe, a.notiz)
        print(f"Quelle zu {a.quelle[0]} ({a.stufe})")
    if a.kosten:
        kosten_zu(db, a.kosten[0], a.kosten[1], float(a.kosten[2]))
        print(f"Kosten zu {a.kosten[0]}: {a.kosten[2]} $")
    if a.offen:
        offen = unbelegte(db, a.offen)
        print(json.dumps([dict(o) for o in offen], ensure_ascii=False,
                         indent=1) if offen
              else "Keine unbelegten Behauptungen.")
    if a.liste or not any((a.anlegen, a.weiter, a.quelle, a.kosten, a.offen)):
        print(uebersicht(db))
    db.close()


if __name__ == "__main__":
    main()
