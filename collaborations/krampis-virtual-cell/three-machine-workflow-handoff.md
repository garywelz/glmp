# Three-Machine Workflow Handoff
**GLMP / CopernicusAI Project · Gary Welz · June 17, 2026**

This document is written for Cursor/GPT on Yoga 730, which has been inactive for two days and needs to be brought up to speed on the current three-machine setup.

---

## Machine Inventory

### Yoga 730
- **What it is:** Older Lenovo laptop. Primary Cursor workstation until recently.
- **Current role:** GLMP repo editing via Cursor. This is where recent GLMP GitHub work has been done. Still a valid development machine but is being superseded by Yoga 9i as the main interactive workstation.
- **Status as of June 17, 2026:** Has been asleep for ~2 days. Needs a `git pull` before any edits to pick up changes made from Yoga 9i and via Claude Code on Jetson Nano.

### Yoga 9i
- **What it is:** New Lenovo Yoga Pro 9i Aura. Intended to become the primary interactive workstation.
- **Current role:** Active development machine. Runs Cursor. Has been the active machine for the past two days including all recent GLMP plan work and Jetson Nano setup work via Claude Code.
- **SSH to Jetson Nano:** Yoga 9i has passwordless SSH access to Jetson Nano configured with an ed25519 key pair. This was set up on June 16, 2026.
  - Username: `gary`
  - IP: `192.168.1.222`
  - Auth: key-based (no password required)
  - Connect: `ssh gary@192.168.1.222`

### Jetson Nano
- **What it is:** Seeed Studio reComputer J1010, Jetson Nano module, 128GB SanDisk Extreme microSD card.
- **Current role:** Dedicated edge compute node for CopernicusAI. Runs a daily paper scout pipeline (arXiv, PubMed, bioRxiv) and paper ingest to Firestore. Accessed exclusively via SSH — cannot run Cursor directly due to OS constraints (Ubuntu 18.04, GLIBC 2.27, ARM64).
- **OS:** Ubuntu 18.04.6 LTS (L4T, kernel 4.9.337-tegra)
- **Python:** 3.8 (installed via deadsnakes PPA; system Python is 3.6)
- **CUDA:** 10.2 (moved to `/media/sdcard/cuda-10.2`, symlinked from `/usr/local/cuda-10.2`)
- **TensorRT:** moved to `/media/sdcard/tensorrt`, symlinked from `/usr/src/tensorrt`
- **Disk:** eMMC ~3GB used of 14GB; SD card ~270MB used of 120GB (exFAT)

---

## What Is Set Up Where

### Yoga 730
- Cursor (primary editor, used for GLMP repo work)
- Git / GitHub — GLMP repo cloned locally
- Google Cloud SDK (gcloud/gsutil) — assumed present from prior work
- Python environment for GLMP work

### Yoga 9i
- Cursor (active editor)
- Claude Code (CLI) — installed and active; used to SSH into Jetson Nano and run remote commands
- Git / GitHub — GLMP repo cloned
- SSH key pair (`~/.ssh/id_ed25519`) — public key installed on Jetson Nano
- Google Cloud SDK — gcloud authenticated to project `regal-scholar-453620-r7`
- Windows PowerShell terminal

### Jetson Nano
- SSH server (OpenSSH, active on port 22, running since boot)
- Git — installed, functional on eMMC only (SD card is exFAT; git cannot run on exFAT)
- Python 3.8 venv at `/home/gary/copernicus-worker/venv`
- CopernicusAI repo cloned at `/home/gary/copernicus-worker/copernicus-web`
- GCP service account credentials at `~/.config/copernicus/gcp-sa.json`
- Environment file at `~/.config/copernicus/env` (contains OPENAI_API_KEY, GOOGLE_CLOUD_PROJECT, FIRESTORE_DATABASE)
- Cron job: daily scout runs at 10:15 AM ET
- Legacy symlink: `/home/gdubs/copernicus-web-public` → `/home/gary/copernicus-worker/copernicus-web`
- Firestore connection verified: project `regal-scholar-453620-r7`, database `copernicusai`

