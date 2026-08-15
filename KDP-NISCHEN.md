# KDP-Nischen

Stand: 2026-08-15

Gemessen auf den öffentlichen Amazon-Trefferlisten und Produktseiten. **Der Bestseller-Rang (BSR) ist die belastbare Zahl** — innerhalb desselben Marktplatzes direkt vergleichbar, niedriger heißt mehr Verkäufe. Die Umrechnung in Stückzahlen ist eine Schätzung.

Verwendete Konstanten: `täglich = 100000 × BSR^-0.85`. Öffentlich kursierende Kalibrierung, **nicht selbst validiert** — gut für Größenordnungen, nicht für Planung.

| Nische | Markt | BSR Median | BSR bester | Verk./Tag (gesch.) | Bewertungen Median | Preis Median | im 70-%-Fenster | in KU | gesponsert |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| geheimes baby liebesroman | www.amazon.de | 792 | 124 | 343.62 | 46 | – | 0/10 | 10/10 | 0/10 |
| milliardär liebesroman | www.amazon.de | 411 | 92 | 600.11 | 64 | – | 0/10 | 10/10 | 0/10 |
| ceo liebesroman | www.amazon.de | 659 | 267 | 401.74 | 523 | – | 0/10 | 10/10 | 0/10 |
| zweite chance liebesroman | www.amazon.de | 217072 | 401 | 2.91 | 9 | 4.62 | 3/10 | 7/10 | 0/10 |

## Wie zu lesen

- **BSR Median niedrig** = viel Nachfrage in dieser Nische.
- **Bewertungen Median niedrig** = die Führenden sitzen locker, ein neuer Titel kann aufschließen. Hohe Werte heißen: dort steht jemand seit Jahren.
- **Viele gesponserte Treffer** = die Suche wird beworben, organisch sichtbar zu werden ist teurer.
- **in KU** = wie viele Titel bei Kindle Unlimited liegen (Preis 0,00 €). Hoher Anteil heißt: In dieser Nische wird gelesen, nicht gekauft — Einnahmen kommen dann über Seitenaufrufe, nicht über Tantiemen je Verkauf.
- **im 70-%-Fenster** = wie viele Titel zwischen 2,99 und 9,99 € liegen. Weit darüber heißt: Der Markt trägt höhere Preise, aber die Tantieme fällt auf 35 %.

Die beste Nische hat **niedrigen BSR bei niedrigen Bewertungszahlen**. Das ist Nachfrage ohne festsitzende Platzhirsche.

## Kategorien der Spitzentitel

In welchen Unterkategorien die gemessenen Titel stehen und auf welchem Rang der beste von ihnen dort liegt. Das ist die Liste, aus der bei KDP die drei Kategorien gewählt werden. Die Oberkategorien (Kindle-Shop, Bücher) sind ausgelassen, weil sie bei jedem Titel stehen und nichts unterscheiden.

**Ein niedriger bester Rang heißt: dort ist es eng.** Eine Kategorie, in der der beste gemessene Titel auf Rang 40 steht, ist leichter zu erreichen als eine, in der er auf Rang 2 steht.

**geheimes baby liebesroman**

| Kategorie | Titel darin | bester Rang |
|---|---:|---:|
| Dramatik - Weibliche Autoren | 2 | 1 |
| Rockstar-Romanze | 2 | 1 |
| Scheidung | 2 | 3 |
| Dark Romance | 2 | 532 |
| Dramen & Theaterstücke von Frauen | 1 | 1 |
| Romantische Sammlungen & Anthologien | 1 | 4 |
| Sammlungen & Erzählbände von Romanzen | 1 | 4 |
| Multikulturelle & interkulturelle Romanzen | 1 | 4 |

**milliardär liebesroman**

