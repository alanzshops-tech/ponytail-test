# Modellvergleich für Produkttexte — Stand 2026-08-10

Dieselben drei echten Produkte an jedes Modell, derselbe Auftrag.
Gemessen wird nicht, ob es schön klingt, sondern ob es Tatsachen
erfindet und die Regeln des Ladens einhält.

**Erfundene Zahlen** sind der teure Fehler: eine Zahl über 10, die
in den Angaben nicht vorkam, steht danach als Zusicherung im Shop
— „waschbar bei 60 Grad“, „3 cm dick“ — ohne dass sie jemand
geprüft hat. Kleine Zählzahlen bleiben außen vor, die sind
Formulierung.

**Denken im Text** ist ein eigener Ausfall, kein erfundener
Fakt: ein Reasoning-Modell ohne gesetztes `reasoning.effort`
liefert seinen Gedankengang als Produkttext aus. Die Zahlen darin
sind Wortzählerei, keine Zusicherungen — deshalb getrennt gezählt.

| Modell | Läufe | Fehler | Wörter ⌀ | erfundene Zahlen | Denken im Text | Maschen | englische Reste | Dauer ⌀ | Kosten |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 3 | 0 | 170 | 0 | 2 | 0 | 6 | 17.7 s | 0.000000 $ |
| `google/gemma-4-31b-it:free` | 3 | **3** | – | – | – | – | – | – | – |
| `google/gemma-4-26b-a4b-it:free` | 3 | 0 | 74 | 0 | 0 | 0 | 0 | 14.4 s | 0.000000 $ |
| `inclusionai/ling-3.0-tiny:free` | 3 | 2 | 67 | 0 | 0 | 0 | 0 | 2.6 s | 0.000000 $ |

## nvidia/nemotron-3-ultra-550b-a55b:free

**gewichtsdecke** — 7.9 s

```
Die Premium Gewichtsdecke in Blau ist in drei Varianten erhältlich: 122 mal 183 Zentimeter mit fünf Kilogramm sowie 135 mal 200 Zentimeter und 137 mal 200 Zentimeter, jeweils mit zehn Kilogramm. Sie gehört zur Kategorie Bett und wird mit den Schlagworten Entspannung, Gewichtsdecke und Schlafzimmer geführt. Der Preis beträgt 74,00 Euro. Das Modell nutzt sanften Druck, um Tiefenentspannung zu fördern und den Schlaf zu verbessern.
```

Befund: nichts zu beanstanden.

**handtuecher** — 11.3 s

```
The user wants a product description for a German online shop selling home accessories.
Constraints:
- Length: 60 to 90 words.
- Only facts from the provided input. No invented specs (dimensions, weight, GSM, temperature, percentages beyond "100% cotton").
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (Fliesstext), no bullet points, no headline.
- Input data: Title (Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig), Category (Bad), Keywords (Bad, Baumwolle, Handtuch-Set), Price (69,00 €), Variants (Schwarz; Grau).

Drafting the text:
Das Premium Handtuch-Set besteht aus 100 % Baumwolle und überzeugt durch eine extra weiche Haptik, hohe Saugkraft und lange Haltbarkeit. Es gehört zur Kategorie Bad und wird in den Farben Schwarz und Grau angeboten. Der Preis beträgt 69,00 €. Das Set eignet sich für den täglichen Gebrauch im Badezimmer und verbindet klassische Materialqualität mit zeitloser Optik. Baumwolle als Naturfaser sorgt für ein angenehmes Hautgefühl und macht die Handtücher zu einer zuverlässigen Grundausstattung.

Word count check (German words):
"Das Premium Handtuch-Set besteht aus 100 % Baumwolle und überzeugt durch eine extra weiche Haptik, hohe Saugkraft und lange Haltbarkeit. (19) Es gehört zur Kategorie Bad und wird in den Farben Schwarz und Grau angeboten. (15) Der Preis beträgt 69,00 €. (5) Das Set eignet sich für den täglichen Gebrauch im Badezimmer und verbindet klassische Material
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

**koerbe** — 34.0 s

```
The user wants a product description for a German online shop.
Constraints:
- Length: 60-90 words.
- Facts only from provided data. No invented specs (dimensions, weight, material, temp, percentages).
- No scarcity, strike-through prices, reviews, claims about other buyers.
- Factual German continuous text (Fließtext), no bullet points, no headline.
- Data provided: Title, Category (Bad), Keywords, Price, Variants (Two sizes in Beige).

