#!/usr/bin/env python3
"""
Check which flowchart-source-papers manifest DOIs appear in CopernicusAI corpora.

Sources checked (first available):
  1. Local acquisition JSON under copernicus-web/huggingface-space/metadata-database/papers/
  2. Optional Zenodo frozen export (research_papers_20260526.jsonl.gz)

Output:
  collaborations/krampis-virtual-cell/copernicus-corpus-gap-report.tsv
  collaborations/krampis-virtual-cell/copernicus-corpus-gap-summary.md
"""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collaborations" / "krampis-virtual-cell" / "flowchart-source-papers.tsv"
OUT_TSV = ROOT / "collaborations" / "krampis-virtual-cell" / "copernicus-corpus-gap-report.tsv"
OUT_MD = ROOT / "collaborations" / "krampis-virtual-cell" / "copernicus-corpus-gap-summary.md"

LOCAL_PAPERS = Path("/home/ubuntu/copernicus-web/huggingface-space/metadata-database/papers")
ZENODO_GZ = ROOT / "data" / "research_papers_20260526.jsonl.gz"
ZENODO_URL = "https://zenodo.org/records/18463303/files/research_papers_20260526.jsonl.gz"


def normalize_doi(doi: str) -> str:
    d = (doi or "").strip().lower()
    d = re.sub(r"^(doi:|https?://(dx\.)?doi\.org/)", "", d).strip()
    return d


def load_manifest() -> list[dict]:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:] if ln.strip()]


def index_local_papers() -> tuple[set[str], set[str]]:
    dois, pmids = set(), set()
    if not LOCAL_PAPERS.exists():
        return dois, pmids
    for path in LOCAL_PAPERS.rglob("*.json"):
        try:
            p = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        d = normalize_doi(p.get("doi"))
        if d:
            dois.add(d)
        if p.get("pmid"):
            pmids.add(str(p["pmid"]).strip())
    return dois, pmids


def index_zenodo(path: Path) -> tuple[set[str], set[str]]:
    dois, pmids = set(), set()
    if not path.exists():
        return dois, pmids
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            p = json.loads(line)
            d = normalize_doi(p.get("doi"))
            if d:
                dois.add(d)
            if p.get("pmid"):
                pmids.add(str(p["pmid"]).strip())
    return dois, pmids


def maybe_download_zenodo(dest: Path) -> bool:
    if dest.exists():
        return True
    try:
        import urllib.request
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading Zenodo export (~large) -> {dest}")
        urllib.request.urlretrieve(ZENODO_URL, dest)
        return dest.exists()
    except Exception as e:
        print(f"Zenodo download skipped: {e}")
        return False


def main():
    if not MANIFEST.exists():
        raise SystemExit("Run build_flowchart_source_papers_manifest.py first")

    rows = load_manifest()
    local_dois, local_pmids = index_local_papers()
    zenodo_path = ZENODO_GZ
    if not zenodo_path.exists():
        maybe_download_zenodo(zenodo_path)
    zenodo_dois, zenodo_pmids = index_zenodo(zenodo_path)

    out_rows = []
    in_local = in_zenodo = missing_both = 0
    for r in rows:
        doi = normalize_doi(r.get("canonical_doi", ""))
        pmid = r.get("canonical_pmid", "").strip()
        hit_local = (doi and doi in local_dois) or (pmid and pmid in local_pmids)
        hit_zenodo = (doi and doi in zenodo_dois) or (pmid and pmid in zenodo_pmids)
        if hit_local:
            in_local += 1
        if hit_zenodo:
            in_zenodo += 1
        if not hit_local and not hit_zenodo:
            missing_both += 1
        status = "in_corpus" if (hit_local or hit_zenodo) else "missing_ingest"
        out_rows.append({**r, "in_local_json": "yes" if hit_local else "no",
                         "in_zenodo_export": "yes" if hit_zenodo else "no",
                         "coverage_status": status})

    header = list(out_rows[0].keys())
    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_TSV.write_text("\n".join(["\t".join(header)] + [
        "\t".join(str(x[k]) for k in header) for x in out_rows
    ]) + "\n", encoding="utf-8")

    missing_list = [r for r in out_rows if r["coverage_status"] == "missing_ingest"]
    md = [
        "# CopernicusAI corpus gap report (GLMP source papers)",
        "",
        f"- Manifest rows: **{len(rows)}**",
        f"- Found in local acquisition JSON: **{in_local}**",
        f"- Found in Zenodo frozen export: **{in_zenodo}**",
        f"- Missing from both (need curated ingest): **{missing_both}**",
        "",
        "## Priority gaps (missing ingest)",
        "",
    ]
    for r in missing_list[:40]:
        md.append(f"- `{r['process_id']}` — {r.get('canonical_title') or '(no title)'} — DOI: `{r.get('canonical_doi') or '—'}`")
    if len(missing_list) > 40:
        md.append(f"- … and {len(missing_list) - 40} more (see TSV)")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_TSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Missing ingest: {missing_both}/{len(rows)}")


if __name__ == "__main__":
    main()
