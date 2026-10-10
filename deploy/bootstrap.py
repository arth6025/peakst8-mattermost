#!/usr/bin/env python3
"""Peakst8 Workology — Mattermost bootstrap.

Creates the team and every channel in build/channels.json, sets server defaults,
and creates the #calls incoming webhook for Bluedot. Idempotent: re-run it after
editing owners, docs links or the vertical list, and it updates in place.

Usage:
  MM_URL=https://mattermost.peakst8.club MM_TOKEN=<admin personal access token> \
    python3 deploy/bootstrap.py [--dry-run] [--manifest build/channels.json]

Standard library only (Python 3.8+).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNELS = ["company-announcements", "decisions", "weekly-digest", "ops-escalations", "random"]
ALLOWED_DOMAIN = os.environ.get("ALLOWED_DOMAIN", "peakst8.club")


class MM:
    def __init__(self, url, token):
        self.base = url.rstrip("/") + "/api/v4"
        self.token = token

    def call(self, method, path, body=None, ok404=False):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        req.add_header("Authorization", "Bearer " + self.token)
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            if ok404 and e.code == 404:
                return None
            sys.exit(f"{method} {path} -> {e.code}: {e.read().decode(errors='replace')[:400]}")


def render(text, owner, docs, name=""):
    owner = owner if owner and owner != "TBD" else "open"
    out = text.replace("{owner}", owner).replace("{docs}", docs or "(coming)")
    out = out.replace("{Name}", name)
    return out.replace("@open", "(open)")


def plan(m):
    """Flatten the manifest into the full list of channels to create."""
    owners, docs = m.get("owners", {}), m.get("docs", {})
    out = []
    for c in m["channels"]:
        out.append(dict(name=c["name"], display_name=c["display_name"], type=c["type"], purpose=c["purpose"],
                        header=render(c["header"], owners.get(c.get("owner_role")), docs.get(c.get("notion_key") or ""))))
    for key, name in m["verticals"].items():
        for t in m["vertical_channel_template"]:
            out.append(dict(name=f"{key}-{t['suffix']}", display_name=f"{name} {t['display_suffix']}", type=t["type"],
                            purpose=render(t["purpose"], None, None, name),
                            header=render(t["header"], owners.get(key), docs.get(key), name)))
    for key, chans in m["horizontal_channels"].items():
        name = m["horizontals"][key]
        for t in chans:
            out.append(dict(name=f"{key}-{t['suffix']}", display_name=f"{name} {t['display_suffix']}", type=t["type"],
                            purpose=render(t["purpose"], None, None, name),
                            header=render(t["header"], owners.get(key), docs.get(key), name).replace("#{vertical}-gtm", "#<vertical>-gtm")))
    for conv in m["on_demand_conventions"].values():
        if not isinstance(conv, dict) or "seed_example" not in conv:
            continue
        out.append(dict(name=conv["seed_example"], display_name=conv["seed_example"].replace("-", " ").title(),
                        type=conv["type"], purpose="Example of the convention: " + conv["rule"],
                        header=f"Convention: {conv['pattern']} | {conv['rule']}"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(ROOT / "build" / "channels.json"))
    ap.add_argument("--state", default=str(ROOT / "build" / "state.json"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    m = json.load(open(a.manifest))
    chans = plan(m)
    names = [c["name"] for c in chans]
    assert len(names) == len(set(names)), "duplicate channel names in manifest"

    if a.dry_run:
        for c in chans:
            print(f"{'private' if c['type'] == 'P' else 'public ':7}  #{c['name']:28} {c['header']}")
        print(f"\n{len(chans)} channels")
        return

    url, token = os.environ.get("MM_URL"), os.environ.get("MM_TOKEN")
    if not url or not token:
        sys.exit("Set MM_URL and MM_TOKEN (a System Admin personal access token).")
    mm = MM(url, token)
    me = mm.call("GET", "/users/me")
    print(f"authenticated as @{me['username']}")

    # Server defaults. Set via API (not env vars) so they stay editable in the System Console.
    # Self sign-up is opened to @ALLOWED_DOMAIN only when email verification is on (needs SMTP);
    # otherwise anyone could type a made-up @peakst8.club address. Until then: invite link only.
    cfg = mm.call("GET", "/config")
    verified = cfg.get("EmailSettings", {}).get("RequireEmailVerification") is True
    mm.call("PUT", "/config/patch", {
        "TeamSettings": {
            "EnableOpenServer": verified,
            "RestrictCreationToDomains": ALLOWED_DOMAIN,
            "MaxUsersPerTeam": 1000,            # default is 50
            "ExperimentalDefaultChannels": DEFAULT_CHANNELS,
        },
        "ServiceSettings": {"EnableIncomingWebhooks": True, "EnableLinkPreviews": True,
                            "EnablePostUsernameOverride": True, "EnablePostIconOverride": True},
    })
    if not verified:
        print(f"WARNING: email verification is off (SMTP not set), so @{ALLOWED_DOMAIN} self sign-up stays closed.")
        print("         Set SMTP_* and SMTP_ENABLED=true in .env, restart, and re-run this script.")
    print("server settings patched")

    t = m["team"]
    team = mm.call("GET", f"/teams/name/{t['name']}", ok404=True)
    if not team:
        team = mm.call("POST", "/teams", {"name": t["name"], "display_name": t["display_name"], "type": t["type"],
                                          "description": t.get("description", "")[:255]})
        print(f"created team {t['name']}")
    # Anyone signed up on the server (only @ALLOWED_DOMAIN can be) may join the team without an invite.
    mm.call("PUT", f"/teams/{team['id']}/patch", {"allowed_domains": ALLOWED_DOMAIN, "allow_open_invite": True})
    state = {"team_id": team["id"], "channels": {}}

    for c in chans:
        ex = mm.call("GET", f"/teams/{team['id']}/channels/name/{c['name']}?include_deleted=true", ok404=True)
        if ex is None:
            ex = mm.call("POST", "/channels", dict(c, team_id=team["id"]))
            print(f"  + #{c['name']}")
        else:
            if ex.get("delete_at"):
                mm.call("POST", f"/channels/{ex['id']}/restore")
                print(f"  ~ #{c['name']} restored")
            want = {k: c[k] for k in ("display_name", "purpose", "header")}
            if any(ex.get(k) != v for k, v in want.items()):
                mm.call("PUT", f"/channels/{ex['id']}/patch", want)
                print(f"  ~ #{c['name']} updated")
        state["channels"][c["name"]] = ex["id"]

    # Incoming webhook for Bluedot -> #calls (via Zapier/Make).
    if "calls" in state["channels"]:
        hooks = mm.call("GET", f"/hooks/incoming?team_id={team['id']}&per_page=200")
        hook = next((h for h in hooks if h["channel_id"] == state["channels"]["calls"]), None)
        if not hook:
            hook = mm.call("POST", "/hooks/incoming", {"channel_id": state["channels"]["calls"],
                                                       "display_name": "Bluedot calls",
                                                       "description": "Call summaries from Bluedot via Zapier/Make",
                                                       "username": "bluedot", "channel_locked": True})
            print("  + incoming webhook for #calls")
        state["calls_webhook_id"] = hook["id"]

    Path(a.state).write_text(json.dumps(state, indent=2))
    team = mm.call("GET", f"/teams/{team['id']}")
    base = url.rstrip("/")
    print(f"\n{len(chans)} channels in place. State written to {a.state}")
    if verified:
        print(f"Sign-up open to @{ALLOWED_DOMAIN}: {base}/signup_user_complete")
    print(f"Team invite link:      {base}/signup_user_complete/?id={team['invite_id']}")
    if "calls_webhook_id" in state:
        print(f"Bluedot webhook URL:   {base}/hooks/{state['calls_webhook_id']}   (treat as a secret)")


if __name__ == "__main__":
    main()