Wait, the category is "Bad" (Bathroom), but the title mentions "Kinderzimmer, Wohnzimmer & Schlafzimmer". I must stick to facts. The title *is* a fact provided. The category *is* a fact provided. I should probably mention the category or the usage scenarios from the title.

Let's draft:
"Das Design Aufbewahrungskörbe im 2er-Set bietet stilvolle Ordnung für Kinderzimmer, Wohnzimmer und Schlafzimmer. Die Kategorie Bad weist auf weitere Einsatzmöglichkeiten hin. Erhältlich sind die Körbe in Beige in zwei Varianten: mit den Maßen 28 x 28 cm oder 40 x 25 cm. Das Set kostet 39,00 €. Als Wohnaccessoire eignen sich die Aufbewahrungskörbe zur Organisation verschiedener Gegenstände. Die Schlagworte Aufbewahrungskorb, Ordnung und Wohnaccessoire beschreiben den Verwendungszweck."

Word count check (German words):
"Das Design Aufbewahrungskörbe im 2er-Set bietet stilvolle Ordnung für Kinderzimmer, Wohnzimmer und Schlafzimmer. (14)
Die Kategorie Bad weist auf weitere Einsatzmöglichkeiten hin. (9)
Erhältlich sind die Körbe in Beige in zwei Varianten: mit den Maßen 28 x 28 cm oder 4
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

## google/gemma-4-31b-it:free

**gewichtsdecke** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

**handtuecher** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

**koerbe** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

## google/gemma-4-26b-a4b-it:free

**gewichtsdecke** — 19.8 s

```
Diese Premium Gewichtsdecke für das Schlafzimmer unterstützt die Tiefenentspannung und das Schlafen durch einen sanften Druck. Das Produkt ist in der Farbe Blau erhältlich und wird in drei verschiedenen Ausführungen angeboten. Zur Auswahl stehen die Varianten mit den Maßen 122 x 183 cm und einem Gewicht von 5 kg sowie zwei Modelle mit den Maßen 135 x 200 cm oder 137 x 200 cm, die jeweils 10 kg wiegen. Der Preis für die Gewichtsdecke beträgt 74,00 €.
```

Befund: nichts zu beanstanden.

**handtuecher** — 8.1 s

```
Dieses Premium Handtuch-Set für das Bad besteht aus 100 % Baumwolle. Das Set ist in den Farben Schwarz und Grau erhältlich. Die Textilien sind extra weich, saugstark sowie langlebig. Für einen Preis von 69,00 € erhalten Sie dieses hochwertige Set für Ihre Badezimmerausstattung. Das Produkt kombiniert Funktionalität mit einer angenehmen Haptik und ist eine praktische Ergänzung für Ihr Zuhause. Es eignet sich ideal für den täglichen Gebrauch in Ihrem Bad.
```

Befund: nichts zu beanstanden.

**koerbe** — 15.4 s

```
Dieses Design Aufbewahrungskörbe im 2er-Set bietet eine stilvolle Möglichkeit, Ordnung in Ihrem Wohnzimmer, Schlafzimmer oder Kinderzimmer zu schaffen. Die Körbe dienen als praktische Wohnaccessoires und lassen sich flexibel im Haus oder im Bad einsetzen. Das Set enthält zwei verschiedene Varianten in der Farbe Beige: Ein Korb misst 28 x 28 cm, während der zweite Korb die Maße 40 x 25 cm aufweist. Diese Aufbewahrungskörbe sind für 39,00 € erhältlich und unterstützen eine strukturierte Gestaltung Ihrer Wohnräume.
```

Befund: nichts zu beanstanden.

## inclusionai/ling-3.0-tiny:free

**gewichtsdecke** — 2.6 s

```
Die Premium Gewichtsdecke bietet Tiefenentspannung und unterstützt Sie durch sanften Druck beim Einschlafen. Sie besteht nach den Angaben aus Material, das für einen weichen, angenehmen Liegekomfort sorgt. Die in Blau erhältlichen Varianten sind in verschiedenen Größen und Gewichten verfügbar. Als Bett-Zubehör erfreuen Sie sich an dieser einzigartigen Lösung für einen erholsamen Schlaf. Der Preis liegt bei 74,00 €. Wählen Sie die Variante, die zu Ihren Bedürfnissen passt.
```

Befund: nichts zu beanstanden.

**handtuecher** — 5.4 s

Fehlgeschlagen: leere Antwort 

**koerbe** — 0.6 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"inclusionai/ling-3.0-tiny:free is temporarily rate-limited upstream. Please retry sh

