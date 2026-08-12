# OpenRouter — Stand 2026-08-12

Zugang zu vielen Modellen über eine Adresse. Erhoben auf dem
Runner; die Arbeitsumgebung erreicht openrouter.ai nicht.

## Schlüssel

| Angabe | Wert |
|---|---|
| Grenze | None |
| verbraucht | 1.194e-06 |
| verbleibend | None |
| Gratisstufe | False |

## Guthaben

| Angabe | Wert |
|---|---|
| eingezahlt | 6 |
| verbraucht | 1.194e-06 |

## Modelle

**406 Modelle erreichbar**, davon 19 ohne Kosten.

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

`liquid/lfm-2.5-2.6b:free`, `nvidia/nemotron-3.5-lightning:free`, `inclusionai/ling-3.0-tiny:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`, `cohere/north-mini-code:free`, `nvidia/nemotron-3.5-content-safety:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `google/gemma-4-26b-a4b-it:free`

Kostenlose Modelle sind gedrosselt und oft überlastet. Für
eine Messung taugen sie nicht — ein Fehlschlag sagt dann
nichts über den Zugang.

## Bildfähige Modelle

Modelle, deren `output_modalities` „image“ enthält — Kandidaten,
um Produktbilder über die bestehende OpenRouter-Anbindung zu
erzeugen oder zu bearbeiten, ohne ein separates Tool zu
installieren.

**11 von 406 Modellen** können Bilder ausgeben.

| Modell | nimmt herein | Eingabe | Ausgabe |
|---|---|---:|---:|
| `openrouter/auto-beta` | text, image, audio, file, video | -1000000.0000 $ | -1000000.0000 $ |
| `openrouter/auto` | text, image, audio, file, video | -1000000.0000 $ | -1000000.0000 $ |
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

Modell `inclusionai/ling-2.6-flash` (guenstigste bezahlte), Verbrauch `{'prompt_tokens': 34, 'completion_tokens': 17, 'total_tokens': 51, 'cost': 8.5e-07, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 8.5e-07, 'upstream_inference_prompt_cost': 3.4e-07, 'upstream_inference_completions_cost': 5.1e-07}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}`.

```
Hundesofas sind bequem, robust und leicht sauber zu machen.
```

Erst das beweist den Zugang. `/key` zu lesen gelingt auch
einem Schlüssel, dessen Guthaben für keine Antwort reicht.

