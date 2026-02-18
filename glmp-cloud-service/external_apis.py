"""
External API Integrations for GLMP Cloud Service
Connects to multiple scientific databases and services
"""

import requests
import json
import logging
import os
from google.cloud import secretmanager

logger = logging.getLogger(__name__)

# Initialize Secret Manager client
PROJECT_ID = os.environ.get('PROJECT_ID', 'regal-scholar-453620-r7')
secret_client = None

try:
    secret_client = secretmanager.SecretManagerServiceClient()
    logger.info("✓ Initialized Secret Manager client")
except Exception as e:
    logger.warning(f"Secret Manager initialization delayed: {e}")


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
        if not secret_client:
            logger.error("Secret Manager client not initialized")
            return None
            
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')
    except Exception as e:
        logger.error(f"Failed to get secret {secret_id}: {e}")
        return None


class ZenodoAPI:
    """
    Zenodo - Open Science Repository
    Access millions of research datasets, publications, and software
    """
    
    def __init__(self):
        self.api_key = get_secret('zenodo_api_key')
        self.base_url = "https://zenodo.org/api"
        logger.info("✓ Initialized Zenodo API")
    
    def search_records(self, query, record_type="publication", max_results=10):
        """
        Search Zenodo records
        
        Args:
            query: Search query
            record_type: 'publication', 'dataset', 'software', 'poster', etc.
            max_results: Max results to return
        
        Returns:
            List of records
        """
        try:
            params = {
                'q': query,
                'type': record_type,
                'size': max_results,
                'access_token': self.api_key
            }
            
            response = requests.get(f"{self.base_url}/records", params=params)
            response.raise_for_status()
            
            data = response.json()
            records = []
            
            for hit in data.get('hits', {}).get('hits', []):
                records.append({
                    'id': hit.get('id'),
                    'doi': hit.get('doi'),
                    'title': hit.get('metadata', {}).get('title'),
                    'description': hit.get('metadata', {}).get('description'),
                    'creators': hit.get('metadata', {}).get('creators', []),
                    'publication_date': hit.get('metadata', {}).get('publication_date'),
                    'resource_type': hit.get('metadata', {}).get('resource_type'),
                    'url': hit.get('links', {}).get('html')
                })
            
            logger.info(f"✓ Found {len(records)} Zenodo records for: {query}")
            return records
            
        except Exception as e:
            logger.error(f"Zenodo search failed: {e}")
            return []
    
    def get_biological_datasets(self, process_name, organism):
        """Find relevant biological datasets"""
        query = f"{process_name} {organism} genomics proteomics"
        return self.search_records(query, record_type='dataset', max_results=5)


