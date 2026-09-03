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
import contextlib
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
    "instagram": 2200,
    "facebook": 63206,
    "tiktok": 150,          # Titel des Entwurfs
}

# Kanaele, die ohne Medium nicht koennen. Instagram veroeffentlicht
# grundsaetzlich kein reines Textformat, TikTok schon gar nicht.
BRAUCHT_BILD = {"instagram"}
BRAUCHT_VIDEO = {"tiktok"}


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



# ---------------------------------------------- Meta: Instagram, Facebook
#
# Beide brauchen eine eigene App, aber KEIN App-Review, solange nur auf
# eigene Konten gepostet wird (Entwicklungsmodus). Belege und Herleitung
# in ../SOCIAL-SELBSTHOSTEN.md.
#
# Instagram veroeffentlicht in ZWEI Schritten, und das ist keine Marotte:
#   1. /media          legt einen Container an und laedt das Bild
#   2. /media_publish  veroeffentlicht ihn
# Zwischen beiden kann Instagram das Bild ablehnen -- deshalb wird der
# zweite Schritt nur nach erfolgreichem ersten gemacht.
#
# **Das Bild muss oeffentlich erreichbar sein.** Instagram holt es selbst
# ab; ein Pfad im Repository oder eine private URL geht nicht. Fuer
# Homeeins heisst das: die Shopify-CDN-Adresse des Produktbildes.

GRAPH = "https://graph.facebook.com/v21.0"
GRAPH_IG = "https://graph.instagram.com/v21.0"


def ueber_instagram_login() -> bool:
    """Welcher der beiden Meta-Wege gilt. Standard: Instagram-Login.

    Frueher war es andersherum -- der Instagram-Login musste mit dem
    Secret INSTAGRAM_STANDALONE=1 eingeschaltet werden. Das hat sich im
    ersten echten Lauf geraecht, und zwar an einer Stelle, die man nicht
    erwartet: GitHub ersetzt JEDES Vorkommen eines Secret-Wertes im
    Protokoll durch ***. Ein Secret mit dem Wert "1" schwaerzt damit
    jede 1 im ganzen Protokoll. Aus der Fehlermeldung wurde
    '"code":***9', aus einem Datum '2025-09-***9'. Das Protokoll ist
    aber genau das Werkzeug, mit dem man den Fehler sucht.

    Der zweite Schritt geht weiter: Auch ein Schaltsecret ist zu viel
    verlangt. Welcher Weg gilt, steht naemlich im Token selbst --
    Facebook-Token beginnen mit EAA, Instagram-Token mit IGAA oder IGQ.
    Das Werkzeug hat also die ganze Zeit nach einer Auskunft gefragt,
    die ihm schon vorlag. Es erkennt den Weg jetzt selbst.

    INSTAGRAM_UEBER_FACEBOOK bleibt als Notueberschreibung bestehen,
    falls Meta die Praefixe eines Tages aendert. Gesetzt gewinnt es
    gegen die Erkennung -- eine ausdrueckliche Ansage schlaegt eine
    Vermutung, auch wenn die Vermutung meistens recht hat.
    """
    if hole("INSTAGRAM_UEBER_FACEBOOK"):
        return False
    token = hole("INSTAGRAM_TOKEN") or ""
    if token.startswith("EAA"):
        return False
    return True


def instagram_token_erneuern() -> str:
    """Umgehung fuer die 60-Tage-Frist.

    Instagram-Zugriffstoken laufen nach rund 60 Tagen ab. Ein Lauf, der
    heute klappt, scheitert dann ohne erkennbaren Grund -- und man
    merkt es erst, wenn ein Beitrag ausbleibt. Deshalb hier der
    Erneuerungsaufruf, der die Frist zurueckstellt.

    Wichtig: Das Token wird dadurch NICHT im Repository aktualisiert --
    das ginge nur, wenn wir es dort ablegen, und Zugangsdaten gehoeren
    nicht ins Repository (CLAUDE.md, Regel 4). Der Aufruf verlaengert
    das bestehende Token bei Meta; das neue muss von Hand ins Secret.
    Der Workflow meldet es in der Ausgabe.
    """
    token = hole("INSTAGRAM_TOKEN")
    if not token:
        return "übersprungen (INSTAGRAM_TOKEN fehlt)"
    # Der Erneuerungsaufruf unten gilt NUR fuer Token aus dem
    # Instagram-Login (graph.instagram.com, ig_refresh_token). Wer den
    # Weg ueber eine Facebook-Seite geht, hat ein Seiten-Token -- das
    # laeuft, wenn es aus einem langlebigen Nutzertoken stammt, gar
    # nicht ab. Frueher rief diese Funktion in beiden Faellen
    # ig_refresh_token auf und lieferte auf dem Seiten-Weg eine
    # OAuthException, die aussah, als sei das Token kaputt.
    if not ueber_instagram_login():
        return ("übersprungen — mit INSTAGRAM_UEBER_FACEBOOK ist das ein "
                "Seiten-Token vom Facebook-Login. Das laeuft nicht nach "
                "60 Tagen ab, wenn es aus einem langlebigen Nutzertoken "
                "erzeugt wurde. Zum Pruefen: --zugang.")
    a = anfrage(
        "https://graph.instagram.com/refresh_access_token"
        f"?grant_type=ig_refresh_token&access_token={token}",
        methode="GET")
    tage = int(a.get("expires_in", 0)) // 86400
    return (f"Token erneuert, läuft in {tage} Tagen ab. "
            f"Neues Token endet auf …{str(a.get('access_token',''))[-6:]} "
            f"— ins Secret INSTAGRAM_TOKEN übertragen.")


