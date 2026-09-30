#!/usr/bin/env python3
"""Generate the algorithmic gradient behind /random-4.

"Two States" — the conceptual seed is the Hamming line the page carries: two
pure conditions that you seldom, if ever, see purely.  So the image is built
from two noise fields that never appear alone:

  - a *science* field: broad, low-frequency, exploratory, drifting to blue
  - an *engineering* field: finer, more octaves, more structure, drifting to
    vermilion

Each one domain-warps the other (Inigo Quilez's fbm(p + fbm(p)) trick), and the
mix weight between them is itself a warped field that is clamped away from 0
and 1 — so no pixel in the frame is ever purely one field.  That clamp is the
whole idea; everything else is finish.

The result is quantised into flat bands with an 8x8 ordered dither, which is
what gives it the riso/screen-print edge the rest of the site already has,
and it is mapped through Judge's own palette (blue -> ink -> vermilion).

Deterministic: the same --seed always produces the same image.

    .venv/bin/python scripts/gen_gradient_art.py --out processed_images/04_twostates.png
"""
import argparse
import sys

import numpy as np
from PIL import Image

# Judge Design System, in ramp order: blue -> ink -> vermilion
STOPS = [
    (0.00, (0x27, 0x46, 0x54)),   # blue
    (0.22, (0x1B, 0x33, 0x3E)),   # blue-deep
    (0.46, (0x10, 0x0C, 0x08)),   # black
    (0.58, (0x1C, 0x17, 0x12)),   # ink
    (0.80, (0xA6, 0x32, 0x1C)),   # vermilion-deep
    (1.00, (0xCB, 0x41, 0x27)),   # vermilion
]

# the clamp that makes the piece: neither field is ever seen pure
PURITY_FLOOR = 0.12

BAYER8 = np.array([
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
], dtype=np.float64) / 64.0 - 0.5


def vnoise(xs, ys, n, lat):
    """Periodic value noise on an n x n lattice, smoothstep-interpolated."""
    x0 = np.floor(xs).astype(np.int64)
    y0 = np.floor(ys).astype(np.int64)
    fx, fy = xs - x0, ys - y0
    sx = fx * fx * (3.0 - 2.0 * fx)
    sy = fy * fy * (3.0 - 2.0 * fy)
    x0 %= n
    y0 %= n
    x1 = (x0 + 1) % n
    y1 = (y0 + 1) % n
    a = lat[y0, x0] + (lat[y0, x1] - lat[y0, x0]) * sx
    b = lat[y1, x0] + (lat[y1, x1] - lat[y1, x0]) * sx
    return a + (b - a) * sy


def fbm(u, v, rng, octaves, base, gain):
    """Fractional Brownian motion; u, v are in turns, not pixels."""
    total = np.zeros_like(u)
    amp, norm, n = 1.0, 0.0, base
    for _ in range(octaves):
        total += amp * vnoise(u * n, v * n, n, rng.random((n, n)))
        norm += amp
        amp *= gain
        n *= 2
    return total / norm


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def stretch(a, lo=1.0, hi=99.0):
    p0, p1 = np.percentile(a, lo), np.percentile(a, hi)
    return np.clip((a - p0) / (p1 - p0), 0.0, 1.0)


def ramp(t):
    """Piecewise-linear palette lookup; t in [0, 1]."""
    out = np.zeros(t.shape + (3,), dtype=np.float64)
    for (p0, c0), (p1, c1) in zip(STOPS, STOPS[1:]):
        m = (t >= p0) & (t <= p1)
        f = (t[m] - p0) / (p1 - p0)
        for c in range(3):
            out[..., c][m] = c0[c] + (c1[c] - c0[c]) * f
    return out


def build(size, seed, levels, warp, grain):
    rng = np.random.default_rng(seed)
    v, u = np.meshgrid(np.linspace(0, 1, size, endpoint=False),
                       np.linspace(0, 1, size, endpoint=False),
                       indexing="ij")

    # first warp: displace the plane by a field of its own
    wu = fbm(u + 0.0, v + 0.0, rng, 4, 2, 0.55)
    wv = fbm(u + 4.7, v + 2.3, rng, 4, 2, 0.55)
    pu = u + warp * (wu - 0.5)
    pv = v + warp * (wv - 0.5)

    # second warp, on the already-warped plane
    qu = fbm(pu + 1.7, pv + 9.2, rng, 5, 3, 0.5)
    qv = fbm(pu + 8.3, pv + 2.8, rng, 5, 3, 0.5)
    pu = pu + warp * 0.75 * (qu - 0.5)
    pv = pv + warp * 0.75 * (qv - 0.5)

    # the two fields: one broad and exploratory, one fine and structured
    science = fbm(pu + 0.6, pv + 3.1, rng, 4, 2, 0.58)
    engineering = fbm(pu + 5.4, pv + 7.9, rng, 7, 5, 0.47)

    # the mix is itself a warped field, and it never reaches either pole
    bias = fbm(pu + 2.9, pv + 6.2, rng, 3, 2, 0.6)
    m = smoothstep(0.5 * (pu + pv) + 0.55 * (bias - 0.5))
    m = PURITY_FLOOR + (1.0 - 2.0 * PURITY_FLOOR) * m

    field = stretch((1.0 - m) * stretch(science) + m * stretch(engineering))
    # push the mix itself into the tone so the two poles read as colour
    field = stretch(0.45 * field + 0.55 * m)

    # flat bands with an ordered dither at the edges -> screen-print feel
    tile = np.tile(BAYER8, (size // 8 + 1, size // 8 + 1))[:size, :size]
    banded = np.floor(np.clip(field + tile / levels, 0, 0.9999) * levels)
    t = banded / (levels - 1.0)

    rgb = ramp(np.clip(t, 0.0, 1.0))

    # a whisper of vignette so the centred quote always has the darkest ground
    r = np.sqrt((u - 0.5) ** 2 + (v - 0.5) ** 2) / 0.7071
    rgb *= (1.0 - 0.16 * smoothstep((r - 0.35) / 0.65))[..., None]

    rgb += rng.normal(0.0, grain, rgb.shape)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), mode="RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=1920)
    ap.add_argument("--seed", type=int, default=1947)   # Hamming at Bell Labs
    ap.add_argument("--levels", type=int, default=13)
    ap.add_argument("--warp", type=float, default=0.42)
    ap.add_argument("--grain", type=float, default=2.2)
    ap.add_argument("--webp", help="also write a webp here")
    ap.add_argument("--quality", type=int, default=78)
    ap.add_argument("--preview", help="also write a small png here, to look at")
    a = ap.parse_args()

    img = build(a.size, a.seed, a.levels, a.warp, a.grain)
    img.save(a.out, optimize=True)
    print(f"  {a.out}  {a.size}x{a.size}  RGB  {_kb(a.out)}")
    if a.webp:
        img.save(a.webp, quality=a.quality, method=6)
        print(f"  {a.webp}  q{a.quality}  {_kb(a.webp)}")
    if a.preview:
        img.resize((720, 720), Image.LANCZOS).save(a.preview)
        print(f"  {a.preview}  720x720")
    return 0


def _kb(p):
    import os
    n = os.path.getsize(p)
    return f"{n/1048576:.2f} MB" if n > 1048576 else f"{n/1024:.0f} KB"


if __name__ == "__main__":
    sys.exit(main())
