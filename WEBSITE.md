# Shop-Messung

Stand: 2026-08-10

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 460 ms | 0 ms | 3292 kB | 301 | 4110 px | – |
| / | desktop | 200 | 456 ms | 0 ms | 3291 kB | 302 | 3815 px | – |
| /collections/hunde | mobil | 200 | 716 ms | 0 ms | 2765 kB | 297 | 4500 px | – |
| /collections/hunde | desktop | 200 | 304 ms | 0 ms | 2723 kB | 297 | 3288 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 424 ms | 0 ms | 3272 kB | 366 | 5814 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 536 ms | 0 ms | 3716 kB | 356 | 6089 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 420 ms | 0 ms | 3098 kB | 343 | 4081 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 384 ms | 0 ms | 3517 kB | 349 | 3852 px | – |
| /cart | mobil | 200 | 424 ms | 0 ms | 2611 kB | 284 | 1081 px | – |
| /cart | desktop | 200 | 360 ms | 0 ms | 2567 kB | 281 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 424 ms | 0 ms | 3098 kB | 346 | 5601 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 348 ms | 0 ms | 3612 kB | 357 | 5395 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1204 kB, other 1025 kB, image 820 kB, font 149 kB, document 60 kB, stylesheet 34 kB
- `/collections/hunde` — script 1275 kB, other 1025 kB, image 211 kB, font 149 kB, document 64 kB, stylesheet 40 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1401 kB, other 1114 kB, image 385 kB, font 149 kB, xhr 94 kB, stylesheet 65 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1363 kB, other 1114 kB, image 244 kB, font 149 kB, xhr 94 kB, stylesheet 69 kB
- `/cart` — script 1350 kB, other 1025 kB, font 137 kB, document 56 kB, stylesheet 31 kB, image 10 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1404 kB, other 1093 kB, image 221 kB, font 149 kB, xhr 94 kB, stylesheet 69 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=244cbe2e-094e-4a63-81de-cc77c92c2e1d&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f2b57ae4-5005-46ed-9747-11e4d6e3e6c2&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d32574fa-8736-4647-91c9-53e0d834e722&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=dc71d26f-4264-4143-9292-440cfa6c95ff&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=22b9a906-3d1e-49a0-8b3a-e51578901905&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0edc0499-4dd4-4ebb-8ede-e7c53d87da27&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=dab40b22-d2d1-431e-b944-0f913964671d&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3d9b1f4c-dce6-4671-b7a4-d633ec28a4e2&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fd8ba206-df36-4e39-bfbe-74aaff0a14f4&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=adf62de8-9e89-4aa7-b204-ba8ac5a63719&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f1feaeaf-24e5-40b2-ad0b-0ddad0da9a50&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fce6b12b-6f15-427b-8e14-cabd285d3138&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 301 Anfragen, davon **30 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 248 | 2164 | ja |
| cdn.shopify.com | 15 | 452 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| www.googletagmanager.com | 3 | 514 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 104 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (560 kB)
- `bilder/startseite-desktop.jpg` (441 kB)
- `bilder/collections-hunde-mobil.jpg` (647 kB)
- `bilder/collections-hunde-desktop.jpg` (361 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (634 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (448 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (434 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (305 kB)
- `bilder/cart-mobil.jpg` (89 kB)
- `bilder/cart-desktop.jpg` (54 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-mobil.jpg` (567 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-desktop.jpg` (413 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 98 | 93 | 78 | 92 |
| collections-hunde | 68 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 90 | 59 | 100 |
| startseite | 86 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

