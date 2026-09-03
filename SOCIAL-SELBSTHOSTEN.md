# Metricool ersetzen? Selbst hosten oder selbst bauen

Stand 03.09.2026. Anlass: Metricool begrenzt die Zahl der geplanten
Beiträge. Frage war, ob es eine quelloffene Alternative gibt, mit der
sich alle Kanäle bespielen lassen — oder ob man das selbst baut.

**Gemessen, nicht erinnert.** Diese Arbeitsumgebung erreicht GitHub,
PyPI und npm. Genau dort liegen solche Werkzeuge, also ist die
Recherche hier ausnahmsweise direkt möglich: Repositories gesucht,
geklont, Lizenzdateien gelesen, Anbieterverzeichnisse und
`.env.example` ausgewertet. Was **nicht** von hier aus prüfbar ist,
steht unten unter „Die Grenze dieser Recherche".

---

## Das Ergebnis in einem Satz

**Die Software ist kostenlos zu haben und ausgereift. Der Zugang zu den
Plattformen ist es nicht** — und der ist das eigentliche Hindernis, bei
jeder Lösung gleich, ob gekauft, selbst gehostet oder selbst gebaut.

---

## Die Kandidaten, gemessen am 03.09.2026

| | Postiz | Mixpost |
|---|---|---|
| Sterne | **35.410** | 3.654 |
| Lizenz | **AGPL-3.0** | **MIT** |
| Letzter Commit | **vor 14 Stunden** | vor **6 Monaten** |
| Sprache | TypeScript (Next.js/NestJS) | PHP (Laravel/Vue) |
| Anbieter im Code | **36** | 3 Familien (Meta, Twitter, Mastodon) |

**Postiz** ist der klare Marktführer und lebendig. Im Verzeichnis
`libraries/nestjs-libraries/src/integrations/social/` liegen 36
Anbieter, darunter alle für Homeeins relevanten:

> `instagram` · `instagram.standalone` · `facebook` · `tiktok` ·
> `tiktok.business` · `youtube` · `pinterest` · `x` · `threads` ·
> `linkedin` · `linkedin.page`

Dazu Bluesky, Mastodon, Reddit, Discord, Telegram, WordPress, Medium,
Dev.to, Tumblr, Twitch, Nostr, Farcaster und weitere.

**Mixpost** ist zwar MIT-lizenziert — juristisch bequemer als AGPL —,
aber seit sechs Monaten ohne Commit und deckt im quelloffenen Teil nur
drei Anbieterfamilien ab. Für „alle Kanäle bespielen" reicht das nicht.

**Ein Nebenfund, der zu diesem Projekt passt:** `gitroomhq/postiz-agent`
(440 Sterne) ist eine CLI, die sich als Claude-Code-Plugin einbinden
lässt — `/plugin install postiz@postiz-agent`. Damit ließe sich das
Planen direkt aus einer Sitzung heraus steuern, statt über eine
Weboberfläche.

---

## Warum „selbst bauen" keinen Vorteil bringt

Der Reflex ist verständlich: ein Scheduler ist technisch simpel — eine
Tabelle mit Terminen, ein Cronjob, pro Plattform ein HTTP-Aufruf. Das
ist an einem Wochenende gebaut.

**Nur ist das nicht die Arbeit.** Postiz' `.env.example` zeigt, was
jeder Kanal tatsächlich verlangt — eigene App-Zugangsdaten, die man bei
der jeweiligen Plattform beantragen muss:

```
FACEBOOK_APP_ID / FACEBOOK_APP_SECRET
THREADS_APP_ID / THREADS_APP_SECRET
TIKTOK_CLIENT_ID / TIKTOK_CLIENT_SECRET
TIKTOK_BUSINESS_CLIENT_ID / TIKTOK_BUSINESS_CLIENT_SECRET
YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET
X_API_KEY / X_API_SECRET
PINTEREST_CLIENT_ID / PINTEREST_CLIENT_SECRET
LINKEDIN_CLIENT_ID / LINKEDIN_CLIENT_SECRET
```

Diese Liste ist identisch, ob man Postiz nimmt oder selbst schreibt.
**Selbst bauen erspart keinen einzigen dieser Anträge** und kostet
zusätzlich die Wartung, wenn eine Plattform ihre API ändert — was
laufend passiert. Postiz hat dafür eine Gemeinschaft; ein Eigenbau hat
niemanden.

**Fazit:** Selbst bauen lohnt nur als Lernprojekt, nicht als Lösung.

---

## Was die Entscheidung wirklich kostet

| | Metricool bezahlen | Postiz selbst hosten |
|---|---|---|
| Geld | Abo | Server (~5–10 €/Monat) |
| Einrichtung | keine | Docker, Domain, HTTPS |
| Plattform-Anträge | **keine** | **für jeden Kanal einzeln** |
| Wartung bei API-Änderungen | Metricool | du |
| Beitragslimit | ja, das ist dein Problem | **keins** |
| Zugangsdaten | bei Metricool | bei dir |

**Der ehrliche Vergleich ist nicht „kostenlos gegen Abo", sondern
„Geld gegen Zeit und Genehmigungen".** Metricool verkauft im Kern
genau das, was Postiz nicht mitliefert: fertige, genehmigte
Plattform-Zugänge.

---

## Empfehlung

**Postiz, selbst gehostet — aber schrittweise, nicht auf einmal.**

Die Reihenfolge folgt der Schwierigkeit der Genehmigung, nicht der
Wichtigkeit des Kanals:

1. **Zuerst die offenen Kanäle.** Mastodon, Bluesky, Telegram,
   Discord und WordPress brauchen keine Freigabe — nur einen Token.
   Damit steht das System und man sieht, ob es trägt.
2. **Dann Meta** (Instagram, Facebook, Threads). Ein App-Review ist
   nötig, aber es ist der Kanal, der für Homeeins zählt.
3. **Dann TikTok und YouTube**, beide mit eigenem Antrag.
4. **X zuletzt oder gar nicht** — die API ist kostenpflichtig, und für
   einen Möbelshop ist der Kanal ohnehin zweitrangig.

**Metricool währenddessen weiterlaufen lassen.** Erst abschalten, wenn
Postiz nachweislich für die wichtigsten Kanäle postet — nicht vorher.

**Und die Regel aus `CLAUDE.md` gilt hier besonders:** Alle diese
Schlüssel gehören in GitHub Secrets oder in die Serverumgebung, nicht
ins Repository und nicht in den Chat.

---

## Die Grenze dieser Recherche

Von hier aus **gemessen**: Sternzahlen, Lizenzen, Commit-Daten,
Anbieterverzeichnisse, benötigte Umgebungsvariablen — alles aus den
geklonten Repositories selbst.

Von hier aus **nicht prüfbar**, weil die Umgebung nur GitHub, PyPI und
npm erreicht:

- **Wie schwer die Genehmigungen tatsächlich sind.** Meta, TikTok und
  X ändern ihre Bedingungen laufend. Ob ein kleiner Händler ohne
  Reichweite die Instagram-Veröffentlichungsrechte bekommt, steht in
  Metas eigenen Unterlagen, nicht auf GitHub.
- **Was die X-API heute kostet.** Preise ändern sich; jede Zahl aus
  meinem Gedächtnis wäre geraten.
- **Ob Postiz im Betrieb hält.** 35.410 Sterne sind ein Signal, kein
  Beweis. Das zeigt erst ein Testlauf.

Diese drei Punkte gehören auf die Plattformseiten selbst nachgesehen,
bevor Geld oder Zeit fließt.
