# -*- coding: utf-8 -*-
"""Add the halftone portrait to the right of the homepage hero.

Multiply-blended so the print texture sits on the paper ground the way ink
would, anchored to the browser's right edge, masked so it dissolves off the
right rather than ending on a hard rectangle edge.

The hero markup is left alone apart from one added, aria-hidden div — the
headline and its wording are untouched. Everything else is CSS: the section
becomes full-bleed and positioned, while the existing children keep their own
widths, so the text lands exactly where it does today.

Tuning knobs live in CSS custom properties on .jd-hero-portrait, so nudging the
crop later is a one-value edit, not a re-run:
  --portrait-x      background-position-x: how far right the head sits
  --portrait-w      width of the portrait band
  --portrait-fade   where the fade to transparent begins on the right

Usage: python3 scripts/add_hero_portrait.py [--image PATH] [--apply]
"""
import sys, os, base64, mimetypes, re, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE, HOME_VIEW = 2, 2034
ATT_NAME = "judge_hero_portrait"
SENTINEL = "jd-hero-portrait"
DEFAULT_IMAGE = os.path.join(REPO, "assets", "judge-portrait.png")

CSS_TEMPLATE = """
/* ---- Hero portrait ---- */
/* two elements share id="top" on this page (Odoo's wrapper + the hero section),
   and the hero carries an inline max-width, so scope tightly and force the
   full-bleed with !important — otherwise the band stops at 78rem. */
section#top{position:relative;max-width:none !important;overflow:hidden;}
section#top > .reveal,section#top > h1{position:relative;z-index:2;}
.jd-hero-portrait{
  --portrait-w:min(62vw,940px);
  --portrait-shift:16vw;   /* pushes the frame right so the near shoulder runs off the page */
  --portrait-feather:20vw; /* how far the left dissolve runs before it is fully opaque */
  --portrait-lean:95deg;   /* 90deg = vertical edge; 95deg rakes the edge 5° forward */
  --portrait-pad:5vw;      /* a raked edge travels sideways across the frame's height;
                              without this pad the fade starts left of the image's own
                              (vertical) left edge near the bottom and that edge shows */
  --portrait-opacity:.85;
  position:absolute;top:0;right:0;bottom:0;width:var(--portrait-w);
  mix-blend-mode:multiply;opacity:var(--portrait-opacity);z-index:1;
  /* One fade only, on the left: it starts where the shifted image starts (any
     earlier and the mask wastes its ramp on empty space, any later and the
     image's own edge shows as a seam). The right side runs hard off the page.
     The 5° lean makes the dissolve a raked edge rather than a ruled line. */
  -webkit-mask-image:linear-gradient(var(--portrait-lean),transparent calc(var(--portrait-shift) + var(--portrait-pad)),#000 calc(var(--portrait-shift) + var(--portrait-pad) + var(--portrait-feather)));
  mask-image:linear-gradient(var(--portrait-lean),transparent calc(var(--portrait-shift) + var(--portrait-pad)),#000 calc(var(--portrait-shift) + var(--portrait-pad) + var(--portrait-feather)));
}
/* a real <img> so it can be swapped in the builder (double-click -> Replace).
   !important guards against the classes Odoo's editor adds on replace
   (img-fluid sets height:auto, which would collapse the frame). */
.jd-hero-portrait img{
  display:block!important;width:100%!important;height:100%!important;
  object-fit:cover!important;
  object-position:calc(100% + var(--portrait-shift)) center!important;
  max-width:none!important;border-radius:0!important;
}
@media (max-width:900px){
  /* narrower frame, gentler shift, and a much longer feather so the portrait
     reads as texture behind the headline rather than competing with it */
  .jd-hero-portrait{--portrait-w:78vw;--portrait-shift:4vw;--portrait-pad:3vw;--portrait-feather:38vw;--portrait-opacity:.22;}
}

"""

DIV = ('<div class="%s"><img src="__URL__" alt="Judge DiCesaro" '
       'class="jd-hero-portrait-img" loading="eager" fetchpriority="high"/></div>') % SENTINEL


def main(argv):
    apply_ = "--apply" in argv
    image = DEFAULT_IMAGE
    if "--image" in argv:
        image = os.path.abspath(argv[argv.index("--image") + 1])

    print("add_hero_portrait [%s]" % ("APPLY" if apply_ else "dry-run"))
    if not os.path.exists(image):
        print("  MISSING image: %s" % image)
        print("  Save the portrait there (or pass --image PATH) and re-run.")
        return 1
    size = os.path.getsize(image)
    mime = mimetypes.guess_type(image)[0] or "image/png"
    print("  image: %s (%s, %.0f KB)" % (os.path.relpath(image, REPO), mime, size / 1024.0))

    uid, call = connect()

    # 1. attachment (public, site-2) — self-hosted, like the credential badges
    found = call("ir.attachment", "search", [["name", "=", ATT_NAME], ["website_id", "=", SITE]])
    if found:
        att = found[0]
        print("  attachment exists: %d (re-run with the same name reuses it)" % att)
    elif apply_:
        att = call("ir.attachment", "create", {
            "name": ATT_NAME, "mimetype": mime, "public": True,
            "website_id": SITE, "res_model": "ir.ui.view",
            "datas": base64.b64encode(open(image, "rb").read()).decode("ascii")})
        print("  uploaded attachment %d" % att)
    else:
        att = 0
        print("  would-upload attachment")

    url = "/web/image/%d" % att
    css = CSS_TEMPLATE.replace("__URL__", url)

    # 2. CSS
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if ".jd-hero-portrait{" in head:
        print("  portrait css already present (edit the custom properties to re-crop)")
    elif apply_:
        assert "</style>" in head
        call("website", "write", [SITE], {"custom_code_head": head.replace("</style>", css + "</style>", 1)})
        print("  appended %d chars of portrait css" % len(css))
    else:
        print("  would-append %d chars of portrait css" % len(css))

    # 3. one added div in the hero — no other markup touched
    arch = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db", "website_id"])[0]
    assert arch["website_id"][0] == SITE
    body = arch["arch_db"]
    if SENTINEL in body:
        print("  hero div already present")
        return 0
    m = re.search(r'<section id="top"[^>]*>', body)
    assert m, "hero section not found"
    end = body.index("</section>", m.end())
    new = body[:end] + DIV + body[end:]
    ET.fromstring(new)
    headline_before = re.search(r"<h1.*?</h1>", body, re.S).group(0)
    headline_after = re.search(r"<h1.*?</h1>", new, re.S).group(0)
    assert headline_before == headline_after, "headline changed — aborting"
    print("  hero: adding 1 div; headline byte-identical (verified)")

    if not apply_:
        print("  would-write view %d" % HOME_VIEW)
        return 0
    call("ir.ui.view", "write", [HOME_VIEW], {"arch": new})
    back = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db"])[0]["arch_db"]
    assert SENTINEL in back and headline_before in back
    print("  wrote view %d, verified (headline intact)" % HOME_VIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