class NASAADSAPI:
    """
    NASA ADS - Astrophysics Data System
    (Can be used for computational biology papers too)
    """
    
    def __init__(self):
        self.token = get_secret('nasa_ads_token')
        self.base_url = "https://api.adsabs.harvard.edu/v1"
        logger.info("✓ Initialized NASA ADS API")
    
    def search_papers(self, query, max_results=10):
        """
        Search NASA ADS
        
        Args:
            query: Search query
            max_results: Max results
        
        Returns:
            List of papers
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'q': query,
                'fl': 'bibcode,title,author,year,abstract,doi,pubdate',
                'rows': max_results
            }
            
            response = requests.get(
                f"{self.base_url}/search/query",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            papers = []
            
            for doc in data.get('response', {}).get('docs', []):
                papers.append({
                    'bibcode': doc.get('bibcode'),
                    'title': doc.get('title', [''])[0],
                    'authors': doc.get('author', []),
                    'year': doc.get('year'),
                    'abstract': doc.get('abstract'),
                    'doi': doc.get('doi', [''])[0] if doc.get('doi') else None,
                    'pubdate': doc.get('pubdate')
                })
            
            logger.info(f"✓ Found {len(papers)} ADS papers for: {query}")
            return papers
            
        except Exception as e:
            logger.error(f"NASA ADS search failed: {e}")
            return []


class OpenRouterAPI:
    """
    OpenRouter - Access Multiple LLMs Through One API
    GPT-4, Claude, Llama, Gemini, and many more
    """
    
    def __init__(self):
        self.api_key = get_secret('openrouter_api_key')
        self.base_url = "https://openrouter.ai/api/v1"
        logger.info("✓ Initialized OpenRouter API")
    
    def chat_completion(self, prompt, model="anthropic/claude-3-sonnet", max_tokens=4096):
        """
        Generate completion using any available model
        
        Available models:
        - openai/gpt-4-turbo
        - anthropic/claude-3-opus
        - anthropic/claude-3-sonnet
        - anthropic/claude-3-haiku
        - meta-llama/llama-3-70b-instruct
        - google/gemini-pro
        - mistralai/mixtral-8x7b-instruct
        
        Args:
            prompt: The prompt
            model: Model identifier
            max_tokens: Max response tokens
        
        Returns:
            Model response text
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://glmp.bio',
                'X-Title': 'GLMP Cloud Service'
            }
            
            payload = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data['choices'][0]['message']['content']
            
            logger.info(f"✓ OpenRouter completion with {model}")
            return result
            
        except Exception as e:
            logger.error(f"OpenRouter request failed: {e}")
            return None
    
    def validate_process_biology(self, process_data, model="anthropic/claude-3-sonnet"):
        """Use Claude/GPT-4 to validate biological accuracy"""
        prompt = f"""You are a molecular biology expert. Validate this process for scientific accuracy.

Process: {process_data.get('name')}
Organism: {process_data.get('organism')}
Description: {process_data.get('description')}

Mermaid Diagram (first 500 chars):
{process_data.get('mermaid', '')[:500]}...

Citations: {len(process_data.get('sources', []))} sources

Provide:
1. Accuracy score (0-10)
2. Key errors or omissions
3. Citation quality assessment
4. Suggestions for improvement

Format as JSON:
{{"accuracy_score": 0-10, "errors": [], "suggestions": [], "assessment": "text"}}"""

        return self.chat_completion(prompt, model=model)
    
    def generate_process_description(self, name, organism, model="anthropic/claude-3-opus"):
        """Generate detailed process description"""
        prompt = f"""As a molecular biology expert, provide a detailed scientific description of:

Process: {name}
Organism: {organism}

Include:
1. Molecular mechanism (proteins, genes, regulators)
2. Key decision points (logic gates)
3. Inputs and outputs
4. Biological significance

Write 3-4 paragraphs suitable for a scientific flowchart."""

        return self.chat_completion(prompt, model=model, max_tokens=2000)
    
    def compare_models(self, prompt, models=None):
        """
        Compare responses from multiple models
        
        Args:
            prompt: The prompt
            models: List of model IDs (default: GPT-4, Claude, Llama)
        
        Returns:
            Dict with model responses
        """
        if models is None:
            models = [
                "openai/gpt-4-turbo",
                "anthropic/claude-3-sonnet",
                "meta-llama/llama-3-70b-instruct"
            ]
        
        results = {}
        for model in models:
            response = self.chat_completion(prompt, model=model)
            results[model] = response
        
        return results


class NewsAPI:
    """
    NewsAPI - Recent news and articles
    Can find recent science news related to processes
    """
    
    def __init__(self):
        self.api_key = get_secret('news_api_key')
        self.base_url = "https://newsapi.org/v2"
        logger.info("✓ Initialized News API")
    
    def search_science_news(self, query, max_results=10):
        """
        Search recent science news
        
        Args:
            query: Search query
            max_results: Max articles
        
        Returns:
            List of articles
        """
        try:
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': max_results,
                'category': 'science',
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(f"{self.base_url}/everything", params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                articles.append({
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'source': article.get('source', {}).get('name'),
                    'published_at': article.get('publishedAt'),
                    'author': article.get('author')
                })
            
            logger.info(f"✓ Found {len(articles)} news articles for: {query}")
            return articles
            
        except Exception as e:
            logger.error(f"News API search failed: {e}")
            return []


class GoogleCustomSearchAPI:
    """
    Google Custom Search - Search the web for scientific content
    """
    
    def __init__(self):
        self.api_key = get_secret('google_api_key')
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        logger.info("✓ Initialized Google Custom Search")
    
    def search(self, query, cx='017576662512468239146:omuauf_lfve', max_results=10):
        """
        Search using Google Custom Search
        
        Args:
            query: Search query
            cx: Custom search engine ID (default: general)
            max_results: Max results
        
        Returns:
            List of search results
        """
        try:
            params = {
                'key': self.api_key,
                'cx': cx,
                'q': query,
                'num': min(max_results, 10)  # Max 10 per request
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'snippet': item.get('snippet'),
                    'display_link': item.get('displayLink')
                })
            
            logger.info(f"✓ Found {len(results)} Google results for: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Google search failed: {e}")
            return []


