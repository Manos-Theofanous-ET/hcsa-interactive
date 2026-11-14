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
PDF_REVF_1 = "/downloads/HCSA-Rev-F-sheets-RF-01-to-RF-04-5-Nov-2026.pdf"
PDF_REVF_2 = "/downloads/HCSA-Rev-F-sheets-RF-05-to-RF-09-14-Nov-2026.pdf"
PDF_REVF_TP = "/downloads/HCSA-Rev-F-test-pieces-TP-00-to-TP-04-9-Nov-2026.pdf"
ZIP_REVF_TP = "/downloads/HCSA-Rev-F-test-pieces-STEP-9-Nov-2026.zip"
PDF_REVF_PKG = "/downloads/HCSA-Rev-F-release-package-14-Nov-2026.pdf"
PDF_REVF_PKG1 = "/downloads/HCSA-Rev-F-release-package-one-page-summary-14-Nov-2026.pdf"
REVF_DATED = "9 November 2026"
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
    nav = [("/team/", "HCSA team", "brand"), ("/plan/", "The plan", ""), ("/blueprints/", "Blueprints", ""),
           ("/tests/", "The tests", ""), ("/#work", "Our work", "wide-only"), ("/#sponsor", "Sponsor", "")]
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
<p>Human-Centric Space Architecture (HCSA) is a student research project at Brown University. It is supported by a Brown UTRA award and developed with RISD. Our faculty advisor is Prof. Rick Fleeter, and our project lead is Manos Theofanous.</p>
<p>We updated this page on {UPDATED}. The Rev D sheets are drawn from the Rev D design spec of {REVD_DATED}. The Rev S drawings of {REVS_DATED} come from the CAD model, and we keep them for reference. Every dimension is in millimetres.</p>
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
         "t550": "T1 550 mm piece", "t2p": "T2 panel at 1:4 scale", "t2r": "T2 water rig"}


# Rev F sheets (public/blueprints/img/revf-<id>.webp). RF-01 to RF-04 are from 5 Nov 2026, RF-05 to RF-09 and the
# test-piece sheets TP-00 to TP-04 from 8 Nov 2026. Make the images with convert_revf_sheets.py.
REVF_SHEETS = [
    ("rf-01", "Sheet RF-01", "Main rib option B (I 400 x 100 x 25, web 8) and the secondary rib (I 180 x 60 x 10, web 5), cut through, with the 21 mm panes seated and the glass bite on each. The notes give the two new requirements: the star-plate nodes must hold the main rib sideways, and the panes need a launch answer."),
    ("rf-02", "Sheet RF-02", "A section through one seam: the 180 mm frame, the two 7.1 x 4.0 mm glands with the butyl cords, the RTV bead and the NAS6705U27 bolt at 4 kN. On the right, the seal loop ends against Parker's R16 minimum. Moving the bolt row to make room failed the 5 November seam run, so the loop corners are still open."),
    ("rf-03", "Sheet RF-03", "The T1 seam slices (75, 150 and 225 mm) and the 550 mm piece with a dummy hardpoint, redrawn at 180 mm deep with the bolt row at z' 58."),
    ("rf-04", "Sheet RF-04", "The docking transfer lock, a concept: the module at 0.8 atm, the 1 atm host station, the hatch that stays shut while the pressures differ, the equalising valves and our own relief valve."),
    ("rf-05", "Sheet RF-05", "A hexagon-to-hexagon seam cut through at the first bolt, 271 mm from the corner. It shows the 180 mm frame, the two butyl glands at z' 18 and 32, the RTV bead at z' 42, the seam bolt at z' 58, the corner tie rows and both hardpoint positions, as drawn at z' 110 to 170 and moved onto the line of the pull at z' 46 to 106. A table turns every depth on the joint face into the panel's own depth, for the hexagon mitre of 20.9 degrees and the pentagon mitre of 16.5 degrees, so the holes line up on hexagon-to-pentagon seams too."),
    ("rf-06", "Sheet RF-06", "The hexagon panel seen from the cabin side at Rev F: 6 main ribs, 108 secondary rib segments on the 562.5 mm grid, 96 panes of 531 mm, 18 six-way star-plate nodes, 3 hardpoints on every edge at the quarter points, and the 16 seam bolts on one edge. The parts list gives the mass of every part, now with the corner blocks, the hardpoint fittings and the rib braces: about 1.9 t for a hexagon with its glass. That does not yet agree with the 36.1 t of the shell model, and the sheet says so."),
    ("rf-07", "Sheet RF-07", "The hardpoint fitting, redrawn on 9 November from the October model: a titanium lug on one panel reaching into a two-cheek clevis on the other, with three 40 mm pins along the panel depth. Where it was first drawn, the frames hinge about it and the seals open at 0.22 to 0.47 atm against the 1.93 atm required. On the line of the pull the seal holds, and the slot for the lug clears the seals and the seam bolts. But in the 180 mm frame the fitting runs into the outer flange and the ribs, and its pins cannot be put in, so the part has to be redrawn. The position is decided with Rick on 10 November."),
    ("rf-08", "Sheet RF-08", "The corner node in plan and on the joint face, with the 7/8-14 Inconel 718 ties preloaded to 198 kN by measured stretch. The corner model gives the worst tie at proof, at 0.8 atm, as 214.5 kN against a limit of 227 kN, and 226.3 kN with the hatch open at 1 atm. The blocks now have their real leaning joint faces: three of them placed at a vertex fit with every tie hole on axis. The ties sit 130 and 186 mm from the vertex line, inside corners are R10, and the block is machined from plate. The P-11 brace that holds the main rib sideways is the proposal at the bottom."),
    ("rf-09", "Sheet RF-09", "The pentagon panel seen from the cabin side: 5 main ribs, 90 secondary rib segments, 5 corner blocks of 108 degrees, 15 hardpoints, and the 10 mm closure plate as five triangles sealed at the main ribs. The notes give what the pentagons do, where the solar cells have to stand off the structure, and the open questions, the first being which side of the frame the closure plate sits on."),
    ("tp-00", "Sheet TP-00", "The cover of the test-piece set: what each piece is for, the notes for the shop, the tolerance table with the loose and tight limits Marco asked us to separate, and the bill of materials for the whole set."),
    ("tp-01", "Sheet TP-01", "Frame B of the T1 seam slice, the grooved half: the 180 mm section with the two 7.1 x 4.0 mm glands, the RTV recess and the leak-test port, the joint face with the bolt holes, and the table of leg holes for the 75, 150 and 225 mm slices."),
    ("tp-02", "Sheet TP-02", "Frame A, the plain half, and the two frames assembled with the pull block on each side. The two pull lines are drawn: run 1 pulls through the block centre at z 90, run 2 through a pin on the z 24 line near the outer flange, which pries the seam open the way pressure does."),
    ("tp-03", "Sheet TP-03", "The 550 mm article with its dummy hardpoint, drawn at both fitting depths, as drawn and moved onto the pull line, with its 2 + 2 seam bolts and the three 40 mm pins at 60 mm pitch."),
    ("tp-04", "Sheet TP-04", "The pull blocks and the fixture: every face of the block with its holes, the M24 pull hole at the centre and the M12 pattern, and the three fixture pieces F-01 to F-03 that put the article in the 100 kN frame."),
]

