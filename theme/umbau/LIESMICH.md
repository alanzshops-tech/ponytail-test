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

## Nachtrag vom 9. August 2026, nach der Kaufprobe

Drei Korrekturen, alle durch Messung ausgelöst, nicht durch Nachdenken:

1. **Zahlarten in der FAQ.** Ich hatte „PayPal, Klarna, Apple Pay, Google
   Pay, Kreditkarte und SEPA" geschrieben. Die Kasse bietet Kreditkarte,
   PayPal, Klarna und Banküberweisung an, dazu Shop Pay und Google Pay
   als Express-Knöpfe. SEPA gibt es nicht. Eine erfundene Zahlart ist
   dieselbe Sorte Behauptung wie eine erfundene Bewertung.

2. **Karussell entfernt.** Es zeigte exakt dieselben sechs Kategorien wie
   der Abschnitt „Kategorien" 1500 Pixel weiter unten — gemessen, nicht
   geschätzt. Zweimal dieselbe Navigation auf einer Seite.

3. **„Bestseller" heißt jetzt „Unsere Auswahl".** Der Abschnitt zog aus
   einer automatischen Kollektion, deren Regel „alles über 10 €" lautet.
   Von den sechs Artikeln, die in drei Jahren tatsächlich verkauft
   wurden, ist keiner mehr im Sortiment. Es gab also nichts, worauf sich
   das Wort hätte stützen können.
