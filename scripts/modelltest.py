"""MODEL-CONNECTION-TEST — welcher Gateway, welches Modell, welcher Weg?

Beantwortet eine Frage eindeutig: worueber laeuft Claude Code gerade, und
welche fremden Modelle sind von hier aus erreichbar.

Zeigt NIE einen Schluesselwert. Nur ob gesetzt, wie lang, und die letzten
drei Zeichen zur Wiedererkennung -- das reicht, um zwei Schluessel
auseinanderzuhalten, und genuegt niemandem, der ihn stehlen will.

    python3 scripts/modelltest.py            # Bestandsaufnahme
    python3 scripts/modelltest.py --fremd    # zusaetzlich OpenRouter pruefen
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from urllib.parse import urlsplit

# Reihenfolge zaehlt: Claude Code waehlt den Anbieter nach dieser Rangfolge.
PROVIDER = [
    ("CLAUDE_CODE_USE_BEDROCK", "Amazon Bedrock", "ANTHROPIC_BEDROCK_BASE_URL"),
    ("CLAUDE_CODE_USE_VERTEX", "Google Agent Platform", "ANTHROPIC_VERTEX_BASE_URL"),
    ("CLAUDE_CODE_USE_FOUNDRY", "Microsoft Foundry", "ANTHROPIC_FOUNDRY_BASE_URL"),
]

GEHEIM = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "OPENROUTER_API_KEY",
          "OPEN_ROUTER", "OPENAI_API_KEY")


def verdeckt(name: str) -> str:
    """Gesetzt ja/nein, Laenge, letzte drei Zeichen. Nie mehr."""
    w = os.environ.get(name)
    if not w:
        return "nicht gesetzt"
    return f"gesetzt · {len(w)} Zeichen · endet auf …{w[-3:]}"


def host(url: str | None) -> str:
    if not url:
        return "–"
    t = urlsplit(url)
    return f"{t.scheme}://{t.netloc}" if t.netloc else url


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fremd", action="store_true",
                    help="zusätzlich prüfen, welche Modelle OpenRouter bietet")
    a = ap.parse_args()

    print("=" * 62)
    print("  MODEL-CONNECTION-TEST")
    print("=" * 62)

    # --- 1. Claude Code selbst -------------------------------------
    print("\n[1] Claude Code")
    pfad = shutil.which("claude")
    if pfad:
        try:
            v = subprocess.run([pfad, "--version"], capture_output=True,
                               text=True, timeout=20).stdout.strip()
        except Exception:                                    # noqa: BLE001
            v = "Version nicht abfragbar"
        print(f"    installiert: {pfad}")
        print(f"    Version:     {v}")
    else:
        print("    NICHT im PATH gefunden")

    # --- 2. Welcher Gateway? ---------------------------------------
    print("\n[2] Gateway")
    aktiv = None
    for schalter, name, urlvar in PROVIDER:
        if os.environ.get(schalter):
            aktiv = (name, os.environ.get(urlvar))
            break
    basis = os.environ.get("ANTHROPIC_BASE_URL")
    if aktiv:
        print(f"    {aktiv[0]}  ({host(aktiv[1])})")
    elif basis:
        # Nur der Host, nie Pfad oder Query -- dort koennen Token stehen.
        print(f"    eigener Gateway über ANTHROPIC_BASE_URL: {host(basis)}")
        print("    (Anthropic-Messages-Format)")
    else:
        print("    Standard: api.anthropic.com")

    # --- 3. Zugangsdaten -------------------------------------------
    print("\n[3] Zugangsdaten (Werte werden nie angezeigt)")
    for n in GEHEIM:
        print(f"    {n:<22} {verdeckt(n)}")
    if not any(os.environ.get(n) for n in
               ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")):
        print("    -> keine Schlüsselvariable: es gilt die claude.ai-Anmeldung")

    # --- 4. Modellwahl ---------------------------------------------
    print("\n[4] Modell")
    for n in ("ANTHROPIC_MODEL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
              "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL",
              "ANTHROPIC_SMALL_FAST_MODEL"):
        print(f"    {n:<30} {os.environ.get(n) or 'nicht gesetzt'}")
    print("    Umschalten im Gespräch: /model")

    # --- 5. Fremde Modelle als Werkzeug ----------------------------
    print("\n[5] Fremde Modelle (nicht als Claude-Code-Motor, sondern als Werkzeug)")
    if not os.environ.get("OPENROUTER_API_KEY"):
        print("    OPENROUTER_API_KEY nicht gesetzt.")
        print("    Weg: GitHub-Actions-Lauf 'OpenRouter' (Secret OPEN_ROUTER),")
        print("         oder lokal OPENROUTER_API_KEY setzen.")
    elif not a.fremd:
        print("    OPENROUTER_API_KEY gesetzt. Mit --fremd wirklich abfragen.")
    else:
        try:
            import openrouter as o                           # noqa: PLC0415
        except ImportError:
            import importlib.util
            import sys
            from pathlib import Path
            s = importlib.util.spec_from_file_location(
                "openrouter", Path(__file__).parent / "openrouter.py")
            o = importlib.util.module_from_spec(s)
            sys.argv = ["modelltest"]
            s.loader.exec_module(o)
        r = o.rufen("/models")
        liste = r.get("data") if isinstance(r, dict) else None
        if not isinstance(liste, list):
            print(f"    Abfrage fehlgeschlagen: {r.get('fehler', r)}")
            return 1
        frei = [m for m in liste if sum(o.preis(m)) == 0]
        print(f"    {len(liste)} Modelle erreichbar, davon {len(frei)} ohne Kosten")

    print("\n" + "=" * 62)
    print("  Anthropic unterstützt für Claude Code selbst nur Claude-Modelle.")
    print("  Fremde Modelle laufen als Werkzeug, nicht als Motor. Siehe")
    print("  README_SETUP.md.")
    print("=" * 62)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
