# homeeins — Reels aus Produktfotos

Erzeugt vertikale 9:16-Reels für Instagram und TikTok aus vorhandenen
Shopify-Produktfotos. Kein Filmteam, kein Videoschnitt, kein kostenpflichtiger
Video-API-Dienst — gerendert wird mit FFmpeg auf einem GitHub-Actions-Runner.

## Warum GitHub Actions

Der Runner hat freien Netzzugang und rendert kostenlos: Bei öffentlichen Repos
sind GitHub-Actions-Minuten unbegrenzt, bei privaten gibt es 2.000 Minuten pro
Monat. Ein Reel braucht ein bis zwei Minuten.

## Einrichtung (einmalig)

**1. Cloudinary-Zugangsdaten als Repository-Secrets hinterlegen**

*Settings → Secrets and variables → Actions → New repository secret*

| Name | Wo zu finden |
|---|---|
| `CLOUDINARY_CLOUD_NAME` | Cloudinary Console, oben links (`kar0bjzs`) |
| `CLOUDINARY_API_KEY` | Settings → API Keys |
| `CLOUDINARY_API_SECRET` | Settings → API Keys |

Ohne diese Secrets läuft alles trotzdem — die fertigen MP4s liegen dann 30 Tage
als Artefakt am Workflow-Lauf zum Herunterladen bereit, statt auf Cloudinary.

**2. Produkte eintragen** in `reels.config.json`:

```json
{
  "name": "samt-sessel",
  "hook": "Die Ecke, um die\ngestritten wird",
  "preis": "124 EUR",
  "bilder": ["https://cdn.shopify.com/.../bild1.jpg", "..."]
}
```

Bild-URLs bekommst du im Shopify-Admin: Produkt → Medien → Bild öffnen →
URL kopieren. Vier bis sechs Bilder ergeben 6,5 bis 10,5 Sekunden.

## Benutzung

*Actions → „Reels rendern" → Run workflow.* Feld `nur` leer lassen rendert alle
Produkte, oder einen `name` eintragen für ein einzelnes.

Der wöchentliche Zeitplan (montags 04:00 UTC) ist in `.github/workflows/reels.yml`
aktiviert. Nimm ihn raus, wenn du lieber manuell auslöst.

Ergebnis: MP4-URLs in der Zusammenfassung des Laufs. Die lassen sich direkt in
Metricool als Reel einplanen.

## Was rauskommt

1080×1920, 30 fps, H.264, stille AAC-Tonspur. Je Bild zwei Sekunden mit
langsamer Ken-Burns-Zoomfahrt, dazwischen halbsekündige Überblendungen.
Hook-Text oben, Preis unten auf halbtransparentem Balken.

Zwei Sekunden pro Bild ist kein Zufall: Auswertungen zur Reel-Performance
nennen 1,5–2,5 Sekunden als Bereich mit der höchsten Watch-Time.

## Grenzen

- **Keine Musik.** Business-Accounts dürfen die reguläre Instagram-Bibliothek
  nicht nutzen, und die Content-Publishing-API kann ohnehin keine Tonspur
  anhängen — Musik müsste vor dem Upload eingebettet sein. Entweder eine eigene
  Lizenz kaufen (Epidemic Sound, Artlist) oder den letzten Schritt manuell in
  der App machen und dort die Meta Sound Collection nutzen.
- **Keine echte Kamerafahrt.** Es bleibt eine gut gemachte Slideshow.
- **Kein KI-Material**, und das ist Absicht: Seit dem 2. August 2026 gelten die
  Transparenzpflichten aus Artikel 50 EU AI Act. Eine Slideshow aus echten,
  unveränderten Produktfotos fällt nicht darunter. KI-generierte Bewegtbilder
  wären kennzeichnungspflichtig — und bei Möbeln käme das Risiko irreführender
  Produktdarstellung dazu, weil die Modelle Maserung und Proportionen verändern.

## Lokal ausführen

```bash
sudo apt-get install -y ffmpeg fonts-dejavu-core
pip install requests
python3 scripts/make_reels.py --config reels.config.json --out dist
```

Wichtig: FFmpeg muss mit `libfreetype` gebaut sein, sonst fehlt der
`drawtext`-Filter und die Reels entstehen ohne Text. Das Skript prüft das beim
Start und warnt. Die FFmpeg-Version aus dem pip-Paket `imageio-ffmpeg` kann
kein `drawtext` — die aus den Ubuntu-Paketquellen schon.

## Technische Notiz

Gerendert wird in zwei Stufen: erst jedes Bild einzeln zu einem Clip, dann die
Clips überblenden. Der Umweg ist nötig, weil `zoompan` keine verwertbare
Bildratenangabe weitergibt und `xfade` sonst mit
`The inputs needs to be a constant frame rate; current rate of 1/0` abbricht.

Ebenso wird die Ausgabedauer per `-t` fest gesetzt: `-shortest` greift bei
Filter-Ausgaben nicht, und die endlose `anullsrc`-Tonspur würde das Video
sonst auf über zwei Minuten aufblähen.
