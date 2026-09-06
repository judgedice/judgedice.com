"""Screenprint/halftone treatment matching assets/judge-portrait.jpg.

Writes a PNG of ink on a transparent background: the dots carry the image in
the alpha channel and nothing else is painted, so whatever the page puts behind
it shows through directly. No mix-blend-mode needed — drop it on the paper
colour (#F2ECDF), on a photo, on anything.

The paper's creases and mottle survive as very faint ink, which is what keeps
it looking printed rather than cut out.

Usage
-----
    .venv/bin/python scripts/halftone.py <src> <dst> [options]

Reads JPEG, PNG, HEIC (straight off an iPhone). Always writes PNG —
the extension on <dst> is corrected to .png if it isn't already.

    # an entry cover
    .venv/bin/python scripts/halftone.py shot.HEIC out.jpg --w 1600 --h 900

Sizes used on the site: entries 1600x900, product 1200x1200,
offerings 1600x1000, social/OG 1200x630.

Options
-------
    --w, --h        output size; the source is centre-cropped to this aspect
    --cell   5      dot pitch in px. 4 = finer, 7 = coarser and more poster-like
    --fx/--fy 0.5   move the crop. --fy 0.35 keeps the top third of a tall photo
    --seed   0      changes the paper creases; use a different one per image so
                    no two covers share a texture
    --contrast 1.10 raise for more punch; too high fills shadows into black slabs
    --gamma  1.20   raise to brighten midtones
    --floor  0.10   darkest ink level. Lower = denser blacks, but past ~0.05 the
                    dots merge and the screen disappears
    --gain   1.30   dot size multiplier
    --clear  0.07   alpha below this goes fully transparent, so the paper grain
                    does not print as a wash across the whole frame. Raise it
                    for a cleaner knock-out, set 0 to keep every speck

Fill the frame when shooting: the screen eats fine detail, so one object edge
to edge beats a wide shot every time.
"""
import sys, os, math, argparse
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageEnhance
try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

PAPER = (247, 244, 236)
INK   = (24, 20, 16)


def prep(im, size, focus=None, contrast=1.0, gamma=1.0,
         floor=0.06, ceil=0.99):
    """Grayscale, crop to aspect, tone-curve."""
    im = ImageOps.exif_transpose(im).convert("L")
    tw, th = size
    im = ImageOps.fit(im, (tw, th), Image.LANCZOS,
                      centering=focus or (0.5, 0.5))
    a = np.asarray(im).astype(np.float32) / 255.0
    # autolevel on 1st/99th percentile so scans and snapshots normalise alike
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    if hi - lo > 1e-3:
        a = np.clip((a - lo) / (hi - lo), 0, 1)
    a = a ** gamma
    a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)
    # keep the plate off pure black/white: the darkest areas must still read as
    # dots, or large shadows fill in and print as flat slabs
    a = floor + a * (ceil - floor)
    return Image.fromarray((a * 255).astype(np.uint8), "L")


