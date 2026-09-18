#!/usr/bin/env python3
"""Render the social card and set it as the site's default og:image.

Shares of judgedice.com have never had a working card. Odoo falls back to
/web/image/website/2/logo, which on this site is an **SVG** - Facebook,
LinkedIn, X and iMessage all ignore SVG og:images, so every link posted
anywhere has rendered bare.

This draws a 1200x630 card in the site's own typography: the wordmark with its
vermilion full stop, a hairline, what the work is, and the domain. Paper ground,
no photograph - it has to stay legible as a 400px-wide thumbnail in a feed.

Fonts come from the Google Fonts repo into the scratch dir (the repo carries no
binaries); --fonts points elsewhere if they are already on disk.

    python3 scripts/make_og_card.py                 # render only, writes a PNG
    python3 scripts/make_og_card.py --apply         # ...and set it on website 2
"""
import argparse
import base64
import io
import os
import sys

from odoo import connect

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow needed: run this with .venv/bin/python")

SITE = 2
W, H = 1200, 630
PAPER = (0xF2, 0xEC, 0xDF)
INK = (0x1C, 0x17, 0x12)
INK_FAINT = (0x8B, 0x83, 0x7A)
VERMILION = (0xCB, 0x41, 0x27)
LINE = (0xD8, 0xCF, 0xBE)
MARGIN = 88


def load(path, size, weight=None):
    """Source Serif 4 ships as a variable font. Its axes are (Weight, Optical
    Size) in that order - passing them the other way round silently clamps the
    weight to the 200 minimum and renders everything hairline-thin.

    Optical size tracks the type size, which is what the axis is for: tight
    spacing and fine hairlines on the display sizes, sturdier small text."""
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            f.set_variation_by_axes([float(weight), float(min(60, max(8, size)))])
        except Exception:
            pass
    return f


def tracked(draw, xy, text, font, fill, tracking):
    """Draw text with letter-spacing; Pillow has no tracking of its own."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def build(fonts):
    serif = os.path.join(fonts, "SourceSerif4-Regular.ttf")
    italic = os.path.join(fonts, "SourceSerif4-Italic.ttf")
    for p in (serif, italic):
        if not os.path.exists(p):
            sys.exit(f"missing font: {p}")

    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    mark = load(serif, 150, 600)
    y = 96
    d.text((MARGIN, y), "Judge", font=mark, fill=INK)
    d.text((MARGIN + d.textlength("Judge", font=mark), y), ".",
           font=mark, fill=VERMILION)

    y += 196
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=1)

    y += 46
    label = load(serif, 25, 600)
    tracked(d, (MARGIN, y), "TRIBUTE WRITING", label, VERMILION, 3.4)

    y += 56
    lead = load(italic, 52, 450)
    d.text((MARGIN, y), "Eulogies, toasts, send-offs", font=lead, fill=INK)
    d.text((MARGIN, y + 66), "and keepsakes.", font=lead, fill=INK)

    foot = load(serif, 23, 550)
    txt, tr = "JUDGEDICE.COM", 3.0
    width = sum(d.textlength(c, font=foot) + tr for c in txt) - tr
    tracked(d, (W - MARGIN - width, H - MARGIN - 18), txt, foot, INK_FAINT, tr)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--fonts", default=os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "jd-fonts"))
    ap.add_argument("--out", default="processed_images/og_card_1200x630.png")
    args = ap.parse_args()

    im = build(args.fonts)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    im.save(args.out, "PNG")
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    blob = buf.getvalue()
    print(f"rendered {args.out}  {im.size[0]}x{im.size[1]}  {len(blob)/1024:.0f} KB")

    if not args.apply:
        print("render only - pass --apply to set it on website 2")
        return 0

    uid, call = connect()
    w = call("website", "read", [SITE], ["id", "name"])[0]
    assert w["name"] != "Half a Glass", "refusing to write site 1"
    call("website", "write", [SITE],
         {"social_default_image": base64.b64encode(blob).decode()})
    back = call("website", "read", [SITE], ["social_default_image"])[0]
    assert back["social_default_image"], "social_default_image did not stick"
    print(f"set social_default_image on website {SITE} ({w['name']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
