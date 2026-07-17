# -*- coding: utf-8 -*-
"""Build judgedice.com (Odoo website id=2) from the Judge Design System.
Dry-run validates XML. --apply performs writes in order; stops on first error."""
import sys, xml.etree.ElementTree as ET
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from odoo import connect

WID = 2  # judgedice.com

# ---------------------------------------------------------------- CSS / tokens
CUSTOM_HEAD = """<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="crossorigin"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,300;1,8..60,400;1,8..60,500&amp;display=swap"/>
<style>
:root{
--paper:#F2ECDF;--paper-raised:#F8F3E8;--paper-sunk:#EAE2D2;--ink:#1C1712;--ink-soft:#57514A;--ink-faint:#8B837A;--line:#D8CFBE;--line-strong:#C3B8A3;
--vermilion:#CB4127;--vermilion-deep:#A6321C;--vermilion-tint:#F0D8CF;--blue:#274654;--blue-deep:#1B333E;--blue-tint:#D3DDE0;--white:#FFFFFF;--black:#100C08;
--bg:var(--paper);--bg-raised:var(--paper-raised);--bg-hover:var(--paper-sunk);--text:var(--ink);--text-muted:var(--ink-soft);--text-faint:var(--ink-faint);--text-accent:var(--vermilion);--text-on-accent:var(--paper);--surface-card:var(--paper-raised);--border:var(--line);--border-strong:var(--line-strong);--accent:var(--vermilion);--accent-hover:var(--vermilion-deep);--accent-wash:var(--vermilion-tint);--link:var(--vermilion);--link-hover:var(--vermilion-deep);--focus-ring:var(--vermilion);
--font-display:'Anton','Arial Narrow',Impact,sans-serif;--font-serif:'Source Serif 4',Georgia,'Times New Roman',serif;--font-sans:var(--font-serif);
--text-hero:7.5rem;--text-display:4.5rem;--text-h1:3rem;--text-h2:2.25rem;--text-h3:1.625rem;--text-h4:1.25rem;--text-lead:1.5rem;--text-body:1.1875rem;--text-small:1rem;--text-label:0.8125rem;--text-meta:0.75rem;
--weight-light:300;--weight-regular:400;--weight-medium:500;--weight-semibold:600;--leading-tight:1.02;--leading-snug:1.15;--leading-body:1.62;--leading-label:1.3;--tracking-label:0.1em;--tracking-wide:0.02em;--tracking-display:-0.02em;--tracking-normal:0;
--space-1:0.25rem;--space-2:0.5rem;--space-3:0.75rem;--space-4:1rem;--space-5:1.5rem;--space-6:2rem;--space-7:3rem;--space-8:4rem;--space-9:6rem;--space-10:8rem;--space-11:12rem;--measure:38rem;--content-max:72rem;--page-gutter:clamp(1.5rem,6vw,6rem);--radius-none:0;--radius-sm:2px;--radius-md:4px;--radius-card:3px;--ease-out:cubic-bezier(0.22,0.61,0.36,1);--ease-in-out:cubic-bezier(0.65,0,0.35,1);--dur-fast:140ms;--dur-base:240ms;--dur-slow:520ms;
}
#wrapwrap{background:var(--paper);color:var(--ink);font-family:var(--font-serif);font-size:var(--text-body);line-height:var(--leading-body);}
#wrapwrap p{text-wrap:pretty;}
#wrapwrap ::selection{background:var(--vermilion-tint);color:var(--ink);}
header#top .jd-nav a{text-decoration:none;}
.jd-nav a .jd-underline{display:block;height:1px;background:var(--vermilion);width:0;transition:width var(--dur-base) var(--ease-out);}
.jd-nav a:hover .jd-underline{width:100%;}
.jd-footer a:hover{color:var(--vermilion);}
@keyframes reveal-up{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:none;}}
.reveal{opacity:0;animation:reveal-up var(--dur-slow) var(--ease-out) forwards;}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;animation:none;}}
</style>"""