| Kategorie | Titel darin | bester Rang |
|---|---:|---:|
| Fake-Dating-Romantik | 2 | 2 |
| Zweite-Chance-Romanze | 2 | 2 |
| eBooks über Romanzen über Milliardäre & Millionäre | 2 | 24 |
| Zeitgenössische Liebesromane | 2 | 54 |
| eBooks: romantische Thriller | 1 | 25 |
| Romantische Thriller | 1 | 37 |
| Action & Abenteuer Liebesromane | 1 | 41 |
| Moderne Belletristik für Frauen | 1 | 49 |

**ceo liebesroman**

| Kategorie | Titel darin | bester Rang |
|---|---:|---:|
| Fake-Dating-Romantik | 6 | 4 |
| Liebesroman | 3 | 19 |
| Romantische Komödien | 2 | 129 |
| Urlaubsromanzen | 1 | 77 |
| Ferienliebesromane | 1 | 80 |
| eBooks über Romanzen über Milliardäre & Millionäre | 1 | 116 |
| Romantische Komödie | 1 | 168 |

**zweite chance liebesroman**

| Kategorie | Titel darin | bester Rang |
|---|---:|---:|
| Zweite-Chance-Romanze | 3 | 7 |
| Belletristik | 2 | 98047 |
| Liebesromane | 2 | 99866 |
| Liebesromane für Junge Erwachsene | 1 | 25 |
| New Adult | 1 | 41 |
| Moderne Belletristik für Frauen | 1 | 5836 |
| Liebesromane für Frauen | 1 | 7118 |
| Liebesroman | 1 | 7514 |

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

---

## Nachtrag: Marktvergleich Deutsch gegen Englisch (14.08.2026)

### Werkzeuggrenze zuerst

Von 11 Versuchen auf **amazon.com** ist **einer** durchgekommen. Auf
amazon.de laufen dieselben Abrufe zuverlässig. Das ist eine
**Werkzeuggrenze, kein Marktbefund** — die FEHLER-Zeilen bei
amazon.com dürfen **nicht** als „keine Konkurrenz auf Englisch" gelesen
werden. Vermutlich greift die Bot-Erkennung auf .com bei
Rechenzentrums-Adressen härter.

Beim Reparaturversuch ist mir ein eigener Fehler unterlaufen: Der
Diagnose-Einbau hat nur zur Hälfte gegriffen (Berichtsteil ja, Setzen der
Werte nein), und ich habe „eingebaut" gemeldet, ohne es zu prüfen.
Deshalb blieb der zweite Fehlschlag wieder ohne Ursache. Korrigiert und
diesmal mit `assert` nachgewiesen.

### Der eine Datenpunkt, der durchkam

| Nische | Markt | Bewertungen Median | Preis | in KU | gesponsert |
|---|---|---:|---:|---:|---:|
| geheimes baby liebesroman | **amazon.de** | **43** | – | 10/10 | 0/10 |
| secret baby romance | **amazon.com** | **292** | 5,99 $ | 8/10 | **2/10** |

Dieselbe Nische, zwei Märkte: Die Führenden auf Englisch haben rund
**siebenmal so viele Bewertungen**. Genau das, was man erwartet — nur
jetzt gemessen statt vermutet.

**Nebenbefund:** Die Spalte „gesponsert" zeigt auf .com **2/10**, auf .de
durchgehend 0/10. Der Selektor ist also **nicht grundsätzlich kaputt** —
er trifft die englische Markierung und die deutsche nicht. Das verengt
die Fehlersuche erheblich.

### Bewertung

Ein Datenpunkt trägt keine Marktentscheidung. Er zeigt aber in dieselbe
Richtung wie alles andere, und die Entscheidung hängt ohnehin an etwas,
das keine Messung beantwortet: **Romance lebt von Stimme und Dialog.**
Das auf Marktniveau in einer Fremdsprache zu treffen, ist etwas anderes
als eine Produktbeschreibung zu übersetzen.

→ **Deutsch**, wo zwei Lücken gemessen sind. Übersetzung später, wenn die
Reihe trägt — dann finanzieren die Bände sie, statt vorgeschossen zu
werden.
