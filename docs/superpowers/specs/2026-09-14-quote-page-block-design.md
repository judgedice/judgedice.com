# Quote Page block — design

**Date:** 2026-09-14
**Status:** approved

A page that is nothing but a background image and one large quote, between the
site's own header and footer. Delivered as a reusable block in the Judge palette
rather than a page template, so a quote page is "new blank page, drop the block".

## Decisions

| Question | Decision | Rejected |
|---|---|---|
| Delivery | Snippet in the Judge palette group | Odoo's New Page template picker (Odoo 19 appears to enumerate its groups from JS, so a custom entry may not register); a single hand-built page (not reusable) |
| Light / dark | Odoo's native colour-combination picker, via `o_cc` on the section | Two separate palette entries; a class toggled by hand in the HTML editor. A genuine two-state option in the builder panel is **not possible**: Odoo 19 removed the XML `snippet_options` system (zero such views exist in the DB) and a custom option would need shipped JS, which Odoo Online cannot deploy. |
| Background image | Chosen per page with Odoo's native Background option, plus an automatic veil | No veil (a busy photo eats the quote); baking an image into the block |
| Anatomy | Quote + attribution line only | Kicker, CTA link, viewport lock |

## Structure

```
section.s_jd_quotepage.o_cc.o_cc1        <- Odoo paints the chosen bg image here
  div.s_jd_quotepage_scrim               <- the veil; own element, see note
  div.s_jd_quotepage_inner
    blockquote.s_jd_quotepage_block
      p.s_jd_quotepage_text              <- Source Serif italic, large
      footer.s_jd_quotepage_cite         <- attribution
```

**Why the veil is its own element:** a `background-image` on an element covers
that element's `background-color`, so the colour combination's background can't
show through the photo. A separate absolutely-positioned child is the only way
to tint the image while leaving the builder's native background-image option
working untouched.

## Light / dark mapping

The colour-combination class is the switch. Presets 1–3 are the light end of the
palette and 4–5 the dark end (defined in `scripts/cc_and_publish.py`):

| Preset | Veil | Quote | Attribution |
|---|---|---|---|
| `o_cc1` `o_cc2` `o_cc3` | paper @ 72% | `--ink` | `--ink-faint`, name `--ink-soft` |
| `o_cc4` `o_cc5` | ink @ 62% | `--paper` | paper @ 62%, name `--paper` |

Accepted trade-off: this surfaces five buttons where the brief asked for two.
Presets 1 and 5 are the intended light/dark answer; 2–4 are intermediate.

## Type

- Quote — `--font-serif`, italic, `clamp(1.75rem, 5vw, 3.5rem)`, line-height
  1.18, measure capped at 26ch so it breaks into short lines, `text-wrap:balance`.
- Attribution — reuses the `.s_jd_quote_cite` treatment from the quotes block
  verbatim: Source Serif roman, `--text-meta`, uppercase, `--tracking-label`.
- Every `<p>` inside the blockquote is styled, not just `.s_jd_quotepage_text`.
  The editor re-nests text into sibling `<p>`s when a link is applied, and the
  quote silently drops to body type if only the first is styled. View 2732
  carries the same guard and the same comment.

## Height

No viewport lock. Generous vertical padding (`clamp(6rem, 18vh, 12rem)`) over a
`min-height: 60vh` floor, so a short quote still leaves the background image room
to read. Below 768px the floor drops to 50vh and the 26ch measure is released.

## Placeholder content

A prompt, not an invented quote attributed to anyone — the discipline the quotes
block already follows, and what hard rule 7 requires.

## Build

`scripts/add_quote_page_block.py`, following `add_quotes_block.py`:
idempotent, sentinel-guarded, XML validated with ElementTree, dry-run by default,
`--apply` to write. Three writes, all scoped to `website_id=2`:

1. create the snippet view `website.s_jd_quote_page`
2. register it in the Judge palette group (view **2271**)
3. append the `.s_jd_quotepage` CSS to `website[2].custom_code_head`

No homepage instance — this is a page block, not a homepage section.
