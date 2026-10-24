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
PDF_REVD = "/downloads/HCSA-Rev-D-blueprint-pack-14-Oct-2026.pdf"
PDF_REVD_SPEC = "/downloads/HCSA-Rev-D-design-spec-14-Oct-2026.pdf"
UPDATED = "23 October 2026"
REVD_DATED = "14 October 2026"
REVS_DATED = "28 September 2026"


def e(s):
    return html.escape(s, quote=True)


CSS = """
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:"Fraunces";src:url(/fonts/fraunces-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic;font-display:swap}
@font-face{font-family:"Inter";src:url(/fonts/inter-latin-wght-normal.woff2) format("woff2-variations"),url(/fonts/inter-latin-wght-normal.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{--bg:#000;--bg1:#0a0b0d;--bg2:#14161a;--ink:#f1efea;--ink2:rgba(241,239,234,.8);--ink3:rgba(241,239,234,.62);
--line:rgba(255,255,255,.13);--accent:#c9b48f;--serif:"Fraunces",ui-serif,Georgia,serif;--sans:"Inter",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-underline-offset:3px}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.top{position:sticky;top:0;z-index:20;background:rgba(0,0,0,.86);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:22px;height:56px;overflow-x:auto;white-space:nowrap}
.top a{font-family:var(--sans);font-size:14.5px;font-weight:500;letter-spacing:0;color:var(--ink3);text-decoration:none;transition:color .2s ease}
.top a:hover,.top a[aria-current]{color:var(--ink)}
.top a.brand{color:var(--ink);font-weight:600;letter-spacing:.06em;margin-right:auto}
.eyebrow,.label{font-family:var(--sans);font-size:14px;font-weight:500;letter-spacing:0;color:var(--accent);margin:0 0 14px}
.label{color:var(--ink3)}
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
ul.dots li:before{content:"";position:absolute;left:2px;top:.72em;width:6px;height:6px;border-radius:50%;background:var(--accent)}
.grid2{display:grid;gap:28px;grid-template-columns:1fr}
.grid3{display:grid;gap:20px;grid-template-columns:1fr}
@media(min-width:760px){.grid2{grid-template-columns:1fr 1fr}.grid3{grid-template-columns:repeat(3,1fr)}}
.card{border-top:1px solid var(--line);padding:20px 0 8px}
.card p:last-child{margin-bottom:0}
.facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px;margin:18px 0 0;padding:0;list-style:none}@media(min-width:760px){.facts{grid-template-columns:repeat(3,minmax(0,1fr))}}
.facts li{font-family:var(--sans);font-size:15px;border-top:1px solid var(--line);padding:10px 0 12px;color:var(--ink2);font-feature-settings:"tnum" 1}
.btn{display:inline-block;font-family:var(--sans);font-size:15px;font-weight:500;letter-spacing:0;text-decoration:none;
border:1px solid rgba(241,239,234,.3);color:var(--ink);padding:11px 18px;border-radius:0;margin:6px 10px 6px 0;transition:border-color .25s ease,background-color .25s ease,color .25s ease}
.btn:hover{border-color:var(--accent);color:var(--accent)}
table{width:100%;border-collapse:collapse;font-size:16px;font-feature-settings:"tnum" 1}
th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
th{font-family:var(--sans);font-size:14px;font-weight:600;letter-spacing:0;color:var(--ink3)}
td.date{font-family:var(--sans);font-size:14px;white-space:nowrap;color:var(--ink2)}
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.group{font-family:var(--sans);font-size:14px;font-weight:600;letter-spacing:0;color:var(--accent);padding-top:26px}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.tag{font-family:var(--sans);font-size:13px;font-weight:500;letter-spacing:0;padding:2px 8px;border-radius:0;border:1px solid var(--line);color:var(--ink3);white-space:nowrap}
.tag.done{border-color:rgba(201,180,143,.6);color:var(--accent)}
figure{margin:0}
.thumbs{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));margin-top:22px}
.thumbs button{all:unset;cursor:zoom-in;display:block;background:#fff;border-radius:2px;overflow:hidden;outline-offset:3px}
.thumbs button:focus-visible{outline:2px solid var(--accent)}
.thumbs figcaption{font-size:14px;line-height:1.45;color:var(--ink3);margin-top:8px}
.thumbs .kind{font-family:var(--sans);font-size:13px;font-weight:600;letter-spacing:0;color:var(--ink2);display:block;margin-bottom:2px}
.subject{scroll-margin-top:70px}
.subject .tested{font-family:var(--sans);font-size:15px;color:var(--accent);margin:0 0 14px}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0;padding:0;list-style:none}
.toc a{font-family:var(--sans);font-size:15px;text-decoration:underline;text-decoration-color:rgba(241,239,234,.28);text-underline-offset:5px;color:var(--ink2);transition:color .2s ease,text-decoration-color .2s ease}
.toc a:hover{color:var(--accent);text-decoration-color:var(--accent)}.toc{gap:10px 22px}
.concept img{border-radius:2px;aspect-ratio:4/3;object-fit:cover;width:100%}
.testimg{background:#fff;border-radius:2px;margin:-4px -4px 14px}
footer{padding:40px 0 64px;color:var(--ink3);font-size:15px}
#lb{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.97);display:none;flex-direction:column;align-items:center;justify-content:center;padding:16px}
#lb.open{display:flex;animation:fade .28s ease}#lb img{animation:fadescale .42s cubic-bezier(.16,1,.3,1)}
@keyframes fade{from{opacity:0}to{opacity:1}}@keyframes fadescale{from{opacity:0;transform:scale(.985)}to{opacity:1;transform:none}}
html.js main>section,html.js main>header{opacity:0;transform:translate3d(0,18px,0);transition:opacity .7s ease,transform 1s cubic-bezier(.16,1,.3,1)}
html.js main>section.in,html.js main>header.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}html.js main>section,html.js main>header{transform:none;transition:opacity .2s linear}#lb.open,#lb img{animation:none}}
#lb img{max-height:calc(100vh - 150px);width:auto;max-width:100%;background:#fff}
#lb p{max-width:900px;color:var(--ink2);font-size:15px;margin:12px 0 0;text-align:center}
#lb .bar{position:absolute;top:10px;right:12px;display:flex;gap:8px}
#lb .bar button{font-family:var(--sans);font-size:14px;background:rgba(255,255,255,.06);color:var(--ink);border:1px solid var(--line);padding:8px 14px;border-radius:0;cursor:pointer;transition:border-color .2s ease}#lb .bar button:hover{border-color:var(--accent)}
section,header{scroll-margin-top:64px}
@media(max-width:640px){.top a.wide-only{display:none}.top .wrap{gap:16px}.top a{font-size:14px}
table.stack thead{display:none}table.stack tr{display:block;border-bottom:1px solid var(--line);padding:12px 0}
table.stack td{display:block;border:0;padding:2px 0}table.stack td.date{white-space:normal;color:var(--accent)}
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
           ("/tests/", "The tests", ""), ("/#work", "Concept art", "wide-only"), ("/#sponsor", "Sponsor", "")]
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
<p>Updated {UPDATED}. The Rev D sheets are drawn from the Rev D design spec ({REVD_DATED}); the Rev S drawings ({REVS_DATED}) are taken from the CAD model and are kept for reference. Every dimension is in millimetres.</p>
</div></footer>
{LIGHTBOX if lightbox else ""}
<script>
(function(){{if(!('IntersectionObserver' in window))return;var d=document.documentElement;d.classList.add('js');
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},{{rootMargin:'0px 0px -6% 0px',threshold:0.04}});
document.querySelectorAll('main>section,main>header').forEach(function(s){{io.observe(s);}});
if(location.hash){{var t=document.querySelector(location.hash);if(t)t.classList.add('in');}}}})();
</script>
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

# Rev D sheets (public/blueprints/img/revd-NN_slug.webp, from the Rev D blueprint pack, 14 Oct 2026).
REVD_SHEETS = [
    ("00_cover", "Sheet 00", "Cover: index of the 13 sheets, what changed from Rev S to Rev D, drawing conventions and the status tags (LOCKED, FEA, PROPOSAL, OPEN)."),
    ("01_shell", "Sheet 01", "The shell in elevation and plan with panel names: 20 hexagons, 12 pentagons, 90 seams and 60 corners; 11,151 mm across, every edge 2,250 mm."),
    ("02_hex_plan", "Sheet 02", "Hexagon panel plan from the cabin side: 6 main ribs from the centre to each corner, 18 secondary ribs of 1,125 mm, 24 triangular panes of 1,125 mm side."),
    ("03_hex_section", "Sheet 03", "Section A-A along a main rib, corner to centre: the 375 mm main rib, the 140 mm edge frame and the 25.4 mm pressure pane on its seat."),
    ("04_rib_sections", "Sheet 04", "Rib sections: main hexagon rib I 375 (200 x 15 flanges, 8 web), main pentagon rib I 400 (80 x 25, 8 web), secondary rib I 160 (64 x 8, 6 web); allowable 160 MPa."),
    ("05_seam_joint", "Sheet 05", "Seam joint in section: frames A and B, the 5/16-24 A286 seal-clamp bolt every 75 mm, two 5.33 mm cords in 7.1 x 4.0 mm glands, the RTV566 bead, and the load path: 63 % of the 623 kN per seam to the corner nodes, 31 % to the hardpoint, 5 % to the bolts."),
    ("06_corner_node", "Sheet 06", "Corner node, plan on the vertex and section along a seam (PROPOSAL): one machined 6061-T651 block per panel corner taking the first 100 mm of both frames, 5.8 kg; vertex ties 4 x 5/8-18 A286 per joint face for 196 kN in tension only; the corner moment goes through block-to-block face contact."),
    ("07_hardpoint", "Sheet 07", "Seam mid hardpoint at x 1,125 mm, plan and section (PROPOSAL): a 40 mm lug on frame A between a 2 x 25 mm clevis on frame B, 40 mm A286 pin (bending 349 MPa at 195 kN; a 30 mm pin would be past yield), 152 to 195 kN across the seam and no moment; lug and clevis below the three seal lines."),
    ("08_glazing", "Sheet 08", "Glazing stack and the pane edge at the frame: 6 mm fused silica debris pane, 12 mm gas gap, PV and electrochromic layers, the shutter, and the 25.4 mm BOROFLOAT 33 pressure pane on a 2 mm strip with a 20 mm bite."),
    ("09_pent_plan", "Sheet 09", "Pentagon panel plan from the cabin side: 5 main ribs, 15 secondary ribs, 20 bays and a 10 mm face plate (Rev S 4 mm); 651 kg before the solar, shield and docking equipment."),
    ("10_test_articles", "Sheet 10", "The test articles against the facility: T0 glass bars in four-point bend, T1 seam slices and the 550 mm article at full size, T2 the 24-pane hexagon at 1:4, T3 one corner at full size."),
    ("11_materials_mass", "Sheet 11", "Materials, heat treatment and mass: 6061-T651 for the prototype, 2219-T851 for flight, A286 fasteners, BOROFLOAT 33 glass; hexagon 1,838 kg, pentagon 651 kg, structure 34.0 t, facility 50.4 t itemised."),
    ("12_open_decisions", "Sheet 12", "The open decisions and which test or submodel settles each: hardpoint pinned or stiff, glass thickness, seal cord, bolt designation, frame bow, corner seal, tie and pin sizes, mass, the shear key, and the factor-of-safety basis."),
]

REVD_INTRO = (
    "The whole-shell stress model, run on three solvers from 9 to 12 October and reviewed independently, showed that the Rev S design "
    "cannot hold 1 atm: the 31 mm glass in the six-pane hexagon reaches 54 MPa against 35 allowable and bends 7.3 mm against 3.1, the "
    "103 mm ribs are far past yield, and the open corners put 100 to 138 kN on end bolts that break at 34 kN. Rev D takes the branch the "
    "specification already allowed for. Each hexagon is split into 24 triangular panes of 1,125 mm side on 375 mm main ribs and 160 mm "
    "secondary ribs; the pressure pane is 25.4 mm BOROFLOAT 33; and the pull across each seam, 623 kN, goes through a solid machined node "
    "at every corner and a pinned hardpoint at every mid-seam (both proposed details, sized on 16 October), so the 26 bolts along a seam only clamp the seals. The structure is 34.0 t "
    "and the facility about 50.4 t. Every item on the sheets carries a status. LOCKED is geometry unchanged from Rev S. FEA is what the "
    "October runs set: the rib sections, the glass thickness, the pane count and the load split. PROPOSAL is a detail drawn to carry an "
    "FEA load and still to be sized in the 16 October submodels and in a physical test: the corner node and its vertex ties, the "
    "hardpoint, the 26-bolt count and the wider seal glands. OPEN is a decision not yet taken, with the Rev D default stated; the ten "
    "open decisions are listed at the bottom of this page. Rev D is not locked in TRUTH until the revision is signed."
)

OPEN_ITEMS = [
    "The mid-seam hardpoint: pinned (the Rev D default) or moment-carrying. It sets the secondary rib, 160 or 200 mm deep. Submodel C3 on 16 October.",
    "The pressure glass: decided 23 October for Rev E. 22 mm BOROFLOAT 33 on 531 mm panes (16 per 2,250 mm triangle, 96 per hexagon); 708 mm panes as upside, 425 mm as fallback, final pick after the T0 bars give the Weibull m. Drawings 8 November; the Rev D sheets above still show 25.4 mm on 1,125 mm panes.",
    "The seal cord: decided 23 October for Rev E. Two butyl BA500 closed loops with the RTV566 bead as the third seal; fluorosilicone is out, on Parker's advice. Drawings 8 November.",
    "The seam bolt part number. The old NAS9306C-06 is a rivet standard and the wrong size; the parts memo of 1 November names the bolt.",
    "The frame bow between corners: 1.4 to 2.0 mm predicted against the 1 mm sealing limit. Keep the frame 140 mm deep and test (default), or deepen it. After T1 and submodel C2.",
    "The corner seal at the vertex plug, where the three seal loops meet.",
    "The vertex ties (tension only; the corner moment goes through the block faces) and the 40 mm hardpoint pin. Submodels C1 and C3 on 16 October.",
    "Mass: the Rev D structure is 34.0 t and the facility 50.4 t, up from a Rev S figure that did not hold. A rib study led by transparency (narrower, deeper ribs) is the next pass to bring it down.",
    "The shear key: none in Rev D (the vertex dowels and the hardpoint pin carry seam shear). Reinstated only if submodel C2 or the whole-shell shear check needs it.",
    "The factor-of-safety basis: 1.5 on yield at 1 atm as used, or NASA-STD-5001 1.5 proof and 2.0 ultimate. To be agreed with the faculty advisers before the 8 November drawings.",
]

OPEN_ITEMS_REVS = [
    "Bolts per seam: the model has 29 (with 30 the end nuts clash at every pentagon corner); the specification says about 30. Needs a decision.",
    "The corner seal: the O-rings of the three seams stop 30 mm short of each corner, and nothing seals the small triangle between them yet.",
    "The ribs in the full-size panels are the old ones and far too weak as spokes. A rib study this fall makes them deeper or adds a ring. Until then the model mass (about 26,700 kg) is not an estimate.",
    "How the whole shell shares the load between panels, seams and corners. The FEA size study answers it.",
    "The pentagon housing, the solar panels and the fold-out shields are not designed yet, and a shield folding out puts loads into the pentagon frame that no test here covers.",
    "The exact bolt part number (the fastener memo is due 1 November), and the T2 frame split into bars before the drawings are released.",
]


def revd_thumbs():
    out = []
    for slug, kind, note in REVD_SHEETS:
        stem = f"revd-{slug}"
        w, h = SIZES[stem]
        cap = f"{kind}. {note}"
        out.append(
            f'<figure><button type="button" data-full="/blueprints/img/{stem}.webp" data-cap="{e(cap)}" aria-label="Open {e(kind)} full size">'
            f'<img src="/blueprints/img/{stem}-thumb.webp" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{e(note)}"></button>'
            f'<figcaption><span class="kind">{e(kind)}</span>{e(note)}</figcaption></figure>')
    return "".join(out)


def blueprints():
    ov = DATA["overview"]
    toc = "".join(f'<li><a href="#{k}">{e(SHORT[k])}</a></li>' for _, ks in ORDER for k in ks)
    parts = [f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">Blueprints, Rev D, {REVD_DATED}</p>
<h1>The shell, the joint and the tests, with dimensions.</h1>
<p class="lead">{e(ov["intro"])} Rev D (14 October 2026) is the first design sized by a stress model of the whole shell: 24 glass panes per hexagon on deep ribs, a solid node at every corner and a hardpoint at every mid-seam.</p>
<ul class="facts"><li>11,151 mm across</li><li>2,250 mm edges</li><li>20 glass hexagons, 24 panes each</li><li>12 solid pentagons</li><li>90 seams, 60 corners</li><li>2,340 seal-clamp bolts</li></ul>
<p style="margin-top:24px"><a class="btn" href="{PDF_REVD}">Download the Rev D blueprint pack (PDF, 13 sheets, 0.3 MB)</a><a class="btn" href="{PDF_REVD_SPEC}">The Rev D design spec (PDF)</a><a class="btn" href="/plan/">Read the plan</a></p>
<ul class="toc" aria-label="Jump to"><li><a href="#revd">Rev D sheets</a></li><li><a href="#revs">Rev S drawings</a></li>{toc}<li><a href="#open">Still open</a></li></ul>
</div></header>
<section id="revd" class="subject"><div class="wrap">
<p class="eyebrow">The baseline</p>
<h2>Rev D, 14 Oct 2026: the FEA-sized baseline</h2>
<p class="tested">13 sheets, A3. Click any sheet to open it full size.</p>
<p>{e(REVD_INTRO)}</p>
<p class="muted">Two of the open decisions were taken on 23 October for Rev E, drawings due 8 November: the pressure pane becomes 22 mm BOROFLOAT 33 on 531 mm panes (96 per hexagon), and the seal becomes two butyl BA500 loops with the RTV566 bead. The sheets below still show the Rev D pane and seal until the new pack. See the plan for the reasons.</p>
<div class="thumbs">{revd_thumbs()}</div>
</div></section>
<section><div class="wrap grid2">
<div><h2>How to read the drawings</h2><ul class="dots"><li>Rev D sheets: one A3 drawing each, with a title block giving the sheet, the material and heat treatment of the parts on it, and the status of every item (LOCKED, FEA, PROPOSAL or OPEN). Not to scale; read the dimensions.</li>{"".join(f"<li>Rev S {e(t[0].lower() + t[1:])}</li>" for t in ov["reading"])}</ul>
<p class="muted">Click any drawing to open it full size. Arrow keys step through them.</p></div>
<div><h2>How the pieces fit</h2>
<p>The shell is 32 panels. Each panel has frames on its edges; two frames bolted together make a seam; three seams meet at a corner. The stress model of the whole shell (9 to 12 October) says how the load is shared: most of the pull across a seam goes into the corner nodes, a third into the mid-seam hardpoint, and the bolts only clamp the seals. We test the parts that decide whether it holds: the seam (T1, built this fall, pulled in January and February 2027 at the Rev D load), the glass (T0, bars in four-point bend, spring 2027), one panel (T2, a hexagon at 1:4, spring 2027) and a corner (T3, 2027). Every test is run on the computer first, nothing is machined before its digital twin has a signed sheet, and a test passes when the measurement lands within 10 % of the prediction.</p>
<p class="muted">Rev D is a design in progress, not a flight design. The open decisions are listed at the bottom of this page.</p></div>
</div></section>
<section id="revs" class="subject" style="padding-bottom:0"><div class="wrap">
<p class="eyebrow">For reference</p>
<h2>Rev S drawings (25 April to 14 Oct 2026, superseded; kept for reference)</h2>
<p class="muted">The drawings below are the Rev S design as it stood on {REVS_DATED}: six glass panes per hexagon on 103 mm ribs, 31 mm glass, 29 bolts per seam carrying the whole seam pull, and open corners. The whole-shell stress model showed that this does not hold 1 atm, and Rev D above replaces it. The text and numbers in these sections are Rev S and are left as they were, so the change can be followed; the T0 disc test is now a bar test and the T2 panel now has 24 panes.</p>
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
<p class="muted">The eight decisions Rev D leaves open, with the default it states for each.</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in OPEN_ITEMS)}</ul>
<p style="margin-top:20px"><a class="btn" href="{PDF_REVD}">The Rev D blueprint pack (PDF)</a><a class="btn" href="{PDF_REVD_SPEC}">The Rev D design spec (PDF)</a><a class="btn" href="{PDF}">The Rev S drawings, explained (PDF, superseded)</a><a class="btn" href="/plan/#need">What we need from sponsors</a></p>
</div></section>""")
    return page("HCSA blueprints: the shell, the joint and the tests (Rev D)",
                "The Rev D sheets (14 Oct 2026, sized by the whole-shell stress model) and every Rev S drawing of the HCSA shell, panels, seam joint, corner and test articles, with dimensions and a plain explanation of each.",
                "/blueprints/", "".join(parts), lightbox=True)


