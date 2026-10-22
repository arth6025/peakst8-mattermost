# peakst8 Festival 2027 — brand system

Source: `PSF27_Branding.pdf` (Visual Identity Exploration V2), Drive folder
"🎨 Design Assets_Peakst8 Festival'2027". When this file and the PDF disagree, the PDF wins.

## The idea

Three festival themes: **discovery, active participation, shared effort.** Visually:

| Principle | Line from the kit | What it means on a post |
|---|---|---|
| INTERACTION | Forms respond to one another. | Elements lean toward, touch or answer each other. Nothing floats alone. |
| OVERLAP | Individual forms create shared space. | Shapes, photos and type overlap. Overlap is where the interest is. |
| BLENDING | Colour and imagery shift where they meet. | Where two colours/forms meet, a third colour appears (glass refraction, gradient). |

Two graphic devices:

1. **Soft intersections + colour blends.** Rounded forms create shared space; colour gathers where they meet.
2. **Optical distortion + surface tension.** Refraction (glass, water, lens) brings blending into focus. Participation gives the image energy.

"Contact creates change": 01 Individual (independent energies) → 02 Contact (a shared space takes shape) → 03 Change (colour shifts at the intersection). Use this as a 3-slide carousel arc or a reveal sequence.

## Family of forms (the glass "gradient elements")

Eight forms, one per way people come together. Each is a PNG in `assets/elements/`.
Pick the form whose meaning matches the post.

| # | Form | Meaning | Use for |
|---|---|---|---|
| 01 | MEET | Collaboration | Lineup / "who's coming", partner intros |
| 02 | CONNECT | Different paths, shared space | Community, multi-sport, "find your people" |
| 03 | COLLECT | Many forms, one ecosystem | Full-programme / schedule / "everything at the fest" |
| 04 | SUPPORT | One lifts, the other flows | Partner / sponsor announcements, coaches |
| 05 | COLLABORATE | Individual strength, collective impact | Team formats (5-a-side, relays), challenges |
| 06 | ADAPT | Forms shift and respond | Workshops, recovery, training, mindset |
| 07 | SHARE | Exchange and openness | Talks, panels, speaker announcements |
| 08 | FLOW | Continuity and shared direction | Run clubs, journeys, "find your flow", countdowns |

## Colour

The palette stays familiar. **Its intersections create the variation.**

| Name | Hex | Role |
|---|---|---|
| GRILL | `#000000` | Black. Type on light, deepest shadows. |
| CORE | `#00386B` | Deep navy. Default ground. Depth. |
| VITAL | `#FF3200` | Signal orange-red. Energy, the point of contact. |
| PRESENCE | `#FFE000` | Warm yellow. Warmth, shared energy. |
| BRISTLE | `#E0FF00` | Acid lime. Sharp accent, use sparingly. |
| BONE | `#FFFAE3` | Off-white. Default type on dark; light ground. |

Approved pairings (from the kit):

- **CORE + VITAL** — "Depth with a point of contact." The hero pairing. Navy ground, orange where things meet.
- **VITAL + PRESENCE** — "Warmth and shared energy." Hot, celebratory posts.
- **CORE + BRISTLE** — "A precise moment of contrast." Data, numbers, countdowns, one punchy word.

