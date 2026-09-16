# -*- coding: utf-8 -*-
"""Style the mobile header/drawer to the design system (website 2 only).

The desktop nav (view 2035) is `d-none d-lg-flex` and below lg the header falls
through to `website.template_header_mobile` -- stock Odoo, never touched. That
template and every placeholder it calls (brand, text element, sign-in, CTA) is
website_id=False, i.e. SHARED WITH SITE 1, so none of it can be edited or
deactivated directly. All markup changes therefore go in a site-2 override that
inherits website.template_header_mobile, the same pattern footer view 2038 uses
on website.layout.

Four things the stock drawer got wrong, fixed in the override:
  brand     - placeholder_header_brand renders an empty <span>, so mobile had no
              wordmark at all; replaced with the "Judge." mark
  phone     - placeholder_header_text_element renders Odoo's demo number
              "+1 555-555-5556" as a live tel: link; removed
  sign-in   - portal.placeholder_user_sign_in exposes /web/login; removed for
              now (portal work is Phase 3). portal.user_dropdown is left alone,
              so an already-signed-in customer keeps their account menu.
  CTA       - header_call_to_action_large is a generic "Contact Us" button;
              replaced with the consult CTA, matching the footer.
  autohide  - Odoo's autohide grabs header#top's FIRST .top_menu and folds the
              links that overflow into a "+" dropdown. View 2035 replaced the
              desktop nav with .jd-nav, which has no .top_menu, so the only
              match on this site is the drawer's list -- and a vertical list
              always "overflows", so at >=768px every link vanished into "+".
              The opt-out class the JS checks sits on header#top, which is built
              with t-attf-class in web.frontend_layout (shared) and so cannot be
              reached from here. But the same JS bails early when every direct
              child of .top_menu is "unfoldable", and .o_no_autohide_item is on
              that list -- so we mark the items instead of the header.

The link numbering (01, 02, ...) is done with CSS counters, the same way the
desktop .jd-nav does it -- no markup change needed. The search box keeps its
stock t-call and is restyled in CSS, so we don't have to guess at the
placeholder's class parameters.

Dry-run by default; --apply writes. Idempotent, sentinel-guarded.
"""
import sys, os, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

SITE = 2
PARENT_KEY = "website.template_header_mobile"
VIEW_KEY = "website.jd_header_mobile"
VIEW_NAME = "Judge Mobile Header"
SENTINEL = "/* ---- jd-mobile-nav v1 ---- */"
END = "/* ---- end jd-mobile-nav ---- */"

ARCH = '''<data inherit_id="website.template_header_mobile" name="Judge Mobile Header" active="True">
    <xpath expr="//t[@t-call='website.placeholder_header_brand']" position="replace">
        <a class="jd-mnav-mark" href="/">Judge<span class="jd-dot">.</span></a>
    </xpath>
    <xpath expr="//t[@t-call='website.placeholder_header_text_element']" position="replace"/>
    <xpath expr="//t[@t-call='portal.placeholder_user_sign_in']" position="replace"/>
    <xpath expr="//t[@t-call='website.submenu']" position="replace">
        <t t-call="website.submenu" item_class.f="nav-item border-top o_no_autohide_item #{submenu_last and 'border-bottom'}" link_class.f="nav-link p-3 text-wrap" dropdown_toggler_classes.f="d-flex justify-content-between align-items-center" dropdown_menu_classes.f="position-relative rounded-0 o_dropdown_without_offset"/>
    </xpath>
    <xpath expr="//t[@t-call='website.header_call_to_action_large']" position="replace">
        <li class="o_no_autohide_item">
            <a class="jd-mnav-cta" href="/offerings">
                <span>Start with a consult</span>
                <span class="jd-arrow" aria-hidden="true">&#8594;</span>
            </a>
        </li>
    </xpath>
</data>
'''

