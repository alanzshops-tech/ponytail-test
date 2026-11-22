# OpenRouter — Stand 2026-08-13

Zugang zu vielen Modellen über eine Adresse. Erhoben auf dem
Runner; die Arbeitsumgebung erreicht openrouter.ai nicht.

## Schlüssel

| Angabe | Wert |
|---|---|
| Grenze | None |
| verbraucht | 0.07532702 |
| verbleibend | None |
| Gratisstufe | False |

## Guthaben

| Angabe | Wert |
|---|---|
| eingezahlt | 6 |
| verbraucht | 0.07532702 |

## Modelle

**409 Modelle erreichbar**, davon 18 ohne Kosten.

Die zehn günstigsten mit Preis. Beträge in US-Dollar je
Million Token — Eingabe ist, was hingeschickt wird, Ausgabe,
was zurückkommt.

| Modell | Kontext | Eingabe | Ausgabe |
|---|---:|---:|---:|
| `inclusionai/ling-2.6-flash` | 262144 | 0.0100 $ | 0.0300 $ |
| `mistralai/mistral-nemo` | 131072 | 0.0190 $ | 0.0300 $ |
| `inclusionai/ling-3.0-flash` | 262144 | 0.0210 $ | 0.0630 $ |
| `sao10k/l3-lunaris-8b` | 8192 | 0.0400 $ | 0.0500 $ |
| `gryphe/mythomax-l2-13b` | 8192 | 0.0600 $ | 0.0600 $ |
| `nex-agi/nex-n2-mini` | 262144 | 0.0250 $ | 0.1000 $ |
| `ibm-granite/granite-4.0-h-micro` | 131000 | 0.0170 $ | 0.1120 $ |
| `mistralai/mistral-small-24b-instruct-2501` | 32768 | 0.0500 $ | 0.0800 $ |
| `meta-llama/llama-3.1-8b-instruct` | 131072 | 0.0500 $ | 0.0800 $ |
| `upstage/solar-pro4` | 524288 | 0.0300 $ | 0.1200 $ |

Ohne Kosten, die ersten zehn:

`liquid/lfm-2.5-2.6b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`, `cohere/north-mini-code:free`, `nvidia/nemotron-3.5-content-safety:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `google/gemma-4-26b-a4b-it:free`, `google/gemma-4-31b-it:free`

Kostenlose Modelle sind gedrosselt und oft überlastet. Für
eine Messung taugen sie nicht — ein Fehlschlag sagt dann
nichts über den Zugang.

## Bildfähige Modelle

Modelle, deren `output_modalities` „image“ enthält — Kandidaten,
um Produktbilder über die bestehende OpenRouter-Anbindung zu
erzeugen oder zu bearbeiten, ohne ein separates Tool zu
installieren.

**9 von 409 Modellen** können Bilder ausgeben.

| Modell | nimmt herein | Eingabe | Ausgabe |
|---|---|---:|---:|
| `google/gemini-3.1-flash-lite-image` | image, text | 0.2500 $ | 1.5000 $ |
| `google/gemini-2.5-flash-image` | image, text | 0.3000 $ | 2.5000 $ |
| `google/gemini-3.1-flash-image` | image, text | 0.5000 $ | 3.0000 $ |
| `google/gemini-3.1-flash-image-preview` | image, text | 0.5000 $ | 3.0000 $ |
| `openai/gpt-5-image-mini` | file, image, text | 2.5000 $ | 2.0000 $ |
| `google/gemini-3-pro-image` | image, text | 2.0000 $ | 12.0000 $ |
| `google/gemini-3-pro-image-preview` | image, text | 2.0000 $ | 12.0000 $ |
| `openai/gpt-5-image` | image, text, file | 10.0000 $ | 10.0000 $ |
| `openai/gpt-5.4-image-2` | image, text, file | 8.0000 $ | 15.0000 $ |

## Rundlauf

Modell `inclusionai/ling-2.6-flash` (guenstigste bezahlte), mit Websuche (Exa) — echte Treffer, kein reines Modellwissen.

Verbrauch `{'prompt_tokens': 2929, 'completion_tokens': 500, 'total_tokens': 3429, 'cost': 0.00704429, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 4.429e-05, 'upstream_inference_prompt_cost': 2.929e-05, 'upstream_inference_completions_cost': 1.5e-05}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}`.

```
Konkretes Produkt, das aktuell (August 2026) eine sehr erfolgreiche, virale Werbeanzeige hat und zusätzlich im Aufwärtstrend ist:

- Produktname: Cable Organizer Box (Kabelfutter-Box / Aufbewahrungsbox für Ladekabel)
- Kategorie: Zubehör für Schreibtisch/Stationery / Kabelorganisation
- Warum die Anzeige gut performt (laut den Quellen):
  - Hook: Visueller “Before-After”-Transformations-Clip – im Sekunden-Takt wird das kabelgeschmierte Desk混乱 zu einem sauberen, aufgeräumten Schreibtisch gezeigt. Das Format ist kurz, klar und sofort verständlich („saubere Arbeitsfläche in drei Sekunden“).
  - Angebot: Sub-$4-Preis macht es zu einem Impulskauf; leicht testbar mit geringem Risiko für den Käufer.
  - Format: Kurzes, motivationsarmes Video eignet sich optimal für TikTok und Facebook-Reels; hohe Abspielfrequenz und klare Nutzungs情境e (Dorm Room Setup, Clean Desk) steigern die Wiederverwendbarkeit der Inhalte.
  - Zusätzliche Performance-Faktoren: Es lässt sich gut bundlen (z. B. mit Phone Stand, LED-Lightbox), hat hohe Conversion durch den Clean-Desk-Trend und eignet sich für Influencer-Mashups mit dem Laptop-Camping-Set-Up.

- China-Bezug: Ja – über CJ Dropshipping und ähnliche Dropshipper (Alibaba-/1688-gestützte Lieferketten) lieferbar.

Quellen:
- TikTok Viral Products August 2026: „The cable organizer box is the quiet workhorse of every clean desk setup video. It hides the charger-cable tangle … before/after demos remain TikTok’s highest-engagement format.“ [astools.app](https://news.astools.app/en/blog/tiktok-viral-products-august-2026)
- 10 Best Dropshipping Products to Sell in August 2026: Desk cable organizer als Top-Performance-Item für Dorm-Room
```

Erst das beweist den Zugang. `/key` zu lesen gelingt auch
einem Schlüssel, dessen Guthaben für keine Antwort reicht.