REVF_INTRO = (
    "In November we made the ribs thinner and lowered the cabin pressure. The main rib is option B, an I-beam 400 mm "
    "deep with 100 mm flanges, and the secondary ribs are 180 by 60 mm, so about 61 percent of each window is open "
    "glass. The cabin runs at 0.8 atm with 26 percent oxygen, which gives the same oxygen pressure as at sea level and "
    "takes about a fifth of the load off the structure. The station is designed as a module for a 1 atm commercial "
    "station, which it joins through a small transfer lock. The pressure pane is 21 mm BOROFLOAT 33, the thickness "
    "SCHOTT makes as a standard sheet, in 531 mm panes, 96 to a hexagon. The frame is 180 mm deep, the seals are two "
    "loops of butyl in 7.1 by 4.0 mm grooves with an RTV bead behind them, and the seam bolts are NAS6705U27 at 4 kN. "
    "The corner ties are preloaded to 198 kN. The shell model weighs 36.1 t; the parts lists add up to more and are being reconciled.",
    "The computer tests of 4 and 5 November ran on this design. The corners pass at 0.8 atm, with the worst tie at "
    "214.5 kN at proof against a limit of 227 kN, and they still pass, only just, if the hatch is left open and the "
    "cabin goes to 1 atm. The seams pass with about 40 percent margin. The hardpoint test of 6 and 7 November found "
    "that the fitting as drawn acts as a hinge and lets the seals open, and that moving it onto the line of the pull "
    "fixes that. Two things are still open: how the seal loops turn their corners, and how the panes are held at launch.",
    "On 8 November we added five more sheets for the release to Marco Cross: the seam section with the depth table, the hexagon and pentagon panels as they now are, the hardpoint and the corner node with the machining points from his review. The five test-piece sheets, TP-00 to TP-04, are the drawings the shop quotes from, and the STEP files of every test piece go with them. On 9 November an independent check corrected them: the corner blocks were rebuilt with their leaning faces so that three fit at a vertex, the hardpoint fitting was redrawn from the October model, and the test-piece files were rebuilt with the drilled hole sizes on sheet TP-00.",
)


# Rev D sheets (public/blueprints/img/revd-NN_slug.webp, from the Rev D blueprint pack, 14 Oct 2026).
REVD_SHEETS = [
    ("00_cover", "Sheet 00", "The cover, with an index of the 13 sheets, what changed from Rev S to Rev D, how the drawings are drawn, and the four status tags: LOCKED, FEA, PROPOSAL and OPEN."),
    ("01_shell", "Sheet 01", "The shell from the side and from above, with the name of each panel. It has 20 hexagons, 12 pentagons, 90 seams and 60 corners. It is 11,151 mm across, and every edge is 2,250 mm long."),
    ("02_hex_plan", "Sheet 02", "A hexagon panel seen from the cabin side. It has 6 main ribs running from the centre to each corner, 18 secondary ribs 1,125 mm long, and 24 triangular panes 1,125 mm on a side."),
    ("03_hex_section", "Sheet 03", "A cut along a main rib from a corner to the centre, labelled section A-A. It shows the 375 mm main rib, the 140 mm edge frame and the 25.4 mm pressure pane on its seat."),
    ("04_rib_sections", "Sheet 04", "Cuts through the ribs, which are I-beams. The main hexagon rib is 375 mm deep, with flanges of 200 by 15 mm and an 8 mm web. The main pentagon rib is 400 mm deep, with flanges of 80 by 25 mm and an 8 mm web. The secondary rib is 160 mm deep, with flanges of 64 by 8 mm and a 6 mm web. We allow a stress of 160 MPa in them."),
    ("05_seam_joint", "Sheet 05", "The seam joint cut open. It shows frames A and B, the 5/16-24 A286 bolt every 75 mm that clamps the seals, two 5.33 mm cords in grooves of 7.1 by 4.0 mm, and the RTV566 bead. It also shows where the load goes. Of the 623 kN on each seam, 63 percent goes to the corner nodes, 31 percent to the hardpoint and 5 percent to the bolts."),
    ("06_corner_node", "Sheet 06", "The corner node, seen from above the corner and cut along a seam. This is a PROPOSAL. Each panel corner gets one machined 6061-T651 block of 5.8 kg, which takes the first 100 mm of both frames. On each joint face, 4 tie bolts of 5/8-18 A286 hold the blocks together for 196 kN, in tension only. The bending at the corner passes from block to block through the faces where they touch."),
    ("07_hardpoint", "Sheet 07", "The hardpoint halfway along the seam, 1,125 mm from the corner, seen from above and cut open. This is a PROPOSAL. A 40 mm lug on frame A sits between the 2 plates of a clevis on frame B, each 25 mm thick, and a 40 mm A286 pin joins them. At 195 kN the pin bends with a stress of 349 MPa, and a 30 mm pin would be past yield. The hardpoint carries 152 to 195 kN across the seam and no bending. The lug and clevis sit below the three lines of seals."),
    ("08_glazing", "Sheet 08", "The layers of glass, and the edge of the pane where it sits in the frame. From the outside in, there is a 6 mm fused silica pane against space dust, a 12 mm gas gap, the solar cell and tint layers, the shutter, and the 25.4 mm BOROFLOAT 33 pressure pane. The pressure pane rests on a 2 mm strip, and the frame overlaps its edge by 20 mm."),
    ("09_pent_plan", "Sheet 09", "A pentagon panel seen from the cabin side, with 5 main ribs, 15 secondary ribs, 20 bays and a 10 mm face plate. The plate was 4 mm in Rev S. The panel weighs 651 kg before the solar, shield and docking equipment goes on."),
    ("10_test_articles", "Sheet 10", "The test pieces drawn against the full facility. T0 bends glass bars at four points. T1 uses full-size seam slices and the 550 mm piece. T2 is the hexagon with 24 panes at 1:4 scale, and T3 is one corner at full size."),
    ("11_materials_mass", "Sheet 11", "Materials, heat treatment and mass. The prototype uses 6061-T651 aluminium, and flight parts would use 2219-T851. The bolts are A286 and the glass is BOROFLOAT 33. A hexagon weighs 1,838 kg and a pentagon 651 kg. The structure weighs 34.0 t, and the facility 50.4 t with every item counted."),
    ("12_open_decisions", "Sheet 12", "The decisions still open, and which test or model settles each one. They are whether the hardpoint is pinned or stiff, the glass thickness, the seal cord, the bolt part number, the bow of the frame, the corner seal, the tie and pin sizes, the mass, the shear key, and the safety factor we design to."),
]

