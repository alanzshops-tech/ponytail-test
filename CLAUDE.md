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
| YouTube-Transkripte | youtube-transcript-api | `scripts/videotext.py` |

Berichte liegen als Markdown an der Wurzel: `WERKZEUGE.md`,
`PRUEFSTAND.md`, `GESAMTSCAN.md`, `AUSBAU.md`, `KAUFPROBE.md`,
`MARGE.md`, `NISCHEN.md`, `TRENDS.md`.

## Offene Punkte

- **`SHOPIFY_CLI_THEME_TOKEN` fehlt.** Ohne ihn kein `shopify theme
  pull/push`, kein `theme check`, keine echte Versionsverwaltung des
  Themes. Anleitung in `WERKZEUGE.md`.
- **Judge.me enthält erfundene Bewertungen.** Die Sterne-Metafelder auf
  fünf Produkten sind gelöscht, die App liefert weiter ein
  `aggregateRating`. Nur im Adminbereich der App zu bereinigen.
- **Währungsformat** steht auf `€{{amount}}`; deutsche Schreibweise wäre
  `{{amount}} €`. Shop-Einstellung, nicht Theme.
- **Praxis-Note 58 auf 30 von 34 Seiten** — eine gemeinsame Ursache,
  vermutlich in den App-Einbindungen. Noch nicht belegt.

## Wenn du hier neu bist

Lies `WERKZEUGE.md`, dann `GESAMTSCAN.md`. Danach weißt du, was gemessen
ist und was noch Vermutung. Frag nicht nach dem, was in diesen beiden
Dateien steht.
