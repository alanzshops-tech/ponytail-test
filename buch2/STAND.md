# Band 2 — Stand

**Fertig.** 24.08.2026.

| | |
|---|---|
| Titel | *Was er nie gefragt hat* |
| Untertitel | Eine geheime Ehe, eine Frist und eine Familie, die alles regelt |
| Reihe | Die Reinhardt-Brüder, Band 2 |
| Autorin | Jule Norden (Pseudonym, wie Band 1) |
| Umfang | **64 Kapitel, 69.294 Wörter Fließtext, 70.028 Wörter gesamt** |
| Erzählform | Ich-Perspektive, wechselnd Amira / Theo, Präteritum |
| Datei | `buch2/reinhardt-2_KDP.epub` (1.143 kB, 66 Abschnitte) |
| Lesefassung | `buch2/Was-er-nie-gefragt-hat.epub` |
| Umschlag | `cover/band2/cover.jpg`, 1600 × 2560 |

---

## Die Prüfläufe

Alle vier Werkzeuge laufen mit `--buch buch2`:

| Werkzeug | Ergebnis |
|---|---|
| `manuskript.py` | Keine Beanstandungen. Kapitelfolge lückenlos, Perspektivwechsel durchgehend, keine Platzhalter |
| `prosa.py` | 0 falsche Anführungszeichen, 0 falsche Apostrophe, 0 falsche Auslassungspunkte |
| `dopplung.py` | Ein Treffer, absichtlich — siehe `PROJEKT.md` 7c |
| `romantik.py` | 0 von 64 Kapiteln ohne gemeinsame Szene |
| `epubcheck.py` | Keine Beanstandungen |

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
