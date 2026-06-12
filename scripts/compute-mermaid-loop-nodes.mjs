#!/usr/bin/env node
/**
 * Count "loop nodes" in each GLMP process Mermaid diagram.
 *
 * Definition (per project): a node is a loop node if it has an outgoing edge to a
 * node that appears *earlier* in the diagram source (top-to-bottom, left-to-right)
 * — i.e. "higher" in a typical graph TD layout = smaller first-seen index.
 *
 * Equivalently: directed edge u → v where index(v) < index(u).
 *
 * Output: updates glmp-v2/metadata.json and glmp-v2/data/metadata.json
 * (adds `loops` on each process and `loops` in `statistics`).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, '..');
const PROCESS_DIRS = ['ecoli', 'yeast', 'bacillus'];

const RESERVED = new Set([
    'graph', 'flowchart', 'subgraph', 'end', 'style', 'classDef', 'linkStyle',
    'click', 'direction', 'class', 'TD', 'TB', 'BT', 'RL', 'LR'
]);

function extractNodeId(seg) {
    if (!seg) return null;
    const s = seg.trim();
    const m = s.match(/^([A-Za-z][A-Za-z0-9_]*)/);
    return m ? m[1] : null;
}

function expandSide(group) {
    if (!group) return [];
    return group.split(/\s*&\s*/).map((g) => extractNodeId(g)).filter(Boolean);
}

function stripEdgeLabels(line) {
    return line
        .replace(/-->\|[^|]*\|\s*/g, '-->')
        .replace(/---\|[^|]*\|\s*/g, '---')
        .replace(/===\|[^|]*\|\s*/g, '==>')
        .replace(/-\.->\|[^|]*\|\s*/g, '-->');
}

function parseEdgesFromLine(line) {
    const edges = [];
    const cleaned = stripEdgeLabels(line);
    const parts = cleaned.split(/\s*(-->|---|==>|-\.->)\s*/);
    if (parts.length < 3) return edges;

    let left = expandSide(parts[0]);
    for (let i = 2; i < parts.length; i += 2) {
        const right = expandSide(parts[i]);
        for (const u of left) {
            for (const v of right) {
                if (u && v && u !== v) edges.push([u, v]);
            }
        }
        left = right;
    }
    return edges;
}

function recordSeen(id, firstSeen, counterRef) {
    if (!id || RESERVED.has(id)) return;
    if (!firstSeen.has(id)) {
        firstSeen.set(id, counterRef.n);
        counterRef.n += 1;
    }
}

/** Register node ids appearing left-to-right along one arrow line (incl. chains). */
function visitLineForOrder(line, firstSeen, counterRef) {
    const cleaned = stripEdgeLabels(line);
    if (!/-->|---|==>|-\.->/.test(cleaned)) return;
    const parts = cleaned.split(/\s*(-->|---|==>|-\.->)\s*/);
    for (let i = 0; i < parts.length; i += 2) {
        const ids = expandSide(parts[i]);
        for (const id of ids) recordSeen(id, firstSeen, counterRef);
    }
}

