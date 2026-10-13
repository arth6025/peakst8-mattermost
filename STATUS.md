# Status

_Last checked: 13 Oct 2026._

| | |
|---|---|
| Server | **Live** at https://mattermost.peakst8.club — Mattermost **Team Edition** (free, no message cap) |
| Site URL | `https://mattermost.peakst8.club` ✅ |
| Claude MCP | Connected via the Agents plugin MCP server (OAuth) ✅ |
| Channels | See [CHANNELS.md](CHANNELS.md) |
| Branding | Team icon = Peakst8 logo ([`assets/peakst8-team-icon.png`](assets/peakst8-team-icon.png)) ✅ |

## Open

- [ ] **Uptime monitor** — add the `MM_STATUS_WEBHOOK` secret and the workflow file ([deploy/monitoring](deploy/monitoring/README.md)).
- [ ] **peakst8_bot** — turn on *System Console → Integrations → Bot Accounts*, then create the bot, so welcome and alert posts come from it.
- [ ] **Site name** — *System Console → Site Configuration → Customization → Site Name* = `Peakst8`, so emails and the browser tab say Peakst8.
- [ ] **Default channels** for new members: #town-square, #announcements, #decisions.
