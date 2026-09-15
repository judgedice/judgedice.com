# -*- coding: utf-8 -*-
"""Retire site 2's redundant website.record_cover override (view 2734).

The override is byte-identical to Odoo's stock view (1362) apart from two
attributes the website builder baked into it: a hardcoded
`style="background-image: url(...)"` naming whichever cover was last opened in
the editor, plus a stray editor-only `o_we_snippet_autofocus` class.

They are inert at render - the sibling t-attf-style/t-attf-class win - so the
covers look right. The damage is upstream of that: every builder visit to a
cover rewrites them, so the snapshot churns, and site 2 is pinned to a frozen
fork of a stock template it never meant to customise, missing any upstream fix.

Stripping the attributes would only reset the clock. The override itself is the
bug, so this deactivates it and lets site 2 fall back to stock.

Deactivating rather than unlinking keeps it reversible, and `ir.ui.view.search`
excludes inactive records, so it also leaves the snapshot. The arch stays in git
history at snapshot/views/2734-website.record_cover.xml if it is ever wanted.

Verifies the live page after the write and ROLLS BACK automatically if covers
stop rendering. Dry-run by default; pass --apply to write.
"""
import sys, os, re, ssl, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE, VIEW, STOCK = 2, 2734, 1362
PAGE = "https://www.judgedice.com/blog/entries-1"
CTX = ssl.create_default_context()


def fetch(url):
    req = urllib.request.Request(url + "?cachebust=%d" % os.getpid(),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=CTX, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")


def covers_ok(html):
    """The index must still render one cover div per post, and the post that has
    a cover image must still point at its own attachment (1480), not a default."""
    divs = re.findall(r'class="o_record_cover_component o_record_cover_image[^"]*"', html)
    has_real = "/web/image/1480-" in html
    has_none = "background-image: none;" in html
    return len(divs), has_real, has_none


def main(apply_):
    uid, call = connect()
    print("dry-run (pass --apply to write)\n" if not apply_ else "APPLYING\n")

    v = call("ir.ui.view", "read", [VIEW], ["key", "website_id", "active", "arch_db"])[0]
    assert v["website_id"] and v["website_id"][0] == SITE, "view %s is not on site 2!" % VIEW
    assert v["key"] == "website.record_cover", "view %s is not record_cover" % VIEW
    if not v["active"]:
        print("  view %s already inactive - nothing to do" % VIEW)
        return 0

    stock = call("ir.ui.view", "read", [STOCK], ["key", "website_id", "active"])[0]
    assert stock["key"] == "website.record_cover" and not stock["website_id"], "stock view missing"
    assert stock["active"], "stock view %s is inactive - falling back would break covers" % STOCK
    print("  stock fallback %s is present and active" % STOCK)

    before = covers_ok(fetch(PAGE))
    print("  before: %d cover divs, real image=%s, empty cover=%s" % before)
    assert before[0] > 0 and before[1], "baseline is already broken - stopping"

    if not apply_:
        print("\n  would-deactivate view %s (site 2 falls back to stock %s)" % (VIEW, STOCK))
        return 0

    call("ir.ui.view", "write", [VIEW], {"active": False})
    print("  deactivated view %s" % VIEW)

    after = covers_ok(fetch(PAGE))
    print("  after : %d cover divs, real image=%s, empty cover=%s" % after)

    if after != before:
        call("ir.ui.view", "write", [VIEW], {"active": True})
        print("\n  ROLLED BACK - covers changed, view %s reactivated. Nothing lost." % VIEW)
        return 1

    print("\n  covers render identically from stock. Override retired.")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
