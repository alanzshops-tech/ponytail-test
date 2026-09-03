# Lektorat durch fremde Modelle

Stand: 2026-08-31 · Modelle: `openai/gpt-4o-2024-05-13`, `~google/gemini-pro-latest` · Kosten: 0.3706 USD

Gefragt wurde nichts, was nicht beantwortbar ist — nicht „ist das gut“, sondern: **wo würdest du aufhören zu lesen**. Das hat eine Stelle, und die Stelle muss wörtlich zitiert werden.

**Jedes Zitat ist gegen den Kapiteltext geprüft.** Ein erfundenes Zitat heißt: Das Modell hat nicht gelesen, sondern etwas Plausibles gesagt. Die Belegquote unten ist die Kalibrierung dieses Geräts — liegt sie niedrig, ist der ganze Bericht wertlos.

**Belegquote: 38 von 38 Zitaten (100.0 %) stehen wirklich im Text.**

## Gegenprobe

Ein absichtlich schlechter Text (Klischee, Perspektivsprung, Erklärbär, Widerspruch in zwei Sätzen) geht bei jedem Lauf mit durch. Winken die Modelle ihn durch, ist jedes „kein Abbruch“ bei den echten Kapiteln wertlos.

- `gpt-4o-2024-05-13`: **Abbruchstelle genannt** — die Frage funktioniert
- `gemini-pro-latest`: **Abbruchstelle genannt** — die Frage funktioniert

## Wo abgebrochen würde

| Kap. | Modell | Stelle | Grund | belegt |
|---:|---|---|---|:--:|
| 3 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 3 | `gemini-pro-latest` | *keine* | – | – |
| 5 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 5 | `gemini-pro-latest` | *keine* | – | – |
| 6 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 6 | `gemini-pro-latest` | *keine* | – | – |
| 20 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 20 | `gemini-pro-latest` | *keine* | – | – |
| 22 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 22 | `gemini-pro-latest` | *keine* | – | – |
| 27 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 27 | `gemini-pro-latest` | *keine* | – | – |
| 28 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 28 | `gemini-pro-latest` | *keine* | – | – |
| 34 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 34 | `gemini-pro-latest` | *keine* | – | – |
| 38 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 38 | `gemini-pro-latest` | *keine* | – | – |
| 47 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 47 | `gemini-pro-latest` | *keine* | – | – |
| 61 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 61 | `gemini-pro-latest` | *keine* | – | – |
| 62 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 62 | `gemini-pro-latest` | *keine* | – | – |

## Was unklar bleibt

| Kap. | Modell | Stelle | Was | belegt |
|---:|---|---|---|:--:|
| 3 | `gemini-pro-latest` | „Meldeadresse Ottensen, seine: Elbchaussee, bei seiner Mutter“ | Es ist beim ersten Lesen verwirrend, wer nun wo offiziell gemeldet ist | ja |
| 5 | `gemini-pro-latest` | „Weil ich die Gutachterin war und er der Bauherr“ | Erst ist Theo der Bauherr, später ist er plötzlich der Bruder des Auft | ja |
| 6 | `gemini-pro-latest` | „einmal vor mir selbst, an einem Grab, mit neunzehn.“ | Es verwirrt mich, wie das logisch in den Zeitrahmen der letzten vierze | ja |
| 20 | `gpt-4o-2024-05-13` | „Ich habe zugesehen, wie sie begreift, in welcher Reihenfolge“ | Welche Reihenfolge ist gemeint? | ja |
| 20 | `gemini-pro-latest` | „Es ist derselbe Ordner. Er ist nur dünner.“ | Es ist nicht sofort klar, auf welchen Ordner des Vaters er sich hier b | ja |
| 27 | `gemini-pro-latest` | „einem Vermerk nach Paragraf einundzwanzig über die Gutachter“ | Als Leserin weiß ich hier überhaupt nicht, was dieser Paragraf bedeute | ja |
| 28 | `gpt-4o-2024-05-13` | „Das ist eine Sache, die mir niemand“ | Was genau ist damit gemeint? | ja |
| 28 | `gemini-pro-latest` | „weil Wendland gesagt hat: „Wenn die Gutachterin, die uns“ | Hier stolpere ich, weil diese Figur im Beirat völlig aus dem Nichts au | ja |
| 34 | `gpt-4o-2024-05-13` | „Ich habe die Serviette hingelegt.“ | Kontext und Bedeutung sind nicht klar. | ja |
| 38 | `gemini-pro-latest` | „„Ich auch nicht.“ | Hier stolpere ich über den Sprecherwechsel und weiß nicht, wer gerade  | ja |
| 47 | `gpt-4o-2024-05-13` | „Kehrwieder vierzehn“ | Was ist Kehrwieder vierzehn? | ja |
| 47 | `gemini-pro-latest` | „warum ich am vierzehnten März 2025 auf einer Treppe“ | Der plötzliche Zeitsprung ins Jahr 2025 verwirrt kurz die zeitliche Ei | ja |
| 62 | `gpt-4o-2024-05-13` | „Das ist mein ganzer Beruf.“ | Was genau ihr Beruf ist, bleibt vage. | ja |
| 62 | `gemini-pro-latest` | „Sie hat sich hingesetzt und mir gegenüber, was sie“ | Hier fehlt beim Lesen gefühlt ein Wort, der Satzbau stolpert. | ja |

## Übereinstimmung der Modelle

Wenn zwei unabhängige Modelle dieselbe Stelle nennen, ist das ein Befund. Nennen sie nie dieselbe, misst das Gerät Rauschen.

- Kapitel 3: nur ein Modell mit Beleg
- Kapitel 5: nur ein Modell mit Beleg
- Kapitel 6: nur ein Modell mit Beleg
- Kapitel 20: nur ein Modell mit Beleg
- Kapitel 22: nur ein Modell mit Beleg
- Kapitel 27: nur ein Modell mit Beleg
- Kapitel 28: nur ein Modell mit Beleg
- Kapitel 34: nur ein Modell mit Beleg
- Kapitel 38: nur ein Modell mit Beleg
- Kapitel 47: nur ein Modell mit Beleg
- Kapitel 61: nur ein Modell mit Beleg
- Kapitel 62: nur ein Modell mit Beleg

**0 von 12 Kapiteln mit übereinstimmendem Abbruchpunkt.**

<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->

