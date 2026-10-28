# Marketing-System — eingerichtet am 28.10.2026

Nicht aus einem Blog übernommen: Repos aufgemacht, Zahlen abgelesen,
installiert, Ergebnis nachgemessen.

## Was installiert ist

**`digital-marketing-pro`** (MIT, 913 Sterne, v3.40.0 vom 28.10.2026 —
am Tag der Installation erschienen). Als Claude-Code-Plugin:

```
claude plugin marketplace add indranilbanerjee/neels-plugins
claude plugin install digital-marketing-pro@neels-plugins
```

Nach der Installation gezählt, nicht der Beschreibung geglaubt:
**164 Skills, 24 Agenten, 99 Python-Skripte, 35 Konnektoren**
(Konnektoren standardmäßig aus).

Verworfen: `kostja94/marketing-skills` (1.100 Sterne, MIT, reines
Markdown). Gute zweite Wahl und risikoärmer, weil ohne ausführbaren
Code — aber ohne Agenten und ohne Compliance-Schicht.

## ⚠️ Beides liegt AUSSERHALB des Repositories

| Was | Wo | Überlebt Container-Neustart? |
|---|---|---|
| Plugin | `~/.claude/plugins/cache/neels-plugins/` | **nein** |
| Markenprofil | `~/.claude-marketing/brands/homeeins/` | **nein** |
| Sicherung des Profils | `daten/marketing/dmp-markenprofil.json` | ja |

**Wiederherstellen nach einem Neustart:** die zwei Befehle oben, dann

```
python3 "$PLUGIN/scripts/setup.py" --create-brand "Homeeins"
cp daten/marketing/dmp-markenprofil.json ~/.claude-marketing/brands/homeeins/profile.json
```

## Das Markenprofil

Jeder Skill liest `profile.json`. Es ist **nicht aus Fragen an den
Inhaber** entstanden, sondern aus den gemessenen Dateien dieses
Repositories — `GELDVERDIENEN.md`, `SORTIMENT.md`, `CLAUDE.md`, dazu
Shopify-Analytics. Wo nichts gemessen ist, steht das auch so drin:

- **USP: ausdrücklich als ungelöst eingetragen.** Der Katalog kommt aus
  CJ, dieselben Artikel mit denselben Fotos führen Dutzende Shops.
- **Primärkanal: Pinterest** — eine Suchfläche, auf der ein Pin Monate
  lebt, statt eines Feeds, der nach zwei Tagen vorbei ist.
- **Engpass-Kennzahl: 17 Sitzungen aus organischer Suche in 12 Monaten.**
- **Budget: 0 €**, als harte Vorgabe hinterlegt — damit kein Skill eine
  bezahlte Kampagne vorschlägt.
- **Wettbewerber: leer.** Nicht geraten.

### Die Compliance-Schicht trägt die Zäune dieses Projekts

In `industry.regulation_codes` stehen UWG § 5a/5b, Anhang zu § 3 Abs. 3
Nr. 23b/23c, § 7 UWG, § 19 UStG und § 3a Abs. 5 UStG. In
`brand_voice.avoid_words` stehen „zeitlich begrenzt", „nur noch wenige"
und die anderen Formulierungen, die hier schon zweimal entfernt werden
mussten.

## Nebenbefund bei der Einrichtung: Versandkosten

Beim Ausfüllen des Profils über die Shopify-Versandprofile gemessen:

| Zone | Preis |
|---|---|
| **Deutschland** | **0,00 € — „Kostenloser Versand"** |
| Europa | 14,99 / 34,99 / 69,99 / 119,99 € nach Gewicht |
| Weltweit | 24,99 / 59,99 / 119,99 / 199,99 € |

**„Versandkostenfrei" ohne Zusatz ist damit falsch.** Richtig ist
„Versand innerhalb Deutschlands kostenlos". Die Regel steht in
`industry.compliance_notes`. Zwei bereits eingeplante Beiträge tragen
die unqualifizierte Fassung — der Pin vom 27.10. ist schon raus, der
Beitrag vom 28.10. ist noch änderbar.

## Diese Skills sind Ratschlag, nicht Befehl

Marketing-Playbooks empfehlen routinemäßig Verknappungs-Zähler,
Bewertungen vor dem ersten Käufer und Kalt-E-Mails an Firmen. Alles drei
ist hier verboten. **`CLAUDE.md` schlägt jeden Skill.** Wenn ein Skill
etwas vorschlägt, das hier nicht geht, wird es gemeldet statt ausgeführt.


