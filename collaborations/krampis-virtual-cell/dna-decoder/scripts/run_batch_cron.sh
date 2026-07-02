#!/bin/bash
. /home/gary/.config/copernicus/env
export GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json
export PATH="/media/sdcard/miniforge3/envs/meme-env/bin:$PATH"
cd /media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder
LOG="/media/sdcard/logs/batch_decoder_$(date +%Y%m%d).log"
exec >> "$LOG" 2>&1
echo "=== batch decode start $(date -Iseconds) ==="
/media/sdcard/miniforge3/envs/meme-env/bin/python3 scripts/run_batch.py --limit 11
echo "=== batch decode end $(date -Iseconds) ==="
