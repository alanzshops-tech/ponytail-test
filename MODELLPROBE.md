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
| `nvidia/nemotron-3-ultra-550b-a55b:free@none` | 3 | 2 | 62 | 0 | 0 | 0 | 0 | 6.7 s | 0.000000 $ |
| `nvidia/nemotron-3-ultra-550b-a55b:free@minimal` | 3 | 0 | 216 | 0 | 3 | 0 | 10 | 20.5 s | 0.000000 $ |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 3 | 1 | 148 | 0 | 1 | 0 | 4 | 16.4 s | 0.000000 $ |
| `google/gemma-4-26b-a4b-it:free` | 3 | 2 | 76 | 0 | 0 | 0 | 0 | 1.8 s | 0.000000 $ |

## nvidia/nemotron-3-ultra-550b-a55b:free@none

**gewichtsdecke** — 6.7 s

```
Die Premium Gewichtsdecke in Blau ist in den Maßen 122 mal 183 Zentimeter mit fünf Kilogramm sowie 135 mal 200 Zentimeter und 137 mal 200 Zentimeter mit jeweils zehn Kilogramm erhältlich. Sie gehört zur Kategorie Bett und wird den Schlagworten Entspannung, Gewichtsdecke und Schlafzimmer zugeordnet. Der Preis beträgt 74,00 Euro. Der Titel nennt Tiefenentspannung und besseres Schlafen durch sanften Druck als Produktmerkmal.
```

Befund: nichts zu beanstanden.

**handtuecher** — 0.3 s

Fehlgeschlagen: leere Antwort 

**koerbe** — 0.5 s

Fehlgeschlagen: leere Antwort 

## nvidia/nemotron-3-ultra-550b-a55b:free@minimal

**gewichtsdecke** — 27.0 s

```
The user wants a product description for a weighted blanket (Gewichtsdecke) for a German online shop.
Constraints:
- Length: 60-90 words.
- Facts only from the provided data (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weights, materials, temperatures, percentages).
- No scarcity, strikethrough prices, reviews, social proof.
- Factual German continuous text (Fließtext), no lists, no headlines.

Data:
- Title: Premium Gewichtsdecke – Tiefenentspannung & besser schlafen mit sanftem Druck
- Category: Bett
- Keywords: Entspannung, Gewichtsdecke, Schlafzimmer
- Price: 74,00 €
- Variants:
  1. Blau / 122 x 183 cm / 5 kg
  2. Blau / 135 x 200 cm / 10 kg
  3. Blau / 137 x 200 cm / 10 kg

Drafting the text (mental or scratchpad):
Die Premium Gewichtsdecke in der Kategorie Bett ist in der Farbe Blau erhältlich. Sie wird in drei Varianten angeboten: mit den Maßen 122 mal 183 Zentimeter und einem Gewicht von 5 Kilogramm sowie in den Größen 135 mal 200 Zentimeter und 137 mal 200 Zentimeter, jeweils mit 10 Kilogramm. Das Modell eignet sich für das Schlafzimmer und unterstützt Entspannung durch sanften Druck. Der Preis beträgt 74,00 Euro.

Word count check (German words):
"Die Premium Gewichtsdecke in der Kategorie Bett ist in der Farbe Blau erhältlich. Sie wird in drei Varianten angeboten: mit den Maßen
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

**handtuecher** — 11.5 s

```
The user wants a product description for a German online shop selling home accessories.
Constraints:
- Length: 60-90 words.
- Facts only from provided data (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weight, GSM, temperature, percentages other than 100% cotton).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (no bullet points, no headlines).
- Language: German.

Provided data:
- Title: Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig
- Category: Bad
- Keywords: Bad, Baumwolle, Handtuch-Set
- Price: 69,00 €
- Variants: Schwarz; Grau

Drafting ideas:
Focus on material (100% cotton), properties from title (soft, absorbent, durable), category (bathroom), variants (black, grey), price.

Draft 1 (Mental):
Das Premium Handtuch-Set besteht aus 100 % Baumwolle und überzeugt durch eine extra weiche Haptik, hohe Saugkraft und lange Haltbarkeit. Es eignet sich ideal für das Bad und ist in den Farben Schwarz und Grau erhältlich. Der Preis beträgt 69,00 €.

Word count check (German words):
Das (1) Premium (2) Handtuch-Set (3) besteht (4) aus (5) 100 (6) % (7) Baumwolle (8) und (9) überzeugt (10) durch (11) eine (12) extra (13) weiche (14) Haptik, (15) hohe (16) Saugkraft (17) und (18) lange (19)
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, soft, the

**koerbe** — 22.9 s

