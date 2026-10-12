# Uptime monitor → #alert-systems

Checks `https://mattermost.peakst8.club/api/v4/system/ping` every 5 minutes from GitHub Actions — outside the
server, so it still reports when the server is down.

| Event | What happens |
|---|---|
| Down (3 failed tries) | GitHub issue labelled `outage` opens → GitHub emails repo watchers; post to #alert-systems is attempted |
| Back up | Issue closes with the downtime; recovery posted in #alert-systems |
| Every day 09:00 IST | "Mattermost up" heartbeat in #alert-systems — if it doesn't arrive, something is wrong |

## Turn it on (2 steps, GitHub web)

1. **Secret** — repo *Settings → Secrets and variables → Actions → New repository secret*:
   name `MM_STATUS_WEBHOOK`, value = the incoming webhook URL for #alert-systems
   (Mattermost → *Integrations → Incoming Webhooks → "Uptime monitor"*).
2. **Workflow** — *Add file → Create new file*, path `.github/workflows/uptime.yml`, paste [`uptime.yml`](uptime.yml), commit.
   Then *Actions → uptime → Run workflow* once to test.

Watch the repo (*Watch → All activity*) to get the outage emails.
GitHub pauses scheduled workflows after 60 days without a commit — re-enable from the Actions tab if that happens.
