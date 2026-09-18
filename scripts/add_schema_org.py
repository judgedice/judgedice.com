#!/usr/bin/env python3
"""JSON-LD structured data, typed to what each page actually is.

Before this, every page on the site emitted one block - an Organization named
"Judge DiCesaro" from the footer - on the homepage, the offer page, a blog post
and a quote page alike. Judge is a person, not an organisation, and the trading
entity is Half a Glass; so the sitewide block becomes a Person plus a WebSite,
and each page adds the type that describes it.

Entities are given @id so they can be referenced rather than repeated: every
page points at the one Person and the one WebSite instead of restating them.

The block is injected between `<t t-call="website.layout">` and `<div
id="wrap">` - inside the layout, outside the builder-editable region, so the
website editor cannot pick it up and move or delete it.

Only facts already published on the site are used: the judge@judgedice.com
address that /connect shows, the $50 consultation that /shop lists, and the
quotes with their attributions as each page carries them. No postal address,
no phone, no private email.

Dry-run by default; --apply writes.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from odoo import connect

SITE = 2
BASE = "@@BASE@@"                       # replaced by a QWeb call at render time
QWEB_BASE = '<t t-out="website.get_base_url()"/>'
MARK = "v1"
BLOCK_RE = re.compile(
    r'\s*<script type="application/ld\+json" data-jd-schema="[^"]*">.*?</script>',
    re.S)

PERSON = f"{BASE}/#judge"
WEBSITE = f"{BASE}/#website"


def page(kind, path, name, extra=None):
    d = {"@context": "https://schema.org", "@type": kind,
         "@id": f"{BASE}{path}#page", "url": f"{BASE}{path}", "name": name,
         "isPartOf": {"@id": WEBSITE}}
    d.update(extra or {})
    return d


def quote_page(path, name, text, author, work=None, work_url=None):
    q = {"@type": "Quotation", "text": text,
         "creator": {"@type": "Person", "name": author}}
    if work:
        src = {"@type": "CreativeWork", "name": work}
        if work_url:
            src["url"] = work_url
        q["isBasedOn"] = src
    return page("WebPage", path, name, {"mainEntity": q})


SITEWIDE = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Person", "@id": PERSON, "name": "Judge DiCesaro",
         "url": f"{BASE}/", "email": "judge@judgedice.com",
         "jobTitle": "Tribute writer and digital architect",
         "description": "Tribute writer and digital architect. Eulogies, toasts, "
                        "send-offs and keepsakes — plus twenty-five years of work "
                        "inside the Adobe Experience Cloud.",
         "image": f"{BASE}/web/image/website/{SITE}/social_default_image"},
        {"@type": "WebSite", "@id": WEBSITE, "url": f"{BASE}/",
         "name": "judgedice.com", "inLanguage": "en-US",
         "publisher": {"@id": PERSON}},
    ],
}

OFFER_ITEMS = ["Eulogies & Memorials", "Celebration Speeches",
               "Professional Tributes", "Written Keepsakes"]

PAGES = {
    2034: page("WebPage", "/", "Judge DiCesaro — Delivering Joy since the turn "
               "of the Century", {"about": {"@id": PERSON},
               "primaryImageOfPage": f"{BASE}/web/image/website/{SITE}/social_default_image"}),
    2039: page("AboutPage", "/work", "Work Life — Judge DiCesaro",
               {"about": {"@id": PERSON},
                "description": "Twenty-five years of digital architecture and marketing "
                               "technology, mostly inside the Adobe Experience Cloud."}),
    2040: page("AboutPage", "/home", "Home Life — Judge DiCesaro",
               {"about": {"@id": PERSON},
                "description": "Life outside the enterprise tech stack."}),
    2041: page("WebPage", "/offerings", "Tribute Writing — Judge DiCesaro",
               {"mainEntity": {
                   "@type": "Service", "@id": f"{BASE}/offerings#service",
                   "name": "Tribute writing", "serviceType": "Tribute writing",
                   "provider": {"@id": PERSON},
                   "areaServed": {"@type": "Country", "name": "United States"},
                   "description": "Eulogies, toasts, send-offs, keepsakes — the right "
                                  "words for the moments that matter.",
                   "hasOfferCatalog": {
                       "@type": "OfferCatalog", "name": "Tribute writing",
                       "itemListElement": [
                           {"@type": "Offer",
                            "itemOffered": {"@type": "Service", "name": n}}
                           for n in OFFER_ITEMS]},
                   "offers": {
                       "@type": "Offer", "name": "Tribute Consultation",
                       "price": "50.00", "priceCurrency": "USD",
                       "url": f"{BASE}/shop/tribute-consultation-7",
                       "availability": "https://schema.org/InStock",
                       "description": "A 30-minute conversation about the tribute you "
                                      "need. Credited toward your quote if we work "
                                      "together."}}}),
    2042: page("ContactPage", "/connect", "Connect — Judge DiCesaro",
               {"mainEntity": {"@id": PERSON}}),
    2745: quote_page("/random-1", "Only light can do that — Judge DiCesaro",
                     "Darkness cannot drive out darkness: only light can do that. "
                     "Hate cannot drive out hate: only love can do that.",
                     "Martin Luther King Jr.", "Strength to Love"),
    2746: quote_page("/random-2", "You don't choose your personality — Judge DiCesaro",
                     "I've decided I can't hate anyone... because you don't choose "
                     "your personality.", "Oliver DiCesaro"),
    2748: quote_page("/random-3", "We are the ones we've been waiting for — Judge DiCesaro",
                     "We are the ones we've been waiting for.", "June Jordan",
                     "Poem for South African Women",
                     "https://poets.org/poem/poem-south-african-women"),
}


def block(data):
    """A <script> holding the JSON, with the base URL left to QWeb."""
    body = json.dumps(data, indent=2, ensure_ascii=False)
    body = escape(body)                      # &, <, > - before the QWeb tag goes in
    body = body.replace(escape(BASE), QWEB_BASE)
    return ('\n        <script type="application/ld+json" data-jd-schema="%s">\n%s\n'
            '        </script>' % (MARK, body))


def inject(arch, data):
    arch = BLOCK_RE.sub("", arch)            # idempotent: drop any previous block
    anchor = '<t t-call="website.layout">'
    assert arch.count(anchor) == 1, "unexpected layout call count"
    i = arch.index(anchor) + len(anchor)
    return arch[:i] + block(data) + arch[i:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    uid, call = connect()

    # --- sitewide: the footer's Organization becomes Person + WebSite ---
    foot = call("ir.ui.view", "read", [2038], ["id", "key", "website_id", "arch_db"])[0]
    assert foot["website_id"][0] == SITE, foot
    new_foot = re.sub(
        r'(<script t-if="website" type="application/ld\+json">)(.*?)(</script>)',
        lambda m: m.group(1) + "\n" + escape(
            json.dumps(SITEWIDE, indent=2, ensure_ascii=False)
        ).replace(escape(BASE), QWEB_BASE) + "\n        " + m.group(3),
        foot["arch_db"], count=1, flags=re.S)
    assert new_foot != foot["arch_db"], "footer JSON-LD block not found"
    ET.fromstring(new_foot)

    plan = [("footer 2038", 2038, new_foot)]
    for vid, data in PAGES.items():
        v = call("ir.ui.view", "read", [vid], ["id", "key", "website_id", "arch_db"])[0]
        assert v["website_id"][0] == SITE, v
        upd = inject(v["arch_db"], data)
        ET.fromstring(upd)
        plan.append(("%s %d" % (data["@type"], vid), vid, upd))

    for label, vid, upd in plan:
        print(f"  {label:<22} view {vid}  -> {len(upd)} chars")
    if not args.apply:
        print("\ndry run - pass --apply to write")
        return 0

    for label, vid, upd in plan:
        call("ir.ui.view", "write", [vid], {"arch": upd})
        back = call("ir.ui.view", "read", [vid], ["arch_db"])[0]["arch_db"]
        assert "application/ld+json" in back, vid
        print(f"  wrote view {vid} ({label})")
    print("applied; readback ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
