#!/usr/bin/env python3
"""
Cloud Function for Podcast Generation
Receives form submissions and forwards to Cloud Run backend
"""

import json
import logging
import requests
import os
import traceback
import functions_framework

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CLOUD_RUN_URL = os.environ.get('CLOUD_RUN_URL', 'https://podcast-backend-service-url')  # Replace with actual URL

@functions_framework.http
def generate_podcast(request):
    """
    Cloud Function entry point for podcast generation
    Forwards requests to Cloud Run backend with proper error handling
    """
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    if request.method != 'POST':
        return (json.dumps({'error': 'Method not allowed'}), 405, headers)
    
    try:
        # Get request data
        request_json = request.get_json(silent=True)
        if not request_json:
            logger.error("No JSON data in request")
            return (json.dumps({'error': 'No JSON data provided'}), 400, headers)
        
        logger.info(f"Received podcast generation request: {json.dumps(request_json, indent=2)}")
        
        # Validate required fields
        required_fields = ['subject', 'category', 'duration', 'speakers', 'difficulty']
        missing_fields = [field for field in required_fields if not request_json.get(field)]
        
        if missing_fields:
            error_msg = f'Missing required fields: {", ".join(missing_fields)}'
            logger.error(error_msg)
            return (json.dumps({'error': error_msg}), 400, headers)
        
        # Forward request to Cloud Run backend
        logger.info(f"Forwarding request to Cloud Run: {CLOUD_RUN_URL}")
        
        backend_response = requests.post(
            f"{CLOUD_RUN_URL}/generate-podcast",
            json=request_json,
            timeout=300,  # 5 minute timeout for podcast generation
            headers={'Content-Type': 'application/json'}
        )
        
        # Log the response
        logger.info(f"Cloud Run response status: {backend_response.status_code}")
        
        if backend_response.status_code == 200:
            result = backend_response.json()
            logger.info(f"Podcast generation successful: {result.get('filename', 'unknown')}")
            return (json.dumps(result), 200, headers)
        else:
            error_msg = f"Backend error: {backend_response.status_code}"
            logger.error(f"{error_msg} - {backend_response.text}")
            return (json.dumps({
                'error': error_msg,
                'details': backend_response.text
            }), backend_response.status_code, headers)
    
    except requests.exceptions.Timeout:
        error_msg = "Request timeout - podcast generation is taking longer than expected"
        logger.error(error_msg)
        return (json.dumps({'error': error_msg}), 504, headers)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to backend service: {str(e)}"
        logger.error(error_msg)
        return (json.dumps({'error': error_msg}), 502, headers)
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"{error_msg} - Traceback: {traceback.format_exc()}")
        return (json.dumps({'error': error_msg}), 500, headers)