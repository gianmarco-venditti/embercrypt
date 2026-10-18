#!/usr/bin/env bash
# Download the official, pinned bundle into this project. No system installation.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p .runtime/downloads
bundle="$PWD/.runtime/downloads/flare-linux64-v1.15.AppImage"
url='https://github.com/flareteam/flare-game/releases/download/v1.15/flare-linux64-v1.15.AppImage'
if [[ ! -s "$bundle" ]]; then
  printf 'Scarico Flare 1.15 ufficiale (circa 580 MB). Nessuna installazione di sistema.\n'
  curl --proto '=https' --tlsv1.2 --fail --location --retry 2 --connect-timeout 20 "$url" -o "$bundle.part"
  mv -- "$bundle.part" "$bundle"
fi
python3 scripts/runtime.py install "$bundle"
python3 scripts/check.py --assets
printf '\nPreparazione completata. Avvia con: ./play.sh\n'
