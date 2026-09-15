# -*- coding: utf-8 -*-
"""Fix the dead selectors in the Entries CSS block of website[2].custom_code_head.

The original Entries rules were written against `.o_wblog_blog_top` and
`.o_wblog_posts_loop`, but the DOM carries both of those as *ids*, so none of
those rules has ever applied - the cards have been rendering close to Odoo
defaults. One more typo rides along: `.o_wblog_post_title` is the blog header's
class; the card title is `.o_blog_post_title`.

This is not a cosmetic no-op. Correcting the selectors switches on styling that
has never been seen, most visibly a 2px ink rule above every card and the loss
of the cover shadow. Verify the result visually, don't just trust the write.

Rules that still match nothing after correction are left in place on purpose:
they match nothing *today* because the blog is in grid view with stats off, and
would come back with a builder toggle.

Idempotent (re-running finds nothing left to fix). Dry-run by default;
pass --apply to write.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2

# (old, new, what fixing it turns on)
FIXES = [
    ("#wrap .o_wblog_blog_top{",
     "#wrap #o_wblog_blog_top{",
     "hero: paper ground + bottom hairline"),
    ("#wrap .o_wblog_blog_top h1,",
     "#wrap #o_wblog_blog_top h1,",
     "nothing new - the rule's other half already matched that h1"),
    ("#wrap .o_wblog_posts_loop article{",
     "#wrap #o_wblog_posts_loop article{",
     "2px ink rule above every card, shadow off  <- the visible one"),
    ("#wrap .o_wblog_posts_loop article img{",
     "#wrap #o_wblog_posts_loop article img{",
     "nothing today - covers are background-images, not <img>"),
    ("#wrap .o_wblog_posts_loop .o_wblog_post_title{",
     "#wrap #o_wblog_posts_loop .o_blog_post_title{",
     "nothing today - card title now lives in the cover; returns in list view"),
    ("#wrap .o_wblog_posts_loop a{",
     "#wrap #o_wblog_posts_loop a{",
     "text-decoration:none on card links"),
    ("#wrap .o_wblog_posts_loop small,#wrap .o_wblog_posts_loop .text-muted{",
     "#wrap #o_wblog_posts_loop small,#wrap #o_wblog_posts_loop .text-muted{",
     "nothing today - returns with the stats option"),
]


def main(apply_):
    uid, call = connect()
    print("dry-run (pass --apply to write)\n" if not apply_ else "APPLYING\n")

    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    new = head
    todo = 0
    for old, fixed, effect in FIXES:
        if new.count(old) == 1:
            new = new.replace(old, fixed, 1)
            todo += 1
            print("  fix  %s\n       -> %s\n       %s" % (old, fixed, effect))
        elif new.count(fixed) >= 1:
            print("  ok   already fixed: %s" % fixed)
        else:
            print("  WARN not found, skipping: %s" % old)

    if not todo:
        print("\n  nothing to do")
        return 0
    assert ".o_wblog_posts_loop" not in new, "a dead .o_wblog_posts_loop selector survived"
    assert ".o_wblog_blog_top" not in new, "a dead .o_wblog_blog_top selector survived"

    if not apply_:
        print("\n  would-fix %d selectors" % todo)
        return 0

    # custom_code_head is read-modify-written whole; re-read immediately before
    # writing so a concurrent session's edit fails loudly instead of vanishing.
    fresh = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    assert fresh == head, ("custom_code_head changed between read and write - "
                           "another session is editing. Re-run; nothing written.")
    call("website", "write", [SITE], {"custom_code_head": new})
    back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
    assert back == new, "readback differs from what we wrote - concurrent write landed"
    print("\n  fixed %d selectors, verified byte-for-byte" % todo)
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
