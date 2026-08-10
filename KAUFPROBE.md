# Kaufprobe und Sichtprüfung

Stand: 2026-08-10T07:57:15+00:00

Zwei Fragen, beide nur im Browser beantwortbar: Sieht die umgebaute Startseite richtig aus, und kann man einkaufen?

## 1. Die Theme-Kopie

Vorschau: `https://www.homeeins.de/?preview_theme_id=182664626499`

- Erfundene Bewertungen im sichtbaren Text: **keine**
- Banner mit Überschrift: ja
- Vertrauenszeile: ja
- Bestseller-Reihe: ja
- Zahlungslogos: ja
- Kategoriekacheln: ja
- FAQ: ja
- Produktkacheln gezählt: 16
- Bilder auf der Seite: 19, davon nicht geladen: keine
- mobil: 4079 px hoch, Querscroll nein
- desktop: 3815 px hoch, Querscroll nein
- Karussell oben: –
- Kategoriekacheln unten: Haustiere, Möbel, Ordnung & Aufbewahrung, Wohnen & Deko, Garten & Outdoor, Bad & Wellness
- **Doppelt auf einer Seite: nichts**
- Leere Abschnitte: keine
- Fehlerhafte Anfrage (mobil): 403 https://shop.app/pay/hop?analytics_trace_id=15f1f725-4275-4c03-ae0e-6bafe2ea26ab&target_origin=https%3A%2F%2Fw
- Fehlerhafte Anfrage (desktop): 403 https://shop.app/pay/hop?analytics_trace_id=b4c9dc8c-61e6-4b08-998d-77fadd58323f&target_origin=https%3A%2F%2Fw

Bilder: `bilder/vorschau-mobil.jpg`, `bilder/vorschau-desktop.jpg`

## 2. Kann man einkaufen?

### `/products/vorratsbehaelter-luftdicht-schwarz` (bestand)

- Seite geladen: HTTP 200
- Preis sichtbar: ja, MwSt-Hinweis: **nein**
- „Ausverkauft" sichtbar: nein
- Kaufknopf gedrückt: ja (product-form button[name='add'])
- Warenkorb danach: **1 Artikel**, 24.99 EUR
- Posten: Vorratsbehälter mit Deckel – Luftdicht für Küche &amp; Speisekammer - BLACK ×1
- Kasse-Knopf im Warenkorb: 2
- Fehlende Dateien (404): keine
- Konsole: 4 Meldungen

    - `error: Framing 'https://shop.app/' violates the following Content Security Policy directive: "frame-ancestors 'self' https://shop.app https://admin.shopify.c`
    - `error: Failed to load resource: the server responded with a status of 403 ()`
    - `error: Error producing monorail event MonorailRequestError: Error completing request. A network failure may have prevented the request from completing. Error`
    - `error: TypeError: Cannot read properties of null (reading 'flags')
    at https://www.homeeins.de/web-pixels/strict/app/web-pixel-2008940867@b3ceb6b433982c0c`

### `/products/led-taschenlampe-aufladbar-zoom-warnlicht` (selbst)

- Seite geladen: HTTP 200
- Preis sichtbar: ja, MwSt-Hinweis: **nein**
- „Ausverkauft" sichtbar: nein
- Kaufknopf gedrückt: ja (product-form button[name='add'])
- Warenkorb danach: **1 Artikel**, 29.99 EUR
- Posten: LED-Taschenlampe aufladbar – 7 Leuchtmodi, Zoom &amp; Warnlicht, USB-C - 1 Stück ×1
- Kasse-Knopf im Warenkorb: 2
- Fehlende Dateien (404): keine
- Konsole: 4 Meldungen

    - `error: Framing 'https://shop.app/' violates the following Content Security Policy directive: "frame-ancestors 'self' https://shop.app https://admin.shopify.c`
    - `error: Failed to load resource: the server responded with a status of 403 ()`
    - `error: Error producing monorail event MonorailRequestError: Error completing request. A network failure may have prevented the request from completing. Error`
    - `error: TypeError: Cannot read properties of null (reading 'flags')
    at https://www.homeeins.de/web-pixels/strict/app/web-pixel-2008940867@b3ceb6b433982c0c`

### Die Kasse

- Kasse erreichbar: **ja** (HTTP 200)
- Land voreingestellt: `US`, umgestellt auf: `DE`
- Adresse: email, firstName, lastName, address1, postalCode, city
- Gesamtpreis in der Kasse: **24,99 €**
- Zahlarten vor Adresseingabe: PayPal, Kreditkarte, Banküberweisung
- Zahlarten nach Adresseingabe: **PayPal, Klarna, Kreditkarte, Banküberweisung**
- Versandzeile: „Lieferung"
- Versandzeile: „Versand"
- Versandzeile: „Wähle eine Versandart aus"
- Versandzeile: „Kostenloser Versand"
- Versandzeile: „Versand"
- Versandzeile: „Aktualisierte Versandart: Kostenloser Versand"

Der Zahlungsabschnitt im Wortlaut:

```
Zahlung
```

Es wurde nichts bezahlt und nichts bestellt. Im Adminbereich erscheint ein abgebrochener Warenkorb auf `kaufprobe-test@example.com` — das ist der Beleg des Tests.

