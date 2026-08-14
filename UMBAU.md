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

---

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