REVD_INTRO = (
    "From 9 to 12 October we ran a stress model of the whole shell in three different programs, and it was reviewed "
    "independently. It showed that the Rev S design cannot hold 1 atm. In the six-pane hexagon, the 31 mm glass reaches "
    "54 MPa, against the 35 MPa we allow, and it bends 7.3 mm, against a limit of 3.1 mm. The 103 mm ribs go far past "
    "yield, the point where the metal bends for good. And the open corners put 100 to 138 kN on the end bolts, which "
    "break at 34 kN.",
    "Rev D takes a route the spec already allowed for. Each hexagon is split into 24 triangular panes, 1,125 mm on a side, "
    "on main ribs 375 mm deep and secondary ribs 160 mm deep. The pressure pane is 25.4 mm BOROFLOAT 33. Air pressure "
    "pulls across each seam with 623 kN. That pull goes through a solid machined block at every corner, the corner node, "
    "and a pinned fitting halfway along every seam, the hardpoint. Both are proposed details, sized on 16 October. So "
    "the 26 bolts along a seam only clamp the seals. The structure weighs 34.0 t, and the whole facility about 50.4 t.",
    "Every item on the sheets has a status tag. LOCKED means the geometry has not changed since Rev S. FEA means our "
    "computer stress models set it in the October runs. That covers the rib sections, the glass thickness, the number of "
    "panes and how the load is split. PROPOSAL means a detail drawn to carry a load from the models. It was sized in the "
    "models of 16 October and still has to pass a physical test. The proposals are the corner node and its tie bolts, "
    "the hardpoint, the count of 26 bolts and the wider seal grooves. OPEN means a decision we have not taken yet, with "
    "the Rev D default stated. Rev D listed ten open decisions, and they are at the bottom of this page. Rev D is the "
    "signed version of TRUTH, our master spec.",
)

OPEN_ITEMS = [
    "The hardpoint halfway along the seam can be pinned, which is the Rev D default, or stiff enough to carry bending. That choice sets the secondary rib at 160 or 200 mm deep. Submodel C3, a detailed computer model of the hardpoint, covered it on 16 October.",
    "We decided the pressure glass on 23 October, for Rev E. It is 22 mm BOROFLOAT 33 in 531 mm panes, 16 to each 2,250 mm triangle and 96 to a hexagon. If the glass proves very consistent we can go up to 708 mm panes, and if it scatters a lot we go down to 425 mm. We make the final pick after the T0 bars give us the Weibull modulus m, the number that says how much the strength of the glass varies. The drawings come out on 8 November. Until then the Rev D sheets above show 25.4 mm glass in 1,125 mm panes.",
    "We decided the seal on 23 October, for Rev E. It is two closed loops of butyl BA500, with the RTV566 bead as a third seal. On Parker's advice we dropped the fluorosilicone cord. The drawings come out on 8 November.",
    "The part number of the seam bolt is still open. The old number, NAS9306C-06, is a rivet standard and the wrong size. The parts memo of 1 November names the right bolt.",
    "How much the frame bows between corners is still open. The models predict 1.4 to 2.0 mm, against a limit of 1 mm for the seals to work. The default is to keep the frame 140 mm deep and test it, and the other choice is to make it deeper. We decide after T1 and submodel C2.",
    "The corner seal is still open. It sits in the plug at the corner point, where the three seal loops meet.",
    "The tie bolts at each corner and the 40 mm hardpoint pin are still open. The ties carry tension only, and the bending at the corner goes through the faces of the blocks. Submodels C1 and C3 covered them on 16 October.",
    "The mass is still open. In Rev D the structure weighs 34.0 t and the facility 50.4 t, up from a Rev S figure that did not hold. The next step to bring it down is a rib study aimed at clearer views, with narrower and deeper ribs.",
    "Rev D has no shear key, the part that stops the two frames of a seam sliding along each other. The dowels at the corners and the hardpoint pin carry that sliding load instead. We bring the shear key back only if submodel C2 or the shear check on the whole shell needs it.",
    "The safety factor is still open. So far we have used 1.5 on yield at 1 atm. The other choice is the NASA-STD-5001 rule, with 1.5 at proof and 2.0 at ultimate failure. We agree this with our faculty advisors before the 8 November drawings.",
]

