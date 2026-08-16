# Lektoratsbericht

*Sein bestgehütetes Geheimnis* · Die Reinhardt-Brüder 1
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
   wurden die Kapitel 7, 9, 11, 13, 15, 42, 43, 44, 46, 48, 51, 52, 56
   ganz neu gelesen und die Kapitel 14, 17, 23, 30, 35, 50 in den
   Abschnitten, gegen die ich prüfen musste. Angefasst habe ich nur
   Kapitel, die ich in dieser Sitzung gelesen habe.
3. **Gemessen, bevor geschrieben wurde.** Zwei neue Messgeräte, eins
   erweitert. Was dabei herauskam, steht unter B.
4. **Eingegriffen.** Neun Kapitel, siehe C.
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
| 86 % | 50 | Ihre Hand an seinem Ärmel |
| 95 % | 56 | Das Handgelenk mit dem Mehl — die Nacht |

Zwischen dem Stirnkuss bei 32 % und der Nacht bei 95 % lagen
**dreiundsechzig Prozent des Buches ohne eine einzige Steigerung.**

Das ist die Antwort auf die Frage, warum das Buch handwerklich stark ist
und sich als Liebesroman trotzdem kühl anfühlt. Es ist kein Stilproblem
und kein Figurenproblem. Es ist eine fehlende Leiter.

### Was das Buch selbst dazu sagt

Kapitel 51 benennt die Spannung wörtlich — *„Alles, was uns bisher
zusammengehalten hat, war ein Problem […] Und jetzt gibt es nichts mehr
zu regeln"* — und **spielt sie nicht**. Die Figur formuliert die
Analyse, die eine Szene hätte sein müssen.

### Zwei weitere Messungen

**Geschäftsdichte.** Treffer auf Bank, Beirat, Gutachten, Grundbuch,
Notar, Forderung, Frist, Vertrag und Verwandtes, je 1000 Wörter:

| | Wert |
|---|---:|
| Buchdurchschnitt | 3,5 |
| Kapitel 39–46 (66–80 %) | 9,1 bis **16,6** |

Acht Kapitel am Stück mit der drei- bis fünffachen Dichte. Das Buch als
Ganzes ist nicht überladen — es hat einen Klumpen an der Stelle, an der
die Liebesgeschichte auf ihren Höhepunkt zulaufen müsste.

**Konfliktloses Fenster.** Zwischen 78 % und 86 % (Kapitel 46 bis 51)
gab es keinen einzigen Konflikt. Grundbuch, Zustimmungsvorbehalt,
Mutterbesuch, Eingewöhnung — alles gelang.

**Was nicht zu beanstanden war:** kein einziges *„sie war wunderschön"*,
kein *„Schmetterlinge im Bauch"*, kein *„die Luft knisterte"*, keine der
zwanzig geprüften KI-typischen Wendungen. Null Treffer, gegen eine
Kontrollsuche geprüft, die treffen musste und traf.

---

## C — Die Eingriffe

Neun Kapitel. Jeder Eingriff benutzt Material, das schon im Buch stand.

### 1. Kapitel 51 — der Beinahe-Kuss (⭐ der wichtigste)

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

### 2. Kapitel 52 — die Rechnung

*„Nicht heute"* fällt hier zum dritten Mal, und Jonas zählt zusammen:

> Es ist kein Nein. Es ist eine Uhr. Sie sagt mir jedes Mal, wie spät es
> ist, und ich habe jedes Mal gemacht, was ein höflicher Mann macht,
> nämlich nichts.

Sein Zettel mit den drei Antworten — warum er *Papa* nicht sagt — hat
jetzt eine Rückseite: dieselbe Feigheit, andere Frage. Und er nimmt am
Morgen danach seinen eigenen Satz zurück: *„Ich frage noch mal. Nicht
heute. Aber ich frage noch mal."*

### 3. Kapitel 56 — sie kommt ihm zuvor

