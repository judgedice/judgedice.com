#!/usr/bin/env python3
"""Give directly-served originals a web copy, and repoint the reference at it.

Some images are served straight from the uploaded master because Odoo never
made a .webp sibling for them - the blog covers and the homepage art. This
creates that sibling and moves the reference onto it. The master attachment is
never modified or deleted; it stays as the editable original, which is also
what the website builder re-opens when you edit the block.

Transparency is preserved: these are ink-on-transparency prints and the alpha
is doing real work, so the webp keeps its alpha channel. Only a provably opaque
channel (extrema 255-255) is dropped, which cannot change a rendered pixel.

Two reference surfaces:
  - blog.post / blog.blog  -> cover_properties (a JSON blob holding a CSS url)
  - ir.ui.view             -> background-image in the arch

Dry-run by default; --apply writes.
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from odoo import connect

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow needed: run this with .venv/bin/python")

MAX_EDGE = 1920
QUALITY = 78
SUFFIX = "-web"


def human(n):
    return f"{n/1024:.0f} KB" if n < 1024 * 1024 else f"{n/1024/1024:.2f} MB"


def encode(im, max_edge, quality):
    keep_alpha = False
    if im.mode in ("RGBA", "LA", "PA"):
        lo, _ = im.convert("RGBA").getchannel("A").getextrema()
        keep_alpha = lo < 255
    out = im.convert("RGBA" if keep_alpha else "RGB")
    w, h = out.size
    scale = min(1.0, max_edge / max(w, h))
    if scale < 1:
        out = out.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                         Image.LANCZOS)
    buf = io.BytesIO()
    out.save(buf, "WEBP", quality=quality, method=4 if keep_alpha else 6)
    return buf.getvalue(), out.size, keep_alpha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-edge", type=int, default=MAX_EDGE)
    ap.add_argument("--quality", type=int, default=QUALITY)
    ap.add_argument("--min-kb", type=int, default=300)
    args = ap.parse_args()

    uid, call = connect()

    # ---- find every reference and the attachment behind it ----
    refs = []   # (kind, record_id, field, attachment_id)
    for model in ("blog.post", "blog.blog"):
        dom = [["blog_id", "=", 1]] if model == "blog.post" else [["id", "=", 1]]
        for r in call(model, "read", call(model, "search", dom),
                      ["id", "name", "cover_properties"]):
            m = re.search(r"/web/image/(\d+)", r["cover_properties"] or "")
            if m:
                refs.append((model, r["id"], r["name"], int(m.group(1))))
    # Only URLs that are actually fetched by the browser. A data-original-src
    # is the builder's pointer back to the uploaded master so the block can be
    # re-edited - it is never requested, and repointing it would break editing.
    SERVED = re.compile(
        r"""(?:background-image:\s*url\((?:&quot;|["'])?|<img\b[^>]*?\bsrc=["'])"""
        r"""(/web/image/(\d+)[^"')&\s]*)""", re.X)
    for v in call("ir.ui.view", "read",
                  call("ir.ui.view", "search", [["website_id", "=", 2]]),
                  ["id", "key", "arch_db"]):
        arch = v["arch_db"] or ""
        for aid in sorted({int(m.group(2)) for m in SERVED.finditer(arch)}):
            refs.append(("ir.ui.view", v["id"], v["key"], aid))

    aids = sorted({r[3] for r in refs})
    atts = {a["id"]: a for a in call("ir.attachment", "read", aids,
            ["id", "name", "mimetype", "file_size", "checksum", "res_model", "res_id"])}

    # skip anything already webp, or below the threshold
    stems = {os.path.splitext(a["name"])[0] for a in atts.values()}
    jobs = []
    for kind, rid, label, aid in refs:
        a = atts[aid]
        if a["mimetype"] == "image/webp":
            continue
        if a["file_size"] < args.min_kb * 1024:
            continue
        jobs.append((kind, rid, label, a))

    if not jobs:
        print("nothing over threshold is served from a non-webp original")
        return 0

    print(f"{len(jobs)} reference(s) served straight from an original "
          f"(>{args.min_kb} KB, target {args.max_edge}px q{args.quality})\n")

    plan = []
    old_t = new_t = 0
    for kind, rid, label, a in jobs:
        raw = call("ir.attachment", "read", [a["id"]], ["datas"])[0]["datas"]
        im = Image.open(io.BytesIO(base64.b64decode(raw)))
        im.load()
        blob, size, alpha = encode(im, args.max_edge, args.quality)
        if len(blob) >= a["file_size"]:
            print(f"  skip  {a['name'][:38]:40} rebuild is no smaller")
            continue
        old_t += a["file_size"]
        new_t += len(blob)
        plan.append((kind, rid, label, a, blob))
        print(f"  {kind:<11} {rid:<5} {label[:26]:28} {a['name'][:30]:32} "
              f"{human(a['file_size']):>9} -> {human(len(blob)):>9} "
              f"({a['file_size']/len(blob):.0f}x) {size[0]}x{size[1]} "
              f"{'RGBA' if alpha else 'RGB'}")

    if not plan:
        print("\nnothing to do")
        return 0
    print(f"\n  total {human(old_t)} -> {human(new_t)} (saves {human(old_t-new_t)})")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    for kind, rid, label, a, blob in plan:
        stem = os.path.splitext(a["name"])[0]
        web_name = f"{stem}{SUFFIX}.webp"

        # Re-runnable: if a previous run already made this derivative, reuse it
        # rather than piling up duplicates.
        existing = call("ir.attachment", "search",
                        [["name", "=", web_name], ["mimetype", "=", "image/webp"]])
        if existing:
            new_id = existing[0]
            call("ir.attachment", "write", [new_id],
                 {"datas": base64.b64encode(blob).decode()})
        else:
            created = call("ir.attachment", "create", [{
                "name": web_name,
                "mimetype": "image/webp",
                "datas": base64.b64encode(blob).decode(),
                "public": True,
                "res_model": "ir.ui.view",
                "res_id": 0,
            }])
            # XML-RPC create returns a list when handed a list of vals
            new_id = created[0] if isinstance(created, list) else created
        assert isinstance(new_id, int), created
        chk = call("ir.attachment", "read", [new_id], ["checksum", "file_size"])[0]
        assert abs(chk["file_size"] - len(blob)) <= 16
        new_url = f"/web/image/{new_id}-{chk['checksum'][:8]}/{web_name}"

        if kind in ("blog.post", "blog.blog"):
            rec = call(kind, "read", [rid], ["cover_properties"])[0]
            cp = rec["cover_properties"]
            before = cp
            cp2 = re.sub(r"/web/image/\d+(?:-[0-9a-f]+)?/[^\"'\\)]+", new_url, cp)
            assert cp2 != before and new_url in cp2
            json.loads(cp2)  # must stay valid JSON
            call(kind, "write", [rid], {"cover_properties": cp2})
            back = call(kind, "read", [rid], ["cover_properties"])[0]["cover_properties"]
            assert new_url in back
        else:
            v = call("ir.ui.view", "read", [rid], ["arch_db"])[0]
            arch = v["arch_db"]
            # rewrite only the served occurrences, never a data-original-src
            pat = re.compile(
                rf"""((?:background-image:\s*url\((?:&quot;|["'])?|<img\b[^>]*?\bsrc=["'])"""
                rf"""/web/image/){a['id']}(?:-[0-9a-f]+)?/[^"')&\s]*""", re.X)
            assert pat.search(arch), (rid, a["id"])
            arch2 = pat.sub(lambda m: m.group(1)[:-len("/web/image/")] + new_url, arch)
            ET.fromstring(arch2)   # must stay well-formed
            call("ir.ui.view", "write", [rid], {"arch": arch2})
            back = call("ir.ui.view", "read", [rid], ["arch_db"])[0]["arch_db"]
            assert new_url in back

        print(f"  {kind} {rid}: attachment {a['id']} -> {new_id} "
              f"({human(len(blob))}), original untouched")

    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
