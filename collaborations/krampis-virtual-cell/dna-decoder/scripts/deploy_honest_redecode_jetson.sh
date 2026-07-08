#!/usr/bin/env bash
# Honest re-decode deploy on Jetson — JASPAR off for E. coli, parser v0.2.5.
set -euo pipefail

DECODER="/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder"
PY="/media/sdcard/miniforge3/envs/meme-env/bin/python3"

cd "$DECODER"
git pull --ff-only

export FIMO_BIN="/media/sdcard/miniforge3/envs/meme-env/bin/fimo"

echo "=== Honest re-decode (17 circuits, custom PWM only) ==="
"$PY" scripts/redecode_honest.py

echo "=== Done ==="
