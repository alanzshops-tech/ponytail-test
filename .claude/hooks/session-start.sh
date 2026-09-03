#!/bin/bash
set -euo pipefail

# Installiert, was die Skripte in scripts/ zum Laufen brauchen, damit
# Tests (die probe_*.py-Dateien, tests/test_kassetten.py) und die
# Hauptskripte direkt importierbar sind -- ohne dass jede Sitzung neu
# pip install ausfuehren muss.
#
# Die meisten Pakete sind in dieser Arbeitsumgebung schon vorhanden
# (playwright, pandas, pytrends, pyyaml, vcrpy, requests, trafilatura,
# faster-whisper, Pillow, piper-tts). Fehlen nur noch die beiden
# Google-API-Pakete, die scripts/gsc.py fuer die Search-Console-Anbindung
# braucht.
pip install --quiet google-api-python-client google-auth

# Chromium liegt in dieser Umgebung schon unter /opt/pw-browsers --
# kein "playwright install" noetig, das wuerde nur unnoetig neu laden.
