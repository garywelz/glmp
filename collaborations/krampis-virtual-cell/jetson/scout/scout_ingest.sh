#!/usr/bin/env bash
# Push metadata JSON to Firestore (research_papers). Safe to re-run.
set -euo pipefail

HFS="/home/gdubs/copernicus-web-public/huggingface-space"
source /home/gary/.config/copernicus/env
export GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json

mkdir -p /media/sdcard/logs
exec bash "${HFS}/scripts/ingest_metadata_to_firestore.sh" >> /media/sdcard/logs/scout_ingest.log 2>&1