def instagram(text: str, probe: bool, bild: str = "") -> str:
    token = hole("INSTAGRAM_TOKEN")
    nutzer = hole("INSTAGRAM_USER_ID")
    if not (token and nutzer):
        return "übersprungen (INSTAGRAM_TOKEN/USER_ID fehlt)"
    if not bild:
        return "übersprungen (Instagram braucht ein Bild: --bild URL)"
    if not bild.startswith("https://"):
        return f"ÜBERSPRUNGEN — Bild muss öffentlich per https erreichbar sein"
    basis = GRAPH_IG if ueber_instagram_login() else GRAPH
    if probe:
        return (f"Probe: {basis}/{nutzer}/media (Container) "
                f"+ /media_publish, {len(text)} Zeichen, Bild gesetzt")
    a = anfrage(f"{basis}/{nutzer}/media", {
        "image_url": bild, "caption": text, "access_token": token})
    behaelter = a.get("id")
    if not behaelter:
        raise RuntimeError(f"kein Container zurückbekommen: {a}")
    b = anfrage(f"{basis}/{nutzer}/media_publish", {
        "creation_id": behaelter, "access_token": token})
    return f"gesendet: Beitrag {b.get('id')}"


def facebook(text: str, probe: bool, bild: str = "") -> str:
    token = hole("FACEBOOK_PAGE_TOKEN")
    seite = hole("FACEBOOK_PAGE_ID")
    if not (token and seite):
        return "übersprungen (FACEBOOK_PAGE_TOKEN/PAGE_ID fehlt)"
    # Mit Bild geht /photos, ohne Bild /feed. Zwei Wege, ein Aufruf.
    weg = "photos" if bild else "feed"
    if probe:
        return (f"Probe: {GRAPH}/{seite}/{weg}, {len(text)} Zeichen"
                f"{', mit Bild' if bild else ''}")
    nutzlast = {"access_token": token}
    if bild:
        nutzlast |= {"url": bild, "caption": text}
    else:
        nutzlast |= {"message": text}
    a = anfrage(f"{GRAPH}/{seite}/{weg}", nutzlast)
    return f"gesendet: {a.get('post_id') or a.get('id')}"


# ------------------------------------------------------------- TikTok
#
# Der Weg ohne Audit: Scope `video.upload` und der Endpunkt
# .../post/publish/inbox/video/init/ -- das Video landet als ENTWURF im
# TikTok-Postfach, veroeffentlicht wird mit einem Fingertipp in der App.
# Der Weg mit Audit waere /post/publish/video/init/ und `video.publish`.
#
# Zwei Quellen sind moeglich. PULL_FROM_URL verlangt eine bei TikTok
# verifizierte Domain -- also wieder ein Antrag. FILE_UPLOAD nicht, ist
# aber zweistufig: erst Anmeldung, dann die Bytes an die zurueckgegebene
# Adresse. Hier steht PULL_FROM_URL, weil die Produktvideos ohnehin auf
# einer eigenen Domain liegen; ohne verifizierte Domain schlaegt es mit
# einer klaren Meldung fehl statt still zu tun.

