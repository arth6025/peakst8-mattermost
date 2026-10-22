# Layouts and brief fields

Every post is a JSON brief rendered by `scripts/make.py`. Keys at the top level apply to all
slides; keys inside a slide override them. Worked briefs for every layout are in
`examples/briefs/`, with their output PNGs in `examples/renders/`.

## Formats

| `format` | Size | Notes |
|---|---|---|
| `post` (default) | 1080×1350 | Feed static and carousel slides (4:5). |
| `square` | 1080×1080 | Only when asked; feed is 4:5 now. |
| `story` | 1080×1920 | Keep text out of the top 250px and bottom 340px (IG UI). `"show_safe": true` draws the zones. |
| `reel-cover` | 1080×1920 | The profile grid crops to the centre 1080×1440. Keep the headline inside it. `show_safe` draws it. |
| `highlight` | 1080×1080 | Highlight cover. Shown as a circle, so keep content inside the centre ~75%. |

## Fields every layout accepts

| Field | Values | Default |
|---|---|---|
| `bg` | `bg1`…`bg8`, an img-bank name (partial ok: `"play-03"`, `"neon"`), a colour name (`black`, `core`), or a file path relative to the brief | per layout |
| `bg_pos` | CSS object-position, e.g. `"70% center"` (useful when a 4:5 bg is cropped into a story) | `center` |
| `logo` | `tl` `tr` `bl` `br` `center` `none` | per layout |
| `logo_colour` | `white` `bone` `black` | `white` |
| `date` | `true` (= "14 JANUARY 2027") or any string, shown under the logo | off |
| `elements` | list of extra glass forms: `{"form":"meet","x":70,"y":20,"size":60,"rotate":0,"opacity":1,"blur":0,"blend":"normal"}`. x/y are the centre in % of width/height; size is % of width. | none |
| `dust` | 0–0.4, scanned dust overlay | 0 (0.1–0.12 on photo layouts) |
| `grain` | 0–0.15, fine noise | 0.06 |
| `scrim` | 0–0.8, black gradient for legibility on photos | photo: 0.35 |
| `scrim_side` | `left` `right` `bottom` `top` | `left` |
| `counter` | `"auto"` for carousels (shows `2/6 >` bottom-right, hidden on the last slide) or a custom string | auto when >1 slide |
| `margin` | px at 1080 width | 64 |
| `show_safe` | draw story / reel / highlight safe zones (for checking only, never export with it) | false |

In any text field: `*word*` colours the word VITAL orange, `~word~` colours it BRISTLE lime, and `\n` forces a line break.

## `headline` — the workhorse (text_ann, text_ann2)

Boldonse headline on a glass bg. Auto-sized to fill the box.

| Field | Notes |
|---|---|
| `headline` | 2–6 words, ends with a full stop in the brand voice ("FIND YOUR FLOW.") |
| `sub` | optional Sora caps line under it |
| `chip` | optional Micro 5 accent ("MORE TO KNOW.", "SWIPE UP", "SAVE THE DATE") |
| `align` | `left` (default) or `center` |
| `valign` | `top` `center` (default) `bottom` |
| `left`, `width` | box position/width in px at 1080 width. Narrow width = more lines, stacked look |
| `top`, `bottom` | fraction of height kept clear above/below the box |
| `size` | max font size in px at 1080 (default 260; the fit shrinks it as needed) |
| `font` | `"anton"` to use the alternate title face |

Match bg to the free space (see the bg table in brand.md): bg1 → left-aligned, bg2 → `left: 300`, bg3/bg4 → centred.

## `photo` — full-bleed image + headline (experience1, experience2)

Same fields as `headline`, plus `photo` (img-bank name or path). Adds a left scrim and light dust by default.
Use for sport formats and experiences: "5 A SIDE FOOTBALL", "MIDNIGHT RUN RAVE.". Break long words with a hyphen across lines: `"MID-\nNIGHT RUN RAVE."`.

## `hero` — wordmark announcement (gen_ann, cover)

Centred logo and a Sora tagline. Fields: `tagline` (default "DISCOVER NEW WAYS TO MOVE."), `logo_size` (default 700), `tag_size`. Default bg `bg3`.

## `partner` — partner announcement (partner_ann)

| Field | Notes |
|---|---|
| `partner_logo` | path to the partner's logo (white/mono PNG or SVG works best on black) |
| `partner` | name typed in Anton italic if no logo file |
| `role` | "PERFORMANCE PARTNER", "OFFICIAL HYDRATION PARTNER" … |
| `partner_logo_width` | px at 1080 (default 620) |

Default bg `bg4`, festival logo top-left.

## `speaker` — speaker / athlete card (kit page 13)

| Field | Notes |
|---|---|
| `photo` | the person. Dramatic, dark, side-lit portrait works best |
| `first`, `last` | Anton. FIRST huge, LAST smaller underneath |
| `blurb` | 1–2 short lines, Sora caps |
| `side` | `left` (name bottom-left, logo top-right) or `right` (mirrored) |
| `last_size` | px at 1080 (default 92) |

Add a glass form over the photo the way the kit does: `"elements":[{"form":"share","x":20,"y":30,"size":95,"opacity":0.55,"blend":"screen","blur":6}]`.
Date under the logo is on by default.

## `form` — one glass form as hero

A form from the family, with its label and a headline. Use for pillars, experiences, explainer carousels.
Fields: `form` (meet, connect, collect, support, collaborate, adapt, share, flow), `label` (defaults to "05 / COLLABORATE"), `headline`, `body`, `form_size` (% width, default 78), `form_y` (% height, default 40), `rotate`.

## `body` — long-form carousel slide

Anton `title`, Sora sentence-case `body` (a string or a list of paragraphs), optional Micro `kicker`.
Black ground with one cropped form bottom-right (override with `elements` / `bg`). Keep it to ~45 words.

## `highlight` — highlight cover

`form` centred, optional short Micro `label` ("RUN", "TALKS", "FAQ"), `form_size`, `label_size`.
Make a matching set: one form per highlight, same size and position.

## Carousel recipe

1. Cover: `headline` on bg2 or bg1, hook headline (counter shows 1/N >).
2. Middle: `form` or `photo` slides, one idea each, or `body` for explanation.
3. Close: `headline` centred on bg3 with date + CTA in `sub`, or `hero`.

Keep 4–8 slides. Vary bg between consecutive slides (or use the "contact creates change" arc: 01 individual → 02 contact → 03 change).