---

## SSH Connectivity

| From | To | Command | Auth |
|---|---|---|---|
| Yoga 9i | Jetson Nano | `ssh gary@192.168.1.222` | Key-based (id_ed25519), no password |
| Yoga 730 | Jetson Nano | Not yet configured — needs SSH key setup | — |
| Claude Code (Yoga 9i) | Jetson Nano | via SSH in Claude Code terminal | Key-based |

**To set up Yoga 730 → Jetson Nano SSH** (if needed):
```powershell
ssh-keygen -t ed25519   # if no key exists yet
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh gary@192.168.1.222 "cat >> ~/.ssh/authorized_keys"
```

---

## Source of Truth — What to Trust

| Asset | Canonical location | Notes |
|---|---|---|
| GLMP working papers | GitHub: `https://github.com/garywelz/glmp` | Always pull before editing |
| Collaboration plan | GitHub: `collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md` | Updated June 16–17, 2026 |
| CopernicusAI app code | GitHub: `copernicus-web` repo | Cloned on Jetson Nano at `/home/gary/copernicus-worker/copernicus-web` |
| Paper JSON metadata | Firestore: `copernicusai` DB, `research_papers` collection | 47,536 documents as of June 16 |
| GCS HTML previews | `gs://regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/` | Read-only reference; do not edit |
| Zenodo preprints | Zenodo DOIs (see below) | Published; do not edit |

**DO NOT treat local folders on any machine as the source of truth.** Always commit and push to GitHub before switching machines.

---

## What Has Changed in the Last Two Days (While Yoga 730 Was Asleep)

This is the critical update for Yoga 730:

1. **Jetson Nano is now fully operational** as a CopernicusAI ingest worker:
   - Daily scout pipeline running (PubMed 600, BioRxiv 250, arXiv 150 papers/day)
   - Cron job installed, fires at 10:15 AM ET
   - Firestore push verified: 47,536 documents, 4 net new on first scout run
   - Python 3.8 venv with all dependencies installed

2. **GLMP collaboration plan updated** (`glmp-collaboration-plan-2026.md`):
   - Added full Jetson Nano infrastructure section with production details
   - Added new DNA Decoder section (near-term infrastructure build)
   - File renaming section updated to "Complete" (files were already renamed)
   - Synthesis paper status corrected to "GitHub working draft; not yet posted to bioRxiv"
   - Cover email to Krampis drafted; working call scheduled June 18, 2026 at 10:30 AM via Zoom

3. **Disk cleanup on Jetson Nano:** root disk freed from 100% to ~64% used (removed libreoffice, thunderbird, snapd, linux-headers, nvm, cursor-server; moved CUDA and TensorRT to SD card)

4. **SD card on Jetson Nano:** was not being detected due to physical seating issue; reseated, now mounted at `/media/sdcard` (120GB available, exFAT format)

5. **Three Zenodo preprints published:**
   - Welz, G. (2026). *Proof Graphs and Algorithm Capsules.* https://doi.org/10.5281/zenodo.20670491
   - Welz, G. (2026). *AI-Powered Knowledge Engines as Research Infrastructure.* https://doi.org/10.5281/zenodo.20601268
   - Welz, G. (2026). *The Programming Framework.* https://doi.org/10.5281/zenodo.20128888

---

## Recommended Workflow Going Forward

### For GLMP repo work (papers, plan, flowcharts)
- **Primary machine: Yoga 9i** with Cursor
- Yoga 730 can also be used but must `git pull` first every session
- Never edit the same file on two machines without committing and pushing between sessions
- Commit message convention: use descriptive messages referencing the paper or section edited

