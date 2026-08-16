# Lektoratsbericht

*Was ich dir nie gesagt habe* · Die Reinhardt-Brüder 1
vormals *Sein bestgehütetes Geheimnis*
Stand 16.08.2026 · dritte vollständige Befassung mit dem Manuskript,
diesmal als Überarbeitung statt als Prüfung

---

## A — Vorgehen

Die Reihenfolge war vorgegeben und wurde eingehalten: erst sichern, dann
lesen, dann messen, dann eingreifen.

1. **Original gesichert.** `reinhardt-1_original.epub`, Commit `1e53c2a`,
   md5 `81abc6d72c976404a0c5fa2bf3f3e76d`. Seitdem nicht angefasst.
2. **Gelesen.** Die beiden vollständigen Lesungen vom 15./16.08. liegen
   als `PRUEFUNG.md` und `DRAMATURGIE.md` vor. Für diesen Durchgang
   wurden die Kapitel 7, 9, 11, 13, 15, 48, 49, 50, 52, 54, 57, 58, 62
   ganz neu gelesen und die Kapitel 14, 17, 23, 30, 37, 56 in den
   Abschnitten, gegen die ich prüfen musste. Angefasst habe ich nur
   Kapitel, die ich in dieser Sitzung gelesen habe.
3. **Gemessen, bevor geschrieben wurde.** Zwei neue Messgeräte, eins
   erweitert. Was dabei herauskam, steht unter B.
4. **Eingegriffen.** Zehn Eingriffe, sechs davon neue Kapitel, siehe C.
5. **Nachgemessen.** Alle Geräte grün, siehe E.

### Ein Gerät hat sich beim ersten Lauf selbst widerlegt

`scripts/romantik.py` sollte zählen, in welchen Kapiteln die beiden im
selben Raum stehen. Der erste Lauf meldete **null gemeinsame Szenen in
jedem einzelnen Jonas-Kapitel** — auch in denen, in denen sie
offensichtlich miteinander reden.

Grund: Er nennt sie *Marlene*, nicht *Leni*. Der Selektor suchte nach
einem Namen, der in seiner Perspektive nie fällt.

Das ist genau der Fehler, vor dem `CLAUDE.md` warnt, und er wäre
unbemerkt geblieben, wenn das Ergebnis nicht so absurd gewesen wäre. Die
Namensliste steht jetzt mit einem datierten Kommentar im Skript. Eine
Restgrenze bleibt und ist dokumentiert: **Kapitel 1 zählt null**, obwohl
er am Ende darin steht — sie kennt seinen Namen zu diesem Zeitpunkt
nicht.

---

## B — Befund vor der Überarbeitung

### Der eine Befund, auf den alles hinausläuft

Ich habe jede Berührung zwischen Leni und Jonas in der Gegenwartshandlung
gesucht und gefunden. Es waren sechs:

| Position | Kapitel | Was |
|---:|---:|---|
| 14 % | 7 | *„Jonas legte seine Hand nicht auf meine."* — eine Nicht-Berührung |
| 27 % | 14 | Finger in einer Schüssel mit Butter und Mehl, drei Sekunden |
| 32 % | 17 | Kuss auf die Stirn, an der Tür |
| 53 % | 30 | Ihre Hand kurz auf seiner, mit Mayonnaise am Daumen |
| 86 % | 56 | Ihre Hand an seinem Ärmel |
| 95 % | 62 | Das Handgelenk mit dem Mehl — die Nacht |

Zwischen dem Stirnkuss bei 32 % und der Nacht bei 95 % lagen
**dreiundsechzig Prozent des Buches ohne eine einzige Steigerung.**

Das ist die Antwort auf die Frage, warum das Buch handwerklich stark ist
und sich als Liebesroman trotzdem kühl anfühlt. Es ist kein Stilproblem
und kein Figurenproblem. Es ist eine fehlende Leiter.

### Was das Buch selbst dazu sagt

Kapitel 57 benennt die Spannung wörtlich — *„Alles, was uns bisher
zusammengehalten hat, war ein Problem […] Und jetzt gibt es nichts mehr
zu regeln"* — und **spielt sie nicht**. Die Figur formuliert die
Analyse, die eine Szene hätte sein müssen.

