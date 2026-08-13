# Shop-Messung

Stand: 2026-08-13

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1008 ms | 0 ms | 3267 kB | 305 | 4215 px | – |
| / | desktop | 200 | 468 ms | 0 ms | 3254 kB | 277 | 4047 px | – |
| /collections/hunde | mobil | 200 | 1072 ms | 0 ms | 2711 kB | 305 | 4500 px | – |
| /collections/hunde | desktop | 200 | 1112 ms | 0 ms | 2628 kB | 277 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 940 ms | 0 ms | 3198 kB | 330 | 6313 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 340 ms | 0 ms | 3609 kB | 331 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 1160 ms | 0 ms | 2898 kB | 284 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 616 ms | 0 ms | 3415 kB | 323 | 3852 px | – |
| /cart | mobil | 200 | 528 ms | 0 ms | 2552 kB | 275 | 1081 px | – |
| /cart | desktop | 200 | 580 ms | 0 ms | 2468 kB | 258 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 656 ms | 0 ms | 3048 kB | 355 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 408 ms | 0 ms | 3514 kB | 334 | 5395 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 616 ms | 0 ms | 3118 kB | 324 | 4405 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 552 ms | 0 ms | 3386 kB | 317 | 4195 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1210 kB, other 989 kB, image 820 kB, font 149 kB, document 61 kB, stylesheet 37 kB
- `/collections/hunde` — script 1280 kB, other 966 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1406 kB, other 1027 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1407 kB, other 869 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/cart` — script 1354 kB, other 963 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1368 kB, other 1080 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1410 kB, other 1016 kB, image 315 kB, font 149 kB, xhr 94 kB, stylesheet 68 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5bfcc28b-d6cb-4dc8-9025-5550927fa04c&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7ac9352b-7c56-4ddf-add2-d78613729dda&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3db4ecea-f894-4f81-b49e-a8ca30eeac11&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=38c512be-5f17-4e29-b74b-991917281a55&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0b895691-4bc6-4d60-b89c-e430a08f2972&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=18f48368-dfc0-4cf1-857b-b7fdd06f80eb&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c20f22e1-9bba-44eb-a212-84ca3534066c&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=6e235ee8-63d8-43c6-ad05-698bb2cf9193&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7a688688-0459-44a5-bb82-045c976069de&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=8575516b-5476-49d0-a534-45cc8eace0d3&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=bfb8f2f4-22f4-4ebf-949f-a7c2845765e1&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ab32c0fc-3adb-4209-a39b-eaf6931c268c&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e7dbf590-5160-4e2b-8287-f8bdbcc91e69&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=389d21ac-15c5-44c4-9503-0ba6d3b6237a&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 305 Anfragen, davon **30 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 250 | 2130 | ja |
| cdn.shopify.com | 16 | 460 | ja |
| otlp-http-production.shopifysvc.com | 5 | 0 | ja |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| www.googletagmanager.com | 3 | 513 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
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
| app.cjdropshipping.com | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
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
| cart | 68 | 93 | 59 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 59 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 88 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 88 | 90 | 59 | 100 |
| startseite | 87 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

