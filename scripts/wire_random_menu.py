#!/usr/bin/env python3
"""Point the "It's on Random" menu item at a random quote page.

Odoo Online cannot deploy a controller, so there is nothing to redirect
through. Instead the menu record carries a sentinel url, /random, and the two
places that render a menu link swap it for a real, published /random-N page at
render time. The href in the delivered HTML is always a genuine page, so there
is no redirect, no JavaScript and no flash - and the back button behaves.

The pick excludes the page you are already on, so clicking it from /random-2
sends you somewhere else. It re-rolls on every page render.

Two surfaces, because the desktop nav and the mobile drawer render from
different templates:
  - view 2035, the site's own header, for the desktop .jd-nav
  - a new site-2 view inheriting the SHARED website.submenu (1259), which the
    drawer renders through. The shared view itself is never edited - site 1
    uses it too.

Keyed on the url, not on position, so reordering the menu cannot promote the
wrong item - the same rule the /appointment CTA already follows.

Dry-run by default; --apply writes, verifies the live site, and rolls back
automatically if anything stops rendering.
"""
import argparse
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
MENU_ID = 9
SENTINEL_URL = "/random"
SUBMENU_KEY = "website.jd_random_submenu_link"

# Short-circuits on the url test, so the search only runs for the one item.
POOL = ("submenu.url == '%s' and [p.url for p in request.env['website.page']"
        ".sudo().search([('url','=like','/random-%%'),('is_published','=',True),"
        "('website_id','=',website.id)])] or []") % SENTINEL_URL
OTHER = "[u for u in jd_pool if u != request.httprequest.path]"
PICK = "jd_other or jd_pool"
HREF = "jd_pick and jd_pick[datetime.datetime.now().microsecond %% len(jd_pick)] or %s"

SUBMENU_ARCH = f"""<data inherit_id="website.submenu" name="Judge Random Menu Link" active="True">
    <xpath expr="//t[@t-set='show_dropdown']" position="before">
        <t t-set="jd_pool" t-value="{POOL}"/>
        <t t-set="jd_other" t-value="{OTHER}"/>
        <t t-set="jd_pick" t-value="{PICK}"/>
    </xpath>
    <xpath expr="//a[@t-att-href='submenu._clean_url()']" position="attributes">
        <attribute name="t-att-href">{HREF % 'submenu._clean_url()'}</attribute>
    </xpath>
</data>"""

OLD_LOOP = """                <t t-foreach="website.menu_id.child_id" t-as="submenu">"""
NEW_LOOP = f"""                <t t-foreach="website.menu_id.child_id" t-as="submenu">
                    <!-- The "It's on Random" item carries the sentinel url /random.
                         No page lives there; it is swapped for a real published
                         /random-N here, excluding the one you are already on. -->
                    <t t-set="jd_pool" t-value="{POOL}"/>
                    <t t-set="jd_other" t-value="{OTHER}"/>
                    <t t-set="jd_pick" t-value="{PICK}"/>"""

OLD_HREF = """<a t-else="" t-att-href="submenu.url" class="jd-link">"""
NEW_HREF = f"""<a t-else="" t-att-href="{HREF % 'submenu.url'}" class="jd-link">"""


def fetch(path):
    req = urllib.request.Request(f"https://www.judgedice.com{path}",
                                 headers={"Cache-Control": "no-cache"})
    try:
        return urllib.request.urlopen(req, timeout=40).getcode()
    except urllib.error.HTTPError as e:
        return e.code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    uid, call = connect()

    menu = call("website.menu", "read", [MENU_ID], ["id", "name", "url", "website_id"])[0]
    assert menu["website_id"][0] == SITE, menu
    hdr = call("ir.ui.view", "read", [2035], ["id", "key", "arch_db", "website_id"])[0]
    assert hdr["website_id"][0] == SITE, hdr

    new_arch = hdr["arch_db"]
    if OLD_LOOP in new_arch:
        assert new_arch.count(OLD_LOOP) == 1
        new_arch = new_arch.replace(OLD_LOOP, NEW_LOOP)
    if OLD_HREF in new_arch:
        assert new_arch.count(OLD_HREF) == 1
        new_arch = new_arch.replace(OLD_HREF, NEW_HREF)
    ET.fromstring(new_arch)

    existing = call("ir.ui.view", "search", [["key", "=", SUBMENU_KEY]])
    ET.fromstring(SUBMENU_ARCH)

    print(f"menu {MENU_ID} '{menu['name']}': {menu['url']} -> {SENTINEL_URL}"
          f"{'  (already)' if menu['url'] == SENTINEL_URL else ''}")
    print(f"view 2035 header: {'patched' if new_arch != hdr['arch_db'] else 'already patched'}")
    print(f"submenu override {SUBMENU_KEY}: "
          f"{'update ' + str(existing) if existing else 'create (site 2, inherits shared 1259)'}")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    before_menu, before_arch = menu["url"], hdr["arch_db"]
    created = None
    try:
        # page_id must go too. Rewriting only the url leaves the item still
        # linked to whatever page it used to point at, and Odoo cascades a
        # page deletion to its menus - deleting that old page would take this
        # item out of the nav with it.
        call("website.menu", "write", [MENU_ID],
             {"url": SENTINEL_URL, "page_id": False})
        if new_arch != before_arch:
            call("ir.ui.view", "write", [2035], {"arch": new_arch})
        if existing:
            call("ir.ui.view", "write", existing, {"arch": SUBMENU_ARCH, "active": True})
        else:
            r = call("ir.ui.view", "create", [{
                "name": "Judge Random Menu Link", "type": "qweb",
                "key": SUBMENU_KEY, "arch": SUBMENU_ARCH, "website_id": SITE,
                "inherit_id": 1259, "mode": "extension", "active": True}])
            created = r[0] if isinstance(r, list) else r
        time.sleep(3)

        bad = [(p, c) for p in ("/", "/work", "/offerings", "/blog", "/random-3")
               for c in [fetch(p)] if c != 200]
        if bad:
            raise RuntimeError(f"pages stopped rendering: {bad}")
        print("  live check: / /work /offerings /blog /random-3 all 200")
    except Exception as e:
        print(f"\nFAILED: {e}\n  rolling back...")
        call("website.menu", "write", [MENU_ID], {"url": before_menu})
        call("ir.ui.view", "write", [2035], {"arch": before_arch})
        if created:
            call("ir.ui.view", "unlink", [created])
        elif existing:
            call("ir.ui.view", "write", existing, {"active": False})
        print("  rolled back.")
        return 3

    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