# ---------------------------------------------------------------- style helpers
P_WORK = "font-family:var(--font-serif);font-size:clamp(1.0625rem,2vw,1.1875rem);line-height:1.62;color:var(--ink-soft);margin:0 0 1.1em;max-width:38rem;"
P_HOME = "font-family:var(--font-serif);font-size:clamp(1.125rem,2.2vw,1.3125rem);line-height:1.6;color:var(--ink-soft);margin:0 0 1.1em;max-width:40rem;"
SEC = "padding:clamp(4rem,10vw,8rem) clamp(1.5rem,6vw,6rem);border-top:1px solid var(--line);"
INNER = "max-width:72rem;margin:0 auto;"

def wrap(tname, title, body):
    return ('<t name="%s" t-name="%s">\n'
            '    <t t-call="website.layout">\n'
            '        <div id="wrap" class="oe_structure">\n%s\n'
            '        </div>\n    </t>\n</t>') % (title, tname, body)

def page_header(index, kicker, title, lead=None, ink=False):
    tcol = "var(--paper)" if ink else "var(--ink)"
    kcol = "color-mix(in srgb, var(--paper) 82%, transparent)" if ink else "var(--vermilion)"
    rcol = "color-mix(in srgb, var(--paper) 30%, transparent)" if ink else "var(--line)"
    lcol = "color-mix(in srgb, var(--paper) 80%, transparent)" if ink else "var(--ink-soft)"
    icol = kcol if ink else "var(--ink-faint)"
    hstyle = "padding:clamp(3.5rem,9vw,6.5rem) clamp(1.5rem,6vw,6rem) clamp(1.75rem,4vw,2.75rem);"
    if ink:
        hstyle += "background:var(--ink);"
    lead_html = ""
    if lead:
        lead_html = ('\n            <p style="font-family:var(--font-serif);font-style:italic;font-size:clamp(1.125rem,2.4vw,1.5rem);line-height:1.4;color:%s;margin:22px 0 0;max-width:40rem;">%s</p>' % (lcol, lead))
    return ('        <header style="%s">\n'
            '            <div style="display:flex;align-items:center;gap:14px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:%s;margin-bottom:20px;">\n'
            '                <span style="color:%s;font-weight:var(--weight-regular);">%s</span>\n'
            '                <span>%s</span>\n'
            '                <span style="flex:1;height:1px;background:%s;min-width:24px;"></span>\n'
            '            </div>\n'
            '            <h1 style="font-family:var(--font-display);font-weight:var(--weight-regular);text-transform:uppercase;font-size:clamp(2.75rem,8vw,6rem);line-height:var(--leading-tight);letter-spacing:-0.005em;color:%s;margin:0;max-width:18ch;">%s</h1>%s\n'
            '        </header>') % (hstyle, kcol, icol, index, kicker, rcol, tcol, title, lead_html)

def pager(prev=None, nxt=None):
    def end(item, is_next):
        align = "flex-end" if is_next else "flex-start"
        label = "Next" if is_next else "Previous"
        arrow = '<span style="color:var(--vermilion);">&#8594;</span>' if is_next else '<span style="color:var(--vermilion);">&#8592;</span>'
        inner = ("<span>%s</span>%s" % (item[1], arrow)) if is_next else ("%s<span>%s</span>" % (arrow, item[1]))
        return ('            <div><a href="%s" style="display:inline-flex;flex-direction:column;gap:8px;text-decoration:none;align-items:%s;">\n'
                '                <span style="font-family:var(--font-serif);font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);">%s</span>\n'
                '                <span style="display:inline-flex;align-items:baseline;gap:10px;font-family:var(--font-display);text-transform:uppercase;font-size:clamp(1.375rem,3vw,2rem);line-height:1.0;letter-spacing:-0.005em;color:var(--ink);">%s</span>\n'
                '            </a></div>') % (item[0], align, label, inner)
    left = end(prev, False) if prev else '            <div></div>'
    right = end(nxt, True) if nxt else '            <div></div>'
    return ('        <nav style="display:flex;justify-content:space-between;align-items:flex-start;gap:24px;padding:clamp(2rem,5vw,3rem) clamp(1.5rem,6vw,6rem);border-top:1px solid var(--line);">\n%s\n%s\n        </nav>') % (left, right)

