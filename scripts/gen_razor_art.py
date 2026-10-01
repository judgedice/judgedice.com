#!/usr/bin/env python3
"""Generate the algorithmic background behind /random-5.

"The Razor" — where /random-4's gradient was two fields refusing to separate,
this one is a field being *taken away*.  The conceptual seed is Ockham's line:
plurality is never to be posited without necessity.

So the number of noise octaves contributing to the field is not constant: it
decays across the plane.  On one side every octave is present and the field is
turbulent with detail; on the other all but the first have been gated off and
what is left is a single smooth sweep.  Nothing is added to make the quiet side
quiet — complexity is simply not posited there.

Over that run a handful of straight half-plane cuts: hard tonal steps along dead
straight lines, the one thing /random-4 had none of.  Those are the razor.

Quantised into 8 flat bands (fewer than random-4's 13 — the simpler page gets
the simpler separation) and ramped through the paper end of Judge's palette,
so this one is a *light* quote page where the others are dark.

Deterministic: the same --seed always produces the same image.

    .venv/bin/python scripts/gen_razor_art.py --out processed_images/05_razor.png
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

from gen_gradient_art import BAYER8, smoothstep, stretch, vnoise

# the paper end of the Judge palette: this page runs light
STOPS = [
    (0.000, (0xF8, 0xF3, 0xE8)),   # paper-raised
    (0.200, (0xEA, 0xE2, 0xD2)),   # paper-sunk
    (0.400, (0xD8, 0xCF, 0xBE)),   # line
    (0.580, (0xC3, 0xB8, 0xA3)),   # line-strong
    (0.740, (0x8B, 0x83, 0x7A)),   # ink-faint
    (0.857, (0x57, 0x51, 0x4A)),   # ink-soft  <- the 7th of 8 bands
    (1.000, (0xCB, 0x41, 0x27)),   # vermilion <- the 8th, and the only red
]


def ramp(t):
    out = np.zeros(t.shape + (3,), dtype=np.float64)
    for (p0, c0), (p1, c1) in zip(STOPS, STOPS[1:]):
        m = (t >= p0) & (t <= p1)
        f = (t[m] - p0) / (p1 - p0)
        for c in range(3):
            out[..., c][m] = c0[c] + (c1[c] - c0[c]) * f
    return out


def decaying_fbm(u, v, rng, octaves, base, gain, complexity):
    """fBm whose octave count is a per-pixel function of `complexity`.

    Octave o is gated by clip(complexity*octaves - o, 0, 1), smoothed: octave 0
    is everywhere, the finest octave only where complexity is at its highest.
    The normaliser is per-pixel too, so the quiet side stays in range instead
    of fading to flat grey.
    """
    total = np.zeros_like(u)
    norm = np.zeros_like(u)
    amp, n = 1.0, base
    for o in range(octaves):
        g = smoothstep(complexity * octaves - o)
        total += amp * g * vnoise(u * n, v * n, n, rng.random((n, n)))
        norm += amp * g
        amp *= gain
        n *= 2
    return total / np.maximum(norm, 1e-6)


def cuts(u, v, rng, count, depth):
    """Straight half-plane steps — the razor strokes."""
    out = np.zeros_like(u)
    for i in range(count):
        th = rng.uniform(0, np.pi)
        d = rng.uniform(-0.34, 0.34)
        side = np.cos(th) * (u - 0.5) + np.sin(th) * (v - 0.5) - d
        # strong first cut, progressively lighter after it
        out += depth * (0.55 ** i) * np.sign(side)
    return out


def build(size, seed, levels, cut_count, cut_depth, grain, gamma):
    rng = np.random.default_rng(seed)
    v, u = np.meshgrid(np.linspace(0, 1, size, endpoint=False),
                       np.linspace(0, 1, size, endpoint=False),
                       indexing="ij")

    # how much structure is permitted at each point: a ramp, gently warped so
    # the boundary between busy and quiet is not a straight line
    from gen_gradient_art import fbm
    bend = fbm(u + 3.3, v + 7.1, rng, 3, 2, 0.6)
    complexity = smoothstep(1.7 * (0.82 * u + 0.18 * v) - 0.3
                            + 0.34 * (bend - 0.5))

    field = decaying_fbm(u, v, rng, 7, 2, 0.52, complexity)
    field = stretch(field) + cuts(u, v, rng, cut_count, cut_depth)
    # bias the distribution downward so the top band - the only vermilion one -
    # stays an accent rather than a mass
    field = stretch(field) ** gamma

    tile = np.tile(BAYER8, (size // 8 + 1, size // 8 + 1))[:size, :size]
    banded = np.floor(np.clip(field + tile / levels, 0, 0.9999) * levels)
    t = banded / (levels - 1.0)

    rgb = ramp(np.clip(t, 0.0, 1.0))
    rgb += rng.normal(0.0, grain, rgb.shape)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def _kb(p):
    n = os.path.getsize(p)
    return f"{n/1048576:.2f} MB" if n > 1048576 else f"{n/1024:.0f} KB"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=1920)
    ap.add_argument("--seed", type=int, default=1639)   # Punch's phrasing
    ap.add_argument("--levels", type=int, default=8)
    ap.add_argument("--cuts", type=int, default=3)
    ap.add_argument("--cut-depth", type=float, default=0.07)
    ap.add_argument("--grain", type=float, default=1.6)
    ap.add_argument("--gamma", type=float, default=1.9)
    ap.add_argument("--webp")
    ap.add_argument("--quality", type=int, default=80)
    ap.add_argument("--preview")
    a = ap.parse_args()

    img = build(a.size, a.seed, a.levels, a.cuts, a.cut_depth,
                a.grain, a.gamma)
    img.save(a.out, optimize=True)
    print(f"  {a.out}  {a.size}x{a.size}  RGB  {_kb(a.out)}")
    if a.webp:
        img.save(a.webp, quality=a.quality, method=6)
        print(f"  {a.webp}  q{a.quality}  {_kb(a.webp)}")
    if a.preview:
        img.resize((720, 720), Image.LANCZOS).save(a.preview)
    return 0


if __name__ == "__main__":
    sys.exit(main())
