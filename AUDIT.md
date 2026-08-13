# HOMEEINS — Business Audit

Stand 10.08.2026 · alle Zahlen in diesem Dokument sind entweder **gemessen**
(Quelle genannt) oder als **EINSCHÄTZUNG** markiert. Nichts geschätzt und
als Tatsache verkauft.

---

## 0. Die Lage in fünf Zahlen

| | | Quelle |
|---|---|---|
| Bestellungen insgesamt | **7** | Shopify `ordersCount` |
| Letzte Bestellung | **17.12.2025** — vor 8 Monaten | Shopify `orders` |
| Bestellungen 2026 | **0** | Shopify |
| Google-Klicks / 28 Tage | **0** (bei 230 Impressionen) | Search Console |
| Abgebrochene Warenkörbe | **0** | Shopify |

**Keine abgebrochenen Warenkörbe bei null Klicks heißt: Es kommt niemand
an.** Der Kaufweg funktioniert (Kaufprobe bis zur Kasse durchgelaufen).
Das ist kein Conversion-Problem — es ist ein Nachfrage- und
Sichtbarkeitsproblem.

---

## 1. Unit Economics

**FAKT:** Aufschlag Faktor 2,5 (`MARGE.md`), Kleinunternehmer § 19 UStG →
0 % Umsatzsteuer. AOV der 7 echten Bestellungen: **68,92 €**.

**EINSCHÄTZUNG:** Zahlungsgebühr 1,9 % + 0,25 €, Retourenquote 5 %.

| Position | IST-AOV 68,92 € |
|---|---:|
| Einkauf + Fracht | −27,57 € |
| Zahlungsgebühr *(S)* | −1,56 € |
| Retouren *(S)* | −3,45 € |
| **Deckungsbeitrag** | **36,35 €** |
| Bruttomarge | 53 % |
| **Break-even ROAS** | **1,90** |
| **Maximaler CPA** | **36,35 €** |

Skalierung (Deckungsbeitrag vor Werbung und Fixkosten):

| Bestellungen | pro Monat |
|---|---:|
| 10 / Tag | 10.904 € |
| 30 / Tag | 32.711 € |
| 100 / Tag | 109.037 € |

**Bewertung: Die Rechnung ist nicht das Problem.** 53 % Bruttomarge und
Break-even-ROAS 1,90 sind für Wohnaccessoires normal bis gut.

**Korrektur einer früheren Aussage von mir:** Ich hatte gesagt, bezahlte
Werbung könne bei diesen Margen nicht funktionieren. Das war zu absolut.
Bei 36 € maximalem CPA gilt:

| Conversion Rate | maximaler Klickpreis |
|---|---:|
| 1 % | 0,36 € |
| **2 %** | **0,72 €** |
| 3 % | 1,09 € |

Bei 2 % Conversion und 0,70 € Klickpreis geht es **knapp** auf. Bei 1 %
nicht. **Die Conversion Rate ist unbekannt** — es gibt keinen Verkehr, um
sie zu messen. Werbung ist damit ein Test mit echtem Verlustrisiko, nicht
eine Rechnung, die aufgeht.

---

## A. Die 10 größten Probleme

