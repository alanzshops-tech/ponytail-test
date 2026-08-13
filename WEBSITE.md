# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1000 ms | 0 ms | 3481 kB | 403 | 4212 px | – |
| / | desktop | 200 | 396 ms | 0 ms | 3436 kB | 373 | 4047 px | – |
| /collections/hunde | mobil | 200 | 832 ms | 0 ms | 2867 kB | 382 | 4496 px | – |
| /collections/hunde | desktop | 200 | 900 ms | 0 ms | 2906 kB | 380 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 1044 ms | 0 ms | 3218 kB | 417 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 340 ms | 0 ms | 3653 kB | 430 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 504 ms | 0 ms | 3038 kB | 428 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 520 ms | 0 ms | 3491 kB | 421 | 3844 px | – |
| /cart | mobil | 200 | 356 ms | 0 ms | 2753 kB | 366 | 1077 px | – |
| /cart | desktop | 200 | 372 ms | 0 ms | 2774 kB | 379 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 604 ms | 0 ms | 3059 kB | 425 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 520 ms | 0 ms | 3552 kB | 429 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 580 ms | 0 ms | 3148 kB | 420 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 520 ms | 0 ms | 3480 kB | 426 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1393 kB, other 965 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1380 kB, other 967 kB, font 212 kB, image 211 kB, stylesheet 49 kB, document 48 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1546 kB, other 963 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 50 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1505 kB, other 967 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 48 kB
- `/cart` — script 1496 kB, other 967 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1548 kB, other 966 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1548 kB, other 963 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 49 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=98ee0f6b-3290-4415-840e-015c4c8d7f77&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=85fa6ea5-e0ec-4702-a866-250cf1047ff1&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c3791e1d-6c97-4b8e-bfa1-982f62281e8d&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=da2229ee-8c97-4522-aaf9-322e9ba57666&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=38963071-c969-44b2-ba1d-2c25b438254d&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5529e569-4d49-45cf-a1c4-41bdbea614e8&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c92c75cc-0e45-4afd-87f6-c2fbb47b638b&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=02fcf486-2d14-4997-a2e9-da750f49dcaf&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=32edab30-1f9a-4fff-a81b-cf3d2a3f2f83&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=75c19737-47fc-4b7b-b315-8d12cfe38658&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=af1328ef-5aed-4bf0-8e25-0007a7a5d79d&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=9e00c62f-4ac3-4b21-be88-4504507996a5&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=88808ee6-b1b8-4830-b1a8-7596bd038fef&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=753ded2b-d960-4fa5-9e5b-c29844bd8eb5&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 403 Anfragen, davon **32 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 239 | 2110 | ja |
| cdn.shopify.com | 113 | 694 | ja |
| otlp-http-production.shopifysvc.com | 11 | 0 | ja |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 513 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (562 kB)
- `bilder/startseite-desktop.jpg` (473 kB)
- `bilder/collections-hunde-mobil.jpg` (647 kB)
- `bilder/collections-hunde-desktop.jpg` (360 kB)
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
| cart | 66 | 93 | 59 | 92 |
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 87 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 90 | 56 | 100 |
| startseite | 75 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

