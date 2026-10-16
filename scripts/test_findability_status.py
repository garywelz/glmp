#!/usr/bin/env python3
"""Fixture tests for findability AUTO-STATUS parsing (stale anchors).

Run:  python scripts/test_findability_status.py
  or: pytest scripts/test_findability_status.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_master_todo import (  # noqa: E402
    format_findability_anchor_cells,
    parse_findability_report,
)


def _report_with_one_stale() -> dict:
    """Minimal probe JSON: 3 anchors, 1 stale, 0 alerts, 2 Check-C warnings."""
    return {
        "generated_at": "2026-10-16T15:00:00+00:00",
        "summary": {
            "check_a_total": 3,
            "check_a_alerts": 0,
            "check_a_stale": 1,
            "check_c_warnings": 2,
            "overall": "WARNING",
        },
        "check_a_positive_findability": [
            {
                "collection": "episodes",
                "query": "dependency structure of a library of formalized proofs",
                "expected_id": "ever-math-260010",
                "rank": 1,
                "severity": "pass",
            },
            {
                "collection": "episodes",
                "query": "gene editing without cutting DNA",
                "expected_id": "ever-bio-250007",
                "rank": None,
                "severity": "STALE ANCHOR",
                "reason": "document missing or not public",
            },
            {
                "collection": "physics_processes",
                "query": "why does a changing magnetic field create an electric current",
                "expected_id": "electromagnetism-electromagnetic-induction",
                "rank": 1,
                "severity": "pass",
            },
        ],
    }


def test_stale_anchor_not_counted_as_passing() -> None:
    parsed = parse_findability_report(_report_with_one_stale())
    assert parsed["anchors_total"] == 3
    assert parsed["alerts"] == 0
    assert parsed["stale"] == 1
    assert parsed["passing"] == 2  # total - alerts - stale
    assert parsed["stale_ids"] == ["ever-bio-250007"]
    assert parsed["overall"] == "WARNING"
    assert parsed["warnings"] == 2


def test_format_includes_stale_line() -> None:
    parsed = parse_findability_report(_report_with_one_stale())
    anchors_cell, stale_line = format_findability_anchor_cells(parsed)
    assert anchors_cell == "2/3 passing"
    assert stale_line == "stale anchors: 1 (`ever-bio-250007`)"


def test_no_stale_omits_line() -> None:
    report = {
        "summary": {
            "check_a_total": 2,
            "check_a_alerts": 0,
            "check_a_stale": 0,
            "check_c_warnings": 0,
            "overall": "OK",
        },
        "check_a_positive_findability": [
            {
                "collection": "glmp_processes",
                "query": "lactose metabolism switch",
                "expected_id": "ecoli_lac_operon",
                "rank": 1,
                "severity": "pass",
            },
            {
                "collection": "glmp_processes",
                "query": "negative feedback loop",
                "expected_id": "synthetic_negative_autoregulation",
                "rank": 1,
                "severity": "pass",
            },
        ],
    }
    parsed = parse_findability_report(report)
    anchors_cell, stale_line = format_findability_anchor_cells(parsed)
    assert parsed["passing"] == 2
    assert anchors_cell == "2/2 passing"
    assert stale_line is None


def test_legacy_report_without_check_a_stale_scans_rows() -> None:
    """Older probe JSON lacked check_a_stale; still must not count STALE as pass."""
    report = {
        "summary": {
            "check_a_total": 2,
            "check_a_alerts": 0,
            "check_c_warnings": 0,
            "overall": "WARNING",
        },
        "check_a_positive_findability": [
            {
                "collection": "episodes",
                "query": "old deleted episode",
                "expected_id": "ever-bio-250007",
                "rank": None,
                "severity": "STALE ANCHOR",
            },
            {
                "collection": "episodes",
                "query": "AlphaFold2 protein structure prediction",
                "expected_id": "ever-compsci-250041",
                "rank": 1,
                "severity": "pass",
            },
        ],
    }
    parsed = parse_findability_report(report)
    assert parsed["stale"] == 1
    assert parsed["passing"] == 1
    assert parsed["stale_ids"] == ["ever-bio-250007"]


if __name__ == "__main__":
    test_stale_anchor_not_counted_as_passing()
    test_format_includes_stale_line()
    test_no_stale_omits_line()
    test_legacy_report_without_check_a_stale_scans_rows()
    print("ok — 4 findability stale-anchor fixtures passed")