| # | Problem | Beleg | Schwere |
|---|---|---|---|
| **1** | **GPSR-Pflichtangaben fehlen noch auf den Produkten.** Die EU-verantwortliche Person ist geklärt (12.08.2026: Alan Lorenz GbR selbst), aber 0 von 5 geprüften Produkten tragen Name/Anschrift, Herstellerangabe oder Warnhinweise. Ohne diese Angaben **auf jedem Artikel** bleibt die Ware **nicht verkehrsfähig** — die Klärung der Person allein reicht nicht. Bußgeld bis 100.000 €, Abmahnrisiko, Marktplätze löschen Angebote. | Shopify-Metafelder, GPSR Art. 16 | **existenziell** |
| **2** | **Null Verkehr.** 0 Klicks in 28 Tagen. | Search Console | existenziell |
| 3 | **Die einzigen Produkte, die je verkauft wurden, sind nicht mehr aktiv.** Alle 7 Bestellungen betrafen Deko-Kleinteile (Kerzenhalter, Kissen, Marmor-Box, Teppich) für 30–130 €. Keines dieser Produkte ist heute aktiv. | Shopify `orders` + Produktabfrage | hoch |
| 4 | **Bauchladen.** 101 aktive Produkte über 8+ Kategorien: Hundebetten, Bürostühle, Kettensägen-Ketten, Dartscheiben, Kunstpalmen, Wimpernlifting-Sets. Kein Grund, sich den Shop zu merken. | Sortimentsabfrage | hoch |
| 5 | **45 von 146 Produkten sind Entwürfe** — Arbeit investiert, nichts davon verkäuflich. | Shopify | mittel |
| 6 | **Judge.me liefert weiter `aggregateRating`** auf `samt-sessel`, obwohl die erfundenen Bewertungen gelöscht sind. Google zeigt Sterne ohne Käufer — Verstoß gegen Anhang zu § 3 Abs. 3 Nr. 23b UWG. | Prüfstand | hoch (rechtlich) |
| 7 | **Englische Seiten ranken mit kaputten Titeln.** `/en/products/washing-machine-cabinet-70-5x25-washing-machine-cabinet-70-5x25-…` steht auf Platz 1,1. | Search Console | mittel |
| 8 | **Deine Sichtbarkeit ist Namensverwechslung.** Top-Suchanfragen: „möbel eins", „möbel-eins unterneukirchen", „tierwagen", „tischkicker klappbar". „Möbel Eins" ist ein anderer Händler. | Search Console | mittel |
| 9 | **12 Verkaufskanäle, keiner liefert.** Amazon (CedCommerce), Microsoft, TikTok, Pinterest, Instagram Shop-AI, Google, Facebook, Inbox, Shop, Collective. Teils kostenpflichtig. | Shopify `publications` | mittel |
| 10 | **Praxis-Note 58 auf 30 von 34 Seiten**, Währungsformat `€{{amount}}` statt `{{amount}} €`. | Gesamtscan, Theme-Einstellungen | niedrig |

---

## B. Die 10 größten Chancen

| # | Chance | Beleg |
|---|---|---|
| **1** | **10 Seiten stehen auf Platz 1–5 und bekommen null Klicks.** Ranking ist da, Klick fehlt → Snippet-Problem. Billigster denkbarer Verkehr. | Search Console |
| **2** | **eBay.** Verkehr existiert dort. Gebühr 11 % + 0,35 €, Dropshipping vom Großhändler erlaubt. Keine Werbekosten. | eBay-Recherche |
| **3** | **Saisonfenster steht offen.** Hundebett, Bürostuhl, Kratzbaum, Hocker haben ihr Nachfragehoch **November bis Januar**. Heute ist August. | TRENDS.md |
| 4 | **Hundemöbel sind der einzige zusammenhängende Bereich mit belegter Nachfrage** (Index 69, +15 %) und tiefem Sortiment (7 Modelle). | TRENDS.md, Sortiment |
| 5 | **Schreibtischstuhl +43 % Trend**, 570 Stück Bestand, 78 € Deckungsbeitrag. | TRENDS.md, Shopify |
| 6 | **Hocker/Schuhbank +107 % Trend** — der stärkste Anstieg im ganzen Datensatz. | TRENDS.md |
| 7 | **17 fertige Reels liegen unbenutzt.** Produktionskosten null (FFmpeg auf dem Runner). | Repository |
| 8 | **Deutsches Lager, 3–5 Tage Lieferzeit.** Voraussetzung für Marktplätze — hast du. | CJ-Daten |
| 9 | **Break-even-ROAS 1,90.** Wenn die Conversion Rate 2 % erreicht, ist Werbung tragfähig. | Rechnung oben |
| 10 | **45 Entwürfe:** darunter kann Brauchbares sein, das nur nie fertig wurde. | Shopify |

