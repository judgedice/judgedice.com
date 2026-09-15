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

Then a second round: drop the bouncing jump arrow and the clock icon, weight up
the subtitle and the pullquote, rename the blog to "Entries", and cut the byline
to "Judge".

That byline is not a name field. Partner 3 is already named "Judge DiCesaro" —
"Half a Glass, Judge DiCesaro" is Odoo's composed display_name, because the
contact sits under the Half a Glass parent company. That partner carries a sale
order, so it is left untouched and the byline is overridden in the template. The
consequence is that the byline is now fixed text: a guest author would also read
"Judge".

The divider is left as Bootstrap's.

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

BYLINE_KEY = "website_blog.jd_post_author_byline"
BYLINE_PARENT = "website_blog.post_author"
BYLINE_NAME = "Entry byline: just 'Judge'"
BYLINE_ARCH = '''<data inherit_id="website_blog.post_author" name="Entry byline: just 'Judge'" active="True">
    <xpath expr="//span[@t-field='blog_post.author_id']" position="replace">
        <span t-if="editable">Judge</span>
    </xpath>
    <xpath expr="//span[@t-out='blog_post.author_name']" position="replace">
        <span t-else="">Judge</span>
    </xpath>
</data>'''

BLOG_ID, BLOG_NAME = 1, "Entries"

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

/* The pull quote on an entry is the standfirst, p.jd-standfirst - there are no
   <blockquote>s in these posts. It also has to out-specify
   `#wrap #o_wblog_post_content p` (two ids), which is what actually sets its
   size today and why the .jd-standfirst rule further up never bites; hence the
   tag+class on the end. Indented as a whole, rule included, and given size and
   weight so it reads as a pull quote rather than a faint caption. */
#wrap #o_wblog_post_content p.jd-standfirst{
  font-size:1.3125rem;
  font-weight:var(--weight-regular);
  line-height:1.5;
  margin-left:2rem;
  color:var(--ink-soft);
}

/* real <blockquote>s, should an entry ever use one, get the same treatment */
#wrap #o_wblog_post_content blockquote{margin-left:2rem;}
#wrap #o_wblog_post_content blockquote p{
  font-size:1.3125rem;
  font-weight:var(--weight-regular);
  line-height:1.5;
}

/* the subtitle carries a little more weight against the photo behind it */
#wrap #o_wblog_post_top .o_wblog_post_subtitle{font-weight:var(--weight-medium);}

/* Odoo's bouncing scroll-down arrow, and the clock glyph in front of the date.
   Hidden rather than removed from the templates: both are stock options Judge
   may want back, and display:none takes them out of the accessibility tree too,
   so neither is announced. */
#wrap #o_wblog_post_content_jump{display:none!important;}
#wrap #o_wblog_post_info .fa-clock-o{display:none!important;}

/* Body links read as highlighter strokes rather than coloured text. The colour
   is the one links already compute to, #65435C - Odoo's theme link colour, not
   a design-system token; --jd-link-hl is the single place to change it, e.g. to
   the brand vermilion 203,65,39.

   The band is a gradient rather than a plain background-color so its height is
   controllable: a background-color fills the whole inline content box. It runs
   .52em to 1.0em, which is x-height to baseline, so it clears the ascenders
   above and stops before the descenders below - the mark sits inside the word
   rather than boxing it. box-decoration-break keeps the padding and the band on
   every line a link wraps onto, not just the first and last.

   The text itself is ink, the same colour as the body, so the highlight is the
   entire signal. It rests at .20 and deepens to .38 on hover - the band is what
   changes, not the type: bolding text on hover reflows the paragraph under the
   reader's cursor.

   The entry CTA keeps its own vermilion-rule treatment, so it is excluded. */
#wrap #o_wblog_post_content .o_wblog_post_content_field p:not(.jd-entry-cta) a{
  --jd-link-hl:101,67,92;
  background-image:linear-gradient(rgba(var(--jd-link-hl),.20),rgba(var(--jd-link-hl),.20));
  background-repeat:no-repeat;
  color:var(--ink);
  background-size:100% .48em;
  background-position:0 .52em;
  padding:0 .28em;
  border-radius:2px;
  box-decoration-break:clone;
  -webkit-box-decoration-break:clone;
}
#wrap #o_wblog_post_content .o_wblog_post_content_field p:not(.jd-entry-cta) a:hover{
  background-image:linear-gradient(rgba(var(--jd-link-hl),.38),rgba(var(--jd-link-hl),.38));
}
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

    # 2. byline view
    ET.fromstring(BYLINE_ARCH)
    existing = call("ir.ui.view", "search_read", [["key", "=", BYLINE_KEY]], fields=["id"])
    if existing:
        print("  %-36s exists as view %s" % (BYLINE_KEY, existing[0]["id"]))
    else:
        parent = call("ir.ui.view", "search_read",
                      [["key", "=", BYLINE_PARENT], ["website_id", "=", False]], fields=["id"])
        assert parent, "parent view not found: %s" % BYLINE_PARENT
        if apply_:
            vid = call("ir.ui.view", "create", {
                "key": BYLINE_KEY, "name": BYLINE_NAME, "type": "qweb", "mode": "extension",
                "inherit_id": parent[0]["id"], "website_id": SITE,
                "active": True, "priority": 16, "arch": BYLINE_ARCH,
            })
            back = call("ir.ui.view", "read", [vid], fields=["website_id", "arch_db"])[0]
            assert back["website_id"][0] == SITE, "view %s is not on site 2!" % vid
            ET.fromstring(back["arch_db"])
            print("  %-36s created as view %s, verified" % (BYLINE_KEY, vid))
        else:
            print("  %-36s would-create (inherits %s=%s)"
                  % (BYLINE_KEY, BYLINE_PARENT, parent[0]["id"]))

    # 3. blog name. Both spellings slugify to "entries-1", so the URL does not move.
    blog = call("blog.blog", "read", [BLOG_ID], ["name", "website_id"])[0]
    assert blog["website_id"][0] == SITE, "blog %s is not on site 2!" % BLOG_ID
    if blog["name"] == BLOG_NAME:
        print("  blog %s already named %r" % (BLOG_ID, BLOG_NAME))
    elif apply_:
        call("blog.blog", "write", [BLOG_ID], {"name": BLOG_NAME})
        back = call("blog.blog", "read", [BLOG_ID], ["name"])[0]["name"]
        assert back == BLOG_NAME, "blog rename readback failed"
        print("  blog %s renamed %r -> %r, verified" % (BLOG_ID, blog["name"], BLOG_NAME))
    else:
        print("  would-rename blog %s %r -> %r" % (BLOG_ID, blog["name"], BLOG_NAME))

    # 4. css
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