def tag(text, emph):
    if emph:
        extra = "border:1px solid var(--accent-wash);color:var(--vermilion-deep);background:var(--accent-wash);"
    else:
        extra = "border:1px solid var(--line-strong);color:var(--ink-soft);background:transparent;"
    return ('<span style="display:inline-flex;align-items:center;font-family:var(--font-serif);font-size:var(--text-meta);letter-spacing:var(--tracking-wide);line-height:1;padding:6px 10px;border-radius:var(--radius-sm);%swhite-space:nowrap;">%s</span>' % (extra, text))

# ---------------------------------------------------------------- HERO (view 2034)
HERO_BODY = '''        <section id="top" style="min-height:calc(100vh - 66px);display:flex;flex-direction:column;justify-content:center;padding:0 clamp(1.5rem,6vw,6rem);max-width:78rem;">
            <div class="reveal" style="animation-delay:80ms;">
                <span style="font-family:var(--font-serif);font-size:13px;text-transform:uppercase;letter-spacing:0.14em;color:var(--vermilion);font-weight:500;">Judge &#8212; Digital Architect</span>
            </div>
            <h1 class="reveal" style="animation-delay:180ms;font-family:var(--font-display);font-weight:400;text-transform:uppercase;font-size:clamp(3rem,10vw,7.5rem);line-height:1.02;letter-spacing:-0.005em;color:var(--ink);margin:28px 0 0;max-width:15ch;">Delivering <em style="font-style:normal;color:var(--vermilion);">Joy</em> since the turn of the Century.</h1>
            <p class="reveal" style="animation-delay:320ms;font-family:var(--font-serif);font-size:13px;color:var(--ink-faint);letter-spacing:0.04em;margin-top:40px;text-transform:uppercase;">Work Life &#183; Home Life &#183; The Exciting Stuff &#183; Connect</p>
        </section>'''