---

## C. Die 5 Produkte mit dem höchsten Potenzial

Bewertet nach **gemessener Nachfrage × Trend × Deckungsbeitrag**,
gefiltert auf echten Bestand. Details in `EBAY-START.md`.

| # | Produkt | Nachfrage | Trend | Hoch im | Bestand | DB | Score |
|---|---|---:|---:|---|---:|---:|---:|
| 1 | Schreibtischstuhl 135° | 62 | **+43 %** | Nov | 570 | 78 € | 69 |
| 2 | Hundesofa 90 cm Kunstleder | 69 | +15 % | Nov | 157 | 80 € | 64 |
| 3 | Hundebett 70 cm Samt | 69 | +15 % | Nov | 233 | 57 € | 45 |
| 4 | Schuhbank 102 cm | 31 | **+107 %** | Jan | 195 | 59 € | 38 |
| 5 | Kratzbaum kompakt | 38 | +19 % | Dez | 174 | 27 € | 12 |

**EINSCHÄTZUNG, ausdrücklich als solche:** Der vollständige 16-Faktoren-
Score aus deinem Auftrag (Viralität, Retourenrisiko, Branding-Potenzial …)
ist mit den vorhandenen Daten nicht seriös berechenbar. Was ich habe, sind
vier harte Faktoren. Die anderen zwölf wären geraten — und geratene
Punktzahlen sehen wie Wissen aus, ohne welches zu sein.

---

## D. Die 10 Maßnahmen mit dem höchsten ROI

| Prio | Maßnahme | Nutzen | Aufwand | Kosten | Risiko |
|---|---|---|---|---|---|
| 🔥 **P0** | **GPSR-Pflichtangaben je Produkt eintragen.** Verantwortliche Person steht fest (Alan Lorenz GbR), jetzt Name/Anschrift + Herstellerdaten in die Metafelder aller 146 Produkte. | verhindert Bußgeld bis 100.000 € und Marktplatz-Sperren | Metafelder, alle Produkte | 0 € | — |
| 🔥 **P0** | **Judge.me `aggregateRating` entfernen.** Sterne ohne Käufer, nur in der App löschbar. | beseitigt Abmahnrisiko | 15 Min | 0 € | — |
| 🟢 **P1** | **Snippets der 10 Seiten auf Platz 1–5 überarbeiten.** Title + Description je Seite. | einziger Verkehr, der ohne Geld kommt | 2–3 h | 0 € | keins |
| 🟢 **P1** | **Englische `/en/`-Seiten prüfen:** Titel reparieren oder Seiten aus dem Index nehmen. | stoppt Verschwendung guter Rankings | 1–2 h | 0 € | niedrig |
| 🟢 **P1** | **eBay: 5 Angebote einstellen** (nach P0). Texte fertig in `EBAY-START.md`. | 25–28 Verkäufe = 1.000 € | 2–3 h | nur Provision | niedrig |
| 🟡 **P2** | **Sortiment halbieren.** 101 aktive → ~40 in 2–3 Bereichen. | Fokus, weniger Pflege, klarere Marke | 3–4 h | 0 € | mittel |
| 🟡 **P2** | **12 Verkaufskanäle durchsehen**, kostenpflichtige ohne Umsatz kündigen. | gespartes Geld | 1 h | 0 € | keins |
| 🟡 **P2** | **Deko-Kleinteile zurückholen** — die einzige Kategorie mit echten Verkäufen. | testet ein belegtes Signal | 2 h | 0 € | niedrig |
| ⚪ **P3** | Währungsformat, Praxis-Note 58, Reels veröffentlichen | Kosmetik und Reichweite | je 1 h | 0 € | keins |

