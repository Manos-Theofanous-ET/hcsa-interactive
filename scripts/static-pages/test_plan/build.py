# -*- coding: utf-8 -*-
"""Build the HCSA physical test plan.

Outputs
  site     public/tests/index.html (team side of hcsa-site, self-hosted fonts, site nav)
  artifact out/index.html          (Google Fonts, no site nav) for the claude.ai artifact
  md       out/HCSA_physical_test_plan_14Nov2026.md (Drive and Project text copy)
  pdf      out/HCSA_physical_test_plan_14Nov2026.pdf (headless Chrome, still frames)

Run: python3 build.py [all|site|artifact|md|pdf]
"""
import html, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import data as D

SITE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
STAMP = "14Nov2026"
ANIM = open(os.path.join(HERE, "anim.js"), encoding="utf-8").read()


def e(s):
    return html.escape(str(s), quote=True)


def money(v):
    if v is None:
        return "&ndash;"
    return "$" + format(int(round(v)), ",")


def money_md(v):
    return "-" if v is None else "$" + format(int(round(v)), ",")


def sums(parts):
    need = sum(p[4] or 0 for p in parts if p[3] == "buy")
    pend = sum(p[4] or 0 for p in parts if p[3] == "quote")
    have = sum(p[4] or 0 for p in parts if p[3] in ("have",))
    loan = sum(p[4] or 0 for p in parts if p[3] in ("agreed", "offered"))
    later = sum(p[4] or 0 for p in parts if p[3] == "later")
    np_ = sum(1 for p in parts if p[3] == "notpriced")
    return dict(need=need, pend=pend, have=have, loan=loan, later=later, notpriced=np_)


FONTS_SITE = """@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Inter";src:url(/fonts/inter-latin-wght-normal.woff2) format("woff2-variations"),url(/fonts/inter-latin-wght-normal.woff2) format("woff2");font-weight:100 900;font-display:swap}
@font-face{font-family:"Space Mono";src:url(/fonts/space-mono-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}"""

FONTS_ART = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;600&family=Inter:wght@400;500;600&family=Space+Mono&display=swap" rel="stylesheet">')

