# Einrichten: von null bis zum ersten Beitrag

Begleitpapier zu `scripts/posten.py` und `.github/workflows/posten.yml`.
Die Herleitung, **warum** das kostenlos geht, steht in
`SOCIAL-SELBSTHOSTEN.md`. Hier steht nur, **was zu tun ist**.

Reihenfolge ist Absicht: erst die Kanäle, bei denen nichts schiefgehen
kann, dann die mit eigener App. Wer bei Instagram anfängt, sitzt am
ersten Abend in Metas Entwicklerkonsole und hat nichts vorzuweisen.

---

## Der Ablauf für jeden Kanal ist immer derselbe

1. Zugangsdaten besorgen (siehe unten)
2. Als Secret eintragen: **Settings → Secrets and variables → Actions**
3. **Actions → Posten → Run workflow**, Haken bei **`zugang`**
4. Steht dort `OK`, weiter. Steht dort `FEHLER`, sagt die Meldung was fehlt
5. Erst dann ein echter Beitrag mit `probe: false`

**Schritt 3 ist der wichtigste.** Die Zugangsprobe ruft je Kanal einen
lesenden Endpunkt auf, veröffentlicht nichts und kann beliebig oft
laufen. Sie sagt nicht nur „geht nicht", sondern was zu tun ist —
abgelaufenes Token, fehlende Berechtigung oder falsche ID sind drei
verschiedene Meldungen.

---

## Stufe 1 — die vier ohne Antrag (ein Abend)

### Telegram
1. In Telegram **@BotFather** anschreiben, `/newbot`, Namen vergeben
2. Der Bot-Token kommt sofort → Secret `TELEGRAM_BOT_TOKEN`
3. Bot als **Administrator** in den eigenen Kanal aufnehmen
4. Secret `TELEGRAM_CHAT_ID` = `@kanalname`

### Discord
1. Kanal → **Bearbeiten → Integrationen → Webhooks → Neuer Webhook**
2. URL kopieren → Secret `DISCORD_WEBHOOK`

### Mastodon
1. **Einstellungen → Entwicklung → Neue Anwendung**
2. Recht **`write:statuses`** genügt
3. „Zugriffsschlüssel" kopieren → Secret `MASTODON_TOKEN`
4. Bei anderem Server als mastodon.social: `MASTODON_SERVER` setzen

### Bluesky
1. **Einstellungen → Datenschutz und Sicherheit → App-Passwörter**
2. Neues App-Passwort → Secret `BLUESKY_APP_PASSWORD`
3. Secret `BLUESKY_HANDLE` = z. B. `homeeins.bsky.social`

> **Nicht das Kontopasswort verwenden.** App-Passwörter lassen sich
> einzeln zurückziehen, das Kontopasswort nicht.

---

## Stufe 2 — Meta: Instagram und Facebook

**Voraussetzung:** Das Instagram-Konto muss ein **Business- oder
Creator-Konto** sein. Ein privates Konto kann über die API nicht
veröffentlichen — das ist die häufigste Fehlerquelle und kein Fehler im
Werkzeug.

1. `developers.facebook.com` → **Meine Apps → App erstellen**
2. Typ: **Business**
3. Produkt hinzufügen: **Instagram** (bzw. **Facebook-Login**)
4. Die App bleibt im **Entwicklungsmodus** — das ist gewollt. Solange
   du nur auf eigene Konten postest, ist kein App-Review nötig.
5. Dich selbst als **Administrator** der App eintragen (das ist der
   Punkt, an dem der Entwicklungsmodus greift)
6. Zugriffstoken erzeugen, Rechte:
   `instagram_business_basic`, `instagram_business_content_publish`
7. Secrets: `INSTAGRAM_TOKEN`, `INSTAGRAM_USER_ID`
8. Für den Weg **ohne Facebook-Seite**: Secret `INSTAGRAM_STANDALONE`
   auf irgendeinen Wert setzen
9. Für die Facebook-Seite zusätzlich: `FACEBOOK_PAGE_TOKEN` (das
   **Seiten**-Token, nicht das Nutzertoken) und `FACEBOOK_PAGE_ID`

### Danach: einmal im Monat das Token verlängern

Instagram-Token laufen nach rund 60 Tagen ab. **Actions → Posten →
Run workflow**, Haken bei **`token_erneuern`**. Die Ausgabe nennt die
neue Restlaufzeit; das neue Token von Hand ins Secret übertragen.

> Automatisch ginge das nur, wenn das Token im Repository läge — und
> Zugangsdaten gehören nicht dorthin (`CLAUDE.md`, Regel 4).

### Bilder müssen öffentlich erreichbar sein

Instagram holt das Bild selbst ab. Ein Pfad im Repository geht nicht,
eine `http`-Adresse auch nicht. **Die Shopify-CDN-Adressen der
Produktbilder sind öffentlich und funktionieren** — im Shop-Adminbereich
das Bild öffnen und die Adresse kopieren.

---

## Stufe 3 — TikTok

1. `developers.tiktok.com` → App anlegen
2. Produkt **Content Posting API** hinzufügen
3. Scope **`video.upload`** — *nicht* `video.publish`. Der erste
   braucht kein Audit, der zweite schon.
4. Login-Kit durchlaufen, Zugriffstoken → Secret `TIKTOK_ACCESS_TOKEN`

**Das Video landet als Entwurf im TikTok-Postfach.** Veröffentlicht
wird mit einem Fingertipp in der App. Das ist der Preis dafür, kein
Auditverfahren zu durchlaufen.

Zur Videoquelle: Das Werkzeug versucht zuerst `PULL_FROM_URL` (TikTok
holt selbst) und weicht bei einer Domain-Beanstandung automatisch auf
`FILE_UPLOAD` aus — dabei lädt das Skript das Video herunter und
schiebt die Bytes selbst hoch. **Keine Domain-Verifizierung nötig.**

---

## Wenn etwas nicht geht

| Meldung | Bedeutung |
|---|---|
| `Token ungültig oder abgelaufen` | Bei Instagram: `token_erneuern`. Sonst neu erzeugen |
| `Berechtigung fehlt` | App hat das Recht nicht, **oder** das Instagram-Konto ist privat statt Business |
| `ID stimmt nicht` | Konto-, Seiten- oder Kanal-ID prüfen |
| `url_ownership_unverified` | passiert automatisch — das Werkzeug weicht auf FILE_UPLOAD aus |

Die Zugangsprobe (`zugang: true`) übersetzt die API-Meldungen in diese
Sätze. Sie lässt sich beliebig oft laufen, weil sie nichts postet.

---

## Was bewusst nicht gebaut ist

**Kein Browser-Automat.** Es wäre technisch möglich, mit dem
vorhandenen Playwright einen angemeldeten Browser fernzusteuern und so
ganz ohne API zu posten — kostenlos und ohne jedes Limit. Dagegen
sprechen zwei Dinge: Es verstößt bei den meisten Plattformen gegen die
Nutzungsbedingungen, und es bricht bei jeder Oberflächenänderung. Der
API-Weg ist langweiliger und hält.

**Keine automatische Token-Ablage.** Siehe oben — Zugangsdaten gehören
nicht ins Repository.
