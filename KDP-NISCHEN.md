# KDP-Nischen

Stand: 2026-08-14

Gemessen auf den öffentlichen Amazon-Trefferlisten und Produktseiten. **Der Bestseller-Rang (BSR) ist die belastbare Zahl** — innerhalb desselben Marktplatzes direkt vergleichbar, niedriger heißt mehr Verkäufe. Die Umrechnung in Stückzahlen ist eine Schätzung.

Verwendete Konstanten: `täglich = 100000 × BSR^-0.85`. Öffentlich kursierende Kalibrierung, **nicht selbst validiert** — gut für Größenordnungen, nicht für Planung.

| Nische | Markt | BSR Median | BSR bester | Verk./Tag (gesch.) | Bewertungen Median | Preis Median | im 70-%-Fenster | in KU | gesponsert |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| secret baby romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| billionaire romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| ceo romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| boss employee romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| fake marriage romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| enemies to lovers romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| arranged marriage romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |
| billionaire boss romance | www.amazon.com | FEHLER | – | – | – | – | – | – | – |

## Fehlgeschlagen

- **secret baby romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **billionaire romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **ceo romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **boss employee romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **fake marriage romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **enemies to lovers romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **arranged marriage romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.
- **billionaire boss romance** — Keine Treffer gelesen. Entweder blockiert Amazon den Abruf oder die Seitenstruktur hat sich geaendert. NICHT als 'keine Konkurrenz' deuten.

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

---

## Nachtrag 14.08.2026, dritter Lauf — vollständig, mit Datenschaden

### Was schiefging

Zwei Läufe haben sich überholt (18:33 und 18:45). Der Commit-Schritt
rebased mit `-X theirs` — für Bildschirmfotos richtig, für Datendateien
falsch. `daten/kdp-nischen.json` wurde **hunk-weise zusammengeführt**:
15 statt 8 Einträge, und ein Eintrag trug das Etikett des einen Laufs
(„chef und angestellte") bei den Daten des anderen (Finanzratgeber).

**Die Markdown-Tabelle ist davon nicht betroffen** — sie wurde in einem
Zug ersetzt, alle acht Zeilen gleichzeitig. Nachgeprüft im Diff.
**Die JSON dieses Laufs ist für Titel-Details unbrauchbar.**

An der Wurzel behoben: `concurrency` in `website.yml`, Läufe warten
jetzt aufeinander.

Zweiter Schaden: Ein Lauf, der noch mit der alten Skriptfassung
unterwegs war, hat die Handnotizen überschrieben — der Marker-Schutz kam
zu spät für bereits laufende Jobs. Aus der Historie zurückgeholt.
**Lehre: Eine Korrektur schützt nicht vor Läufen, die schon fliegen.**

### Reproduzierbarkeit — belegt

Drei Kontrollbegriffe lieferten über zwei Läufe hinweg **identische
Werte** (chef und angestellte: 14856/14522/82/4,99; scheinehe:
15333/792/105; enemies to lovers: 1385/157/1051). Die Läufe lagen ~12
Minuten auseinander, BSR aktualisiert stündlich. Das Messgerät ist
also **stabil** — es liefert bei gleicher Lage gleiche Zahlen.

### Nachfrage gegen Verankerung, vollständig

| Nische | BSR Median | BSR bester | Bewertungen | in KU | Lesart |
|---|---:|---:|---:|---:|---|
| **geheimes baby liebesroman** | **671** | 119 | **43** | 10/10 | **Nachfrage ohne Platzhirsch** |
| **milliardär liebesroman** | **902** | 82 | **56** | 10/10 | **Nachfrage ohne Platzhirsch** |
| billionaire romance deutsch | 428 | 20 | 403 | 9/10 | besetzt |
| ceo liebesroman | 1068 | 237 | 1056 | 10/10 | besetzt |
| enemies to lovers deutsch | 1385 | 157 | 1051 | 8/10 | besetzt |
| scheinehe liebesroman | 15333 | 792 | 105 | 10/10 | wenig Nachfrage |
| chef und angestellte | 14856 | 14522 | 82 | 9/10 | wenig Nachfrage |
| milliardärsboss liebesroman | 32050 | 11710 | 114 | 9/10 | wenig Nachfrage |

**Korrektur an der eigenen Empfehlung:** In `ROMANCE.md` stand „chef und
angestellte" als offenste Nische — abgeleitet aus dem unvollständigen
zweiten Lauf, in dem ausgerechnet die Kernbegriffe gescheitert waren.
Jetzt gemessen: Diese Nische hat **rund 20-mal weniger Nachfrage** als
„geheimes baby" und „milliardär" bei vergleichbarer Verankerung. Die
Empfehlung war auf Sand gebaut und ist hiermit ersetzt.

**KU bleibt bei 8 bis 10 von 10** über alle acht Nischen. Der Befund
aus dem zweiten Lauf hält.

### Weiterhin offen

Die Spalte **gesponsert** zeigt trotz reparierter Selektoren erneut in
**allen acht** Nischen exakt `0/10`. Der Reparaturversuch hat nicht
gewirkt. Weiterhin **nicht als „keine Anzeigenkonkurrenz" lesen** —
entweder greift der Selektor immer noch nicht, oder Amazon liefert an
den Runner Seiten ohne Anzeigen aus.
