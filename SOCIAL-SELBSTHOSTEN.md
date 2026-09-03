# Metricool ersetzen — der kostenlose Weg

Stand 03.09.2026, **zweiter Durchgang mit Korrektur**. Anlass:
Metricool begrenzt die Zahl der geplanten Beiträge.

> ## Korrektur des ersten Berichts
>
> Der erste Durchgang endete mit dem Satz, jeder Kanal brauche ein
> Genehmigungsverfahren („Geld gegen Zeit und Genehmigungen"). **Das
> war zu pauschal und in der Sache falsch.**
>
> Übersehen hatte ich den **Entwicklungsmodus** von Meta-Apps. Wer nur
> auf **eigene** Konten postet und selbst Administrator der App ist,
> darf die Veröffentlichungsrechte **ohne App-Review** benutzen. Genau
> das ist der Fall bei Homeeins — es wird auf die eigenen Kanäle
> gepostet, nicht im Auftrag Dritter.
>
> Damit ist der kostenlose Weg für die wichtigsten Kanäle offen, und
> die Antwort im ersten Bericht war unnötig entmutigend.

---

## Die Trennlinie, auf die es ankommt

Nicht „welche Software", sondern **wem gehört das Konto, auf das
gepostet wird**:

| | App-Review nötig? |
|---|---|
| Du postest auf **fremde** Konten (wie Metricool es tut) | **ja**, immer |
| Du postest auf **deine eigenen** Konten | **nein**, Entwicklungsmodus reicht |

Metricool braucht das Review, weil es für tausende fremde Kunden
postet. Du brauchst es nicht.

---

## Kanal für Kanal

**Kostenlos und ohne Genehmigung — sofort nutzbar:**

| Kanal | Weg | Praktische Grenze |
|---|---|---|
| **Mastodon** | Zugangstoken in den Kontoeinstellungen | keine nennenswerte |
| **Bluesky** | App-Passwort, AT-Protokoll | keine nennenswerte |
| **Telegram** | Bot-Token vom BotFather | 30 Nachrichten/Sekunde |
| **Discord** | Webhook-URL, ein Klick | 5 pro Sekunde |
| **WordPress** | Anwendungspasswort | keine |
| **Reddit** | eigene App, Skript-Typ | 100 Anfragen/Minute |

**Kostenlos, aber einmalige Einrichtung — kein Review, wenn eigenes Konto:**

| Kanal | Voraussetzung | Praktische Grenze |
|---|---|---|
| **Instagram** | eigene Meta-App im Entwicklungsmodus. **Zwei Wege** — siehe unten | Content-Publishing-Limit je Konto und Tag |
| **Facebook-Seite** | dieselbe Meta-App, Seiten-Token | großzügig |
| **Threads** | eigene Threads-App, eigenes Konto | Tageslimit je Konto |
| **YouTube** | Google-Cloud-Projekt, OAuth auf den eigenen Kanal | Tagesquote; ein Upload kostet viel davon |

**Auch kostenlos — mit einem Zugeständnis:**

| Kanal | Weg | Zugeständnis |
|---|---|---|
| **TikTok** | Scope `video.upload` statt `video.publish`. Das Video landet als **Entwurf** im TikTok-Postfach. | ein Fingertipp je Video in der App |
| **X** | Free-Tier-Schreibzugriff über `api.x.com/2/tweets` | Monatskontingent |
| **Pinterest** | Testzugang | eingeschränkt |

**Der TikTok-Fund im Beleg.** In `gerardosilva/TiktokBot-Draft-Updater`
steht der Endpunkt im Klartext:

```
https://open.tiktokapis.com/v2/post/publish/inbox/video/init/
scope: video.upload
```

`inbox` statt `direct` und `video.upload` statt `video.publish` — das
ist der Weg, den nicht geprüfte Apps offiziell gehen dürfen. Kein
Audit, keine Kosten, keine Regelverletzung. Nur der letzte Tipp auf
„Posten" bleibt von Hand.

### Instagram geht auch ohne Facebook-Seite

Postiz hat für Instagram **zwei** Anbieter im Code, und der zweite ist
der bequemere:

| | Endpunkt | Voraussetzung |
|---|---|---|
| `instagram.provider.ts` | `graph.facebook.com` | Instagram-Konto **muss** mit einer Facebook-Seite verknüpft sein |
| `instagram.standalone.provider.ts` | `graph.instagram.com`, Login über `instagram.com/oauth/authorize?enable_fb_login=0` | **keine Facebook-Seite nötig** |

Die Rechte des Standalone-Wegs, aus dem Quelltext:

```
instagram_business_basic
instagram_business_content_publish
instagram_business_manage_comments
instagram_business_manage_insights
```

Das heißt: Business- oder Creator-Konto genügt, die Facebook-Seite
entfällt. Ein Einrichtungsschritt weniger.

---

## Und der Weg, den „andere im Internet" gehen

Bei der Suche kamen sofort die meistgesternten Treffer hoch:
`instagrapi` (6.738 ⭐), `instagram-private-api` (6.472 ⭐),
`instagram4j`, `InstagramApiSharp`. Das sind **rückentwickelte private
APIs** — sie melden sich an wie die Handy-App und umgehen die
offizielle Schnittstelle vollständig.

**Sie sind kostenlos, unbegrenzt und funktionieren.** Deshalb findet
man sie überall.

**Und sie sind der Grund, warum Konten gesperrt werden.** Sie
verstoßen gegen die Nutzungsbedingungen; Meta erkennt automatisierte
Anmeldungen an Gerätekennungen und Verhaltensmustern. Der Verlust
trifft nicht die App, sondern **das Konto des Ladens**.

Für einen Shop mit echten Kunden ist dieser Handel schlecht: unbegrenzt
posten gegen das Risiko, den Kanal ganz zu verlieren. Für einen
Wegwerf-Account mag das anders aussehen — für Homeeins nicht.

**Das ist kein moralischer Einwand, sondern eine Risikorechnung.**

---

## Ergebnis: Für jeden Kanal gibt es einen kostenlosen Weg

| Kanal | kostenlos? | Aufwand |
|---|---|---|
| Mastodon, Bluesky, Telegram, Discord, WordPress, Nostr, Medium, Dev.to | **ja** | Token einfügen, fertig |
| Instagram | **ja** | eigene Meta-App, Entwicklungsmodus |
| Facebook-Seite | **ja** | dieselbe App |
| Threads | **ja** | eigene App |
| YouTube | **ja** | Google-Cloud-Projekt |
| **TikTok** | **ja** | ein Fingertipp je Video |
| **X** | **ja** | Monatskontingent |

**Es muss nichts bezahlt werden.** Der einzige laufende Posten ist ein
kleiner Server für Postiz — und selbst der entfällt, wenn du es auf
einem Rechner laufen lässt, der ohnehin läuft.

---

## Die Empfehlung

**Postiz selbst hosten** (AGPL-3.0, 35.410 ⭐, Commit von gestern, 36
Anbieter) und die eigenen App-Zugangsdaten im Entwicklungsmodus
eintragen. Kosten: ein kleiner Server, sonst nichts. Kein Beitragslimit.

Reihenfolge nach Aufwand:

1. **Sofort, ohne Einrichtungsaufwand:** Mastodon, Bluesky, Telegram,
   Discord. Damit steht das System an einem Abend, und du siehst, ob
   der Betrieb trägt.
2. **Dann Meta** — Instagram und Facebook, eine App für beide. Das ist
   der Kanal, der für Möbel zählt.
3. **Dann YouTube**, eigenes Google-Cloud-Projekt.
4. **TikTok** über den Entwurfs-Weg, **X** über das Free-Tier. Beides
   kostet nichts; TikTok kostet einen Fingertipp je Video.

**Metricool währenddessen laufen lassen.** Erst kündigen, wenn Postiz
für die wichtigsten Kanäle nachweislich postet.

`gitroomhq/postiz-agent` (440 ⭐) ist eine CLI, die sich als
Claude-Code-Plugin einbinden lässt — damit ließe sich das Planen direkt
aus einer Sitzung steuern.

**Zugangsdaten gehören in GitHub Secrets oder die Serverumgebung**, nie
ins Repository und nie in den Chat (`CLAUDE.md`, Regel 4).

---

## Die Grenze dieser Recherche

**Gemessen** — aus geklonten Repositories: Sternzahlen, Lizenzen,
Commit-Daten, die 36 Anbieter in Postiz, die benötigten Rechte
(`instagram_content_publish`, `instagram_basic`,
`instagram_business_account`), n8ns Knotenliste.

**Nicht von hier prüfbar**, weil die Umgebung nur GitHub, PyPI und npm
erreicht — das sind die Stellen, an denen konkrete Zahlen stehen:

- **Die genauen Tageslimits** für Instagram, Threads und YouTube.
  Sie stehen in Metas und Googles eigenen Unterlagen und ändern sich.
- **Ob der Entwicklungsmodus weiterhin ohne Review veröffentlicht.**
  Das Verfahren gilt seit Jahren, aber Meta ändert Bedingungen.
- **Was X' Schreibzugriff heute kostet.**

Der erste Schritt sollte deshalb ein **Testlauf mit einem Kanal** sein,
nicht der Umbau aller Kanäle auf einmal.
