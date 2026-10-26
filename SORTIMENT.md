# Sortiment — gemessen am 22.10.2026

Über die Shopify-Admin-Anbindung ausgelesen, nicht geschätzt. Rein
lesend, nichts am Laden geändert.

## Zuerst eine Korrektur

`CLAUDE.md` nennt seit August **146 Produkte**. Gemessen sind es heute
**96 aktive**. Die Zahl war veraltet, und ich habe sie in diesem
Gespräch mehrfach nachgesprochen, statt sie nachzusehen.

Damit fällt auch der Satz, der daran hing — „die heutigen Produkte
stehen in Kategorien mit null Bestellungen". Das stimmt so nicht mehr.

## Das Preisband trifft inzwischen

Aus `GELDVERDIENEN.md`: Alle sieben jemals verkauften Artikel waren
verschenkbare Wohn-Deko zwischen **30 und 130 €**.

| | Produkte |
|---|---|
| aktiv insgesamt | **96** |
| mit mindestens einer Variante in 30–130 € | **74** |
| nur außerhalb des Bandes | **22** |
| über die Grenze hinweg (mehrere Varianten) | 5 |

**77 % des Sortiments liegt im nachgewiesenen Preisband.** Das ist eine
deutliche Verbesserung gegenüber August und spricht gegen die These,
das Sortiment sei das Hauptproblem.

Die Warentypen im Band — Aufbewahrungskörbe, Handtuch-Sets,
Magazinhalter, Pflanzkübel, Schuhbänke, Hundemöbel — passen zum Muster
„verschenkbare Wohn-Deko". Das Sortiment zeigt in die richtige
Richtung.

## ✅ Erledigt am 22.10.2026: Die Rabatt-Texte sind bereinigt

**Es waren sechs Produkte, nicht vier.** Erst beim Durchsuchen aller 96
aktiven Beschreibungen kamen die letzten beiden dazu.

Geändert wurde das Minimum: der Zusatz `, zeitlich begrenzt.` ist raus,
der Rabattcode bleibt stehen.

```
vorher:   15% Rabatt auf Hundemöbel, zeitlich begrenzt.
nachher:  15% Rabatt auf Hundemöbel.
```

| Produkt | Code |
|---|---|
| Erhöhtes Hundebett 95 cm | MEHRHUNDE15 |
| Erhöhtes Hundebett 90 cm | MEHRHUNDE15 |
| Erhöhtes Hundebett 80 cm | MEHRHUNDE15 |
| Hundebett & Katzenbett Kunstleder | MEHRHUNDE15 |
| Erhöhtes Hundebett XXL mit Erweiterung | MEHRHUNDE15 |
| Selbstreinigende Katzentoilette 65L | WILLKOMMEN10 |

Mit frischen Daten gegengeprüft: alle sechs Beschreibungen enthalten
den Zusatz nicht mehr, die Rabattcodes stehen unverändert da.

**Rückbau:** Die Originaltexte liegen vollständig in
`daten/rabatt-rueckbau-2026-10-22.json`. Wer die Frist zurückhaben
will, braucht dann aber ein echtes Enddatum.

### Warum das nötig war

Drei Produktbeschreibungen beginnen mit:

> 🎉 Jetzt mit Code MEHRHUNDE15 – 15% Rabatt auf Hundemöbel,
> **zeitlich begrenzt**.

Eine vierte mit `WILLKOMMEN10`, ebenfalls „zeitlich begrenzt".

**Das ist erfundene Knappheit.** Es steht kein Enddatum dabei, und die
betroffenen Produkte wurden zuletzt am 20.10.2026 angefasst — die
„Begrenzung" läuft also mindestens seit Tagen und endet nie. Genau das
verbietet `CLAUDE.md` Regel 3, und es fällt unter die
Omnibus-Richtlinie (§ 5a/5b UWG).

Am 9.8.2026 wurden solche Inhalte schon einmal aus diesem Shop
entfernt. Sie sind zurück.

**Zwei saubere Lösungen, beide in Minuten gemacht:**

