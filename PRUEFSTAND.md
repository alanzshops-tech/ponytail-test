# Prüfstand

Stand: 2026-08-09

Gemessen mit **axe-core** (Deque, MPL-2.0) gegen WCAG 2.1 AA, dazu Lesbarkeitsmaße und ein Pixelvergleich gegen die letzte Grundlinie.

> Barrierefreiheit ist für Homeeins keine gesetzliche Pflicht — das BFSG nimmt Kleinstunternehmen für Dienstleistungen aus. Die Befunde sind trotzdem echte Bedienfehler.

| Seite | Gerät | schwer | leicht | Schrift | Zeilenlänge | Pixel geändert |
|---|---|---:|---:|---:|---:|---:|
| / | mobil | **3** | 0 | 16.5 px | 0 Z. | – |
| / | desktop | **3** | 0 | 15.4 px | 0 Z. | – |
| /collections/hunde | mobil | **2** | 0 | 16.5 px | 21 Z. | – |
| /collections/hunde | desktop | **2** | 0 | 17.6 px | 0 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | **3** | 0 | 16.5 px | 41 Z. | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | **3** | 0 | 15.4 px | 0 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | **3** | 0 | 16.5 px | 38 Z. | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | **3** | 0 | 15.4 px | 0 Z. | – |
| /cart | mobil | **2** | 0 | 16.5 px | 0 Z. | – |
| /cart | desktop | **2** | 0 | 15.4 px | 0 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | **3** | 0 | 16.5 px | 0 Z. | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | **3** | 0 | 15.4 px | 0 Z. | – |

Richtwerte: Fließtext ab **16 px**, Zeilen **45–80 Zeichen**. Längere Zeilen verliert das Auge beim Rücksprung.

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
| /products/hundesofa-samt-erhoeht-xxl | ja | 1 | 0 | 0 | 0 |
| /products/sitzbank-stauraum-gepolstert-klappbar | ja | 0 | 0 | 0 | 0 |
| /cart | – | 0 | 0 | 0 | 0 |
| /products/samt-sessel-design-armlehnen-holzbeine | ja | 1 | 0 | 0 | 1 |

**aggregateRating** ist die Stelle, an der Google Sterne für die Trefferliste abgreift. Steht dort etwas ohne echte Käufe, wirbt der Shop auch außerhalb der eigenen Seite mit Erfundenem.

## Befunde, nach Häufigkeit

| Regel | Schwere | Fälle | betroffen |
|---|---|---:|---|
| Frames must have an accessible name | serious | 12 | /, /cart, /collections/hunde, /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Scrollable region must have keyboard access | serious | 12 | /, /cart, /collections/hunde, /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Form elements must have labels | critical | 6 | /products/hundesofa-samt-erhoeht-xxl, /products/samt-sessel-design-armlehnen-holzbeine, /products/sitzbank-stauraum-gepolstert-klappbar |
| Elements must meet minimum color contrast ratio thresholds | serious | 2 | / |

Beispiele:

- `frame-title` — `<iframe id="PBarNextFrame" src="https://cdn.shopify...." sandbox="allow-same-origin al..." style="width: 100%; height:...">`
- `scrollable-region-focusable` — `<div class="grid grid--1-col slider slider--everywhere" id="Slider-sections--25600953188675__announcement-bar" aria-live="off" aria-atomic="true" data-autoplay=`
- `label` — `<input class="quantity__input" type="number" name="quantity" id="Quantity-template--25600956498243__main" data-cart-quantity="0" data-min="1" min="1" step="1" v`
- `color-contrast` — `<p class="he-faq__eyebrow">FAQ</p>`

