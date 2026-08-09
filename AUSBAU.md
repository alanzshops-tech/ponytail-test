# Ausbau in der Sandbox — Nacht vom 9. auf den 10. August 2026

**Theme:** „Sandbox Ausbau – Claude (nicht veröffentlichen)", ID `182664790339`, unveröffentlicht.
**Vorschau:** `https://www.homeeins.de/?preview_theme_id=182664790339`

Nichts davon ist live. Der Shop läuft unverändert auf „Umbau Conversion – Claude".

## Was gebaut wurde

### Produktseite neu geordnet

Die Reihenfolge folgt jetzt dem Entscheidungsweg statt der Zufallsreihenfolge,
in der Bausteine über die Jahre dazugekommen sind:

| | vorher | nachher |
|---|---|---|
| 1 | Titel | Titel |
| 2 | Preis | Preis |
| 3 | Variantenwahl | **Kostenloser Versand · 30 Tage Rückgabe · Sicher bezahlen** |
| 4 | Menge | Variantenwahl |
| 5 | Kaufknopf | **Lagerstatus** („Auf Lager") |
| 6 | Beschreibung | Menge |
| 7 | Bewertungen | Kaufknopf |
| 8 | | **Versand & Lieferung** (aufklappbar) |
| 9 | | **Rückgabe & Widerruf** (aufklappbar) |
| 10 | | **Zahlungsarten** (aufklappbar) |
| 11 | | Beschreibung |
| 12 | | Bewertungen |

Der Gedanke dahinter: Der Preis wird sofort qualifiziert („und Lieferung
kostet nichts"), bevor die Auswahl beginnt. Die drei Fragen, die vor dem
Klick bremsen — Wann kommt es? Kann ich es zurückgeben? Wie zahle ich? —
stehen direkt unter dem Kaufknopf, aufgeklappt nur bei Bedarf.

**Alles davon sind Dawn-eigene Bausteine.** Kein eigenes CSS, kein
eigenes JavaScript, kein einziges Zeichen in einer Dawn-Datei. Ich habe
vorher aus Shopifys Dawn 15.5.0 ausgelesen, welche Blocktypen es
tatsächlich gibt (`icon-with-text`, `inventory`, `collapsible_tab`), und
gegen diese Liste geprüft, statt sie mir zu merken.

Der Lagerstatus zeigt **keine Stückzahl**. „Nur noch 3 Stück" neben
einem echten Lagerbestand von 500 wäre genau die Dringlichkeit, die ich
nicht baue.

Der Text der Zahlungsarten ist die Liste, die die Kasse am 9.8.2026
wirklich angeboten hat — nachgemessen, nicht abgeschrieben.

### Zahlungslogo-Wand abgeschaltet

Der Block mit zwölf Zahlungslogos unter dem Kaufknopf kam nicht aus dem
Theme, sondern von der App **Essential Trust Badges**. Er nahm mehr Platz
ein als die halbe Produktbeschreibung, wiederholte die Logos aus der
Fußzeile und warb mit **SEPA**, das es in der Kasse nicht gibt.

In der Sandbox ist die App-Einbindung abgeschaltet. An ihre Stelle tritt
die dreiteilige Vertrauenszeile aus Dawns eigenem Baustein — eine Zeile
statt sechs, und ohne falsche Zahlart.

### Theme-Einstellungen

| Einstellung | vorher | nachher | Grund |
|---|---|---|---|
| `currency_code_enabled` | an | **aus** | beseitigt „€124,99 EUR" |
| `body_scale` | 100 % | **110 %** | Fließtext war 14–15 px, empfohlen ≥ 16 |
| `buttons_border_thickness` | 3 px | **1 px** | Dawns Voreinstellung; 3 px wirken alt |

Alles Regler, die Shopify selbst vorsieht. Jede Änderung ist im
Theme-Editor mit einem Klick zurückzudrehen.

## Gemessen, nicht behauptet

Gleiche sechs Seiten, gleiche Geräte, einmal live und einmal Sandbox.

| Maß | Live | Sandbox |
|---|---:|---:|
| Fließtext mobil | 15 px | **16,5 px** |
| Fließtext Desktop | 14 px | **15,4 px** |
| Preise mit „EUR" | **22** | **0** |
| Kontrastverstöße | **6** | **2** |
| Formularfeld ohne Beschriftung | 4 | 6 |
| Scrollbereich ohne Tastatur | 10 | 12 |
| „Frames ohne Namen" | 0 | 12 |

Zwei dieser Zeilen sehen nach Rückschritt aus und sind keiner:

**„Frames ohne Namen", 12 Fälle** — ich habe nachgesehen statt zu raten.
Das Beispiel lautet `<iframe id="PBarNextFrame" src="https://cdn.shopify...">`.
Das ist **Shopifys eigene Vorschauleiste**, die nur bei
`?preview_theme_id=` erscheint. Genau ein Fall je Seitenaufruf, sechs
Seiten mal zwei Geräte = zwölf. Beim Veröffentlichen verschwindet sie.

**Formularfeld ohne Beschriftung, 4 → 6** — dasselbe Dawn-Mengenfeld,
nur auf drei Produktseiten statt auf zwei gezählt. Kein neuer Fehler.

Der echte Gewinn steckt in **Kontrast 6 → 2**: Die vier verschwundenen
Fälle waren die Zahlungslogos der App. Die verbleibenden zwei sind meine
eigene FAQ-Rubrikzeile, die in der Sandbox inzwischen auch korrigiert ist
(3,71:1 → 5,42:1) — die Messung lief davor.

## Was ich bewusst nicht getan habe

- **Kein eigenes CSS, kein eigenes JavaScript.** 43 von 52 Abschnitten
  sind byte-identisch mit Shopifys Dawn 15.5.0. Diese Updatefähigkeit ist
  das wertvollste technische Gut des Shops. Sie geht in dem Moment
  verloren, in dem jemand anfängt, in Dawns Dateien zu schreiben.
- **Keine Dringlichkeit, keine Knappheit, keine erfundenen Zahlen.**
- **Kein klebender Kaufknopf auf dem Handy.** Wirkt nachweislich, braucht
  aber eigenes JavaScript. Das bespreche ich vorher mit Ihnen, statt es
  nachts einzubauen.

## Bekannte Abweichung, die Sie wissen sollten

Beim Neuschreiben von `config/settings_data.json` sind zwei
**abgeschaltete** App-Einbindungen weggefallen: die Wunschzettel-App
(`mst-wishlist`) und der Widerrufsbutton (`revoq`). Beide standen auf
`disabled: true`, hatten also keine Wirkung im Shop. Falls eine davon
später gebraucht wird, muss sie im Theme-Editor neu eingeschaltet und
eingestellt werden. In der Sandbox ist das folgenlos — nur nicht
vergessen, wenn dieses Theme einmal veröffentlicht werden soll.

## Was als Nächstes ansteht

1. **Ansehen und entscheiden.** Vorschau öffnen, Produktseite auf dem
   Handy durchscrollen. Bilder liegen in `bilder/sandbox/`.
2. **Judge.me leeren.** Der Samt-Sessel liefert weiter ein
   `aggregateRating` in den Strukturdaten — die Bewertungen liegen in der
   App, nicht in Shopify. Ohne das bleibt die Sache halb erledigt.
3. **Preiszeichen.** „€124,99" statt „124,99 €" ist eine
   Shop-Einstellung unter *Einstellungen → Allgemein → Währungsformat*.
   Da komme ich nicht heran.
4. **Theme-Access-Token** (siehe `WERKZEUGE.md`). Damit wird aus
   dateiweisem Hochladen echte Versionsverwaltung.
5. **Produkttitel kürzen.** „Erhöhtes Hundebett mit Beinen – Luxus
   Hunde-Sofa aus Samt, stabil bis 50 kg" braucht auf dem Handy drei
   Zeilen, bevor der Preis kommt. Das ist Textarbeit an 146 Produkten,
   keine Theme-Arbeit — und der nächste große Hebel.