1. Ein **echtes Enddatum** nennen: „bis 31.10.2026". Dann ist die
   Aussage wahr und die Begrenzung überprüfbar.
2. Oder „zeitlich begrenzt" **streichen**. Der Rabattcode bleibt, die
   Falschaussage geht.

Ein Rabatt ist erlaubt. Eine erfundene Frist nicht.

## ✅ Erledigt am 26.10.2026: neun leere SEO-Felder geschlossen

Über alle 96 aktiven Produkte ausgelesen, nicht gestichprobt:

| | vorher | nachher |
|---|---|---|
| ohne `seo.title` | **6** | 0 |
| ohne `seo.description` | **3** | 0 |

Ein fehlender `seo.title` heißt: Google nimmt den Produkttitel, und der
ist bei diesen sechs 70–90 Zeichen lang und wird im Treffer
abgeschnitten. Eine fehlende `seo.description` heißt: Google schreibt
den Textausschnitt selbst, aus irgendeinem Satz der Seite. Genau das
ist der „rankt, wird aber nicht geklickt"-Fall aus `AUDIT.md`.

**Die sechs ohne Titel waren alle Hundemöbel** — also die Warengruppe
im nachgewiesenen Preisband. Die drei ohne Beschreibung: Bürostuhl,
Rattan-Sonnenliege, Gartenstuhl.

Alle neun Texte stammen aus vorhandenen Daten — Maße, Material,
Belastbarkeit aus den Varianten und Beschreibungen. Nichts
dazuerfunden, keine Versandaussage, kein Preisversprechen.

Bei jeder Mutation wurden **beide** `seo`-Unterfelder mitgeschickt, auch
wo nur eines fehlte — das Feld ersetzt, statt zu ergänzen
(`CLAUDE.md`). Rückbau: `daten/seo-rueckbau-2026-10-26.json`.

### Nebenbefund: ein Emoji-Titel war übrig

```
vorher:   Kompakter Kratzbaum für Katzen – Spielen, Kratzen & Entspannen in einem 🐾
nachher:  Kompakter Kratzbaum für Katzen – Sisal-Säulen und Plüsch-Liegefläche
```

Oben steht, 26 Titel seien entanglisiert und emoji-frei. Das war über
die damals geprüften Produkte richtig, über alle 96 nicht — dieser hier
stand noch. Der neue Titel nennt außerdem Material und Bauform, also
das, wonach gesucht wird.

## Weitere Funde, nach Hebel sortiert

### ✅ Erledigt: 26 Titel entanglisiert und ohne Emoji

Über alle 96 Produkte gezählt waren es **26**, nicht 15 — die
Stichprobe von 50 hatte nur die Hälfte erfasst.

```
vorher:   🌲 PINE CUBE PLANTER – Massiver Holz-Pflanzkasten für Garten…
nachher:  Pflanzkasten aus Kiefernholz – Massiver Blumenkasten für Garten…

vorher:   ✈️ TRAVEL ELITE TROLLEY SET – Stilvoll reisen. Perfekt organisiert.
nachher:  Kofferset 4-teilig – Hartschalen-Trolleys für Reise und Urlaub
```

Grundsatz dabei: **Der Titel nennt, was es ist, in deutschen
Suchbegriffen.** „PINE CUBE PLANTER" sucht niemand; „Pflanzkasten
Kiefernholz" schon.

Alle Angaben in den neuen Titeln stammen aus den vorhandenen Daten —
`4-teilig` und `2er-Set` aus den Adressen, `bis 350 kg` aus den
Varianten, `230–250 cm` aus der Produktkennung, `10-teilig` aus der
Beschreibung. Nichts dazuerfunden.

Ein Nebenbefund: Zwei Produkte hießen **wortgleich**
„FOLD & GO HANDWAGEN". Sie unterscheiden sich durch das Sonnendach —
das steht jetzt im Titel, sonst konkurrieren sie in der Suche
gegeneinander.

Keine Adressen geändert, also **keine Links gebrochen**. Die alten
Titel liegen in `daten/titel-rueckbau-2026-10-22.json`.

