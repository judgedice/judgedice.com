# -*- coding: utf-8 -*-
"""Create the Judge design-system block kit as editor snippets (website_id=2).

Five blocks translated from `Judge Design System/components/content/`:
PageHeader, SectionLabel, Callout, Card(s), Rule. Each is:
  - a snippet template view (website.s_jd_*), semantic markup, styled by
    .s_jd_* CSS appended to website[2].custom_code_head (tokens already there)
  - registered in a new "Judge" group in the snippet palette via a site-2
    inherited view of website.snippets

Idempotent: skips views whose key already exists on site 2; CSS append is
sentinel-guarded. Dry-run by default; pass --apply to write.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2

SNIPPETS = {
    "website.s_jd_page_header": ("Judge Page Header", '''<t name="Judge Page Header" t-name="website.s_jd_page_header">
    <section class="s_jd_page_header">
        <div class="container">
            <div class="s_jd_kicker"><span class="s_jd_index">01</span><span>Section Kicker</span><span class="s_jd_rule_fill"/></div>
            <h1>Page Title Here</h1>
            <p class="s_jd_lead">An italic serif lead that sets the scene for the page in a sentence or two.</p>
        </div>
    </section>
</t>'''),
    "website.s_jd_section_label": ("Judge Section Label", '''<t name="Judge Section Label" t-name="website.s_jd_section_label">
    <section class="s_jd_section_label_wrap pt24 pb0">
        <div class="container">
            <div class="s_jd_section_label"><span class="s_jd_index">01</span><span>Section Label</span><span class="s_jd_rule_fill"/></div>
        </div>
    </section>
</t>'''),
    "website.s_jd_callout": ("Judge Callout", '''<t name="Judge Callout" t-name="website.s_jd_callout">
    <section class="s_jd_callout pt24 pb24">
        <div class="container">
            <div class="s_jd_callout_inner">
                <p class="s_jd_quote">Add the aside or pull quote here &#8212; the line worth pulling out of the story.</p>
                <p class="s_jd_cite">&#8212; Attribution</p>
            </div>
        </div>
    </section>
</t>'''),
    "website.s_jd_cards": ("Judge Cards", '''<t name="Judge Cards" t-name="website.s_jd_cards">
    <section class="s_jd_cards pt32 pb32">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 pb16"><div class="s_jd_card_item"><h3>Card Title</h3><p>Restrained content container on a raised paper surface. Swap in your own copy.</p></div></div>
                <div class="col-lg-4 pb16"><div class="s_jd_card_item"><h3>Card Title</h3><p>Hairline border, near-sharp corners, no shadows &#8212; print doesn&#8217;t cast them.</p></div></div>
                <div class="col-lg-4 pb16"><div class="s_jd_card_item"><h3>Card Title</h3><p>Duplicate or delete cards from the column options after dropping the block.</p></div></div>
            </div>
        </div>
    </section>
</t>'''),
    "website.s_jd_rule": ("Judge Rule", '''<t name="Judge Rule" t-name="website.s_jd_rule">
    <section class="s_jd_rule pt16 pb16">
        <div class="container">
            <div class="s_jd_rule_row"><span class="s_jd_rule_label">Label</span><span class="s_jd_rule_fill"/></div>
        </div>
    </section>
</t>'''),
}

REGISTRY_KEY = "website.snippets_judge"
REGISTRY_ARCH = '''<data inherit_id="website.snippets" name="Judge Blocks" active="True">
    <xpath expr="//snippets[@id='snippet_groups']" position="inside">
        <t snippet-group="judge" t-snippet="website.s_snippet_group" string="Judge" t-thumbnail="/website/static/src/img/snippets_thumbs/s_text_image.svg"/>
    </xpath>
    <xpath expr="//snippets[@id='snippet_structure']" position="inside">
        <t t-snippet="website.s_jd_page_header" string="Page Header" group="judge"/>
        <t t-snippet="website.s_jd_section_label" string="Section Label" group="judge"/>
        <t t-snippet="website.s_jd_callout" string="Callout" group="judge"/>
        <t t-snippet="website.s_jd_cards" string="Cards" group="judge"/>
        <t t-snippet="website.s_jd_rule" string="Rule" group="judge"/>
    </xpath>
</data>'''

CSS = '''
/* ---- Judge blocks (s_jd_*) ---- */
.s_jd_page_header{padding:clamp(3.5rem,9vw,6.5rem) 0 clamp(1.75rem,4vw,2.75rem);}
.s_jd_page_header h1{font-family:var(--font-display);font-weight:var(--weight-regular);text-transform:uppercase;font-size:clamp(2.75rem,8vw,6rem);line-height:var(--leading-tight);letter-spacing:-0.005em;color:var(--ink);margin:0;max-width:18ch;}
.s_jd_page_header .s_jd_lead{font-family:var(--font-serif);font-style:italic;font-size:clamp(1.125rem,2.4vw,1.5rem);line-height:1.4;color:var(--ink-soft);margin:22px 0 0;max-width:40rem;}
.s_jd_kicker,.s_jd_section_label{display:flex;align-items:center;gap:14px;font-family:var(--font-sans);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);}
.s_jd_kicker{color:var(--vermilion);margin-bottom:20px;}
.s_jd_section_label{color:var(--text-accent);}
.s_jd_index{color:var(--ink-faint);font-weight:var(--weight-regular);}
.s_jd_rule_fill{flex:1 1 auto;height:1px;background:var(--line);min-width:24px;}
.s_jd_callout_inner{border-left:2px solid var(--vermilion);padding-left:var(--space-5);}
.s_jd_callout_inner .s_jd_quote{font-family:var(--font-serif);font-style:italic;font-size:var(--text-lead);line-height:1.45;color:var(--ink);margin:0;}
.s_jd_callout_inner .s_jd_cite{font-family:var(--font-sans);font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);margin:var(--space-3) 0 0;}
.s_jd_card_item{background:var(--surface-card);border:1px solid var(--line);border-radius:var(--radius-card);padding:var(--space-6);height:100%;}
.s_jd_card_item h3{font-size:var(--text-h4);margin:0 0 var(--space-3);}
.s_jd_card_item p{margin:0;font-size:var(--text-small);color:var(--ink-soft);}
.s_jd_rule_row{display:flex;align-items:center;gap:16px;}
.s_jd_rule_label{font-family:var(--font-sans);font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);white-space:nowrap;}
'''


def main(apply_):
    uid, call = connect()
    mode = "APPLY" if apply_ else "dry-run"
    print("build_blocks [%s]" % mode)

    # validate all arches up front
    for key, (name, arch) in list(SNIPPETS.items()) + [(REGISTRY_KEY, ("Judge Blocks", REGISTRY_ARCH))]:
        ET.fromstring(arch)
    print("[ok] all 6 arches are well-formed XML")

    # snippet templates
    for key, (name, arch) in SNIPPETS.items():
        existing = call("ir.ui.view", "search", [["key", "=", key], ["website_id", "=", SITE]])
        if existing:
            print("  exists %s (view %s) — skipping create" % (key, existing[0])); continue
        if not apply_:
            print("  would-create %s (%d chars)" % (key, len(arch))); continue
        vid = call("ir.ui.view", "create", {
            "name": name, "key": key, "type": "qweb", "arch": arch, "website_id": SITE})
        print("  created view %d %s" % (vid, key))

    # palette registration (inherits website.snippets)
    parent = call("ir.ui.view", "search", [["key", "=", "website.snippets"], ["website_id", "=", False]])[0]
    existing = call("ir.ui.view", "search", [["key", "=", REGISTRY_KEY], ["website_id", "=", SITE]])
    if existing:
        print("  exists %s (view %s) — skipping create" % (REGISTRY_KEY, existing[0]))
    elif apply_:
        rid = call("ir.ui.view", "create", {
            "name": "Judge Blocks", "key": REGISTRY_KEY, "type": "qweb", "mode": "extension",
            "inherit_id": parent, "arch": REGISTRY_ARCH, "website_id": SITE})
        print("  created registry view %d %s (inherits %d)" % (rid, REGISTRY_KEY, parent))
    else:
        print("  would-create %s inheriting view %d" % (REGISTRY_KEY, parent))

    # block CSS -> custom_code_head (sentinel-guarded append)
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if ".s_jd_page_header{" in head:
        print("  css already present in custom_code_head — skipping")
    elif apply_:
        assert "</style>" in head
        call("website", "write", [SITE], {"custom_code_head": head.replace("</style>", CSS + "</style>", 1)})
        print("  appended %d chars of block css to custom_code_head" % len(CSS))
    else:
        print("  would-append %d chars of block css to custom_code_head" % len(CSS))
    print("done [%s]" % mode)


if __name__ == "__main__":
    main("--apply" in sys.argv)