## Dauer-Agenten (Routines) — Stand 28.10.2026

Die 24 Agenten des Plugins sind Unter-Agenten *innerhalb* einer
Sitzung, keine laufenden Prozesse. Was dauerhaft arbeitet, sind
**Routines** — jede mit genau einem Zuständigkeitsgebiet und einer
eigenen Messlatte.

| Agent | Takt | Gebiet | Messlatte | Connectors |
|---|---|---|---|---|
| **Social-Agent** | Mo/Mi/Fr 08:00 | Beiträge, Pinterest zuerst | Sitzungen je Kanal | **fehlen** |
| **SEO-Agent** | Di 07:41 | nur organische Suche | 17 Sitzungen/Jahr | **fehlen** |
| **Laden-Wache** | Do 07:23 | Rückfälle im Shop | 7 Prüfungen, alle 96 Produkte | **fehlen** |
| Wochen-Check | Mo 08:50 | Bericht an den Inhaber | — | alle 17 |
| GSC-Erinnerung | Mo 08:00 | fragt nach dem GSC-Lauf | — | — |

Jeder der drei neuen Agenten trägt seine Engpass-Kennzahl im Auftrag
und die ausdrückliche Warnung, die Gesamtsitzungen **nicht** als
Erfolg zu lesen — 94 % davon sind die eigenen Messwerkzeuge.

Die **Laden-Wache** prüft sieben Dinge, die hier alle schon einmal
zurückgekommen sind: erfundene Knappheit, Bewertungen ohne Käufer,
ausverkaufte Varianten, leere SEO-Felder, englische Titel und Emojis,
Entwurfsprodukte, falsche Versandaussagen. Mit Pflicht-Positivprobe:
Ein leeres Ergebnis gilt erst als Entwarnung, wenn eine Suche nach
einem Begriff, der treffen *muss*, auch wirklich trifft.

Der **Social-Agent** hat bis Ende Dezember einen festen Schwerpunkt:
Hundemöbel und verschenkbare Deko zwischen 30 und 130 €. Grundlage ist
die Trends-Messung vom 28.10. — „hundebett" steht im November und
Dezember bei 92 gegen 75 im Jahresschnitt.

### ⚠️ Der Grund, warum drei davon nichts bewirken

`create_trigger` antwortet auf den Parameter `connectors`:

```
the connectors parameter is not available for this organization
```

Zweimal versucht, am 22.10. und am 28.10. **Ein Agent ohne Connectors
sieht weder Shopify noch Metricool.** Der Social-Agent ist am 28.10.
um 08:17 gelaufen und konnte nichts tun; so steht er seit dem 22.10.

**Nur ein Mensch kann das beheben:** claude.ai → Routines → Routine
öffnen → Connectors → **Shopify** und **Metricool** anhaken. Drei
Routinen, je zwei Haken.

Alle drei Texte fangen den Fall ab: Fehlen die Connectors, melden sie
das in einem Satz und beenden — statt eine Ersatzhandlung zu erfinden.

## Weitere Skills — ausgewählt, nicht alle genommen

Der Katalog hat mehr; genommen wurden drei, die auf den gemessenen
Engpass zahlen. Sie liegen im claude.ai-Konto und werden über die
Oberfläche installiert, nicht über die CLI (dort sind sie nicht
auffindbar — am 28.10. geprüft).

| Plugin | Warum |
|---|---|
| **SEO Audit** (5 Skills) | `search-console-data-review` passt exakt zum anstehenden GSC-Lauf; nennt Shopify ausdrücklich |
| **Website Copywriting & Positioning** (5) | gegen das ungelöste USP-Problem; erfindet laut eigener Beschreibung nie Testimonials oder Dringlichkeit |
| **Social Media Skills** (106) | `pinterest-seo`, `pinterest-growth`, `pinterest-pin-design`, `tiktok-photo-mode`, `seasonal-and-moment-marketing` |

**Bewusst nicht genommen:**

- *SEO-AEO-GEO Ultimate* (27 Skills) — überschneidet sich fast
  vollständig mit den 164 aus `digital-marketing-pro`. Zwei Bibliotheken
  für dieselbe Aufgabe machen die Auswahl schlechter, nicht besser.
