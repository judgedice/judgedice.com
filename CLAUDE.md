# CLAUDE.md — judgedice.com

Personal-brand site + tribute-writing business for Judge DiCesaro, running as **website id 2** on the Half a Glass Odoo Online instance (`half-a-glass1.odoo.com`, db `half-a-glass1`, Odoo 19 Enterprise). Site 1 on the same instance is Half a Glass (the operating LLC and Stripe entity) — **scope every Odoo write to `website_id=2` and never touch site 1's records**.

## Hard rules

1. **Never modify `Judge Design System/`** — it's the source-of-truth design (paper `#F2ECDF`, ink `#1C1712`, vermilion `#CB4127`; Anton + Source Serif 4). It informs the Odoo build; it is not part of it.
2. Odoo creds come from `.env` (`ODOO_URL/DB/USER/KEY`) via `scripts/odoo.py`. Never hardcode, print, or commit them. `.env` is gitignored.
3. Production Odoo writes need the user's explicit go-ahead. Dry-run first where a script supports it.
4. View arches must be well-formed XML (validate with ElementTree before writing; numeric entities, `&amp;`). Write field `arch`, read `arch_db` — Odoo normalizes on save, so verify by parsed-content comparison, not string equality.
5. Verify CSS/SCSS changes via the newest `web.assets_frontend` attachment in the DB — Odoo serves stale cached bundles over HTTP, so curl flip-flops.
6. After any Odoo write: run `python3 scripts/snapshot.py`, review `git diff snapshot/`, commit, push.
7. The header view (2035) contains a hidden `jd-header-plugs` span with six `website.placeholder_header_*` t-calls — **never remove it**; module installs fail validation without those anchors.

## Workflow

`snapshot/` mirrors the live site-2 state and is the GitOps source of truth: edit → commit → push deploys via `.github/workflows/deploy.yml` + `scripts/deploy.py` (drift-guarded; recover from DRIFT by running snapshot.py and committing). Direct XML-RPC writes via scripts are the fallback while Actions secrets are unset.

Scripts (all load `.env`, talk XML-RPC): `odoo.py` connector · `snapshot.py` (read-only mirror) · `deploy.py` (push snapshot→live) · `build_blocks.py` (Judge snippet kit) · `morning_check.py` (read-only daily brief → `reports/morning.html`, published as the "Morning Docket" artifact).

## Key live IDs (site 2)

- Pages/views: home 2034 · header **2035** (menu-driven) · footer 2038 · work 2039 · home-life 2040 · **offerings 2041** (page 8, `/offerings`) · connect 2042 (orphaned from nav)
- Judge block kit: views 2266–2270 (snippets) + 2271 (palette registration)
- Appointment-page email hiders: 2272/2273 · checkout booking CTA: 2720 · statement-descriptor note: 2731
- SCSS attachments: palette **1086**, values/fonts **1087** (edit base64 `datas`; insert before `// -- hook --`)
- Blog 1 = "Entries" (site 2); tags 1 Tributes / 2 Opinions / 3 Reviews
- Funnel: product.template **7** "Tribute Consultation" $50 → cart (+ founding-customer promo code — loyalty.program 2, capped uses; code name lives on the private board only) → Stripe provider **16** (LIVE via Connect onboarding, proxy mode — cannot switch to test) → confirmation CTA → appointment.type **1** (2:00/2:30 PM ET daily; slots are one-start-per-record)
- Menu root 7. Statement descriptor is HALF A GLASS by design (disclosed at payment + product page).

## Business context

Offer: tribute writing (eulogies/memorials, celebration speeches, professional tributes, written keepsakes). Model: $50 consult credited toward a flat quote. Entries (blog) = anonymized samples + opinion/review pieces, every entry ends in a CTA to /offerings. Roadmap: `ROADMAP.md` (public summary) + private GitHub Project #2 ("judgedice.com Roadmap", Phase field P0–P5). Morning Docket artifact: https://claude.ai/code/artifact/ec9f53b2-351f-4c7e-9641-8f3b4ddbc543
