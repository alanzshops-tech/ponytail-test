# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1300 ms | 0 ms | 3737 kB | 391 | 4183 px | – |
| / | desktop | 200 | 936 ms | 0 ms | 3764 kB | 399 | 4172 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1615 kB, other 961 kB, image 706 kB, font 259 kB, stylesheet 146 kB, document 46 kB

## Befunde

- `/` (mobil): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b5d7b99f-0e6a-4808-860e-3a9604029fb8&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a2222db5-ad3c-4b18-89cf-220837bdc0bb&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/nachher-startseite-mobil.jpg` (505 kB)
- `bilder/nachher-startseite-desktop.jpg` (441 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 67 | 93 | 59 | 92 |
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 89 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 88 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 88 | 90 | 56 | 100 |
| startseite | 83 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

