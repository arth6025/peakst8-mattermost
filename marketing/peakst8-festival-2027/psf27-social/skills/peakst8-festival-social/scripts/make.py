#!/usr/bin/env python3
"""peakst8 Festival 2027 post builder.

    python3 make.py brief.json            # writes HTML + PNG per slide
    python3 make.py brief.json --html     # HTML only (no render)

A brief is JSON. Top-level keys apply to every slide; each slide can override them.

{
  "format": "post",                 # post 1080x1350 | square 1080x1080 | story 1080x1920
                                    # | reel-cover 1080x1920 | highlight 1080x1080
  "out": "out/round-2",             # file prefix, relative to the brief. Carousels add -1, -2 ...
  "slides": [
    {"layout": "headline", "bg": "bg1", "headline": "WE'RE BACK FOR ROUND 2.", "chip": "MORE TO KNOW."}
  ]
}

Layouts: headline, photo, hero, partner, speaker, form, body, highlight.
See references/layouts.md for every field.
"""
import html, json, os, re, subprocess, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(SKILL, "assets")

FORMATS = {
    "post": (1080, 1350), "square": (1080, 1080), "story": (1080, 1920),
    "reel-cover": (1080, 1920), "highlight": (1080, 1080),
}
FORMS = {
    "meet": "01-meet", "connect": "02-connect", "collect": "03-collect", "support": "04-support",
    "collaborate": "05-collaborate", "adapt": "06-adapt", "share": "07-share", "flow": "08-flow",
}
COLOURS = {
    "grill": "#000000", "core": "#00386B", "vital": "#FF3200", "presence": "#FFE000",
    "bristle": "#E0FF00", "bone": "#FFFAE3", "black": "#000000",
}


def url(p):
    return "file://" + os.path.abspath(p).replace(" ", "%20")


def esc(s):
    return html.escape(str(s or ""))


def rich(s):
    """Escape, keep line breaks, and colour *words* in VITAL (or ~words~ in BRISTLE)."""
    s = esc(s).replace("\\n", "\n")
    s = re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', s)
    s = re.sub(r"~(.+?)~", r'<span class="hl2">\1</span>', s)
    return s.replace("\n", "<br>")


def resolve_image(v, base):
    """bg1..bg8, img-bank names (partial match ok), form names, or a file path."""
    if not v:
        return None
    if re.fullmatch(r"bg[1-8]", v):
        return url(os.path.join(A, "bg", v + ".jpg"))
    if v.lower() in FORMS:
        return url(os.path.join(A, "elements", FORMS[v.lower()] + ".png"))
    bank = os.path.join(A, "img-bank")
    for f in sorted(os.listdir(bank)):
        if v.lower().replace(" ", "-") in f:
            return url(os.path.join(bank, f))
    p = v if os.path.isabs(v) else os.path.join(base, os.path.expanduser(v))
    if not os.path.exists(p):
        sys.exit(f"Image not found: {v}")
    return url(p)


def fonts_css():
    f = os.path.join(A, "fonts")
    return f"""
@font-face{{font-family:Boldonse;src:url({url(f + '/Boldonse-Regular.ttf')})}}
@font-face{{font-family:Anton;src:url({url(f + '/Anton-Regular.ttf')})}}
@font-face{{font-family:Micro;src:url({url(f + '/Micro5Charted-Regular.ttf')})}}
@font-face{{font-family:Sora;src:url({url(f + '/Sora-Variable.ttf')});font-weight:100 800}}
"""


