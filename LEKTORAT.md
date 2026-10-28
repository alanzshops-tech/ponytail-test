# Lektorat durch fremde Modelle

Stand: 2026-08-15 · Modelle: `openai/gpt-4o-2024-05-13`, `anthropic/claude-sonnet-4.6` · Kosten: 0.0929 USD

Gefragt wurde nichts, was nicht beantwortbar ist — nicht „ist das gut“, sondern: **wo würdest du aufhören zu lesen**. Das hat eine Stelle, und die Stelle muss wörtlich zitiert werden.

**Jedes Zitat ist gegen den Kapiteltext geprüft.** Ein erfundenes Zitat heißt: Das Modell hat nicht gelesen, sondern etwas Plausibles gesagt. Die Belegquote unten ist die Kalibrierung dieses Geräts — liegt sie niedrig, ist der ganze Bericht wertlos.

**Belegquote: 13 von 14 Zitaten (92.9 %) stehen wirklich im Text.**

## Gegenprobe

Ein absichtlich schlechter Text (Klischee, Perspektivsprung, Erklärbär, Widerspruch in zwei Sätzen) geht bei jedem Lauf mit durch. Winken die Modelle ihn durch, ist jedes „kein Abbruch“ bei den echten Kapiteln wertlos.

- `gpt-4o-2024-05-13`: **Abbruchstelle genannt** — die Frage funktioniert
- `claude-sonnet-4.6`: **Abbruchstelle genannt** — die Frage funktioniert

## Wo abgebrochen würde

| Kap. | Modell | Stelle | Grund | belegt |
|---:|---|---|---|:--:|
| 1 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 1 | `claude-sonnet-4.6` | *keine* | – | – |
| 12 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 12 | `claude-sonnet-4.6` | *keine* | – | – |
| 21 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 21 | `claude-sonnet-4.6` | *keine* | – | – |
| 28 | `gpt-4o-2024-05-13` | *keine* | – | – |
| 28 | `claude-sonnet-4.6` | *keine* | – | – |

## Was unklar bleibt

| Kap. | Modell | Stelle | Was | belegt |
|---:|---|---|---|:--:|
| 1 | `gpt-4o-2024-05-13` | „Die Immobilie ist in ihrer aktuellen Nutzung nicht“ | Was bedeutet "nicht ausreichend werthaltig"? | ja |
| 1 | `claude-sonnet-4.6` | „Das Ergebnis war jedes Mal dasselbe, egal wie oft“ | unklar ob sie tatsächlich keine Option sieht oder einfach aufgehört ha | ja |
| 12 | `claude-sonnet-4.6` | „das ist der Teil, bei dem ich schlecht dastehe“ | kurz unklar, ob sie die eigene Feigheit meint oder etwas Konkretes, da | ja |
| 21 | `claude-sonnet-4.6` | „wählen müssen. Merkst du was? Er merkte es nicht sofort“ | unklar, was genau Jonas "merkt"; der gedankliche Sprung von Beirat zu  | **NEIN** |
| 28 | `gpt-4o-2024-05-13` | „Ich zähle den zwanzigsten Januar mit.“ | Was ist am zwanzigsten Januar passiert? | ja |
| 28 | `claude-sonnet-4.6` | „die von ihr kam und die albern klingt“ | unklar ist, ob er "albern" ironisch meint oder wirklich kritisch, was  | ja |

## Übereinstimmung der Modelle

Wenn zwei unabhängige Modelle dieselbe Stelle nennen, ist das ein Befund. Nennen sie nie dieselbe, misst das Gerät Rauschen.

- Kapitel 1: nur ein Modell mit Beleg
- Kapitel 12: nur ein Modell mit Beleg
- Kapitel 21: nur ein Modell mit Beleg
- Kapitel 28: nur ein Modell mit Beleg

**0 von 4 Kapiteln mit übereinstimmendem Abbruchpunkt.**

<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->


