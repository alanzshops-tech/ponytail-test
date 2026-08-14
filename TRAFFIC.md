# Traffic — alle Wege, priorisiert

Stand 13.08.2026 · externe Recherche (Websuche), FAKT von EINSCHÄTZUNG
getrennt wie im Master-Prompt gefordert. Ausgangslage bleibt die aus
`AUDIT.md`: 0 Klicks in 28 Tagen, 0 Bestellungen 2026, kein Werbebudget
im Einsatz.

## Nachtrag 13./14.08.2026 (nachts) — technische Traffic-Grundlagen

Zweite Recherche-Runde, diesmal zu technischen Grundlagen statt
Content-Kanälen. Vier Funde, zwei davon direkt behoben:

1. **Sitemap war nie eingereicht.** 🔥 Wahrscheinlich der größte
   Einzelhebel der ganzen Recherche — siehe `AUDIT.md` P0. Braucht
   einen Menschen (2 Minuten), automatisches Einreichen scheiterte
   absichtlich an fehlender Schreibberechtigung.
2. **Vertriebskanäle (Google Shopping, Bing, Amazon, TikTok, Pinterest)
   sind längst verbunden**, nicht wie ursprünglich angenommen neu
   einzurichten. Details: `VERTRIEBSKANAELE.md`.
3. **GTIN-Kennzeichnung fehlte auf allen 101 aktiven Produkten** —
   behoben (`mm-google-shopping.custom_product = true` gesetzt). Könnte
   die Sichtbarkeit im Google-Shopping-Feed verbessern, unbelegt bis
   zur Prüfung im Merchant-Center-Dashboard selbst.
4. **Praxis-Note 58 (Lighthouse Best Practices) war seit Tagen
   ungeklärt** — Ursache jetzt belegt (`GESAMTSCAN.md`): veraltete
   APIs, Third-Party-Cookies, DevTools-Issues auf allen 34 Seiten.
   Vermutlich Tracking-Skripte, nicht ohne Weiteres behebbar ohne
   Marketing-Funktionalität zu verlieren. Die Tempo-Note (Performance)
   hat konkretere Ansatzpunkte: ungenutztes JavaScript und
   render-blockierende Anfragen auf allen 34 Seiten.

