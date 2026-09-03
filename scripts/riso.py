"""Riso — two-ink risograph with deliberate misregistration.

Shadows print in ink, midtones print in the design system's vermilion, and the
two plates are offset by a few pixels so they don't quite line up. That
off-register edge is the whole character of the effect, and it is the only one
of the four that puts the brand accent into the image itself. Best on frames
with a clear subject and simple tone: objects, signage, paper on a table.

    .venv/bin/python scripts/riso.py shot.HEIC out.jpg --w 1600 --h 900

    --offset 5      misregistration in px; 0 is clean, 10 is sloppy and loud
    --spread 0.18   width of the tonal band the accent covers. Widen it and the
                    accent floods light backgrounds instead of picking out the
                    subject, which is the usual way this effect goes wrong
    --centre 0.45   where in the tonal range the accent sits (0 dark, 1 light)
    --accent 0.60   maximum accent coverage
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _effects_common import (tone, sheet, ink_on, save, base_args,
                             PAPER, INK, VERMILION)


def _shift(a, dx, dy):
    return np.roll(np.roll(a, dy, axis=0), dx, axis=1)


def _rough(cov, rng, amount=0.10):
    """Riso ink lays down unevenly — speckle and blotch the coverage."""
    cov = np.clip(cov + rng.normal(0, amount, cov.shape), 0, 1)
    return np.asarray(Image.fromarray((cov * 255).astype(np.uint8), "L")
                      .filter(ImageFilter.GaussianBlur(0.6))
                      ).astype(np.float32) / 255.0


def render(src, dst, size, focus=(.5, .5), seed=0, contrast=1.10, gamma=1.20,
           offset=5, spread=0.18, centre=0.45, accent=0.60):
    t = tone(src, size, focus=focus, contrast=contrast, gamma=gamma,
             floor=0.06, ceil=1.0)
    rng = np.random.default_rng(seed + 4127)

    key = np.clip((0.55 - t) / 0.55, 0, 1) ** 1.15          # shadows -> ink
    mid = np.exp(-((t - centre) ** 2) / (2 * spread ** 2))   # midtones -> accent
    mid = np.clip(mid * accent, 0, 1)

    key = _rough(key, rng, 0.07)
    mid = _rough(mid, rng, 0.11)

    # the misregistration: each plate wanders in its own direction
    a = rng.uniform(0, 2 * np.pi)
    kdx, kdy = int(round(np.cos(a) * offset / 2)), int(round(np.sin(a) * offset / 2))
    mdx, mdy = -kdx + int(rng.integers(-1, 2)), -kdy + int(rng.integers(-1, 2))

    pap = sheet(size, seed=seed)
    base = np.repeat(pap[:, :, None], 3, axis=2) * (np.array(PAPER, np.float32) / 255.0)
    out = ink_on(base, _shift(mid, mdx, mdy), VERMILION)
    out = ink_on(out, _shift(key, kdx, kdy), INK)
    return save(out, dst)


if __name__ == "__main__":
    p = base_args(argparse.ArgumentParser())
    p.add_argument("--offset", type=int, default=5)
    p.add_argument("--spread", type=float, default=0.18)
    p.add_argument("--centre", type=float, default=0.45)
    p.add_argument("--accent", type=float, default=0.60)
    a = p.parse_args()
    print(render(a.src, a.dst, (a.w, a.h), focus=(a.fx, a.fy), seed=a.seed,
                 contrast=a.contrast, gamma=a.gamma, offset=a.offset,
                 spread=a.spread, centre=a.centre, accent=a.accent))
