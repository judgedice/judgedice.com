# incoming

Drop images in here, then run:

    python3 scripts/process_images.py

Every image gets put through all four print effects — halftone, duotone, riso,
stencil — and the results land in `../processed_images/` named
`<name>__<effect>.jpg`. Originals in this folder are left untouched, so you can
re-run as often as you like.

Takes JPEG, PNG, HEIC, TIFF and WebP. HEIC straight off the phone is fine.

Useful variants:

    python3 scripts/process_images.py --size social       # 1200x630 instead of 1600x900
    python3 scripts/process_images.py --effects riso      # just one effect
    python3 scripts/process_images.py --fy 0.35           # crop nearer the top

Images dropped here are gitignored — this README is the only tracked file.
