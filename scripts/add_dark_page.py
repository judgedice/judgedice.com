#!/usr/bin/env python3
"""Run /connect dark, top to bottom.

The page was already half-dark: its <header> carries background:var(--ink)
inline, and the body copy underneath is written in paper at 82%. But the
section holding that copy has no background, so the paragraph was paper text
on the paper ground - invisible. The blank band between the headline and the
email button was the missing paragraph.

Rather than patch one inline style, this marks the page's #wrap with
jd-dark-page and adds a CSS block that carries the ink through the section and
the footer, reversing the footer type to paper the same way the quote pages
do. Any other page can be darkened later by adding the one class.

No !important on the section background, so the website builder can still set
a background there and win.

Dry-run by default; --apply writes.
"""
import argparse
import sys
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
VIEW = 2042
OLD = '<div id="wrap" class="oe_structure">'
NEW = '<div id="wrap" class="oe_structure jd-dark-page">'

SENTINEL = "/* ---- jd-dark-page v1 ---- */"
END = "/* ---- end jd-dark-page ---- */"
D = "#wrapwrap:has(#wrap.jd-dark-page)"

CSS = f"""{SENTINEL}
/* A page marked jd-dark-page runs ink from its header down through the footer.
   /connect's copy is already written in paper, which is why it read as blank
   on the default ground. No !important on the section background - the builder
   should still be able to set one and win. */
{D}{{background:var(--ink);}}
{D} #wrap.jd-dark-page > section{{background:var(--ink);}}
{D} > footer,
{D} #footer{{background:transparent;}}
{D} .jd-footer-base{{background:var(--ink);}}
{D} .jd-footer-baseinner{{border-top:1px solid rgba(242,236,223,.16);}}
{D} .jd-footer-mark,
{D} .jd-footer-cta{{color:var(--paper);}}
{D} .jd-footer-baseinner>span{{color:rgba(242,236,223,.62);}}
{D} .jd-footer-mark:hover,
{D} .jd-footer-cta:hover{{color:var(--vermilion);}}
{END}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    v = call("ir.ui.view", "read", [VIEW], ["id", "key", "website_id", "arch_db"])[0]
    assert v["website_id"][0] == SITE, v
    arch = v["arch_db"]
    if "jd-dark-page" in arch:
        new_arch, what_v = arch, "already marked"
    else:
        assert arch.count(OLD) == 1, "unexpected #wrap markup"
        new_arch, what_v = arch.replace(OLD, NEW), "add jd-dark-page class"
    ET.fromstring(new_arch)

    site = call("website", "read", [SITE], ["id", "name", "custom_code_head"])[0]
    assert site["name"] != "Half a Glass", "refusing to write site 1"
    head = site["custom_code_head"] or ""
    if SENTINEL in head:
        i, j = head.index(SENTINEL), head.index(END) + len(END)
        new_head, what_c = head[:i] + CSS + head[j:], "replace"
    else:
        # custom_code_head is a <head> fragment: past the final </style> the
        # rules render as text on the page. Always insert inside.
        i = head.rindex("</style>")
        new_head, what_c = head[:i].rstrip() + "\n\n" + CSS + "\n" + head[i:], "insert"
    assert new_head.index(SENTINEL) < new_head.rindex("</style>")

    print(f"  view {VIEW}: {what_v}")
    print(f"  css: {what_c} ({len(head)} -> {len(new_head)} chars)")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    if new_arch != arch:
        call("ir.ui.view", "write", [VIEW], {"arch": new_arch})
        assert "jd-dark-page" in call("ir.ui.view", "read", [VIEW], ["arch_db"])[0]["arch_db"]
    call("website", "write", [SITE], {"custom_code_head": new_head})
    back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
    assert SENTINEL in back and back.index(SENTINEL) < back.rindex("</style>")
    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
