#!/usr/bin/env python3
"""
Export DOIs that need curated CopernicusAI ingestion for GLMP source papers.

Input: collaborations/krampis-virtual-cell/copernicus-corpus-gap-report.tsv
Output:
  collaborations/krampis-virtual-cell/curated-doi-ingest-priority.tsv
  collaborations/krampis-virtual-cell/curated-doi-ingest-priority.txt  (one DOI per line)
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = ROOT / "collaborations" / "krampis-virtual-cell" / "copernicus-corpus-gap-report.tsv"
OUT_TSV = ROOT / "collaborations" / "krampis-virtual-cell" / "curated-doi-ingest-priority.tsv"
OUT_TXT = ROOT / "collaborations" / "krampis-virtual-cell" / "curated-doi-ingest-priority.txt"


def main():
    if not GAP.exists():
        raise SystemExit("Run check_manifest_corpus_coverage.py first")

    lines = GAP.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    rows = [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]
    missing = [r for r in rows if r.get("coverage_status") == "missing_ingest" and r.get("canonical_doi")]
    # de-dupe by DOI, keep first process_id as example
    seen = set()
    unique = []
    for r in missing:
        doi = r["canonical_doi"].strip().lower()
        if doi in seen:
            continue
        seen.add(doi)
        unique.append(r)

    out_header = ["doi", "process_id", "canonical_title", "organism", "circuit_class", "ground_truth"]
    tsv_lines = ["\t".join(out_header)]
    txt_lines = []
    for r in unique:
        tsv_lines.append("\t".join(
            r.get(k, "") for k in out_header
        ))
        txt_lines.append(r["canonical_doi"])

    OUT_TSV.write_text("\n".join(tsv_lines) + "\n", encoding="utf-8")
    OUT_TXT.write_text("\n".join(txt_lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(unique)} unique DOIs -> {OUT_TSV}")
    print(f"Wrote plain list -> {OUT_TXT}")


if __name__ == "__main__":
    main()
