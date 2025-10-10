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


@app.route('/api/generate', methods=['POST'])
def generate_process():
    """
    Generate a new process (Phase 2 - Vertex AI integration)
    POST body: {
        "name": "GAL Gene Regulation",
        "organism": "S. cerevisiae",
        "category": "Gene Regulation"
    }
    """
    return jsonify({
        'success': False,
        'message': 'Process generation with Vertex AI coming in Phase 2',
        'status': 'not_implemented'
    }), 501


@app.route('/api/enrich', methods=['POST'])
def enrich_process():
    """
    Enrich process with recent literature (Phase 2 - ArXiv integration)
    POST body: {"process_id": "ecoli_lac_operon"}
    """
    return jsonify({
        'success': False,
        'message': 'Process enrichment with ArXiv coming in Phase 2',
        'status': 'not_implemented'
    }), 501


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
