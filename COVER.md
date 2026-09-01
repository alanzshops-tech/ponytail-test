# Cover in den gemessenen Nischen

Stand: 2026-08-15

Gemessen an den Cover-Bildern der organischen Spitzentitel auf den öffentlichen Amazon-Trefferlisten. Gemessen wird nur, was ohne Deutung in der Bilddatei steht: Format, Helligkeit, Kontrast, Sättigung, Farbanteile und die Lage der Kantenenergie. **Ob ein Mensch abgebildet ist, welche Schrift verwendet wird und welche Stimmung entsteht, wird hier nicht gemessen** — dafür liegen die Kontaktbögen in `cover/`.

Die Spalte **Textzone** sagt, in welchem waagerechten Fünftel die meiste Kantenenergie sitzt; dort steht in aller Regel der Titel. Die Messung ist gegen einen Positiv- und einen Negativfall kalibriert (`--selbsttest`).

| Nische | Cover | Verhältnis | Helligkeit | Kontrast | Sättigung | Textzone (Median) | Kontaktbogen |
|---|---:|---:|---:|---:|---:|---:|---|
| geheimes baby liebesroman | 12 | 1.5 | 64.5 | 67.2 | 106.2 | 4.0 | `cover/kontaktbogen-geheimes-baby-liebesroman.png` |
| milliardär liebesroman | 12 | 1.5 | 55.8 | 59.3 | 94.5 | 4.0 | `cover/kontaktbogen-milliard-r-liebesroman.png` |
| ceo liebesroman | 12 | 1.5 | 63.9 | 68.4 | 119.7 | 2.5 | `cover/kontaktbogen-ceo-liebesroman.png` |

## Farbwelt je Nische

Die häufigsten Farben aller gemessenen Cover einer Nische, nach Gesamtfläche. Das ist der Farbraum, in dem ein neues Cover auffallen oder sich einfügen muss.

**geheimes baby liebesroman** — `#000000` 35%, `#202020` 7%, `#c0a0a0` 5%, `#200000` 5%, `#402020` 5%, `#8060e0` 4%, `#e0e0e0` 3%, `#604040` 3%

**milliardär liebesroman** — `#000000` 39%, `#202020` 8%, `#200000` 8%, `#202040` 6%, `#200020` 5%, `#c0c0c0` 3%, `#604040` 3%, `#c0a080` 3%

**ceo liebesroman** — `#000000` 39%, `#000020` 10%, `#202020` 8%, `#202040` 5%, `#a0a0c0` 4%, `#a0c0c0` 4%, `#8080a0` 4%, `#c0c0a0` 3%

## Grenzen dieser Messung

- **Die Stichprobe ist die erste Trefferseite**, nicht die Bestsellerliste. Wer oben steht, steht dort auch wegen Suchbegriff-Treffern.
- **Cover werden als Miniatur ausgeliefert** (500 px). Feine Typografie ist darin nicht beurteilbar — auf dem Handy sieht die Kundin allerdings auch nur eine Miniatur.
- **Die Kantenmessung findet Schrift, nicht Titel.** Ein detailreiches Foto im selben Band verschiebt den Wert.
- Die Cover sind urheberrechtlich geschützt. Sie liegen hier zur Messung, nicht zur Verwendung.

<!-- HANDNOTIZEN - alles darunter bleibt beim naechsten Lauf erhalten -->

---

## Auswertung 15.08.2026 — 36 Cover, drei Nischen

Zwei Quellen: die Zahlen oben (aus der Bilddatei) und die Kontaktbögen
(angesehen). Ich halte beides getrennt, weil das eine überprüfbar ist und
das andere ein Urteil.

### Was gemessen ist

**Cover sind dunkel, und zwar sehr.** Mittlere Helligkeit im Median 56
bis 65 von 255. Von 36 Covern liegen **zwei** über 100. Das hellste
(152) ist eine Illustration, das zweithellste (141) ein
Sonnenuntergangsfoto. Ein helles Cover fällt in dieser Nische auf — aber
gegen den Strom.

**Schwarz ist die Grundfarbe, nicht ein Akzent.** In jeder der drei
Nischen belegt reines Schwarz 35 bis 39 Prozent der Gesamtfläche, das
nächstdunklere Grau weitere 7 bis 8. Alles Übrige sind Hauttöne, ein
Marineblau (`#202040`) und ein warmes Gold (`#c0a080`).

