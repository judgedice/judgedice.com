# -*- coding: utf-8 -*-
"""Set judgedice.com (website 2) theme palette to the design-system colors.
Edits ir.attachment 1086 (user_theme_color_palette.scss) by inserting o-color-1..5
before the existing '// -- hook --' marker. Prints a base64 backup first."""
import sys, base64
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

ATT = 1086
COLORS = [
    ("o-color-1", "#CB4127"),  # vermilion  (primary)
    ("o-color-2", "#274654"),  # ink-blue   (secondary)
    ("o-color-3", "#F2ECDF"),  # paper      (light bg)
    ("o-color-4", "#F8F3E8"),  # paper-raised (alt surface)
    ("o-color-5", "#1C1712"),  # ink        (dark)
]

def main():
    uid, call = connect()
    att = call("ir.attachment", "read", [ATT], ["url", "website_id", "datas"])[0]
    assert att["website_id"] and att["website_id"][0] == 2, "attachment is not website 2!"
    cur = base64.b64decode(att["datas"]).decode("utf-8")

    print("=== BACKUP (base64 of current datas — keep to restore) ===")
    print(att["datas"])
    print("=== current content ===")
    print(cur)

    if "o-color-1" in cur:
        print("\nPalette already contains o-color-1; aborting to avoid double-insert.")
        sys.exit(1)

    lines = "".join("    '%s': %s,\n" % (k, v) for k, v in COLORS)
    marker = "    // -- hook --"
    assert marker in cur, "hook marker not found"
    new = cur.replace(marker, lines + marker, 1)

    # sanity: parens/braces balance unchanged
    assert new.count("(") == cur.count("(") and new.count(")") == cur.count(")"), "paren imbalance"

    print("\n=== NEW content ===")
    print(new)

    datas = base64.b64encode(new.encode("utf-8")).decode("ascii")
    call("ir.attachment", "write", [ATT], {"datas": datas})
    print("\n[ok] attachment %d updated — theme palette set for website 2." % ATT)
    print("Reload the website editor; asset bundle recompiles on next request.")

if __name__ == "__main__":
    if "--apply" in sys.argv:
        main()
    else:
        print("dry-run; pass --apply")
