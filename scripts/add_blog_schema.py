#!/usr/bin/env python3
"""BlogPosting structured data on each entry.

The static pages carry their JSON-LD in their own arch, but entries share one
template, so this rides on website_blog.blog_post_complete - overridden for
site 2 only. The shared view (2222) is never edited; site 1 uses it too.

Values come from the record through json.dumps, which is what makes this safe:
a title containing a quote or an ampersand is escaped by dumps before QWeb ever
sees it. Probed on a throwaway page first - json.dumps(chr(34)+chr(38)+chr(39))
renders inside a <script> as "\\"\\u0026'" and parses back correctly.

The blog's own URL is derived from the post's rather than read off blog.blog,
which has no website_url field at all - asking for one raises, which is what
made the first working draft of this still 500.

An earlier attempt wrapped those in Markup() to stop QWeb escaping them. Markup
is not in the QWeb sandbox, and every blog post 500'd until it was pulled. That
is why this writes, then immediately fetches four live URLs and rolls itself
back if any of them stops rendering.

Odoo stores datetimes as UTC, so the dates are trimmed to whole seconds and
marked Z - str() on a Datetime yields a space where ISO 8601 wants a T.

Dry-run by default; --apply writes.
"""
import argparse
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
KEY = "website_blog.jd_post_schema"
PARENT = 2222
CHECK = ["/blog/entries-1/for-dad-2", "/blog/entries-1/a-midlife-mark-3",
         "/blog/entries-1/the-ninth-decade-4", "/blog/entries-1/in-service-to-andover-5"]

ARCH = """<data inherit_id="website_blog.blog_post_complete" name="Judge Entry Schema" active="True">
    <xpath expr="." position="inside">
        <t t-set="jd_cover" t-value="json.loads(blog_post.cover_properties or '{}').get('background-image','')"/>
        <t t-set="jd_cover" t-value="jd_cover[5:-2] if jd_cover.startswith('url(') else ''"/>
        <script type="application/ld+json" data-jd-schema="v1">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": <t t-out="json.dumps(website.get_base_url() + blog_post.website_url + '#post')"/>,
  "headline": <t t-out="json.dumps(blog_post.name)"/>,
  "url": <t t-out="json.dumps(website.get_base_url() + blog_post.website_url)"/>,
  "mainEntityOfPage": <t t-out="json.dumps(website.get_base_url() + blog_post.website_url)"/>,
  "datePublished": <t t-out="json.dumps(str(blog_post.post_date or '')[:19].replace(' ', 'T') + 'Z')"/>,
  "dateModified": <t t-out="json.dumps(str(blog_post.write_date or '')[:19].replace(' ', 'T') + 'Z')"/>,
  "description": <t t-out="json.dumps(blog_post.subtitle or '')"/>,
  "author": {"@id": <t t-out="json.dumps(website.get_base_url() + '/#judge')"/>},
  "publisher": {"@id": <t t-out="json.dumps(website.get_base_url() + '/#judge')"/>},
  "isPartOf": {
    "@type": "Blog",
    "@id": <t t-out="json.dumps(website.get_base_url() + blog_post.website_url.rsplit('/', 1)[0] + '#blog')"/>,
    "name": <t t-out="json.dumps(blog_post.blog_id.name)"/>
  }<t t-if="jd_cover">,
  "image": <t t-out="json.dumps(website.get_base_url() + jd_cover)"/></t>
}
        </script>
    </xpath>
</data>"""


def status(path):
    req = urllib.request.Request("https://www.judgedice.com" + path,
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

    ET.fromstring(ARCH)
    shared = call("ir.ui.view", "read", [PARENT], ["id", "key", "website_id"])[0]
    assert shared["website_id"] is False, "parent must be the shared template"
    existing = call("ir.ui.view", "search", [["key", "=", KEY]],
                    context={"active_test": False})
    print(f"  parent {PARENT} ({shared['key']}) is shared — not edited")
    print(f"  site-{SITE} override {KEY}: "
          f"{'update ' + str(existing) if existing else 'create'}")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    created = None
    try:
        if existing:
            call("ir.ui.view", "write", existing, {"arch": ARCH, "active": True})
            vid = existing[0]
        else:
            r = call("ir.ui.view", "create", [{
                "name": "Judge Entry Schema", "type": "qweb", "key": KEY,
                "arch": ARCH, "website_id": SITE, "inherit_id": PARENT,
                "mode": "extension", "active": True}])
            vid = created = r[0] if isinstance(r, list) else r
        time.sleep(4)
        bad = [(p, c) for p in CHECK for c in [status(p)] if c != 200]
        if bad:
            raise RuntimeError(f"entries stopped rendering: {bad}")
        print(f"  view {vid} written; all {len(CHECK)} entries still 200")
    except Exception as e:
        print(f"\nFAILED: {e}\n  rolling back...")
        if created:
            call("ir.ui.view", "unlink", [created])
        elif existing:
            call("ir.ui.view", "write", existing, {"active": False})
        print("  rolled back.")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
