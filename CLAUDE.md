# Arbeitsregeln für Homeeins

Diese Datei ist das Erste, was ein Agent in diesem Repository liest.
Sie steht hier, weil jede ernstzunehmende Anleitung zur Arbeit mit
Coding-Agenten dieselbe Empfehlung gibt: Regeln und Gefahrenzonen
gehören an die Wurzel des Projekts, nicht in den Kopf einer einzelnen
Sitzung. Jede Regel unten ist bezahlt — mit einem Fehler, der schon
passiert ist.

## Der Laden

**Homeeins**, www.homeeins.de, Shopify, Theme **Dawn 15.4.1**.
Alan Lorenz GbR, Bochum. **Kleinunternehmer nach § 19 UStG** — es fällt
keine Umsatzsteuer an. Es gibt kein Netto und kein Brutto, nur einen
Preis.

Stand August 2026: 146 Produkte, **sieben Bestellungen in drei Jahren**,
**null im Jahr 2026**, null abgebrochene Warenkörbe. Die Kasse
funktioniert (nachgemessen). Das Problem ist nicht, dass niemand kaufen
kann — es kommt niemand.

## Nicht verhandelbar

1. **Nie ins veröffentlichte Theme schreiben.** Immer Kopie, dann
   veröffentlicht ein Mensch. Shopify sperrt das ohnehin, verlass dich
   nicht darauf.
2. **Nie in Dawns Dateien schreiben.** 43 von 52 Abschnitten sind
   byte-identisch mit Shopifys Original. Diese Updatefähigkeit ist das
   wertvollste technische Gut des Shops. Reihenfolge: erst Dawns
   Einstellungen, dann Dawns Bausteine, und nur wenn beides
   nachweislich nicht reicht, eigener Code in `custom-liquid`.
3. **Keine Dark Patterns.** Keine ablaufenden Zähler, keine erfundene
   Knappheit, keine „17 Leute sehen sich das an", keine
   Fantasie-Streichpreise, keine Bewertung ohne Käufer. In der EU
   verboten (Omnibus-Richtlinie, § 5b UWG; bei Bewertungen ohne
   Abwägung, Anhang zu § 3 Abs. 3 Nr. 23b/23c). Am 9.8.2026 wurden
   genau solche Inhalte aus diesem Shop entfernt — sie kommen nicht in
   neuer Verpackung zurück.
4. **Keine Zugangsdaten in den Chat, nicht im Repository, nicht in
   Kassetten.** Schlüssel gehören in GitHub Secrets. `aufzeichnen.py`
   löscht jede Kassette, die noch etwas enthält.
5. **Entwickeln und pushen nur auf dem zugewiesenen Branch.**

## Arbeitsweise

**Nichts behaupten, was nicht gemessen wurde.** Wo ein Messgerät fehlt,
wird eins gebaut. Das ist keine Attitüde, das ist die Lehre aus einem
Tag mit acht Irrtümern — sechs über die CJ-API, zwei über den eigenen
Shop. Jeder davon hatte einen grünen Test daneben, weil die Tests
handgeschriebene Attrappen prüften statt der Wirklichkeit.

**Der Runner ist Augen und Netz.** Die Arbeitsumgebung erreicht nur
GitHub, PyPI und npm — nicht homeeins.de, nicht YouTube, nicht die
CJ-API. Alles Externe läuft über GitHub Actions, das Ergebnis kommt als
Commit zurück.

**Ein Selektor, der zu viel fängt, ist kein Messgerät.** Schon dreimal
passiert: „Ausverkauft" im Theme-Template, „Rechnung" in
„Rechnungsadresse", Judge.mes Einstellungs-Script statt des Widgets.
Jede Textsuche gegen einen bekannten Positiv- **und** Negativfall
prüfen.

**Eine Messung ohne Bezugsrahmen ist keine.** „28 Kacheln" war falsch,
weil über die ganze Seite gezählt wurde. „0 Preise" war falsch, weil das
Muster nur nachgestellte Währungszeichen fand.

**Leeres Ergebnis ≠ kein Problem.** Vor „nichts gefunden" immer eine
Probe mit einem Begriff, der treffen *muss*.

**Shopifys `collectionUpdate`-Feld `seo` ersetzt, statt zu ergänzen.**
Wer nur `seo.title` mitschickt, löscht `seo.description` — passiert am
13.08.2026 bei der „dekoration"-Kollektion, sofort bemerkt und
zurückgeschrieben, weil danach nachgeprüft wurde. Bei jeder
`collectionUpdate`/`productUpdate`-Mutation mit einem `seo`-Feld immer
beide Unterfelder mitschicken, auch wenn nur eines geändert werden soll.

