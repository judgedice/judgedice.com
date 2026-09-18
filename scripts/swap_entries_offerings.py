#!/usr/bin/env python3
"""Trade nav places between Entries and Offerings, so Offerings sits at 02.

The nav numbers are a CSS counter (`counter(jdnav, decimal-leading-zero)` in
custom_code_head), so reordering the two menu records renumbers the nav on its
own.  The one thing that does not follow automatically is the eyebrow printed
at the top of the /offerings page itself, which hard-codes its own number to
match the nav - that moves 03 -> 02 here so the page and the nav agree again.

Menu items are matched by url, not by position or id, so a reorder done in the
builder between runs cannot make this move the wrong pair.

Dry-run by default; --apply writes and then re-reads the rendered nav and page.
"""
import argparse
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
OFFERINGS = 2041                       # website.judge_exciting, the /offerings page
SWAP = ("/blog", "/offerings")         # Entries <-> Offerings
# the page eyebrow, distinguished from the numbered cards further down the page
# by its style attribute - asserted unique before anything is written
OLD_EYEBROW = '<span style="color:var(--ink-faint);font-weight:var(--weight-regular);">03</span>'
NEW_EYEBROW = '<span style="color:var(--ink-faint);font-weight:var(--weight-regular);">02</span>'


def fetch(path):
    return urllib.request.urlopen(urllib.request.Request(
        "https://www.judgedice.com" + path,
        headers={"Cache-Control": "no-cache"}), timeout=40).read().decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    menus = call("website.menu", "read",
                 call("website.menu", "search",
                      [["website_id", "=", SITE], ["parent_id", "=", 7]]),
                 ["id", "name", "url", "sequence"])
    by_url = {m["url"]: m for m in menus}
    for u in SWAP:
        assert u in by_url, f"no menu item for {u}"
    a, b = by_url[SWAP[0]], by_url[SWAP[1]]

    page = call("ir.ui.view", "read", [OFFERINGS], ["id", "website_id", "arch_db"])[0]
    assert page["website_id"][0] == SITE, page
    n = page["arch_db"].count(OLD_EYEBROW)
    assert n == 1, f"expected exactly one /offerings eyebrow, found {n}"
    new_arch = page["arch_db"].replace(OLD_EYEBROW, NEW_EYEBROW)
    ET.fromstring(new_arch)

    order = sorted(menus, key=lambda m: m["sequence"])
    print("  nav now:   " + " · ".join(
        f"{i:02d} {m['name']}" for i, m in enumerate(order, 1)))
    swapped = sorted(menus, key=lambda m: (b if m is a else a if m is b else m)["sequence"])
    print("  nav after: " + " · ".join(
        f"{i:02d} {m['name']}" for i, m in enumerate(swapped, 1)))
    print(f"  /offerings eyebrow: 03 -> 02")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    call("website.menu", "write", [a["id"]], {"sequence": b["sequence"]})
    call("website.menu", "write", [b["id"]], {"sequence": a["sequence"]})
    call("ir.ui.view", "write", [OFFERINGS], {"arch": new_arch})
    assert NEW_EYEBROW in call("ir.ui.view", "read", [OFFERINGS],
                               ["arch_db"])[0]["arch_db"]
    time.sleep(3)

    h = fetch("/offerings")
    nav = h[h.find('<nav class="jd-nav'):]
    nav = nav[:nav.find("</nav>")]
    items = [(m.group(3), m.group(2)) for m in re.finditer(
        r'<a class="jd-(link|navcta)" href="([^"]+)"[\s\S]*?'
        r'<span class="jd-label">([^<]*)</span>', nav)]
    print("\n  rendered nav:")
    for i, (n_, u) in enumerate(items, 1):
        print(f"    {i:02d} {n_:<20} -> {u}")
    urls = [u for _, u in items]
    assert urls.index("/offerings") < urls.index("/blog"), urls

    assert NEW_EYEBROW in h and OLD_EYEBROW not in h, "eyebrow did not re-render"
    print("\n  /offerings eyebrow renders 02")
    return 0


if __name__ == "__main__":
    sys.exit(main())
