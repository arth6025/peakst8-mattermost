# Peakst8 Mattermost — deploy runbook (for Zadence)

**Target:** `https://mattermost.peakst8.club` (a shorter alias can be added later: one more A record + a second
site block in `Caddyfile`, and update `DOMAIN`/Site URL).
**Edition:** Mattermost Enterprise binary `11.11.1`, running unlicensed (= free Team Edition features).
When Professional is approved: System Console → About → Edition and License → upload the licence. No migration.

## 1. Server

| | |
|---|---|
| OS | Ubuntu 24.04 LTS (22.04 also fine) |
| Size | 2 vCPU, 4 GB RAM, 80 GB SSD — comfortable to ~200 users |
| Region | Mumbai / Bangalore (closest to users) |
| Ports | 22, 80, 443 open. Nothing else. |
| DNS | `A  mattermost.peakst8.club → <server IPv4>` — before running the install, or HTTPS will fail |

## 2. Install — one command (≈10 minutes)

Production is built from this repo. `deploy/local.sh` runs the identical setup on a laptop first if you want a rehearsal.

```bash
sudo git clone https://github.com/arth6025/peakst8-mattermost.git /opt/peakst8-mattermost
cd /opt/peakst8-mattermost/deploy
sudo cp .env.example .env && sudo nano .env      # ACME_EMAIL, ADMIN_EMAIL + the SMTP_* block (see below)
sudo ./install.sh
```

`install.sh` installs Docker, generates the DB password, opens 80/443, starts Postgres + Mattermost + Caddy,
waits for HTTPS, then runs `setup.sh`, which:

- creates the System Admin `peakst8-admin` (`ADMIN_EMAIL`), password written to `admin-credentials.txt` — move it to the vault and delete the file;
- creates team `peakst8` and every channel in `build/channels.json` with owner/docs headers;
- restricts sign-up to **@peakst8.club**, lets any such user join the team without an invite, raises the 50-user cap, auto-joins the five company channels;
- creates the `#calls` incoming webhook for Bluedot and prints its URL (a secret — send to Arvind directly).

Safe to re-run at any time: `sudo ./setup.sh https://mattermost.peakst8.club`.

### SMTP is required for @peakst8.club self sign-up

Self sign-up only opens when email verification is on, otherwise anyone could register a made-up
`@peakst8.club` address. Fill `SMTP_HOST/PORT/USER/PASSWORD`, `MAIL_FROM` and `SMTP_ENABLED=true` in `.env`
**before** `install.sh` (Google Workspace SMTP relay or SES). If it was missed: fill it, `docker compose up -d`,
re-run `setup.sh` — the script prints a warning while sign-up is still closed.

## 3. Changing channels later

Edit `build/channels.json` (owners, Notion links, a new vertical), commit, `git pull` on the server and re-run `setup.sh`. It updates in place and
never duplicates. `build/state.json` holds ids and the webhook id — keep it private.

## 4. Before Wave 2 (people beyond leadership)

- **Mobile push.** System Console → Environment → Push Notification Server. Unlicensed servers use Mattermost's
  test push service (TPNS), which works but has no SLA. With the Professional licence switch to HPNS.
  Mobile push is what makes this replace WhatsApp — confirm a phone receives a notification before Wave 2.
- **Backups.** `crontab -e` as root:
  `15 2 * * * /opt/peakst8-mattermost/deploy/backup.sh >> /var/log/mm-backup.log 2>&1`
  Off-site: install `rclone`, configure a remote, set `BACKUP_REMOTE=` in `.env`.
  **Test a restore once** onto a scratch VM before cutover (14 Nov).

## 5. When Professional is approved

1. Upload the licence (System Console → Edition and License).
2. Enable guest accounts (Authentication → Guest Access) — partners go only into `#ext-*` channels.
3. Wire SSO (Google or the chosen IdP) and test a joiner and a leaver before switching email sign-up off.
4. Switch push to HPNS (`https://push.mattermost.com`).

## 6. Day-2

| Task | How |
|---|---|
| Upgrade | Change `MM_VERSION` in `.env` → `docker compose pull && docker compose up -d`. Take a backup first. Read the release notes for 11.x → 12.x before crossing a major. |
| Logs | `docker compose logs -f mattermost` |
| Admin CLI | `docker compose exec mattermost mmctl --local <command>` |
| Restore | `pg_restore -U mmuser -d mattermost --clean` from `mattermost.dump`, untar `files.tar.gz` into `volumes/app/mattermost` |
| Update the kit | `cd /opt/peakst8-mattermost && sudo git pull`, then re-run `setup.sh` |
