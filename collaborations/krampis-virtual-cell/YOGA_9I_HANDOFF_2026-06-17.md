# Handoff Report — Yoga 9i Cursor

**GLMP / CopernicusAI Project · Gary Welz · June 17, 2026**  
**Prepared for:** Cursor on Yoga 9i  
**Covers:** June 15–17, 2026 — all three machines

**Related docs:**
- [`three-machine-workflow-handoff.md`](three-machine-workflow-handoff.md) — machine roles, SSH, workflow rules
- [`jetson/JETSON_SETUP_HANDOFF.md`](jetson/JETSON_SETUP_HANDOFF.md) — Jetson ingest worker technical detail
- [`glmp-collaboration-plan-2026.md`](glmp-collaboration-plan-2026.md) — canonical Krampis collaboration plan

---

## Machine Context

| Machine | Role | Status |
|---|---|---|
| Yoga 730 | Older Lenovo; Cursor/GPT; GLMP repo work | Active June 17; QA pass complete |
| Yoga 9i | New primary workstation; Cursor + Claude Code | This machine — receiving handoff |
| Jetson Nano | Seeed Studio reComputer J1010; SSH-only; CopernicusAI ingest worker | Fully operational |

**GitHub is the source of truth.** Always `git pull` before editing on any machine.

---

## What Was Accomplished June 15–17

### 1. Jetson Nano — Full Recovery and Production Setup (June 15–16)

The Jetson Nano had been stuck in an emergency boot loop due to a full root disk (100% used) caused by a broken Cursor `.deb` install and a missing/unseated SD card. Full recovery was completed via the emergency shell and SSH from Yoga 9i.

**Recovery steps completed:**
- Diagnosed emergency mode boot loop — root cause: `/etc/fstab` entry for SD card (`/dev/mmcblk1p1`) failing because card was not detected
- Removed broken fstab entry; rebooted to desktop
- Freed root disk from 100% → 64% by removing: libreoffice, thunderbird, snapd, linux-headers, `.nvm`, `.cursor-server`, Downloads cache, Chromium cache
- Moved CUDA 10.2 (2.9GB) and TensorRT (537MB) to SD card with symlinks
- Physically reseated SD card (SanDisk Extreme 128GB) — was not making contact; now detected as `mmcblk1`, 120GB available
- Mounted SD card at `/media/sdcard` (exFAT); added to `/etc/fstab` with `nofail` option
- Fixed `/etc/passwd` home directory corruption (caused by a failed `usermod` attempt) via SSH from Yoga 9i

**CopernicusAI ingest worker setup (via Claude Code on Yoga 9i → SSH → Jetson Nano):**
- Generated SSH key pair on Yoga 9i (`~/.ssh/id_ed25519`); installed on Jetson Nano — passwordless SSH now working
- Copied GCP service account credentials to `~/.config/copernicus/gcp-sa.json` (chmod 600)
- Fetched `OPENAI_API_KEY` from GCP Secret Manager; wrote `~/.config/copernicus/env`
- Installed Python 3.8 via deadsnakes PPA (Ubuntu 18.04 system Python is 3.6, too old)
- Cloned `copernicus-web` repo to `/home/gary/copernicus-worker/copernicus-web`
- Created venv at `/home/gary/copernicus-worker/venv`; installed all dependencies (biopython, google-cloud-firestore, google-auth, openai, requests, pdfplumber, PyPDF2, google-cloud-secret-manager)
- Fixed two broken venvs in repo: `huggingface-space/paper_acquisition_venv` and `cloud-run-backend/venv`
- Firestore connection verified: `regal-scholar-453620-r7 / copernicusai`
- Smoke test passed: 3 priority DOIs acquired via Crossref
- Pushed 47,331 local JSON papers to Firestore: 6 net new, 47,325 skipped (already existed)
- Daily scout run: PubMed (600), BioRxiv/MedRxiv (250), arXiv (150) — all OK — 4 net new papers
- Cron job installed: fires daily at 10:15 AM ET

