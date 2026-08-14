#!/usr/bin/env python3
"""
kontrast.py — misst den WCAG-Kontrast von Text über einem Bild.

Wozu: axe-core (in `pruefstand.py`) kann Text über einem *Bild* nicht
bewerten. Es kennt die Textfarbe, aber nicht den effektiven Hintergrund,
weil der aus Fotopixeln besteht. Genau deshalb tauchte der auffälligste
Fehler der Startseite — der unlesbare Hero — im Prüfstand nie auf.

Dieses Werkzeug schliesst die Lücke: Es liest die tatsächlichen Pixel im
angegebenen Bereich aus dem Screenshot und rechnet den Kontrast gegen die
Textfarbe aus.

**Was es NICHT kann:** Es findet den Text nicht selbst. Der Bereich wird
angegeben. Es unterscheidet Text- von Hintergrundpixeln nur über die
Farbähnlichkeit zur Textfarbe (`--toleranz`) — eine Heuristik, kein
OCR. Bei Bildern, die grossflächig die Textfarbe enthalten, wird zu viel
ausgeschlossen. Das ist eine bekannte Grenze, keine Nachlässigkeit.

Aufruf:
    python3 scripts/kontrast.py --bild bilder/startseite-mobil.jpg \\
        --bereich 0,150,780,400 --textfarbe "#FFFFFF"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

# WCAG 2.1: ab 4.5:1 gilt normaler Text als lesbar, grosser Text ab 3:1.
AA_NORMAL = 4.5
AA_GROSS = 3.0


def kanal_linear(wert: int) -> float:
    """sRGB-Kanal (0..255) in lineare Helligkeit. Formel aus WCAG 2.1."""
    c = wert / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def leuchtdichte(rgb: tuple[int, int, int]) -> float:
    r, g, b = (kanal_linear(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = leuchtdichte(a), leuchtdichte(b)
    hell, dunkel = max(la, lb), min(la, lb)
    return (hell + 0.05) / (dunkel + 0.05)


def farbe_lesen(text: str) -> tuple[int, int, int]:
    t = text.strip().lstrip("#")
    if len(t) == 3:
        t = "".join(ch * 2 for ch in t)
    if len(t) != 6:
        raise ValueError(f"Farbe nicht lesbar: {text!r} (erwartet #RRGGBB)")
    return tuple(int(t[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def abstand(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """Einfacher euklidischer RGB-Abstand, 0..441."""
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def messen(bildpfad: Path, bereich: tuple[int, int, int, int],
           textfarbe: tuple[int, int, int], toleranz: float) -> dict:
    from PIL import Image

    with Image.open(bildpfad) as im:
        im = im.convert("RGB")
        breite, hoehe = im.size
        x, y, w, h = bereich
        # Bereich auf das Bild begrenzen, statt bei Überstand abzustürzen.
        x, y = max(0, x), max(0, y)
        w, h = min(w, breite - x), min(h, hoehe - y)
        if w <= 0 or h <= 0:
            raise ValueError(
                f"Bereich {bereich} liegt ausserhalb des Bildes {breite}x{hoehe}")
        ausschnitt = im.crop((x, y, x + w, y + h))
        # tobytes() statt getdata(): getdata() ist ab Pillow 14 weg.
        roh = ausschnitt.tobytes()
        pixel = [tuple(roh[i:i + 3]) for i in range(0, len(roh), 3)]

    # Pixel, die der Textfarbe sehr ähnlich sind, gelten als Text selbst
    # und nicht als Hintergrund.
    hintergrund = [p for p in pixel if abstand(p, textfarbe) > toleranz]
    textpixel = len(pixel) - len(hintergrund)

    if not hintergrund:
        return {
            "fehler": "Alle Pixel im Bereich gleichen der Textfarbe — "
                      "kein Hintergrund messbar. Bereich oder Toleranz prüfen.",
            "pixel_gesamt": len(pixel),
        }

    werte = sorted(kontrast(textfarbe, p) for p in hintergrund)
    n = len(werte)

    def anteil_unter(schwelle: float) -> float:
        return round(100.0 * sum(1 for v in werte if v < schwelle) / n, 1)

    return {
        "bild": str(bildpfad),
        "bereich": {"x": x, "y": y, "breite": w, "hoehe": h},
        "textfarbe": "#%02X%02X%02X" % textfarbe,
        "pixel_gesamt": len(pixel),
        "pixel_als_text_ausgeschlossen": textpixel,
        "pixel_hintergrund": n,
        "kontrast_min": round(werte[0], 2),
        "kontrast_median": round(werte[n // 2], 2),
        "kontrast_max": round(werte[-1], 2),
        "anteil_unter_4_5_prozent": anteil_unter(AA_NORMAL),
        "anteil_unter_3_0_prozent": anteil_unter(AA_GROSS),
        # Urteil nach dem schlechtesten Pixel ist die strenge Lesart.
        # Sie ist bei Text ueber Bild aber unbrauchbar streng: Zwischen
        # weisser Schrift und dunklem Grund liegen immer
        # kantengeglaettete Uebergangspixel, die per Definition
        # dazwischen liegen. Die faellt kein Design weg.
        "urteil_streng": "bestanden" if werte[0] >= AA_NORMAL else "durchgefallen",
        # Deshalb zusaetzlich ein Flaechenurteil mit 2 % Zugestaendnis
        # fuer genau diese Kantenpixel. Ob eine Messung wirklich
        # Kantenglaettung zeigt oder echten zu hellen Grund, verraet die
        # Empfindlichkeitspruefung: --toleranz hochdrehen. Faellt der
        # Anteil dann steil, waren es Kanten. Bleibt er flach, ist der
        # Hintergrund wirklich zu hell. Am 14.08.2026 hat genau dieser
        # Test eine bequeme Ausrede widerlegt und eine Runde spaeter
        # eine echte Verbesserung bestaetigt.
        "urteil_flaeche_normal": "bestanden" if anteil_unter(AA_NORMAL) <= 2.0 else "durchgefallen",
        "urteil_flaeche_gross": "bestanden" if anteil_unter(AA_GROSS) <= 2.0 else "durchgefallen",
    }


def bericht(e: dict) -> str:
    if "fehler" in e:
        return f"\n**Nicht messbar:** {e['fehler']}\n"
    z = [
        "",
        f"### {Path(e['bild']).name} — Bereich "
        f"{e['bereich']['x']},{e['bereich']['y']} "
        f"{e['bereich']['breite']}×{e['bereich']['hoehe']}",
        "",
        f"Textfarbe {e['textfarbe']} · {e['pixel_hintergrund']} Hintergrundpixel "
        f"({e['pixel_als_text_ausgeschlossen']} als Text ausgeschlossen)",
        "",
        "| Kennwert | Wert |",
        "|---|---:|",
        f"| Kontrast schlechtester Pixel | **{e['kontrast_min']}:1** |",
        f"| Kontrast Median | {e['kontrast_median']}:1 |",
        f"| Kontrast bester Pixel | {e['kontrast_max']}:1 |",
        f"| Fläche unter 4,5:1 (normaler Text) | **{e['anteil_unter_4_5_prozent']} %** |",
        f"| Fläche unter 3,0:1 (grosser Text) | {e['anteil_unter_3_0_prozent']} % |",
        "",
        f"Streng (schlechtester Pixel): normaler Text "
        f"**{e['urteil_streng']}**",
        f"Nach Fläche (bis 2 % Kantenpixel zugestanden): normaler Text "
        f"**{e['urteil_flaeche_normal']}** · grosser Text "
        f"**{e['urteil_flaeche_gross']}**",
        "",
        "Weichen die beiden Urteile ab, `--toleranz` hochdrehen: Fällt der "
        "Anteil dann steil, waren es kantengeglättete Buchstabenränder. "
        "Bleibt er flach, ist der Hintergrund wirklich zu hell.",
        "",
    ]
    return "\n".join(z)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bild", required=True)
    ap.add_argument("--bereich", required=True,
                    help="x,y,breite,hoehe in Pixeln")
    ap.add_argument("--textfarbe", default="#FFFFFF")
    ap.add_argument("--toleranz", type=float, default=60.0,
                    help="RGB-Abstand, ab dem ein Pixel als Hintergrund gilt")
    ap.add_argument("--out", default="")
    a = ap.parse_args()

    teile = [int(t) for t in a.bereich.split(",")]
    if len(teile) != 4:
        raise SystemExit("--bereich braucht vier Zahlen: x,y,breite,hoehe")

    e = messen(Path(a.bild), tuple(teile), farbe_lesen(a.textfarbe),  # type: ignore[arg-type]
               a.toleranz)
    print(bericht(e))

    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(e, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"geschrieben: {p}")


if __name__ == "__main__":
    main()
