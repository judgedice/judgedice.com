# Judge — Design System

An editorial, print-inspired design system for the personal site of **Judge** (`judge@judgedice.com`) — a senior digital-marketing solutions architect with a 25-year career. 

The site has a philosophy buried in it: *more demand than awareness.* Judge is the kind of person people don't know they need until they're in the room with him. Every design decision should create the feeling of **discovering something good that wasn't being marketed at you** — confident, understated, dry.

## Sources given

- **Brand & copy brief** (pasted text): section labels, hero tagline, full body copy for Work Life / Home Life / The Exciting Stuff / Connect, plus per-section "spirit" notes on tone.

---

## CONTENT FUNDAMENTALS

**Voice: dry, direct, Northeast/big-city, senior. Humor is earned, not performed.**

- **Person:** First person throughout. "I've been building things on the internet since before it was cool." The site is *him*, not a company.
- **Casing:** Sentence case for prose. Section labels and metadata are UPPERCASE mono. The hero tagline uses Title-ish sentence case: "Delivering Joy since the turn of the Century."
- **Sentence length:** Short. Declarative. Especially in Home Life, which should *exhale* — "I have a family that puts up with me." No subordinate-clause pile-ups.
- **Place:** Northeast, big-city sensibility (born in New England, time in South Carolina and Florida, back in New England). Not Midwestern. When geography surfaces it's the Northeast — "opinions about winters," not cornfields.
- **Self-deprecation as credibility:** Claims are undercut on purpose. "That sounds like a brag. It's mostly just a fact." The undercut *is* the confidence.
- **Asides in parentheses / em-dashes:** They sound like him. "(and when necessary jumped in to fix the integration the night before launch)", "Flash is dead, long live the API." Keep them.
- **The tools list is proof, not bragging.** Render tool names plainly (mono tags). Don't dress them up with icons or three-word headlines.
- **One ask, made obvious.** Connect has a single CTA and one email address. No eight-field form, no "explore synergies."
- **No emoji. No exclamation-point enthusiasm. No capabilities-deck cadence** ("We leverage best-in-class…"). If it sounds like a conference talk, rewrite it as if said at dinner.

**Examples that define the register:**

- Hero: *"Delivering Joy since the turn of the Century."* — a statement, not a description. Give it space.
- Work Life: *"Where a roadmap stops being a slide and starts being a thing that works in production."*
- The Exciting Stuff: *"…which will require a ticket that becomes a different ticket. I have stories."*
- Home Life: *"There is no force stronger than the gravity of free lunch, and I will not be argued out of this."*
- Connect: *"I'm responsive on email, better on a call, and genuinely bad at LinkedIn DMs."*

---

## VISUAL FOUNDATIONS

The system is **editorial / print**: warm newsprint paper, warm-black ink, one confident vermilion accent, generous negative space, and hairline rules doing the work that shadows do elsewhere. It should read like a well-set independent magazine, not a SaaS marketing page.

- **Color:** Warm paper background (`--paper #F2ECDF`), warm near-black ink (`--ink #1C1712`), and a single editorial **vermilion** accent (`--vermilion #CB4127`) used sparingly — a spice, never the meal. A muted **ink-blue** (`--blue #274654`) is available for the rare second accent. Neutrals are all warm greys; there is no pure cold white in body surfaces (white is reserved for hard edges only).
- **Type:** Two faces. **Anton** — a condensed poster grotesque — is the display voice for headlines, hero, and section openers, always set UPPERCASE with tight leading. **Source Serif 4** is the text voice and carries everything that reads: body, subheads, and every piece of micro-type (kickers, bylines, labels, nav, tool tags, metadata) — the "one-typeface" discipline where prose and structure share a serif. There is **no monospace anywhere** in the system. The display/text split is the core motif: Anton shouts, Source Serif thinks.
- **Type scale:** Editorial extremes. Hero up to 120px with tight tracking (−0.02em) and leading (1.02); body at 19px with roomy 1.62 leading. Big things are *big*, and there's air around them.
- **Spacing:** 8px base, but the top of the scale is generous (96–192px) so the hero and section breaks can breathe. Sections are separated by whitespace and rules, not boxes.
- **Backgrounds:** Solid warm paper. **No gradients, no photographic hero, no mesh, no texture overlays.** Depth comes from type scale, rules, and negative space. (An optional very-fine paper grain is acceptable but off by default.)
- **Borders & rules:** Hairline `1px solid --line` for containers; a `1px/2px solid --ink` **editorial rule** for section dividers and framed cards. Rules frequently carry a small mono label sitting on the line.
- **Corner radius:** Near-sharp. `0` for framed/editorial elements, `2px` for buttons/inputs/tags, `3px` for soft cards. Nothing is pill-shaped or heavily rounded.
- **Shadow:** Mostly **none** — print doesn't cast shadows. A soft `--shadow-card` appears only on hover for genuinely clickable cards. Never a resting drop shadow on static content.
- **Cards:** Paper-raised surface with either a hairline border (`3px` radius) or the `framed` variant — no border except a 2px ink rule along the top edge, sharp corners. Quiet.
- **Motion:** Quiet and considered — short fades and slides (140–240ms), `ease-out`, **no bounce, no spring, no infinite loops**. The hero can do one staggered reveal on load. Reduced-motion always shows final state.
- **Hover states:** Links darken vermilion and fill their underline; nav items slide a 1px accent underline in from the left; primary buttons darken to `--vermilion-deep`; secondary buttons invert to ink fill; cards (only if clickable) lift 2px.
- **Press states:** No shrink/scale games. Color deepens; that's it.
- **Transparency & blur:** Used almost never. This is opaque, printed-page design. No glassmorphism.
- **Imagery vibe:** If photography is ever added it should be warm, natural, unglamorous — him at dinner, not him at a conference. B&W or warm-toned, never stock-bright. None is included here by default.

