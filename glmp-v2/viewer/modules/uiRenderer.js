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

    renderCircuitClass(process);
    renderSequenceAnnotation(process);
    
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

const CIRCUIT_CLASS_NAMES = {
    'I': 'Feed-forward cascade',
    'II': 'Negative feedback (homeostatic)',
    'III': 'Bistable switch / positive feedback',
    'IV': 'Delayed negative feedback (oscillator)',
    'V': 'Self-modifying chromatin / epigenetic'
};
const CIRCUIT_CLASS_COLORS = {
    'I': '#64748b', 'II': '#2e86de', 'III': '#e74c3c', 'IV': '#8e44ad', 'V': '#27867a'
};

/**
 * Render the GLMP five-class circuit tag (Paper I/III) next to organism/category.
 */
function renderCircuitClass(process) {
    const el = document.getElementById('process-circuit-class');
    if (!el) return;
    const cls = (process.circuitClass || '').toString().trim();
    const name = (process.circuitClassName || '').toString().trim()
        || CIRCUIT_CLASS_NAMES[cls]
        || 'Unclassified';
    if (!cls && name === 'Unclassified') { el.style.display = 'none'; return; }
    // Descriptive name is the label; Roman numeral stays ordinal metadata only.
    el.textContent = name;
    if (cls) el.setAttribute('data-circuit-class', cls);
    else el.removeAttribute('data-circuit-class');
    el.style.backgroundColor = CIRCUIT_CLASS_COLORS[cls] || '#bbb';
    el.style.color = '#fff';
    const ordinal = cls ? `Class ${cls} (ordinal)` : '';
    el.title = process.circuitClassRationale
        ? [ordinal, name, process.circuitClassRationale].filter(Boolean).join(' — ')
        : [ordinal, name].filter(Boolean).join(' — ');
    el.style.display = '';
}

/**
 * Render the sequence -> logic (regulatory grammar) block, when present.
 * Maps each cis-regulatory site to the logical operator it implements.
 */
function renderSequenceAnnotation(process) {
    const section = document.getElementById('sequence-annotation-section');
    const container = document.getElementById('sequence-annotation');
    if (!section || !container) return;

    const sa = process.sequenceAnnotation;
    if (!sa || !Array.isArray(sa.regulatoryRegions) || sa.regulatoryRegions.length === 0) {
        section.style.display = 'none';
        return;
    }

    let html = '';
    if (sa.derivedLogic) {
        html += `<p class="seq-derived-logic"><strong>Derived logic:</strong> <code>${escapeHtml(sa.derivedLogic)}</code></p>`;
    }
    html += `
        <table class="seq-annotation-table">
            <thead>
                <tr><th>Regulatory site</th><th>Bound factor</th><th>Operator</th><th>Effect</th><th>Motif</th></tr>
            </thead>
            <tbody>`;
    sa.regulatoryRegions.forEach(r => {
        html += `
            <tr>
                <td>${escapeHtml(r.name || '')}</td>
                <td>${escapeHtml(r.boundFactor || '')}</td>
                <td><span class="seq-operator">${escapeHtml(r.operator || '')}</span></td>
                <td>${escapeHtml(r.effect || '')}</td>
                <td><code>${escapeHtml(r.sequenceMotif || '')}</code>${r.note ? `<br><small>${escapeHtml(r.note)}</small>` : ''}</td>
            </tr>`;
    });
    html += '</tbody></table>';
    if (Array.isArray(sa.references) && sa.references.length) {
        html += `<p class="seq-refs"><small>References: ${sa.references.map(escapeHtml).join('; ')}</small></p>`;
    }
    html += `<p class="seq-schema"><small>sequenceAnnotation schema v${escapeHtml(sa.schemaVersion || '0.1')} — the genome's control layer read as logical formulae (GLMP Big Picture).</small></p>`;

    container.innerHTML = html;
    section.style.display = 'block';
}

/**
 * Compact graph stats + arXiv "Frontier" link (mirrors mathematics process pages, e.g. Frontier: math.MP).
 */
export function renderProcessStatistics(process) {
    const box = document.getElementById('process-statistics');
    if (!box) return;
    
    const summary = process._metaSummary || {};
    const nodes = process.totalNodes
        ?? process.complexity?.nodes
        ?? summary.nodes
        ?? estimateMermaidNodeCount(process.mermaid);
    const edges = process.edges
        ?? countMermaidEdges(process.mermaid);
    
    const nodesStr = nodes != null ? String(nodes) : '—';
    const edgesStr = edges != null ? String(edges) : '—';
    
    const frontier = getArxivFrontier(process);
    const loopsVal = process.loops != null
        ? String(process.loops)
        : (summary.loops != null ? String(summary.loops) : '—');
    
    box.innerHTML = `
        <h3 class="process-statistics-title">Process statistics</h3>
        <dl class="process-statistics-grid">
            <dt>Nodes</dt><dd>${escapeHtml(nodesStr)}</dd>
            <dt>Edges</dt><dd>${escapeHtml(edgesStr)}</dd>
            <dt title="Nodes on at least one directed regulatory cycle (Paper I / III definition).">Loop nodes</dt>
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

