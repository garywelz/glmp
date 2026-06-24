#!/usr/bin/env python3.8
"""
Supplemental PubMed acquisition for GLMP query term clusters 1–3.

Runs from huggingface-space cwd; imports acquire_pubmed_batch helpers in-process.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

SCOUT_DIR = Path(__file__).resolve().parent
if str(SCOUT_DIR) not in sys.path:
    sys.path.insert(0, str(SCOUT_DIR))

from query_terms import ALL_CLUSTERS_1_3, GLMP_PUBMED_MAX_RESULTS_PER_TERM  # noqa: E402

ACQUIRE_DIR = Path("scripts/acquire_papers")
if not (ACQUIRE_DIR / "acquire_pubmed_batch.py").exists():
    print(f"ERROR: run from huggingface-space root; missing {ACQUIRE_DIR}", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(ACQUIRE_DIR.resolve()))

import acquire_pubmed_batch as pubmed  # noqa: E402


def main() -> int:
    pubmed.setup_entrez()
    output_dir = pubmed.OUTPUT_DIR / "glmp_scout"
    output_dir.mkdir(parents=True, exist_ok=True)

    all_papers = []
    mindate = "2024/01/01"
    maxdate = datetime.now().strftime("%Y/%m/%d")

    print(f"GLMP PubMed supplement: {len(ALL_CLUSTERS_1_3)} terms")

    for term in ALL_CLUSTERS_1_3:
        query = f'({term}) AND ("2024"[PDAT] : "3000"[PDAT])'
        print(f"\nTerm: {term}")
        pmids = pubmed.search_pubmed(
            query,
            GLMP_PUBMED_MAX_RESULTS_PER_TERM,
            mindate=mindate,
            maxdate=maxdate,
        )
        if not pmids:
            continue
        papers = pubmed.fetch_pubmed_details(pmids)
        all_papers.extend(papers)
        print(f"  fetched {len(papers)} papers")

    if all_papers:
        pubmed.save_papers(all_papers, output_dir, batch_num=int(datetime.now().strftime("%m%d%H")))

    print(f"\nTotal GLMP supplement papers: {len(all_papers)}")
    print(f"Saved under: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
