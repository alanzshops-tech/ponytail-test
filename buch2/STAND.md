# Band 2 — Stand

**Fertig.** 24.08.2026.

| | |
|---|---|
| Titel | *Was er nie gefragt hat* |
| Untertitel | Eine geheime Ehe, eine Frist und eine Familie, die alles regelt |
| Reihe | Die Reinhardt-Brüder, Band 2 |
| Autorin | Jule Norden (Pseudonym, wie Band 1) |
| Umfang | **64 Kapitel, 69.297 Wörter Fließtext, 70.243 Wörter gesamt** |
| Erzählform | Ich-Perspektive, wechselnd Amira / Theo, Präteritum |
| Datei | `buch2/reinhardt-2_KDP.epub` (1.143 kB, 66 Abschnitte) |
| Lesefassung | `buch2/Was-er-nie-gefragt-hat.epub` |
| Umschlag | `cover/band2/cover.jpg`, 1600 × 2560 |

---

## Die Prüfläufe

Alle Werkzeuge laufen mit `--buch buch2`:

| Werkzeug | Ergebnis |
|---|---|
| `manuskript.py` | Keine Beanstandungen. Kapitelfolge lückenlos, Perspektivwechsel durchgehend, keine Platzhalter |
| `prosa.py` | 0 falsche Anführungszeichen, 0 falsche Apostrophe, 0 falsche Auslassungspunkte |
| `prosa.py --sprache` | LanguageTool: 110 Treffer, 8 echte Fehler behoben, 47 als Stil gefiltert |
| `dopplung.py` | Ein Treffer, absichtlich — siehe `PROJEKT.md` 7c |
| `romantik.py` | 0 von 64 Kapiteln ohne gemeinsame Szene |
| `epubcheck.py` | Keine Beanstandungen |
| `kalender.py` | 12 Datumsangaben mit Wochentag geprüft, keine Beanstandungen (nach 9 Korrekturen) |
| `namen.py` | 32 Eigennamen, 3 Verdachtsfälle, alle drei falsch — keine Schreibvariante im Buch |
| `vale.sh buch2` | 0 Fehler, 0 Warnungen, 10 Hinweise (Füllwörter in wörtlicher Rede) |
| `lektorat.py` | 10 Kapitel, zwei fremde Modelle, Belegquote 96,4 %, 0 Abbruchstellen |

Band 1 nach allen Änderungen an den gemeinsamen Werkzeugen
gegengeprüft: unverändert ohne Beanstandung, Kennung weiterhin
`reinhardt-1-79fe7dd70150`.

---

## Was die Werkzeuge gefunden haben, das ich nicht gesehen hätte

Sechs Sachen, alle durch Messen und nicht durch Lesen:

1. **Die Kapitel waren zu kurz.** Band 1 hat 1.207 Wörter je Kapitel,
   Band 2 lag bei 765 — hochgerechnet 47.400 statt 78.000. Die Zeile
   *„Kapitel unter 900 Wörtern"* stand sechs Läufe lang im Terminal, und
   ich habe sie als Rauschen gelesen, weil sie bei Band 1 immer drei
   Nummern enthielt.
2. **Die Romantik war flach, nicht schwach.** `romantik.py`: Berührung
   1,67 gegen Band 1s 3,15 je 1000 Wörter, Sehnsucht sogar höher
   (1,43 zu 0,92), stärkstes Kapitel 6 gegen 15. Viel Sehnen, wenig
   Körper, keine Spitze. Ursache ist der Stoff: Ein Ehepaar, das
   zusammenwohnt, ist automatisch im selben Bild, und Nähe, die nie
   verhandelt werden muss, erzeugt keine Spannung.
3. **Drei Altersfehler.** Amiras Mutter zweimal (Kapitel 10 und 51),
   Theo einmal (Kapitel 2). Gefunden durch einen Suchlauf über alle
   Zahlwörter mit Umfeld, nicht beim Lesen. Verzeichnet in `PROJEKT.md`
   7d, samt dem Widerspruch, der in Band 1 selbst liegt und dort nicht
   angerührt wird.
4. **Ein toter Link in der fertigen EPUB.** `manuskript.py` schrieb den
   Cover-Eintrag ins Verzeichnis, auch wenn kein Cover übergeben wurde —
   fiel nie auf, weil Band 1 immer eins hatte. `epubcheck.py` hat ihn
   beim ersten Bau von Band 2 gemeldet.
