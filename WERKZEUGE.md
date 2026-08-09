# Werkzeugkasten Homeeins

Alles quelloffen, alles ohne Abo, alles läuft auf dem GitHub-Runner.
Der Grundsatz bleibt: **Wo ich blind bin, baue ich ein Messgerät.**

## Der Befund, der alles andere ordnet

Die Annahme „Dawn schränkt uns ein" habe ich am 9.8.2026 nachgemessen:

| | |
|---|---|
| Theme von Homeeins | Dawn **15.4.1** |
| Dawn bei Shopify (GitHub) | **15.5.0** |
| Abschnitte insgesamt | 52 |
| davon **byte-identisch** mit Dawn 15.5.0 | **43** |
| abweichend | 9 — und zwar alle *kleiner*, also schlicht die ältere Fassung |
| eigene, selbstgeschriebene Abschnitte | **0** |

Das Theme ist praktisch unverändertes Dawn, eine Nebenversion hinterher.
Dawn schränkt hier nichts ein. Die Lage ist das Gegenteil: Weil kaum
etwas verbogen wurde, lassen sich Shopify-Updates **noch sauber
übernehmen**. Das ist ein Vermögenswert, und der geht in dem Moment
verloren, in dem jemand anfängt, eigene Abschnitte danebenzustellen.

Deshalb die Leitlinie für alles Weitere:

> Zuerst Dawns eigene Einstellungen, dann Dawns eigene Abschnitte,
> und nur wenn beides nachweislich nicht reicht, eigener Code — und
> dann in `custom-liquid`, nie in Dawns Dateien.

## Was schon läuft

| Werkzeug | Lizenz | Wofür | Wo |
|---|---|---|---|
| Playwright | Apache-2.0 | Fotos in Handy- und Laptopgröße, Kennzahlen aus dem Browser | `scripts/webcheck.py` |
| Lighthouse | Apache-2.0 | Googles eigene Bewertung: Tempo, Praxis, SEO | `.github/workflows/website.yml` |
| axe-core | MPL-2.0 | Kontraste, Beschriftungen, Überschriftenfolge (WCAG 2.1 AA) | `scripts/pruefstand.py` |
| Pillow | HPND | Pixelvergleich gegen die letzte Grundlinie | `scripts/pruefstand.py` |
| VCR.py | MIT | Echte API-Antworten aufzeichnen, Tests dagegen laufen lassen | `scripts/aufzeichnen.py` |
| pytrends | Apache-2.0 | Nachfrage und Saison | `scripts/trends.py` |
| Shopify Dawn | MIT | Vergleichsmaßstab: Was ist Original, was ist verändert? | geklont im Lauf |

### Prüfstand

```
python3 scripts/pruefstand.py --urls urls-shop.txt            # messen
python3 scripts/pruefstand.py --urls urls-shop.txt --grundlinie  # Basis setzen
```

Ergebnis in `PRUEFSTAND.md`. Der Pixelvergleich beantwortet die Frage,
die man sonst erst durch einen verlorenen Kunden beantwortet bekommt:
*Habe ich mit dieser Änderung woanders etwas kaputtgemacht?*

Barrierefreiheit ist für Homeeins **keine Pflicht** — das BFSG nimmt
Kleinstunternehmen (unter 10 Beschäftigte **und** unter 2 Mio. Umsatz)
für Dienstleistungen aus. Die Befunde sind trotzdem Bedienfehler, und
Google rechnet sie mit.

## Was noch fehlt und woran es hängt

**Shopify CLI** (MIT) wäre der größte Sprung: das ganze Theme als
Dateien im Repository, `shopify theme pull`/`push`, `theme check` als
Linter, örtliche Vorschau. Damit fällt das dateiweise Hochladen über die
API weg, jede Änderung wird ein Commit mit Diff, und ein Fehlgriff ist
ein `git revert` statt einer Reparatur von Hand.

Dafür braucht der Runner einen **Theme-Access-Token**:

1. Im Shopify-Adminbereich die App **„Theme Access"** installieren
   (kostenlos, von Shopify selbst)
2. Dort ein Passwort für `alanz.shops@gmail.com` erzeugen
3. Es kommt per E-Mail und beginnt mit `shptka_`
4. In GitHub unter *Settings → Secrets and variables → Actions →
   New repository secret* als **`SHOPIFY_CLI_THEME_TOKEN`** hinterlegen

Den Token selbst brauche ich nie zu sehen — er liegt im Tresor von
GitHub, der Runner holt ihn sich.

## Was ich nicht bauen werde

Keine erfundene Verknappung, keine ablaufenden Zähler, keine „17 Leute
sehen sich das gerade an", keine durchgestrichenen Fantasiepreise, keine
Bewertungen ohne Käufer. Das ist in der EU nach der Omnibus-Richtlinie
und § 5b UWG verboten, bei Bewertungen sogar ohne Abwägung
(Anhang zu § 3 Abs. 3 Nr. 23b/23c).

Was stattdessen wirkt und erlaubt ist: Tempo, ein klares Versprechen
oberhalb der Falz, weniger Auswahl je Bildschirm, echte Vertrauenszeichen
(Impressum, Widerruf, Zahlarten, freier Versand), lesbare Preise, gute
Bilder, kurze Titel. Das sind dieselben Hebel — nur ohne die Rechnung,
die später kommt.
