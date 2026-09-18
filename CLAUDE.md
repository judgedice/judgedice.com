# CLAUDE.md — judgedice.com

Personal-brand site + tribute-writing business for Judge DiCesaro, running as **website id 2** on the Half a Glass Odoo Online instance (`half-a-glass1.odoo.com`, db `half-a-glass1`, Odoo 19 Enterprise). Site 1 on the same instance is Half a Glass (the operating LLC and Stripe entity) — **scope every Odoo write to `website_id=2` and never touch site 1's records**.

## Hard rules

1. **Never modify `Judge Design System/`** — it's the source-of-truth design (paper `#F2ECDF`, ink `#1C1712`, vermilion `#CB4127`; Anton + Source Serif 4). It informs the Odoo build; it is not part of it. Its `SKILL.md` also registers it as the `nav-judge-design` skill, so editing the folder changes what that skill teaches.
2. Odoo creds come from `.env` (`ODOO_URL/DB/USER/KEY`) via `scripts/odoo.py`. Never hardcode, print, or commit them. `.env` is gitignored.
3. Production Odoo writes need the user's explicit go-ahead. Dry-run first where a script supports it.
4. View arches must be well-formed XML (validate with ElementTree before writing; numeric entities, `&amp;`). Write field `arch`, read `arch_db` — Odoo normalizes on save, so verify by parsed-content comparison, not string equality.
5. Verify CSS changes — SCSS attachments **and** `custom_code_head` — against the newest `web.assets_frontend` attachment in the DB, never over HTTP: Odoo serves stale cached bundles, so curl flip-flops.
6. After any Odoo write: run `python3 scripts/snapshot.py`, review `git diff snapshot/`, commit, push.
7. **Never alter Judge's writing.** Anything he authored — entries, tributes, page copy, quotes — publishes **verbatim**. Do not trim, truncate, reorder, rewrite, condense, "clean up", or drop lines, and do not treat something as an artifact, a duplicate, stale logistics, or a privacy issue and remove it on your own judgment. If a change genuinely seems needed, **show him the exact lines and ask** — the decision is always his. Editorial additions (standfirsts, CTAs, captions) are allowed only as clearly separate elements, never merged into or substituted for his text. This applies to his content already live, too: never overwrite it.
8. The header view (2035) contains a hidden `jd-header-plugs` span with **five** `website.placeholder_header_*` t-calls — `search_box`, `text_element`, `social_links`, `language_selector`, `call_to_action` — **never remove it**; module installs fail validation without those anchors. (Verify with `grep -o 'website\.placeholder_header_[a-z_]*' snapshot/views/2035-*.xml | sort`.)

## Workflow

`snapshot/` mirrors the live site-2 state and is the GitOps source of truth: edit → commit → push deploys via `.github/workflows/deploy.yml` + `scripts/deploy.py` (drift-guarded; recover from DRIFT by running snapshot.py and committing). **Actions secrets are configured and the pipeline is live**: any push to `main` touching `snapshot/**` deploys those files with `--apply`. Direct XML-RPC writes via `deploy.py`/builders are for applying a change immediately; the push that follows then no-ops (`live already matches`). Live is authoritative for content — a builder edit you haven't snapshotted makes the push fail DRIFT rather than overwrite it.

Scripts (all load `.env`, talk XML-RPC): `odoo.py` connector · `snapshot.py` (read-only mirror) · `deploy.py` (push snapshot→live) · `build_blocks.py` (Judge snippet kit) · `morning_check.py` (read-only daily brief → `reports/morning.html`, published as the "Morning Docket" artifact).

## Commands

No test suite. Verification is: dry-run → `--apply` → readback assert (built into the scripts)
→ `python3 scripts/snapshot.py` → `git diff snapshot/`.

```bash
python3 scripts/snapshot.py                              # pull live site-2 → snapshot/ (read-only)
python3 scripts/deploy.py --base HEAD snapshot/<file>    # dry-run; add --apply to write
python3 scripts/morning_check.py                         # read-only brief → reports/morning.html
python3 scripts/<builder>.py                             # every writer is dry-run by default
python3 scripts/<builder>.py --apply                     # ...and needs Judge's go-ahead first
python3 scripts/process_images.py                        # incoming/ → processed_images/, all 4 effects
.venv/bin/python scripts/halftone.py in.HEIC out.png --w 1600 --h 900   # single effect
```

`deploy.py` exit codes: 0 ok · 1 usage/validation · 2 DRIFT · 3 verify failed.
`process_images.py` self-bootstraps `.venv` (Pillow, numpy, pillow-heif); the individual effect
scripts don't — run those through `.venv/bin/python`.

## Architecture

Odoo Online has no module deployment, so the whole site is **four writable surfaces**, reached
over XML-RPC by `scripts/odoo.py` → `connect()` → `(uid, call)`:

