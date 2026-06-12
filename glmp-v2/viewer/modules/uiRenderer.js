/**
 * UI Renderer Module
 * Handles rendering of UI elements (process list, process details, etc.)
 */

import { escapeHtml } from './utils.js';
import { getArxivFrontier, countMermaidEdges, estimateMermaidNodeCount } from './frontier.js';

/**
 * Render the process list as a table
 * @param {Array} processList - Array of process objects
 */
export function renderProcessList(processList) {
    const listContainer = document.getElementById('process-list');
    if (!listContainer) return;
    
    if (processList.length === 0) {
        listContainer.innerHTML = `
            <div class="empty-state">
                <p>📋 No processes available yet.</p>
                <p>Processes will appear here as they are added to the collection.</p>
            </div>
        `;
        return;
    }
    
    // Render as simple table list
    let html = `
        <table class="process-table">
            <thead>
                <tr>
                    <th>Process Name</th>
                    <th>Organism</th>
                    <th>Category</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    // Sort all processes alphabetically by name
    const sortedProcs = [...processList].sort((a, b) => a.name.localeCompare(b.name));
    
    sortedProcs.forEach(proc => {
        html += `
            <tr onclick="window.loadProcessFromCard('${proc.id}')" style="cursor: pointer;">
                <td class="process-name">
                    <a href="#${proc.id}" onclick="event.preventDefault(); window.loadProcessFromCard('${proc.id}');">
                        ${escapeHtml(proc.name)}
                    </a>
                </td>
                <td class="organism">${escapeHtml(proc.organism || 'Unknown')}</td>
                <td><span class="category-badge">${escapeHtml(proc.category || 'Uncategorized')}</span></td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    listContainer.innerHTML = html;
}

/**
 * Render the process details view
 * @param {Object} process - The process data object
 */
export function renderProcess(process) {
    if (!process) return;
    
    // Set title
    const titleEl = document.getElementById('process-title');
    if (titleEl) {
        titleEl.textContent = process.name || 'Unknown Process';
    }
    
    // Set organism, category, description
    const organismEl = document.getElementById('process-organism');
    const categoryEl = document.getElementById('process-category');
    const descEl = document.getElementById('process-desc');
    
    if (organismEl) organismEl.textContent = process.organism || 'Unknown';
    if (categoryEl) categoryEl.textContent = process.category || 'Uncategorized';
    if (descEl) descEl.textContent = process.description || '';
    
    // Render scientific accuracy
    renderScientificAccuracy(process);
    
    // Render color legend
    renderColorLegend(process);
    
    // Render citations
    renderCitations(process);
    
    // Render metadata
    renderMetadata(process);
    
    renderProcessStatistics(process);
}

/**
 * Compact graph stats + arXiv "Frontier" link (mirrors mathematics process pages, e.g. Frontier: math.MP).
 */
export function renderProcessStatistics(process) {
    const box = document.getElementById('process-statistics');
    if (!box) return;
    
    const summary = process._metaSummary || {};
    const nodes = summary.nodes
        ?? process.complexity?.nodes
        ?? estimateMermaidNodeCount(process.mermaid);
    const edges = process.edges
        ?? countMermaidEdges(process.mermaid);
    
    const nodesStr = nodes != null ? String(nodes) : '—';
    const edgesStr = edges != null ? String(edges) : '—';
    
    const frontier = getArxivFrontier(process);
    const loopsVal = summary.loops != null ? String(summary.loops) : '—';
    
    box.innerHTML = `
        <h3 class="process-statistics-title">Process statistics</h3>
        <dl class="process-statistics-grid">
            <dt>Nodes</dt><dd>${escapeHtml(nodesStr)}</dd>
            <dt>Edges</dt><dd>${escapeHtml(edgesStr)}</dd>
            <dt title="Count of nodes that have an outgoing edge to a node defined earlier in the Mermaid source (text order). Many edges to one early hub (e.g. regulation) count as separate loop nodes—not the same as counting obvious visual cycles on the canvas.">Loop nodes</dt>
            <dd>${escapeHtml(loopsVal)}</dd>
            <dt>Frontier</dt>
            <dd>
                <a href="${escapeHtml(frontier.href)}" target="_blank" rel="noopener noreferrer" class="frontier-link" title="${escapeHtml(frontier.hint)} — recent arXiv preprints">${escapeHtml(frontier.code)}</a>
                <span class="frontier-hint">(${escapeHtml(frontier.hint)})</span>
            </dd>
        </dl>
    `;
    box.style.display = 'block';
}