BASE_CSS = """
:root{--grill:#000;--core:#00386B;--vital:#FF3200;--presence:#FFE000;--bristle:#E0FF00;--bone:#FFFAE3}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:var(--W);height:var(--H);overflow:hidden;background:#000}
.c{position:relative;width:var(--W);height:var(--H);overflow:hidden;background:var(--ground,#000);color:var(--ink,#fff)}
.layer{position:absolute;inset:0}
.bgimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dust{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:screen;pointer-events:none}
.grain{position:absolute;inset:0;pointer-events:none;mix-blend-mode:overlay}
.logo{position:absolute;width:calc(var(--u)*250)}
.logo img{width:100%;display:block}
.logo .date{font:600 calc(var(--u)*21)/1 Sora;letter-spacing:.14em;text-align:center;margin-top:calc(var(--u)*10);white-space:nowrap}
.logo.tl{left:var(--m);top:var(--mt)} .logo.tr{right:var(--m);top:var(--mt)}
.logo.bl{left:var(--m);bottom:var(--m)} .logo.br{right:var(--m);bottom:var(--m)}
.box{position:absolute;display:flex;flex-direction:column}
.hd{font-family:Boldonse;text-transform:uppercase;line-height:1.3;letter-spacing:0;width:100%}
.hd.anton{font-family:Anton;line-height:1.0;letter-spacing:0;padding-top:0}
.hl{color:var(--vital)} .hl2{color:var(--bristle)}
.sub{font:600 calc(var(--u)*26)/1.25 Sora;letter-spacing:.06em;text-transform:uppercase}
.para{font:600 calc(var(--u)*34)/1.3 Sora}
.chip{font:calc(var(--u)*54)/1 Micro;display:inline-block;background:#000;padding:calc(var(--u)*2) calc(var(--u)*6);align-self:flex-start}
.counter{position:absolute;font:calc(var(--u)*40)/1 Micro;background:#000;padding:calc(var(--u)*2) calc(var(--u)*6)}
.rule{position:absolute;width:2px;background:var(--ink,#fff);opacity:.85}
.el{position:absolute;pointer-events:none}
"""

FIT_JS = """
<script>
// Shrink every .fit until it fits its box (no clipped words, no overflow).
function fit(){document.querySelectorAll('.fit').forEach(el=>{
  const box=el.parentElement; let s=parseFloat(el.dataset.max), min=parseFloat(el.dataset.min||20);
  el.style.fontSize=s+'px';
  // Sum the children's real heights: scrollHeight ignores overflow when the box is flex-end aligned.
  const used=()=>[...box.children].reduce((a,c)=>{const cs=getComputedStyle(c);
    return a+c.getBoundingClientRect().height+parseFloat(cs.marginTop)+parseFloat(cs.marginBottom)},0);
  const over=()=>el.scrollWidth>el.clientWidth+1||used()>box.clientHeight+1;
  while(over()&&s>min){s-=2;el.style.fontSize=s+'px'}
});}
document.fonts.ready.then(()=>{fit();document.body.dataset.ready=1});
</script>
"""


def grain_svg(op):
    if not op:
        return ""
    return (f'<svg class="grain" style="opacity:{op}" width="100%" height="100%"><filter id="n">'
            '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
            '<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 .9 0"/></filter>'
            '<rect width="100%" height="100%" filter="url(#n)"/></svg>')


def logo_html(s, W, H, default="tr"):
    pos = s.get("logo", default)
    if pos in (None, False, "none"):
        return ""
    colour = "black" if s.get("light") else s.get("logo_colour", "white")
    date = s.get("date")
    if date is True:
        date = "30 JANUARY 2027"
    d = f'<div class="date">{esc(date)}</div>' if date else ""
    style = ""
    if pos == "center":
        style = f'style="left:50%;top:50%;transform:translate(-50%,-50%);width:calc(var(--u)*{s.get("logo_size", 760)})"'
        pos = ""
    return f'<div class="logo {pos}" {style}><img src="{url(os.path.join(A, "logo", f"psf_{colour}.svg"))}">{d}</div>'


def element_html(s, base):
    """Extra glass forms: [{"form":"meet","x":70,"y":-10,"size":60,"rotate":20,"blur":0,"opacity":1}]
    x/y/size are % of canvas width (y is % of canvas height)."""
    out = []
    for e in s.get("elements", []):
        src = resolve_image(e["form"], base)
        st = (f'left:{e.get("x", 50)}%;top:{e.get("y", 50)}%;width:{e.get("size", 50)}%;'
              f'transform:translate(-50%,-50%) rotate({e.get("rotate", 0)}deg);'
              f'opacity:{e.get("opacity", 1)};filter:blur({e.get("blur", 0)}px);'
              f'mix-blend-mode:{e.get("blend", "normal")}')
        out.append(f'<img class="el" src="{src}" style="{st}">')
    return "".join(out)


def ground(s, base, W, H, default_bg=None):
    bg = s.get("bg", default_bg)
    pos = s.get("bg_pos", "center")
    layers = ""
    g = COLOURS.get(str(bg).lower()) if bg else None
    if bg and not g:
        layers += f'<img class="bgimg" src="{resolve_image(bg, base)}" style="object-position:{pos}">'
    if s.get("scrim"):
        side = s.get("scrim_side", "left")
        layers += (f'<div class="layer" style="background:linear-gradient(to {"right" if side == "left" else "left" if side == "right" else "top" if side == "bottom" else "bottom"},'
                   f'rgba(0,0,0,{s["scrim"]}) 0%,rgba(0,0,0,0) 70%)"></div>')
    return g or "#000", layers


