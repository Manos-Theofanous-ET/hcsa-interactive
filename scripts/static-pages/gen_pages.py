"""Build the two plain HTML pages that sit next to the 3D site:
  public/plan/index.html        the fall 2026 plan and what we need from sponsors
  public/blueprints/index.html  every Rev S drawing, with dimensions, and what it shows
They are static on purpose: they load fast on a phone, print, and do not need WebGL.
Text for the drawings comes from blueprints-data.json (exported from the CAD repo's
explain_text.py); image files come from convert_images.py. Run from the site root:
  python scripts/static-pages/gen_pages.py
"""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, "..", "..", "public")
DATA = json.load(open(os.path.join(HERE, "blueprints-data.json")))
SIZES = json.load(open(os.path.join(HERE, "image-sizes.json")))
PDF = "/downloads/HCSA-Rev-S-drawings-explained-26-Sep-2026.pdf"
UPDATED = "28 September 2026"


def e(s):
    return html.escape(s, quote=True)


CSS = """
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:"Space Mono";src:url(/fonts/space-mono-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Space Mono";src:url(/fonts/space-mono-latin-700-normal.woff2) format("woff2");font-weight:700;font-display:swap}
:root{--bg:#000;--bg1:#0a0b0d;--bg2:#14161a;--ink:#f4f5f7;--ink2:rgba(244,245,247,.78);--ink3:rgba(244,245,247,.58);
--line:rgba(255,255,255,.12);--cyan:#00f0ff;--serif:"Fraunces",ui-serif,Georgia,serif;--mono:"Space Mono",ui-monospace,SFMono-Regular,monospace}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--cyan);text-underline-offset:3px}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.top{position:sticky;top:0;z-index:20;background:rgba(0,0,0,.86);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:22px;height:56px;overflow-x:auto;white-space:nowrap}
.top a{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3);text-decoration:none}
.top a:hover,.top a[aria-current]{color:var(--ink)}
.top a.brand{color:var(--ink);font-weight:700;letter-spacing:.24em;margin-right:auto}
.eyebrow,.label{font-family:var(--mono);font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--cyan);margin:0 0 12px}
.label{color:var(--ink3);letter-spacing:.18em}
h1{font-weight:400;font-size:clamp(2.1rem,5vw,3.6rem);line-height:1.08;letter-spacing:-.01em;margin:0 0 18px}
h2{font-weight:400;font-size:clamp(1.6rem,3.2vw,2.4rem);line-height:1.15;margin:0 0 14px}
h3{font-weight:600;font-size:1.25rem;line-height:1.3;margin:0 0 8px}
.lead{font-size:1.25rem;color:var(--ink2);max-width:760px;margin:0}
header.hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
section{padding:56px 0;border-bottom:1px solid var(--line)}
p{margin:0 0 14px}
.muted{color:var(--ink3)}
ul.dots{list-style:none;padding:0;margin:0 0 14px}
ul.dots li{position:relative;padding-left:20px;margin:0 0 8px;color:var(--ink2)}
ul.dots li:before{content:"";position:absolute;left:2px;top:.72em;width:6px;height:6px;border-radius:50%;background:var(--cyan)}
.grid2{display:grid;gap:28px;grid-template-columns:1fr}
.grid3{display:grid;gap:20px;grid-template-columns:1fr}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}.grid3{grid-template-columns:repeat(3,1fr)}}
.card{border:1px solid var(--line);background:rgba(255,255,255,.03);border-radius:3px;padding:20px}
.card p:last-child{margin-bottom:0}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0;padding:0;list-style:none}
.facts li{font-family:var(--mono);font-size:13px;border:1px solid var(--line);padding:6px 10px;border-radius:2px;color:var(--ink2)}
.btn{display:inline-block;font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;
border:1px solid var(--cyan);color:var(--ink);padding:12px 16px;border-radius:2px;margin:6px 10px 6px 0}
.btn:hover{background:rgba(0,240,255,.12)}
table{width:100%;border-collapse:collapse;font-size:16px}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
th{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);font-weight:400}
td.date{font-family:var(--mono);font-size:14px;white-space:nowrap;color:var(--ink2)}
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.group{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--cyan);padding-top:22px}
.tag{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;padding:2px 6px;border-radius:2px;border:1px solid var(--line);color:var(--ink3);white-space:nowrap}
.tag.done{border-color:rgba(0,240,255,.6);color:var(--cyan)}
figure{margin:0}
.thumbs{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));margin-top:22px}
.thumbs button{all:unset;cursor:zoom-in;display:block;background:#fff;border-radius:2px;overflow:hidden;outline-offset:3px}
.thumbs button:focus-visible{outline:2px solid var(--cyan)}
.thumbs figcaption{font-size:14px;line-height:1.45;color:var(--ink3);margin-top:8px}
.thumbs .kind{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);display:block;margin-bottom:2px}
.subject{scroll-margin-top:70px}
.subject .tested{font-family:var(--mono);font-size:13px;color:var(--cyan);margin:0 0 14px}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0;padding:0;list-style:none}
.toc a{font-family:var(--mono);font-size:13px;text-decoration:none;border:1px solid var(--line);padding:6px 10px;border-radius:2px;color:var(--ink2)}
.toc a:hover{border-color:var(--cyan);color:var(--ink)}
.concept img{border-radius:2px;aspect-ratio:4/3;object-fit:cover;width:100%}
.testimg{background:#fff;border-radius:2px;margin:-4px -4px 14px}
footer{padding:40px 0 64px;color:var(--ink3);font-size:15px}
#lb{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.97);display:none;flex-direction:column;align-items:center;justify-content:center;padding:16px}
#lb.open{display:flex}
#lb img{max-height:calc(100vh - 150px);width:auto;max-width:100%;background:#fff}
#lb p{max-width:900px;color:var(--ink2);font-size:15px;margin:12px 0 0;text-align:center}
#lb .bar{position:absolute;top:10px;right:12px;display:flex;gap:8px}
#lb .bar button{font-family:var(--mono);font-size:13px;background:rgba(255,255,255,.08);color:var(--ink);border:1px solid var(--line);padding:8px 12px;border-radius:2px;cursor:pointer}
section,header{scroll-margin-top:64px}
@media(max-width:640px){.top a.wide-only{display:none}.top .wrap{gap:14px}.top a{font-size:11px;letter-spacing:.1em}
table.stack thead{display:none}table.stack tr{display:block;border-bottom:1px solid var(--line);padding:12px 0}
table.stack td{display:block;border:0;padding:2px 0}table.stack td.date{white-space:normal;color:var(--cyan)}
table.stack td.group{padding-top:18px}}
@media print{.top,#lb,.btn{display:none}body{background:#fff;color:#000}section{border-color:#ccc}}
"""

