# Shop-Messung

Stand: 2026-08-16

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 920 ms | 0 ms | 3425 kB | 388 | 4212 px | – |
| / | desktop | 200 | 200 ms | 0 ms | 3504 kB | 390 | 4047 px | – |
| /collections/hunde | mobil | 200 | 576 ms | 0 ms | 2893 kB | 388 | 4641 px | – |
| /collections/hunde | desktop | 200 | 296 ms | 0 ms | 2931 kB | 392 | 3365 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 464 ms | 0 ms | 3246 kB | 432 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 552 ms | 0 ms | 3655 kB | 431 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 520 ms | 0 ms | 3103 kB | 428 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 532 ms | 0 ms | 3517 kB | 430 | 3844 px | – |
| /cart | mobil | 200 | 472 ms | 0 ms | 2674 kB | 343 | 1077 px | – |
| /cart | desktop | 200 | 428 ms | 0 ms | 2776 kB | 376 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 536 ms | 0 ms | 3083 kB | 437 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 480 ms | 0 ms | 3577 kB | 441 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 484 ms | 0 ms | 3174 kB | 427 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 320 ms | 0 ms | 3464 kB | 432 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1316 kB, other 986 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1387 kB, other 986 kB, font 212 kB, image 211 kB, stylesheet 49 kB, document 49 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1551 kB, other 986 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1551 kB, other 986 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 49 kB
- `/cart` — script 1461 kB, other 922 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1552 kB, other 986 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1551 kB, other 986 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 49 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=6b49278b-8584-422c-b3d9-414b42bd2c3f&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4723e07c-e321-45f6-ae18-ec585a3c2692&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=51bed87e-4966-4037-968a-4c749b892114&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9c5de532-a6f2-44a7-a8ef-e3eb2e749a4f&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9b82cf85-15b4-4ea0-b065-85a7c561a2ed&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=45252bbe-0dd5-452c-8ebe-460df2348a6c&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9235905d-cdd0-4d33-b370-ea55b8fa85a3&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=75dd95ae-2e8c-48f1-8546-d91cbe7528d4&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=63c17317-6ef5-494a-aa26-20e5e828bf41&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c2982e9a-43e9-40b3-937e-547f252d8b75&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=cb007347-a00b-48be-8833-7ae1e0b2b0ef&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a7cf6371-c219-4e19-ba52-3bcdefa51bb5&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=94f54c92-4e61-42b0-80dd-857929ce0f75&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2e03e2f0-c3a6-499c-9d1e-4617ec7a3c89&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 388 Anfragen, davon **32 von 18 fremden Servern** mit 641 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 246 | 2109 | ja |
| cdn.shopify.com | 91 | 673 | ja |
| otlp-http-production.shopifysvc.com | 11 | 0 | ja |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 478 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (562 kB)
- `bilder/startseite-desktop.jpg` (473 kB)
- `bilder/collections-hunde-mobil.jpg` (681 kB)
- `bilder/collections-hunde-desktop.jpg` (378 kB)
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
| cart | 96 | 93 | 59 | 92 |
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 89 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 87 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 88 | 90 | 56 | 100 |
| startseite | 96 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

