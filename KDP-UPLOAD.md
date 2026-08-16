# KDP-Upload — Band 1

Stand: 15.08.2026

Alles, was beim Hochladen in ein Feld eingetragen wird, steht hier
fertig. Was noch fehlt, steht ganz oben und nicht versteckt.

---

## Was noch fehlt

| | Stand |
|---|---|
| Manuskript, 58 Kapitel + Epilog | **fertig**, 69.603 Wörter |
| Cover 1600 × 2560 | **fertig**, Bild über OpenRouter erzeugt |
| EPUB mit eingebettetem Cover | **fertig**, 658 kB |
| Impressum, Autor, Copyright | **fertig** |
| Metadaten, Schlagwörter, Kategorien | **fertig**, Kategorien gemessen |
| Typografie | **0 Fehler**, von `prosa.py` und Vale unabhängig bestätigt |
| **Länge** | **69.603 Wörter** — ⚠️ unter der heute gemessenen Spanne, siehe unten |

**Hochladbar ist es. Optimal ist es bei einem Punkt nicht.** Am
14.08. maß `kdp_nischen.py` in der Hauptnische 291 bis 337 Druckseiten,
und daraus wurde das Ziel 65.000 bis 82.000 Wörter. Der Lauf vom
**16.08. misst dieselbe Nische neu: Median 337 Seiten, Spanne 312 bis
398.** Das Manuskript liegt bei 69.603 Wörtern, also rund 250 bis 280
Druckseiten — unter dem kürzesten dort gemessenen Titel.

Bei Kindle Unlimited wird pro gelesener Seite gezahlt; das sind
schätzungsweise 22 % weniger Ertrag pro Leserin. Die vollständige
Abwägung samt Stichprobengröße steht in `buch/PRUEFUNG.md`. Bis zum
unteren Rand der Spanne fehlen rund 13.300 Wörter.

Auch die beiden erzählerischen Entscheidungen sind gefallen, und zwar
in die Richtung, die den Leser dieser Nische zufriedenstellt: **Happy
End mit Epilog** und **eine sinnliche, nicht explizite Liebesszene**.
Die zweite ist gemessen und nicht geraten — siehe `KDP-NISCHEN.md`,
Abschnitt „Hitzegrad der Spitzentitel".

## Die Dateien

| Datei | Wofür | Stand |
|---|---|---|
| `buch/reinhardt-1.epub` | **das ist die Datei, die hochgeladen wird** | fertig, 658 kB, 61 Abschnitte |
| `buch/manuskript.md` | zum Lesen und Korrigieren | fertig |
| `cover/fertig/cover.jpg` | **Cover zum Hochladen** | fertig, 1600 × 2560 nachgemessen, 447 kB |
| `cover/fertig/schrift-ebene.png` | transparent, für Canva | fertig |

**KDP nimmt kein Markdown.** Zulässig sind unter anderem DOCX, EPUB und
KPF. Deshalb baut `manuskript.py` die EPUB — mit Inhaltsverzeichnis,
Cover und einem Stylesheet, das Absätze einzieht und Szenentrenner
setzt.

---

## Metadaten, Feld für Feld

**Sprache:** Deutsch

**Buchtitel:** `Sein bestgehütetes Geheimnis`

**Untertitel:** `Ein Geheimes-Baby-Milliardär-Liebesroman`

> Ich habe zuvor geschrieben, der Titel trage keine Suchbegriffe, und das
> war ungenau. Amazon indiziert **Titel und Untertitel zusammen**. Der
> Untertitel trägt „Geheimes Baby", „Milliardär" und „Liebesroman" —
> also genau die drei gemessenen Begriffe. Der Haupttitel darf deshalb
> kurz und merkbar sein. Er bleibt.

**Reihe:** `Die Reinhardt-Brüder` · **Band:** `1`

**Autor:** `Alan Lorenz`

> Klarname, so entschieden. Zur Kenntnis, nicht als Widerspruch: In
> dieser Nische sind Pseudonyme die Regel. Der Name steht später bei
> Amazon, in jeder Leseprobe und in jeder Suche neben dem Genre. Das ist
> umkehrbar — ein zweites Autorenprofil ist bei KDP jederzeit anlegbar,
> nur die bereits verkauften Exemplare tragen den alten Namen.

**Beschreibung** (max. 4.000 Zeichen; KDP erlaubt einfaches HTML — so
einfügen, dann steht die Formatierung auch da):

