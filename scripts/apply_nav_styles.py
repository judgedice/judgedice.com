# -*- coding: utf-8 -*-
"""Site-2 only: (1) rewrite header view 2035 to be menu-driven + CSS-class styled,
(2) append nav CSS + brand cascade into website[2].custom_code_head.
Validates header XML before writing; guards against double-apply on the head."""
import sys, xml.etree.ElementTree as ET
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

HEADER_VIEW = 2035

HEADER_ARCH = '''<data inherit_id="website.layout" name="Template Header Default" active="True">
    <xpath expr="//header//nav" position="replace">
        <nav class="jd-nav d-none d-lg-flex">
            <a href="/" class="jd-brand">Judge<span class="jd-dot">.</span></a>
            <span class="jd-links">
                <t t-foreach="website.menu_id.child_id" t-as="submenu">
                    <a t-att-href="submenu.url" class="jd-link">
                        <span class="jd-row"><span class="jd-num"/><span class="jd-label" t-esc="submenu.name"/></span>
                        <span class="jd-underline"/>
                    </a>
                </t>
            </span>
        </nav>
        <t t-call="website.template_header_mobile"/>
    </xpath>
</data>'''

CSS_ADD = '''
/* ---- editable menu-driven nav (jd) ---- */
.jd-nav{align-items:center;justify-content:space-between;width:100%;padding:20px clamp(1.5rem,6vw,6rem);background:color-mix(in srgb,var(--paper) 88%,transparent);border-bottom:1px solid var(--line);}
.jd-brand{font-family:var(--font-serif);font-size:26px;color:var(--ink);text-decoration:none;letter-spacing:-0.01em;}
.jd-brand .jd-dot{color:var(--vermilion);}
.jd-links{display:inline-flex;gap:clamp(18px,3vw,40px);flex-wrap:wrap;align-items:center;counter-reset:jdnav;}
.jd-nav .jd-link{display:inline-flex;flex-direction:column;gap:5px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:var(--ink);text-decoration:none;counter-increment:jdnav;}
.jd-nav .jd-link .jd-row{display:inline-flex;align-items:baseline;gap:7px;}
.jd-nav .jd-link .jd-num::before{content:counter(jdnav,decimal-leading-zero);color:var(--vermilion);font-size:var(--text-meta);font-weight:var(--weight-regular);}
/* ---- brand cascade so builder-added blocks match ---- */
#wrap h1,#wrap h2,#wrap h3,#wrap h4,#wrap h5,#wrap h6,#wrap .display-1,#wrap .display-2,#wrap .display-3,#wrap .display-4,#wrap .h1,#wrap .h2,#wrap .h3,#wrap .h4,#wrap .h5,#wrap .h6{font-family:var(--font-display);font-weight:400;text-transform:uppercase;letter-spacing:var(--tracking-display);line-height:var(--leading-tight);}
#wrap,#wrap p,#wrap li,#wrap .lead,#wrap blockquote,#wrap .o_default_snippet_text{font-family:var(--font-serif);}
#wrap .btn{font-family:var(--font-serif);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);border-radius:var(--radius-none);}
'''

def main():
    uid, call = connect()

    # ---- guardrails ----
    v = call("ir.ui.view","read",[HEADER_VIEW],["website_id","key"])[0]
    assert v["website_id"] and v["website_id"][0] == 2, "header view not site 2!"
    ET.fromstring(HEADER_ARCH)  # well-formed check
    print("[ok] header arch is well-formed XML; view %d site-scoped=2 (%s)" % (HEADER_VIEW, v["key"]))

    w = call("website","read",[2],["custom_code_head"])[0]
    head = w["custom_code_head"] or ""
    assert "</style>" in head, "no </style> anchor in custom_code_head"
    if ".jd-links{" in head:
        print("[abort] nav CSS already present in custom_code_head; not re-appending."); sys.exit(1)
    new_head = head.replace("</style>", CSS_ADD + "</style>", 1)
    assert new_head.count("<style>") == new_head.count("</style>"), "style tag imbalance"

    # ---- writes (site 2 only) ----
    call("ir.ui.view","write",[HEADER_VIEW],{"arch": HEADER_ARCH})
    print("[write] view %d — header rewritten: menu-driven (t-foreach website.menu_id.child_id), CSS-class styled." % HEADER_VIEW)

    call("website","write",[2],{"custom_code_head": new_head})
    print("[write] website[2].custom_code_head — +%d chars (nav CSS counter numbering + brand cascade for #wrap blocks)." % (len(new_head)-len(head)))

    # ---- readback ----
    chk = call("website","read",[2],["custom_code_head"])[0]["custom_code_head"]
    a2 = call("ir.ui.view","read",[HEADER_VIEW],["arch_db"])[0]["arch_db"]
    print("[verify] head now %d chars, .jd-links present=%s; header t-foreach present=%s"
          % (len(chk), ".jd-links{" in chk, "t-foreach" in a2))
    print("DONE.")

if __name__ == "__main__":
    main()
