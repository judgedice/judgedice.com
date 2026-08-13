# -*- coding: utf-8 -*-
"""Judge Swath: a full-bleed dark band with a fractal-edged olo swath + text.

Reusable editor snippet (Judge palette group) plus one instance on the homepage.

The swath edge is fractal Brownian motion (multi-octave value noise): each
octave halves the amplitude and doubles the frequency, so big torn lobes carry
medium notches carrying fine serrations — self-similar at every scale. Geometry
is computed deterministically at build time (hash-based noise, no RNG), so
re-running produces byte-identical output and the script stays idempotent.

"Olo" is the blue-green Berkeley produced in 2025 by laser-stimulating M cones;
it is outside the sRGB gamut, so #00FFCC is the standard screen stand-in.

Idempotent; dry-run by default, pass --apply.
"""
import sys, os, math, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE, HOME_VIEW, PALETTE_VIEW = 2, 2034, 2271
SNIPPET_KEY = "website.s_jd_swath"
CSS_SENTINEL = ".s_jd_swath_wrapper{"
HOME_SENTINEL = "jd-swath-home"

OLO = "#00FFCC"
DARK = "#131A18"

W, H = 600, 520
MARGIN = 46          # room for the ragged edge to wander
OCTAVES = 7          # fractal depth: 7 octaves ≈ detail from ~250px down to ~4px


# ---------------------------------------------------------------- fractal noise
def _hash(i):
    """Deterministic pseudo-random in [-1, 1] from an integer lattice point."""
    x = math.sin(i * 127.1 + 311.7) * 43758.5453123
    return 2.0 * (x - math.floor(x)) - 1.0


def _vnoise(t):
    """1-D value noise with smoothstep interpolation."""
    i = math.floor(t)
    f = t - i
    u = f * f * (3.0 - 2.0 * f)
    return _hash(i) * (1.0 - u) + _hash(i + 1) * u


def fbm(t, octaves=OCTAVES, persistence=0.5, lacunarity=2.0):
    """Fractal Brownian motion — the self-similarity that reads as 'fractal'."""
    amp, freq, total, norm = 1.0, 1.0, 0.0, 0.0
    for _ in range(octaves):
        total += amp * _vnoise(t * freq)
        norm += amp
        amp *= persistence
        freq *= lacunarity
    return total / norm


# ---------------------------------------------------------------- swath geometry
# Midpoint displacement (the classic fractal-coastline construction): repeatedly
# split each span and offset its midpoint by a shrinking random amount. Because
# the offset shrinks by 2^-H per level, the roughness is statistically identical
# at every zoom level — that self-similarity is what reads as "fractal", and the
# sharp corners it leaves at every scale are what smooth noise fails to give.
LEVELS = 8          # 2^8 = 256 segments per edge
ROUGHNESS = 0.56    # H: lower = jaggeder (0.5 ≈ Brownian, 1.0 ≈ smooth)

# (seed, base amplitude) per edge
EDGES = {"top": (11, 34.0), "right": (57, 42.0), "bottom": (91, 37.0), "left": (23, 39.0)}


def _displacements(seed, amp0):
    n = 1 << LEVELS
    d = [0.0] * (n + 1)
    # corners drift a little too, so the swath has torn corners, not clipped ones
    d[0] = amp0 * 0.3 * _hash(seed * 13 + 1)
    d[n] = amp0 * 0.3 * _hash(seed * 13 + 2)
    step, amp, level = n, amp0, 0
    while step > 1:
        half = step >> 1
        for i in range(half, n, step):
            avg = 0.5 * (d[i - half] + d[i + half])
            d[i] = avg + amp * _hash(seed * 7919 + level * 131 + i)
        step = half
        amp *= 2.0 ** (-ROUGHNESS)
        level += 1
    return d


def _edge(kind, x0, y0, x1, y1):
    seed, amp0 = EDGES[kind]
    d = _displacements(seed, amp0)
    n = len(d) - 1
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        off = d[i]
        if kind == "top":
            y -= off
        elif kind == "bottom":
            y += off
        elif kind == "left":
            x -= off
        else:
            x += off
        pts.append((x, y))
    return pts


def _poly(pts):
    """L-segments: at this density they read sharper than curves — which is
    exactly right for a torn edge — and cost about half the characters."""
    d = "M%.1f %.1f" % pts[0]
    for p in pts[1:]:
        d += "L%.1f %.1f" % p
    return d + "Z"


def swath_path():
    return _poly(_edge("top", MARGIN, MARGIN, W - MARGIN, MARGIN)
                 + _edge("right", W - MARGIN, MARGIN, W - MARGIN, H - MARGIN)
                 + _edge("bottom", W - MARGIN, H - MARGIN, MARGIN, H - MARGIN)
                 + _edge("left", MARGIN, H - MARGIN, MARGIN, MARGIN))


