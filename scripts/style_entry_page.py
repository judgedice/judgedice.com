# -*- coding: utf-8 -*-
"""Entry (blog post) page: reverse the cover title, rebuild the breadcrumb, indent pullquotes.

Three changes Judge asked for on /blog/entries-1/<post>:

  1. the cover title was rendering in ink over the photo, because the Entries
     block paints .o_wblog_post_page_cover h1 with var(--ink). The blog index
     banner escapes that through its .text-white rules; the post cover has no
     such class, so it stayed dark. Scoped to #o_wblog_post_top, which wraps the
     post cover and does not exist on the index.
  2. the breadcrumb read `entries... / A midlife mark`. It now leads with Home
     and carries the post's first tag as the category, linked to that tag's
     filter. Posts without a tag skip the segment. Home and the category are
     desktop-only: four segments do not fit a phone, and Odoo already hides the
     title there behind a back-chevron.
  3. pullquotes gain a left margin, so the whole quote indents, vermilion rule
     included, rather than only its text.

The blog name is left exactly as Judge wrote it ("entries...") and the divider
is left as Bootstrap's.

Idempotent: the view is keyed and skipped if present, the CSS block is
delimited and refreshed in place. Dry-run by default; pass --apply to write.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2
CSS_START = "/* jd-post-page:start */"
CSS_END = "/* jd-post-page:end */"

VIEW_KEY = "website_blog.jd_post_breadcrumb"
VIEW_PARENT = "website_blog.post_breadcrumbs"
VIEW_NAME = "Entry breadcrumb: lead with Home, carry the category"
VIEW_ARCH = '''<data inherit_id="website_blog.post_breadcrumbs" name="Entry breadcrumb: lead with Home, carry the category" active="True">
    <xpath expr="//li[@class='breadcrumb-item']" position="before">
        <li class="breadcrumb-item d-none d-lg-inline"><a href="/">Home</a></li>
    </xpath>
    <xpath expr="//li[contains(@class, 'active')]" position="before">
        <t t-if="blog_post.tag_ids">
            <t t-set="jd_bc_tag" t-value="blog_post.tag_ids[0]"/>
            <li class="breadcrumb-item d-none d-lg-inline">
                <a t-attf-href="#{blog_url(tag=slug(jd_bc_tag), date_begin=False, date_end=False)}" t-out="jd_bc_tag.name"/>
            </li>
        </t>
    </xpath>
</data>'''

CSS = '''
/* jd-post-page:start */
/* ---- Entry (blog post) page ---- */
/* The title sits on the cover photo, so it has to reverse out of it. The
   Entries block above paints this h1 with var(--ink); the index banner escapes
   that via its .text-white rules, the post cover has no such class. Scoped to
   #o_wblog_post_top, which wraps the post cover and is absent on the index. */
#wrap #o_wblog_post_top .o_wblog_post_name{
  color:var(--paper)!important;
  text-shadow:0 2px 18px rgba(0,0,0,.45);
}
#wrap #o_wblog_post_top .o_wblog_post_subtitle{
  color:var(--paper)!important;
  opacity:.92;
  text-shadow:0 1px 12px rgba(0,0,0,.5);
}

/* breadcrumb: quieter and smaller than the prose it sits above */
#wrap #o_wblog_post_content .breadcrumb{
  font-family:var(--font-serif);
  font-size:var(--text-meta);
  font-weight:var(--weight-regular);
  margin-bottom:var(--space-4);
}
#wrap #o_wblog_post_content .breadcrumb a,
#wrap #o_wblog_post_content .breadcrumb .active span,
#wrap #o_wblog_post_content .breadcrumb .breadcrumb-item::before{
  color:var(--ink-faint);
}
#wrap #o_wblog_post_content .breadcrumb a{text-decoration:none;}
#wrap #o_wblog_post_content .breadcrumb a:hover{color:var(--vermilion);}

/* pullquote: indent the whole quote, vermilion rule and all, not just the text */
#wrap #o_wblog_post_content blockquote{margin-left:2rem;}
/* jd-post-page:end */
'''


def main(apply_):
    uid, call = connect()
    print("dry-run (pass --apply to write)\n" if not apply_ else "APPLYING\n")

    # 1. breadcrumb view
    ET.fromstring(VIEW_ARCH)  # hard rule 4
    existing = call("ir.ui.view", "search_read", [["key", "=", VIEW_KEY]], fields=["id"])
    if existing:
        print("  %-36s exists as view %s" % (VIEW_KEY, existing[0]["id"]))
    else:
        parent = call("ir.ui.view", "search_read",
                      [["key", "=", VIEW_PARENT], ["website_id", "=", False]], fields=["id"])
        assert parent, "parent view not found: %s" % VIEW_PARENT
        if apply_:
            vid = call("ir.ui.view", "create", {
                "key": VIEW_KEY, "name": VIEW_NAME, "type": "qweb", "mode": "extension",
                "inherit_id": parent[0]["id"], "website_id": SITE,
                "active": True, "priority": 16, "arch": VIEW_ARCH,
            })
            back = call("ir.ui.view", "read", [vid], fields=["website_id", "arch_db"])[0]
            assert back["website_id"][0] == SITE, "view %s is not on site 2!" % vid
            ET.fromstring(back["arch_db"])
            print("  %-36s created as view %s, verified" % (VIEW_KEY, vid))
        else:
            print("  %-36s would-create (inherits %s=%s)"
                  % (VIEW_KEY, VIEW_PARENT, parent[0]["id"]))

    # 2. css
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if CSS_START in head:
        assert CSS_END in head, "css start marker without end marker - fix by hand"
        pre, rest = head.split(CSS_START, 1)
        want = pre + CSS.strip("\n") + rest.split(CSS_END, 1)[1]
        verb = "refresh"
    else:
        assert "</style>" in head
        want = head.replace("</style>", CSS + "</style>", 1)
        verb = "append"

    if want == head:
        print("\n  entry-page css already up to date")
        return 0
    if not apply_:
        print("\n  would-%s %d chars of entry-page css" % (verb, len(CSS)))
        return 0

    fresh = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    assert fresh == head, ("custom_code_head changed between read and write - "
                           "another session or the builder is editing. Re-run; nothing written.")
    call("website", "write", [SITE], {"custom_code_head": want})
    back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
    assert back == want, "readback differs from what we wrote - concurrent write landed"
    print("\n  %sed %d chars of entry-page css, verified byte-for-byte" % (verb, len(CSS)))
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
