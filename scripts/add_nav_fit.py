#!/usr/bin/env python3
"""Keep the desktop nav on one line now that it carries six links plus the CTA.

Re-linking /home and /connect took the nav from four numbered items to six.
At 1440px that still fits comfortably, but between the lg breakpoint (992px)
and roughly 1200px the brand, the links and the Let's Talk button together
overflow, and .jd-links wraps - dropping the CTA onto a second row and pushing
the header from 86px to 143px.

Rather than move the breakpoint (which would need the mobile header's own
visibility rules changed to match), this just tightens the gutter, the gap and
the CTA padding across that one band. Above 1200px nothing changes.

Dry-run by default; --apply writes.
"""
import argparse
import sys

from odoo import connect

SITE = 2
SENTINEL = "/* ---- jd-nav-fit v1 ---- */"
END = "/* ---- end jd-nav-fit ---- */"

CSS = f"""{SENTINEL}
/* Six links + a button is wider than the lg breakpoint allows. Close the
   spacing up between 992px and 1200px so the row survives; the 1440px
   composition is untouched. */
@media (min-width:992px) and (max-width:1199.98px){{
  .jd-nav{{padding-left:clamp(1rem,3vw,2.5rem);padding-right:clamp(1rem,3vw,2.5rem);}}
  .jd-links{{gap:clamp(12px,1.7vw,22px);}}
  .jd-nav .jd-link{{font-size:0.75rem;}}
  .jd-nav .jd-navcta{{margin-left:clamp(4px,1vw,12px);padding:10px 14px;font-size:0.75rem;}}
  .jd-brand{{font-size:23px;}}
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
        i, j = head.index(SENTINEL), head.index(END) + len(END)
        new_head = head[:i] + CSS + head[j:]
        what = "replace"
    else:
        # custom_code_head is a <head> fragment: anything past the final
        # </style> renders as text on the page. Always insert inside.
        i = head.rindex("</style>")
        new_head = head[:i].rstrip() + "\n\n" + CSS + "\n" + head[i:]
        what = "insert"

    assert new_head.index(SENTINEL) < new_head.rindex("</style>")
    assert new_head.count(SENTINEL) == 1 and new_head.count(END) == 1
    print(f"{what}: {len(head)} -> {len(new_head)} chars (+{len(new_head)-len(head)})")
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
