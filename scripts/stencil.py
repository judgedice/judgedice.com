"""Stencil — high-contrast posterisation, cut down to a few flat tones.

The loud one. Tone is crushed to three or four levels with a noise dither at
the boundaries, so the image reads as cut shapes rather than a photograph —
closer to a linocut or a screenprinted poster than to print reproduction. Wants
strong light and a bold subject; it will destroy anything subtle, which is the
point. Good for social cards, where the image competes with a headline.

    .venv/bin/python scripts/stencil.py shot.HEIC out.jpg --w 1200 --h 630

    --levels 3      number of flat tones; 2 is a pure stencil, 5 is gentler
    --dither 0.028  noise at the tone boundaries; 0 gives hard vector edges
    --consolidate 3 blur radius applied before quantising. This is what makes
                    the result read as cut shapes rather than grain: without it
                    a photograph's fine tonal noise fragments every level
"""
import argparse
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _effects_common import tone, sheet, ink_on, save, base_args, PAPER, INK


def render(src, dst, size, focus=(.5, .5), seed=0, contrast=1.55, gamma=1.05,
           levels=3, dither=0.028, consolidate=3.0):
    t = tone(src, size, focus=focus, contrast=contrast, gamma=gamma,
             floor=0.0, ceil=1.0)
    rng = np.random.default_rng(seed + 77)

    # consolidate first: smoothing merges a photograph's tonal noise into solid
    # regions, so quantising yields shapes instead of speckle
    if consolidate > 0:
        from PIL import Image as _I, ImageFilter as _F
        t = np.asarray(_I.fromarray((t * 255).astype(np.uint8), "L")
                       .filter(_F.GaussianBlur(consolidate))
                       ).astype(np.float32) / 255.0

    # then dither: noise pushes pixels either side of each step, so boundaries
    # break up into grain instead of banding
    q = np.clip(t + rng.normal(0, dither, t.shape), 0, 1)
    q = np.round(q * (levels - 1)) / (levels - 1)

    pap = sheet(size, seed=seed)
    base = np.repeat(pap[:, :, None], 3, axis=2) * (np.array(PAPER, np.float32) / 255.0)
    return save(ink_on(base, 1.0 - q, INK), dst)


if __name__ == "__main__":
    p = base_args(argparse.ArgumentParser())
    p.set_defaults(contrast=1.55, gamma=1.05)
    p.add_argument("--levels", type=int, default=3)
    p.add_argument("--dither", type=float, default=0.028)
    p.add_argument("--consolidate", type=float, default=3.0)
    a = p.parse_args()
    print(render(a.src, a.dst, (a.w, a.h), focus=(a.fx, a.fy), seed=a.seed,
                 contrast=a.contrast, gamma=a.gamma, levels=a.levels,
                 dither=a.dither, consolidate=a.consolidate))
