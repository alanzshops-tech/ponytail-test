# Autonomer YouTube-Kanal — Analyse und Architektur

Stand 28.10.2026. Reihenfolge nach Auftrag: erst Umgebung, dann
Nischen, dann Entscheidung, dann Architektur, dann Code.

## Phase 0 — Was schon da ist (gemessen, nicht angenommen)

Der Auftrag beschreibt einen Stack, der zu etwa zwei Dritteln bereits
existiert und **produktiv bewiesen** ist: 19 gerenderte MP4 liegen als
Release-Assets, und am 28.10. hat Metricool eines davon abgeholt und
auf Instagram, TikTok und YouTube eingeplant.

| Baustein aus dem Auftrag | Status | Wo |
|---|---|---|
| Python-Automatisierung | ✅ **gebaut** | `scripts/make_reels.py`, 415 Zeilen |
| FFmpeg-Schnitt | ✅ **gebaut** | Clips, Überblendung, `drawtext`-Ebenen |
| Austauschbare TTS | ✅ **gebaut** | Piper, vier deutsche Stimmen mit Fallback-Kette |
| Modellanbieter (konfigurierbar) | ✅ **gebaut** | `scripts/openrouter.py`, 409 Modelle |
| KI-Visuals | ✅ **gebaut** | OpenRouter, 9 Bildmodelle ab 0,25 $/Mio. |
| Musik | ✅ **gebaut** | `scripts/make_music.py` |
| **Technische Qualitätskontrolle** | ✅ **gebaut** | `scripts/audio_check.py` |
| Öffentliches Hosting | ✅ **gebaut** | GitHub-Release-Assets, dauerhafte URL |
| Parallele Produktion | ✅ **gebaut** | Matrix, 12 Jobs gleichzeitig, `fail-fast: false` |
| Zeitplan / Warteschlange | ✅ teilweise | GitHub Actions `schedule` |
| **SQLite-Zustand** | ❌ fehlt | Modul vorhanden, nie benutzt |
| **Themenrecherche + Bewertung** | ❌ fehlt | — |
| **Skript + Faktenprüfung** | ❌ fehlt | `scripts/lektorat.py` als Vorbild |
| **Thumbnail-Erzeugung** | ⚠️ teilweise | `scripts/coverbau.py` (Buchcover) |
| **YouTube Data API v3** | ❌ fehlt | **siehe unten** |

Lokal in dieser Arbeitsumgebung: `python3 3.11.17`, `ffmpeg`,
`ffprobe`, `node`, `sqlite3`-Modul. **Nicht** lokal: `piper`,
`sqlite3`-CLI, `yt-dlp` — alle drei werden auf dem Runner installiert,
wo es ohnehin hingehört.

