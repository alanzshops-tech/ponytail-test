# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1136 ms | 0 ms | 3733 kB | 401 | 4183 px | – |
| / | desktop | 200 | 664 ms | 0 ms | 3769 kB | 410 | 4172 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1615 kB, other 958 kB, image 706 kB, font 259 kB, stylesheet 146 kB, document 46 kB

## Befunde

- `/` (mobil): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=8131a479-ff80-42e4-b2ea-5d936bd2ab98&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ef6f7b99-b31c-48de-908b-3c98fa007e8a&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/nachher2-startseite-mobil.jpg` (470 kB)
- `bilder/nachher2-startseite-desktop.jpg` (439 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 66 | 93 | 59 | 92 |
| collections-hunde | 66 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 86 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 75 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 84 | 90 | 56 | 100 |
| startseite | 71 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

