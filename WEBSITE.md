# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1120 ms | 0 ms | 3721 kB | 408 | 4183 px | – |
| / | desktop | 200 | 972 ms | 0 ms | 3768 kB | 401 | 4172 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1575 kB, other 986 kB, image 706 kB, font 259 kB, stylesheet 146 kB, document 46 kB

## Befunde

- `/` (mobil): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=57e017bf-444b-4da9-96f8-6b7d8ef87d51&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9a572b30-5a08-4a9c-a352-d02a8a1459a0&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/nachher4-startseite-mobil.jpg` (486 kB)
- `bilder/nachher4-startseite-desktop.jpg` (461 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 67 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 86 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 83 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 86 | 90 | 56 | 100 |
| startseite | 87 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

