#!/usr/bin/env python3
"""Reorder the nav, drop Connect from it, and put Connect in the footer.

Three changes, all at Judge's request:

  - swap the second and fourth numbered items, so Entries sits at 02 and
    It's on Random at 04
  - take Connect out of the top menu (the /connect page stays published; only
    the menu record goes)
  - the footer call to action stops being "Start with a consult" -> /offerings
    and becomes "Connect" -> /connect, taking over the job the nav item had

Menu items are matched by url rather than by position or id, so a reordering
done in the builder between runs cannot make this move the wrong one.

Dry-run by default; --apply writes and re-reads the rendered nav and footer.
"""
import argparse
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
FOOTER = 2038
OLD_CTA = ('<a class="jd-footer-cta" href="/offerings">Start with a consult '
           '<span class="jd-arrow" aria-hidden="true">→</span></a>')
NEW_CTA = ('<a class="jd-footer-cta" href="/connect">Connect '
           '<span class="jd-arrow" aria-hidden="true">→</span></a>')
SWAP = ("/random", "/blog")     # the two that trade places
DROP = "/connect"               # leaves the nav, keeps the page


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
    for u in SWAP + (DROP,):
        assert u in by_url, f"no menu item for {u}"
    a, b = by_url[SWAP[0]], by_url[SWAP[1]]
    drop = by_url[DROP]

    foot = call("ir.ui.view", "read", [FOOTER], ["id", "website_id", "arch_db"])[0]
    assert foot["website_id"][0] == SITE, foot
    assert foot["arch_db"].count(OLD_CTA) == 1, "footer CTA not found as expected"
    new_arch = foot["arch_db"].replace(OLD_CTA, NEW_CTA)
    ET.fromstring(new_arch)

    print(f"  swap  {a['name']} (seq {a['sequence']}) <-> {b['name']} (seq {b['sequence']})")
    print(f"  drop  {drop['name']} -> {drop['url']} from the menu (page stays published)")
    print(f"  footer CTA: 'Start with a consult' -> /offerings  becomes  'Connect' -> /connect")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    call("website.menu", "write", [a["id"]], {"sequence": b["sequence"]})
    call("website.menu", "write", [b["id"]], {"sequence": a["sequence"]})
    call("website.menu", "unlink", [drop["id"]])
    call("ir.ui.view", "write", [FOOTER], {"arch": new_arch})
    assert NEW_CTA in call("ir.ui.view", "read", [FOOTER], ["arch_db"])[0]["arch_db"]
    time.sleep(3)

    h = fetch("/work")
    nav = h[h.find('<nav class="jd-nav'):]
    nav = nav[:nav.find("</nav>")]
    items = [(m.group(3), m.group(2)) for m in re.finditer(
        r'<a class="jd-(link|navcta)" href="([^"]+)"[\s\S]*?'
        r'<span class="jd-label">([^<]*)</span>', nav)]
    print("\n  rendered nav:")
    for n, u in items:
        print(f"    {n:<20} -> {u}")
    assert not any(u == "/connect" for _, u in items), "Connect still in the nav"

    cta = re.search(r'<a class="jd-footer-cta" href="([^"]+)">([^<]*)<', h)
    print(f"\n  footer CTA: {cta.group(2).strip()!r} -> {cta.group(1)}")
    assert cta.group(1) == "/connect", cta.group(1)

    # /connect must still be reachable even though it left the menu
    code = urllib.request.urlopen("https://www.judgedice.com/connect", timeout=40).getcode()
    print(f"  /connect still live: http {code}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