**Format 1,5 bis 1,6.** Median genau 1,5, Spanne 1,45 bis 1,61. KDP
empfiehlt 1,6 — also **1600 × 2560 px**. Wer 1,5 nimmt, ist nicht allein,
aber 1,6 ist die Norm, an der Amazon die Vorschau ausrichtet.

**Sättigung mittel** (Median 95 bis 120 von 255). Keine Pastelltöne,
keine Knallfarben.

### Was die Kantenmessung hergibt — und wo sie danebenliegt

| Nische | Textzone (Median) | Stimmt das? |
|---|---:|---|
| geheimes baby liebesroman | 4 | **ja** — Titel sitzt im unteren Mitteldrittel |
| milliardär liebesroman | 4 | **ja** — dito |
| ceo liebesroman | 2 | **nein** — dort sitzt das Gesicht |

Der dritte Wert ist genau der Fehler, vor dem der Skriptkopf warnt: „Die
Kantenmessung findet Schrift, nicht Titel." Auf den CEO-Covern füllt ein
Männerkopf das obere Drittel, und Augen, Haaransatz und Hemdkragen
erzeugen mehr Kanten als der Titel darunter. Ich lasse den Wert stehen
und schreibe daneben, dass er falsch ist, statt ihn zu löschen.

**Ergebnis trotzdem eindeutig, aus dem Ansehen:** Der Titel steht auf
allen 36 Covern im mittleren bis unteren Bereich, nie oben. Oben steht,
wenn überhaupt, die Reihenzeile.

### Was ich auf den Kontaktbögen sehe (Urteil, nicht Messung)

**1. Fast immer ein Mensch: 34 von 36.** Die beiden Ausnahmen sind ein
Illustrationscover und eines mit Ringen und Blumen.

**2. Meistens ein Mann allein.** Geheimes Baby 7 von 12, Milliardär 9 von
12, CEO 10 von 12. Anzug oder offenes Hemd, Brustbild oder Kopf,
Blick meistens direkt in die Kamera, ernst.

**3. Das Baby fehlt — im Baby-Trope.** In „geheimes baby liebesroman"
zeigen **2 von 12** Covern ein Kind. Der Trope wird über den **Titel**
transportiert (*Das geheime Baby des Milliardärs*, *Verschwiegen von
meinem Milliardärs-Boss — Ein geheimer Baby-Roman*), nicht über das Bild.
Das war für mich das überraschendste Ergebnis, und es spart Arbeit: Wir
brauchen kein Kind auf dem Cover.

**4. Die Reihenzeile steht ganz oben, klein und gesperrt.** *DIE WHITLEY
BRÜDER*, *THE CHESTER BILLIONAIRES*, *DIE VALENTI-MÄNNER — MILLIONÄR-
LIEBESROMANE*, *Seattle Single Daddies 1*. Layla Hagens „Die Whitley
Brüder" ist dieselbe Konstruktion wie unsere Reinhardt-Brüder. Das ist
kein Zufall und keine Erfindung von uns — es ist die Norm.

**5. Zwei Schriften, immer.** Eine große Versalschrift für das
Schlagwort, dazu **ein einziges Wort** in Schreibschrift oder Kursiv:
*Soulless* **CEO**, *Küss* **den CEO**, *her secret* **husband**, *Seine*
**Frau auf Zeit**. Farben: Weiß, Champagner/Gold, Silber; selten ein
Magenta-Akzent.

**6. Die Genre-Zeile steht mit auf dem Cover.** „Ein CEO-Liebesroman",
„Ein geheimer Baby-Roman", „Eine Dark Reverse Harem Romance". Klein,
unter dem Titel.

**7. Autorname unten, gesperrt, Versalien**, oft mit einer Zeile
darüber: *USA TODAY BESTSELLING AUTHOR*. Die haben wir nicht — die Zeile
bleibt leer, sie wird nicht erfunden.

### Was das für unser Cover heißt

Unser Buch spielt in der Speicherstadt, in einer Konditorei, und es ist
geschlossen erzählt. Die Nische zeigt Oberkörper vor Skyline. Zwei Wege:

**Anpassen** — Mann im Anzug, dunkel, Goldschrift. Wird gefunden, geht
in der Menge unter.