**Key paths on Jetson Nano:**

| Item | Path |
|---|---|
| Repo | `/home/gary/copernicus-worker/copernicus-web` |
| Venv | `/home/gary/copernicus-worker/venv` |
| Credentials | `~/.config/copernicus/gcp-sa.json` |
| Env file | `~/.config/copernicus/env` |
| Cron log | `.../paper_acquisition_logs/daily_scout/cron.log` |
| SD card | `/media/sdcard` (120GB, exFAT) |
| CUDA | `/usr/local/cuda-10.2` → `/media/sdcard/cuda-10.2` |
| TensorRT | `/usr/src/tensorrt` → `/media/sdcard/tensorrt` |

**Known Jetson constraints:**
- Ubuntu 18.04, GLIBC 2.27 — cannot run Cursor, Claude Code, or modern Node.js directly
- SD card is exFAT — git cannot operate on it; all repo work on eMMC only
- Python 3.8 only (3.10+ not available without major work)
- Root disk: ~64% used, ~4.8GB free — monitor; do not install large packages without checking

---

### 2. GLMP Collaboration Plan — Full Revision (June 16–17)

The `glmp-collaboration-plan-2026.md` was substantially revised and is pushed to GitHub as the canonical document for the Krampis collaboration.

**Canonical location:**  
`collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md`  
https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md

**What was added/changed:**
- **Jetson Nano infrastructure section** — daily scout specs, cron schedule, first-run results, key paths, known constraints
- **DNA Decoder section** — five-stage pipeline; Jetson handles stages 1–3; GCP handles 4–5; Biolink/KGX target; candidate prototype design
- **Document count clarification** — 47,536 = first scout run count; 59,702 = total Firestore index from all prior ingestion
- **Benchmark count clarification** — Paper III used 16 models total; 14 support the DE20 metric
- **"Largest corpus" claim softened** — "one of the largest curated corpora focused on regulatory biology and sequence-to-logic evidence"
- **Flowchart section rewritten** — live collection exists; must undergo QA/correction pass before training corpus; expansion blocked until QA signed off
- **Lac operon QA caveat** — flagged with `circuitClassNeedsReview: true`; not anchor example until Krampis validates
- **File renaming section** — updated to "Complete"
- **Synthesis paper status** — GitHub working draft; not yet on bioRxiv
- **DNA Decoder added** to paper trajectory table and Division of Labor
- **Immediate Next Steps** — QA/correction pass leads; Batch 1 expansion replaced with QA task
- **Date** — June 17, 2026

**Files intentionally NOT committed (local temp copies only):**
- `GLMP-plan-06172026.md`
- `GLMP-plan-06172026 (1).md`
- `glmp-collaboration-plan-2026_update-0617 (1).md`

---

### 3. Three-Machine Workflow Handoff Document (June 17)

Created and committed: [`three-machine-workflow-handoff.md`](three-machine-workflow-handoff.md)

Covers: machine roles, software/credentials/SSH setup on each machine, source of truth hierarchy, recommended workflow, what not to run on Jetson Nano, and readiness checks for all three machines.

---

### 4. GLMP Flowchart QA Pass (June 17 — Cursor on Yoga 730)

Cursor/GPT on Yoga 730 ran a full QA/correction pass on the existing flowchart collection and pushed results.

**Commit:** `aecd8db` — `Fix flowchart QA metadata and class review flags`

**Live collection as of this commit:**

| Metric | Value |
|---|---|
| Total charts | 217 |
| Class I | 70 |
| Class II | 72 |
| Class III | 52 |
| Class IV | 16 |
| Class V | 7 |
| Total loops | 527 |