Rules:
- **Default ground is GRILL black.** Every applied post in the kit sits on black with glass forms bleeding in from the edges, or on a full-bleed photo. CORE navy appears inside the forms and photos, not as a flat fill.
- **Type is white** on dark (that is what the designer's posts use). BONE is fine for a softer, print-like feel. On light grounds use GRILL.
- Accent a single word in VITAL (`*word*` in a brief). BRISTLE (`~word~`) only on black, never on BONE.
- Max two brand colours dominant per frame. The blend between them is the third colour, never a new hex.
- Photography carries its own colour but must read blue/orange (see `assets/img-bank`).

## Type

From the kit's FONTS page:

| Font | Role | Case | In the examples |
|---|---|---|---|
| **Boldonse** Regular | PRIMARY, for titles | ALL CAPS | WE'RE BACK FOR ROUND 2. / FIND YOUR FLOW. / 5 A SIDE FOOTBALL. Condensed, circular O. Caps are taller than the em, so leading ≈ 1.3 (the builder handles it). |
| **Anton** Regular | ALTERNATE title font | ALL CAPS | Speaker names (ANDREW / HUBERMAN), badge words (AAA, ATHLETE), partner names. |
| **Sora** SemiBold | Long-form content | CAPS for short lines; **sentence case for paragraphs** | "DISCOVER NEW WAYS TO MOVE.", "PERFORMANCE PARTNER", "30 JANUARY 2027", speaker blurbs, body slides. |
| **Micro 5 Charted** | Fun typography / type accents | Any | "MORE TO KNOW." chip, "1/6 >" counter, form labels. Dot-matrix grid look. Small doses. |

Hierarchy: one Boldonse (or Anton) title → one Sora line → at most one Micro accent. Never all four on one frame.

## Logo

`assets/logo/psf_white.svg` (default, on dark), `psf_bone.svg`, `psf_black.svg` (on light).
Lockup is the stacked "peakst8 / FESTIVAL" wordmark with the 8-glyph.

- Corner position on posts: top-right (headline posts) or top-left (partner, carousel), ~23% of canvas width.
- Optional date line under it: "30 JANUARY 2027" in Sora SemiBold, wide tracking (speaker cards, billboard).
- Hero use: centred, ~65% width, with a Sora tagline under it (cover, general announcement).
- Clear space: at least the height of the "8" glyph on all sides.
- Never recolour outside GRILL / BONE. Never stretch, outline, or put on a busy part of a photo without a scrim.

## Application of design (kit page "Application of design")

Each form can be adapted, cropped, blurred, layered or combined with imagery:

| Move | Kit line | Builder field |
|---|---|---|
| A. Close up | Zoom into intersection points. | `elements: [{size: 180, ...}]` (bigger than the canvas) |
| B. Crop | Use partial forms for dynamic layouts. | `x`/`y` near or past the edge (e.g. `x: 95, y: 90`) |
| C. Layer | Build depth with transparency. | `opacity: .5`, two forms overlapping |
| D. Blur | Introduce softness at contact points. | `blur: 20` |
| E. Combine | Create new forms through layering. | two or three `elements` with `blend: "screen"` |

## Textures & elements

- **Detailed close-ups.** Macro shots of textures, themed 01 Endurance, 03 Movement, 04 Recovery, 06 Play, 07 Mindset. In `assets/img-bank/` (play-01..05 nets and cords, rain basketball, neon sprinter, cobalt grid, wet shoulder).
- **Dust and dither.** Scanned grain (`assets/textures/dust-dark.jpg`, `dust-light.jpg`) as overlays, varied blending. Builder: `dust: 0.1–0.3` (screen), `grain: 0–0.15` (SVG noise, default 0.06).
- **Glass forms** from the family above, often overlapping photos or each other, so the overlap shows refraction.

## Plain backgrounds (`assets/bg/bg1–8`, 4:5, forms already composed on black)

| bg | What's on it | Free space for type | Used in kit for |
|---|---|---|---|
| bg1 | Small form top-left, big glass pills bottom-right | Left two-thirds, top to 70% | WE'RE BACK FOR ROUND 2. |
| bg2 | Pills top-right + right edge, pill bottom-left | Centre | FIND YOUR FLOW. (carousel cover) |
| bg3 | Disc arcs top and bottom | Middle band | General announcement / cover |
| bg4 | Disc top-right, discs bottom | Middle band, left | Partner announcement |
| bg5 | Huge orange arch, top-right | Bottom-left | Bold single word / number |
| bg6 | Blue/orange arches, full frame | Little: use with a short word or scrim | Texture slide, transitions |
| bg7 | Lime top-left, big blue disc right | Left half | Night / run / cool-tone posts |
| bg8 | Flow ribbons top and bottom-left | Middle-right | Flow / journey posts |

## Recurring copy patterns from the kit's applied examples

- Brand line: **FIND YOUR FLOW.**
- Date lockup: **30 JANUARY 2027** (the kit's mock-ups show 14 January, a placeholder) (Micro 5 Charted or Sora, small, near logo).
- Return message: **WE'RE BACK FOR ROUND 2.**
- Hook / CTA: **MORE TO KNOW.**
- Partner card: partner name big + role line ("PERFORMANCE PARTNER").
- Speaker card: FIRST name over LAST name, stacked, big; one Anton line of description.
- Format card: sport name in Boldonse stacked over 2–4 lines ("5 A SIDE / FOOT- / BALL").
- Carousel counter: "1/6" top-right in Micro 5 Charted.
