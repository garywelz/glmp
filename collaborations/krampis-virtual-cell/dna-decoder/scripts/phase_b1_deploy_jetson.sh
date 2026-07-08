#!/usr/bin/env bash
# Phase B1 deploy on Jetson — lac re-anchor, guard, ara/trp coord sync, re-decode.
set -euo pipefail

DECODER="/media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder"
PY="/media/sdcard/miniforge3/envs/meme-env/bin/python3"

cd "$DECODER"
git pull --ff-only

export FIMO_BIN="/media/sdcard/miniforge3/envs/meme-env/bin/fimo"

echo "=== Phase B1 re-anchor ==="
"$PY" scripts/phase_b1_reanchor.py

echo "=== Done ==="
