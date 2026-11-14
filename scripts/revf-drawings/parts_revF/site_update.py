"""Bring the website parts page (public/parts/index.html) to the 9 Nov 2026 state of the Rev F parts, in the existing markup.
Idempotent: each entry is replaced if it is on the page and inserted if it is not.  Also copies the STEP, GLB and SVG files.

    python3 site_update.py /path/to/repo/public/parts

9 Nov: CB-01, CB-02 (leaning joint faces), A-03 (mated node), HP-01M (plain bolts on the row beside the block), HP-01 (note), P-06H, P-06P
(leaning frame members, new), HP-02A, HP-02B, HP-03 and A-05 (the hardpoint fitting from the C3 model, new; the schematic HP-02 removed),
P-06 marked 'schematic, straight'."""
import html, json, os, re, shutil, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wt-lean/public/parts"
PAGE = os.path.join(SITE, "index.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
PARTS = json.load(open(f"{OUT}/parts.json"))
CHECKS = json.load(open(f"{OUT}/checks.json"))
page = open(PAGE).read()
VIEWS = ("front", "top", "side", "iso")

def esc(s):
    return html.escape(str(s), quote=False).replace("'", "&#x27;")

def fmt(v):
    return f"{v:g}" if isinstance(v, float) else str(v)

def dims_rows(dims):
    return "".join(f"<tr><td>{esc(k.replace('_', ' '))}</td><td>{esc(fmt(v))}</td></tr>" for k, v in dims.items() if not isinstance(v, (list, dict)))

def views(fn):
    return "<div class=\"drawing\">" + "".join(f"<figure><img src='svg/{fn}_{v}.svg' alt='{v} view'><figcaption>{v}</figcaption></figure>" for v in VIEWS) + "</div>"

def links(fn, asm=False):
    step = f"<a href=\"step/{fn}.step\" download>STEP{' assembly' if asm else ''}</a>"
    return f"<p class=\"dl\">{step} <a href=\"glb/{fn}.glb\" download>GLB</a> " + " ".join(f"<a href='svg/{fn}_{v}.svg' download>{v} SVG</a>" for v in VIEWS) + "</p>"

def meta(info, extra=None):
    return f"<div class=\"meta\"><span>{esc(info['material'])}</span><span>{info['mass_kg']:.2f} kg</span><span>{esc(extra or info['rev'])}</span></div>"

def part_section(pid, extra_rev=None, extra_note=None):
    info = PARTS[pid]; fn = info["files"]
    notes = esc(info["notes"]) + (("</p><p>" + esc(extra_note)) if extra_note else "")
    src = f"<p class=\"src\">Source: {esc(info['source'])}</p>" if info.get("source") else ""
    return f"""<section class="part" id="{pid}">
  <header><span class="pid">{pid}</span><h2>{esc(info['name'])}</h2>
    {meta(info, extra_rev)}</header>
  <div class="row">
    <div class="viewer" data-glb="glb/{fn}.glb"><canvas></canvas><div class="hint">drag to turn, wheel to zoom</div></div>
    {views(fn)}
  </div>
  <div class="row2">
    <div><table class='dims'>{dims_rows(info['dims'])}</table><p class="units">All dimensions in mm.</p></div>
    <div class="notes"><p>{notes}</p>{src}
      {links(fn)}</div>
  </div>
</section>
"""

def asm_section(pid, dims, figure=None):
    info = PARTS[pid]; fn = info["files"]
    src = f"<p class=\"src\">Source: {esc(info['source'])}</p>" if info.get("source") else ""
    fig = (f"<figure style='margin:16px 0;background:#fff;border-radius:6px;padding:6px'><img src='{figure[0]}' style='width:100%;display:block' alt='{esc(figure[1])}'>"
           f"<figcaption style='color:#333;padding:4px 6px'>{esc(figure[1])}</figcaption></figure>") if figure else ""
    return f"""<section class="part asm" id="{pid}">
  <header><span class="pid">{pid}</span><h2>{esc(info['name'])}</h2>
    {meta(info)}</header>
  <div class="row"><div class="viewer big" data-glb="glb/{fn}.glb"><canvas></canvas><div class="hint">drag to turn, wheel to zoom, right-drag to pan</div></div></div>
  <div class="row">
    <div><table class='dims'>{dims}</table><p class="units">All dimensions in mm; mass is the model volume times the nominal densities.</p></div>
    {views(fn)}
  </div>{fig}
  <div class="notes" style="margin-top:14px"><p>{esc(info['notes'])}</p>{src}{links(fn, asm=True)}</div>
</section>
"""

def sec_re(pid):
    return re.compile(r'<section class="part(?: asm)?" id="' + re.escape(pid) + r'">.*?</section>\n?', re.S)

def put(pid, new, after=None):
    """replace the entry, or insert it after the entry `after`"""
    global page
    m = sec_re(pid).search(page)
    if m:
        page = page[:m.start()] + new + page[m.end():]
    else:
        m = sec_re(after).search(page); assert m, f"{after} not on the page"
        page = page[:m.end()] + (new if page[m.end() - 1] == "\n" else "\n" + new) + page[m.end():]

def drop(pid):
    global page
    page = sec_re(pid).sub("", page)
    page = re.sub(r"<li><a href='#" + re.escape(pid) + r"'>.*?</a></li>", "", page)

def nav(pid, after=None, short=False):
    global page
    name = PARTS[pid]["name"]
    if short and len(name) > 60:
        name = name[:60] + "..."
    li = f"<li><a href='#{pid}'>{pid} {esc(name)}</a></li>"
    pat = re.compile(r"<li><a href='#" + re.escape(pid) + r"'>.*?</a></li>")
    if pat.search(page):
        page = pat.sub(lambda _: li, page)
    else:
        pa = re.compile(r"<li><a href='#" + re.escape(after) + r"'>.*?</a></li>"); m = pa.search(page); assert m, after
        page = page[:m.end()] + li + page[m.end():]

HP_PENDING = ("HP-01 (as drawn) and HP-01M (fitting moved onto the line of the pull) are the two hardpoint depths; which one goes forward is pending the decision with Rick on 10 November and "
              "Marco's review on 13 November. The fitting itself is now HP-02A, HP-02B and HP-03, assembled in A-05.")

# ---- parts
put("CB-01", part_section("CB-01")); put("CB-02", part_section("CB-02"))
put("P-06H", part_section("P-06H"), after="P-06"); put("P-06P", part_section("P-06P"), after="P-06H")
put("HP-01", part_section("HP-01", extra_rev="8 Nov 2026 PROPOSAL, as drawn; superseded in concept by A-05", extra_note=HP_PENDING))
put("HP-01M", part_section("HP-01M", extra_rev="9 Nov 2026 PROPOSAL, moved; superseded in concept by A-05", extra_note=HP_PENDING))
drop("HP-02")
put("HP-02A", part_section("HP-02A"), after="HP-01M"); put("HP-02B", part_section("HP-02B"), after="HP-02A")
put("HP-03", part_section("HP-03"), after="HP-02B")

# ---- assemblies
d3 = PARTS["A-03"]["dims"]; w = d3["worst"]; c3 = CHECKS["A-03"]; c1, c2 = CHECKS["CB-01"]["clearances"], CHECKS["CB-02"]["clearances"]
a03_dims = dims_rows({
    "blocks": "2 x CB-01 (hexagon), 1 x CB-02 (pentagon)", "ties": f"{d3['ties']} x 22.2 x 300 (7/8-14 Inconel 718), through the mated holes", "dowels": f"{d3['dowels']} x 20 x 100",
    "edge": d3["edge"], "dihedral angles measured": "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in d3["seams"]) + " deg",
    "(a) common volume of the blocks, pairwise": ", ".join(str(x) for x in d3["interference_mm3"].values()) + f" mm3 (control {c3['control_overlap_when_one_block_is_pushed_0p5mm_into_its_neighbour_mm3']:.0f} mm3 at 0.5 mm push)",
    "(b) joint faces coplanar within": f"{w['joint_faces_coplanar_mm']:.6f} mm (limit 0.01)",
    "(c) tie hole pairs, axes apart": f"{w['tie_axis_offset_mm']:.6f} mm (limit 0.05)", "(c) dowel hole pairs, axes apart": f"{w['dowel_axis_offset_mm']:.6f} mm (limit 0.05)",
    "(d) hole to rib landing": f"{c1['hole_to_landing']} hexagon, {c2['hole_to_landing']} pentagon", "(d) washer seat to landing edge": f"{c1['washer_to_landing_edge']} hexagon, {c2['washer_to_landing_edge']} pentagon",
    "(d) hole to outer / cabin face": f"{c1['hole_to_outer_face']} / {c1['hole_to_cabin_face']} hexagon, {c2['hole_to_outer_face']} / {c2['hole_to_cabin_face']} pentagon",
    "(e) landing wall to joint face, z 0 and z 400": f"{c1['landing_wall_sharp_corner']['z0']} and {c1['landing_wall_sharp_corner']['z400']} hexagon, {c2['landing_wall_sharp_corner']['z0']} and {c2['landing_wall_sharp_corner']['z400']} pentagon",
    "wedge angles about the vertex line": ", ".join(str(x) for x in d3["wedge_angles_deg"]) + " deg",
    **{"mass " + k.replace("_kg", ""): f"{v} kg" for k, v in PARTS["A-03"]["masses"].items()}})
put("A-03", asm_section("A-03", a03_dims, figure=("figures/montage_corner_node_9nov.png", "The leaning corner blocks and the three blocks mated at a vertex, with a section square to the vertex line (9 Nov 2026).")))
d5 = PARTS["A-05"]["dims"]; s5 = d5["slot_clearances"]; c5 = CHECKS["A-05"]; cm = c5["clashes_moved_position"]; ins = c5["pin_insertion"]["cabin_side"]
a05_dims = dims_rows({
    "frame": d5["frame_lengths"], "slot for the lug": d5["slot"], "lug mid-plane z'": d5["lug_mid_plane_zp"], "pins": d5["pins"], "plain seam bolts": d5["plain_bolts"],
    "slot to RTV recess / inner gland": f"{s5['to_rtv_recess_edge']} / {s5['to_inner_gland_edge']}", "slot to plain bolt hole": s5["to_plain_bolt_hole_at_137p5"],
    "lug corner into the slot's R5": f"{s5['lug_square_corner_into_R5_slot_corner_mm']} (clash; R{s5['largest_slot_corner_radius_that_clears_a_square_lug']} clears)",
    "clash with the outer flange, mm3": f"lug body {cm['HP-02A']['common_volume_with_frame_A_flange_mm3']}, clevis {cm['HP-02B']['common_volume_with_frame_B_flange_mm3']}, pins {cm['pins']['common_volume_with_frame_B_flange_mm3']}",
    "clash with the seat lip, mm3": f"{cm['HP-02A']['common_volume_with_frame_A_lip_mm3']}, {cm['HP-02B']['common_volume_with_frame_B_lip_mm3']}, {cm['pins']['common_volume_with_frame_B_lip_mm3']}",
    "clash with the secondary ribs at the node, mm3": f"lug body {cm['HP-02A']['common_volume_with_the_two_secondary_ribs_of_panel_A_mm3']}, clevis {cm['HP-02B']['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']}, pins {cm['pins']['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']}",
    "pin insertion from the cabin side": f"blocked: {ins['free_travel_before_the_seat_lip']} of 95 free before the seat lip",
    "fastening of the base blocks": "OPEN (not in the C3 model)",
    **{"mass " + k.replace("_kg", "").replace("_", " "): f"{v} kg" for k, v in PARTS["A-05"]["masses"].items()}})
put("A-05", asm_section("A-05", a05_dims), after="A-03")

# ---- P-06 marked schematic, straight
page = page.replace('<span class="pid">P-06</span><h2>Frame member, 180 deep</h2>', '<span class="pid">P-06</span><h2>Frame member, 180 deep (schematic, straight)</h2>')
page = page.replace("<li><a href='#P-06'>P-06 Frame member, 180 deep</a></li>", "<li><a href='#P-06'>P-06 Frame member, 180 deep (schematic, straight)</a></li>")
old = "Straight schematic: the real member&#x27;s web leans 20.9 degrees to the joint plane.</p>"
if old in page:
    page = page.replace(old, "Schematic, straight: the real member&#x27;s web leans 20.905 degrees (hexagon) or 16.472 degrees (pentagon) so that its joint face lies on the seam&#x27;s radial plane; "
                             "the leaning members are P-06H and P-06P below, which also carry the glands, the RTV recess and the seam bolts at z&#x27; 58 in bays of 3, 5, 5, 3.</p>")

# ---- navigation
nav("CB-01"); nav("CB-02"); nav("P-06H", after="P-06"); nav("P-06P", after="P-06H"); nav("HP-01"); nav("HP-01M")
nav("HP-02A", after="HP-01M"); nav("HP-02B", after="HP-02A"); nav("HP-03", after="HP-02B"); nav("A-03", short=True); nav("A-05", after="A-03", short=True)

# ---- introduction
MARK = "<p><strong>9 Nov 2026:</strong>"
intro9 = (MARK + " the corner blocks CB-01 and CB-02 are redrawn with leaning joint faces (each joint face on the seam's radial plane, the block swept along the vertex line), and the corner node A-03 "
          "is rebuilt and checked on the real polyhedron: the three blocks no longer overlap, their joint faces are coplanar and the facing tie and dowel holes are coaxial. "
          "New: the leaning frame members P-06H (hexagon) and P-06P (pentagon); P-06 stays as 'schematic, straight'. "
          "Depth convention: z is panel depth (the 180 mm frame is z 0 to z 180); z' is depth along the leaning joint face, and seam features (glands z' 18 and 32, RTV recess 42, bolt row 58, corner tie rows 133.8 and 380.0) are placed by z'. "
          "Hardpoint: HP-01M has its two plain seam bolts back on the bolt row at z' 58, beside the block at +-137.5 (the 'pad covers the bolts' clash of 8 Nov was an artefact of that solid). "
          "The fitting is rebuilt from the C3 model as HP-02A (lug), HP-02B (clevis) and HP-03 (pins along the depth, double shear), assembled in A-05; the schematic fitting half HP-02 is removed. "
          "A-05 lists what clashes (the outer flange, the secondary ribs at the node, pin insertion against the seat lip) and what is open (how the base blocks fasten to the frame). "
          "All proposals for the 13 Nov review; PL-01 and A-04 still use the straight corner block of 8 Nov.</p>")
page = re.sub(r"\n?" + re.escape(MARK) + r".*?</p>", "", page, flags=re.S)
m = re.search(r"<p><strong>8 Nov 2026:</strong>.*?</p>", page, re.S); assert m
page = page[:m.end()] + "\n" + intro9 + page[m.end():]
page = page.replace("HP-02 and HP-03 (the titanium fitting and the 40 mm pin)", "the titanium fitting and the 40 mm pin (schematic then; rebuilt on 9 Nov, see below)")

# ---- footer
page = page.replace("and build_parts_revF.py (8 November 2026). Masses", "and build_parts_revF.py (8 and 9 November 2026). Masses")
open(PAGE, "w").write(page)
print("page written", len(page), "chars")

# ---- files
copied = 0
for pid in ("CB-01", "CB-02", "P-06H", "P-06P", "HP-01", "HP-01M", "HP-02A", "HP-02B", "HP-03", "A-03", "A-05"):
    fn = PARTS[pid]["files"]
    for sub, names in (("step", [f"{fn}.step"]), ("glb", [f"{fn}.glb"]), ("svg", [f"{fn}_{v}.svg" for v in VIEWS])):
        for n in names:
            shutil.copyfile(f"{OUT}/{sub}/{n}", f"{SITE}/{sub}/{n}"); copied += 1
for n in ["step/HP-02.step", "glb/HP-02.glb"] + [f"svg/HP-02_{v}.svg" for v in VIEWS]:
    if os.path.exists(f"{SITE}/{n}"):
        os.remove(f"{SITE}/{n}")
shutil.copyfile(f"{OUT}/montage_corner_node_9nov.png", f"{SITE}/figures/montage_corner_node_9nov.png")
print("files copied", copied)
