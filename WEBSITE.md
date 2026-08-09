# Shop-Messung

Stand: 2026-08-09

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1456 ms | 0 ms | 3952 kB | 325 | 10371 px | – |
| / | desktop | 200 | 544 ms | 0 ms | 4457 kB | 335 | 7019 px | – |
| /collections/hunde | mobil | 200 | 664 ms | 0 ms | 2717 kB | 298 | 4155 px | – |
| /collections/hunde | desktop | 200 | 796 ms | 0 ms | 2757 kB | 300 | 3104 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 700 ms | 0 ms | 3274 kB | 361 | 5783 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 472 ms | 0 ms | 3665 kB | 371 | 5516 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 868 ms | 0 ms | 3091 kB | 360 | 3682 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 812 ms | 0 ms | 3503 kB | 362 | 3549 px | – |
| /cart | mobil | 200 | 644 ms | 0 ms | 2597 kB | 280 | 996 px | – |
| /cart | desktop | 200 | 392 ms | 0 ms | 2556 kB | 278 | 900 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — image 1465 kB, script 1195 kB, other 1029 kB, font 149 kB, document 79 kB, stylesheet 34 kB
- `/collections/hunde` — script 1223 kB, other 1029 kB, image 211 kB, font 149 kB, document 69 kB, stylesheet 36 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1392 kB, other 1119 kB, image 385 kB, font 149 kB, xhr 94 kB, document 70 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1353 kB, other 1119 kB, image 244 kB, font 149 kB, xhr 94 kB, document 67 kB
- `/cart` — script 1337 kB, other 1027 kB, font 137 kB, document 58 kB, stylesheet 26 kB, image 10 kB

## Befunde

- `/` (mobil): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ee2882d4-f8db-4930-932f-608ff7ea1a42&target_origin=https%3A%2F%2Fw
- `/` (desktop): 2 von 67 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b47d7513-2338-4cee-8192-bdfc76fbd9c1&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f483d305-fa4a-4b1c-a67c-f0f7e208bfe5&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=1f86d658-75e9-4968-b263-a8090f3020ad&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=db62ba97-2631-44af-85fb-923c99e06b71&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ad4eda29-7152-479d-95cc-b935c689dbe7&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d9c5c71d-5ea1-401e-830f-5368aadd1ed8&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2700c6ae-d1f3-426d-8c6a-3453f40e0d28&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d5cb2397-5e46-4fcc-8d6b-7d0027ee9270&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5ebcaabb-1a52-4d0c-a5a2-bb7d2b15e9a2&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 325 Anfragen, davon **31 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 265 | 2376 | ja |
| cdn.shopify.com | 21 | 899 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| www.googletagmanager.com | 4 | 514 | **nein** |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 104 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| www.trustedsite.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (1010 kB)
- `bilder/startseite-desktop.jpg` (729 kB)
- `bilder/collections-hunde-mobil.jpg` (612 kB)
- `bilder/collections-hunde-desktop.jpg` (329 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (631 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (398 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (391 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (276 kB)
- `bilder/cart-mobil.jpg` (80 kB)
- `bilder/cart-desktop.jpg` (51 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 97 | 93 | 59 | 92 |
| collections-hunde | 67 | 93 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 86 | 90 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 88 | 90 | 59 | 100 |
| startseite | 86 | 88 | 74 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

