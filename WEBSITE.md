# Shop-Messung

Stand: 2026-08-09

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 1200 ms | 0 ms | 3292 kB | 294 | 4079 px | – |
| / | desktop | 200 | 508 ms | 0 ms | 3290 kB | 294 | 3815 px | – |
| /collections/hunde | mobil | 200 | 656 ms | 0 ms | 2755 kB | 294 | 4155 px | – |
| /collections/hunde | desktop | 200 | 692 ms | 0 ms | 2756 kB | 296 | 3104 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 628 ms | 0 ms | 3274 kB | 359 | 5625 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 696 ms | 0 ms | 3673 kB | 350 | 5516 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 656 ms | 0 ms | 3108 kB | 355 | 3524 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 684 ms | 0 ms | 3501 kB | 359 | 3387 px | – |
| /cart | mobil | 200 | 688 ms | 0 ms | 2575 kB | 277 | 996 px | – |
| /cart | desktop | 200 | 544 ms | 0 ms | 2575 kB | 279 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 660 ms | 0 ms | 3045 kB | 354 | 4573 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 540 ms | 0 ms | 3604 kB | 367 | 4273 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1195 kB, other 1028 kB, image 820 kB, font 149 kB, document 66 kB, stylesheet 32 kB
- `/collections/hunde` — script 1263 kB, other 1027 kB, image 211 kB, font 149 kB, document 69 kB, stylesheet 36 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1392 kB, other 1119 kB, image 385 kB, font 149 kB, xhr 94 kB, document 70 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1392 kB, other 1095 kB, image 244 kB, font 149 kB, xhr 94 kB, document 67 kB
- `/cart` — script 1337 kB, other 1005 kB, font 137 kB, document 58 kB, stylesheet 26 kB, image 10 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1351 kB, other 1094 kB, image 221 kB, font 149 kB, xhr 94 kB, document 71 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=970d26a6-caae-4474-a0ba-856f9e99ae0c&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=752db02a-f13b-4f20-a84f-252738d9575c&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ce42daaa-372a-4c5a-93eb-04aa82d5d5f4&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=2f7fe262-02e2-41a1-9db3-f45efb24e56f&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=f79aa44c-97b2-4b42-80fe-bc847619e167&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e5fd70e7-a7de-400f-af1c-96c815b21440&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3b1cda88-2030-44ea-bd54-9c8ce71c32a4&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3448751e-566f-4db3-a195-e6de8e3fff6c&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=3dec2212-1c62-40e0-b0f7-06a4e6dd11fc&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fb3de5dd-7066-4726-a3f8-1ab95c32d07f&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=07fae8e0-8377-46ff-adef-85d4ff9bb2dc&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 30 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d4bdc062-6ec2-46be-9470-d7f7635f6b4c&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 294 Anfragen, davon **30 von 18 fremden Servern** mit 676 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 242 | 2166 | ja |
| cdn.shopify.com | 14 | 449 | ja |
| otlp-http-production.shopifysvc.com | 4 | 0 | ja |
| shop.app | 3 | 0 | **nein** |
| monorail-edge.shopifysvc.com | 3 | 0 | ja |
| www.googletagmanager.com | 3 | 514 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| analytics.tiktok.com | 3 | 45 | **nein** |
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
| metashop.dolphinsuite.com | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (556 kB)
- `bilder/startseite-desktop.jpg` (440 kB)
- `bilder/collections-hunde-mobil.jpg` (612 kB)
- `bilder/collections-hunde-desktop.jpg` (329 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (617 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (398 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (378 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (268 kB)
- `bilder/cart-mobil.jpg` (80 kB)
- `bilder/cart-desktop.jpg` (51 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-mobil.jpg` (453 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-desktop.jpg` (337 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 98 | 93 | 59 | 92 |
| collections-hunde | 67 | 93 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 87 | 91 | 59 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 87 | 90 | 59 | 100 |
| startseite | 97 | 96 | 78 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

