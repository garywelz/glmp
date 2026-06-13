/**
 * Process Loader Module
 * Handles loading processes from GCS and managing process data
 */

import { CONFIG } from './config.js';

// Global state (will be managed by this module)
let currentProcess = null;
let processList = [];

/**
 * Load the process list from metadata.json
 * Tries local file first (for testing), then falls back to GCS
 */
export async function loadProcessList() {
    try {
        // First, try local metadata.json (for local testing)
        let metadataUrl = './metadata.json';
        let response = await fetch(metadataUrl, { cache: 'no-store' });
        
        if (!response.ok) {
            // Fall back to GCS
            console.log('⚠️ Local metadata.json not found, trying GCS...');
            metadataUrl = CONFIG.metadataPath + '?v=' + Date.now();
            console.log('🔄 Loading GLMP processes from:', metadataUrl);
            
            response = await fetch(metadataUrl, { 
                cache: 'no-store',
                headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache'
                }
            });
        } else {
            console.log('✅ Using local metadata.json');
        }
        
        console.log('📥 Response:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch metadata: ${response.status} ${response.statusText}`);
        }
        
        const metadata = await response.json();
        processList = metadata.processes || [];
        console.log('✅ Loaded successfully:', processList.length, 'processes');
        
        // Small delay to ensure DOM is ready
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Return the list for rendering
        return processList;
        
    } catch (error) {
        console.error('❌ Error loading process list:', error);
        console.error('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        throw error;
    }
}

/**
 * Load a specific process by ID
 */
export async function loadProcess(processId) {
    console.log('📄 Loading process:', processId);
    
    try {
        // Determine organism from process ID
        const organism = processId.startsWith('ecoli_') ? 'ecoli'
            : processId.startsWith('yeast_') ? 'yeast'
            : processId.startsWith('bacillus_') ? 'bacillus'
            : processId.startsWith('synthetic_') ? 'synthetic'
            : processId.startsWith('human_') ? 'human'
            : processId.startsWith('arabidopsis_') ? 'arabidopsis'
            : 'ecoli';
        
        const processUrl = `${CONFIG.processesPath}${organism}/${processId}.json?v=${Date.now()}`;
        console.log('🔄 Fetching from:', processUrl);
        
        const response = await fetch(processUrl, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Failed to load process: ${response.status} ${response.statusText}`);
        }
        
        const processData = await response.json();
        currentProcess = processData;
        console.log('✅ Process loaded:', processData.name);
        
        return processData;
        
    } catch (error) {
        console.error('❌ Error loading process:', error);
        throw error;
    }
}

/**
 * Scan for available processes (fallback if no metadata)
 */
export async function scanForProcesses() {
    // This is a simple implementation - you can enhance it
    // For now, return empty array and rely on metadata.json
    return [];
}

/**
 * Get current process
 */
export function getCurrentProcess() {
    return currentProcess;
}

/**
 * Get process list
 */
export function getProcessList() {
    return processList;
}

/**
 * Set current process
 */
export function setCurrentProcess(process) {
    currentProcess = process;
}