5. **Die Kennung von Band 2 wies ihn als Band 1 aus.** `reinhardt-1-`
   war fest verdrahtet. Die Bücher waren trotzdem unterscheidbar, weil
   der Hash abweicht; aufgefallen ist es erst, als beide Kennungen
   nebeneinander ausgegeben wurden.
6. **Eine wörtliche Wiederholung zwischen Kapitel 59 und 63** (0,74).
   Sabine zitierte sich selbst fast wortgleich. Auf einen Verweis
   zurückgenommen — dieselbe Lehre wie bei Band 1s Kapitel 41.

---

## Die eine Zahl, die stehen bleibt

`dopplung.py` meldet **Kapitel 6 und 7 mit 0,62**, und das bleibt so.
Die beiden werden dort **getrennt** von zwei Sachbearbeitern befragt,
und die Behörde prüft, ob ihre Antworten zusammenpassen. Dass sie
denselben Sachverhalt in eigenen Worten erklären, ist der Inhalt der
Szene. Wer das wegschreibt, nimmt der Anhörung ihren Zweck.
Begründung in `PROJEKT.md` 7c, damit es beim nächsten Lauf nicht als
Mangel „behoben" wird.

---

## Die Fehlerprüfung vom 31.08.2026

Das Buch war fertig. Geprüft wurde trotzdem noch einmal, und zwar auf
die Fehlerart, die kein Leser verzeiht und kein bisheriges Werkzeug
gesehen hat: **Zahlen, die im Text aufeinander zeigen.**

Zwei neue Messgeräte, beide mit Selbsttest:

**`kalender.py`** rechnet jede Datumsangabe mit ausgeschriebenem
Wochentag gegen den echten Kalender. Gefunden: **neun falsche
Wochentage** in den Kapiteln 30 bis 64. Behoben wurden die *Daten*, nicht
die Wochentage — der Sonntag beim Essen und der Dienstag beim Amt
tragen Bedeutung, das Datum daneben nicht.

*Die erste Fassung des Werkzeugs hat 6 von 11 prüfbaren Stellen nicht
gesehen*, weil sie nur eine Wortstellung kannte, und hätte „keine
Beanstandungen" gemeldet. Ein Messgerät, das die Hälfte nicht sieht,
ist schlimmer als keins. Jetzt vier Wortformen, jede mit ihrem echten
Satz im Selbsttest.

**`namen.py`** hält jedes großgeschriebene Wort gegen einen umgrenzten
Namensbestand. Ergebnis: 32 Eigennamen, drei Verdachtsfälle, alle drei
falsch (*Erst/Ernst*, *Krise/Kruse*, *Sein/Selin* sind echte Wörter).
Keine Schreibvariante im Buch.

### Die Ehedauer stand fünfzehn Kapitel lang still

Der größte Fund kam nicht vom Werkzeug, sondern vom Nachrechnen: Die
Wendung *„seit fünfzehn Monaten verheiratet"* stand von Kapitel 12 bis
Kapitel 24 unverändert da — während die Handlung von Mai bis September
2026 läuft. **Fünfzehn Stellen**, jede einzeln gegen ihr Kapiteldatum
und die Hochzeit am 14.03.2025 gerechnet:

| Kapitel | Im Buch datiert auf | Stand | Jetzt |
|---|---|---|---|
| 12 | 27.05.2026 | fünfzehn | **vierzehn** |
| 13 | 04.06.2026 | fünfzehn | **vierzehn** |
| 14, 15 | 21.06. / 08.07.2026 | fünfzehn | **vierzehn** (Rückblick auf die Geheimhaltung) |
| 17 | 26.07.2026 | fünfzehn | **sechzehn** |
| 19 | 21.08.2026 | fünfzehn (5×) | **siebzehn** |
| 21, 22, 23 | 30.08.–08.09.2026 | fünfzehn | **siebzehn** |
| 24 | 08.09.2026 | fünfzehn | **vierzehn** (Zeitraum ohne Dokumentation) |