# ---------------------------------------------------------------- WORK LIFE
WORK_BODY = (page_header("01", "Work Life", "Delivering joy, in production.",
             "Twenty-five years of digital architecture and marketing technology &#8212; mostly inside the Adobe Experience Cloud.")
+ '''
        <section style="%s">
            <div style="%s">
                <p style="font-family:var(--font-serif);font-size:clamp(1.375rem,3vw,1.75rem);line-height:1.4;color:var(--ink);margin:0 0 1.1em;">I've been building things on the internet since before it was cool. That sounds like a brag. <em style="font-style:italic;color:var(--vermilion-deep);">It's mostly just a fact.</em></p>
                <div style="height:clamp(1.5rem,4vw,2.5rem);"></div>
                <p style="%s">What started as Flash development at McKinsey became a 25-year career in digital architecture and marketing technology. I currently work at WillowTree, where I design and build enterprise systems for brands in financial services, real estate, hospitality, and media &#8212; mostly inside the Adobe Experience Cloud.</p>
                <p style="%s">My specialty is the space where strategy meets implementation. Where a roadmap stops being a slide and starts being a thing that works in production. I've done the architecture, run the workshops, led the demos, and when necessary jumped in to fix the integration the night before launch.</p>
                <p style="%s">I also teach Search Engine Marketing at the Chicago Portfolio School. I believe in passing things forward.</p>
                <div style="margin-top:clamp(2.5rem,6vw,4.5rem);display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:clamp(2rem,5vw,4rem);">
                    <div>
                        <div style="display:flex;align-items:center;gap:16px;"><span style="font-family:var(--font-serif);font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);white-space:nowrap;">Career arc</span><span style="flex:1;height:1px;background:var(--line);"></span></div>
                        <p style="font-family:var(--font-serif);font-size:13px;line-height:1.9;color:var(--ink-soft);margin-top:20px;letter-spacing:0.01em;">Flash developer at <b style="color:var(--ink);font-weight:500;">McKinsey &amp; Company</b><span style="color:var(--vermilion);"> &#8594; </span>founded <b style="color:var(--ink);font-weight:500;">The Flash Ministry</b><span style="color:var(--vermilion);"> &#8594; </span>partner at <b style="color:var(--ink);font-weight:500;">Pixelwelders</b><span style="color:var(--vermilion);"> &#8594; </span>Development Director at <b style="color:var(--ink);font-weight:500;">Vertical Inc.</b><span style="color:var(--vermilion);"> &#8594; </span>Lead Solutions Architect at <b style="color:var(--ink);font-weight:500;">Hanson Dodge</b><span style="color:var(--vermilion);"> &#8594; </span><b style="color:var(--ink);font-weight:500;">Velir</b><span style="color:var(--vermilion);"> &#8594; </span>Principal Solutions Architect at <b style="color:var(--ink);font-weight:500;">Maark</b>, acquired by <b style="color:var(--ink);font-weight:500;">WillowTree</b>.</p>
                    </div>
                    <div>
                        <div style="display:flex;align-items:center;gap:16px;"><span style="font-family:var(--font-serif);font-size:var(--text-meta);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-faint);white-space:nowrap;">What I work with</span><span style="flex:1;height:1px;background:var(--line);"></span></div>
                        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;">%s</div>
                    </div>
                </div>
            </div>
        </section>''' % (SEC, INNER, P_WORK, P_WORK, P_WORK,
            "".join([tag(t, i < 4) for i, t in enumerate([
                "Adobe Experience Manager", "Adobe Journey Optimizer", "Adobe Workfront",
                "Adobe Experience Platform", "Adobe Target", "Salesforce", "Smartsheet",
                "APIs &amp; the integrations nobody else wants to wire up"])])))

# ---------------------------------------------------------------- HOME LIFE
HOME_BODY = (page_header("02", "Home Life", "The exhale.",
             "When I'm not untangling enterprise tech stacks, I'm somewhere quieter &#8212; and usually still thinking about work.")
+ '''
        <section style="%sbackground:var(--paper-raised);">
            <div style="%s">
                <p style="font-family:var(--font-serif);font-size:clamp(1.375rem,3vw,1.75rem);line-height:1.42;color:var(--ink);margin:0 0 1.1em;max-width:26ch;">When I'm not untangling enterprise tech stacks, I'm probably driving someone to band practice, arguing about something mundane, or still thinking about work.</p>
                <div style="height:clamp(1.5rem,4vw,2.5rem);"></div>
                <p style="%s">I have a family that puts up with me. I've been in New England long enough to have opinions about winters.</p>
                <div style="margin:clamp(2rem,5vw,3rem) 0;max-width:40rem;">
                    <div style="border-left:2px solid var(--vermilion);padding-left:var(--space-5);margin:0;">
                        <p style="font-family:var(--font-serif);font-style:italic;font-size:var(--text-lead);line-height:1.45;color:var(--ink);margin:0;">I believe strongly in the power of a good lunch &#8212; there is no force stronger than the gravity of free lunch, and I will not be argued out of this.</p>
                    </div>
                </div>
                <p style="%s">I got into this work because I liked building things that didn't exist yet. That's still true. The tools have changed &#8212; <em style="font-style:italic;color:var(--ink);">Flash is dead, long live the API</em> &#8212; but the feeling of shipping something that works is the same.</p>
            </div>
        </section>''' % (SEC, INNER, P_HOME, P_HOME))

