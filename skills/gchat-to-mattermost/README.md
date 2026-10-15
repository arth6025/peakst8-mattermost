# Google Chat → Mattermost: Claude skill

For **Neil and the Yoska team**: move a Google Chat space into a Peakst8 Mattermost channel, with history, authors and times kept and a pinned summary on top. Claude does the work; you approve before anything is posted.

**Download the skill:** [gchat-to-mattermost.zip](https://github.com/arth6025/peakst8-mattermost/raw/main/skills/gchat-to-mattermost.zip) · the skill itself is [`SKILL.md`](SKILL.md)

---

## One-time setup (about 5 minutes)

- [ ] **Install the skill:** Claude desktop → **Settings → Capabilities → Skills → Upload skill**, then pick `gchat-to-mattermost.zip`.
- [ ] **Connect Mattermost:** Claude → **Settings → Connectors → Add custom connector**, use
  `https://mattermost.peakst8.club/plugins/mattermost-ai/mcp-server/mcp`, then sign in with your Mattermost account.
- [ ] **Claude in Chrome:** install the extension, and sign in to Google Chat (https://chat.google.com) in that Chrome.

## Moving a space

Type something like:

> Move the Google Chat space "Yoska Ops" into #ironman70-3-goa-2026

## What the skill does from there

1. **Asks** which channel to use, or creates one (following the naming rules in [CHANNELS.md](../../CHANNELS.md) and setting an owner), and whether you want the full history, a summary, or both.
2. **Reads the whole space**, including thread replies. It loads all the history and works around the browser extension's limits on output.
3. **Cleans it:** strips phone numbers, personal emails and addresses. Names are written out without @, so nobody gets pinged.
4. **Shows you a preview** and waits for your go-ahead.
5. **Posts** one intro message with a weekly thread of history under it, plus a pinned summary of decisions, open tasks and links.
6. **Checks** the channel to confirm it all landed without duplicates. Then it reminds you to post a "we've moved" note in Google Chat, and to ask Arvind to add any new channel to [CHANNELS.md](../../CHANNELS.md).

It never deletes anything in Google Chat, and never posts before you approve.

## If something goes wrong

| What you see | What to do |
|---|---|
| Claude can't find the Mattermost tools | Check the connector shows as connected in Settings → Connectors, then start a new chat. |
| Google Chat shows "Use here" or "open in another window" | Close other Google Chat tabs, or click **Use here** yourself, then ask Claude to retry. |
| Only recent messages came through | Ask Claude to "load the full history again". Chat loads older messages lazily. |
| A post appears twice | Ask Claude to delete the duplicate. A timeout can still post. |

Questions: Arvind on Mattermost (@arth).