OPEN_ITEMS_REVS = [
    "Bolts per seam: the model has 29 (with 30 the end nuts clash at every pentagon corner); the specification says about 30. Needs a decision.",
    "The corner seal: the O-rings of the three seams stop 30 mm short of each corner, and nothing seals the small triangle between them yet.",
    "The ribs in the full-size panels are the old ones and far too weak as spokes. A rib study this fall makes them deeper or adds a ring. Until then the model mass (about 26,700 kg) is not an estimate.",
    "How the whole shell shares the load between panels, seams and corners. The FEA size study answers it.",
    "The pentagon housing, the solar panels and the fold-out shields are not designed yet, and a shield folding out puts loads into the pentagon frame that no test here covers.",
    "The exact bolt part number (the fastener memo is due 1 November), and the T2 frame split into bars before the drawings are released.",
]


def revf_thumbs():
    out = []
    for sid, kind, note in REVF_SHEETS:
        stem = f"revf-{sid}"
        w, h = SIZES[stem]
        cap = f"{kind}. {note}"
        out.append(
            f'<figure><button type="button" data-full="/blueprints/img/{stem}.webp" data-cap="{e(cap)}" aria-label="Open {e(kind)} full size">'
            f'<img src="/blueprints/img/{stem}-thumb.webp" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{e(cap)}"></button>'
            f'<figcaption><span class="kind">{e(kind)}</span>{e(note)}</figcaption></figure>')
    return "".join(out)


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
<p class="eyebrow">Blueprints, Rev F working baseline, {REVF_DATED}</p>
<h1>The shell, the joint and the tests, with dimensions.</h1>
<p class="lead">{e(ov["intro"])} Rev F is our working baseline of November 2026. It keeps the Rev D layout, with 96 glass panes per hexagon on deep ribs, a solid node at every corner and a hardpoint along every seam, and it makes the ribs thinner, the frame deeper and the cabin pressure 0.8 atm. Rev D, signed on 14 October 2026, is the last full set below it.</p>
<ul class="facts"><li>11,151 mm across</li><li>2,250 mm edges</li><li>20 glass hexagons with 96 panes each</li><li>12 solid pentagons</li><li>90 seams and 60 corners</li><li>1,440 bolts that clamp the seals</li><li>0.8 atm inside</li></ul>
<p style="margin-top:24px"><a class="btn" href="{PDF_REVF_1}">Rev F sheets RF-01 to RF-04 (PDF)</a><a class="btn" href="{PDF_REVF_2}">Rev F sheets RF-05 to RF-09 (PDF)</a><a class="btn" href="{PDF_REVF_TP}">Test-piece sheets TP-00 to TP-04 (PDF)</a><a class="btn" href="{PDF_REVD}">The Rev D blueprint pack (PDF)</a><a class="btn" href="/plan/">Read the plan</a></p>
<ul class="toc" aria-label="Jump to"><li><a href="#revf">Rev F sheets</a></li><li><a href="#revd">Rev D sheets</a></li><li><a href="#revs">Rev S drawings</a></li>{toc}<li><a href="#open">Still open</a></li></ul>
</div></header>
<section id="revf" class="subject"><div class="wrap">
<p class="eyebrow">The current baseline</p>
<h2>Rev F, the working baseline of November 2026</h2>
<p class="tested">Fourteen sheets at A3 size: nine of the facility and five of the test pieces. Click any sheet to open it full size. They are drawn from our parameter file, and the facility sheets are not yet checked for machining.</p>
{"".join(f"<p>{e(t)}</p>" for t in REVF_INTRO)}
<p class="muted">The Rev D sheets below are the last full signed set. Where they disagree with these sheets, the Rev F sheets win.</p>
<p><a class="btn" href="{PDF_REVF_1}">Sheets RF-01 to RF-04 (PDF, 5 November)</a><a class="btn" href="{PDF_REVF_2}">Sheets RF-05 to RF-09 (PDF, 14 November)</a><a class="btn" href="{PDF_REVF_TP}">Test pieces TP-00 to TP-04 (PDF, 9 November)</a><a class="btn" href="{ZIP_REVF_TP}">Test pieces, STEP files (zip, 1.3 MB)</a><a class="btn" href="{PDF_REVF_PKG}">The release package for Marco (PDF, 14 November)</a><a class="btn" href="{PDF_REVF_PKG1}">The package on one page (PDF)</a><a class="btn" href="/tests/">The physical test plan (updated 14 November)</a><a class="btn" href="/parts/">The parts library</a></p>
<div class="thumbs">{revf_thumbs()}</div>
</div></section>
<section id="revd" class="subject"><div class="wrap">
<p class="eyebrow">The last full set</p>
<h2>Rev D, 14 October 2026, the design sized by our stress model</h2>
<p class="tested">There are 13 sheets at A3 size. Click any sheet to open it full size.</p>
{"".join(f"<p>{e(t)}</p>" for t in REVD_INTRO)}
<p class="muted">On 23 October we took two of the open decisions for Rev E, the next version of the spec, with drawings due on 8 November. The pressure pane becomes 22 mm BOROFLOAT 33, in 531 mm panes, 96 to a hexagon. The seal becomes two loops of butyl BA500 with the RTV566 bead behind them. Until the new drawings come out, the sheets below show the Rev D pane and seal. The plan page gives the reasons.</p>
<div class="thumbs">{revd_thumbs()}</div>
</div></section>
<section><div class="wrap grid2">
<div><h2>How to read the drawings</h2><ul class="dots"><li>Each Rev D sheet is one A3 drawing. Its title block gives the sheet, the material and heat treatment of the parts on it, and the status of every item as LOCKED, FEA, PROPOSAL or OPEN. The sheets are not to scale, so read the dimensions.</li>{"".join(f"<li>{e(t)}</li>" for t in ov["reading"])}</ul>
<p class="muted">Click any drawing to open it full size. The arrow keys on your keyboard step through them.</p></div>
<div><h2>How the pieces fit</h2>
<p>The shell is made of 32 panels. Each panel has a frame along each edge. Two frames bolted together make a seam, and three seams meet at a corner. The stress model of the whole shell, run from 9 to 12 October, shows how the load is shared. Most of the pull across a seam goes into the corner nodes and about a third into the hardpoint halfway along the seam. The bolts only clamp the seals.</p>
<p>We test the parts that decide whether the shell holds. T1 tests the seam. We build it this fall and pull it apart at the Rev D load in late January and February 2027. T0 tests the glass by bending bars at four points in spring 2027. T2 tests one hexagon panel at 1:4 scale in spring 2027, and T3 tests a corner in 2027. Every test runs on the computer first, and nothing is machined until its digital twin, the computer model of that test, has a signed sheet. A test passes when the measurement comes within 10 percent of the prediction.</p>
<p class="muted">Rev D is a design in progress, not a design ready to fly. The open decisions are listed at the bottom of this page.</p></div>
</div></section>
<section id="revs" class="subject" style="padding-bottom:0"><div class="wrap">
<p class="eyebrow">For reference</p>
<h2>Rev S drawings, used from 25 April to 14 October 2026 and now out of date</h2>
<p class="muted">These sections are out of date. They show the Rev S design as it stood on {REVS_DATED}, with six glass panes per hexagon on 103 mm ribs, 31 mm glass, 29 bolts per seam carrying the whole pull across the seam, and open corners. The stress model of the whole shell showed that this design does not hold 1 atm, and Rev D above replaces it. We left the Rev S text and numbers as they were, so you can follow the change. Since then the T0 disc test has become a bar test, and the T2 panel now has 24 panes.</p>
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
<p class="muted">Rev D left ten decisions open, each with a default. We took two of them on 23 October for Rev E, the pressure glass and the seal, so eight are still open.</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in OPEN_ITEMS)}</ul>
<p style="margin-top:20px"><a class="btn" href="{PDF_REVD}">The Rev D blueprint pack (PDF)</a><a class="btn" href="{PDF_REVD_SPEC}">The Rev D design spec (PDF)</a><a class="btn" href="{PDF}">The Rev S drawings, explained (PDF, out of date)</a><a class="btn" href="/plan/#need">What we need from sponsors</a></p>
</div></section>""")
    return page("HCSA blueprints, Rev F",
                "The Rev D drawing sheets of 14 October 2026 and every older Rev S drawing of the HCSA shell, panels, seam joint, corner and test pieces, each with dimensions and a plain explanation.",
                "/blueprints/", "".join(parts), lightbox=True)


# ---------------------------------------------------------------- plan
MILESTONES = [
    ("27 September", "15 requirements for the seam, each with its source", "Sent to advisor"),
    ("27 September", "The load cases for the seam, with the two hand estimates brought into agreement", "Sent to advisor"),
    ("4 October", "The glass and frame materials, chosen from published design data", ""),
    ("11 October", "The design strength of the glass, from published data scaled up to a full pane. The T0 bars check it in spring 2027.", ""),
    ("12 October", "A stress model of the whole shell in three different programs, which gave the Rev D sizes on 14 October", "Done"),
    ("23 October", "We decided the pane and the seal for Rev E. The glass is 22 mm thick in 531 mm panes, and the seal is two butyl loops and a silicone bead.", "Decided"),
    ("1 November", "The parts memo, with the bolt part number confirmed", ""),
    ("8 November", "We release the drawings, parts list and quotes, which make up the Rev E pack, and decide whether to go ahead and build. Nothing is machined until its digital twin has a signed sheet.", ""),
    ("18 November", "The 100 kN load frame at Brown becomes free", ""),
    ("22 November", "The test plan for spring 2027, with test dates set with Dewesoft for the loan of the strain recorder", ""),
    ("6 December", "If the shop delivers on time, we build the 550 mm joint piece and measure bolt tension against how much the seal is squeezed.", ""),
    ("11 December", "The fall report, 10 to 15 pages long", ""),
    ("Late January to February 2027", "We pull the seam slices apart in the 100 kN frame, with the strain recorder on loan from Dewesoft.", ""),
]

TESTS = [
    ("t0", "T0: how strong is our glass?", "3d_render-17_T0_ring_on_ring",
     "We bend borosilicate glass bars, 1 inch wide and 1/8 inch thick, at four points until they break, the way the ENGN 1440 class does it. We break 30 or more for each edge finish, so we learn the real strength and how much it scatters. That scatter picks the final pane size. We plan on 531 mm, can go to 708 mm if the glass is consistent, and drop to 425 mm if it is not. We have dropped the disc test drawn here. Its fixture would cost thousands, and the small frame at Brown only goes to 0.5 kN, not 5 kN. We keep the BOROFLOAT discs from Precision Glass & Optics and the 15 sapphire discs from Meller Optics for a second look.",
     "This happens in spring 2027, in ENGN 1440, the Brown materials lab course. We are still deciding whether to break a first set of bars this fall on the 0.5 kN frame."),
    ("t1", "T1: does the seam hold when it is pulled apart?", "3d_render-10_T1_slice_150",
     "We pull full-size slices of the seam, 75, 150 and 225 mm long, in the 100 kN load frame at Brown, and check the seal between the two butyl loops while we pull. A 550 mm piece of the seam checks that it goes together and holds air. On 23 October we changed the seal to two butyl BA500 loops and the silicone bead, in place of fluorosilicone cord. Parker advised this, because a closed loop has no cut ends that could leak at the corners.",
     "The Rev F test pieces are drawn (sheets TP-00 to TP-04, 9 November). We make them once the money is in and pull them in late January and February 2027. The frame is free after 18 November, and Dewesoft lends the 16-channel strain recorder in batches of 3 to 4 weeks, booked a month ahead."),
    ("t2p", "T2: how does a window panel bend?", "3d_render-14_T2_rig_pinned",
     "We load a hexagon panel at quarter scale, 1.1 m across, with water in a steel tub, up to 2 atm. It has aluminium panes in place of glass. The test shows how the panes bend onto the frame and ribs. The test piece is being redrawn on the Rev F grid, and it needs its own funding and a host.",
     "This happens in spring 2027."),
    ("shell", "FEA: how does the whole shell share the load?", "3d_render-02_shell_cutaway",
     "FEA means our computer stress models. We model one panel, a cap of seven panels and the full shell. They tell us how much load the seams and corners really carry, and that sets the bolt size.",
     "These models ran from 9 to 12 October and set Rev D. Every physical test now gets its own computer twin first, and nothing is machined before that twin has a signed sheet."),
]

# What we need, grouped by test. (item, size and quantity, needed by)
NEEDS = [
    ("For T0, the glass bars", [
        ("Borosilicate glass bars (Borofloat 33)", "The bars are 1 inch wide, 1/8 inch thick and about 4 inches long, with the same edge finish within a set. We need 30 or more for each edge finish. Swift Glass has quoted about $1,040 for 100 bars. We already have BOROFLOAT discs from Precision Glass & Optics and 15 sapphire discs from Meller Optics.", "Early 2027"),
        ("A four-point bending fixture", "We need the ENGN 1440 fixture, or one like it, that fits a 0.5 kN frame.", "Early 2027"),
    ]),
    ("For T1, the seam slices and the 550 mm joint piece", [
        ("6061-T651 aluminium, and CNC machining of 8 edge frames", "There are six slice frames, 180 mm deep and 75, 150 and 225 mm long, two of each, and the two frames of the 550 mm piece. The two butyl glands are 7.1 by 4.0 mm and the bolts are every 75 mm. The frames weigh about 40 kg in all. The STEP files and sheets TP-00 to TP-04 are ready (9 November).", "Once funded"),
        ("4140 steel pull blocks, quenched and tempered", "There are six blocks for the slices, 160 by 80 mm in section, and two 550 mm blocks for the long piece, about 200 kg in all; in 6061 aluminium they would be much lighter. A lug, fork and pin pry the joint open in the second run.", "Once funded"),
        ("5/16-24 bolts, with nuts and washers", "We need about 20 sets. Catalogue alloy steel bolts stand in for the NAS6705 flight bolt in every test piece, since at 4 kN the bolt's stiffness is what matters.", "Once funded"),
        ("Butyl seal loops (Parker BA500)", "Each joint takes two closed loops, spliced from extruded cord 0.210 inch thick, in glands 7.1 by 4.0 mm (sheets TP-00 to TP-04). We no longer need fluorosilicone cord.", "November"),
        ("RTV566 silicone with its primer", "We need one kit, plus a syringe and tips to lay a 3 mm bead.", "November"),
        ("Fixture hardware", "We have 60 M12 class 12.9 screws from Bolt Depot. We still need 2 m of M8 threaded rod with nuts, eight rubber-faced end dams, and the adapters to the load frame.", "Once funded"),
    ]),
    ("For T2, one panel at quarter scale and its water rig (sizes from the October article, being redrawn for Rev F)", [
        ("6061-T6 aluminium for the panel frame, six ribs and hub", "When finished it weighs about 31 kg and measures 1,217 by 1,054 by 124 mm. It is cut from 12 mm and 10 mm plate and bar, and the cut list comes with the drawings.", "January"),
        ("Six aluminium panes", "The panes are triangles of about 525 by 455 mm, cut from 8 mm (5/16 inch) 6061-T6 plate. One sheet of 1,220 by 2,440 mm covers all six. They are cut by laser or waterjet.", "January"),
        ("Steel plate for the rig, cut and welded", "We need about 490 kg of A36 or S355 steel. That covers a 25 mm floor of 1,222 by 1,058 mm, 12 mm walls 175 mm tall, and three hexagonal rings 1,409 by 1,220 mm outside, 25, 22 and 25 mm thick.", "January"),
        ("Rubber and small parts", "We need a 1 mm EPDM sheet of 1.5 by 1.3 m, 8 m of neoprene strip 1.5 by 10 mm, 24 M16 bolts of class 8.8 with nuts, six ground steel bars 12 mm thick and 548 mm long, a relief valve set at 220 kPa, brass fittings and a pressure gauge.", "January"),
    ]),
    ("For measuring", [
        ("Strain gauges", "TML is donating 30 gauges for the seam test, 15 rosettes and 15 single gauges. The count for T2 is still being settled. The 16-channel strain recorder comes on loan from Dewesoft, in batches of 3 to 4 weeks.", "T2 gauges by January"),
        ("Dial gauges or LVDTs, and a pressure sensor", "We need four gauges that measure how far a point moves, either dial gauges or LVDTs, their electronic version. We also need one pressure sensor that reads 0 to 300 kPa.", "January"),
    ]),
    ("Time, software and funds", [
        ("Test frame time", "We need the 100 kN frame at Brown for T1. It is free after 18 November, and it is booked for late January and February 2027. The T0 bars run on a 0.5 kN frame in spring 2027.", "Late January to February"),
        ("Software for computer stress models (FEA)", "Ansys and SolidWorks licences are donated, and the models run on a team laptop.", "Done"),
        ("Funding", "It pays for machining, the steel rig and anything not donated. Every dollar goes to parts and shop time.", "Any time"),
        ("Expert advice", "We would value a 20 minute review from someone who knows bolted joints, seals, structural glass or pressure testing.", "Any time"),
    ]),
]


REVD_NOTE = (
    "From 9 to 12 October we ran a stress model of the whole shell in three different programs. It showed that the Rev S "
    "design does not hold 1 atm, and Rev D replaces it. Rev D has 24 glass panes per hexagon on 375 mm ribs and 25.4 mm "
    "glass. It has a solid block at every corner, the corner node, and a pinned fitting halfway along every seam, the "
    "hardpoint. The bolts only clamp the seals.",
    "Three things in this plan change. T0, the glass test, moves from glass discs to borosilicate bars bent at four points, "
    "in the ENGN 1440 class in spring 2027. The test piece for T2, the panel test, becomes the hexagon with 24 panes, at "
    "1:4 scale. T1, the seam test, tests the Rev D seam at the normal working load of 12 kN per bolt and at the upper bound. The full-size seam slices and the 550 mm piece go "
    "ahead this fall as planned, cut to the Rev D section. The Rev D pack is on the blueprints page.",
)

OCT_NOTE = (
    "On 23 October we made two design decisions. Both go into Rev E, the next version of our spec, and its drawings come "
    "out on 8 November.",
    "The first is the glass. The pressure pane becomes 22 mm BOROFLOAT 33 in 531 mm panes. Each 2,250 mm triangle is "
    "split into 16 panes, so there are 96 per hexagon and 1,920 on the shell. We made this change because the glass makers "
    "can only finish thick glass in small sheets, and the largest polished square they can make is 787 mm. A smaller pane "
    "also carries less stress at the same thickness. If the glass is very consistent we can go up to 708 mm panes, and if "
    "it is not we go down to 425 mm. The choice is final once T0, our glass strength test, measures how much the strength "
    "of the glass scatters.",
    "The second is the seal. On Parker's advice we replace the fluorosilicone cord with two loops of butyl BA500, and we "
    "keep the RTV566 bead as a third seal. The blueprints and the 3D model show Rev D until the 8 November pack. The cabin "
    "stays at 1 atm.",
    "Three things in the test plan change. The glass test moves from discs to bars bent at four points, 1 inch by 1/8 "
    "inch, the way the ENGN 1440 class runs it, in spring 2027. The disc fixture would cost thousands, and the small frame "
    "at Brown only goes to 0.5 kN, not the 5 kN the plan assumed. The seam pulls move to late January and February 2027, "
    "on the 100 kN frame at Brown, which is free after 18 November. Dewesoft lends the 16-channel strain recorder in "
    "batches of 3 to 4 weeks, with a month's notice. This fall is for fabrication. We also follow one rule. Every physical "
    "test is completed on the computer first, and nothing is machined until its digital twin, the computer model of that "
    "test, has a signed sheet.",
)

SUPPLIER_LIMITS = [
    "SUPREMAX 33 comes rolled at 34.9 mm, in sheets of 1,000 by 1,500 mm. Ground and polished, it is 29.4 mm thick, and the largest piece Swift Glass can finish is 787 by 787 mm. (Tina Gallo at SCHOTT, 20 October, and Charlie Burke at Swift Glass, 14 and 20 October.)",
    "BOROFLOAT 33 comes at 25.4 mm in sheets of 1,150 by 850 mm, at 21 mm in sheets of 1,700 by 1,300 mm, and at 15 mm in sheets of 2,300 by 1,700 mm. (SCHOTT, 20 October.)",
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
        ("/assets/web/images-facility-render-day.webp", "The garden column, the ramp and the seating pods"),
    ]
    concept_html = "".join(f'<figure><img src="{s}" loading="lazy" alt="{e(c)}"><figcaption class="muted" style="font-size:15px;margin-top:8px">{e(c)}</figcaption></figure>' for s, c in concept)
    body = f"""
