#!/usr/bin/env bash
# Run the whole Peakst8 Mattermost setup on this laptop, exactly as production will be built.
#   ./local.sh         start + set up      ./local.sh down     stop (keeps data)
#   ./local.sh reset   stop and delete all local data
set -euo pipefail
cd "$(dirname "$0")"
DC=(docker compose -p peakst8-local --env-file .env.local -f docker-compose.yml -f docker-compose.local.yml)
case "${1:-up}" in
  down)  "${DC[@]}" down; exit 0 ;;
  reset) "${DC[@]}" down -v; rm -rf volumes-local admin-credentials.local.txt; exit 0 ;;
esac
command -v docker >/dev/null || { echo "Docker is not installed."; exit 1; }
mkdir -p volumes-local/db volumes-local/app/mattermost/{config,data,logs,plugins,client/plugins,bleve-indexes}
"${DC[@]}" up -d
echo -n "waiting for Mattermost"
until curl -fsS http://localhost:8065/api/v4/system/ping >/dev/null 2>&1; do echo -n .; sleep 3; done; echo
ENV_FILE=.env.local CRED_FILE=admin-credentials.local.txt ./setup.sh http://localhost:8065 \
  -p peakst8-local --env-file .env.local -f docker-compose.yml -f docker-compose.local.yml
echo
echo "Mattermost:  http://localhost:8065   (admin login in admin-credentials.local.txt)"
echo "Mailbox:     http://localhost:8025   (verification emails land here)"