5. **Product-Schema war unvollständig — jetzt behoben, in einer
   unveröffentlichten Theme-Kopie, bereit zur Freigabe (13./14.08.2026
   nachts).** `scripts/schemaprobe.py` gegen zwei echte Produktseiten
   zeigte: Dawn liefert `sku`, `offers` (Preis/Verfügbarkeit/Währung)
   und `image`, aber **kein** `brand`, `gtin`, `aggregateRating`,
   `review` oder `description` im JSON-LD-Block. Passt exakt zur
   Recherche ("Stores relying solely on default schema miss out on
   60–70% of available rich snippet opportunities").

   **Umsetzung:** Auf ausdrückliche Freigabe hin (CLAUDE.md Regel 1
   für diesen einen Fall bewusst aufgehoben) ein `custom_liquid`-Block
   mit ergänzendem Product-Schema (`brand`, `mpn` = `sku`,
   `description`) in einer **Kopie** des Live-Themes ergänzt — Dawns
   eigene `sections/main-product.liquid` (Regel 2) blieb unangetastet,
   das Werkzeug selbst verweigert Schreibzugriffe aufs Live-Theme
   ohnehin serverseitig. Gegen die Vorschau-URL erneut mit
   `schemaprobe.py` geprüft: `brand`/`mpn`/`description` jetzt ✅,
   `aggregateRating`/`review`/`gtin` bewusst weiterhin ❌ (Judge.me-
   Bewertungslage ungeklärt, kein echtes GTIN vorhanden). Theme:
   „Schema-Ergänzung (Claude, 13.08.2026 nachts) – zur Freigabe",
   `gid://shopify/OnlineStoreTheme/182683926851` — **veröffentlicht**
   (14.08.2026, vom Nutzer selbst im Adminbereich). Per `graphql_query`
   bestätigt: das Theme steht jetzt auf `role: MAIN`. Live-Verifizierung
   gegen die echte Produkt-URL (ohne `preview_theme_id`) läuft.

6. **Interne Verlinkung der 4 Ratgeber ergänzt (14.08.2026).** Alle vier
   waren nur über Pinterest/direkt erreichbar, keine Kollektionsseite
   verlinkte auf sie — ein einfacher, oft übersehener SEO-Hebel
   (interne Links geben Google zusätzliches Gewicht). Ergänzt:
   `hunde` → beide Hundebett-Ratgeber, `haustiere` → Kratzbaum-Ratgeber,
   `mobel-1` → Bürostuhl-Ratgeber. Jeweils nur ein Absatz angehängt,
   nichts Bestehendes ersetzt.

   **Dabei ein Fehler passiert und sofort korrigiert:** Beim ersten
   Versuch eine falsche, veraltete Collection-ID aus einer viel
   früheren Abfrage wiederverwendet — das hat kurz die
   `haustiere`-Beschreibung mit dem `hunde`-Text überschrieben. Beim
   Lesen der Antwort bemerkt (Handle stimmte nicht), sofort mit dem
   ursprünglichen Text zurückgeschrieben, dann die echte `hunde`-ID neu
   abgefragt statt geraten. Für die restlichen zwei Kollektionen wurden
   beide IDs vorher frisch abgefragt.

Diese sechs Funde ändern **nichts** an der Kanal-Priorisierung unten
(Reels/Pinterest/Ratgeber) — sie sind eine Ebene darunter: Ob die
Kanäle überhaupt technisch sauber funktionieren, bevor mehr Content
draufgepackt wird.

**Der Rahmen, bevor die Liste kommt:** Zwei Wege verlangen kein Geld und
haben schon fertige Vorarbeit — die sollten zuerst laufen, bevor über
Instagram-Content-Pläne oder Pinterest-Boards nachgedacht wird, die bei
null anfangen müssten.

---

## 🔥 P0 — kostet nichts, ist schon fast fertig

### 1. Die 10 Seiten, die schon auf Platz 1–5 stehen, aber 0 Klicks bekommen

**FAKT** (Search Console, bereits in `AUDIT.md` Chance #1): Ranking ist
da, Klick fehlt. Das ist der billigste Traffic, den es geben kann —
er kostet nur bessere Title-Tags und Meta-Descriptions, keine neue
Reichweite, kein neuer Content.

**FAKT** (SEOsherpa/BigCommerce-Recherche): Organische Suche macht im
E-Commerce durchschnittlich 23,6 % aller Bestellungen und 53,3 % des
gesamten Website-Traffics aus — mit einem durchschnittlichen Return von
22 $ je investiertem 1 $, ohne laufende Werbekosten.
[SEOsherpa](https://seosherpa.com/ecommerce-seo-statistics/)

**Aufwand:** 2–3 Stunden (steht schon so in `AUDIT.md` Punkt D).
**Status:** noch offen — nicht in dieser Sitzung erledigt.

### 2. 17 fertige Reels veröffentlichen

**Korrektur, noch am 13.08.2026 nachgetragen — dieser Punkt war falsch:**
Beim Prüfen über Metricool (`mcp__Metricool__getScheduledPosts`) hat sich
gezeigt, dass bereits ein aktiver Kalender läuft und ein Großteil der
Reels längst auf TikTok/YouTube Shorts eingeplant oder veröffentlicht ist.
Details, Belege und was tatsächlich noch fehlt: `SOCIAL.md`. Es sind
außerdem 19 statt 17 Reels (drei Produkte kamen am 9.8. nach der ersten
Zählung dazu).

~~**FAKT** (Repository, `reels.config.json` / `.github/workflows/reels.yml`):
17 vertikale 9:16-Reels liegen fertig gerendert, Produktionskosten
bereits bezahlt (FFmpeg auf dem GitHub-Runner, kein laufendes Abo).
Bisher: nicht veröffentlicht.~~ — falsch, siehe Korrektur oben.

**FAKT** (Social Insider / Dash Social-Recherche): Organische Reichweite
auf TikTok erreicht 10–30 % (gegenüber 2–5 % auf Instagram), der
Algorithmus bevorzugt Geschäftskonten nicht schlechter als private, und
gute Inhalte können unabhängig von der Followerzahl viral gehen.
[Social Insider](https://www.socialinsider.io/blog/organic-tiktok-growth/)

**Aufwand:** Hochladen auf TikTok, Instagram Reels, YouTube Shorts —
selbes Video, drei Plätze. Wenige Stunden für alle 17.
**Kosten:** 0 €. **Risiko:** keins — der Content existiert bereits.

**Korrektur einer früheren Einschätzung von mir:** Ich hatte SkyReels/
KI-Videoproduktion in `AUDIT.md` als "lassen wir komplett" eingestuft,
weil die Produktion nicht das Problem sei. Das bleibt richtig — aber es
heißt nicht, dass die *Veröffentlichung* der vorhandenen 17 Reels warten
sollte. Das ist ein eigener, offener P0-Punkt, den ich vorher nicht klar
genug herausgestellt hatte.

---

## 🟢 P1 — echte Arbeit, aber mit belegtem Hebel

### 3. Pinterest — läuft bereits, siehe Korrektur

**Korrektur, noch am 13.08.2026 nachgetragen — "neu aufbauen" war falsch:**
Pinterest ist über Metricool bereits aktiv, mit eigenem Board und
mehreren veröffentlichten Pins. Details: `SOCIAL.md`. Die Einschätzung
unten (warum Pinterest inhaltlich passt) bleibt richtig, nur die
Ausgangslage "keine Vorarbeit vorhanden" nicht.

**FAKT** (mehrere Quellen übereinstimmend): Pinterest ist
such-orientiert, nicht scroll-orientiert — Nutzer kommen mit
Kaufabsicht. 83 % treffen Kaufentscheidungen auf Basis von
Pinterest-Funden, es bringt 33 % mehr Referral-Traffic zu Online-Shops
als Facebook.
[Improvado](https://improvado.io/blog/pinterest-marketing-tactics) ·
[IPFoxy](https://www.ipfoxy.com/blog/ideas-inspiration/5139)

**FAKT, besonders relevant für einen Ein-Personen-Betrieb:** Ein
einzelner erfolgreicher Pin kann 12–24 Monate lang Traffic bringen —
Pinterest-Inhalte "leben" Monate bis Jahre, nicht Stunden wie ein
TikTok-Post. Das ist ein Kanal, der mit wenig laufender Pflege
auskommt, was hier realistisch zur einzigen verfügbaren Arbeitszeit
passt.

**EINSCHÄTZUNG:** Pinterest passt inhaltlich besser zu Wohnen/Möbel/
Haustier als zu den übrigen 8 Sortimentsbereichen — genau die Kategorie,
die laut `AUDIT.md` (Chance #4) ohnehin der einzige zusammenhängende
Bereich mit belegter Nachfrage ist.

**Aufwand:** Neu aufzubauen, keine Vorarbeit vorhanden (Korrektur: ich
hatte in dieser Sitzung fälschlich angenommen, es gäbe schon eine
Pinterest-Automatisierung im Repository — geprüft, gibt es nicht).
Realistisch 3–5 Boards, 10–15 Pins zum Start, aus vorhandenen
Produktfotos.
**Kosten:** 0 €, nur Zeit.

### 4. TikTok — über die 17 Reels hinaus, laufender Content

**FAKT** (Dash Social / Stackmatix-Recherche): Die stärksten
TikTok-Strategien bauen auf 3–4 wiederkehrenden Content-Säulen auf —
Bildungsinhalte, Behind-the-Scenes, Produkt-Storytelling, UGC. Regel:
80 % wertvoller/unterhaltender Inhalt, 20 % direkte Werbung. Die meisten
kleinen Shops sehen erste Traktion nach 2–4 Wochen regelmäßigen
Postens, spürbaren Umsatzeffekt erst nach 2–3 Monaten.
[Stackmatix](https://www.stackmatix.com/blog/tiktok-marketing-strategy-2026)

**EINSCHÄTZUNG, konkret statt generisch (Master-Prompt Punkt 9 verlangt
das ausdrücklich):**

> Hook: „Warum steht in jedem zweiten Home-Office-Video dieser Stuhl?"
> Szene 1: Stuhl wird auf 135° zurückgelehnt.
> Szene 2: Nahaufnahme Netzrücken + Fußstütze ausklappen.
> Szene 3: Person tippt entspannt zurückgelehnt weiter.
> CTA: „129,99 € bei Homeeins — Link in Bio."

Das ist ein Beispiel-Skript für den Bürostuhl 135°, nicht mehr — echte
Wirkung erst nach echten Tests messbar.

**Aufwand:** 4–6 Posts/Woche für spürbare Wirkung laut Recherche — bei
einer Person realistisch nur mit Batch-Produktion an einem Tag pro
Woche machbar. **EINSCHÄTZUNG:** Das ist der Punkt, an dem organischer
Content an die Kapazitätsgrenze eines Ein-Personen-Betriebs stößt.

### 5. Content-Cluster / Ratgeber ausbauen — erledigt (13.08.2026)

**FAKT** (Repository): Zwei Ratgeber zu Hundemöbeln existierten bereits
(aus früherer Sitzung). **FAKT** (Recherche): Guides/Ratgeber sind ein
etablierter SEO-Hebel für Long-Tail-Keywords ohne Backlink-Aufwand.

Zwei weitere Ratgeber im gleichen Muster ergänzt, live veröffentlicht:
- [„Ergonomischer Bürostuhl: Worauf es beim Sitzen wirklich ankommt"](https://www.homeeins.de/blogs/news/buerostuhl-ergonomie-worauf-es-ankommt)
- [„Kratzbaum kaufen: Welche Größe passt zu deiner Katze?"](https://www.homeeins.de/blogs/news/kratzbaum-groesse-material-standort)

Beide verlinken auf die jeweiligen realen Produkte (Bürostuhl 135°,
kompakter und XXL-Kratzbaum) und passende Kollektionen. Beide auch als
Pinterest-Pin eingeplant (Details: `SOCIAL.md`), wie bei den zwei
bestehenden Hundemöbel-Ratgebern.

---

## 🟡 P2 — sinnvoll, aber nicht vor P0/P1

- **Instagram** — gleiche 17 Reels dort mitverwenden (siehe P0), organisches Wachstum darüber hinaus braucht laut Recherche deutlich mehr Aufwand für weniger Reichweite als TikTok (2–5 % vs. 10–30 % organische Reichweite).
- **Influencer-/Micro-Creator-Kooperationen** — laut Recherche ein Hebel mit "minimalem Aufwand" für Reichweite, aber: **EINSCHÄTZUNG**, ohne Trackrecord (0 Bestellungen 2026) ist die Verhandlungsposition für kostenlose/günstige Kooperationen schwach. Erst nach den ersten eBay-Verkäufen als Beleg realistisch.
- **YouTube Shorts** — dieselben 17 Reels passen technisch (9:16), aber YouTube-Publikum sucht eher nach Anleitungen als nach Produktentdeckung. Geringere Priorität als TikTok/Pinterest für diese Produktkategorie.

## ⚪ P3 — erst wenn P0/P1 laufen

- **Gastbeiträge / Digitale PR** — laut Recherche wirksam, aber braucht bereits etwas Reputation, um überhaupt platziert zu werden.
- **Community-Marketing (Foren, Facebook-Gruppen)** — zeitintensiv, Wirkung schwer messbar, für einen Ein-Personen-Betrieb schwer skalierbar.

---

## Was "Experten kopieren" hier wirklich heißt

**Keine erfundenen Namen oder Zahlen.** Die Recherche fand wiederholt
denselben Kernbefund, unabhängig von der Quelle: Shops, die überwiegend
auf organischen statt bezahltem Traffic setzen, hatten in einer
Shopify-eigenen Umfrage 2024 im Schnitt **28 % Nettomarge** gegenüber
**17 %** bei Shops mit bezahltem Traffic als Hauptkanal.
[Quelle über easync.io referenziert] — **EINSCHÄTZUNG zur Einordnung:**
Diese Zahl stammt aus einer Sekundärquelle, nicht direkt von Shopify
nachgeprüft; als Richtungsindiz brauchbar, nicht als exakte Kennzahl für
HOMEEINS zu verwenden.

Das eigentliche Muster hinter jeder echten Fallstudie, die in der
Recherche auftauchte, war nicht ein Trick, sondern **Konsistenz über
Wochen bei wenigen, klar definierten Kanälen** — nicht Aktivität auf
allen Plattformen gleichzeitig. Genau deshalb die Reihenfolge oben:
zwei kostenlose Schnellstarts zuerst, dann ein Kanal (Pinterest), der zur
Kapazität eines Ein-Personen-Betriebs passt, statt gleichzeitig fünf
Kanäle anzufangen und keinen davon durchzuhalten.

---

## Die Reihenfolge, konkret

1. **Diese Woche:** Snippets der 10 rankenden Seiten (aus `AUDIT.md`, noch offen) + 17 Reels auf TikTok/Instagram/YouTube Shorts hochladen.
2. **Nächste 2 Wochen:** Pinterest-Boards aufsetzen, vorhandene Produktfotos verpinnen.
3. **Danach, laufend:** TikTok-Content-Rhythmus aufbauen, wenn Kapazität da ist — nicht vorher, sonst leidet Qualität und Konsistenz gleichzeitig.

**Was hier weiterhin nicht passiert, aus denselben Gründen wie in
`AUDIT.md`:** bezahlte Werbung auf allen drei Kanälen — die
Grundfrage (Conversion Rate unbekannt) hat sich durch diese Recherche
nicht geändert, nur die kostenlosen Alternativen sind jetzt konkreter.
