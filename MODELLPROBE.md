# Modellvergleich für Produkttexte — Stand 2026-08-10

Dieselben drei echten Produkte an jedes Modell, derselbe Auftrag.
Gemessen wird nicht, ob es schön klingt, sondern ob es Tatsachen
erfindet und die Regeln des Ladens einhält.

**Erfundene Zahlen** sind der teure Fehler: eine Zahl über 10, die
in den Angaben nicht vorkam, steht danach als Zusicherung im Shop
— „waschbar bei 60 Grad“, „3 cm dick“ — ohne dass sie jemand
geprüft hat. Kleine Zählzahlen bleiben außen vor, die sind
Formulierung.

| Modell | Läufe | Fehler | Wörter ⌀ | erfundene Zahlen | Maschen | englische Reste | Dauer ⌀ | Kosten |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 3 | 1 | 210 | 16 | 0 | 6 | 31.8 s | 0.000000 $ |
| `google/gemma-4-31b-it:free` | 3 | **3** | – | – | – | – | – | – |
| `google/gemma-4-26b-a4b-it:free` | 3 | 1 | 73 | 0 | 0 | 0 | 18.4 s | 0.000000 $ |
| `inclusionai/ling-3.0-tiny:free` | 3 | **3** | – | – | – | – | – | – |

## nvidia/nemotron-3-ultra-550b-a55b:free

**gewichtsdecke** — 0.5 s

Fehlgeschlagen: leere Antwort 

**handtuecher** — 9.9 s

```
The user wants a product description for a German online shop.
Constraints:
- Length: 60-90 words.
- Only facts from the provided data.
- No invented specs (dimensions, weight, GSM, temp, %).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German continuous text (no bullet points, no headlines).
- Data: Title: "Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig", Category: Bad, Keywords: Bad, Baumwolle, Handtuch-Set, Price: 69,00 €, Variants: Schwarz; Grau.

Drafting:
Das Premium Handtuch-Set besteht aus 100 % Baumwolle und bietet eine extra weiche, saugstarke sowie langlebige Qualität für das Bad. Erhältlich ist das Set in den Farben Schwarz und Grau zum Preis von 69,00 €. Die hochwertige Verarbeitung sorgt für ein angenehmes Hautgefühl und eine hohe Saugfähigkeit im täglichen Einsatz. Als Teil der Kategorie Bad ergänzen die Handtücher die Badezimmerausstattung zuverlässig und pflegeleicht.

Word count check (German words):
Das (1) Premium (2) Handtuch-Set (3) besteht (4) aus (5) 100 (6) % (7) Baumwolle (8) und (9) bietet (10) eine (11) extra (12) weiche, (13) saugstarke (14) sowie (15) langlebige (16) Qualität (17) für (18) das (19) Bad. (20) Erhältlich (21) ist (22) das (2
```

**Befund:** erfundene Zahlen: 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 60, 90; englisch: for, from, the

**koerbe** — 53.8 s

```
The user wants a product description for a German online shop.
Constraints:
- 60-90 words.
- Only facts from the provided data.
- No invented specs (dimensions, weight, material, etc.).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German flowing text (no lists, no headlines).
- Data provided: Title, Category, Keywords, Price, Variants (Colors/Size). Note: Category is "Bad" (Bathroom) but Title mentions Kinderzimmer, Wohnzimmer, Schlafzimmer. I must stick to facts provided. The title says "Design Aufbewahrungskörbe im 2er-Set – Stilvolle Ordnung für Kinderzimmer, Wohnzimmer & Schlafzimmer". Category says "Bad". I should probably mention the use cases from the title as they are part of the product title/description intent, but be careful not to invent. The variants are Beige in two sizes. Price is 39,00 €.

Drafting:
Das Set besteht aus zwei Design-Aufbewahrungskörben in Beige, die für stilvolle Ordnung in Kinderzimmer, Wohnzimmer oder Schlafzimmer sorgen. Erhältlich sind die Körbe in den Varianten 28 mal 28 Zentimeter sowie 40 mal 25 Zentimeter. Als Wohnaccessoire eignen sie sich vielseitig zur Aufbewahrung. Der Preis für das 2er-Set beträgt 39,00 Euro. Die Kategorie ist Bad, der Titel nennt aber weitere Räume.

Word count check (German words):
"Das Set besteht aus zwei Design-Aufbewahrungskörben in Beige, die für stilvolle Ordnung in Kinderzimmer, Wohnzimmer oder Schlafzimmer sorgen. Erhältlich sind die Körbe in den Varianten 28 mal 28 Zentimeter sowie 40 mal 25 Zentimeter. Als
```

**Befund:** erfundene Zahlen: 60, 90; englisch: for, from, the

## google/gemma-4-31b-it:free

**gewichtsdecke** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

**handtuecher** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

**koerbe** — 0.1 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

## google/gemma-4-26b-a4b-it:free

**gewichtsdecke** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream. Please retry sh

**handtuecher** — 3.6 s

```
Dieses Handtuch-Set für das Bad besteht zu 100 % aus Baumwolle. Die Textilien sind in den Farben Schwarz und Grau erhältlich. Das Set überzeugt durch seine Eigenschaften extra weich, saugstark und langlebig. Für einen Preis von 69,00 € erhalten Sie dieses hochwertige Set für Ihre Badezimmer-Ausstattung. Die Materialzusammensetzung aus reiner Baumwolle sorgt für ein angenehmes Gefühl auf der Haut. Damit ist dieses Set eine praktische Ergänzung für Ihr Badezimmer.
```

Befund: nichts zu beanstanden.

**koerbe** — 33.1 s

```
Dieses 2er-Set Design Aufbewahrungskörbe dient der Organisation in verschiedenen Wohnbereichen. Als stilvolles Wohnaccessoire eignet es sich für das Kinderzimmer, das Wohnzimmer, das Schlafzimmer oder das Bad. Die Körbe sind in der Farbe Beige erhältlich und werden in zwei unterschiedlichen Ausführungen geliefert. Zur Auswahl stehen die Maße 28 x 28 cm sowie 40 x 25 cm. Mit diesem Set für 39,00 € schaffen Sie praktische Ordnung in Ihren Räumen. Die vielseitigen Aufbewahrungskörbe unterstützen eine strukturierte Gestaltung Ihrer Inneneinrichtung.
```

Befund: nichts zu beanstanden.

## inclusionai/ling-3.0-tiny:free

**gewichtsdecke** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"inclusionai/ling-3.0-tiny:free is temporarily rate-limited upstream. Please retry sh

**handtuecher** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"inclusionai/ling-3.0-tiny:free is temporarily rate-limited upstream. Please retry sh

**koerbe** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"inclusionai/ling-3.0-tiny:free is temporarily rate-limited upstream. Please retry sh