```html
<p><b>Vor zwei Jahren hat er mich verlassen, ohne sich umzudrehen.<br>
Heute steht er in meinem Café und will mein Haus kaufen.<br>
Und er weiß immer noch nicht, dass unser Sohn oben schläft.</b></p>

<p>Marlene Voss hat gelernt, sich auf niemanden zu verlassen. Ihre
Konditorei in der Hamburger Speicherstadt läuft, ihr Sohn Emil ist
gesund, und wenn sie nachts wach liegt, dann wegen der Zahlen, nicht
wegen eines Mannes.</p>

<p>Bis die Bank den Kredit kündigt.</p>

<p>Und bis Jonas Reinhardt durch ihre Tür kommt — derselbe Jonas, der
vor zwei Jahren nach einem Wochenende verschwand, der auf drei Anrufe
nie geantwortet hat, dem sie einen Brief geschrieben hat, den er nie
beantwortete. Jetzt gehört ihm halbe Speicherstadt, und für sein
Kontorhaus-Projekt fehlt ihm genau ein Gebäude.</p>

<p><b>Ihres.</b></p>

<p>Er bietet ihr mehr Geld, als sie je gesehen hat. Sie sagt nein. Sie
sagt es noch dreimal. Und irgendwann zwischen Bauplänen um Mitternacht
und einem Mann, der endlich einmal gefragt wird, was <i>er</i>
eigentlich will, wird aus der Verhandlung etwas anderes.</p>

<p>Dann sieht Jonas das Kind.</p>

<p><b>Und rechnet nach.</b></p>

<p>Eine Zweite-Chance-Geschichte über zwei Menschen, die beide gelernt
haben, niemanden zu brauchen — und über die Wahrheit, die keiner von
beiden mehr aufhalten kann.</p>

<p><i>Band 1 der Reihe „Die Reinhardt-Brüder". Abgeschlossen, mit
Happy End und Epilog — kein Cliffhanger für dieses Paar. Erst danach
öffnet sich der Blick auf Band 2. Sinnlich, aber ohne explizite
Szenen.</i></p>
```

> Der letzte Halbsatz steht da mit Absicht, und er heißt jetzt
> *sinnlich, aber ohne explizite Szenen* statt *geschlossene Tür* —
> weil es seit Kapitel 56 eine Liebesszene gibt. Beide Erwartungen
> werden damit vorab bedient: Wer Spice sucht, weiß, dass es keiner
> wird; wer keinen will, weiß, dass die Tür zugeht. Ein Stern wegen
> falscher Erwartung entsteht an genau dieser Zeile oder gar nicht.

**Schlagwörter (7 Felder):**

| # | Schlagwort | Grundlage |
|---|---|---|
| 1 | `geheimes baby liebesroman` | **gemessen**, BSR-Median 671 |
| 2 | `milliardär liebesroman` | **gemessen**, BSR-Median 902 |
| 3 | `ceo liebesroman` | **gemessen**, BSR-Median 1068 |
| 4 | `enemies to lovers deutsch` | **gemessen**, BSR-Median 1385 |
| 5 | `zweite chance liebesroman` | Trope des Buches, ungemessen |
| 6 | `alleinerziehende mutter roman` | Trope des Buches, ungemessen |
| 7 | `liebesroman hamburg` | Schauplatz, ungemessen |

Die ersten vier stammen aus `KDP-NISCHEN.md`, sind also echte Zahlen.
Die letzten drei sind Vermutungen und als solche markiert.

**Kategorien (3 Stück):** jetzt gemessen — `KDP-NISCHEN.md`,
Abschnitt „Kategorien der Spitzentitel". Die Unterkategorien stehen auf
den Produktseiten neben dem Bestseller-Rang; gelesen wurden sie bei 20
Titeln aus vier Nischen.

| Kategorie | Warum | Enge |
|---|---|---|
| **eBooks über Romanzen über Milliardäre & Millionäre** | trifft das Buch und den Untertitel | bester gemessener Rang 24 bzw. 116 — locker |
| **Zweite-Chance-Romanze** | trifft den Kern: zwei Jahre Funkstille, dann wieder | bester Rang 7 bzw. 2 — dort sitzt jemand |
| **Zeitgenössische Liebesromane** | die breite Heimatkategorie | bester Rang 54 |

