# Cursor Briefing: GLMP Decoder Automation + CopernicusAI Scout Expansion
**Project:** GLMP DNA Decoder + CopernicusAI Scout Pipeline  
**Date:** June 24, 2026  
**Prepared by:** Claude (handoff to Cursor for implementation)

---

## Context

This is an active research project running on a Jetson Nano edge compute node. There are two pipelines to extend:

1. **DNA Decoder** — decodes gene regulatory circuits from sequence data using FIMO motif scanning + a custom GLMP logic parser. Currently working on 3 E. coli circuits (lac, ara, trp). Goal: automate via manifest-driven batch runner and extend to eukaryotes (yeast GAL system first).

2. **CopernicusAI Scout** — daily PubMed/BioRxiv/arXiv paper ingestion into Firestore. Currently one cron job at 10:15 AM. Goal: split into 3 independent workers, add an evening run, expand query terms.

Both pipelines write to Firestore. A new `scheduler_status` collection will track job heartbeats for observability.

---

## Infrastructure

| Resource | Detail |
|---|---|
| Edge node | Jetson Nano (Seeed Studio reComputer J1010) |
| SSH | `gary@192.168.1.222` |
| SD card mount | `/media/sdcard/` |
| Scout repo | `/media/sdcard/copernicus-worker/copernicus-web/` (symlinked from `/home/gdubs/copernicus-web-public`) |
| Decoder | `/media/sdcard/decoder/` |
| FIMO/MEME | `/media/sdcard/miniforge3/` (meme-env, v5.5.9) |
| JASPAR 2024 CORE | `/media/sdcard/decoder/motifs/` (2346 motifs) |
| Parser | `collaborations/krampis-virtual-cell/dna-decoder/glmp_logic_parser.py` (v0.2.0) |
| GCP project | `regal-scholar-453620-r7` |
| Firestore credentials | `/home/gary/.config/copernicus/gcp-sa.json` |
| Embeddings | OpenAI `text-embedding-3-small` (1536d), nDCG@10 = 0.828 |
| Firestore index | ~59,700 documents (papers collection) |
| Python env | Python 3.8 venv on SD card |

---

## Step 0: READ BEFORE TOUCHING ANYTHING

**Before writing any code**, read these files in order:

```bash
# 1. Find and read the active scout script (the one cron actually calls)
crontab -l
# Then read whatever script the 10:15 AM job points to

# 2. Read the decoder parser
cat collaborations/krampis-virtual-cell/dna-decoder/glmp_logic_parser.py

# 3. Confirm Firestore credentials work
GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json \
python -c "from google.cloud import firestore; db = firestore.Client(); print('OK')"
```

The scout may be a monolith or already modular — do not assume. The refactor scope depends entirely on what you find.

---

## Implementation Plan (execute in this order)

### Step 1 — Firestore: New Collections

Create two new Firestore collections by writing a setup script. Do not use the Cloud Console UI.

**Collection: `glmp_circuits`** — one document per decoded circuit:

```json
{
  "circuit_id": "yeast_gal_system",
  "organism": "Saccharomyces cerevisiae",
  "taxon_id": 4932,
  "glmp_class": "III",
  "decoded_at": "2026-06-24T02:15:00Z",
  "mermaid_flowchart": "graph TD\n  GAL4 -->|activates| GAL1\n...",
  "binding_sites": [
    {"tf": "GAL4", "gene": "GAL1", "start": 423, "end": 441, "qvalue": 0.001}
  ],
  "source_papers": [
    {"doi": "10.1093/nar/...", "title": "...", "firestore_id": "abc123"}
  ],
  "source_sequences": [
    {
      "gene": "GAL1",
      "accession": "SGD:S000000224",
      "fasta_path": "/media/sdcard/decoder/sequences/GAL1.fa"
    }
  ],
  "parser_version": "0.2.0",
  "fimo_version": "5.5.9",
  "jaspar_version": "2024_CORE",
  "notes": ""
}
```

**Collection: `scheduler_status`** — one document per job, updated each run:

```json
{
  "job_id": "scout_pubmed_am",
  "last_run_start": "2026-06-24T10:15:00Z",
  "last_run_end": "2026-06-24T10:18:43Z",
  "last_status": "success",
  "last_doc_count": 47,
  "consecutive_failures": 0,
  "total_runs": 312,
  "next_scheduled": "2026-06-25T10:15:00Z"
}
```

---

### Step 2 — `status_writer.py` (lowest risk, standalone)

Create `/media/sdcard/scheduler/status_writer.py`:

- Accepts: `job_id`, `status` ("success"/"failure"), `doc_count`, `start_time`, `end_time`
- Writes/upserts a document to `scheduler_status` collection in Firestore
- Uses credentials at `/home/gary/.config/copernicus/gcp-sa.json`
- Increments `total_runs` and `consecutive_failures` (reset to 0 on success)
- Standalone — importable by any job script

Test it independently before wiring into any scout job.

---

