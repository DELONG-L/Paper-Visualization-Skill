#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$ROOT_DIR/site/"
DST_DIR="$ROOT_DIR/package/"

python3 "$ROOT_DIR/scripts/render_demo.py"

if [ -f "$ROOT_DIR/scripts/materialize_page_metadata.py" ]; then
  python3 "$ROOT_DIR/scripts/materialize_page_metadata.py" "$SRC_DIR" --config-name "paper-visualization.config.json" --locale-dir "zh"
fi

mkdir -p "$DST_DIR"
rsync -av --delete "$SRC_DIR" "$DST_DIR"
cp "$ROOT_DIR/../../LICENSE" "$DST_DIR/LICENSE"

echo "Site package synced to: $DST_DIR"