**Was ich bewusst nicht nehme, obwohl die Zahlen locken:**
*Fake-Dating-Romantik* steht bei **6 von 12** Titeln der CEO-Nische und
ist damit die meistgenutzte Kategorie überhaupt — aber in diesem Buch
gibt es kein Fake Dating. *Rockstar-Romanze* und *Dramatik — Weibliche
Autoren* zeigen besten Rang 1, also praktisch leere Kategorien, in die
sich andere hineingeschummelt haben. Falsche Einordnung verstößt gegen
die KDP-Richtlinien, bringt Rückgaben und Ein-Stern-Bewertungen von
Leserinnen, die etwas anderes erwartet haben. Ein Abzeichen in einer
Kategorie, die nicht passt, ist keins.

**Altersfreigabe:** keine Jugendschutzeinstufung nötig — die
Liebesszene ist nicht explizit dargestellt, es gibt keine Gewalt. Die
Inhaltshinweise stehen im Vorspann des Buches.

**Veröffentlichungsrechte:** eigenes Werk, keine Gemeinfreiheit.

---

## Der Untertitel sagt Milliardär — deckt das Buch das?

Ja, seit Kapitel 44, und ich hatte das in einer früheren Fassung dieses
Berichts falsch dargestellt.

Im Text steht: Bestand der Reinhardt Immobilien **1,7 Milliarden**,
zweihundertvierzig Objekte zwischen Altona und Rothenburgsort,
**neunundvierzig Prozent der Gesellschaft gehören Jonas**. Das war nur
an einer einzigen Stelle gesagt, und zwar erst im Januar-Kapitel — bis
dahin las sich die Firma wie ein mittlerer Bestandshalter.

Deshalb steht die Zahl jetzt auch in **Kapitel 12**, im Oktober, wo sie
zum ersten Mal gebraucht wird, und sie steht dort so, wie dieser Erzähler
sie sagen würde:

> *Ich sage diese Zahl nie laut. Nicht aus Bescheidenheit — weil sie
> nichts bedeutet. […] Ein Mann mit diesen Zahlen, der um Viertel nach
> neun abends vor einem Kontorhaus parkt, um zu sehen, ob im ersten
> Stock Licht brennt, ist trotzdem nur ein Mann, der vor einem
> Kontorhaus parkt.*

Damit ist das Etikett gedeckt, ohne dass das Buch seinen Ton wechselt —
und der stärkste gemessene Suchbegriff (`milliardär liebesroman`,
BSR-Median 902) bleibt im Untertitel, wo Amazon ihn indiziert.

---

## Preis, Tantieme und KU

**Listenpreis: 4,99 €.**

Das 70-%-Fenster liegt in Deutschland zwischen 2,99 € und 9,99 €.
Darunter und darüber gibt es 35 %. Bei 70 % werden zusätzlich
Auslieferungskosten nach Dateigröße abgezogen — bei 658 kB sind das
Cent, nicht Euro.

**KDP Select: ja.** Das bedeutet 90 Tage Exklusivität bei Amazon —
das Buch darf in der Zeit nirgends sonst als E-Book erscheinen. Dafür
liegt es in **Kindle Unlimited**.

Warum das hier die richtige Wahl ist, und zwar aus unserer eigenen
Messung: In `KDP-NISCHEN.md` liegen **8 bis 10 von 10** Titeln jeder
deutschen Romance-Nische in KU. In dieser Nische wird gelesen, nicht
gekauft. Wer nicht in KU liegt, steht neben zehn Büchern, die für die
Leserin nichts extra kosten.

**Und deshalb zählt die Länge — jetzt mit gemessener Zahl.** In KU wird
pro gelesener Seite gezahlt. Die Spitzentitel der vier gemessenen
Nischen haben im Median **326 bis 544 Druckseiten** (`KDP-NISCHEN.md`,
Lauf vom 16.08.). Dieses Buch hat **69.603 Wörter**, also rund 250 bis
280 Druckseiten.

Der Lauf vom 16.08. hat diese Zahlen nach oben korrigiert: In der
Hauptnische *geheimes baby liebesroman* liegt der Median bei 337 Seiten,
die Spanne bei 312 bis 398, gelesen an vier Titeln mit Angabe. Damit ist
das Buch kürzer als jeder dort gemessene Spitzentitel.

Zur Einordnung, damit die Zahl nicht als Befehl gelesen wird: vier Titel
sind eine Andeutung, und die Umrechnung Wörter → Seiten ist eine
Faustregel. Was nicht wackelt: In allen vier gemessenen Nischen liegt
der Median über 320 Seiten. `buch/PRUEFUNG.md` rechnet vor, was das
Schließen der Lücke kostet.

---

## Vor dem Hochladen

Fünf Punkte. Die ersten drei sind hier schon nachgemessen und
abgehakt — sie stehen trotzdem da, weil sie nach jeder Textänderung neu
gelten. Die letzten zwei kann nur jemand am KDP-Konto erledigen.

