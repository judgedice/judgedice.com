# -*- coding: utf-8 -*-
"""Set SEO meta title + description on site-2 pages and the Entries blog.

Every static page on website 2 shipped with empty meta, so Odoo fell back to
"<page name> | judgedice.com" for the title and, on the homepage, to the stock
placeholder "This is the homepage of the website" for the description. That
placeholder is what rendered in link previews.

Blog *posts* are deliberately left alone: blog.post already falls back to
Judge's own subtitle and the post cover image, which makes a correct card.

Copy rule: descriptions are editorial additions, drawn from Judge's own page
copy. /offerings reuses his standfirst verbatim. Nothing he wrote is edited.

Dry-run by default; --apply writes. Idempotent — re-running is a no-op.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2

# url -> (meta title, meta description)
PAGES = {
    "/": (
        "Judge DiCesaro — Delivering Joy since the turn of the Century",
        "Tribute writer and digital architect. Eulogies, toasts, send-offs and "
        "keepsakes — plus twenty-five years of work inside the Adobe Experience Cloud.",
    ),
    "/work": (
        "Work Life — Judge DiCesaro",
        "Twenty-five years of digital architecture and marketing technology, mostly "
        "inside the Adobe Experience Cloud — from Flash at McKinsey to WillowTree.",
    ),
    "/home": (
        "Home Life — Judge DiCesaro",
        "The exhale. Band practice, New England winters, and a firm belief in the "
        "power of a good lunch — life outside the enterprise tech stack.",
    ),
    "/offerings": (
        "Tribute Writing — Judge DiCesaro",
        "Eulogies, toasts, send-offs, keepsakes — the right words for the moments "
        "that matter, written for the people who have to stand up and say them.",
    ),
    "/connect": (
        "Connect — Judge DiCesaro",
        "Let's talk. Responsive on email, better on a call. For Adobe Experience "
        "Cloud architecture work, or a hairy integration you need to talk through.",
    ),
}

# blog.blog id -> (meta title, meta description)
BLOGS = {
    1: (
        "Entries — Judge DiCesaro",
        "Sample tributes, opinion pieces and reviews by Judge DiCesaro — eulogies "
        "and send-offs, shared as examples of the work.",
    ),
}


def plan(label, current_t, current_d, want_t, want_d):
    """Print one row; return the dict of fields that actually need writing."""
    vals = {}
    if (current_t or "") != want_t:
        vals["website_meta_title"] = want_t
    if (current_d or "") != want_d:
        vals["website_meta_description"] = want_d
    flag = "set" if vals else "ok "
    print("  [%s] %-14s title (%2d) %s" % (flag, label, len(want_t), want_t))
    print("       %-14s desc  (%3d) %s" % ("", len(want_d), want_d))
    return vals


def main(argv):
    apply_ = "--apply" in argv
    uid, call = connect()
    print("set_meta [%s] site=%d" % ("APPLY" if apply_ else "dry-run", SITE))

    todo = []  # (model, id, label, vals)

    pages = call("website.page", "search_read", [["website_id", "=", SITE]],
                 fields=["id", "url", "website_meta_title", "website_meta_description"])
    by_url = {p["url"]: p for p in pages}
    for url, (t, d) in PAGES.items():
        p = by_url.get(url)
        if not p:
            print("  MISS %s — no website.page on site %d" % (url, SITE))
            continue
        vals = plan(url, p["website_meta_title"], p["website_meta_description"], t, d)
        if vals:
            todo.append(("website.page", p["id"], url, vals))

    for bid, (t, d) in BLOGS.items():
        b = call("blog.blog", "read", [bid],
                 ["name", "website_id", "website_meta_title", "website_meta_description"])[0]
        assert b["website_id"] and b["website_id"][0] == SITE, \
            "blog %d is not website %d — refusing" % (bid, SITE)
        vals = plan("blog:" + b["name"], b["website_meta_title"],
                    b["website_meta_description"], t, d)
        if vals:
            todo.append(("blog.blog", bid, b["name"], vals))

    if not todo:
        print("nothing to do — live already matches")
        return 0
    if not apply_:
        print("would write %d record(s); re-run with --apply" % len(todo))
        return 0

    wrote, failed = 0, 0
    for model, rid, label, vals in todo:
        call(model, "write", [rid], vals)
        back = call(model, "read", [rid], list(vals))[0]
        if all((back[k] or "") == v for k, v in vals.items()):
            print("  wrote %s(%d) %s — verified" % (model, rid, label)); wrote += 1
        else:
            print("  FAIL  %s(%d) %s — readback mismatch" % (model, rid, label)); failed += 1
    print("done: %d written, %d failed" % (wrote, failed))
    return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
