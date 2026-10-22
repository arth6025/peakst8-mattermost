---
name: peakst8-festival-social
description: Design on-brand social posts for peakst8 Festival 2027 (PSF27): Instagram statics, carousels, stories, reel covers and highlight covers, rendered to PNG from the official brand kit (glass "family of forms", Boldonse/Anton/Sora/Micro 5 type, GRILL/CORE/VITAL/PRESENCE/BRISTLE/BONE palette, plain backgrounds, img bank, logos). Use whenever someone asks for a peakst8 / Peak State / PSF festival post, carousel, story, cover, announcement, speaker card, partner/sponsor post, lineup or countdown, or hands over festival copy and says "design this", "make this a post", "turn this into a carousel".
---

# peakst8 Festival 2027 — social design

Turns copy into finished, on-brand PNGs. Everything needed is inside this folder:

```
SKILL.md
references/brand.md      ← the brand system (read first, every time)
references/layouts.md    ← every layout, format and brief field
scripts/make.py          ← brief.json → HTML → PNG (one per slide)
scripts/render.sh        ← HTML → PNG via headless Chrome
assets/bg/bg1–8.jpg      ← plain backgrounds, forms already composed (4:5)
assets/elements/01-meet … 08-flow.png   ← the 8 glass forms (transparent)
assets/img-bank/         ← macro / sport photography (blue-orange)
assets/textures/         ← dust & dither scans
assets/logo/             ← psf_white / psf_bone / psf_black .svg
assets/fonts/            ← Boldonse, Anton, Sora, Micro 5 Charted
assets/examples/         ← the designer's own posts + key kit pages (ground truth)
examples/briefs/ + examples/renders/    ← working briefs and what they produce (renders saved as JPEG; make.py writes PNG)
```

## Workflow

1. **Read `references/brand.md`.** For a new kind of post, also look at the closest file in `assets/examples/` (text_ann, text_ann2, experience1/2, partner_ann, gen_ann, cover, kit-speakers).
2. **Pin down the brief.** You need: format(s), the copy, and the purpose (announcement, partner, speaker, format/experience, explainer, countdown). If the copy is long, split it: headline ≤ 6 words on the image; the rest goes in the caption. Don't invent facts (names, dates, prices, venues). Use only what the person gave you. The festival date is **30 January 2027**. (The designer's mock-ups in `assets/examples/` say 14 January: that was a placeholder, never use it.)
3. **Pick a layout** (`references/layouts.md`):
   - Short punchy line → `headline` on a bg whose free space suits the line length.
   - A sport / format / experience → `photo` with an img-bank shot (or their photo).
   - Partner / sponsor → `partner` (ask for their logo file; mono white works best).
   - Speaker / athlete → `speaker` (needs a portrait photo from them).
   - Explainer / multi-point → carousel: `headline` cover → `form`/`body` slides → `headline`/`hero` close.
   - Big brand moment → `hero`.
   - Highlights → `highlight`, one form per highlight.
   Choose the glass form by meaning (MEET = lineup, SUPPORT = partners, SHARE = talks, COLLABORATE = team formats, ADAPT = recovery/workshops, FLOW = runs/journeys, CONNECT = community, COLLECT = full programme).
4. **Write the brief** to a working folder (e.g. `./psf-posts/<slug>.json`). Same copy in several formats → one brief per format.
5. **Render:** `python3 <skill>/scripts/make.py ./psf-posts/<slug>.json` (writes `.html` + `.png` next to `out`).
6. **Look at every PNG** (Read the image) and run the checklist below. Fix the brief and re-render until it passes. Never hand over a render you haven't looked at.
7. **Deliver:** the PNGs, the brief (so they can tweak copy and re-run), and a suggested caption if useful. Mention which bg/form you chose and why in one line.

## Checklist (run on every render)

- Headline is legible at phone size, doesn't collide with the logo, a glass form's brightest part, or the counter.
- Nothing is cut off at the edges (except glass forms, which are meant to bleed).
- One title face, one Sora line, at most one Micro accent. Max one highlighted word.
- Logo is present (except highlight covers and when a `hero` already shows it) and sits in a clear corner.
- Story: text clear of the top 250px and bottom 340px. Reel cover: headline inside the centre 1080×1440.
- Carousel: counter correct, consecutive slides don't reuse the same bg, last slide has the CTA/date.
- Copy is exactly what was supplied (spelling, names, dates), in ALL CAPS for titles and sentence case for paragraphs.

## Going off-template

The layouts cover the kit's applied examples. For anything else, generate the HTML with `--html`, edit it by hand (it's plain HTML/CSS with the brand fonts and assets already wired in), then `bash scripts/render.sh file.html`. Stay inside brand.md: black ground, glass forms bleeding from edges, white type, the four fonts, the six colours.

If the designer adds assets later (new bg, new photo), drop them into the matching `assets/` folder. Briefs can also point `bg`/`photo` at any file path.

## Requirements

Python 3 (preinstalled on macOS) and Google Chrome, Chromium, Edge or Playwright's Chromium (`npx playwright install chromium`). Set `CHROME=/path/to/chrome` if it's somewhere unusual. No other installs.