**Bewusst nicht in dieser Liste:** Meta Ads, Google Shopping, TikTok Ads,
UGC, E-Mail-Marketing, A/B-Tests. Begründung unter Punkt F.

---

## E. 30-Tage-Plan

**Woche 1 — Blockaden lösen**
- Erledigt (12.08.2026): Neutralversand von CJ bestätigt, EU-verantwortliche Person geklärt (Alan Lorenz GbR selbst)
- Tag 1: GPSR-Angaben (Name, Anschrift, Herstellerdaten) in die Produkt-Metafelder eintragen — mindestens für die 5 eBay-Kandidaten aus `EBAY-START.md`, danach den Rest
- Tag 1: Judge.me-Bewertungen in der App löschen
- Tag 2–3: Snippets der 10 rankenden Seiten neu schreiben
- Tag 4–5: englische Seiten entscheiden — reparieren oder auslisten

**Woche 2 — eBay**
- Gewerbliches eBay-Konto
- Marketplace Connect installieren (kostenlos bis 50 Bestellungen/Monat)
- 5 Angebote aus `EBAY-START.md`, **erst nachdem die GPSR-Angaben auf diesen 5 Produkten stehen**

**Woche 3 — aufräumen**
- Sortiment auf 2–3 Bereiche verdichten
- Verkaufskanäle prüfen, Kostenfresser kündigen
- 45 Entwürfe: fertigstellen oder löschen

**Woche 4 — messen**
- eBay: welche Angebote wurden angesehen, welche verkauft?
- Search Console: haben die neuen Snippets Klicks gebracht?
- Entscheidung: verdoppeln, drehen oder abbrechen

---

## F. Der Weg zu 1.000 € Gewinn/Monat

Rückwärts gerechnet, mit gemessenem Deckungsbeitrag von 36,35 €:

| Schritt | Zahl |
|---|---|
| Zielgewinn | 1.000 €/Monat |
| Deckungsbeitrag je Bestellung | 36,35 € |
| **Benötigte Bestellungen** | **28 / Monat** ≈ 1 pro Tag |

Und dann trennen sich die Wege:

### Weg 1 — eBay (empfohlen)

| | |
|---|---|
| Nach eBay-Gebühr (11 % + 0,35 €) bleiben | ~36 € |
| Benötigte Verkäufe | **28 / Monat** |
| Werbebudget | **0 €** |
| Verkehr | ist dort schon |
| Blockade | GPSR-Angaben je Produkt (Verantwortliche Person und Neutralversand sind seit 12.08.2026 geklärt) |

### Weg 2 — eigener Shop mit Werbung

| | |
|---|---|
| Benötigte Bestellungen | 28 |
| Bei 2 % Conversion → Besucher | **1.400 / Monat** |
| Bei 0,70 € Klickpreis *(S)* | **980 € Werbekosten** für 1.018 € DB |
| Ergebnis | **±0** |
| Bei 1 % Conversion | **−960 € Verlust** |

**Die Conversion Rate ist unbekannt.** Weg 2 ist eine Wette darauf, dass
sie ≥ 2 % liegt. Bei einem Shop ohne Bewertungen, ohne Marke und mit
101 zusammenhanglosen Produkten halte ich 1 % für wahrscheinlicher als
2 % — **das ist eine Einschätzung, keine Messung.**

### Weg 3 — organischer Verkehr

1.400 Besucher/Monat aus Google sind erreichbar, brauchen aber
**6–12 Monate** und einen Grund, warum Google dich vor anderen zeigt.
Kostet Zeit statt Geld. Als Ergänzung sinnvoll, als einziger Weg zu
langsam für „1.000 € im Monat".

**Empfehlung: Weg 1 zuerst, Weg 3 parallel nebenher, Weg 2 erst wenn eBay
eine echte Conversion Rate geliefert hat.** eBay-Verkäufe zeigen dir, ob
die Produkte gewollt werden — diese Information ist die Voraussetzung
dafür, Werbegeld nicht zu verbrennen.

