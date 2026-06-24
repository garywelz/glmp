# Jetson Ingest Worker & DNA Decoder — Handoff Report

**Date:** 2026-06-24  
**Jetson:** `gary@192.168.1.222` (Seeed reComputer J1010)  
**Yoga 9i:** `C:\Users\garyw` · repo `github.com/garywelz/glmp`  
**Prepared for:** Cursor (Yoga 9i) and Claude Code (SSH)

**Related docs:**
- [`jetson/JETSON_SETUP_HANDOFF.md`](jetson/JETSON_SETUP_HANDOFF.md) — initial ingest worker setup
- [`jetson/RECON_LIVE_2026-06-24.md`](jetson/RECON_LIVE_2026-06-24.md) — Phase 1 recon
- [`jetson/scout/README.md`](jetson/scout/README.md) — Phase 2 split scouts
- [`dna-decoder/dna-decoder-prototype-report-2026-06-24.md`](dna-decoder/dna-decoder-prototype-report-2026-06-24.md)
- [`dna-decoder/CURSOR_BRIEFING_DECODER_AUTOMATION.md`](dna-decoder/CURSOR_BRIEFING_DECODER_AUTOMATION.md)

---

## Executive summary

Three pipelines are live on the Jetson:

1. **CopernicusAI daily scout** — monolith cron at 10:15 AM ET still running; fetches PubMed/bioRxiv/arXiv → local JSON → Firestore `research_papers`
2. **DNA Decoder (Stages 1–3)** — FIMO + `glmp_logic_parser.py` v0.2.0; lac, ara, trp operons validated on SD card
3. **Scheduler / split scouts (Phase 1–2)** — Firestore `scheduler_status` + `glmp_circuits` bootstrapped; `scout_pubmed.py am` first live run succeeded (75 papers, ~40s)

**GitHub is source of truth.** Pull before editing on any machine.

---

## Important correction: `am` and `pm` are NOT topic labels

In `scout_pubmed.py am`, the argument **`am`** means **morning run slot** (for cron scheduling and `job_id` naming), **not** a subject area or PubMed topic.

| Argument | Meaning | Example `job_id` |
|----------|---------|------------------|
| `am` | Morning scout window (cron ~10:15 ET in proposed schedule) | `scout_pubmed_am` |
| `pm` | Evening scout window (cron ~20:00 ET in proposed schedule) | `scout_pubmed_pm` |

**Topic/query expansion** comes from:
- `daily_scout_config.json` (existing journal/category queries)
- `query_terms.py` clusters 1–3 (GLMP supplement, PubMed only, via `glmp_pubmed_supplement.py`)

There are no other “topic variants” like `am`/`pm` beyond morning vs evening scheduling.

---

## Part 1 — Infrastructure

### SD card migration (June 23–24)

eMMC was ~77% full. SD card reformatted **exFAT → ext4** (`jetson-data`) so git and large workloads can live on SD.

| Item | Path |
|------|------|
| SD mount | `/media/sdcard` (ext4, ~117 GB) |
| fstab | `/dev/mmcblk1p1 /media/sdcard ext4 defaults,nofail 0 2` |
| Copernicus repo | `/media/sdcard/copernicus-worker/copernicus-web` |
| Copernicus venv | `/media/sdcard/copernicus-worker/venv` (Python 3.8) |
| Legacy symlink | `/home/gdubs/copernicus-web-public` → SD card repo |
| GCP key | `~/.config/copernicus/gcp-sa.json` (chmod 600) |
| Env | `~/.config/copernicus/env` |
| Decoder | `/media/sdcard/decoder/` |
| Scheduler | `/media/sdcard/scheduler/` |
| Logs | `/media/sdcard/logs/` |

### Credentials

- Only production key: `~/.config/copernicus/gcp-sa.json`
- `$GOOGLE_APPLICATION_CREDENTIALS` empty in bare SSH — set via `source ~/.config/copernicus/env` or cron
- SD card / venv hits are library metadata only, not secrets

### Daily scout cron (still live — do not remove yet)

