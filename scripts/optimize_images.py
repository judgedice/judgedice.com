#!/usr/bin/env python3
"""Re-encode the web-serving copies of oversized images. Masters stay untouched.

Odoo's own model is: an uploaded file is the master, and a .webp sibling is the
copy actually served. On this site that conversion ran at near-lossless settings
and preserved alpha channels that were fully opaque, so several derivatives came
out LARGER than the master they came from - 01_flowfield.webp is 6.8 MB of webp
generated from a 6.2 MB png.

This rebuilds each derivative from its master, bounded and properly encoded. It
writes only to derivative attachments; a master's bytes are never touched, and
no reference is repointed, so pages keep working without any view edit.

Transparency is preserved wherever it is real. The alpha channel is dropped only
when it is provably opaque (extrema 255-255), which is a no-op on the rendered
pixels - it is not the same as flattening artwork onto a background colour.

Dry-run by default; --apply writes.
"""
import argparse
import base64
import io
import os
import sys

from odoo import connect

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow needed: run this with .venv/bin/python")

MAX_EDGE = 1920
QUALITY = 78


def human(n):
    return f"{n/1024:.0f} KB" if n < 1024 * 1024 else f"{n/1024/1024:.2f} MB"


def load(call, aid):
    a = call("ir.attachment", "read", [aid],
             ["id", "name", "mimetype", "file_size", "datas"])[0]
    im = Image.open(io.BytesIO(base64.b64decode(a["datas"])))
    im.load()
    return a, im


def encode(im, max_edge=MAX_EDGE, quality=QUALITY):
    """Bounded webp. Keeps genuine transparency, drops a dead alpha channel."""
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
    args = ap.parse_args()

    uid, call = connect()
    ids = call("ir.attachment", "search", [["mimetype", "like", "image/"]])
    atts = call("ir.attachment", "read", ids,
                ["id", "name", "mimetype", "file_size", "website_id"])

    # Pair each .webp derivative with the master of the same stem.
    by_stem = {}
    for a in atts:
        by_stem.setdefault(os.path.splitext(a["name"])[0], []).append(a)

    jobs = []
    for stem, group in by_stem.items():
        webps = [a for a in group if a["mimetype"] == "image/webp"]
        masters = [a for a in group if a["mimetype"] != "image/webp"]
        if len(webps) == 1 and len(masters) == 1:
            jobs.append((webps[0], masters[0]))
    jobs.sort(key=lambda j: -j[0]["file_size"])

    if not jobs:
        print("no derivative/master pairs found")
        return 0

    print(f"{len(jobs)} derivative(s) rebuildable from a master "
          f"(longest edge {args.max_edge}px, quality {args.quality})\n")
    total_old = total_new = 0
    pending = []
    for deriv, master in jobs:
        assert deriv["mimetype"] == "image/webp", deriv
        assert deriv["id"] != master["id"]
        m, im = load(call, master["id"])
        blob, size, alpha = encode(im, args.max_edge, args.quality)
        if len(blob) >= deriv["file_size"]:
            print(f"  skip  {deriv['name'][:34]:36} already smaller than a rebuild")
            continue
        total_old += deriv["file_size"]
        total_new += len(blob)
        pending.append((deriv, blob))
        print(f"  {deriv['id']:>5} {deriv['name'][:34]:36} "
              f"{human(deriv['file_size']):>9} -> {human(len(blob)):>9} "
              f"({deriv['file_size']/len(blob):.0f}x)  "
              f"{size[0]}x{size[1]} {'RGBA' if alpha else 'RGB'}  "
              f"from master {master['id']}")

    if not pending:
        print("\nnothing to do")
        return 0
    print(f"\n  total {human(total_old)} -> {human(total_new)} "
          f"(saves {human(total_old - total_new)})")

    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    for deriv, blob in pending:
        call("ir.attachment", "write", [deriv["id"]],
             {"datas": base64.b64encode(blob).decode()})
        back = call("ir.attachment", "read", [deriv["id"]],
                    ["file_size", "mimetype"])[0]
        assert back["mimetype"] == "image/webp", back
        assert abs(back["file_size"] - len(blob)) <= 16, (back, len(blob))
        print(f"  wrote {deriv['id']} -> {human(back['file_size'])}")
    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
