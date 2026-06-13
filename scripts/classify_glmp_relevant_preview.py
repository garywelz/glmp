#!/usr/bin/env python3
"""
Dry-run glmp_relevant + sequence_logic_content classifier for CopernicusAI papers.

Implements the rules from glmp-collaboration-plan-2026.md on local JSON corpora
(no Firestore writes). Produces a preview TSV for Welz/Krampis review before GCP backfill.

Input (first found):
  - /home/ubuntu/copernicus-web/huggingface-space/metadata-database/papers/**/*.json
  - data/research_papers_20260526.jsonl.gz (Zenodo export)

Output:
  collaborations/krampis-virtual-cell/glmp-relevant-corpus-preview.tsv
"""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collaborations" / "krampis-virtual-cell" / "flowchart-source-papers.tsv"
OUT = ROOT / "collaborations" / "krampis-virtual-cell" / "glmp-relevant-corpus-preview.tsv"
LOCAL_PAPERS = Path("/home/ubuntu/copernicus-web/huggingface-space/metadata-database/papers")
ZENODO_GZ = ROOT / "data" / "research_papers_20260526.jsonl.gz"

BIOLOGY_CATEGORIES = {
    "gene regulation", "transcription", "chromatin", "epigenetics", "systems biology",
    "synthetic biology", "regulatory genomics", "computational biology", "perturbation",
    "single-cell", "rna", "protein binding", "promoter", "enhancer", "operon",
    "signal transduction", "metabolism", "developmental biology", "immunology",
}
CS_CATEGORIES = {"computational biology", "bioinformatics", "sequence models", "machine learning genomics"}
SEQUENCE_LOGIC_KW = re.compile(
    r"\b(mpra|massively parallel reporter|promoter library|synthetic promoter|"
    r"cis-regulatory|enhancer assay|regulon|operon|binding site|motif discovery|"
    r"position weight matrix|pwm|jaspar|hocomoco|logic gate|boolean network|"
    r"repressilator|toggle switch|feed-?forward loop)\b",
    re.I,
)


def normalize_doi(doi: str) -> str:
    d = (doi or "").strip().lower()
    d = re.sub(r"^(doi:|https?://(dx\.)?doi\.org/)", "", d).strip()
    return d


def load_manifest_dois() -> set[str]:
    if not MANIFEST.exists():
        return set()
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()[1:]
    dois = set()
    for ln in lines:
        parts = ln.split("\t")
        if len(parts) < 7:
            continue
        # canonical_doi column index from header
        header = MANIFEST.read_text(encoding="utf-8").splitlines()[0].split("\t")
        idx = header.index("canonical_doi")
        d = normalize_doi(parts[idx])
        if d:
            dois.add(d)
    return dois


def classify(paper: dict, manifest_dois: set[str]) -> tuple[bool, bool, str]:
    discipline = (paper.get("discipline") or paper.get("category") or "").lower()
    cats = paper.get("categories") or paper.get("subcategories") or []
    if isinstance(cats, str):
        cats = [cats]
    cats_l = {str(c).lower() for c in cats}
    doi = normalize_doi(paper.get("doi"))
    text = f"{paper.get('title','')} {paper.get('abstract','')}"

    glmp = False
    reason = []

    if doi and doi in manifest_dois:
        glmp = True
        reason.append("manifest_doi")
    if discipline == "biology" and (cats_l & BIOLOGY_CATEGORIES):
        glmp = True
        reason.append("biology_category")
    if discipline == "computer science" and (cats_l & CS_CATEGORIES):
        glmp = True
        reason.append("cs_bio_category")
    if discipline == "biology" and not cats_l and discipline == "biology":
        glmp = True
        reason.append("biology_discipline")

    seq_logic = bool(SEQUENCE_LOGIC_KW.search(text))
    return glmp, seq_logic, ";".join(reason) if reason else "none"


def iter_papers():
    manifest_dois = load_manifest_dois()
    if LOCAL_PAPERS.exists():
        for path in LOCAL_PAPERS.rglob("*.json"):
            try:
                p = json.loads(path.read_text(encoding="utf-8"))
                p["_source_path"] = str(path)
                yield p, manifest_dois
            except Exception:
                pass
        return
    if ZENODO_GZ.exists():
        with gzip.open(ZENODO_GZ, "rt", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line), manifest_dois


def main():
    rows = []
    n_glmp = n_seq = 0
    for paper, manifest_dois in iter_papers():
        glmp, seq_logic, reason = classify(paper, manifest_dois)
        if glmp:
            n_glmp += 1
        if seq_logic:
            n_seq += 1
        rows.append({
            "doc_id": paper.get("id") or paper.get("doc_id", ""),
            "doi": normalize_doi(paper.get("doi")),
            "pmid": paper.get("pmid", ""),
            "discipline": paper.get("discipline") or paper.get("category", ""),
            "glmp_relevant": "true" if glmp else "false",
            "sequence_logic_content": "true" if seq_logic else "false",
            "classify_reason": reason,
            "title": (paper.get("title") or "")[:120].replace("\t", " "),
        })

    if not rows:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text("doc_id\tdoi\tpmid\tdiscipline\tglmp_relevant\tsequence_logic_content\tclassify_reason\ttitle\n", encoding="utf-8")
        print("No local papers found; wrote empty preview. Clone copernicus-web or download Zenodo export.")
        return

    header = list(rows[0].keys())
    OUT.write_text("\n".join(["\t".join(header)] + [
        "\t".join(str(r[k]) for k in header) for r in rows
    ]) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows -> {OUT}")
    print(f"  glmp_relevant=true: {n_glmp}")
    print(f"  sequence_logic_content=true: {n_seq}")


if __name__ == "__main__":
    main()
