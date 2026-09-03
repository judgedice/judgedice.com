# Image sourcing — running findings

Source: Judge's Apple Photos library (6,874 items), swept newest → oldest.
Library is untagged (no titles/descriptions/keywords); People/faces data is not
reachable (Photos.sqlite is TCC-blocked, AppleScript exposes no person object),
so every frame below was identified by eye.

Direction (confirmed 2026-09-03): real faces are in scope for the four family
entries; the opinion/review entries, product, offerings and social cards stay
oblique and textural.

## Targets

| # | Slug / use | Size | Treatment | Status |
|---|---|---|---|---|
| 1 | a-tribute-to-michael-di-cesaro-2 (father) | 1600x900 | face OK | open |
| 2 | the-halfway-eulogy-3 (Chad, golf) | 1600x900 | face OK | open |
| 3 | the-ninth-decade-4 (mother, 80th) | 1600x900 | face OK | open |
| 4 | an-endorsement-and-a-marriage-5 (Emily, 2022) | 1600x900 | face OK | open |
| 5 | for-doug-6 (mentor) | 1600x900 | oblique | open |
| 6 | micro-learning-micro-results-7 (Duolingo) | 1600x900 | oblique | open |
| 7 | chicago-a-farewell-8 | 1600x900 | oblique | open |
| 8 | the-short-game-9 (OTTO, Andover) | 1600x900 | oblique | open |
| 9 | Tribute Consultation product | 1200x1200 | oblique | open |
| 10-12 | /offerings sections x3 | 1600x1000 | oblique | open |
| 13-14 | social / OG cards x2 | 1200x630 | oblique | open |

## Candidates found

Indices are positions in the library sweep (newest = 6874).

### Strong
- **#6680** `IMG_4323` — handwritten list, marker on white pad, warm wood table,
  a crossed-out word and "(over)". Reads as *writing*, not stationery. Best
  single frame found so far. Candidate: product image, or /offerings "written
  keepsakes", or `for-doug-6`.
- **#6855** `IMG_4547` — handwritten grocery list, ballpoint on white pad,
  photographed flat. Same family as #6680, slightly less character.

- **#6650-6652** `IMG_*` — near-empty recital stage: music stands, mics, piano,
  nobody at the microphone yet. The brief's "empty lectern" — the moment before
  someone speaks. Candidate: `the-halfway-eulogy-3`, or /offerings
  "celebration speeches".
- **#6656** — printed recital programme in a display case, warm ochre paper.
  Candidate: /offerings "eulogies & memorials", or a social card.

### Maybes
- #6873 `IMG_4566` — stack of shipping labels / order paperwork, warm.
- #6797 `IMG_4475` — Boston Logan parking receipt, thermal print, held in hand.
- #6759 `IMG_4410` — business card on a white envelope.
- #6818 `IMG_4494` — rusted metal with a grease-pencil batch label.
- #6813 / #6714 `IMG_4489` / `IMG_4357` — cabin interiors, wood paneling,
  window light. Texture only.
- #6832 `IMG_4524` — board game on a table, cabin, warm lamp. Oblique.
- #6688 `IMG_4333` — lake at dusk from a dock. Cool/blue; would need heavy
  treatment to sit on paper.

- #6657-6663 — concert hall, audience in the dark toward a lit stage. Texture.

## Swept so far
- 6874 → 6675 (200 newest): reviewed in full. Two strong, eight maybes.
- 6674 → 6650: reviewed. Two strong (stage, programme).

## Scope
Judge, 2026-09-03: **nothing older than 2020.**
- Rules out the Google Photos takeout in ~/Downloads/Takeout entirely (its
  newest frames are 2019) and the literal Chicago-2013 material.
- Addressable pool is the Photos library 2020+ = 4,076 stills
  (2020:44 2021:458 2022:36 2023:645 2024:1120 2025:997 2026:776), ~9h to
  sweep whole, so we work per-entry date windows instead.

## Date windows (from each entry's publish date)

| window | frames | result |
|---|---|---|
| Chad's 50th, Apr-Jun 2023 | 11 | **empty** — school concert, a kid in a suit. No Chad, no golf. |
| Emily campaign, Jan-May 2022 | 34 | **empty** — anime drawings, the dog, a sofa, screenshots. |
| for Doug, Oct-Dec 2022 | 1 | negligible |
| father's last summer, May-Oct 2021 | 248 | running |
| mother's 80th, Nov 2025-Feb 2026 | 389 | queued |
| Duolingo, Oct-Dec 2025 | 307 | low priority (opinion piece; oblique is fine) |
| OTTO / Andover, Sep-Nov 2025 | 201 | queued |
| Chicago, 2013 | 203 | **out of scope** under the 2020 floor |

The library is a phone camera roll, not an archive of the events Judge wrote
about — two of three tested windows held nothing related to their entry.
Entries 2, 3, 5, 7, 8 should be assumed oblique unless a window proves otherwise.

## Constraints hit
- Photos is set to optimise Mac storage: many originals must download from
  iCloud on export. Measured 1s/5 frames at the newest end, 47s/5 around
  position 4000, 3s/5 around position 1000. A full 6,874-frame sweep is hours.
- Library is untagged and People/faces data is unreachable, so every frame is
  identified by eye.