LIGHTBOX = """
<div id="lb" role="dialog" aria-modal="true" aria-label="Drawing, full size">
  <div class="bar"><button type="button" data-lb="prev" aria-label="Previous drawing">Prev</button><button type="button" data-lb="next" aria-label="Next drawing">Next</button><button type="button" data-lb="close" aria-label="Close">Close</button></div>
  <img alt="">
  <p></p>
</div>
<script>
(function(){
  var lb=document.getElementById('lb'),img=lb.querySelector('img'),cap=lb.querySelector('p');
  var items=[].slice.call(document.querySelectorAll('[data-full]')),i=0,last=null;
  function show(k){i=(k+items.length)%items.length;var b=items[i];img.src=b.getAttribute('data-full');
    img.alt=b.querySelector('img').alt;cap.textContent=b.getAttribute('data-cap')||'';}
  items.forEach(function(b,k){b.addEventListener('click',function(){last=b;show(k);lb.classList.add('open');lb.querySelector('[data-lb=close]').focus();});});
  function close(){lb.classList.remove('open');img.removeAttribute('src');if(last)last.focus();}
  lb.addEventListener('click',function(ev){var a=ev.target.getAttribute('data-lb');
    if(a==='close'||ev.target===lb)close();else if(a==='next')show(i+1);else if(a==='prev')show(i-1);});
  document.addEventListener('keydown',function(ev){if(!lb.classList.contains('open'))return;
    if(ev.key==='Escape')close();else if(ev.key==='ArrowRight')show(i+1);else if(ev.key==='ArrowLeft')show(i-1);});
})();
</script>
"""


