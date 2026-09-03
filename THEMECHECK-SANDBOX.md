# Theme Check

Stand: 2026-08-10

Shopifys eigener Linter für Liquid, gelaufen über `arbeitskopie`. Prüft, was kein Screenshot zeigt: ungültige Schemata, fehlende Übersetzungen, veraltete Filter, tote Snippets, teure Schleifen.

369 Dateien im Theme, **8 Befunde**.

| Schwere | Anzahl |
|---|---:|
| warning | 8 |

## Nach Regel

| Regel | Fälle |
|---|---:|
| `UndefinedObject` | 3 |
| `VariableName` | 2 |
| `UnusedAssign` | 2 |
| `OrphanedSnippet` | 1 |

## Die ersten 25 im Einzelnen

| Datei | Zeile | Regel | Meldung |
|---|---:|---|---|
| `/home/runner/work/ponytail-test/ponytail-test/snippets/quick-order-product-row.liquid` | ? | `OrphanedSnippet` | This snippet is not referenced by any other files |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-list-collections.liquid` | 19 | `VariableName` | The variable 'moduloResult' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-article.liquid` | 101 | `VariableName` | The variable 'anchorId' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-search.liquid` | 273 | `UnusedAssign` | The variable 'product_settings' is assigned but not used |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-product.liquid` | 744 | `UnusedAssign` | The variable 'seo_media' is assigned but not used |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-product.liquid` | 600 | `UndefinedObject` | Unknown object 'continue' used. |
| `/home/runner/work/ponytail-test/ponytail-test/layout/password.liquid` | 39 | `UndefinedObject` | Unknown object 'scheme_classes' used. |
| `/home/runner/work/ponytail-test/ponytail-test/layout/theme.liquid` | 81 | `UndefinedObject` | Unknown object 'scheme_classes' used. |

