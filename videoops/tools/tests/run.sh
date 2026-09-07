#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_media_contracts.py --check
python3 scripts/sync_package_schemas.py --check
python3 -m unittest discover -s tests -p 'test_*.py' -v
./bin/videoops --help >/dev/null