| Surface | What lives there | Snapshot file |
|---|---|---|
| `ir.ui.view.arch` | page / header / footer / snippet QWeb | `snapshot/views/<id>-<key>.xml` |
| `website[2].custom_code_head` | **the real stylesheet** — `:root` design tokens + every `.jd-*` and `.s_jd_*` rule | `snapshot/custom_code_head.html` |
| `ir.attachment.datas` (1086/1087) | only the Odoo theme palette + font names | `snapshot/scss/<id>-*.scss` |
| `website.page` / `website.menu` | page + nav records | `snapshot/records.json` (informational, never deployed) |

The record id is encoded in every snapshot filename — that's how `deploy.py` maps file → target.
`records.json` and `views/_index.json` are read-only artifacts and are skipped by the deploy.

A view that is **deactivated** is snapshotted as `<id>-<key>.inactive.xml`. Odoo's
`search` hides inactive records unless `active_test` is off, so without that marker a
switched-off view is indistinguishable from a deleted one. `deploy.py` reads the marker
back and treats `active` as deployable state alongside the arch — toggling a view travels
through git as a rename, and a flag changed in the builder trips the drift guard.

**Token sync:** the design tokens exist in three places and must agree —
`Judge Design System/tokens/*.css` (source of truth, never edited) → the `:root` block in
`custom_code_head` (live) → `snapshot/custom_code_head.html` (tracked).

**Adding a snippet block** (the pattern in `build_blocks.py`, `add_quotes_block.py`,
`add_swath_block.py`) — all four parts, idempotent, sentinel-guarded, dry-run by default:

1. snippet template view, key `website.s_jd_<name>`, semantic markup only
2. register it in the "Judge" palette group — inherited view **2271**
3. append `.s_jd_<name>` CSS to `website[2].custom_code_head` behind a literal sentinel string
4. optionally place one instance on a page view, behind its own sentinel

Build on Odoo's own component skeletons (e.g. the Bootstrap `carousel` classes in
`add_quotes_block.py`) so the website builder's native controls keep working — no custom JS.

`scripts/` splits in two. **Maintenance** (`odoo.py`, `snapshot.py`, `deploy.py`,
`morning_check.py`) is run repeatedly. **One-shot builders** (`build.py`, `theme_apply.py`,
`cc_and_publish.py`, `wire_fonts.py`, `apply_nav_styles.py`, `build_blocks.py`, `add_*.py`,
`publish_entries.py`) each ran once to create live state; they're kept as the record of how it
was made, and are safe to re-run because they're idempotent. The print effects
(`_effects_common.py` + `halftone` / `duotone` / `riso` / `stencil` / `process_images`) touch no
Odoo: they turn photos into ink-on-transparency PNGs for the paper ground. `incoming/` and
`processed_images/` are gitignored.

## Key live IDs (site 2)

- Pages/views: home 2034 · header **2035** (menu-driven) · footer 2038 · work 2039 · home-life 2040 · **offerings 2041** (page 8, `/offerings`; the view key is still `website.judge_exciting` — the page was renamed, the key wasn't, so grep the id not the word) · connect 2042 (orphaned from nav) · **mobile header 2747** (`website.jd_header_mobile`, site-2 override of the *shared* `website.template_header_mobile` 1268 — edit 2747, never 1268)
- Judge block kit: views 2266–2270 (page-header, section-label, callout, cards, rule) + 2732 quotes + 2733 swath, all registered in **2271** (palette). Separately, **2736** (`website_blog.jd_cover_title_overlay`) lays the entry title over the cover; the cover images themselves come from each record's `cover_properties`, not from a template override.
- Appointment-page email hiders: 2272/2273 · checkout booking CTA: 2720 · statement-descriptor note: 2731
- SCSS attachments: palette **1086**, values/fonts **1087** (edit base64 `datas`; insert before `// -- hook --`)
- Blog 1 = "Entries" (site 2); tags 1 Tributes / 2 Opinions / 3 Reviews
- Funnel: product.template **7** "Tribute Consultation" $50 → cart (+ founding-customer promo code — loyalty.program 2, capped uses; code name lives on the private board only) → Stripe provider **16** (LIVE via Connect onboarding, proxy mode — cannot switch to test) → confirmation CTA → appointment.type **1** (2:00/2:30 PM ET daily; slots are one-start-per-record)
- Menu root 7. Statement descriptor is HALF A GLASS by design (disclosed at payment + product page).

## Business context

Offer: tribute writing (eulogies/memorials, celebration speeches, professional tributes, written keepsakes). Model: $50 consult credited toward a flat quote. Entries (blog) = anonymized samples + opinion/review pieces, every entry ends in a CTA to /offerings. Roadmap: `ROADMAP.md` (public summary) + private GitHub Project #2 ("judgedice.com Roadmap", Phase field P0–P5). Morning Docket artifact: https://claude.ai/code/artifact/ec9f53b2-351f-4c7e-9641-8f3b4ddbc543
