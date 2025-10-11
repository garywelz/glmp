# Complete GLMP Cloud Service API Reference

## 🚀 Service URL
```
https://glmp-service-204731194849.us-central1.run.app
```

---

## 📋 Table of Contents

1. [Core Endpoints](#core-endpoints)
2. [AI & Validation](#ai--validation)
3. [Literature Search](#literature-search)
4. [Multi-Database Search](#multi-database-search)
5. [Examples](#examples)

---

## Core Endpoints

### `GET /`
Service info and health check

**Response:**
```json
{
  "service": "GLMP Cloud Service",
  "version": "2.0.0",
  "status": "healthy"
}
```

### `GET /health`
Kubernetes health check

### `GET /api/secrets/list`
List all available Secret Manager secrets (names only, secure)

### `GET /api/processes`
List all biological processes in GCS

### `GET /api/process/<process_id>`
Get specific process JSON

**Example:**
```bash
curl https://glmp-service-204731194849.us-central1.run.app/api/process/ecoli_lac_operon
```

---

## AI & Validation

### `POST /api/generate`
**Generate new process using Vertex AI**

**Body:**
```json
{
  "name": "GAL Gene Regulation",
  "organism": "S. cerevisiae",
  "category": "Gene Regulation",
  "description": "Detailed description...",
  "save_to_gcs": true
}
```

**Response:** Complete process JSON with 30-50 nodes

---

### `POST /api/validate`
**Basic structure validation**

**Body:**
```json
{
  "process": { "id": "...", "mermaid": "..." }
}
```

---

### `POST /api/ai-validate`
**AI-powered biological validation (Vertex AI)**

**Body:**
```json
{
  "process_id": "ecoli_lac_operon"
}
```

**Response:**
```json
{
  "success": true,
  "ai_validation": {
    "accuracy_score": 9,
    "errors": [],
    "suggestions": ["Add more detail on CAP-cAMP"],
    "overall_assessment": "Highly accurate..."
  }
}
```

---

### `POST /api/openrouter-validate`
**Validate using OpenRouter (Claude, GPT-4, Llama)**

**Body:**
```json
{
  "process_id": "ecoli_lac_operon",
  "model": "anthropic/claude-3-opus"
}
```

**Available Models:**
- `openai/gpt-4-turbo`
- `anthropic/claude-3-opus` (most capable)
- `anthropic/claude-3-sonnet` (balanced)
- `anthropic/claude-3-haiku` (fast)
- `meta-llama/llama-3-70b-instruct`
- `google/gemini-pro`
- `mistralai/mixtral-8x7b-instruct`

**Response:**
```json
{
  "success": true,
  "model": "anthropic/claude-3-opus",
  "validation": {
    "accuracy_score": 9,
    "errors": [],
    "suggestions": []
  }
}
```

---

## Literature Search

### `POST /api/search-pubmed`
**Search PubMed (30M+ biomedical papers)**

**Body:**
```json
{
  "query": "lac operon E. coli regulation",
  "max_results": 10
}
```

**Response:**
```json
{
  "success": true,
  "pmid_count": 150,
  "pmids": ["12345678", ...],
  "papers_with_details": [
    {
      "pmid": "12345678",
      "title": "...",
      "authors": "...",
      "year": 2023,
      "abstract": "..."
    }
  ]
}
```

---

### `POST /api/search-arxiv`
**Search ArXiv (preprints)**

**Body:**
```json
{
  "query": "bacterial gene regulation",
  "max_results": 10,
  "category": "q-bio"
}
```

**Categories:**
- `q-bio` - Quantitative Biology
- `q-bio.MN` - Molecular Networks
- `q-bio.GN` - Genomics
- `cs.AI` - Artificial Intelligence

---

### `POST /api/search-zenodo`
**Search Zenodo (datasets & publications)**

**Body:**
```json
{
  "query": "E. coli genomics",
  "type": "dataset",
  "max_results": 10
}
```

**Types:**
- `dataset` - Research datasets
- `publication` - Papers
- `software` - Code & tools
- `poster` - Conference posters

**Response:**
```json
{
  "success": true,
  "count": 8,
  "records": [
    {
      "id": "123456",
      "doi": "10.5281/zenodo.123456",
      "title": "E. coli gene expression data",
      "description": "...",
      "creators": [...],
      "url": "https://zenodo.org/record/123456"
    }
  ]
}
```

---

### `POST /api/search-news`
**Search recent science news**

**Body:**
```json
{
  "query": "CRISPR gene editing",
  "max_results": 10
}
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "articles": [
    {
      "title": "New CRISPR breakthrough...",
      "description": "...",
      "url": "https://...",
      "source": "Nature News",
      "published_at": "2025-10-01T12:00:00Z"
    }
  ]
}
```

---

### `POST /api/validate-citations`
**Validate all citations against PubMed**

**Body:**
```json
{
  "process_id": "ecoli_lac_operon"
}
```

**Response:**
```json
{
  "success": true,
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

### `POST /api/enrich`
**Full literature enrichment (ArXiv + PubMed + validation)**

**Body:**
```json
{
  "process_id": "ecoli_lac_operon",
  "include_arxiv": true,
  "include_pubmed": true
}
```

**Response:**
```json
{
  "success": true,
  "enrichment": {
    "arxiv_count": 5,
    "pubmed_count": 10,
    "citation_validation": {...},
    "arxiv_papers": [...],
    "pubmed_papers": [...]
  }
}
```

---

## Multi-Database Search

### `POST /api/comprehensive-search`
**Search across ALL databases simultaneously**

**Body:**
```json
{
  "query": "lac operon regulation",
  "include_pubmed": true,
  "include_arxiv": true,
  "include_zenodo": true,
  "include_news": true
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "query": "lac operon regulation",
    "total_results": 28,
    "pubmed": {"count": 10, "pmids": [...]},
    "arxiv": {"count": 5, "papers": [...]},
    "zenodo": {"count": 8, "records": [...]},
    "news": {"count": 5, "articles": [...]}
  }
}
```

---

## Examples

### Example 1: Generate & Validate New Process

```bash
# 1. Generate process
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yeast GAL Regulation",
    "organism": "S. cerevisiae",
    "category": "Gene Regulation",
    "description": "GAL genes encode galactose metabolism enzymes...",
    "save_to_gcs": false
  }' > new_process.json

# 2. Validate with Claude Opus (best model)
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/openrouter-validate \
  -H "Content-Type: application/json" \
  -d '{
    "process_id": "yeast_gal_regulation",
    "model": "anthropic/claude-3-opus"
  }'
```

---

### Example 2: Comprehensive Literature Review

```bash
# Search across all databases
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/comprehensive-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "CRISPR Cas9 bacterial immunity",
    "include_pubmed": true,
    "include_arxiv": true,
    "include_zenodo": true,
    "include_news": true
  }' | python3 -m json.tool
```

---

### Example 3: Validate All Existing Processes

```bash
# Bash script to validate all processes
for process in ecoli_lac_operon ecoli_trp_operon ecoli_ara_operon; do
  echo "Validating $process..."
  curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/openrouter-validate \
    -H "Content-Type: application/json" \
    -d "{\"process_id\": \"$process\", \"model\": \"anthropic/claude-3-sonnet\"}"
  echo ""
done
```

---

### Example 4: Find Datasets for Process

```bash
# Search Zenodo for datasets
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-zenodo \
  -H "Content-Type: application/json" \
  -d '{
    "query": "E. coli lac operon gene expression",
    "type": "dataset",
    "max_results": 5
  }'
