# Peakst8 Mattermost

Everything needed to run Peakst8's internal chat at **https://mattermost.peakst8.club**: one place for every
internal conversation, part of **Peakst8 Workology** (Mattermost to talk, Notion to keep).

| You are… | Read |
|---|---|
| The developer deploying the server | This README, top to bottom. Detail in [`deploy/RUNBOOK.md`](deploy/RUNBOOK.md). |
| Anyone at Peakst8 joining Mattermost | [`ONBOARDING.md`](ONBOARDING.md) |
| Checking where the deployment stands | [`STATUS.md`](STATUS.md) |
| Finding or creating a channel | [`CHANNELS.md`](CHANNELS.md) — the live channel directory |
| Moving a Google Chat space here | [`skills/gchat-to-mattermost`](skills/gchat-to-mattermost/README.md): setup steps + Claude skill download |

**One command** (`deploy/install.sh`) installs Docker, Postgres, Mattermost 11.11.1 and HTTPS, then creates the
admin, the `peakst8` team, all 33 channels, the @peakst8.club sign-up rule and the Bluedot webhook.

## Get the deployment package

This repo **is** the package. Get it either way, then follow the checklist below.

| Option | How |
|---|---|
| **Download** (one file) | [**peakst8-mattermost.tar.gz**](https://github.com/arth6025/peakst8-mattermost/releases/latest/download/peakst8-mattermost.tar.gz) — always the latest release. All versions: [Releases](https://github.com/arth6025/peakst8-mattermost/releases). |
| **Clone** (easier to update later with `git pull`) | `git clone https://github.com/arth6025/peakst8-mattermost.git` |

Straight onto the server, without a laptop in between:

```bash
sudo mkdir -p /opt/peakst8-mattermost
curl -fsSL https://github.com/arth6025/peakst8-mattermost/releases/latest/download/peakst8-mattermost.tar.gz \
  | sudo tar -xz -C /opt/peakst8-mattermost --strip-components=1
```

---

## Developer checklist

Tick these off in order. Each phase needs the previous one done.

### Phase 1 — Before install

- [ ] **Server** — Ubuntu 24.04 LTS, 2 vCPU, 4 GB RAM, 80 GB SSD, India region. Inbound ports 22, 80, 443 only.
- [ ] **DNS** — `A  mattermost.peakst8.club → <server IPv4>`, live before install (`dig mattermost.peakst8.club`).
      Without it the HTTPS certificate fails.
- [ ] **SMTP** — an outgoing mail account for @peakst8.club (Google Workspace SMTP relay or Amazon SES): host,
      port, user, password, sender address. **Required:** @peakst8.club self sign-up only opens when email
      verification works, otherwise anyone could register a made-up address.
- [ ] **Admin mailbox** — a shared address such as `it@peakst8.club`. It becomes the System Admin.

### Phase 2 — Install (about 10 minutes)

```bash
sudo git clone https://github.com/arth6025/peakst8-mattermost.git /opt/peakst8-mattermost   # or the download above
cd /opt/peakst8-mattermost/deploy
sudo cp .env.example .env
sudo nano .env
sudo ./install.sh
```

- [ ] In `.env`: set `ACME_EMAIL`, `ADMIN_EMAIL`, and the `SMTP_*` block with `SMTP_ENABLED=true`.
      Leave `POSTGRES_PASSWORD` blank — the installer generates it.
- [ ] Run `sudo ./install.sh` and let it finish. It is safe to re-run.
- [ ] Move the admin password from `deploy/admin-credentials.txt` into the team vault, then delete the file.
- [ ] Send the **Bluedot webhook URL** the script prints to Arvind directly. It is a secret — never post it in a channel.
- [ ] If the output says *"self sign-up stays closed"*, SMTP is not working: fix `.env`, run
      `docker compose up -d`, then `sudo ./setup.sh https://mattermost.peakst8.club`.

### Phase 3 — Checks before anyone joins

- [ ] **Sign-up works** — sign up with a test @peakst8.club address; the verification email arrives; you land in
      the Peakst8 team inside #company-announcements, #decisions, #weekly-digest, #ops-escalations and #random.
- [ ] **Other domains are refused** — sign-up with a gmail.com address fails.
- [ ] **Mobile push works** — install the Mattermost app on a phone, sign in, get a notification on an @-mention.
      This is what makes it replace WhatsApp; don't skip it.
- [ ] **Backups run** — as root, `crontab -e`:
      `15 2 * * * /opt/peakst8-mattermost/deploy/backup.sh >> /var/log/mm-backup.log 2>&1`.
      Off-site: install `rclone`, set `BACKUP_REMOTE` in `.env`.
- [ ] **A restore works** — restore one backup onto a scratch server; messages and files come back.
- [ ] **Announce** — post in #tech-general that the server is live, and tell Arvind.

### Phase 4 — Onboarding the team

- [ ] Optional, before sending invites: swap in the branded invite email — [`deploy/email-templates/`](deploy/email-templates/README.md) — and set Site Name to `Peakst8`.

People join in waves ahead of the WhatsApp cutover on **14 November 2026**. Arvind and the channel owners decide
who is in each wave; tech keeps sign-in smooth. Everyone follows [`ONBOARDING.md`](ONBOARDING.md).

- [ ] **Wave 0** — Dilip, Deepak, Arvind, Zadence. Sit with each through the first sign-in and the phone app.
- [ ] **Wave 1** — the 8 channel owners and backups. Add owners to private channels (#finance, #people) as needed.
- [ ] **Wave 2** — one pilot vertical plus Tech. Watch for sign-up, email and push problems; fix before Wave 3.
- [ ] **Wave 3** — everyone else. Every Friday, send Arvind who hasn't signed in (System Console → Users).
- [ ] **Cutover, 14 Nov** — siloed WhatsApp groups go read-only; one stays for urgent pings on the ground.

People without a @peakst8.club email can't sign up — send their names to Arvind, don't create accounts by hand.

### Phase 5 — Ongoing

- [ ] Answer #tech-general the same day.
- [ ] When `build/channels.json` changes: `sudo git pull`, then `sudo ./setup.sh https://mattermost.peakst8.club`.
      It updates in place and never duplicates.
- [ ] Upgrades: backup, change `MM_VERSION` in `.env`, `docker compose pull && docker compose up -d`.

When the **Mattermost Professional** licence is approved:

- [ ] Upload it — System Console → About → Edition and License. No migration.
- [ ] Turn on Guest Access — partners join only their `#ext-` channel.
- [ ] Set up Google sign-in for @peakst8.club, test a joiner and a leaver, then turn off email sign-up.
- [ ] Switch push notifications to `https://push.mattermost.com`.

---

## What's in the repo

```
README.md                 this checklist
ONBOARDING.md             the checklist for everyone joining — share with the team
build/channels.json       the channel tree: verticals × horizontals, owners, Notion links
deploy/
  install.sh              one-shot install on Ubuntu (Docker, firewall, start, then setup.sh)
  setup.sh                admin + team + channels + settings + webhook; re-runnable
  bootstrap.py            the channel/settings logic setup.sh calls (stdlib Python, idempotent)
  docker-compose.yml      Postgres 16 + Mattermost + Caddy (automatic HTTPS)
  Caddyfile               reverse proxy
  .env.example            settings template — copy to .env
  backup.sh               nightly DB + files backup, 14-day retention, optional rclone off-site
  local.sh                rehearse the whole setup on a laptop (needs Docker)
  docker-compose.local.yml  local overrides: localhost:8065 + Mailpit on localhost:8025
  RUNBOOK.md              detail: SMTP, push, licence upgrade, day-2 operations
  email-templates/        branded Peakst8 invite email (one-off swap, see its README)
```

### Rehearse on a laptop (optional)

With Docker running: `cd deploy && ./local.sh`. Mattermost comes up on http://localhost:8065 and every email
(including sign-up verification) is caught at http://localhost:8025. `./local.sh reset` wipes it.

### Changing the channel tree

Edit `build/channels.json` — add a vertical under `verticals`, fill `owners` with Mattermost usernames and `docs`
with Notion URLs — then commit and re-run `setup.sh` on the server. Preview without touching anything:
`python3 deploy/bootstrap.py --dry-run`.

**Never commit** `deploy/.env`, `admin-credentials*.txt` or `build/state.json` — `.gitignore` already blocks them.

Questions: Arvind.
