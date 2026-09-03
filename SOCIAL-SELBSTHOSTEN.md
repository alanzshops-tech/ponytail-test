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
| **Instagram** | Business- oder Creator-Konto, verknüpft mit einer Facebook-Seite; eigene Meta-App im Entwicklungsmodus | Content-Publishing-Limit je Konto und Tag |
| **Facebook-Seite** | dieselbe Meta-App, Seiten-Token | großzügig |
| **Threads** | eigene Threads-App, eigenes Konto | Tageslimit je Konto |
| **YouTube** | Google-Cloud-Projekt, OAuth auf den eigenen Kanal | Tagesquote; ein Upload kostet viel davon |

**Echte Mauern — hier gibt es keinen kostenlosen Weg:**

| Kanal | Warum |
|---|---|
| **TikTok** | Die Content-Posting-API lässt nicht geprüfte Apps nur **privat** veröffentlichen. Öffentlich posten geht erst nach Audit. |
| **X** | Schreibzugriff ist seit 2023 kostenpflichtig bzw. im Gratis-Kontingent sehr eng. |
| **Pinterest** | Nur eingeschränkter Testzugang, mehr erst nach Prüfung. |

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
4. **TikTok und X bleiben bei Metricool** oder werden von Hand
   gepostet — dort ist der kostenlose Weg tatsächlich zu.

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
