/**
 * "Cite" modal for the process view: how to attribute this GLMP diagram (not the same as Sources & Citations).
 */

import { CONFIG } from './config.js';
import { escapeHtml } from './utils.js';
import { getCurrentProcess } from './processLoader.js';

const TABLE_URL =
    'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html';
const VIEWER_BASE =
    'https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html';

function openProcessCiteModal(open) {
    const modal = document.getElementById('process-cite-modal');
    if (!modal) return;
    modal.setAttribute('aria-hidden', open ? 'false' : 'true');
    modal.style.display = open ? 'flex' : 'none';
}

async function copyPreContents(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    try {
        await navigator.clipboard.writeText(el.textContent);
    } catch (_) {
        /* ignore */
    }
}

/**
 * Call when a process is loaded so the modal is prefilled before first open.
 */
export function fillProcessCiteModal(process) {
    if (!process) return;

    const id = process.id || '';
    const name = process.name || 'Unknown process';
    const viewerUrl = `${VIEWER_BASE}?process=${encodeURIComponent(id)}`;
    const metadataUrl = CONFIG.metadataPath;
    const year = new Date().getFullYear();

    const plain =
        `GLMP (Genome Logic Modeling Project) process diagram: "${name}" (process id: ${id}). ` +
        `Interactive viewer: ${viewerUrl} . ` +
        `Collection index: ${metadataUrl} . ` +
        `Summary table: ${TABLE_URL} . ` +
        `For biological claims, cite the peer-reviewed sources listed under "Sources & Citations" on this page.`;

    const bibKey = `glmp_${id.replace(/[^a-zA-Z0-9_]/g, '_')}`;
    const bibTitle = name.replace(/[{}]/g, '').trim();
    const bib = `@misc{${bibKey},
  title = {{GLMP diagram: ${bibTitle}}},
  howpublished = {\\url{${viewerUrl}}},
  note = {Process ID: ${id}. Genome Logic Modeling Project. Metadata: \\url{${metadataUrl}}},
  year = {${year}}
}`;

    const plainEl = document.getElementById('process-cite-plain');
    const bibEl = document.getElementById('process-cite-bibtex');
    const listEl = document.getElementById('process-cite-links');
    if (plainEl) plainEl.textContent = plain;
    if (bibEl) bibEl.textContent = bib;

    if (listEl) {
        listEl.innerHTML = `
            <li><a href="${escapeHtml(viewerUrl)}" target="_blank" rel="noopener">This process (interactive viewer)</a></li>
            <li><a href="${escapeHtml(TABLE_URL)}" target="_blank" rel="noopener">GLMP database table</a></li>
            <li><a href="${escapeHtml(metadataUrl)}" target="_blank" rel="noopener">metadata.json</a></li>
            <li><em>Sources &amp; Citations</em> (below) lists primary literature for the biology, not for attributing GLMP itself.</li>
        `;
    }
}

let processCiteModalBound = false;

export function initProcessCiteModal() {
    const modal = document.getElementById('process-cite-modal');
    if (!modal) return;

    if (processCiteModalBound) return;
    processCiteModalBound = true;

    // Delegation: survives module load order vs DOMContentLoaded and avoids a dead handler on #process-cite-btn.
    document.addEventListener('click', (e) => {
        const citeBtn = e.target && e.target.closest && e.target.closest('#process-cite-btn');
        if (!citeBtn) return;
        e.preventDefault();
        const p = getCurrentProcess();
        if (p) fillProcessCiteModal(p);
        openProcessCiteModal(true);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        const m = document.getElementById('process-cite-modal');
        if (m && m.getAttribute('aria-hidden') === 'false') openProcessCiteModal(false);
    });

    document.getElementById('process-cite-close')?.addEventListener('click', () => {
        openProcessCiteModal(false);
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) openProcessCiteModal(false);
    });

    document.getElementById('process-cite-copy-plain')?.addEventListener('click', () => {
        copyPreContents('process-cite-plain');
    });
    document.getElementById('process-cite-copy-bib')?.addEventListener('click', () => {
        copyPreContents('process-cite-bibtex');
    });
}
