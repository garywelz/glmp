#!/bin/bash
# Deploy Batch 9: glmp-v2 viewer/processes/data + database table to GCS
set -euo pipefail

export PATH="${HOME}/google-cloud-sdk/bin:${PATH}"
# Windows Git Bash: Google Cloud SDK default install location
if [[ -d "${LOCALAPPDATA:-}/Google/Cloud SDK/google-cloud-sdk/bin" ]]; then
  WIN_GCLOUD_BIN="$(cygpath -u "${LOCALAPPDATA}/Google/Cloud SDK/google-cloud-sdk/bin" 2>/dev/null || echo "/c/Users/${USER}/AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin")"
  export PATH="${WIN_GCLOUD_BIN}:${PATH}"
fi

GCS_BUCKET="regal-scholar-453620-r7-podcast-storage"
PROJECT_ID="regal-scholar-453620-r7"
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "=== GLMP Batch 9 full deploy ==="
echo "Repo: ${REPO_ROOT}"
echo "Branch: $(git -C "${REPO_ROOT}" branch --show-current)"

if ! command -v gcloud >/dev/null 2>&1; then
  echo "ERROR: gcloud not found. Install Google Cloud SDK first."
  exit 1
fi

if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q .; then
  echo "ERROR: Not authenticated. Run:"
  echo "  gcloud auth login --no-launch-browser"
  echo "  gcloud config set project ${PROJECT_ID}"
  exit 1
fi

gcloud config set project "${PROJECT_ID}" --quiet
echo "Authenticated as: $(gcloud auth list --filter=status:ACTIVE --format='value(account)' | head -1)"

cd "${REPO_ROOT}/glmp-v2"
./DEPLOY_TO_GCS.sh

cd "${REPO_ROOT}"
echo ""
echo "=== Uploading database table ==="
gsutil cp glmp-database-table.html "gs://${GCS_BUCKET}/glmp-database-table.html"
gsutil setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" "gs://${GCS_BUCKET}/glmp-database-table.html"

echo ""
echo "=== Deploy complete ==="
echo "Viewer:  https://storage.googleapis.com/${GCS_BUCKET}/glmp-v2/viewer/index.html"
echo "Table:   https://storage.googleapis.com/${GCS_BUCKET}/glmp-database-table.html"
echo "Processes: $(find "${REPO_ROOT}/glmp-v2/processes" -name '*.json' 2>/dev/null | wc -l | tr -d ' ') (deploy from main)"
