#!/usr/bin/env python3
"""
Dual-scenario feedback_loops: gate outcomes as regulatory vs non-regulatory.
Rules 1 and 3 apply in both. Rule 2 retired as binding.
Read charts; write sensitivity TSV only.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mermaid_graph import (  # noqa: E402
    parse_mermaid,
    count_cycle_nodes,
    compute_feedback_loops,
    _enumerate_simple_cycles,
    _unique_edges,
)
import _type_cycle_batch as T  # noqa: E402

HARVEST = Path(__file__).resolve().parent
PROCESSES = ROOT / "glmp-v2" / "processes"
OUT = HARVEST / "feedback_loops_gate_sensitivity.tsv"
BAR = "\u22a3"
MINUS = "\u2212"

FIXTURES = {
    "ecoli_tca_cycle": 0,
    "ecoli_tryptophan_biosynthesis": 2,
    "human_nfkb_ikb_oscillator": 1,
    "human_ampk_energy_homeostat": 1,
    "yeast_cell_cycle_control": 1,
    "ecoli_base_excision_repair": 0,
    "human_oct4_sox2_nanog_pluripotency": 2,
    "ecoli_sos_lexa": 1,
    "drosophila_gap_gene_network": 4,
    "ecoli_lac_operon": 0,
    "human_camp_pka_desensitization": 2,
    "ecoli_iron_homeostasis": 5,
    "human_iron_irp_ire": 1,
    "yeast_yeast_glycolysis_regulation": 2,
    "human_mtorc1_nutrient": 1,
    "ecoli_phosphate_regulation": 4,
}


def cycle_edge_set(m: str) -> set[tuple[str, str]]:
    _, edges = parse_mermaid(m)
    cycles, capped = _enumerate_simple_cycles(_unique_edges(edges))
    if capped:
        raise RuntimeError("capped")
    return {(c[i], c[(i + 1) % len(c)]) for c in cycles for i in range(len(c))}


def chart_path(cid: str) -> Path:
    hits = list(PROCESSES.rglob(f"{cid}.json"))
    if not hits:
        raise FileNotFoundError(cid)
    return hits[0]


def load_base_types() -> dict[str, dict[tuple[str, str], str]]:
    tm: dict[str, dict[tuple[str, str], str]] = defaultdict(dict)
    for fn in ["pilot_edge_types.retyped.tsv", "pilot_edge_types_round2.retyped.tsv"]:
        with (HARVEST / fn).open(encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                tm[r["chart_id"]][(r["source_id"], r["target_id"])] = r["edge_type"]
    with (HARVEST / "cycle_edge_types.tsv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            tm[r["chart_id"]][(r["source_id"], r["target_id"])] = r["edge_type"]
    return tm


def apply_rule1(src_lab: str, tgt_lab: str, elab: str) -> str | None:
    el = (elab or "").strip()
    ell = el.lower()
    sl, tl = (src_lab or "").lower(), (tgt_lab or "").lower()
    if (
        BAR in el
        or MINUS in el
        or ell in {"-|", "--o", "x", "inhibit", "inhibits", "represses"}
        or re.match(r"^[-−]\s*feedback", ell)
    ):
        if "sequester" in sl or "sequester" in tl:
            return "sequesters"
        return "represses"
    if (
        ell in {"+", "activates", "enhances", "enhance", "stimulates", "stimulate"}
        or ell.startswith("activates")
        or ell.startswith("+")
    ):
        return "activates"
    if re.search(r"\binhibit", ell) or re.search(r"\brepress", ell):
        return "represses"
    return None


def apply_rule3(src_lab: str, tgt_lab: str) -> str | None:
    if T.expression_own_product(src_lab, tgt_lab):
        return "produces"
    return None


def build_chart_context(cid: str, m: str):
    meta = T.node_meta(m)
    order, _ = parse_mermaid(m)
    for nid in order:
        meta.setdefault(nid, {"label": nid, "shape_raw": "", "is_decision": False})
        if meta[nid]["label"].endswith("?"):
            meta[nid]["is_decision"] = True
    cyc = cycle_edge_set(m)
    label_map: dict[tuple[str, str], str] = {}
    for a, b, el in T.parse_edge_instances(m):
        if (a, b) in cyc and (a, b) not in label_map:
            label_map[(a, b)] = el
    return meta, cyc, label_map


def is_gate_edge(src_id: str, elab: str, meta: dict) -> bool:
    if not (elab or "").strip():
        return False
    return bool(meta.get(src_id, {}).get("is_decision"))


def main() -> None:
    base = load_base_types()
    rows_out = []
    fixture_rows = []
    gate_edge_counts = Counter()
    n_rule1 = n_rule3 = 0

    charts = []
    for p in sorted(PROCESSES.rglob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        m = d.get("mermaid") or ""
        if not m:
            continue
        try:
            cyc = cycle_edge_set(m)
        except RuntimeError:
            continue
        if not cyc and p.stem not in FIXTURES:
            continue
        # include lac (0 cycles) as fixture-only later
        if cyc:
            charts.append((p.stem, d, m, cyc))

    # also ensure all FIXTURES present
    fixture_ids = set(FIXTURES)
    have = {c[0] for c in charts}
    for cid in fixture_ids - have:
        d = json.loads(chart_path(cid).read_text(encoding="utf-8"))
        m = d.get("mermaid") or ""
        try:
            cyc = cycle_edge_set(m) if m else set()
        except RuntimeError:
            cyc = set()
        charts.append((cid, d, m, cyc))

    for cid, d, m, cyc in charts:
        meta, cyc, label_map = build_chart_context(cid, m)
        tm_reg: dict[tuple[str, str], str] = {}
        tm_non: dict[tuple[str, str], str] = {}
        n_gates = 0

        # start from all base edges for this chart (cycle + off-cycle for safety)
        keys = set(base.get(cid, {}).keys()) | set(cyc)
        for a, b in keys:
            prior = base.get(cid, {}).get((a, b), "proceeds")
            src_lab = meta.get(a, {}).get("label", a)
            tgt_lab = meta.get(b, {}).get("label", b)
            elab = label_map.get((a, b), "")
            # if edge not in cycle label_map, try empty
            if (a, b) not in label_map:
                # off-cycle or unlabeled
                elab = elab or ""

            et = prior
            r1 = apply_rule1(src_lab, tgt_lab, elab)
            if r1:
                et = r1
                n_rule1 += 1
                tm_reg[(a, b)] = et
                tm_non[(a, b)] = et
                continue
            r3 = apply_rule3(src_lab, tgt_lab)
            if r3:
                et = r3
                n_rule3 += 1
                tm_reg[(a, b)] = et
                tm_non[(a, b)] = et
                continue

            if (a, b) in cyc and is_gate_edge(a, elab, meta):
                n_gates += 1
                pol = T.branch_polarity(elab, tgt_lab) or "activates"
                tm_reg[(a, b)] = pol
                tm_non[(a, b)] = "proceeds"
            else:
                tm_reg[(a, b)] = et
                tm_non[(a, b)] = et

        gate_edge_counts[cid] = n_gates

        if not cyc:
            fl_reg = fl_non = 0
            fln_reg = fln_non = 0
        else:
            fb_reg = compute_feedback_loops(m, tm_reg)
            fb_non = compute_feedback_loops(m, tm_non)
            fl_reg = fb_reg["feedback_loops"]
            fl_non = fb_non["feedback_loops"]
            fln_reg = fb_reg["feedback_loop_nodes"]
            fln_non = fb_non["feedback_loop_nodes"]

        loops = count_cycle_nodes(m) if m else 0
        cc = str(d.get("circuitClass") or "")
        invariant = fl_reg == fl_non
        rows_out.append(
            {
                "chart_id": cid,
                "circuitClass": cc,
                "loops": loops,
                "n_gate_cycle_edges": n_gates,
                "feedback_loops_gates_as_reg": fl_reg,
                "feedback_loops_gates_as_nonreg": fl_non,
                "feedback_loop_nodes_gates_as_reg": fln_reg,
                "feedback_loop_nodes_gates_as_nonreg": fln_non,
                "invariant": "true" if invariant else "false",
                "delta": (fl_reg - fl_non) if fl_reg is not None and fl_non is not None else "",
            }
        )

    # only cycle-bearing for the 132 claim (exclude lac from the 132 if 0 cycles)
    cycle_bearing = [r for r in rows_out if int(r["loops"]) > 0 or int(r["n_gate_cycle_edges"]) > 0]
    # better: charts that have directed cycles
    cycle_bearing = []
    for r in rows_out:
        m = json.loads(chart_path(r["chart_id"]).read_text(encoding="utf-8")).get("mermaid") or ""
        try:
            cyc = cycle_edge_set(m) if m else set()
        except RuntimeError:
            cyc = set()
        if cyc:
            cycle_bearing.append(r)

    # write all rows including lac
    with OUT.open("w", encoding="utf-8", newline="") as f:
        cols = [
            "chart_id",
            "circuitClass",
            "loops",
            "n_gate_cycle_edges",
            "feedback_loops_gates_as_reg",
            "feedback_loops_gates_as_nonreg",
            "feedback_loop_nodes_gates_as_reg",
            "feedback_loop_nodes_gates_as_nonreg",
            "invariant",
            "delta",
        ]
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in sorted(rows_out, key=lambda x: x["chart_id"]):
            w.writerow({k: r[k] for k in cols})

    inv = [r for r in cycle_bearing if r["invariant"] == "true"]
    sens = [r for r in cycle_bearing if r["invariant"] == "false"]

    print(f"Wrote {OUT}")
    print(f"Rule1 overlays applied (edge instances): {n_rule1}")
    print(f"Rule3 overlays applied (edge instances): {n_rule3}")
    print(f"Cycle-bearing charts: {len(cycle_bearing)}")
    print(f"INVARIANT: {len(inv)} / {len(cycle_bearing)}")
    print(f"SENSITIVE: {len(sens)} / {len(cycle_bearing)}")
    print("\nSensitive charts (gates_as_reg -> gates_as_nonreg):")
    for r in sorted(sens, key=lambda x: (-abs(int(x["delta"])), x["chart_id"])):
        print(
            f"  {r['chart_id']} [{r['circuitClass']}]  "
            f"fl_reg={r['feedback_loops_gates_as_reg']}  "
            f"fl_nonreg={r['feedback_loops_gates_as_nonreg']}  "
            f"delta={r['delta']:+}  gate_edges={r['n_gate_cycle_edges']}"
        )

    print("\n=== Fixtures under BOTH scenarios ===")
    all_ok = True
    for cid, exp in FIXTURES.items():
        r = next(x for x in rows_out if x["chart_id"] == cid)
        fr, fn = r["feedback_loops_gates_as_reg"], r["feedback_loops_gates_as_nonreg"]
        # lac: both 0
        ok_reg = fr == exp
        ok_non = fn == exp
        if not (ok_reg and ok_non):
            all_ok = False
        print(
            f"  {cid}: expected={exp}  reg={fr}{' OK' if ok_reg else ' FAIL'}  "
            f"nonreg={fn}{' OK' if ok_non else ' FAIL'}  invariant={r['invariant']}"
        )
    print(f"All fixtures hold under BOTH: {all_ok}")

    # class breakdown of sensitive
    print("\nSensitive by circuitClass:", dict(Counter(r["circuitClass"] for r in sens)))
    print(
        "II/III/IV with fl_nonreg==0:",
        [
            r["chart_id"]
            for r in cycle_bearing
            if r["circuitClass"] in {"II", "III", "IV"}
            and r["feedback_loops_gates_as_nonreg"] == 0
        ],
    )
    print(
        "II/III/IV with fl_reg==0:",
        [
            r["chart_id"]
            for r in cycle_bearing
            if r["circuitClass"] in {"II", "III", "IV"}
            and r["feedback_loops_gates_as_reg"] == 0
        ],
    )

    # claim line
    print(
        f"\nCLAIM: Decision-gate outcomes are a contested edge class. "
        f"We compute feedback_loops with gate branches treated as regulatory and as "
        f"non-regulatory. {len(inv)} of {len(cycle_bearing)} charts are invariant; "
        f"we name those that are not ({len(sens)})."
    )


if __name__ == "__main__":
    main()