def page(title, desc, current, body, lightbox=False):
    nav = [("/", "HCSA", "brand"), ("/plan/", "The plan", ""), ("/blueprints/", "Blueprints", ""),
           ("/#work", "Concept art", "wide-only"), ("/#sponsor", "Sponsor", "")]
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}" class="{c}"{cur if h == current else ""}>{e(t)}</a>' for h, t, c in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#000000">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://hcsa-site.vercel.app/og-blueprints.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>{CSS}</style>
</head>
<body>
<nav class="top" aria-label="Site"><div class="wrap">{links}</div></nav>
<main>
{body}
</main>
<footer><div class="wrap">
<p>Human-Centric Space Architecture (HCSA), a student research project at Brown University, supported by a Brown UTRA award and developed with RISD. Faculty advisor: Prof. Rick Fleeter. Project lead: Manos Theofanous.</p>
<p>Updated {UPDATED}. Drawings are Rev S, taken from the CAD model; every dimension is in millimetres.</p>
</div></footer>
{LIGHTBOX if lightbox else ""}
</body>
</html>
"""


KIND_LABEL = {"2d_sketch": "2D sketch", "2d_render": "2D render", "3d_sketch": "3D sketch", "3d_render": "3D render"}


def thumbs_for(key):
    out = []
    for subj, kind, name, note in DATA["pages"]:
        if subj != key:
            continue
        kinds = [kind] if kind != "3d" else ["3d_render", "3d_sketch"]
        for k in kinds:
            stem = f"{k}-{name}"
            w, h = SIZES[stem]
            cap = f"{KIND_LABEL[k]}. {note}"
            out.append(
                f'<figure><button type="button" data-full="/blueprints/img/{stem}.webp" data-cap="{e(cap)}" aria-label="Open {e(KIND_LABEL[k])} full size">'
                f'<img src="/blueprints/img/{stem}-thumb.webp" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{e(note)}"></button>'
                f'<figcaption><span class="kind">{e(KIND_LABEL[k])}</span>{e(note)}</figcaption></figure>')
    return "".join(out)


# ---------------------------------------------------------------- blueprints
ORDER = [("The structure", ["shell", "hex", "pent", "joint", "seam", "corner"]),
         ("The tests", ["t0", "t1", "t550", "t2p", "t2r"])]
SUBJ = {s["key"]: s for s in DATA["subjects"]}
SHORT = {"shell": "The whole shell", "hex": "Hexagon panel", "pent": "Pentagon panel", "joint": "The joint",
         "seam": "One seam", "corner": "A corner", "t0": "T0 glass discs", "t1": "T1 seam slice",
         "t550": "T1 550 mm article", "t2p": "T2 panel at 1:4", "t2r": "T2 water rig"}

OPEN_ITEMS = [
    "Bolts per seam: the model has 29 (with 30 the end nuts clash at every pentagon corner); the specification says about 30. Needs a decision.",
    "The corner seal: the O-rings of the three seams stop 30 mm short of each corner, and nothing seals the small triangle between them yet.",
    "The ribs in the full-size panels are the old ones and far too weak as spokes. A rib study this fall makes them deeper or adds a ring. Until then the model mass (about 26,700 kg) is not an estimate.",
    "How the whole shell shares the load between panels, seams and corners. The FEA size study answers it.",
    "The pentagon housing, the solar panels and the fold-out shields are not designed yet, and a shield folding out puts loads into the pentagon frame that no test here covers.",
    "The exact bolt part number (the fastener memo is due 1 November), and the T2 frame split into bars before the drawings are released.",
]


def blueprints():
    ov = DATA["overview"]
    toc = "".join(f'<li><a href="#{k}">{e(SHORT[k])}</a></li>' for _, ks in ORDER for k in ks)
    parts = [f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Blueprints, Rev S, {UPDATED}</p>
<h1>The shell, the joint and the tests, with dimensions.</h1>
<p class="lead">{e(ov["intro"])}</p>
<ul class="facts"><li>11,151 mm across</li><li>2,250 mm edges</li><li>20 glass hexagons</li><li>12 solid pentagons</li><li>90 seams</li><li>60 corners</li><li>2,610 bolts</li></ul>
<p style="margin-top:24px"><a class="btn" href="{PDF}">Download all drawings, explained (PDF, 53 pages, 8.6 MB)</a><a class="btn" href="/plan/">Read the plan</a></p>
<ul class="toc" aria-label="Jump to">{toc}</ul>
</div></header>
<section><div class="wrap grid2">
<div><h2>How to read the drawings</h2><ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in ov["reading"])}</ul>
<p class="muted">Click any drawing to open it full size. Arrow keys step through them.</p></div>
<div><h2>How the pieces fit</h2>
<p>The shell is 32 panels. Each panel has frames on its edges; two frames bolted together make a seam; three seams meet at a corner. We test the parts that decide whether it holds: the glass (T0), the seam (T1) and one panel (T2). A computer study of the whole shell (FEA) comes first, because it says how the panels share the load.</p>
<p class="muted">Drawings are a design in progress, not a flight design. The open items are listed at the bottom of this page.</p></div>
</div></section>
"""]
    for group, keys in ORDER:
        parts.append(f'<section style="padding:28px 0 0;border:0"><div class="wrap"><p class="eyebrow">{e(group)}</p></div></section>')
        for k in keys:
            s = SUBJ[k]
            why = "".join(f"<li>{e(t)}</li>" for t in s["why"])
            tests = "".join(f"<li>{e(t)}</li>" for t in s["tests"])
            nums = "".join(f"<li>{e(t)}</li>" for t in s["numbers"])
            parts.append(f"""
<section id="{k}" class="subject"><div class="wrap">
<h2>{e(s["title"])}</h2>
<p class="tested">{e(s["tested_by"])}</p>
<div class="grid2">
<div><p>{e(s["what"])}</p><p class="muted">{e(s["where"])}</p>
<p class="label">Key numbers</p><ul class="facts">{nums}</ul></div>
<div><p class="label">Why it is like this</p><ul class="dots">{why}</ul>
<p class="label">How it is tested</p><ul class="dots">{tests}</ul></div>
</div>
<div class="thumbs">{thumbs_for(k)}</div>
</div></section>""")
    parts.append(f"""
<section id="open"><div class="wrap">
<h2>Still open</h2>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in OPEN_ITEMS)}</ul>
<p style="margin-top:20px"><a class="btn" href="{PDF}">Download the drawings (PDF)</a><a class="btn" href="/plan/#need">What we need from sponsors</a></p>
</div></section>""")
    return page("HCSA blueprints: the shell, the joint and the tests (Rev S)",
                "Every Rev S drawing of the HCSA shell, panels, seam joint, corner and test articles, with dimensions and a plain explanation of each.",
                "/blueprints/", "".join(parts), lightbox=True)