---

## G. Langfristig: 3.000–5.000 €/Monat

Bei gleichem Deckungsbeitrag: **83–140 Bestellungen/Monat**, also 3–5 pro
Tag. Das geht nicht mit demselben Sortiment auf demselben Weg.

**Stufe 1 — Gewinnerprodukt finden (Monat 1–3)**
eBay als Messgerät. Ziel ist nicht Umsatz, sondern die Antwort: welches
Produkt kaufen Leute wirklich?

**Stufe 2 — vertiefen statt verbreitern (Monat 3–6)**
Aus einem Gewinner werden 10 Varianten, nicht 10 neue Kategorien. Bei
Hundemöbeln: Größen, Materialien, Zubehör. Wiederkäufe entstehen erst,
wenn ein Kunde einen Grund hat, wiederzukommen.

**Stufe 3 — Marke aufbauen (Monat 6–12)**
Eigene Verpackung, eigene Fotos, EU-Lager mit kürzerer Lieferzeit. Ab
hier wird ein Preis über dem Marktplatzniveau durchsetzbar.

**Stufe 4 — Private Label (ab Monat 12)**
Erst wenn ein Produkt belegbar läuft. Vorher ist es Kapital in einem
Lager, das niemand nachgefragt hat.

**Der Ehrlichkeit halber:** 80–90 % der Dropshipping-Shops scheitern, nur
1,5 % kommen über 50.000 $ Monatsumsatz. Du bist seit drei Jahren dabei
und hast 7 Bestellungen. Der Sprung auf 5.000 € Gewinn ist kein
Ausbauschritt, sondern ein anderes Geschäft.

---

## Was ich NICHT geprüft habe

Damit du nicht denkst, das hier sei vollständig:

| Lücke | Warum |
|---|---|
| **Konkurrenzanalyse** | Keine konkreten Wettbewerber untersucht. Braucht Namen — von dir oder aus einer Suchanalyse. |
| **Echte Klickpreise** | Ahrefs: „Insufficient plan". Semrush: API-Einheiten aufgebraucht. Die 0,70 € sind Schätzung. |
| **Meta-/TikTok-Kosten für diese Nische** | Nicht recherchiert. |
| **Verpackungsgesetz / LUCID** | Nicht geprüft. Für Versandhandel in Deutschland relevant — vermutlich eine weitere offene Pflicht. |
| **Alle 146 Produkte auf GPSR** | 5 geprüft, 5-mal negativ. Der Rest ist wahrscheinlich, aber nicht gemessen. |

---

## Was machen wir heute, diese Woche, und was gar nicht?

### Heute — geklärt, jetzt eintragen

**CJ hat geantwortet** (12.08.2026): Versand ist immer neutral, kein
CJ-Absender auf dem Paket. Und die EU-verantwortliche Person nach GPSR
Art. 16 ist Alan Lorenz GbR selbst — keine externe Zusage nötig, aber
damit auch keine Abkürzung: Name, Anschrift und Herstellerdaten müssen
jetzt tatsächlich auf jedem Produkt stehen, nicht nur feststehen, wer
sie liefert.

**Nächster Schritt:** Metafelder für die 5 eBay-Kandidaten aus
`EBAY-START.md` ausfüllen, dann für den Rest des Katalogs.

**Und in der Judge.me-App** die erfundenen Bewertungen löschen.

### Diese Woche

Snippets der 10 rankenden Seiten überarbeiten. Kostet nichts, kann nichts
kaputtmachen, und ist der einzige Verkehr, der ohne Geld kommt.

### Was wir komplett lassen

