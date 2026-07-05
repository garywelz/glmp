#!/usr/bin/env python3
"""Re-decode a fixed regression set from queue/completed manifests (no Firestore)."""
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from run_batch import (  # noqa: E402
    DECODER_DIR,
    QUEUE,
    RESULTS_DIR,
    fetch_sequence,
    run_fimo,
    run_parser,
    log,
)

REGRESSION_CIRCUITS = [
    "ecoli_lac_operon",
    "ecoli_ara_operon",
    "ecoli_trp_operon",
    "ecoli_sos_lexa",
    "ecoli_sos_reca",
    "ecoli_flhdc_flagellar",
    "ecoli_lambda_switch",
    "ecoli_dna_damage_checkpoint",
]

OLD_REFERENCE = {
    "ecoli_lac_operon": RESULTS_DIR / "lac_operon_logic_v2.json",
    "ecoli_ara_operon": RESULTS_DIR / "ara_operon_logic_v3.json",
    "ecoli_trp_operon": RESULTS_DIR / "trp_operon_logic_v4.json",
    "ecoli_sos_lexa": RESULTS_DIR / "ecoli_sos_lexa_logic_20260702.json",
    "ecoli_sos_reca": RESULTS_DIR / "ecoli_sos_reca_logic_20260702.json",
    "ecoli_flhdc_flagellar": RESULTS_DIR / "ecoli_flhdc_flagellar_logic_20260701.json",
    "ecoli_lambda_switch": RESULTS_DIR / "ecoli_lambda_switch_logic_20260703.json",
    "ecoli_dna_damage_checkpoint": RESULTS_DIR / "ecoli_dna_damage_checkpoint_logic_20260705.json",
}


def load_old_class(path: Path) -> str:
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("dna_topology_class", "?")


def redecode_one(circuit_id: str) -> dict:
    manifest_path = QUEUE / "completed" / f"{circuit_id}.yaml"
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    running_path = QUEUE / "running" / f"{circuit_id}.yaml"
    running_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(manifest_path, running_path)

    log.info("Re-decoding %s", circuit_id)
    seq_file = fetch_sequence(manifest, dry_run=False)
    fimo_hits, prok_hits = run_fimo(manifest, seq_file, dry_run=False)
    result = run_parser(manifest, fimo_hits, prok_hits, dry_run=False)

    if running_path.exists():
        running_path.unlink()

    return result


def reason_from_result(result: dict) -> str:
    note = result.get("dna_topology_note") or ""
    stats = (result.get("logic_summary") or {}).get("classification_confidence") or {}
    has_not = (result.get("logic_summary") or {}).get("has_not_gate")
    has_and = (result.get("logic_summary") or {}).get("has_and_gate")
    total = stats.get("supporting_gates_total", 0)
    cls = result.get("dna_topology_class")
    if cls == "I/II":
        return (
            f"eligible NOT gates ({total} supporting); eligible AND absent "
            f"(has_not={has_not}, has_and={has_and}) — repression-only I/II"
        )
    if cls == "INSUFFICIENT_EVIDENCE":
        return note or "zero confident identified-regulator gates"
    if cls == "INDETERMINATE":
        return note or "confident OR/XOR; no NOT/AND resolution"
    if cls == "II":
        return f"eligible NOT and AND present (supporting={total})"
    if cls == "I":
        return "eligible AND without NOT — activation-only I"
    return note or ""


def main():
    parser = argparse.ArgumentParser(description="Re-decode 8-circuit regression set")
    parser.add_argument(
        "--circuits", nargs="*", default=REGRESSION_CIRCUITS,
        help="Circuit IDs (default: all 8 regression targets)",
    )
    args = parser.parse_args()

    rows = []
    for circuit_id in args.circuits:
        old_path = OLD_REFERENCE.get(circuit_id)
        old_class = load_old_class(old_path) if old_path and old_path.exists() else "?"
        result = redecode_one(circuit_id)
        new_class = result.get("dna_topology_class")
        rows.append({
            "circuit_id": circuit_id,
            "old_class": old_class,
            "new_class": new_class,
            "bio_class": result.get("glmp_biological_class"),
            "reason": reason_from_result(result),
            "output_file": sorted(RESULTS_DIR.glob(f"{circuit_id}_logic_*.json"))[-1].name,
            "pending_custom_pwms": None,
        })

    ara_manifest = QUEUE / "completed" / "ecoli_ara_operon.yaml"
    with open(ara_manifest, encoding="utf-8") as f:
        ara_pending = yaml.safe_load(f).get("pending_custom_pwms", [])
    for row in rows:
        if row["circuit_id"] == "ecoli_ara_operon":
            row["pending_custom_pwms"] = ara_pending

    print("circuit_id|old_class|new_class|bio_class|reason|output_file")
    for row in rows:
        print(
            f"{row['circuit_id']}|{row['old_class']}|{row['new_class']}|"
            f"{row['bio_class']}|{row['reason']}|{row['output_file']}"
        )

    summary_path = RESULTS_DIR / f"regression_redecode_{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"rows": rows, "ara_pending_custom_pwms": ara_pending}, f, indent=2)
    print(f"\nWrote summary: {summary_path}")
    print(f"ara pending_custom_pwms: {json.dumps(ara_pending)}")


if __name__ == "__main__":
    main()
