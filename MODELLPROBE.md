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
| `nvidia/nemotron-3-ultra-550b-a55b:free@medium` | 3 | 0 | 214 | 0 | 3 | 0 | 9 | 12.6 s | 0.000000 $ |
| `nvidia/nemotron-3-ultra-550b-a55b:free@high` | 3 | 0 | 168 | 0 | 2 | 0 | 7 | 10.8 s | 0.000000 $ |
| `google/gemma-4-26b-a4b-it:free` | 3 | 0 | 75 | 0 | 0 | 0 | 0 | 6.9 s | 0.000000 $ |

## nvidia/nemotron-3-ultra-550b-a55b:free@medium

**gewichtsdecke** — 9.5 s

```
The user wants a product description for a German online shop.
Constraints:
- 60-90 words.
- Only facts from the provided data (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weights, materials, temps, percentages).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (fließtext), no bullet points, no headlines.

Data:
- Title: Premium Gewichtsdecke – Tiefenentspannung & besser schlafen mit sanftem Druck
- Category: Bett
- Keywords: Entspannung, Gewichtsdecke, Schlafzimmer
- Price: 74,00 €
- Variants: Blau / 122 x 183 cm / 5 kg; Blau / 135 x 200 cm / 10 kg; Blau / 137 x 200 cm / 10 kg

Drafting:
Die Premium Gewichtsdecke in der Kategorie Bett unterstützt Entspannung und Schlaf durch sanften Druck. Erhältlich in Blau mit den Maßen 122 mal 183 Zentimeter bei fünf Kilogramm sowie 135 mal 200 Zentimeter und 137 mal 200 Zentimeter jeweils mit zehn Kilogramm. Das Modell eignet sich für das Schlafzimmer und kostet 74,00 Euro.

Word count check (German words):
Die (1) Premium (2) Gewichtsdecke (3) in (4) der (5) Kategorie (6) Bett (7) unterstützt (8) Entspannung (9) und (10) Schlaf (11) durch (12) sanften (13) Druck (14). Erhältlich (15) in (16) Blau (17)
```

**Befund:** Denken im Text: constraints:, drafting:, the user wants, word count; englisch: for, from, the

**handtuecher** — 19.4 s

```
The user wants a product description for a German online shop selling home accessories.
Constraints:
- Length: 60-90 words.
- Facts only from provided data (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weight, GSM, temperature, percentages beyond "100% cotton" from title).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (no bullet points, no headline).
- Data: Title: "Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig", Category: Bad, Keywords: Bad, Baumwolle, Handtuch-Set, Price: 69,00 €, Variants: Schwarz; Grau.

Drafting:
Das Premium Handtuch-Set besteht aus 100 % Baumwolle und überzeugt durch eine extra weiche, saugstarke und langlebige Qualität. Es gehört zur Kategorie Bad und ist in den Farbvarianten Schwarz und Grau erhältlich. Das Set wird für 69,00 € angeboten und eignet sich ideal für den täglichen Gebrauch im Badezimmer. Die hochwertige Verarbeitung der Baumwolle sorgt für ein angenehmes Hautgefühl und hohe Strapazierfähigkeit.

Word count check (German words):
"Das Premium Handtuch-Set besteht aus 100 % Baumwolle und überzeugt durch eine extra weiche, saugstarke und langlebige Qualität. Es gehört zur Kategorie Bad und ist in den Farbvarianten Schwarz und Grau erhältlich. Das Set wird für 69,00 € angeboten und eignet sich ideal für den täglichen Gebrauch im Badezimmer. Die hochwertige Verarbeitung der Baumwolle sorgt für ein angenehmes Haut
```

**Befund:** Denken im Text: constraints:, drafting:, the user wants, word count; englisch: for, from, the

**koerbe** — 8.9 s

```
The user wants a product description for a German online shop.
Constraints:
- Length: 60-90 words.
- Only facts from the provided data.
- No invented specs (dimensions, weight, material, temp, percentages).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German running text (Fliesstext), no bullet points, no headlines.
- Data: Title, Category (Bad), Keywords, Price, Variants (Beige / 28x28cm; Beige / 40x25cm).

Drafting ideas:
- Mention it's a 2-piece set.
- Mention the category "Bad" (bathroom) but title says Kinderzimmer, Wohnzimmer, Schlafzimmer. I should stick to the data. The category is "Bad", the title mentions other rooms. I can mention the title's suggested use cases as part of the product name/description context.
- Mention the two size variants.
- Mention color (Beige).
- Mention price.

Draft 1 (Mental):
Das Design Aufbewahrungskörbe im 2er-Set bietet stilvolle Ordnung für Kinderzimmer, Wohnzimmer und Schlafzimmer. Die Kategorie ist Bad. Erhältlich in den Varianten Beige mit den Maßen 28 x 28 cm sowie Beige mit 40 x 25 cm. Der Preis beträgt 39,00 €. Schlagworte sind Aufbewahrungskorb, Ordnung, Wohnaccessoire.

Word count check: ~55 words. Need a bit more to hit 60-90. Expand slightly on the description flow.

Draft 2:
Das Design Aufbewahrungskörbe im 2er-Set schafft stilvolle Ordnung in Kinderzimmer, Wohnzimmer und Schlafzimmer. Das Set wird in der Kategorie Bad geführt und ist in der Farbe Beige
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

## nvidia/nemotron-3-ultra-550b-a55b:free@high

**gewichtsdecke** — 6.8 s

```
Die Premium Gewichtsdecke in Blau ist in drei Varianten erhältlich: 122 mal 183 Zentimeter mit 5 Kilogramm sowie 135 mal 200 Zentimeter und 137 mal 200 Zentimeter, jeweils mit 10 Kilogramm. Sie gehört zur Kategorie Bett und wird mit den Schlagworten Entspannung, Gewichtsdecke und Schlafzimmer geführt. Der Preis beträgt 74,00 Euro. Das Modell nutzt sanften Druck, um Tiefenentspannung zu fördern und den Schlaf zu verbessern.
```

Befund: nichts zu beanstanden.

**handtuecher** — 8.5 s

```
The user wants a product description for a German online shop selling home accessories.
Constraints:
- Length: 60-90 words.
- Facts only from the provided input (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weight, GSM, temperature, percentages other than 100% cotton mentioned in title).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (Fliesstext), no bullet points, no headline.

