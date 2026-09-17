# -*- coding: utf-8 -*-
"""Remove the Previous/Next pager from the static pages (site 2).

Each hand-built page carried a footer <nav> stepping through the pages in
sequence. Judge asked for them gone. Two of them (/home, /connect) still
pointed at /exciting, which has been /offerings since the page was renamed, so
this also clears two dead links.

Scope, deliberately narrow:
  - only the five page views listed below
  - only a <nav> whose inline style carries justify-content:space-between AND
    whose text contains Previous/Next -- exactly one per file, asserted
  - the quotes carousel's controls are <button class="carousel-control-*">,
    not <nav>, so they are never matched
  - the header's <nav> lives in view 2035, which is not in this list
  - blog posts are untouched: their pager is Odoo's own, on a different view

Operates on the snapshot files; deploy them afterwards with deploy.py. Text
surgery rather than an ElementTree rewrite, so the rest of each file keeps its
exact formatting and the diff stays readable.

Dry-run by default; --apply edits the files.
"""
import sys, os, io, xml.etree.ElementTree as ET

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPEN_MARK = '<nav style="display:flex;justify-content:space-between'
CLOSE = "</nav>"

FILES = [
    "snapshot/views/2034-website.homepage.xml",
    "snapshot/views/2039-website.judge_work.xml",
    "snapshot/views/2040-website.judge_home.xml",
    "snapshot/views/2041-website.judge_exciting.xml",
    "snapshot/views/2042-website.judge_connect.xml",
]


def strip_pager(src, label):
    """Return (new_src, removed_block) or (src, None) if already clean."""
    n = src.count(OPEN_MARK)
    if n == 0:
        return src, None
    assert n == 1, "%s: expected 1 pager nav, found %d" % (label, n)
    i = src.index(OPEN_MARK)
    j = src.index(CLOSE, i)
    assert OPEN_MARK not in src[i + 1:j], "%s: nested pager nav" % label
    block = src[i:j + len(CLOSE)]
    assert "Previous" in block or "Next" in block, \
        "%s: matched nav has no Previous/Next — refusing" % label
    assert "carousel" not in block, "%s: matched nav touches the carousel" % label
    # swallow the indentation on the pager's own line, and its trailing newline
    start = src.rfind("\n", 0, i) + 1
    assert not src[start:i].strip(), "%s: pager shares its line with content" % label
    end = j + len(CLOSE)
    if src[end:end + 1] == "\n":
        end += 1
    return src[:start] + src[end:], block


def main(argv):
    apply_ = "--apply" in argv
    print("drop_page_pagers [%s]" % ("APPLY" if apply_ else "dry-run"))
    changed = 0
    for rel in FILES:
        path = os.path.join(REPO, rel)
        src = io.open(path, encoding="utf-8").read()
        new, block = strip_pager(src, rel)
        if block is None:
            print("  noop  %s — no pager" % rel); continue
        ET.fromstring(new)  # must still be well-formed
        assert new.count("<nav") == src.count("<nav") - 1
        links = [l for l in block.split('href="')[1:]]
        print("  %s  %s — removing %d chars, links: %s"
              % ("strip" if apply_ else "would-strip", rel, len(block),
                 ", ".join(l.split('"')[0] for l in links)))
        if apply_:
            io.open(path, "w", encoding="utf-8").write(new)
        changed += 1
    print("done: %d file(s) %s" % (changed, "changed" if apply_ else "would change"))
    if not apply_ and changed:
        print("re-run with --apply, then deploy the files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