# ---------------------------------------------------------------- EXCITING STUFF
EX_ITEMS = [
    ("Marketing Technology Architecture", "Designing end-to-end digital marketing systems that hold together under real conditions &#8212; across strategy, platform selection, integration design, and build. The kind of architecture that doesn't collapse when a stakeholder changes their mind in month three."),
    ("Adobe Experience Cloud", "AEM, Adobe Journey Optimizer, Workfront, Target, AEP. I've shipped all of it, across industries and client contexts. I know which parts to use, which to skip, and which will require a ticket that becomes a different ticket. I have stories."),
    ("Marketing Operations &amp; Automation", "Building the workflows and integrations that let marketing teams actually use the platforms they've paid for. Approval flows that don't require a PhD. Automations that run without babysitting. The operational layer that makes the strategy real."),
    ("Workshop Facilitation", "I've run a lot of them. Discovery, architecture, stakeholder alignment. I know how to get a room full of people with competing priorities to walk out with decisions made and next steps owned. This is harder than it sounds."),
    ("Strategy &amp; Solutions Architecture", "The part before the build. What are we trying to do? What does the ecosystem need to look like? What do we build first and what do we defer? This is where 25 years of pattern-matching earns its keep."),
    ("Teaching &amp; Consulting", "Search Engine Marketing at the Chicago Portfolio School. Digital consulting for educational programs. If you're building a curriculum or a team, I can help."),
]
def ex_card(i, t, d):
    return ('                <div style="background:var(--surface-card);border:none;border-top:2px solid var(--ink);border-radius:0;padding:var(--space-6);">\n'
            '                    <div style="display:flex;align-items:baseline;gap:12px;"><span style="font-family:var(--font-serif);font-size:12px;color:var(--vermilion);">%02d</span><h3 style="font-family:var(--font-serif);font-size:clamp(1.375rem,2.4vw,1.625rem);font-weight:400;letter-spacing:-0.01em;line-height:1.15;margin:0;color:var(--ink);">%s</h3></div>\n'
            '                    <p style="font-family:var(--font-serif);font-size:1.0625rem;line-height:1.6;color:var(--ink-soft);margin:14px 0 0;">%s</p>\n'
            '                </div>') % (i + 1, t, d)
EX_BODY = (page_header("03", "The Exciting Stuff", "Here's what I actually do.",
           "In plain English &#8212; no icons, no three-word headlines with three bullets.")
+ '''
        <section style="%s">
            <div style="%s">
                <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:clamp(1rem,2vw,1.5rem);">
%s
                </div>
            </div>
        </section>''' % (SEC, INNER, "\n".join([ex_card(i, t, d) for i, (t, d) in enumerate(EX_ITEMS)])))

# ---------------------------------------------------------------- CONNECT
CONNECT_BODY = (page_header("04", "Connect", "Let's talk.", None, ink=True)
+ '''
        <section style="padding:clamp(2rem,6vw,5rem) clamp(1.5rem,6vw,6rem) clamp(4rem,10vw,8rem);background:var(--ink);">
            <div style="max-width:72rem;margin:0 auto;">
                <div style="max-width:44rem;">
                    <p style="font-family:var(--font-serif);font-size:clamp(1.125rem,2.4vw,1.5rem);line-height:1.5;color:color-mix(in srgb, var(--paper) 82%, transparent);margin:0;max-width:36rem;">I'm responsive on email, better on a call, and genuinely bad at LinkedIn DMs.</p>
                    <p style="font-family:var(--font-serif);font-size:clamp(1.0625rem,2vw,1.25rem);line-height:1.6;color:color-mix(in srgb, var(--paper) 66%, transparent);margin:20px 0 0;max-width:38rem;">If you're working on something in the Adobe Experience Cloud space and need a senior architect &#8212; or just need someone to talk through a hairy integration &#8212; I'm interested. Find 30 minutes.</p>
                    <div style="margin-top:clamp(2.5rem,6vw,3.5rem);display:flex;align-items:center;gap:28px;flex-wrap:wrap;">
                        <a href="mailto:judge@judgedice.com" style="display:inline-flex;align-items:center;gap:0.6em;font-family:var(--font-serif);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);line-height:1;border-radius:var(--radius-sm);border:1px solid var(--vermilion);background:var(--vermilion);color:var(--paper);padding:17px 34px;font-size:14px;text-decoration:none;">judge@judgedice.com <span style="font-family:var(--font-serif);">&#8594;</span></a>
                    </div>
                </div>
            </div>
        </section>''')