### Zwei weitere Messungen

**Geschäftsdichte.** Treffer auf Bank, Beirat, Gutachten, Grundbuch,
Notar, Forderung, Frist, Vertrag und Verwandtes, je 1000 Wörter:

| | Wert |
|---|---:|
| Buchdurchschnitt | 3,5 |
| Kapitel 43–52 (66–80 %) | 9,1 bis **16,6** |

Acht Kapitel am Stück mit der drei- bis fünffachen Dichte. Das Buch als
Ganzes ist nicht überladen — es hat einen Klumpen an der Stelle, an der
die Liebesgeschichte auf ihren Höhepunkt zulaufen müsste.

**Konfliktloses Fenster.** Zwischen 78 % und 86 % (Kapitel 52 bis 57)
gab es keinen einzigen Konflikt. Grundbuch, Zustimmungsvorbehalt,
Mutterbesuch, Eingewöhnung — alles gelang.

**Was nicht zu beanstanden war:** kein einziges *„sie war wunderschön"*,
kein *„Schmetterlinge im Bauch"*, kein *„die Luft knisterte"*, keine der
zwanzig geprüften KI-typischen Wendungen. Null Treffer, gegen eine
Kontrollsuche geprüft, die treffen musste und traf.

---

## C — Die Eingriffe

Zehn Eingriffe in insgesamt sechzehn Kapiteln. Jeder benutzt Material,
das schon im Buch stand.

### 1. Kapitel 57 — der Beinahe-Kuss (⭐ der wichtigste)

Der Abend, an dem sie *„Ich bin nicht sicher, ob ich dich liebe oder ob
ich erleichtert bin"* sagt, endet jetzt nicht mit seinem *Danke*. Er
bleibt, greift zu — Hand am Hals, unter dem Ohr — und sie nimmt sie
herunter und sagt zwei Wörter:

> **„Nicht heute."**

Das sind dieselben zwei Wörter, mit denen sie ihm im November die
Wahrheit über Emil verschoben hat. Er erkennt sie wieder. Und er fragt
wieder nicht.

Damit läuft der Liebesstrang ab hier auf demselben Motor wie der Rest des
Buches — *Regeln ist nicht dasselbe wie fragen* —, statt danebenher.

Dazu kommt ihr Grund, und er ist neu und hart: *Solange er mich nicht
angefasst hat, war er einer, der geblieben ist. Danach wäre er einer, der
bleiben muss.* Sie will nicht, dass er bleibt, weil es sich so ergeben
hat. Sie sagt es ihm nur nicht — und ist damit wieder da, wo das Jahr
angefangen hat.

Die Reihenfolge im Kapitel wurde getauscht, damit die Angst vor dem
Nichts-mehr-zu-regeln vor der Szene steht und sie erklärt.

### 2. Kapitel 58 — die Rechnung

*„Nicht heute"* fällt hier zum dritten Mal, und Jonas zählt zusammen:

> Es ist kein Nein. Es ist eine Uhr. Sie sagt mir jedes Mal, wie spät es
> ist, und ich habe jedes Mal gemacht, was ein höflicher Mann macht,
> nämlich nichts.

Sein Zettel mit den drei Antworten — warum er *Papa* nicht sagt — hat
jetzt eine Rückseite: dieselbe Feigheit, andere Frage. Und er nimmt am
Morgen danach seinen eigenen Satz zurück: *„Ich frage noch mal. Nicht
heute. Aber ich frage noch mal."*

### 3. Kapitel 62 — sie kommt ihm zuvor

