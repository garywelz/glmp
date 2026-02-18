# GLMP Cloud Service

Biological Process Generator & Validator running on Google Cloud Run

## Features

### Phase 1 (Current):
- ✅ Health check endpoint
- ✅ List all processes
- ✅ Retrieve specific process
- ✅ Basic validation
- ✅ GCS integration
- ✅ Secret Manager integration

### Phase 2 (Coming):
- 🔄 Vertex AI process generation
- 🔄 ArXiv literature enrichment
- 🔄 PubMed citation validation
- 🔄 Automated quality checks

## API Endpoints

### Health & Info
- `GET /` - Service info
- `GET /health` - Health check

### Process Management
- `GET /api/processes` - List all processes
- `GET /api/process/<id>` - Get specific process
- `POST /api/validate` - Validate a process

### Coming Soon
- `POST /api/generate` - Generate new process
- `POST /api/enrich` - Enrich with recent literature

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_ID=regal-scholar-453620-r7
export BUCKET_NAME=regal-scholar-453620-r7-podcast-storage
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Run locally
python main.py
```

## Deployment to Cloud Run

### Option 1: Using gcloud CLI

```bash
# Deploy directly
gcloud run deploy glmp-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage
```

### Option 2: Using Cloud Build

```bash
# Trigger build
gcloud builds submit --config cloudbuild.yaml
```

### Option 3: From GitHub (CI/CD)

Connect GitHub repository to Cloud Build triggers for automatic deployment.

## Testing

```bash
# Test health endpoint
curl https://glmp-service-XXXXX-uc.a.run.app/health

# List processes
curl https://glmp-service-XXXXX-uc.a.run.app/api/processes

# Get specific process
curl https://glmp-service-XXXXX-uc.a.run.app/api/process/ecoli_lac_operon

# Validate process
curl -X POST https://glmp-service-XXXXX-uc.a.run.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

## Architecture

```
┌─────────────────────────────────────┐
│       Cloud Run Service             │
│     (glmp-service)                  │
└───────────┬─────────────────────────┘
            │
    ┌───────┼──────────┬──────────────┐
    ▼       ▼          ▼              ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Vertex  │ │Secret  │ │  GCS   │ │ ArXiv  │
│  AI    │ │Manager │ │ Bucket │ │PubMed  │
└────────┘ └────────┘ └────────┘ └────────┘
```

## Environment Variables

- `PROJECT_ID` - Google Cloud project ID
- `BUCKET_NAME` - GCS bucket name
- `PORT` - Service port (default: 8080)

## IAM Permissions Required

The service account needs:
- `storage.buckets.get`
- `storage.objects.get`
- `storage.objects.create`
- `secretmanager.versions.access`
- `aiplatform.endpoints.predict` (Phase 2)

## Version

Current: 1.0.0 (Phase 1 - Basic Service)
