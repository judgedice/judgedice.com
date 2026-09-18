#!/usr/bin/env python3
"""Put /home and /connect back in the nav.

Both pages are published and live but unreachable from the menu: /connect was
already orphaned, and /home lost its slot when "It's on Random" took it over.

Order pairs the two life pages and keeps the booking CTA last, where the header
template expects it:

    01 Work · 02 It's on Random · 03 Home Life · 04 Offerings · 05 Entries
    · 06 Connect · [Let's Talk]

"Home Life" rather than "Home" so it reads as the page it is and not as the
site root. Labels match the page names; nothing else about the menu changes.

Dry-run by default; --apply writes and verifies the rendered nav.
"""
import argparse
import sys
import time
import urllib.request

from odoo import connect

SITE = 2
ROOT = 7
# (url, label, sequence) - the full intended menu, in order
WANT = [("/work", "Work", 0),
        ("/random", "It's on Random", 1),
        ("/home", "Home Life", 2),
        ("/offerings", "Offerings", 3),
        ("/blog", "Entries", 4),
        ("/connect", "Connect", 5),
        ("/appointment", "Let's Talk", 6)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    existing = call("website.menu", "read",
                    call("website.menu", "search",
                         [["website_id", "=", SITE], ["parent_id", "=", ROOT]]),
                    ["id", "name", "url", "sequence"])
    by_url = {m["url"]: m for m in existing}

    # every page we are about to link must actually be published
    for url, _, _ in WANT:
        if url.startswith("/") and url not in ("/random", "/appointment", "/blog"):
            pages = call("website.page", "search_read",
                         [["url", "=", url], ["website_id", "=", SITE]],
                         fields=["id", "url", "is_published"])
            assert pages and pages[0]["is_published"], f"{url} is not a published page"

    plan = []
    for url, label, seq in WANT:
        m = by_url.get(url)
        if m is None:
            plan.append(("create", url, label, seq, None))
        elif m["sequence"] != seq or m["name"] != label:
            plan.append(("reseq", url, label, seq, m["id"]))
    orphaned = [m for m in existing if m["url"] not in {u for u, _, _ in WANT}]

    for action, url, label, seq, mid in plan:
        print(f"  {action:<6} seq={seq} {label:<16} -> {url}" + (f"  (menu {mid})" if mid else ""))
    if orphaned:
        print(f"  leaving alone: {[(m['name'], m['url']) for m in orphaned]}")
    if not plan:
        print("  menu already matches")
        return 0
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    for action, url, label, seq, mid in plan:
        if action == "create":
            r = call("website.menu", "create", [{
                "name": label, "url": url, "parent_id": ROOT,
                "website_id": SITE, "sequence": seq}])
            mid = r[0] if isinstance(r, list) else r
            print(f"  created menu {mid}: {label} -> {url}")
        else:
            call("website.menu", "write", [mid], {"sequence": seq, "name": label})
            print(f"  updated menu {mid}: {label} -> {url} (seq {seq})")

    time.sleep(3)
    html = urllib.request.urlopen(
        urllib.request.Request("https://www.judgedice.com/",
                               headers={"Cache-Control": "no-cache"}), timeout=40).read().decode()
    import re
    nav = html[html.find('<nav class="jd-nav'):]
    nav = nav[:nav.find("</nav>")]
    rendered = re.findall(r'<a class="jd-link" href="([^"]+)"[\s\S]*?<span class="jd-label">([^<]*)</span>', nav)
    print("\n  rendered nav:")
    for href, label in rendered:
        print(f"    {label:<18} -> {href}")
    labels = [l for _, l in rendered]
    for _, want_label, _ in WANT[:-1]:
        assert any(want_label.replace("'", "&#39;") == l or want_label == l for l in labels), \
            f"{want_label} missing from rendered nav: {labels}"
    print("\napplied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
