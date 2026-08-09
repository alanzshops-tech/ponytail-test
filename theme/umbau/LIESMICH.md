# Theme-Umbau

Diese Dateien werden in die **unveröffentlichte** Theme-Kopie
„Umbau Conversion – Claude" geschrieben, nicht in das laufende Theme.
Shopify holt sie über die öffentliche Rohadresse dieses Repositories ab.

## index.json — Startseite

Entfernt gegenüber dem Original:

- **Elf erfundene Kundenbewertungen.** Der Shop hatte 2026 null
  Bestellungen; die Bewertungen sind auf März 2026 datiert. Gefälschte
  Bewertungen stehen auf der schwarzen Liste des UWG (Anhang zu § 3
  Abs. 3, Nr. 23b/23c) und sind ohne Abwägung unzulässig.
- Drei leere Rich-Text-Abschnitte.
- Ein abgeschalteter Carousel-App-Block, der trotzdem geladen wurde.

Geändert:

- Bestseller von **24 auf 8** Produkte. Das war die Hauptursache für
  265 Anfragen und 12 Bildschirmlängen Seitenhöhe.
- Kategorien am Handy **zweispaltig** statt einspaltig, und von acht auf
  sechs gekürzt.
- FAQ und Zahlungslogos kompakter, mit `loading="lazy"` und festen
  Bildmaßen, damit nichts nachträglich springt.

Behalten: Hero, Vertrauenszeile, der aktive Carousel-Block.

Von 28.871 auf 10.661 Zeichen.
