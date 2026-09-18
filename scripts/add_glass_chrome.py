#!/usr/bin/env python3
"""Liquid-glass header + footer on the quote ("random") pages.

Two changes, both pure CSS in website[2].custom_code_head:

1. The citation link fix. Nothing in the stylesheet ever styled the <a> inside
   .s_jd_quotepage_cite - only the one inside the blockquote's <p> - so it fell
   through to the user-agent default, pure black, sitting on a near-black
   photograph. Verified in the browser: computed colour rgb(0, 0, 0).

2. The chrome. A page whose whole body is a single quote block gets its header
   and footer lifted out of the flex column and floated over the artwork as
   fixed-height translucent bars, with the type reversed out to paper.

Scoping is done with :has() rather than a class on the page, so any quote page
Judge builds later is picked up with no extra work - and a browser without
:has() simply renders today's opaque chrome instead of a broken half-version.
The :only-child guard keeps a quote block used as one section among many on an
ordinary page from dragging the site's chrome along with it.

Dry-run by default; --apply writes.
"""
import argparse
import sys

from odoo import connect

SITE = 2
SENTINEL = "/* ---- jd-glass-chrome v1 ---- */"
END = "/* ---- end jd-glass-chrome ---- */"

# The scoping prefix, spelled out once per rule below. `main` is a direct child
# of #wrapwrap, #wrap a direct child of main.
Q = "#wrapwrap:has(>main>#wrap>.s_jd_quotepage:only-child)"
DARK = ".s_jd_quotepage.o_cc4, .s_jd_quotepage.o_cc5"  # documentation only

# Colour split, matching the one the Judge Quote Page block already uses:
# o_cc4/o_cc5 are the dark artwork combinations, o_cc1-o_cc3 the light ones.
DARK = f"{Q}:has(.s_jd_quotepage:is(.o_cc4,.o_cc5))"
LIGHT = f"{Q}:has(.s_jd_quotepage:is(.o_cc1,.o_cc2,.o_cc3))"

# Bootstrap paints the burger and the close X as background SVGs, so the colour
# is baked into the image and no property can reach it - the whole data URI has
# to be swapped for one stroked in paper.
BURGER = ("url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' "
          "viewBox='0 0 30 30'%3e%3cpath stroke='%23F2ECDF' stroke-width='2' "
          "stroke-linecap='round' d='M4 9h22M4 15h22M4 21h22'/%3e%3c/svg%3e\")")
CLOSE = ("url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' "
         "viewBox='0 0 16 16'%3e%3cpath stroke='%23F2ECDF' stroke-width='1.6' "
         "stroke-linecap='round' d='M3 3l10 10M13 3L3 13'/%3e%3c/svg%3e\")")

