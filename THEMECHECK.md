# Theme Check

Stand: 2026-08-10

Shopifys eigener Linter für Liquid, gelaufen über `theme/live`. Prüft, was kein Screenshot zeigt: ungültige Schemata, fehlende Übersetzungen, veraltete Filter, tote Snippets, teure Schleifen.

379 Dateien im Theme, **236 Befunde**.

| Schwere | Anzahl |
|---|---:|
| error | 184 |
| warning | 52 |

## Nach Regel

| Regel | Fälle |
|---|---:|
| `MatchingTranslations` | 180 |
| `VariableName` | 35 |
| `OrphanedSnippet` | 5 |
| `UnusedAssign` | 5 |
| `UndefinedObject` | 3 |
| `DeprecatedFilter` | 2 |
| `ValidSchemaTranslations` | 2 |
| `LiquidHTMLSyntaxError` | 1 |
| `RemoteAsset` | 1 |
| `DeprecatedTag` | 1 |
| `ContentForHeaderModification` | 1 |

## Die ersten 25 im Einzelnen

| Datei | Zeile | Regel | Meldung |
|---|---:|---|---|
| `/home/runner/work/ponytail-test/ponytail-test/snippets/ebay-default.liquid` | 130 | `LiquidHTMLSyntaxError` | SyntaxError: expected ">" or "/>" |
| `/home/runner/work/ponytail-test/ponytail-test/snippets/sb-speed-booster.liquid` | 55 | `ContentForHeaderModification` | Do not rely on the content of `content_for_header` |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 164 | `MatchingTranslations` | A default translation for 'products.product.include_taxes' does not exist |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 181 | `MatchingTranslations` | A default translation for 'products.product.volume_pricing.price_at_each' does not exist |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 288 | `MatchingTranslations` | A default translation for 'sections.cart.taxes_and_shipping_policy_at_checkout_html' does  |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 289 | `MatchingTranslations` | A default translation for 'sections.cart.taxes_included_but_shipping_at_checkout' does not |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 290 | `MatchingTranslations` | A default translation for 'sections.cart.taxes_included_and_shipping_policy_html' does not |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 291 | `MatchingTranslations` | A default translation for 'sections.cart.taxes_and_shipping_at_checkout' does not exist |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 116 | `MatchingTranslations` | The translation for 'products.product.nested_label' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 120 | `MatchingTranslations` | The translation for 'products.product.quantity.min_of' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 120 | `MatchingTranslations` | The translation for 'products.product.quantity.max_of' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 120 | `MatchingTranslations` | The translation for 'products.product.quantity.in_cart_aria_label' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 177 | `MatchingTranslations` | The translation for 'products.product.volume_pricing.price_at_each_html' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 116 | `MatchingTranslations` | The translation for 'products.product.taxes_included' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 116 | `MatchingTranslations` | The translation for 'products.product.duties_included' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 116 | `MatchingTranslations` | The translation for 'products.product.duties_and_taxes_included' is missing |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.duties_and_taxes_included_shipping_at_checkout_with_pol |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.duties_and_taxes_included_shipping_at_checkout_without_ |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.taxes_included_shipping_at_checkout_with_policy_html' i |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.taxes_included_shipping_at_checkout_without_policy' is  |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.duties_included_taxes_at_checkout_shipping_at_checkout_ |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.duties_included_taxes_at_checkout_shipping_at_checkout_ |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.taxes_at_checkout_shipping_at_checkout_with_policy_html |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 280 | `MatchingTranslations` | The translation for 'sections.cart.taxes_at_checkout_shipping_at_checkout_without_policy'  |
| `/home/runner/work/ponytail-test/ponytail-test/locales/bg-BG.json` | 350 | `MatchingTranslations` | The translation for 'sections.quick_order_list.remove_all_single_item_confirmation' is mis |