### Noch offen: englische Adressen

`🌲 PINE CUBE PLANTER`, `✈️ TRAVEL ELITE TROLLEY SET`,
`😻 XXL KRATZBAUM`, `🛠️ HEAVY DUTY GARTENWAGEN`.

Das war schon einmal behoben und ist zurückgekommen — offenbar bei
jedem Produkt, das seither neu aus CJ importiert wurde. Emojis am
Titelanfang schneiden in Google-Treffern und in Vergleichsportalen
schlecht ab, weil sie die ersten Zeichen belegen.

### Englische Produktnamen in einem deutschen Laden

`PINE CUBE PLANTER`, `GARDEN STORAGE PRO 420L`, `FOLD & STORE`,
`INDUSTRIAL EDGE PLANTER`. Das sind CJ-Originalnamen, die nicht
übersetzt wurden.

### Die Adressen sind CJ-Rohdaten

```
garden-trolley-garden-trolley-garden-trolley-garden-trolley
folding-foosball-table-121-x-folding-foosball-table
folding-handcart-with-sun-canopy-folding-handcart
plant-pots-2-pcs-blue-grey-30x-polypropylene
```

Acht von fünfzig Adressen enthalten englische Wörter, mehrere
wiederholen denselben Begriff bis zu viermal. Für deutsche Suchbegriffe
ist das die denkbar schlechteste Adresse, und sie steht in jedem
Suchergebnis mit.

Eine Adresse zu ändern verlangt eine Weiterleitung von der alten —
sonst entstehen 404er. Shopify legt die beim Umbenennen automatisch an.

### ✅ Erledigt am 26.10.2026: 44 unverkäufliche Varianten entfernt

Hier stand: „Beim Hundesofa XXL sind 2 von 5 Varianten auf 0, beim
Rattan-Ecksofa 2 von 3." Das war richtig gezählt — aber nur über die
Stichprobe von 50. **Über alle 96 aktiven Produkte gezählt waren es
29 Produkte mit 44 unverkäuflichen Varianten.** Wieder eine Messung
ohne Bezugsrahmen, und wieder zu niedrig.

Die schlimmsten Fälle waren nicht die genannten:

| Produkt | tot / gesamt |
|---|---|
| Aufbewahrungskorb aus Stoff | **4 von 6** |
| Mobiles Tennisnetz | **3 von 4** |
| Metall-Pflanzkübel schlank | **3 von 4** |
| Ergonomischer Hochstuhl | **3 von 4** |
| Trekking-Rucksack | 2 von 3 |
| Kofferset 4-teilig | 2 von 3 |

Alle 44 hatten Bestand 0 bei `inventoryPolicy DENY` — sie standen als
Auswahl da, waren aber nicht bestellbar. Kein Produkt hat dadurch
seine letzte Variante verloren; jedes ist weiter kaufbar.

Mit frischen Daten gegengeprüft: **null `availableForSale: false`
über alle 96 Produkte.**

Rückbau mit Preis, SKU und Gewicht je Variante:
`daten/varianten-rueckbau-2026-10-26.json` (die ersten beiden
Produkte) und `daten/varianten-rueckbau-2026-10-26-alle.json` (die
übrigen 27). **Nicht gemessen:** ob die CJ-Anbindung bei Nachschub
selbst wieder anlegt.

## Was das für die Prioritäten heißt

Das Sortiment ist **nicht** mehr der erste Hebel — es passt inzwischen
zum nachgewiesenen Muster. Die Reihenfolge nach heutiger Messung:

1. **Rabatt-Texte bereinigen** — rechtliches Risiko, Minutenaufwand
2. **Titel und Adressen entanglisieren** — betrifft jeden Suchtreffer
3. **Besucher holen** — danach, denn vorher sieht niemand das Ergebnis

---

*Gemessen über die Shopify-Admin-Anbindung, 22.10.2026. Die
Stichprobe für Titel, Rabatt-Texte und Adressen umfasst die ersten 50
der 74 Produkte im Preisband; die übrigen 24 sind nicht geprüft.*
