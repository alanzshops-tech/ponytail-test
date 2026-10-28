# Design und Conversion — Grundlagen für den Umbau

Stand 14.08.2026 · Auslöser: Auftrag „Weltklasse-Shop mit atemberaubendem
Design, umgesetzt in der Sicherheitskopie, Theme darf komplett
umgeschrieben werden"

**Vor jeder Design-Änderung zuerst hier lesen.** Diese Datei ersetzt das
Neu-Recherchieren.

---

## 1. Was ich am Shop tatsächlich gesehen habe

Erstmals am 14.08.2026 die echten Screenshots angesehen
(`bilder/startseite-desktop.jpg`, `bilder/startseite-mobil.jpg`, Stand
13.08.2026 17:39). Acht konkrete Befunde, nach Schwere sortiert:

| # | Befund | Warum es zählt |
|---|---|---|
| 1 | **Hero-Text kaum lesbar.** Heller Text auf hellem, unruhigem Wohnzimmerfoto; die Unterzeile verschwindet fast; beide Buttons sind Umriss-Buttons ohne Füllung und auf dem Handy praktisch unsichtbar. | Trifft die Stelle, die jeder Besucher zuerst sieht |
| 2 | **Drei schwebende Widgets überlagern sich** auf dem Handy: „Vertrag widerrufen" (blaue Pille links), Chat-Knopf, Trust-Siegel. Sie verdecken Hero und Vertrauenszeile. | Verdeckt Inhalt, wirkt unfertig |
| 3 | **Zehn Hauptmenüpunkte**, Umbruch auf zwei Zeilen — bei 146 Produkten. | Auswahllähmung, kein klarer Einstieg |
| 4 | **Produkttitel sprengen die Kacheln.** „Schuhbank mit Sitzpolster & Stauraum – Massive Optik, 110 kg belastbar, perfekt für Flur & Diele" als Kachel-Titel. | Text dominiert das Bild, Raster wird unruhig |
| 5 | **Uneinheitliche Bildsprache im selben Raster:** Lifestyle-Fotos neben freigestellten Weißbildern neben einer **Infografik** (Hundebett mit Maßangaben). | Wirkt zusammengewürfelt statt kuratiert |
| 6 | **Währungsformat `€99,00`** statt deutsch `99,00 €`. | Steht seit Tagen offen in `CLAUDE.md` |
| 7 | **Zahlungs-Icons doppelt** (Seitenmitte und Fußzeile). | Wiederholung ohne Nutzen |
| 8 | **Emoji als Vertrauens-Icons** (🚚 ⏱ 📦 💳 💬). | Wirkt improvisiert, nicht hochwertig |

### Der wichtigste methodische Punkt

**Befund 1 taucht im Prüfstand nicht auf.** axe-core meldet nur ein
Judge.me-Dropdown als Kontrastproblem. Grund: axe-core kann Text über
einem *Bild* nicht bewerten, weil es den effektiven Hintergrund nicht
berechnen kann. Der auffälligste Fehler der Seite ist genau der, den das
vorhandene Messgerät prinzipbedingt nicht sieht.

→ Deshalb `scripts/kontrast.py`: liest die Pixel hinter dem Text aus dem
Screenshot und rechnet den WCAG-Wert aus. Nach dem Grundsatz „Wo ein
Messgerät fehlt, wird eins gebaut".

---

## 2. Conversion — was die Zahlen hergeben

| Kennzahl | Wert |
|---|---|
| Durchschnittliche E-Commerce-Conversion | **2,5 %** |
| Spitzenfeld | **5,5 %** — bei gleichem Traffic doppelter Umsatz |
| Trefferquote von A/B-Tests (127.000 Experimente, Optimizely) | nur **~12 %** der Ideen gewinnen messbar |
| Firmen mit systematischem Testen (Harvard Business School) | **30–100 %** Verbesserung im ersten Jahr |
| Kumulierte Jahresverbesserung durch strukturierte Programme | **25–40 %**, aus vielen 5–15-%-Schritten |