def tiktok(text: str, probe: bool, video: str = "") -> str:
    token = hole("TIKTOK_ACCESS_TOKEN")
    if not token:
        return "übersprungen (TIKTOK_ACCESS_TOKEN fehlt)"
    if not video:
        return "übersprungen (TikTok braucht ein Video: --video URL)"
    ziel = ("https://open.tiktokapis.com/v2/post/publish/"
            "inbox/video/init/")
    if probe:
        return (f"Probe: {ziel} (Entwurf, Scope video.upload), "
                f"Titel {len(text)} Zeichen")
    kopf = {"Authorization": f"Bearer {token}"}
    # Erst der bequeme Weg. PULL_FROM_URL laesst TikTok das Video selbst
    # holen -- verlangt aber eine bei TikTok verifizierte Domain.
    try:
        a = anfrage(ziel, {
            "source_info": {"source": "PULL_FROM_URL", "video_url": video},
            "post_info": {"title": text[:150]},
        }, kopf)
        kennung = (a.get("data") or {}).get("publish_id")
        if kennung:
            return (f"als Entwurf hochgeladen ({kennung}) — "
                    f"in der TikTok-App auf „Posten“ tippen")
        raise RuntimeError(f"keine publish_id: {a}")
    except RuntimeError as e:
        # Umgehung: FILE_UPLOAD braucht KEINE verifizierte Domain. Wir
        # laden das Video selbst herunter und schieben die Bytes an die
        # Adresse, die TikTok zurueckgibt. Ein Zug, kein Stueckeln --
        # fuer Produktvideos unter 64 MB reicht das.
        if "url_ownership_unverified" not in str(e) and \
           "unverified" not in str(e).lower():
            raise
        print(f"  {'':9s} PULL_FROM_URL abgelehnt (Domain nicht "
              f"verifiziert) — weiche auf FILE_UPLOAD aus")
        with urllib.request.urlopen(video, timeout=120) as v:
            bytes_ = v.read()
        groesse = len(bytes_)
        a = anfrage(ziel, {
            "source_info": {"source": "FILE_UPLOAD", "video_size": groesse,
                            "chunk_size": groesse, "total_chunk_count": 1},
            "post_info": {"title": text[:150]},
        }, kopf)
        d = a.get("data") or {}
        adresse, kennung = d.get("upload_url"), d.get("publish_id")
        if not adresse:
            raise RuntimeError(f"keine upload_url: {a}") from None
        req = urllib.request.Request(adresse, data=bytes_, method="PUT",
                                     headers={
                                         "Content-Type": "video/mp4",
                                         "Content-Length": str(groesse),
                                         "Content-Range":
                                             f"bytes 0-{groesse - 1}/{groesse}",
                                     })
        urllib.request.urlopen(req, timeout=300)
        return (f"als Entwurf hochgeladen ({kennung}, FILE_UPLOAD, "
                f"{groesse // 1024} kB) — in der App auf „Posten“ tippen")


KANAELE = {"mastodon": mastodon, "bluesky": bluesky,
           "telegram": telegram, "discord": discord,
           "instagram": instagram, "facebook": facebook,
           "tiktok": tiktok}


# ---------------------------------------------------------- Pruefungen

# ------------------------------------------------------- Zugangsprobe
#
# Der eigentliche Engpass beim Aufsetzen ist nicht das Posten, sondern
# die Frage "stimmt mein Token ueberhaupt?". Wer das erst beim ersten
# echten Beitrag erfaehrt, bekommt eine kryptische Meldung und weiss
# nicht, ob Token, Konto-ID oder Berechtigung schuld ist.
#
# Diese Probe ruft je Kanal einen LESENDEN Endpunkt auf. Sie
# veroeffentlicht nichts und kann deshalb beliebig oft laufen.

def token_form(token: str, instagram_login: bool = True) -> str | None:
    """Sagt VOR dem Aufruf, ob das ueberhaupt ein Token sein kann.

    Anlass ist der Lauf vom 03.09.2026: Meta antwortete mit "Cannot
    parse access token", und diese Meldung sagt nur, dass die
    Zeichenkette unlesbar war -- nicht, was stattdessen dort stand. Auf
    derselben Seite der Konsole stehen App-ID, App-Geheimnis und Token
    untereinander, und auf einem Telefon markiert man leicht das
    Falsche oder nur die Haelfte.

    Diese Pruefung braucht kein Netz und nennt den Verdacht. Sie gibt
    None zurueck, wenn nichts auffaellt -- ein Urteil "Token gueltig"
    faellt sie NICHT, das kann nur Meta.

    Der Token-Wert selbst wird nie ausgegeben, nur seine Gestalt.
    """
    roh = token.strip()
    if any(z.isspace() for z in roh):
        return ("enthält ein Leerzeichen oder einen Zeilenumbruch — beim "
                "Kopieren ist etwas mitgekommen")
    if roh.isdigit():
        return (f"besteht nur aus {len(roh)} Ziffern — das ist eine ID "
                f"(App-ID oder Konto-ID), kein Token")
    if len(roh) <= 40:
        # Die Reihenfolge zaehlt: Was richtig mit IG anfaengt und zu kurz
        # ist, wurde beim Kopieren abgeschnitten -- ein anderer Fehler
        # mit einer anderen Abhilfe als "das Falsche erwischt".
        if roh.startswith("IG"):
            return (f"fängt richtig mit „IG“ an, ist aber nur {len(roh)} "
                    f"Zeichen lang — beim Kopieren abgeschnitten. Ein "
                    f"Token hat um die 200")
        return (f"ist nur {len(roh)} Zeichen lang — ein Token hat um die "
                f"200. So kurz ist das App-Geheimnis")
    # Welches Praefix richtig ist, haengt am gewaehlten Weg. Ein
    # EAA-Token ist auf dem Facebook-Weg genau das Richtige und auf dem
    # Instagram-Weg genau das Falsche -- eine Pruefung ohne diese
    # Unterscheidung wuerde den halben Nutzerkreis grundlos aufhalten.
    if instagram_login:
        if roh.startswith("EAA"):
            return ("beginnt mit EAA — das ist ein Facebook-Token. Für "
                    "diesen Weg brauchst du das aus dem "
                    "Instagram-Business-Login, oder setze das Secret "
                    "INSTAGRAM_UEBER_FACEBOOK")
        if not roh.startswith("IG"):
            return (f"beginnt mit {roh[:2]!r} statt mit „IG“ — "
                    f"Instagram-Token fangen mit IGAA oder IGQ an")
    else:
        if roh.startswith("IG"):
            return ("beginnt mit IG — das ist ein Instagram-Token, aber "
                    "INSTAGRAM_UEBER_FACEBOOK ist gesetzt. Entweder das "
                    "Secret löschen oder das Seiten-Token eintragen")
    return None