def fleck_paths(count=18):
    """Detached spatter — the same construction at a much smaller scale."""
    out = []
    for k in range(count):
        a, b, c = _hash(k * 3 + 1), _hash(k * 7 + 5), _hash(k * 11 + 9)
        side = k % 4
        t = 0.5 + 0.45 * a
        if side == 0:
            cx, cy = MARGIN + (W - 2 * MARGIN) * t, MARGIN - 16 - 20 * abs(b)
        elif side == 1:
            cx, cy = W - MARGIN + 14 + 22 * abs(b), MARGIN + (H - 2 * MARGIN) * t
        elif side == 2:
            cx, cy = MARGIN + (W - 2 * MARGIN) * t, H - MARGIN + 15 + 21 * abs(b)
        else:
            cx, cy = MARGIN - 15 - 21 * abs(b), MARGIN + (H - 2 * MARGIN) * t
        r = 1.8 + 4.4 * abs(c)
        pts = []
        for j in range(11):
            ang = 2 * math.pi * j / 11.0
            rr = r * (0.5 + 0.5 * abs(_hash(k * 17 + j)))
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        out.append(_poly(pts))
    return out


# keep streaks clear of the torn edge: the boundary can wander inward by roughly
# the edge amplitude, so inset by more than that rather than clipping (a clip path
# would mean carrying the 11 KB swath outline twice)
STREAK_INSET = 62


def streak_path(y, amp, freq, phase, thick, n=64):
    """Dry-brush drag across the swath."""
    top, bot = [], []
    x0 = MARGIN + STREAK_INSET
    span = W - 2 * (MARGIN + STREAK_INSET)
    for i in range(n + 1):
        t = i / float(n)
        x = x0 + span * t
        wob = amp * fbm(t * freq + phase)
        th = thick * (0.35 + 0.65 * math.sin(math.pi * t) ** 0.7)
        top.append((x, y + wob - th / 2))
        bot.append((x, y + wob + th / 2))
    return _poly(top + list(reversed(bot)))


STREAKS = [(150, 10, 4.2, 2.5, 13), (286, 13, 3.4, 8.1, 18), (404, 9, 5.0, 14.9, 11)]


# ---------------------------------------------------------------- markup
def svg_markup():
    flecks = "".join('<path class="s_jd_swath_fleck" d="%s"/>' % d for d in fleck_paths())
    streaks = "".join('<path class="s_jd_swath_streak s_jd_swath_streak_%d" d="%s"/>'
                      % (i, streak_path(*s)) for i, s in enumerate(STREAKS))
    return ('<div class="s_jd_swath_media o_not_editable" contenteditable="false" '
            'aria-hidden="true">'
            '<svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="presentation" '
            'focusable="false">'
            '<path class="s_jd_swath_shape" d="%s"/>%s%s'
            '</svg></div>' % (W, H, swath_path(), streaks, flecks))


COPY_HEAD = "Words that hold a room."
COPY_BODY = ("A tribute is not a r&#233;sum&#233; read aloud. It is the one story that explains a "
             "person &#8212; found in a conversation, and shaped so whoever has to stand up "
             "sounds like themselves.")


def section(extra_class=""):
    return (
        '<section class="s_jd_swath_wrapper %s" data-snippet="s_jd_swath" '
        'data-name="Judge Swath">'
        '<div class="s_jd_swath_inner">'
        '%s'
        '<div class="s_jd_swath_copy">'
        '<div class="s_jd_swath_label"><span>The work</span>'
        '<span class="s_jd_swath_rule"/></div>'
        '<h2>%s</h2><p>%s</p>'
        '<a class="s_jd_swath_cta" href="/offerings">See what I write &#8594;</a>'
        '</div></div></section>' % (extra_class, svg_markup(), COPY_HEAD, COPY_BODY)
    )


