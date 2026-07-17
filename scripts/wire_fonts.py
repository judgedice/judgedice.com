# -*- coding: utf-8 -*-
import sys, base64, urllib.request, ssl, re, time
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect
ATT=1087; HOME="https://www.judgedice.com/"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
REPL=[("    'font': null,","    'font': 'Source Serif 4',"),
      ("    'headings-font': null,","    'headings-font': 'Anton',"),
      ("    'navbar-font': null,","    'navbar-font': 'Source Serif 4',"),
      ("    'buttons-font': null,","    'buttons-font': 'Source Serif 4',")]
GF="    'google-fonts': ('Anton', 'Source Serif 4'),\n"; MARK="    // -- hook --"
def fetch(u):
    r=urllib.request.Request(u,headers={"User-Agent":"curl"})
    with urllib.request.urlopen(r,context=ctx,timeout=40) as x: return x.getcode(),x.read().decode("utf-8","ignore")
def bundle_href(html):
    m=re.search(r'href="([^"]*web\.assets_frontend[^"]*\.css)"',html); 
    if not m: return None
    u=m.group(1); return ("https://www.judgedice.com"+u) if u.startswith("/") else u
uid,call=connect()
att=call("ir.attachment","read",[ATT],["website_id","datas"])[0]
assert att["website_id"][0]==2
orig=att["datas"]; cur=base64.b64decode(orig).decode()
_,h0=fetch(HOME); old_href=bundle_href(h0); print("[pre] old bundle:", old_href)
if "'font': 'Source Serif 4'" in cur: print("already set"); sys.exit(0)
new=cur
for o,r in REPL:
    assert new.count(o)==1,o; new=new.replace(o,r)
new=new.replace(MARK,GF+MARK,1)
call("ir.attachment","write",[ATT],{"datas":base64.b64encode(new.encode()).decode()})
print("[write] applied.")
ok=False; last=""
for i in range(8):
    time.sleep(4)
    try:
        _,h=fetch(HOME); href=bundle_href(h)
        cc,css=fetch(href) if href else (0,"")
        changed = href and href!=old_href
        hasfont = ("Source Serif 4" in css) or ("Anton" in css) or ("Source+Serif" in css) or ("family=Anton" in css)
        last="try%d href=%s changed=%s css=%s len=%d font=%s"%(i,href.split('/')[-2] if href else None,changed,cc,len(css),hasfont)
        print("  ",last)
        if changed and cc==200 and len(css)>2000:
            ok=True
            # show how the font is emitted
            for pat in ("font-family:[^;{}]*Serif[^;{}]*","@import[^;]*Anton[^;\"']*","--o-theme-font[^;]*","Source Serif 4"):
                mm=re.search(pat,css)
                if mm: print("     emit:",mm.group(0)[:120])
            break
    except Exception as e:
        last="try%d err %s"%(i,e); print("  ",last)
if not ok:
    call("ir.attachment","write",[ATT],{"datas":orig})
    print("[REVERTED] no fresh healthy bundle after retries:",last); sys.exit(2)
print("[ok] fonts wired; fresh bundle compiled. keeping change.")
