"""Duotone — continuous tone, no dot screen.

The quiet one. Where halftone.py breaks the image into dots, this keeps a
smooth ink ramp and lets grain do the work, so fine detail survives:
handwriting, small type, receipts, anything with texture that a dot screen
would eat. Closest to a warm monochrome photograph printed on stock.

    .venv/bin/python scripts/duotone.py shot.HEIC out.jpg --w 1600 --h 900

    --grain 0.045   film grain amount; 0 is clinical, 0.09 is coarse
    --lift  0.06    veils the shadows the way ink sinks into uncoated paper
"""
import argparse
import numpy as np
from PIL import ImageFilter, Image
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _effects_common import tone, sheet, ink_on, save, base_args, PAPER, INK


def render(src, dst, size, focus=(.5, .5), seed=0, contrast=1.10, gamma=1.20,
           grain=0.045, lift=0.06):
    t = tone(src, size, focus=focus, contrast=contrast, gamma=gamma,
             floor=0.04, ceil=1.0)
    rng = np.random.default_rng(seed + 991)

    # ink coverage is simply the inverse of tone, softened at the top end so
    # highlights hold a whisper of ink instead of dropping to bare paper
    cov = 1.0 - t
    cov = np.clip(cov * (1.0 - lift) + lift * cov ** 0.5, 0, 1)
    cov = np.clip(cov + rng.normal(0, grain, cov.shape), 0, 1)

    pap = sheet(size, seed=seed)
    base = np.repeat(pap[:, :, None], 3, axis=2) * (np.array(PAPER, np.float32) / 255.0)
    return save(ink_on(base, cov, INK), dst)


if __name__ == "__main__":
    p = base_args(argparse.ArgumentParser())
    p.add_argument("--grain", type=float, default=0.045)
    p.add_argument("--lift", type=float, default=0.06)
    a = p.parse_args()
    print(render(a.src, a.dst, (a.w, a.h), focus=(a.fx, a.fy), seed=a.seed,
                 contrast=a.contrast, gamma=a.gamma, grain=a.grain, lift=a.lift))
