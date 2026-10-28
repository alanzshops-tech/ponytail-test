# Social Media — was in Metricool tatsächlich läuft

Stand 13.08.2026, per `mcp__Metricool__getScheduledPosts` live abgefragt.

**Warum diese Datei existiert:** Metricool-Aktionen (Posts einplanen,
veröffentlichen) hinterlassen keine Spur im Git. Jede neue Sitzung startet
ohne dieses Wissen — und hätte ohne die Live-Abfrage vom 13.08.2026 munter
Dutzende Posts doppelt eingeplant, weil `TRAFFIC.md` (selbe Sitzung, davor
geschrieben) fälschlich behauptete, die 17/19 Reels seien "bisher nicht
veröffentlicht" und Pinterest müsse "neu aufgebaut" werden. Beides war
falsch. **Vor jeder neuen Social-Media-Planung zuerst hier nachsehen, dann
trotzdem live mit `getScheduledPosts` gegenprüfen** — diese Datei ist ein
Schnappschuss, kein Ersatz für die Live-Abfrage, weil sich der Kalender
seit dem Schreiben verändert haben kann.

## Was verbunden ist

Metricool-Brand "Homeeins" (id 6583241), erreichbar über die
`mcp__Metricool__*`-Tools dieser Sitzung. Verbundene echte Konten:
Facebook, Instagram (homeeins.de), TikTok (homeeins.de), YouTube,
Pinterest (homeeins), Bluesky (homeeins.bsky.social), LinkedIn, Google
Business Profile, Twitch.

## Was läuft

Erstellt ab 07./08.08.2026 (`creationDate` der frühesten Posts), mit
Publikationsdaten von 08.08.2026 bis mindestens 22.09.2026 durchgehend
belegt — vermutlich noch weiter, nicht bis zum Ende geprüft. Über 110
Posts insgesamt, verteilt auf:

- **Facebook + Instagram** (gemeinsam, "POST"): Karussell aus 4 Produktfotos,
  langer Text mit Frage am Ende, ~alle 1-2 Tage, 11:00 Uhr.
- **Instagram Reel**: einzelne Reels aus `reels.config.json` extra als
  "REEL"-Typ eingeplant (nicht nur über den FB/IG-Post-Kanal).
- **Pinterest**: ein Pin pro Produkt, 20:00 Uhr, eigenes Board
  (boardId 1072490167452344718), inkl. Pins zu den beiden
  Hundemöbel-Ratgebern (Blogartikel als `pinLink`).
- **TikTok**: die gerenderten `.mp4` aus dem Reels-Release, 18:00 Uhr,
  kurzer Hook-Text + Hashtags.
- **YouTube Shorts**: dieselben `.mp4`, 16:00 Uhr, mit Produktlink im
  Beschreibungstext, `#shorts`-Tag.
- **Bluesky**: kurzer Text + ein Bild, 10:00 Uhr.
- **LinkedIn**: vereinzelt, B2B-Winkel (Homeoffice-Fürsorgepflicht beim
  Bürostuhl, Ordnung im Homeoffice) — als Entwurf (`draft: true`), also
  noch nicht automatisch live.

Bereits **veröffentlicht** (bestätigt mit echten Post-URLs, Auswahl):
- Facebook/Instagram: Rattan-Sonnenliege, Loungeset, Samt-Sessel (2×),
  Gartentisch, Schuhbank
- Pinterest: Samt-Sessel, Rattan-Sonnenliege, Waschmaschinenschrank,
  Couchtisch, Hundesofa
- TikTok: Samt-Sessel, Waschmaschinenschrank
- YouTube Shorts: Samt-Sessel, Waschmaschinenschrank, Rattan-Sonnenliege
- Bluesky: Samt-Sessel, Waschmaschinenschrank, Hundesofa

Der Rest steht mit `status: PENDING` im Kalender und wird automatisch
veröffentlicht (`autoPublish: true`), sobald die Uhrzeit erreicht ist —
das braucht kein manuelles Zutun mehr.

## Deckung der 19 `reels.config.json`-Produkte (Stand 13.08.2026)

Geprüft gegen Preis- und Textmarker in den abgefragten Zeitfenstern
(19.07.–13.08., 13.08.–20.08., 20.08.–05.09., 05.09.–05.10.). Kein
Skript-Abgleich, sondern manuelle Zuordnung — **vor dem nächsten Schritt
mit einer gezielten `getScheduledPosts`-Abfrage pro fehlendem Produkt
gegenprüfen, nicht blind auf diese Tabelle verlassen.**

