# Design-Umbau in der Arbeitskopie

Stand 14.08.2026 · Auftrag: Weltklasse-Design, Theme darf in der Kopie
komplett umgeschrieben werden

**Grundlagen stehen in `DESIGN.md`** — dort die acht Befunde, die
Conversion-Benchmarks und das Farbsystem. Diese Datei ist das Protokoll
der Umsetzung.

---

## Die Arbeitskopie

| | |
|---|---|
| Name | **Design-Umbau Claude 14.08.2026 – Arbeitskopie** |
| ID | `gid://shopify/OnlineStoreTheme/182686056771` |
| Rolle | UNPUBLISHED |
| Vorschau | `https://www.homeeins.de/?preview_theme_id=182686056771` |
| Vorlage | das Live-Theme (`182683926851`), am 14.08.2026 dupliziert |

**Bewusst nicht angefasst:** „Sicherung Live 09.08.2026 – Stand vor
Umbau" (`182664724803`) und „Sicherung 08" (`182681403715`). Das sind
Rückfallpunkte — wer darin arbeitet, zerstört ihren Zweck. Deshalb eine
frische Kopie statt einer der vorhandenen.

---

## Erledigt

### Hero lesbar gemacht (Befund 1)

Die Ursache war nicht *eine* Einstellung, sondern vier, die einzeln
harmlos sind und zusammen den Text verschlucken:

| Einstellung | vorher | nachher | Warum |
|---|---|---|---|
| `image_overlay_opacity` | 20 | **50** | 20 % Abdunklung reichen über einem hellen Foto nicht |
| `image_behavior` | `ambient` | **`none`** | Wanderndes Bild hinter Text: Unruhe, schlechter LCP |
| `button_style_secondary_1` | `true` | **`false`** | Haupt-CTA war ein Umriss-Button und verschwand |
| `button_style_secondary_2` | `true` | `true` | bleibt Umriss — ein Primär-, ein Sekundärknopf |

Datei: `templates/index.json`, geschrieben über `themeFilesUpsert`.
**Gegengeprüft:** MD5 der Quelle `aaf62b9bf5276d73f0534449b207fed4`,
MD5 in Shopify nach dem Schreiben identisch. Keine abgeschnittene
Übertragung.

### Nachgemessen — und die 50 % reichen nicht ganz

Mit dem neuen `scripts/kontrast.py` den **Ausgangszustand** gemessen
(`bilder/startseite-mobil.jpg`, weisser Text, ohne Pixel-Ausschluss, weil
der Hintergrund selbst weiss ist):

| Bereich | schlechtester Pixel | Median | Fläche unter 4,5:1 |
|---|---:|---:|---:|
| Überschrift (y 390–685) | 1,0:1 | 1,8:1 | **92,2 %** |
| Unterzeile (y 725–900) | 1,01:1 | 4,09:1 | **53,0 %** |

Die Überschrift steht auf weisser Marmorwand und weisser Decke — weisser
Text auf Weiss, Kontrast 1,0:1. Das ist kein Geschmacksurteil mehr.

**Was ein Overlay rechnerisch bringt** (weisser Text, weisser Grund):

| Overlay | Hintergrund | Kontrast | grosser Text (3:1) | normaler Text (4,5:1) |
|---:|---|---:|---|---|
| 20 % (Ausgangszustand) | `#CCCCCC` | 1,61:1 | durchgefallen | durchgefallen |
| **50 % (jetzt gesetzt)** | `#808080` | 3,95:1 | **bestanden** | **durchgefallen** |
| 55 % | `#737373` | 4,74:1 | bestanden | bestanden |
| 60 % | `#666666` | 5,74:1 | bestanden | bestanden |

**Korrektur an der eigenen Arbeit:** Die gesetzten 50 % lösen die
Überschrift (`h0`, gilt als grosser Text), **nicht aber die Unterzeile**
(normaler Text, braucht 4,5:1). Stand der Arbeitskopie ist also
„Überschrift repariert, Unterzeile weiterhin durchgefallen".

Der saubere Weg ist nicht, das Overlay pauschal auf 60 % zu ziehen — dann
versinkt das Foto im Grau. Besser ist ein **Verlauf, der nur dort
abdunkelt, wo der Text steht**. Das braucht CSS und kommt in den
Sammel-Durchgang, sobald der Token da ist.

---

### Umgesetzt am 14.08.2026, nach dem Theme-Token

Der Token war bereits im Tresor. Damit lief die richtige Pipeline an:
`theme pull` → lokal bearbeiten → `theme check` → `theme push`.

