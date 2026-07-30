# -*- coding: utf-8 -*-
"""Add the Adobe credentials strip to the judgedice.com homepage (view 2034).

Uploads the two Adobe badge images as public site-2 attachments, then inserts
a "Credentials" section after the hero. Idempotent: skips the insert if the
sentinel is already present, and reuses attachments by name.

Badge PNGs are read from assets/ (committed alongside this script) because
Adobe serves them from signed URLs that expire.

Dry-run by default; pass --apply to write.
"""
import sys, os, base64, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE, VIEW = 2, 2034
SENTINEL = "jd-credentials"

BADGES = {
    "expert": ("adobe_certified_expert_badge.png", "assets/adobe_ace_badge.png"),
    "professional": ("adobe_certified_professional_badge.png", "assets/adobe_acp_badge.png"),
}

# (tier, name, issued, valid-through, verify uuid)
CREDENTIALS = [
    ("expert", "Experience Manager Sites Business Practitioner", "2026", "June 2028",
     "6b622dda-5f52-11f1-be16-42010a400fe2"),
    ("expert", "Workfront Core Developer", "2022", "May 2028",
     "014aa341-5da3-44ec-93f9-833e442424ad"),
    ("professional", "Experience Manager Assets Developer", "2026", "June 2028",
     "9620905c-601b-11f1-be16-42010a400fe2"),
    ("professional", "Real-Time CDP Business Practitioner", "2023", "July 2027",
     "cc6d9e14-bbff-4bf0-8aa0-0cecce36ba3f"),
]

TIER_LABEL = {"expert": "Adobe Certified Expert", "professional": "Adobe Certified Professional"}

SERIF = "font-family:var(--font-serif);"
CARD = ("background:var(--surface-card);border:none;border-top:2px solid var(--ink);"
        "border-radius:0;padding:var(--space-6);display:flex;flex-direction:column;gap:12px;")
META = (SERIF + "font-size:var(--text-meta);text-transform:uppercase;"
        "letter-spacing:var(--tracking-label);color:var(--ink-faint);margin:0;")


def card(att_id, tier, name, issued, valid, uuid):
    return (
        '<div style="%s">'
        '<img src="/web/image/%d" alt="%s badge" loading="lazy" '
        'style="width:56px;height:auto;display:block;"/>'
        '<div>'
        '<p style="%sfont-size:var(--text-label);text-transform:uppercase;'
        'letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);'
        'color:var(--vermilion);margin:0 0 6px;">%s</p>'
        '<h3 style="%sfont-size:1.125rem;font-weight:400;line-height:1.25;'
        'letter-spacing:-0.01em;color:var(--ink);margin:0;">%s</h3>'
        '</div>'
        '<p style="%s">Issued %s &#183; Valid through %s</p>'
        '<a href="https://certification.adobe.com/credential/verify/%s" '
        'target="_blank" rel="noopener noreferrer" '
        'style="%sfont-size:var(--text-meta);text-transform:uppercase;'
        'letter-spacing:var(--tracking-label);color:var(--ink);text-decoration:none;'
        'border-bottom:1px solid var(--vermilion);padding-bottom:2px;align-self:flex-start;'
        'margin-top:auto;">Verify &#8599;</a>'
        '</div>'
        % (CARD, att_id, TIER_LABEL[tier], SERIF, TIER_LABEL[tier], SERIF, name,
           META, issued, valid, uuid, SERIF)
    )


def section(att_ids):
    cards = "".join(card(att_ids[t], t, n, i, v, u) for t, n, i, v, u in CREDENTIALS)
    return (
        '<section class="%s" style="padding:clamp(3.5rem,8vw,6rem) clamp(1.5rem,6vw,6rem);'
        'border-top:1px solid var(--line);">'
        '<div style="max-width:72rem;margin:0 auto;">'
        '<div style="display:flex;align-items:center;gap:14px;%sfont-size:var(--text-label);'
        'text-transform:uppercase;letter-spacing:var(--tracking-label);'
        'font-weight:var(--weight-medium);color:var(--vermilion);margin-bottom:26px;">'
        '<span>Certifications</span>'
        '<span style="flex:1;height:1px;background:var(--line);min-width:24px;"/>'
        '</div>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));'
        'gap:clamp(1rem,2vw,1.5rem);">%s</div>'
        '</div></section>' % (SENTINEL, SERIF, cards)
    )


def main(apply_):
    uid, call = connect()
    print("add_credentials [%s]" % ("APPLY" if apply_ else "dry-run"))

    att_ids = {}
    for tier, (name, relpath) in BADGES.items():
        path = os.path.join(REPO, relpath)
        if not os.path.exists(path):
            print("  MISSING asset %s — aborting" % relpath)
            return 1
        found = call("ir.attachment", "search", [["name", "=", name], ["website_id", "=", SITE]])
        if found:
            att_ids[tier] = found[0]
            print("  attachment exists: %s -> %d" % (name, found[0]))
        elif apply_:
            att_ids[tier] = call("ir.attachment", "create", {
                "name": name,
                "datas": base64.b64encode(open(path, "rb").read()).decode("ascii"),
                "mimetype": "image/png", "public": True,
                "website_id": SITE, "res_model": "ir.ui.view"})
            print("  uploaded %s -> attachment %d" % (name, att_ids[tier]))
        else:
            att_ids[tier] = 0
            print("  would-upload %s (%d bytes)" % (name, os.path.getsize(path)))

    arch = call("ir.ui.view", "read", [VIEW], ["arch_db", "website_id"])[0]
    assert arch["website_id"][0] == SITE, "view %d is not site %d" % (VIEW, SITE)
    if SENTINEL in arch["arch_db"]:
        print("  credentials section already present — nothing to do")
        return 0

    body = arch["arch_db"]
    marker = '</section><section class="s_text_image'
    assert marker in body, "expected hero/text-image boundary not found"
    new = body.replace(marker, "</section>" + section(att_ids) + '<section class="s_text_image', 1)
    ET.fromstring(new)
    print("  section built (%d chars), XML valid" % (len(new) - len(body)))

    if not apply_:
        print("  would-write view %d" % VIEW)
        return 0

    call("ir.ui.view", "write", [VIEW], {"arch": new})
    back = call("ir.ui.view", "read", [VIEW], ["arch_db"])[0]["arch_db"]
    assert SENTINEL in back, "readback failed — section not in saved arch"
    print("  wrote view %d, verified" % VIEW)
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
