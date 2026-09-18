#!/usr/bin/env python3
"""301 /home -> / , now that the Home Life page is gone.

/home was published and indexed, so it has search results and possibly inbound
links pointing at it. Without this it answers 404. Odoo Online cannot take a
controller, but website.rewrite is a data record, so the redirect is ordinary
site state rather than code.

Scoped to website 2: site 1 has its own URL space and must not inherit this.

Dry-run by default; --apply writes and checks the live response.
"""
import argparse
import sys
import time
import urllib.error
import urllib.request

from odoo import connect

SITE = 2
FROM, TO = "/home", "/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    # the page really must be gone, or the redirect would shadow a live page
    assert not call("website.page", "search",
                    [["url", "=", FROM], ["website_id", "=", SITE]]), \
        f"{FROM} still exists as a page — refusing to shadow it"

    existing = call("website.rewrite", "search",
                    [["url_from", "=", FROM], ["website_id", "=", SITE]],
                    context={"active_test": False})
    print(f"  existing rewrite for {FROM}: {existing or 'none'}")
    print(f"  plan: 301 {FROM} -> {TO} on website {SITE}")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    vals = {"name": "Home Life retired", "redirect_type": "301",
            "url_from": FROM, "url_to": TO, "website_id": SITE, "active": True}
    if existing:
        call("website.rewrite", "write", existing, vals)
        rid = existing[0]
    else:
        r = call("website.rewrite", "create", [vals])
        rid = r[0] if isinstance(r, list) else r
    back = call("website.rewrite", "read", [rid],
                ["id", "redirect_type", "url_from", "url_to", "website_id", "active"])[0]
    assert back["website_id"][0] == SITE and back["redirect_type"] == "301", back
    print(f"  wrote rewrite {rid}: {back}")

    time.sleep(3)
    req = urllib.request.Request("https://www.judgedice.com" + FROM,
                                 headers={"Cache-Control": "no-cache"})

    class NoFollow(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    try:
        code = urllib.request.build_opener(NoFollow).open(req, timeout=40).getcode()
        loc = None
    except urllib.error.HTTPError as e:
        code, loc = e.code, e.headers.get("Location")
    print(f"  live {FROM} -> http {code} Location: {loc}")
    if code != 301:
        print("  WARNING: expected 301")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