### Step 3 — Scout Refactor (read first, then split)

After reading the existing scout script:

**If it's a monolith:** split into three independent scripts:
- `scout_pubmed.py`
- `scout_biorxiv.py`  
- `scout_arxiv.py`

Each script:
- Accepts an argument: `am` or `pm` (for logging)
- Uses a **lock file** to prevent double-runs:
  ```python
  LOCK_FILE = f"/tmp/scout_{source}_{run_type}.lock"
  if os.path.exists(LOCK_FILE):
      log("previous run still active, skipping")
      sys.exit(0)
  open(LOCK_FILE, 'w').close()
  try:
      run_job()
  finally:
      os.remove(LOCK_FILE)
  ```
- Calls `status_writer.py` at start and end of each run
- Writes papers to existing Firestore `papers` collection (no schema changes)

**If it's already modular:** wire in `status_writer.py` and the lock file pattern only.

---

### Step 4 — Expanded Query Terms (Clusters 1–3 only)

Add these terms to the scout workers. Keep as a separate importable `query_terms.py` so Clusters 4–5 can be added later without touching the worker scripts.

```python
# query_terms.py
CLUSTER_1_GLMP = [
    "boolean gene regulatory networks",
    "typed computational models gene regulation",
    "Mermaid flowchart bioinformatics",
    "circuit topology gene expression",
    "formal grammar gene regulatory",
]

CLUSTER_2_DECODER = [
    "JASPAR transcription factor motifs",
    "PWM position weight matrix prokaryote",
    "FIMO motif enrichment promoter",
    "binding site prediction eukaryote",
    "regulatory sequence annotation",
]

CLUSTER_3_SYSTEMS_BIO = [
    "Biolink knowledge graph genomics",
    "KGX biological knowledge graph",
    "gene regulatory network inference",
    "RegVelo single cell regulatory",
    "systems biology Boolean model",
]

ALL_CLUSTERS_1_3 = CLUSTER_1_GLMP + CLUSTER_2_DECODER + CLUSTER_3_SYSTEMS_BIO
```

Each source worker imports `ALL_CLUSTERS_1_3` and appends to its existing query list.

---

### Step 5 — Updated Cron Schedule

Replace the existing single 10:15 AM cron with:

```bash
# Morning scout — staggered by source (5 min apart)
15 10 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_pubmed.py am >> /media/sdcard/logs/scout_pubmed_am.log 2>&1
20 10 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_biorxiv.py am >> /media/sdcard/logs/scout_biorxiv_am.log 2>&1
25 10 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_arxiv.py am >> /media/sdcard/logs/scout_arxiv_am.log 2>&1

# Evening scout — same sources, catches late preprints
0 20 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_pubmed.py pm >> /media/sdcard/logs/scout_pubmed_pm.log 2>&1
5 20 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_biorxiv.py pm >> /media/sdcard/logs/scout_biorxiv_pm.log 2>&1
10 20 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/copernicus-worker/copernicus-web/huggingface-space/scout_arxiv.py pm >> /media/sdcard/logs/scout_arxiv_pm.log 2>&1

# Nightly decoder batch — CPU-bound, runs unattended
0 2 * * * nice -n 10 /path/to/venv/bin/python /media/sdcard/decoder/run_batch.py >> /media/sdcard/logs/decoder.log 2>&1
```

**Note:** Confirm the venv path from the existing cron before editing. Do not break the working 10:15 AM job — add new jobs first, test, then remove the old one.

---

### Step 6 — `firestore_writer.py` for Decoder

Create `/media/sdcard/decoder/firestore_writer.py`:

- Reads a decoded circuit result (from parser output + manifest)
- Writes a document to `glmp_circuits` collection
- Looks up related papers in the `papers` collection by DOI or title match and links them in `source_papers`
- Uses credentials at `/home/gary/.config/copernicus/gcp-sa.json`
- Idempotent: upsert by `circuit_id`, do not duplicate

---

### Step 7 — `run_batch.py` Decoder Batch Runner

Create `/media/sdcard/decoder/run_batch.py`:

```
for each YAML manifest in /media/sdcard/decoder/manifests/:
    1. Check if sequence files exist; fetch from NCBI/SGD if not (cache to sequences/)
    2. Run FIMO scoped to promoter window (±1kb from TSS, not whole chromosome)
    3. Run glmp_logic_parser.py on FIMO output
    4. Write Mermaid + JSON to parser_out/
    5. Call firestore_writer.py to push to glmp_circuits collection
    6. Update corpus_registry.json
    7. Call status_writer.py with result
```

Use lock file pattern. Log all steps. Skip circuits whose `circuit_id` already exists in Firestore (unless `--force` flag passed).

---

### Step 8 — YAML Manifests for Existing Circuits

Retrofit the 3 working circuits as manifests in `/media/sdcard/decoder/manifests/`. Use this schema:

