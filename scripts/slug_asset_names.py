#!/usr/bin/env python3
"""Give served images URL-safe filenames, and repoint what refers to them.

Odoo serves an attachment at /web/image/<id>-<checksum>/<name>, so the name
lands verbatim in the URL - and these names came from uploads like

    Blog Post 'for dad' cover image.png

which put a raw space and an apostrophe inside every og:image tag. The image
itself resolves (Odoo matches on the id), but a meta tag carrying an unencoded
URL is not something every social scraper will follow, which is the whole point
of having an og:image.

Renaming changes no bytes and no checksum, so the reference only needs its name
segment swapped. Blog covers live in cover_properties (a JSON blob holding a CSS
url) and page art in a view arch; both are rewritten here.

Dry-run by default; --apply writes.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
UNSAFE = re.compile(r"[^A-Za-z0-9._-]")


def replace_url(text, aid, new_url):
    """Swap the URL for `aid`, scanning to a real delimiter.

    The old name may contain quotes or spaces, so the end of the URL is found by
    looking for what actually terminates it in markup - a quote, an escaped
    quote, or the closing paren - rather than by a character class."""
    out, i = [], 0
    needle = f"/web/image/{aid}"
    while True:
        k = text.find(needle, i)
        if k < 0 or (k + len(needle) < len(text) and text[k + len(needle)].isdigit()):
            if k < 0:
                break
            out.append(text[i:k + len(needle)]); i = k + len(needle); continue
        end = len(text)
        for delim in ('&quot;', '"', "')", ')', '&#34;'):
            d = text.find(delim, k)
            if d >= 0:
                end = min(end, d)
        out.append(text[i:k]); out.append(new_url); i = end
    out.append(text[i:])
    return "".join(out)


def slug(name):
    """Make a name safe to sit in a URL path, changing as little as possible.

    Case is left alone: this is about characters that need escaping, not about
    tidiness, and every rename costs a reference rewrite. A name already inside
    [A-Za-z0-9._-] comes back unchanged."""
    if not UNSAFE.search(name):
        return name
    stem, _, ext = name.rpartition(".")
    stem = stem or name
    s = stem.replace("'", "").replace("\N{RIGHT SINGLE QUOTATION MARK}", "")
    s = UNSAFE.sub("-", s)
    s = re.sub(r"\.{2,}", "", s)          # "entries..." -> "entries"
    s = re.sub(r"-{2,}", "-", s).strip("-.")
    return f"{s}.{ext}" if ext else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    # Only things actually referenced from a page: covers and view art.
    refs = []
    for model in ("blog.post", "blog.blog"):
        dom = [["blog_id", "=", 1]] if model == "blog.post" else [["id", "=", 1]]
        for r in call(model, "read", call(model, "search", dom),
                      ["id", "name", "cover_properties"]):
            m = re.search(r"/web/image/(\d+)", r["cover_properties"] or "")
            if m:
                refs.append((model, r["id"], "cover_properties", int(m.group(1))))
    for v in call("ir.ui.view", "read",
                  call("ir.ui.view", "search", [["website_id", "=", SITE]]),
                  ["id", "key", "arch_db"]):
        for aid in sorted({int(x) for x in
                           re.findall(r"/web/image/(\d+)", v["arch_db"] or "")}):
            refs.append(("ir.ui.view", v["id"], "arch", aid))

    aids = sorted({r[3] for r in refs})
    atts = {a["id"]: a for a in call("ir.attachment", "read", aids,
                                     ["id", "name", "checksum"])}
    jobs = [(aid, a["name"], slug(a["name"])) for aid, a in sorted(atts.items())
            if slug(a["name"]) != a["name"]]

    if not jobs:
        print("every referenced attachment already has a URL-safe name")
        return 0
    for aid, old, new in jobs:
        print(f"  {aid}  {old!r}\n        -> {new!r}")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    for aid, old, new in jobs:
        call("ir.attachment", "write", [aid], {"name": new})
        a = call("ir.attachment", "read", [aid], ["name", "checksum"])[0]
        assert a["name"] == new
        url = f"/web/image/{aid}-{a['checksum'][:8]}/{new}"
        assert not UNSAFE.search(new), url

        for model, rid, field, ref_aid in refs:
            if ref_aid != aid:
                continue
            if field == "cover_properties":
                # Rebuild the value from the attachment instead of substituting
                # inside it. A regex over this string has to guess where the old
                # URL ends, and these names contain apostrophes - the first
                # version of this stopped at one and left the tail behind,
                # producing ".../Blog-Post-for-dad-...webp'for dad' cover
                # image-web.webp" in every og:image tag.
                cp = json.loads(call(model, "read", [rid], ["cover_properties"])[0]
                                ["cover_properties"])
                cp["background-image"] = f'url("{url}")'
                call(model, "write", [rid], {"cover_properties": json.dumps(cp)})
                back = json.loads(call(model, "read", [rid], ["cover_properties"])[0]
                                  ["cover_properties"])["background-image"]
                assert back == f'url("{url}")', back
            else:
                arch = call(model, "read", [rid], ["arch_db"])[0]["arch_db"]
                upd = replace_url(arch, aid, url)
                assert upd != arch, (rid, aid)
                ET.fromstring(upd)
                call(model, "write", [rid], {"arch": upd})
                assert url in call(model, "read", [rid], ["arch_db"])[0]["arch_db"]
            print(f"    repointed {model} {rid}")
        print(f"  renamed {aid} -> {new}")

    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
