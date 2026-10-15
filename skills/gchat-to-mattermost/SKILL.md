---
name: gchat-to-mattermost
description: Move a Google Chat space or group conversation into a Peakst8 Mattermost channel, with original authors and times kept, nobody pinged, and a pinned summary on top. Use when someone says "move this Google Chat space to Mattermost", "migrate our G-chat group", "bring the chat history over", "import Google Chat into Mattermost", or names a Google Chat space and a Mattermost channel.
---

# Google Chat → Mattermost (Peakst8)

Moves the history of one Google Chat space into one Mattermost channel on **https://mattermost.peakst8.club**, then leaves a pinned summary so the team can stop using the old space.

The person running this (usually Neil) only needs to name the source space and the target channel. Everything else is below.

## Before you start (one-time setup)

Check these first. If any is missing, stop and tell the person exactly which step to do.

1. **Claude in Chrome** is installed and connected, and the person is signed in to Google Chat in that Chrome (https://chat.google.com).
2. **Mattermost connector** is added in Claude: Settings → Connectors → Add custom connector → `https://mattermost.peakst8.club/plugins/mattermost-ai/mcp-server/mcp` → sign in with their Mattermost account. Check by calling the connector's `get_me`.
3. The person is a member of the target channel, or allowed to create one.

## Ask once, up front

- Which **Google Chat space** (exact name)?
- Which **Mattermost channel**? Existing, or a new one? For a new one, follow the naming rules: `team-<name>`, `project-<name>-<year>`, or `<event>-<city>-<year>`, lowercase, hyphens only (no dots: "Ironman 70.3" → `ironman70-3`). Ask who the owner is.
- **Everything**, or a date range? Default: everything.
- **Full history**, or a **summary** (decisions, open tasks, links)? Default: both. Full history in a thread, summary pinned.

## Step 1: read the Google Chat space

1. Open https://chat.google.com in a **new tab**. Never reuse or reload a tab the person is typing in, because Chat warns about unsaved drafts. Find the space with the `find` tool and open it.
2. **Load the whole history.** Chat loads lazily. Run JavaScript that finds the biggest scrollable element in the message pane, sets `scrollTop = 0`, waits about 1.5 s, and repeats until `scrollHeight` stops growing. Then read the messages with `get_page_text`.
3. **Threads:** look for buttons like "3 replies". Click each one. The replies open in a side panel that `get_page_text` doesn't include, so read them with JavaScript: `document.body.innerText`, sliced from the last occurrence of "N replies". Note which message each thread belongs to.
4. **If output is blocked or cut:** the Chrome extension hides output that looks like links, emails or phone numbers, and trims long output to about 600 characters. Clean the text inside the JavaScript first (replace emails with `[email]`, phone numbers with `[phone]`, drop `?…` query strings), store it on `window`, then read it back in 600-character slices.
5. Keep, for every message: **author, date, time, text**, plus thread replies under their parent.

## Step 2: clean it

- Remove **phone numbers, personal emails, home addresses and payment details**. Keep work links (docs, sheets, event links), but strip tracking query strings.
- **Write names out without @** ("Jithin K Sunil", not "@Jithin"), so nobody is pinged by old messages.
- Drop "joined / left / added" system lines, reactions and empty media placeholders. Keep image captions as text.

## Step 3: show the person a preview (required)

Before posting anything, show:
- the target channel and how many messages and days you'll post;
- the first two days exactly as they'll appear;
- the summary post in full.

**Only post after they say yes.** Posting notifies channel members.

## Step 4: post into Mattermost

Use the Mattermost connector. Post as the person's own account.

1. **Create the channel** if it's new: public by default, with the header `Owner: @<owner> · <what it's for> · Channel list: https://github.com/arth6025/peakst8-mattermost/blob/main/CHANNELS.md`. Make the owner channel admin with `update_channel_member_roles`.
2. **Intro post** (becomes the thread root):
   `📥 **History: <space name> (Google Chat), <first date> – <last date>.** Moved here so the history lives with the team. Open the thread: one reply per week, original author and time on every message, no one pinged. From now on this conversation happens here.`
3. **One reply per week** in that thread (`create_post` with `root_id` = the intro post). Format:
   ```
   ### Week of 7 Sep
   #### Mon 7 Sep
   **Jithin K Sunil** · 18:04
   <message text>
   > ↳ **Arvind Subramanian** · 12:15: <thread reply>
   ```
   Keep each post under 15,000 characters. Split a busy week into two posts if needed.
4. End the last reply with: `_End of the Google Chat history (last message <date>)._`
5. **Summary post** (top-level, if asked): what it is, key dates, decisions, open tasks with owners, and key links. Then **pin** both the intro and the summary with `pin_post`.

**Gotchas:**
- **Group DMs** (no team) fail with `create_post`. Use `group_message` instead; it can't thread, so post one combined message.
- **A 502 or timeout** can still mean the post went through. **Read the channel back before retrying**, and delete any duplicate you created.

## Step 5: close the loop

- Read the channel back and confirm the posts are there, in order, and pinned.
- Tell the person:
  - what moved (message count, date range, thread replies included);
  - what was left out (personal data, media files);
  - two manual steps for them:
    1. In Google Chat, post "We've moved to ~<channel> on Mattermost" and restrict who can post in the space.
    2. Ask Arvind to add the channel to CHANNELS.md if it's new.

## Never

- Post before the person approves the preview.
- Bring over phone numbers, personal emails, addresses or payment details.
- @mention people in migrated history.
- Delete anything in Google Chat.