# ---------------------------------------------------------------- plan
MILESTONES = [
    ("27 Sep", "15 requirements for the seam, each with its source", "Sent to advisor"),
    ("27 Sep", "Load cases for the seam, with the two hand estimates reconciled", "Sent to advisor"),
    ("4 Oct", "Glass and frame materials chosen, from published design data", ""),
    ("11 Oct", "Design strength of the glass from published data, scaled up to a full pane; the T0 bars check it in spring 2027", ""),
    ("12 Oct", "Stress model of the whole shell on three solvers; Rev D sizes (14 Oct)", "Done"),
    ("23 Oct", "Pane and seal decided for Rev E: 22 mm glass on 531 mm panes, two butyl loops and a silicone bead", "Decided"),
    ("1 Nov", "Parts memo, with the bolt part number confirmed", ""),
    ("8 Nov", "Drawings, parts list and quotes released (the Rev E pack); go or no-go for building. Nothing is machined before its digital twin has a signed sheet", ""),
    ("18 Nov", "The 100 kN load frame at Brown becomes free", ""),
    ("22 Nov", "Test plan for spring 2027; test dates set with Dewesoft for the strain recorder loan", ""),
    ("6 Dec", "If the shop delivers: the 550 mm joint article built, bolt tension against seal squeeze measured", ""),
    ("11 Dec", "Fall report, 10 to 15 pages", ""),
    ("Jan to Feb 27", "The seam slices pulled apart in the 100 kN frame, with the Dewesoft recorder on loan", ""),
]

