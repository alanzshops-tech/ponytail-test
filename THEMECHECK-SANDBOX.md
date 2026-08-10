# Theme Check

Stand: 2026-08-10

Shopifys eigener Linter für Liquid, gelaufen über `arbeitskopie`. Prüft, was kein Screenshot zeigt: ungültige Schemata, fehlende Übersetzungen, veraltete Filter, tote Snippets, teure Schleifen.

369 Dateien im Theme, **47 Befunde**.

| Schwere | Anzahl |
|---|---:|
| error | 3 |
| warning | 44 |

## Nach Regel

| Regel | Fälle |
|---|---:|
| `VariableName` | 33 |
| `UnusedAssign` | 5 |
| `UndefinedObject` | 3 |
| `OrphanedSnippet` | 2 |
| `ValidSchemaTranslations` | 2 |
| `DeprecatedTag` | 1 |
| `ContentForHeaderModification` | 1 |

## Die ersten 25 im Einzelnen

| Datei | Zeile | Regel | Meldung |
|---|---:|---|---|
| `/home/runner/work/ponytail-test/ponytail-test/snippets/sb-speed-booster.liquid` | 55 | `ContentForHeaderModification` | Do not rely on the content of `content_for_header` |
| `/home/runner/work/ponytail-test/ponytail-test/sections/featured-product.liquid` | 742 | `ValidSchemaTranslations` | 't:sections.main-product.blocks.icon_with_text.settings.content.label' does not have a mat |
| `/home/runner/work/ponytail-test/ponytail-test/sections/featured-product.liquid` | 743 | `ValidSchemaTranslations` | 't:sections.main-product.blocks.icon_with_text.settings.content.info' does not have a matc |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/tapita-seo-schema.liquid` | 2 | `VariableName` | The variable 'pageType' uses wrong naming format |
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