# ---------------------------------------------------------------- assemble pages
NAV = [("/work", "Work Life", "01"), ("/home", "Home Life", "02"),
       ("/exciting", "The Exciting Stuff", "03"), ("/connect", "Connect", "04")]

PAGES = {
    2034: ("website.homepage", "Homepage",
           HERO_BODY + "\n" + pager(nxt=("/work", "Work Life"))),
}
NEW_PAGES = [
    ("website.judge_work", "Work Life", "/work",
     WORK_BODY + "\n" + pager(("/", "Home"), ("/home", "Home Life"))),
    ("website.judge_home", "Home Life", "/home",
     HOME_BODY + "\n" + pager(("/work", "Work Life"), ("/exciting", "The Exciting Stuff"))),
    ("website.judge_exciting", "The Exciting Stuff", "/exciting",
     EX_BODY + "\n" + pager(("/home", "Home Life"), ("/connect", "Connect"))),
    ("website.judge_connect", "Connect", "/connect",
     CONNECT_BODY + "\n" + pager(("/exciting", "The Exciting Stuff"), None)),
]

# ---------------------------------------------------------------- header (2035)
def navitem(href, index, label):
    return ('<a href="%s" style="display:inline-flex;flex-direction:column;gap:5px;font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);font-weight:var(--weight-medium);color:var(--ink);text-decoration:none;"><span style="display:inline-flex;align-items:baseline;gap:7px;"><span style="color:var(--vermilion);font-size:var(--text-meta);font-weight:var(--weight-regular);">%s</span><span>%s</span></span><span class="jd-underline"></span></a>' % (href, index, label))

HEADER_ARCH = ('<data inherit_id="website.layout" name="Template Header Default" active="True">\n'
    '    <xpath expr="//header//nav" position="replace">\n'
    '        <nav class="jd-nav d-none d-lg-flex" style="align-items:center;justify-content:space-between;width:100%%;padding:20px clamp(1.5rem,6vw,6rem);background:color-mix(in srgb, var(--paper) 88%%, transparent);border-bottom:1px solid var(--line);">\n'
    '            <a href="/" style="font-family:var(--font-serif);font-size:26px;color:var(--ink);text-decoration:none;letter-spacing:-0.01em;">Judge<span style="color:var(--vermilion);">.</span></a>\n'
    '            <span style="display:inline-flex;gap:clamp(18px,3vw,40px);flex-wrap:wrap;align-items:center;">%s</span>\n'
    '        </nav>\n'
    '        <t t-call="website.template_header_mobile"/>\n'
    '    </xpath>\n'
    '</data>') % "".join([navitem(h, idx, lbl) for (h, lbl, idx) in NAV])

# ---------------------------------------------------------------- footer (2038)
def footlink(href, label):
    return ('<a href="%s" style="font-family:var(--font-serif);font-size:var(--text-label);text-transform:uppercase;letter-spacing:var(--tracking-label);color:var(--ink-soft);text-decoration:none;">%s</a>' % (href, label))

FOOTER_ARCH = ('<data inherit_id="website.layout" name="Default" active="True">\n'
    '    <xpath expr="//div[@id=\'footer\']" position="replace">\n'
    '        <div id="footer" class="oe_structure oe_structure_solo" t-ignore="true" t-if="not no_footer">\n'
    '            <section class="s_text_block jd-footer" data-snippet="s_text_block" data-name="Footer">\n'
    '                <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:18px 40px;padding:32px clamp(1.5rem,6vw,6rem);border-top:1px solid var(--line);background:var(--paper);">\n'
    '                    <a href="/" style="font-family:var(--font-serif);font-size:18px;color:var(--ink);text-decoration:none;letter-spacing:-0.01em;">Judge<span style="color:var(--vermilion);">.</span></a>\n'
    '                    <span style="display:flex;flex-wrap:wrap;gap:10px 24px;">%s</span>\n'
    '                    <span style="font-family:var(--font-serif);font-size:var(--text-meta);color:var(--ink-faint);letter-spacing:var(--tracking-wide);text-transform:uppercase;">Delivering Joy since the turn of the Century</span>\n'
    '                </div>\n'
    '            </section>\n'
    '        </div>\n'
    '    </xpath>\n'
    '</data>') % "".join([footlink(h, lbl) for (h, lbl, idx) in NAV])