```cron
CRON_TZ=America/New_York
10 10 * * *  remind_paper_scout_coffee.sh
15 10 * * *  . ~/.config/copernicus/env && \
             GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json \
             .../run_daily_scout_with_ingest.sh >> cron.log 2>&1
```

Budget from `daily_scout_config.json`: ~1000 papers/run weighted → PubMed ~600, bioRxiv ~250, arXiv ~150.

### Venv fix

Broken repo `paper_acquisition_venv` (Python 3.12, no pip) recreated with Python 3.8 at:
`/media/sdcard/copernicus-worker/copernicus-web/huggingface-space/paper_acquisition_venv`

Split scouts prefer this venv’s `python3` when present.

`cloud-run-backend/venv` → symlink to `/media/sdcard/copernicus-worker/venv`

### Firestore (confirmed)

| Setting | Value |
|---------|-------|
| Project | `regal-scholar-453620-r7` |
| Database | `copernicusai` |
| Scout ingest collection | **`research_papers`** (not `papers`) |
| New: circuits | `glmp_circuits` |
| New: heartbeats | `scheduler_status` |

---

## Part 2 — DNA Decoder prototype

### Stack

| Component | Location | Version |
|-----------|----------|---------|
| Miniforge3 | `/media/sdcard/miniforge3` | conda 26.3.2 |
| MEME Suite | `.../envs/meme-env` | 5.5.9 |
| Parser (git + Jetson) | `dna-decoder/glmp_logic_parser.py` · `/media/sdcard/decoder/` | **v0.2.0** |
| JASPAR 2024 CORE | `/media/sdcard/decoder/motifs/` | 2,346 motifs |
| Prokaryotic PWMs | `laci_motif.meme` | LacI lacO1, TrpR (approx) |

### Validated circuits (Jetson)

| Circuit | Sequence | Topology (parser) | Biology |
|---------|----------|-------------------|---------|
| lac operon | `lac_operon_region.fa` (350 bp curated) | Class II (NOT+AND) | LacI + CRP ✅ |
| ara operon | `ara_operon_region.fa` (601 bp NC_000913.3) | Class I (AND only) | AraC not in JASPAR ⚠️ |
| trp operon | `trp_operon_region_v3.fa` (700 bp) | Class II (NOT+AND) | TrpR + CRP ✅ |

### Parser v0.2.0 (in git)

- `--repressor-qvalue-threshold` — looser filter so repressor hits survive before `--max-sites` cap
- TSV header row skip fix
- Production defaults: `--qvalue-threshold 0.05 --repressor-qvalue-threshold 1.0 --max-sites 50`

### Production decode pattern (trp/lac template)

```bash
source /media/sdcard/miniforge3/bin/activate meme-env

fimo --thresh 0.001 --oc results/CIRCUIT_jaspar \
  motifs/JASPAR2024_CORE_non-redundant_pfms_meme.txt sequences/CIRCUIT.fa

fimo --thresh 0.01 --oc results/CIRCUIT_prok \
  motifs/laci_motif.meme sequences/CIRCUIT.fa

python3.8 glmp_logic_parser.py \
  --hits results/CIRCUIT_jaspar/fimo.tsv results/CIRCUIT_prok/fimo.tsv \
  --circuit CIRCUIT_NAME --organism ecoli_k12 \
  --output results/CIRCUIT_logic.json \
  --qvalue-threshold 0.05 --repressor-qvalue-threshold 1.0 --max-sites 50
```

---

## Part 3 — Scheduler & split scouts

### Phase 1 (complete)

Deployed `/media/sdcard/scheduler/`:

- `firestore_config.py`, `setup_firestore_collections.py`, `scheduler/status_writer.py`
- Firestore seeds: `glmp_circuits/_schema`, `scheduler_status/_schema`
- Smoke: `phase1_smoke` heartbeat ✅

### Phase 2 (in git + deployed; partial live test)

```
/media/sdcard/scheduler/scout/
├── scout_pubmed.py      (+ glmp_pubmed_supplement.py)
├── scout_biorxiv.py
├── scout_arxiv.py
├── scout_common.py      ← was missing on first deploy attempt; fixed by full scp
├── query_terms.py
└── scout_ingest.sh
```

**First live run:** `scout_pubmed.py am --no-glmp-queries`

