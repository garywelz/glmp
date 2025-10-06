# GLMP Project - Deployment Guide

## Overview
This guide explains how to deploy the GLMP project files to Google Cloud Storage (GCS).

## Recent Updates
The "Standardize Yeast Biology charts" agent has created comprehensive biological process files including:
- E. coli batch files (15 processes)
- Yeast batch files (23 processes)
- Biological processes directory with organized content
- Templates and scripts for process generation

## Deployment Target
- **GCS Bucket**: `regal-scholar-453620-r7-podcast-storage`
- **Base Path**: `glmp/`
- **Public URL**: `https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/`

## Quick Deployment

### Option 1: Using the Deployment Script (Recommended)

```bash
# Run the deployment script
./deploy_to_gcs.sh
```

The script will:
1. Check authentication and permissions
2. Verify bucket access
3. Upload all project files
4. Set public read permissions
5. Configure cache headers

### Option 2: Manual Deployment

```bash
# Set environment
export PATH="/workspace/glmp/google-cloud-sdk/bin:$PATH"

# Authenticate (if needed)
gcloud auth login

# Set project
gcloud config set project regal-scholar-453620-r7

# Deploy files
gsutil -m cp -r biological_processes/* gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
gsutil -m cp *.html gs://regal-scholar-453620-r7-podcast-storage/glmp/
gsutil -m cp -r collections/* gs://regal-scholar-453620-r7-podcast-storage/glmp/collections/
gsutil -m cp -r docs/* gs://regal-scholar-453620-r7-podcast-storage/glmp/docs/

# Set public access
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/**/*.html
```

### Option 3: Deploy Specific Files Only

```bash
# Deploy just the biological processes (new content from standardization)
gsutil -m cp -r biological_processes/* gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/

# Deploy E. coli files
gsutil -m cp ecoli_batch*.html gs://regal-scholar-453620-r7-podcast-storage/glmp/

# Deploy yeast files
gsutil -m cp yeast_batch*.html gs://regal-scholar-453620-r7-podcast-storage/glmp/
```

## Files to Deploy

### Priority 1: New Biological Process Files
These are the main outputs from the "Standardize Yeast Biology charts" work:

```
biological_processes/
├── ecoli/
│   ├── ecoli_batch01_dna_replication_repair.html
│   ├── ecoli_batch02_cell_division_segregation.html
│   ├── ecoli_batch03_translation_protein_synthesis.html
│   ├── ... (15 total E. coli files)
├── yeast/
│   ├── yeast_batch01_dna_replication_repair.html
│   ├── yeast_batch02_cell_cycle_control.html
│   ├── yeast_batch03_protein_synthesis.html
│   ├── ... (23 total yeast files)
├── index.html
└── templates/
```

### Priority 2: Supporting Files
```
- index.html
- GLMP_Foundation.html
- README.md
- dataset_info.json
- process_inventory.csv
```

### Priority 3: Documentation and Collections
```
- collections/
- docs/
- A_Programming_Framework_for_Systematic_Analysis_of_Complex_Systems.md
```

## Verification

After deployment, verify the files are accessible:

```bash
# Check a few key files
curl -I https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/index.html
curl -I https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/index.html
curl -I https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/yeast/yeast_batch01_dna_replication_repair.html
```

## Troubleshooting

### Authentication Issues
If you get authentication errors:
```bash
gcloud auth login
gcloud auth application-default login
```

### Permission Issues
If you can't access the bucket:
```bash
# Check your permissions
gsutil iam get gs://regal-scholar-453620-r7-podcast-storage

# Verify you're using the correct account
gcloud auth list
```

### File Access Issues
If deployed files aren't publicly accessible:
```bash
# Set public read on all HTML files
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/**/*.html

# Or for specific directories
gsutil -m acl ch -r -u AllUsers:R gs://regal-scholar-453620-r7-podcast-storage/glmp/biological_processes/
```

## Performance Optimization

Set cache headers for better performance:
```bash
# HTML files - 1 hour cache
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp/**/*.html

# JSON/CSV files - 24 hour cache
gsutil -m setmeta -h "Cache-Control:public, max-age=86400" \
  gs://regal-scholar-453620-r7-podcast-storage/glmp/**/*.json
```

## Git Integration

After successful deployment, commit the deployment scripts:
```bash
git add deploy_to_gcs.sh DEPLOYMENT_GUIDE.md
git commit -m "Add GCS deployment scripts and guide"
```

## Summary

The deployment script (`deploy_to_gcs.sh`) automates all of these steps. Simply run it when you have GCS access configured, and it will handle:
- ✅ Authentication verification
- ✅ File uploads
- ✅ Permission settings
- ✅ Cache configuration
- ✅ Deployment verification

For immediate deployment of just the standardized biology files:
```bash
cd /workspace
gsutil -m cp -r biological_processes gs://regal-scholar-453620-r7-podcast-storage/glmp/
```