def finish(s):
    dust = s.get("dust", 0)
    d = (f'<img class="dust" src="{url(os.path.join(A, "textures", "dust-dark.jpg"))}" style="opacity:{dust}">'
         if dust else "")
    return d + grain_svg(s.get("grain", 0.06))


# ---------- layouts ----------

def L_headline(s, base, W, H, u, m):
    """Big Boldonse headline on a glass background. text_ann / text_ann2 / experience*."""
    align = s.get("align", "left")
    font = "anton" if s.get("font") == "anton" else ""
    # nowrap: break lines only where the brief puts \n, shrinking the type instead of wrapping (dates, numbers)
    nowrap = ' style="white-space:nowrap"' if s.get("nowrap") else ""
    top = s.get("top", 0.25 if H > W * 1.4 else 0.12)  # clear the logo; stories keep top 250px free
    bottom = s.get("bottom", 0.24 if H > W * 1.4 else 0.16)
    left = s.get("left", m / u)
    width = s.get("width", 760 if align == "left" else 860)
    x = f"left:{left * u}px" if align == "left" else f"left:{(W - width * u) / 2}px"
    max_px = s.get("size", 260) * u
    chip = f'<div class="chip" style="margin-top:{36 * u}px">{esc(s["chip"])}</div>' if s.get("chip") else ""
    sub = f'<div class="sub" style="margin-top:{28 * u}px">{rich(s["sub"])}</div>' if s.get("sub") else ""
    just = {"top": "flex-start", "center": "center", "bottom": "flex-end"}[s.get("valign", "center")]
    ta = "center" if align == "center" else "left"
    return f"""
<div class="box" style="{x};top:{top * H}px;width:{width * u}px;height:{H * (1 - top - bottom)}px;justify-content:{just};text-align:{ta};align-items:{'center' if ta == 'center' else 'flex-start'}">
  <div class="hd fit {font}"{nowrap} data-max="{max_px}" data-min="{60 * u}">{rich(s.get("headline", ""))}</div>
  {sub}{chip}
</div>"""


def L_photo(s, base, W, H, u, m):
    """Full-bleed img-bank photo + headline. 5 A SIDE FOOTBALL / MIDNIGHT RUN RAVE."""
    s.setdefault("bg", s.get("photo", "play-03"))
    s.setdefault("dust", 0.12)
    s.setdefault("scrim", 0.35)
    return L_headline(s, base, W, H, u, m)


def L_hero(s, base, W, H, u, m):
    """Centred wordmark + Sora tagline. gen_ann / cover."""
    tag = s.get("tagline", "DISCOVER NEW WAYS TO MOVE.")
    size = s.get("logo_size", 700)
    ty = H / 2 + size * u * 0.36 / 2 + 40 * u
    return f"""
<div class="logo" style="left:50%;top:50%;transform:translate(-50%,-58%);width:{size * u}px">
  <img src="{url(os.path.join(A, 'logo', 'psf_' + s.get('logo_colour', 'white') + '.svg'))}"></div>
<div class="sub" style="position:absolute;left:0;right:0;top:{ty}px;text-align:center;font-size:{s.get('tag_size', 30) * u}px">{rich(tag)}</div>"""


def L_partner(s, base, W, H, u, m):
    """Partner announcement. partner_ann (ULTRAHUMAN / PERFORMANCE PARTNER)."""
    inner = ""
    if s.get("partner_logo"):
        inner = f'<img src="{resolve_image(s["partner_logo"], base)}" style="max-width:{s.get("partner_logo_width", 620) * u}px;max-height:{260 * u}px">'
    else:
        inner = f'<div class="hd fit anton" data-max="{150 * u}" data-min="{60 * u}" style="text-align:center;font-style:italic">{rich(s.get("partner", "PARTNER"))}</div>'
    return f"""
<div class="box" style="left:{m}px;right:{m}px;top:{H * .36}px;height:{H * .3}px;align-items:center;justify-content:center;text-align:center">
  {inner}
  <div class="sub" style="margin-top:{56 * u}px;font-size:{28 * u}px">{rich(s.get("role", "OFFICIAL PARTNER"))}</div>
</div>"""