TESTS = [
    ("t0", "T0: how strong is our glass?", "3d_render-17_T0_ring_on_ring",
     "Borosilicate glass bars, 1 in wide and 1/8 in thick, bent in four-point bending until they break, the way ENGN 1440 does it. 30 or more per edge finish, so we know the real strength and how much it scatters. That scatter picks the final pane size: 531 mm as planned, 708 mm if the glass is consistent, 425 mm if it is not. The disc test drawn here is off: the fixture would cost thousands and the small frame at Brown is 0.5 kN, not 5 kN. The 60 BOROFLOAT and 15 sapphire discs already received stay for a second look.",
     "Spring 2027, with Prof. Padture's class. Bars this fall on the 0.5 kN frame are still being weighed."),
    ("t1", "T1: does the seam hold when it is pulled apart?", "3d_render-10_T1_slice_150",
     "Full-size slices of the seam, 75, 150 and 225 mm long, pulled in the 100 kN load frame at Brown while we check the seal between the two butyl loops. Plus a 550 mm piece of the seam to check it goes together and holds air. The seal changed on 23 Oct: two butyl BA500 loops and the silicone bead, in place of fluorosilicone cord, because a closed loop has no cut ends to leak at the corners (Parker's advice).",
     "Built this fall from the 8 November drawings. Pulled late January to February 2027: the frame is free after 18 November, and Dewesoft lends the 16-channel strain recorder in 3 to 4 week batches, booked a month ahead."),
    ("t2p", "T2: how does a window panel bend?", "3d_render-14_T2_rig_pinned",
     "A hexagon panel at quarter scale, 1.1 m across, with aluminium in place of glass, loaded with water up to 2 atm in a steel tub. It shows how the panes bend onto the frame and ribs.",
     "Spring 2027."),
    ("shell", "FEA: how does the whole shell share the load?", "3d_render-02_shell_cutaway",
     "Computer models of one panel, a cap of seven panels and the full shell. They tell us how much load the seams and corners really carry, which sets the bolt size.",
     "Ran 9 to 12 October (Rev D). Every physical test now gets its own computer twin first, and nothing is machined before that twin has a signed sheet."),
]

