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
  snapshot/views/<id>-*.xml        -> ir.ui.view(<id>).arch
  snapshot/scss/<id>-*.scss        -> ir.attachment(<id>).datas (base64)
  snapshot/custom_code_head.html   -> website(2).custom_code_head
  snapshot/custom_code_footer.html -> website(2).custom_code_footer
  snapshot/records.json, views/_index.json -> informational, skipped

Usage:
  python3 scripts/deploy.py --base <sha> [--apply] [--force] <files...>

Dry-run is the default; nothing is written without --apply.
--force skips the drift guard (use only after reviewing the drift).
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
    """Return (live_content, label). Asserts site-2 ownership."""
    if kind == "view":
        r = call("ir.ui.view", "read", [rid], ["arch_db", "website_id", "key"])[0]
        assert r["website_id"] and r["website_id"][0] == SITE, \
            "view %d is not website %d — refusing" % (rid, SITE)
        return r["arch_db"] or "", "view %d (%s)" % (rid, r["key"])
    if kind == "scss":
        r = call("ir.attachment", "read", [rid], ["datas", "website_id", "url"])[0]
        assert r["website_id"] and r["website_id"][0] == SITE, \
            "attachment %d is not website %d — refusing" % (rid, SITE)
        live = base64.b64decode(r["datas"]).decode("utf-8") if r["datas"] else ""
        return live, "attachment %d (%s)" % (rid, os.path.basename(r["url"] or ""))
    field = "custom_code_head" if kind == "head" else "custom_code_footer"
    r = call("website", "read", [SITE], [field])[0]
    return r[field] or "", "website(%d).%s" % (SITE, field)


def write_target(call, kind, rid, content):
    if kind == "view":
        call("ir.ui.view", "write", [rid], {"arch": content})
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

        live, label = read_live(call, kind, rid)
        if norm(live) == norm(new):
            print("  noop  %s — live already matches" % rel); continue

        # drift guard: live must equal what the repo last knew was deployed
        if not force:
            prev = git_show(base, rel)
            if prev is None:
                print("  DRIFT %s — no version at base %s to compare against; "
                      "rerun with --force after review" % (rel, base))
                drift += 1; continue
            if norm(live) != norm(prev):
                print("  DRIFT %s — live %s differs from base commit (edited in "
                      "Odoo builder?). Run snapshot.py, commit, retry." % (rel, label))
                drift += 1; continue

        if not apply_:
            print("  would-write  %s -> %s (%d chars)" % (rel, label, len(new))); continue

        write_target(call, kind, rid, new)
        back, _ = read_live(call, kind, rid)
        if norm(back) != norm(new):
            print("  FAIL  %s — readback mismatch after write!" % rel); failures += 1
        else:
            print("  wrote %s -> %s (%d chars, verified)" % (rel, label, len(new))); wrote += 1

    print("done: %d written, %d drift, %d failed [%s]" % (wrote, drift, failures, mode))
    if failures:
        return 3
    if drift:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