CSS = r"""
:root{
/* layout: one long reading column; each test is a block with its animation on top, then the facts in two columns, then parts and readiness */
--bg:#0a0b0d;--bg2:#121419;--bg3:#191c22;--ink:#f1efea;--ink2:rgba(241,239,234,.80);--ink3:rgba(241,239,234,.58);
--line:rgba(255,255,255,.13);--accent:#c9b48f;
--ok:#79c48f;--loan:#7fb6dd;--pend:#e6b75c;--buy:#ef7d6b;--muted:rgba(241,239,234,.5);
--serif:"Fraunces",ui-serif,Georgia,serif;--sans:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;--mono:"Space Mono",ui-monospace,Menlo,Consolas,monospace;
color-scheme:dark}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--accent)}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.sitenav{position:sticky;top:0;z-index:20;background:rgba(0,0,0,.86);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.sitenav .in{max-width:1120px;margin:0 auto;padding:0 20px;display:flex;align-items:center;gap:22px;height:56px;overflow-x:auto;white-space:nowrap}
.sitenav a{font-size:14.5px;font-weight:500;color:var(--ink3);text-decoration:none}
.sitenav a.brand{color:var(--ink);font-weight:600;letter-spacing:.06em;margin-right:auto}
.sitenav a[aria-current]{color:var(--ink)}
header.top{padding:56px 0 28px;border-bottom:1px solid var(--line)}
.eyebrow{font-size:14px;font-weight:500;color:var(--accent);margin:0 0 12px}
h1,h2{font-family:var(--serif);font-weight:400;text-wrap:balance;margin:0}
h1{font-size:clamp(2.1rem,5vw,3.4rem);line-height:1.08;margin-bottom:16px}
h2{font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.15}
h3{font-size:15px;font-weight:600;letter-spacing:.02em;color:var(--accent);margin:0 0 8px;text-transform:none}
h4{font-size:15px;font-weight:600;margin:0 0 8px}
.lead{font-family:var(--serif);font-size:1.2rem;color:var(--ink2);max-width:780px;margin:0}
.base{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:0 28px;margin:26px 0 0;padding:0;list-style:none}
.base li{border-top:1px solid var(--line);padding:9px 0 10px;font-size:14.5px;color:var(--ink2)}
.base b{color:var(--ink);font-weight:600;margin-right:6px}
nav.toc{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}
nav.toc a{font-size:14px;text-decoration:none;color:var(--ink);border:1px solid var(--line);padding:6px 11px;background:var(--bg2)}
nav.toc a:hover,nav.toc a:focus-visible{border-color:var(--accent)}
section{padding:44px 0;border-bottom:1px solid var(--line)}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:22px 0}
.tile{background:var(--bg2);border:1px solid var(--line);padding:14px 16px}
.tile .v{font-family:var(--mono);font-size:24px;color:var(--ink);display:block}
.tile .k{font-size:13.5px;color:var(--ink3)}
.tile.buy{border-left:3px solid var(--buy)}.tile.ok{border-left:3px solid var(--ok)}.tile.loan{border-left:3px solid var(--loan)}.tile.pend{border-left:3px solid var(--pend)}.tile.muted{border-left:3px solid var(--muted)}
.tw{overflow-x:auto;margin:12px 0}
table{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}
th,td{text-align:left;vertical-align:top;padding:9px 10px 9px 0;border-top:1px solid var(--line)}
th{font-size:13px;font-weight:600;color:var(--ink3);white-space:nowrap}
td.r,th.r{text-align:right;padding-right:14px;white-space:nowrap}
td.note{color:var(--ink3);font-size:13.5px;min-width:220px}
tfoot td{font-weight:600;color:var(--ink)}
.chip{display:inline-block;font-size:12.5px;font-weight:500;padding:2px 8px;border:1px solid currentColor;white-space:nowrap;line-height:1.5}
.chip.ok{color:var(--ok)}.chip.loan{color:var(--loan)}.chip.pend{color:var(--pend)}.chip.buy{color:var(--buy)}.chip.muted{color:var(--muted)}
.test .head{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 16px;margin-bottom:6px}
.code{font-family:var(--mono);font-size:15px;color:var(--bg);background:var(--accent);padding:2px 9px}
.when{color:var(--ink2);margin:4px 0 18px;font-size:15px}
figure.anim{margin:0 0 26px;background:#0d1014;border:1px solid var(--line)}
figure.anim canvas{display:block;width:100%;height:auto;aspect-ratio:960/460}
.prog{height:3px;background:rgba(255,255,255,.06)}.prog i{display:block;height:3px;width:0;background:var(--accent)}
.ctrl{display:flex;flex-wrap:wrap;gap:8px;padding:10px 12px 0}
.ctrl button,.steps button{font:500 13.5px var(--sans);color:var(--ink);background:var(--bg3);border:1px solid var(--line);padding:6px 11px;cursor:pointer}
.ctrl button:hover,.steps button:hover{border-color:var(--accent)}
button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.steps{display:flex;flex-wrap:wrap;gap:6px;padding:8px 12px 0}
.steps button{font-size:12.5px;color:var(--ink3);padding:4px 9px}
.steps button.on{color:var(--bg);background:var(--accent);border-color:var(--accent)}
figure.anim:not(.live) .ctrl,figure.anim:not(.live) .steps,figure.anim:not(.live) .prog{display:none}
figcaption{padding:10px 14px 14px;font-size:14.5px;color:var(--ink2);min-height:3.6em}
figcaption b{color:var(--ink);font-weight:600}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px 36px}
.facts ul,.facts ol{margin:0;padding-left:20px}
.facts li{margin:0 0 6px;color:var(--ink2);font-size:15px;max-width:70ch}
.ready{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:18px}
.ready>div{background:var(--bg2);border:1px solid var(--line);padding:14px 16px}
.ready ul{list-style:none;margin:0;padding:0}
.ready li{padding:5px 0 5px 24px;position:relative;font-size:14.5px;color:var(--ink2);border-top:1px solid var(--line)}
.ready li:first-child{border-top:0}
.ready .have li::before{content:"\2713";position:absolute;left:2px;color:var(--ok);font-weight:700}
.ready .need li::before{content:"\25CB";position:absolute;left:2px;color:var(--buy)}
.ready .have{border-left:3px solid var(--ok)}.ready .need{border-left:3px solid var(--buy)}
.sum td:first-child{white-space:nowrap}
.small{font-size:13.5px;color:var(--ink3)}
.rules{margin:0;padding-left:20px}.rules li{margin-bottom:6px;color:var(--ink2);max-width:80ch}
.cols2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px 36px}
dl.kv{margin:0}dl.kv dt{font-weight:600;color:var(--ink);font-size:14.5px;margin-top:10px}dl.kv dd{margin:2px 0 0;color:var(--ink2);font-size:14.5px}
footer{padding:30px 0 60px;color:var(--ink3);font-size:13.5px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{
:root{--bg:#fff;--bg2:#f4f4f2;--bg3:#eee;--ink:#111;--ink2:#222;--ink3:#555;--line:#ccc;--accent:#7a5f2c;color-scheme:light}
.sitenav,.ctrl,.steps,.prog,nav.toc{display:none!important}
body{font-size:11pt}
section{padding:18px 0;page-break-inside:auto}
figure.anim{break-inside:avoid;border:1px solid #999;background:#fff}figure.anim canvas{background:#0d1014}figcaption{background:#fff;color:#222}
.test{break-before:page}
.ready>div,.tile{background:#fff}
a{color:#111}
@page{size:Letter;margin:14mm 13mm}
.wrap{max-width:none;padding:0}
.facts,.ready,.cols2,.base{display:block}
.facts>div,.ready>div{margin-bottom:12px;break-inside:avoid}
.tw{overflow:visible}
table{font-size:8.5pt}
td.note{min-width:0}
.tiles{grid-template-columns:repeat(3,1fr)}
h1{font-size:26pt}h2{font-size:17pt}
}
"""

