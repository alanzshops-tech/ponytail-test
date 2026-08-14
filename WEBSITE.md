# Shop-Messung

Stand: 2026-08-14

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 636 ms | 0 ms | 3458 kB | 396 | 4212 px | – |
| / | desktop | 200 | 420 ms | 0 ms | 3437 kB | 387 | 4047 px | – |
| /collections/hunde | mobil | 200 | 664 ms | 0 ms | 2905 kB | 393 | 4641 px | – |
| /collections/hunde | desktop | 200 | 740 ms | 0 ms | 2886 kB | 400 | 3365 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 832 ms | 0 ms | 3216 kB | 422 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 416 ms | 0 ms | 3611 kB | 439 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 528 ms | 0 ms | 3097 kB | 431 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 440 ms | 0 ms | 3517 kB | 442 | 3844 px | – |
| /cart | mobil | 200 | 472 ms | 0 ms | 2772 kB | 381 | 1077 px | – |
| /cart | desktop | 200 | 476 ms | 0 ms | 2773 kB | 384 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 512 ms | 0 ms | 3053 kB | 429 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 556 ms | 0 ms | 3571 kB | 445 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 584 ms | 0 ms | 3144 kB | 418 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 672 ms | 0 ms | 3501 kB | 444 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1351 kB, other 984 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1421 kB, other 964 kB, font 212 kB, image 211 kB, stylesheet 49 kB, document 49 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1548 kB, other 958 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1544 kB, other 986 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 49 kB
- `/cart` — script 1496 kB, other 986 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1548 kB, other 960 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1547 kB, other 960 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 49 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7f2fd4ec-f7d4-422c-bd93-d2729bd08bda&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e4065e35-fa54-45ec-8dd4-fe2689e23b3e&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=745c2d14-5d13-44c8-a109-cbefc1b1c01b&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b71becdc-de32-4d96-b969-7c3cb6788ce4&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=11f763a6-b9dc-43a6-a44c-a164798e9894&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e7845637-43ca-4da4-9057-c1a74848dafb&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=18136e73-d76a-4377-8462-87905a82ad9f&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=dcb55bfc-6cbd-4833-aca6-07107978f893&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=59cd7e66-566c-402d-adc6-7ad4febb406d&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=60f5dff4-12a6-4094-a36d-db1adde0fbd2&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b66155c8-3fff-4845-a41f-70ac3632c8c0&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a0c51c2a-f089-46f5-8292-0aebec424976&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fb27f6f9-b487-4f18-9f96-98be9089c845&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=cd086c52-dd94-40b1-b2c7-e4069c2c3ceb&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 396 Anfragen, davon **39 von 18 fremden Servern** mit 674 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 247 | 2109 | ja |
| cdn.shopify.com | 91 | 673 | ja |
| otlp-http-production.shopifysvc.com | 11 | 0 | ja |
| analytics.tiktok.com | 10 | 43 | **nein** |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| www.googletagmanager.com | 3 | 513 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |

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
| cart | 69 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 87 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 90 | 90 | 56 | 100 |
| startseite | 85 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

