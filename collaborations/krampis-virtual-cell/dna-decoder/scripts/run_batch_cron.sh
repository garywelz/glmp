#!/bin/bash
. /home/gary/.config/copernicus/env
export GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json
export PATH="/media/sdcard/miniforge3/envs/meme-env/bin:$PATH"
cd /media/sdcard/glmp/collaborations/krampis-virtual-cell/dna-decoder
/media/sdcard/miniforge3/envs/meme-env/bin/python3 scripts/run_batch.py --limit 10