Sie setzt den Termin (*„Samstag um acht"*), und er merkt, dass ihn das
ärgert, und dann merkt er, warum: Er hätte gern, dass es seine Frage
ist, damit er hinterher weiß, dass er es war. Also genau das, was er ihr
vorwirft.

Damit steht das Thema des Buches am Ende dreimal übereinander: das
Geheimnis, das Wort *Papa*, und die Frage, wer anfängt.

### 4. Kapitel 48 — der Rückschlag im leeren Fenster

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

### 6. Kapitel 44 — Geschäftsstrang zurückgenommen

Raus: die 1,7-Milliarden-Aufstellung (steht schon in Kapitel 12) und
Wendlands Siebenhunderttausend-Rechnung. Zwei Zahlenblöcke im
geschäftsdichtesten Kapitel des Buches, die den Satz danach nicht besser
machen.

### 7. Kapitel 23 — ein Sprachtick

*„Das ist der Teil, den ich mir …"* stand fast wortgleich schon in
Kapitel 8.

### 8. Kapitel 50 — ein Datumsfehler, der vorher drinstand

Tag eins der Eingewöhnung war als *„Achtzehnter Februar, Montag"*
angegeben. Der 18. Februar 2026 ist ein **Mittwoch**. Mit Montag fiel
der fünfte Eingewöhnungstag auf einen Freitag, obwohl im selben Kapitel
steht, es sei ein Dienstag gewesen (*„Sie war dienstags nie da. Dienstag
ist Backtag"*). Mit Mittwoch stimmt beides.

Das Buch benutzt sonst durchgehend den echten Kalender 2025/26 —
nachgerechnet für den 27.01., 26.03., 27.03., 02.04., 04.04., 15.04. und
18.04. Alle stimmen.

### 9. Kapitel 47/56/52 — Anschlüsse

Kleinere Nähte, damit die neuen Szenen nicht in der Luft hängen: der
Freitag nach dem Beinahe-Kuss, an dem beide so tun, als sei nichts; die
zwölf Tage zwischen seiner Zusage und ihrem Termin.

---

## D — Was ich absichtlich nicht angefasst habe

| Stelle | Warum |
|---|---|
| Kapitel 14, die Schüssel mit Butter und Mehl | Die beste Annäherungsszene des Buches. Drei Sekunden, keine Erklärung. |
| Kapitel 35, der Anruf bei Theo | Die Heldin löst ihr Problem selbst und ruft nicht den Mann an. In dieser Nische die Ausnahme. |
| Kapitel 44, die Beiratssitzung als Ganzes | Sein Höhepunkt. Nur die zwei Zahlenblöcke raus. |
| Kapitel 46, der Notartermin | Die Zurückhaltung *ist* die Szene: *„Ich habe im Flur gestanden und gesehen, wie sie sich am Geländer festhielt, und ich bin nicht hingegangen."* |
| Kapitel 56, die Nacht | Drei Dinge in einer Liste statt einer Szene. Es funktioniert, es ist nicht explizit, es bleibt. |
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
| **Romance** | 5 | **7** | Die Leiter existiert jetzt: Nicht-Berührung 14 %, Berührung 27 %, Stirnkuss 32 %, Hand 53 %, Ärmel 86 %, **Beinahe-Kuss 87 %**, Nacht 95 %, Antrag 100 %. Noch immer langsamer als die Nische — aber nicht mehr leer. |
| **Figuren** | 9 | **9** | Beide verändern sich am selben Fehler, von zwei Seiten. Leni entscheidet, widerspricht, setzt Grenzen und löst ihr Problem selbst. |
| **Spannung** | 6 | **7** | Das konfliktlose Fenster 78–86 % ist geschlossen. Es gewinnt weiterhin kein Gegenspieler jemals etwas — siehe F. |
| **Emotion** | 9 | **9** | Kapitel 27/28 (Fieberkrampf), 34 (Heiligabend), 52 (*Papa*) tragen ohne Hilfe. |
| **Secret Baby** | 8 | **8** | Der häufigsten Ein-Stern-Kritik ist die Grundlage entzogen: drei Anrufe, drei Seiten Brief, der Vermerk *erledigt*, und die Frau, die ihn abgefangen hat. |
| **Billionaire Romance** | 5 | **6** | Bewusst leise: Er wischt Tische ab und trägt einen Anorak aus dem Fundkorb. Wer Privatjets erwartet, bekommt keine. Kapitel 12 nennt die 1,7 Mrd früh genug, damit der Untertitel gedeckt ist. |
| **KDP-Potenzial** | 5 | **6** | Kategorien und Hitzegrad gemessen, Keywords und Klappentext stehen. Zwei Bremsen bleiben: Länge und Titel — siehe F. |
| **Serienpotenzial** | 8 | **8** | Theo, Niklas, Bastian und Amira sind angelegt, ohne dass Band 1 offen bleibt. Bastians Zeile *„Halt dir August frei"* ist der beste Haken. |

---

## F — Was offen bleibt

Vier Punkte. Der erste ist eine gemessene Abweichung, die anderen drei
sind Entscheidungen, die dem Autor gehören.

### 1. Die Länge — der einzige gemessene Fehlschlag

| | Wörter | ≈ Druckseiten |
|---|---:|---:|
| Jetzt | **71.273** | 285 |
| Unterkante der Nische | 78.000 | 312 |
| Median der Nische | 84.250 | 337 |

Gemessen am 16.08. an vier Spitzentiteln der Nische *geheimes baby*
(`../KDP-NISCHEN.md`). Es fehlen **6.700 Wörter** bis zur Unterkante,
**13.000** bis zum Median.

Wo sie hingehören, wenn sie hinsollen: in die Strecke 55–75 %, in der
das Buch am dünnsten mit gemeinsamen Szenen besetzt ist, und nicht in
den Anfang.

### 2. Kein Gegenspieler gewinnt jemals etwas

Kellermann wird abgelehnt und steht danach nur in der Zeitung. Wendland
wird Verbündeter. Bosses Abberufungsantrag scheitert in derselben Szene,
in der er gestellt wird.

Jeder Widerstand ist innerer Widerstand. Das ist der Grund, warum das
Buch nicht kitschig wird — und es heißt, dass die Handlung ausschließlich
von den Fehlern der beiden Hauptfiguren angetrieben wird. Ich habe das
nicht eigenmächtig geändert, weil eine eingebaute Intrige das Buch zu
einem anderen Buch machen würde.

### 3. Kapitel 10 und 11

Zwei Texturkapitel hintereinander bei 18–24 %, dort, wo sich bei Kindle
Unlimited entscheidet, ob weitergelesen wird. Beide sind gut. Der
Perspektivwechsel lässt einen Tausch nicht zu, ohne den Rest zu drehen.
Möglicher Eingriff: eines auf rund tausend Wörter kürzen.

### 4. Der Titel

*„Sein bestgehütetes Geheimnis"* schreibt das Geheimnis ihm zu. Es ist
ihres. Zehn Alternativen mit Empfehlung stehen in `KDP-PAKET.md`; die
Entscheidung ist eine Geschäftsentscheidung und keine Lektoratsfrage.
**Die finale EPUB trägt noch den alten Titel** — ein Lauf von
`manuskript.py --titel "…"` tauscht ihn.

---

## G — Die Dateien

| Datei | Was |
|---|---|
| `reinhardt-1_original.epub` | Der Stand vor der Überarbeitung. Unverändert. |
| `reinhardt-1_KDP_final.epub` | 71.273 Wörter, 59 Kapitel, 663 kB, 61 Abschnitte |
| `KDP-PAKET.md` | Titel, Klappentext, Keywords, Kategorien — **nicht im Buch** |
| `LEKTORAT.md` | dieser Bericht |
| `DRAMATURGIE.md`, `PRUEFUNG.md` | die beiden Lesungen davor |

Im Buch selbst steht nichts davon. Keine Lektoratskommentare, keine
Platzhalter, keine internen Notizen — `manuskript.py` prüft das bei jedem
Lauf gegen einen Positiv- und einen Negativfall und meldet „Keine
Beanstandungen".

---

## H — Was als Nächstes ansteht

1. **Titel entscheiden** (`KDP-PAKET.md`, Abschnitt 1), dann EPUB neu
   bauen.
2. **Länge entscheiden.** 6.700 Wörter bis zur Unterkante. Das ist die
   einzige gemessene Abweichung von der Nische.
3. **Zwei Dinge, die nur der Kontoinhaber kann:** die KI-Angabe im
   Veröffentlichungsformular und das US-Steuerinterview.
4. **Judge.me aufräumen** — die App liefert weiterhin ein
   `aggregateRating` aus erfundenen Bewertungen. Das ist ein anderer
   Vorgang als dieses Buch, steht aber in `CLAUDE.md` unter „Offene
   Punkte" und wäre bei einer Autorenseite im Shop ein Rechtsproblem.
