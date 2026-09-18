#!/usr/bin/env python3
"""Take the leading number off the /connect page eyebrow.

Connect left the top menu, so its hard-coded "04" both duplicates the number
It's on Random now carries and points at a position the page no longer has.
The label and the rule stay; only the number span goes.

Dry-run by default; --apply writes and re-reads the rendered page.
"""
import argparse
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
CONNECT = 2042                 # website.judge_connect, the /connect page
NUM = ('<span style="color:color-mix(in srgb, var(--paper) 82%, transparent);'
       'font-weight:var(--weight-regular);">04</span>\n                ')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    page = call("ir.ui.view", "read", [CONNECT],
                ["id", "website_id", "arch_db"])[0]
    assert page["website_id"][0] == SITE, page
    n = page["arch_db"].count(NUM)
    assert n == 1, f"expected exactly one eyebrow number, found {n}"
    new_arch = page["arch_db"].replace(NUM, "")
    ET.fromstring(new_arch)
    assert ">Connect</span>" in new_arch, "lost the eyebrow label"

    print("  /connect eyebrow: '04 Connect' -> 'Connect'")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    call("ir.ui.view", "write", [CONNECT], {"arch": new_arch})
    back = call("ir.ui.view", "read", [CONNECT], ["arch_db"])[0]["arch_db"]
    assert NUM not in back and ">Connect</span>" in back
    time.sleep(3)

    h = urllib.request.urlopen(urllib.request.Request(
        "https://www.judgedice.com/connect",
        headers={"Cache-Control": "no-cache"}), timeout=40).read().decode()
    head = h[h.find('<div id="wrap"'):]
    head = head[:head.find("</header>")]
    assert ">04<" not in head, "number still rendering"
    assert ">Connect<" in head, "label missing"
    print("  rendered: eyebrow reads 'Connect', no number")
    return 0


if __name__ == "__main__":
    sys.exit(main())
