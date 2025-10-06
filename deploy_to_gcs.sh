#!/bin/bash
# GLMP Project - Google Cloud Storage Deployment Script
# This script deploys the GLMP project files to Google Cloud Storage
# 
# Prerequisites:
# 1. Google Cloud SDK installed (gcloud)
# 2. Authenticated with GCS (gcloud auth login)
# 3. Project configured (gcloud config set project PROJECT_ID)

set -e  # Exit on error

# Configuration
GCS_BUCKET="regal-scholar-453620-r7-podcast-storage"
GCS_BASE_PATH="glmp"
PROJECT_ROOT="/workspace"

# Color output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GLMP Project - GCS Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed or not in PATH${NC}"
    echo "Please install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check authentication
echo -e "${YELLOW}Checking authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with Google Cloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
echo -e "${GREEN}✓ Authenticated as: ${ACTIVE_ACCOUNT}${NC}"

# Check project configuration
echo -e "${YELLOW}Checking project configuration...${NC}"
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -z "$CURRENT_PROJECT" ]; then
    echo -e "${RED}Error: No project configured${NC}"
    echo "Please run: gcloud config set project PROJECT_ID"
    exit 1
fi
echo -e "${GREEN}✓ Using project: ${CURRENT_PROJECT}${NC}"

# Verify bucket exists
echo -e "${YELLOW}Verifying GCS bucket...${NC}"
if ! gsutil ls "gs://${GCS_BUCKET}" &> /dev/null; then
    echo -e "${RED}Error: Cannot access bucket gs://${GCS_BUCKET}${NC}"
    echo "Please check bucket name and permissions"
    exit 1
fi
echo -e "${GREEN}✓ Bucket accessible: gs://${GCS_BUCKET}${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to upload files
upload_files() {
    local source_path="$1"
    local gcs_path="$2"
    local description="$3"
    
    echo -e "${YELLOW}Uploading ${description}...${NC}"
    
    if [ -f "$source_path" ]; then
        # Single file
        gsutil -m cp "$source_path" "gs://${GCS_BUCKET}/${gcs_path}"
        echo -e "${GREEN}✓ Uploaded: $source_path${NC}"
    elif [ -d "$source_path" ]; then
        # Directory - recursive upload
        gsutil -m cp -r "$source_path"/* "gs://${GCS_BUCKET}/${gcs_path}/"
        echo -e "${GREEN}✓ Uploaded: $source_path (directory)${NC}"
    else
        echo -e "${RED}✗ Not found: $source_path${NC}"
        return 1
    fi
}

# Deploy main HTML files
echo -e "${BLUE}1. Deploying main HTML files...${NC}"
upload_files "$PROJECT_ROOT/index.html" "$GCS_BASE_PATH/index.html" "Main index page"
upload_files "$PROJECT_ROOT/GLMP_Foundation.html" "$GCS_BASE_PATH/GLMP_Foundation.html" "Foundation page"

# Deploy biological processes
echo ""
echo -e "${BLUE}2. Deploying biological processes...${NC}"
upload_files "$PROJECT_ROOT/biological_processes" "$GCS_BASE_PATH/biological_processes" "Biological processes directory"

# Deploy E. coli batch files (from standardization work)
echo ""
echo -e "${BLUE}3. Deploying E. coli batch files...${NC}"
for file in ecoli_batch*.html; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        upload_files "$PROJECT_ROOT/$file" "$GCS_BASE_PATH/$file" "E. coli file: $file"
    fi
done

# Deploy yeast batch files
echo ""
echo -e "${BLUE}4. Deploying yeast batch files...${NC}"
for file in yeast_batch*.html; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        upload_files "$PROJECT_ROOT/$file" "$GCS_BASE_PATH/$file" "Yeast file: $file"
    fi
done

# Deploy collections
echo ""
echo -e "${BLUE}5. Deploying collections...${NC}"
upload_files "$PROJECT_ROOT/collections" "$GCS_BASE_PATH/collections" "Collections directory"

# Deploy documentation
echo ""
echo -e "${BLUE}6. Deploying documentation...${NC}"
upload_files "$PROJECT_ROOT/docs" "$GCS_BASE_PATH/docs" "Documentation directory"

# Deploy key markdown files
echo ""
echo -e "${BLUE}7. Deploying key documentation files...${NC}"
upload_files "$PROJECT_ROOT/README.md" "$GCS_BASE_PATH/README.md" "README"
upload_files "$PROJECT_ROOT/A_Programming_Framework_for_Systematic_Analysis_of_Complex_Systems.md" "$GCS_BASE_PATH/A_Programming_Framework_for_Systematic_Analysis_of_Complex_Systems.md" "Programming Framework"

# Deploy dataset files
echo ""
echo -e "${BLUE}8. Deploying dataset files...${NC}"
upload_files "$PROJECT_ROOT/dataset_info.json" "$GCS_BASE_PATH/dataset_info.json" "Dataset info"
upload_files "$PROJECT_ROOT/process_inventory.csv" "$GCS_BASE_PATH/process_inventory.csv" "Process inventory"

# Set public read access for HTML files
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Setting Public Access Permissions${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Making HTML files publicly accessible...${NC}"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_BASE_PATH}/**/*.html"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_BASE_PATH}/**/*.json"
gsutil -m acl ch -r -u AllUsers:R "gs://${GCS_BUCKET}/${GCS_BASE_PATH}/**/*.csv"
echo -e "${GREEN}✓ Public access configured${NC}"

# Set cache control for better performance
echo ""
echo -e "${YELLOW}Setting cache control headers...${NC}"
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://${GCS_BUCKET}/${GCS_BASE_PATH}/**/*.html"
gsutil -m setmeta -h "Cache-Control:public, max-age=86400" "gs://${GCS_BUCKET}/${GCS_BASE_PATH}/**/*.json"
echo -e "${GREEN}✓ Cache headers configured${NC}"

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Files deployed to: ${YELLOW}gs://${GCS_BUCKET}/${GCS_BASE_PATH}/${NC}"
echo ""
echo -e "Access your files at:"
echo -e "${BLUE}https://storage.googleapis.com/${GCS_BUCKET}/${GCS_BASE_PATH}/index.html${NC}"
echo ""
echo -e "${GREEN}Deployment completed successfully!${NC}"
