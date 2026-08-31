# Shop-Messung

Stand: 2026-08-31

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 680 ms | 0 ms | 3365 kB | 383 | 4212 px | – |
| / | desktop | 200 | 576 ms | 0 ms | 3426 kB | 379 | 4047 px | – |
| /collections/hunde | mobil | 200 | 648 ms | 0 ms | 2812 kB | 374 | 4641 px | – |
| /collections/hunde | desktop | 200 | 712 ms | 0 ms | 2835 kB | 384 | 3365 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 424 ms | 0 ms | 3154 kB | 428 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 424 ms | 0 ms | 3624 kB | 430 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 312 ms | 0 ms | 3010 kB | 420 | 4065 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 384 ms | 0 ms | 3401 kB | 421 | 3844 px | – |
| /cart | mobil | 200 | 344 ms | 0 ms | 2682 kB | 365 | 1077 px | – |
| /cart | desktop | 200 | 240 ms | 0 ms | 2658 kB | 365 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 412 ms | 0 ms | 3007 kB | 427 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 348 ms | 0 ms | 3523 kB | 433 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 380 ms | 0 ms | 3119 kB | 419 | 4389 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 332 ms | 0 ms | 3360 kB | 424 | 4188 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1328 kB, other 914 kB, image 820 kB, font 212 kB, stylesheet 45 kB, document 45 kB
- `/collections/hunde` — script 1400 kB, other 891 kB, font 212 kB, image 211 kB, document 49 kB, stylesheet 49 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1528 kB, other 916 kB, image 385 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1528 kB, other 916 kB, image 244 kB, font 212 kB, stylesheet 60 kB, document 49 kB
- `/cart` — script 1475 kB, other 916 kB, font 200 kB, document 40 kB, stylesheet 39 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1569 kB, other 893 kB, image 220 kB, font 212 kB, stylesheet 60 kB, document 51 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1567 kB, other 914 kB, image 315 kB, font 212 kB, stylesheet 60 kB, document 49 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=db65a908-8226-46c2-a801-1b6472253a06&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=fa1039d9-fc12-485e-8b0c-1a796aa4620d&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=718f36c9-9cde-4df3-97c1-5a8fe84653ab&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=edc99ab4-2c82-4dfa-914f-8191af283043&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=22ae8556-9cb9-4a76-bd67-919402a12896&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=baecaece-5cb5-4e32-a723-f5602e636c18&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d579579d-bc1e-4ae5-9411-7d4aa191a309&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a32ca924-29ae-42a6-a4ee-fdbfb6217b88&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=31dd10bf-9b82-4181-bb6f-24260ada548f&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5289a877-91dc-4edd-800f-bdc43f758fb8&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=0e36abb1-0e47-4a13-a412-904f1f469781&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=a3ace37d-0b31-4b11-aef0-fa4e4866e8b5&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=b8bf80c3-5149-40e1-9e5a-af9d7e397800&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=5513a1a0-df05-4464-adcd-a7560ffab5f9&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 383 Anfragen, davon **33 von 18 fremden Servern** mit 646 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 242 | 2044 | ja |
| cdn.shopify.com | 90 | 674 | ja |
| otlp-http-production.shopifysvc.com | 10 | 0 | ja |
| monorail-edge.shopifysvc.com | 6 | 0 | ja |
| shop.app | 5 | 0 | **nein** |
| analytics.tiktok.com | 4 | 44 | **nein** |
| www.googletagmanager.com | 3 | 484 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 105 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| bundler.nice-team.net | 1 | 0 | **nein** |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |
| error-analytics-sessions-production.shopifysvc | 1 | 0 | ja |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (562 kB)
- `bilder/startseite-desktop.jpg` (473 kB)
- `bilder/collections-hunde-mobil.jpg` (681 kB)
- `bilder/collections-hunde-desktop.jpg` (378 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (690 kB)
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
| cart | 97 | 93 | 59 | 92 |
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 89 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 87 | 90 | 56 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 86 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 90 | 56 | 100 |
| startseite | 76 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

