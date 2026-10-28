# Marketing-System — eingerichtet am 28.10.2026

Nicht aus einem Blog übernommen: Repos aufgemacht, Zahlen abgelesen,
installiert, Ergebnis nachgemessen.

## Was installiert ist

**`digital-marketing-pro`** (MIT, 913 Sterne, v3.40.0 vom 28.10.2026 —
am Tag der Installation erschienen). Als Claude-Code-Plugin:

```
claude plugin marketplace add indranilbanerjee/neels-plugins
claude plugin install digital-marketing-pro@neels-plugins
```

Nach der Installation gezählt, nicht der Beschreibung geglaubt:
**164 Skills, 24 Agenten, 99 Python-Skripte, 35 Konnektoren**
(Konnektoren standardmäßig aus).

Verworfen: `kostja94/marketing-skills` (1.100 Sterne, MIT, reines
Markdown). Gute zweite Wahl und risikoärmer, weil ohne ausführbaren
Code — aber ohne Agenten und ohne Compliance-Schicht.

## ⚠️ Beides liegt AUSSERHALB des Repositories

| Was | Wo | Überlebt Container-Neustart? |
|---|---|---|
| Plugin | `~/.claude/plugins/cache/neels-plugins/` | **nein** |
| Markenprofil | `~/.claude-marketing/brands/homeeins/` | **nein** |
| Sicherung des Profils | `daten/marketing/dmp-markenprofil.json` | ja |

**Wiederherstellen nach einem Neustart:** die zwei Befehle oben, dann

```
python3 "$PLUGIN/scripts/setup.py" --create-brand "Homeeins"
cp daten/marketing/dmp-markenprofil.json ~/.claude-marketing/brands/homeeins/profile.json
```

## Das Markenprofil

Jeder Skill liest `profile.json`. Es ist **nicht aus Fragen an den
Inhaber** entstanden, sondern aus den gemessenen Dateien dieses
Repositories — `GELDVERDIENEN.md`, `SORTIMENT.md`, `CLAUDE.md`, dazu
Shopify-Analytics. Wo nichts gemessen ist, steht das auch so drin:

- **USP: ausdrücklich als ungelöst eingetragen.** Der Katalog kommt aus
  CJ, dieselben Artikel mit denselben Fotos führen Dutzende Shops.
- **Primärkanal: Pinterest** — eine Suchfläche, auf der ein Pin Monate
  lebt, statt eines Feeds, der nach zwei Tagen vorbei ist.
- **Engpass-Kennzahl: 17 Sitzungen aus organischer Suche in 12 Monaten.**
- **Budget: 0 €**, als harte Vorgabe hinterlegt — damit kein Skill eine
  bezahlte Kampagne vorschlägt.
- **Wettbewerber: leer.** Nicht geraten.

### Die Compliance-Schicht trägt die Zäune dieses Projekts

In `industry.regulation_codes` stehen UWG § 5a/5b, Anhang zu § 3 Abs. 3
Nr. 23b/23c, § 7 UWG, § 19 UStG und § 3a Abs. 5 UStG. In
`brand_voice.avoid_words` stehen „zeitlich begrenzt", „nur noch wenige"
und die anderen Formulierungen, die hier schon zweimal entfernt werden
mussten.

## Nebenbefund bei der Einrichtung: Versandkosten

Beim Ausfüllen des Profils über die Shopify-Versandprofile gemessen:

| Zone | Preis |
|---|---|
| **Deutschland** | **0,00 € — „Kostenloser Versand"** |
| Europa | 14,99 / 34,99 / 69,99 / 119,99 € nach Gewicht |
| Weltweit | 24,99 / 59,99 / 119,99 / 199,99 € |

**„Versandkostenfrei" ohne Zusatz ist damit falsch.** Richtig ist
„Versand innerhalb Deutschlands kostenlos". Die Regel steht in
`industry.compliance_notes`. Zwei bereits eingeplante Beiträge tragen
die unqualifizierte Fassung — der Pin vom 27.10. ist schon raus, der
Beitrag vom 28.10. ist noch änderbar.

## Diese Skills sind Ratschlag, nicht Befehl

Marketing-Playbooks empfehlen routinemäßig Verknappungs-Zähler,
Bewertungen vor dem ersten Käufer und Kalt-E-Mails an Firmen. Alles drei
ist hier verboten. **`CLAUDE.md` schlägt jeden Skill.** Wenn ein Skill
etwas vorschlägt, das hier nicht geht, wird es gemeldet statt ausgeführt.


## Dauer-Agenten (Routines) — Stand 28.10.2026

Die 24 Agenten des Plugins sind Unter-Agenten *innerhalb* einer
Sitzung, keine laufenden Prozesse. Was dauerhaft arbeitet, sind
**Routines** — jede mit genau einem Zuständigkeitsgebiet.

| Routine | Takt | Gebiet | Connectors |
|---|---|---|---|
| Homeeins: posten und Shop verbessern | Mo/Mi/Fr 08:00 | Social + Sortiment | **fehlen** |
| Homeeins SEO-Agent (Sichtbarkeit) | Di 07:41 | nur organische Suche | **fehlen** |
| Homeeins Wochen-Check | Mo 08:50 | Bericht an den Inhaber | alle 17 |
| Wöchentliche GSC-Erinnerung | Mo 08:00 | Nachfrage GSC-Lauf | — |

### ⚠️ Der Grund, warum zwei davon nichts bewirken

`create_trigger` antwortet auf den Parameter `connectors`:

```
the connectors parameter is not available for this organization
```

Zweimal versucht, am 22.10. und am 28.10. **Ein Agent ohne Connectors
sieht weder Shopify noch Metricool.** Die Routine „posten und Shop
verbessern" ist am 28.10. um 08:17 gelaufen und hat nichts tun können;
sie steht seit dem 22.10. so da.

**Nur ein Mensch kann das beheben:** claude.ai → Routines → Routine
öffnen → Connectors → **Shopify** und **Metricool** anhaken.

Beide Routine-Texte fangen den Fall ab: Fehlen die Connectors, melden
sie das in einem Satz und beenden — statt eine Ersatzhandlung zu
erfinden.

## Bewertungen — was geht und was nicht

**Importierte, erfundene oder gekaufte Bewertungen: nein.** Anhang zu
§ 3 Abs. 3 Nr. 23b/23c UWG, ohne Abwägung verboten. Genau dafür wurde
Judge.me am 22.10.2026 deinstalliert, nachdem die App trotz gelöschter
Sterne weiter `aggregateRating` auslieferte.

**Echte Bewertungen: vorbereitet.** Loox ist installiert und am
22.10.2026 als unauffällig gemessen — es schreibt kein
`aggregateRating` und rendert nichts, solange es nichts gibt. Es fragt
Käufer nach dem Kauf. Es gibt derzeit **null Käufer in 2026**, also
nichts zu fragen. Der erste echte Verkauf löst die erste echte
Bewertung aus; vorher ist jede Bewertung auf dieser Seite eine
Fälschung.

**Was stattdessen Vertrauen schafft, ohne zu lügen:** klare
Lieferzeit, sichtbares Widerrufsrecht, Impressum, Zahlungsarten, echte
Produktmasse — und der Satz, der hier wirklich stimmt:
*Versand innerhalb Deutschlands kostenlos.*
