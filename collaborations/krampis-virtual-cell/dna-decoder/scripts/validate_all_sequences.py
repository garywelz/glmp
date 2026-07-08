#!/usr/bin/env python3
"""Validate all completed-circuit FASTAs against manifests (Phase B1 Step 5)."""

import argparse
import json
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DECODER_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from run_batch import resolve_path  # noqa: E402
from sequence_guard import validate_sequence_against_manifest  # noqa: E402

QUEUE_COMPLETED = DECODER_DIR / "queue" / "completed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate decode FASTAs vs manifests")
    parser.add_argument(
        "--skip-ncbi",
        action="store_true",
        help="Header/sha256 only (no live NCBI fetch)",
    )
    args = parser.parse_args()

    manifests = sorted(QUEUE_COMPLETED.glob("*.yaml"))
    if not manifests:
        print(f"No manifests in {QUEUE_COMPLETED}", file=sys.stderr)
        return 1

    results = []
    failures = []

    for mf_path in manifests:
        manifest = yaml.safe_load(mf_path.read_text(encoding="utf-8"))
        cid = manifest.get("circuit_id", mf_path.stem)
        seq_path = resolve_path(manifest["sequence_file"])
        try:
            meta = validate_sequence_against_manifest(
                manifest, seq_path, skip_ncbi=args.skip_ncbi
            )
            results.append(meta)
            print(f"PASS  {cid}  len={meta['length']}  sha256={meta['sha256'][:12]}…")
        except RuntimeError as exc:
            failures.append({"circuit_id": cid, "error": str(exc)})
            print(f"FAIL  {cid}\n  {exc}", file=sys.stderr)

    summary = {
        "total": len(manifests),
        "passed": len(results),
        "failed": len(failures),
        "results": results,
        "failures": failures,
    }
    out = DECODER_DIR / "results" / "sequence_guard_validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S) — guard would block batch decode", file=sys.stderr)
        return 1
    print(f"\nAll {len(results)} circuits PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
