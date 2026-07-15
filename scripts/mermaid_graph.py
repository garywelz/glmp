#!/usr/bin/env python3
"""
Parse GLMP Mermaid flowcharts into directed graphs and detect cycles.

Two cycle metrics (do not conflate them):

  `loops` (legacy)
      Distinct nodes that lie on at least one directed cycle in the WHOLE graph.
      Conflates metabolic circularity and state-machine returns with regulatory
      feedback, and scales with cycle SIZE (nodes on the tour), not feedback COUNT.

  `feedback_loops` (requires an edge type map)
      Count of simple cycles that contain >= 1 regulatory edge
      (activates / represses / sequesters / modifies / induces). Counted per cycle,
      never per-SCC. Returns None when no edge type map is supplied — absence of
      typing must not masquerade as absence of feedback.

Paper-aligned intent (GLMP Papers I / III): a feedback loop is a directed cycle
involving regulatory interactions. The legacy `loops` field does not implement that.

This module also retains the legacy declaration-order back-edge heuristic as
`legacyLoops` for comparison.
"""

from __future__ import annotations

import re
import time
from collections import defaultdict
from typing import Any

ARROW_RE = re.compile(
    r"\s*(?:<-->|<==>|x--x|o--o|-\.-+>|-\.-+|--+>|--+|==+>|==+|--[xo]|[ox]--)\s*"
)

RESERVED = {
    "graph", "flowchart", "subgraph", "end", "style", "classdef", "class",
    "linkstyle", "direction", "click", "td", "tb", "bt", "rl", "lr",
}

REGULATORY_EDGE_TYPES = frozenset(
    {"activates", "represses", "sequesters", "modifies", "induces"}
)

# Enumeration insurance (probes: densest chart ~72 cycles in ~8ms)
DEFAULT_MAX_CYCLES = 10_000
DEFAULT_MAX_SECONDS = 60.0
DEFAULT_MAX_CYCLE_LEN = 80


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
    """Nodes that participate in at least one directed cycle (whole graph)."""
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
    """Legacy `loops`: count of distinct nodes on any whole-graph directed cycle."""
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


def _unique_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []
    for e in edges:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out


def _enumerate_simple_cycles(
    edges: list[tuple[str, str]],
    max_cycles: int = DEFAULT_MAX_CYCLES,
    max_seconds: float = DEFAULT_MAX_SECONDS,
    max_len: int = DEFAULT_MAX_CYCLE_LEN,
) -> tuple[list[tuple[str, ...]], bool]:
    """
    Enumerate simple cycles in a digraph.
    Returns (cycles, capped). If capped, the cycle list must not be trusted as complete.
    """
    t0 = time.perf_counter()
    succ: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for a, b in edges:
        succ[a].append(b)
        nodes.add(a)
        nodes.add(b)

    cycles: list[tuple[str, ...]] = []
    seen: set[tuple[str, ...]] = set()
    capped = False

    def add_cycle(body: tuple[str, ...]) -> None:
        if not body:
            return
        rotations = [body[i:] + body[:i] for i in range(len(body))]
        canon = min(rotations)
        if canon not in seen:
            seen.add(canon)
            cycles.append(canon)

    def timed_out() -> bool:
        return (time.perf_counter() - t0) >= max_seconds

    for comp in _tarjan_scc(succ, nodes):
        if capped or timed_out() or len(cycles) >= max_cycles:
            capped = True
            break

        if len(comp) == 1:
            v = comp[0]
            if v in succ.get(v, []):
                add_cycle((v,))
            continue

        comp_set = set(comp)
        sub: dict[str, list[str]] = defaultdict(list)
        for u in comp:
            for w in succ.get(u, ()):
                if w in comp_set:
                    sub[u].append(w)

        order = sorted(comp)

        def dfs(start: str, path: list[str]) -> None:
            nonlocal capped
            if capped:
                return
            if timed_out() or len(cycles) >= max_cycles:
                capped = True
                return
            u = path[-1]
            for v in sub.get(u, []):
                if v == start:
                    add_cycle(tuple(path))
                    if len(cycles) >= max_cycles:
                        capped = True
                        return
                    continue
                if v in path:
                    continue
                if v < start:
                    continue
                if len(path) >= max_len:
                    continue
                path.append(v)
                dfs(start, path)
                path.pop()
                if capped:
                    return

        for start in order:
            if capped:
                break
            dfs(start, [start])

    if timed_out() or len(cycles) >= max_cycles:
        # Cap hit during or at end of search — treat as incomplete.
        # (If we exactly filled max_cycles, we cannot know whether more exist.)
        if len(cycles) >= max_cycles or timed_out():
            capped = True

    return cycles, capped