CSS = SENTINEL + '''
/* Odoo's mobile header (view 1268) is shared with site 1, so the markup lives in
   the site-2 override website.jd_header_mobile; this is the paint. */

/* --- top bar: match the desktop .jd-nav hairline, drop Bootstrap's shadow --- */
header#top .o_header_mobile{background:var(--paper);border-bottom:1px solid var(--line);box-shadow:none!important;}
header#top .o_header_mobile .o_main_nav{padding-top:13px;padding-bottom:13px;}
.jd-mnav-mark{align-self:center;font-family:var(--font-serif);font-size:22px;line-height:1;color:var(--ink);text-decoration:none;letter-spacing:-0.01em;}
.jd-mnav-mark .jd-dot{color:var(--vermilion);}
.jd-mnav-mark:hover{color:var(--vermilion);}
header#top .o_header_mobile .o_wsale_my_cart .btn{color:var(--ink)!important;}

/* Bootstrap paints the burger and the close X as background SVGs, so the colour
   is baked into the image and no property can reach it - swap the whole data
   URI for one stroked in ink. */
header#top .o_header_mobile .navbar-toggler-icon{
  width:26px;height:26px;
  background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='%231C1712' stroke-width='2' stroke-linecap='round' d='M4 9h22M4 15h22M4 21h22'/%3e%3c/svg%3e");
}
.o_navbar_mobile .btn-close{
  opacity:1;width:1.1em;height:1.1em;
  background-image:url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3e%3cpath stroke='%231C1712' stroke-width='1.6' stroke-linecap='round' d='M3 3l10 10M13 3L3 13'/%3e%3c/svg%3e");
}

/* --- the drawer --- */
.o_navbar_mobile{background:var(--paper);border-left:1px solid var(--line);}
.o_navbar_mobile .offcanvas-header{padding:12px clamp(1.25rem,5vw,1.75rem);}
.o_navbar_mobile .offcanvas-body{padding-left:clamp(1.25rem,5vw,1.75rem);padding-right:clamp(1.25rem,5vw,1.75rem);}

/* search: strip the pill + grey fill for a hairline rule. The stock classes are
   Bootstrap utilities (bg-light, text-bg-light, rounded-*-pill), so these need
   !important to land. */
.o_navbar_mobile .o_searchbar_form .input-group{border-bottom:1px solid var(--line-strong);margin-bottom:4px!important;}
.o_navbar_mobile .o_searchbar_form .oe_search_box{
  border:0!important;border-radius:0!important;background:transparent!important;
  box-shadow:none!important;padding:11px 2px!important;
  font-family:var(--font-serif);font-size:var(--text-small);color:var(--ink);
}
.o_navbar_mobile .o_searchbar_form .oe_search_box::placeholder{color:var(--ink-faint);font-style:italic;opacity:1;}
.o_navbar_mobile .o_searchbar_form .oe_search_button{
  border:0!important;border-radius:0!important;background:transparent!important;
  color:var(--ink-faint);padding:11px 2px!important;
}
.o_navbar_mobile .o_searchbar_form .oe_search_button:hover{color:var(--vermilion);}

/* links: same decimal-leading-zero counter the desktop .jd-nav uses */
/* mx-n3 is a Bootstrap utility (so, !important) that cancels the offcanvas-body's
   default 1rem padding to make the rules full-bleed. We set our own gutter on
   the body, so that negative margin instead pushes the ul 32px WIDER than its
   container -- and Odoo's autohide reads the overflow and sweeps every link into
   a "+" dropdown. Cancelling it keeps the links, and aligns the rules with the
   search box and the CTA. */
.o_navbar_mobile .top_menu{counter-reset:jdmnav;margin:0!important;}
.o_navbar_mobile .top_menu .nav-item{border-top:1px solid var(--line)!important;border-bottom:0!important;}
.o_navbar_mobile .top_menu .nav-item:last-child{border-bottom:1px solid var(--line)!important;}
.o_navbar_mobile .top_menu .nav-link{
  display:flex;align-items:baseline;gap:12px;
  padding:17px 2px!important;counter-increment:jdmnav;
  font-family:var(--font-serif);font-size:var(--text-label);
  text-transform:uppercase;letter-spacing:var(--tracking-label);
  font-weight:var(--weight-medium);color:var(--ink);
}
.o_navbar_mobile .top_menu .nav-link::before{
  content:counter(jdmnav,decimal-leading-zero);
  color:var(--vermilion);font-size:var(--text-meta);font-weight:var(--weight-regular);
}
.o_navbar_mobile .top_menu .nav-link:hover,
.o_navbar_mobile .top_menu .nav-link:focus{color:var(--vermilion);background:transparent;}

/* CTA: the one filled element in the drawer, so it reads as the exit */
.jd-mnav-cta{
  display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;
  padding:15px 18px;border:1px solid var(--vermilion);border-radius:0;
  background:var(--vermilion);color:var(--paper);text-decoration:none;
  font-family:var(--font-serif);font-size:var(--text-label);
  text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);
}
.jd-mnav-cta:hover,.jd-mnav-cta:focus{background:var(--vermilion-deep);border-color:var(--vermilion-deep);color:var(--paper);}
.jd-mnav-cta .jd-arrow{display:inline-block;transition:transform var(--dur-base) var(--ease-out);}
.jd-mnav-cta:hover .jd-arrow{transform:translateX(5px);}
@media (prefers-reduced-motion:reduce){.jd-mnav-cta .jd-arrow{transition:none;}}
''' + END


