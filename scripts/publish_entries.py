# -*- coding: utf-8 -*-
"""Publish Entries (blog posts) from the Facebook archive candidates.

Source: reports/facebook-entry-candidates.md (verbatim post text in fenced
blocks). Each entry gets per-piece cleanup, an italic editorial standfirst
giving context, and a closing CTA to /offerings.

Cleanup handled here:
  - Facebook's export duplicates caption blocks; the Chad piece repeats five
    paragraphs verbatim -> truncate at the sign-off.
  - Funeral service logistics (addresses, dates) stripped from the eulogy.
  - A 2022 election-day call to action and a one-day fundraiser are framed as
    archive pieces by their standfirst rather than read as live calls.

Idempotent (skips posts whose title already exists); dry-run by default.
"""
import sys, os, re, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "reports", "facebook-entry-candidates.md")
BLOG, SITE = 1, 2
TAGS = {"Tributes": 1, "Opinions": 2, "Reviews": 3}

CTA = ('<p class="jd-entry-cta">I write tributes for a living &#8212; eulogies, toasts, '
       'send-offs and keepsakes. <a href="/offerings">See how that works</a>.</p>')

# source heading -> published entry
ENTRIES = [
    {
        "src": "[Tributes] A Tribute to Michael Di Cesaro",
        "title": "A Tribute to Michael Di Cesaro",
        "subtitle": "My father, in the only terms that would have suited him.",
        "tag": "Tributes",
        "date": "2021-09-22 16:22:15",
        "stand": ("Written the week my father died, in September 2021. Service details "
                  "have been removed; everything else is as it was published."),
        # drop the two logistics paragraphs, keep the closing joke without the address
        "truncate_after": "He will be missed.",
        "append": ["Reception with offensively expensive champagne and embarrassingly "
                   "cheap scotch to follow."],
    },
    {
        "src": "[Tributes] The Halfway Eulogy (Chad at 50)",
        "title": "The Halfway Eulogy",
        "subtitle": "For my brother at fifty &#8212; a progress report, not an obituary.",
        "tag": "Tributes",
        "date": "2023-05-15 23:44:34",
        "stand": ("A tribute doesn't need a death to justify it. Written for my brother's "
                  "50th birthday, and filed just before midnight."),
        "truncate_after": "11:45. Birdie",   # everything after is Facebook's duplicate block
    },
    {
        "src": "[Tributes] The Ninth Decade",
        "title": "The Ninth Decade",
        "subtitle": "For my mother at eighty.",
        "tag": "Tributes",
        "date": "2026-01-08 12:26:23",
        "stand": ("Most of a life happens before you arrive to witness it. This one is "
                  "reconstructed from inherited anecdote."),
        "drop_containing": ["Great grandchild clips posted in the comments."],
    },
    {
        "src": "[Tributes] An Endorsement, and a Marriage",
        "title": "An Endorsement, and a Marriage",
        "subtitle": "The same craft, aimed at persuasion.",
        "tag": "Tributes",
        "date": "2022-03-22 12:24:21",
        "stand": ("Written for my wife's 2022 run at the Andover School Committee. The "
                  "campaign is long over; the argument is what I'd keep."),
        "drop_containing": ["TL;DR", "polling place"],
    },
    {
        "src": "[Tributes] For Doug",
        "title": "For Doug",
        "subtitle": "Six sentences, thirty years later.",
        "tag": "Tributes",
        "date": "2022-12-05 15:15:32",
        "stand": "Not every tribute needs a podium, or a page. Some need six sentences.",
    },
    {
        "src": "[Opinions] Micro Learning, Micro Results",
        "title": "Micro Learning, Micro Results",
        "subtitle": "365 days of Duolingo, and what it bought me.",
        "tag": "Opinions",
        "date": "2025-12-03 22:45:25",
        "stand": "On the limits of dimestore self-improvement.",
    },
    {
        "src": "[Opinions] Chicago, A Farewell",
        "title": "Chicago, A Farewell",
        "subtitle": "A tribute to a place, on the way out of it.",
        "tag": "Opinions",
        "date": "2013-09-06 09:40:36",
        "stand": "Written twenty-four hours before moving east, in 2013.",
    },
    {
        "src": "[Reviews] The Short Game",
        "title": "The Short Game",
        "subtitle": "Buy local, shop small, nurture the roots.",
        "tag": "Reviews",
        "date": "2025-10-21 18:23:46",
        "stand": ("Written for a one-day fundraiser at OTTO in Andover, October 2025. "
                  "The pizza argument still stands."),
    },
]


def parse_source():
    """heading -> verbatim body from the fenced block under it."""
    text = open(SRC, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)```\n(.*?)\n```", text, re.S | re.M):
        out[m.group(1).strip()] = m.group(3)
    return out


def build_html(entry, body):
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]

    if entry.get("truncate_after"):
        cut = entry["truncate_after"]
        keep = []
        for p in paras:
            keep.append(p)
            if cut in p:
                break
        paras = keep

    for needle in entry.get("drop_containing", []):
        paras = [p for p in paras if needle not in p]

    paras += entry.get("append", [])

    parts = ['<p class="jd-standfirst"><em>%s</em></p>' % entry["stand"]]
    for p in paras:
        parts.append("<p>%s</p>" % html.escape(p).replace("\n", "<br/>"))
    parts.append(CTA)
    return "".join(parts), len(paras)


def main(apply_):
    uid, call = connect()
    print("publish_entries [%s]" % ("APPLY" if apply_ else "dry-run"))
    src = parse_source()

    created = 0
    for e in ENTRIES:
        match = [k for k in src if k.startswith(e["src"])]
        if not match:
            print("  MISSING source: %s" % e["src"]); continue
        body = src[match[0]]
        content, n = build_html(e, body)
        words = len(re.findall(r"\w+", content))

        exists = call("blog.post", "search", [["name", "=", e["title"]], ["blog_id", "=", BLOG]])
        if exists:
            print("  exists: %-34s (post %d)" % (e["title"], exists[0])); continue
        print("  %-34s %-9s %s  %3d paras / %4d words"
              % (e["title"], e["tag"], e["date"][:10], n, words))
        if not apply_:
            continue
        pid = call("blog.post", "create", {
            "name": e["title"],
            "subtitle": e["subtitle"],
            "blog_id": BLOG,
            "tag_ids": [(6, 0, [TAGS[e["tag"]]])],
            "content": content,
            "post_date": e["date"],
            "is_published": True,
        })
        # post_date is often overwritten on publish; force it back to the original
        call("blog.post", "write", [pid], {"post_date": e["date"]})
        print("      -> created post %d, published" % pid)
        created += 1

    print("done: %d created" % created)
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
