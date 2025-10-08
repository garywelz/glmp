// GLMP Viewer - Main JavaScript
// Handles process loading, navigation, and Mermaid rendering

// Initialize Mermaid
mermaid.initialize({ 
    startOnLoad: false,
    theme: 'default',
    flowchart: { 
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
    }
});

// Global state
let currentProcess = null;
let processList = [];
let currentDetailLevel = 1;

// Configuration
const CONFIG = {
    processesPath: '../processes/',
    metadataPath: '../data/metadata.json'
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeViewer();
});

/**
 * Initialize the viewer
 */
async function initializeViewer() {
    // Check URL parameters for direct process loading
    const params = new URLSearchParams(window.location.search);
    const processId = params.get('process');
    
    if (processId) {
        // Load specific process from URL
        await loadProcess(processId);
    } else {
        // Show home view
        showHome();
        // Load process list in background
        await loadProcessList();
    }
}

/**
 * Load the list of available processes
 */
async function loadProcessList() {
    try {
        // Try to load metadata file
        const response = await fetch(CONFIG.metadataPath);
        if (response.ok) {
            const metadata = await response.json();
            processList = metadata.processes || [];
        } else {
            // If no metadata file, scan for processes manually
            processList = await scanForProcesses();
        }
        
        renderProcessList();
    } catch (error) {
        console.error('Error loading process list:', error);
        // Show error message
        document.getElementById('process-list').innerHTML = `
            <div class="error-message">
                <p>⚠️ Could not load process list.</p>
                <p>Please ensure processes are available in the correct directory.</p>
            </div>
        `;
    }
}

/**
 * Scan for available processes (fallback if no metadata)
 */
async function scanForProcesses() {
    // This is a simple implementation - you can enhance it
    // For now, return empty array and rely on metadata.json
    return [];
}

/**
 * Render the process list
 */
