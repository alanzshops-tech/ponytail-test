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
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 3 | 1 | 145 | 0 | 1 | 0 | 4 | 11.0 s | 0.000000 $ |
| `google/gemma-4-31b-it:free` | 3 | 2 | 83 | 0 | 0 | 0 | 0 | 4.3 s | 0.000000 $ |
| `google/gemma-4-26b-a4b-it:free` | 3 | 1 | 77 | 0 | 0 | 0 | 0 | 7.8 s | 0.000000 $ |
| `inclusionai/ling-3.0-tiny:free` | 3 | 2 | 63 | 0 | 0 | 0 | 0 | 2.0 s | 0.000000 $ |

## nvidia/nemotron-3-ultra-550b-a55b:free

**gewichtsdecke** — 0.5 s

Fehlgeschlagen: leere Antwort 

**handtuecher** — 12.4 s

```
The user wants a product description for a German online shop selling home accessories.
Constraints:
- Length: 60-90 words.
- Facts only from the provided data (Title, Category, Keywords, Price, Variants).
- No invented specs (dimensions, weight, GSM, temperature, percentages other than 100% cotton).
- No scarcity, strike-through prices, reviews, social proof.
- Factual German running text (no bullet points, no headlines).
- Language: German.

Data:
- Title: Premium Handtuch-Set aus 100 % Baumwolle – Extra weich, saugstark & langlebig
- Category: Bad
- Keywords: Bad, Baumwolle, Handtuch-Set
- Price: 69,00 €
- Variants: Schwarz; Grau

Drafting ideas:
Start with the product name/material. Mention the category context. Mention the variants. Mention the price. Use adjectives from title (extra weich, saugstark, langlebig) as they are in the title provided.

Draft 1:
Das Premium Handtuch-Set besteht aus 100 % Baumwolle und ist für das Bad konzipiert. Es überzeugt durch eine extra weiche Haptik, hohe Saugstärke und langlebige Verarbeitung. Erhältlich ist das Set in den Farben Schwarz und Grau. Der Preis beträgt 69,00 €. Die hochwertige Materialqualität sorgt für angenehmen Komfort im Alltag und behält auch nach häufigem Waschen Form und Farbe. Ein klassisches Accessoire für moderne Badezimmer.

Word count check:
"Das Premium Handtuch-Set besteht aus 100 % Baumwolle und ist für das Bad konzipiert. (13) Es überzeugt durch eine extra weiche Haptik
```

**Befund:** Denken im Text: constraints:, the user wants, word count; englisch: for, from, the, with

**koerbe** — 9.6 s

```
Das 2er-Set Design Aufbewahrungskörbe bietet stilvolle Ordnung für Kinderzimmer, Wohnzimmer und Schlafzimmer. Die Körbe sind in der Farbe Beige erhältlich und werden als Set in zwei Größen geliefert: ein Korb misst 28 x 28 cm, der andere 40 x 25 cm. Als Wohnaccessoire eignen sie sich vielseitig zur Aufbewahrung verschiedener Gegenstände. Der Preis für das Set beträgt 39,00 €. Die Kategorie Bad deutet auf eine zusätzliche Verwendungsmöglichkeit im Sanitärbereich hin.
```

Befund: nichts zu beanstanden.

## google/gemma-4-31b-it:free

**gewichtsdecke** — 4.3 s

```
Diese Premium Gewichtsdecke für das Schlafzimmer ist darauf ausgelegt, durch sanften Druck eine Tiefenentspannung zu fördern und das Schlafen zu verbessern. Das Produkt ist in der Farbe Blau erhältlich und wird in drei verschiedenen Varianten angeboten. Kunden können zwischen den Maßen 122 x 183 cm mit einem Gewicht von 5 kg sowie 135 x 200 cm oder 137 x 200 cm mit einem Gewicht von jeweils 10 kg wählen. Die Gewichtsdecke aus der Kategorie Bett ist zu einem Preis von 74,00 € erhältlich.
```

Befund: nichts zu beanstanden.

**handtuecher** — 0.1 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

**koerbe** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. Please retry shortl

## google/gemma-4-26b-a4b-it:free

**gewichtsdecke** — 7.1 s

```
Diese Premium Gewichtsdecke für das Schlafzimmer fördert die Entspannung und unterstützt ein besseres Schlafen durch sanften Druck. Das Produkt ist in der Farbe Blau erhältlich und wird in verschiedenen Ausführungen angeboten. Sie können zwischen einer Variante mit den Maßen 122 x 183 cm und einem Gewicht von 5 kg sowie zwei Ausführungen mit den Maßen 135 x 200 cm oder 137 x 200 cm und jeweils 10 kg wählen. Der Preis für diese Gewichtsdecke beträgt 74,00 €.
```

Befund: nichts zu beanstanden.

**handtuecher** — 0.2 s

Fehlgeschlagen: HTTP 429 {"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream. Please retry sh

**koerbe** — 8.5 s

```
Diese Design Aufbewahrungskörbe im 2er-Set dienen der stilvollen Ordnung in Ihrem Zuhause. Sie lassen sich vielseitig im Kinderzimmer, im Wohnzimmer, im Schlafzimmer oder im Bad als Wohnaccessoire einsetzen. Das Set umfasst zwei verschiedene Varianten in der Farbe Beige: Ein Korb hat die Maße 28 x 28 cm, während der andere eine Größe von 40 x 25 cm aufweist. Mit einem Preis von 39,00 € bieten diese Aufbewahrungskörbe eine praktische Lösung, um Ordnung in Ihren Wohnbereichen zu schaffen.
```

Befund: nichts zu beanstanden.

## inclusionai/ling-3.0-tiny:free

**gewichtsdecke** — 2.0 s

```
Diese Premium Gewichtsdecke bietet Tiefenentspannung durch einen sanften Druck, der den Körper entlastet und den besseren Schlaf unterstützt. Sie ist in eleganten Blautönen erhältlich und kommt dem oft unterschätzten Bedürfnis nach sanfter Überführung gerecht. Die gestaltete Decke lässt sich nahtlos in jedes Schlafzimmer integrieren und sorgt für ein rundheres Wohlbefinden nach dem Aufstehen. Mit einem klaren Preis von 74,00 € erhalten Sie ein
```

Befund: nichts zu beanstanden.

**handtuecher** — 1.5 s

Fehlgeschlagen: leere Antwort 

**koerbe** — 2.1 s

Fehlgeschlagen: leere Antwort 

