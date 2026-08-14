# KDP-Nischen

Stand: 2026-08-14

Gemessen auf den öffentlichen Amazon-Trefferlisten und Produktseiten. **Der Bestseller-Rang (BSR) ist die belastbare Zahl** — innerhalb desselben Marktplatzes direkt vergleichbar, niedriger heißt mehr Verkäufe. Die Umrechnung in Stückzahlen ist eine Schätzung.

Verwendete Konstanten: `täglich = 100000 × BSR^-0.85`. Öffentlich kursierende Kalibrierung, **nicht selbst validiert** — gut für Größenordnungen, nicht für Planung.

| Nische | Markt | BSR Median | BSR bester | Verk./Tag (gesch.) | Bewertungen Median | Preis Median | im 70-%-Fenster | in KU | gesponsert |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| milliardär liebesroman | www.amazon.de | FEHLER | – | – | – | – | – | – | – |
| billionaire romance deutsch | www.amazon.de | FEHLER | – | – | – | – | – | – | – |
| chef und angestellte liebesroman | www.amazon.de | 14856 | 14522 | 28.44 | 82 | 4.99 | 1/10 | 9/10 | 0/10 |
| enemies to lovers deutsch | www.amazon.de | 1385 | 157 | 213.68 | 1051 | 14.99 | 0/10 | 8/10 | 0/10 |
| scheinehe liebesroman | www.amazon.de | 15333 | 792 | 27.68 | 105 | – | 0/10 | 10/10 | 0/10 |
| zweite chance liebesroman | www.amazon.de | 207921 | 377 | 3.02 | 9 | 3.99 | 3/10 | 7/10 | 0/10 |
| reicher mann liebesroman | www.amazon.de | 186383 | 25504 | 3.31 | 32 | 3.99 | 1/10 | 9/10 | 0/10 |
| dark romance deutsch | www.amazon.de | 245 | 171 | 931.56 | 2345 | 14.49 | 2/10 | 4/10 | 0/10 |

## Fehlgeschlagen

- **milliardär liebesroman** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **billionaire romance deutsch** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.

## Wie zu lesen

- **BSR Median niedrig** = viel Nachfrage in dieser Nische.
- **Bewertungen Median niedrig** = die Führenden sitzen locker, ein neuer Titel kann aufschließen. Hohe Werte heißen: dort steht jemand seit Jahren.
- **Viele gesponserte Treffer** = die Suche wird beworben, organisch sichtbar zu werden ist teurer.
- **in KU** = wie viele Titel bei Kindle Unlimited liegen (Preis 0,00 €). Hoher Anteil heißt: In dieser Nische wird gelesen, nicht gekauft — Einnahmen kommen dann über Seitenaufrufe, nicht über Tantiemen je Verkauf.
- **im 70-%-Fenster** = wie viele Titel zwischen 2,99 und 9,99 € liegen. Weit darüber heißt: Der Markt trägt höhere Preise, aber die Tantieme fällt auf 35 %.

Die beste Nische hat **niedrigen BSR bei niedrigen Bewertungszahlen**. Das ist Nachfrage ohne festsitzende Platzhirsche.

<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->
---

## Auswertung 14.08.2026 — und was diese Zahlen NICHT hergeben

### Vier Einschränkungen zuerst

**1. Die zwei wichtigsten Begriffe fehlen weiterhin.** „milliardär
liebesroman" und „billionaire romance deutsch" sind erneut gescheitert,
und wieder waren es die ersten beiden der Liste. Die Consent-Behandlung
hat also nicht gereicht. Ausgerechnet die Kernbegriffe der gewählten
Richtung sind ungemessen.

**2. Die Spalte „gesponsert" ist kaputt, nicht leer.** Sie zeigt in
**allen sechs** Nischen exakt `0/10`. Dass auf amazon.de bei
Liebesroman-Suchen gar keine Anzeigen laufen, ist unglaubwürdig — ein
gleichförmiger Nullwert über alle Fälle ist das Muster eines defekten
Selektors, nicht eines Befunds. **Nicht als „keine Anzeigenkonkurrenz"
lesen.**