CSS = '''
/* ---- Judge swath (dark band + olo) ---- */
.s_jd_swath_wrapper{--jd-olo:%(olo)s;--jd-dark:%(dark)s;background:var(--jd-dark);padding:clamp(3.5rem,8vw,6.5rem) clamp(1.5rem,6vw,6rem);}
.s_jd_swath_inner{max-width:72rem;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(1.75rem,5vw,4rem);align-items:center;}
.s_jd_swath_media svg{display:block;width:100%%;height:auto;}
.s_jd_swath_shape{fill:var(--jd-olo,%(olo)s);}
.s_jd_swath_fleck{fill:var(--jd-olo,%(olo)s);opacity:.8;}
.s_jd_swath_streak{fill:#fff;opacity:.14;}
.s_jd_swath_streak_1{fill:#000;opacity:.10;}
.s_jd_swath_label{display:flex;align-items:center;gap:14px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:var(--jd-olo,%(olo)s);margin-bottom:18px;}
.s_jd_swath_rule{flex:1;height:1px;background:var(--jd-olo,%(olo)s);opacity:.35;min-width:24px;}
.s_jd_swath_copy h2{font-family:var(--font-display);font-weight:var(--weight-regular);text-transform:uppercase;font-size:clamp(1.75rem,4.5vw,3.25rem);line-height:1.04;letter-spacing:-0.005em;color:var(--paper);margin:0;max-width:16ch;}
.s_jd_swath_copy p{font-family:var(--font-serif);font-size:1.0625rem;line-height:1.6;color:#C9BEAF;margin:16px 0 0;max-width:44ch;}
.s_jd_swath_cta{display:inline-block;margin-top:24px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:var(--paper);text-decoration:none;border-bottom:1px solid var(--jd-olo,%(olo)s);padding-bottom:3px;}
.s_jd_swath_cta:hover{color:var(--jd-olo,%(olo)s);}
@media (max-width:820px){.s_jd_swath_inner{grid-template-columns:1fr;}}
''' % {"olo": OLO, "dark": DARK}


def main(apply_):
    uid, call = connect()
    print("add_swath_block [%s]" % ("APPLY" if apply_ else "dry-run"))

    snippet_arch = ('<t name="Judge Swath" t-name="%s">\n    %s\n</t>'
                    % (SNIPPET_KEY, section()))
    instance = section(HOME_SENTINEL)
    ET.fromstring(snippet_arch)
    ET.fromstring(instance)
    print("  [ok] markup is well-formed XML; swath path %d chars, %d flecks, %d streaks"
          % (len(swath_path()), len(fleck_paths()), len(STREAKS)))

    # 1. snippet template
    found = call("ir.ui.view", "search", [["key", "=", SNIPPET_KEY], ["website_id", "=", SITE]])
    if found:
        print("  snippet view exists: %d" % found[0])
    elif apply_:
        vid = call("ir.ui.view", "create", {
            "name": "Judge Swath", "key": SNIPPET_KEY, "type": "qweb",
            "arch": snippet_arch, "website_id": SITE})
        print("  created snippet view %d" % vid)
    else:
        print("  would-create snippet view %s" % SNIPPET_KEY)

    # 2. palette entry in the Judge group
    pal = call("ir.ui.view", "read", [PALETTE_VIEW], ["arch_db", "website_id"])[0]
    assert pal["website_id"][0] == SITE
    entry = '<t t-snippet="website.s_jd_swath" string="Swath" group="judge"/>'
    if "s_jd_swath" in pal["arch_db"]:
        print("  palette already lists Swath")
    else:
        anchor = '<t t-snippet="website.s_jd_rule"'
        assert anchor in pal["arch_db"], "palette anchor missing"
        new_pal = pal["arch_db"].replace(anchor, entry + "\n        " + anchor, 1)
        ET.fromstring(new_pal)
        if apply_:
            call("ir.ui.view", "write", [PALETTE_VIEW], {"arch": new_pal})
            print("  registered Swath in the Judge palette group")
        else:
            print("  would-register Swath in the Judge palette group")

    # 3. CSS
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if CSS_SENTINEL in head:
        print("  swath css already present")
    elif apply_:
        assert "</style>" in head
        call("website", "write", [SITE], {"custom_code_head": head.replace("</style>", CSS + "</style>", 1)})
        print("  appended %d chars of swath css" % len(CSS))
    else:
        print("  would-append %d chars of swath css" % len(CSS))

    # 4. homepage instance, after the certifications band
    home = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db", "website_id"])[0]
    assert home["website_id"][0] == SITE
    body = home["arch_db"]
    if HOME_SENTINEL in body:
        print("  homepage instance already present")
        return 0
    marker = '<section class="s_text_image'
    assert marker in body, "could not find the insertion point on the homepage"
    new = body.replace(marker, instance + marker, 1)
    ET.fromstring(new)
    print("  homepage instance ready (%d chars, above the text-image block)" % len(instance))
    if apply_:
        call("ir.ui.view", "write", [HOME_VIEW], {"arch": new})
        back = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db"])[0]["arch_db"]
        assert HOME_SENTINEL in back, "readback failed"
        print("  wrote homepage view %d, verified" % HOME_VIEW)
    else:
        print("  would-write homepage view %d" % HOME_VIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
