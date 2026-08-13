# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 888 ms | 0 ms | 3266 kB | 303 | 4215 px | – |
| / | desktop | 200 | 628 ms | 0 ms | 3305 kB | 304 | 4047 px | – |
| /collections/hunde | mobil | 200 | 624 ms | 0 ms | 2735 kB | 303 | 4500 px | – |
| /collections/hunde | desktop | 200 | 400 ms | 0 ms | 2732 kB | 303 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 688 ms | 0 ms | 3233 kB | 352 | 6313 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 604 ms | 0 ms | 3686 kB | 366 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 584 ms | 0 ms | 3108 kB | 352 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 460 ms | 0 ms | 3525 kB | 357 | 3852 px | – |
| /cart | mobil | 200 | 824 ms | 0 ms | 2516 kB | 258 | 1081 px | – |
| /cart | desktop | 200 | 248 ms | 0 ms | 2577 kB | 288 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 568 ms | 0 ms | 3089 kB | 357 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 372 ms | 0 ms | 3584 kB | 366 | 5395 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 464 ms | 0 ms | 3141 kB | 353 | 4405 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 556 ms | 0 ms | 3402 kB | 356 | 4195 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1208 kB, other 990 kB, image 820 kB, font 149 kB, document 61 kB, stylesheet 37 kB
- `/collections/hunde` — script 1279 kB, other 991 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1410 kB, other 1058 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1409 kB, other 1078 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/cart` — script 1354 kB, other 927 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1409 kB, other 1080 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1368 kB, other 1081 kB, image 315 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0edd6dd0-942c-4eaa-acca-e25f76a740a3&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=98594ac5-07cc-4998-ad77-79a7b66c5f11&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=01cf16f2-edcd-44df-b98a-c692953d7c98&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=397c8da7-0393-42f4-ba5c-2d5cae03ad64&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e0a5fc26-e28f-4a3a-ac97-3679278afd8d&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=34a00a8d-ad15-46dd-b1f1-26574a5cb3f9&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4c454986-540c-45c2-bfb5-0899dffa8b6a&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=502efec6-4637-4b52-a17f-53bd60fe7fb9&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e1448f38-346d-4148-a5bb-a932d314f671&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=369e2444-dd0c-465b-af57-2d9b264f3e0f&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7b3982b2-cec5-489e-bbf7-174eda5bc785&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2deb7af4-88e5-4a5c-9414-2786713e32c5&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=731b6480-5af1-4d11-9497-538576052f70&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d747137f-c063-40c2-80a1-ea1bef92248e&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 303 Anfragen, davon **30 von 18 fremden Servern** mit 677 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 249 | 2129 | ja |
| cdn.shopify.com | 16 | 460 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| www.googletagmanager.com | 3 | 514 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.trustedsite.com | 1 | 0 | **nein** |

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
| cart | 99 | 93 | 78 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 89 | 90 | 59 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 90 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 90 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 90 | 90 | 59 | 100 |
| startseite | 94 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