<header class="hero"><div class="wrap">
<p class="eyebrow">The plan for fall 2026. We wrote it on {REVS_DATED}, added the Rev D note on {REVD_DATED} and updated it on {UPDATED}.</p>
<h1>This fall we build the seam between two panels. We pull it apart in late January.</h1>
<p class="lead">We take the joint where two panels meet from a design on paper to hardware we have built and measured. We also do the analysis it depends on, for the loads, the glass strength and the frame material, so the tests mean something. Every test runs on the computer first.</p>
<p style="margin-top:24px"><a class="btn" href="#need">What we need from sponsors</a><a class="btn" href="/blueprints/">See the blueprints</a><a class="btn" href="#nov">What changed in November</a><a class="btn" href="{PDF_REVF_1}">Rev F sheets (PDF)</a></p>
</div></header>

<section id="nov" style="padding:32px 0"><div class="wrap">
<p class="eyebrow">What changed on 4 and 5 November 2026 (Rev F)</p>
<p>In the first week of November we took six more decisions. Together they make Rev F, our working baseline. TRUTH Rev F is drafted, and Prof. Fleeter still has to sign the cabin pressure, the safety factors and the change to leak before break.</p>
<ul class="dots"><li><b>Thinner ribs.</b> The secondary ribs are 180 by 60 mm (2 November) and the main rib is option B, 400 by 100 mm (4 November). About 61 percent of each window is now open glass, and the station is 3.8 t lighter than with option A.</li>
<li><b>The cabin at 0.8 atm.</b> The air is 81 kPa with 26 percent oxygen, the same oxygen pressure as at sea level. It takes about a fifth of the load off the structure, so with the thin ribs nothing yields below the ultimate load. The station is now a module for a 1 atm commercial station, such as Orbital Reef, and not for the ISS, which is being retired. It joins its host through a small transfer lock with a hatch that stays shut while the pressures differ, and it has its own relief valve.</li>
<li><b>21 mm glass.</b> SCHOTT told us on 4 November that 22 mm BOROFLOAT would need container loads, and 21 mm is a standard sheet of 1,700 by 1,300 mm. At 0.8 atm the 21 mm pane passes if the glass bars in the spring show a Weibull modulus of about 7.7 or more. It saves 0.6 t.</li>
<li><b>The seam.</b> The frame is 180 mm deep, the seal grooves are 7.1 by 4.0 mm, and the seam bolts are NAS6705U27 with a KFN670 nut, tightened to 4 kN. The corner ties are preloaded to 198 kN.</li></ul>
<p>The computer tests on this design ran on 4 and 5 November. The corner passes at 0.8 atm, with the worst tie at 214.5 kN at proof against 227 kN, and it still passes, by only 0.7 kN, if the hatch is left open and the cabin goes to 1 atm. The seam passes with about 40 percent margin. We tried moving the seam bolts 12 mm deeper to give the seal loops the rounder corners Parker asks for, and the seal then opened too far, so the bolts stay where they are and the loop corners are worked out in the corner block drawing instead. Two tests still have to give numbers: the seal at the hardpoints and the panes at launch.</p>
<p>The test plan does not change: glass bars in the spring, seam pulls in late January and February 2027. The test pieces are redrawn at 180 mm deep. <a href="/blueprints/#revf">The Rev F sheets</a> show the new parts.</p>
</div></section>