# What we need, grouped by test. (item, size and quantity, needed by)
NEEDS = [
    ("For T0, the glass bars", [
        ("Borosilicate glass bars (Borofloat 33)", "1 in wide, 1/8 in thick, about 4 in long, with the same edge finish within a set. 30 or more per edge finish. The 60 Borofloat discs (SCHOTT) and 15 sapphire discs (Meller Optics) already received are in hand.", "Early 2027"),
        ("Four-point bend fixture", "The ENGN 1440 fixture, or one like it, for a 0.5 kN frame.", "Early 2027"),
    ]),
    ("For T1, the seam slices and the 550 mm joint article", [
        ("6061-T6 aluminium, and CNC machining of 8 edge frames", "Six slice frames about 205 x 140 mm in section, 75, 150 and 225 mm long (two of each), and two frames about 60 x 140 x 550 mm. O-ring grooves 6.6 x 4.0 mm, bolt holes 8.03 mm at 75 mm. About 27 kg finished; STEP files ready now.", "8 Nov release"),
        ("4140 steel pull blocks, quenched and tempered", "Six blocks 83 x 80 mm in section, 75, 150 and 225 mm long, each with an M24 tapped hole. About 45 kg.", "8 Nov release"),
        ("5/16 in (-10) A286 bolts, nuts and washers", "30 sets (13 used, the rest spares). Part number confirmed 1 November.", "November"),
        ("Butyl seal loops (Parker BA500)", "Two closed loops per joint, moulded to the groove; sizes with the 8 November drawings. Fluorosilicone cord is no longer needed.", "November"),
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
        ("Strain gauges", "About 20 rosettes and 10 single gauges. The 16-channel strain recorder is on loan from Dewesoft, in 3 to 4 week batches.", "November"),
        ("Dial gauges or LVDTs, and a pressure sensor", "Four displacement gauges; one 0 to 300 kPa pressure transducer.", "January"),
    ]),
    ("Time, software and funds", [
        ("Test frame time", "The 100 kN frame at Brown for T1, free after 18 November, booked for late January to February 2027. T0 bars run on a 0.5 kN frame in spring 2027.", "January to February"),
        ("FEA software", "One academic seat for structural and thermal analysis, for the shell size study.", "October"),
        ("Funding", "Pays for machining, the steel rig and anything not donated. Every dollar goes to parts and shop time.", "Any time"),
        ("Expert advice", "A 20 minute review from people who know bolted joints, seals, structural glass or pressure testing.", "Any time"),
    ]),
]