```

---

### Example 5: Model Comparison

```bash
# Compare GPT-4, Claude, and Llama
for model in "openai/gpt-4-turbo" "anthropic/claude-3-opus" "meta-llama/llama-3-70b-instruct"; do
  echo "Testing $model..."
  curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/openrouter-validate \
    -H "Content-Type: application/json" \
    -d "{\"process_id\": \"ecoli_lac_operon\", \"model\": \"$model\"}"
done
```

---

## 🎯 Use Cases

### **Automated Curation**
Generate 100s of processes from literature, validate with AI, enrich with citations

### **Quality Control**
Nightly validation of all processes, citation checking, news monitoring

### **Research Discovery**
Find related datasets, track new papers, monitor science news

### **Multi-Model Validation**
Compare results from GPT-4, Claude, Gemini for consensus

### **Literature Watch**
Weekly searches for new papers on your processes

---

## 🔐 API Keys Used

All stored securely in Google Secret Manager:

| API | Purpose | Rate Limits |
|-----|---------|-------------|
| PubMed | Search biomedical literature | 3-10 req/sec |
| ArXiv | Search preprints | No limit |
| Zenodo | Search datasets | 60 req/min |
| OpenRouter | Multi-LLM access | Pay-as-you-go |
| News API | Science news | 1000 req/day |
| Vertex AI | Gemini models | Pay-as-you-go |
| Google Search | Web search | 100 queries/day (free tier) |

---

## 💰 Cost Estimate

**Cloud Run:** $0.01-0.05/hour  
**Vertex AI:** $0.0025 per 1K chars  
**OpenRouter:** $0.01-0.03 per 1K tokens (model dependent)  
**Storage:** $0.02/GB/month  

**Total:** ~$5-20/month for moderate use

---

## 🚀 Best Practices

1. **Use Claude Opus** for highest accuracy validation
2. **Use Claude Sonnet** for balanced speed/quality
3. **Use Haiku** for quick checks
4. **Batch operations** to reduce API calls
5. **Cache results** for repeated queries
6. **Use comprehensive search** to cover all bases

---

**Last Updated:** 2025-10-10  
**Service Version:** 2.0.0  
**Status:** ✅ All systems operational