<section id="oct" style="padding:32px 0"><div class="wrap">
<p class="eyebrow">What the October meetings changed (23 October 2026)</p>
{"".join(f"<p>{e(t)}</p>" for t in OCT_NOTE)}
<p class="label" style="margin-top:18px">What the glass makers can supply, for the pane sizes we are studying</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in SUPPLIER_LIMITS)}</ul>
</div></section>

<section id="revd" style="padding:32px 0"><div class="wrap">
<p class="eyebrow">Rev D (14 October 2026)</p>
{"".join(f"<p>{e(t)}</p>" for t in REVD_NOTE)}
<p class="muted">The sizes below this note come from the plan of {REVS_DATED}, and we have kept them as written. Where they differ, the Rev D pack is current, and the 23 October note above is newer still. We updated the test cards and dates below on {UPDATED}.</p>
</div></section>

<section id="concept"><div class="wrap">
<p class="eyebrow">The concept</p>
<div class="grid2">
<div><h2>A room in orbit made mostly of windows.</h2>
<p>HCSA is a design for a facility in low Earth orbit, for short visits. Nobody lives there. People come to look at Earth, move around, meet, do research and spend time among plants.</p>
<p>Its wall is made of 32 flat panels, in the shape of a football. The 20 hexagons are glass, and they are the windows. The 12 pentagons are solid, and they hold the solar panels and the shields that fold out over the windows around them. Every window borders three pentagons, so a shield can reach every one.</p>
<p>Inside is air at normal pressure and outside is vacuum, so the air pushes out on every panel, with about 1.07 meganewtons on each hexagon at 0.8 atm. This fall's work is about holding that push at the seams and through the glass.</p></div>
<div><ul class="facts" style="margin-top:0"><li>11.15 m across</li><li>2.25 m edges</li><li>630 m³ inside</li><li>32 panels</li><li>90 seams</li><li>0.8 atm inside, vacuum outside</li></ul>
<p class="muted" style="margin-top:18px">More concept art, the 3D model and our physical model are on the <a href="/story/#work">earlier scroll site</a>.</p></div>
</div>
<div class="grid3 concept" style="margin-top:26px">{concept_html}</div>
</div></section>

