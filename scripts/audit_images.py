#!/usr/bin/env python3
"""What every image on the site actually weighs, and what it should weigh.

Read-only. Nothing here writes to Odoo.

For each image attachment over --min-kb it pulls the bytes, measures the real
dimensions, checks whether an alpha channel is doing any work, and re-encodes
to webp at the target bound to show the achievable size. Pairs an original
(.png/.jpeg) with its Odoo-generated .webp derivative where both exist, because
the derivative is the safe thing to shrink - the original stays untouched.

    python3 scripts/audit_images.py                 # everything over 300 KB
    python3 scripts/audit_images.py --min-kb 100
    python3 scripts/audit_images.py --width 1600 --quality 72
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


def human(n):
    return f"{n/1024:.0f} KB" if n < 1024 * 1024 else f"{n/1024/1024:.2f} MB"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-kb", type=int, default=300,
                    help="only analyse attachments above this size (default 300)")
    ap.add_argument("--width", type=int, default=1920,
                    help="longest-edge bound for the projection (default 1920)")
    ap.add_argument("--quality", type=int, default=78,
                    help="webp quality for the projection (default 78)")
    args = ap.parse_args()

    uid, call = connect()
    ids = call("ir.attachment", "search", [["mimetype", "like", "image/"]])
    atts = call("ir.attachment", "read", ids,
                ["id", "name", "mimetype", "file_size", "website_id",
                 "res_model", "res_id", "url"])
    atts = [a for a in atts if a["file_size"]]

    # An Odoo-generated .webp sits next to the file it came from. Shrinking the
    # derivative is safe; the original is Judge's master and is left alone.
    by_stem = {}
    for a in atts:
        by_stem.setdefault(os.path.splitext(a["name"])[0], []).append(a)

    big = sorted((a for a in atts if a["file_size"] >= args.min_kb * 1024),
                 key=lambda a: -a["file_size"])
    print(f"{len(atts)} image attachments, {human(sum(a['file_size'] for a in atts))} total")
    print(f"analysing {len(big)} over {args.min_kb} KB "
          f"-> webp, longest edge {args.width}px, quality {args.quality}\n")

    hdr = f"{'id':>5}  {'now':>9} {'dims':>11} {'A':>1} {'kind':>10} {'target':>9} {'save':>7}  name"
    print(hdr)
    print("-" * len(hdr))

    now_total = new_total = 0
    rows = []
    for a in big:
        raw = call("ir.attachment", "read", [a["id"]], ["datas"])[0]["datas"]
        if not raw:
            continue
        blob = base64.b64decode(raw)
        try:
            im = Image.open(io.BytesIO(blob))
            im.load()
        except Exception as e:
            print(f"{a['id']:>5}  {human(len(blob)):>9}  unreadable ({e})")
            continue

        alpha = "-"
        if im.mode in ("RGBA", "LA", "PA"):
            lo, _ = im.getchannel("A").getextrema()
            alpha = "." if lo == 255 else "A"   # "." = opaque, alpha is dead weight

        w, h = im.size
        # Only drop the alpha channel when it is genuinely doing nothing.
        # The duotone/halftone art is ink on transparency by design - flattening
        # that onto a background destroys the image (and fakes a huge "saving"),
        # so real transparency is carried through into the webp.
        target_mode = "RGBA" if alpha == "A" else "RGB"
        out = im.convert(target_mode)
        scale = min(1.0, args.width / max(w, h))
        if scale < 1:
            out = out.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                             Image.LANCZOS)
        buf = io.BytesIO()
        out.save(buf, "WEBP", quality=args.quality, method=6)
        new = buf.tell()

        siblings = by_stem.get(os.path.splitext(a["name"])[0], [])
        kind = "derivative" if (a["mimetype"] == "image/webp" and len(siblings) > 1) else "original"

        now_total += len(blob)
        new_total += new
        rows.append((a, len(blob), new, kind))
        print(f"{a['id']:>5}  {human(len(blob)):>9} {w:>5}x{h:<5} {alpha:>1} {kind:>10} "
              f"{human(new):>9} {len(blob)/new:>6.0f}x  {a['name'][:40]}")

    print("-" * len(hdr))
    if now_total:
        print(f"{'':>5}  {human(now_total):>9} {'':>11} {'':>1} {'':>10} {human(new_total):>9} "
              f"{now_total/new_total:>6.0f}x  TOTAL  (saves {human(now_total-new_total)})")

    opaque = [r for r in rows if r[0]["mimetype"] == "image/webp"]
    if opaque:
        print(f"\nDerivatives safe to replace without touching an original: "
              f"{sum(1 for r in rows if r[3]=='derivative')} of {len(rows)}")
    print("\nA column: '.' = has an alpha channel that is fully opaque (pure overhead), "
          "'A' = real transparency, '-' = no alpha.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