# ---------------------------------------------------------------- plan
MILESTONES = [
    ("27 Sep", "15 requirements for the seam, each with its source", "Sent to advisor"),
    ("27 Sep", "Load cases for the seam, with the two hand estimates reconciled", "Sent to advisor"),
    ("4 Oct", "Glass and frame materials chosen, from published design data", ""),
    ("11 Oct", "Design strength of the glass from published data, scaled up to a full pane; the T0 discs check it later in October", ""),
    ("18 Oct", "First computer model (FEA) of the seam and one panel; rib depth settled", ""),
    ("25 Oct", "Seam design Rev D, with the open decisions closed", ""),
    ("1 Nov", "Parts memo, with the bolt part number confirmed", ""),
    ("8 Nov", "Drawings, parts list and quotes released; go or no-go for building", ""),
    ("22 Nov", "Test plan for spring 2027", ""),
    ("6 Dec", "If the shop delivers: the 550 mm joint article built, bolt tension against seal squeeze measured", ""),
    ("11 Dec", "Fall report, 10 to 15 pages", ""),
]

TESTS = [
    ("t0", "T0: how strong is our glass?", "3d_render-17_T0_ring_on_ring",
     "Glass discs 50 mm across and 3 mm thick, pressed in the middle until they break. 30 or more per type of glass, so we know the real strength and how much it scatters.",
     "October, in a small load frame."),
    ("t1", "T1: does the seam hold when it is pulled apart?", "3d_render-10_T1_slice_150",
     "Full-size slices of the seam, 75, 150 and 225 mm long, pulled in a 100 kN load frame while we check the seal between the O-rings. Plus a 550 mm piece of the seam to check it goes together and holds air.",
     "Parts ordered after the 8 November release; tests as soon as they arrive."),
    ("t2p", "T2: how does a window panel bend?", "3d_render-14_T2_rig_pinned",
     "A hexagon panel at quarter scale, 1.1 m across, with aluminium in place of glass, loaded with water up to 2 atm in a steel tub. It shows how the panes bend onto the frame and ribs.",
     "Spring 2027."),
    ("shell", "FEA: how does the whole shell share the load?", "3d_render-02_shell_cutaway",
     "Computer models of one panel, a cap of seven panels and the full shell. They tell us how much load the seams and corners really carry, which sets the bolt size.",
     "October and November."),
]

