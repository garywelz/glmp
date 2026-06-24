#!/usr/bin/env bash
# Bootstrap CopernicusAI ingest worker on Jetson Nano (Ubuntu 18.04 LTS).
# Run on the Jetson as user gary after copying this script over SSH.
#
# What this does:
#   - Clones copernicus-web (default: SD card; use eMMC if SD is exFAT — git cannot run on exFAT)
#   - Symlinks legacy /home/gdubs/copernicus-web-public path used by acquisition scripts
#   - Creates a Python venv with minimal ingest dependencies
#   - Verifies GCP + OpenAI credentials
#
# Prerequisites (manual, before running):
#   1. GCP service account JSON at ~/.config/copernicus/gcp-sa.json
#   2. OPENAI_API_KEY in ~/.config/copernicus/env (export OPENAI_API_KEY=sk-...)
#   3. Optional: PUBMED_API_KEY in the same env file
#   4. GitHub SSH key or HTTPS access to github.com/garywelz/copernicus-web
#
# Usage:
#   bash bootstrap_ingest_worker.sh
#   bash bootstrap_ingest_worker.sh --skip-clone   # venv + symlinks only

set -euo pipefail

REPO_URL="${COPERNICUS_REPO_URL:-https://github.com/garywelz/copernicus-web.git}"
# exFAT SD cards cannot host git repos; on J1010 use:
#   COPERNICUS_SD_ROOT=/home/gary/copernicus-worker bash bootstrap_ingest_worker.sh
SD_ROOT="${COPERNICUS_SD_ROOT:-/home/gary/copernicus-worker}"
REPO_DIR="${SD_ROOT}/copernicus-web"
LEGACY_ROOT="/home/gdubs/copernicus-web-public"
HFS_DIR="${REPO_DIR}/huggingface-space"
VENV_DIR="${SD_ROOT}/venv"
ENV_FILE="${HOME}/.config/copernicus/env"
SA_FILE="${HOME}/.config/copernicus/gcp-sa.json"
SKIP_CLONE=0

for arg in "$@"; do
  case "$arg" in
    --skip-clone) SKIP_CLONE=1 ;;
    -h|--help)
      sed -n '2,20p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg" >&2
      exit 2
      ;;
  esac
done

echo "==> CopernicusAI Jetson ingest worker bootstrap"
echo "    SD root: ${SD_ROOT}"
echo "    Repo:    ${REPO_DIR}"

mkdir -p "${SD_ROOT}" "${HOME}/.config/copernicus"

if [ "${SKIP_CLONE}" -eq 0 ]; then
  if [ -d "${REPO_DIR}/.git" ]; then
    echo "==> Repo exists; pulling latest"
    git -C "${REPO_DIR}" pull --ff-only
  else
    echo "==> Cloning copernicus-web (must run on Linux — Windows checkout fails)"
    git clone --depth 1 "${REPO_URL}" "${REPO_DIR}"
  fi
fi

if [ ! -d "${HFS_DIR}" ]; then
  echo "❌ huggingface-space not found at ${HFS_DIR}" >&2
  exit 2
fi

echo "==> Legacy path symlink (acquisition scripts hardcode /home/gdubs/...)"
sudo mkdir -p /home/gdubs
if [ -e "${LEGACY_ROOT}" ] && [ ! -L "${LEGACY_ROOT}" ]; then
  echo "⚠️  ${LEGACY_ROOT} exists and is not a symlink; leaving as-is"
else
  sudo ln -sfn "${REPO_DIR}" "${LEGACY_ROOT}"
fi

PY=""
for candidate in python3.10 python3.9 python3.8 python3; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    ver="$("${candidate}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
    major="${ver%%.*}"
    minor="${ver#*.}"
    if [ "${major}" -ge 3 ] && [ "${minor}" -ge 8 ]; then
      PY="${candidate}"
      break
    fi
  fi
done

if [ -z "${PY}" ]; then
  echo "❌ Need Python 3.8+. Ubuntu 18.04 default is 3.6 — install deadsnakes:" >&2
  echo "   sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt update && sudo apt install -y python3.8 python3.8-venv python3.8-dev" >&2
  exit 2
fi

echo "==> Using ${PY}"
if [ ! -d "${VENV_DIR}" ]; then
  "${PY}" -m venv "${VENV_DIR}"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip wheel

pip install \
  biopython \
  google-cloud-firestore \
  google-auth \
  openai \
  requests \
  pdfplumber \
  PyPDF2

if [ -f "${ENV_FILE}" ]; then
  # shellcheck source=/dev/null
  set -a
  source "${ENV_FILE}"
  set +a
  echo "==> Loaded ${ENV_FILE}"
else
  echo "⚠️  Create ${ENV_FILE} with OPENAI_API_KEY (and optional PUBMED_API_KEY)"
fi

if [ -f "${SA_FILE}" ]; then
  export GOOGLE_APPLICATION_CREDENTIALS="${SA_FILE}"
  export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-regal-scholar-453620-r7}"
  export FIRESTORE_DATABASE="${FIRESTORE_DATABASE:-copernicusai}"
  echo "==> GCP credentials: ${SA_FILE}"
else
  echo "⚠️  Place service account JSON at ${SA_FILE}"
fi

cat <<EOF

============================================================
Bootstrap complete
============================================================

Activate worker venv:
  source ${VENV_DIR}/bin/activate
  [ -f ${ENV_FILE} ] && source ${ENV_FILE}
  export GOOGLE_APPLICATION_CREDENTIALS=${SA_FILE}

Smoke test — acquire 3 GLMP priority DOIs (copy list from glmp repo first):
  scp collaborations/krampis-virtual-cell/curated-doi-ingest-priority.txt gary@192.168.1.222:~/
  head -3 ~/curated-doi-ingest-priority.txt > /tmp/doi-smoke.txt
  cd ${LEGACY_ROOT}/huggingface-space/scripts/acquire_papers
  python3 acquire_crossref_batch.py --doi-file /tmp/doi-smoke.txt

Push new JSON metadata to Firestore (no embeddings):
  cd ${LEGACY_ROOT}/huggingface-space
  bash scripts/ingest_metadata_to_firestore.sh --dry-run
  bash scripts/ingest_metadata_to_firestore.sh

Daily scout (PubMed + arXiv recent papers):
  bash scripts/acquire_papers/run_daily_scout_with_ingest.sh

Not yet in repo (Jetson Phase 2):
  - Local OpenAI embedding before Firestore push (backfill_embeddings.py lives on Yoga, not in git)
  - PDF full-text extraction wired into acquisition
  - FIMO/MEME motif scanning for sequence_logic_content
  - glmp_relevant auto-tagging at ingest time

GCP project: regal-scholar-453620-r7
Firestore DB: copernicusai
Jetson SSH:   gary@192.168.1.222
EOF
