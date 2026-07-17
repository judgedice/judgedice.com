# -*- coding: utf-8 -*-
"""Set site-2 color combinations (o-cc1..5) in user_values.scss (att 1087),
then publish all 5 judgedice pages. Backup printed before the SCSS write."""
import sys, base64
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

ATT = 1087
PAGES = [5, 6, 7, 8, 9]  # /, /work, /home, /exciting, /connect

# design palette
PAPER="#F2ECDF"; RAISED="#F8F3E8"; SUNK="#EAE2D2"; INK="#1C1712"; INKSOFT="#57514A"
BLACK="#100C08"; VERM="#CB4127"; VERMDEEP="#A6321C"; VERMLT="#E88C77"; BLUE="#274654"; PAPERDIM="#E6DFD0"

CC = {
 1: dict(bg=PAPER,  text=INKSOFT, headings=INK,   link=VERM,     bp=VERM, bpt=PAPER, bs=BLUE, bst=PAPER),
 2: dict(bg=RAISED, text=INKSOFT, headings=INK,   link=VERM,     bp=VERM, bpt=PAPER, bs=BLUE, bst=PAPER),
 3: dict(bg=SUNK,   text=INK,     headings=INK,   link=VERMDEEP, bp=VERM, bpt=PAPER, bs=INK,  bst=PAPER),
 4: dict(bg=INK,    text=PAPERDIM,headings=PAPER, link=VERMLT,   bp=VERM, bpt=PAPER, bs=PAPER,bst=INK),
 5: dict(bg=BLACK,  text=PAPERDIM,headings=PAPER, link=VERMLT,   bp=VERM, bpt=PAPER, bs=BLUE, bst=PAPER),
}

def cc_lines():
    out = []
    for n, c in CC.items():
        pairs = [
            (f"o-cc{n}-bg", c["bg"]), (f"o-cc{n}-text", c["text"]),
            (f"o-cc{n}-headings", c["headings"]), (f"o-cc{n}-link", c["link"]),
            (f"o-cc{n}-btn-primary", c["bp"]), (f"o-cc{n}-btn-primary-text", c["bpt"]),
            (f"o-cc{n}-btn-secondary", c["bs"]), (f"o-cc{n}-btn-secondary-text", c["bst"]),
        ]
        for k, v in pairs:
            out.append("    '%s': %s,\n" % (k, v))
    return "".join(out)

def main():
    uid, call = connect()

    att = call("ir.attachment","read",[ATT],["url","website_id","datas"])[0]
    assert att["website_id"] and att["website_id"][0] == 2, "not website 2!"
    cur = base64.b64decode(att["datas"]).decode("utf-8")
    print("=== BACKUP att %d (base64) ===\n%s\n" % (ATT, att["datas"]))

    if "'o-cc1-bg':" in cur:
        print("cc keys already present; aborting to avoid double-insert."); sys.exit(1)
    marker = "    // -- hook --"
    assert marker in cur, "hook marker missing"
    new = cur.replace(marker, cc_lines() + marker, 1)
    assert new.count("(") == cur.count("(") and new.count(")") == cur.count(")"), "paren imbalance"
    assert new.count("'") % 2 == 0, "unbalanced quotes"

    call("ir.attachment","write",[ATT], {"datas": base64.b64encode(new.encode()).decode("ascii")})
    print("[cc] att %d updated with o-cc1..5 combinations (%d keys)." % (ATT, len(CC)*8))

    # verify readback
    chk = base64.b64decode(call("ir.attachment","read",[ATT],["datas"])[0]["datas"]).decode()
    for n in range(1,6):
        assert ("o-cc%d-bg" % n) in chk
    print("[cc] readback OK — all 5 combinations present.")

    # publish pages
    call("website.page","write", PAGES, {"is_published": True})
    rows = call("website.page","read", PAGES, ["url","is_published"])
    print("\n[publish] pages:")
    for r in sorted(rows, key=lambda x: x["url"]):
        print("   %-11s published=%s" % (r["url"], r["is_published"]))
    print("\nDONE.")

if __name__ == "__main__":
    if "--apply" in sys.argv:
        main()
    else:
        print("dry-run. cc SCSS preview:\n" + cc_lines())