```yaml
circuit_id: ecoli_lac_operon
organism: Escherichia coli
taxon_id: 511145
glmp_class: II
genes:
  - id: lacZ
    accession: NC_000913.3
    promoter_window_bp: 1000
transcription_factors:
  - name: LacI
    role: repressor
    pwm_source: custom
  - name: CRP
    role: activator
    jaspar_id: null
signals:
  - name: allolactose
    effect: relieve_repression
  - name: cAMP
    effect: activate
parser_flags:
  eukaryotic: false
  repressor_qvalue_threshold: 0.05
source_papers:
  - doi: "10.1038/..."
    title: "..."
notes: "Class II dual-control circuit, canonical lac operon"
```

Create one file each for: `ecoli_lac_operon.yaml`, `ecoli_ara_operon.yaml`, `ecoli_trp_operon.yaml`.

---

### Step 9 — GAL System Manifest + Test Decode

Create `yeast_gal_system.yaml`:

```yaml
circuit_id: yeast_gal_system
organism: Saccharomyces cerevisiae
taxon_id: 4932
glmp_class: III
genes:
  - id: GAL1
    accession: SGD:S000000224
    promoter_window_bp: 1000
  - id: GAL4
    accession: SGD:S000006100
    promoter_window_bp: 1000
transcription_factors:
  - name: GAL4
    jaspar_id: MA0803.1      # verify this exists in JASPAR 2024
    role: activator
  - name: GAL80
    role: repressor
    pwm_source: custom       # check JASPAR first; use custom if absent
signals:
  - name: galactose
    effect: relieve_repression
  - name: glucose
    effect: repress
parser_flags:
  eukaryotic: true
  repressor_qvalue_threshold: 0.05
notes: "First eukaryotic circuit in GLMP corpus. Class III feed-forward with repressor titration."
```

**Before running:** verify `MA0803.1` (GAL4) exists in the local JASPAR 2024 CORE motif database. If absent, the custom PWM path needs to be used — check the parser's `--repressor-qvalue-threshold` flag handling for eukaryotic mode.

Run decode manually first (not via batch runner) and inspect output before wiring into automation.

---

## File Structure After Implementation

```
/media/sdcard/
├── decoder/
│   ├── manifests/
│   │   ├── ecoli_lac_operon.yaml
│   │   ├── ecoli_ara_operon.yaml
│   │   ├── ecoli_trp_operon.yaml
│   │   └── yeast_gal_system.yaml
│   ├── sequences/              (cached FASTA files)
│   ├── motifs/                 (existing JASPAR + custom PWMs)
│   ├── fimo_out/               (FIMO results per circuit)
│   ├── parser_out/             (Mermaid + GLMP class JSON)
│   ├── run_batch.py            (NEW)
│   ├── firestore_writer.py     (NEW)
│   └── corpus_registry.json   (NEW — index of all decoded circuits)
│
├── copernicus-worker/copernicus-web/huggingface-space/
│   ├── scout_pubmed.py         (refactored or new)
│   ├── scout_biorxiv.py        (refactored or new)
│   ├── scout_arxiv.py          (refactored or new)
│   └── query_terms.py          (NEW — Clusters 1-3)
│
├── scheduler/
│   └── status_writer.py        (NEW)
│
└── logs/
    ├── scout_pubmed_am.log
    ├── scout_biorxiv_am.log
    ├── scout_arxiv_am.log
    ├── scout_pubmed_pm.log
    ├── scout_biorxiv_pm.log
    ├── scout_arxiv_pm.log
    └── decoder.log
```

---

## Firestore Collections Summary

| Collection | Status | Purpose |
|---|---|---|
| `papers` | Existing (~59,700 docs) | Scout ingestion target — no schema changes |
| `glmp_circuits` | New | Decoded circuit documents |
| `scheduler_status` | New | Job heartbeats for all cron workers |

---

## Constraints and Cautions

- **Do not break the working 10:15 AM scout job.** Add new cron entries first, test, remove old entry last.
- **Jetson RAM is ~4GB shared CPU/GPU.** Do not run decoder batch and scout simultaneously. The nightly 2 AM slot is safe.
- **FIMO scope to promoter windows** (±1kb from TSS), not whole chromosomes. Whole-chromosome scans will be slow on the Nano.
- **Embedding provider is fixed** at OpenAI `text-embedding-3-small` (1536d). Do not change — would invalidate the existing Firestore index.
- **Python 3.8 venv** on SD card. Confirm venv path from existing crontab before running any Python.
- **Credentials:** always use `/home/gary/.config/copernicus/gcp-sa.json`. Set via `GOOGLE_APPLICATION_CREDENTIALS` env var or pass path explicitly.
- **Lock files** in `/tmp/` — they clear on reboot. This is intentional.

---

## What This Does NOT Include (deferred)

- HF Space dashboard (garywelz/glmp is out of date; full update deferred)
- Scout query term Clusters 4–5 (add later once Clusters 1–3 are confirmed working)
- B. subtilis or P. aeruginosa circuits (after GAL system validated)
- TDA integration (separate thread, not part of GLMP)
