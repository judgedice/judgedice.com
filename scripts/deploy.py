# -*- coding: utf-8 -*-
"""Deploy snapshot/ files to the live Odoo site (website_id=2).

Inverse of snapshot.py: snapshot/ is the source of truth and this pushes
changed files back to Odoo over XML-RPC. Guardrails:

  - every target must belong to website 2 (site 1 / Half a Glass is never touched)
  - view XML is validated with ElementTree before writing
  - DRIFT GUARD: the live value must match the --base commit's version of the
    file. If it doesn't, someone edited the site directly (Odoo builder) since
    the last deploy — abort so we never clobber those edits. Recover with:
    run snapshot.py, commit the drift, push again.
  - readback verify after each write

File → target mapping (ids are encoded in the snapshot filenames):
  snapshot/views/<id>-*.xml        -> ir.ui.view(<id>).arch + .active
  snapshot/views/<id>-*.inactive.xml -> same, deployed with active=False
  snapshot/scss/<id>-*.scss        -> ir.attachment(<id>).datas (base64)
  snapshot/custom_code_head.html   -> website(2).custom_code_head
  snapshot/custom_code_footer.html -> website(2).custom_code_footer
  snapshot/records.json, views/_index.json -> informational, skipped

Usage:
  python3 scripts/deploy.py --base <sha> [--apply] [--force] <files...>

Dry-run is the default; nothing is written without --apply.
--force skips the drift guard (use only after reviewing the drift).

A view file carries its active state in its name: the `.inactive` marker that
snapshot.py writes. Both the arch and the flag are compared and deployed, so
switching a view off (or back on) travels through git like any other change,
and renaming between the two forms is recognised as the same record.
Exit codes: 0 ok · 1 usage/validation · 2 drift detected · 3 verify failed
"""
import sys, os, re, base64, subprocess, xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 2


def norm(s):
    return (s or "").strip()