```
The user wants a product description for a German online shop.
Constraints:
- Length: 60-90 words.
- Only facts from the provided input.
- No invented specs (dimensions, weight, material, temp, percentages).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German running text (Fliesstext), no bullet points, no headline.
- Input data: Title, Category (Bad), Keywords, Price, Variants (Beige / 28x28cm; Beige / 40x25cm).

Wait, the title says "Kinderzimmer, Wohnzimmer & Schlafzimmer" but the Category is "Bad" (Bathroom). I must stick to facts. The title is a fact (it's the product title). The category is a fact. I should probably mention the category or the use cases mentioned in the title. The variants have dimensions. I can use those. Material is not given, so I must not invent it (e.g., "aus Rattan" or "aus Stoff" is forbidden). Price is given.

Drafting text (mental):
"Das Design-Aufbewahrungskörbe-Set zum Preis von 39,00 € umfasst zwei Körbe in Beige. Die Varianten unterscheiden sich in den Abmessungen: Ein Modell misst 28 x 28 cm, das andere 40 x 25 cm. Laut Titel eignen sie sich für Kinderzimmer, Wohnzimmer und Schlafzimmer, sind jedoch der Kategorie Bad zugeordnet. Als Wohnaccessoires dienen sie der Ordnung und Aufbewahrung. Das Set wird als 2er-Set angeboten."

Word count check:
"Das Design-Aufbewahrungskörbe-Set zum Preis von 39,00 € umfasst zwei Körbe in Beige." (14 words)
"Die Varianten unterscheiden sich in den Ab
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

## nvidia/nemotron-3-ultra-550b-a55b:free

**gewichtsdecke** — 5.4 s

```
Die Premium Gewichtsdecke in Blau. Blau wird in drei Varianten angeboten: 122 mal 183 Zentimeter mit fünf Kilogramm sowie 135 mal 200 Zentimeter und 137 mal 200 Zentimeter, jeweils mit zehn Kilogramm. Die Decke gehört zur Kategorie Bett und ist den Themen Entspannung, Gewichtsdecke und Schlafzimmer zugeordnet. Der Preis beträgt 74,00 Euro. Der sanfte Druck der Decke unterstützt die Tiefenentspannung und kann das Einschlafen sowie die Schlafqualität verbessern.
```

Befund: nichts zu beanstanden.

**handtuecher** — 45.1 s

Fehlgeschlagen: IncompleteRead(1177 bytes read) 

**koerbe** — 27.3 s

```
The user wants a product description for a German online shop for home accessories.
Constraints:
- Length: 60-90 words.
- Only facts from the provided data. No invented specs (dimensions, weight, material, temp, percentages).
- No scarcity, no strike-through prices, no reviews, no claims about other buyers.
- Factual German continuous text (Fließtext), no bullet points, no headline.
- Data provided: Title, Category (Bad), Keywords, Price, Variants (Beige / 28x28cm; Beige / 40x25cm).

Wait, the title says "Kinderzimmer, Wohnzimmer & Schlafzimmer" but the category is "Bad" (Bathroom). I must use the facts provided. The category is "Bad". The title mentions other rooms. I should probably mention the category or the usage scenarios from the title, but stick to facts. The title *is* a fact provided. The category *is* a fact provided. I will combine them carefully.

Variants: Two sizes, both Beige. 28x28cm and 40x25cm. It's a 2er-Set (2-piece set). Price 39,00 €.

Drafting text (German):
"Das Design Aufbewahrungskörbe im 2er-Set wird in der Kategorie Bad geführt und eignet sich für Kinderzimmer, Wohnzimmer und Schlafzimmer. Die beiden Körbe in Beige haben die Maße 28 mal 28 Zentimeter sowie 40 mal 25 Zentimeter. Sie dienen als Wohnaccessoire zur Ordnung. Der Preis für das Set beträgt 39,00 Euro."

Word count check:
"Das Design Aufbewahrungskörbe im 2er-Set wird in der Kategorie Bad geführt und eignet sich für Kinderzimmer, Wohnzimmer und Schlafzimmer
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: and, for, from, the

## google/gemma-4-26b-a4b-it:free

**gewichtsdecke** — 0.1 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream. Please retry sh

**handtuecher** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream. Please retry sh

**koerbe** — 1.8 s

```
Dieses Design Aufbewahrungskörbe im 2er-Set bietet eine stilvolle Möglichkeit, für Ordnung in Ihrem Zuhause zu sorgen. Die Körbe können vielseitig im Kinderzimmer, Wohnzimmer, Schlafzimmer oder im Bad eingesetzt werden. Das Set umfasst zwei verschiedene Varianten in der Farbe Beige. Zur Auswahl stehen eine Größe von 28 x 28 cm sowie eine Größe von 40 x 25 cm. Als praktisches Wohnaccessoire lassen sich die Körbe flexibel zur Aufbewahrung nutzen. Der Preis für dieses Set beträgt 39,00 €.
```

Befund: nichts zu beanstanden.

