# Prüfstand

Stand: 2026-08-10

Gemessen mit **axe-core** (Deque, MPL-2.0) gegen WCAG 2.1 AA, dazu Lesbarkeitsmaße und ein Pixelvergleich gegen die letzte Grundlinie.

> Barrierefreiheit ist für Homeeins keine gesetzliche Pflicht — das BFSG nimmt Kleinstunternehmen für Dienstleistungen aus. Die Befunde sind trotzdem echte Bedienfehler.

| Seite | Gerät | schwer | leicht | Schrift | Zeilenlänge | Pixel geändert |
|---|---|---:|---:|---:|---:|---:|
| / | mobil | **1** | 0 | 16.5 px | 0 Z. | – |
| / | desktop | **1** | 0 | 15.4 px | 0 Z. | – |
| /collections/hunde | mobil | **1** | 0 | 16.5 px | 21 Z. | – |
| /collections/hunde | desktop | **1** | 0 | 17.6 px | 0 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | **2** | 0 | 16.5 px | 41 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | **2** | 0 | 15.4 px | 0 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | **2** | 0 | 16.5 px | 41 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | **2** | 0 | 15.4 px | 0 Z. | – |
| /cart | mobil | **1** | 0 | 16.5 px | 0 Z. | – |
| /cart | desktop | **1** | 0 | 15.4 px | 0 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | **5** | 0 | 16.5 px | 38 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | **5** | 0 | 15.4 px | 0 Z. | – |

Richtwerte: Fließtext ab **16 px**, Zeilen **45–80 Zeichen**. Längere Zeilen verliert das Auge beim Rücksprung.

## Widerrufsbutton

| Seite | Elemente | sichtbar | schwebend m. Text | Skripte |
|---|---:|---:|---:|---:|
| / | 3 | 3 | 1 | 1 |
| /collections/hunde | 3 | 3 | 1 | 1 |
| /products/hundesofa-samt-erhoeht-xxl | 3 | 3 | 1 | 1 |
| /products/sitzbank-stauraum-gepolstert-klappbar | 3 | 3 | 1 | 1 |
| /cart | 3 | 3 | 1 | 1 |
| /products/samt-sessel-design-armlehnen-holzbeine | 3 | 3 | 1 | 1 |

**Schwebende Elemente auf dem Handy** (390 × 844 px), Abstände vom rechten und unteren Rand:

| Element | Text | Größe | von rechts | von unten |
|---|---|---|---:|---:|
| `widerruf-trigger-button widerruf-trigger-button--floating wi` | Vertrag widerrufen | 162×42 | 20 px | 20 px |
| `trustedsite-tm-image` | – | 92×38 | 0 px | -13 px |

**Überlappungen: widerruf-trigger-button widerruf-trigger-button--floating wi × trustedsite-tm-image (72 × 5 px)**


Erstes gefundenes Element:

```
<div class="widerruf-popup-source widerruf-popup-source--embed" data-widerruf-popup-source="" data-widerruf-popup-source-kind="embed" data-widerruf-popup-css-url="https://cdn.shopi
```

Derselbe Detektor läuft gegen das veröffentlichte Theme, wo der Knopf abgeschaltet ist. Nur wenn er dort **null** meldet und in der Sandbox mehr, ist der Fund ein Beweis.

## Preisschreibweise

| Seite | Preise | davon mit „EUR" |
|---|---:|---:|
| / | 0 | 0 |
| /collections/hunde | 0 | 0 |
| /products/hundesofa-samt-erhoeht-xxl | 0 | 0 |
| /products/sitzbank-stauraum-gepolstert-klappbar | 0 | 0 |
| /cart | 0 | 0 |
| /products/samt-sessel-design-armlehnen-holzbeine | 0 | 0 |

Deutsche Schreibweise ist „124,99 €" — Zahl vorn, Zeichen hinten, ohne Währungskürzel. Das Kürzel schaltet ein Haken im Theme ab; die Stellung des Zeichens ist eine Shop-Einstellung.

## Bewertungen auf der Live-Seite

| Seite | Judge.me-Widget | ★-Symbole | „Bewertung" | „Sterne" | aggregateRating |
|---|:-:|---:|---:|---:|---:|
| / | – | 0 | 0 | 0 | 0 |
| /collections/hunde | – | 0 | 0 | 0 | 0 |
| /products/hundesofa-samt-erhoeht-xxl | ja | 1 | 1 | 0 | 0 |
| /products/sitzbank-stauraum-gepolstert-klappbar | ja | 0 | 1 | 0 | 0 |
| /cart | – | 0 | 0 | 0 | 0 |
| /products/samt-sessel-design-armlehnen-holzbeine | ja | 1 | 3 | 0 | 1 |

Widget-Inhalt auf `/products/hundesofa-samt-erhoeht-xxl`:

```
Kundenbewertungen
Schreiben Sie die erste Bewertung
```

Widget-Inhalt auf `/products/sitzbank-stauraum-gepolstert-klappbar`:

```
Kundenbewertungen
Schreiben Sie die erste Bewertung
```

Widget-Inhalt auf `/products/samt-sessel-design-armlehnen-holzbeine`:

```
Kundenbewertungen
 5.00 von 5
Basierend auf 1 Bewertung
 
 1
 
 0
 
 0
 
 0
 
 0
Sort by
Neueste
Höchste Bewertung
Niedrigste Bewertung
Nur Bilder
Bilder zuerst
Videos zuerst
Hilfreichste
03/29/2026
Anna M.
Absolut top!

Absolut top! Der Design-Samt-Sessel ist genau so schön wie auf den Fotos – supe
```

**aggregateRating** ist die Stelle, an der Google Sterne für die Trefferliste abgreift. Steht dort etwas ohne echte Käufe, wirbt der Shop auch außerhalb der eigenen Seite mit Erfundenem.

## Befunde, nach Häufigkeit

| Regel | Schwere | Fälle | betroffen |
|---|---|---:|---|
| Scrollable region must have keyboard access | serious | 12 | /, /cart, /collections/hunde, /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Form elements must have labels | critical | 6 | /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Elements must meet minimum color contrast ratio thresholds | serious | 6 | /products/samt-sessel-design-armlehnen-holzbeine |

Beispiele:

- `scrollable-region-focusable` — `<div class="grid grid--1-col slider slider--everywhere" id="Slider-sections--25601111064899__announcement-bar" aria-live="off" aria-atomic="true" data-autoplay=`
- `label` — `<input class="quantity__input" type="number" name="quantity" id="Quantity-template--25601110737219__main" data-cart-quantity="0" data-min="1" min="1" step="1" v`
- `color-contrast` — `<select class="jdgm-sort-dropdown">`