def git_show(base, relpath):
    """Content of relpath at commit `base`, or None if it didn't exist."""
    r = subprocess.run(["git", "show", "%s:%s" % (base, relpath)],
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


INACTIVE_MARK = ".inactive"


def wants_active(relpath):
    """A view file is deployed inactive when its name carries the marker."""
    return not relpath.endswith(INACTIVE_MARK + ".xml")


def sibling(relpath):
    """The same view file under the opposite active state."""
    if relpath.endswith(INACTIVE_MARK + ".xml"):
        return relpath[: -len(INACTIVE_MARK + ".xml")] + ".xml"
    return relpath[: -len(".xml")] + INACTIVE_MARK + ".xml"


def classify(relpath):
    m = re.match(r"snapshot/views/(\d+)-.*\.xml$", relpath)
    if m:
        return "view", int(m.group(1))
    m = re.match(r"snapshot/scss/(\d+)-.*\.scss$", relpath)
    if m:
        return "scss", int(m.group(1))
    if relpath == "snapshot/custom_code_head.html":
        return "head", SITE
    if relpath == "snapshot/custom_code_footer.html":
        return "footer", SITE
    return None, None


def read_live(call, kind, rid):
    """Return (live_content, label, live_active). Asserts site-2 ownership.

    live_active is None for anything that is not a view. Reading by id works on
    inactive records; only search() hides them."""
    if kind == "view":
        r = call("ir.ui.view", "read", [rid],
                 ["arch_db", "website_id", "key", "active"])[0]
        assert r["website_id"] and r["website_id"][0] == SITE, \
            "view %d is not website %d — refusing" % (rid, SITE)
        return r["arch_db"] or "", "view %d (%s)" % (rid, r["key"]), r["active"]
    if kind == "scss":
        r = call("ir.attachment", "read", [rid], ["datas", "website_id", "url"])[0]
        assert r["website_id"] and r["website_id"][0] == SITE, \
            "attachment %d is not website %d — refusing" % (rid, SITE)
        live = base64.b64decode(r["datas"]).decode("utf-8") if r["datas"] else ""
        return live, "attachment %d (%s)" % (rid, os.path.basename(r["url"] or "")), None
    field = "custom_code_head" if kind == "head" else "custom_code_footer"
    r = call("website", "read", [SITE], [field])[0]
    return r[field] or "", "website(%d).%s" % (SITE, field), None


def write_target(call, kind, rid, content, active=None):
    if kind == "view":
        vals = {"arch": content}
        if active is not None:
            vals["active"] = active
        call("ir.ui.view", "write", [rid], vals)
    elif kind == "scss":
        call("ir.attachment", "write", [rid],
             {"datas": base64.b64encode(content.encode("utf-8")).decode("ascii")})
    else:
        field = "custom_code_head" if kind == "head" else "custom_code_footer"
        call("website", "write", [SITE], {field: content or ""})


def main(argv):
    base, apply_, force, files = None, False, False, []
    it = iter(argv)
    for a in it:
        if a == "--base":
            base = next(it, None)
        elif a == "--apply":
            apply_ = True
        elif a == "--dry-run":
            apply_ = False
        elif a == "--force":
            force = True
        else:
            files.append(a)
    if not files:
        print(__doc__); return 1
    if not base and not force:
        print("--base <sha> is required (or --force to skip the drift guard)"); return 1

    uid, call = connect()
    mode = "APPLY" if apply_ else "dry-run"
    print("deploy [%s] base=%s files=%d" % (mode, base, len(files)))

    wrote, failures, drift = 0, 0, 0
    for f in files:
        rel = os.path.relpath(os.path.abspath(f), REPO).replace(os.sep, "/")
        kind, rid = classify(rel)
        if not kind:
            print("  skip  %s (informational, not deployable)" % rel); continue
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print("  skip  %s (deleted in repo; deletion not supported)" % rel); continue
        new = open(path, encoding="utf-8").read()

        if kind == "view":
            try:
                ET.fromstring(new)
            except ET.ParseError as e:
                print("  FAIL  %s — invalid XML: %s" % (rel, e)); failures += 1; continue

        live, label, live_active = read_live(call, kind, rid)
        want_active = wants_active(rel) if kind == "view" else None
        arch_same = norm(live) == norm(new)
        active_same = want_active is None or live_active == want_active
        if arch_same and active_same:
            print("  noop  %s — live already matches" % rel); continue

        # drift guard: live must equal what the repo last knew was deployed.
        # A view that was switched on or off is the SAME record under a new
        # filename, so when this path is absent at base look for its opposite
        # before calling it unknown - otherwise every toggle reads as drift.
        if not force:
            prev, prev_active = git_show(base, rel), want_active
            if prev is None and kind == "view":
                alt = git_show(base, sibling(rel))
                if alt is not None:
                    prev, prev_active = alt, not want_active
            if prev is None:
                print("  DRIFT %s — no version at base %s to compare against; "
                      "rerun with --force after review" % (rel, base))
                drift += 1; continue
            if norm(live) != norm(prev):
                print("  DRIFT %s — live %s differs from base commit (edited in "
                      "Odoo builder?). Run snapshot.py, commit, retry." % (rel, label))
                drift += 1; continue
            if prev_active is not None and live_active != prev_active:
                print("  DRIFT %s — live %s is %s but the base commit says %s "
                      "(toggled in Odoo?). Run snapshot.py, commit, retry."
                      % (rel, label, "active" if live_active else "inactive",
                         "active" if prev_active else "inactive"))
                drift += 1; continue

        changes = ([] if arch_same else ["arch %d chars" % len(new)]) + \
                  ([] if active_same else ["active=%s" % want_active])
        if not apply_:
            print("  would-write  %s -> %s (%s)" % (rel, label, ", ".join(changes))); continue

        write_target(call, kind, rid, new, want_active)
        back, _, back_active = read_live(call, kind, rid)
        if norm(back) != norm(new) or (want_active is not None and back_active != want_active):
            print("  FAIL  %s — readback mismatch after write!" % rel); failures += 1
        else:
            print("  wrote %s -> %s (%s, verified)" % (rel, label, ", ".join(changes))); wrote += 1

    print("done: %d written, %d drift, %d failed [%s]" % (wrote, drift, failures, mode))
    if failures:
        return 3
    if drift:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