def canon(x):
    """Canonical XML, so Odoo's entity normalisation isn't read as a mismatch."""
    return ET.tostring(ET.fromstring(x), encoding="unicode")


def main(argv):
    apply_ = "--apply" in argv
    uid, call = connect()
    print("add_mobile_nav [%s] site=%d" % ("APPLY" if apply_ else "dry-run", SITE))

    ET.fromstring(ARCH)  # fail loudly before touching anything

    parent = call("ir.ui.view", "search_read", [["key", "=", PARENT_KEY]],
                  fields=["id", "website_id"])
    assert parent, "parent view %s not found" % PARENT_KEY
    print("  parent %s = view %d (website_id=%s, shared -> never edited)"
          % (PARENT_KEY, parent[0]["id"], parent[0]["website_id"]))

    # --- 1. the override view ---
    existing = call("ir.ui.view", "search_read",
                    [["key", "=", VIEW_KEY], ["website_id", "=", SITE]],
                    fields=["id", "arch_db", "active"])
    if existing:
        vid = existing[0]["id"]
        if canon(existing[0]["arch_db"]) == canon(ARCH):
            print("  noop  view %d (%s) already matches" % (vid, VIEW_KEY))
        elif apply_:
            call("ir.ui.view", "write", [vid], {"arch": ARCH, "active": True})
            back = call("ir.ui.view", "read", [vid], ["arch_db"])[0]["arch_db"]
            ok = canon(back) == canon(ARCH)
            print("  %s view %d (%s)" % ("wrote" if ok else "FAIL ", vid, VIEW_KEY))
            if not ok:
                return 3
        else:
            print("  would-update  view %d (%s)" % (vid, VIEW_KEY))
    elif apply_:
        vid = call("ir.ui.view", "create", {
            "name": VIEW_NAME, "type": "qweb", "key": VIEW_KEY,
            "inherit_id": parent[0]["id"], "website_id": SITE,
            "mode": "extension", "priority": 16, "active": True, "arch": ARCH,
        })
        back = call("ir.ui.view", "read", [vid], ["arch_db", "website_id"])[0]
        assert back["website_id"][0] == SITE, "created view is not website %d!" % SITE
        ok = canon(back["arch_db"]) == canon(ARCH)
        print("  %s view %d (%s) created on website %d"
              % ("wrote" if ok else "FAIL ", vid, VIEW_KEY, SITE))
        if not ok:
            return 3
    else:
        print("  would-create  %s (inherit %d, website %d)"
              % (VIEW_KEY, parent[0]["id"], SITE))

    # --- 2. the CSS ---
    head = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"] or ""
    if SENTINEL in head:
        s = head.index(SENTINEL)
        e = head.index(END) + len(END)
        new_head = head[:s] + CSS + head[e:]
        what = "update"
        assert new_head.index(SENTINEL) < new_head.rindex("</style>"), \
            "sentinel block sits outside <style> — would render as page text"
    else:
        # custom_code_head is a <head> fragment, not a bare stylesheet: it opens
        # with <link> tags and a <style>. Appending past the final </style> puts
        # the rules in the document as *text*, which the browser then renders on
        # the page. Always insert inside the stylesheet.
        i = head.rindex("</style>")
        new_head = head[:i].rstrip() + "\n\n" + CSS + "\n" + head[i:]
        what = "insert"
    if new_head == head:
        print("  noop  custom_code_head already matches")
    elif apply_:
        call("website", "write", [SITE], {"custom_code_head": new_head})
        back = call("website", "read", [SITE], ["custom_code_head"])[0]["custom_code_head"]
        ok = (back or "").strip() == new_head.strip()
        print("  %s custom_code_head (%s, %d -> %d chars)"
              % ("wrote" if ok else "FAIL ", what, len(head), len(new_head)))
        if not ok:
            return 3
    else:
        print("  would-%s  custom_code_head (%d -> %d chars)" % (what, len(head), len(new_head)))

    if not apply_:
        print("dry-run only; re-run with --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
