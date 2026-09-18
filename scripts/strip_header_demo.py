#!/usr/bin/env python3
"""Stop Odoo's demo phone number and Contact Us button rendering on site 2.

View 2035 keeps a hidden jd-header-plugs span holding the five
website.placeholder_header_* t-calls, because module installs validate against
those anchors (CLAUDE.md rule 8). The anchors are empty templates; the demo
content is injected by two of Odoo's own SHARED views:

    1396 website.header_text_element     -> tel:+1 555-555-5556, info@yourcompany
    1358 website.header_call_to_action   -> a "Contact Us" button to /contactus

They are display:none, so nothing shows - but they are still in the delivered
HTML, where screen readers and crawlers find a fake phone number and a link to
a page that does not exist on this site.

Both views belong to site 1 as well, so they are never edited. Instead this
uses Odoo's own copy-on-write: writing active=False with website_id in the
context makes Odoo fork a website-specific copy and deactivate that, leaving
the shared original active for Half a Glass. The t-calls in 2035 stay exactly
where they are and still resolve - they just render nothing.

Verifies both sites afterwards and rolls back if the shared view was hit.
"""
import argparse
import sys
import time
import urllib.request

from odoo import connect

SITE = 2
TARGETS = {1396: "website.header_text_element", 1358: "website.header_call_to_action"}
MARKERS = ["555-555-5556", "/contactus", "yourcompany.example.com"]


def page(url):
    req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    return urllib.request.urlopen(req, timeout=40).read().decode()


def markers(html):
    return {m: html.count(m) for m in MARKERS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    for vid, key in TARGETS.items():
        v = call("ir.ui.view", "read", [vid], ["id", "key", "website_id", "active"])[0]
        assert v["key"] == key and v["website_id"] is False, v
        print(f"  {vid} {key}: shared, active={v['active']}")

    before2 = markers(page("https://www.judgedice.com/"))
    before1 = markers(page("https://www.halfa.glass/shop"))
    print(f"\n  site 2 before: {before2}")
    print(f"  site 1 before: {before1}")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    made = []
    try:
        for vid, key in TARGETS.items():
            call("ir.ui.view", "write", [vid], {"active": False},
                 context={"website_id": SITE, "lang": "en_US"})
            shared = call("ir.ui.view", "read", [vid], ["active", "website_id"])[0]
            if not shared["active"] or shared["website_id"] is not False:
                raise RuntimeError(f"copy-on-write did not fork: {vid} -> {shared}")
            # ir.ui.view.search hides inactive records unless active_test is
            # off - and the fork we just made is inactive by definition.
            forks = call("ir.ui.view", "search",
                         [["key", "=", key], ["website_id", "=", SITE]],
                         context={"active_test": False})
            assert forks, f"no site-{SITE} fork created for {key}"
            made += forks
            print(f"  {key}: shared {vid} still active, site-2 fork {forks} deactivated")

        time.sleep(3)
        after2 = markers(page("https://www.judgedice.com/"))
        after1 = markers(page("https://www.halfa.glass/shop"))
        print(f"\n  site 2 after: {after2}")
        print(f"  site 1 after: {after1}")
        if after1 != before1:
            raise RuntimeError(f"site 1 changed: {before1} -> {after1}")
        if any(after2.values()):
            raise RuntimeError(f"site 2 still carries demo markers: {after2}")
    except Exception as e:
        print(f"\nFAILED: {e}\n  rolling back...")
        for vid in TARGETS:
            call("ir.ui.view", "write", [vid], {"active": True})
        if made:
            call("ir.ui.view", "write", made, {"active": True})
        print("  rolled back.")
        return 3

    print("\napplied - site 2 clean, site 1 unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
