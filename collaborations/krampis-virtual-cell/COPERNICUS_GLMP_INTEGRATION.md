# CopernicusAI ↔ GLMP Integration

**Track #4** — literature corpus linking, source-paper manifest, and `glmp_relevant` tagging pipeline.  
**Branch:** `cursor/copernicus-glmp-integration-c7ff`  
**Status:** 2026-06-13 — manifest + gap analysis + classifier preview complete; Firestore backfill pending GCP.

---

## Architecture

```mermaid
flowchart LR
  GLMP[GLMP process JSON\n217 flowcharts] --> MANIFEST[flowchart-source-papers.tsv]
  MANIFEST --> GAP[corpus gap report]
  MANIFEST --> INGEST[curated-doi-ingest-priority.txt]
  COPERNICUS[CopernicusAI papers\n~47K local JSON] --> GAP
  COPERNICUS --> PREVIEW[glmp-relevant-corpus-preview.tsv]
  MANIFEST --> PREVIEW
  GAP --> LINK[link_glmp_processes_to_papers.py]
  LINK --> GLMP
  PREVIEW --> FIRESTORE[Firestore backfill\n(glmp_relevant, sequence_logic_content)]
  INGEST --> FIRESTORE
```

**Repos**

| Repo | Role |
|---|---|
| [garywelz/glmp](https://github.com/garywelz/glmp) | Flowcharts, manifest, annotation schema, integration scripts |
| [garywelz/copernicus-web](https://github.com/garywelz/copernicus-web) | Firestore `research_papers`, `glmp_processes`, ingest/backfill |
| [garywelz/copernicusai-research-metadata](https://github.com/garywelz/copernicusai-research-metadata) | Stub README only — real stack is `copernicus-web` |

---

## What this PR delivers

### 1. Flowchart source paper manifest

`collaborations/krampis-virtual-cell/flowchart-source-papers.tsv` — one row per GLMP process (217), with canonical DOI/PMID, expected Firestore doc id, circuit class, and review flags.

| Metric | Count |
|---|---|
| Total processes | 217 |
| With DOI or PMID | 208 |
| Needs DOI/PMID (Krampis review) | 9 |

**Needs review** (no canonical DOI in sources): `bacillus_germination`, `ecoli_aerobic_respiration`, `ecoli_peptidoglycan_biosynthesis`, `yeast_aerobic_respiration`, `yeast_alcoholic_fermentation`, `yeast_cell_cycle_checkpoints`, `yeast_dna_replication`, `yeast_nucleotide_excision_repair`, `yeast_ribosome_biogenesis`.

### 2. Corpus gap analysis

`copernicus-corpus-gap-report.tsv` + `copernicus-corpus-gap-summary.md`

Against the local Copernicus acquisition JSON (~37,643 papers with DOI):

| Coverage | Count |
|---|---|
| Source paper in local corpus | **1** (`yeast_mitochondrial_import`) |
| Missing — need curated ingest | **216** |
| Unique DOIs to ingest | **192** |

The Zenodo frozen export (`research_papers_20260526.jsonl.gz`) returned 404 at publish time; gap analysis used local JSON only.

**Curated ingest list:** `curated-doi-ingest-priority.tsv` / `.txt` — de-duplicated DOIs for Copernicus `curated DOI ingestion mode` (see collaboration plan).

### 3. `glmp_relevant` classifier preview (dry-run)

`glmp-relevant-corpus-preview.tsv` — rules from `glmp-collaboration-plan-2026.md`, no Firestore writes.

| Flag | Papers (local 47,328) |
|---|---|
| `glmp_relevant=true` | 24,155 |
| `sequence_logic_content=true` | 90 |

### 4. Sequence annotation schema v0.2

`sequence-annotation-schema.json` — field definitions for `sequenceAnnotation` blocks and `copernicusIntegration` process-level linking. Extends v0.1 blocks already on ground-truth charts.

### 5. Process JSON linking

All 217 process JSON files now include a `copernicusIntegration` object (canonical DOI, expected Firestore id, corpus coverage status). Re-run:

```bash
python3 scripts/build_flowchart_source_papers_manifest.py
python3 scripts/check_manifest_corpus_coverage.py
python3 scripts/link_glmp_processes_to_papers.py --apply
```

---

## Scripts (GLMP repo)

| Script | Output |
|---|---|
| `scripts/build_flowchart_source_papers_manifest.py` | `flowchart-source-papers.tsv` |
| `scripts/check_manifest_corpus_coverage.py` | `copernicus-corpus-gap-report.tsv`, gap summary |
| `scripts/classify_glmp_relevant_preview.py` | `glmp-relevant-corpus-preview.tsv` |
| `scripts/export_curated_doi_ingest_list.py` | `curated-doi-ingest-priority.tsv/.txt` |
| `scripts/link_glmp_processes_to_papers.py` | Updates `copernicusIntegration` in process JSON |

**Prerequisites for gap/classifier scripts:** clone `copernicus-web` locally:

```bash
git clone https://github.com/garywelz/copernicus-web.git
# papers under huggingface-space/metadata-database/papers/
```

---

## Next steps (requires GCP / copernicus-web)

These steps run in `copernicus-web`, not in this PR:

1. **Curated DOI ingest** — feed `curated-doi-ingest-priority.txt` into the Copernicus ingest pipeline; tag `glmp_relevant: true` on ingest.
2. **Firestore backfill** — apply classifier rules to existing `research_papers` (~59K in production); set `glmp_relevant` and `sequence_logic_content` booleans.
3. **Re-sync `glmp_processes`** — push updated 217 processes from GCS; use `process_sync_common.py` + canonical metadata IDs (deprecate path-derived IDs in `sync_glmp_processes.py`).
4. **Embedding backfill** — `backfill_embeddings.py --submit --collection glmp_processes` after process sync.

**GCP project:** `regal-scholar-453620-r7`  
**Deploy from Yoga 9i:** PowerShell with `gcloud.cmd` / `gsutil.cmd` (see Batch 9 deploy scripts).

---

## Krampis joint tasks

From `glmp-collaboration-plan-2026.md`:

- Validate and extend `flowchart-source-papers.tsv` — especially hematopoietic / virtual-cell circuits and the 9 `needs_doi` rows.
- Review `sequence-annotation-schema.json` v0.2 for human Class IIIa fields (genomic coordinates, spacing, confidence).
- After curated ingest, confirm manifest DOIs resolve in Copernicus browse/search.

---

## Related PRs

- **Batch 9 circuits (217 total):** [PR #14](https://github.com/garywelz/glmp/pull/14) on `cursor/batch-9-ground-truth-c7ff` — merge before or with this integration branch.

---

*Gary Welz · GLMP · gwelz@gc.cuny.edu*
