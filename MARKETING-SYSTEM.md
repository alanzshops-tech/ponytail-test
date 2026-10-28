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
