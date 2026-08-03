# -*- coding: utf-8 -*-
"""Add the Judge Quotes carousel as a reusable editor snippet + place it on the homepage.

Built on Odoo's own carousel skeleton (classes `carousel` / `carousel-inner` /
`carousel-item`, Bootstrap data attributes) so the website builder's native
"Add Slide" / "Remove Slide" controls work on it — no custom JS. Images are
deliberately omitted: type only.

Indicator numbers (01, 02, ...) come from a CSS counter, so slides added in the
builder renumber themselves.

Creates:
  - snippet template view  website.s_jd_quotes
  - palette entry in the existing "Judge" group (view 2271)
  - .s_jd_quotes CSS appended to website[2].custom_code_head
  - one instance on the homepage (view 2034), directly under the hero headline

Idempotent; dry-run by default, pass --apply.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE, HOME_VIEW, PALETTE_VIEW = 2, 2034, 2271
SNIPPET_KEY = "website.s_jd_quotes"
CSS_SENTINEL = ".s_jd_quotes_wrapper{"  # must be a string that literally appears in CSS below
HOME_SENTINEL = "jd-quotes-home"

# Placeholder prompts — NOT invented testimonials. Judge replaces these in the builder.
SLIDES = [
    ("Write a quote here from someone you wrote for &#8212; the line they still repeat "
     "back to you months later.", "Their name", "The occasion"),
    ("Or drop in an excerpt from a tribute you wrote, and let the writing make the case "
     "on its own.", "From a eulogy", "Place, year"),
    ("Keep each one short. Two lines lands harder than ten, and the carousel gives every "
     "quote its own moment.", "Their name", "The occasion"),
]


def slide(text, who, ctx, first=False):
    return (
        '<div class="carousel-item%s" data-name="Slide">'
        '<blockquote class="s_blockquote s_jd_quote_block" data-snippet="s_blockquote" '
        'data-name="Blockquote">'
        '<p class="s_jd_quote_text">%s</p>'
        '<footer class="s_jd_quote_cite"><strong>%s</strong> &#8212; %s</footer>'
        '</blockquote></div>' % (" active" if first else "", text, who, ctx)
    )


def carousel(dom_id, id_expr=None):
    """id_expr lets the snippet template use a qweb-generated unique id."""
    target = id_expr or ("#" + dom_id)
    id_attr = ('t-attf-id="%s"' % dom_id) if id_expr else ('id="%s"' % dom_id)
    tgt_attr = (lambda: 't-attf-data-bs-target="%s"' % target) if id_expr else \
               (lambda: 'data-bs-target="%s"' % target)
    slides = "".join(slide(t, w, c, i == 0) for i, (t, w, c) in enumerate(SLIDES))
    dots = "".join(
        '<button type="button" %s data-bs-slide-to="%d"%s aria-label="Quote %d"/>'
        % (tgt_attr(), i, ' class="active" aria-current="true"' if i == 0 else "", i + 1)
        for i in range(len(SLIDES)))
    return (
        '<div %s class="s_jd_quotes carousel carousel-fade slide" data-bs-ride="true" '
        'data-bs-interval="7000" data-bs-pause="hover">'
        '<div class="carousel-inner">%s</div>'
        '<div class="s_jd_quotes_controls o_not_editable" contenteditable="false">'
        '<div class="carousel-indicators s_jd_quotes_dots">%s</div>'
        '<div class="s_jd_quotes_arrows">'
        '<button class="carousel-control-prev" type="button" %s data-bs-slide="prev" '
        'aria-label="Previous quote"><span aria-hidden="true">&#8592;</span></button>'
        '<button class="carousel-control-next" type="button" %s data-bs-slide="next" '
        'aria-label="Next quote"><span aria-hidden="true">&#8594;</span></button>'
        '</div></div></div>'
        % (id_attr, slides, dots, tgt_attr(), tgt_attr())
    )


def wrapper(inner, extra_class=""):
    return (
        '<section class="s_jd_quotes_wrapper %s" data-snippet="s_jd_quotes" '
        'data-name="Judge Quotes">'
        '<div class="s_jd_quotes_inner">'
        '<div class="s_jd_quotes_label"><span>In their words</span>'
        '<span class="s_jd_rule_fill"/></div>'
        '%s</div></section>' % (extra_class, inner)
    )


SNIPPET_ARCH = (
    '<t name="Judge Quotes" t-name="website.s_jd_quotes">\n'
    '    <t t-set="uniq" t-value="datetime.datetime.now().microsecond"/>\n'
    '    ' + wrapper(carousel("jdQuotes{{uniq}}", "#jdQuotes{{uniq}}")) + '\n'
    '</t>'
)

HOME_INSTANCE = wrapper(carousel("jdQuotesHome"), HOME_SENTINEL)

CSS = '''
/* ---- Judge quotes carousel ---- */
.s_jd_quotes_wrapper{padding:clamp(3rem,8vw,6rem) clamp(1.5rem,6vw,6rem);border-top:1px solid var(--line);}
.s_jd_quotes_inner{max-width:72rem;margin:0 auto;}
.s_jd_quotes_label{display:flex;align-items:center;gap:14px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:var(--vermilion);margin-bottom:clamp(1.5rem,4vw,2.5rem);}
.s_jd_quotes .carousel-inner{min-height:clamp(10rem,17vw,14rem);}
.s_jd_quotes .s_jd_quote_block{margin:0;border-left:2px solid var(--vermilion);padding:0 0 0 clamp(1.25rem,3vw,2.25rem);background:none;}
.s_jd_quotes .s_jd_quote_text{font-family:var(--font-serif);font-style:italic;font-size:clamp(1.25rem,3.2vw,2.25rem);line-height:1.32;color:var(--ink);margin:0;max-width:34ch;}
.s_jd_quotes .s_jd_quote_cite{font-family:var(--font-serif);font-style:normal;font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);margin:clamp(1rem,2.5vw,1.5rem) 0 0;}
.s_jd_quotes .s_jd_quote_cite strong{color:var(--ink-soft);font-weight:var(--weight-medium);}
.s_jd_quotes_controls{display:flex;align-items:center;gap:clamp(1rem,3vw,2rem);margin-top:clamp(1.75rem,4vw,2.75rem);padding-top:18px;border-top:1px solid var(--line);}
.s_jd_quotes .carousel-indicators{position:static;margin:0;padding:0;display:flex;gap:18px;counter-reset:jdq;}
.s_jd_quotes .carousel-indicators button{width:auto;height:auto;text-indent:0;background:none;border:none;border-bottom:1px solid transparent;opacity:1;flex:0 0 auto;padding:4px 0;font-family:var(--font-serif);font-size:var(--text-meta);letter-spacing:var(--tracking-label);color:var(--ink-faint);font-variant-numeric:tabular-nums;}
.s_jd_quotes .carousel-indicators button::before{counter-increment:jdq;content:counter(jdq,decimal-leading-zero);}
.s_jd_quotes .carousel-indicators button:hover{color:var(--ink);}
.s_jd_quotes .carousel-indicators button.active{color:var(--vermilion);border-bottom-color:var(--vermilion);}
.s_jd_quotes_arrows{display:flex;gap:10px;margin-left:auto;}
.s_jd_quotes .carousel-control-prev,.s_jd_quotes .carousel-control-next{position:static;width:44px;height:44px;opacity:1;background:none;border:1px solid var(--line);color:var(--ink);font-size:1rem;transition:background .2s ease,border-color .2s ease,color .2s ease;}
.s_jd_quotes .carousel-control-prev:hover,.s_jd_quotes .carousel-control-next:hover{background:var(--surface-card);border-color:var(--vermilion);color:var(--vermilion);}
.s_jd_quotes .carousel-control-prev:focus-visible,.s_jd_quotes .carousel-control-next:focus-visible,.s_jd_quotes .carousel-indicators button:focus-visible{outline:2px solid var(--vermilion);outline-offset:3px;}
@media (prefers-reduced-motion:reduce){.s_jd_quotes .carousel-item{transition:none;}}
@media (max-width:640px){.s_jd_quotes_controls{flex-wrap:wrap;gap:14px;}.s_jd_quotes_arrows{margin-left:0;}}
'''


def main(apply_):
    uid, call = connect()
    print("add_quotes_block [%s]" % ("APPLY" if apply_ else "dry-run"))
    ET.fromstring(SNIPPET_ARCH.replace("{{uniq}}", "0"))
    ET.fromstring(HOME_INSTANCE)
    print("  [ok] snippet + instance markup are well-formed XML")

    # 1. snippet template
    existing = call("ir.ui.view", "search", [["key", "=", SNIPPET_KEY], ["website_id", "=", SITE]])
    if existing:
        print("  snippet view exists: %d" % existing[0])
    elif apply_:
        vid = call("ir.ui.view", "create", {
            "name": "Judge Quotes", "key": SNIPPET_KEY, "type": "qweb",
            "arch": SNIPPET_ARCH, "website_id": SITE})
        print("  created snippet view %d" % vid)
    else:
        print("  would-create snippet view %s" % SNIPPET_KEY)

    # 2. palette registration (extend the existing Judge group)
    pal = call("ir.ui.view", "read", [PALETTE_VIEW], ["arch_db", "website_id"])[0]
    assert pal["website_id"][0] == SITE
    entry = '<t t-snippet="website.s_jd_quotes" string="Quotes" group="judge"/>'
    if "s_jd_quotes" in pal["arch_db"]:
        print("  palette already lists Quotes")
    else:
        new_pal = pal["arch_db"].replace(
            '<t t-snippet="website.s_jd_rule"', entry + '\n        <t t-snippet="website.s_jd_rule"', 1)
        assert entry in new_pal, "could not place palette entry"
        ET.fromstring(new_pal)
        if apply_:
            call("ir.ui.view", "write", [PALETTE_VIEW], {"arch": new_pal})
            print("  registered Quotes in the Judge palette group")
        else:
            print("  would-register Quotes in the Judge palette group")

    # 3. CSS
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if CSS_SENTINEL in head:
        print("  quotes css already present")
    elif apply_:
        assert "</style>" in head
        call("website", "write", [SITE], {"custom_code_head": head.replace("</style>", CSS + "</style>", 1)})
        print("  appended %d chars of quotes css" % len(CSS))
    else:
        print("  would-append %d chars of quotes css" % len(CSS))

    # 4. homepage instance, directly under the hero headline
    home = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db", "website_id"])[0]
    assert home["website_id"][0] == SITE
    body = home["arch_db"]
    if HOME_SENTINEL in body:
        print("  homepage instance already present")
        return 0
    marker = '</section><section class="jd-credentials"'
    if marker not in body:
        marker = '</section><section class="s_text_image'
    assert marker in body, "could not find the insertion point under the hero"
    new = body.replace(marker, "</section>" + HOME_INSTANCE + marker[len("</section>"):], 1)
    ET.fromstring(new)
    print("  homepage instance ready (%d chars, inserted under the hero)" % len(HOME_INSTANCE))
    if apply_:
        call("ir.ui.view", "write", [HOME_VIEW], {"arch": new})
        back = call("ir.ui.view", "read", [HOME_VIEW], ["arch_db"])[0]["arch_db"]
        assert HOME_SENTINEL in back, "readback failed"
        print("  wrote homepage view %d, verified" % HOME_VIEW)
    else:
        print("  would-write homepage view %d" % HOME_VIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