**✅ 1. Prüfläufe grün.** Zuletzt am 16.08.2026:

| Werkzeug | Ergebnis |
|---|---|
| `python3 scripts/manuskript.py --autor "Alan Lorenz"` | Keine Beanstandungen |
| `python3 scripts/prosa.py` | 0 Typografiefehler |
| `./scripts/vale.sh` | 0 errors, 0 warnings |

Meldet `manuskript.py` „Keine Beanstandungen", obwohl du Platzhalter
erwartest, prüfe zuerst das Prüfwerkzeug selbst: `--selbsttest`.

**✅ 2. Cover nachgemessen.** 1600 × 2560 Pixel, Verhältnis exakt 1,600,
447 kB. Die Miniaturprobe (`cover/fertig/miniaturprobe.png`) zeigt den
Titel bei 160 Pixeln — so sieht ihn die Leserin in der Trefferliste.
Wenn er dort nicht lesbar ist, ist das Cover falsch, egal wie gut es
in groß aussieht.

**✅ 3. Die Leseprobe fängt bei Kapitel 1 an.** Das war nicht so. Der
Vorspann enthielt Titelei, Impressum und Hinweise; „Blick ins Buch"
hätte damit einen Teil der zehn Prozent für ein Impressum verbraucht.
Geändert: Das **Impressum steht jetzt im Nachspann**, und die EPUB trägt
eine Startposition (`guide type="text"` auf `kap01.xhtml`), sodass der
Kindle auf Seite eins von Kapitel 1 öffnet. Nachgeprüft in der fertigen
Datei.

**⬜ 4. Die KI-Frage — der einzige Punkt, an dem etwas kaputtgehen
kann.**

KDP fragt beim Hochladen getrennt nach **Text**, **Bildern** und
**Übersetzung**. Für dieses Buch ist die Antwort:

| Feld | Antwort |
|---|---|
| Text | **Ja, KI-generiert** |
| Bilder | **Ja, KI-generiert** |
| Übersetzung | Nein |

Amazon unterscheidet „AI-generated" (von KI erzeugt, auch wenn du danach
bearbeitest) von „AI-assisted" (du hast geschrieben, KI hat geholfen).
Hier ist es Ersteres, und zwar auch dann noch, wenn du jeden zweiten
Satz umschreibst — solange KI-Text im Buch steht.

Die Angabe ist **nicht öffentlich sichtbar** und verzögert die Freigabe
nicht. Eine unterlassene Angabe führt zur Entfernung des Titels und im
Wiederholungsfall zur Kontosperre samt gesamtem Katalog (`DIGITAL.md`,
Abschnitt 7). Im Buch selbst steht der Hinweis ohnehin, im Vorspann
unter „Hinweise" — das ersetzt die Angabe im Formular aber nicht.

**⬜ 5. Steuerinterview.** Vor der ersten Auszahlung verlangt KDP ein
US-Steuerinterview. Ohne ausgefülltes Formular behält Amazon **30 %
Quellensteuer** ein; mit dem deutsch-amerikanischen
Doppelbesteuerungsabkommen sind es bei Lizenzeinnahmen 0 %. Läuft online
im KDP-Konto, zehn Minuten. Der Kleinunternehmerstatus nach § 19 UStG
ändert daran nichts — das ist Umsatzsteuer, hier geht es um
Quellensteuer.

**Übersprungen, auf deine Ansage:** der Abgleich der erfundenen Namen
(„Reinhardt Immobilien", „Café Voss", „Hanseatische Volksbank",
„Kellermann") gegen reale Firmen. Der Haftungsausschluss im Vorspann
steht und benennt sie einzeln.

---

## Nach dem Hochladen

Die Freigabe dauert bei Amazon üblicherweise bis zu 72 Stunden.

Danach: den Link zur Reihenseite in `buch/99-nachspann.md` eintragen
und die EPUB neu bauen. Ein toter Link im Buch ist schlimmer als
keiner — deshalb steht dort jetzt eine Klammer und kein Link.

---

## Und der Satz, der bleibt

Diese Reihe zahlt frühestens ab Band 3, realistisch 100–500 € im Monat
(`GELDVERDIENEN.md`). Näher am Geld liegen weiterhin die **fünf
fertigen eBay-Angebote** (`EBAY-START.md`, eingestellt ist keins), der
ungeklärte **Neutralversand bei CJ** und die **Deko-Kategorie**, die
als einzige je etwas verkauft hat und immer noch nicht im Shop ist.
