# Shop-Messung

Stand: 2026-08-09

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 552 ms | 0 ms | 3985 kB | 302 | 10371 px | – |
| / | desktop | 200 | 480 ms | 0 ms | 4431 kB | 324 | 7019 px | – |
| /collections/hunde | mobil | 200 | 764 ms | 0 ms | 2729 kB | 276 | 4155 px | – |
| /collections/hunde | desktop | 200 | 504 ms | 0 ms | 2681 kB | 259 | 3104 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 280 ms | 0 ms | 3204 kB | 342 | 5625 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 508 ms | 0 ms | 3601 kB | 338 | 5516 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 772 ms | 0 ms | 3061 kB | 341 | 3524 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 468 ms | 0 ms | 3521 kB | 350 | 3387 px | – |
| /cart | mobil | 200 | 744 ms | 0 ms | 2519 kB | 256 | 996 px | – |
| /cart | desktop | 200 | 400 ms | 0 ms | 2521 kB | 258 | 900 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — image 1465 kB, script 1260 kB, other 997 kB, font 149 kB, document 79 kB, stylesheet 34 kB
- `/collections/hunde` — script 1263 kB, other 1000 kB, image 211 kB, font 149 kB, document 69 kB, stylesheet 36 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1352 kB, other 1089 kB, image 385 kB, font 149 kB, xhr 94 kB, document 70 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1353 kB, other 1088 kB, image 244 kB, font 149 kB, xhr 94 kB, document 67 kB
- `/cart` — script 1296 kB, other 990 kB, font 137 kB, document 59 kB, stylesheet 26 kB, image 10 kB

## Befunde

- `/` (mobil): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=1e8158c5-3ddd-4490-a43f-aa0aa27eb1f1&target_origin=https%3A%2F%2Fw
- `/` (desktop): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ba7ae6a1-424c-46c1-b10e-ee320f611478&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e5381405-1c6c-45a5-8eb8-3c4a7465eb5a&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5fbb25fa-8cc6-4795-84cc-853445a31dee&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7977358a-d579-4dd1-b860-674449bff813&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c33ce0f2-86b7-48ed-8571-65dbf523d769&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b050f72f-d5d1-43c5-a15b-7f284ef49be6&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0d769aa2-ccb3-4c70-891c-d81ab23274fe&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=81a5abd2-ac1e-4bdc-9f83-da51c35e21e1&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ad057bc9-f56c-46bb-9e20-bcd0f7d6a6f7&target_origin=https%3A%2F%2Fw

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (1010 kB)
- `bilder/startseite-desktop.jpg` (730 kB)
- `bilder/collections-hunde-mobil.jpg` (612 kB)
- `bilder/collections-hunde-desktop.jpg` (329 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (617 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (398 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (377 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (268 kB)
- `bilder/cart-mobil.jpg` (80 kB)
- `bilder/cart-desktop.jpg` (51 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 68 | 93 | 59 | 92 |
| collections-hunde | 68 | 93 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 87 | 90 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 90 | 59 | 100 |
| startseite | 98 | 88 | 74 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

