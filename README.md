# judgedice.com

Personal site for Judge DiCesaro, hosted on **Odoo Online** (`half-a-glass1.odoo.com`, website record **id 2**). Site 1 on the same instance is the Half a Glass store — everything here is scoped to `website_id=2` only.

## Layout

| Path | What it is |
|---|---|
| `Judge Design System/` | Source-of-truth design (editorial/print: paper `#F2ECDF`, ink `#1C1712`, vermilion `#CB4127`; Anton + Source Serif 4). **Do not modify** — it informs the Odoo build. |
| `scripts/` | Python XML-RPC tooling that built and maintains the live site |
| `snapshot/` | Version-controlled mirror of the live Odoo state (views, SCSS, head code, page/menu records) |
| `.env` | Odoo API credentials (`ODOO_URL/DB/USER/KEY`) — **gitignored, never commit** |

## Scripts

All scripts load creds from `.env` and talk to Odoo over XML-RPC (`/xmlrpc/2/common` + `/object`). Odoo Online has no module deployment — everything is done by writing `ir.ui.view` arches, `ir.attachment` SCSS, and `website.custom_code_head`.

- `odoo.py` — shared connector (`connect()` → `uid, call`)
- `snapshot.py` — **read-only**; pulls live site-2 state into `snapshot/`. Run it, `git diff`, commit. This is the change-tracking + restore source.
- `build.py` — original page/header/footer builder (views 2034–2042)
- `theme_apply.py` — main palette (o-color-1..5) → att 1086 `user_theme_color_palette.scss`
- `cc_and_publish.py` — color presets (o-cc1..5) → att 1087 `user_values.scss`; publishes pages
- `wire_fonts.py` — theme fonts (Anton / Source Serif 4) + `google-fonts` → att 1087
- `apply_nav_styles.py` — menu-driven header (view 2035) + brand CSS cascade in `custom_code_head`

## Rules for writing to Odoo

1. Scope every write to `website_id=2`. Site 1 has its own COW views/attachments — never touch.
2. Views: write field `arch`; arch must be well-formed XML (numeric entities, `&amp;`); validate with `ElementTree` before writing.
3. SCSS attachments: edit base64 `datas`; insert before the `// -- hook --` marker; print a backup first.
4. Compiled CSS regenerates lazily and Odoo serves stale cached bundles over HTTP — verify via the newest `web.assets_frontend` attachment in the DB, not curl.
5. Production writes need explicit approval; take a `snapshot.py` run + commit before and after.

## Key live IDs

Views: home 2034 · header 2035 · footer 2038 · work 2039 · home-life 2040 · exciting 2041 · connect 2042. Pages 5–9 (`/`, `/work`, `/home`, `/exciting`, `/connect`). Menu root 7. SCSS atts: palette 1086, values 1087.

## Roadmap

Tracked in the **judgedice.com Roadmap** GitHub Project on the `judgedice` account.