CSS = f"""{SENTINEL}

/* --- (1) the citation link ---------------------------------------------
   Belongs with the Judge Quote Page block above; it lives here so the whole
   change sits behind one sentinel. Untouched, this <a> is UA-default black.
   It carries the poem's title, so it reads a step brighter than the dim cite
   text around it, with a hairline rule instead of an underline. --- */
.s_jd_quotepage .s_jd_quotepage_cite a{{
  text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:1px;
  transition:color var(--dur-base) var(--ease-out),
             border-color var(--dur-base) var(--ease-out);
}}
.s_jd_quotepage:is(.o_cc1,.o_cc2,.o_cc3) .s_jd_quotepage_cite a{{color:var(--ink-soft);border-bottom-color:var(--line-strong);}}
.s_jd_quotepage:is(.o_cc4,.o_cc5) .s_jd_quotepage_cite a{{color:var(--paper);border-bottom-color:rgba(242,236,223,.45);}}
.s_jd_quotepage .s_jd_quotepage_cite a:hover,
.s_jd_quotepage .s_jd_quotepage_cite a:focus-visible{{color:var(--vermilion);border-color:var(--vermilion);}}
@media (prefers-reduced-motion:reduce){{.s_jd_quotepage .s_jd_quotepage_cite a{{transition:none;}}}}

/* --- (2) structure: float the chrome over the artwork -------------------
   #wrapwrap is already a flex column of min-height 100vh with <main> as the
   growing child, so taking the two bars out of flow is all it takes for the
   quote section to claim the whole viewport behind them. --- */
{Q}{{position:relative;--jd-glass-h:56px;}}
{Q}>header#top,
{Q}>footer{{position:absolute;left:0;right:0;z-index:6;}}
{Q}>header#top{{top:0;}}
{Q}>footer{{bottom:0;}}
{Q} main,
{Q} #wrap{{display:flex;flex-direction:column;}}
{Q} #wrap,
{Q} .s_jd_quotepage{{flex:1 1 auto;}}
/* keep the quote clear of both bars even on a short viewport */
{Q} .s_jd_quotepage{{padding-top:max(clamp(6rem,18vh,12rem),calc(var(--jd-glass-h) + 2rem));
  padding-bottom:max(clamp(6rem,18vh,12rem),calc(var(--jd-glass-h) + 2rem));}}
/* both wrappers carry an opaque theme background of their own; the glass
   lives on the bar inside, so it needs something to actually see through */
{Q}>header#top,
{Q}>footer,
{Q} #footer{{background:transparent;}}

/* --- (3) fixed, minimal bar heights --- */
{Q} .jd-nav{{height:var(--jd-glass-h);padding-top:0;padding-bottom:0;}}
{Q} .jd-brand{{font-size:22px;}}
{Q} header#top .o_header_mobile .o_main_nav{{height:var(--jd-glass-h);padding-top:0;padding-bottom:0;}}
{Q} .jd-footer-baseinner{{height:var(--jd-glass-h);padding-top:0;padding-bottom:0;
  flex-wrap:nowrap;align-items:center;border-top:0;max-width:none;}}
{Q} .jd-footer-mark{{font-size:18px;}}
/* the bar is a fixed height, so shed the optional items rather than wrap */
@media (max-width:900px){{{Q} .jd-footer-tagline{{display:none;}}}}
@media (max-width:620px){{{Q} .jd-footer-copy{{display:none;}}}}

/* --- (4) the glass itself --- */
{Q} .jd-nav,
{Q} header#top .o_header_mobile,
{Q} .jd-footer-base{{
  -webkit-backdrop-filter:blur(18px) saturate(150%);
  backdrop-filter:blur(18px) saturate(150%);
  box-shadow:none;
}}

/* --- (5) dark artwork: smoked glass, type reversed to paper --- */
{DARK} .jd-nav,
{DARK} header#top .o_header_mobile{{background:rgba(16,12,8,.30);border-bottom:1px solid rgba(242,236,223,.16);}}
{DARK} .jd-footer-base{{background:rgba(16,12,8,.30);border-top:1px solid rgba(242,236,223,.16);}}
{DARK} .jd-brand,
{DARK} .jd-mnav-mark,
{DARK} .jd-nav .jd-link,
{DARK} .jd-footer-mark,
{DARK} .jd-footer-cta{{color:var(--paper);}}
{DARK} .jd-footer-baseinner>span{{color:rgba(242,236,223,.62);}}
{DARK} header#top .o_header_mobile .o_wsale_my_cart .btn{{color:var(--paper)!important;}}
{DARK} .jd-nav .jd-navcta{{color:var(--paper);border-color:rgba(242,236,223,.55);padding-top:8px;padding-bottom:8px;}}
{DARK} .jd-nav .jd-navcta:hover,
{DARK} .jd-nav .jd-navcta:focus-visible{{background:var(--vermilion);border-color:var(--vermilion);color:var(--paper);}}
{DARK} header#top .o_header_mobile .navbar-toggler-icon{{background-image:{BURGER};}}

/* the drawer slides out over the artwork too, so it gets the same smoked
   glass - heavier, because menu text has to stay readable over a photograph -
   and every ink-coloured part of it reverses. */
{DARK} .o_navbar_mobile{{
  background:rgba(16,12,8,.84);
  -webkit-backdrop-filter:blur(24px) saturate(150%);
  backdrop-filter:blur(24px) saturate(150%);
  border-left:1px solid rgba(242,236,223,.16);
}}
{DARK} .o_navbar_mobile .btn-close{{background-image:{CLOSE};}}
{DARK} .o_navbar_mobile .top_menu .nav-item{{border-top-color:rgba(242,236,223,.16)!important;}}
{DARK} .o_navbar_mobile .top_menu .nav-item:last-child{{border-bottom-color:rgba(242,236,223,.16)!important;}}
{DARK} .o_navbar_mobile .top_menu .nav-link{{color:var(--paper);}}
{DARK} .o_navbar_mobile .top_menu .nav-link[href="/appointment"]{{border-color:rgba(242,236,223,.55);}}
{DARK} .o_navbar_mobile .o_searchbar_form .input-group{{border-bottom-color:rgba(242,236,223,.35);}}
{DARK} .o_navbar_mobile .o_searchbar_form .oe_search_box{{color:var(--paper)!important;}}
{DARK} .o_navbar_mobile .o_searchbar_form .oe_search_box::placeholder{{color:rgba(242,236,223,.55);}}
{DARK} .o_navbar_mobile .o_searchbar_form .oe_search_button{{color:rgba(242,236,223,.62);}}

/* --- (6) light artwork: frosted paper, type stays ink. Nothing uses this
   yet - it is here so a light quote page does not come out unreadable. --- */
{LIGHT} .jd-nav,
{LIGHT} header#top .o_header_mobile{{background:rgba(242,236,223,.55);border-bottom:1px solid rgba(28,23,18,.12);}}
{LIGHT} .jd-footer-base{{background:rgba(242,236,223,.55);border-top:1px solid rgba(28,23,18,.12);}}
{LIGHT} .o_navbar_mobile{{
  background:rgba(242,236,223,.88);
  -webkit-backdrop-filter:blur(24px) saturate(150%);
  backdrop-filter:blur(24px) saturate(150%);
}}

{END}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    uid, call = connect()
    site = call("website", "read", [SITE], ["id", "name", "custom_code_head"])[0]
    assert site["name"] != "Half a Glass", "refusing to write site 1"
    head = site["custom_code_head"] or ""

    if SENTINEL in head:
        i = head.index(SENTINEL)
        j = head.index(END) + len(END)
        new_head = head[:i] + CSS + head[j:]
        what = "replace"
    else:
        # custom_code_head is a <head> fragment, not a bare stylesheet: it opens
        # with <link> tags and a <style>. Anything appended past the final
        # </style> lands in the document as text and gets painted on the page.
        # Always insert inside the stylesheet.
        i = head.rindex("</style>")
        new_head = head[:i].rstrip() + "\n\n" + CSS + "\n" + head[i:]
        what = "insert"

    assert new_head.index(SENTINEL) < new_head.rindex("</style>"), \
        "sentinel escaped the <style> block"
    assert new_head.count(SENTINEL) == 1 and new_head.count(END) == 1

    print(f"{what}: {len(head)} -> {len(new_head)} chars "
          f"(+{len(new_head) - len(head)}) on website {SITE} ({site['name']})")
    if not args.apply:
        print("dry run - pass --apply to write")
        return 0

    call("website", "write", [SITE], {"custom_code_head": new_head})
    back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
    assert SENTINEL in back and back.index(SENTINEL) < back.rindex("</style>")
    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