Dabei ist eine Regel sichtbar geworden, die das Buch vorher nur
zufällig eingehalten hat und jetzt durchgehend einhält: **Vierzehn
Monate ist die Geheimhaltung** (Hochzeit bis zu Amiras Anruf im Mai
2026) — eine feste Zahl, die von Kapitel 18 bis Kapitel 59 immer wieder
zurückzitiert wird. Alles andere ist die laufende Ehedauer und wächst
mit.

### Zwei Widersprüche in der Messreihe

- Die Setzung an der Ostwand war in Kapitel 11 **vierzehn Monate**
  lang gemessen und in vier weiteren Kapiteln **drei Jahre**. Kapitel 11
  sagt jetzt, dass sich die vier Punkte *seit* vierzehn Monaten nicht
  mehr bewegt haben — das Bild („dieselben vierzehn Monate", der
  Gleichlauf von Riss und Ehe) bleibt, der Widerspruch ist weg.
- Die Messreihe begann im **April 2023**, der Auftrag kam im **August
  2023**. Sie hat gemessen, bevor sie beauftragt war. Jetzt September,
  und damit 72 statt 78 Messtermine.

### Zwei fremde Modelle haben zehn Kapitel gelesen

Das ist die eine Prüfung, die ich selbst nicht sein kann: Mein Urteil
über meine eigene Prosa ist als Messung wertlos. `lektorat.py` schickt
die Kapitel an zwei fremde Modelle und **prüft jedes Zitat gegen den
Kapiteltext** — ein erfundenes Zitat heißt, das Modell hat nicht
gelesen, sondern etwas Plausibles gesagt.

Gelesen wurden die Kapitel 1, 2, 3, 5, 12, 19, 23, 36, 53 und 64.
Bericht: `buch2/LEKTORAT.md`. Kosten: 0,29 USD.

- **Belegquote 27 von 28 Zitaten (96,4 %)** — beide Modelle haben
  tatsächlich gelesen.
- **Die Gegenprobe hat gegriffen.** Der absichtlich schlechte
  Kontrolltext läuft bei jedem Lauf mit; beide Modelle haben dort eine
  Abbruchstelle genannt. Ohne das wäre jedes „kein Abbruch" bei den
  echten Kapiteln nur Höflichkeit.
- **0 von 20 Leseproben mit einer Abbruchstelle.** Keins der zehn
  Kapitel legt ein fremder Leser weg.

Vier der acht Unklarheiten waren echte Fehler, und drei davon hätte
kein Suchmuster gefunden:

1. **Kapitel 1.** Sie nimmt *ihr* Telefon und sucht in *seiner*
   Kontaktliste. Umgeschrieben: Sie sucht die Nummer, die sie sich vor
   einem Jahr aus seinem Telefon abgeschrieben hat.
2. **Kapitel 2** — von *beiden* Modellen genannt. „Ich habe Theo —
   nein. Ich habe Jonas am Telefon gehabt": Theo erzählt das Kapitel
   selbst, er kann sich nicht mit seinem eigenen Namen verhaspeln. Ein
   Rest aus einer früheren Fassung, gestrichen.
3. **Kapitel 5.** Der Satz auf dem Parkplatz in Eppendorf fiel „im Juni
   2024" und lag laut demselben Absatz „vor drei Jahren" — das Kapitel
   spielt im Mai 2026. Auf *vor zwei Jahren* korrigiert.
4. **Kapitel 64.** „Weil Nadia gegessen werden wollte." Gemeint war das
   Baby, das Hunger hat; dasteht, dass es verspeist werden möchte.

Beim Nachsehen dazu gefunden: Amira sagt im letzten Kapitel, sie habe
*achtzehn Jahre* gewartet, ob sie bleiben darf. Es sind elf — die Zahl,
die das ganze Buch trägt.

**Zwei Meldungen waren keine Fehler**, und das ist genauso ein
Ergebnis: Frau Sarrazin sei „aus dem Nichts" erwähnt (sie steht in
Kapitel 1, das Modell liest jedes Kapitel einzeln), und Theo sei mal
„der Bauherr" und mal der Bruder des Auftraggebers (beides stimmt — er
hält neunzehn Prozent der Firma).

### Elf Jahre sind eine Zahl, keine laufende Uhr