## Werkzeuge

| Zweck | Werkzeug | Datei |
|---|---|---|
| Fotos + Browserwerte | Playwright | `scripts/webcheck.py` |
| Barrierefreiheit, Lesbarkeit, Pixelvergleich | axe-core, Pillow | `scripts/pruefstand.py` |
| Lighthouse über den ganzen Shop | Unlighthouse | `scripts/gesamtscan.py` |
| Kaufweg bis zur Kasse | Playwright | `scripts/kaufprobe.py` |
| Stichprobengröße für A/B-Tests | eigen | `scripts/stichprobe.py` |
| Echte API-Antworten aufzeichnen | VCR.py | `scripts/aufzeichnen.py` |
| Nachfrage und Saison | pytrends | `scripts/trends.py` |
| Lieferantenkatalog | CJ API | `scripts/cj.py`, `scripts/marge.py` |
| Fremde Modelle rufen | OpenRouter | `scripts/openrouter.py` |

Berichte liegen als Markdown an der Wurzel: `WERKZEUGE.md`,
`PRUEFSTAND.md`, `GESAMTSCAN.md`, `AUSBAU.md`, `KAUFPROBE.md`,
`MARGE.md`, `NISCHEN.md`, `TRENDS.md`, `PRODUKTBILDER.md`, `TRAFFIC.md`,
`SOCIAL.md`, `VERTRIEBSKANAELE.md`, `GELDVERDIENEN.md`, `DESIGN.md`.

`GELDVERDIENEN.md` — **vor jeder Sortiments- oder Strategiefrage zuerst
hier lesen.** Enthält den am 14.08.2026 erstmals abgefragten Befund aus den
sieben echten Bestellungen: **alle sieben waren verschenkbare Wohn-Deko
zwischen 30 und 130 €, und alle sieben Artikel sind heute nicht mehr im
Sortiment** (mit Positivprobe gegengeprüft). Die heutigen 146 Produkte
stehen in Kategorien mit null Bestellungen in drei Jahren. Dazu die
Marktrecherche zu Dropshipping-Margen, Eigenmarke und
Dienstleistungssätzen — inklusive des rechtlichen Zauns, dass
**Kalt-E-Mails an Unternehmen nach § 7 UWG abmahnfähig** sind
(1.500–3.000 € pro Fall), telefonische B2B-Akquise dagegen zulässig.

`SOCIAL.md` — **vor jeder Social-Media-Aktion zuerst hier lesen, dann
live mit `mcp__Metricool__getScheduledPosts` gegenprüfen.** Es läuft
bereits ein aktiver Metricool-Kalender auf den echten Konten (Facebook,
Instagram, TikTok, YouTube, Pinterest, Bluesky, LinkedIn) — mehrfach in
dieser Sitzung fälschlich als "nicht vorhanden" angenommen, weil
Metricool-Aktionen keine Spur im Git hinterlassen. Diese Datei ist der
Ausgleich dafür, aber nur ein Schnappschuss vom 13.08.2026.

`VERTRIEBSKANAELE.md` — derselbe blinde Fleck wie bei `SOCIAL.md`, nur
für Shopifys eigene Sales Channels statt Metricool: Google & YouTube,
Microsoft (Bing), Amazon, TikTok, Pinterest, Instagram Shop-AI sind
längst verbunden und Produkte dorthin veröffentlicht. **Vor dem
Vorschlagen "Google Shopping einrichten" o. ä. zuerst hier nachsehen.**

`TRAFFIC.md` — externe Recherche (Stand 13.08.2026) zu allen
Traffic-Strategien, priorisiert P0–P3. **Achtung:** Der Abschnitt zu den
Reels und zu Pinterest ging von falschen Annahmen aus (siehe
`SOCIAL.md`) — vor dem Umsetzen dort gegenprüfen, nicht blind befolgen.
Die 10 unbeklickten Rankings (SEO-Snippets) bleiben davon unberührt und
offen. Vor jeder neuen Marketing-Idee zuerst dort nachsehen, nicht neu
recherchieren.

