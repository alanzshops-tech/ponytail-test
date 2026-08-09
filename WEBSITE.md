# Shop-Messung

Stand: 2026-08-09

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1660 ms | 0 ms | 3879 kB | 305 | 10371 px | – |
| / | desktop | 200 | 1228 ms | 0 ms | 4405 kB | 310 | 7019 px | – |
| /collections/hunde | mobil | 200 | 660 ms | 0 ms | 2729 kB | 281 | 4155 px | – |
| /collections/hunde | desktop | 200 | 496 ms | 0 ms | 2728 kB | 287 | 3104 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 932 ms | 0 ms | 3233 kB | 361 | 5625 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 964 ms | 0 ms | 3682 kB | 364 | 5516 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 624 ms | 0 ms | 3993 kB | 324 | 10371 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 596 ms | 0 ms | 4434 kB | 330 | 7019 px | – |
| /cart | mobil | 200 | 552 ms | 0 ms | 2574 kB | 269 | 996 px | – |
| /cart | desktop | 200 | 700 ms | 0 ms | 2533 kB | 278 | 900 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — image 1465 kB, script 1154 kB, other 997 kB, font 149 kB, document 79 kB, stylesheet 34 kB
- `/collections/hunde` — script 1263 kB, other 1001 kB, image 211 kB, font 149 kB, document 69 kB, stylesheet 36 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1352 kB, other 1119 kB, image 385 kB, font 149 kB, xhr 94 kB, document 70 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — image 1465 kB, script 1260 kB, other 1006 kB, font 149 kB, document 79 kB, stylesheet 34 kB
- `/cart` — script 1339 kB, other 1002 kB, font 137 kB, document 59 kB, stylesheet 26 kB, image 10 kB

## Befunde

- `/` (mobil): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0ed88d30-d6ad-4ec3-8732-ed8e5d1cea47&target_origin=https%3A%2F%2Fw
- `/` (desktop): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fe30a96c-0fb2-49fe-8876-7c21da067512&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=14b3670f-88fe-4875-9369-93e9f5e09c53&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=6fc307a0-dda7-45a0-9c6a-21d4024f38ba&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4d5a2fe1-4551-4e9b-836a-248d331d6365&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=83a130e2-635b-4352-b502-46dd20d4eb25&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` (mobil): 2 von 67 Bildern ohne Alt-Text
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c1bb917d-53e7-4033-bd2b-501896cd8b9c&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` (desktop): 2 von 67 Bildern ohne Alt-Text
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=10e18623-cd70-4e7c-9481-389444202533&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d3ebd62f-cbf6-4c6d-87b6-787921f309a0&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=1ab28daf-ce66-47fc-a999-9fed75860690&target_origin=https%3A%2F%2Fw

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (1010 kB)
- `bilder/startseite-desktop.jpg` (729 kB)
- `bilder/collections-hunde-mobil.jpg` (612 kB)
- `bilder/collections-hunde-desktop.jpg` (329 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (617 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (398 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (1010 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (729 kB)
- `bilder/cart-mobil.jpg` (80 kB)
- `bilder/cart-desktop.jpg` (51 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 68 | 93 | 59 | 92 |
| collections-hunde | 68 | 93 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 87 | 90 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 91 | 88 | 74 | 100 |
| startseite | 98 | 88 | 74 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

