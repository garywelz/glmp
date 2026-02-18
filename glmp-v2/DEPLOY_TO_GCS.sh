#!/bin/bash
# GLMP v2 - Deployment Script for Google Cloud Storage
# Run this script with proper GCS authentication

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          GLMP v2 - Google Cloud Storage Deployment          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
GCS_BUCKET="regal-scholar-453620-r7-podcast-storage"
GCS_PATH="glmp-v2"
PROJECT_ID="regal-scholar-453620-r7"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Bucket: gs://${GCS_BUCKET}"
echo "  Path: ${GCS_PATH}/"
echo "  Project: ${PROJECT_ID}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not found${NC}"
    echo "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓${NC} gcloud CLI found"

# Check if gsutil is available
if ! command -v gsutil &> /dev/null; then
    echo -e "${RED}Error: gsutil not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} gsutil found"

# Check authentication
echo ""
echo -e "${YELLOW}Checking authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with Google Cloud${NC}"
    echo ""
    echo "Please authenticate first:"
    echo "  Option 1: User account"
    echo "    gcloud auth login"
    echo ""
    echo "  Option 2: Service account"
    echo "    gcloud auth activate-service-account --key-file=YOUR_KEY.json"
    exit 1
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1)
echo -e "${GREEN}✓${NC} Authenticated as: ${ACTIVE_ACCOUNT}"

# Set project
echo ""
echo -e "${YELLOW}Setting project...${NC}"
gcloud config set project ${PROJECT_ID} --quiet
echo -e "${GREEN}✓${NC} Project set to: ${PROJECT_ID}"

# Verify bucket access
echo ""
echo -e "${YELLOW}Verifying bucket access...${NC}"
if ! gsutil ls "gs://${GCS_BUCKET}" &> /dev/null; then
    echo -e "${RED}Error: Cannot access bucket gs://${GCS_BUCKET}${NC}"
    echo "Please check permissions"
    exit 1
fi
echo -e "${GREEN}✓${NC} Bucket accessible"

# Start deployment
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    Starting Deployment                       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Deploy viewer
echo -e "${YELLOW}[1/4] Deploying viewer...${NC}"
gsutil -m cp -r viewer/* "gs://${GCS_BUCKET}/${GCS_PATH}/viewer/"
echo -e "${GREEN}✓${NC} Viewer deployed"

# Deploy processes
echo ""
echo -e "${YELLOW}[2/4] Deploying processes...${NC}"
gsutil -m cp -r processes/* "gs://${GCS_BUCKET}/${GCS_PATH}/processes/"
echo -e "${GREEN}✓${NC} Processes deployed (4 files)"

# Deploy data files
echo ""
echo -e "${YELLOW}[3/4] Deploying data files...${NC}"
gsutil -m cp -r data/* "gs://${GCS_BUCKET}/${GCS_PATH}/data/"
echo -e "${GREEN}✓${NC} Data files deployed"

# Deploy README
echo ""
echo -e "${YELLOW}Deploying README...${NC}"
gsutil cp README.md "gs://${GCS_BUCKET}/${GCS_PATH}/README.md"
echo -e "${GREEN}✓${NC} README deployed"

# Set public access
echo ""
echo -e "${YELLOW}[4/4] Setting public access permissions...${NC}"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_PATH}/viewer/"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_PATH}/processes/"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_PATH}/data/"
gsutil acl ch -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_PATH}/README.md"
echo -e "${GREEN}✓${NC} Public access configured"

# Set cache control headers
echo ""
echo -e "${YELLOW}Setting cache control headers...${NC}"
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.html"
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.js"
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://${GCS_BUCKET}/${GCS_PATH}/viewer/*.css"
gsutil -m setmeta -h "Cache-Control:public, max-age=86400" "gs://${GCS_BUCKET}/${GCS_PATH}/processes/**/*.json"
gsutil -m setmeta -h "Cache-Control:public, max-age=86400" "gs://${GCS_BUCKET}/${GCS_PATH}/data/*.json"
echo -e "${GREEN}✓${NC} Cache headers configured"

# Deployment complete
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✓ Deployment Complete!                      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Display URLs
echo -e "${YELLOW}Your GLMP v2 Viewer is now live at:${NC}"
echo ""
echo -e "${GREEN}Main Viewer:${NC}"
echo "  https://storage.googleapis.com/${GCS_BUCKET}/${GCS_PATH}/viewer/index.html"
echo ""
echo -e "${GREEN}Direct Process Links:${NC}"
echo "  Lac Operon:"
echo "    https://storage.googleapis.com/${GCS_BUCKET}/${GCS_PATH}/viewer/index.html?process=ecoli_lac_operon"
echo ""
echo "  DNA Replication:"
echo "    https://storage.googleapis.com/${GCS_BUCKET}/${GCS_PATH}/viewer/index.html?process=ecoli_dna_replication_initiation"
echo ""
echo "  Transcription:"
echo "    https://storage.googleapis.com/${GCS_BUCKET}/${GCS_PATH}/viewer/index.html?process=ecoli_transcription_regulation"
echo ""
echo "  Cell Cycle:"
echo "    https://storage.googleapis.com/${GCS_BUCKET}/${GCS_PATH}/viewer/index.html?process=yeast_cell_cycle_control"
echo ""

# List deployed files
echo -e "${YELLOW}Deployed files:${NC}"
gsutil ls -lh "gs://${GCS_BUCKET}/${GCS_PATH}/**" | grep -E "\.(html|js|css|json|md)$" | head -20

echo ""
echo -e "${GREEN}Deployment successful!${NC} 🎉"
echo ""