| Produkt | FB/IG | Pinterest | TikTok | YouTube | Bluesky |
|---|---|---|---|---|---|
| samt-sessel | ✅ | ✅ | ✅ | ✅ | ✅ |
| rattan-sonnenliege | ✅ | ✅ | geplant | ✅ | — |
| waschmaschinenschrank | geplant | ✅ | ✅ | ✅ | — |
| hundesofa | geplant | ✅ | geplant | geplant | ✅ |
| couchtisch | geplant | ✅ | geplant | geplant | — |
| schuhbank | ✅ | geplant | — | geplant | geplant |
| weinregal | geplant | geplant | geplant | geplant | geplant |
| gewichtsdecke | geplant | geplant | geplant | geplant | geplant |
| feuerschale | geplant | geplant | geplant | geplant | geplant |
| buerostuhl | — | geplant | geplant | geplant | geplant |
| kratzbaum | geplant | — | geplant | — | geplant |
| hundebett-95 | — | geplant | — | — | — |
| hundebett-xxl | — | geplant | — | — | — |
| haustiertreppe | geplant | geplant | — | — | — |
| hundebett-klein | — | geplant(?) | — | — | — |
| **rattan-ecksofa** | ? | ? | — | — | — |
| **sitzbank-stauraum** | — | — | — | — | — |
| **sitzhocker-38** | — | — | — | — | — |
| **taschenlampe** | — | — | — | — | — |

**Einschätzung, nicht gemessen:** Die vier fett markierten Produkte sind
die drei jüngsten Neuanlagen (Commit "Drei neue Produkte angelegt",
09.08.2026, nach 20:22 Uhr) plus die LED-Taschenlampe (13.08.2026) — beide
nach den Zeitpunkten, an denen der Kalender laut `creationDate` gebaut
wurde (07./08.08., mit einer Nachtragswelle am 09.08. 19 Uhr, die aber vor
dem 20:22-Uhr-Commit lag). Wahrscheinlichste Erklärung: für diese vier
gibt es noch **keine** eingeplanten Posts, weil sie zum Zeitpunkt der
Kalender-Erstellung noch nicht existierten. Nicht mit einer gezielten
Abfrage bestätigt — das ist der nächste Schritt, kein Ergebnis.

## Offene Fragen

- **Wer hat das aufgesetzt?** Vermutlich eine frühere Sitzung dieses
  Agenten (erkennbar an `creatorUserMail: alanz.shops@gmail.com`, aber
  kein Hinweis, ob Mensch oder Agent über den Metricool-Login). Nicht
  geklärt.
- **Bis wann läuft der Kalender?** Zuletzt geprüft bis 05.10.2026, letzter
  gefundener Post 22.09.2026. Nicht abschließend geprüft, ob danach noch
  etwas eingeplant ist.

## Nachtrag 13.08.2026 (abends) — zwei neue Pinterest-Pins

Zu den zwei neuen Ratgebern (`buerostuhl-ergonomie-worauf-es-ankommt`,
`kratzbaum-groesse-material-standort`, siehe `TRAFFIC.md`) je ein Pin
über `mcp__Metricool__createScheduledPost` eingeplant, gleiches Board
(`1072490167452344718`) wie alle bisherigen Pins:

| Pin | Datum | Bild |
|---|---|---|
| Kratzbaum-Ratgeber | 16.08.2026, 19:00 | Produktfoto kompakter Kratzbaum |
| Bürostuhl-Ratgeber | 19.08.2026, 19:00 | Produktfoto Bürostuhl |

Bewusst nicht am 17.08. eingeplant — da lag schon ein Pinterest-Pin
direkt auf das Bürostuhl-Produkt (`buerostuhl-premium-relaxfunktion-
135-grad`, 20:00 Uhr). Der Ratgeber-Pin verlinkt stattdessen auf den
Blogartikel, nicht direkt aufs Produkt — ergänzend, nicht doppelt.

**Wichtig für nächste Sitzungen:** `createScheduledPost` verlangt sowohl
den Top-Level-Parameter `date` als auch `info.publicationDate` (gleicher
Zeitpunkt, zweimal) — ohne `info.publicationDate` schlägt der Aufruf
fehl. `info.providers` darf nur Netzwerke enthalten, für die auch
`...Data` mitgeschickt wird (z. B. kein `instagramData`, wenn nur
`pinterest` in `providers` steht) — sonst Fehler „networkData contains
data for network X not listed in providers".