- **Meta Ads, Google Shopping, TikTok Ads** — solange die Conversion Rate unbekannt ist, ist jedes Werbebudget ein Blindflug. Erst eBay, dann Zahlen, dann Werbung.
- **SkyReels und KI-Videoproduktion** — du hast 17 unbenutzte Reels. Das Problem ist nicht die Produktion.
- **Neue Produkte suchen** — 101 aktive und 45 Entwürfe reichen. Mehr Sortiment ist keine Antwort auf null Verkehr.
- **UGC, E-Mail-Marketing, A/B-Tests, Wiederkauf-Programme** — alle brauchen Kunden. Du hast sieben, den letzten vor acht Monaten.

**Der eine Satz:** Nicht mehr bauen, bevor nicht einmal etwas verkauft
wurde. Der nächste Meilenstein ist **eine Bestellung**, nicht 1.000 €.

---

## Nachtrag 13.08.2026 — was sich seit dem letzten Audit geändert hat

Drei Tage, sieben echte Entwicklungen. Wieder: **gemessen**, wo eine
Quelle steht, **EINSCHÄTZUNG**, wo nicht.

**1. Ein neues Produkt ist live und bricht mit dem eigenen Plan.**
Die LED-Taschenlampe (`led-taschenlampe-aufladbar-zoom-warnlicht`) wurde
heute nicht über eBay getestet, sondern direkt im eigenen Shop
veröffentlicht — entgegen der Empfehlung unter Punkt F ("erst eBay,
dann Zahlen, dann eigener Shop"). Sie kam über dieselbe
Trends×Bestand-Methode wie die eBay-Kandidaten zustande, mit einem
Unterschied: Sie ist die einzige Nische im ganzen Datensatz, deren
CJ-Bestand an **drei getrennten Tagen** (9., 10., 13.08.) exakt
identisch war — 11 von 11 SKUs, keine Abweichung. Das ist der
verlässlichste Lieferantenbeleg, den dieses Projekt bisher hatte.
**EINSCHÄTZUNG:** Ob der Bruch mit "erst eBay" richtig war, zeigt sich
erst an echten Bestellungen — bisher: 0, wie bei den 146 anderen.

| | Wert | Quelle |
|---|---:|---|
| Einkauf (CJ, inkl. Versand) | 9,27–12,04 € | `daten/produkte-roh.json` |
| Verkaufspreis | 29,99 € / 39,99 € | Shopify |
| Deckungsbeitrag | ~21–28 € | Rechnung |
| GPSR-Angaben | **vorhanden** | live geprüft |
| Bewertungen | ~~5 Sterne, 0 Bewertungen~~ → behoben (App deaktiviert) | live geprüft |

**2. Dasselbe Judge.me-Problem wächst mit jedem neuen Produkt — behoben.**
Die Taschenlampe zeigte fünf volle Sterne ohne eine einzige Bewertung —
identisch zum bereits bekannten Fall auf `samt-sessel`, also kein
Einzelfall mehr, sondern systematisches Verhalten der App bei jedem neu
angelegten Produkt. **Update 13.08.2026:** Judge.me wurde deaktiviert.
Live geprüft — keine Sterne mehr sichtbar, stattdessen ein neutraler
"Be the first to write a review"-Hinweis (auf Englisch, siehe P3 unten).

**3. CJs deutsches Lager ist instabiler als angenommen.** Kommode und
Couchtisch — beide am 10.08. mit echten SKUs und Bestand bestätigt —
sind am 13.08. bei direkter Einzelabfrage "removed from shelves". Bei
Bürostuhl fiel die Trefferzahl im selben Zeitraum von 8 auf 2 SKUs. Das
bedeutet: **eine einmalige Bestandsprüfung reicht bei diesem Lieferanten
nicht** — vor jeder Einkaufsentscheidung erneut prüfen, nicht auf einen
Stand von vor mehreren Tagen verlassen.

**4. Erweiterte Nischensuche (Küche, Schlafzimmer, Büro-Technik, Heim-
fitness) — größtenteils ergebnislos, aber ein echter Fund dabei.**
Faszienrolle hat mit 83,2 den höchsten Nachfragewert aller 49 je
gemessenen Begriffe in diesem Projekt — über 20 % mehr als der
bisherige Spitzenreiter. Bei CJ nicht auffindbar (weder "foam roller"
noch "fascia roller" liefern echte Treffer). **Offen, nicht erledigt:**
Das ist die stärkste unbediente Nachfrage im ganzen Datensatz — ein Blick
direkt auf cjdropshipping.com (Mensch, wegen Captcha) könnte lohnen,
bevor die Sache liegen bleibt.

**5. `PRODUKTBILDER.md` — neue Dauerhaft-Referenz.** Recherche zu
Produktbildern, die messbar besser verkaufen, direkt an der
Taschenlampe erprobt: Freisteller-Bild ergänzt, alle Detailbilder von
Englisch auf Deutsch, Dateigröße von bis zu 1,2 MB auf unter 150 KB
komprimiert. Für alle 145 übrigen Produkte noch nicht gemacht — die
meisten haben vermutlich weder Freisteller noch Maßstabsbild, das ist
aber **nicht geprüft**, nur naheliegend.

**6. Neue Werkzeuge, direkt einsetzbar:**
- `scripts/zoomprobe.py` — misst echten Pinch-/Tap-Zoom auf dem Handy, nicht nur ob die Seite lädt
- `scripts/produktdaten.py --bildgroessen` — echte Pixelmaße von CJ-Bildern vor dem Einkauf
- OpenRouter-Websuche und Bildbearbeitung (`scripts/openrouter.py`) — u. a. für die Bildübersetzung genutzt
- Claude-Code-SessionStart-Hook — künftige Sitzungen starten mit allen nötigen Paketen bereits installiert

**7. Der "Vertrag widerrufen"-Button ist kein Fehler.** Kurz als
mögliches Bug-Risiko markiert, dann aufgeklärt: Er gehört zur App
"Revoq" (EU-Widerrufsrecht-Erweiterung), ist rechtlich nicht
vorgeschrieben, aber ein legitimes Vertrauens-Feature. Kein
Handlungsbedarf.

### Was das für die Prioritätenliste (Punkt D) ändert

Nichts an der Reihenfolge — GPSR bleibt P0 für die **145 anderen**
Produkte. Aber jetzt gibt es dafür eine funktionierende Vorlage: Die
Taschenlampe zeigt exakt, wie die Pflichtangaben aussehen müssen. Neu
dazu, beide 🔥 P0 wegen wachsendem Schaden bei jedem neuen Produkt:

| Prio | Maßnahme | Beleg |
|---|---|---|
| ✅ erledigt | ~~Judge.me-Sterne-Anzeige grundsätzlich prüfen/abstellen~~ — App am 13.08.2026 deaktiviert, live geprüft: keine Sterne mehr auf der Taschenlampen-Seite, stattdessen neutrales "Be the first to write a review" | Frisches Foto, `bilder/products-led-taschenlampe-…-mobil.jpg` |
| 🟢 P1 | CJ-Bestand vor jedem Einkauf frisch prüfen, nicht auf alte Daten verlassen | Kommode/Couchtisch-Fund |
| 🟡 P2 | Faszienrolle manuell bei CJ nachsehen (Mensch, wegen Captcha) | höchste gemessene Nachfrage im Datensatz |
| 🟡 P2 | Bilder der übrigen 145 Produkte gegen `PRODUKTBILDER.md`-Checkliste prüfen | bisher nur 1 von 146 geprüft |
| ⚪ P3 | Judge.me-Deaktivierung hat den Bewertungsblock auf Englisch zurückgesetzt ("Customer Reviews / Be the first to write a review") statt Deutsch — kurz prüfen, ob das so gewollt ist oder ein Theme-Text nachgestellt werden muss | live beobachtet, 13.08.2026 |