`elf Jahre` ist das Leitmotiv des Buches: Amiras Zeit auf Zeit. An
zehn Stellen in den Kapiteln 37 bis 64 stand sie in der Verlaufsform —
*„seit elf Jahren"*, *„in den letzten elf Jahren"* —, obwohl diese
Kapitel 2027 bis 2029 spielen, wo es zwölf, dreizehn, vierzehn wären.
Alle zehn auf die abgeschlossene Form gebracht (*„elf Jahre lang"*,
*„nach elf Jahren"*). Die Zahl bleibt, die Uhr steht still, und das ist
inhaltlich genau richtig: Die elf Jahre enden mit dem Titel im
November 2026.

### Vorspann und Nachspann

- Der Inhaltshinweis nannte eine Fehlgeburt, „die zwölf Jahre
  zurückliegt". Im Text (Kapitel 35) war Amira dabei neunundzwanzig,
  also vor rund fünf Jahren. Die Jahreszahl ist raus.
- In der Leseprobe auf Band 3 ist ein Vertrag von 2019 „vor sechs
  Jahren" geschrieben worden. Auf *acht* korrigiert.

### Die Rechtschreibprüfung stand im Handbuch und lief nie

Der Kopf von `prosa.py` zählt seit dem ersten Tag auf, was das Gerät
kann, und *„Rechtschreibung und Grammatik (LanguageTool)"* steht in
dieser Liste. Die Filterliste der auszunehmenden Regeln steht auch da.
**Der Aufruf fehlte.** In keinem Lauf, bei keinem der beiden Bände, ist
je ein Wort auf Rechtschreibung geprüft worden — und der Bericht las
sich, als sei es geschehen. Das ist schlimmer als ein Gerät, das nichts
verspricht.

Am 31.08.2026 nachgetragen, mit Kalibrierung in drei Fällen: ein
bekannter Grammatikfehler *muss* anschlagen, ein sauberer Satz *darf
nicht*, und die erfundenen Eigennamen (Kehrwieder, Haddad, Okonkwo)
müssen gefiltert bleiben, sonst ertrinkt jeder echte Fund.

**110 Treffer beim ersten Lauf. Acht davon waren echte Fehler:**

| Kapitel | Stand | Jetzt |
|---|---|---|
| 6 | `Jahr — “` (Leerzeichen vor dem Schlusszeichen) | `Jahr —“` |
| 18 | „Hören Sie damit auf, **so bald** Sie können" | **sobald** |
| 30 | „wenn die Sonne den ganzen Tag **drauf stand**" | **draufstand** |
| 35 | „Sonst **muss** du mich trösten" | **musst** |
| 37 | „**wegen dem** ich vierzehn Monate lang" | **wegen dessen** |
| 46 | „und wieder **runter gefahren**" | **runtergefahren** |
| 52 | „an **den zweiten** Juniwoche gehalten" | **die zweite** |
| 52 | „Wir **haben** beide nichts vorbereitet **gehabt**" (Doppelperfekt) | „Wir **hatten** beide nichts vorbereitet" |

**47 der 110 Treffer waren gar keine**, sondern die Stimme des Buches:
*rausgehen* statt *hinausgehen* und aufeinanderfolgende Sätze mit
demselben Anfang. Beides sind jetzt begründete Einträge in der
Filterliste — wer sie wegkorrigiert, korrigiert die Erzählstimme.
Bleiben **54**, alle durchgesehen: bewusste Satzfragmente („Nicht weil
Hamburg besser ist."), Ellipsen („Welche?" „Die erste."), das
*daß* im zitierten Dokument von 1943 und Ruszczyks Plattdeutsch.

Ein Treffer war ein Artefakt der eigenen Messung: In Kapitel 55 steht
ein Zitat im Zitat kursiv, und weil vor dem Prüfen das Markdown
entfernt wird, wurde daraus ein doppeltes „hat". Das steht jetzt als
Warnung im Code.

**Band 1 gleich mitgeprüft** (`PROSA.md`): 90 Treffer, dieselben
Kategorien, **kein harter Fehler darunter**. Band 1 bleibt unangetastet.

### Ein Werkzeug, das man richtig aufrufen muss, ist falsch gebaut

`prosa.py --buch buch2` **ohne** `--bericht` hat den Prosa-Bericht von
Band 1 mit den Zahlen von Band 2 überschrieben. Der Berichtspfad
richtet sich jetzt nach dem Buch; Band 2s Bericht liegt als
`buch2/PROSA.md`.

---

## Was recherchiert und nicht erfunden ist

- **Ehegattennachzug und Scheineheverdacht** (§§ 27, 28 AufenthG):
  getrennte Anhörung beider Ehepartner, materielle Beweislast beim
  Antragsteller, Auskunftsverlangen nach § 86 AufenthG.
- **Der Hausbesuch** braucht die Einwilligung der Bewohner (Art. 13 GG).
  Ablehnung ist zulässig, wird aber in der Abwägung berücksichtigt —
  genau diese Zange ist Kapitel 18, und sie ist nicht ausgedacht.
- **Befangenheit von Sachverständigen**: § 21 VwVfG gilt entsprechend,
  Maßstab ist nicht die tatsächliche Parteilichkeit, sondern ob ein
  vernünftiger Dritter sie befürchten dürfte. Das ist der niedrigere
  Maßstab, und darauf beruht Kapitel 13.
- **Zement in Kalkmörtelfugen** eines Backsteinbaus von 1888: Der
  Zement ist härter als der Stein, die Wand kann nicht mehr arbeiten,
  und was bricht, ist der Stein. Das trägt das Leitmotiv des Buches.

---

## Das KDP-Paket

Steht in `KDP-LAUNCH-2.md`: Untertitel, drei Klappentexte mit
Empfehlung, sieben Keywords, drei Kategorien, Preis, KDP Select.

**Der Nischenlauf vom 31.08.2026 hat die Empfehlung geändert, die ich
vorher aufgeschrieben hatte.** Drei Sachen, die ich ohne Messung falsch
gehabt hätte:

- **Band 2 steht in schwächeren Nischen als Band 1.** *Geheime Ehe* hat
  BSR-Median 10.091, *geheimes baby* hatte 829. Eine Größenordnung
  weniger Nachfrage. Band 2 lebt deshalb stärker von Band 1s
  Leserinnen als von eigener Sichtbarkeit — die Reihenseite ist hier
  wichtiger als jedes Keyword.
- **Die Nische mit der besten Nachfrage ist die falsche.** *ehe roman
  deutsch* liegt bei BSR 1.567, aber der Preis-Median ist 24,32 €, kein
  einziger Titel im 70-%-Fenster, und die Spitzenplätze belegen
  Psychothriller und ein expliziter Erotiktitel. Dort wird keine
  Liebesgeschichte gesucht.
- **Slow Burn ist eine Hitzegrad-Falle.** Der Trope trifft auf dieses
  Buch zu, aber drei von fünf messbaren Spitzentiteln der Nische sind
  ausdrücklich explizit. Der Begriff ist deshalb *nicht* in den
  Keywords, obwohl er inhaltlich stimmt.

Die beste passende Nische ist **familiengeheimnis liebesroman**
(BSR 2.989, Bewertungen-Median nur 60), und ihre Spitzentitel stehen
unter deutschen Autorinnennamen — Karla Linden, Lina Martens, Leni
Lund. Jule Norden passt dort hin.

---

## Offen

| Punkt | Wer |
|---|---|
| KI-Angabe im KDP-Formular (Text **und** Bild) | nur der Kontoinhaber |
| US-Steuerinterview | nur der Kontoinhaber; gilt fürs Konto, nicht je Titel |
| Reihenseite bei KDP anlegen | erst möglich, wenn beide Bände online sind |
| Keyword-Feld 6 (`brüder saga deutsch`) gegenprüfen | *Brüder* steht im Untertitel in der Reihenklammer; ob Amazon die mitindiziert, ist nicht messbar |
| Band 3 (Niklas) | Haken steht im Epilog und im Nachspann |

**Der Umschlag ist gebaut und gemessen**, alle vier Werte im
Nischenband: Helligkeit 58,7 (55,8–64,5), Sättigung 113,6
(94,5–119,7), Verhältnis 1,60, Textzone 4. Weiß auf Grund 12,83 : 1.
Erreicht mit den neuen Reglern `--helligkeit 1.35 --saettigung 0.95`,
die es vorher nicht gab — Band 1 hatte seine Sättigung im August von
Hand nachgezogen, und das stand nirgends.