REVD_NOTE = (
    "The whole-shell stress model (9 to 12 October, three solvers) showed the Rev S design does not hold 1 atm, and Rev D replaces it: "
    "24 glass panes per hexagon on 375 mm ribs, 25.4 mm glass, a solid node at every corner and a hardpoint at every mid-seam, with the "
    "bolts as seal clamps. Three things in this plan change. T0 moves from glass discs to borosilicate bars in four-point bend, run in "
    "ENGN 1440 in spring 2027. The T2 article becomes the 24-pane hexagon at 1:4. T1 tests the Rev D seam at the service load of 12 kN "
    "per bolt and at the upper bound. The 1:1 seam slices and the 550 mm article go ahead this fall as planned, to the Rev D section. "
    "See the Rev D pack on the blueprints page."
)

OCT_NOTE = (
    "Two design decisions, labelled Rev E, decided 23 October, drawings 8 November. The pressure pane becomes 22 mm BOROFLOAT 33 on "
    "531 mm panes: each 2,250 mm triangle is split into 16 panes, 96 per hexagon and 1,920 on the shell, because the glass makers can "
    "finish a square no larger than 787 mm and a smaller pane makes the glass thinner and safer. 708 mm panes are the upside and 425 mm the "
    "fallback; the pick is final once T0 measures how much the glass strength scatters. The seal becomes two butyl BA500 loops with the "
    "RTV566 bead kept as the third seal, in place of fluorosilicone cord, on Parker's advice. The blueprints and the 3D model stay Rev D "
    "until the 8 November pack. Cabin pressure stays 1 atm. "
    "Three things in the test plan change. The glass test moves from discs to bars in four-point bend, 1 in by 1/8 in, the way ENGN 1440 "
    "runs it, in spring 2027: the disc fixture would cost thousands, and the small frame at Brown is 0.5 kN, not the 5 kN the plan assumed. "
    "The seam pulls move to late January to February 2027 on the 100 kN frame at Brown, which is free after 18 November; Dewesoft lends the "
    "16-channel strain recorder in 3 to 4 week batches with a month's notice. This fall is fabrication. "
    "And one rule: every physical test is completed on the computer first, and nothing is machined before its digital twin has a signed sheet."
)