### Die entscheidende Einschränkung für genau diesen Shop

**Alle Conversion-Optimierung setzt Traffic voraus.** Bei praktisch null
Sitzungen lässt sich nichts testen, nichts messen, nichts iterieren — die
Stichprobe fehlt (siehe `scripts/stichprobe.py`, das genau das ausrechnet).

Daraus folgt die Arbeitsweise für diesen Umbau: **keine Hypothesen testen,
sondern belegte Voreinstellungen anwenden.** Also das nehmen, was in
großen Stichproben bei anderen zuverlässig funktioniert, statt hier
herumzuprobieren. Sobald Traffic da ist, kehrt sich das um.

Und die zweite Konsequenz, unbequem aber wichtig: Die Quellen sind
einhellig, dass die großen Gewinne **nicht** aus Knopffarben und
Schriftgrößen kommen, sondern aus dem Beseitigen von Reibung an konkreten
Entscheidungspunkten. Ein schöneres Design macht die Besucher besser, die
kommen — es holt keine.

---

## 3. Hero-Bereich — die Anatomie, die funktioniert

Der Hero muss drei Fragen in Sekunden beantworten: **Worum geht es hier?
Warum sollte mich das interessieren? Was soll ich tun?**

Bestandteile:
- **Eine** Überschrift mit *einem* Nutzenversprechen
- Unterzeile, die erklärt, warum es zählt
- Bild, das emotional trägt — aber den Text nicht schluckt
- **CTA mit kontrastierender Füllfarbe**, nicht als Umriss
- Ladezeit unter 3 Sekunden
- **Zuerst fürs Handy entwerfen**, dann für Desktop

Der aktuelle Hero verstößt gegen Punkt 4 (Umriss-Buttons) und Punkt 3
(Bild schluckt den Text) gleichzeitig.

---

## 4. Visuelles System — „stiller Luxus" statt Effekthascherei

Aus der Recherche zu hochwertigem E-Commerce-Design 2026:

### Farbe
- **Höchstens vier Farben.** Ein dunkler Anker, ein warmes Off-White, ein
  Akzent, eine Textfarbe.
- **Kein Reinweiß.** 2026 geht der Standard zu leicht warmem Off-White —
  weniger Blendung, höhere wahrgenommene Qualität. Pantones Farbe des
  Jahres „Cloud Dancer" steht genau dafür.
- **Kein Reinschwarz für Text.** Dunkelgrau (~`#2E2E2E`) wirkt weicher und
  liest sich besser als `#000`.
- Belegte Werte aus den Quellen: Onyx `#0A0A0A` als Anker, warmes Ivory
  `#F4EADE` für editorialen Weißraum, Gold zwischen `#C69B3C` und
  `#D4AF37`, warme Neutrale `#D6CFB5` / `#C19066`.

### Typografie und Raum
- **Serifen für Überschriften**, großzügiger Weißraum — das ist der
  stärkste einzelne Hebel für „hochwertig".
- Klare Größenskala statt zufälliger Werte.
- Luft zwischen den Abschnitten. Der aktuelle Shop ist gleichmäßig eng.

### Was daraus für Homeeins folgt
Der Shop verkauft Wohnen und Deko. Die einzige Kategorie mit belegter
Nachfrage (siehe `GELDVERDIENEN.md`) sind **verschenkbare Wohn-Accessoires
zwischen 30 und 130 €**. Für genau dieses Segment ist „stiller Luxus" die
passende Anmutung — nicht Rabatt-Optik, nicht Technik-Look.

---

## 5. Werkzeuge — was da ist, was fehlt