| Was | Wo |
|---|---|
| Designsystem: warmes Off-White, `#2e2e2e` statt Reinschwarz, Raum-Skala, Serifen | `assets/homeeins-design.css` (neu), eingebunden in `layout/theme.liquid` |
| Farbschemata `background-1` und `background-2` | `config/settings_data.json` |
| Vertrauensbalken mit vier SVG-Icons statt Emoji, doppelte Zahlungs-Icons entfernt | `templates/index.json` |
| Kacheltitel auf zwei Zeilen begrenzt | CSS, `line-clamp` — kürzt nur optisch |
| Hero-Scrim hinter dem Textblock | CSS, `.banner__box` |

### Drei Messrunden, drei Befunde

**Runde 1 — Cookie-Dialog über dem Hero.** Die erste Nachher-Aufnahme war
unbrauchbar, weil ein Zustimmungsdialog genau über dem Messbereich lag.
Eine Messung darauf hätte den Dialog gemessen. `webcheck.py` klickt ihn
jetzt weg (bewusst „Ablehnen" vor „Akzeptieren").

**Runde 2 — falsche Annahme über die Textposition.** Der erste Scrim war
ein Verlauf, unten am dunkelsten, weil `desktop_content_position` auf
`bottom-center` steht. Der Text sitzt aber in der **Mitte** des Banners,
wo der Verlauf noch bei 0,3 lag. Die Rechnung war richtig, die Annahme
darunter falsch. Der Scrim sitzt jetzt hinter `.banner__box` und ist
damit unabhängig von der Textposition.

**Runde 3 — selbst eingebauter Fehler.** Die Typografie-Regel setzte
`color: var(--he-text)` auf alle Überschriften. Damit wurde die
Hero-Überschrift dunkelgrau **auf dunklem Scrim**. Dawns Farbschemata
kennen den Untergrund, eine pauschale Farbregel darüber nicht. Die Regel
setzt jetzt nur noch Schriftschnitt und Rhythmus.

Die Unterzeile ist weiss geblieben und trennt deshalb die Effekte sauber:

| Hero, Handy | Ausgangszustand | nach Scrim |
|---|---:|---:|
| Unterzeile, Median | 4,09:1 | **7,22:1** |
| Unterzeile, Fläche unter 4,5:1 | 53,0 % | **13,1 %** |

Der Scrim wirkt also nachweislich. Die Überschrift war schlecht, weil ich
sie eingefärbt hatte, nicht weil der Scrim zu schwach wäre.

**Runde 4 — der Scrim kam oben nicht an.** Mit `alpha 0.58` blieb die
Überschrift bei Median 3,4:1. Verdacht: Kantenglättung der grossen
Serifenschrift verfälscht die Messung. **Die Empfindlichkeitsprüfung hat
diesen Verdacht widerlegt** — der Wert blieb über alle Ausschluss-Schwellen
von 0 bis 150 flach bei 3,4:1, nur 11–13 % der Pixel sind Buchstaben. Der
Zeilen-Scan zeigte den echten Grund: oben 155 Helligkeit, unten 85. Dawns
eigene Klassen auf `.banner__box` gewinnen. Mit `!important` und
`alpha 0.72` sitzt der Scrim.

### Endstand der Messung

| Hero, Handy | Ausgangszustand | Endstand |
|---|---:|---:|
| **Überschrift** — Median | 1,8:1 | **10,85:1** |
| **Überschrift** — Fläche unter 4,5:1 | 92,2 % | **2,9 %** |
| **Unterzeile** — Median | 4,09:1 | **12,48:1** |
| **Unterzeile** — Fläche unter 4,5:1 | 53,0 % | 12,9 % |

**Das Flächenurteil steht auf „durchgefallen"** — 2,9 % gegen die
selbstgesetzte 2-%-Grenze. Diese Grenze wurde **nicht** nachträglich
angehoben, um das Ergebnis grün zu bekommen. Sie stand vorher fest.

Dass der Rest Kantenglättung ist und kein zu heller Grund, zeigt die
Empfindlichkeitsprüfung — und zwar sauber gegen den Vergleichsfall:

| Toleranz | Runde 3 (Grund zu hell) | Runde 4 (nur Kanten) |
|---:|---:|---:|
| 0 | 78,5 % | 13,1 % |
| 140 | 75,9 % (**flach**) | 1,5 % (**steil**) |

Bleibt der Anteil beim Hochdrehen flach, ist der Hintergrund wirklich zu
hell. Fällt er steil, waren es Übergangspixel zwischen Schrift und Grund.
Derselbe Test hat in Runde 3 eine bequeme Ausrede widerlegt und in Runde 4
eine echte Verbesserung bestätigt. Deshalb gibt `kontrast.py` seit dem
14.08.2026 beide Urteile aus, das strenge und das nach Fläche, und
verweist im Bericht auf diese Prüfung.

