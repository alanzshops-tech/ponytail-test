# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 780 ms | 0 ms | 3397 kB | 378 | 4212 px | – |
| / | desktop | 200 | 884 ms | 0 ms | 3477 kB | 376 | 4047 px | – |
| /collections/hunde | mobil | 200 | 796 ms | 0 ms | 2865 kB | 378 | 4496 px | – |
| /collections/hunde | desktop | 200 | 528 ms | 0 ms | 2899 kB | 373 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 684 ms | 0 ms | 3178 kB | 422 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 448 ms | 0 ms | 3654 kB | 436 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 368 ms | 0 ms | 3040 kB | 421 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 460 ms | 0 ms | 3450 kB | 421 | 3844 px | – |
| /cart | mobil | 200 | 296 ms | 0 ms | 2705 kB | 356 | 1077 px | – |
| /cart | desktop | 200 | 228 ms | 0 ms | 2709 kB | 359 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 808 ms | 0 ms | 3019 kB | 428 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 392 ms | 0 ms | 3444 kB | 434 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 368 ms | 0 ms | 3112 kB | 428 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 360 ms | 0 ms | 3437 kB | 421 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1311 kB, other 963 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1380 kB, other 965 kB, font 212 kB, image 211 kB, stylesheet 49 kB, document 48 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1506 kB, other 963 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 50 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1509 kB, other 965 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 49 kB
- `/cart` — script 1455 kB, other 960 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1506 kB, other 968 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1509 kB, other 965 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 50 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=03475cad-7cf8-46cb-ace6-14a5440a9414&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c696bbaa-5fb8-4630-9e8c-7d3d95e98775&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=eacc8ba7-f235-4fea-8356-80af09d2a3e7&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=33b0bb64-f56a-47ad-b93a-da7f9610ddc5&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=19a40853-89e3-4c5a-a04a-4aeba992f751&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=afb25e21-e9a8-4659-88bf-c37fa603b21d&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ea89e1e5-b0d9-44a8-95c0-531a09a49a16&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=cafe3b2f-670d-4acf-9a1e-b09c976bb08b&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ac1861f4-a7cc-44d8-9fec-d25b633f95bd&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2ed7f0d7-0b48-423b-8990-9e75e6568c0e&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=6f9c87e6-c283-4b74-81e2-933ba2c25cab&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ced353d7-6432-46fc-bf8b-8ea5d9cf4128&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a4142812-2161-4ca2-adfa-d74d0371f2da&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=799fad50-f48f-4a5c-95bc-973190800b14&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 378 Anfragen, davon **32 von 18 fremden Servern** mit 635 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 235 | 2109 | ja |
| cdn.shopify.com | 90 | 651 | ja |
| otlp-http-production.shopifysvc.com | 13 | 0 | ja |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 472 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| error-analytics-sessions-production.shopifysvc | 1 | 0 | ja |
| app.cjdropshipping.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (562 kB)
- `bilder/startseite-desktop.jpg` (473 kB)
- `bilder/collections-hunde-mobil.jpg` (648 kB)
- `bilder/collections-hunde-desktop.jpg` (361 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (689 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (444 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (434 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (303 kB)
- `bilder/cart-mobil.jpg` (86 kB)
- `bilder/cart-desktop.jpg` (53 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-mobil.jpg` (555 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-desktop.jpg` (409 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-mobil.jpg` (483 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-desktop.jpg` (372 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 67 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 87 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 90 | 90 | 56 | 100 |
| startseite | 86 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

