# Setup: Claude Code, Modelle und OpenRouter

Stand 10.08.2026 · geprüft gegen Claude Code 2.1.226 und die offizielle
Dokumentation, nicht aus dem Gedächtnis geschrieben.

---

## Das Wichtigste zuerst

**OpenRouter kann Claude Code nicht antreiben.** Das ist keine
Vorsichtsmaßnahme, sondern die dokumentierte Lage:

> „Anthropic doesn't endorse, maintain, or audit third-party gateway
> products, and **doesn't support routing Claude Code to non-Claude models
> through any gateway**."
> — [Other LLM gateways](https://code.claude.com/docs/en/llm-gateway)

Drei Gründe, warum es auch technisch nicht geht:

| Hürde | Was dagegensteht |
|---|---|
| **Format** | Claude Code spricht drei Formate: Anthropic Messages, Bedrock InvokeModel, Vertex rawPredict. OpenRouters `/chat/completions` (OpenAI-Format) ist keines davon. |
| **Modellfilter** | Bei der Modellerkennung behält Claude Code nur IDs, die „claude" oder „anthropic" enthalten. GPT und Gemma fallen raus. |
| **Ungeprüft** | Ob OpenRouter überhaupt einen Anthropic-Messages-Endpunkt anbietet, ist nicht belegt. Im SDK `@openrouter/sdk` 1.2.18 ist der einzige Inferenzweg `/chat/completions`. |

**Deshalb wurde `ANTHROPIC_BASE_URL` nicht verändert.**

---

## Was stattdessen eingerichtet ist

Zwei getrennte Wege — kein Umschalter, weil es zwei verschiedene Dinge sind:

| | Motor | Werkzeug |
|---|---|---|
| **Was** | Claude Code selbst | fremde Modelle auf Zuruf |
| **Modelle** | nur Claude | 399, u. a. GPT, Gemma, Qwen, DeepSeek |
| **Wie** | `/model` im Gespräch | `scripts/openrouter.py` |
| **Wo** | hier | GitHub-Actions-Lauf (das Netz erreicht OpenRouter nur dort) |

---

## Geänderte und neue Dateien

| Datei | Was |
|---|---|
| `scripts/modelltest.py` | **neu** — MODEL-CONNECTION-TEST |
| `README_SETUP.md` | **neu** — diese Datei |
| `scripts/openrouter.py` | bestand schon, unverändert |
| `.github/workflows/openrouter.yml` | bestand schon, unverändert |

**Nichts an der Umgebung wurde verändert.** Keine Umgebungsvariable
gesetzt, keine Konfigurationsdatei angelegt, `ANTHROPIC_BASE_URL` nicht
angefasst.

---

## Befehle

### Verbindung prüfen

```bash
python3 scripts/modelltest.py           # Gateway, Modell, Zugangsdaten
python3 scripts/modelltest.py --fremd   # zusätzlich OpenRouter abfragen
```

Zeigt nie einen Schlüsselwert — nur ob gesetzt, wie lang, letzte drei
Zeichen.

### Claude-Modell wechseln

```
/model
```

Das ist der eingebaute Umschalter. Ein eigenes Skript dafür wäre eine
Doppelung, die gepflegt werden müsste.

Dauerhaft über eine Umgebungsvariable:

```bash
export ANTHROPIC_MODEL=claude-sonnet-5     # Beispiel
```

### Ein fremdes Modell beauftragen

Über den GitHub-Actions-Lauf **OpenRouter**, Felder:

| Feld | Bedeutung |
|---|---|
| `frage` | der Auftrag |
| `modell` | leer = günstigstes passendes; sonst z. B. `google/gemma-4-26b-a4b-it:free` |
| `info` | Steckbriefe aller Modelle, deren ID diesen Text enthält |

Örtlich, wenn ein Schlüssel gesetzt ist:

```bash
export OPENROUTER_API_KEY=…               # niemals in eine Datei schreiben
python3 scripts/openrouter.py --pruefen --fragen "Ein Satz über Hundesofas."
python3 scripts/openrouter.py --info gpt-5.6      # Steckbriefe
```

---

## Schlüssel

**Kein Schlüssel gehört in den Quellcode oder in eine Datei im
Repository.** Zwei zulässige Orte:

1. **GitHub Secrets** — für Läufe. Vorhanden: `OPEN_ROUTER`,
   `SHOPIFY_CLI_THEME_TOKEN`. Der Workflow hängt `OPEN_ROUTER` auf die
   Variable `OPENROUTER_API_KEY` um.
2. **Umgebungsvariable auf deinem Rechner** — für örtliche Läufe.

Am 10.08.2026 stand ein maskiertes Schlüsselfragment im Bericht, weil
OpenRouters Feld `label` den maskierten Schlüssel enthält und ungeprüft
durchgereicht wurde. `scripts/openrouter.py` hat seitdem eine
Positivliste: nur ausdrücklich freigegebene Felder kommen in den Bericht.

---

## Verfügbare Modelle über OpenRouter

Gemessen am 10.08.2026, nicht aus der Erinnerung:

| | |
|---|---|
| Modelle gesamt | **399** |
| davon ohne Kosten | 17 |
| Anbieter | openai (94), qwen (49), google (39), anthropic (28), mistralai (18), z-ai (13), deepseek (12), nvidia (11) |

Aktuelle Liste jederzeit:

```bash
python3 scripts/openrouter.py --info ""      # alle
python3 scripts/openrouter.py --info gpt     # gefiltert
```

**Kein Modell ist fest eingetragen.** Ohne Angabe wählt das Skript nach
Guthaben: mit Guthaben das günstigste bezahlte, ohne Guthaben die
Gratisstufe.

---

## Zurücksetzen

Es wurde nichts verändert, also gibt es nichts zurückzusetzen. Falls du
später selbst etwas gesetzt hast:

```bash
unset ANTHROPIC_MODEL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY
unset CLAUDE_CODE_USE_BEDROCK CLAUDE_CODE_USE_VERTEX
# ANTHROPIC_BASE_URL NICHT löschen, solange die Umgebung sie selbst setzt
```

Die neuen Dateien entfernen:

```bash
git rm scripts/modelltest.py README_SETUP.md
```

---

## Zwei Eigenheiten dieser Umgebung

1. **`ANTHROPIC_BASE_URL` ist hier von der verwalteten Umgebung gesetzt**
   — auf `https://api.anthropic.com`, also das Standardziel. Wer sie
   überschreibt, kappt die laufende Sitzung.
2. **Der Container ist flüchtig.** Lokal gesetzte Variablen und Dateien
   außerhalb des Repositorys sind beim nächsten Mal weg. Dauerhaft ist
   nur, was committet ist.

---

## Wenn du OpenRouter trotzdem als Motor versuchen willst

Es gibt genau **eine** offene Frage, und sie ist von hier nicht zu
beantworten, weil die Arbeitsumgebung openrouter.ai nicht erreicht:

**Beantwortet OpenRouter `POST https://openrouter.ai/api/v1/messages` im
Anthropic-Messages-Format?**

Auf deinem Rechner prüfbar:

```bash
curl -s -o /dev/null -w "%{http_code}\n" \
  -X POST https://openrouter.ai/api/v1/messages \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"anthropic/claude-sonnet-4.5","max_tokens":16,
       "messages":[{"role":"user","content":"ping"}]}'
```

* **200** → der Endpunkt existiert. Dann wäre `ANTHROPIC_BASE_URL` auf
  OpenRouter technisch denkbar — aber laut Dokumentation weiterhin
  ausschließlich für Claude-Modelle unterstützt, und ohne Zusage, dass
  künftige Claude-Code-Funktionen durchgereicht werden.
* **404** → der Endpunkt existiert nicht. Damit ist das Thema erledigt.

Sag mir das Ergebnis, dann geht es von dort weiter. **Schick den Schlüssel
nicht mit.**
