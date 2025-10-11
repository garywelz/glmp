# Phase 2 Features - AI & Literature Integration

## ✅ NEW Capabilities Added

### **1. Vertex AI Integration**

Generate and validate biological processes using Google's Gemini models.

#### **Generate New Process:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "GAL Gene Regulation",
    "organism": "S. cerevisiae",
    "category": "Gene Regulation",
    "description": "The GAL genes in yeast encode enzymes for galactose metabolism. Regulated by Gal4 activator and Gal80 repressor. In presence of galactose, Gal3 binds Gal80, releasing Gal4 to activate transcription.",
    "save_to_gcs": true
  }'
```

**What it does:**
- Uses Vertex AI Gemini to generate complete process JSON
- Creates 30-50 node Mermaid flowchart
- Identifies logic gates automatically
- Applies 7-color scheme
- Suggests citations
- Optionally saves to GCS

---

#### **AI-Powered Validation:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/ai-validate \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

**What it does:**
- Analyzes biological accuracy (0-10 score)
- Evaluates citation quality
- Identifies errors or inconsistencies
- Suggests improvements
- Notes missing mechanisms

---

### **2. ArXiv Integration**

Search for recent preprints and cutting-edge research.

#### **Search ArXiv:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-arxiv \
  -H "Content-Type: application/json" \
  -d '{
    "query": "lac operon regulation",
    "max_results": 10,
    "category": "q-bio"
  }'
```

**Returns:**
- Recent papers from ArXiv
- Titles, authors, abstracts
- PDF links
- Publication dates

---

### **3. PubMed Integration**

Validate citations and search biomedical literature.

#### **Search PubMed:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-pubmed \
  -H "Content-Type: application/json" \
  -d '{
    "query": "lac operon E. coli regulation",
    "max_results": 10
  }'
```

**Returns:**
- List of PubMed IDs
- Paper details (title, authors, journal, year)
- Abstracts
- DOIs

---

#### **Validate Citations:**
```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/validate-citations \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

**What it does:**
- Checks all citations against PubMed
- Verifies PMIDs are correct
- Validates title/author matches
- Reports validation rate

---

### **4. Literature Enrichment**

Combine ArXiv + PubMed + Citation Validation in one call.

```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": "ecoli_lac_operon",
    "include_arxiv": true,
    "include_pubmed": true
  }'
```

**What it does:**
- Finds recent ArXiv papers
- Finds recent PubMed papers
- Validates all existing citations
- Provides comprehensive enrichment report

---

## 📋 Complete API Reference

### **Process Management:**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/processes` | GET | List all processes |
| `/api/process/<id>` | GET | Get specific process |
| `/api/validate` | POST | Basic structure validation |

### **AI-Powered (NEW):**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate` | POST | Generate process with Vertex AI |
| `/api/ai-validate` | POST | AI-powered accuracy validation |

### **Literature (NEW):**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search-arxiv` | POST | Search ArXiv papers |
| `/api/search-pubmed` | POST | Search PubMed papers |
| `/api/validate-citations` | POST | Validate citations against PubMed |
| `/api/enrich` | POST | Full enrichment (ArXiv + PubMed + validation) |

---

## 🎯 Usage Examples

### **Example 1: Generate a New Process**

```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yeast GAL Gene Regulation",
    "organism": "Saccharomyces cerevisiae",
    "category": "Gene Regulation",
    "description": "GAL genes encode galactose metabolism enzymes. Gal4 activator is inhibited by Gal80. Galactose induces Gal3 to sequester Gal80, allowing Gal4 to activate transcription. System includes glucose repression via Mig1 and feedback regulation.",
    "save_to_gcs": false
  }'
```

**Expected:** Complete JSON with 30-50 nodes, logic gates identified, citations included.

---

### **Example 2: Validate All Citations**

```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/validate-citations \
  -H "Content-Type: application/json" \
  -d '{"process_id": "ecoli_lac_operon"}'
```

