# Prüfstand

Stand: 2026-08-09

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

Richtwerte: Fließtext ab **16 px**, Zeilen **45–80 Zeichen**. Längere Zeilen verliert das Auge beim Rücksprung.

## Bewertungen auf der Live-Seite

| Seite | Judge.me-Widget | ★-Symbole | „Bewertung" | „Sterne" | aggregateRating |
|---|:-:|---:|---:|---:|---:|
| / | ja | 0 | 0 | 0 | 0 |
| /collections/hunde | ja | 0 | 0 | 0 | 0 |
| /products/hundesofa-samt-erhoeht-xxl | ja | 1 | 0 | 0 | 0 |
| /products/sitzbank-stauraum-gepolstert-klappbar | ja | 0 | 0 | 0 | 0 |
| /cart | ja | 0 | 0 | 0 | 0 |

Widget-Inhalt auf `/`:

```
window.jdgmSettings={"pagination":5,"disable_web_reviews":false,"badge_no_review_text":"Keine Bewertungen","badge_n_reviews_text":"{{ n }} Bewertung/Bewertungen","badge_star_color":"#ffd700","hide_badge_preview_if_no_reviews":true,"badge_hide_text":false,"enforce_center_preview_badge":false,"widget_
```

Widget-Inhalt auf `/collections/hunde`:

```
window.jdgmSettings={"pagination":5,"disable_web_reviews":false,"badge_no_review_text":"Keine Bewertungen","badge_n_reviews_text":"{{ n }} Bewertung/Bewertungen","badge_star_color":"#ffd700","hide_badge_preview_if_no_reviews":true,"badge_hide_text":false,"enforce_center_preview_badge":false,"widget_
```

Widget-Inhalt auf `/products/hundesofa-samt-erhoeht-xxl`:

```
window.jdgmSettings={"pagination":5,"disable_web_reviews":false,"badge_no_review_text":"Keine Bewertungen","badge_n_reviews_text":"{{ n }} Bewertung/Bewertungen","badge_star_color":"#ffd700","hide_badge_preview_if_no_reviews":true,"badge_hide_text":false,"enforce_center_preview_badge":false,"widget_
```

Widget-Inhalt auf `/products/sitzbank-stauraum-gepolstert-klappbar`:

```
window.jdgmSettings={"pagination":5,"disable_web_reviews":false,"badge_no_review_text":"Keine Bewertungen","badge_n_reviews_text":"{{ n }} Bewertung/Bewertungen","badge_star_color":"#ffd700","hide_badge_preview_if_no_reviews":true,"badge_hide_text":false,"enforce_center_preview_badge":false,"widget_
```

Widget-Inhalt auf `/cart`:

```
window.jdgmSettings={"pagination":5,"disable_web_reviews":false,"badge_no_review_text":"Keine Bewertungen","badge_n_reviews_text":"{{ n }} Bewertung/Bewertungen","badge_star_color":"#ffd700","hide_badge_preview_if_no_reviews":true,"badge_hide_text":false,"enforce_center_preview_badge":false,"widget_
```

**aggregateRating** ist die Stelle, an der Google Sterne für die Trefferliste abgreift. Steht dort etwas ohne echte Käufe, wirbt der Shop auch außerhalb der eigenen Seite mit Erfundenem.

## Befunde, nach Häufigkeit

| Regel | Schwere | Fälle | betroffen |
|---|---|---:|---|
| Scrollable region must have keyboard access | serious | 10 | /, /cart, /collections/hunde, /products/hundesofa-samt-erhoeht-xxl, /products/sitzbank-stauraum-gepolstert-klappbar |
| Elements must meet minimum color contrast ratio thresholds | serious | 6 | /, /products/hundesofa-samt-erhoeht-xxl, /products/sitzbank-stauraum-gepolstert-klappbar |
| Form elements must have labels | critical | 4 | /products/hundesofa-samt-erhoeht-xxl, /products/sitzbank-stauraum-gepolstert-klappbar |

Beispiele:

- `scrollable-region-focusable` — `<div class="grid grid--1-col slider slider--everywhere" id="Slider-sections--25600909050179__announcement-bar" aria-live="off" aria-atomic="true" data-autoplay=`
- `color-contrast` — `<p class="he-faq__eyebrow">FAQ</p>`
- `label` — `<input class="quantity__input" type="number" name="quantity" id="Quantity-template--25600912359747__main" data-cart-quantity="0" data-min="1" min="1" step="1" v`

