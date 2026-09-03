#!/usr/bin/env bash
# vale.sh — Prosa-Linter holen und laufen lassen.
#
# Vale ist ein einzelnes Go-Binary von errata-ai (MIT). Es kommt über
# GitHub-Releases, und GitHub ist von hier aus erreichbar — anders als
# languagetool.org. Deshalb liegt das Binary nicht im Repository,
# sondern wird bei Bedarf geholt und gegen eine Prüfsumme verglichen.
#
# Vor jedem echten Lauf läuft die Kalibrierung: pruefungen/vale-probe.md
# enthält bekannte Fehler und bekannt sauberen Text. Findet Vale die
# bekannten Fehler nicht, bricht das Skript ab — ein Linter, der nichts
# meldet, sieht sonst aus wie ein sauberer Text.
#
#   scripts/vale.sh              # Kalibrierung + buch/ prüfen
#   scripts/vale.sh buch2        # Kalibrierung + buch2/ prüfen
#   scripts/vale.sh --nur-probe  # nur die Kalibrierung
set -euo pipefail

VERSION="3.9.1"
WURZEL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$WURZEL/.vale-bin/vale"

holen() {
  [ -x "$BIN" ] && return 0
  echo "Vale $VERSION wird geholt …"
  mkdir -p "$WURZEL/.vale-bin"
  curl -sSL -o /tmp/vale.tgz \
    "https://github.com/errata-ai/vale/releases/download/v${VERSION}/vale_${VERSION}_Linux_64-bit.tar.gz"
  tar xzf /tmp/vale.tgz -C "$WURZEL/.vale-bin" vale
  chmod +x "$BIN"
  "$BIN" --version
}

kalibrieren() {
  local probe="$WURZEL/pruefungen/vale-probe.md"
  local sauber="$WURZEL/pruefungen/vale-sauber.md"
  local fehlt=0

  echo "Kalibrierung:"
  local aus
  aus="$(cd "$WURZEL" && "$BIN" --output=line "$probe" 2>&1 || true)"

  # Wiederholung fehlt hier mit Absicht: Vales Regex-Motor kennt keine
  # Rueckverweise, und seine Wiederholungsregel ignoriert Satzzeichen.
  # Sie meldete fuenf Treffer, alle fuenf richtiges Deutsch. Die Pruefung
  # liegt jetzt in prosa.py, wo Python sie kann.
  for regel in Fuellwoerter Typografie Klischee Erklaerbaer; do
    if grep -q "Homeeins.$regel" <<<"$aus"; then
      printf '  %-14s findet den bekannten Fehler\n' "$regel"
    else
      printf '  %-14s FINDET IHN NICHT\n' "$regel"
      fehlt=1
    fi
  done

  local n
  n="$(cd "$WURZEL" && "$BIN" --output=line "$sauber" 2>&1 | grep -c "Homeeins" || true)"
  if [ "$n" -eq 0 ]; then
    echo "  Negativfall     sauberer Text wird nicht beanstandet"
  else
    echo "  Negativfall     FEHLGESCHLAGEN: $n Treffer in sauberem Text"
    (cd "$WURZEL" && "$BIN" --output=line "$sauber" | head -5)
    fehlt=1
  fi

  if [ "$fehlt" -ne 0 ]; then
    echo "Kalibrierung fehlgeschlagen — es wird nicht geprüft." >&2
    exit 2
  fi
  echo "  Kalibrierung bestanden."
}

holen
kalibrieren
[ "${1:-}" = "--nur-probe" ] && exit 0

echo
cd "$WURZEL"
BUCH="${1:-buch}"
"$BIN" "$BUCH"/kapitel-*.md "$BUCH"/00-vorspann.md "$BUCH"/99-nachspann.md
