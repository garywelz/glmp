#!/usr/bin/env python3
"""
Add CopernicusAI integration fields to GLMP process JSON from the source-paper manifest.

Reads:
  collaborations/krampis-virtual-cell/flowchart-source-papers.tsv
  collaborations/krampis-virtual-cell/copernicus-corpus-gap-report.tsv (optional)

Writes (with --apply):
  glmp-v2/processes/**/*.json  — adds/updates top-level `copernicusIntegration` object

Dry-run (default): prints how many files would change.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC_DIR = ROOT / "glmp-v2" / "processes"
MANIFEST = ROOT / "collaborations" / "krampis-virtual-cell" / "flowchart-source-papers.tsv"
GAP = ROOT / "collaborations" / "krampis-virtual-cell" / "copernicus-corpus-gap-report.tsv"


def load_tsv(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write changes to process JSON files")
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit("Run build_flowchart_source_papers_manifest.py first")

    manifest = {r["process_id"]: r for r in load_tsv(MANIFEST)}
    gap = {}
    if GAP.exists():
        gap = {r["process_id"]: r for r in load_tsv(GAP)}

    changed = 0
    for path in sorted(PROC_DIR.rglob("*.json")):
        proc = json.loads(path.read_text(encoding="utf-8"))
        pid = proc.get("id", path.stem)
        row = manifest.get(pid)
        if not row:
            continue
        g = gap.get(pid, {})
        integration = {
            "canonicalSourceDoi": row.get("canonical_doi", ""),
            "canonicalSourcePmid": row.get("canonical_pmid", ""),
            "canonicalSourceTitle": row.get("canonical_title", ""),
            "expectedFirestoreId": row.get("expected_firestore_id", ""),
            "copernicusPaperId": g.get("expected_firestore_id", row.get("expected_firestore_id", ""))
            if g.get("coverage_status") == "in_corpus"
            else "",
            "manifestStatus": row.get("manifest_status", ""),
            "corpusCoverage": g.get("coverage_status", "unknown"),
            "needsKrampisReview": row.get("needs_krampis_review", "no") == "yes",
        }
        if proc.get("copernicusIntegration") == integration:
            continue
        changed += 1
        if args.apply:
            proc["copernicusIntegration"] = integration
            path.write_text(json.dumps(proc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    verb = "Updated" if args.apply else "Would update"
    print(f"{verb} {changed} process JSON files")
    if not args.apply and changed:
        print("Re-run with --apply to write copernicusIntegration blocks.")


if __name__ == "__main__":
    main()