# ---------------------------------------------------------------- validate
def validate():
    ok = True
    checks = [("HERO/home arch", wrap("website.homepage", "Homepage", PAGES[2034][2]))]
    for key, name, url, body in NEW_PAGES:
        checks.append((name, wrap(key, name, body)))
    checks.append(("header 2035", HEADER_ARCH))
    checks.append(("footer 2038", FOOTER_ARCH))
    for label, arch in checks:
        try:
            ET.fromstring(arch)
            print("  XML OK  %-22s (%d chars)" % (label, len(arch)))
        except ET.ParseError as e:
            ok = False
            print("  XML FAIL %-22s -> %s" % (label, e))
    print("custom_code_head: %d chars (not XML-validated; raw head injection)" % len(CUSTOM_HEAD))
    return ok

# ---------------------------------------------------------------- apply
def apply():
    uid, call = connect()
    print("connected uid=%s\n" % uid)

    # 1. CANARY + tokens: write custom_code_head (first write => access-gate test)
    try:
        call("website", "write", [WID], {"custom_code_head": CUSTOM_HEAD})
        print("[1] website %d custom_code_head set (fonts+tokens+reveal) — %d chars" % (WID, len(CUSTOM_HEAD)))
    except Exception as e:
        print("STOP: first write failed — likely API writes are gated by the plan.\n%s" % e)
        sys.exit(2)

    # 2. Homepage hero (view 2034) + unpublish homepage page (id 5) for preview
    arch = wrap("website.homepage", "Homepage", PAGES[2034][2])
    call("ir.ui.view", "write", [2034], {"arch": arch})
    call("website.page", "write", [5], {"is_published": False})
    print("[2] view 2034 Home -> Hero written; page 5 set unpublished")

    # 3-6. new pages (view + website.page, unpublished)
    created = []
    for key, name, url, body in NEW_PAGES:
        arch = wrap(key, name, body)
        vid = call("ir.ui.view", "create", {
            "name": name, "type": "qweb", "key": key,
            "website_id": WID, "arch": arch})
        pid = call("website.page", "create", {
            "name": name, "url": url, "view_id": vid,
            "website_id": WID, "is_published": False})
        created.append((name, url, vid, pid))
        print("[+] %-18s url=%-10s view=%s page=%s (unpublished)" % (name, url, vid, pid))

    # 7. header (view 2035)
    call("ir.ui.view", "write", [2035], {"arch": HEADER_ARCH})
    print("[7] view 2035 header -> editorial nav (Judge. + 01-04)")

    # 8. footer (view 2038)
    call("ir.ui.view", "write", [2038], {"arch": FOOTER_ARCH})
    print("[8] view 2038 footer -> editorial footer")

    # 9. menu: update 8/9, create Exciting + Connect
    call("website.menu", "write", [8], {"name": "Work Life", "url": "/work", "sequence": 10})
    call("website.menu", "write", [9], {"name": "Home Life", "url": "/home", "sequence": 20})
    m3 = call("website.menu", "create", {"name": "The Exciting Stuff", "url": "/exciting", "parent_id": 7, "sequence": 30, "website_id": WID})
    m4 = call("website.menu", "create", {"name": "Connect", "url": "/connect", "parent_id": 7, "sequence": 40, "website_id": WID})
    print("[9] menu updated: Work Life, Home Life, Exciting(%s), Connect(%s)" % (m3, m4))

    print("\nDONE. Pages are UNPUBLISHED — visible to you as admin for preview.")

if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        print("DRY RUN — validating XML only, no writes.\n")
        validate()
