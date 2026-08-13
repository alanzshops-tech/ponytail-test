# Zoomprobe — funktioniert Bild-Zoom auf dem Handy?

Seite: `/products/led-taschenlampe-aufladbar-zoom-warnlicht`

Gemessen, nicht angenommen: zwei unabhängige Fragen, jede mit Screenshot als Beleg.

## 0. Herkunft des "Vertrag widerrufen"-Buttons

Elternpfad vom Button nach oben, bis zu 6 Ebenen:

0. `<button>` class="widerruf-trigger-button widerruf-trigger-button--floating widerruf-trigger-button--floating-left" data-widerruf-popup-open="" data-widerruf-popup-bound="true"
1. `<div>` class="widerruf-popup-source widerruf-popup-source--embed" data-widerruf-popup-source-root="true" data-widerruf-popup-source="" data-widerruf-popup-source-kind="embed" data-widerruf-popup-css-url="https://cdn.shopify.com/extensions/019fe83d-98b8-7eb3-9910-09ce4c58d9cc/revoq-eu-withdrawal

**Fremde Skript-Adressen auf der Seite** (11, ohne shopify.com/homeeins.de selbst):

- `https://cdn-bundler.nice-team.net/app/js/bundler.js?shop=7a0a31.myshopify.com`
- `https://cdn.trustedsite.com/js/partner-shopify.js?shop=7a0a31.myshopify.com`
- `https://metashop.dolphinsuite.com/ow_static/plugins/biolink/js/clicktracking.js?t=1706697725&shop=7a0a31.myshopify.com`
- `https://app.cjdropshipping.com/static/shopify/pod/cjpodflag.js?shop=7a0a31.myshopify.com`
- `https://www.googletagmanager.com/gtag/js?id=GT-K55447S&cx=c&gtm=4e68c0`
- `https://connect.facebook.net/en_US/fbevents.js`
- `https://shop.app/checkouts/internal/preloads.js?locale=de-US&shop_id=75888525635`
- `https://bundler.nice-team.net/app/shop/status/7a0a31.myshopify.com.js?1786642353`
- `https://cdn-bundler.nice-team.net/app/js/bundler-script.js?shop=7a0a31.myshopify.com&1785857358`
- `https://www.googletagmanager.com/gtag/js?id=G-138EQ9NKMZ`
- `https://www.googletagmanager.com/gtag/js?id=GT-K55447S`

## 1. Erlaubt das Viewport-Meta-Tag Pinch-Zoom?

`width=device-width,initial-scale=1`

**Pinch-Zoom technisch möglich: ja**

## 2. Öffnet ein Tap auf das Bild eine vergrößerte Ansicht?

Bild-Selektor gefunden: `.product__media img`
**Dialog/Modal nach einfachem Tap geöffnet: nein**
**Dialog/Modal nach Doppeltipp geöffnet: nein**
Seitenzustand hat sich nach dem Tap überhaupt verändert: nein
Tap-Fehler: Locator.tap: Timeout 8000ms exceeded.
Call log:
  - waiting for locator(".product__media img").first
    - locator resolved to <img width="1946" height="1946" class="image-magnify-lightbox" alt="LED-T
Doppeltipp-Fehler: Locator.dblclick: Timeout 8000ms exceeded.
Call log:
  - waiting for locator(".product__media img").first
    - locator resolved to <img width="1946" height="1946" class="image-magnify-lightbox" alt="

Screenshots: `bilder/zoomprobe-1-vorher.jpg`, `bilder/zoomprobe-2-nach-tap.jpg`, `bilder/zoomprobe-3-doppeltipp.jpg`

## Einordnung

Weder Tap noch Doppeltipp haben ein Modal geöffnet, und das Meta-Tag blockiert nicht. Das ist kein Beweis, dass gar kein Zoom existiert — es kann auch ein anderer Auslöser sein (z. B. ein eigenes Zoom-Symbol), der hier nicht gefunden wurde. Die Screenshots vorher/nachher zeigen den tatsächlichen Zustand.
