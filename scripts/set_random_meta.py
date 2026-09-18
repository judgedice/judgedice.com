#!/usr/bin/env python3
"""SEO meta for the three quote pages.

They were published and indexed with no title or description at all, so a
search result showed a bare URL. Each now gets a title built from the line it
carries and a description that quotes it in full with its attribution.

The quotes are reproduced exactly as they appear on the page - same wording,
same punctuation, same ellipses. Nothing is trimmed or tidied (CLAUDE.md rule
7); the only editorial addition is the trailing sentence explaining what the
page is, which sits outside the quotation.

Dry-run by default; --apply writes.
"""
import argparse
import sys

from odoo import connect

SITE = 2
META = {
    "/random-1": (
        "Only light can do that — Judge DiCesaro",
        "\"Darkness cannot drive out darkness: only light can do that. Hate cannot "
        "drive out hate: only love can do that.\" — Martin Luther King Jr., Strength to Love.",
    ),
    "/random-2": (
        "You don't choose your personality — Judge DiCesaro",
        "\"I've decided I can't hate anyone... because you don't choose your "
        "personality.\" — Oliver DiCesaro. One of the lines kept on rotation at judgedice.com.",
    ),
    "/random-3": (
        "We are the ones we've been waiting for — Judge DiCesaro",
        "\"We are the ones we've been waiting for.\" — June Jordan, Poem for South "
        "African Women. One of the lines kept on rotation at judgedice.com.",
    ),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    pages = call("website.page", "search_read",
                 [["url", "in", list(META)], ["website_id", "=", SITE]],
                 fields=["id", "url", "website_id", "is_published",
                         "website_meta_title", "website_meta_description"])
    assert len(pages) == len(META), pages

    todo = []
    for p in sorted(pages, key=lambda x: x["url"]):
        assert p["website_id"][0] == SITE, p
        title, desc = META[p["url"]]
        print(f"  {p['url']}  published={p['is_published']}")
        print(f"     title ({len(title):>3}) {title}")
        print(f"     desc  ({len(desc):>3}) {desc}")
        if len(title) > 60:
            print(f"     NOTE: title is {len(title)} chars, Google will clip around 60")
        if len(desc) > 160:
            print(f"     NOTE: description is {len(desc)} chars, Google clips around 155-160")
        if (p["website_meta_title"], p["website_meta_description"]) != (title, desc):
            todo.append((p["id"], title, desc))
        print()

    if not todo:
        print("all three already set")
        return 0
    if not args.apply:
        print("dry run - pass --apply to write")
        return 0

    for pid, title, desc in todo:
        call("website.page", "write", [pid],
             {"website_meta_title": title, "website_meta_description": desc})
        back = call("website.page", "read", [pid],
                    ["url", "website_meta_title", "website_meta_description"])[0]
        assert back["website_meta_title"] == title
        assert back["website_meta_description"] == desc
        print(f"  wrote {back['url']}")
    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
