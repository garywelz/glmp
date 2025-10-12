"""
GLMP Cloud Service - Biological Process Generator & Validator
Runs on Google Cloud Run with Vertex AI, Secret Manager, and GCS integration
"""

from flask import Flask, request, jsonify
from google.cloud import storage, secretmanager
import os
import json
import logging
from datetime import datetime

# Import our new modules - use lazy loading to avoid startup failures
# These will be imported only when needed
vertex_ai_integration = None
literature_integration = None
external_apis = None

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
PROJECT_ID = os.environ.get('PROJECT_ID', 'regal-scholar-453620-r7')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'regal-scholar-453620-r7-podcast-storage')
GCS_PREFIX = 'glmp-v2'

# Initialize Google Cloud clients
try:
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    secret_client = secretmanager.SecretManagerServiceClient()
    logger.info(f"✓ Initialized GCS bucket: {BUCKET_NAME}")
except Exception as e:
    logger.error(f"Failed to initialize cloud clients: {e}")
    storage_client = None
    bucket = None
    secret_client = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_secret(secret_id):
    """Retrieve secret from Google Secret Manager"""
    try:
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
        response = secret_client.access_secret_version(request={"name": name})
        return response.payload.data.decode('UTF-8')
    except Exception as e:
        logger.error(f"Failed to retrieve secret {secret_id}: {e}")
        return None


def load_process_from_gcs(process_id):
    """Load a process JSON file from GCS"""
    try:
        blob = bucket.blob(f'{GCS_PREFIX}/processes/{process_id}.json')
        if not blob.exists():
            # Try ecoli/ and yeast/ subdirectories
            for subdir in ['ecoli', 'yeast']:
                blob = bucket.blob(f'{GCS_PREFIX}/processes/{subdir}/{process_id}.json')
                if blob.exists():
                    break
        
        if blob.exists():
            content = blob.download_as_string()
            return json.loads(content)
        return None
    except Exception as e:
        logger.error(f"Failed to load process {process_id}: {e}")
        return None


def save_process_to_gcs(process_id, process_data, organism='ecoli'):
    """Save a process JSON file to GCS"""
    try:
        blob = bucket.blob(f'{GCS_PREFIX}/processes/{organism}/{process_id}.json')
        blob.upload_from_string(
            json.dumps(process_data, indent=2),
            content_type='application/json'
        )
        logger.info(f"✓ Saved process {process_id} to GCS")
        return True
    except Exception as e:
        logger.error(f"Failed to save process {process_id}: {e}")
        return False


def list_all_processes():
    """List all processes from GCS"""
    try:
        processes = []
        blobs = bucket.list_blobs(prefix=f'{GCS_PREFIX}/processes/')
        for blob in blobs:
            if blob.name.endswith('.json') and 'metadata.json' not in blob.name:
                processes.append(blob.name)
        return processes
    except Exception as e:
        logger.error(f"Failed to list processes: {e}")
        return []


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def home():
    """Health check and service info"""
    return jsonify({
        'service': 'GLMP Cloud Service',
        'version': '1.0.0',
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'health': '/health',
            'list': '/api/processes',
            'get': '/api/process/<process_id>',
            'validate': '/api/validate',
            'generate': '/api/generate (coming soon)',
            'enrich': '/api/enrich (coming soon)'
        }
    })


