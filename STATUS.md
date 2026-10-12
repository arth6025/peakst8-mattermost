# Status

_Last checked: 11 Oct 2026, from outside the server._

| | |
|---|---|
| Server | **Live.** Mattermost 11.11.1 behind Cloudflare, health check OK |
| Address for everyone | **https://mattermost.peakst8.club** |
| Site URL on the server | `https://chat.ps8.in` — **wrong, change it** (see below) |
| @peakst8.club self sign-up | **Closed** — SMTP / email verification not on yet |
| Licence | Free (unlicensed); guests off |

## Developer — remaining

- [ ] **Site URL → `https://mattermost.peakst8.club`.** In `deploy/.env` set `DOMAIN=mattermost.peakst8.club`, then
      `docker compose up -d`. Until then, emails, push notifications and shared links point at `chat.ps8.in`.
      Keep `chat.ps8.in` only as a redirect, or remove it.
- [ ] **Open @peakst8.club sign-up.** Fill the `SMTP_*` block in `.env` with `SMTP_ENABLED=true`,
      `docker compose up -d`, then `sudo ./setup.sh https://mattermost.peakst8.club`. The warning disappears when it works.
- [ ] **Phase 3 checks** in the [README](README.md#phase-3--checks-before-anyone-joins): test sign-up, gmail refused,
      mobile push, backups, one restore.
- [ ] **Tell Arvind** when all three are done — Wave 0 starts then.
