#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python3 scripts/check.py --assets
exec python3 scripts/runtime.py play "$@"