# What we need, grouped by test. (item, size and quantity, needed by)
NEEDS = [
    ("For T0, the glass discs", [
        ("Borosilicate glass discs (for example Borofloat 33)", "50 mm across (or 50 mm squares), 3 mm thick, all with the same surface finish. 60 pieces: 30 for strength, 30 for four loading speeds. Edge chips are fine: the test only loads the middle.", "Mid October"),
        ("Fused silica discs", "Same size, 30 pieces.", "Mid October"),
        ("ALON or sapphire discs, for comparison", "Same size, 10 to 15 pieces.", "November"),
        ("Hardened tool steel for the test rings", "Two small rings, 70 mm across; machining.", "Early October"),
    ]),
    ("For T1, the seam slices and the 550 mm joint article", [
        ("6061-T6 aluminium, and CNC machining of 8 edge frames", "Six slice frames about 205 x 140 mm in section, 75, 150 and 225 mm long (two of each), and two frames about 60 x 140 x 550 mm. O-ring grooves 6.6 x 4.0 mm, bolt holes 8.03 mm at 75 mm. About 27 kg finished; STEP files ready now.", "8 Nov release"),
        ("4140 steel pull blocks, quenched and tempered", "Six blocks 83 x 80 mm in section, 75, 150 and 225 mm long, each with an M24 tapped hole. About 45 kg.", "8 Nov release"),
        ("5/16 in (-10) A286 bolts, nuts and washers", "30 sets (13 used, the rest spares). Part number confirmed 1 November.", "November"),
        ("Fluorosilicone (FVMQ) O-ring cord", "5.33 mm (0.210 in) cross-section, 70 Shore A, 5 m.", "November"),
        ("RTV566 silicone with its primer", "One kit, plus a syringe and tips for a 3 mm bead.", "November"),
        ("Fixture hardware", "50 M12 class 10.9 bolts, 1 m of M8 threaded rod with nuts, eight steel end plates 84 x 38 x 10 mm, 3 mm neoprene sheet 300 x 300 mm.", "November"),
    ]),
    ("For T2, one panel at quarter scale and its water rig", [
        ("6061-T6 aluminium for the panel frame, six ribs and hub", "About 31 kg finished, 1,217 x 1,054 x 124 mm overall, from 12 mm and 10 mm plate and bar. Cut list with the drawings.", "January"),
        ("Six aluminium panes", "6061-T6 plate, 8 mm (5/16 in), triangles about 525 x 455 mm; one 1,220 x 2,440 mm sheet covers all six. Laser or waterjet cut.", "January"),
        ("Steel plate for the rig, cut and welded", "About 490 kg of A36 or S355: a 25 mm floor 1,222 x 1,058 mm, 12 mm walls 175 mm tall, and three hexagonal rings 1,409 x 1,220 mm outside (25, 22 and 25 mm thick).", "January"),
        ("Rubber and small parts", "1 mm EPDM sheet 1.5 x 1.3 m; neoprene strip 1.5 x 10 mm, 8 m; 24 M16 class 8.8 bolts and nuts; six 12 mm ground steel bars 548 mm long; a relief valve set at 220 kPa; brass fittings and a pressure gauge.", "January"),
    ]),
    ("For measuring", [
        ("Strain gauges and a strain amplifier board", "About 20 rosettes and 10 single gauges; a 16-channel strain-gauge amplifier board (PCB).", "November"),
        ("Dial gauges or LVDTs, and a pressure sensor", "Four displacement gauges; one 0 to 300 kPa pressure transducer.", "January"),
    ]),
    ("Time, software and funds", [
        ("Test frame time", "A 100 kN universal test frame for T1 and a 5 kN frame for T0.", "October to December"),
        ("FEA software", "One academic seat for structural and thermal analysis, for the shell size study.", "October"),
        ("Funding", "Pays for machining, the steel rig and anything not donated. Every dollar goes to parts and shop time.", "Any time"),
        ("Expert advice", "A 20 minute review from people who know bolted joints, seals, structural glass or pressure testing.", "Any time"),
    ]),
]


