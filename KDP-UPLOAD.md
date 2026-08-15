# KDP-Upload — Band 1

Stand: 15.08.2026

Alles, was beim Hochladen in ein Feld eingetragen wird, steht hier
fertig. Was noch fehlt, steht ganz oben und nicht versteckt.

---

## Was noch fehlt

| | Stand |
|---|---|
| Manuskript, 28 Kapitel | **fertig**, 35.692 Wörter |
| Cover 1600 × 2560 | **fertig**, Bild über OpenRouter erzeugt |
| EPUB mit eingebettetem Cover | **fertig**, 554 kB |
| Impressum, Autor, Copyright | **fertig** |
| Metadaten, Schlagwörter, Kategorien | **fertig**, Kategorien gemessen |
| Typografie | **0 Fehler**, von `prosa.py` und Vale unabhängig bestätigt |
| **Länge** | **35.692 von 65.000** — siehe unten |

**Hochladbar ist es damit heute.** Der einzige offene Punkt ist die
Länge: Die Spitzentitel der Nische liegen bei 65.000 bis 82.000 Wörtern
(`KDP-NISCHEN.md`). Bei Kindle Unlimited wird pro gelesener Seite
gezahlt — dieses Buch bringt bei vollständigem Durchlesen rund die
Hälfte dessen, was ein Titel üblicher Länge bringt.

Das ist eine Entscheidung, keine Baustelle: als Novelle veröffentlichen
und die Länge im Klappentext ehrlich nennen, oder einen dritten
Durchgang schreiben. Der Weg dafür steht in `buch/STAND.md`.

## Die Dateien

| Datei | Wofür | Stand |
|---|---|---|
| `buch/reinhardt-1.epub` | **das ist die Datei, die hochgeladen wird** | fertig, 239 kB, 30 Abschnitte |
| `buch/manuskript.md` | zum Lesen und Korrigieren | fertig |
| `cover/fertig/cover.jpg` | Cover, 1600 × 2560 | Schrift fertig, Bild fehlt |
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

<p><i>Band 1 der Reihe „Die Reinhardt-Brüder". Die Liebesgeschichte von
Leni und Jonas ist abgeschlossen — kein Cliffhanger für dieses Paar.
Auf der letzten Seite öffnet sich der Blick auf Band 2. Geschlossene
Tür: keine expliziten Szenen.</i></p>
```

> Der letzte Halbsatz zur geschlossenen Tür steht da mit Absicht. Wer
> „Milliardär-Liebesroman" sucht und Spice erwartet, vergibt sonst
> einen Stern für etwas, das im Buch nie versprochen wurde.

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

**Altersfreigabe:** keine Jugendschutzeinstufung nötig — geschlossene
Tür, keine Gewalt.

**Veröffentlichungsrechte:** eigenes Werk, keine Gemeinfreiheit.

---

## Die KI-Frage — nicht überspringen

KDP fragt beim Hochladen getrennt nach **Text**, **Bildern** und
**Übersetzung**. Für dieses Buch ist die Antwort:

- **Text: KI-generiert.** Die Prosa stammt von einer KI. Auch wenn du
  überarbeitest, bleibt die Angabe richtig, solange KI-Text im Buch
  steht.
- **Bilder: KI-generiert**, sobald das Cover aus einem Bildmodell kommt.
- **Übersetzung: nein.**

Amazon unterscheidet „AI-generated" (von KI erzeugt, auch wenn danach
bearbeitet) von „AI-assisted" (du hast geschrieben, KI hat geholfen).
Hier ist es Ersteres.

Diese Angabe ist **nicht öffentlich sichtbar** und beeinflusst die
Freigabe nicht. Eine unterlassene Angabe dagegen führt zur Entfernung
des Titels und im Wiederholungsfall zur Kontosperre samt gesamtem
Katalog (`DIGITAL.md`, Abschnitt 7). Es gibt keinen Grund, das Risiko
einzugehen.

---

## Eine Unstimmigkeit, die dir gehört

Der Untertitel sagt **Milliardär**. Im Buch steht das nirgends. Jonas
führt eine Immobilienfirma mit ein paar hundert Angestellten; die
Zahlen, die vorkommen, sind 4,2 Millionen bei einem Projekt, 186.000
privat und eine Tantieme von 120.000 im Jahr. Das ist sehr reich, aber
kein Milliardär.

Genre-Leserinnen bemerken das und schreiben es in Bewertungen. Drei
Wege:

1. **So lassen.** „Milliardär" ist in dieser Nische ein Genre-Etikett,
   kein Vermögensnachweis, und die Amazon-Kategorie heißt selbst
   „Milliardäre **& Millionäre**".
2. **Untertitel ändern** auf *Ein Geheimes-Baby-Liebesroman* und
   „milliardär liebesroman" nur als Schlagwort führen. Kostet
   Sichtbarkeit im Titel, ist aber sauber.
3. **Die Zahl im Buch anheben** — eine einzige Stelle, Kapitel 26, wo
   die Tantieme steht.

Ich empfehle **1**, weil es Marktbrauch ist und die Kategorie es
abdeckt. Es ist trotzdem deine Entscheidung, und sie ist in zwei
Minuten umsetzbar.

---

## Preis, Tantieme und KU

**Listenpreis: 4,99 €.**

Das 70-%-Fenster liegt in Deutschland zwischen 2,99 € und 9,99 €.
Darunter und darüber gibt es 35 %. Bei 70 % werden zusätzlich
Auslieferungskosten nach Dateigröße abgezogen — bei 239 kB sind das
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
Nischen haben im Median **291 bis 337 Druckseiten**, also rund
**65.000 bis 82.000 Wörter** (`KDP-NISCHEN.md`). Dieses Buch hat
30.575 — **etwa 40 % davon**. Bei vollständigem Durchlesen bringt es
entsprechend rund 40 % der Seitenerlöse eines typischen Titels der
Nische.

**Steuerinterview nicht vergessen.** KDP verlangt vor der ersten
Auszahlung ein US-Steuerinterview. Ohne ausgefülltes Formular behält
Amazon **30 % Quellensteuer** ein. Mit dem deutsch-amerikanischen
Doppelbesteuerungsabkommen sind es bei Lizenzeinnahmen 0 %. Das
Interview läuft online im KDP-Konto und dauert zehn Minuten. Der
Kleinunternehmerstatus nach § 19 UStG ändert daran nichts — das ist
Umsatzsteuer, hier geht es um Quellensteuer.

---

## Vor dem Hochladen prüfen

1. **`python3 scripts/manuskript.py`** — muss „Keine Beanstandungen"
   melden. Tut es das, obwohl du Platzhalter erwartest, prüfe zuerst
   das Prüfwerkzeug: `--selbsttest`.
2. **Miniaturprobe ansehen** (`cover/fertig/miniaturprobe.png`). Ist der
   Titel bei 160 Pixeln lesbar? Wenn nicht, ist das Cover falsch.
3. **KDP-Vorschau** durchklicken, besonders die erste Seite und den
   Kapitelübergang. Der Previewer zeigt, was der Kindle zeigt.
4. **Erste Seite ohne Vorspann?** Prüfen, wo „Blick ins Buch" anfängt.
   Wenn die Leseprobe mit dem Impressum beginnt, ist sie verschenkt.

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
