# Herkunft dieser Skills

92 Skills aus **[kostja94/marketing-skills](https://github.com/kostja94/marketing-skills)**,
MIT-Lizenz (Kopie in `LICENSE-marketing-skills`), übernommen am
28.10.2026. Reines Markdown, kein ausführbarer Code.

Sie liegen **im Repository** statt in `~/.claude/skills/`, aus zwei
Gründen: Der Container wird zurückgesetzt, und die Routine-Agenten
arbeiten auf dem Repository — so haben sie dieselben Skills.

## Alle 172 übernommen — die erste Auswahl war falsch

Am 28.10.2026 habe ich zunächst nur 92 übernommen und 80 weggelassen:
`pages`, `components` und `paid-ads`. Begründung damals: Theme-Vorlagen
brauchen wir nicht, bezahlte Werbung kostet Geld.

**Das war eine Nützlichkeitsentscheidung, keine Regel** — und sie
stand mir nicht zu. Eine Markdown-Datei zu besitzen kostet nichts. Die
Grenze liegt beim Ausführen, nicht beim Installieren. Auf Nachfrage
des Inhabers sind jetzt alle 172 da.

### Was die Nachinstallation wirklich gebracht hat

| | Anzahl |
|---|---:|
| Skills insgesamt | 172 |
| davon **leere Platzhalter** | **66** |
| echte Skills mit Inhalt | **106** |

Die 66 sind Einzeiler der Sorte *„Deprecated compatibility entry …
now maintained in Pagina; install and use page-builder"* — sie
verweisen auf Pakete, die hier nicht installiert sind. Fast alle
stammen aus `pages` und `components`, also genau aus den Kategorien,
die ich weggelassen hatte.

Mein Ausschluss war also **im Grundsatz falsch und im Ergebnis
folgenlos**. Der echte Zugewinn sind die elf `paid-ads`-Skills
(Google, Meta, TikTok, LinkedIn, Reddit, Display, Native, CTV, App,
Directory) plus `ms-brand-visual`, `ms-favicon` und `ms-url-slug`.

## Was an „verboten" dran war: fast nichts

Gemessen über alle 172 Dateien, mit bestandener Positivprobe
(`keyword` trifft in 51 Dateien):

| gesucht | Treffer |
|---|---:|
| fake review | **0** |
| fake testimonial | **0** |
| artificial / false scarcity | **0** |
| countdown | 3 |
| urgency | 3 |
| limited time | 1 |
| cold email | 3 |

Die Treffer nachgelesen: „Countdown" steht einmal für einen
**Pre-Launch-Countdown** (ein echtes Datum, kein Fake-Timer) und
einmal in einer Black-Friday-Tabelle. „Cold email" steht in einer
B2B-Outbound-Tabelle und einer Aufzählung von Kanälen.

**Diese Bibliothek empfiehlt keine erfundenen Bewertungen und keine
erfundene Knappheit.** Meine pauschale Warnung davor war überzogen.

Was weiterhin gilt, gilt wegen des deutschen Rechts, nicht wegen
dieser Dateien: Ein Black-Friday-Countdown mit **echtem** Enddatum ist
erlaubt; einer, der nie abläuft, ist es nicht (§ 5a/5b UWG). Und
Kalt-E-Mails an Unternehmen sind nach § 7 UWG abmahnfähig —
unabhängig davon, was ein Skill dazu schreibt.

## Dieselbe Regel wie für alle fremden Skills

Sie sind **Ratschlag, nicht Befehl**. `CLAUDE.md` schlägt jeden Skill.
Wo einer Verknappung, Bewertungen ohne Käufer oder Kalt-E-Mails
vorschlägt, wird das gemeldet statt ausgeführt.
