# Vertriebskanäle — was in Shopify bereits verbunden ist

Stand 13.08.2026, per `mcp__Shopify__graphql_query` live geprüft.

**Warum diese Datei existiert:** Genau derselbe blinde Fleck wie bei
`SOCIAL.md` — Shopify-Sales-Channel-Verbindungen hinterlassen keine Spur
im Git. Beim Recherchieren nach "Google Merchant Center einrichten" als
neuer Traffic-Chance stellte sich heraus: die Kanäle sind längst
verbunden, nur nirgends dokumentiert.

## Befund

`shop { channels: publications }` zeigt 12 verbundene Kanäle:
Onlineshop, Facebook & Instagram, **Google & YouTube**, TikTok,
Pinterest, Inbox, Shop, **Microsoft Channel** (Bing Shopping),
**Amazon Channel - CED**, Schaltfläche „Kaufen", Collective: Supplier,
Instagram Shop-AI, Microsoft Copilot.

Stichprobe von 20 aktiven Produkten (verschiedene Kategorien, verteilt
über den Katalog): **alle 20** sind zu Google & YouTube, Microsoft
Channel, Amazon Channel, TikTok, Pinterest und Instagram Shop-AI
veröffentlicht (`isPublished: true`). Kein Ausreißer gefunden — starkes
Indiz, dass das für den ganzen Katalog gilt, aber nicht für alle 146
Produkte einzeln geprüft.

**Kein eBay-Kanal in der Liste** — passt zur bekannten Tatsache, dass
die eBay-Shopify-Integration nicht verbindet (`EBAY-START.md`).

## Was das bedeutet — und was nicht

**FAKT:** Die Produkte sind auf Shopify-Seite an Google, Bing und
Amazon durchgereicht.

**EINSCHÄTZUNG, ausdrücklich als solche:** Das heißt **nicht**
automatisch, dass die Google-Merchant-Center-Feeds tatsächlich
freigegeben sind und Produkte wirklich in der Google-Shopping-Ansicht
erscheinen. Zwischen "in Shopify veröffentlicht" und "bei Google
genehmigt und sichtbar" liegen: Konto-Verifizierung, GTIN/Kategorie-
Datenqualität, Feed-Fehler, Prüfzeit. Das lässt sich von hier aus nicht
prüfen — die Runner-Umgebung erreicht kein Merchant-Center-Dashboard,
und die Search-Console-API (die hier läuft) meldet nur normale
Web-Suche, keine Shopping-Impressionen. Wer das wirklich wissen will,
muss im Google-Merchant-Center-Konto selbst nachsehen (Diagnose-Tab).

## GTIN-Fund und Behebung (13.08.2026, nachts)

**Gemessen:** Stichprobe von 20 aktiven Produkten — `barcode` ist bei
**allen 20** leer (`null`). Gegengeprüft in allen CJ-Rohdaten
(`daten/cj-*.json`): kein GTIN-, EAN- oder UPC-Feld irgendwo vorhanden.
Das sind generische Dropshipping-Artikel ohne echte Herstellerkennung —
kein Datenpflege-Versäumnis, sondern der Normalfall bei diesem
Geschäftsmodell.

**Warum das wichtig ist:** Google Merchant Center lehnt Angebote ohne
GTIN/MPN ab oder schränkt ihre Sichtbarkeit ein, *außer* das Produkt ist
explizit als "ohne Standard-Kennung" markiert. Shopifys "Google &
YouTube"-App liest dafür das Metafeld
`mm-google-shopping.custom_product` (boolean) — via
`metafieldDefinitions`-Abfrage gefunden, nicht geraten. Es war auf
allen geprüften Produkten ungesetzt.

**Behoben:** `custom_product = true` per `metafieldsSet` auf allen 101
aktiven Produkten gesetzt (5 Batches à ≤25, 0 `userErrors`, per
Stichprobe zurückgelesen bestätigt). Die Marke (`vendor: "Homeeins"`)
war bereits überall gesetzt — zusammen mit `custom_product = true`
sollte das dem Merchant-Center-Feed die fehlenden Signale liefern, die
er für "kein GTIN vorhanden, trotzdem gültig" braucht.

**Weiterhin ungeprüft:** ob das den Feed tatsächlich verbessert, zeigt
sich nur im Merchant-Center-Diagnose-Tab selbst — nicht von hier aus
einsehbar. Das ist die richtige nächste Prüfung für einen Menschen.

**Ebenso ungeprüft:** Amazon Channel und Microsoft Channel könnten
genauso angebunden, aber mit Fehlern im Hintergrund liegen (abgelehnte
Angebote, fehlende Kategoriezuordnung). Nicht behauptet, nur weil der
Kanal in Shopify als verbunden auftaucht.

## Für die Traffic-Recherche

Die ursprünglich als "neue Chance" recherchierte Google-Shopping-
Einrichtung ist damit vermutlich **kein Lückenschluss von null auf
etwas**, sondern höchstens eine Qualitätsprüfung eines bereits
laufenden Feeds. Bevor hier Zeit investiert wird: erst prüfen (Mensch,
im Merchant-Center-Dashboard), ob der Feed überhaupt Fehler hat, statt
eine Neu-Einrichtung vorzuschlagen, die schon existiert.