**Key corrections made:**
- `synthetic_fold_change_detector` reclassified as **Class I / Feed-forward cascade** (was incorrectly assigned)
- `ecoli_lac_operon` now has `circuitClassConfidence: medium` and `circuitClassNeedsReview: true`
- Hardcoded complexity metadata issue addressed
- Class II/III/IV charts with `loops == 0` reviewed and flagged

**GCS deployment verified:**
- `glmp-v2/metadata.json`
- `glmp-v2/data/metadata.json`
- `glmp-v2/viewer/metadata.json`
- All corrected/review-flagged process JSONs live

---

### 5. Zenodo Preprints Published

| Paper | DOI |
|---|---|
| Proof Graphs and Algorithm Capsules (v2.0) | https://doi.org/10.5281/zenodo.20670491 |
| AI-Powered Knowledge Engines as Research Infrastructure | https://doi.org/10.5281/zenodo.20601268 |
| The Programming Framework (v2) | https://doi.org/10.5281/zenodo.20128888 |

---

### 6. Krampis Collaboration — Ready for Call

**Working call:** June 18, 2026 at 10:30 AM via Zoom

**Cover email:** Sent to Krampis with canonical GitHub link and three Zenodo DOIs.

**Suggested call agenda:**
1. Align on priority order
2. QA/correction pass on flowchart collection — discuss lac operon review findings
3. Define sequence annotation schema for GLMP flowchart nodes
4. RegVelo configuration for K562 GRN
5. GitHub pull request workflow for Krampis contributions
6. DNA Decoder tool choices (FIMO vs. MEME vs. prokka for stage 2)

---

## Current GitHub State

| File | Commit | Status |
|---|---|---|
| `collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md` | `5c6f889` | Live, canonical |
| `collaborations/krampis-virtual-cell/three-machine-workflow-handoff.md` | `5c6f889` | Live |
| Flowchart QA metadata + process JSONs | `aecd8db` | Live, GCS deployed |

---

## Immediate Next Priorities (Do Not Start New Flowchart Batches Yet)

1. **Krampis call** — June 18 at 10:30 AM. No new commits needed before call.
2. **Post-call:** Update plan based on Krampis feedback; begin joint sequence annotation schema definition
3. **Remaining QA items** (after call):
   - Validation script to prevent future class/topology contradictions
   - Remaining Class II/III/IV charts with `loops == 0` needing biological review
   - Lac operon class/loop/sequence annotation — awaiting Krampis biological validation
4. **New flowchart batch expansion** — blocked until QA pass signed off jointly with Krampis
5. **Methods paper revision** — reframe abstract/intro around Big Picture Goal; add lac operon sequence annotation section (after QA)
6. **RPE1 replication** — download benchmark data from scPerturb / Figshare; run classification using `gene_circuit_classes.tsv` protocol

**CopernicusAI / Jetson (post-call, lower urgency than Krampis QA):**
- P1: Full curated DOI ingest (192 GLMP priority DOIs) on Jetson
- P2: `glmp_relevant` auto-tagging at ingest
- P3: Local OpenAI embeddings before Firestore push
- P4: DNA Decoder stages 1–3 (PDF parse, motif scan)

---

## SSH Quick Reference

```bash
# From Yoga 9i to Jetson Nano
ssh gary@192.168.1.222

# Check Jetson disk
ssh gary@192.168.1.222 "df -h / && df -h /media/sdcard"

# Check cron log
ssh gary@192.168.1.222 "tail -20 /home/gary/copernicus-worker/copernicus-web/paper_acquisition_logs/daily_scout/cron.log"

# Check Firestore connectivity on Jetson
ssh gary@192.168.1.222 "source ~/.config/copernicus/env && GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json /home/gary/copernicus-worker/venv/bin/python3.8 -c \"from google.cloud import firestore; db = firestore.Client(project='regal-scholar-453620-r7', database='copernicusai'); print('Firestore OK:', db.project)\""
```

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*  
*gwelz@gc.cuny.edu · ORCID 0009-0005-7806-0892*  
*Handoff prepared: June 17, 2026*
