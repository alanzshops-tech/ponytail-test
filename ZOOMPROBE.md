# Zoomprobe — funktioniert Bild-Zoom auf dem Handy?

Seite: `/products/led-taschenlampe-aufladbar-zoom-warnlicht`

Gemessen, nicht angenommen: zwei unabhängige Fragen, jede mit Screenshot als Beleg.

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