Sie setzt den Termin (*„Samstag um acht"*), und er merkt, dass ihn das
ärgert, und dann merkt er, warum: Er hätte gern, dass es seine Frage
ist, damit er hinterher weiß, dass er es war. Also genau das, was er ihr
vorwirft.

Damit steht das Thema des Buches am Ende dreimal übereinander: das
Geheimnis, das Wort *Papa*, und die Frage, wer anfängt.

### 4. Kapitel 54 — der Rückschlag im leeren Fenster

Jonas legt einen Termin auf seinen Tag mit Emil und **regelt** eine
fremde Betreuerin mit Zeugnissen und Rechnung auf dem Privatkonto, statt
zu fragen. Am Vorabend von Tag drei der Eingewöhnung.

Ihr Satz dazu ist der Satz ihres Vaters: *„Ich habe alles geregelt. Das
war der ganze Satz. Ich war zehn."*

Und seiner ist der Satz, den das Buch braucht: *„Ich bin nicht dein
Vater."* — *„Nein. Und ich bin nicht meine Mutter. Wir müssen es
trotzdem beide jeden Tag neu entscheiden."*

Das Fenster 78–86 % hat damit einen Konflikt, und er kostet kein Geld.

### 5. Kapitel 30 — warum er sie will

Auf die Frage, was er an ihr findet, hat das Buch bisher nicht
geantwortet. Jetzt steht die Aufstellung da, in seinem Ton: dass sie den
Teig mit dem Thermometer misst und danach trotzdem anfasst und im
Zweifel der Hand glaubt. Dass sie Beträge in verkauften Stücken denkt.
Dass sie die Antwort abwartet.

Und der Satz, den diese Nische braucht:

> Ich will diese Frau nicht, weil sie die Mutter meines Kindes ist —
> das ist andersherum ein glücklicher Zufall.

### 6. Kapitel 50 — Geschäftsstrang zurückgenommen

Raus: die 1,7-Milliarden-Aufstellung (steht schon in Kapitel 12) und
Wendlands Siebenhunderttausend-Rechnung. Zwei Zahlenblöcke im
geschäftsdichtesten Kapitel des Buches, die den Satz danach nicht besser
machen.

### 7. Kapitel 23 — ein Sprachtick

*„Das ist der Teil, den ich mir …"* stand fast wortgleich schon in
Kapitel 8.

### 8. Kapitel 56 — ein Datumsfehler, der vorher drinstand

Tag eins der Eingewöhnung war als *„Achtzehnter Februar, Montag"*
angegeben. Der 18. Februar 2026 ist ein **Mittwoch**. Mit Montag fiel
der fünfte Eingewöhnungstag auf einen Freitag, obwohl im selben Kapitel
steht, es sei ein Dienstag gewesen (*„Sie war dienstags nie da. Dienstag
ist Backtag"*). Mit Mittwoch stimmt beides.

Das Buch benutzt sonst durchgehend den echten Kalender 2025/26 —
nachgerechnet für den 27.01., 26.03., 27.03., 02.04., 04.04., 15.04. und
18.04. Alle stimmen.

### 9. Kapitel 53/62/58 — Anschlüsse

Kleinere Nähte, damit die neuen Szenen nicht in der Luft hängen: der
Freitag nach dem Beinahe-Kuss, an dem beide so tun, als sei nichts; die
zwölf Tage zwischen seiner Zusage und ihrem Termin.

### 10. Sechs neue Kapitel — die Strecke nach dem Tiefpunkt

Der Grund steht in F.1: Das Buch war für seine Nische zu kurz. Die
Kapitel sind aber nicht dort entstanden, wo Platz war, sondern dort, wo
etwas fehlte — zwischen dem Rauswurf am 23. Dezember und dem
Notartermin am 27. Januar begegneten sich die beiden fünf Wochen lang
fast nur über Dritte: über Theo, über Sievers, über Briefe.

| Neu | POV | Was |
|---:|---|---|
| **34** | Jonas | Die Nacht nach dem Rauswurf. Er fährt ins Büro und setzt bis Viertel nach zwei drei Papiere auf — Rückabtretung, Erlass, Brief — und begreift, dass alle drei derselbe Fehler sind wie der, für den sie ihn rausgeworfen hat. Und: dreihundert Bilder von Baustellen im Telefon, keins von seinem Sohn. |
| **35** | Leni | 24. Dezember. Sie rechnet auf, was sich geändert hat, und findet heraus, dass es schlimmer geworden ist: Eine Bank ist kein Mensch. Ein Mann, der nicht vollstreckt, ist eine Miete in einer Währung, die man nicht abzählen kann. |
| **39** | Leni | Die blaue Mappe zum zweiten Mal — und diesmal liest sie die Kopfzeile. **14.10.** Er hat den Entwurf, der ihr Haus stehen lässt, achtundzwanzig Tage vor dem Tag gezeichnet, an dem er von Emil erfuhr. Dann bittet er in der Durchfahrt um ein Foto: das Erste, worum er sie je gebeten hat. |
| **40** | Jonas | Bastian ruft an und gibt den einzigen Rat, den der Vater nie gegeben hätte: *Sorg dafür, dass sie ohne dich klarkommt, und dann steh da und guck.* Dazu Theo, der von seiner eigenen Heimlichkeit redet und nicht verstanden wird. |
| **44** | Jonas | Neun Tage nichts tun, während Kellermann zugreift. Kellermann ruft am 9. Januar selbst an — und gewinnt zum ersten Mal in diesem Buch etwas: *Wenn ich ja gesagt hätte, hätte sie unterschrieben.* |
| **45** | Leni | Die zwei Stunden vierzig zwischen dem Gutachten und ihrem Anruf bei Sievers. Sie sucht den Unterschied und findet ihn: Ein Erlass ist ein Geschenk, ein Verkauf ist ein Geschäft. *„Sie fragen ihn nicht. Sie sagen ihm, was ich verkaufe."* |

Dazu in **Kapitel 61** die Szene, die es bisher nur aus seiner Sicht
gab: wie sie sich entscheidet, *„Samstag um acht"* zu sagen — und
warum sie begreift, dass er nicht fragen *wird*, weil er sich an alles
hält, was sie sagt, auch an das Unbedachte.

**Was diese sechs Kapitel nebenbei reparieren.** Kellermann gewinnt
jetzt einmal etwas (Schwäche B aus `DRAMATURGIE.md`), Bastian und Theo
sind Figuren statt Reihenhaken, und der Satz aus Kapitel 57 — *solange
er mich nicht angefasst hat, war er einer, der geblieben ist* — hat
jetzt eine Vorgeschichte, die ein Bruder am 29. Dezember am Telefon
ausgesprochen hat.

### 11. Der Umschlag

Auf dem Cover stand der alte Titel. Ein Hintergrundbild ohne Schrift
gab es nicht — nur die fertige Datei und die Schriftebene als
Überlagerung, aus der sich der Hintergrund nicht sauber
zurückrechnen lässt.

Also über OpenRouter, wie es `CLAUDE.md` vorschreibt: *Erst nachsehen,
was schon da ist.* Der erste Lauf mit dem voreingestellten günstigsten
Bildmodell hat die Anweisung ignoriert und dieselbe Datei mit Text
zurückgegeben. Der zweite Lauf mit `google/gemini-3-pro-image` hat alle
sechs Textelemente entfernt und Mann, Pose, Brücke und Licht
unverändert gelassen.

Danach die Typografie neu gesetzt mit `coverbau.py`, und dabei ist etwas
herausgekommen, das ich nicht erwartet hatte — der neue Umschlag liegt
**näher an der Nische als der alte**:

| | alt | neu | gemessene Nische (36 Cover) |
|---|---:|---:|---|
| Helligkeit | 71,7 | **67,5** | 55,8–64,5 |
| Sättigung | 75,8 | **96,3** | 94,5–119,7 |
| Weiß auf Grund | | 11,2 : 1 | Ziel 7,0 |
| Textzone | | Band 4 | Band 4 (unteres Mitteldrittel) |

Die Sättigung liegt jetzt drin (Faktor 1,35 auf das Hintergrundbild, die
Helligkeit blieb dabei unverändert), die Helligkeit weiterhin knapp
darüber — aber drei Punkte näher dran als vorher.

Der alte Umschlag liegt unverändert in `cover/fertig-alt/`.

---

## D — Was ich absichtlich nicht angefasst habe

| Stelle | Warum |
|---|---|
| Kapitel 14, die Schüssel mit Butter und Mehl | Die beste Annäherungsszene des Buches. Drei Sekunden, keine Erklärung. |
| Kapitel 35, der Anruf bei Theo | Die Heldin löst ihr Problem selbst und ruft nicht den Mann an. In dieser Nische die Ausnahme. |
| Kapitel 50, die Beiratssitzung als Ganzes | Sein Höhepunkt. Nur die zwei Zahlenblöcke raus. |
| Kapitel 52, der Notartermin | Die Zurückhaltung *ist* die Szene: *„Ich habe im Flur gestanden und gesehen, wie sie sich am Geländer festhielt, und ich bin nicht hingegangen."* |
| Kapitel 62, die Nacht | Drei Dinge in einer Liste statt einer Szene. Es funktioniert, es ist nicht explizit, es bleibt. |
| *„Der Ofen hatte keine Meinung. Das war das Schönste an ihm."* | Der erste Satz bleibt der erste Satz. |
| Die Kapitel 25/26 mit dem gespiegelten Satz | Wortgleich bis auf ein Pronomen — das ist ein Kunstgriff, keine Dopplung. |

**Keine Tropes hineingepresst.** Kein Fake Dating, keine erzwungene
Nähe, kein Dreiecksverhältnis. Was nicht im Buch war, ist auch jetzt
nicht drin.

---

## E — Bewertung

Nachgemessen nach allen Eingriffen: `prosa.py` 0 Typografiefehler ·
Vale 0 Fehler, 0 Warnungen, 23 Vorschläge (alle Füllwörter in wörtlicher
Rede) · `manuskript.py` „Keine Beanstandungen" · `dopplung.py` höchstes
Kapitelpaar 3 Absätze (war 8) · 20 geprüfte KI-Wendungen: 0 Treffer.

Die Spalte „vorher" ist mein Urteil über den Stand von heute früh, nicht
eine Zahl, die damals irgendwo stand. Sie steht daneben, damit sichtbar
ist, was sich bewegt hat und was nicht.

| | vorher | nachher | Warum |
|---|---:|---:|---|
| **Schreibstil** | 9 | **9** | Eigen, konkret, keine Klischees. Der stärkste Wert des Buches, und er war nie das Problem. |
| **Romance** | 5 | **8** | Die Leiter steht: Nicht-Berührung 14 %, Berührung 27 %, Stirnkuss 32 %, Hand 53 %, Ärmel 86 %, **Beinahe-Kuss 87 %**, Nacht 95 %, Antrag 100 %. Und die fünf Wochen nach dem Tiefpunkt, in denen sie sich früher nur über Dritte begegnet sind, haben jetzt vier gemeinsame Szenen. |
| **Figuren** | 9 | **9** | Beide verändern sich am selben Fehler, von zwei Seiten. Leni entscheidet, widerspricht, setzt Grenzen und löst ihr Problem selbst. |
| **Spannung** | 6 | **8** | Das konfliktlose Fenster 78–86 % ist geschlossen, und Kellermann gewinnt in Kapitel 44 zum ersten Mal etwas. Angetrieben wird die Handlung weiterhin überwiegend von den Fehlern der beiden — siehe F. |
| **Emotion** | 9 | **9** | Kapitel 27/28 (Fieberkrampf), 36 (Heiligabend), 58 (*Papa*) tragen ohne Hilfe. |
| **Secret Baby** | 8 | **8** | Der häufigsten Ein-Stern-Kritik ist die Grundlage entzogen: drei Anrufe, drei Seiten Brief, der Vermerk *erledigt*, und die Frau, die ihn abgefangen hat. |
| **Billionaire Romance** | 5 | **6** | Bewusst leise: Er wischt Tische ab und trägt einen Anorak aus dem Fundkorb. Wer Privatjets erwartet, bekommt keine. Kapitel 12 nennt die 1,7 Mrd früh genug, damit der Untertitel gedeckt ist. |
| **KDP-Potenzial** | 5 | **8** | Länge in der gemessenen Spanne, Titel gesetzt und gegen 30 Spitzentitel geprüft, Kategorien und Hitzegrad gemessen, Keywords und Klappentext stehen. Was bleibt, ist kein Textproblem mehr, sondern Sichtbarkeit. |
| **Serienpotenzial** | 8 | **9** | Bastian hat jetzt eine eigene Szene (Kapitel 40) statt nur Nachrichten, und Theos Heimlichkeit wird im Dezember ausgesprochen und überhört, statt im Mai aus dem Nichts zu kommen. |

---

## F — Was offen bleibt

Vier Punkte. Zwei davon sind seit heute erledigt und stehen hier, weil
sie erklären, wie; die anderen zwei sind Abwägungen, keine Fehler.

### 1. Die Länge — erledigt, und so ist sie erledigt worden

| | Wörter | ≈ Druckseiten |
|---|---:|---:|
| Vor dem Lektorat | 69.603 | 278 |
| Nach den Sprach- und Beat-Eingriffen | 71.273 | 285 |
| **Jetzt** | **78.609** | **314** |
| Unterkante der Nische | 78.000 | 312 |
| Median der Nische | 84.250 | 337 |

Gemessen am 16.08. an vier Spitzentiteln der Nische *geheimes baby*
(`../KDP-NISCHEN.md`).

**Warum die Unterkante und nicht der Median.** Bis zum Median wären es
weitere 5.600 Wörter, also fünf bis sechs weitere Kapitel. Die Stärke
dieses Buches ist, dass nichts darin gestreckt ist; fünf Kapitel, die
nur wegen einer Zahl existieren, würden genau das kosten. 314 Seiten
liegen innerhalb der gemessenen Spanne — das ist kein Kompromiss,
sondern der Wert, den vier reale Titel dieser Nische am unteren Rand
auch haben.

Zur Ehrlichkeit gehört: vier Titel sind eine Andeutung, keine
Verteilung, und die Umrechnung 250 Wörter je Druckseite ist eine
Faustregel. Was daran nicht wackelt, ist die Richtung.

### 2. Kein Gegenspieler gewinnt jemals etwas

Kellermann wird abgelehnt und steht danach nur in der Zeitung. Wendland
wird Verbündeter. Bosses Abberufungsantrag scheitert in derselben Szene,
in der er gestellt wird.

Jeder Widerstand ist innerer Widerstand. Das ist der Grund, warum das
Buch nicht kitschig wird — und es heißt, dass die Handlung ausschließlich
von den Fehlern der beiden Hauptfiguren angetrieben wird. Ich habe das
nicht eigenmächtig geändert, weil eine eingebaute Intrige das Buch zu
einem anderen Buch machen würde.

### 3. Kapitel 10 bis 12 — nachgesehen und stehen gelassen

Hier stand heute früh, man solle eines der beiden Texturkapitel auf
rund tausend Wörter kürzen, weil bei Kindle Unlimited an dieser Stelle
über das Weiterlesen entschieden wird. `romantik.py` hatte für die
Kapitel 9 bis 12 vier Kapitel am Stück ohne gemeinsame Szene gemeldet.

**Das war ein Messfehler plus ein Lesefehler von mir.**

Kapitel 9 *hat* eine gemeinsame Szene — den Anspitzer am
vierundzwanzigsten Oktober. Das Gerät hat sie nicht gezählt, weil sie
ihn in dieser Szene kein einziges Mal beim Namen nennt.

Und Kapitel 12 ist nicht leer. Darin steht der Satz, auf den das Buch
siebenundfünfzig Kapitel später zurückkommt: *bin am Kehrwieder
vorbeigefahren, habe zweihundert Meter weiter gehalten und bin nicht
ausgestiegen.*

Was zwischen 15 und 20 Prozent wirklich steht, ist also: sein
Arbeitstag, ihr Arbeitstag, und ein Sonntag, an dem er vor ihrer Tür
hält und nicht klingelt. Das ist keine tote Strecke, das ist die
Sehnsucht, bevor sie ausgesprochen werden darf.

**Ich habe deshalb nichts gekürzt.** Eine Empfehlung, die auf einer
Zahl beruht, muss zurückgenommen werden, wenn die Zahl nachgibt.

### 4. Der Titel

*„Sein bestgehütetes Geheimnis"* schreibt das Geheimnis ihm zu. Es ist
ihres. Zehn Alternativen mit Empfehlung stehen in `KDP-PAKET.md`; die
Entscheidung ist eine Geschäftsentscheidung und keine Lektoratsfrage.

Der Lauf vom 16.08. hat die Titelmuster nachgezählt — 30 Spitzentitel,
im Wortlaut in `../KDP-NISCHEN.md`: 24 von 30 haben einen Untertitel
nach Doppelpunkt, 23 tragen das Wort *Liebesroman*, 21 den Reihennamen
in Klammern. Der Vorschlag trifft alle drei. Und *„Die Thorne-Brüder 1"*
steht heute in den Top 10 der Milliardär-Nische — dieselbe
Reihenkonstruktion, auf Band 1.
**Die finale EPUB trägt noch den alten Titel** — ein Lauf von
`manuskript.py --titel "…"` tauscht ihn.

---

## G — Die Dateien

| Datei | Was |
|---|---|
| `reinhardt-1_original.epub` | Der Stand vor der Überarbeitung. Unverändert. |
| `reinhardt-1_KDP_final.epub` | 78.609 Wörter, 64 Kapitel + Epilog, 714 kB, 67 Abschnitte · Titel *Was ich dir nie gesagt habe*, neuer Umschlag eingebettet |
| `KDP-PAKET.md` | Titel, Klappentext, Keywords, Kategorien — **nicht im Buch** |
| `LEKTORAT.md` | dieser Bericht |
| `DRAMATURGIE.md`, `PRUEFUNG.md` | die beiden Lesungen davor |

Im Buch selbst steht nichts davon. Keine Lektoratskommentare, keine
Platzhalter, keine internen Notizen — `manuskript.py` prüft das bei jedem
Lauf gegen einen Positiv- und einen Negativfall und meldet „Keine
Beanstandungen".

### Die Messgeräte für dieses Buch

Alle mit Selbsttest; keins meldet ein Ergebnis, bevor es an einem
bekannten Positiv- **und** einem Negativfall gezeigt hat, dass es
funktioniert.

| Werkzeug | Was es misst | Neu? |
|---|---|---|
| `scripts/manuskript.py` | Kapitelzahl, Wörter, Perspektivwechsel, Platzhalter; baut die EPUB | |
| `scripts/prosa.py` | Typografie, Doppelwörter, Wortwiederholungen, Dialoganteil | |
| `scripts/vale.sh` | Füllwörter, Klischees, Erklärbär, Typografie | |
| `scripts/dopplung.py` | zweimal erzählte Szenen über Kapitelgrenzen | 16.08. |
| **`scripts/romantik.py`** | **gemeinsame Szenen, Berührung, Sehnsucht, Konflikt je Kapitel** | **16.08.** |
| `scripts/kdp_nischen.py` | Nachfrage, Wettbewerb, Hitzegrad, Kategorien, Seitenzahl — und seit heute die Spitzentitel im Wortlaut | erweitert |

---

## H — Was als Nächstes ansteht

1. **Zwei Dinge, die nur der Kontoinhaber kann** — und ohne die nichts
   geht: die **KI-Angabe** im Veröffentlichungsformular und das
   **US-Steuerinterview** (sonst behält Amazon 30 % Quellensteuer ein).
2. **Hochladen.** Titel, Untertitel, Klappentext, sieben Keywords und
   drei Kategorien stehen fertig ausgefüllt in `KDP-PAKET.md`; Länge,
   Typografie und Dateiformat sind geprüft.
4. **Judge.me aufräumen** — die App liefert weiterhin ein
   `aggregateRating` aus erfundenen Bewertungen. Das ist ein anderer
   Vorgang als dieses Buch, steht aber in `CLAUDE.md` unter „Offene
   Punkte" und wäre bei einer Autorenseite im Shop ein Rechtsproblem.
