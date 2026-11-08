"""Add the Rev F parts to the website parts page (public/parts/index.html) in the existing markup. 8 Nov 2026."""
import html, json, re, sys

PAGE = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/wt-parts/public/parts/index.html"
PARTS = json.load(open("/home/claude/package/parts_revF/out/parts.json"))
CHECKS = json.load(open("/home/claude/package/parts_revF/out/checks.json"))
page = open(PAGE).read()

def esc(s):
    return html.escape(str(s), quote=False).replace("'", "&#x27;")

def fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)

def dims_rows(dims):
    rows = []
    for k, v in dims.items():
        if isinstance(v, (list, dict)):
            continue
        rows.append(f"<tr><td>{esc(k.replace('_', ' '))}</td><td>{esc(fmt(v))}</td></tr>")
    return "".join(rows)

def views(fn):
    return ("<div class=\"drawing\">" + "".join(f"<figure><img src='svg/{fn}_{v}.svg' alt='{v} view'><figcaption>{v}</figcaption></figure>" for v in ("front", "top", "side", "iso")) + "</div>")

def links(fn, asm=False):
    step = f"<a href=\"step/{fn}.step\" download>STEP{' assembly' if asm else ''}</a>"
    return (f"<p class=\"dl\">{step} <a href=\"glb/{fn}.glb\" download>GLB</a> " + " ".join(f"<a href='svg/{fn}_{v}.svg' download>{v} SVG</a>" for v in ("front", "top", "side", "iso")) + "</p>")

def meta(info, extra=None):
    mass = f"{info['mass_kg']:.2f} kg"
    rev = extra or info["rev"]
    return f"<div class=\"meta\"><span>{esc(info['material'])}</span><span>{mass}</span><span>{esc(rev)}</span></div>"

def part_section(pid, extra_rev=None, extra_note=None, dims_override=None):
    info = PARTS[pid]; fn = info["files"]
    notes = esc(info["notes"])
    if extra_note:
        notes += "</p><p>" + esc(extra_note)
    src = f"<p class=\"src\">Source: {esc(info['source'])}</p>" if info.get("source") else ""
    dims = dims_override if dims_override is not None else dims_rows(info["dims"])
    return f"""<section class="part" id="{pid}">
  <header><span class="pid">{pid}</span><h2>{esc(info['name'])}</h2>
    {meta(info, extra_rev)}</header>
  <div class="row">
    <div class="viewer" data-glb="glb/{fn}.glb"><canvas></canvas><div class="hint">drag to turn, wheel to zoom</div></div>
    {views(fn)}
  </div>
  <div class="row2">
    <div><table class='dims'>{dims}</table><p class="units">All dimensions in mm.</p></div>
    <div class="notes"><p>{notes}</p>{src}
      {links(fn)}</div>
  </div>
</section>
"""

def asm_section(pid, dims):
    info = PARTS[pid]; fn = info["files"]
    src = f"<p class=\"src\">Source: {esc(info['source'])}</p>" if info.get("source") else ""
    return f"""<section class="part asm" id="{pid}">
  <header><span class="pid">{pid}</span><h2>{esc(info['name'])}</h2>
    {meta(info)}</header>
  <div class="row"><div class="viewer big" data-glb="glb/{fn}.glb"><canvas></canvas><div class="hint">drag to turn, wheel to zoom, right-drag to pan</div></div></div>
  <div class="row">
    <div><table class='dims'>{dims}</table><p class="units">All dimensions in mm; mass is the model volume times the nominal densities.</p></div>
    {views(fn)}
  </div>
  <div class="notes" style="margin-top:14px"><p>{esc(info['notes'])}</p>{src}{links(fn, asm=True)}</div>
</section>
"""

HP_PENDING = "HP-01 (as drawn) and HP-01M (fitting moved onto the line of the pull) are the two hardpoint positions; which one goes forward is pending the decision with Rick on 10 November and Marco's review on 13 November."

new_parts = (
    part_section("CB-01") + part_section("CB-02") +
    part_section("HP-01", extra_rev="8 Nov 2026 PROPOSAL, as drawn (pending 10 Nov decision)", extra_note=HP_PENDING) +
    part_section("HP-01M", extra_rev="8 Nov 2026 PROPOSAL, moved (pending 10 Nov decision)", extra_note=HP_PENDING) +
    part_section("HP-02") + part_section("HP-03") + part_section("P-11") + part_section("PL-01"))

d3 = PARTS["A-03"]["dims"]
dih = "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in d3["dihedrals"])
jf = ", ".join(str(d["measured_from_solid_faces_deg"]) for d in d3["dihedrals"])
a03_dims = dims_rows(dict(blocks="2 x CB-01 (hexagon), 1 x CB-02 (pentagon)", ties=f"{d3['ties']} x 22.2 x 300 (7/8-14 Inconel 718)", dowels=f"{d3['dowels']} x 20 x 100",
                          edge=d3["edge"], dihedral_angles_measured=dih + " deg (138.19 and 142.62 expected)", straight_block_joint_faces_apart=jf + " deg (should be 0)",
                          **{"mass " + k.replace("_kg", ""): f"{v} kg" for k, v in PARTS["A-03"]["masses"].items()}))