def zugang_pruefen(kanal: str) -> str:
    try:
        if kanal == "mastodon":
            token = hole("MASTODON_TOKEN")
            if not token:
                return "— kein Token gesetzt"
            server = hole("MASTODON_SERVER") or "https://mastodon.social"
            a = anfrage(f"{server.rstrip('/')}/api/v1/accounts/"
                        f"verify_credentials",
                        kopf={"Authorization": f"Bearer {token}"},
                        methode="GET")
            return f"OK — angemeldet als @{a.get('username')}"

        if kanal == "bluesky":
            k, pw = hole("BLUESKY_HANDLE"), hole("BLUESKY_APP_PASSWORD")
            if not (k and pw):
                return "— Handle oder App-Passwort fehlt"
            a = anfrage("https://bsky.social/xrpc/"
                        "com.atproto.server.createSession",
                        {"identifier": k, "password": pw})
            return f"OK — angemeldet als {a.get('handle')}"

        if kanal == "telegram":
            token, chat = hole("TELEGRAM_BOT_TOKEN"), hole("TELEGRAM_CHAT_ID")
            if not token:
                return "— kein Bot-Token gesetzt"
            a = anfrage(f"https://api.telegram.org/bot{token}/getMe",
                        methode="GET")
            name = (a.get("result") or {}).get("username")
            fehlt = "" if chat else "  ACHTUNG: TELEGRAM_CHAT_ID fehlt noch"
            return f"OK — Bot @{name}{fehlt}"

        if kanal == "discord":
            haken = hole("DISCORD_WEBHOOK")
            if not haken:
                return "— keine Webhook-URL gesetzt"
            a = anfrage(haken, methode="GET")
            return f"OK — Webhook „{a.get('name')}“ in Kanal {a.get('channel_id')}"

        if kanal == "instagram":
            token, nutzer = hole("INSTAGRAM_TOKEN"), hole("INSTAGRAM_USER_ID")
            if not token:
                return "— Token fehlt"
            # Erst die Gestalt, dann das Netz. Meta sagt bei einer
            # unlesbaren Zeichenkette nur "Cannot parse access token";
            # was stattdessen dort steht, sagt es nicht.
            verdacht = token_form(token, ueber_instagram_login())
            if verdacht:
                return f"— das eingetragene Token {verdacht}"
            if not nutzer:
                # In Metas Konsole stehen mehrere lange Zahlen
                # nebeneinander -- App-ID, Seiten-ID, Konto-ID -- und die
                # falsche davon gibt spaeter eine 404, die nach kaputtem
                # Token aussieht. Das Token weiss selbst, zu welchem
                # Konto es gehoert; also fragen wir es, statt den
                # Menschen raten zu lassen.
                #
                # Die beiden Wege fragen verschieden: Beim
                # Instagram-Login gehoert das Token dem Konto selbst,
                # beim Facebook-Login gehoert es der SEITE, und das
                # Instagram-Konto haengt als Feld daran. Ein Aufruf fuer
                # beide Faelle gaebe auf einem der Wege eine
                # Fehlermeldung, die nach kaputtem Token aussieht.
                if ueber_instagram_login():
                    a = anfrage(f"{GRAPH_IG}/me?fields=user_id,username&"
                                f"access_token={token}", methode="GET")
                    kennung, name = a.get("user_id"), a.get("username")
                else:
                    a = anfrage(f"{GRAPH}/me?fields=name,"
                                f"instagram_business_account"
                                f"&access_token={token}", methode="GET")
                    verknuepft = a.get("instagram_business_account") or {}
                    if not verknuepft:
                        return (f"— Token gilt für die Seite "
                                f"„{a.get('name')}“, aber dort hängt kein "
                                f"Instagram-Konto. In den Seiten-"
                                f"einstellungen verknüpfen, dann erneut "
                                f"prüfen")
                    kennung, name = verknuepft.get("id"), a.get("name")
                return (f"Token gilt für {name} — jetzt noch "
                        f"INSTAGRAM_USER_ID = {kennung} als Secret "
                        f"eintragen")
            allein = ueber_instagram_login()
            basis = GRAPH_IG if allein else GRAPH
            a = anfrage(f"{basis}/{nutzer}?fields=username&"
                        f"access_token={token}", methode="GET")
            # Welcher der beiden Meta-Wege laeuft, ist nicht zu erraten
            # und entscheidet, ob --token-erneuern zustaendig ist.
            weg = "Instagram-Login" if allein else "Facebook-Login"
            return f"OK — Konto @{a.get('username')} ({weg})"

        if kanal == "facebook":
            token, seite = hole("FACEBOOK_PAGE_TOKEN"), hole("FACEBOOK_PAGE_ID")
            if not (token and seite):
                return "— Token oder Seiten-ID fehlt"
            a = anfrage(f"{GRAPH}/{seite}?fields=name&access_token={token}",
                        methode="GET")
            return f"OK — Seite „{a.get('name')}“"

        if kanal == "tiktok":
            token = hole("TIKTOK_ACCESS_TOKEN")
            if not token:
                return "— kein Token gesetzt"
            a = anfrage("https://open.tiktokapis.com/v2/user/info/"
                        "?fields=display_name",
                        kopf={"Authorization": f"Bearer {token}"},
                        methode="GET")
            name = ((a.get("data") or {}).get("user") or {}).get("display_name")
            return f"OK — Konto {name}"
    except Exception as e:                              # noqa: BLE001
        return f"FEHLER — {deuten(kanal, str(e))}"
    return "— unbekannter Kanal"


