# -*- coding: utf-8 -*-
"""Judge Quote Page: a whole page reduced to a background image and one quote.

A reusable editor snippet in the Judge palette group. Judge makes a blank page,
drops this on it, and the site header and footer supply the rest.

Light/dark is Odoo's own colour-combination picker. The section carries `o_cc`,
so selecting it in the builder and opening Background -> Colors switches between
presets 1-3 (the light end of the palette) and 4-5 (the dark end); the CSS keys
the veil and the type colour off whichever class is on the section. Odoo 19
removed the XML snippet_options system, so a bespoke two-state toggle in the
options panel would need shipped JS, which Odoo Online cannot deploy.

The veil is its own absolutely-positioned child rather than a background-color
on the section: a background-image covers an element's own background-color, so
tinting the photo any other way would mean taking over the builder's native
background-image option instead of leaving it working.

Creates:
  - snippet template view  website.s_jd_quote_page
  - palette entry in the existing "Judge" group (view 2271)
  - .s_jd_quotepage CSS appended to website[2].custom_code_head

No page instance: this is a block Judge places, not a section of an existing page.

Idempotent; dry-run by default, pass --apply.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE, PALETTE_VIEW = 2, 2271
SNIPPET_KEY = "website.s_jd_quote_page"
CSS_SENTINEL = ".s_jd_quotepage{"  # must literally appear in CSS below

# A prompt, not an invented quote put in someone's mouth. Judge replaces it.
QUOTE = ("Write the line here that the page exists to carry &#8212; one sentence, "
         "set large enough that a reader has to slow down for it.")
CITE_NAME = "Their name"
CITE_CONTEXT = "the occasion"

SNIPPET_ARCH = (
    '<t name="Judge Quote Page" t-name="website.s_jd_quote_page">\n'
    '    <section class="s_jd_quotepage o_cc o_cc1" data-snippet="s_jd_quote_page" '
    'data-name="Quote Page">'
    # the veil sits between the builder-chosen background image and the type
    '<div class="s_jd_quotepage_scrim o_not_editable" contenteditable="false" aria-hidden="true"/>'
    '<div class="s_jd_quotepage_inner">'
    '<blockquote class="s_jd_quotepage_block">'
    '<p class="s_jd_quotepage_text">%s</p>'
    '<footer class="s_jd_quotepage_cite"><strong>%s</strong> &#8212; %s</footer>'
    '</blockquote></div></section>\n'
    '</t>' % (QUOTE, CITE_NAME, CITE_CONTEXT)
)

CSS = '''
/* ---- Judge Quote Page (s_jd_quote_page) ---- */
/* Odoo paints the builder-chosen background image onto the <section> itself, and
   a background-image covers that element's own background-color — so the veil
   has to be a separate child, and the colour-combination class on the section is
   what decides whether that veil is paper or ink. */
.s_jd_quotepage{position:relative;isolation:isolate;display:flex;align-items:center;justify-content:center;min-height:60vh;padding:clamp(6rem,18vh,12rem) var(--page-gutter);background-size:cover;background-position:center;}
.s_jd_quotepage_scrim{position:absolute;inset:0;z-index:0;pointer-events:none;}
.s_jd_quotepage_inner{position:relative;z-index:1;width:100%;max-width:var(--content-max);margin:0 auto;text-align:center;}
.s_jd_quotepage_block{margin:0;border:none;padding:0;background:none;}

/* Light presets veil the photo with paper and set ink type; dark presets invert
   it. Picking a preset in the builder's Background panel IS the light/dark
   switch — presets 1 and 5 are the two ends, 2-4 are intermediate. */
.s_jd_quotepage.o_cc1 .s_jd_quotepage_scrim,
.s_jd_quotepage.o_cc2 .s_jd_quotepage_scrim,
.s_jd_quotepage.o_cc3 .s_jd_quotepage_scrim{background:rgba(242,236,223,.72);}
.s_jd_quotepage.o_cc4 .s_jd_quotepage_scrim,
.s_jd_quotepage.o_cc5 .s_jd_quotepage_scrim{background:rgba(16,12,8,.62);}

/* every <p> in the blockquote, not just .s_jd_quotepage_text: the editor
   re-nests text into sibling <p>s when a link is applied, and the quote would
   silently drop to body type if only the first were styled (see .s_jd_quotes) */
.s_jd_quotepage .s_jd_quotepage_block p,
.s_jd_quotepage .s_jd_quotepage_block p a{font-family:var(--font-serif);font-style:italic;font-size:clamp(1.75rem,5vw,3.5rem);line-height:1.18;letter-spacing:-0.01em;margin:0 auto;max-width:26ch;text-wrap:balance;}
.s_jd_quotepage .s_jd_quotepage_block p a{text-decoration:none;border-bottom:1px solid currentColor;}
.s_jd_quotepage .s_jd_quotepage_block p:empty{display:none;}
.s_jd_quotepage .s_jd_quotepage_cite{font-family:var(--font-serif);font-style:normal;font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);margin:clamp(1.25rem,3vw,2rem) 0 0;}
.s_jd_quotepage .s_jd_quotepage_cite strong{font-weight:var(--weight-medium);}

.s_jd_quotepage.o_cc1 .s_jd_quotepage_block p,
.s_jd_quotepage.o_cc2 .s_jd_quotepage_block p,
.s_jd_quotepage.o_cc3 .s_jd_quotepage_block p{color:var(--ink);}
.s_jd_quotepage.o_cc1 .s_jd_quotepage_cite,
.s_jd_quotepage.o_cc2 .s_jd_quotepage_cite,
.s_jd_quotepage.o_cc3 .s_jd_quotepage_cite{color:var(--ink-faint);}
.s_jd_quotepage.o_cc1 .s_jd_quotepage_cite strong,
.s_jd_quotepage.o_cc2 .s_jd_quotepage_cite strong,
.s_jd_quotepage.o_cc3 .s_jd_quotepage_cite strong{color:var(--ink-soft);}
.s_jd_quotepage.o_cc4 .s_jd_quotepage_block p,
.s_jd_quotepage.o_cc5 .s_jd_quotepage_block p{color:var(--paper);}
.s_jd_quotepage.o_cc4 .s_jd_quotepage_cite,
.s_jd_quotepage.o_cc5 .s_jd_quotepage_cite{color:rgba(242,236,223,.62);}
.s_jd_quotepage.o_cc4 .s_jd_quotepage_cite strong,
.s_jd_quotepage.o_cc5 .s_jd_quotepage_cite strong{color:var(--paper);}

@media (max-width:767.98px){
.s_jd_quotepage{min-height:50vh;padding:clamp(4rem,12vh,7rem) var(--page-gutter);}
.s_jd_quotepage .s_jd_quotepage_block p{max-width:none;}
}
'''


def main(apply_):
    uid, call = connect()
    print("add_quote_page_block [%s]" % ("APPLY" if apply_ else "dry-run"))
    ET.fromstring(SNIPPET_ARCH)
    print("  [ok] snippet markup is well-formed XML")

    # 1. snippet template
    existing = call("ir.ui.view", "search",
                    [["key", "=", SNIPPET_KEY], ["website_id", "=", SITE]])
    if existing:
        print("  snippet view exists: %d" % existing[0])
    elif apply_:
        vid = call("ir.ui.view", "create", {
            "name": "Judge Quote Page", "key": SNIPPET_KEY, "type": "qweb",
            "arch": SNIPPET_ARCH, "website_id": SITE})
        print("  created snippet view %d" % vid)
    else:
        print("  would-create snippet view %s" % SNIPPET_KEY)

    # 2. palette registration (extend the existing Judge group)
    pal = call("ir.ui.view", "read", [PALETTE_VIEW], ["arch_db", "website_id"])[0]
    assert pal["website_id"][0] == SITE, "palette view is not website 2!"
    entry = '<t t-snippet="website.s_jd_quote_page" string="Quote Page" group="judge"/>'
    if "s_jd_quote_page" in pal["arch_db"]:
        print("  palette already lists Quote Page")
    else:
        anchor = '<t t-snippet="website.s_jd_rule"'
        assert anchor in pal["arch_db"], "could not find the Rule entry to insert before"
        new_pal = pal["arch_db"].replace(anchor, entry + '\n        ' + anchor, 1)
        assert entry in new_pal, "could not place palette entry"
        ET.fromstring(new_pal)
        if apply_:
            call("ir.ui.view", "write", [PALETTE_VIEW], {"arch": new_pal})
            back = call("ir.ui.view", "read", [PALETTE_VIEW], ["arch_db"])[0]["arch_db"]
            assert "s_jd_quote_page" in back, "palette readback failed"
            print("  registered Quote Page in the Judge palette group, verified")
        else:
            print("  would-register Quote Page in the Judge palette group")

    # 3. CSS
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if CSS_SENTINEL in head:
        print("  quote-page css already present")
    elif apply_:
        assert "</style>" in head, "no </style> to append before"
        call("website", "write", [SITE],
             {"custom_code_head": head.replace("</style>", CSS + "</style>", 1)})
        back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
        assert CSS_SENTINEL in back, "css readback failed"
        print("  appended %d chars of quote-page css, verified" % len(CSS))
    else:
        print("  would-append %d chars of quote-page css" % len(CSS))
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