NAV = ('<nav class="sitenav" aria-label="Site"><div class="in"><a href="/team/" class="brand">HCSA team</a><a href="/plan/">The plan</a>'
       '<a href="/blueprints/">Blueprints</a><a href="/tests/" aria-current="page">The tests</a><a href="/#work">Our work</a><a href="/#sponsor">Sponsor</a></div></nav>')


def li(items):
    return "".join("<li>%s</li>" % e(x) for x in items)


def chip(k):
    lab, cls = D.STATUS[k]
    return '<span class="chip %s">%s</span>' % (cls, e(lab))


def anim_fig(t):
    return ('<figure class="anim" data-scene="%s"><canvas role="img" aria-label="Animation of the %s test. %s"></canvas>'
            '<div class="prog"><i></i></div><div class="ctrl"><button type="button" class="play" aria-pressed="false">Play</button>'
            '<button type="button" class="restart">Restart</button></div><div class="steps" aria-label="Steps"></div>'
            '<figcaption><b class="ph-title"></b> <span class="ph-text">%s</span></figcaption></figure>'
            % (t["id"], e(t["code"]), e(t["anim_caption"]), e(t["anim_caption"])))


def parts_table(t):
    rows = []
    for name, qty, who, st, price, note in t["parts"]:
        pr = money(price) if st not in ("counted",) else "&ndash;"
        if st in ("agreed", "offered", "have") and price:
            pr = '<span class="small">value</span> ' + money(price)
        elif st in ("agreed", "offered", "have"):
            pr = "&ndash;"
        rows.append('<tr><td>%s</td><td class="num">%s</td><td>%s</td><td>%s</td><td class="r num">%s</td><td class="note">%s</td></tr>'
                    % (e(name), e(qty), e(who), chip(st), pr, e(note)))
    s = sums(t["parts"])
    foot = []
    if s["need"]:
        foot.append("Need to buy %s" % money(s["need"]))
    if s["later"]:
        foot.append("Estimate, later %s" % money(s["later"]))
    if s["pend"]:
        foot.append("Quote pending %s" % money(s["pend"]))
    if s["notpriced"]:
        foot.append("%d line%s not priced yet" % (s["notpriced"], "s" if s["notpriced"] > 1 else ""))
    return ('<div class="tw"><table><thead><tr><th>Part</th><th>Qty</th><th>Who provides it</th><th>Status</th><th class="r">Price</th><th>Notes</th></tr></thead>'
            '<tbody>%s</tbody><tfoot><tr><td colspan="6">%s</td></tr></tfoot></table></div>' % ("".join(rows), " &middot; ".join(foot)))