/** Standalone node declaration line (no arrow), e.g. A[...] or Start([...]). */
function visitStandaloneLine(line, firstSeen, counterRef) {
    const t = line.replace(/%%.*$/, '').trim();
    if (!t || /-->|---|==>|-\.->/.test(t)) return;
    if (/^(style|classDef|linkStyle|click|direction|class|subgraph)\b/i.test(t)) return;
    if (/^end\s*$/i.test(t)) return;
    const m = t.match(/^\s*([A-Za-z][A-Za-z0-9_]*)\s*[\[\(\{]/);
    if (m) recordSeen(m[1], firstSeen, counterRef);
}

function countLoopNodes(mermaid) {
    const empty = () => ({
        loops: 0,
        loopEdges: 0,
        nodeCount: 0,
        loopNodeIds: [],
        backwardExamples: new Map()
    });
    if (!mermaid || typeof mermaid !== 'string') {
        return empty();
    }

    const firstSeen = new Map();
    const counterRef = { n: 0 };
    const lines = mermaid.split(/\r?\n/);
    const allEdges = [];

    for (const raw of lines) {
        const line = raw.replace(/%%.*$/, '').trim();
        if (!line) continue;

        visitStandaloneLine(raw, firstSeen, counterRef);

        if (/^(style|classDef|linkStyle|click|direction)\b/i.test(line)) {
            const sm = line.match(/^style\s+([A-Za-z][A-Za-z0-9_]*)/i);
            if (sm) recordSeen(sm[1], firstSeen, counterRef);
            continue;
        }
        if (/^subgraph\b/i.test(line) || /^end\s*$/i.test(line)) continue;

        if (/-->|---|==>|-\.->/.test(line)) {
            visitLineForOrder(raw, firstSeen, counterRef);
            allEdges.push(...parseEdgesFromLine(raw));
        }
    }

    const loopNodes = new Set();
    let loopEdges = 0;
    for (const [u, v] of allEdges) {
        if (!firstSeen.has(u) || !firstSeen.has(v)) continue;
        if (firstSeen.get(v) < firstSeen.get(u)) {
            loopNodes.add(u);
            loopEdges += 1;
        }
    }

    return {
        loops: loopNodes.size,
        loopEdges,
        nodeCount: firstSeen.size,
        loopNodeIds: [...loopNodes].sort(),
        backwardExamples: collectBackwardExamples(allEdges, firstSeen, loopNodes)
    };
}

function collectBackwardExamples(edges, firstSeen, loopNodes, maxPerNode = 2) {
    const byU = new Map();
    for (const u of loopNodes) byU.set(u, []);
    for (const [u, v] of edges) {
        if (!loopNodes.has(u)) continue;
        if (!firstSeen.has(u) || !firstSeen.has(v)) continue;
        if (firstSeen.get(v) >= firstSeen.get(u)) continue;
        const list = byU.get(u);
        if (list.length < maxPerNode) {
            list.push({ v, iu: firstSeen.get(u), iv: firstSeen.get(v) });
        }
    }
    return byU;
}

function loadJson(p) {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function writeJson(p, obj) {
    fs.writeFileSync(p, JSON.stringify(obj, null, 2) + '\n', 'utf8');
}

function explainProcess(processId) {
    const processRoot = path.join(ROOT, 'glmp-v2', 'processes');
    for (const dir of PROCESS_DIRS) {
        const full = path.join(processRoot, dir, `${processId}.json`);
        if (!fs.existsSync(full)) continue;
        const data = loadJson(full);
        const r = countLoopNodes(data.mermaid);
        console.log(`\nProcess: ${data.name} (${processId})`);
        console.log(`Loop nodes (count): ${r.loops} — nodes with ≥1 outgoing edge to a node that appears earlier in the Mermaid file.`);
        console.log(`Backward edges (count): ${r.loopEdges}`);
        console.log(`Tracked node ids: ${r.nodeCount}\n`);
        console.log('Loop node ids:', r.loopNodeIds.join(', '));
        console.log('\nSample backward edges (source → earlier target):');
        for (const u of r.loopNodeIds) {
            const ex = r.backwardExamples.get(u) || [];
            for (const { v, iu, iv } of ex) {
                console.log(`  ${u} (order ${iu}) → ${v} (order ${iv})`);
            }
        }
        console.log(
            '\nNote: Mermaid layout can route arrows so these do not look like obvious “loops”; the metric is file order, not pixel Y-position.'
        );
        return;
    }
    console.error('Process not found:', processId);
    process.exit(1);
}

function main() {
    const argv = process.argv.slice(2);
    if (argv[0] === '--explain' && argv[1]) {
        explainProcess(argv[1]);
        return;
    }

    const processRoot = path.join(ROOT, 'glmp-v2', 'processes');
    const byId = new Map();

    for (const dir of PROCESS_DIRS) {
        const d = path.join(processRoot, dir);
        if (!fs.existsSync(d)) continue;
        for (const f of fs.readdirSync(d)) {
            if (!f.endsWith('.json')) continue;
            const full = path.join(d, f);
            const data = loadJson(full);
            const id = data.id;
            if (!id) continue;
            const r = countLoopNodes(data.mermaid);
            byId.set(id, { loops: r.loops, loopEdges: r.loopEdges });
        }
    }

    const metaPaths = [
        path.join(ROOT, 'glmp-v2', 'metadata.json'),
        path.join(ROOT, 'glmp-v2', 'data', 'metadata.json'),
        path.join(ROOT, 'glmp-v2', 'viewer', 'metadata.json')
    ];

    for (const metaPath of metaPaths) {
        if (!fs.existsSync(metaPath)) {
            console.warn('Skip missing', metaPath);
            continue;
        }
        const meta = loadJson(metaPath);
        if (!meta.processes) continue;

        for (const proc of meta.processes) {
            const c = byId.get(proc.id);
            proc.loops = c ? c.loops : 0;
        }

        if (!meta.statistics) meta.statistics = {};
        meta.statistics.loops = meta.processes.reduce((s, p) => s + (p.loops || 0), 0);
        meta.statistics.loopEdges = meta.processes.reduce(
            (s, p) => s + (byId.get(p.id)?.loopEdges || 0),
            0
        );

        meta.lastUpdated = new Date().toISOString().slice(0, 10);

        writeJson(metaPath, meta);
        console.log('Wrote', metaPath);
    }

    const sumLoops = [...byId.values()].reduce((s, x) => s + x.loops, 0);
    const sumEdges = [...byId.values()].reduce((s, x) => s + x.loopEdges, 0);
    console.log('Processes with diagrams:', byId.size);
    console.log('Sum of loop-node counts (per diagram):', sumLoops);
    console.log('Sum of backward edges:', sumEdges);
}

main();
