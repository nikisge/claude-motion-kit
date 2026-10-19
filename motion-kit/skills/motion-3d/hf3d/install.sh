#!/usr/bin/env bash
# hf3d in ein HyperFrames-Projekt kopieren (lokal, keine Netz-Fetches beim Rendern).
#   bash <motion-3d>/hf3d/install.sh <hf-projektordner> [--template]
# Legt <hf>/vendor/hf3d/{hf3d.js,three/,fonts/} an. --template kopiert zusätzlich template.html nach <hf>/index.html
# (nur wenn dort noch keine eigene Komposition liegt). Nach Updates von hf3d.js erneut ausführen.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DST="${1:?Ziel: HyperFrames-Projektordner (mit index.html)}"
mkdir -p "$DST/vendor/hf3d"
rm -rf "$DST/vendor/hf3d/three" "$DST/vendor/hf3d/fonts"
cp "$SRC/hf3d.js" "$DST/vendor/hf3d/hf3d.js"
cp -R "$SRC/vendor/three" "$DST/vendor/hf3d/three"
cp -R "$SRC/fonts" "$DST/vendor/hf3d/fonts"
if [[ "${2:-}" == "--template" ]]; then
  if [[ -f "$DST/index.html" ]] && ! grep -q 'data-start="0" data-duration="10"' "$DST/index.html" && ! grep -q '>Title</h1>' "$DST/index.html"; then
    echo "index.html existiert schon (eigene Komposition) - Vorlage nicht kopiert: $SRC/template.html"
  else
    cp "$SRC/template.html" "$DST/index.html"; echo "Vorlage -> $DST/index.html"
  fi
fi
echo "hf3d installiert -> $DST/vendor/hf3d  (Importmap: siehe $SRC/README.md)"
