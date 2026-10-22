# Shop-Messung

Stand: 2026-10-22

Gemessen mit einem echten Browser auf dem Runner, Sprache de-DE. **Mobil** entspricht einem iPhone (390 px), **Desktop** einem Laptop (1440 px).

> Das sind Mängelmessungen, keine Conversion-Tests. Für Tests bräuchte es Besucher — die Zahlen hier gelten auch ohne.

| Seite | Gerät | Status | Erste Anzeige | Größtes Element | Gewicht | Anfragen | Höhe | Querscroll |
|---|---|---:|---:|---:|---:|---:|---:|:-:|
| / | mobil | 200 | 856 ms | 0 ms | 3386 kB | 400 | 4211 px | – |
| / | desktop | 200 | 840 ms | 0 ms | 3473 kB | 392 | 4047 px | – |
| /collections/hunde | mobil | 200 | 472 ms | 0 ms | 2941 kB | 393 | 4352 px | – |
| /collections/hunde | desktop | 200 | 452 ms | 0 ms | 2940 kB | 392 | 3365 px | – |
| /products/hundesofa-samt-erhoeht-xxl | mobil | 200 | 348 ms | 0 ms | 3299 kB | 435 | 6297 px | – |
| /products/hundesofa-samt-erhoeht-xxl | desktop | 200 | 480 ms | 0 ms | 3731 kB | 439 | 6082 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | mobil | 200 | 420 ms | 0 ms | 3545 kB | 395 | 4211 px | – |
| /products/sitzbank-stauraum-gepolstert-klappbar | desktop | 200 | 528 ms | 0 ms | 3457 kB | 394 | 4047 px | – |
| /cart | mobil | 200 | 352 ms | 0 ms | 2858 kB | 376 | 1077 px | – |
| /cart | desktop | 200 | 332 ms | 0 ms | 2857 kB | 375 | 900 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | mobil | 200 | 352 ms | 0 ms | 3126 kB | 431 | 5646 px | – |
| /products/samt-sessel-design-armlehnen-holzbeine | desktop | 200 | 496 ms | 0 ms | 3669 kB | 442 | 5372 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | mobil | 200 | 408 ms | 0 ms | 3548 kB | 399 | 4211 px | – |
| /products/led-taschenlampe-aufladbar-zoom-warnlicht | desktop | 200 | 580 ms | 0 ms | 3518 kB | 390 | 4047 px | – |

Richtwerte von Google: Das größte Element sollte nach **2500 ms** stehen, alles darüber gilt als verbesserungswürdig. Ein Seitengewicht über **2000 kB** ist auf Mobilfunk spürbar.

## Was schwer wiegt

- `/` — script 1458 kB, other 873 kB, image 760 kB, font 212 kB, stylesheet 82 kB, fetch 1 kB
- `/collections/hunde` — script 1563 kB, other 868 kB, font 212 kB, image 187 kB, stylesheet 61 kB, document 49 kB
- `/products/hundesofa-samt-erhoeht-xxl` — script 1697 kB, other 873 kB, image 389 kB, font 212 kB, stylesheet 73 kB, document 52 kB
- `/products/sitzbank-stauraum-gepolstert-klappbar` — script 1598 kB, other 871 kB, image 760 kB, font 212 kB, stylesheet 58 kB, document 47 kB
- `/cart` — script 1683 kB, other 870 kB, font 200 kB, stylesheet 52 kB, document 42 kB, image 11 kB
- `/products/samt-sessel-design-armlehnen-holzbeine` — script 1696 kB, other 870 kB, image 221 kB, font 212 kB, stylesheet 73 kB, document 53 kB
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` — script 1597 kB, other 874 kB, image 760 kB, font 212 kB, stylesheet 58 kB, document 47 kB

## Befunde

- `/` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ce432485-54c0-40f3-ab14-fd767c7b278d&target_origin=https%3A%2F%2Fw
- `/` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c1cfd8ce-5488-43b5-aa30-8d699bb46014&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=7e07d9ba-eb11-4adb-b165-6412af91bcc0&target_origin=https%3A%2F%2Fw
- `/collections/hunde` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=d614365c-abbb-443b-9849-5b5f80d2487b&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=ce2055a4-041b-473f-aff3-cf28d4e88af4&target_origin=https%3A%2F%2Fw
- `/products/hundesofa-samt-erhoeht-xxl` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=4ee80438-e262-4d4d-86a3-1a8cefaa2c30&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=44a1c442-6eee-45a0-b776-785470e763da&target_origin=https%3A%2F%2Fw
- `/products/sitzbank-stauraum-gepolstert-klappbar` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/products/sitzbank-stauraum-gepolstert-klappbar` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=6a1e6159-758c-4ce7-abd0-6a36b76b4e38&target_origin=https%3A%2F%2Fw
- `/cart` hat 2 H1-Überschriften statt einer
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e817611b-ff27-4f65-b3c3-bdc1a9a484ba&target_origin=https%3A%2F%2Fw
- `/cart` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=c7c32689-312e-4b0f-be05-984283dec53a&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (mobil): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=90a5b07b-3284-4b9b-bad7-76ce8123ae11&target_origin=https%3A%2F%2Fw
- `/products/samt-sessel-design-armlehnen-holzbeine` (desktop): 9 von 29 Bildern ohne Alt-Text
- `/products/samt-sessel-design-armlehnen-holzbeine` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=005a1e10-3e11-468a-85ed-fbed51009ece&target_origin=https%3A%2F%2Fw
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` (mobil): 1 von 19 Bildern ohne Alt-Text
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` (desktop): 1 von 19 Bildern ohne Alt-Text
- `/products/led-taschenlampe-aufladbar-zoom-warnlicht` lädt etwas, das fehlschlägt: https://shop.app/pay/hop?analytics_trace_id=e0ac7d7c-1453-419e-9925-4f646d2ecbc6&target_origin=https%3A%2F%2Fw