d4 = PARTS["A-04"]["dims"]
a04_dims = dims_rows(dict(edge=d4["edge"], circumradius=d4["circumradius"], apothem=d4["apothem"], frames=d4["frames"], main_ribs=d4["main_ribs"], cap_angles=d4["cap_angles"],
                          hub_parts=d4["hub"], secondary_ribs=d4["secondary_ribs"], corner_blocks=d4["corner_blocks"], closure_triangles=d4["closure_triangles"],
                          **{"mass " + k: f"{v} kg" for k, v in PARTS["A-04"]["masses"].items()}))
new_asms = asm_section("A-03", a03_dims) + asm_section("A-04", a04_dims)

# ---- splice: parts after the P-07 section, assemblies after A-02B
m = re.search(r'<section class="part" id="P-07">.*?</section>\n', page, re.S)
assert m, "P-07 section not found"
page = page[:m.end()] + new_parts + page[m.end():]
m = re.search(r'<section class="part asm" id="A-02B">.*?</section>', page, re.S)
assert m, "A-02B section not found"
page = page[:m.end()] + "\n" + new_asms.rstrip("\n") + page[m.end():]

# ---- P-07 entry to 21 mm
old_dims = "<tr><td>thickness</td><td>22.0</td></tr>"
assert old_dims in page
page = page.replace(old_dims, "<tr><td>thickness</td><td>21.0</td></tr>")
old_note = "21 mm since 5 November (SCHOTT's standard 1,700 x 1,300 sheet; 22 mm would need container loads); the 3D model, drawing views and STEP file below are still drawn at 22 mm."
assert old_note in page
page = page.replace(old_note, "21 mm since 5 November (SCHOTT's standard 1,700 x 1,300 sheet; 22 mm would need container loads); the 3D model, drawing views, STEP and GLB below were regenerated at 21 mm on 8 November.")
page = page.replace("<span>5.50 kg at 21 mm</span><span>DECIDED 5 Nov 2026 (21 mm)</span>", "<span>5.50 kg</span><span>DECIDED 5 Nov 2026 (21 mm), model regenerated 8 Nov</span>")

# ---- nav
nav_parts = "".join(f"<li><a href='#{pid}'>{pid} {esc(PARTS[pid]['name'])}</a></li>" for pid in ("CB-01", "CB-02", "HP-01", "HP-01M", "HP-02", "HP-03", "P-11", "PL-01"))
anchor = "<li><a href='#P-07'>P-07 Pressure pane L7, 531 mm, 21 mm BOROFLOAT 33</a></li>"
assert anchor in page
page = page.replace(anchor, anchor + nav_parts)
nav_asms = "".join(f"<li><a href='#{pid}'>{pid} {esc(PARTS[pid]['name'][:60])}{'...' if len(PARTS[pid]['name']) > 60 else ''}</a></li>" for pid in ("A-03", "A-04"))
anchor2 = "<li><a href='#A-02B'>A-02B Hexagon panel, option B (thin): the same with the 400 x 100 </a></li>"
assert anchor2 in page
page = page.replace(anchor2, anchor2 + nav_asms)

# ---- introduction
old_intro = "Not here yet: the corner block and its ties (the C1 deck), the mid-seam hardpoints, the pentagon panel, the shutters and the outer glass layers. They follow as their designs settle.</p>"
assert old_intro in page
page = page.replace(old_intro, "Not here yet: the shutters, the outer glass layers, the hardpoint and corner seals, and the node cores of the pentagon grid. They follow as their designs settle.</p>"
                    "\n<p><strong>8 Nov 2026:</strong> corner blocks, hardpoint, main rib brace, pentagon closure and the corner node assembly added as proposals for the 13 Nov review; P-07 at 21 mm. "
                    "The new entries are CB-01 and CB-02 (the corner blocks with R10 inside corners after Marco's review), HP-01 and HP-01M (the hardpoint block in its two positions, pending the 10 Nov decision), HP-02 and HP-03 (the titanium fitting and the 40 mm pin), P-11 (the main rib lateral brace), PL-01 (one triangle of the pentagon closure plate), A-03 (the corner node on the real polyhedron) and A-04 (the pentagon panel, schematic). "
                    "Each note says where the model departs from the sheets and what clashes it found; the full list is in the parts_revF README in Drive.</p>")

# ---- footer
old_footer = "Built with CadQuery from parts_lib.py and assemblies.py. Masses are model volumes times nominal densities. 2 November 2026."
assert old_footer in page
page = page.replace(old_footer, "Built with CadQuery from parts_lib.py and assemblies.py (2 November 2026) and build_parts_revF.py (8 November 2026). Masses are model volumes times nominal densities.")

open(PAGE, "w").write(page)
print("page written", len(page), "chars")