def plan():
    def tag(s):
        return f'<span class="tag done">{e(s)}</span>' if s else ""
    ms = "".join(
        f'<tr><td class="date">{e(d)}</td><td>{e(t)}</td><td>{tag(s)}</td></tr>'
        for d, t, s in MILESTONES)
    tests = "".join(
        f'<div class="card"><img class="testimg" src="/blueprints/img/{img}-thumb.webp" width="{SIZES[img][0]}" height="{SIZES[img][1]}" loading="lazy" alt="{e(title)}">'
        f'<h3>{e(title)}</h3><p>{e(body)}</p><p class="muted">{e(when)}</p><p><a href="/blueprints/#{k}">Drawings and dimensions</a></p></div>'
        for k, title, img, body, when in TESTS)
    need_rows = []
    for g, rows in NEEDS:
        need_rows.append(f'<tr><td colspan="3" class="group">{e(g)}</td></tr>')
        for item, size, when in rows:
            need_rows.append(f'<tr><td><strong style="font-weight:600">{e(item)}</strong></td><td>{e(size)}</td><td class="date">{e(when)}</td></tr>')
    concept = [
        ("/assets/web/images-concept-exterior.webp", "The facility in orbit, with gardens inside"),
        ("/assets/web/images-concept-observatory.webp", "Walkways and gardens under a glass sky"),
        ("/assets/web/images-facility-render-day.webp", "Garden column, ramp and seating pods"),
    ]
    concept_html = "".join(f'<figure><img src="{s}" loading="lazy" alt="{e(c)}"><figcaption class="muted" style="font-size:15px;margin-top:8px">{e(c)}</figcaption></figure>' for s, c in concept)
    body = f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">The plan, fall 2026. Updated {UPDATED}</p>
<h1>This fall we build and test the seam between two panels.</h1>
<p class="lead">We take the joint where two panels meet from a design on paper to hardware we have built and measured, and we do the analysis it depends on (loads, glass strength, frame material) so the tests mean something.</p>
<p style="margin-top:24px"><a class="btn" href="#need">What we need from sponsors</a><a class="btn" href="/blueprints/">See the blueprints</a><a class="btn" href="{PDF}">Drawings (PDF)</a></p>
</div></header>