@app.route('/health')
def health():
    """Kubernetes/Cloud Run health check"""
    checks = {
        'storage': bucket is not None,
        'secrets': secret_client is not None,
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code


@app.route('/api/secrets/list')
def list_secrets():
    """
    List all available secrets in Secret Manager
    (Does not return secret values, just names for security)
    """
    try:
        if not secret_client:
            return jsonify({
                'success': False,
                'error': 'Secret Manager client not initialized'
            }), 503
        
        parent = f"projects/{PROJECT_ID}"
        secrets_list = []
        
        for secret in secret_client.list_secrets(request={"parent": parent}):
            secret_id = secret.name.split('/')[-1]
            secrets_list.append({
                'id': secret_id,
                'name': secret.name,
                'created': secret.create_time.isoformat() if hasattr(secret, 'create_time') else None
            })
        
        logger.info(f"Listed {len(secrets_list)} secrets")
        
        return jsonify({
            'success': True,
            'project_id': PROJECT_ID,
            'count': len(secrets_list),
            'secrets': sorted(secrets_list, key=lambda x: x['id'])
        })
        
    except Exception as e:
        logger.error(f"Failed to list secrets: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/processes')
def list_processes():
    """List all available processes"""
    try:
        processes = list_all_processes()
        return jsonify({
            'success': True,
            'count': len(processes),
            'processes': processes
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/process/<process_id>')
def get_process(process_id):
    """Retrieve a specific process"""
    try:
        process = load_process_from_gcs(process_id)
        if process:
            return jsonify({
                'success': True,
                'process': process
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/validate', methods=['POST'])
def validate_process():
    """
    Validate a process
    POST body: {"process_id": "ecoli_lac_operon"}
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Basic validation
        validation_results = {
            'has_id': 'id' in process,
            'has_name': 'name' in process,
            'has_organism': 'organism' in process,
            'has_mermaid': 'mermaid' in process,
            'has_sources': 'sources' in process and len(process.get('sources', [])) > 0,
            'has_color_scheme': 'colorScheme' in process,
            'has_scientific_accuracy': 'scientificAccuracy' in process,
            'node_count': process.get('complexity', {}).get('nodes', 0),
            'logic_gate_count': process.get('complexity', {}).get('logicGates', {}).get('total', 0)
        }
        
        all_valid = all([
            validation_results['has_id'],
            validation_results['has_name'],
            validation_results['has_mermaid'],
            validation_results['has_sources']
        ])
        
        return jsonify({
            'success': True,
            'process_id': process_id,
            'valid': all_valid,
            'checks': validation_results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def get_vertex_module():
    """Lazy load vertex AI module"""
    global vertex_ai_integration
    if vertex_ai_integration is None:
        import vertex_ai_integration as vai
        vertex_ai_integration = vai
    return vertex_ai_integration

def get_literature_module():
    """Lazy load literature module"""
    global literature_integration
    if literature_integration is None:
        import literature_integration as li
        literature_integration = li
    return literature_integration

def get_external_module():
    """Lazy load external APIs module"""
    global external_apis
    if external_apis is None:
        import external_apis as ea
        external_apis = ea
    return external_apis


@app.route('/api/generate', methods=['POST'])
def generate_process():
    """
    Generate a new process using Vertex AI
    POST body: {
        "name": "GAL Gene Regulation",
        "organism": "S. cerevisiae",
        "category": "Gene Regulation",
        "description": "Detailed description of the process...",
        "save_to_gcs": true (optional)
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required = ['name', 'organism', 'category', 'description']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {missing}'
            }), 400
        
        # Generate process using Vertex AI
        logger.info(f"Generating process: {data['name']}")
        vai = get_vertex_module()
        generator = vai.get_generator()
        
        process_data = generator.generate_process_from_description(
            name=data['name'],
            organism=data['organism'],
            category=data['category'],
            description=data['description'],
            sources=data.get('sources')
        )
        
        if not process_data:
            return jsonify({
                'success': False,
                'error': 'Failed to generate process'
            }), 500
        
        # Optionally save to GCS
        if data.get('save_to_gcs', False):
            organism_dir = 'ecoli' if 'coli' in data['organism'].lower() else 'yeast'
            saved = save_process_to_gcs(process_data['id'], process_data, organism_dir)
            
            if saved:
                return jsonify({
                    'success': True,
                    'process': process_data,
                    'saved_to_gcs': True,
                    'url': f'https://storage.googleapis.com/{BUCKET_NAME}/{GCS_PREFIX}/viewer/index.html?process={process_data["id"]}'
                })
        
        return jsonify({
            'success': True,
            'process': process_data,
            'saved_to_gcs': False,
            'message': 'Set save_to_gcs=true to save to GCS'
        })
        
    except Exception as e:
        logger.error(f"Generate process failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/enrich', methods=['POST'])
def enrich_process():
    """
    Enrich process with recent literature from ArXiv and PubMed
    POST body: {
        "process_id": "ecoli_lac_operon",
        "include_arxiv": true,
        "include_pubmed": true
    }
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        # Load process
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Enrich with literature
        logger.info(f"Enriching process: {process_id}")
        enricher = get_literature_enricher()
        
        enrichment = enricher.enrich_process(
            process,
            include_arxiv=data.get('include_arxiv', True),
            include_pubmed=data.get('include_pubmed', True)
        )
        
        return jsonify({
            'success': True,
            'enrichment': enrichment
        })
        
    except Exception as e:
        logger.error(f"Enrich process failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/validate-citations', methods=['POST'])
def validate_citations():
    """
    Validate all citations in a process against PubMed
    POST body: {"process_id": "ecoli_lac_operon"}
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        # Load process
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Validate citations
        logger.info(f"Validating citations for: {process_id}")
        li = get_literature_module()
        pubmed = li.get_pubmed()
        validation = pubmed.validate_all_citations(process)
        
        return jsonify({
            'success': True,
            'process_id': process_id,
            'validation': validation
        })
        
    except Exception as e:
        logger.error(f"Citation validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-arxiv', methods=['POST'])
def search_arxiv():
    """
    Search ArXiv for papers on a topic
    POST body: {
        "query": "lac operon regulation",
        "max_results": 10,
        "category": "q-bio" (optional)
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        # Search ArXiv
        logger.info(f"Searching ArXiv for: {query}")
        li = get_literature_module()
        arxiv_search = li.get_arxiv()
        
        papers = arxiv_search.search_papers(
            query=query,
            max_results=data.get('max_results', 10),
            category=data.get('category')
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(papers),
            'papers': papers
        })
        
    except Exception as e:
        logger.error(f"ArXiv search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-pubmed', methods=['POST'])
def search_pubmed():
    """
    Search PubMed for papers
    POST body: {
        "query": "lac operon E. coli",
        "max_results": 10
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        # Search PubMed
        logger.info(f"Searching PubMed for: {query}")
        pubmed = get_pubmed()
        
        pmids = pubmed.search_pubmed(
            query=query,
            max_results=data.get('max_results', 10)
        )
        
        # Fetch details for first few
        papers = []
        for pmid in pmids[:5]:
            details = pubmed.fetch_paper_details(pmid)
            if details:
                papers.append(details)
        
        return jsonify({
            'success': True,
            'query': query,
            'pmid_count': len(pmids),
            'pmids': pmids,
            'papers_with_details': papers
        })
        
    except Exception as e:
        logger.error(f"PubMed search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ai-validate', methods=['POST'])
def ai_validate():
    """
    Validate biological accuracy using Vertex AI
    POST body: {"process_id": "ecoli_lac_operon"}
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        # Load process
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Validate with AI
        logger.info(f"AI validation for: {process_id}")
        generator = get_generator()
        validation = generator.validate_biological_accuracy(process)
        
        return jsonify({
            'success': True,
            'process_id': process_id,
            'ai_validation': validation
        })
        
    except Exception as e:
        logger.error(f"AI validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/openrouter-validate', methods=['POST'])
def openrouter_validate():
    """
    Validate using OpenRouter (Claude, GPT-4, etc.)
    POST body: {
        "process_id": "ecoli_lac_operon",
        "model": "anthropic/claude-3-opus" (optional)
    }
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        model = data.get('model', 'anthropic/claude-3-sonnet')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        # Load process
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Validate with OpenRouter
        logger.info(f"OpenRouter validation for: {process_id} using {model}")
        openrouter = get_openrouter()
        result = openrouter.validate_process_biology(process, model=model)
        
        # Try to parse as JSON
        try:
            validation = json.loads(result)
        except:
            validation = {'raw_response': result}
        
        return jsonify({
            'success': True,
            'process_id': process_id,
            'model': model,
            'validation': validation
        })
        
    except Exception as e:
        logger.error(f"OpenRouter validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-zenodo', methods=['POST'])
def search_zenodo():
    """
    Search Zenodo for datasets and publications
    POST body: {
        "query": "lac operon E. coli",
        "type": "dataset" (or "publication"),
        "max_results": 10
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        zenodo = get_zenodo()
        records = zenodo.search_records(
            query=query,
            record_type=data.get('type', 'publication'),
            max_results=data.get('max_results', 10)
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(records),
            'records': records
        })
        
    except Exception as e:
        logger.error(f"Zenodo search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-news', methods=['POST'])
def search_news():
    """
    Search recent science news
    POST body: {
        "query": "CRISPR gene editing",
        "max_results": 10
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        ea = get_external_module()
        news_api = ea.get_news_api()
        articles = news_api.search_science_news(
            query=query,
            max_results=data.get('max_results', 10)
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(articles),
            'articles': articles
        })
        
    except Exception as e:
        logger.error(f"News search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/search-core', methods=['POST'])
def search_core():
    """
    Search CORE API (270M+ papers)
    POST body: {
        "query": "lac operon regulation",
        "max_results": 10
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        ea = get_external_module()
        core = ea.get_core()
        papers = core.search_papers(
            query=query,
            max_results=data.get('max_results', 10)
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'count': len(papers),
            'papers': papers,
            'source': 'CORE (270M+ open access papers)'
        })
        
    except Exception as e:
        logger.error(f"CORE search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/openai-validate', methods=['POST'])
def openai_validate():
    """
    Validate using OpenAI Direct (GPT-4)
    POST body: {
        "process_id": "ecoli_lac_operon",
        "model": "gpt-4-turbo-preview" (optional)
    }
    """
    try:
        data = request.json
        process_id = data.get('process_id')
        model = data.get('model', 'gpt-4-turbo-preview')
        
        if not process_id:
            return jsonify({
                'success': False,
                'error': 'process_id is required'
            }), 400
        
        # Load process
        process = load_process_from_gcs(process_id)
        if not process:
            return jsonify({
                'success': False,
                'error': f'Process {process_id} not found'
            }), 404
        
        # Validate with OpenAI
        logger.info(f"OpenAI validation for: {process_id} using {model}")
        ea = get_external_module()
        openai = ea.get_openai_direct()
        result = openai.validate_process(process)
        
        # Try to parse as JSON
        try:
            validation = json.loads(result)
        except:
            validation = {'raw_response': result}
        
        return jsonify({
            'success': True,
            'process_id': process_id,
            'model': model,
            'validation': validation
        })
        
    except Exception as e:
        logger.error(f"OpenAI validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/comprehensive-search', methods=['POST'])
def comprehensive_search():
    """
    Search across ALL databases simultaneously
    POST body: {
        "query": "lac operon regulation",
        "include_pubmed": true,
        "include_arxiv": true,
        "include_zenodo": true,
        "include_core": true,
        "include_news": true
    }
    """
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        results = {
            'query': query,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # PubMed
        if data.get('include_pubmed', True):
            li = get_literature_module()
            pubmed = li.get_pubmed()
            pmids = pubmed.search_pubmed(query, max_results=5)
            results['pubmed'] = {
                'count': len(pmids),
                'pmids': pmids,
                'source': 'PubMed (30M biomedical papers)'
            }
        
        # ArXiv
        if data.get('include_arxiv', True):
            li = get_literature_module()
            arxiv_search = li.get_arxiv()
            papers = arxiv_search.search_papers(query, max_results=5)
            results['arxiv'] = {
                'count': len(papers),
                'papers': papers,
                'source': 'ArXiv (2M preprints)'
            }
        
        # CORE (NEW!)
        if data.get('include_core', True):
            ea = get_external_module()
            core = ea.get_core()
            core_papers = core.search_papers(query, max_results=10)
            results['core'] = {
                'count': len(core_papers),
                'papers': core_papers,
                'source': 'CORE (270M open access papers)'
            }
        
        # Zenodo
        if data.get('include_zenodo', True):
            zenodo = get_zenodo()
            records = zenodo.search_records(query, max_results=5)
            results['zenodo'] = {
                'count': len(records),
                'records': records,
                'source': 'Zenodo (10M datasets & publications)'
            }
        
        # News
        if data.get('include_news', True):
            ea = get_external_module()
            news_api = ea.get_news_api()
            articles = news_api.search_science_news(query, max_results=5)
            results['news'] = {
                'count': len(articles),
                'articles': articles,
                'source': 'Science News (real-time)'
            }
        
        # Total results
        results['total_results'] = sum([
            results.get('pubmed', {}).get('count', 0),
            results.get('arxiv', {}).get('count', 0),
            results.get('core', {}).get('count', 0),
            results.get('zenodo', {}).get('count', 0),
            results.get('news', {}).get('count', 0)
        ])
        
        results['summary'] = f"Found {results['total_results']} results across {sum([1 for k in ['pubmed', 'arxiv', 'core', 'zenodo', 'news'] if k in results])} databases"
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Comprehensive search failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': str(error)
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
