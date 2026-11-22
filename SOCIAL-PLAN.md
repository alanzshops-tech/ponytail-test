# Beitragsplan — fertig zum Senden

Zwölf Beiträge zu den sechs Produkten, die in den Messdaten dieses
Repositories wirklich vorkommen. Keine erfundenen Produkte, keine
erfundenen Preise, keine Knappheit, keine Bewertungen — `CLAUDE.md`
Regel 3.

**Jede Länge unten ist gemessen**, nicht geschätzt: gegen `GRENZE`
aus `scripts/posten.py`.

## Grenzen je Kanal

| Kanal | Zeichen |
|---|---|
| bluesky | 300 |
| mastodon | 500 |
| telegram | 4096 |
| discord | 2000 |
| instagram | 2200 |
| tiktok | 150 |

> TikTok (150 Zeichen) ist nur der Entwurfstitel und braucht ein
> Video — die Texte unten sind dafür nicht gedacht.

## Die Beiträge

### 1. Hundesofa · haustiere

```
Ein erhöhter Rand zum Anlehnen, Samtbezug, Größe XXL. Hunde schlafen lieber mit dem Rücken an etwas — das ist der ganze Trick an der Form.

Hundesofa Samt XXL bei Homeeins.

https://www.homeeins.de/products/hundesofa-samt-erhoeht-xxl
```

**233 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 2. Schuhbank · wohnen

```
Sitzen und verstauen an derselben Stelle. Die Bank klappt auf, innen ist Platz für Schuhe, Decken oder was sonst im Flur herumliegt.

Gepolsterte Sitzbank mit Stauraum.

https://www.homeeins.de/products/schuhbank-sitzpolster-102cm-massiv
```

**240 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 3. Samt-Sessel · wohnen

```
Samt, Armlehnen, Holzbeine. Ein Sessel für die Ecke, in der bisher nur die Wäsche gelandet ist.

https://www.homeeins.de/products/samt-sessel-design-armlehnen-holzbeine
```

**168 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 4. Kratzbaum · haustiere

```
Kompakt gebaut, für Wohnungen ohne freie Wand. Plüschbezug, Liegefläche oben — Katzen wollen Höhe, nicht Fläche.

https://www.homeeins.de/products/kratzbaum-katzen-kompakt-plusch
```

**178 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 5. Bürostuhl · arbeiten

```
135 Grad Rückenlehne und eine ausziehbare Fußstütze. Für die Stunden nach Feierabend, in denen der Schreibtischstuhl ein Sessel sein soll.

https://www.homeeins.de/products/buerostuhl-premium-relaxfunktion-135-grad
```

**214 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 6. Magazinhalter · wohnen

```
Aufladbar, Zoom, zusätzliches Warnlicht. Liegt im Auto, bis man sie braucht.

https://www.homeeins.de/products/magazinhalter-holz-zeitungsstaender
```

**152 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 7. Kollektion Hunde · haustiere

```
Alles für den Hund an einer Stelle: Sofas, Betten, Zubehör.

Versand ist bei uns kostenlos.

https://www.homeeins.de/collections/hunde
```

**134 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 8. Flur · wohnen

```
Der Flur ist der Raum, den alle sehen und niemand einrichtet. Eine Bank mit Stauraum erledigt beides auf einem Quadratmeter.

https://www.homeeins.de/products/schuhbank-sitzpolster-102cm-massiv
```

**196 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 9. Samt · wohnen

```
Warum Samt: Er nimmt Licht anders an als Webstoff und lässt eine Ecke wärmer wirken, ohne dass man etwas umstellen muss.

https://www.homeeins.de/products/samt-sessel-design-armlehnen-holzbeine
```

**193 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 10. Katzenhöhe · haustiere

```
Katzen suchen den höchsten Punkt im Raum. Wenn der Kratzbaum ihn nicht bietet, ist es der Schrank.

https://www.homeeins.de/products/kratzbaum-katzen-kompakt-plusch
```

**164 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 11. Homeoffice · arbeiten

```
Ein Stuhl, der sich auf 135 Grad legen lässt, ist kein Luxus, sondern der Unterschied zwischen acht Stunden sitzen und acht Stunden aushalten.

https://www.homeeins.de/products/buerostuhl-premium-relaxfunktion-135-grad
```

**218 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

### 12. Hundeschlaf · haustiere

```
Hunde schlafen 12 bis 14 Stunden am Tag. Die Liegefläche ist damit das Möbelstück, das sie am längsten benutzen.

https://www.homeeins.de/products/hundesofa-samt-erhoeht-xxl
```

**173 Zeichen** · passt auf: bluesky, mastodon, telegram, discord, instagram

## So wird gesendet

```
Actions → Posten → Run workflow
  text:     <Text von oben>
  kanaele:  bluesky,mastodon,telegram,discord
  probe:    false
```

Für Instagram zusätzlich `bild` mit einer öffentlichen
`https`-Adresse — die Shopify-CDN-Adresse des Produktbilds.

## Geprüft am 22.10.2026

Drei Beiträge zeigten auf Produkte im **Entwurfsstatus** — für
Besucher eine tote Seite. Gegen den Shop abgeglichen und durch aktive
Produkte ersetzt (Schuhbank, Magazinhalter).

**Lehre:** Ein Produkt, das im Repository steht, ist deshalb noch
nicht im Laden sichtbar. Vor jedem Beitrag der Abgleich mit
`status:active`.

## Was fehlt

Nichts an den Texten. Es fehlt **ein einziger Zugang**, dann geht
der erste Beitrag raus.
