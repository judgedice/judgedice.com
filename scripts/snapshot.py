# -*- coding: utf-8 -*-
"""Pull the live judgedice.com (Odoo website_id=2) state into snapshot/ so the
site is version-controlled: run, review `git diff`, commit.

Captures: all site-2 qweb view arches, theme SCSS sources (palette + values),
website.custom_code_head/custom_code_footer, and page/menu records.

A mirror that only ever adds is not a mirror: a view that is deleted or
deactivated leaves its file behind, still looking deployable to deploy.py, which
maps filename -> record id. So files this run did not write are pruned.

Pruning deletes, so it is guarded. An empty view read aborts outright, and a
prune that would take more files than it leaves is refused - both look like a
failed read rather than a real deletion. --force-prune overrides the second,
--no-prune skips pruning entirely.

Read-only with respect to Odoo — it never writes there, and only ever deletes
inside snapshot/."""
import sys, os, json, base64, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(REPO, "snapshot")
SITE = 2  # judgedice.com — never touch site 1 (Half a Glass)


def slug(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s or "").strip("-") or "unnamed"


WRITTEN = set()  # relpaths this run produced; everything else in snapshot/ is stale


def write(relpath, content):
    path = os.path.join(SNAP, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content if content.endswith("\n") else content + "\n")
    WRITTEN.add(relpath)
    print("  wrote", os.path.relpath(path, REPO))


def prune(subdir, force=False):
    """Remove files under snapshot/<subdir>/ that this run did not write.

    Refuses when the stale files outnumber the surviving ones: that is the shape
    of a partial read, not of someone deleting a view."""
    d = os.path.join(SNAP, subdir)
    if not os.path.isdir(d):
        return
    present = {"%s/%s" % (subdir, n) for n in os.listdir(d)
               if os.path.isfile(os.path.join(d, n))}
    stale = sorted(present - WRITTEN)
    if not stale:
        return
    kept = len(present) - len(stale)
    if not force and len(stale) > kept:
        print("  REFUSING to prune %d of %d files in %s/ — that is the shape of a "
              "failed read, not a deletion. Re-run, or pass --force-prune."
              % (len(stale), len(present), subdir))
        return
    for rel in stale:
        os.remove(os.path.join(SNAP, rel))
        print("  pruned snapshot/%s" % rel)


def main(prune_=True, force_prune=False):
    uid, call = connect()

    # --- qweb views scoped to site 2 ---
    vids = call("ir.ui.view", "search", [["website_id", "=", SITE], ["type", "=", "qweb"]])
    views = call("ir.ui.view", "read", vids,
                 ["id", "name", "key", "inherit_id", "mode", "active", "arch_db"])
    print(f"[views] {len(views)} qweb views on site {SITE}")
    if not views:
        sys.exit("[views] live returned no qweb views for site %d. Refusing to write "
                 "a snapshot that would read as 'everything was deleted'." % SITE)
    index = []
    for v in sorted(views, key=lambda x: x["id"]):
        fname = "views/%04d-%s.xml" % (v["id"], slug(v["key"] or v["name"]))
        write(fname, v["arch_db"] or "")
        index.append({k: v[k] for k in ("id", "name", "key", "inherit_id", "mode", "active")})
    write("views/_index.json", json.dumps(index, indent=2, default=str))

    # --- theme SCSS sources (customized files live under /_custom/) ---
    aids = call("ir.attachment", "search",
                [["website_id", "=", SITE], ["url", "like", "/_custom/"]])
    atts = call("ir.attachment", "read", aids, ["id", "url", "datas"])
    print(f"[scss] {len(atts)} customized asset sources on site {SITE}")
    for a in sorted(atts, key=lambda x: x["id"]):
        body = base64.b64decode(a["datas"]).decode("utf-8") if a["datas"] else ""
        write("scss/%04d-%s" % (a["id"], slug(os.path.basename(a["url"]))), body)

    # --- website record: injected head/footer code ---
    w = call("website", "read", [SITE],
             ["name", "domain", "custom_code_head", "custom_code_footer", "homepage_url"])[0]
    write("custom_code_head.html", w.get("custom_code_head") or "")
    write("custom_code_footer.html", w.get("custom_code_footer") or "")

    # --- pages + menus ---
    pids = call("website.page", "search", [["website_id", "=", SITE]])
    pages = call("website.page", "read", pids,
                 ["id", "name", "url", "view_id", "is_published", "website_indexed"])
    mids = call("website.menu", "search", [["website_id", "=", SITE]])
    menus = call("website.menu", "read", mids,
                 ["id", "name", "url", "parent_id", "sequence"])
    write("records.json", json.dumps(
        {"website": {k: w[k] for k in ("name", "domain", "homepage_url")},
         "pages": sorted(pages, key=lambda p: p["id"]),
         "menus": sorted(menus, key=lambda m: (str(m["parent_id"]), m["sequence"]))},
        indent=2, default=str))

    if prune_:
        prune("views", force_prune)
        prune("scss", force_prune)

    print("\nSnapshot complete. Review with `git diff snapshot/`, then commit.")


if __name__ == "__main__":
    main(prune_="--no-prune" not in sys.argv,
         force_prune="--force-prune" in sys.argv)
