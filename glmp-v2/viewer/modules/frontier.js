/**
 * Map GLMP process categories to arXiv q-bio subject classes (same role as math.MP on mathematics pages).
 * @see https://arxiv.org/archive/q-bio
 */

const CATEGORY_TO_ARXIV = {
    'Stress Response': 'q-bio.CB',
    'Metabolic Pathway': 'q-bio.MN',
    'Signal Transduction': 'q-bio.MN',
    'Biological Process': 'q-bio.OT',
    'Gene Regulation': 'q-bio.GN',
    'DNA Repair': 'q-bio.GN',
    'Metabolic Regulation': 'q-bio.MN',
    'Gene Expression': 'q-bio.GN',
    'Developmental Decision': 'q-bio.CB',
    'DNA Replication': 'q-bio.GN',
    'Protein Transport': 'q-bio.SC',
    'Protein Synthesis': 'q-bio.SC',
    'Cell Cycle': 'q-bio.CB',
    'Protein Quality Control': 'q-bio.SC',
    'Cell Division': 'q-bio.CB',
    'Cell Wall Biogenesis': 'q-bio.SC',
    'Developmental Program': 'q-bio.CB',
    'Innate Immunity': 'q-bio.CB',
    'Nutrient Transport': 'q-bio.SC',
    'Organelle Biology': 'q-bio.SC',
    'Translation Machinery': 'q-bio.SC'
};

/**
 * arXiv only accepts canonical case for q-bio subcategories (e.g. q-bio.GN). Lowercase q-bio.gn returns 400.
 */
function normalizeQBioCode(code) {
    const s = String(code || '').trim();
    const m = s.match(/^q-bio\.([a-z]{2})$/i);
    if (!m) return null;
    return `q-bio.${m[1].toUpperCase()}`;
}

/**
 * Recent preprints in a q-bio arXiv subcategory.
 * Uses arXiv's classic /list/ URLs - the site search does not reliably match `cat:q-bio.MN` in "All fields"
 * (it often returns zero hits). See https://arxiv.org/archive/q-bio
 */
export function arxivCategorySearchUrl(code) {
    const normalized = normalizeQBioCode(code) || 'q-bio.OT';
    const safe = normalized.replace(/[^a-z0-9.-]/gi, '');
    return `https://arxiv.org/list/${safe}/recent`;
}

/**
 * @returns {{ code: string, href: string, hint: string }}
 */
export function getArxivFrontier(process) {
    const raw = process && process.frontier;
    const fromMeta = typeof raw === 'string' && raw.trim() ? normalizeQBioCode(raw.trim()) : null;
    const code =
        fromMeta ||
        normalizeQBioCode(CATEGORY_TO_ARXIV[process.category]) ||
        'q-bio.OT';
    const hints = {
        'q-bio.BM': 'Biomolecules',
        'q-bio.CB': 'Cell behavior',
        'q-bio.GN': 'Genomics',
        'q-bio.MN': 'Molecular networks',
        'q-bio.NC': 'Neurons and cognition',
        'q-bio.OT': 'Other quantitative biology',
        'q-bio.PE': 'Populations and evolution',
        'q-bio.QM': 'Quantitative methods',
        'q-bio.SC': 'Subcellular processes',
        'q-bio.TO': 'Tissues and organs'
    };
    return {
        code,
        href: arxivCategorySearchUrl(code),
        hint: hints[code] || 'Quantitative biology'
    };
}

export function countMermaidEdges(mermaidStr) {
    if (!mermaidStr || typeof mermaidStr !== 'string') return null;
    const matches = mermaidStr.match(/-->|---|==>|===|-.->|-\.->|\.\.\/>/g);
    return matches ? matches.length : 0;
}

/**
 * Rough node count from Mermaid source when metadata is missing.
 */
export function estimateMermaidNodeCount(mermaidStr) {
    if (!mermaidStr || typeof mermaidStr !== 'string') return null;
    const ids = new Set();
    const re = /^\s*([A-Za-z][A-Za-z0-9_]*)\s*[\[({]/gm;
    let m;
    while ((m = re.exec(mermaidStr)) !== null) {
        ids.add(m[1]);
    }
    return ids.size || null;
}