**3. Die Stichprobe ist winzig.** Je Nische wurden nur 3 bis 5
BSR-Werte gelesen. Ein Median aus drei Zahlen ist eine Andeutung, keine
Messung.

**4. Der Median verdeckt hier mehr, als er zeigt.** Die
Bewertungszahlen sind zweigipflig verteilt:

| Nische | Bewertungen der Spitzentitel einzeln |
|---|---|
| scheinehe liebesroman | 1101, 715, **9, 5**, 105 |
| reicher mann liebesroman | **1**, 1148, **2**, 63 |
| chef und angestellte | 139, 25, **2**, 858 |
| dark romance deutsch | 2414, 292, 2898, 212, 2345 |

Bei „scheinehe" sitzen zwei Titel mit 700–1100 Bewertungen und drei mit
fast keinen. Der Median von 105 beschreibt keinen davon.

### Was trotzdem robust ist

**Kindle Unlimited beherrscht den deutschen Romance-Markt.** In jeder
gemessenen Nische liegen **7 bis 10 von 10 Titeln in KU**:

| Nische | in KU |
|---|---|
| scheinehe liebesroman | 10/10 |
| chef und angestellte | 9/10 |
| reicher mann liebesroman | 9/10 |
| enemies to lovers deutsch | 8/10 |
| zweite chance liebesroman | 7/10 |
| dark romance deutsch | 4/10 |

Das ist der wichtigste Befund des ganzen Laufs und stand in **keiner**
der recherchierten Quellen. Die Folge: In diesem Markt wird nicht
gekauft, sondern **gelesen**. Einnahmen kommen über Seitenaufrufe
(KENP), nicht über Tantiemen je Verkauf. Damit ist die ganze
Preisstrategie aus Abschnitt 7 von `DIGITAL.md` — das
2,99–9,99-€-Fenster für 70 % — für Romance zweitrangig. Nur **0 bis 3
von 10** Titeln liegen überhaupt darin.

Das ändert auch, was ein Buch leisten muss: Bei KU zählt, dass es **zu
Ende gelesen** wird. Ein Titel, der nach 20 % abgebrochen wird, bringt
20 % der Seiten.

### Nachfrage gegen Verankerung

| Nische | BSR (Spanne) | Bewertungen | Lesart |
|---|---|---|---|
| **dark romance deutsch** | 171–2888 | 212–2898 | riesige Nachfrage, **Verlage sitzen fest** |
| **enemies to lovers** | 157–5513 | 98–2898 | starke Nachfrage, **ebenfalls besetzt** |
| **scheinehe** | 792–70272 | 5–1101 | mittel, **gemischt besetzt** |
| **chef und angestellte** | 14522–78185 | 2–858 | mittel, **eher offen** |
| **zweite chance** | 377–291434 | 1–124 | **kaum Nachfrage**, aber auch niemand da |
| **reicher mann** | 25504–265772 | 1–1148 | kaum Nachfrage |

**Es gibt in dieser Stichprobe keinen klaren Gewinner.** Wo Nachfrage
ist, sitzen etablierte Titel; wo niemand sitzt, ist auch keine Nachfrage.
Das ist das erwartbare Ergebnis eines funktionierenden Marktes, und es
wäre unredlich, daraus eine Empfehlung zu konstruieren.

Am ehesten offen wirkt **„chef und angestellte"** — mittlere Nachfrage
bei überwiegend niedrigen Bewertungszahlen. Das ist eine Andeutung aus
drei BSR-Werten, keine Grundlage für eine Entscheidung.

### Was der nächste Lauf klären muss

1. Die beiden gescheiterten Kernbegriffe zum Laufen bringen
2. Den Selektor für gesponserte Treffer reparieren
3. Stichprobe erhöhen (`--details 10` statt 5)
4. Dieselben Begriffe auf **amazon.com** messen — dann steht die Frage
   Deutsch oder Englisch in einer Tabelle statt im Raum
