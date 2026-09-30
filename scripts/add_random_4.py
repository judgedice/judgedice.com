#!/usr/bin/env python3
"""Add /random-4 — the Hamming quote, over the generated gradient.

Four parts, idempotent and sentinel-guarded:

  1. upload processed_images/04_twostates.webp as a site-2 attachment
     (the master is not uploaded: the image is regenerable, byte for byte,
      with `gen_gradient_art.py --seed 1947`, which is in the repo)
  2. a `jd-quote-long` CSS modifier in custom_code_head — this quote is 45
     words against the ~20 the other quote pages carry, and the stock
     3.5rem display size turns it into a wall
  3. the page view, with WebPage + Quotation schema
  4. the website.page record, published and indexed, with meta

The random menu item picks any published /random-% page, so this one joins
the rotation with no further wiring.

Dry-run by default; --apply writes and then fetches the live page.
"""
import argparse
import base64
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

from odoo import connect

SITE = 2
SLUG = "random-4"
ART = "processed_images/04_twostates.webp"
ART_NAME = "04_twostates.webp"

CSS_SENTINEL = "/* ---- jd-quote-long v1 ---- */"
CSS = CSS_SENTINEL + """
/* a quote two or three times the usual length: keep it a big quote, but let
   it breathe instead of filling the viewport at the stock display size */
.s_jd_quotepage.jd-quote-long .s_jd_quotepage_block p{
  font-size:clamp(1.25rem,2.8vw,2.125rem);max-width:36ch;line-height:1.28;
}
@media (max-width:575.98px){
  .s_jd_quotepage.jd-quote-long .s_jd_quotepage_block p{max-width:none;}
}
"""

QUOTE = ("In science, if you know what you are doing, you should not be doing "
         "it. In engineering, if you do not know what you are doing, you "
         "should not be doing it. Of course, you seldom, if ever, see either "
         "pure state.")
WHO = "Richard Hamming"
WORK = "The Art of Doing Science and Engineering"
TITLE = "You seldom, if ever, see either pure state — Judge DiCesaro"
DESC = ('"Of course, you seldom, if ever, see either pure state." — Richard '
        "Hamming, The Art of Doing Science and Engineering. One of the lines "
        "kept on rotation at judgedice.com.")

ARCH = """<t t-name="website.{slug}">
    <t t-call="website.layout">
        <script type="application/ld+json" data-jd-schema="v1">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "<t t-out="website.get_base_url()"/>/{slug}#page",
  "url": "<t t-out="website.get_base_url()"/>/{slug}",
  "name": "{title}",
  "isPartOf": {{
    "@id": "<t t-out="website.get_base_url()"/>/#website"
  }},
  "mainEntity": {{
    "@type": "Quotation",
    "text": "{quote}",
    "creator": {{
      "@type": "Person",
      "name": "{who}"
    }},
    "isBasedOn": {{
      "@type": "Book",
      "name": "{work}"
    }}
  }}
}}
        </script>
        <div id="wrap" class="oe_structure oe_empty"><section class="s_jd_quotepage o_cc o_colored_level oe_img_bg o_bg_img_center o_bg_img_origin_border_box o_cc4 jd-quote-long" data-snippet="s_jd_quote_page" data-name="Quote Page" data-attachment-id="{aid}" data-format-mimetype="image/webp" data-resize-width="1920" data-original-id="{aid}" data-original-src="{src}" data-mimetype-before-conversion="image/webp" data-mimetype="image/webp" style="background-image: url('{src}');"><div class="s_jd_quotepage_scrim o_not_editable" aria-hidden="true"/><div class="s_jd_quotepage_inner"><blockquote class="s_jd_quotepage_block"><p class="s_jd_quotepage_text">{quote}</p><footer class="s_jd_quotepage_cite"><strong>{who}</strong> — <em>{work}</em></footer></blockquote></div></section></div>
    </t>
</t>
"""


