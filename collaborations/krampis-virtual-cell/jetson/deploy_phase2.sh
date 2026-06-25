#!/usr/bin/env bash
# Deploy Phase 2 split scout scripts to Jetson.
# Does NOT modify crontab — see install_scout_cron.example.sh
set -euo pipefail

JETSON="${JETSON:-gary@192.168.1.222}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE="/media/sdcard/scheduler"

echo "==> Deploy Phase 2 scout to ${JETSON}:${REMOTE}/scout"
ssh "${JETSON}" "mkdir -p ${REMOTE}/scout ${REMOTE}/scheduler /media/sdcard/logs"

scp "${SCRIPT_DIR}/firestore_config.py" \
    "${SCRIPT_DIR}/setup_firestore_collections.py" \
    "${SCRIPT_DIR}/check_scout_status.py" \
    "${JETSON}:${REMOTE}/"

scp "${SCRIPT_DIR}/scheduler/status_writer.py" \
    "${JETSON}:${REMOTE}/scheduler/"

scp "${SCRIPT_DIR}/scout/"*.py \
    "${SCRIPT_DIR}/scout/scout_ingest.sh" \
    "${JETSON}:${REMOTE}/scout/"

ssh "${JETSON}" "chmod +x ${REMOTE}/scout/scout_ingest.sh"

echo ""
echo "==> Dry-run PubMed scout (no acquire, status dry-run)"
ssh "${JETSON}" \
  "source /home/gary/.config/copernicus/env && \
   GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json \
   cd /home/gdubs/copernicus-web-public/huggingface-space && \
   /media/sdcard/copernicus-worker/venv/bin/python3.8 \
   ${REMOTE}/scout/scout_pubmed.py am --dry-run-status --no-glmp-queries"

echo ""
echo "Manual test (one source, no ingest):"
echo "  ssh ${JETSON} 'source ~/.config/copernicus/env && GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json cd /home/gdubs/copernicus-web-public/huggingface-space && /media/sdcard/copernicus-worker/venv/bin/python3.8 ${REMOTE}/scout/scout_pubmed.py am --no-glmp-queries'"
echo ""
echo "After all three AM scouts succeed, run ingest once:"
echo "  ssh ${JETSON} 'bash ${REMOTE}/scout/scout_ingest.sh'"
echo ""
echo "See scout/install_scout_cron.example.sh before replacing the 10:15 monolith cron."
