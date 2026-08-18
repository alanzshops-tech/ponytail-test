# Shop-Messung

Stand: 2026-08-18

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1560 ms | 0 ms | 3435 kB | 374 | 4212 px | – |
| / | desktop | 200 | 448 ms | 0 ms | 3480 kB | 375 | 4047 px | – |
| /collections/hunde | mobil | 200 | 1036 ms | 0 ms | 2913 kB | 382 | 4641 px | – |
| /collections/hunde | desktop | 200 | 596 ms | 0 ms | 2908 kB | 376 | 3365 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 744 ms | 0 ms | 3223 kB | 419 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 428 ms | 0 ms | 3610 kB | 425 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 900 ms | 0 ms | 3081 kB | 419 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 524 ms | 0 ms | 3449 kB | 412 | 3844 px | – |
| /cart | mobil | 200 | 520 ms | 0 ms | 2710 kB | 350 | 1077 px | – |
| /cart | desktop | 200 | 476 ms | 0 ms | 2744 kB | 357 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 708 ms | 0 ms | 3057 kB | 423 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 548 ms | 0 ms | 3490 kB | 433 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 560 ms | 0 ms | 3150 kB | 422 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 576 ms | 0 ms | 3440 kB | 419 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1353 kB, other 957 kB, image 821 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1426 kB, other 964 kB, image 213 kB, font 212 kB, stylesheet 49 kB, document 49 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1550 kB, other 962 kB, image 387 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1552 kB, other 962 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 49 kB
- `/cart` — script 1500 kB, other 919 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1550 kB, other 962 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1550 kB, other 962 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 49 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=8c9d510f-91bb-4aad-ba88-0a5391cccd10&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=08660da5-1232-4545-b5a2-e2628a1f6746&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=34f3dd82-3d30-4c56-949a-b393c185f557&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=02ac46d0-6378-4520-a536-e7bed27b75c9&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=cf28c8eb-db18-4955-9763-7caae6991269&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=800e8c48-0496-4c9d-bd6a-f3d6f119f9d1&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0b097f39-ed5e-4ebc-8cbe-34561249bc17&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f85e2bae-e7b2-45de-92f0-055ce71aab76&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=20c91876-edd2-4440-a249-f29add1921ad&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=31a22c54-b430-49a0-8dd1-29def1f02c95&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=dd6ee628-67cc-496f-9333-3f5d7e405c41&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2825c023-097a-4e5e-94c8-02cb151c2531&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e1169431-25d7-40ad-930a-0c28c8a7cccd&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3fa2ca96-44cd-4505-9008-926120adc03e&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 374 Anfragen, davon **32 von 18 fremden Servern** mit 679 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 233 | 2104 | ja |
| cdn.shopify.com | 90 | 651 | ja |
| otlp-http-production.shopifysvc.com | 11 | 0 | ja |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 516 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| error-analytics-sessions-production.shopifysvc | 1 | 0 | ja |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (562 kB)
- `bilder/startseite-desktop.jpg` (473 kB)
- `bilder/collections-hunde-mobil.jpg` (680 kB)
- `bilder/collections-hunde-desktop.jpg` (378 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (690 kB)
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
| cart | 68 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 85 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 90 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 90 | 56 | 100 |
| startseite | 80 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

