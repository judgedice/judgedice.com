# -*- coding: utf-8 -*-
"""Create an Entry (blog post) as an UNPUBLISHED draft, for Judge to review.

The body is an HTML fragment under entries/ holding Judge's text verbatim. The
only addition is the standard closing CTA to /offerings, as its own element
(the same one publish_entries.py uses). No standfirst or subtitle is invented:
pass --subtitle / --stand only with Judge's own words.

Nothing is published. is_published stays False, so the post is visible only to
logged-in editors at its URL until Judge publishes it from the website editor.

Idempotent (skips if a post with the title already exists in blog 1); dry-run by
default. After --apply it reads the post back and asserts the draft state, the
site, and that every word and link of the source survived Odoo's sanitizer.

  python3 scripts/draft_entry.py entries/<slug>.html --title "..." --tag Opinions
  python3 scripts/draft_entry.py entries/<slug>.html --title "..." --tag Opinions --apply
"""
import sys, os, re, argparse, html as htmllib
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

BLOG, SITE = 1, 2
TAGS = {"Tributes": 1, "Opinions": 2, "Reviews": 3}
CTA = ('<p class="jd-entry-cta">I write tributes for a living &#8212; eulogies, toasts, '
       'send-offs and keepsakes. <a href="/offerings">See how that works</a>.</p>')


class _Flat(HTMLParser):
    """Visible text + link targets, whitespace-normalized: what a reader gets."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.links = [], []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))
        if tag in ("p", "h1", "h2", "h3", "li", "td", "th", "tr", "br"):
            self.text.append(" ")

    def handle_data(self, data):
        self.text.append(data)


def flat(fragment):
    p = _Flat()
    p.feed(fragment)
    return re.sub(r"\s+", " ", "".join(p.text)).strip(), p.links


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--title", required=True)
    ap.add_argument("--tag", choices=sorted(TAGS), required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--stand", default="", help="italic standfirst, Judge's words only")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    body = open(a.source, encoding="utf-8").read().strip()
    parts = []
    if a.stand:
        parts.append('<p class="jd-standfirst"><em>%s</em></p>' % htmllib.escape(a.stand))
    parts += [body, CTA]
    content = "\n".join(parts)
    want_text, want_links = flat(content)

    uid, call = connect()
    print("draft_entry [%s]" % ("APPLY" if a.apply else "dry-run"))
    print("  title:   %s" % a.title)
    print("  tag:     %s   subtitle: %r   standfirst: %r" % (a.tag, a.subtitle, a.stand))
    print("  body:    %d words, %d links, %d headings, %d tables (+ CTA)"
          % (len(want_text.split()), len(want_links),
             len(re.findall(r"<h2", body)), len(re.findall(r"<table", body))))

    blog = call("blog.blog", "read", [BLOG], ["website_id"])[0]
    assert blog["website_id"] and blog["website_id"][0] == SITE, blog

    exists = call("blog.post", "search", [["name", "=", a.title], ["blog_id", "=", BLOG]])
    if exists:
        print("  exists: post %d - nothing to do" % exists[0])
        return 0
    if not a.apply:
        print("  would create post on blog %d (site %d), is_published=False" % (BLOG, SITE))
        return 0

    vals = {"name": a.title, "blog_id": BLOG, "tag_ids": [(6, 0, [TAGS[a.tag]])],
            "content": content, "is_published": False}
    if a.subtitle:
        vals["subtitle"] = a.subtitle
    pid = call("blog.post", "create", vals)

    got = call("blog.post", "read", [pid],
               ["name", "is_published", "website_id", "blog_id", "tag_ids",
                "content", "website_url"])[0]
    got_text, got_links = flat(got["content"] or "")
    assert got["is_published"] is False, "post %d is published!" % pid
    assert got["website_id"][0] == SITE and got["blog_id"][0] == BLOG, got
    assert got["tag_ids"] == [TAGS[a.tag]], got["tag_ids"]
    assert got_text == want_text, "text changed on save:\n%s\n---\n%s" % (want_text, got_text)
    assert got_links == want_links, "links changed on save:\n%s\n%s" % (want_links, got_links)
    print("  -> created post %d, UNPUBLISHED; readback ok (text + %d links match)"
          % (pid, len(got_links)))
    print("     %s" % got["website_url"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
