# Theme Check

Stand: 2026-08-10

Shopifys eigener Linter für Liquid, gelaufen über `theme/sandbox-neu`. Prüft, was kein Screenshot zeigt: ungültige Schemata, fehlende Übersetzungen, veraltete Filter, tote Snippets, teure Schleifen.

378 Dateien im Theme, **48 Befunde**.

| Schwere | Anzahl |
|---|---:|
| error | 1 |
| warning | 47 |

## Nach Regel

| Regel | Fälle |
|---|---:|
| `VariableName` | 33 |
| `OrphanedSnippet` | 7 |
| `UnusedAssign` | 4 |
| `UndefinedObject` | 3 |
| `ContentForHeaderModification` | 1 |

## Die ersten 25 im Einzelnen

| Datei | Zeile | Regel | Meldung |
|---|---:|---|---|
| `/home/runner/work/ponytail-test/ponytail-test/snippets/sb-speed-booster.liquid` | 55 | `ContentForHeaderModification` | Do not rely on the content of `content_for_header` |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 2 | `VariableName` | The variable 'pageType' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | ? | `OrphanedSnippet` | This snippet is not referenced by any other files |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 5 | `VariableName` | The variable 'templateType' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 9 | `VariableName` | The variable 'templateType' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 13 | `VariableName` | The variable 'templateType' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 16 | `VariableName` | The variable 'variableMapper' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 17 | `VariableName` | The variable 'variableValueMapper' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 18 | `VariableName` | The variable 'variableValueMapper' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 37 | `VariableName` | The variable 'productNotValid' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 39 | `VariableName` | The variable 'productNotValid' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 52 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 55 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 57 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 59 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 61 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 63 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 65 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 69 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 71 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 73 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 75 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 77 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 80 | `VariableName` | The variable 'variableValueItem' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/lazyload_img.liquid` | ? | `OrphanedSnippet` | This snippet is not referenced by any other files |