def test_section(t):
    return ('<section class="test" id="%s"><div class="wrap">'
            '<div class="head"><span class="code">%s</span><h2>%s</h2><span class="chip %s">%s</span></div>'
            '<p class="when"><b>When:</b> %s</p>%s'
            '<div class="facts">'
            '<div><h3>What it tests</h3><ul>%s</ul></div>'
            '<div><h3>How we test it</h3><ol>%s</ol></div>'
            '<div><h3>What we record</h3><ul>%s</ul></div>'
            '<div><h3>What it tells us</h3><ul>%s</ul></div>'
            '<div><h3>Why we do it this way</h3><ul>%s</ul></div>'
            '<div><h3>It passes when</h3><ul>%s</ul></div>'
            '</div>'
            '<h3 style="margin-top:28px">Parts, who provides them, and the price</h3>%s'
            '<div class="ready"><div class="have"><h4>We have</h4><ul>%s</ul></div>'
            '<div class="need"><h4>Still needed before it can run</h4><ul>%s</ul></div></div>'
            '</div></section>'
            % (t["id"], e(t["code"]), e(t["name"]), t["state_cls"], e(t["state"]), e(t["when"]), anim_fig(t),
               li(t["what"]), li(t["how"]), li(t["record"]), li(t["tells"]), li(t["why"]), li(t["passes"]),
               parts_table(t), li(t["have"]), li(t["need"])))


def proposed_section(p):
    return ('<div class="prop" id="%s"><div class="head"><span class="code">%s</span><h2>%s</h2><span class="chip muted">%s</span></div>'
            '<p class="when"><b>When:</b> %s</p>%s<div class="facts">'
            '<div><h3>What it tests</h3><ul>%s</ul></div><div><h3>How</h3><ul>%s</ul></div>'
            '<div><h3>What we record</h3><ul>%s</ul></div><div><h3>What it tells us</h3><ul>%s</ul></div>'
            '<div><h3>Why this way</h3><ul>%s</ul></div><div><h3>What it needs</h3><ul><li>%s</li></ul></div></div></div>'
            % (p["id"], e(p["code"]), e(p["name"]), e(p["state"]), e(p["when"]), anim_fig(p),
               li(p["what"]), li(p["how"]), li(p["record"]), li(p["tells"]), li(p["why"]), e(p["needs"])))


def totals():
    tot = dict(need=0, pend=0, have=0, later=0, notpriced=0)
    per = []
    for t in D.TESTS:
        s = sums(t["parts"]); per.append((t, s))
        for k in tot:
            tot[k] += s[k]
    return tot, per