**Innerhalb der Norm abweichen** — dunkle Grundfarbe, Goldschrift,
Reihenzeile oben, Titel unten: alles wie gemessen. Aber statt Manhattan
die **Speicherstadt** — roter Backstein, grünes Brückengeländer, Fleet
mit Spiegelung in der blauen Stunde. Das ist ortsgenau, es steht so im
Buch, und „hamburg" ist bereits eines unserer Keywords.

**Empfehlung: der zweite Weg, mit Mann.** Bei 34 von 36 ist die Person
kein Stilmittel, sondern das, was in der Miniatur überhaupt erkennbar
ist. Ein Cover ohne Gesicht verzichtet auf den einzigen Blickfang, der
bei 160 Pixel Höhe noch funktioniert.

### Zwei Dinge, die kein Bildmodell erledigt

**Die Schrift nicht generieren lassen.** Bildmodelle setzen deutsche
Wörter mit Umlauten zuverlässig falsch — „MILLIARDÄRS" wird zu
Buchstabensalat. Der Ablauf ist: **Modell macht das Bild ohne jeden
Text**, die Typografie kommt danach in Canva darüber. Deshalb steht im
Prompt unten ausdrücklich, dass die unteren 40 Prozent ruhig und dunkel
bleiben müssen.

**KI-Bilder sind bei KDP offenlegungspflichtig**, genau wie KI-Text
(`../DIGITAL.md`, Abschnitt 7). Ein generiertes Cover wird im
Veröffentlichungsformular angegeben. Zusätzlich: Wenn ein Mensch
abgebildet ist, der einer realen Person ähnelt, ist das ein eigenes
Risiko — bei generierten Gesichtern gering, bei Stockfotos braucht es
eine Lizenz, die Buchcover einschließt.

---

## Prompt für das Bild (ohne Text)

Englisch, weil die Bildmodelle darauf besser reagieren. Für Nano Banana,
ChatGPT/DALL·E, Midjourney gleichermaßen brauchbar.

```
Vertical book cover artwork, aspect ratio 10:16, no text, no lettering,
no logo, no watermark.

Subject: a man in his mid-thirties, dark hair, short trimmed beard,
wearing an open dark navy wool overcoat over a white shirt with the
collar open, no tie. Chest-up portrait, his head in the upper third of
the frame. He looks directly at the camera. Serious, tired, not smiling
— a man who has worked too long.

Setting: the brick archway of a Hamburg Speicherstadt warehouse at blue
hour, just after rain. Behind him, out of focus: red-brick warehouse
facades, a green steel bridge railing, warm window light reflecting in a
narrow canal.

Light: one warm practical light low from the left. Deep shadow fills the
right third and the entire bottom of the frame.

Colour palette: near-black #0d0d0f as the dominant tone, deep warm
brick #3a2018, muted teal-blue #1c2b33, one warm gold highlight #c8a06a.

Style: photorealistic, 85mm portrait lens, shallow depth of field,
cinematic, natural skin texture, no HDR, no glossy retouching.

Composition requirement: the bottom 40 percent of the frame must stay
dark, calm and empty — it is reserved for typography.
```

**Variante B**, falls der Trope stärker sichtbar sein soll — obwohl die
Messung sagt, dass 10 von 12 darauf verzichten: denselben Prompt
verwenden und ersetzen durch

```
Setting: ... In the lit window of a small corner patisserie behind him,
out of focus, a woman's silhouette holding a small child. Very subtle,
barely readable, no faces visible in the window.
```

## Typografie danach in Canva

Format **1600 × 2560 px**, RGB, JPEG unter 50 MB.

| Element | Inhalt | Lage | Schrift |
|---|---|---|---|
| Reihenzeile | DIE REINHARDT-BRÜDER | ganz oben, zentriert | Versalien, weit gesperrt, ~28 px, `#c8a06a` |
| Titel Zeile 1 | *Sein bestgehütetes* | unteres Mitteldrittel | Schreibschrift/Kursiv, `#ffffff` |
| Titel Zeile 2 | GEHEIMNIS | direkt darunter | Versalien-Serife, sehr groß, `#ffffff` |
| Genre-Zeile | Ein Geheimes-Baby-Liebesroman | unter dem Titel | klein, gesperrt, `#c8a06a` |
| Reihennummer | BAND 1 | darunter oder oben rechts | klein, gesperrt |
| Autorname | (dein Autorenname) | unten, zentriert | Versalien, gesperrt, `#ffffff` |

