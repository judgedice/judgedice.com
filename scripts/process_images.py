#!/usr/bin/env python3
"""Run every print effect over a batch of images.

Drop images into ./incoming and run it with no arguments:

    python3 scripts/process_images.py

Each input goes through all four effects and lands in ./processed_images as
<name>__<effect>.jpg, so one shot comes back as four options side by side.
halftone and duotone write .png instead: they print ink on a transparent
background, light parts clear, so the page can supply its own. Originals in ./incoming are left
alone. Reads JPEG, PNG, HEIC straight off a phone.

    python3 scripts/process_images.py                      # everything in incoming/
    python3 scripts/process_images.py --size social
    python3 scripts/process_images.py ~/Desktop/shoot      # some other folder
    python3 scripts/process_images.py a.HEIC --effects halftone,riso

    --size    entry (1600x900, default) | product (1200x1200)
              | offering (1600x1000) | social (1200x630)
    --w --h   exact size, overrides --size
    --effects comma-separated subset; default is all four
    --out     output folder (default: processed_images)

First run creates a .venv and installs Pillow/numpy/pillow-heif by itself, so
there is nothing to set up beforehand.
"""
import os
import subprocess
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VENV_PY = os.path.join(ROOT, ".venv", "bin", "python")
DEPS = ["Pillow", "numpy", "pillow-heif"]


def bootstrap():
    """Re-exec under an interpreter that has the deps, installing them once."""
    try:
        import numpy, PIL  # noqa: F401
        return
    except ImportError:
        pass

    stage = os.environ.get("_EFFECTS_BOOTSTRAPPED")
    me = os.path.abspath(__file__)

    if stage == "installed":
        sys.exit("could not install dependencies: " + ", ".join(DEPS))

    if stage == "venv":
        # already inside .venv but the deps aren't there yet — install them
        print("installing " + ", ".join(DEPS) + " ...", flush=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + DEPS,
                       check=True)
        os.environ["_EFFECTS_BOOTSTRAPPED"] = "installed"
        os.execv(sys.executable, [sys.executable, me] + sys.argv[1:])

    if not os.path.exists(VENV_PY):
        print("first run: creating .venv ...", flush=True)
        subprocess.run([sys.executable, "-m", "venv", os.path.join(ROOT, ".venv")],
                       check=True)
    # hop into the venv first and only install if it turns out to be bare,
    # so repeat runs cost nothing
    os.environ["_EFFECTS_BOOTSTRAPPED"] = "venv"
    os.execv(VENV_PY, [VENV_PY, me] + sys.argv[1:])


bootstrap()

import argparse  # noqa: E402

DROP = os.path.join(ROOT, "incoming")
EFFECTS = ["halftone", "duotone", "riso", "stencil"]
# halftone and duotone print ink on transparency, so they have to be PNGs
EXT = {"halftone": ".png", "duotone": ".png"}
SIZES = {"entry": (1600, 900), "product": (1200, 1200),
         "offering": (1600, 1000), "social": (1200, 630)}
READABLE = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".tif", ".tiff", ".webp"}


def collect(paths):
    out = []
    for p in paths:
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            for fn in sorted(os.listdir(p)):
                if os.path.splitext(fn)[1].lower() in READABLE:
                    out.append(os.path.join(p, fn))
        elif os.path.splitext(p)[1].lower() in READABLE:
            out.append(p)
        else:
            print(f"skipping (not an image): {p}")
    return out


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("inputs", nargs="*", default=[DROP])
    ap.add_argument("--out", default="processed_images")
    ap.add_argument("--size", choices=sorted(SIZES), default="entry")
    ap.add_argument("--w", type=int); ap.add_argument("--h", type=int)
    ap.add_argument("--effects", default=",".join(EFFECTS))
    ap.add_argument("--fy", type=float, default=0.5)
    a = ap.parse_args()

    w, h = SIZES[a.size]
    if a.w: w = a.w
    if a.h: h = a.h

    chosen = [e.strip() for e in a.effects.split(",") if e.strip()]
    unknown = [e for e in chosen if e not in EFFECTS]
    if unknown:
        sys.exit(f"unknown effect(s): {', '.join(unknown)}\nchoose from: {', '.join(EFFECTS)}")

    files = collect(a.inputs or [DROP])
    if not files:
        if not a.inputs or a.inputs == [DROP]:
            os.makedirs(DROP, exist_ok=True)
            sys.exit(f"nothing to do — drop images into {DROP}/ and run this again")
        sys.exit("no images found")
    os.makedirs(a.out, exist_ok=True)

    print(f"{len(files)} image(s) x {len(chosen)} effect(s) -> {a.out}/  at {w}x{h}\n")
    made, failed = 0, []
    for i, src in enumerate(files, 1):
        stem = os.path.splitext(os.path.basename(src))[0]
        print(f"[{i}/{len(files)}] {stem}")
        for effect in chosen:
            dst = os.path.join(a.out, f"{stem}__{effect}{EXT.get(effect, '.jpg')}")
            # seed off the filename so paper texture differs per image but the
            # same input always reproduces the same sheet
            seed = zlib.crc32(stem.encode()) % 9973
            r = subprocess.run(
                [sys.executable, os.path.join(HERE, f"{effect}.py"), src, dst,
                 "--w", str(w), "--h", str(h), "--seed", str(seed),
                 "--fy", str(a.fy)],
                capture_output=True, text=True)
            if r.returncode:
                failed.append((stem, effect, r.stderr.strip().splitlines()[-1:] or [""]))
                print(f"      {effect:9s} FAILED")
            else:
                made += 1
                print(f"      {effect:9s} ok")

    print(f"\n{made} file(s) written to {a.out}/")
    for stem, effect, msg in failed:
        print(f"  failed: {stem} [{effect}] {msg[0] if msg else ''}")


if __name__ == "__main__":
    main()
