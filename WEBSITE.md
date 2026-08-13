# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 792 ms | 0 ms | 3264 kB | 303 | 4215 px | – |
| / | desktop | 200 | 500 ms | 0 ms | 3306 kB | 303 | 4047 px | – |
| /collections/hunde | mobil | 200 | 748 ms | 0 ms | 2625 kB | 303 | 4500 px | – |
| /collections/hunde | desktop | 200 | 700 ms | 0 ms | 2690 kB | 306 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 668 ms | 0 ms | 3212 kB | 353 | 6313 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 732 ms | 0 ms | 3640 kB | 365 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 508 ms | 0 ms | 3064 kB | 349 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 528 ms | 0 ms | 3525 kB | 354 | 3852 px | – |
| /cart | mobil | 200 | 544 ms | 0 ms | 2535 kB | 289 | 1081 px | – |
| /cart | desktop | 200 | 488 ms | 0 ms | 2576 kB | 288 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 620 ms | 0 ms | 2982 kB | 357 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 652 ms | 0 ms | 3584 kB | 369 | 5395 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 728 ms | 0 ms | 3181 kB | 350 | 4405 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 620 ms | 0 ms | 3509 kB | 358 | 4195 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1208 kB, other 988 kB, image 820 kB, font 149 kB, document 61 kB, stylesheet 37 kB
- `/collections/hunde` — script 1171 kB, other 989 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1368 kB, other 1080 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1365 kB, other 1078 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/cart` — script 1313 kB, other 988 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1302 kB, other 1080 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1409 kB, other 1080 kB, image 315 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a7623f1c-9eef-40e4-876a-4733b26743eb&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e180ad06-2b75-471c-b47d-cf4236d3c375&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f5a84a20-9bca-470c-917d-e80363a6167b&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5a049011-2ab1-4199-aca6-d6ae45e41c9b&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=417df79d-4667-4312-bbb7-b79d8b954cc9&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4279833b-90bb-4872-babe-c18ef77b093c&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ad1fa013-6096-4c3b-add6-f4ad1b11cf8e&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=71fd22f5-a003-4e7a-b509-bd0e817da8e2&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e2f7e10d-4c92-4a3e-b85d-db2fd6689240&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=da43071e-6346-4c9d-85d7-6df86d886688&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=88b5d1fc-ec54-4146-b080-439e611c7168&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7ad3d387-d57f-48af-9cb6-7562f2305276&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=decdc455-3cac-41d2-baa0-566144b695b6&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=43333a1a-d9f7-4457-877c-d1e1fa2692aa&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 303 Anfragen, davon **30 von 18 fremden Servern** mit 675 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 249 | 2129 | ja |
| cdn.shopify.com | 16 | 460 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| www.googletagmanager.com | 3 | 514 | **nein** |
| analytics.tiktok.com | 3 | 43 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| www.trustedsite.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (565 kB)
- `bilder/startseite-desktop.jpg` (475 kB)
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
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 59 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 90 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 86 | 90 | 59 | 100 |
| startseite | 89 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

