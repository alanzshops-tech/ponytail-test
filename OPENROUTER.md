# OpenRouter — Stand 2026-08-10

Zugang zu vielen Modellen über eine Adresse. Erhoben auf dem
Runner; die Arbeitsumgebung erreicht openrouter.ai nicht.

## Schlüssel

| Angabe | Wert |
|---|---|
| Grenze | None |
| verbraucht | 0 |
| verbleibend | None |
| Gratisstufe | True |

## Guthaben

| Angabe | Wert |
|---|---|
| eingezahlt | 0 |
| verbraucht | 0 |

## Modelle

**399 Modelle erreichbar**, davon 17 ohne Kosten.

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
| `ibm-granite/granite-4.1-8b` | 131072 | 0.0500 $ | 0.1000 $ |

Ohne Kosten, die ersten zehn:

`inclusionai/ling-3.0-tiny:free`, `poolside/laguna-s-2.1:free`, `poolside/laguna-xs-2.1:free`, `cohere/north-mini-code:free`, `nvidia/nemotron-3.5-content-safety:free`, `nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`, `google/gemma-4-26b-a4b-it:free`, `google/gemma-4-31b-it:free`, `google/lyria-3-pro-preview`

Kostenlose Modelle sind gedrosselt und oft überlastet. Für
eine Messung taugen sie nicht — ein Fehlschlag sagt dann
nichts über den Zugang.

## Rundlauf

Modell `nvidia/nemotron-3-ultra-550b-a55b:free` (Gratisstufe, weil kein Guthaben vorhanden ist), Verbrauch `{'prompt_tokens': 31, 'completion_tokens': 33, 'total_tokens': 64, 'cost': 0, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0, 'upstream_inference_prompt_cost': 0, 'upstream_inference_completions_cost': 0}, 'completion_tokens_details': {'reasoning_tokens': 17, 'image_tokens': 0, 'audio_tokens': 0}}`.

```
Hundesofas bieten Hunden einen gemütlichen und geschützten Ruheplatz.
```

Erst das beweist den Zugang. `/key` zu lesen gelingt auch
einem Schlüssel, dessen Guthaben für keine Antwort reicht.

Davor abgelehnt (2):

| Modell | Grund |
|---|---|
| `google/lyria-3-pro-preview` | HTTP 502 {"error":{"message":"Provider returned error","code":502,"metadata":{"raw":"{\n  |
| `google/lyria-3-clip-preview` | HTTP 502 {"error":{"message":"Provider returned error","code":502,"metadata":{"raw":"{\n  |

