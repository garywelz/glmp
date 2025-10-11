# Secrets Manager Integration Guide

## 🔐 Available API Keys

Your GLMP Cloud Service can access **all secrets** stored in Google Secret Manager.

### **Check Available Secrets:**

```bash
# List all secrets (safe - doesn't show values)
curl https://glmp-service-204731194849.us-central1.run.app/api/secrets/list
```

**Expected Response:**
```json
{
  "success": true,
  "project_id": "regal-scholar-453620-r7",
  "count": 10,
  "secrets": [
    {"id": "anthropic_api_key", "name": "projects/.../secrets/anthropic_api_key"},
    {"id": "arxiv_api_key", "name": "projects/.../secrets/arxiv_api_key"},
    {"id": "openrouter_api_key", "name": "projects/.../secrets/openrouter_api_key"},
    {"id": "pubmed_api_key", "name": "projects/.../secrets/pubmed_api_key"},
    ...
  ]
}
```

---

## 🔧 How to Use Secrets in Code

### **Current Implementation:**

The `get_secret()` function in `main.py` retrieves secrets:

```python
def get_secret(secret_id, version_id="latest"):
    """
    Get secret value from Secret Manager
    
    Args:
        secret_id: Secret name (e.g., 'pubmed_api_key')
        version_id: Version (default: 'latest')
    
    Returns:
        Secret value as string
    """
    try:
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')
    except Exception as e:
        logger.error(f"Failed to get secret {secret_id}: {e}")
        return None
```

---

## 🚀 Add More API Integrations

### **Example 1: OpenRouter (LLM APIs)**

OpenRouter provides access to GPT-4, Claude, Llama, etc.

Add to `literature_integration.py`:

```python
from main import get_secret
import requests

class OpenRouterSearch:
    """Use OpenRouter for advanced LLM queries"""
    
    def __init__(self):
        self.api_key = get_secret('openrouter_api_key')
        self.base_url = "https://openrouter.ai/api/v1"
        logger.info("✓ Initialized OpenRouter")
    
    def analyze_process(self, process_data):
        """Use GPT-4 to analyze a biological process"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "openai/gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this biological process: {process_data['name']}\n\nDescription: {process_data['description']}\n\nProvide insights on accuracy and completeness."
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        return response.json()
```

---

### **Example 2: Anthropic (Claude)**

Use Claude for biological reasoning:

```python
from main import get_secret
import anthropic

class ClaudeValidator:
    """Use Claude for biological validation"""
    
    def __init__(self):
        self.api_key = get_secret('anthropic_api_key')
        self.client = anthropic.Anthropic(api_key=self.api_key)
        logger.info("✓ Initialized Claude")
    
    def validate_citations(self, citations):
        """Use Claude to analyze citation quality"""
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Analyze these scientific citations:\n\n{citations}\n\nAre they appropriate and high-quality?"
            }]
        )
        
        return message.content[0].text
```

---

### **Example 3: PubMed API Key (Enhanced)**

If you have a PubMed API key, use it for higher rate limits:

Update `literature_integration.py`:

```python
from main import get_secret

# At module level
PUBMED_API_KEY = get_secret('pubmed_api_key')

# Update Entrez configuration
Entrez.email = "garywelz@gmail.com"
Entrez.tool = "GLMP_Service"
Entrez.api_key = PUBMED_API_KEY  # ← Add this for 10x rate limit
```

**Benefits:**
- Rate limit: **10 requests/second** (vs 3 without key)
- More reliable for batch operations

---

## 📋 Common Secret Names

Typical secrets you might have:

| Secret ID | Purpose | Used For |
|-----------|---------|----------|
| `pubmed_api_key` | NCBI API key | PubMed searches (higher rate limits) |
| `arxiv_api_key` | ArXiv (optional) | ArXiv searches (rarely needed) |
| `openrouter_api_key` | OpenRouter | Access GPT-4, Claude, Llama |
| `anthropic_api_key` | Anthropic | Claude API directly |
| `openai_api_key` | OpenAI | GPT-4 API directly |
| `google_api_key` | Google | Custom Search, other APIs |
| `huggingface_token` | HuggingFace | Model downloads, datasets |

---

## 🎯 Recommended Next Steps

### **1. Enable PubMed API Key** (if you have one)

Update `literature_integration.py`:

```python
# At the top, after imports
from main import get_secret

PUBMED_API_KEY = get_secret('pubmed_api_key')
if PUBMED_API_KEY:
    Entrez.api_key = PUBMED_API_KEY
    logger.info("✓ Using PubMed API key - 10 req/sec")
else:
    logger.info("⚠ No PubMed API key - 3 req/sec limit")
```

---

### **2. Add OpenRouter for Multi-Model Access**

Create `glmp-cloud-service/llm_integration.py`:

```python
"""
LLM Integration via OpenRouter
Access GPT-4, Claude, Llama, and more through a single API
"""

from main import get_secret
import requests
import logging

logger = logging.getLogger(__name__)

class LLMOrchestrator:
    """Access multiple LLMs via OpenRouter"""
    
    def __init__(self):
        self.api_key = get_secret('openrouter_api_key')
        self.base_url = "https://openrouter.ai/api/v1"
        logger.info("✓ Initialized LLM Orchestrator")
    
    def analyze_with_model(self, process_data, model="openai/gpt-4-turbo"):
        """
        Analyze process with any available model
        
        Available models:
        - openai/gpt-4-turbo
        - anthropic/claude-3-opus
        - meta-llama/llama-3-70b-instruct
        - google/gemini-pro
        """
        # ... implementation
```

Then add endpoint to `main.py`:

```python
@app.route('/api/llm-analyze', methods=['POST'])
def llm_analyze():
    """
    Analyze process with specific LLM
    POST body: {
        "process_id": "ecoli_lac_operon",
        "model": "openai/gpt-4-turbo"
    }
    """
    # ... implementation
```

---

### **3. Test Secret Access**

After redeploying:

```bash
# Check what secrets are available
curl https://glmp-service-204731194849.us-central1.run.app/api/secrets/list

# Test PubMed with API key (should be faster)
curl -X POST https://glmp-service-204731194849.us-central1.run.app/api/search-pubmed \
  -H "Content-Type: application/json" \
  -d '{"query": "lac operon", "max_results": 20}'
```

---

## 🔒 Security Notes

- ✅ Secrets are **never** exposed via API (only names, not values)
- ✅ Service account has read-only access to Secret Manager
- ✅ Secrets are loaded at runtime, never committed to git
- ✅ Cloud Run environment is isolated and secure

---

## 💡 Pro Tip

Since you have multiple API keys in Secret Manager, you can:

1. **Fallback chains** - Try OpenRouter → Vertex AI → Anthropic
2. **Model comparison** - Run same query on GPT-4 vs Claude vs Gemini
3. **Cost optimization** - Use cheaper models for validation, expensive ones for generation
4. **A/B testing** - Compare which model generates better processes

---

**Want me to enable any of these integrations?** I can add OpenRouter, Claude, or enhance the PubMed integration with your API key! 🚀