| Werkzeug | Zustand |
|---|---|
| Playwright, axe-core, Pillow, Lighthouse, chrome-devtools | **vorhanden** |
| Shopify Theme-Prüfer (`validate_theme_codeblocks`) | **vorhanden** |
| **Cloudinary** (Bilder erzeugen, freistellen, vereinheitlichen) | **verbunden, nie benutzt** — passt zu Befund 5 |
| **Canva** | verbunden, **nicht freigeschaltet** — braucht Autorisierung durch den Nutzer |
| `shopify theme pull/push` (ganzes Theme als Dateien, mit Git-Verlauf) | **blockiert**, `SHOPIFY_CLI_THEME_TOKEN` fehlt |
| Theme-Dateien über Admin-API lesen und schreiben | **funktioniert**, nachgewiesen 14.08.2026 |
| Kontrastmesser für Text über Bild | **fehlt, wird gebaut** |

### Wie ohne Theme-Token gearbeitet wird
Lesen über `theme(id:…){ files(filenames:[…]) }`, Schreiben über
`themeFilesUpsert`. **Schreiben funktioniert nur in unveröffentlichte
Themes** — Shopify blockiert Schreibzugriff auf das Live-Theme
serverseitig, unabhängig von jeder Freigabe. `themePublish` ist für dieses
Werkzeug dauerhaft gesperrt; veröffentlichen kann nur ein Mensch im
Adminbereich.

---

## 6. Regeln, die auch hier gelten

Der Nutzer hat am 14.08.2026 ausdrücklich erlaubt, **in der Arbeitskopie**
Dawns Dateien umzuschreiben. Das hebt Regel 2 aus `CLAUDE.md` für diese
Kopie auf — **nicht** für das Live-Theme.

Preis dieser Freigabe, einmal festgehalten: Sobald Dawns Dateien verändert
sind, kommen Shopify-Updates nicht mehr sauber an. Bei 43 von 52
byte-identischen Abschnitten ist das der Verlust des laut `CLAUDE.md`
wertvollsten technischen Guts. In einer Kopie ist das folgenlos — beim
Veröffentlichen wird es real.

**Unverändert gültig:** keine Dark Patterns. Keine erfundene Knappheit,
keine Countdown-Zähler, keine Streichpreise ohne echten Vorpreis, keine
Bewertungen ohne Käufer. Das ist EU-Recht (Omnibus, § 5b UWG), nicht
Geschmackssache — und es gilt auch für ein „Weltklasse-Design".

**Nicht in die Sicherungen schreiben.** „Sicherung Live 09.08.2026 – Stand
vor Umbau" (`182664724803`) und „Sicherung 08" (`182681403715`) sind
Rückfallpunkte. Wer darin arbeitet, zerstört ihren Zweck.

---

## Quellen

Conversion-Benchmarks und A/B-Trefferquoten:
[DTC Pages](https://www.dtcpages.com/blog/ecommerce-conversion-rate-benchmarks-2026),
[Growth Engines](https://growth-engines.com/insights/ecommerce/ecommerce-a-b-testing-the-data-driven-guide-to-higher-conversions),
[Digital Applied](https://www.digitalapplied.com/blog/conversion-rate-optimization-2026-ab-testing-guide),
[VWO](https://vwo.com/blog/ecommerce-ab-testing/) ·
Hero-Anatomie:
[SplitBase](https://splitbase.com/blog/hero-section),
[Omniconvert](https://www.omniconvert.com/blog/hero-section-examples/),
[Shopify](https://www.shopify.com/blog/16480796-how-to-create-beautiful-and-persuasive-hero-images-for-your-online-store),
[Nudge](https://www.nudgenow.com/blogs/web-design-hero-section-best-practices) ·
Farbe und Typografie:
[Zoviz](https://zoviz.com/blog/luxury-brand-colors-meanings),
[Lounge Lizard](https://www.loungelizard.com/blog/web-design-color-trends/),
[Superhero Design](https://superherodesign.co/6-unique-color-palettes-for-trendsetting-branding-in-2026/),
[Muffin Group](https://muffingroup.com/blog/luxury-color-palette/)