**Die eine Prüfung, die man wirklich machen muss:** Das fertige Cover auf
**160 Pixel Höhe** verkleinern und aus zwei Metern Entfernung ansehen. So
kommt es auf dem Handy in der Trefferliste an. Wenn Titel oder Gesicht
dann nicht mehr lesbar sind, ist das Cover falsch — egal wie gut es in
Originalgröße aussieht. Alle 36 gemessenen Cover bestehen diesen Test;
das ist der Grund für die riesigen Versalien und die zwei Farben.

---

## Band 2: der Bruder (Stand 01.09.2026)

Das vorhandene Band-2-Cover (`cover/band2/cover.jpg`) hat den richtigen
Aufbau — Speicherstadt, Reihenzeile, Typografie sitzt —, aber der Mann
darauf ist blond und hell, während Jonas auf Band 1 dunkel, gebräunt
und bärtig ist. **Es gibt keine familiäre Ähnlichkeit.** In einer Reihe
ist das ein Fehler: Der Wiedererkennungswert der Reihe hängt in der
Miniatur an genau zwei Dingen — der Typografie und dem Gesicht.

Ziel für Band 2: **derselbe Mann-Typ wie Band 1, erkennbar als Bruder,
mit leichten Abweichungen.** Theo ist der jüngere (geboren August 1990,
Architekt), also etwas jünger und eine Spur weniger hart als Jonas.

### Prompt (ohne Text, wie immer)

```
Vertical book cover artwork, aspect ratio 10:16, no text, no lettering,
no logo, no watermark.

Subject: a man in his mid-thirties, unmistakably the younger brother of
a slightly older man with the same family face — dark brown hair combed
back off the forehead, strong straight eyebrows, deep-set grey-blue
eyes, straight nose, defined square jaw, short dark stubble beard along
the jawline. Slightly younger and a shade less hard than his elder
brother: the hair a little less severely slicked, a few strands loose at
the temple. He wears a charcoal wool overcoat over a white shirt, collar
open, no tie. Chest-up portrait, his head in the upper third of the
frame, shoulders squared to camera, looking directly into the lens.
Serious, tired, not smiling — a man who has worked too long and is
holding something back.

Setting: the Hamburg Speicherstadt at blue hour just after rain. Far
behind him and thrown well out of focus: red-brick warehouse facades, a
green steel bridge, warm window light reflecting in a narrow canal,
scattered bokeh street lamps.

Light: a cool teal rim light along the right side of his face and hair,
one warm practical light low from the left, deep shadow filling the
right third and the entire bottom of the frame.

Colour palette: near-black #0d0d0f dominant, deep warm brick #3a2018,
muted teal-blue #1c2b33, one warm gold highlight #c8a06a. Cinematic
night-city colour grade.

Style: photorealistic, 85mm portrait lens, shallow depth of field,
natural skin texture and pores, no HDR, no glossy retouching, no beauty
filter.

Composition requirement: the bottom 40 percent of the frame must stay
dark, calm and empty — it is reserved for typography.
```

**Besser noch, wenn das Werkzeug Referenzbilder kann** (Nano Banana,
GPT-Image, Flux Kontext): `cover/roh/newyork2.jpg` als Referenz
mitgeben und dazuschreiben *„the younger brother of the man in the
reference image, same face family, same colour grade"*. Das trifft die
Ähnlichkeit zuverlässiger als jede Beschreibung.

### Danach

Bild als `cover/roh/theo.jpg` ablegen, dann:

```
python3 scripts/coverbau.py --bild cover/roh/theo.jpg \
    --titel-script "Was er nie" --titel-caps "GEFRAGT HAT" \
    --genre "Geheime Ehe · Familiengeheimnis" --band "BAND 2" \
    --autor "Jule Norden" --ordner cover/band2
```

`coverbau.py` setzt die Typografie, misst den Titelkontrast gegen das
Ziel von 7,0 und legt die Miniaturprobe daneben. **Die Miniaturprobe
ist der eigentliche Test** — in der Trefferliste ist das Cover 160
Pixel hoch.

### Warum das hier steht und nicht erledigt ist

Diese Arbeitsumgebung erreicht nur GitHub, PyPI und npm. Der
Cloudinary-Zugang hat für Bilderzeugung keine Freigabe
(`invalid scope`, auch beim Standardmodell), Canva ist nicht
autorisiert. **Das Bild kann in einer Sitzung hier nicht erzeugt
werden.** Der Prompt steht deshalb hier, damit er nicht in einem
Chatverlauf verlorengeht.
