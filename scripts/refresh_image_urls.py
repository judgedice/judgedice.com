#!/usr/bin/env python3
"""Point the quote-page view arches at the rebuilt derivatives' new checksums.

The checksum in /web/image/<id>-<checksum>/ is a cache-buster, not a lookup key:
Odoo serves the current bytes whatever it says. But a browser that already
cached the old URL keeps the old (6.8 MB) file until it expires, so the arch has
to move to the new checksum for the fix to actually reach returning visitors.

Only the <id>-<checksum> prefix changes; nothing else in the arch is touched.
"""
import re, sys
sys.path.insert(0, "scripts")
from odoo import connect
import xml.etree.ElementTree as ET

APPLY = "--apply" in sys.argv
uid, call = connect()

current = {a["id"]: a["checksum"]
           for a in call("ir.attachment", "read", [1495, 1496, 1497, 1515, 1516],
                         ["id", "checksum"])}

for v in call("ir.ui.view", "read", [2745, 2746, 2748], ["id", "key", "arch_db"]):
    arch = v["arch_db"]
    new = arch
    changed = []

    def sub(m):
        aid, old = int(m.group(1)), m.group(2)
        cur = current.get(aid)
        if not cur or cur.startswith(old):
            return m.group(0)
        changed.append((aid, old[:8], cur[:8]))
        return f"/web/image/{aid}-{cur[:8]}/"

    new = re.sub(r"/web/image/(\d+)-([0-9a-f]+)/", sub, arch)
    if not changed:
        print(f"  view {v['id']}: already current")
        continue

    # the only difference may be the checksums
    assert len(new) - len(arch) == 0 or True
    ET.fromstring(new)  # must stay well-formed
    stripped_old = re.sub(r"/web/image/(\d+)-([0-9a-f]+)/", r"/web/image/\1/", arch)
    stripped_new = re.sub(r"/web/image/(\d+)-([0-9a-f]+)/", r"/web/image/\1/", new)
    assert stripped_old == stripped_new, "something other than a checksum changed"

    print(f"  view {v['id']} {v['key']}: " +
          ", ".join(f"{a} {o}->{n}" for a, o, n in changed))
    if APPLY:
        call("ir.ui.view", "write", [v["id"]], {"arch": new})
        back = call("ir.ui.view", "read", [v["id"]], ["arch_db"])[0]["arch_db"]
        for aid, _, n in changed:
            assert f"/web/image/{aid}-{n}" in back, (aid, n)
        print(f"    written, readback ok")

print("dry run - pass --apply to write" if not APPLY else "done")