## Woher die Anfragen kommen

Nur Startseite, mobil. **Fremd** heißt: nicht von homeeins.de und nicht von Shopify selbst — also Apps und Dienste Dritter.

Insgesamt 400 Anfragen, davon **34 von 17 fremden Servern** mit 673 kB.

| Absender | Anfragen | kB | eigen |
|---|---:|---:|:-:|
| www.homeeins.de | 204 | 1896 | ja |
| cdn.shopify.com | 73 | 646 | ja |
| shopify-assets.shopifycdn.com | 66 | 170 | ja |
| otlp-http-production.shopifysvc.com | 14 | 0 | ja |
| shop.app | 7 | 0 | **nein** |
| monorail-edge.shopifysvc.com | 7 | 0 | ja |
| analytics.tiktok.com | 4 | 46 | **nein** |
| www.googletagmanager.com | 3 | 502 | **nein** |
| ct.pinterest.com | 3 | 0 | **nein** |
| connect.facebook.net | 2 | 112 | **nein** |
| cdn-bundler.nice-team.net | 2 | 1 | **nein** |
| s3-us-west-2.amazonaws.com | 2 | 0 | **nein** |
| cdn.ywxi.net | 2 | 7 | **nein** |
| analytics.google.com | 1 | 0 | **nein** |
| stats.g.doubleclick.net | 1 | 0 | **nein** |
| www.merchant-center-analytics.goog | 1 | 0 | **nein** |
| analytics-ipv6.tiktokw.us | 1 | 0 | **nein** |
| forms.shopifyapps.com | 1 | 0 | ja |
| app.cjdropshipping.com | 1 | 0 | **nein** |
| cdn.trustedsite.com | 1 | 5 | **nein** |
| www.cjdropshipping.com | 1 | 0 | **nein** |
| error-analytics-sessions-production.shopifysvc | 1 | 0 | ja |

## Bilder

Vollständige Seitenfotos liegen in `bilder/`.

- `bilder/startseite-mobil.jpg` (535 kB)
- `bilder/startseite-desktop.jpg` (451 kB)
- `bilder/collections-hunde-mobil.jpg` (645 kB)
- `bilder/collections-hunde-desktop.jpg` (358 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-mobil.jpg` (692 kB)
- `bilder/products-hundesofa-samt-erhoeht-xxl-desktop.jpg` (446 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-mobil.jpg` (535 kB)
- `bilder/products-sitzbank-stauraum-gepolstert-klappbar-desktop.jpg` (450 kB)
- `bilder/cart-mobil.jpg` (87 kB)
- `bilder/cart-desktop.jpg` (53 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-mobil.jpg` (556 kB)
- `bilder/products-samt-sessel-design-armlehnen-holzbeine-desktop.jpg` (409 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-mobil.jpg` (535 kB)
- `bilder/products-led-taschenlampe-aufladbar-zoom-warnlicht-desktop.jpg` (450 kB)

## Lighthouse (Google-Bewertung, Desktop)

| Seite | Tempo | Barrierefreiheit | Praxis | SEO |
|---|---:|---:|---:|---:|
| cart | 68 | 93 | 59 | 92 |
| collections-hunde | 67 | 94 | 59 | 100 |
| products-hundesofa-samt-erhoeht-xxl | 88 | 90 | 56 | 100 |
| products-led-taschenlampe-aufladbar-zoom-warnlicht | 89 | 93 | 59 | 100 |
| products-samt-sessel-design-armlehnen-holzbeine | 89 | 90 | 56 | 100 |
| products-sitzbank-stauraum-gepolstert-klappbar | 89 | 93 | 59 | 100 |
| startseite | 86 | 93 | 59 | 100 |

Skala 0 bis 100. Unter 50 ist rot, ab 90 gut.

