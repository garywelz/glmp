# Jetson Live Recon — 2026-06-24

Verified via `ssh gary@192.168.1.222` before Phase 1 implementation.

## Crontab (America/New_York)

```
10 10 * * * ... remind_paper_scout_coffee.sh
15 10 * * * . ~/.config/copernicus/env && GOOGLE_APPLICATION_CREDENTIALS=~/.config/copernicus/gcp-sa.json \
  .../run_daily_scout_with_ingest.sh >> .../cron.log
```

## Paths (live, not briefing assumptions)

| Item | Path |
|------|------|
| Legacy symlink | `/home/gdubs/copernicus-web-public` → `/media/sdcard/copernicus-worker/copernicus-web` |
| HuggingFace space | `/home/gdubs/copernicus-web-public/huggingface-space` |
| Scout + ingest | `.../scripts/acquire_papers/run_daily_scout_with_ingest.sh` |
| Python venv | `/media/sdcard/copernicus-worker/venv/bin/python3.8` |
| GCP credentials | `/home/gary/.config/copernicus/gcp-sa.json` |
| Env file | `/home/gary/.config/copernicus/env` |
| Decoder | `/media/sdcard/decoder/` |
| Phase 1 deploy target | `/media/sdcard/scheduler/` |

## Firestore (confirmed from ingest script + config)

| Setting | Value |
|---------|-------|
| Project | `regal-scholar-453620-r7` |
| Database | `copernicusai` |
| Scout ingest collection | **`research_papers`** (not `papers`) |
| New collections | `glmp_circuits`, `scheduler_status` |

## Phase 1 — do not change yet

The 10:15 AM `run_daily_scout_with_ingest.sh` cron remains untouched until split scouts are tested.