- *Ayrshare* — Social-API, kostet Geld.
- *shopify-ai-toolkit* — sendet laut eigener Beschreibung
  Nutzungsdaten (Abfragen, Code) an shopify.dev, sofern man nicht
  `OPT_OUT_INSTRUMENTATION=true` setzt. Ausserdem auf
  Theme-Entwicklung ausgelegt, und ins veröffentlichte Theme wird hier
  ohnehin nicht geschrieben.

## Bewertungen — was geht und was nicht

**Importierte, erfundene oder gekaufte Bewertungen: nein.** Anhang zu
§ 3 Abs. 3 Nr. 23b/23c UWG, ohne Abwägung verboten. Genau dafür wurde
Judge.me am 22.10.2026 deinstalliert, nachdem die App trotz gelöschter
Sterne weiter `aggregateRating` auslieferte.

**Echte Bewertungen: vorbereitet.** Loox ist installiert und am
22.10.2026 als unauffällig gemessen — es schreibt kein
`aggregateRating` und rendert nichts, solange es nichts gibt. Es fragt
Käufer nach dem Kauf. Es gibt derzeit **null Käufer in 2026**, also
nichts zu fragen. Der erste echte Verkauf löst die erste echte
Bewertung aus; vorher ist jede Bewertung auf dieser Seite eine
Fälschung.

**Was stattdessen Vertrauen schafft, ohne zu lügen:** klare
Lieferzeit, sichtbares Widerrufsrecht, Impressum, Zahlungsarten, echte
Produktmasse — und der Satz, der hier wirklich stimmt:
*Versand innerhalb Deutschlands kostenlos.*

## Reels — die Produktion stand seit August still

**Gemessen am 28.10.2026.** Die komplette Video-Pipeline existiert
schon und war nie benutzt worden.

| | |
|---|---|
| Werkzeug | `.github/workflows/reels.yml` + `reels.config.json` |
| Rendern | FFmpeg auf dem GitHub-Runner, ein Job je Produkt, parallel |
| Vertonung | Piper, deutscher Sprechertext je Produkt |
| Bildebenen | Hook und Preis |
| Ablage | GitHub-Release-Assets → **dauerhafte öffentliche URL** |
| Konfiguriert | **19 Produkte** |
| Gerendert | **19 MP4** im Release `reels-20260809-205221` |

### Der Befund

**`download_count` lag bei allen 19 Dateien auf 0.** Die Videos sind
seit dem 9. August öffentlich abrufbar und wurden **kein einziges Mal
abgerufen** — von niemandem, auch nicht von Metricool.

`SOCIAL.md` hielt am 13.08. fest, ein Großteil der Reels sei „längst
auf TikTok/YouTube Shorts eingeplant oder veröffentlicht". Der
Zählerstand 0 widerspricht dem: Hätte Metricool sie eingeplant, hätte
es sie heruntergeladen (es kopiert jedes Medium auf den eigenen CDN).
**Die Reels waren nie draußen.**

### Die Kette ist jetzt nachgewiesen

GitHub-Release-URL → Metricool → Instagram Reel + TikTok. Belegt, weil
Metricool die MP4 geholt und auf `static.metricool.com` kopiert hat.

| Datum | Reel | Kanäle |
|---|---|---|
| 02.11., 19:00 | Hundebett 95 cm | Instagram Reel + TikTok |
| 05.11., 19:00 | Hundebett XXL mit Erweiterung | Instagram Reel + TikTok |

Preise vorher gegen den Shop geprüft: alle fünf Hunde-Reels stimmen
noch (94,99 / 94,00 / 199,00 / 99,00 / 44,99 €).

### Zwei Dinge, die vor dem Rest zu klären sind

1. **Zwei der 19 Reels zeigen auf Entwurfsprodukte** —
   `sitzbank-stauraum` und `taschenlampe`. Die dürfen nicht raus,
   solange die Produkte auf Entwurf stehen.
2. **Es sind Bildfolgen mit Sprecherstimme, kein gefilmtes Material.**
   Das ist für Produktvideos üblich und erlaubt; eine
   KI-Kennzeichnung nach EU-AI-Act ist zu prüfen, sobald Bilder
   KI-erzeugt sind (hier sind es Produktfotos des Lieferanten).
