# Theme Check

Stand: 2026-08-14

Shopifys eigener Linter für Liquid, gelaufen über `theme/arbeitskopie`. Prüft, was kein Screenshot zeigt: ungültige Schemata, fehlende Übersetzungen, veraltete Filter, tote Snippets, teure Schleifen.

357 Dateien im Theme, **12 Befunde**.

| Schwere | Anzahl |
|---|---:|
| error | 1 |
| warning | 11 |

## Nach Regel

| Regel | Fälle |
|---|---:|
| `UndefinedObject` | 6 |
| `VariableName` | 2 |
| `UnusedAssign` | 2 |
| `LiquidHTMLSyntaxError` | 1 |
| `OrphanedSnippet` | 1 |

## Die ersten 25 im Einzelnen

| Datei | Zeile | Regel | Meldung |
|---|---:|---|---|
| `/home/runner/work/ponytail-test/ponytail-test/snippets/ebay-default.liquid` | 130 | `LiquidHTMLSyntaxError` | SyntaxError: expected ">" or "/>" |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/quick-order-product-row.liquid` | ? | `OrphanedSnippet` | This snippet is not referenced by any other files |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-list-collections.liquid` | 19 | `VariableName` | The variable 'moduloResult' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-article.liquid` | 101 | `VariableName` | The variable 'anchorId' uses wrong naming format |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-search.liquid` | 273 | `UnusedAssign` | The variable 'product_settings' is assigned but not used |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-product.liquid` | 744 | `UnusedAssign` | The variable 'seo_media' is assigned but not used |
| `/home/runner/work/ponytail-test/ponytail-test/sections/main-product.liquid` | 600 | `UndefinedObject` | Unknown object 'continue' used. |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/header-drawer.liquid` | 27 | `UndefinedObject` | Unknown object 'section' used. |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/header-drawer.liquid` | 22 | `UndefinedObject` | Unknown object 'section' used. |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/header-drawer.liquid` | 11 | `UndefinedObject` | Unknown object 'section' used. |
| `/home/runner/work/ponytail-test/ponytail-test/layout/password.liquid` | 39 | `UndefinedObject` | Unknown object 'scheme_classes' used. |
| `/home/runner/work/ponytail-test/ponytail-test/layout/theme.liquid` | 81 | `UndefinedObject` | Unknown object 'scheme_classes' used. |

