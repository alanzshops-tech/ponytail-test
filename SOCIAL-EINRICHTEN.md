# Einrichten: von null bis zum ersten Beitrag

Begleitpapier zu `scripts/posten.py` und `.github/workflows/posten.yml`.
Die Herleitung, **warum** das kostenlos geht, steht in
`SOCIAL-SELBSTHOSTEN.md`. Hier steht nur, **was zu tun ist**.

Die Stufen sind nach Aufwand sortiert, nicht nach Wichtigkeit. Stufe 1
ist der bequeme Einstieg — aber für Homeeins liegt die Reichweite bei
Instagram, und wer die will, fängt bei **Stufe 2** an. Das kostet einen
Abend in Metas Entwicklerkonsole statt zwanzig Minuten. Die Stufen sind
voneinander unabhängig; man kann jede einzeln machen.

**Für den Instagram-Start direkt zu [Stufe 2](#stufe-2--meta-instagram-und-facebook).**

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

### Es gibt zwei Wege. Nimm den ersten.

Meta bietet für Instagram zwei getrennte Verfahren an. Sie sehen
ähnlich aus, haben aber verschiedene Adressen, verschiedene Rechte und
verschiedene Ablauffristen. Wer sie vermischt, bekommt Token-Fehler,
die nach kaputten Zugangsdaten aussehen, obwohl nur die Adresse nicht
passt.

| | **Instagram-Login** *(empfohlen)* | Facebook-Login |
|---|---|---|
| Adresse | `graph.instagram.com` | `graph.facebook.com` |
| Facebook-Seite nötig? | **nein** | ja, verknüpft |
| Token | 60 Tage, verlängerbar | Seiten-Token, läuft nicht ab |
| Secret `INSTAGRAM_STANDALONE` | **setzen** | leer lassen |
| `token_erneuern` zuständig? | ja | nein (braucht es nicht) |

Für Homeeins ist der **Instagram-Login** der richtige: weniger
Schritte, keine Facebook-Seite als Zwischenglied, und der
Verlängerungsbefehl im Werkzeug bedient genau diesen Weg.

### Voraussetzung, an der die meisten scheitern

Das Instagram-Konto muss ein **Business- oder Creator-Konto** sein. Ein
privates Konto kann über die API nicht veröffentlichen — die API
antwortet dann mit einem Berechtigungsfehler, der aussieht, als fehle
der App ein Recht. Umstellen in der Instagram-App:
**Einstellungen → Konto → Kontotyp**.

### Die Schritte

1. Instagram-Konto auf **Business** oder **Creator** umstellen (siehe
   oben)
2. `developers.facebook.com` → **Meine Apps → App erstellen**
3. Als App-Typ **Business** wählen
4. Produkt hinzufügen: **Instagram**, darin der Einrichtungsweg mit
   **Instagram-Business-Login**
5. Die App bleibt im **Entwicklungsmodus** — das ist gewollt und der
   ganze Grund, warum das kostenlos und ohne App-Review geht. Solange
   nur auf eigene Konten gepostet wird, ist kein Review nötig.
6. Dich selbst als **Administrator** der App eintragen. Das ist der
   Punkt, an dem der Entwicklungsmodus greift — ohne diesen Eintrag
   gilt dein Konto der App als fremd.
7. Rechte: **`instagram_business_basic`** und
   **`instagram_business_content_publish`**. Ohne das zweite kann die
   App lesen, aber nicht posten.
8. Zugriffstoken erzeugen. **Es muss das langlebige sein** (60 Tage),
   nicht das kurzlebige (1 Stunde). Die Konsole zeigt die Laufzeit an.
9. Direkt neben dem Token steht die **Instagram-Konto-ID** — eine lange
   Zahl, die mit `1784…` beginnt. Das ist `INSTAGRAM_USER_ID`, **nicht**
   der @-Name.
10. Drei Secrets eintragen:
    `INSTAGRAM_TOKEN`, `INSTAGRAM_USER_ID`, und
    `INSTAGRAM_STANDALONE` = `1`
11. **Actions → Posten → Run workflow**, `kanaele` = `instagram`,
    Haken bei **`zugang`**

Bei Schritt 11 muss dort stehen:

```
  instagram  OK — Konto @deinname (Instagram-Login)
```

Steht in der Klammer **Facebook-Login**, fehlt `INSTAGRAM_STANDALONE`.
Steht dort ein `FEHLER`, nennt die Meldung den Grund.

> Die Menübezeichnungen in Metas Konsole ändern sich mehrmals im Jahr,
> und diese Arbeitsumgebung erreicht `developers.facebook.com` nicht —
> die Schrittnamen oben sind also nicht nachgemessen. Was nachgemessen
> ist, sind die Rechte, die Adressen und die Secret-Namen; die prüft
> die Zugangsprobe. Wenn ein Menü anders heißt, such nach dem Recht
> `instagram_business_content_publish` — daran hängt alles.

### Für die Facebook-Seite (später, optional)

Zusätzlich `FACEBOOK_PAGE_TOKEN` (das **Seiten**-Token, nicht das
Nutzertoken) und `FACEBOOK_PAGE_ID`. Facebook läuft immer über
`graph.facebook.com` und ist von `INSTAGRAM_STANDALONE` unberührt.

### Danach: alle zwei Monate das Token verlängern

Token aus dem Instagram-Login laufen nach rund 60 Tagen ab.
**Actions → Posten → Run workflow**, Haken bei **`token_erneuern`**.
Die Ausgabe nennt die neue Restlaufzeit; das neue Token von Hand ins
Secret `INSTAGRAM_TOKEN` übertragen.

Auf dem Facebook-Login-Weg ist das nicht nötig — ein Seiten-Token aus
einem langlebigen Nutzertoken läuft nicht ab. Der Befehl überspringt
dort und sagt das auch.

> Automatisch ginge die Verlängerung nur, wenn das Token im Repository
> läge — und Zugangsdaten gehören nicht dorthin (`CLAUDE.md`, Regel 4).

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
| `übersprungen (Instagram braucht ein Bild)` | `bild` mit einer öffentlichen `https`-Adresse füllen |
| `ÜBERSPRUNGEN — Bild muss öffentlich per https` | `http` reicht nicht, Instagram holt es selbst ab |
| Zugangsprobe sagt `(Facebook-Login)`, obwohl Instagram-Login eingerichtet ist | Secret `INSTAGRAM_STANDALONE` fehlt |

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