def halftone(gray, cell=5, angle=45, ss=4, gain=1.30):
    """Rotated-screen dot halftone. Dot area tracks local darkness."""
    W, H = gray.size
    g = gray.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255)
    gw, gh = g.size
    cols, rows = max(1, gw // cell), max(1, gh // cell)
    means = np.asarray(g.resize((cols, rows), Image.BOX)).astype(np.float32)
    k = np.clip((255.0 - means) / 255.0, 0, 1)      # darkness
    rad = (cell * ss / 2.0) * np.sqrt(k) * gain      # area ∝ darkness

    out = Image.new("L", (cols * cell * ss, rows * cell * ss), 255)
    d = ImageDraw.Draw(out)
    half = cell * ss / 2.0
    ys, xs = np.nonzero(rad > 0.35)
    for y, x in zip(ys.tolist(), xs.tolist()):
        r = float(rad[y, x])
        cx = x * cell * ss + half
        cy = y * cell * ss + half
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)

    out = out.resize((cols * cell, rows * cell), Image.LANCZOS)
    out = out.rotate(-angle, resample=Image.BICUBIC, expand=True, fillcolor=255)
    ow, oh = out.size
    return out.crop(((ow - W) // 2, (oh - H) // 2,
                     (ow - W) // 2 + W, (oh - H) // 2 + H))


def paper(size, seed=0):
    """Off-white ground: low-freq blotching, fine grain, a few soft creases."""
    rng = np.random.default_rng(seed)
    W, H = size
    low = rng.normal(0.5, 0.5, (max(2, H // 24), max(2, W // 24))).astype(np.float32)
    low = np.asarray(Image.fromarray(np.clip(low, 0, 1) * 255).convert("L")
                     .resize((W, H), Image.BICUBIC)).astype(np.float32) / 255.0
    low = 1.0 - (1.0 - low) * 0.10                      # gentle mottle
    grain = rng.normal(0.0, 0.020, (H, W)).astype(np.float32)
    a = np.clip(low + grain, 0, 1)

    sheet = Image.fromarray((a * 255).astype(np.uint8), "L")
    d = ImageDraw.Draw(sheet)
    for _ in range(rng.integers(2, 4)):                 # vertical folds
        x = int(rng.uniform(0.15, 0.85) * W)
        d.line((x, 0, x + rng.integers(-12, 12), H), fill=214,
               width=int(rng.integers(2, 5)))
    for _ in range(rng.integers(1, 3)):                 # horizontal folds
        y = int(rng.uniform(0.2, 0.8) * H)
        d.line((0, y, W, y + rng.integers(-10, 10)), fill=218,
               width=int(rng.integers(2, 4)))
    return sheet.filter(ImageFilter.GaussianBlur(1.1))


def render(src, dst, size, cell=5, contrast=1.10, gamma=1.20, focus=None,
           seed=0, gain=1.30, floor=0.10, ceil=0.99, clear=0.07):
    im = Image.open(src)
    gray = prep(im, size, focus=focus, contrast=contrast, gamma=gamma,
                floor=floor, ceil=ceil)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=3))
    dots = np.asarray(halftone(gray, cell=cell, gain=gain)).astype(np.float32) / 255.0
    sheet = np.asarray(paper(size, seed=seed)).astype(np.float32) / 255.0
    plate = dots * sheet                                 # 1 = bare, 0 = solid ink

    # the plate becomes alpha rather than a painted background: compositing
    # ink at alpha=(1-plate) over a colour gives exactly what baking that
    # colour in used to give, but now the page chooses the colour
    alpha = np.clip(1.0 - plate, 0, 1)
    # the paper's mottle and grain would otherwise print as a faint wash over
    # the entire frame; below `clear` the sheet goes properly transparent, and
    # what is left is rescaled so the dots keep their weight
    if clear > 0:
        alpha = np.clip((alpha - clear) / (1.0 - clear), 0, 1)
    rgba = np.zeros((size[1], size[0], 4), np.uint8)
    rgba[:, :, 0], rgba[:, :, 1], rgba[:, :, 2] = INK
    rgba[:, :, 3] = np.clip(alpha * 255, 0, 255).astype(np.uint8)

    dst = os.path.splitext(dst)[0] + ".png"
    d = os.path.dirname(dst)
    if d:
        os.makedirs(d, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(dst, optimize=True)
    return dst


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--w", type=int, default=1600)
    p.add_argument("--h", type=int, default=900)
    p.add_argument("--cell", type=int, default=5)
    p.add_argument("--contrast", type=float, default=1.10)
    p.add_argument("--gamma", type=float, default=1.20)
    p.add_argument("--gain", type=float, default=1.30)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--fx", type=float, default=0.5)
    p.add_argument("--fy", type=float, default=0.5)
    p.add_argument("--floor", type=float, default=0.10)
    p.add_argument("--ceil", type=float, default=0.99)
    p.add_argument("--clear", type=float, default=0.07)
    a = p.parse_args()
    print(render(a.src, a.dst, (a.w, a.h), cell=a.cell, contrast=a.contrast,
                 gamma=a.gamma, focus=(a.fx, a.fy), seed=a.seed, gain=a.gain,
                 floor=a.floor, ceil=a.ceil, clear=a.clear))