### For Jetson Nano work (ingest pipeline, scout, diagnostics)
- **Access via: Yoga 9i → Claude Code → SSH**
- Do not attempt to run Cursor, Node.js, or modern Python tooling directly on Jetson Nano
- All git operations on Jetson Nano must happen on eMMC paths (not the SD card)
- Working directory: `/home/gary/copernicus-worker/copernicus-web`

### For GCP / Firestore / Cloud Run work
- Use Yoga 9i or Yoga 730 with gcloud CLI authenticated
- Jetson Nano has read/write access to Firestore via service account only — do not use it for GCP admin tasks

### Git sync discipline
```
Before starting work on any machine:
  git pull origin main

After completing work:
  git add -A
  git commit -m "descriptive message"
  git push origin main
```

---

## What NOT to Run on Jetson Nano

| Task | Reason |
|---|---|
| Cursor IDE | Requires GLIBC 2.28+; Jetson has 2.27 |
| Claude Code | Same GLIBC constraint |
| Modern Node.js (v18+) | Same GLIBC constraint |
| Python 3.10+ | Not available on Ubuntu 18.04 without major work |
| Git operations on SD card | SD card is exFAT; git cannot store on exFAT |
| GPU-intensive model training | 4GB RAM limit; use GCP for training |
| Embedding generation | Keep on OpenAI API to preserve index integrity |
| GCP admin / IAM changes | Use Yoga 9i or Yoga 730 with gcloud |

---

## Readiness Checks — Run These on Each Machine

### Yoga 730 (run these now to verify readiness after sleep)
```bash
# Git status
cd /path/to/glmp && git status && git log --oneline -5

# Pull latest
git pull origin main

# Python
python --version

# gcloud
gcloud auth list
gcloud config get-value project

# Disk space
df -h
```

### Yoga 9i
```bash
# Git status
git status && git log --oneline -5

# SSH to Jetson Nano
ssh gary@192.168.1.222 "echo OK && df -h / && df -h /media/sdcard"

# Claude Code
claude --version

# gcloud
gcloud auth list
```

### Jetson Nano (run via SSH from Yoga 9i)
```bash
# OS
uname -a
lsb_release -a

# Disk
df -h / && df -h /media/sdcard

# Python
python3.8 --version
source /home/gary/copernicus-worker/venv/bin/activate && pip list | grep -E "firestore|openai|biopython"

# Cron
crontab -l

# Firestore connectivity
cd /home/gary/copernicus-worker/copernicus-web
source /home/gary/copernicus-worker/venv/bin/activate
source ~/.config/copernicus/env
GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json python3.8 -c "
from google.cloud import firestore
db = firestore.Client(project='regal-scholar-453620-r7', database='copernicusai')
print('Firestore OK:', db.project)
"

# SSH server
sudo systemctl status ssh

# CUDA symlink
ls -la /usr/local/cuda-10.2
ls -la /usr/src/tensorrt
```

---

## Key Paths Quick Reference

| Item | Machine | Path |
|---|---|---|
| GLMP repo | Yoga 730 | (check local clone path) |
| GLMP repo | Yoga 9i | (check local clone path) |
| CopernicusAI repo | Jetson Nano | `/home/gary/copernicus-worker/copernicus-web` |
| Python venv | Jetson Nano | `/home/gary/copernicus-worker/venv` |
| GCP credentials | Jetson Nano | `~/.config/copernicus/gcp-sa.json` |
| Env file | Jetson Nano | `~/.config/copernicus/env` |
| SD card | Jetson Nano | `/media/sdcard` |
| CUDA | Jetson Nano | `/usr/local/cuda-10.2` → `/media/sdcard/cuda-10.2` |
| Cron log | Jetson Nano | `/home/gary/copernicus-worker/copernicus-web/paper_acquisition_logs/daily_scout/cron.log` |
| Ingest log | Jetson Nano | `/home/gary/copernicus-worker/copernicus-web/paper_acquisition_logs/daily_scout/ingest.log` |

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*
*gwelz@gc.cuny.edu · ORCID 0009-0005-7806-0892*
*Document prepared: June 17, 2026*