### Noch offen
- **`spacing_sections` steht auf 0.** Der Weissraum kommt bisher aus
  meinem CSS. Dawns native Einstellung ist der sauberere Ort und bleibt
  im Theme-Editor sichtbar.
- **Befund 2, schwebende Widgets.** Aus `settings_data.json` bekannt:
  Shopify Inbox (Chat, unten rechts) ist aktiv, der Widerrufsbutton von
  Revoq und die Essential Trust Badges stehen auf `disabled`. Auf den
  Aufnahmen ist nur noch der Chat-Knopf zu sehen — der Befund hat sich
  womöglich von selbst erledigt, ist aber nicht abgehakt.
- **`snippets/ebay-default.liquid`** meldet einen `LiquidHTMLSyntaxError`.
  **Nicht reparieren:** Das ist eBays eigene Template-Sprache
  (`{if …}{else}{/if}`), kein kaputtes Liquid. Theme Check liest sie nur
  falsch. Eine „Korrektur" würde die eBay-Vorlage zerstören.

## Der Engpass, der den Rest bremst

Ohne `SHOPIFY_CLI_THEME_TOKEN` gibt es nur einen Schreibweg: die
Admin-API, **Datei für Datei, und der komplette Dateiinhalt muss durch
den Chat**. Für `templates/index.json` waren das rund **14 KB
Base64 für eine einzige Datei mit drei geänderten Werten.**

Das Theme hat **369 Dateien**. Ein vollständiges Umschreiben auf diesem
Weg ist nicht machbar — nicht aus Unwillen, sondern arithmetisch.

**Mit dem Token ändert sich das vollständig:**

```
shopify theme pull  →  Dateien liegen lokal im Git
   ... beliebig viele chirurgische Änderungen, billig ...
shopify theme check →  Shopifys eigener Linter über alles
shopify theme push  →  zurück in die Arbeitskopie
```

Dann ist jede Änderung ein Commit mit Diff, ein Fehlgriff ein
`git revert`, und die Kosten pro Datei fallen praktisch auf null. Der
Workflow **`.github/workflows/theme.yml` ist dafür bereits fertig
gebaut** und bricht heute nur an der fehlenden Zeile im Tresor ab.

Einrichtung (5 Minuten, Anleitung steht in `WERKZEUGE.md`):
1. Shopify-Adminbereich → App **„Theme Access"** installieren
2. Passwort für `alanz.shops@gmail.com` erzeugen — kommt per E-Mail,
   beginnt mit `shptka_`
3. GitHub → *Settings → Secrets and variables → Actions → New repository
   secret* → Name **`SHOPIFY_CLI_THEME_TOKEN`**

Ich bekomme den Token nie zu sehen; nur der Runner liest ihn zur
Laufzeit.

---

## Offen

| Befund | Wo zu beheben | Aufwand ohne Token |
|---|---|---|
| 1b · **Unterzeile im Hero** weiterhin unter 4,5:1 | Verlaufs-Scrim per CSS | im Sammel-Durchgang |
| 2 · Drei schwebende Widgets überlagern sich | seitenweites CSS → `layout/theme.liquid` | 22 KB Übertragung |
| 3 · Zehn Hauptmenüpunkte | Shopify-Navigation, **nicht** im Theme | im Adminbereich, von Hand |
| 4 · Produkttitel sprengen die Kacheln | seitenweites CSS | 22 KB Übertragung |
| 5 · Uneinheitliche Bildsprache | Cloudinary (verbunden, ungenutzt) | Inhaltsarbeit |
| 6 · Währungsformat `€99,00` | **Shop-Einstellung**, nicht Theme | im Adminbereich, von Hand |
| 7 · Zahlungs-Icons doppelt | `templates/index.json` | 14 KB Übertragung |
| 8 · Emoji als Vertrauens-Icons | `templates/index.json` | 14 KB Übertragung |
| — · Designsystem (Farbe, Typografie, Raum) | `config/settings_data.json` + eigenes CSS | groß |

**Lehre aus dem ersten Schreibvorgang:** Befund 7 und 8 sitzen beide in
`templates/index.json` — dieselbe Datei, die gerade geschrieben wurde.
Sie hätten im selben Vorgang miterledigt werden können. Bei diesem
Übertragungsweg gilt: **alle Änderungen an einer Datei sammeln und in
einem Zug schreiben**, nie einzeln nacheinander.
