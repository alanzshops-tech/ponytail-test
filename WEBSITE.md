# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1300 ms | 0 ms | 3721 kB | 408 | 4183 px | – |
| / | desktop | 200 | 1348 ms | 0 ms | 3766 kB | 401 | 4172 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1575 kB, other 986 kB, image 706 kB, font 259 kB, stylesheet 146 kB, document 46 kB

## Befunde

- `/` (mobil): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5248bbd5-5d0c-474e-a4aa-91027e9a0352&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 16 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a9dfc91c-702a-4ff4-a53a-a8fcb5299632&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/nachher3-startseite-mobil.jpg` (475 kB)
- `bilder/nachher3-startseite-desktop.jpg` (446 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 66 | 93 | 59 | 92 |
| collections-hunde | 66 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 85 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 88 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 86 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 86 | 90 | 56 | 100 |
| startseite | 89 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