`DESIGN.md` — **vor jeder Design- oder Theme-Änderung zuerst hier
lesen.** Die acht konkreten Befunde aus den echten Screenshots
(14.08.2026), Conversion-Benchmarks, Farb- und Typografiesystem, und der
methodische Kernpunkt: **axe-core kann Text über einem Bild nicht
bewerten** — der auffälligste Fehler der Startseite (unlesbarer Hero)
fehlt deshalb im Prüfstand. Dafür gibt es `scripts/kontrast.py`.
Ausserdem festgehalten, welche Werkzeuge verbunden, ungenutzt oder
blockiert sind.

`PRODUKTBILDER.md` — externe Recherche (Stand 13.08.2026) zu
Produktbildern, die messbar besser verkaufen: wie viele Bilder,
welche Bildarten, Möbel-/Haustier-spezifische Regeln, Mobil-Zoom,
Ladezeit, Alt-Text/SEO, UGC-Fotos, und die neue EU-AI-Act-Kennzeichnung
für KI-Bilder. Vor jeder Änderung an Produktbildern zuerst dort
nachsehen, nicht neu recherchieren.

## MCP-Server (`.mcp.json`)

**shopify-dev** (`@shopify/dev-mcp`, ISC, v1.14.4). Im Paket
nachgesehen, nicht aus einem Blog übernommen — es bringt wirklich
`learn_shopify_api`, `search_docs_chunks`, `validate_graphql_codeblocks`,
`validate_theme` und `validate_theme_codeblocks` mit. Ein
`introspect_admin_schema`, das mehrere Anleitungen nennen, ist **nicht**
enthalten.

`LIQUID_VALIDATION_MODE=partial` ist gesetzt. Damit prüft
`validate_theme_codeblocks` einzelne Liquid-Schnipsel gegen Theme Check
— also genau das, was in `custom-liquid`-Abschnitten geschrieben wird,
ohne dass das ganze Theme lokal liegen muss. Sobald der Theme-Token da
ist, prüft `validate_theme` das ganze Verzeichnis auf einmal.

**chrome-devtools** (`chrome-devtools-mcp`, Apache-2.0, v1.6.0). Fährt
einen echten Chrome, nimmt Performance-Traces auf und liest die Konsole.
Damit lässt sich die Frage „warum steht die Praxis-Note auf 58" direkt
beantworten, statt sie aus Lighthouse-Zahlen zu erschließen.

Beide sind lesend und brauchen keine Ladenzugangsdaten.

## Offene Punkte

- **`SHOPIFY_CLI_THEME_TOKEN` fehlt.** Ohne ihn kein `shopify theme
  pull/push`, kein `theme check`, keine echte Versionsverwaltung des
  Themes. Anleitung in `WERKZEUGE.md`.
- **`SHOPIFY_ADMIN_API_TOKEN` fehlt.** Ohne ihn läuft
  `scripts/bestandsautomatik.py` (täglich 06:00 UTC) nicht — schreibt
  nur eine Erklärung in `BESTANDSAUTOMATIK.md`, statt rot zu werden.
  Anleitung in `WERKZEUGE.md`.
- **Judge.me war die Quelle erfundener Bewertungen** (Sterne-Metafelder
  gelöscht, App lieferte weiter `aggregateRating`) — am 13.08.2026
  deaktiviert, live geprüft: keine Sterne mehr. Offener Rest: Der
  Bewertungsblock zeigt seitdem Englisch statt Deutsch (⚪ P3 in
  `AUDIT.md`).
- **Währungsformat** steht auf `€{{amount}}`; deutsche Schreibweise wäre
  `{{amount}} €`. Shop-Einstellung, nicht Theme.
- **Praxis-Note 58 auf 34 von 34 Seiten — Ursache jetzt belegt**
  (13.08.2026, `GESAMTSCAN.md`): "Uses deprecated APIs", "Uses
  third-party cookies" und "Issues im DevTools-Issues-Panel" schlagen auf
  jeder einzelnen Seite fehl, nicht nur auf den meisten. Vermutlich
  App-Einbindungen (Tracking-/Analytics-Skripte) — noch nicht auf eine
  einzelne App zurückgeführt, und drittanbieter-Cookies lassen sich ohne
  Verzicht auf Marketing-Tracking oft gar nicht vermeiden. Die
  Performance-Note (Tempo, Median 62) hat konkretere, eher behebbare
  Funde: ungenutztes JavaScript und render-blockierende Anfragen auf
  allen 34 Seiten.

## Wenn du hier neu bist

Lies `WERKZEUGE.md`, dann `GESAMTSCAN.md`. Danach weißt du, was gemessen
ist und was noch Vermutung. Frag nicht nach dem, was in diesen beiden
Dateien steht.
