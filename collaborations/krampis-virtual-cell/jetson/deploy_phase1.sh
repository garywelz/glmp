#!/usr/bin/env bash
# Deploy Phase 1 scheduler scripts from glmp repo staging to Jetson SD paths.
# Run from Yoga: bash deploy_phase1.sh
# Requires: passwordless SSH to gary@192.168.1.222

set -euo pipefail

JETSON="${JETSON:-gary@192.168.1.222}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_SCHED="/media/sdcard/scheduler"

echo "==> Deploy Phase 1 to ${JETSON}:${REMOTE_SCHED}"
ssh "${JETSON}" "mkdir -p ${REMOTE_SCHED}/scheduler"

scp "${SCRIPT_DIR}/firestore_config.py" \
    "${JETSON}:${REMOTE_SCHED}/"

scp "${SCRIPT_DIR}/setup_firestore_collections.py" \
    "${JETSON}:${REMOTE_SCHED}/"

scp "${SCRIPT_DIR}/scheduler/status_writer.py" \
    "${JETSON}:${REMOTE_SCHED}/scheduler/"

echo "==> Dry-run Firestore setup (no writes)"
ssh "${JETSON}" \
  "source /home/gary/.config/copernicus/env && \
   export GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json && \
   /media/sdcard/copernicus-worker/venv/bin/python3.8 ${REMOTE_SCHED}/setup_firestore_collections.py"

echo ""
echo "If schema looks correct, apply seeds:"
echo "  ssh ${JETSON} 'source ~/.config/copernicus/env && GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json /media/sdcard/copernicus-worker/venv/bin/python3.8 ${REMOTE_SCHED}/setup_firestore_collections.py --apply'"
echo ""
echo "Test status_writer dry-run:"
echo "  ssh ${JETSON} '... python3.8 ${REMOTE_SCHED}/scheduler/status_writer.py --job-id phase1_smoke --status success --doc-count 0 --dry-run'"
