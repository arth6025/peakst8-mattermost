#!/usr/bin/env bash
# Peakst8 Workology — one-shot install on a fresh Ubuntu 22.04 / 24.04 VM.
# Run from this directory as root:  sudo ./install.sh
# Safe to re-run: it only creates what is missing.
set -euo pipefail
cd "$(dirname "$0")"

[[ $EUID -eq 0 ]] || { echo "Run as root (sudo ./install.sh)"; exit 1; }

echo "==> Docker"
if ! command -v docker >/dev/null || ! docker compose version >/dev/null 2>&1; then
  apt-get update -y
  apt-get install -y docker.io docker-compose-v2 curl python3
  systemctl enable --now docker
fi

echo "==> .env"
if [[ ! -f .env ]]; then
  cp .env.example .env
fi
if ! grep -q '^POSTGRES_PASSWORD=.\+' .env; then
  pw=$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 32)
  sed -i "s/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=${pw}/" .env
  echo "    generated POSTGRES_PASSWORD"
fi
chmod 600 .env
set -a; . ./.env; set +a
[[ -n "${DOMAIN:-}" ]] || { echo "DOMAIN missing in .env"; exit 1; }

echo "==> DNS check for ${DOMAIN}"
myip=$(curl -fsS4 https://ifconfig.me || true)
dnsip=$(getent ahostsv4 "$DOMAIN" | awk 'NR==1{print $1}' || true)
if [[ -z "$dnsip" || "$dnsip" != "$myip" ]]; then
  echo "    WARNING: ${DOMAIN} resolves to '${dnsip:-nothing}', this server is '${myip:-unknown}'."
  echo "    HTTPS certificates will fail until the A record points here. Continuing in 10s (Ctrl-C to stop)."
  sleep 10
fi

echo "==> Volumes"
mkdir -p volumes/db volumes/caddy/{data,config} \
  volumes/app/mattermost/{config,data,logs,plugins,client/plugins,bleve-indexes}
chown -R 2000:2000 volumes/app/mattermost   # Mattermost runs as uid 2000

echo "==> Firewall"
if command -v ufw >/dev/null; then
  ufw allow OpenSSH >/dev/null; ufw allow 80/tcp >/dev/null; ufw allow 443 >/dev/null
  ufw --force enable >/dev/null
fi

echo "==> Start"
docker compose pull
docker compose up -d

echo "==> Waiting for https://${DOMAIN}"
for i in $(seq 1 60); do
  if curl -fsS "https://${DOMAIN}/api/v4/system/ping" >/dev/null 2>&1; then
    echo "    up."
    echo "==> Admin, team, channels, settings"
    ./setup.sh "https://${DOMAIN}"
    echo
    echo "Done. https://${DOMAIN} is live. Admin credentials: $(pwd)/admin-credentials.txt"
    exit 0
  fi
  sleep 5
done
echo "Not reachable over HTTPS yet. Check: docker compose logs caddy mattermost"
exit 1
