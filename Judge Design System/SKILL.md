---
name: nav-judge-design
description: Use this skill to generate well-branded interfaces and assets for NAV / Judge — the editorial personal-site brand of Judge (judge@judgedice.com), a senior digital-marketing solutions architect — either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Brand in one breath
Editorial / print. Warm newsprint paper, warm-black ink, one vermilion accent used sparingly. Two faces: **Anton** (condensed poster grotesque) for headlines and section openers, always UPPERCASE; **Source Serif 4** carries everything that reads — body, subheads, and all micro-type (kickers, bylines, labels, nav, tags). One serif for prose *and* structure. No monospace anywhere. Sharp corners, hairline rules, no shadow drama, quiet motion. The voice is dry, first-person, Northeast/big-city, self-deprecating-as-confidence — "more demand than awareness." No emoji, near-iconless.

## Key files
- `readme.md` — full design guide: content fundamentals, visual foundations, iconography, index.
- `styles.css` — global entry (link this). `tokens/` — colors, typography, spacing, fonts, base.
- `components/` — Button, TextLink, NavItem, SectionLabel, Tag, Card, Rule, Callout (each with `.prompt.md`).
- `ui_kits/nav-site/` — the full personal-site recreation.
- `guidelines/` — foundation specimen cards.