Input facts:
- Title: Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig
- Category: Bad
- Keywords: Bad, Baumwolle, Handtuch-Set
- Price: 69,00 €
- Variants: Schwarz; Grau

Drafting the text (German):
"Dieses Premium Handtuch-Set besteht aus 100 % Baumwolle und ist in den Farben Schwarz und Grau erhältlich. Die Handtücher zeichnen sich durch eine extra weiche Haptik, hohe Saugfähigkeit und lange Haltbarkeit aus. Das Set eignet sich ideal für das Badezimmer und wird zum Preis von 69,00 € angeboten. Die hochwertige Verarbeitung sorgt für angenehmen Komfort im täglichen Gebrauch. Die natürliche Baumwolle fühlt sich sanft auf der Haut an."

Word count check:
"Dieses Premium Handtuch-Set besteht aus 100 % Baumwolle und ist in den Farben Schwarz und Grau erhältlich. (16)
Die Handtücher zeichnen sich durch eine extra weiche Haptik, hohe Saugfähigkeit und lange Haltbarkeit aus. (16)
Das Set eignet sich ideal für das Badezimmer und wird zum Preis von 69,
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the

**koerbe** — 17.2 s

```
The user wants a product description for a German online shop.
Constraints:
- Length: 60-90 words.
- Only facts from the provided data.
- No invented specs (dimensions, weight, material, temp, percentages).
- No scarcity, strike-through prices, reviews, claims about other buyers.
- Factual German running text (prose), no lists, no headlines.

Data provided:
- Title: Design Aufbewahrungskörbe im 2er-Set – Stilvolle Ordnung für Kinderzimmer, Wohnzimmer & Schlafzimmer
- Category: Bad (Bathroom) -> Note: Title mentions children's room, living room, bedroom. Category says Bathroom. I should mention the rooms from the title as usage examples, maybe mention category if relevant, but title is more descriptive.
- Keywords: Aufbewahrungskorb, Ordnung, Wohnaccessoire
- Price: 39,00 €
- Variants: Beige / 28 x 28 cm; Beige / 40 x 25 cm

Drafting facts to include:
- 2er-Set (2-piece set)
- Design storage baskets (Design Aufbewahrungskörbe)
- Color: Beige
- Two size variants: 28x28 cm and 40x25 cm
- Suitable for: Kinderzimmer, Wohnzimmer, Schlafzimmer (from title)
- Category: Bad (could mention suitable for bathroom too, but title doesn't say it. I'll stick to title usage or general "Wohnaccessoire").
- Price: 39,00 €

Drafting text (German):
"Das Design-Aufbewahrungskörbe-Set besteht aus zwei Körben in Beige und eignet sich für Kinderzimmer, Wohnzimmer und Schlafzimmer. Zwei Varianten stehen zur Wahl: ein quadratisches Format mit 28 mal
```

**Befund:** Denken im Text: constraints:, the user wants; englisch: and, for, from, the

## google/gemma-4-26b-a4b-it:free

**gewichtsdecke** — 1.9 s

```
Diese Premium Gewichtsdecke für das Schlafzimmer unterstützt die Tiefenentspannung und einen besseren Schlaf durch sanften Druck. Das Produkt ist in der Farbe Blau erhältlich und kann in verschiedenen Ausführungen gewählt werden. Zur Auswahl stehen die Varianten mit den Maßen 122 x 183 cm und einem Gewicht von 5 kg sowie die Varianten mit den Maßen 135 x 200 cm oder 137 x 200 cm und jeweils 10 kg Gewicht. Der Preis für diese Gewichtsdecke beträgt 74,00 €.
```

Befund: nichts zu beanstanden.

**handtuecher** — 15.1 s

```
Dieses Premium Handtuch-Set für das Badezimmer besteht aus 100 % Baumwolle. Die Textilien zeichnen sich durch eine extra weiche Beschaffenheit, eine hohe Saugkraft sowie eine hohe Langlebigkeit aus. Das Set ist in den Farbvarianten Schwarz und Grau erhältlich. Für eine hochwertige Ausstattung Ihres Badezimmers bietet dieses Set eine praktische Lösung. Der Preis für das Produkt beträgt 69,00 €. Die Materialzusammensetzung von reiner Baumwolle sorgt für die gewünschten Eigenschaften der Handtücher.
```

Befund: nichts zu beanstanden.

**koerbe** — 3.6 s

```
Diese Design Aufbewahrungskörbe im 2er-Set unterstützen Sie dabei, Ordnung in Ihrem Zuhause zu schaffen. Die Körbe dienen als vielseitige Wohnaccessoires und lassen sich im Kinderzimmer, im Wohnzimmer oder im Schlafzimmer einsetzen. Das Set ist zudem für die Nutzung im Bad geeignet. Sie können zwischen zwei verschiedenen Varianten wählen: Beige mit den Maßen 28 x 28 cm oder Beige mit den Maßen 40 x 25 cm. Dieses Set bietet eine praktische Lösung zur Aufbewahrung von Gegenständen in verschiedenen Räumen.
```

Befund: nichts zu beanstanden.

