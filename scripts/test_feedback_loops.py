#!/usr/bin/env python3
"""
Fixture tests for compute_feedback_loops against pilot edge-type TSVs.

Run:  python scripts/test_feedback_loops.py
  or: pytest scripts/test_feedback_loops.py -q
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mermaid_graph import (  # noqa: E402
    compute_feedback_loops,
    compute_regulatory_stats,
    count_cycle_nodes,
)

PROCESSES = ROOT / "glmp-v2" / "processes"
PILOT = ROOT / "collaborations" / "krampis-virtual-cell" / "harvest" / "pilot_edge_types.tsv"
ROUND2 = (
    ROOT
    / "collaborations"
    / "krampis-virtual-cell"
    / "harvest"
    / "pilot_edge_types_round2.tsv"
)

# Verified pilot numbers — do not adjust code to force a match
FIXTURES: dict[str, int] = {
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


def load_edge_types() -> dict[str, dict[tuple[str, str], str]]:
    by_chart: dict[str, dict[tuple[str, str], str]] = defaultdict(dict)
    for path in (PILOT, ROUND2):
        assert path.is_file(), f"missing type sidecar: {path}"
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                key = (row["source_id"], row["target_id"])
                by_chart[row["chart_id"]][key] = row["edge_type"]
    return by_chart


def load_mermaid(chart_id: str) -> str:
    matches = list(PROCESSES.rglob(f"{chart_id}.json"))
    assert matches, f"chart not found: {chart_id}"
    data = json.loads(matches[0].read_text(encoding="utf-8"))
    return data["mermaid"]


def test_empty_types_returns_none():
    mermaid = load_mermaid("human_ampk_energy_homeostat")
    r = compute_feedback_loops(mermaid, {})
    assert r["feedback_loops"] is None, f"expected None, got {r['feedback_loops']!r}"
    r2 = compute_feedback_loops(mermaid, None)
    assert r2["feedback_loops"] is None
    stats = compute_regulatory_stats(mermaid)  # no edge_types
    assert stats["feedback_loops"] is None
    # existing keys still present and numeric
    assert isinstance(stats["loops"], int)
    assert isinstance(stats["feedbackEdges"], int)
    assert isinstance(stats["legacyLoops"], int)


def test_fixtures():
    types = load_edge_types()
    failures = []
    results = []
    for chart_id, expected in FIXTURES.items():
        mermaid = load_mermaid(chart_id)
        et = types.get(chart_id)
        assert et, f"no edge types for {chart_id}"
        r = compute_feedback_loops(mermaid, et)
        got = r["feedback_loops"]
        capped = r["capped"]
        ok = (got == expected) and (capped is False)
        results.append((chart_id, expected, got, capped, ok))
        if not ok:
            failures.append(
                f"{chart_id}: expected feedback_loops={expected}, "
                f"got {got!r} capped={capped} raw={r['raw_cycle_count']}"
            )
    return results, failures


def test_existing_loops_unchanged():
    """Adding feedback_loops must not change legacy loops computation."""
    for chart_id in (
        "ecoli_tca_cycle",
        "human_ampk_energy_homeostat",
        "ecoli_lac_operon",
    ):
        mermaid = load_mermaid(chart_id)
        direct = count_cycle_nodes(mermaid)
        stats = compute_regulatory_stats(mermaid)
        assert stats["loops"] == direct


def main() -> int:
    print("test_empty_types_returns_none ...", end=" ")
    try:
        test_empty_types_returns_none()
        print("PASS")
        empty_ok = True
    except AssertionError as e:
        print(f"FAIL: {e}")
        empty_ok = False

    print("test_existing_loops_unchanged ...", end=" ")
    try:
        test_existing_loops_unchanged()
        print("PASS")
        legacy_ok = True
    except AssertionError as e:
        print(f"FAIL: {e}")
        legacy_ok = False

    print("fixture feedback_loops:")
    results, failures = test_fixtures()
    for chart_id, expected, got, capped, ok in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {chart_id}: expected={expected} got={got} capped={capped}")

    if failures:
        print("\nSTOP — fixture disagreement(s):")
        for f in failures:
            print(f"  {f}")
        return 1

    if not empty_ok or not legacy_ok:
        return 1

    print("\nAll fixtures passed. Existing loops keys unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
