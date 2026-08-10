# Prüfstand

Stand: 2026-08-10

Gemessen mit **axe-core** (Deque, MPL-2.0) gegen WCAG 2.1 AA, dazu Lesbarkeitsmaße und ein Pixelvergleich gegen die letzte Grundlinie.

> Barrierefreiheit ist für Homeeins keine gesetzliche Pflicht — das BFSG nimmt Kleinstunternehmen für Dienstleistungen aus. Die Befunde sind trotzdem echte Bedienfehler.

| Seite | Gerät | schwer | leicht | Schrift | Zeilenlänge | Pixel geändert |
|---|---|---:|---:|---:|---:|---:|
| / | mobil | **2** | 0 | 15 px | 0 Z. | – |
| / | desktop | **2** | 0 | 14 px | 0 Z. | – |
| /collections/hunde | mobil | **1** | 0 | 15 px | 24 Z. | – |
| /collections/hunde | desktop | **1** | 0 | 16 px | 0 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | **3** | 0 | 15 px | 46 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | **3** | 0 | 14 px | 0 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | **3** | 0 | 15 px | 43 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | **3** | 0 | 14 px | 0 Z. | – |
| /cart | mobil | **1** | 0 | 15 px | 0 Z. | – |
| /cart | desktop | **1** | 0 | 14 px | 0 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | **6** | 0 | 15 px | 43 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | **6** | 0 | 14 px | 0 Z. | – |

Richtwerte: Fließtext ab **16 px**, Zeilen **45–80 Zeichen**. Längere Zeilen verliert das Auge beim Rücksprung.

## Widerrufsbutton

| Seite | Elemente | sichtbar | schwebend m. Text | Skripte |
|---|---:|---:|---:|---:|
| / | 0 | 0 | 0 | 0 |
| /collections/hunde | 0 | 0 | 0 | 0 |
| /products/hundesofa-samt-erhoeht-xxl | 0 | 0 | 0 | 0 |
| /products/sitzbank-stauraum-gepolstert-klappbar | 0 | 0 | 0 | 0 |
| /cart | 0 | 0 | 0 | 0 |
| /products/samt-sessel-design-armlehnen-holzbeine | 0 | 0 | 0 | 0 |

Derselbe Detektor läuft gegen das veröffentlichte Theme, wo der Knopf abgeschaltet ist. Nur wenn er dort **null** meldet und in der Sandbox mehr, ist der Fund ein Beweis.

## Preisschreibweise

| Seite | Preise | davon mit „EUR" |
|---|---:|---:|
| / | 8 | 8 |
| /collections/hunde | 11 | 11 |
| /products/hundesofa-samt-erhoeht-xxl | 1 | 1 |
| /products/sitzbank-stauraum-gepolstert-klappbar | 1 | 1 |
| /cart | 0 | 0 |
| /products/samt-sessel-design-armlehnen-holzbeine | 1 | 1 |

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
| Elements must meet minimum color contrast ratio thresholds | serious | 14 | /, /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Scrollable region must have keyboard access | serious | 12 | /, /cart, /collections/hunde, /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Form elements must have labels | critical | 6 | /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |

Beispiele:

- `color-contrast` — `<p class="he-faq__eyebrow">FAQ</p>`
- `scrollable-region-focusable` — `<div class="grid grid--1-col slider slider--everywhere" id="Slider-sections--25601117323587__announcement-bar" aria-live="off" aria-atomic="true" data-autoplay=`
- `label` — `<input class="quantity__input" type="number" name="quantity" id="Quantity-template--25601116995907__main" data-cart-quantity="0" data-min="1" min="1" step="1" v`