/**
 * Render scientific accuracy section
 * @param {Object} process - The process data object
 */
function renderScientificAccuracy(process) {
    const accuracyStatement = document.getElementById('accuracy-statement');
    if (!accuracyStatement) return;
    
    const accuracyDetails = accuracyStatement.closest('details');
    
    if (process.scientificAccuracy) {
        accuracyStatement.textContent = process.scientificAccuracy;
        if (accuracyDetails) accuracyDetails.style.display = 'block';
    } else {
        if (accuracyDetails) accuracyDetails.style.display = 'none';
    }
}

/**
 * Render color legend
 * @param {Object} process - The process data object
 */
export function renderColorLegend(process) {
    const legendSection = document.getElementById('color-legend');
    const colorGrid = document.getElementById('color-key-grid');
    
    if (!legendSection || !colorGrid) {
        if (legendSection) legendSection.style.display = 'none';
        return;
    }
    
    if (!process.colorScheme) {
        legendSection.style.display = 'none';
        return;
    }
    
    let html = '';
    // Standardized 5-color legend (shared across Programming Framework collections)
    const colors = ['red', 'yellow', 'green', 'blue', 'violet'];
    
    colors.forEach(color => {
        if (process.colorScheme[color]) {
            const scheme = process.colorScheme[color];
            html += `
                <div class="color-key-item">
                    <span class="color-badge" style="background-color: ${scheme.hex}"></span>
                    <div class="color-info">
                        <strong>${escapeHtml(scheme.category)}</strong>
                        <small>${escapeHtml(scheme.description)}</small>
                    </div>
                </div>
            `;
        }
    });
    
    colorGrid.innerHTML = html;
    legendSection.style.display = 'block';
}

/**
 * Render citations
 * @param {Object} process - The process data object
 */
export function renderCitations(process) {
    const citationsContainer = document.getElementById('citations-list');
    
    if (!citationsContainer) return;

    // Process JSON uses `sources` in most files; some use `citations` (same shape).
    const sources = process.sources || process.citations;
    if (!sources || sources.length === 0) {
        citationsContainer.innerHTML =
            '<p>No primary-literature sources are listed for this process.</p>' +
            '<p class="citations-empty-hint">To cite the <strong>GLMP diagram</strong> (not the biology papers), use the purple <strong>Cite</strong> button next to the title at the top of the page.</p>';
        return;
    }
    
    let html = '<ol class="citations">';
    sources.forEach(source => {
        html += '<li class="citation">';
        html += `<strong>${escapeHtml(source.authors || 'Unknown')}.</strong> `;
        html += `${escapeHtml(source.title || 'Untitled')}. `;
        html += `<em>${escapeHtml(source.journal || '')}</em>. `;
        html += `${escapeHtml(source.year || '')}. `;
        
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
 * Render metadata section
 * @param {Object} process - The process data object
 */
export function renderMetadata(process) {
    const metadataContainer = document.getElementById('metadata-info');
    
    if (!metadataContainer) return;
    
    let html = '<dl class="metadata-list">';
    html += `<dt>Process ID:</dt><dd>${escapeHtml(process.id || 'Unknown')}</dd>`;
    html += `<dt>Created:</dt><dd>${escapeHtml(process.created || 'Unknown')}</dd>`;
    html += `<dt>Verified:</dt><dd>${process.verified ? '✅ Yes' : '⚠️ Pending'}</dd>`;
    if (process.lastUpdated) {
        html += `<dt>Last Updated:</dt><dd>${escapeHtml(process.lastUpdated)}</dd>`;
    }
    html += '</dl>';
    
    metadataContainer.innerHTML = html;
}

/**
 * Show loading spinner
 */
export function showLoadingSpinner() {
    const listContainer = document.getElementById('process-list');
    if (listContainer) {
        listContainer.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>🔄 Loading GLMP processes...</p>
            </div>
        `;
    }
}