def summary_section():
    tot, per = totals()
    rows = []
    for t, s in per:
        n_need = len(t["need"])
        rows.append('<tr><td><a href="#%s"><span class="num">%s</span></a></td><td>%s</td><td>%s</td><td><span class="chip %s">%s</span></td>'
                    '<td class="r num">%s</td><td class="r num">%s</td><td><span class="chip buy">No</span> %d thing%s still needed</td></tr>'
                    % (t["id"], e(t["code"]), e(t["name"]), e(t["when"]), t["state_cls"], e(t["state"]),
                       money(s["need"] or s["later"]) + ("" if s["need"] else " later"), str(s["notpriced"]), n_need, "" if n_need == 1 else "s"))
    tiles = ('<div class="tiles">'
             '<div class="tile buy"><span class="v">%s</span><span class="k">to buy for T0, T1, SA-550 and T2 (unfunded today)</span></div>'
             '<div class="tile muted"><span class="v">%s</span><span class="k">T3 corner estimate, not needed before late 2027</span></div>'
             '<div class="tile pend"><span class="v">%d</span><span class="k">lines with no price yet, mostly parts added since October</span></div>'
             '<div class="tile ok"><span class="v">$500</span><span class="k">SendCutSend credit in hand (11 Nov), unused</span></div>'
             '<div class="tile loan"><span class="v">$4,076</span><span class="k">value of the Dewesoft recorder on loan (agreed, one unit for every test)</span></div>'
             '</div>' % (money(tot["need"]), money(tot["later"]), tot["notpriced"]))
    return ('<section id="summary"><div class="wrap"><h2>The tests at a glance</h2>'
            '<p class="small" style="margin-top:8px">Budget today: $0. Prices are the 10 November budget sheet, mostly 5 October list estimates; the machining lines were made for 140 mm frames and will rise for the 180 mm Rev F frames.</p>'
            + tiles +
            '<div class="tw"><table class="sum"><thead><tr><th>Test</th><th>What</th><th>When</th><th>State</th><th class="r">To buy</th><th class="r">Not priced</th><th>Ready to test?</th></tr></thead><tbody>%s</tbody></table></div>'
            '<p class="small">No test is ready yet. The last column counts what still has to happen before each test can run; the section on each test lists it, next to what we already have.</p>'
            '</div></section>' % "".join(rows))


def fab_section():
    rows = "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td class="note">%s</td></tr>' % tuple(e(x) for x in f) for f in D.FAB)
    base = "".join("<li><b>%s</b>%s</li>" % (e(k), e(v)) for k, v in D.BASELINE)
    return ('<section id="fab"><div class="wrap"><h2>What has to be made, and who makes it</h2>'
            '<div class="tw"><table><thead><tr><th>Who</th><th>What</th><th>For</th><th>Where it stands</th></tr></thead><tbody>%s</tbody></table></div>'
            '<h3 style="margin-top:26px">The rules we work by</h3><ol class="rules">%s</ol>'
            '</div></section>' % (rows, li(D.RULES)))