---

## ICONOGRAPHY

**This brand is deliberately near-iconless.** The spirit notes are explicit: *"No icons. No three-word headlines followed by three bullet points."* Meaning is carried by type, rules, and mono labels — not by decorative glyphs.

- **No icon font, no icon set is bundled**, because the brand's voice rejects the capabilities-deck / icon-grid convention.
- The **only glyph in regular use is the arrow `→`** (U+2192), for standalone CTAs and "read more" affordances. It is set in Source Serif 4 to match the label type.
- **Section numbering** (`01`–`04`) in Source Serif 4 acts as the closest thing to an icon system — a wayfinding motif, not decoration.
- **No emoji, ever.** They'd puncture the dry register.
- **Middot `·`** (U+00B7) is the canonical separator for inline tool lists ("AEM · AJO · Workfront"), matching the source copy.
- If a future need for functional UI icons arises (e.g. an external-link or email glyph in a real build), substitute **Lucide** (thin, 1.5px stroke, CDN-available) as the closest match to the hairline aesthetic and note it — but default to *no icon* first. **No brand logo or mark was provided; none has been invented.** The wordmark is simply the name "Judge" set in Source Serif 4 with a vermilion period (see the Brand → Wordmark specimen). Replace with a real mark if one exists.

---

## Components

Reusable primitives, sized to a personal-site brand (not a full app). Each lives in `components/<group>/` with a `.jsx`, `.d.ts`, `.prompt.md`, and a directory card.

- **Button** (`forms/`) — mono-label editorial button; `primary` / `secondary` / `ghost`, three sizes, optional `arrow`.
- **TextLink** (`forms/`) — inline / standalone link with fill-on-hover underline; `muted` and `arrow` options.
- **NavItem** (`navigation/`) — one oblique nav label with faint index and slide-in accent underline.
- **Pager** (`navigation/`) — prev / next page navigation for the foot of a standalone page.
- **Footer** (`navigation/`) — shared site footer: wordmark, optional page links, serif tagline.
- **SectionLabel** (`content/`) — mono uppercase section kicker; optional `index` and trailing `rule`.
- **PageHeader** (`content/`) — standalone-page masthead: numbered kicker + Anton title + serif lead; `tone` paper/ink.
- **Tag** (`content/`) — mono chip for tool / capability lists; `emphasis` tint.
- **Card** (`content/`) — restrained paper container; `framed` (top ink rule) and `hover` (lift) variants.
- **Rule** (`content/`) — horizontal divider, hairline / strong / ink, with optional mono label on the line.
- **Callout** (`content/`) — dry aside / pull-quote with a left vermilion rule; `aside` / `quote` variants.

*Intentional scope note:* No Toast, Modal, Avatar, Tabs, or form-heavy primitives are included — the brand is a single narrative site with one ask, and inventing app chrome it doesn't use would mislead. Add them only if the product grows into something that needs them.

---

## Templates

Starting-point layouts a consuming project can copy whole. Each lives in `templates/<slug>/` with a `<Slug>.dc.html` entry and a `ds-base.js` that links this system.

- **Article** (`templates/article/`) — editorial article page. One `layout` tweak switches the hero-image treatment across four rules: **overlay** (headline on the image behind a gradient scrim, default), **full-bleed** (image edge-to-edge above the masthead), **split** (headline and image side by side), **portrait float** (no top hero; a 3:4 image floats inside the body). The byline starts as a single rule and expands to the full block on hover/focus. Uses only the system's two faces — Anton + Source Serif 4.

---

## UI kit

- **`ui_kits/nav-site/`** — the NAV / Judge personal site. Now a **multi-page** site: `index.html` (hero landing) plus `work.html`, `home.html`, `exciting.html`, `connect.html`. A shared `Page.jsx` shell wraps every page with the sticky `Header`, the section body, an automatic `Pager` (prev/next), and the `Footer`; each content page opens with a `PageHeader` masthead. Built from the component primitives.

---

## Foundation specimens (Design System tab)

`guidelines/` holds the small `@dsCard` specimens: **Colors** (neutrals, accent), **Type** (display, headings, body, mono), **Spacing** (scale, rules & radius), **Brand** (wordmark, nav labels, voice).

---

## Index / manifest

- `styles.css` — global entry (imports only). Consumers link this.
- `tokens/` — `fonts.css`, `colors.css`, `typography.css`, `spacing.css`, `base.css`.
- `components/` — `forms/`, `content/`, `navigation/`.
- `guidelines/` — foundation specimen cards.
- `ui_kits/nav-site/` — the personal-site UI kit.
- `SKILL.md` — Agent-Skills-compatible entry for downloading this system into Claude Code.
- `readme.md` — this file.

---

## Caveats

- **Fonts are substitutions.** No brand font files were provided, so the system loads **Anton** (display/headline) and **Source Serif 4** (body + all micro-type) from Google Fonts via `tokens/fonts.css`. No monospace is used. If Judge has licensed brand faces, drop the files in and swap the `@import` for `@font-face` rules.
- **No logo / mark exists.** The wordmark is the name set in type. Nothing was invented; replace when a real mark is available.
- **No colors were specified** in the brief — the warm-paper + vermilion palette is an authored interpretation of the "delivering joy," dry, editorial voice. Easy to retune if the intended palette differs.
