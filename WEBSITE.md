# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1020 ms | 0 ms | 3292 kB | 304 | 4215 px | – |
| / | desktop | 200 | 576 ms | 0 ms | 3334 kB | 304 | 4047 px | – |
| /collections/hunde | mobil | 200 | 768 ms | 0 ms | 2759 kB | 306 | 4500 px | – |
| /collections/hunde | desktop | 200 | 644 ms | 0 ms | 2760 kB | 305 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 404 ms | 0 ms | 3238 kB | 357 | 6313 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 532 ms | 0 ms | 3671 kB | 361 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 716 ms | 0 ms | 3138 kB | 352 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 608 ms | 0 ms | 3512 kB | 354 | 3852 px | – |
| /cart | mobil | 200 | 660 ms | 0 ms | 2606 kB | 289 | 1081 px | – |
| /cart | desktop | 200 | 276 ms | 0 ms | 2605 kB | 288 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 556 ms | 0 ms | 3117 kB | 354 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 288 ms | 0 ms | 3568 kB | 365 | 5395 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 616 ms | 0 ms | 3089 kB | 351 | 4274 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 396 ms | 0 ms | 3234 kB | 354 | 4056 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1208 kB, other 1016 kB, image 820 kB, font 149 kB, document 61 kB, stylesheet 37 kB
- `/collections/hunde` — script 1279 kB, other 1016 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1368 kB, other 1106 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1410 kB, other 1107 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/cart` — script 1353 kB, other 1017 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1409 kB, other 1108 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1409 kB, other 1108 kB, image 195 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a072ce04-8262-4c58-9ab7-a0d4bda243d0&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0ff1206e-f558-48db-b643-7ecd21c4bbd6&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e79eb880-1554-453a-91dc-eb0518615937&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7b0a1156-a3d0-4fdd-9bfd-a42b95dbba1e&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=198f4439-e12d-4b6e-9394-302d4793f052&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=db900f0c-5ed1-4337-9977-d349a26caa2b&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=64c139c8-55dc-40f8-acf8-942f9127f587&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=91e59e02-672a-4cfb-8e8a-19f9b5d0549a&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=60d6b2f8-952f-4268-99e4-d054e146cdb1&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c1a7ff95-9233-444f-a016-035ec76ba53a&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=66b15fd0-9338-4194-b010-f99b2580d298&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=efdc6a8d-5dd0-4a4b-bcf4-3771f03d0888&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=66d2d9f1-97b6-4136-b38c-fff3246bc6bb&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=816d5714-48ce-4cdd-9432-a1ac5144f5b3&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 304 Anfragen, davon **30 von 18 fremden Servern** mit 674 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 249 | 2129 | ja |
| cdn.shopify.com | 17 | 488 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| www.googletagmanager.com | 3 | 513 | **nein** |
| analytics.tiktok.com | 3 | 43 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| www.trustedsite.com | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (565 kB)
- `bilder/startseite-desktop.jpg` (474 kB)
- `bilder/collections-hunde-mobil.jpg` (647 kB)
- `bilder/collections-hunde-desktop.jpg` (361 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (690 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (448 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (434 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (305 kB)
- `bilder/cart-mobil.jpg` (89 kB)
- `bilder/cart-desktop.jpg` (54 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-mobil.jpg` (567 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-desktop.jpg` (413 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-mobil.jpg` (505 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-desktop.jpg` (386 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 98 | 93 | 78 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 86 | 90 | 59 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 86 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 87 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 90 | 90 | 59 | 100 |
| startseite | 90 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

