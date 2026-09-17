# -*- coding: utf-8 -*-
"""Style the booking link as the nav's call to action (website 2 only).

The markup half lives in view 2035 (desktop, `.jd-navcta`) and is deployed from
snapshot/ the normal way; this script only owns the CSS.

Both navs key on the URL /appointment rather than on position, so adding a sixth
menu item later can't promote the wrong link. Desktop drops out of the numbered
sequence on its own -- the counter increments on .jd-link, which the CTA isn't.
Mobile is CSS-only (the drawer's links come from a website.submenu t-call we'd
rather not restructure), so the counter there is suppressed explicitly.

Dry-run by default; --apply writes. Idempotent, sentinel-guarded.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2
SENTINEL = "/* ---- jd-nav-cta v1 ---- */"
END = "/* ---- end jd-nav-cta ---- */"

CSS = SENTINEL + '''
/* The booking link reads as an action, not a destination, so it sits apart from
   the numbered links: an ink outline that fills vermilion on hover. Restrained
   on purpose -- the border alone carries the affordance, no arrow. */

/* --- desktop (.jd-nav) --- */
.jd-nav .jd-navcta{
  display:inline-flex;align-items:center;
  margin-left:clamp(6px,1.5vw,20px);
  padding:11px 20px;border:1px solid var(--ink);border-radius:var(--radius-none);
  font-family:var(--font-serif);font-size:var(--text-label);
  text-transform:uppercase;letter-spacing:var(--tracking-label);
  font-weight:var(--weight-medium);color:var(--ink);text-decoration:none;
  white-space:nowrap;
  transition:background var(--dur-base) var(--ease-out),
             border-color var(--dur-base) var(--ease-out),
             color var(--dur-base) var(--ease-out);
}
.jd-nav .jd-navcta:hover,
.jd-nav .jd-navcta:focus-visible{background:var(--vermilion);border-color:var(--vermilion);color:var(--paper);}
@media (prefers-reduced-motion:reduce){.jd-nav .jd-navcta{transition:none;}}

/* --- mobile drawer --- */
/* Keyed on href so it matches the desktop rule; :has() lifts the treatment to
   the <li> so the hairline rules stop above the button. */
.o_navbar_mobile .top_menu .nav-item:has(> .nav-link[href="/appointment"]){
  border-top:0!important;border-bottom:0!important;margin-top:20px;
}
.o_navbar_mobile .top_menu .nav-link[href="/appointment"]{
  justify-content:center;
  padding:14px 18px!important;border:1px solid var(--ink);
  counter-increment:none;
}
.o_navbar_mobile .top_menu .nav-link[href="/appointment"]::before{content:none;}
.o_navbar_mobile .top_menu .nav-link[href="/appointment"]:hover,
.o_navbar_mobile .top_menu .nav-link[href="/appointment"]:focus{
  background:var(--vermilion);border-color:var(--vermilion);color:var(--paper);
}
''' + END


def main(argv):
    apply_ = "--apply" in argv
    uid, call = connect()
    print("add_nav_cta [%s] site=%d" % ("APPLY" if apply_ else "dry-run", SITE))

    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if SENTINEL in head:
        s = head.index(SENTINEL)
        e = head.index(END) + len(END)
        new_head = head[:s] + CSS + head[e:]
        what = "update"
    else:
        # custom_code_head is a <head> fragment: appending past the final
        # </style> renders the rules as page text. Always insert inside it.
        i = head.rindex("</style>")
        new_head = head[:i].rstrip() + "\n\n" + CSS + "\n" + head[i:]
        what = "insert"
    assert new_head.index(SENTINEL) < new_head.rindex("</style>"), \
        "sentinel block sits outside <style> — would render as page text"

    if new_head == head:
        print("  noop  custom_code_head already matches")
        return 0
    if not apply_:
        print("  would-%s  custom_code_head (%d -> %d chars)" % (what, len(head), len(new_head)))
        print("dry-run only; re-run with --apply")
        return 0

    call("website", "write", [SITE], {"custom_code_head": new_head})
    back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
    ok = (back or "").strip() == new_head.strip()
    print("  %s custom_code_head (%s, %d -> %d chars)"
          % ("wrote" if ok else "FAIL ", what, len(head), len(new_head)))
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
