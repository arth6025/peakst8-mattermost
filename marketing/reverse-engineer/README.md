# Reverse engineer any video

Saw a video you love on X, LinkedIn, YouTube or Instagram? Paste the link into Claude and get **the same format back as a peakst8 video (MP4)**: same pacing, structure, layout and motion, with our brand, logo and copy.

It runs on [HyperFrames](https://github.com/heygen-com/hyperframes), an open-source tool that turns HTML into video, and lives in its own repo: **[arth6025/reference-video-kit](https://github.com/arth6025/reference-video-kit)**.

**The idea:** keep a swipe file of the best videos on the internet, then reverse engineer each one into ours. That's a social roadmap that writes itself, and it's a good fit for the newer IPs like IRONMAN.

## Set up (once, about 3 minutes)

Open **Claude Code** (desktop app or terminal) and paste:

```
Clone https://github.com/arth6025/reference-video-kit and set it up.
```

Claude installs everything and tells you when it's ready. Then start a new Claude Code session.
You need a Mac with Node 20+ and Python 3; Claude will tell you if anything is missing.

## Make a video

1. Paste the video link, plus what it's for:
   ```
   /reference-video https://x.com/someone/status/123456
   ```
   or in plain words:
   ```
   Make a video like this one for us: [link]. It's for [the festival registrations], [9:16 for Reels].
   ```
2. Claude downloads the video, breaks it down scene by scene and shows you a **storyboard**: their scene → our scene.
3. Reply **"go"**, or ask for changes.
4. Claude builds and renders the MP4 and shows it side by side with the original. It's saved in `reference-video-kit/projects/`.

## Follow-ups you can ask for

- "Make a 9:16 version for Reels"
- "Cut it to 15 seconds"
- "Change the headline in scene 2 to …"
- "Add a voiceover"
- "Use the same storyboard but with [another link] as the style"

## Good to know

| | |
|---|---|
| **What gets copied** | The *format* only: pacing, structure, layout, motion. Never their footage, logo, music, voice or words. |
| **Links that won't download** | Private posts or LinkedIn posts behind a login. Save or screen-record the video and drop the file into Claude instead. |
| **How long** | 1–2 hours per video, mostly hands-off. You step in once, to approve the storyboard. |
| **Music** | Drop your own .mp3 into the chat; otherwise the video is silent. |
| **People** | Use real, approved peakst8 photos or event footage only. No stock models or AI faces passed off as members. |
| **For the festival look** | Mention "use the PSF27 brand kit" and attach assets from [`../peakst8-festival-2027/psf27-social/skills/peakst8-festival-social/assets/`](../peakst8-festival-2027/psf27-social/skills/peakst8-festival-social/assets/). |

Questions? Ask Arvind.
