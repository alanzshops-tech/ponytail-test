# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 744 ms | 0 ms | 3225 kB | 301 | 4215 px | – |
| / | desktop | 200 | 508 ms | 0 ms | 3266 kB | 303 | 4047 px | – |
| /collections/hunde | mobil | 200 | 700 ms | 0 ms | 2692 kB | 303 | 4500 px | – |
| /collections/hunde | desktop | 200 | 796 ms | 0 ms | 2735 kB | 306 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 700 ms | 0 ms | 3210 kB | 356 | 6313 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 648 ms | 0 ms | 3643 kB | 363 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 400 ms | 0 ms | 3003 kB | 353 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 380 ms | 0 ms | 3525 kB | 354 | 3852 px | – |
| /cart | mobil | 200 | 544 ms | 0 ms | 2537 kB | 286 | 1081 px | – |
| /cart | desktop | 200 | 328 ms | 0 ms | 2577 kB | 286 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 476 ms | 0 ms | 3025 kB | 352 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 228 ms | 0 ms | 3520 kB | 358 | 5395 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 428 ms | 0 ms | 3140 kB | 353 | 4405 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 420 ms | 0 ms | 3512 kB | 353 | 4195 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1167 kB, other 990 kB, image 820 kB, font 149 kB, document 61 kB, stylesheet 37 kB
- `/collections/hunde` — script 1238 kB, other 990 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1368 kB, other 1078 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1302 kB, other 1080 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/cart` — script 1313 kB, other 989 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1368 kB, other 1057 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1368 kB, other 1080 kB, image 315 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=79f18900-2c66-46cd-9655-a7323197f8b0&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4bf2ac35-7170-4bf0-a328-bb53a63dd54e&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d0dc7b77-99bd-40b9-b4c0-f03838dd6ed9&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7c267603-1023-481c-8f97-ee81a161583e&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b63b3959-52de-4340-8fde-2e536a1700ce&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=bd727a19-a1c6-438e-a6da-c3b83b93419d&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=756fa5bf-59e0-4821-9de3-51bc73a1ef14&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c0905001-9f11-4784-bc0f-6c56b976c81b&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7b1a893e-f410-4807-b2e7-8bffb41d4241&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2673d12d-1e7b-432f-afbd-7d97a1506dfe&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=dffb9763-79ea-4a85-89fc-28a97b288977&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=bfae20e1-b38b-404a-ba70-9ac97941b5fa&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=630ee5af-f1c4-41c4-9018-bbc7ade7ebcb&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0fcd0e4a-f0eb-434b-beb3-47a74cc74668&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 301 Anfragen, davon **30 von 18 fremden Servern** mit 636 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 247 | 2129 | ja |
| cdn.shopify.com | 16 | 460 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| www.googletagmanager.com | 3 | 473 | **nein** |
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
| cdn.trustedsite.com | 1 | 5 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |

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
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-mobil.jpg` (483 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-desktop.jpg` (374 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 99 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 89 | 90 | 59 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 90 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 90 | 90 | 59 | 100 |
| startseite | 98 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

