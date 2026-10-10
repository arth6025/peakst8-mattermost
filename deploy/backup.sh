#!/usr/bin/env bash
# Nightly backup: Postgres dump + uploaded files + config. Keeps 14 days locally.
# Cron (as root):  15 2 * * *  /opt/peakst8-mattermost/deploy/backup.sh >> /var/log/mm-backup.log 2>&1
# Optional off-site copy: set BACKUP_REMOTE in .env to an rclone remote, e.g. "b2:peakst8-mm-backups".
set -euo pipefail
cd "$(dirname "$0")"
set -a; . ./.env; set +a

stamp=$(date +%Y%m%d-%H%M)
dest=backups/$stamp
mkdir -p "$dest"

docker compose exec -T postgres pg_dump -U mmuser -d mattermost -Fc > "$dest/mattermost.dump"
tar -czf "$dest/files.tar.gz" -C volumes/app/mattermost data config \
  --exclude='data/mattermost_local.socket'

find backups -mindepth 1 -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +

if [[ -n "${BACKUP_REMOTE:-}" ]] && command -v rclone >/dev/null; then
  rclone copy "$dest" "${BACKUP_REMOTE}/${stamp}"
fi
echo "$(date -Is) backup ok: $dest ($(du -sh "$dest" | cut -f1))"
