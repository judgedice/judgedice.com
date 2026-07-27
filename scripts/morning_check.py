# -*- coding: utf-8 -*-
"""Morning check: test the live site against the roadmap; emit a decisions brief.

Read-only everywhere: HTTP probes of the public site, XML-RPC reads of the
funnel records, drift comparison against snapshot/, and gh reads of the
deploy workflow + roadmap board. Never writes to Odoo.

Output: reports/morning.html (published as the Morning Docket artifact)
        reports/morning.json (raw results, for debugging)
Exit 0 always (a failed check is a report line, not a crash).
"""
import sys, os, re, json, ssl, socket, html, base64, subprocess, datetime
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect
import deploy  # reuse classify/read_live/norm for drift checks

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ODOO_HOST = "half-a-glass1.odoo.com"
SITE_HOST = "www.judgedice.com"

checks = []       # {area, name, ok, detail}
numbers = []      # {label, value, note}
decisions = []    # {title, why, options: [..]}
roadmap = {}      # phase -> {done, total, todo_titles}

def check(area, name, ok, detail=""):
    checks.append({"area": area, "name": name, "ok": bool(ok), "detail": detail})

def decision(title, why, options):
    decisions.append({"title": title, "why": why, "options": options})

def fetch(path):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request("https://%s%s" % (ODOO_HOST, path),
                                 headers={"Host": SITE_HOST, "User-Agent": "morning-check"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")

def gh(*args):
    r = subprocess.run(["gh"] + list(args), capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return r.stdout

# ---------------------------------------------------------------- HTTP probes
PAGES = [
    ("/", "Home", None),
    ("/offerings", "Offerings", "I write tributes"),
    ("/blog", "Entries", "Entries"),
    ("/appointment", "Booking listing", "Tribute Consultation"),
    ("/shop/tribute-consultation-7", "Consult product", "HALF A GLASS"),
    ("/shop/cart", "Cart", None),
]
for path, name, sentinel in PAGES:
    try:
        code, body = fetch(path)
        ok = code == 200 and (sentinel is None or sentinel in body)
        detail = "HTTP %d" % code + ("" if ok or sentinel is None else ", sentinel missing")
        check("Site", name + " (" + path + ")", ok, detail)
        if path == "/appointment/1":
            pass
    except Exception as e:
        check("Site", name + " (" + path + ")", False, str(e)[:120])

# appointment slots actually offered
try:
    code, body = fetch("/appointment/1")
    m = re.findall(r'data-available-slots="([^"]*)"', body)
    nslots = sum(html.unescape(x).count('"datetime"') for x in m)
    check("Site", "Booking calendar shows slots", code == 200 and nslots > 0,
          "%d slots in first visible window" % nslots)
except Exception as e:
    check("Site", "Booking calendar shows slots", False, str(e)[:120])

# DNS + certificate for the real domain
try:
    socket.gethostbyname(SITE_HOST)
    dns_ok = True
except Exception:
    dns_ok = False
check("Launch", "DNS resolves for %s" % SITE_HOST, dns_ok,
      "" if dns_ok else "domain not pointed anywhere yet")
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with socket.create_connection((ODOO_HOST, 443), timeout=15) as s:
        with ctx.wrap_socket(s, server_hostname=SITE_HOST) as w:
            der = w.getpeercert(binary_form=True)
    cn = ""
    try:
        import tempfile
        pem = ssl.DER_cert_to_PEM_cert(der)
        with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
            f.write(pem); pemf = f.name
        out = subprocess.run(["openssl", "x509", "-noout", "-subject", "-in", pemf],
                             capture_output=True, text=True).stdout
        os.unlink(pemf)
        cn = out.strip()
    except Exception:
        pass
    per_domain = "judgedice" in cn
    check("Launch", "Per-domain SSL certificate", per_domain,
          cn or "could not parse cert subject")
    if not per_domain:
        decision("Point DNS + get the per-domain cert",
                 "The site still serves the *.odoo.com wildcard cert; browsers hitting "
                 "www.judgedice.com directly will warn until DNS points at Odoo and the "
                 "cert is provisioned.",
                 ["Point www CNAME at %s in Route 53 now" % ODOO_HOST,
                  "Hold until content is ready for public traffic"])
except Exception as e:
    check("Launch", "Per-domain SSL certificate", False, str(e)[:120])

# ---------------------------------------------------------------- Odoo state
uid = call = None
try:
    uid, call = connect()
    check("Odoo", "API reachable", True, "uid %s" % uid)
except Exception as e:
    check("Odoo", "API reachable", False, str(e)[:120])

if call:
    try:
        p = call("product.template", "read", [7], ["list_price", "is_published", "website_id"])[0]
        check("Funnel", "Consult product $50 + published",
              p["is_published"] and p["list_price"] == 50.0 and p["website_id"][0] == 2,
              "price %s" % p["list_price"])
    except Exception as e:
        check("Funnel", "Consult product", False, str(e)[:120])

    try:
        pr = call("loyalty.program", "read", [2], ["active", "max_usage", "total_order_count"])[0]
        used = pr.get("total_order_count") or 0
        left = (pr.get("max_usage") or 0) - used
        check("Funnel", "FOUNDING coupon active", pr["active"], "%d redemptions, %d left" % (used, left))
        numbers.append({"label": "Founding seats left", "value": left, "note": "of 25"})
        if left <= 5 and pr["active"]:
            decision("Founding program nearly exhausted",
                     "Only %d free-consult redemptions remain." % left,
                     ["Raise the cap", "Let it lapse and go full price", "New code for a second cohort"])
    except Exception as e:
        check("Funnel", "FOUNDING coupon", False, str(e)[:120])

    try:
        a = call("appointment.type", "read", [1], ["is_published", "users_wo_google_calendar_msg"])[0]
        check("Funnel", "Consult appointment published", a["is_published"], "")
        no_sync = bool(a.get("users_wo_google_calendar_msg"))
        check("Funnel", "Google Calendar synced", not no_sync,
              "busy times won't block slots" if no_sync else "")
        if no_sync:
            decision("Connect Google Calendar",
                     "Odoo can't see your real calendar; a 2pm conflict still shows as bookable.",
                     ["Connect it in Odoo user preferences (5 min)",
                      "Accept double-booking risk for now"])
    except Exception as e:
        check("Funnel", "Appointment type", False, str(e)[:120])

    try:
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        meetings = call("calendar.event", "search_read",
                        [["appointment_type_id", "=", 1], ["start", ">=", now]],
                        fields=["start", "partner_ids"], limit=10, order="start")
        numbers.append({"label": "Upcoming consults", "value": len(meetings),
                        "note": meetings[0]["start"] if meetings else "none booked"})
    except Exception as e:
        numbers.append({"label": "Upcoming consults", "value": "?", "note": str(e)[:60]})

    try:
        day_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        orders = call("sale.order", "search_read",
                      [["website_id", "=", 2], ["create_date", ">=", day_ago],
                       ["state", "in", ["sale", "done"]]],
                      fields=["amount_total", "partner_id"], limit=20)
        rev = sum(o["amount_total"] for o in orders)
        numbers.append({"label": "Orders last 24h", "value": len(orders), "note": "$%.0f" % rev})
        if orders:
            decision("New customer(s) overnight",
                     "%d confirmed order(s) — the clock on their consult experience is running." % len(orders),
                     ["Review the intake notes before the call", "Send a personal welcome note"])
    except Exception as e:
        numbers.append({"label": "Orders last 24h", "value": "?", "note": str(e)[:60]})

    try:
        s = call("payment.provider", "read", [16], ["state"])[0]["state"]
        check("Funnel", "Stripe provider enabled", s == "enabled", "state: %s" % s)
    except Exception as e:
        check("Funnel", "Stripe provider", False, str(e)[:120])

    try:
        pub = call("blog.post", "search_count", [["blog_id", "=", 1], ["is_published", "=", True]])
        numbers.append({"label": "Published entries", "value": pub, "note": "target: 4-6 samples"})
        if pub == 0:
            decision("The Entries shelf is empty",
                     "The funnel's top (sample tributes that make people want one) has no content; "
                     "the sample post is still unpublished.",
                     ["Draft one anonymized tribute this week (Claude formats + publishes)",
                      "Write the first opinion piece instead"])
    except Exception as e:
        numbers.append({"label": "Published entries", "value": "?", "note": str(e)[:60]})

    # drift: live Odoo vs committed snapshot
    try:
        drifted = []
        snapdir = os.path.join(REPO, "snapshot")
        for root, _, files in os.walk(snapdir):
            for fn in files:
                rel = os.path.relpath(os.path.join(root, fn), REPO).replace(os.sep, "/")
                kind, rid = deploy.classify(rel)
                if not kind:
                    continue
                live, _label = deploy.read_live(call, kind, rid)
                disk = open(os.path.join(REPO, rel), encoding="utf-8").read()
                if deploy.norm(live) != deploy.norm(disk):
                    drifted.append(rel)
        check("Repo", "Live matches snapshot (no drift)", not drifted,
              ", ".join(d.split("/")[-1] for d in drifted[:5]) if drifted else "")
        if drifted:
            decision("Snapshot drift detected",
                     "%d file(s) changed in the Odoo builder since the last commit; the next "
                     "GitOps deploy will abort until captured." % len(drifted),
                     ["Run snapshot.py + commit (keeps builder edits)",
                      "Deploy repo version over it (discards builder edits)"])
    except Exception as e:
        check("Repo", "Drift check", False, str(e)[:120])

# ---------------------------------------------------------------- GitHub side
try:
    secrets = gh("secret", "list", "--repo", "judgedice/judgedice.com")
    have = all(k in secrets for k in ["ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_KEY"])
    check("Repo", "Actions secrets set (GitOps live)", have,
          "" if have else "deploys skip until the four ODOO_* secrets are set")
    if not have:
        decision("Turn on push-to-deploy",
                 "The deploy Action still skips: repo secrets are unset, so snapshot edits "
                 "don't reach Odoo on push.",
                 ["Run the gh secret set commands from the P0 board item",
                  "Keep deploying via local scripts"])
except Exception as e:
    check("Repo", "Actions secrets", False, str(e)[:120])

try:
    run = json.loads(gh("run", "list", "--repo", "judgedice/judgedice.com",
                        "--limit", "1", "--json", "conclusion,displayTitle"))[0]
    check("Repo", "Last deploy workflow", run["conclusion"] == "success",
          "%s (%s)" % (run["conclusion"], run["displayTitle"][:40]))
except Exception as e:
    check("Repo", "Last deploy workflow", False, str(e)[:120])

try:
    items = json.loads(gh("project", "item-list", "2", "--owner", "judgedice",
                          "--format", "json", "--limit", "80"))["items"]
    for it in items:
        ph = (it.get("phase") or "?").split(" ")[0]
        st = it.get("status") or "Todo"
        roadmap.setdefault(ph, {"done": 0, "total": 0, "todo": []})
        roadmap[ph]["total"] += 1
        if st == "Done":
            roadmap[ph]["done"] += 1
        elif ph in ("P0", "P1", "P2"):
            roadmap[ph]["todo"].append(it["title"])
except Exception as e:
    check("Repo", "Roadmap board read", False, str(e)[:120])

# standing decisions the board can't see
decision("Free side door on the booking calendar",
         "/appointment/1 is public: anyone with the link books a consult without paying. "
         "The funnel steers through checkout, but nothing enforces it.",
         ["Unpublish the type (link only from post-payment page)",
          "Add Odoo's native payment step as a backstop",
          "Leave open while volume is founding-customer only"])

# ---------------------------------------------------------------- render
ok_n = sum(1 for c in checks if c["ok"])
stamp = datetime.datetime.now().strftime("%A, %B %-d, %Y · %-I:%M %p")
verdict = ("All %d checks passing." % len(checks)) if ok_n == len(checks) else \
          ("%d of %d checks failing." % (len(checks) - ok_n, len(checks)))

def esc(s):
    return html.escape(str(s), quote=True)

rows = ""
area_prev = None
for c in checks:
    area = c["area"] if c["area"] != area_prev else ""
    area_prev = c["area"]
    rows += ('<tr><td class="area">%s</td><td>%s</td><td class="%s">%s</td>'
             '<td class="detail">%s</td></tr>'
             % (esc(area), esc(c["name"]), "ok" if c["ok"] else "fail",
                "PASS" if c["ok"] else "FAIL", esc(c["detail"])))

tiles = "".join('<div class="tile"><div class="v">%s</div><div class="l">%s</div>'
                '<div class="n">%s</div></div>'
                % (esc(n["value"]), esc(n["label"]), esc(n["note"])) for n in numbers)

dec_html = ""
for i, d in enumerate(decisions, 1):
    opts = "".join("<li>%s</li>" % esc(o) for o in d["options"])
    dec_html += ('<article class="dec"><div class="dnum">%02d</div><div>'
                 '<h3>%s</h3><p>%s</p><ul>%s</ul></div></article>'
                 % (i, esc(d["title"]), esc(d["why"]), opts))
if not decisions:
    dec_html = '<p class="quiet">Nothing needs a call today.</p>'

phases = ""
ORDER = ["P0", "P1", "P2", "P3", "P4", "P5"]
NAMES = {"P0": "Go-live", "P1": "Offer & Entries", "P2": "Checkout", "P3": "Portal",
         "P4": "Marketing", "P5": "Scale"}
for ph in ORDER:
    r = roadmap.get(ph)
    if not r:
        continue
    pct = int(100 * r["done"] / r["total"]) if r["total"] else 0
    todo = "".join("<li>%s</li>" % esc(t) for t in r.get("todo", [])[:4])
    phases += ('<div class="phase"><div class="phead"><span>%s · %s</span>'
               '<span class="tnum">%d/%d</span></div>'
               '<div class="bar"><span style="width:%d%%"></span></div>%s</div>'
               % (ph, NAMES.get(ph, ""), r["done"], r["total"], pct,
                  ("<ul class='ptodo'>%s</ul>" % todo) if todo else ""))

page = """<title>Morning Docket - judgedice.com</title>
<style>
:root{--paper:#F2ECDF;--raised:#F8F3E8;--ink:#1C1712;--soft:#4A4038;--faint:#8A7E70;
--line:#D8CFBE;--verm:#CB4127;--good:#3E6B4F;}
@media (prefers-color-scheme: dark){:root{--paper:#1C1712;--raised:#26201A;--ink:#F2ECDF;
--soft:#C9BEAF;--faint:#8A7E70;--line:#3A322A;--verm:#E05A3D;--good:#7FB08F;}}
:root[data-theme="dark"]{--paper:#1C1712;--raised:#26201A;--ink:#F2ECDF;--soft:#C9BEAF;
--faint:#8A7E70;--line:#3A322A;--verm:#E05A3D;--good:#7FB08F;}
:root[data-theme="light"]{--paper:#F2ECDF;--raised:#F8F3E8;--ink:#1C1712;--soft:#4A4038;
--faint:#8A7E70;--line:#D8CFBE;--verm:#CB4127;--good:#3E6B4F;}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);margin:0;
font-family:'Iowan Old Style','Palatino Linotype',Georgia,serif;line-height:1.55}
.wrap{max-width:62rem;margin:0 auto;padding:clamp(1.5rem,5vw,3.5rem)}
.kicker{display:flex;align-items:center;gap:12px;text-transform:uppercase;
letter-spacing:.14em;font-size:.72rem;color:var(--verm);font-weight:600}
.kicker .rule{flex:1;height:1px;background:var(--line)}
h1{font-family:'Arial Narrow','Avenir Next Condensed','Helvetica Neue',sans-serif;
font-stretch:condensed;text-transform:uppercase;font-weight:700;letter-spacing:-.005em;
font-size:clamp(2.2rem,7vw,4rem);line-height:1.02;margin:.35rem 0 0;text-wrap:balance}
.stamp{font-style:italic;color:var(--soft);margin:.6rem 0 0}
.verdict{margin:1.1rem 0 0;padding:12px 16px;background:var(--raised);
border-left:2px solid var(--verm);font-size:1.05rem}
h2{font-family:'Arial Narrow','Avenir Next Condensed',sans-serif;text-transform:uppercase;
font-size:1.15rem;letter-spacing:.03em;margin:2.6rem 0 .9rem;display:flex;gap:12px;align-items:center}
h2::after{content:"";flex:1;height:1px;background:var(--line)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.tile{background:var(--raised);border:1px solid var(--line);padding:14px 16px}
.tile .v{font-family:'Arial Narrow','Avenir Next Condensed',sans-serif;font-size:2rem;
font-weight:700;font-variant-numeric:tabular-nums}
.tile .l{text-transform:uppercase;font-size:.7rem;letter-spacing:.12em;color:var(--soft)}
.tile .n{font-size:.82rem;color:var(--faint);font-style:italic}
.dec{display:grid;grid-template-columns:3rem 1fr;gap:14px;padding:18px 0;
border-top:1px solid var(--line)}
.dec .dnum{font-size:1rem;color:var(--verm);font-variant-numeric:tabular-nums}
.dec h3{margin:0;font-size:1.2rem;font-weight:600}
.dec p{margin:.4rem 0 .5rem;color:var(--soft);max-width:60ch}
.dec ul{margin:0;padding-left:1.1rem;color:var(--soft);font-size:.95rem}
.dec li{margin:.15rem 0}
table{border-collapse:collapse;width:100%;font-size:.92rem}
td{padding:7px 10px;border-top:1px solid var(--line);vertical-align:top}
td.area{text-transform:uppercase;font-size:.7rem;letter-spacing:.12em;color:var(--faint);
white-space:nowrap;padding-top:10px}
td.ok{color:var(--good);font-weight:700;font-family:'Arial Narrow',sans-serif}
td.fail{color:var(--verm);font-weight:700;font-family:'Arial Narrow',sans-serif}
td.detail{color:var(--faint);font-style:italic}
.phase{margin:0 0 1.1rem}
.phead{display:flex;justify-content:space-between;text-transform:uppercase;
font-size:.78rem;letter-spacing:.1em;color:var(--soft)}
.tnum{font-variant-numeric:tabular-nums}
.bar{height:6px;background:var(--raised);border:1px solid var(--line);margin-top:5px}
.bar span{display:block;height:100%;background:var(--verm)}
.ptodo{margin:.5rem 0 0;padding-left:1.1rem;font-size:.88rem;color:var(--faint)}
.quiet{font-style:italic;color:var(--faint)}
footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);
font-size:.8rem;color:var(--faint);font-style:italic}
@media (max-width:520px){.dec{grid-template-columns:1fr}.dec .dnum{display:none}}
</style>
<div class="wrap">
<div class="kicker"><span>Daily brief</span><span class="rule"></span></div>
<h1>The Morning Docket</h1>
<p class="stamp">__STAMP__</p>
<div class="verdict">__VERDICT__ __NDEC__ decision__PLURAL__ waiting below.</div>
<h2>Decisions on your desk</h2>
__DECISIONS__
<h2>The numbers</h2>
<div class="tiles">__TILES__</div>
<h2>Roadmap</h2>
__PHASES__
<h2>Checks</h2>
<div style="overflow-x:auto"><table>__ROWS__</table></div>
<footer>Read-only checks against the live Odoo site, the snapshot repo, and the
roadmap board. Regenerated each morning by scripts/morning_check.py.</footer>
</div>"""

page = (page.replace("__STAMP__", esc(stamp))
            .replace("__VERDICT__", esc(verdict))
            .replace("__NDEC__", str(len(decisions)))
            .replace("__PLURAL__", "" if len(decisions) == 1 else "s")
            .replace("__DECISIONS__", dec_html)
            .replace("__TILES__", tiles or '<p class="quiet">no numbers yet</p>')
            .replace("__PHASES__", phases or '<p class="quiet">board unreachable</p>')
            .replace("__ROWS__", rows))

os.makedirs(os.path.join(REPO, "reports"), exist_ok=True)
with open(os.path.join(REPO, "reports", "morning.html"), "w") as f:
    f.write(page)
with open(os.path.join(REPO, "reports", "morning.json"), "w") as f:
    json.dump({"checks": checks, "numbers": numbers, "decisions": decisions,
               "roadmap": roadmap, "stamp": stamp}, f, indent=1)
print("checks: %d pass / %d fail" % (ok_n, len(checks) - ok_n))
for c in checks:
    print("  %s %s | %s | %s" % ("PASS" if c["ok"] else "FAIL", c["area"], c["name"], c["detail"]))
print("decisions: %d" % len(decisions))
for d in decisions:
    print("  -", d["title"])
print("wrote reports/morning.html + morning.json")