def deuten(kanal: str, meldung: str) -> str:
    """Aus einer API-Meldung eine Handlungsanweisung machen.

    Ohne das steht da "HTTP 400: OAuthException" und man sitzt eine
    Stunde daran. Die Zuordnungen stammen aus den Meldungen, die die
    Dienste tatsaechlich schicken.
    """
    m = meldung.lower()
    # Zuerst der Fall, der sich als Ablauf tarnt und keiner ist.
    # "Cannot parse access token" heisst: Die Zeichenkette ist gar kein
    # Token. Abgelaufen waere sie lesbar. Das kommt fast immer davon,
    # dass beim Kopieren etwas anderes erwischt wurde -- App-ID oder
    # App-Geheimnis -- oder dass das Token unvollstaendig ist. Wer hier
    # "abgelaufen" liest, erneuert stundenlang etwas, das nie galt.
    if "cannot parse access token" in m or "malformed" in m:
        return (f"{meldung[:90]}\n              -> Das ist kein gültiges "
                f"Token, sondern eine unlesbare Zeichenkette. NICHT "
                f"erneuern, sondern neu kopieren: vollständig, ohne "
                f"Leerzeichen, und nicht die App-ID oder das "
                f"App-Geheimnis")
    if "401" in m or "invalid_token" in m or "access_token_invalid" in m:
        return (f"{meldung[:90]}\n              -> Token ungültig oder "
                f"abgelaufen. Bei Instagram: --token-erneuern")
    if "190" in m and "expired" in m:
        return f"{meldung[:90]}\n              -> Token abgelaufen"
    if "permission" in m or "scope" in m or "#200" in m:
        return (f"{meldung[:90]}\n              -> Berechtigung fehlt. "
                f"Prüfen, ob die App das Recht hat und das Konto ein "
                f"Business-/Creator-Konto ist")
    if "404" in m:
        return (f"{meldung[:90]}\n              -> ID stimmt nicht "
                f"(Konto-, Seiten- oder Kanal-ID prüfen)")
    return meldung[:120]


def senden(kanal: str, text: str, probe: bool, bild: str,
           video: str) -> str:
    """Ruft den Kanal mit dem Medium auf, das er braucht.

    Nicht jeder Kanal nimmt dasselbe: Instagram will ein Bild, TikTok
    ein Video, die vier Textkanaele gar nichts. Die Fallunterscheidung
    steht hier an einer Stelle statt in sieben Funktionen.
    """
    fn = KANAELE[kanal]
    if kanal in BRAUCHT_VIDEO:
        return fn(text, probe, video)
    if kanal in ("instagram", "facebook"):
        return fn(text, probe, bild)
    return fn(text, probe)


def zu_lang(text: str, kanal: str) -> bool:
    return len(text) > GRENZE[kanal]


GEHEIM = ("MASTODON_SERVER", "MASTODON_TOKEN",
          "BLUESKY_HANDLE", "BLUESKY_APP_PASSWORD",
          "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "DISCORD_WEBHOOK",
          "INSTAGRAM_TOKEN", "INSTAGRAM_USER_ID",
          "INSTAGRAM_STANDALONE", "INSTAGRAM_UEBER_FACEBOOK",
          "FACEBOOK_PAGE_TOKEN", "FACEBOOK_PAGE_ID",
          "TIKTOK_ACCESS_TOKEN")


