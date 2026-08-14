# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 360 ms | 0 ms | 3440 kB | 387 | 4212 px | – |
| / | desktop | 200 | 232 ms | 0 ms | 3475 kB | 384 | 4047 px | – |
| /collections/hunde | mobil | 200 | 240 ms | 0 ms | 2904 kB | 385 | 4496 px | – |
| /collections/hunde | desktop | 200 | 260 ms | 0 ms | 2901 kB | 382 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 708 ms | 0 ms | 3186 kB | 442 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 232 ms | 0 ms | 3654 kB | 439 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 304 ms | 0 ms | 3079 kB | 427 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 224 ms | 0 ms | 3498 kB | 445 | 3844 px | – |
| /cart | mobil | 200 | 232 ms | 0 ms | 2751 kB | 369 | 1077 px | – |
| /cart | desktop | 200 | 204 ms | 0 ms | 2751 kB | 372 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 224 ms | 0 ms | 3015 kB | 428 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 448 ms | 0 ms | 3553 kB | 442 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 236 ms | 0 ms | 3154 kB | 438 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 216 ms | 0 ms | 3475 kB | 426 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1352 kB, other 965 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1421 kB, other 963 kB, font 212 kB, image 211 kB, stylesheet 49 kB, document 48 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1507 kB, other 969 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1547 kB, other 966 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 48 kB
- `/cart` — script 1496 kB, other 965 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1506 kB, other 965 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1550 kB, other 966 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 50 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7be4aa05-0e50-48c9-a81a-1d586aae856a&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=1178823b-fe96-4332-9c60-22d747d17e54&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=bf41095c-f184-4e1c-9f39-d2da8631f6fd&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=59df2252-5449-4eaa-b7d9-8d6fc6f81358&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=8bfa40c3-e458-4429-9360-8f6a3932adc5&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=1c08ce46-9fb6-494c-9c11-a48aa5df2a65&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3276c0a5-0913-4cc5-81ef-a0a8d984b7b2&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2f63594d-fd6a-45f5-978e-dc02a04293d8&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=763b473a-6ee7-4b4b-b73c-4dd604d54b62&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9bd80274-3b9d-4f28-9705-e466272e6cdb&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d6d5ca3e-677c-4da9-9ee4-721e7945d3c0&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2837aaca-1e8d-440c-93f3-4f5399928b44&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d395f13c-2cf1-4fef-a471-613481e7d881&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=eb533f30-7f11-4975-836a-c443c63a9ba8&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 387 Anfragen, davon **39 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 236 | 2110 | ja |
| cdn.shopify.com | 91 | 653 | ja |
| otlp-http-production.shopifysvc.com | 13 | 0 | ja |
| analytics.tiktok.com | 10 | 45 | **nein** |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 513 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| error-analytics-sessions-production.shopifysvc | 1 | 0 | ja |

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
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 86 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 88 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 88 | 90 | 56 | 100 |
| startseite | 87 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

