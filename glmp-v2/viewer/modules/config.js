/**
 * GLMP Viewer Configuration
 * Centralized configuration for paths, endpoints, and settings
 */

// API Endpoints
export const FEEDBACK_ENDPOINT = 'https://us-central1-regal-scholar-453620-r7.cloudfunctions.net/glmp_feedback';

// GCS Paths
export const CONFIG = {
    processesPath: 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/',
    metadataPath: 'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/metadata.json'
};

// Mermaid Configuration
export const MERMAID_CONFIG = {
    startOnLoad: false,
    theme: 'default',
    flowchart: { 
        useMaxWidth: false,
        htmlLabels: true,
        curve: 'basis',
        padding: 20,
        nodeSpacing: 50,
        rankSpacing: 80
    },
    fontFamily: 'Arial, sans-serif',
    fontSize: 16
};