def fetch(path):
    return urllib.request.urlopen(urllib.request.Request(
        "https://www.judgedice.com" + path,
        headers={"Cache-Control": "no-cache"}), timeout=40).read().decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    assert os.path.exists(ART), f"missing {ART} — run gen_gradient_art.py first"
    uid, call = connect()

    existing = call("website.page", "search_read",
                    [["url", "=", "/" + SLUG], ["website_id", "=", SITE]],
                    ["id", "view_id", "is_published"])
    att = call("ir.attachment", "search_read",
               [["name", "=", ART_NAME], ["website_id", "=", SITE]], ["id"])
    site = call("website", "read", [SITE], ["custom_code_head"])[0]
    head = site["custom_code_head"] or ""

    print(f"  art        {ART}  {os.path.getsize(ART)/1024:.0f} KB"
          f"  {'already uploaded' if att else 'upload'}")
    print(f"  css        jd-quote-long  "
          f"{'already present' if CSS_SENTINEL in head else 'append'}")
    print(f"  page       /{SLUG}  {'exists' if existing else 'create'}")
    if not a.apply:
        print("\ndry run - pass --apply to write")
        return 0

    if att:
        aid = att[0]["id"]
    else:
        with open(ART, "rb") as f:
            blob = base64.b64encode(f.read()).decode()
        aid = call("ir.attachment", "create", [{
            "name": ART_NAME, "datas": blob, "mimetype": "image/webp",
            "public": True, "website_id": SITE,
            "res_model": "ir.ui.view", "res_id": 0, "type": "binary",
        }])
        aid = aid[0] if isinstance(aid, list) else aid
        print(f"  attachment {aid}")
    chk = call("ir.attachment", "read", [aid], ["checksum"])[0]["checksum"]
    src = f"/web/image/{aid}-{chk[:8]}/{ART_NAME}"

    if CSS_SENTINEL not in head:
        i = head.rindex("</style>")
        call("website", "write", [SITE],
             {"custom_code_head": head[:i] + CSS + head[i:]})
        back = call("website", "read", [SITE], ["custom_code_head"])[0]
        assert CSS_SENTINEL in back["custom_code_head"]

    arch = ARCH.format(slug=SLUG, title=TITLE, quote=QUOTE, who=WHO,
                       work=WORK, aid=aid, src=src)
    ET.fromstring(arch)

    if existing:
        pid, vid = existing[0]["id"], existing[0]["view_id"][0]
        call("ir.ui.view", "write", [vid], {"arch": arch})
    else:
        vid = call("ir.ui.view", "create", [{
            "name": SLUG, "type": "qweb", "key": f"website.{SLUG}",
            "arch": arch, "website_id": SITE,
        }])
        vid = vid[0] if isinstance(vid, list) else vid
        pid = call("website.page", "create", [{
            "view_id": vid, "url": "/" + SLUG, "website_id": SITE,
        }])
        pid = pid[0] if isinstance(pid, list) else pid
        print(f"  view {vid}  page {pid}")

    call("website.page", "write", [pid], {
        "is_published": True, "website_indexed": True,
        "website_meta_title": TITLE, "website_meta_description": DESC,
    })
    time.sleep(3)

    h = fetch("/" + SLUG)
    assert QUOTE in h, "quote not on the page"
    assert WORK in h, "citation not on the page"
    assert src in h, f"background {src} not on the page"
    assert "jd-quote-long" in h, "long-quote modifier missing"
    img = urllib.request.urlopen("https://www.judgedice.com" + src, timeout=40)
    print(f"\n  https://www.judgedice.com/{SLUG}  ok")
    print(f"  background {img.getcode()}  {img.headers.get('Content-Type')}"
          f"  {int(img.headers.get('Content-Length', 0))/1024:.0f} KB")

    nav = fetch("/work")
    print(f"  /random-% pages now in the menu rotation: "
          f"{'yes' if '/random-' in nav else 'check'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