function renderProcessList() {
    const listContainer = document.getElementById('process-list');
    
    if (processList.length === 0) {
        listContainer.innerHTML = `
            <div class="empty-state">
                <p>📋 No processes available yet.</p>
                <p>Processes will appear here as they are added to the collection.</p>
            </div>
        `;
        return;
    }
    
    // Group by organism
    const grouped = {};
    processList.forEach(proc => {
        const org = proc.organism || 'Other';
        if (!grouped[org]) grouped[org] = [];
        grouped[org].push(proc);
    });
    
    // Render grouped list
    let html = '';
    Object.keys(grouped).sort().forEach(organism => {
        html += `
            <div class="organism-group">
                <h3>${organism}</h3>
                <div class="process-cards">
        `;
        
        grouped[organism].forEach(proc => {
            html += `
                <div class="process-card" onclick="loadProcessFromCard('${proc.id}')">
                    <h4>${proc.name}</h4>
                    <p class="card-category">${proc.category || 'Uncategorized'}</p>
                    <p class="card-desc">${proc.description?.substring(0, 100) || ''}...</p>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    listContainer.innerHTML = html;
}

/**
 * Load a process from a card click
 */
async function loadProcessFromCard(processId) {
    await loadProcess(processId);
    // Update URL without reload
    const url = new URL(window.location);
    url.searchParams.set('process', processId);
    window.history.pushState({}, '', url);
}

/**
 * Load and display a specific process
 */
async function loadProcess(processId) {
    try {
        // Determine file path
        const organism = processId.split('_')[0]; // e.g., 'ecoli' from 'ecoli_lac_operon'
        const filePath = `${CONFIG.processesPath}${organism}/${processId}.json`;
        
        // Fetch the process file
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`Process not found: ${processId}`);
        }
        
        currentProcess = await response.json();
        currentDetailLevel = 1; // Reset detail level
        
        // Render the process
        renderProcess();
        
        // Show process view
        showProcessView();
        
    } catch (error) {
        console.error('Error loading process:', error);
        alert(`Error loading process: ${error.message}`);
    }
}

/**
 * Render the current process
 */
function renderProcess() {
    if (!currentProcess) return;
    
    // Update title and metadata
    document.getElementById('process-title').textContent = currentProcess.name;
    document.getElementById('process-organism').textContent = currentProcess.organism || 'Unknown';
    document.getElementById('process-category').textContent = currentProcess.category || 'Uncategorized';
    document.getElementById('process-desc').textContent = currentProcess.description || '';
    
    // Render scientific accuracy statement
    renderScientificAccuracy();
    
    // Render color legend
    renderColorLegend();
    
    // Render diagram
    renderDiagram();
    
    // Render citations
    renderCitations();
    
    // Render metadata
    renderMetadata();
    
    // Show/hide detail selector if process has multiple detail levels
    if (currentProcess.detailLevels && currentProcess.detailLevels.length > 1) {
        document.getElementById('detail-selector').style.display = 'block';
    } else {
        document.getElementById('detail-selector').style.display = 'none';
    }
}

/**
 * Render scientific accuracy statement
 */
function renderScientificAccuracy() {
    const accuracySection = document.getElementById('scientific-accuracy');
    const accuracyStatement = document.getElementById('accuracy-statement');
    
    if (currentProcess.scientificAccuracy) {
        accuracyStatement.textContent = currentProcess.scientificAccuracy;
        accuracySection.style.display = 'block';
    } else {
        accuracySection.style.display = 'none';
    }
}

/**
 * Render color legend
 */
function renderColorLegend() {
    const legendSection = document.getElementById('color-legend');
    const colorGrid = document.getElementById('color-key-grid');
    
    if (currentProcess.colorScheme) {
        let html = '';
        const colors = ['red', 'yellow', 'green', 'blue', 'violet'];
        
        colors.forEach(color => {
            if (currentProcess.colorScheme[color]) {
                const scheme = currentProcess.colorScheme[color];
                html += `
                    <div class="color-key-item">
                        <span class="color-badge" style="background-color: ${scheme.hex}"></span>
                        <div class="color-info">
                            <strong>${scheme.category}</strong>
                            <small>${scheme.description}</small>
                        </div>
                    </div>
                `;
            }
        });
        
        colorGrid.innerHTML = html;
        legendSection.style.display = 'block';
    } else {
        legendSection.style.display = 'none';
    }
}

/**
 * Render the Mermaid diagram
 */
function renderDiagram() {
    const diagramContainer = document.getElementById('mermaid-diagram');
    
    // Get Mermaid code (either single or based on detail level)
    let mermaidCode = currentProcess.mermaid;
    
    // If process has detail levels, use the current one
    if (currentProcess.detailLevels) {
        const detailLevel = currentProcess.detailLevels[currentDetailLevel - 1];
        if (detailLevel && detailLevel.mermaid) {
            mermaidCode = detailLevel.mermaid;
        }
    }
    
    // Clear previous diagram
    diagramContainer.innerHTML = mermaidCode;
    
    // Render with Mermaid
    mermaid.run({
        querySelector: '.mermaid'
    });
}

/**
 * Update detail level
 */
function updateDetailLevel(level) {
    currentDetailLevel = parseInt(level);
    const labels = ['Basic', 'Detailed', 'Complex', 'Advanced', 'Complete'];
    document.getElementById('detail-label').textContent = `${labels[level - 1]} (${level})`;
    
    // Re-render diagram
    renderDiagram();
}

/**
 * Render citations
 */
function renderCitations() {
    const citationsContainer = document.getElementById('citations-list');
    
    if (!currentProcess.sources || currentProcess.sources.length === 0) {
        citationsContainer.innerHTML = '<p>No citations available.</p>';
        return;
    }
    
    let html = '<ol class="citations">';
    currentProcess.sources.forEach(source => {
        html += '<li class="citation">';
        html += `<strong>${source.authors || 'Unknown'}.</strong> `;
        html += `${source.title || 'Untitled'}. `;
        html += `<em>${source.journal || ''}</em>. `;
        html += `${source.year || ''}. `;
        
        if (source.pmid) {
            html += `<a href="https://pubmed.ncbi.nlm.nih.gov/${source.pmid}/" target="_blank" class="citation-link">PubMed: ${source.pmid}</a> `;
        }
        if (source.doi) {
            html += `<a href="https://doi.org/${source.doi}" target="_blank" class="citation-link">DOI: ${source.doi}</a>`;
        }
        
        html += '</li>';
    });
    html += '</ol>';
    
    citationsContainer.innerHTML = html;
}

/**
 * Render metadata
 */
function renderMetadata() {
    const metadataContainer = document.getElementById('metadata-info');
    
    let html = '<dl class="metadata-list">';
    html += `<dt>Process ID:</dt><dd>${currentProcess.id || 'Unknown'}</dd>`;
    html += `<dt>Created:</dt><dd>${currentProcess.created || 'Unknown'}</dd>`;
    html += `<dt>Verified:</dt><dd>${currentProcess.verified ? '✅ Yes' : '⚠️ Pending'}</dd>`;
    if (currentProcess.lastUpdated) {
        html += `<dt>Last Updated:</dt><dd>${currentProcess.lastUpdated}</dd>`;
    }
    html += '</dl>';
    
    metadataContainer.innerHTML = html;
}

/**
 * Navigation functions
 */
function showHome() {
    hideAllViews();
    document.getElementById('home-view').style.display = 'block';
    // Clear URL params
    window.history.pushState({}, '', window.location.pathname);
}

function showProcessList() {
    hideAllViews();
    document.getElementById('list-view').style.display = 'block';
    // Clear URL params
    window.history.pushState({}, '', window.location.pathname);
}

function showProcessView() {
    hideAllViews();
    document.getElementById('process-view').style.display = 'block';
}

function showAbout() {
    hideAllViews();
    document.getElementById('about-view').style.display = 'block';
    // Clear URL params
    window.history.pushState({}, '', window.location.pathname);
}

function hideAllViews() {
    document.querySelectorAll('.view').forEach(view => {
        view.style.display = 'none';
    });
}

// Handle browser back/forward buttons
window.addEventListener('popstate', () => {
    initializeViewer();
});
