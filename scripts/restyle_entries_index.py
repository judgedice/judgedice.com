# -*- coding: utf-8 -*-
"""Restyle the Entries index (/blog/entries-1) cards and hero search.

Three changes Judge asked for, built as four small site-2 inherited views over
Odoo's stock blog templates plus one CSS block, so the website builder's own
blog options (list view, cards design, sidebar) keep working:

  1. the story title moves off the card body and into the cover image, reversed
     out of a scrim, with the post date trailing it. The stock byline block
     ("Half a Glass, Judge DiCesaro") is what it replaces - it read the same on
     every card, so it wasn't earning the space. Title stays in Anton; no third
     typeface is loaded.
  2. the category tag becomes a smaller eyebrow sitting above the teaser.
  3. the search bar moves out of its own nav band and into the hero, near the
     top edge, prompting "find an entry". Below 768px it drops back under the
     hero rather than crowding the blog title.

Because the title and date now live in the cover, the card's own heading and
date footer are removed - otherwise each would print twice.

Idempotent: views are keyed and skipped if they already exist on site 2, the
CSS append is sentinel-guarded. Dry-run by default; pass --apply to write.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2
CSS_START = "/* jd-entries-index:start */"
CSS_END = "/* jd-entries-index:end */"

# key -> (parent view key, human name, arch)
VIEWS = [
    (
        "website_blog.jd_cover_title_overlay",
        "website_blog.post_cover_image",
        "Entries card: title + date reversed into the cover",
        '''<data inherit_id="website_blog.post_cover_image" name="Entries card: title + date reversed into the cover" active="True">
    <xpath expr="//t[@t-call='website_blog.post_author']" position="replace">
        <div class="jd-cover-meta o_list_cover o_not_editable position-relative d-flex align-items-baseline flex-wrap w-100">
            <span class="jd-cover-title" t-out="blog_post.name"/>
            <time class="jd-cover-date" t-field="blog_post.post_date" t-options="{'widget': 'datetime', 'date_only': 'true', 'format': 'medium'}"/>
        </div>
    </xpath>
</data>''',
    ),
    (
        "website_blog.jd_posts_loop_no_dup_meta",
        "website_blog.posts_loop",
        "Entries card: drop heading + date footer (both now in the cover)",
        '''<data inherit_id="website_blog.posts_loop" name="Entries card: drop heading + date footer (both now in the cover)" active="True">
    <xpath expr="//div[contains(@t-att-class, 'card-body px-2 py-0 mb-2')]/t[@t-call='website_blog.post_heading']" position="replace"/>
    <xpath expr="//div[t[@t-call='website_blog.post_info']][contains(@t-attf-class, 'o_wblog_normalize_font')]" position="replace"/>
</data>''',
    ),
    (
        "website_blog.jd_tags_above_teaser",
        "website_blog.post_teaser",
        "Entries card: category eyebrow above the teaser",
        '''<data inherit_id="website_blog.post_teaser" name="Entries card: category eyebrow above the teaser" active="True">
    <xpath expr="//a[@class='text-reset text-decoration-none']" position="before">
        <xpath expr="//div[contains(@class, 'o_wblog_post_short_tag_section')]" position="move"/>
    </xpath>
</data>''',
    ),
    (
        "website_blog.jd_search_in_hero",
        "website_blog.blog_post_short",
        "Entries index: search bar inside the hero",
        '''<data inherit_id="website_blog.blog_post_short" name="Entries index: search bar inside the hero" active="True">
    <xpath expr="//div[@id='o_wblog_blog_top']" position="inside">
        <xpath expr="//t[@t-call='website_blog.blogs_nav']" position="move"/>
    </xpath>
    <xpath expr="//t[@t-call='website_blog.blogs_nav']" position="inside">
        <t t-set="additionnal_classes" t-value="''"/>
        <t t-set="placeholder">find an entry</t>
    </xpath>
</data>''',
    ),
]

CSS = '''
/* jd-entries-index:start */
/* ---- Entries index: title in the cover, search in the hero ---- */
/* NB these are ID selectors on purpose: the DOM carries o_wblog_posts_loop and
   o_wblog_blog_top as ids, not classes. */

/* The cover carries no filter layer, so reversed type needs its own ground:
   a scrim that fades out before it reaches the middle of the picture. */
#wrap #o_wblog_posts_loop .jd-cover-meta{
  margin-top:auto;
  gap:.7rem;
  padding:3.25rem 1.1rem 1rem;
  background:linear-gradient(to top,rgba(16,12,8,.74) 0%,rgba(16,12,8,.46) 46%,rgba(16,12,8,0) 100%);
}
#wrap #o_wblog_posts_loop .jd-cover-title{
  font-family:var(--font-display);
  font-weight:var(--weight-regular);
  text-transform:uppercase;
  font-size:clamp(1.25rem,2.1vw,1.625rem);
  line-height:1.04;
  letter-spacing:.005em;
  color:var(--paper);
  text-shadow:0 1px 14px rgba(0,0,0,.55);
}
#wrap #o_wblog_posts_loop .jd-cover-date{
  font-family:var(--font-serif);
  font-size:var(--text-meta);
  text-transform:uppercase;
  letter-spacing:var(--tracking-label);
  color:var(--paper);
  opacity:.72;
  white-space:nowrap;
  text-shadow:0 1px 10px rgba(0,0,0,.6);
}

/* category eyebrow: smaller, and now sitting above the teaser */
#wrap #o_wblog_posts_loop .o_wblog_post_short_tag_section{padding-top:0;margin-bottom:.3rem;}
#wrap #o_wblog_posts_loop .o_wblog_post_short_tag_section .o_tag{
  font-size:.6875rem;
  letter-spacing:var(--tracking-label);
  padding:.22rem .5rem;
}

/* search bar lifted into the hero, just inside its top edge */
#wrap #o_wblog_blog_top{position:relative;}
/* Odoo's theme paints .navbar solid white; over the hero it has to be glass. */
#wrap #o_wblog_blog_top > nav.navbar{
  position:absolute;top:var(--space-6);left:0;right:0;z-index:3;
  background:transparent!important;border:0!important;
  padding-top:0!important;padding-bottom:0!important;
}
#wrap #o_wblog_blog_top .o_searchbar_form{max-width:24rem;margin-left:auto;margin-right:0;}
#wrap #o_wblog_blog_top .oe_search_box,
#wrap #o_wblog_blog_top .oe_search_button{
  background:color-mix(in srgb,var(--paper) 90%,transparent)!important;
  border:1px solid var(--line-strong)!important;
  border-radius:0;
  color:var(--ink);
}
#wrap #o_wblog_blog_top .oe_search_button{border-left:0!important;}
#wrap #o_wblog_blog_top .oe_search_box{
  font-family:var(--font-serif);font-size:var(--text-small);
}
#wrap #o_wblog_blog_top .oe_search_box::placeholder{
  color:var(--ink-soft);opacity:1;font-style:italic;
}
/* on a phone the hero is short and the blog title fills it - let the search
   fall back below the hero instead of sitting on top of the title */
@media (max-width:767.98px){
  #wrap #o_wblog_blog_top > nav.navbar{position:static;padding:1rem 0 0!important;background:var(--paper)!important;}
  #wrap #o_wblog_blog_top .o_searchbar_form{max-width:none;margin-left:0;}
}
/* jd-entries-index:end */
'''


def main(apply_):
    uid, call = connect()
    print("dry-run (pass --apply to write)\n" if not apply_ else "APPLYING\n")

    # 1. the four inherited views
    for key, parent_key, name, arch in VIEWS:
        ET.fromstring(arch)  # hard rule 4: well-formed before it goes anywhere

        existing = call("ir.ui.view", "search_read", [["key", "=", key]],
                        fields=["id", "website_id"])
        if existing:
            print("  %-44s exists as view %s" % (key, existing[0]["id"]))
            continue

        parent = call("ir.ui.view", "search_read",
                      [["key", "=", parent_key], ["website_id", "=", False]],
                      fields=["id"])
        assert parent, "parent view not found: %s" % parent_key

        if apply_:
            vid = call("ir.ui.view", "create", {
                "key": key, "name": name, "type": "qweb", "mode": "extension",
                "inherit_id": parent[0]["id"], "website_id": SITE,
                "active": True, "priority": 16, "arch": arch,
            })
            back = call("ir.ui.view", "read", [vid], fields=["website_id", "arch_db"])[0]
            assert back["website_id"][0] == SITE, "view %s is not on site 2!" % vid
            assert ET.fromstring(back["arch_db"]) is not None
            print("  %-44s created as view %s, verified" % (key, vid))
        else:
            print("  %-44s would-create (inherits %s=%s)" % (key, parent_key, parent[0]["id"]))

    # 2. the CSS
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""

    # One-time migration: the first install of this block predated the
    # start/end markers. It was appended last, so it runs from its header
    # comment to just before </style>. Reclaim it so the marker path can own it.
    LEGACY = "/* ---- Entries index: title in the cover, search in the hero ---- */"
    if CSS_START not in head and LEGACY in head:
        pre, rest = head.split(LEGACY, 1)
        assert "</style>" in rest, "unexpected shape - fix by hand"
        head = pre + "</style>" + rest.split("</style>", 1)[1]
        print("  reclaimed the unmarked first-install css block")
        if apply_:
            call("website", "write", [SITE], {"custom_code_head": head})
            back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
            assert back == head, "migration readback differs - a concurrent write landed"

    if CSS_START in head:
        # already installed: replace our own block in place so the script stays
        # the single source of this CSS and re-runs pick up edits.
        assert CSS_END in head, "css start marker without end marker - fix by hand"
        pre, rest = head.split(CSS_START, 1)
        _, post = rest.split(CSS_END, 1)
        want = pre + CSS.strip("\n") + post
        if want == head:
            print("\n  entries-index css already up to date")
        elif apply_:
            call("website", "write", [SITE], {"custom_code_head": want})
            back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
            assert back == want, "css readback differs - a concurrent write landed"
            print("\n  refreshed entries-index css in place (%d chars), verified" % len(CSS))
        else:
            print("\n  would-refresh entries-index css in place (%d chars)" % len(CSS))
    elif apply_:
        assert "</style>" in head
        # custom_code_head is one field read-modify-written whole, so a second
        # session appending at the same moment would be silently clobbered.
        # Re-read immediately before writing, then assert the result is exactly
        # what we intended - if anyone landed in between, this fails loudly
        # instead of eating their change.
        fresh = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
        assert fresh == head, (
            "custom_code_head changed underneath us between read and write - "
            "another session is editing. Re-run; nothing was written.")
        want = fresh.replace("</style>", CSS + "</style>", 1)
        call("website", "write", [SITE], {"custom_code_head": want})
        back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
        assert CSS_START in back, "css readback failed"
        assert back == want, (
            "custom_code_head readback differs from what we wrote - a "
            "concurrent write landed. Check the field before re-running.")
        print("\n  appended %d chars of entries-index css, verified byte-for-byte" % len(CSS))
    else:
        print("\n  would-append %d chars of entries-index css" % len(CSS))

    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