def L_speaker(s, base, W, H, u, m):
    """Speaker / athlete card. FIRST over LAST in Anton, blurb in Sora caps, thin rules."""
    side = s.get("side", "left")
    s.setdefault("bg", s.get("photo", "cinematic-blue-orange"))
    s.setdefault("bg_pos", "70% 30%" if side == "left" else "30% 30%")
    s.setdefault("logo", "tr" if side == "left" else "tl")
    s.setdefault("date", True)
    s.setdefault("dust", 0.1)
    s.setdefault("scrim", 0.55)
    s.setdefault("scrim_side", "bottom")
    al = "left" if side == "left" else "right"
    xs = f"left:{m}px" if side == "left" else f"right:{m}px"
    blurb_x = f"right:{m * 2.3}px" if side == "left" else f"left:{m * 2.3}px"
    blurb_y = H * (0.2 if side == "left" else 0.62)
    rule_a = f"left:{m * .6}px;top:{H * .07}px;height:{H * .55}px" if side == "left" else f"right:{m * .6}px;top:{H * .07}px;height:{H * .55}px"
    rule_b = f"right:{m * .9}px;top:{H * .38}px;height:{H * .3}px" if side == "left" else f"left:{m * .9}px;top:{H * .4}px;height:{H * .3}px"
    return f"""
<div class="rule" style="{rule_a}"></div><div class="rule" style="{rule_b}"></div>
<div class="sub" style="position:absolute;{blurb_x};top:{blurb_y}px;width:{430 * u}px;text-align:left;font-size:{28 * u}px">{rich(s.get("blurb", ""))}</div>
<div class="box" style="{xs};bottom:{H * .07}px;width:{W * .62}px;height:{H * .33}px;justify-content:flex-end;align-items:{'flex-start' if al == 'left' else 'flex-end'};text-align:{al}">
  <div class="hd fit anton" data-max="{230 * u}" data-min="{80 * u}">{rich(s.get("first", "FIRST"))}</div>
  <div class="hd anton" style="font-size:{s.get('last_size', 92) * u}px;margin-top:{6 * u}px">{rich(s.get("last", "LAST"))}</div>
</div>"""


def L_form(s, base, W, H, u, m):
    """One glass form as hero + label + headline. For pillars, experiences, explainers."""
    form = s.get("form", "meet")
    num = FORMS.get(form, "00-x")[:2]
    label = s.get("label", f"{num} / {form.upper()}")
    size = s.get("form_size", 78)
    fy = s.get("form_y", 40)
    return f"""
<img class="el" src="{resolve_image(form, base)}" style="left:50%;top:{fy}%;width:{size}%;transform:translate(-50%,-50%) rotate({s.get('rotate', 0)}deg)">
<div class="box" style="left:{m}px;right:{m}px;bottom:{H * .08}px;height:{H * .3}px;justify-content:flex-end">
  <div class="chip" style="margin-bottom:{24 * u}px">{esc(label)}</div>
  <div class="hd fit" data-max="{s.get('size', 120) * u}" data-min="{50 * u}">{rich(s.get("headline", ""))}</div>
  {f'<div class="para" style="margin-top:{18 * u}px;font-size:{30 * u}px;opacity:.9">{rich(s["body"])}</div>' if s.get("body") else ""}
</div>"""


def L_body(s, base, W, H, u, m):
    """Long-form carousel slide: Anton title, Sora sentence-case paragraphs, Micro kicker."""
    # Reading slides need calm space: black ground, one cropped form in a corner (kit "B. Crop").
    s.setdefault("bg", "black")
    if "elements" not in s:
        s["elements"] = [{"form": s.get("form", "meet"), "x": 92, "y": 90, "size": 55, "rotate": -15}]
    kicker = f'<div class="chip" style="margin-bottom:{30 * u}px">{esc(s["kicker"])}</div>' if s.get("kicker") else ""
    paras = s.get("body", "")
    if isinstance(paras, str):
        paras = [paras]
    body = "".join(f'<p class="para" style="margin-top:{22 * u}px">{rich(p)}</p>' for p in paras)
    top = 0.27 if H > W * 1.4 else 0.17
    return f"""
<div class="box" style="left:{m}px;width:{W - 2 * m - 80 * u}px;top:{H * top}px;height:{H * (0.92 - top)}px;justify-content:center">
  {kicker}
  <div class="hd fit anton" data-max="{s.get('size', 120) * u}" data-min="{56 * u}">{rich(s.get("title", ""))}</div>
  {body}
</div>"""