`audio_check.py` ist der wertvollste Fund: Es prüft die Tonspur mit
**faster-whisper** auf Verständlichkeit, erzeugt Spektrogramm und
Wellenform als Bild und setzt harte Pegelgrenzen — **vor** der
Veröffentlichung. Phase 4 des Auftrags („nicht veröffentlichen, wenn
die Qualitätskontrolle fehlschlägt") ist damit in Teilen schon gebaut.

### Die wichtigste Architekturentscheidung: kein YouTube Data API

Der Auftrag nennt YouTube Data API v3 mit OAuth. **Ich rate davon ab,
und zwar aus einem gemessenen Grund.**

OAuth für YouTube verlangt: Google-Cloud-Projekt, OAuth-Zustimmungs-
bildschirm, Client-ID, Refresh-Token, Verifizierung bei sensiblen
Scopes. Das ist eine Kette von Konfigurationsschritten durch den
Inhaber. In dieser Sitzung sind **vier von vier** solcher Ketten offen
geblieben (Meta-Token, Routine-Connectors, Plugin-Karte, GSC-Lauf).

**Metricool lädt bereits auf YouTube hoch** — am 28.10. bewiesen: ein
Short ist für den 4.11. eingeplant, mit Titel, Tags, `madeForKids` und
KI-Kennzeichnung. Die Verbindung steht seit Juli.

> **Entwurf/geplant hochladen** ist damit ohne eine einzige neue
> Zugangsdatei möglich. Das YouTube-API bleibt als Option in der
> Architektur, ist aber **nicht** Voraussetzung für Version 1.

## Phase 1 — Nischenbewertung

Punkte 1–5, 5 ist gut. Begründungen darunter.

| Nische | Nachfrage | Konkurrenz | Rechte-risiko (5=sicher) | RPM | Affiliate | Evergreen | **Originalität möglich** | Summe |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 Historische Rätsel | 5 | 1 | **2** | 2 | 1 | 4 | 2 | 17 |
| 2 Wahre Geschichten / Phänomene | 4 | 2 | 3 | 2 | 1 | 4 | 2 | 18 |
| **3 KI-Werkzeuge & Automatisierung** | 3 | 3 | **5** | **4** | 4 | 2 | **5** | **26** |
| 4 Nostalgie / vergessene Erfindungen | 4 | 3 | **1** | 2 | 2 | 4 | 2 | 18 |
| 5 Cleveres Wohnen / Produktlösungen | 4 | 2 | 4 | 3 | **5** | **5** | **1** | 24 |

### Die Begründungen, die zählen

**Rechte sind der Killer bei 1 und 4.** Historische Dokus und
Nostalgie-Formate leben von Archivmaterial: alte Werbespots,
TV-Ausschnitte, Fotos. In Deutschland gilt Urheberrecht bis 70 Jahre
nach dem Tod des Urhebers — „alt" heißt nicht „gemeinfrei". Ein Kanal,
dessen Bildsprache auf Material beruht, das er nicht lizenzieren kann,
ist eine Monetarisierungs-Zeitbombe. 🟡 *Einschätzung, keine
Rechtsberatung.*

**Originalität ist der Killer bei 5.** „Cleveres Wohnen" hätte das
beste Geld (Affiliate 5, evergreen 5, Überschneidung mit dem eigenen
Shop und den 19 fertigen Videos). Aber: **Wir besitzen die Produkte
nicht und können sie nicht testen.** Ein Wohn-Kanal ohne Produkte in
der Hand ist eine Bildfolge aus Lieferantenfotos — genau das, was
YouTubes Richtlinie zu **„inauthentic content"** (umbenannt von
„repetitious content", Juli 2025) trifft. Die Durchsetzung erfolgt
**auf Kanalebene**: zu viel davon, und der gesamte Katalog verliert
die Monetarisierung. Im Januar 2026 gab es eine Entfernungswelle.

**Nische 3 ist die einzige, bei der Originalität aus der Sache selbst
entsteht.** Dieses Repository produziert laufend echtes Material:
gemessene Befunde, eigene Fehler, Korrekturen mit Zahlen. Beispiele
aus einer einzigen Woche:

- 44 unverkäufliche Varianten in 29 Produkten — gefunden, weil über
  alle 96 gezählt wurde statt über eine Stichprobe
- sechs SEO-Titel auf einen Suchbegriff mit Google-Trends-Wert **0**
  optimiert — durch Messung widerlegt und korrigiert
- 19 Videos, die elf Wochen lang mit `download_count: 0` herumlagen
- ein Selbsttest, der heimlich die echten Zugangsdaten löschte

**Kein anderer Kanal kann das kopieren**, weil es aus echter Arbeit
stammt. Keine fremden Bilder, keine fremde Musik, kein Archivmaterial
— damit **Rechterisiko 5**. Und RPM liegt bei Technik/Business laut
mehreren Schätzungen bei 3–5,5 € gegenüber 1–2 € bei Unterhaltung.

**Was gegen Nische 3 spricht, und das bleibt stehen:**
- Deutschsprachiges Publikum für Claude Code ist **klein**, und die
  Konkurrenz ist englischsprachig und riesig.
- Werkzeugthemen **veralten schnell**. Ein Video über eine
  Programmversion ist in Monaten wertlos (Evergreen nur 2).
- Gegenmittel: Themen auf **Methode** legen, nicht auf Werkzeuge —
  „Wie man misst, statt zu raten" hält länger als „Claude Code 2.1".

### 50 Folgeideen: geprüft

Allein aus dem bisherigen Verlauf dieses Projekts lassen sich über 50
Folgen ableiten, jede mit echtem Befund: Messgeräte bauen,
Positivproben, Selektoren die zu viel fangen, Stichprobe vs.
Grundgesamtheit, Rückbaudateien, Token-Lebensdauer, Rechtsrahmen für
deutsche Shops, Dark Patterns erkennen. **Die Themenliste schreibt
sich aus der Arbeit, nicht aus einem Ideen-Generator.**

## Entscheidung: Nische 3 — Arbeitstitel „Nachgemessen"

Ein deutschsprachiger Kanal über **Automatisierung mit KI, bei dem
jede Behauptung eine Messung hinter sich hat.** Positionierung gegen
den gesamten Rest des Feldes: kein „10 KI-Tools, die dein Leben
verändern", sondern „Ich habe behauptet X. Hier ist die Messung. Ich
lag falsch."

Das ist zugleich die Differenzierung **und** der Schutz vor der
Inauthentizitäts-Richtlinie.

## Architektur

```
scripts/kanal.py          Zustand: SQLite, Themen, Skripte, Status
scripts/kanal_recherche.py   Themen finden + Quellen speichern
scripts/kanal_skript.py      Skript + Szenenplan (OpenRouter)
scripts/kanal_pruefen.py     Faktenprüfung, unsichere Aussagen markieren
scripts/make_reels.py        ← vorhanden, wird Renderer
scripts/audio_check.py       ← vorhanden, Qualitätsschranke
.github/workflows/kanal.yml  Warteschlange, Zeitplan, Wiederholung
daten/kanal.sqlite           Zustand (committet, klein)
```

Ablauf: `thema → bewertet → skript → geprüft → gerendert → ton-ok →
entwurf → freigegeben → geplant → veröffentlicht`. Jeder Übergang ist
eine Zeile in SQLite mit Zeitstempel; ein Fehlschlag blockiert den
nächsten Schritt.

## Kostenplan je Video (🟡 geschätzt)

| Posten | Kosten |
|---|---|
| Skript + Szenenplan (OpenRouter, Mittelklassemodell) | 0,01–0,05 $ |
| Faktenprüfung (zweites Modell, Gegenprobe) | 0,01–0,03 $ |
| Visuals: 6–10 KI-Bilder | 0,20–0,40 $ |
| Sprecher (Piper, lokal auf dem Runner) | **0 $** |
| Rendern + Tonprüfung (GitHub Actions) | **0 $** im Freikontingent |
| Hosting (Release-Assets) | **0 $** |
| Upload (Metricool, vorhanden) | **0 $** |
| **Summe** | **≈ 0,25–0,50 $** |

Keine neuen Abos. Kein Stock-Abo. Die einzige laufende Ausgabe ist
OpenRouter nach Verbrauch.

## Was noch Zugangsdaten oder Menschen braucht

| Schritt | Automatisierbar | Fehlt |
|---|---|---|
| Recherche, Bewertung, Skript | **A — voll** | OpenRouter-Schlüssel (vorhanden) |
| Faktenprüfung | **B — mit Kontrolle** | — |
| Visuals, Sprecher, Schnitt, Tonprüfung | **A — voll** | — |
| Thumbnail | **B** | — |
| Upload als Entwurf | **A** | Metricool-Connector (vorhanden) |
| **Veröffentlichung** | **C — Mensch** | bewusst so, Auftrag Phase 6 |