def page(variant):
    fonts = ("<style>%s</style>" % FONTS_SITE) if variant == "site" else FONTS_ART
    nav = NAV if variant == "site" else ""
    tests = "".join(test_section(t) for t in D.TESTS)
    props = "".join(proposed_section(p) for p in D.PROPOSED)
    toc = "".join('<a href="#%s">%s</a>' % (t["id"], e(t["code"] + " " + t["name"].split(",")[0].split(":")[0])) for t in D.TESTS)
    toc += '<a href="#proposed">Proposed tests</a><a href="#new">New since 10 Nov</a>'
    base = "".join("<li><b>%s</b>%s</li>" % (e(k), e(v)) for k, v in D.BASELINE)
    new = "".join("<dt>%s</dt><dd>%s</dd>" % (e(k), e(v)) for k, v in D.NEW_SINCE)
    dates = "".join('<tr><td class="num" style="white-space:nowrap">%s</td><td>%s</td></tr>' % (e(a), e(b)) for a, b in D.DATES)
    fund = "".join("<dt>%s</dt><dd>%s</dd>" % (e(a), e(b)) for a, b in D.FUNDING)
    src = li(D.SOURCES)
    old = ('<p class="small">The October test film (Rev S, out of date) is kept at <a href="/tests/film-oct/">/tests/film-oct/</a>.</p>'
           if variant == "site" else '<p class="small">This page is also on the team side of the site, at hcsa-site.vercel.app/tests/.</p>')
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark"><title>HCSA physical test plan</title>
<meta name="description" content="Every physical test HCSA plans at Rev F: what it tests, how, what it records and tells us, what has to be made, what we have, who provides each piece and the price, with an animation of each test.">
{('<link rel="icon" type="image/svg+xml" href="/favicon.svg">' if variant == 'site' else '')}
{fonts}<style>{CSS}</style></head>
<body>{nav}
<header class="top"><div class="wrap">
<p class="eyebrow">Rev F &middot; {e(D.DATE)}</p>
<h1>The physical tests</h1>
<p class="lead">What we plan to test, how each test runs, what it records and what it tells us, what has to be made, what we already have, who provides each piece and what it costs. No physical test has run yet: every predicted number on this page comes from a model.</p>
<ul class="base">{base}</ul>
<nav class="toc" aria-label="Tests">{toc}</nav>
</div></header>
{summary_section()}
{fab_section()}
{tests}
<section id="proposed"><div class="wrap"><h2 style="margin-bottom:6px">Proposed, not yet in the plan</h2>
<p class="small" style="margin-bottom:22px">Two tests have come up since October. Neither has a parts list or a price yet.</p>{props}</div></section>
<section id="new"><div class="wrap"><div class="cols2">
<div><h2 style="margin-bottom:10px">New since the 10 November budget sheet</h2><dl class="kv">{new}</dl></div>
<div><h2 style="margin-bottom:10px">The next dates</h2><div class="tw"><table><tbody>{dates}</tbody></table></div>
<h2 style="margin:26px 0 10px">Where the money could come from</h2><dl class="kv">{fund}</dl></div>
</div></div></section>
<footer><div class="wrap"><p><b>Sources.</b></p><ul>{src}</ul>
<p>Animations are schematic. Rev F dimensions are used where the drawings give them; gaps and deflections are drawn far larger than life, and bars and plots show the shape of a reading, not data. Written {e(D.DATE)} for the HCSA team.</p>{old}</div></footer>
<script>{ANIM}</script>
</body></html>
"""


def markdown():
    out = ["# HCSA physical test plan (%s)" % D.DATE, "",
           "What we plan to test at Rev F, how each test runs, what it records and tells us, what has to be made, what we already have, who provides each piece and what it costs. No physical test has run yet: every predicted number comes from a model. The interactive version with an animation of each test is on the team site at hcsa-site.vercel.app/tests/.", "",
           "## The baseline the tests check", ""]
    out += ["- **%s:** %s" % kv for kv in D.BASELINE]
    tot, per = totals()
    out += ["", "## At a glance", "",
            "Budget today: $0. To buy for T0, T1, SA-550 and T2: %s (unfunded). T3 corner estimate, later: %s. %d lines not priced yet. SendCutSend credit in hand: $500. Dewesoft recorder on loan (agreed): value $4,076." % (money_md(tot["need"]), money_md(tot["later"]), tot["notpriced"]), "",
            "| Test | When | State | To buy | Not priced | Ready to test? |", "| --- | --- | --- | --- | --- | --- |"]
    for t, s in per:
        out.append("| %s %s | %s | %s | %s | %d | No: %d things still needed |" % (t["code"], t["name"], t["when"], t["state"], money_md(s["need"] or s["later"]), s["notpriced"], len(t["need"])))
    out += ["", "## What has to be made, and who makes it", "", "| Who | What | For | Where it stands |", "| --- | --- | --- | --- |"]
    out += ["| %s | %s | %s | %s |" % f for f in D.FAB]
    out += ["", "## The rules we work by", ""] + ["%d. %s" % (i + 1, r) for i, r in enumerate(D.RULES)]
    for t in D.TESTS:
        out += ["", "## %s. %s" % (t["code"], t["name"]), "", "**When:** %s. **State:** %s." % (t["when"], t["state"]), "",
                "*Animation:* %s" % t["anim_caption"], ""]
        for title, key in (("What it tests", "what"), ("How we test it", "how"), ("What we record", "record"),
                           ("What it tells us", "tells"), ("Why we do it this way", "why"), ("It passes when", "passes")):
            out += ["### " + title, ""] + ["- " + x for x in t[key]] + [""]
        out += ["### Parts, who provides them, and the price", "", "| Part | Qty | Who provides it | Status | Price | Notes |", "| --- | --- | --- | --- | --- | --- |"]
        for name, qty, who, st, price, note in t["parts"]:
            pr = "-" if st == "counted" else money_md(price)
            if st in ("agreed", "offered", "have") and price:
                pr = "value " + pr
            elif st in ("agreed", "offered", "have"):
                pr = "-"
            out.append("| %s | %s | %s | %s | %s | %s |" % (name, qty, who, D.STATUS[st][0], pr, note))
        s = sums(t["parts"])
        out += ["", "Need to buy %s; quote pending %s; %d line%s not priced." % (money_md(s["need"]), money_md(s["pend"]), s["notpriced"], "" if s["notpriced"] == 1 else "s"), "",
                "### We have", ""] + ["- " + x for x in t["have"]] + ["", "### Still needed before it can run", ""] + ["- " + x for x in t["need"]]
    out += ["", "## Proposed, not yet in the plan", ""]
    for p in D.PROPOSED:
        out += ["### %s (%s)" % (p["name"], p["when"]), "", "- What: " + " ".join(p["what"]), "- How: " + " ".join(p["how"]),
                "- Record: " + " ".join(p["record"]), "- Tells us: " + " ".join(p["tells"]), "- Why: " + " ".join(p["why"]), "- Needs: " + p["needs"], ""]
    out += ["## New since the 10 November budget sheet", ""] + ["- **%s:** %s" % kv for kv in D.NEW_SINCE]
    out += ["", "## The next dates", ""] + ["- **%s:** %s" % kv for kv in D.DATES]
    out += ["", "## Where the money could come from", ""] + ["- **%s:** %s" % kv for kv in D.FUNDING]
    out += ["", "## Sources", ""] + ["- " + x for x in D.SOURCES]
    out += ["", "*Written %s. Prices are the 10 November budget sheet unless a note says otherwise.*" % D.DATE]
    return "\n".join(out) + "\n"


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "site"):
        p = os.path.join(SITE, "public", "tests", "index.html")
        open(p, "w", encoding="utf-8").write(page("site")); print("wrote", p)
    if what in ("all", "artifact", "pdf"):
        p = os.path.join(OUT, "index.html")
        open(p, "w", encoding="utf-8").write(page("artifact")); print("wrote", p)
    if what in ("all", "md"):
        p = os.path.join(OUT, "HCSA_physical_test_plan_%s.md" % STAMP)
        open(p, "w", encoding="utf-8").write(markdown()); print("wrote", p)
    if what in ("all", "pdf"):
        src = os.path.join(OUT, "index.html"); pdf = os.path.join(OUT, "HCSA_physical_test_plan_%s.pdf" % STAMP)
        chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if subprocess.run(["which", c], capture_output=True).returncode == 0), None)
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--run-all-compositor-stages-before-draw",
                        "--virtual-time-budget=8000", "--no-pdf-header-footer", "--print-to-pdf=" + pdf, "file://" + src + "?still=1"], check=True,
                       capture_output=True)
        print("wrote", pdf, round(os.path.getsize(pdf) / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