| Field | Value |
|-------|-------|
| `job_id` | `scout_pubmed_am` |
| `last_status` | success |
| `last_doc_count` | 75 (JSON delta estimate) |
| Duration | ~40 s |
| `total_runs` | 1 |

Uses `paper_acquisition_venv/bin/python3` and existing `acquire_pubmed_batch.py --recent 600 --classic 0`.

**Monolith 10:15 cron unchanged.** Split scouts not yet on cron.

### Deploy gotcha (June 24)

Initial `scout_pubmed.py` run failed with `ModuleNotFoundError: scout_common` because not all scout files were copied. **Fix:** deploy entire `jetson/scout/` directory:

```bash
bash collaborations/krampis-virtual-cell/jetson/deploy_phase2.sh
# or scp all *.py from jetson/scout/ to /media/sdcard/scheduler/scout/
```

---

## GitHub state (glmp repo)

| Path | Commit area |
|------|-------------|
| `jetson/` Phase 1 + 2 | `d4df03c`, `3745ba4` |
| `dna-decoder/glmp_logic_parser.py` v0.2.0 | `f222ac2` |
| `lac-operon-annotation-review.md` | `bcd7efb` |
| `glmp-collaboration-plan-2026.md` (revised) | `5a0a4ec` |
| `docs/index.html` Zenodo methods link | `1f9dd22` |

---

## Division of labor

| Task | Cursor (Yoga 9i) | Claude Code (SSH Jetson) |
|------|------------------|---------------------------|
| Write/refactor scripts | ✅ Primary | Review logs |
| Deploy to Jetson | `deploy_phase1.sh` / `deploy_phase2.sh` | `scp`, manual fixes |
| Run FIMO / parser / scout | Dry-run only | ✅ Primary |
| Edit crontab | Document only | ✅ After validation |
| Firestore schema changes | Code in git | Run `--apply` on Jetson |
| Biology validation | Docs, flowchart QA | Expert review coordination |

---

## Immediate next steps

### Scout (Phase 2 completion)

1. ✅ `scout_pubmed.py am` — done
2. Run `scout_biorxiv.py am` and `scout_arxiv.py am`
3. Run `bash /media/sdcard/scheduler/scout/scout_ingest.sh` once (pushes to `research_papers`)
4. Optional: `scout_pubmed.py am` **with** GLMP supplement (slower; 15 terms × 10 papers)
5. Test `pm` slots manually
6. Add cron from `jetson/scout/install_scout_cron.example.sh`
7. **Only then** remove 10:15 monolith cron

### Decoder (Phase 3 in briefing)

1. YAML manifests for lac/ara/trp → `run_batch.py` + `firestore_writer.py`
2. Manual GAL (`yeast_gal_system.yaml`) before automation
3. Wire decoder → `glmp_circuits` Firestore collection

### Other

1. RegulonDB — manual browser download → `/media/sdcard/decoder/motifs/regulondb/`
2. TrpR PWM refinement (PDB 1QP0)
3. Lac operon expert review — [`lac-operon-annotation-review.md`](lac-operon-annotation-review.md)
4. Python 3.8 EOL — plan upgrade before Google drops support
5. `rm /media/sdcard/Miniforge3-Linux-aarch64.sh` (installer cleanup)

---

## Quick reference commands

```bash
# SSH
ssh gary@192.168.1.222

# Env (every manual run)
source ~/.config/copernicus/env
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json

# Split scout (from huggingface-space cwd)
cd /home/gdubs/copernicus-web-public/huggingface-space
/media/sdcard/copernicus-worker/venv/bin/python3.8 \
  /media/sdcard/scheduler/scout/scout_pubmed.py am --no-glmp-queries

# Ingest after scouts
bash /media/sdcard/scheduler/scout/scout_ingest.sh

# Cron log (monolith)
tail -30 .../paper_acquisition_logs/daily_scout/cron.log

# Check heartbeat (Firestore console or script)
# collection: scheduler_status, doc: scout_pubmed_am
```

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*  
*gwelz@gc.cuny.edu · ORCID 0009-0005-7806-0892*  
*Handoff prepared: 2026-06-24*
