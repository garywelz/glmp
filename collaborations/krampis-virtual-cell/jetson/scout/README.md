# Phase 2 — Split Scout Workers

Staged under `jetson/scout/`; deploy to `/media/sdcard/scheduler/scout/` on the Jetson.

## Scripts

| File | Purpose |
|------|---------|
| `scout_pubmed.py` | PubMed acquire + GLMP query supplement (clusters 1–3) |
| `scout_biorxiv.py` | BioRxiv/MedRxiv acquire |
| `scout_arxiv.py` | arXiv acquire |
| `scout_common.py` | Lock files, status_writer, budget math, subprocess wrappers |
| `query_terms.py` | GLMP query term clusters 1–3 |
| `glmp_pubmed_supplement.py` | Extra PubMed searches for GLMP terms |
| `scout_ingest.sh` | One-shot push to Firestore `research_papers` |

## Deploy

From Yoga (git repo root):

```bash
bash collaborations/krampis-virtual-cell/jetson/deploy_phase2.sh
```

## Manual test (Jetson)

```bash
source ~/.config/copernicus/env
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json
cd /home/gdubs/copernicus-web-public/huggingface-space

# Dry run
/media/sdcard/copernicus-worker/venv/bin/python3.8 \
  /media/sdcard/scheduler/scout/scout_pubmed.py am --dry-run-status

# Single source (no GLMP supplement, faster)
/media/sdcard/copernicus-worker/venv/bin/python3.8 \
  /media/sdcard/scheduler/scout/scout_pubmed.py am --no-glmp-queries

# Ingest after all three AM scouts
bash /media/sdcard/scheduler/scout/scout_ingest.sh
```

Check heartbeats: Firestore `scheduler_status` collection (`scout_pubmed_am`, etc.).

## Cron

**Do not remove** the live 10:15 AM `run_daily_scout_with_ingest.sh` until split scouts are validated.

See `install_scout_cron.example.sh` for proposed AM/PM schedule.

## Notes

- Firestore papers collection: **`research_papers`** (not `papers`)
- Acquire scripts are unchanged in `copernicus-web`; scouts wrap them
- `--ingest` on individual scouts is optional; prefer one `scout_ingest.sh` after all three