class COREAPI:
    """
    CORE - World's largest aggregator of open access research papers
    270+ million papers from repositories worldwide
    """
    
    def __init__(self):
        self.api_key = get_secret('core_api_key')
        self.base_url = "https://api.core.ac.uk/v3"
        logger.info("✓ Initialized CORE API (270M+ papers)")
    
    def search_papers(self, query, max_results=10):
        """
        Search CORE for research papers
        
        Args:
            query: Search query
            max_results: Max results to return
        
        Returns:
            List of papers with full metadata
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            params = {
                'q': query,
                'limit': max_results
            }
            
            response = requests.get(
                f"{self.base_url}/search/works",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            papers = []
            
            for result in data.get('results', []):
                papers.append({
                    'id': result.get('id'),
                    'title': result.get('title'),
                    'abstract': result.get('abstract'),
                    'authors': result.get('authors', []),
                    'year': result.get('yearPublished'),
                    'doi': result.get('doi'),
                    'download_url': result.get('downloadUrl'),
                    'full_text_url': result.get('fullTextIdentifier'),
                    'citations': result.get('citationCount'),
                    'publisher': result.get('publisher'),
                    'journal': result.get('journals', [{}])[0].get('title') if result.get('journals') else None
                })
            
            logger.info(f"✓ Found {len(papers)} papers on CORE for: {query}")
            return papers
            
        except Exception as e:
            logger.error(f"CORE API search failed: {e}")
            return []
    
    def get_paper_by_doi(self, doi):
        """Get specific paper by DOI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.get(
                f"{self.base_url}/works/{doi}",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"CORE DOI lookup failed: {e}")
            return None
    
    def search_biological_papers(self, process_name, organism):
        """Search CORE specifically for biological papers"""
        query = f"{process_name} {organism} molecular biology gene regulation"
        return self.search_papers(query, max_results=10)


class OpenAIDirectAPI:
    """
    OpenAI Direct API - GPT-4 and other OpenAI models
    (Alternative to OpenRouter for direct access)
    """
    
    def __init__(self):
        self.api_key = get_secret('openai_api_key')
        self.base_url = "https://api.openai.com/v1"
        logger.info("✓ Initialized OpenAI Direct API")
    
    def chat_completion(self, prompt, model="gpt-4-turbo-preview", max_tokens=4096):
        """
        Generate completion using OpenAI models
        
        Args:
            prompt: The prompt
            model: Model (gpt-4-turbo-preview, gpt-3.5-turbo, etc.)
            max_tokens: Max response tokens
        
        Returns:
            Model response text
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            result = data['choices'][0]['message']['content']
            
            logger.info(f"✓ OpenAI completion with {model}")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI request failed: {e}")
            return None
    
    def validate_process(self, process_data):
        """Use GPT-4 to validate biological process"""
        prompt = f"""You are a molecular biology expert. Validate this biological process.

Process: {process_data.get('name')}
Organism: {process_data.get('organism')}
Description: {process_data.get('description')}

Provide accuracy score (0-10), errors, and suggestions in JSON format."""

        return self.chat_completion(prompt, model="gpt-4-turbo-preview")


# Global instances
zenodo_api = None
nasa_ads_api = None
openrouter_api = None
news_api = None
google_search_api = None
core_api = None
openai_direct_api = None


def get_zenodo():
    """Get or create Zenodo API instance"""
    global zenodo_api
    if zenodo_api is None:
        zenodo_api = ZenodoAPI()
    return zenodo_api


def get_nasa_ads():
    """Get or create NASA ADS API instance"""
    global nasa_ads_api
    if nasa_ads_api is None:
        nasa_ads_api = NASAADSAPI()
    return nasa_ads_api


def get_openrouter():
    """Get or create OpenRouter API instance"""
    global openrouter_api
    if openrouter_api is None:
        openrouter_api = OpenRouterAPI()
    return openrouter_api


def get_news_api():
    """Get or create News API instance"""
    global news_api
    if news_api is None:
        news_api = NewsAPI()
    return news_api


def get_google_search():
    """Get or create Google Search API instance"""
    global google_search_api
    if google_search_api is None:
        google_search_api = GoogleCustomSearchAPI()
    return google_search_api


def get_core():
    """Get or create CORE API instance"""
    global core_api
    if core_api is None:
        core_api = COREAPI()
    return core_api


def get_openai_direct():
    """Get or create OpenAI Direct API instance"""
    global openai_direct_api
    if openai_direct_api is None:
        openai_direct_api = OpenAIDirectAPI()
    return openai_direct_api
