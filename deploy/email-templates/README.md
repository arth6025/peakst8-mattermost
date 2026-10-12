# Branded invite email (one-off)

Replaces Mattermost's built-in "You've been invited" email with the Peakst8 design.
The button uses `{{.Props.ButtonURL}}` — Mattermost's own per-recipient join link.

**It is lost on the next container recreate or upgrade.** That's accepted; re-copy it if needed.

On the server, from the folder with `docker-compose.yml`:

```bash
docker compose cp mattermost:/mattermost/templates/invite_body.html ./invite_body.original.html   # backup
docker compose cp ./email-templates/invite_body.html mattermost:/mattermost/templates/invite_body.html
docker compose restart mattermost
```

Not using our compose file? Same thing with `docker cp <mattermost-container>:/mattermost/templates/invite_body.html …`.

Then send invites from Mattermost: team menu → **Invite People** → paste emails.
Undo: copy `invite_body.original.html` back and restart.

The subject line comes from the site name, not this file: set **System Console → Site Configuration →
Customization → Site Name** to `Peakst8` so it reads "[Peakst8] … invited you to join".
