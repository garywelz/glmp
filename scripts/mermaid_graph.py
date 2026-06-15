#!/usr/bin/env python3
"""
Parse GLMP Mermaid flowcharts into directed graphs and detect regulatory cycles.

Paper-aligned definition (GLMP Papers I / III):
  A *feedback loop* is a directed cycle in the regulatory subgraph.
  The `loops` field counts distinct nodes that lie on at least one directed cycle.

This replaces the legacy declaration-order back-edge heuristic, which inflated counts
when many edges converged on downstream hubs (e.g. ecoli_antibiotic_efflux_pumps).
"""

from __future__ import annotations

import re
from collections import defaultdict

ARROW_RE = re.compile(
    r"\s*(?:<-->|<==>|x--x|o--o|-\.-+>|-\.-+|--+>|--+|==+>|==+|--[xo]|[ox]--)\s*"
)

RESERVED = {
    "graph", "flowchart", "subgraph", "end", "style", "classdef", "class",
    "linkstyle", "direction", "click", "td", "tb", "bt", "rl", "lr",
}


def _strip_labels(line: str) -> str:
    """Remove edge labels |..| and node-shape brackets so only ids + arrows remain."""
    line = re.sub(r"\|[^|]*\|", " ", line)
    prev = None
    while prev != line:
        prev = line
        line = re.sub(r"\[\([^()\[\]]*\)\]", " ", line)
        line = re.sub(r"\[\[[^\[\]]*\]\]", " ", line)
        line = re.sub(r"\(\([^()]*\)\)", " ", line)
        line = re.sub(r"\{\{[^{}]*\}\}", " ", line)
        line = re.sub(r"\(\[[^()\[\]]*\]\)", " ", line)
        line = re.sub(r"\[[^\[\]]*\]", " ", line)
        line = re.sub(r"\([^()]*\)", " ", line)
        line = re.sub(r"\{[^{}]*\}", " ", line)
        line = re.sub(r">[^\]]*\]", " ", line)
    return line


def _first_id(segment: str) -> str | None:
    toks = re.findall(r"[A-Za-z][A-Za-z0-9_]*", segment or "")
    return toks[0] if toks else None


def parse_mermaid(mermaid: str) -> tuple[dict[str, int], list[tuple[str, str]]]:
    """
    Return (node_order, edges) from a Mermaid graph TD source.
    node_order maps first-seen node id -> declaration index (for legacy metric only).
    """
    order: dict[str, int] = {}
    edges: list[tuple[str, str]] = []

    for raw in (mermaid or "").splitlines():
        s = raw.strip()
        if not s or s.startswith("%%"):
            continue
        low = s.split()[0].lower() if s.split() else ""
        if low in RESERVED:
            continue

        cleaned = _strip_labels(s)
        if not ARROW_RE.search(cleaned):
            for tok in re.findall(r"[A-Za-z][A-Za-z0-9_]*", cleaned):
                order.setdefault(tok, len(order))
            continue

        parts = ARROW_RE.split(cleaned)
        ids = [_first_id(part) for part in parts]
        for nid in ids:
            if nid is not None:
                order.setdefault(nid, len(order))
        for a, b in zip(ids, ids[1:]):
            if a is not None and b is not None:
                edges.append((a, b))

    return order, edges


def count_legacy_back_edge_nodes(mermaid: str) -> int:
    """Legacy metric: nodes with an edge to an earlier-declared node."""
    order, edges = parse_mermaid(mermaid)
    loop_sources = {a for a, b in edges if a in order and b in order and order[b] < order[a]}
    return len(loop_sources)


def _tarjan_scc(graph: dict[str, list[str]], nodes: set[str]) -> list[list[str]]:
    index_counter = [0]
    stack: list[str] = []
    on_stack: set[str] = set()
    index: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        index[v] = lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])
        if lowlink[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for n in nodes:
        if n not in index:
            strongconnect(n)
    return sccs


def cycle_nodes(mermaid: str) -> set[str]:
    """Nodes that participate in at least one directed cycle."""
    _, edges = parse_mermaid(mermaid)
    graph: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for a, b in edges:
        graph[a].append(b)
        nodes.add(a)
        nodes.add(b)

    cyclic: set[str] = set()
    for a, b in edges:
        if a == b:
            cyclic.add(a)

    for comp in _tarjan_scc(graph, nodes):
        if len(comp) == 1:
            continue
        comp_set = set(comp)
        sub_edges = [(a, b) for a, b in edges if a in comp_set and b in comp_set]
        # A directed cycle exists in an SCC iff |E| >= |V| for this subgraph
        # (necessary) — verify with reachability within SCC.
        if _subgraph_has_cycle(comp, sub_edges):
            cyclic.update(comp)
    return cyclic


def _subgraph_has_cycle(nodes: list[str], edges: list[tuple[str, str]]) -> bool:
    graph: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}

    def dfs(u: str) -> bool:
        color[u] = GRAY
        for v in graph.get(u, []):
            if color.get(v) == GRAY:
                return True
            if color.get(v) == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    for n in nodes:
        if color[n] == WHITE and dfs(n):
            return True
    return False


def count_cycle_nodes(mermaid: str) -> int:
    """Paper-aligned loops: nodes on directed cycles."""
    return len(cycle_nodes(mermaid))


def count_cycle_edges(mermaid: str) -> int:
    """Edges that participate in at least one directed cycle."""
    _, edges = parse_mermaid(mermaid)
    on_cycle = cycle_nodes(mermaid)
    return sum(1 for a, b in edges if a in on_cycle and b in on_cycle)


def cycle_nodes_from_edges(edges: list[tuple[str, str]]) -> set[str]:
    """Cycle detection on an authored (src, dst) edge list."""
    if not edges:
        return set()
    lines = ["graph TD"] + [f"    {a} --> {b}" for a, b in edges]
    return cycle_nodes("\n".join(lines))


def compute_regulatory_stats(mermaid: str) -> dict:
    order, edges = parse_mermaid(mermaid)
    cyc = cycle_nodes(mermaid)
    conditionals = sum(
        1 for raw in (mermaid or "").splitlines()
        if "{" in raw and "-->" in raw and not raw.strip().startswith("%%")
    )
    return {
        "nodes": len(order),
        "edges": len(edges),
        "loops": len(cyc),
        "feedbackEdges": count_cycle_edges(mermaid),
        "legacyLoops": count_legacy_back_edge_nodes(mermaid),
        "conditionals": conditionals,
    }