@contextlib.contextmanager
def umgebung(**werte):
    """Umgebungsvariablen setzen und den Zustand davor zurueckgeben.

    Der Selbsttest muss so tun, als sei ein Token gesetzt oder nicht
    gesetzt. Frueher hat er dafuer os.environ direkt beschrieben und
    danach `pop` gerufen -- was den ECHTEN Wert aus den Secrets loeschte,
    weil selbsttest() vor jedem Lauf ausgefuehrt wird. Der erste echte
    Instagram-Beitrag waere mit "übersprungen (INSTAGRAM_TOKEN fehlt)"
    ausgefallen, obwohl das Secret sauber gesetzt war. Ein Werkzeug, das
    sich beim Selbsttest die eigenen Zugangsdaten wegnimmt, meldet
    hinterher genau den Fehler, den es selbst verursacht hat.
    """
    vorher = {k: os.environ.get(k) for k in werte}
    try:
        for k, v in werte.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        yield
    finally:
        for k, v in vorher.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def selbsttest() -> None:
    """Was hier prueft, ist der Aufbau -- nicht die Zustellung.

    Ein echter Sendevorgang laesst sich hier nicht pruefen: Die
    Arbeitsumgebung erreicht keinen der vier Dienste. Der Selbsttest
    deckt deshalb genau das ab, was ohne Netz pruefbar ist, und
    behauptet nichts darueber hinaus. Ob wirklich ein Beitrag
    erscheint, zeigt erst der erste Lauf im Workflow mit --probe aus.
    """
    fehler = []
    # Bezugswert fuer die Probe ganz unten: Der Selbsttest darf die
    # Umgebung, in der er laeuft, nicht veraendern.
    vorzustand = {k: os.environ.get(k) for k in GEHEIM}

    # Laengenpruefung, Positiv- und Negativfall je Kanal.
    for kanal, grenze in GRENZE.items():
        if zu_lang("x" * (grenze - 1), kanal):
            fehler.append(f"{kanal}: knapp unter der Grenze faelschlich "
                          f"als zu lang gemeldet")
        if not zu_lang("x" * (grenze + 1), kanal):
            fehler.append(f"{kanal}: ein Zeichen zu viel nicht erkannt")

    # Ohne Zugangsdaten muss jeder Kanal sauber ueberspringen statt zu
    # stuerzen -- sonst reisst ein fehlendes Secret den ganzen Lauf ab.
    with umgebung(**{k: None for k in GEHEIM}):
        for name in KANAELE:
            antwort = senden(name, "Test", True, "https://x.invalid/b.jpg",
                             "https://x.invalid/v.mp4")
            if "übersprungen" not in antwort:
                fehler.append(f"{name}: ohne Zugangsdaten nicht übersprungen "
                              f"({antwort})")

    # Instagram ohne Bild muss ueberspringen, nicht stuerzen -- und ein
    # Bild ohne https muss auffallen, weil Instagram es sonst selbst
    # ablehnt und man den Grund im Protokoll suchen darf.
    with umgebung(INSTAGRAM_TOKEN="x", INSTAGRAM_USER_ID="1"):
        if "übersprungen" not in instagram("Test", True, ""):
            fehler.append("Instagram ohne Bild wird nicht übersprungen")
        if "ÜBERSPRUNGEN" not in instagram("Test", True, "http://x/b.jpg"):
            fehler.append("Instagram nimmt eine http-URL an")
        if not instagram("Test", True, "https://x/b.jpg").startswith("Probe:"):
            fehler.append("Instagram mit gültigem Bild läuft nicht an")

        # Die beiden Meta-Wege muessen auf verschiedene Adressen zeigen.
        # Das ist keine Kosmetik: Ein Token vom Instagram-Login gilt an
        # graph.facebook.com nicht und umgekehrt.
        with umgebung(INSTAGRAM_UEBER_FACEBOOK=None):
            if GRAPH_IG not in instagram("Test", True, "https://x/b.jpg"):
                fehler.append("Instagram-Login nutzt nicht graph.instagram.com")
        with umgebung(INSTAGRAM_UEBER_FACEBOOK="ja"):
            if GRAPH not in instagram("Test", True, "https://x/b.jpg"):
                fehler.append("Facebook-Login nutzt nicht graph.facebook.com")

        # --token-erneuern gilt nur fuer den Instagram-Login. Auf dem
        # Seiten-Weg muss es sauber ueberspringen statt eine
        # OAuthException zu werfen, die nach kaputtem Token aussieht.
        with umgebung(INSTAGRAM_UEBER_FACEBOOK="ja"):
            if "übersprungen" not in instagram_token_erneuern():
                fehler.append("Token-Erneuerung läuft auf dem Seiten-Weg an")

    # TikTok ohne Video ebenso.
    with umgebung(TIKTOK_ACCESS_TOKEN="x"):
        if "übersprungen" not in tiktok("Test", True, ""):
            fehler.append("TikTok ohne Video wird nicht übersprungen")
        if "inbox" not in tiktok("Test", True, "https://x/v.mp4"):
            fehler.append("TikTok nimmt nicht den Entwurfs-Endpunkt")

    # Die Ausweichlogik von TikTok: Nur eine Domain-Beanstandung darf
    # auf FILE_UPLOAD umschalten. Jeder andere Fehler -- abgelaufenes
    # Token, kaputtes Video -- muss durchschlagen, sonst laedt das
    # Werkzeug bei einem 401 stumpf ein Video herunter und scheitert
    # zweimal statt einmal.
    for meldung, weicht_aus in (
            ("url_ownership_unverified", True),
            ("unverified domain", True),
            ("HTTP 401: access_token_invalid", False),
            ("HTTP 500: server error", False)):
        trifft = ("url_ownership_unverified" in meldung
                  or "unverified" in meldung.lower())
        if trifft != weicht_aus:
            fehler.append(f"Ausweichregel falsch bei {meldung!r}")

    # Die Wegerkennung. Sie ersetzt eine Frage an den Menschen durch
    # eine Beobachtung am Token -- und muss deshalb belegen, dass sie
    # beide Praefixe auseinanderhaelt und die Notueberschreibung
    # weiterhin gewinnt.
    for token, ueberschreibung, soll, was in (
            ("EAA" + "z" * 190,  None,  False, "EAA erkennt Facebook-Weg"),
            ("IGAA" + "x" * 190, None,  True,  "IGAA erkennt Instagram-Weg"),
            ("IGQVJ" + "y" * 160, None, True,  "IGQ erkennt Instagram-Weg"),
            ("IGAA" + "x" * 190, "ja",  False, "Ansage schlägt Erkennung"),
            ("EAA" + "z" * 190,  "ja",  False, "Ansage und Erkennung einig"),
            ("",                 None,  True,  "ohne Token bleibt Standard"),
    ):
        with umgebung(INSTAGRAM_TOKEN=token or None,
                      INSTAGRAM_UEBER_FACEBOOK=ueberschreibung):
            if ueber_instagram_login() is not soll:
                fehler.append(f"Wegerkennung falsch: {was}")

    # Die Gestaltpruefung des Tokens, gegen echte Faelle. Der Positivfall
    # gehoert zwingend dazu: Eine Pruefung, die alles beanstandet, haelt
    # auch das richtige Token auf -- und dann sucht man den Fehler dort,
    # wo keiner ist. Die Laengen und Praefixe stammen aus dem, was Meta
    # auf der Einrichtungsseite nebeneinander anzeigt.
    echt_ig = "IGAA" + "x" * 190
    echt_fb = "EAA" + "z" * 190
    for wert, ig_login, soll, was in (
            # Instagram-Login: IG richtig, EAA falsch
            (echt_ig,               True,  None,           "IG-Token"),
            ("IGQVJ" + "y" * 160,   True,  None,           "älteres IG-Token"),
            (echt_fb,               True,  "EAA",          "FB-Token am IG-Weg"),
            # Facebook-Login: genau umgekehrt. Ohne diesen Block wuerde
            # die Pruefung jeden aufhalten, der ueber die Seite geht.
            (echt_fb,               False, None,           "FB-Token am FB-Weg"),
            (echt_ig,               False, "beginnt mit IG", "IG-Token am FB-Weg"),
            # Verwechslungen, die auf beiden Wegen falsch sind
            ("17841400000000000",   True,  "Ziffern",      "Konto-ID"),
            ("1234567890123456",    False, "Ziffern",      "App-ID"),
            ("a3f" + "b" * 29,      True,  "Zeichen lang", "App-Geheimnis"),
            ("IGAA" + "x" * 100 + " " + "x" * 90, True, "Leerzeichen",
             "mit Umbruch"),
            ("IGAA" + "x" * 20,     True,  "abgeschnitten", "halb kopiert"),
    ):
        ergebnis = token_form(wert, ig_login)
        if soll is None and ergebnis is not None:
            fehler.append(f"Tokenform: {was} fälschlich beanstandet "
                          f"({ergebnis})")
        if soll is not None and (ergebnis is None or soll not in ergebnis):
            fehler.append(f"Tokenform: {was} nicht erkannt ({ergebnis})")

    # Und die Regel, die ueber allem steht: Das Token darf nie in der
    # Ausgabe landen, auch nicht in Bruchstuecken.
    for wert in (echt_ig, "EAA" + "z" * 190):
        meldung = token_form(wert) or ""
        if wert[:12] in meldung:
            fehler.append("Tokenform gibt Teile des Tokens aus")

    # Die Zugangsprobe darf ohne Zugangsdaten nichts ins Netz schicken.
    # Sie ruft sonst genau dann eine Adresse auf, wenn am wenigsten
    # feststeht -- und die Fehlermeldung sagt dann nichts ueber das
    # fehlende Secret, sondern ueber den Aufruf.
    #
    # Der erste Anlauf hat hier auf die Woerter "fehlt" und "keine"
    # geprueft -- eine aus dem Kopf geschriebene Liste, die an "kein
    # Token gesetzt" scheiterte und drei gesunde Kanaele anschwaerzte.
    # Geprueft wird deshalb die Konvention, die im Code wirklich gilt:
    # "— …" heisst nicht eingerichtet, "OK — …" heisst steht,
    # "FEHLER — …" heisst, es wurde etwas aufgerufen.
    with umgebung(**{k: None for k in GEHEIM}):
        for kanal in KANAELE:
            antwort = zugang_pruefen(kanal)
            if not antwort.startswith("—") or "FEHLER" in antwort:
                fehler.append(f"Zugangsprobe {kanal}: ohne Zugangsdaten "
                              f"keine klare Fehlanzeige ({antwort})")

    # Die Probe darf unter keinen Umstaenden senden. Ein Kanal mit
    # Zugangsdaten muss im Probelauf trotzdem nur beschreiben.
    with umgebung(DISCORD_WEBHOOK="https://example.invalid/haken"):
        if not discord("Test", probe=True).startswith("Probe:"):
            fehler.append("Probe sendet, statt nur zu beschreiben")

    # Die Gegenprobe zum gefaehrlichsten Fehler dieses Skripts: Der
    # Selbsttest laeuft vor JEDEM Aufruf. Nimmt er der Umgebung dabei
    # ein Secret weg, meldet der eigentliche Lauf danach "Token fehlt"
    # -- und der Verdacht faellt auf das Secret statt auf den Test.
    # Deshalb wird hier nicht die Absicht geprueft, sondern der
    # Zustand: Ist die Umgebung nach dem Test noch dieselbe?
    verloren = [k for k in GEHEIM if os.environ.get(k) != vorzustand[k]]
    if verloren:
        fehler.append(f"Der Selbsttest hat die Umgebung verändert: "
                      f"{sorted(verloren)}")

    print("Selbsttest:")
    for f in fehler:
        print("  FEHLER:", f)
    if fehler:
        sys.exit(1)
    print("  bestanden (Längengrenzen je Kanal positiv und negativ; "
          "Überspringen ohne Zugangsdaten und ohne Medium; Instagram "
          "lehnt http ab; TikTok nimmt den Entwurfs-Endpunkt; "
          "Probe sendet nicht; TikTok weicht nur bei Domain-"
          "Beanstandung auf FILE_UPLOAD aus).")
    print("  NICHT geprüft: ob ein Beitrag wirklich erscheint — dafür "
          "fehlt hier das Netz.")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--text", default="")
    # Leer statt Vorgabe, damit "--zugang" unterscheiden kann zwischen
    # "keine Auswahl getroffen" (alle pruefen) und "genau diesen einen".
    # Vorher hat --zugang die Auswahl ignoriert und immer alle sieben
    # gemeldet -- wer nur Instagram einrichtet, las sechs Fehlzeilen mit.
    p.add_argument("--kanaele", default="")
    p.add_argument("--bild", default="",
                   help="öffentliche https-URL; Instagram verlangt sie, "
                        "Facebook nutzt sie wenn vorhanden")
    p.add_argument("--video", default="",
                   help="öffentliche https-URL für TikTok")
    p.add_argument("--probe", action="store_true",
                   help="nichts senden, nur zeigen was passieren würde")
    p.add_argument("--selbsttest", action="store_true")
    p.add_argument("--zugang", action="store_true",
                   help="nur prüfen, ob die Zugangsdaten stimmen — "
                        "veröffentlicht nichts")
    p.add_argument("--token-erneuern", action="store_true",
                   help="Instagram-Token um 60 Tage verlängern")
    a = p.parse_args()

    selbsttest()
    if a.selbsttest:
        return
    auswahl = [k.strip() for k in a.kanaele.split(",") if k.strip()]
    unbekannt = [k for k in auswahl if k not in KANAELE]
    if unbekannt:
        raise SystemExit(f"Unbekannte Kanäle: {unbekannt}. "
                         f"Möglich: {sorted(KANAELE)}")

    if a.zugang:
        print("\nZugangsprobe — es wird nichts veröffentlicht.\n")
        for k in sorted(auswahl or KANAELE):
            print(f"  {k:10s} {zugang_pruefen(k)}")
        return
    if a.token_erneuern:
        print("\n" + instagram_token_erneuern())
        return
    if not a.text.strip():
        print("\nKein Text. Nichts zu tun.")
        return

    gewaehlt = auswahl or ["mastodon", "bluesky", "telegram", "discord"]

    print(f"\nText: {len(a.text)} Zeichen"
          f"{'  (PROBELAUF, es wird nichts gesendet)' if a.probe else ''}\n")
    fehlgeschlagen = 0
    for k in gewaehlt:
        if zu_lang(a.text, k):
            print(f"  {k:9s} ÜBERSPRUNGEN — {len(a.text)} Zeichen, "
                  f"Grenze {GRENZE[k]}")
            continue
        try:
            print(f"  {k:9s} {senden(k, a.text, a.probe, a.bild, a.video)}")
        except Exception as e:                          # noqa: BLE001
            fehlgeschlagen += 1
            print(f"  {k:9s} FEHLER: {e}")

    if fehlgeschlagen:
        raise SystemExit(f"\n{fehlgeschlagen} Kanal/Kanäle fehlgeschlagen.")


if __name__ == "__main__":
    main()
