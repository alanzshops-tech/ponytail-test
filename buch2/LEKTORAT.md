# Lektorat durch fremde Modelle

Stand: 2026-08-31 · Modelle: `openai/gpt-4o-2024-05-13`, `~google/gemini-pro-latest` · Kosten: 0.2912 USD

Gefragt wurde nichts, was nicht beantwortbar ist — nicht „ist das gut“, sondern: **wo würdest du aufhören zu lesen**. Das hat eine Stelle, und die Stelle muss wörtlich zitiert werden.

**Jedes Zitat ist gegen den Kapiteltext geprüft.** Ein erfundenes Zitat heißt: Das Modell hat nicht gelesen, sondern etwas Plausibles gesagt. Die Belegquote unten ist die Kalibrierung dieses Geräts — liegt sie niedrig, ist der ganze Bericht wertlos.

**Belegquote: 27 von 28 Zitaten (96.4 %) stehen wirklich im Text.**

## Gegenprobe

Ein absichtlich schlechter Text (Klischee, Perspektivsprung, Erklärbär, Widerspruch in zwei Sätzen) geht bei jedem Lauf mit durch. Winken die Modelle ihn durch, ist jedes „kein Abbruch“ bei den echten Kapiteln wertlos.

- `gpt-4o-2024-05-13`: **Abbruchstelle genannt** — die Frage funktioniert
- `gemini-pro-latest`: **Abbruchstelle genannt** — die Frage funktioniert

## Wo abgebrochen würde

| Kap. | Modell | Stelle | Grund | belegt |
|---:|---|---|---|:--:|
| 1 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 1 | `gemini-pro-latest` | *keine* | – | – |
| 2 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 2 | `gemini-pro-latest` | *keine* | – | – |
| 3 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 3 | `gemini-pro-latest` | *keine* | – | – |
| 5 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 5 | `gemini-pro-latest` | *keine* | – | – |
| 12 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 12 | `gemini-pro-latest` | *keine* | – | – |
| 19 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 19 | `gemini-pro-latest` | *keine* | – | – |
| 23 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 23 | `gemini-pro-latest` | *keine* | – | – |
| 36 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 36 | `gemini-pro-latest` | *keine* | – | – |
| 53 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 53 | `gemini-pro-latest` | *keine* | – | – |
| 64 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 64 | `gemini-pro-latest` | *keine* | – | – |

## Was unklar bleibt

| Kap. | Modell | Stelle | Was | belegt |
|---:|---|---|---|:--:|
| 1 | `gemini-pro-latest` | „ich sein Telefon nicht nahm, sondern meins, und in seiner Ko“ | Wenn sie ihr eigenes Handy benutzt, wie kann sie dann in seiner Kontak | ja |
| 2 | `gpt-4o-2024-05-13` | „Ich habe Theo — nein. Ich habe Jonas am Telefon“ | nein. Ich habe Jonas am Telefon" — Warum der Wechsel von Theo zu Jonas | ja |
| 2 | `gemini-pro-latest` | „Ich habe Theo — nein. Ich habe Jonas am Telefon gehabt“ | nein. Ich habe Jonas am Telefon gehabt" — Es reißt mich aus dem Lesefl | ja |
| 3 | `gemini-pro-latest` | „Frau Sarrazin hat in ihrer Abteilung echte Scheinehen gesehe“ | Es wird aus dem Nichts eine Frau Sarrazin erwähnt, ohne dass vorher er | ja |
| 5 | `gemini-pro-latest` | „Weil ich die Gutachterin war und er der Bauherr“ | Später heißt es, er sei der Bruder des Auftraggebers, was ein Widerspr | ja |
| 36 | `gemini-pro-latest` | „weil da die Schiene sitzt, wenn sie nachts nicht schläft.“ | Es verwirrt beim ersten Lesen kurz, ob sie die Schiene nur bei Schlafl | ja |
| 64 | `gpt-4o-2024-05-13` | „Er hat gesagt, das gibt es im öffentlichen Dienst nicht“ | Warum gibt es das nicht? | ja |
| 64 | `gemini-pro-latest` | „weil Nadia gegessen werden wollte“ | Es klingt unfreiwillig komisch, als ob das Baby verspeist werden soll, | ja |

## Übereinstimmung der Modelle

Wenn zwei unabhängige Modelle dieselbe Stelle nennen, ist das ein Befund. Nennen sie nie dieselbe, misst das Gerät Rauschen.

- Kapitel 1: nur ein Modell mit Beleg
- Kapitel 2: nur ein Modell mit Beleg
- Kapitel 3: nur ein Modell mit Beleg
- Kapitel 5: nur ein Modell mit Beleg
- Kapitel 12: nur ein Modell mit Beleg
- Kapitel 19: nur ein Modell mit Beleg
- Kapitel 23: nur ein Modell mit Beleg
- Kapitel 36: nur ein Modell mit Beleg
- Kapitel 53: nur ein Modell mit Beleg
- Kapitel 64: nur ein Modell mit Beleg

**0 von 10 Kapiteln mit übereinstimmendem Abbruchpunkt.**

<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->
