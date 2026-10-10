#!/usr/bin/env bash
# Post-start setup, same for local and production: creates the System Admin (once),
# mints a token, and runs bootstrap.py (team, channels, settings, #calls webhook).
# Usage: ./setup.sh <site-url> [extra docker compose args, e.g. -f docker-compose.yml -f docker-compose.local.yml]
set -euo pipefail
cd "$(dirname "$0")"
URL=${1:?site url}; shift
DC=(docker compose "$@")
ENV_FILE=${ENV_FILE:-.env}
set -a; . "./$ENV_FILE"; set +a
ADMIN_USER=${ADMIN_USERNAME:-peakst8-admin}
CRED=${CRED_FILE:-admin-credentials.txt}
mmctl() { "${DC[@]}" exec -T mattermost mmctl --local "$@"; }

if mmctl user search "$ADMIN_USER" >/dev/null 2>&1; then
  echo "admin @$ADMIN_USER exists"
else
  pw="$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 20)Aa1!"
  mmctl user create --email "${ADMIN_EMAIL:?set ADMIN_EMAIL in $ENV_FILE}" --username "$ADMIN_USER" \
    --password "$pw" --system-admin --email-verified >/dev/null
  umask 077; printf 'url=%s\nusername=%s\npassword=%s\n' "$URL" "$ADMIN_USER" "$pw" > "$CRED"
  echo "created admin @$ADMIN_USER — credentials in $(pwd)/$CRED (move them to the vault)"
fi

token=$(mmctl token generate "$ADMIN_USER" "bootstrap-$(date +%Y%m%d%H%M)" --json | python3 -c '
import json,sys
raw=sys.stdin.read().strip()
try:
    d=json.loads(raw); d=d[0] if isinstance(d,list) else d; print(d["token"])
except Exception:
    print(raw.split(":")[0].strip())')

MM_URL="$URL" MM_TOKEN="$token" ALLOWED_DOMAIN="${ALLOWED_DOMAIN:-peakst8.club}" python3 ./bootstrap.py