**Expected:**
```json
{
  "success": true,
  "process_id": "ecoli_lac_operon",
  "validation": {
    "total_citations": 4,
    "valid_citations": 4,
    "invalid_citations": 0,
    "validation_rate": 1.0,
    "results": [...]
  }
}
```

---

### **Example 3: Find Recent Research**

```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-arxiv \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bacterial gene regulation two-component systems",
    "max_results": 5,
    "category": "q-bio"
  }'
```

**Expected:** 5 recent ArXiv papers with abstracts and PDF links.

---

### **Example 4: Comprehensive Enrichment**

```bash
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": "ecoli_trp_operon",
    "include_arxiv": true,
    "include_pubmed": true
  }'
```

**Expected:**
- Recent ArXiv papers on trp operon
- Recent PubMed papers
- Citation validation results
- Comprehensive enrichment report

---

## 🔐 Authentication & Permissions

The service uses the Cloud Run service account which has access to:
- ✅ GCS bucket (read/write)
- ✅ Secret Manager (all your API keys)
- ✅ Vertex AI (Gemini models)

**No additional authentication needed!**

---

## 🎨 Advanced Use Cases

### **Use Case 1: Automated Process Generation**

Generate 10 yeast processes in one batch:

```python
import requests

processes_to_generate = [
    {"name": "GAL Gene Regulation", "description": "..."},
    {"name": "Mating Type Switching", "description": "..."},
    # ... 8 more
]

for proc in processes_to_generate:
    response = requests.post(
        'https://glmp-service-204731194849.us-central1.run.app/api/generate',
        json={**proc, "organism": "S. cerevisiae", "save_to_gcs": True}
    )
    print(f"Generated: {proc['name']}")
```

---

### **Use Case 2: Nightly Citation Validation**

Validate all 14 processes automatically:

```python
import requests

# Get all processes
processes = requests.get(
    'https://glmp-service-204731194849.us-central1.run.app/api/processes'
).json()['processes']

# Validate each
for process_path in processes:
    process_id = process_path.split('/')[-1].replace('.json', '')
    validation = requests.post(
        'https://glmp-service-204731194849.us-central1.run.app/api/validate-citations',
        json={'process_id': process_id}
    ).json()
    
    print(f"{process_id}: {validation['validation']['validation_rate']*100}% valid")
```

---

### **Use Case 3: Literature Watch**

Monitor for new papers on your processes:

```python
# Weekly check for new papers
processes = ["lac operon", "trp operon", "SOS response"]

for process in processes:
    arxiv_papers = requests.post(
        'https://glmp-service-204731194849.us-central1.run.app/api/search-arxiv',
        json={"query": f"{process} bacteria", "max_results": 3}
    ).json()
    
    if arxiv_papers['count'] > 0:
        print(f"New papers on {process}: {arxiv_papers['count']}")
        # Could auto-tweet or email you
```

---

## 📊 Service Capabilities Summary

| Feature | Status | Technology |
|---------|--------|------------|
| Process Generation | ✅ Working | Vertex AI (Gemini) |
| Biological Validation | ✅ Working | Vertex AI (Gemini) |
| Citation Validation | ✅ Working | PubMed (BioPython) |
| ArXiv Search | ✅ Working | ArXiv API |
| PubMed Search | ✅ Working | NCBI Entrez |
| Literature Enrichment | ✅ Working | Combined |
| GCS Storage | ✅ Working | Cloud Storage |
| Secret Manager | ✅ Working | Google Secrets |

---

## 🚀 Ready to Deploy

Update your Cloud Run service with these new features:

```bash
cd ~/glmp-clean/glmp-cloud-service
git pull origin main

gcloud run deploy glmp-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=regal-scholar-453620-r7,BUCKET_NAME=regal-scholar-453620-r7-podcast-storage \
  --project regal-scholar-453620-r7 \
  --memory 1Gi \
  --timeout 600
```

**Note:** Increased memory (1Gi) and timeout (10 min) for AI workloads.

---

**Last Updated:** 2025-10-10  
**Status:** ✅ Ready for deployment
