#!/bin/bash
set -euo pipefail

# Historical 10:45 standalone installer. Production now runs MASTER_TODO from
# run_post_ingest_hooks.sh after ingest success. Keep this path in sync with
# that hook: the glmp git checkout, never /media/sdcard/glmp-cron/.
CRON_CMD='/media/sdcard/venvs/master-todo-cron/bin/python /media/sdcard/glmp/scripts/build_master_todo.py >> /media/sdcard/logs/master_todo_cron.log 2>&1'
PROD_LINE='45 10 * * * '"$CRON_CMD"

schedule_temp() {
  local now_m now_h target_m target_h dom mon
  now_m=$(date +%M)
  now_h=$(date +%H)
  target_m=$((10#$now_m + 3))
  target_h=$now_h
  if [ "$target_m" -ge 60 ]; then
    target_m=$((target_m - 60))
    target_h=$((10#$now_h + 1))
  fi
  dom=$(date +%-d)
  mon=$(date +%-m)
  crontab -l > /tmp/crontab.master_todo.bak
  {
    crontab -l
    echo ''
    echo '# TEMP master-todo cron test (remove after verify)'
    echo "$target_m $target_h $dom $mon * $CRON_CMD"
  } | crontab -
  echo "SCHEDULED: $target_m $target_h $dom $mon * (Jetson local ET)"
  date
  crontab -l | tail -3
}

install_prod() {
  crontab /tmp/crontab.master_todo.bak
  {
    crontab -l
    echo ''
    echo '# GLMP MASTER_TODO assembler — 10:45 AM ET (after scout ingest)'
    echo "$PROD_LINE"
  } | crontab -
  echo 'PRODUCTION CRON INSTALLED:'
  crontab -l | tail -3
}

case "${1:-}" in
  install-temp) schedule_temp ;;
  install-prod) install_prod ;;
  *) echo "usage: $0 install-temp|install-prod" >&2; exit 1 ;;
esac
