#!/usr/bin/env python3
"""
Honest re-decode: all completed E. coli circuits with JASPAR off + custom PWMs only.

Reads manifests from queue/completed/, validates sequences, runs FIMO + parser,
writes new results/*_logic_YYYYMMDD.json. Does not move manifests or touch Firestore.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from run_batch import (  # noqa: E402
    QUEUE,
    RESULTS_DIR,
    fetch_sequence,
    jaspar_enabled,
    run_fimo,
    run_parser,
)

COMPLETED = QUEUE / "completed"
CUSTOM_PWM = frozenset({
    "LacI_lacO1", "LacI_lacO", "TrpR_trpO", "LexA_SOS_box", "CRP_CAP",
})
JASPAR_RE = re.compile(r"^MA\d+\.\d+$")


def latest_logic_json(circuit_id: str) -> Path | None:
    matches = sorted(RESULTS_DIR.glob(f"{circuit_id}_logic_*.json"))
    return matches[-1] if matches else None


def load_before_class(circuit_id: str) -> str | None:
    path = latest_logic_json(circuit_id)
    if not path:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("dna_topology_class")


def count_eligible_ands(relationships: list, binding_sites: list) -> dict:
    """Mirror parser eligibility for AND gates (post-decode summary)."""
    site_index = {
        (s["motif_id"], s["start"], s["stop"]): s for s in binding_sites
    }

    def lookup(site_id: str, pos: str) -> dict | None:
        if not pos:
            return None
        sep = "–" if "–" in pos else "-"
        parts = pos.split(sep)
        if len(parts) == 2:
            try:
                key = (site_id, int(parts[0]), int(parts[1]))
                if key in site_index:
                    return site_index[key]
            except ValueError:
                pass
        for s in binding_sites:
            if s["motif_id"] == site_id:
                return s
        return None

    from glmp_logic_parser import (  # noqa: WPS433
        CONFIDENCE_Q_THRESHOLD,
        _relationship_eligible_for_classification,
        _relationship_is_confident,
        BindingSite,
        LogicalRelationship,
    )

    rel_objs = []
    for r in relationships:
        sa = lookup(r["site_a"], r.get("site_a_pos", ""))
        sb = lookup(r["site_b"], r.get("site_b_pos", ""))
        if not sa or not sb:
            continue
        bs_a = BindingSite(
            sa["motif_id"], sa.get("motif_alt", ""), "x",
            sa["start"], sa["stop"], sa.get("strand", "+"),
            sa.get("score", 0), sa.get("pvalue", 1), sa.get("qvalue", 1),
            sa.get("matched_seq", ""),
        )
        bs_b = BindingSite(
            sb["motif_id"], sb.get("motif_alt", ""), "x",
            sb["start"], sb["stop"], sb.get("strand", "+"),
            sb.get("score", 0), sb.get("pvalue", 1), sb.get("qvalue", 1),
            sb.get("matched_seq", ""),
        )
        rel_objs.append(LogicalRelationship(
            bs_a, bs_b, r["distance_bp"], r["logic_type"],
            r.get("confidence", "medium"), r.get("rule_applied", ""),
            r.get("notes", ""),
        ))

    eligible_ands = [
        r for r in rel_objs
        if r.logic_type == "AND"
        and _relationship_eligible_for_classification(r, CONFIDENCE_Q_THRESHOLD)
        and _relationship_is_confident(r, CONFIDENCE_Q_THRESHOLD)
    ]
    jaspar = sum(
        1 for r in eligible_ands
        if JASPAR_RE.match(r.site_a.motif_id) or JASPAR_RE.match(r.site_b.motif_id)
    )
    custom_only = sum(
        1 for r in eligible_ands
        if r.site_a.motif_id in CUSTOM_PWM and r.site_b.motif_id in CUSTOM_PWM
    )
    return {
        "eligible_and_total": len(eligible_ands),
        "jaspar_involved_and": jaspar,
        "custom_pwm_only_and": custom_only,
    }


def redecode_manifest(manifest_path: Path, dry_run: bool = False) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    circuit_id = manifest["circuit_id"]
    before = load_before_class(circuit_id)

    row = {
        "circuit_id": circuit_id,
        "before": before,
        "after": None,
        "glmp_biological_class": manifest.get("glmp_biological_class"),
        "jaspar_enabled": jaspar_enabled(manifest),
        "custom_pwm_files": manifest.get("custom_pwm_files") or [],
        "eligible_and_total": 0,
        "jaspar_involved_and": 0,
        "custom_pwm_only_and": 0,
        "error": None,
    }

    if dry_run:
        row["after"] = "DRY_RUN"
        return row

    running_path = QUEUE / "running" / manifest_path.name
    running_path.parent.mkdir(parents=True, exist_ok=True)
    running_path.write_text(manifest_path.read_text(encoding="utf-8"), encoding="utf-8")

    try:
        seq_file = fetch_sequence(manifest, dry_run=False)
        jaspar_hits, prok_hits = run_fimo(manifest, seq_file, dry_run=False)
        result = run_parser(manifest, jaspar_hits, prok_hits, dry_run=False)
        row["after"] = result.get("dna_topology_class")
        and_counts = count_eligible_ands(
            result.get("relationships", []),
            result.get("binding_sites", []),
        )
        row.update(and_counts)
    except Exception as exc:
        row["error"] = str(exc)
    finally:
        if running_path.exists():
            running_path.unlink()

    return row


def main():
    parser = argparse.ArgumentParser(description="Honest re-decode (JASPAR off for E. coli)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifests = sorted(COMPLETED.glob("*.yaml"))
    if not manifests:
        print(f"No manifests in {COMPLETED}", file=sys.stderr)
        sys.exit(1)

    print(f"Honest re-decode — {len(manifests)} circuits — {datetime.now(timezone.utc).isoformat()}")
    print(f"Parser path: JASPAR off for ecoli_k12 by default\n")
    print(
        f"{'circuit_id':<40} {'before':<22} {'after':<22} "
        f"{'bio':<6} {'AND':>4} {'jaspar_AND':>10}"
    )
    print("-" * 110)

    rows = []
    for path in manifests:
        row = redecode_manifest(path, dry_run=args.dry_run)
        rows.append(row)
        print(
            f"{row['circuit_id']:<40} {str(row['before']):<22} {str(row['after']):<22} "
            f"{str(row['glmp_biological_class']):<6} {row['eligible_and_total']:>4} "
            f"{row['jaspar_involved_and']:>10}"
            + (f"  ERROR: {row['error']}" if row.get("error") else "")
        )

    totals = {
        "eligible_and_total": sum(r["eligible_and_total"] for r in rows),
        "jaspar_involved_and": sum(r["jaspar_involved_and"] for r in rows),
        "custom_pwm_only_and": sum(r["custom_pwm_only_and"] for r in rows),
    }
    print("-" * 110)
    print(f"TOTALS eligible_AND={totals['eligible_and_total']} "
          f"jaspar_AND={totals['jaspar_involved_and']} "
          f"custom_only_AND={totals['custom_pwm_only_and']}")

    out = RESULTS_DIR / f"honest_redecode_summary_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    if not args.dry_run:
        out.write_text(json.dumps({"rows": rows, "totals": totals}, indent=2), encoding="utf-8")
        print(f"\nSummary written: {out}")


if __name__ == "__main__":
    main()
