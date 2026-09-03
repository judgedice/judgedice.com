# Shot list — judgedice.com covers

Everything here is shot by Judge, on a table, in daylight, and run through
`scripts/halftone.py`. That treatment is already built and proven: it flattens
an iPhone frame into the same screenprint world as the hero portrait, so the
camera does not need to be good — the *objects* and the *light* carry it.

## Why a shoot rather than more searching

The 2020+ library was searched by date window against every entry's publish
date. It does not contain the events the entries describe — no Michael, no
Chad's 50th, no campaign. What it does contain, and what already works, is
incidental paper: a shopping list, a parking receipt, a shipping label. That is
the seam worth mining, and it is far easier to shoot ten deliberate frames than
to find them by accident.

## How to shoot

- **Light:** one window, indirect, north-facing if you have it. No flash, no
  overhead. Late morning.
- **Surface:** the warm wood table already in `IMG_4323`. It halftones well.
- **Angle:** square-on from above for paper; low and raking for objects.
- **Fill the frame.** The halftone eats fine detail, so get close — one object,
  edge to edge. The weak covers in this batch all failed by being too far away.
- **Shoot horizontal**, 3–4 frames each, slightly different angles.
- **Don't tidy.** Creases, coffee rings, crossings-out and thumbprints are the
  whole point. `IMG_4323` works because of the crossed-out word and the
  "(over)".

## The frames

| # | Slot | What to put in front of the camera |
|---|---|---|
| 1 | `the-ninth-decade-4` (mother, 80th) | A stack of eight or nine birthday cards, envelopes still on, fanned so only the edges and a bit of handwriting show. Ninth decade = the depth of the stack. |
| 2 | `an-endorsement-and-a-marriage-5` | A campaign lawn sign face-down on the table, or a folded local-paper endorsement page. Political object, no faces, no live candidate's name if you'd rather. |
| 3 | `chicago-a-farewell-8` | A packing box flap with a shipping label, tape half-pulled. A farewell to a place is a box, not a skyline. |
| 4 | `written-keepsakes` (offerings) | A short handwritten note on good paper beside a pen, folded once. Distinct from the shopping lists — deliberate, not domestic. |
| 5 | `eulogies-and-memorials` (offerings) | A folded order-of-service programme, held open, thumb visible at the fold. Print, paper, no candles. |
| 6 | `a-tribute-to-michael-di-cesaro-2` | Your father's own handwriting if any survives — a note, an inscription, a tool with his initials. Nothing of him, something of his. This is the one frame worth hunting the house for. |
| 7 | `the-halfway-eulogy-3` (Chad, golf) | A scorecard, pencil still on it, halfway down the column. The metaphor is already yours; the object just has to be a card and a pencil. |
| 8 | Spare / rotation | Typewriter or keyboard keys raking light, very close. |
| 9 | Spare / rotation | A pen nib or biro tip on paper mid-stroke. |
| 10 | Spare / rotation | The edge of a stack of paper, shallow focus, warm light. |

Frames 8–10 are the reserve that stops one picture doing four jobs, which is
the main weakness of the current batch.

## After the shoot

Drop the files in a folder and run, per image:

```
scripts/halftone.py <src> assets/entries/<slug>.jpg --w 1600 --h 900
```

Sizes: entries 1600x900 · product 1200x1200 · offerings 1600x1000 · social
1200x630. `--cell` sets the dot pitch (4–5 is right), `--fy` moves the crop
vertically, `--seed` changes the paper creases so no two images share a texture.