def _is_regulatory(
    edge_type: str | None,
    *,
    untypable_as_regulatory: bool,
) -> bool:
    if edge_type is None:
        return False
    if edge_type in REGULATORY_EDGE_TYPES:
        return True
    if edge_type == "UNTYPABLE" and untypable_as_regulatory:
        return True
    return False


def compute_feedback_loops(
    mermaid: str,
    edge_types: dict[tuple[str, str], str] | None,
    untypable_as_regulatory: bool = False,
    *,
    max_cycles: int = DEFAULT_MAX_CYCLES,
    max_seconds: float = DEFAULT_MAX_SECONDS,
) -> dict[str, Any]:
    """
    Count simple cycles that contain >= 1 regulatory edge (Rule B).

    Parameters
    ----------
    mermaid:
        Mermaid flowchart source.
    edge_types:
        Map (source_id, target_id) -> type string. Regulatory types:
        activates, represses, sequesters, modifies, induces.
        Non-regulatory: produces, consumes, transitions, proceeds.
        UNTYPABLE is non-regulatory unless untypable_as_regulatory=True.
        If edge_types is None or empty, feedback_loops is None (not 0).
    untypable_as_regulatory:
        When True, UNTYPABLE edges count as regulatory for the keep-condition.

    Returns
    -------
    dict with keys:
      feedback_loops      — int count of kept cycles, or None if untyped / capped
      feedback_loop_nodes — int distinct nodes on kept cycles, or None if untyped / capped
      kept_cycles         — list of node-id sequences (tuples), empty if none/untyped/capped
      raw_cycle_count     — int simple cycles enumerated before filter (0 if untyped;
                            incomplete if capped)
      capped              — True if enumeration hit max_cycles or timeout
    """
    empty = {
        "feedback_loops": None,
        "feedback_loop_nodes": None,
        "kept_cycles": [],
        "raw_cycle_count": 0,
        "capped": False,
    }

    if not edge_types:
        return dict(empty)

    _, edges = parse_mermaid(mermaid)
    edges = _unique_edges(edges)
    cycles, capped = _enumerate_simple_cycles(
        edges, max_cycles=max_cycles, max_seconds=max_seconds
    )

    if capped:
        return {
            "feedback_loops": None,
            "feedback_loop_nodes": None,
            "kept_cycles": [],
            "raw_cycle_count": len(cycles),
            "capped": True,
        }

    kept: list[tuple[str, ...]] = []
    for cyc in cycles:
        has_reg = False
        for i, u in enumerate(cyc):
            v = cyc[(i + 1) % len(cyc)]
            et = edge_types.get((u, v))
            if _is_regulatory(et, untypable_as_regulatory=untypable_as_regulatory):
                has_reg = True
                break
        if has_reg:
            kept.append(cyc)

    nodes: set[str] = set()
    for cyc in kept:
        nodes.update(cyc)

    return {
        "feedback_loops": len(kept),
        "feedback_loop_nodes": len(nodes),
        "kept_cycles": kept,
        "raw_cycle_count": len(cycles),
        "capped": False,
    }


def compute_regulatory_stats(
    mermaid: str,
    edge_types: dict[tuple[str, str], str] | None = None,
    untypable_as_regulatory: bool = False,
) -> dict:
    """
    Compute graph / cycle stats for a Mermaid chart.

    Existing keys (loops, feedbackEdges, legacyLoops, …) are unchanged in meaning.
    When edge_types is provided, also includes feedback_loops / feedback_loop_nodes
    / feedback_loops_capped / feedback_loops_raw_cycle_count from
    compute_feedback_loops. Without edge_types, feedback_loops is None.
    """
    order, edges = parse_mermaid(mermaid)
    cyc = cycle_nodes(mermaid)
    conditionals = sum(
        1 for raw in (mermaid or "").splitlines()
        if "{" in raw and "-->" in raw and not raw.strip().startswith("%%")
    )
    out: dict[str, Any] = {
        "nodes": len(order),
        "edges": len(edges),
        "loops": len(cyc),
        "feedbackEdges": count_cycle_edges(mermaid),
        "legacyLoops": count_legacy_back_edge_nodes(mermaid),
        "conditionals": conditionals,
    }
    fb = compute_feedback_loops(
        mermaid, edge_types, untypable_as_regulatory=untypable_as_regulatory
    )
    out["feedback_loops"] = fb["feedback_loops"]
    out["feedback_loop_nodes"] = fb["feedback_loop_nodes"]
    out["feedback_loops_capped"] = fb["capped"]
    out["feedback_loops_raw_cycle_count"] = fb["raw_cycle_count"]
    return out
