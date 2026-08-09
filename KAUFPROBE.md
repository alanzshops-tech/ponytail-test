# Kaufprobe und Sichtprüfung

Stand: 2026-08-09T21:15:06+00:00

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
- Produktkacheln gezählt: 28
- Bilder auf der Seite: 25, davon nicht geladen: keine
- mobil: 4338 px hoch, Querscroll nein
- desktop: 4052 px hoch, Querscroll nein
- Leere Abschnitte: keine
- Fehlerhafte Anfrage (mobil): 403 https://shop.app/pay/hop?analytics_trace_id=956291fc-ace3-4a78-bd1c-e6f513431c26&target_origin=https%3A%2F%2Fw
- Fehlerhafte Anfrage (desktop): 403 https://shop.app/pay/hop?analytics_trace_id=7bf52acb-89cf-421f-a218-bf407fff13d0&target_origin=https%3A%2F%2Fw

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

### `/products/led-taschenlampe-aufladbar-zoom-warnlicht` (selbst)

- Seite geladen: HTTP 200
- Preis sichtbar: ja, MwSt-Hinweis: **nein**
- „Ausverkauft" sichtbar: nein
- Kaufknopf gedrückt: ja (product-form button[name='add'])
- Warenkorb danach: **1 Artikel**, 29.99 EUR
- Posten: LED-Taschenlampe aufladbar – 7 Leuchtmodi, Zoom &amp; Warnlicht, USB-C - 1 Stück ×1
- Kasse-Knopf im Warenkorb: 2

### Die Kasse

- Kasse erreichbar: **ja** (HTTP 200)
- Adresse: email, firstName, lastName, address1, postalCode, city
- Zahlarten vor Adresseingabe: PayPal, Kreditkarte, Rechnung
- Zahlarten nach Adresseingabe: **PayPal, Kreditkarte, Rechnung**
- Versandzeile: „Lieferung"
- Versandzeile: „Versand"
- Versandzeile: „Wähle eine Versandart aus"
- Versandzeile: „Versand"
- Versandzeile: „Neuer Gesamtpreis: 39,98 € EURAktualisierte Versandart: Auslandsversand (bis 2kg)"

Es wurde nichts bezahlt und nichts bestellt. Im Adminbereich erscheint ein abgebrochener Warenkorb auf `kaufprobe-test@example.com` — das ist der Beleg des Tests.

