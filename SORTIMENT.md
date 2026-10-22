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

## Weitere Funde, nach Hebel sortiert

### 15 von 50 Titeln beginnen mit einem Emoji

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

### Ausverkaufte Varianten stehen weiter im Laden

Beim Hundesofa XXL sind 2 von 5 Varianten auf 0, beim Rattan-Ecksofa 2
von 3. Wer die auswählt, läuft in eine Sackgasse.

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