def L_highlight(s, base, W, H, u, m):
    """Instagram highlight cover: one form, centred, inside the circle-safe zone, tiny Micro label."""
    form = s.get("form", "meet")
    label = s.get("label", "")
    lab = (f'<div style="position:absolute;left:0;right:0;top:{H * .72}px;text-align:center">'
           f'<span class="chip" style="font-size:{s.get("label_size", 120) * u}px">{esc(label)}</span></div>') if label else ""
    return f"""
<img class="el" src="{resolve_image(form, base)}" style="left:50%;top:{46 if label else 50}%;width:{s.get('form_size', 70)}%;transform:translate(-50%,-50%)">{lab}"""


LAYOUTS = {"headline": L_headline, "photo": L_photo, "hero": L_hero, "partner": L_partner,
           "speaker": L_speaker, "form": L_form, "body": L_body, "highlight": L_highlight}
DEFAULT_BG = {"headline": "bg1", "hero": "bg3", "partner": "bg4", "form": None, "highlight": None}
DEFAULT_LOGO = {"headline": "tr", "photo": "tr", "hero": "none", "partner": "tl", "speaker": "tr",
                "form": "tl", "body": "tl", "highlight": "none"}


def build_slide(s, base, i, n):
    fmt = s.get("format", "post")
    W, H = FORMATS[fmt]
    u = W / 1080
    m = s.get("margin", 64) * u
    layout = s.get("layout", "headline")
    if layout not in LAYOUTS:
        sys.exit(f"Unknown layout '{layout}'. Use one of: {', '.join(LAYOUTS)}")
    content = LAYOUTS[layout](s, base, W, H, u, m)  # may set defaults on s
    gcol, glayers = ground(s, base, W, H, DEFAULT_BG.get(layout))
    logo = logo_html(s, W, H, DEFAULT_LOGO[layout])
    counter = ""
    c = s.get("counter", "auto" if n > 1 else None)
    if c:
        text = f"{i}/{n} >" if c == "auto" else c
        if not (c == "auto" and i == n):
            counter = f'<div class="counter" style="right:{m}px;bottom:{m}px">{esc(text)}</div>'
    safe = ""
    if s.get("show_safe"):
        if fmt == "story":
            safe = (f'<div class="layer" style="border-top:{250 * u}px solid rgba(255,0,255,.25);'
                    f'border-bottom:{340 * u}px solid rgba(255,0,255,.25)"></div>')
        if fmt == "reel-cover":
            safe = f'<div class="layer" style="top:{(H - 1440 * u) / 2}px;bottom:{(H - 1440 * u) / 2}px;outline:4px dashed #f0f"></div>'
        if fmt == "highlight":
            safe = '<div class="layer" style="border-radius:50%;outline:4px dashed #f0f;inset:12%"></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{esc(s.get('name', layout))}</title>
<style>{fonts_css()}{BASE_CSS}:root{{--W:{W}px;--H:{H}px;--u:{u}px;--m:{m}px;--mt:{(260 * u) if H > W * 1.5 else m}px}}</style></head>
<body data-w="{W}" data-h="{H}"><div class="c" style="--ground:{gcol}">
{glayers}{element_html(s, base)}{finish(s)}{content}{logo}{counter}{safe}
</div>{FIT_JS}</body></html>"""


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    brief_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(brief_path)
    brief = json.load(open(brief_path))
    slides = brief.get("slides") or [{}]
    top = {k: v for k, v in brief.items() if k != "slides"}
    out = os.path.join(base, brief.get("out", os.path.splitext(os.path.basename(brief_path))[0]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = len(slides)
    render = os.path.join(SKILL, "scripts", "render.sh")
    for i, sl in enumerate(slides, 1):
        s = {**top, **sl}
        name = f"{out}-{i}" if n > 1 else out
        page = build_slide(s, base, i, n)
        open(name + ".html", "w").write(page)
        if "--html" in sys.argv:
            print(name + ".html")
            continue
        subprocess.run(["bash", render, name + ".html", name + ".png"], check=True)


if __name__ == "__main__":
    main()