<section id="now"><div class="wrap grid2">
<div><p class="eyebrow">Where we are</p><h2>The design is simple enough to build.</h2></div>
<div><ul class="dots">
<li>In Rev S we redesigned the panel joint to be simple. Two aluminium frames are bolted face to face, with one row of bolts every 75 mm, two O-rings and a bead of sealant.</li>
<li>We modelled the whole shell in CAD, with 32 panels, 90 seams, 2,610 bolts and every seal, and no parts overlap.</li>
<li>We have designed the tests and drawn every test piece and rig. The test plan is going to Brown engineering faculty for review.</li>
<li>Every drawing, with dimensions and a plain explanation, is on the <a href="/blueprints/">blueprints page</a>.</li>
<li>The <a href="/tests/">tests page</a> has the physical test plan of 13 November: every test, how it runs, what it records and tells us, what has to be made, what we have, who provides each piece and the price, with an animation of each test. The October film is kept there for reference.</li>
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
<p class="muted" style="margin-top:16px">After this fall, in late January and February 2027, we pull the T1 slices in the 100 kN frame. In spring 2027 we break the T0 bars, run T2 under water pressure, check the computer model against all of them and design the corner seal. In spring 2028 the work becomes a capstone project.</p>
</div></section>

<section id="need"><div class="wrap">
<p class="eyebrow">What we need</p>
<h2>Parts, materials and time, with the sizes.</h2>
<p class="lead" style="margin-bottom:22px">Everything below comes from the CAD model of the test pieces. Offcuts, rejects and loans are welcome wherever they fit the sizes.</p>
<div class="tablewrap"><table class="stack"><thead><tr><th>Item</th><th>Size and quantity</th><th>Needed by</th></tr></thead><tbody>{"".join(need_rows)}</tbody></table></div>
<div class="card" style="margin-top:26px"><h3>What a sponsor gets</h3>
<p>We put your name or logo on this site, in our fall report and on our posters and talks. We send you photos and test results as each step is finished. You can also visit to see the hardware and meet the team.</p>
<p>To help, reply to the email you received from us, or reach Manos Theofanous, our project lead, through the Brown University School of Engineering.</p></div>
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
