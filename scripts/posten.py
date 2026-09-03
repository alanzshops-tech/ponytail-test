#!/usr/bin/env python3
"""posten.py — veröffentlicht auf den Kanälen, die keine Genehmigung brauchen.

Vier Kanäle lassen sich mit einem einzigen Zugangstoken bespielen, ohne
App-Review, ohne Kosten, ohne Beitragslimit:

  * **Mastodon**  — Token in den Kontoeinstellungen erzeugen
  * **Bluesky**   — App-Passwort in den Einstellungen erzeugen
  * **Telegram**  — Bot-Token vom BotFather, Kanal-ID
  * **Discord**   — Webhook-URL, ein Klick im Kanalmenü

Die Belege dafür stehen in `../SOCIAL-SELBSTHOSTEN.md`. Instagram,
Facebook, Threads, YouTube und TikTok sind ebenfalls kostenlos, brauchen
aber je eine eigene App und OAuth — die kommen in einem zweiten Schritt.

**Warum das hier und nicht in der Arbeitsumgebung laeuft:** Die erreicht
nur GitHub, PyPI und npm. mastodon.social, bsky.social, api.telegram.org
und discord.com sind gesperrt. Der Runner ist Augen und Netz, das
Ergebnis kommt als Commit zurueck — dasselbe Muster wie bei
`openrouter.py` und `trends.py`.

**Zugangsdaten** kommen ausschliesslich aus Umgebungsvariablen, die der
Workflow aus den Repository-Secrets fuellt. Sie stehen in keinem Befehl
und damit in keinem Protokoll (`CLAUDE.md`, Regel 4).

Aufruf:
    python3 scripts/posten.py --selbsttest
    python3 scripts/posten.py --text "..." --probe      # nichts senden
    python3 scripts/posten.py --text "..." --kanaele mastodon,telegram
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# Zeichengrenzen der Kanaele. Ueberschreiten heisst nicht "wird
# gekuerzt", sondern "der Aufruf schlaegt fehl" -- deshalb wird vorher
# geprueft und nicht hinterher repariert.
GRENZE = {
    "mastodon": 500,
    "bluesky": 300,
    "telegram": 4096,
    "discord": 2000,
}


def hole(name: str) -> str | None:
    wert = os.environ.get(name, "").strip()
    return wert or None


def anfrage(url: str, daten=None, kopf=None, methode="POST") -> dict:
    """Ein HTTP-Aufruf. Gibt die Antwort als dict zurueck.

    Fehler werden nicht verschluckt: Wer eine 401 bekommt, soll das
    sehen und nicht ein stilles "0 gesendet".
    """
    koerper = None
    kopf = dict(kopf or {})
    if daten is not None:
        koerper = json.dumps(daten).encode("utf-8")
        kopf.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=koerper, headers=kopf,
                                 method=methode)
    try:
        with urllib.request.urlopen(req, timeout=30) as a:
            roh = a.read().decode("utf-8") or "{}"
            return json.loads(roh) if roh.strip().startswith(("{", "[")) \
                else {"ok": True, "roh": roh[:200]}
    except urllib.error.HTTPError as e:
        text = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"HTTP {e.code}: {text}") from None


# ------------------------------------------------------------- Kanaele

def mastodon(text: str, probe: bool) -> str:
    server = hole("MASTODON_SERVER") or "https://mastodon.social"
    token = hole("MASTODON_TOKEN")
    if not token:
        return "übersprungen (MASTODON_TOKEN fehlt)"
    if probe:
        return f"Probe: {server}/api/v1/statuses, {len(text)} Zeichen"
    a = anfrage(f"{server.rstrip('/')}/api/v1/statuses",
                {"status": text},
                {"Authorization": f"Bearer {token}"})
    return f"gesendet: {a.get('url') or a.get('id')}"


def bluesky(text: str, probe: bool) -> str:
    kennung = hole("BLUESKY_HANDLE")
    passwort = hole("BLUESKY_APP_PASSWORD")
    if not (kennung and passwort):
        return "übersprungen (BLUESKY_HANDLE/APP_PASSWORD fehlt)"
    if probe:
        return f"Probe: bsky.social als {kennung}, {len(text)} Zeichen"
    # Zwei Schritte: Sitzung eroeffnen, dann Datensatz anlegen.
    s = anfrage("https://bsky.social/xrpc/com.atproto.server.createSession",
                {"identifier": kennung, "password": passwort})
    from datetime import datetime, timezone
    jetzt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    a = anfrage("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                {"repo": s["did"], "collection": "app.bsky.feed.post",
                 "record": {"$type": "app.bsky.feed.post", "text": text,
                            "createdAt": jetzt}},
                {"Authorization": f"Bearer {s['accessJwt']}"})
    return f"gesendet: {a.get('uri')}"


def telegram(text: str, probe: bool) -> str:
    token = hole("TELEGRAM_BOT_TOKEN")
    chat = hole("TELEGRAM_CHAT_ID")
    if not (token and chat):
        return "übersprungen (TELEGRAM_BOT_TOKEN/CHAT_ID fehlt)"
    if probe:
        return f"Probe: Telegram an {chat}, {len(text)} Zeichen"
    a = anfrage(f"https://api.telegram.org/bot{token}/sendMessage",
                {"chat_id": chat, "text": text,
                 "disable_web_page_preview": False})
    return f"gesendet: Nachricht {a.get('result', {}).get('message_id')}"


def discord(text: str, probe: bool) -> str:
    haken = hole("DISCORD_WEBHOOK")
    if not haken:
        return "übersprungen (DISCORD_WEBHOOK fehlt)"
    if probe:
        return f"Probe: Discord-Webhook, {len(text)} Zeichen"
    anfrage(haken, {"content": text})
    return "gesendet"


KANAELE = {"mastodon": mastodon, "bluesky": bluesky,
           "telegram": telegram, "discord": discord}


# ---------------------------------------------------------- Pruefungen

def zu_lang(text: str, kanal: str) -> bool:
    return len(text) > GRENZE[kanal]


def selbsttest() -> None:
    """Was hier prueft, ist der Aufbau -- nicht die Zustellung.

    Ein echter Sendevorgang laesst sich hier nicht pruefen: Die
    Arbeitsumgebung erreicht keinen der vier Dienste. Der Selbsttest
    deckt deshalb genau das ab, was ohne Netz pruefbar ist, und
    behauptet nichts darueber hinaus. Ob wirklich ein Beitrag
    erscheint, zeigt erst der erste Lauf im Workflow mit --probe aus.
    """
    fehler = []

    # Laengenpruefung, Positiv- und Negativfall je Kanal.
    for kanal, grenze in GRENZE.items():
        if zu_lang("x" * (grenze - 1), kanal):
            fehler.append(f"{kanal}: knapp unter der Grenze faelschlich "
                          f"als zu lang gemeldet")
        if not zu_lang("x" * (grenze + 1), kanal):
            fehler.append(f"{kanal}: ein Zeichen zu viel nicht erkannt")

    # Ohne Zugangsdaten muss jeder Kanal sauber ueberspringen statt zu
    # stuerzen -- sonst reisst ein fehlendes Secret den ganzen Lauf ab.
    sicherung = {k: os.environ.pop(k, None) for k in
                 ("MASTODON_TOKEN", "BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD",
                  "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "DISCORD_WEBHOOK")}
    try:
        for name, fn in KANAELE.items():
            antwort = fn("Test", probe=True)
            if "übersprungen" not in antwort:
                fehler.append(f"{name}: ohne Zugangsdaten nicht übersprungen "
                              f"({antwort})")
    finally:
        for k, v in sicherung.items():
            if v is not None:
                os.environ[k] = v

    # Die Probe darf unter keinen Umstaenden senden. Ein Kanal mit
    # Zugangsdaten muss im Probelauf trotzdem nur beschreiben.
    os.environ["DISCORD_WEBHOOK"] = "https://example.invalid/haken"
    try:
        if not discord("Test", probe=True).startswith("Probe:"):
            fehler.append("Probe sendet, statt nur zu beschreiben")
    finally:
        os.environ.pop("DISCORD_WEBHOOK", None)

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  bestanden (Längengrenzen je Kanal positiv und negativ, "
          "Überspringen ohne Zugangsdaten, Probe sendet nicht).")
    print("  NICHT geprüft: ob ein Beitrag wirklich erscheint — dafür "
          "fehlt hier das Netz.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--text", default="")
    p.add_argument("--kanaele", default="mastodon,bluesky,telegram,discord")
    p.add_argument("--probe", action="store_true",
                   help="nichts senden, nur zeigen was passieren würde")
    p.add_argument("--selbsttest", action="store_true")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return
    if not a.text.strip():
        print("\nKein Text. Nichts zu tun.")
        return

    gewaehlt = [k.strip() for k in a.kanaele.split(",") if k.strip()]
    unbekannt = [k for k in gewaehlt if k not in KANAELE]
    if unbekannt:
        raise SystemExit(f"Unbekannte Kanäle: {unbekannt}. "
                         f"Möglich: {sorted(KANAELE)}")

    print(f"\nText: {len(a.text)} Zeichen"
          f"{'  (PROBELAUF, es wird nichts gesendet)' if a.probe else ''}\n")
    fehlgeschlagen = 0
    for k in gewaehlt:
        if zu_lang(a.text, k):
            print(f"  {k:9s} ÜBERSPRUNGEN — {len(a.text)} Zeichen, "
                  f"Grenze {GRENZE[k]}")
            continue
        try:
            print(f"  {k:9s} {KANAELE[k](a.text, a.probe)}")
        except Exception as e:                          # noqa: BLE001
            fehlgeschlagen += 1
            print(f"  {k:9s} FEHLER: {e}")

    if fehlgeschlagen:
        raise SystemExit(f"\n{fehlgeschlagen} Kanal/Kanäle fehlgeschlagen.")


if __name__ == "__main__":
    main()
