# Automations

## Daily update — #team-platform, weekdays 10:00 IST

Posts a "Daily Updates" thread every Monday–Friday at 10:00 IST. People reply in the thread:
what they got done, next steps, blockers. Runs on GitHub's servers, so it works whether or not anyone's laptop is on.

**Turn it on (GitHub web, 2 minutes)**

1. **Secret** — repo *Settings → Secrets and variables → Actions → Secrets → New repository secret*:
   name `MM_TEAM_PLATFORM_WEBHOOK`, value = the incoming webhook URL
   (Mattermost → *Integrations → Incoming Webhooks → "Platform daily update"*).
2. **Workflow** — *Add file → Create new file*, path `.github/workflows/daily-update.yml`,
   paste [`daily-update.yml`](daily-update.yml), commit. Then *Actions → daily-update → Run workflow* to test.

**Notion link** — repo *Settings → Secrets and variables → Actions → Variables*: `PLATFORM_NOTION_URL`.
Change the board without touching the workflow.

**Change the time** — edit the `cron` line (UTC). 10:00 IST = `30 4 * * 1-5`.