SUPPLIER_LIMITS = [
    "SUPREMAX 33: rolled at 34.9 mm in 1,000 x 1,500 mm sheets; ground and polished to 29.4 mm at 787 x 787 mm, the largest part Swift Glass can finish (SCHOTT, Tina Gallo, 20 Oct; Swift Glass, Charlie Burke, 14 and 20 Oct).",
    "BOROFLOAT 33: 25.4 mm in 1,150 x 850 mm sheets; 21 mm in 1,700 x 1,300 mm; 15 mm in 2,300 x 1,700 mm (SCHOTT, 20 Oct).",
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
<p class="eyebrow">The plan, fall 2026. Written {REVS_DATED}, Rev D note added {REVD_DATED}, updated {UPDATED}</p>
<h1>This fall we build the seam between two panels. We pull it apart in January.</h1>
<p class="lead">We take the joint where two panels meet from a design on paper to hardware we have built and measured, and we do the analysis it depends on (loads, glass strength, frame material) so the tests mean something. Every test runs on the computer first.</p>
<p style="margin-top:24px"><a class="btn" href="#need">What we need from sponsors</a><a class="btn" href="/blueprints/">See the blueprints</a><a class="btn" href="{PDF_REVD}">Rev D blueprint pack (PDF)</a></p>
</div></header>

<section id="oct" style="padding:32px 0"><div class="wrap">
<p class="eyebrow">23 Oct 2026: what the October meetings changed</p>
<p>{e(OCT_NOTE)}</p>
<p class="label" style="margin-top:18px">Supplier limits, for the pane sizes under study</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in SUPPLIER_LIMITS)}</ul>
</div></section>

<section id="revd" style="padding:32px 0"><div class="wrap">
<p class="eyebrow">14 Oct 2026: Rev D</p>
<p>{e(REVD_NOTE)}</p>
<p class="muted">The sizes below this note are from the {REVS_DATED} plan and are kept as written; where they differ, the Rev D pack is current and the 23 October note above is newer still. The test cards and dates below were updated on {UPDATED}.</p>
</div></section>

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
<li>Every test as a 23-minute film, with how each piece is made, what the test tells us, plan B, cost and dates, is on the <a href="/tests/">tests page</a>.</li>
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
<div class="tablewrap"><table class="stack"><thead><tr><th>Date</th><th>What</th><th><span class="sr">Status</span></th></tr></thead><tbody>{ms}</tbody></table></div>
<p class="muted" style="margin-top:16px">After this fall: in late January and February 2027 we pull the T1 slices in the 100 kN frame; in spring 2027 we break the T0 bars, run T2 under water pressure, check the computer model against all of them, and design the corner seal. In spring 2028 the work becomes a capstone project.</p>
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
