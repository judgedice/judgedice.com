"""Shared plumbing for the judgedice.com print effects.

Every effect follows the same shape: load the source, flatten it to a tone map,
turn that tone into one or more ink *coverage* maps, then multiply those inks
onto a sheet of paper. Only the coverage step differs between effects.

Output is a near-white ground carrying near-black ink, so a page can lay it on
the site's paper (#F2ECDF) with mix-blend-mode:multiply the way the hero
portrait does. Viewed on its own a file looks flat — that is correct.
"""
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter

try:
    import pillow_heif; pillow_heif.register_heif_opener()
except Exception:
    pass

PAPER     = (247, 244, 236)
INK       = (24, 20, 16)
VERMILION = (203, 65, 39)   # the design system's accent


def tone(src, size, focus=(0.5, 0.5), contrast=1.10, gamma=1.20,
         floor=0.10, ceil=0.99, sharpen=True):
    """Load, crop to aspect, and flatten to a 0..1 tone map (1 = light)."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("L")
    im = ImageOps.fit(im, size, Image.LANCZOS, centering=focus)
    if sharpen:
        im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=3))
    a = np.asarray(im).astype(np.float32) / 255.0
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    if hi - lo > 1e-3:
        a = np.clip((a - lo) / (hi - lo), 0, 1)
    a = a ** gamma
    a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)
    # never let the plate reach pure black or white: solid areas print as flat
    # slabs and lose the texture that makes these read as print
    return floor + a * (ceil - floor)


def sheet(size, seed=0, folds=True):
    """Off-white ground: low-frequency mottle, fine grain, a few soft creases."""
    rng = np.random.default_rng(seed)
    W, H = size
    low = rng.normal(0.5, 0.5, (max(2, H // 24), max(2, W // 24))).astype(np.float32)
    low = np.asarray(Image.fromarray((np.clip(low, 0, 1) * 255).astype(np.uint8))
                     .resize((W, H), Image.BICUBIC)).astype(np.float32) / 255.0
    a = np.clip(1.0 - (1.0 - low) * 0.10 + rng.normal(0, 0.020, (H, W)), 0, 1)

    img = Image.fromarray((a * 255).astype(np.uint8), "L")
    if folds:
        d = ImageDraw.Draw(img)
        for _ in range(int(rng.integers(2, 4))):
            x = int(rng.uniform(0.15, 0.85) * W)
            d.line((x, 0, x + int(rng.integers(-12, 12)), H),
                   fill=214, width=int(rng.integers(2, 5)))
        for _ in range(int(rng.integers(1, 3))):
            y = int(rng.uniform(0.2, 0.8) * H)
            d.line((0, y, W, y + int(rng.integers(-10, 10))),
                   fill=218, width=int(rng.integers(2, 4)))
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    return np.asarray(img).astype(np.float32) / 255.0


def ink_on(base, coverage, colour):
    """Multiply one ink plate onto whatever is already there.

    `coverage` is 0..1 ink density; `base` and the result are HxWx3 floats.
    """
    c = np.array(colour, np.float32) / 255.0
    return base * (1.0 - coverage[:, :, None] * (1.0 - c[None, None, :]))


def save(rgb, dst):
    import os
    d = os.path.dirname(dst)
    if d:
        os.makedirs(d, exist_ok=True)
    Image.fromarray(np.clip(rgb * 255, 0, 255).astype(np.uint8), "RGB").save(
        dst, quality=92, subsampling=1)
    return dst


def base_args(p):
    """Flags every effect shares, so the batch driver can call them alike."""
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--w", type=int, default=1600)
    p.add_argument("--h", type=int, default=900)
    p.add_argument("--fx", type=float, default=0.5)
    p.add_argument("--fy", type=float, default=0.5)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--contrast", type=float, default=1.10)
    p.add_argument("--gamma", type=float, default=1.20)
    return p
