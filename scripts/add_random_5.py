#!/usr/bin/env python3
"""Add /random-5 — Ockham's razor, over the generated razor field.

The same four parts as /random-4, with two differences worth knowing:

  - this one runs LIGHT (o_cc1).  The quote-page CSS and the glass chrome
    both have a light branch already; none of the random pages had exercised
    it until now.
  - the quote is the one Ockham actually wrote.  The famous phrasing,
    "entities must not be multiplied beyond necessity", is absent from his
    extant work — that wording is John Punch's, 1639.  What is his, from the
    commentary on the Sentences, is "numquam ponenda est pluralitas sine
    necessitate": plurality is never to be posited without necessity.

The art comes from gen_razor_art.py --seed 1639 (Punch's year, since his
sentence is the one everybody quotes).

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
SLUG = "random-5"
ART = "processed_images/05_razor.webp"
ART_NAME = "05_razor.webp"

QUOTE = "Plurality is never to be posited without necessity."
WHO = "William of Ockham"
WORK = "Commentary on the Sentences of Peter Lombard"
TITLE = "Never to be posited without necessity — Judge DiCesaro"
DESC = ('"Plurality is never to be posited without necessity." — William of '
        "Ockham, Commentary on the Sentences of Peter Lombard. One of the "
        "lines kept on rotation at judgedice.com.")

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
        <div id="wrap" class="oe_structure oe_empty"><section class="s_jd_quotepage o_cc o_colored_level oe_img_bg o_bg_img_center o_bg_img_origin_border_box o_cc1" data-snippet="s_jd_quote_page" data-name="Quote Page" data-attachment-id="{aid}" data-format-mimetype="image/webp" data-resize-width="1920" data-original-id="{aid}" data-original-src="{src}" data-mimetype-before-conversion="image/webp" data-mimetype="image/webp" style="background-image: url('{src}');"><div class="s_jd_quotepage_scrim o_not_editable" aria-hidden="true"/><div class="s_jd_quotepage_inner"><blockquote class="s_jd_quotepage_block"><p class="s_jd_quotepage_text">{quote}</p><footer class="s_jd_quotepage_cite"><strong>{who}</strong> — <em>{work}</em></footer></blockquote></div></section></div>
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
    print(f"  art        {ART}  {os.path.getsize(ART)/1024:.0f} KB"
          f"  {'already uploaded' if att else 'upload'}")
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
    assert "o_cc1" in h, "light colour combination missing"
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