<section id="concept"><div class="wrap">
<p class="eyebrow">The concept</p>
<div class="grid2">
<div><h2>A room in orbit made mostly of windows.</h2>
<p>HCSA is a design for a facility in low Earth orbit for short visits. Nobody lives there; people come to look at Earth, move around, meet, do research and spend time among plants.</p>
<p>Its wall is 32 flat panels in the shape of a football. The 20 hexagons are glass: they are the windows. The 12 pentagons are solid: they house the solar panels and the shields that fold out over the windows around them. Every window borders three pentagons, so a shield can reach every one.</p>
<p>Inside is air at normal pressure and outside is vacuum, so the air pushes out on every panel with about 1.33 meganewtons on each hexagon. Holding that at the seams, and through the glass, is what this fall's work is about.</p></div>
<div><ul class="facts" style="margin-top:0"><li>11.15 m across</li><li>2.25 m edges</li><li>630 m³ inside</li><li>32 panels</li><li>90 seams</li><li>1 atm inside, vacuum outside</li></ul>
<p class="muted" style="margin-top:18px">More concept art, the 3D model and our physical model are on the <a href="/#work">main site</a>.</p></div>
</div>
<div class="grid3 concept" style="margin-top:26px">{concept_html}</div>
</div></section>

<section id="now"><div class="wrap grid2">
<div><p class="eyebrow">Where we are</p><h2>The design is simple enough to build.</h2></div>
<div><ul class="dots">
<li>The panel joint is redesigned to be simple (Rev S): two aluminium frames bolted face to face, one row of bolts every 75 mm, two O-rings and a sealant bead.</li>
<li>The whole shell is modelled in CAD: 32 panels, 90 seams, 2,610 bolts and every seal, with no parts overlapping.</li>
<li>The tests are designed, with drawings for every test piece and rig, and the test plan is going to Brown engineering faculty for review.</li>
<li>Every drawing, with dimensions and a plain explanation, is on the <a href="/blueprints/">blueprints page</a>.</li>
</ul></div>
</div></section>

<section id="tests"><div class="wrap">
<p class="eyebrow">The tests, smallest first</p>
<h2>Each test answers one question.</h2>
<div class="grid2" style="margin-top:22px">{tests}</div>
</div></section>

<section id="milestones"><div class="wrap">
<p class="eyebrow">By 11 December</p>
<h2>What we will finish this fall.</h2>
<div class="tablewrap"><table class="stack"><thead><tr><th>Date</th><th>What</th><th></th></tr></thead><tbody>{ms}</tbody></table></div>
<p class="muted" style="margin-top:16px">After this fall: in spring 2027 we run the T1 and T2 tests under pressure, check the computer model against them, and design the corner seal. In spring 2028 the work becomes a capstone project.</p>
</div></section>

<section id="need"><div class="wrap">
<p class="eyebrow">What we need</p>
<h2>Parts, materials and time, with the sizes.</h2>
<p class="lead" style="margin-bottom:22px">Everything below comes from the CAD model of the test pieces. Offcuts, rejects and loans are welcome wherever they fit the sizes.</p>
<div class="tablewrap"><table class="stack"><thead><tr><th>Item</th><th>Size and quantity</th><th>Needed by</th></tr></thead><tbody>{"".join(need_rows)}</tbody></table></div>
<div class="card" style="margin-top:26px"><h3>What a sponsor gets</h3>
<p>Your name or logo on this site, in our fall report and on our posters and talks; photos and test results as each step is finished; and a visit to see the hardware and meet the team.</p>
<p>To help, reply to the email you received from us, or reach Manos Theofanous, project lead, through the Brown University School of Engineering.</p></div>
</div></section>
"""
    return page("HCSA plan for fall 2026, and what we need",
                "What the HCSA team at Brown University is building and testing in fall 2026, the milestones, and the parts, materials and sizes we are asking sponsors for.",
                "/plan/", body, lightbox=False)


if __name__ == "__main__":
    for rel, html_ in (("blueprints/index.html", blueprints()), ("plan/index.html", plan())):
        p = os.path.join(PUB, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(html_)
        print(rel, len(html_))
