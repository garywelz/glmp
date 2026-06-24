#!/usr/bin/env bash
# EXAMPLE cron entries for split scouts — DO NOT install until manual tests pass.
# Keep the existing 10:15 run_daily_scout_with_ingest.sh until split scouts are validated.
#
# Install: crontab -e (merge with existing reminder_coffee line)
# Remove monolith ONLY after 3+ successful days on split scouts + scout_ingest.sh

CRON_TZ=America/New_York
SCHED=/media/sdcard/scheduler
PY=/media/sdcard/copernicus-worker/venv/bin/python3.8
HFS=/home/gdubs/copernicus-web-public/huggingface-space
ENV='. /home/gary/.config/copernicus/env && GOOGLE_APPLICATION_CREDENTIALS=/home/gary/.config/copernicus/gcp-sa.json'

# Morning scout — staggered (after existing 10:10 coffee reminder)
# 15 10 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_pubmed.py am >> /media/sdcard/logs/scout_pubmed_am.log 2>&1
# 20 10 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_biorxiv.py am >> /media/sdcard/logs/scout_biorxiv_am.log 2>&1
# 25 10 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_arxiv.py am >> /media/sdcard/logs/scout_arxiv_am.log 2>&1
# 30 10 * * * ${ENV} bash ${SCHED}/scout/scout_ingest.sh

# Evening scout
# 0 20 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_pubmed.py pm >> /media/sdcard/logs/scout_pubmed_pm.log 2>&1
# 5 20 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_biorxiv.py pm >> /media/sdcard/logs/scout_biorxiv_pm.log 2>&1
# 10 20 * * * ${ENV} cd ${HFS} && nice -n 10 ${PY} ${SCHED}/scout/scout_arxiv.py pm >> /media/sdcard/logs/scout_arxiv_pm.log 2>&1
# 15 20 * * * ${ENV} bash ${SCHED}/scout/scout_ingest.sh
