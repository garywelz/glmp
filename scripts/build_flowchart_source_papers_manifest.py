#!/usr/bin/env python3
"""
Build flowchart-source-papers.tsv — canonical source paper per GLMP flowchart.

Drives CopernicusAI curated DOI ingestion and the planned Firestore glmp_relevant
backfill (see collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md).

Reads: glmp-v2/processes/**/*.json
Optional: collaborations/krampis-virtual-cell/flowchart-circuit-classes.tsv

Output: collaborations/krampis-virtual-cell/flowchart-source-papers.tsv
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC_DIR = ROOT / "glmp-v2" / "processes"
OUT = ROOT / "collaborations" / "krampis-virtual-cell" / "flowchart-source-papers.tsv"
CLASS_TSV = ROOT / "collaborations" / "krampis-virtual-cell" / "flowchart-circuit-classes.tsv"


def normalize_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = doi.strip().lower()
    d = re.sub(r"^(doi:|https?://(dx\.)?doi\.org/)", "", d).strip()
    return d


def firestore_doc_id(pmid: str | None, arxiv_id: str | None, fallback_id: str = "") -> str:
    if pmid:
        return f"pubmed_{str(pmid).strip()}"
    if arxiv_id:
        return f"arxiv_{str(arxiv_id).replace('/', '_')}"
    return fallback_id


def load_class_map() -> dict[str, dict[str, str]]:
    if not CLASS_TSV.exists():
        return {}
    rows = {}
    lines = CLASS_TSV.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("\t")
        row = dict(zip(header, parts))
        rows[row["process_id"]] = row
    return rows


def pick_canonical_source(sources: list) -> dict | None:
    if not sources:
        return None
    # Prefer entries with DOI; among those, prefer earlier (usually primary).
    with_doi = [s for s in sources if normalize_doi(s.get("doi"))]
    pool = with_doi or sources
    return pool[0]


def main():
    class_map = load_class_map()
    rows = []
    missing = 0

    for path in sorted(PROC_DIR.rglob("*.json")):
        proc = json.loads(path.read_text(encoding="utf-8"))
        pid = proc.get("id", path.stem)
        src = pick_canonical_source(proc.get("sources") or [])
        doi = normalize_doi(src.get("doi") if src else None)
        pmid = str(src.get("pmid", "") or "").strip() if src else ""
        title = (src.get("title") or "").replace("\t", " ").strip() if src else ""
        year = str(src.get("year", "") or "") if src else ""
        doc_id = firestore_doc_id(pmid or None, src.get("arxiv_id") if src else None)
        cls_row = class_map.get(pid, {})
        circuit_class = proc.get("circuitClass") or cls_row.get("circuit_class", "")
        ground_truth = "yes" if proc.get("groundTruth") else "no"
        if not doi and not pmid:
            missing += 1
            status = "needs_doi"
        else:
            status = "ok"
        rows.append({
            "process_id": pid,
            "name": proc.get("name", "").replace("\t", " "),
            "organism": proc.get("organism", ""),
            "category": proc.get("category", ""),
            "circuit_class": circuit_class,
            "ground_truth": ground_truth,
            "canonical_doi": doi,
            "canonical_pmid": pmid,
            "canonical_title": title,
            "canonical_year": year,
            "expected_firestore_id": doc_id,
            "source_count": len(proc.get("sources") or []),
            "manifest_status": status,
            "needs_krampis_review": "yes" if status == "needs_doi" else "no",
        })

    header = list(rows[0].keys()) if rows else []
    lines = ["\t".join(header)]
    for r in rows:
        lines.append("\t".join(str(r[k]) for k in header))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    ok = sum(1 for r in rows if r["manifest_status"] == "ok")
    print(f"Wrote {len(rows)} rows -> {OUT}")
    print(f"  With DOI or PMID: {ok}")
    print(f"  Needs DOI/PMID:   {missing}")


if __name__ == "__main__":
    main()
