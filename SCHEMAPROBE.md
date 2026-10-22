# Schemaprobe — strukturierte Daten (JSON-LD)

Rein lesend geprüft, keine Theme-Änderung. Prüft, ob und wie vollständig Product-Schema auf Produktseiten steht — das beeinflusst laut Recherche die Klickrate in der Google-Suche, unabhängig vom Ranking selbst.

## https://www.homeeins.de/products/buerostuhl-premium-relaxfunktion-135-grad

0 `application/ld+json`-Block(e) gefunden, davon 0 mit `@type: Product`.

**Kein Product-Schema gefunden.** Das ist ein leeres Ergebnis, kein bestätigtes "nichts da" — möglich, dass es dynamisch nach dem gemessenen Zeitpunkt nachlädt. Mit einer Seite gegenprüfen, die sicher ein Schema haben sollte, bevor das als Befund gilt.

## https://www.homeeins.de/products/kratzbaum-katzen-kompakt-plusch

3 `application/ld+json`-Block(e) gefunden, davon 4 mit `@type: Product`.

| Feld | vorhanden |
|---|---|
| `gtin` | ❌ |
| `gtin8` | ❌ |
| `gtin12` | ❌ |
| `gtin13` | ❌ |
| `gtin14` | ❌ |
| `mpn` | ✅ |
| `brand` | ✅ |
| `sku` | ✅ |
| `aggregateRating` | ❌ |
| `review` | ❌ |
| `offers` | ✅ |
| `image` | ✅ |
| `description` | ✅ |

`offers`-Unterfelder: `price` ✅, `availability` ✅, `priceCurrency` ✅

