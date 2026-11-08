"""GLB files from the STL meshes (trimesh), the iso-view montage PNG, and out/README.md. 8 Nov 2026.
Run after build_parts_revF.py:  python3 postprocess.py"""
import json, math, os, subprocess, sys
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/claude/package/parts_revF/out"
os.makedirs(f"{OUT}/glb", exist_ok=True)
PARTS = json.load(open(f"{OUT}/parts.json"))
CHECKS = json.load(open(f"{OUT}/checks.json"))
BLENDS = json.load(open(f"{OUT}/blend_log.json"))["failed_blends"] if os.path.exists(f"{OUT}/blend_log.json") else []

# vertex colours as on the existing site GLBs: aluminium (170,178,186), forging (150,120,90), hub/Ti (120,130,150), glass (160,210,240,110)
COLOR = {"6061-T6": (170, 178, 186, 255), "7075-T7351": (150, 158, 170, 255), "2219-T852": (150, 120, 90, 255), "Ti-6Al-4V": (120, 130, 150, 255),
         "A286": (120, 125, 135, 255), "Inconel 718": (95, 100, 115, 255), "BOROFLOAT 33": (160, 210, 240, 110)}

def colour_mesh(m, rgba):
    m.visual = trimesh.visual.ColorVisuals(m, vertex_colors=np.tile(np.array(rgba, np.uint8), (len(m.vertices), 1)))
    return m

def glb_single(pid, info):
    m = trimesh.load(f"{OUT}/stl/{info['files']}.stl", force="mesh")
    colour_mesh(m, COLOR.get(info["material"], (170, 178, 186, 255)))
    sc = trimesh.Scene(); sc.add_geometry(m, node_name=pid, geom_name=pid)
    sc.export(f"{OUT}/glb/{info['files']}.glb")
    return len(m.faces)

def glb_assembly(pid, info):
    name = info["files"]; pdir = f"{OUT}/stl/_parts/{name}"
    man = json.load(open(f"{pdir}/manifest.json"))
    sc = trimesh.Scene(); nf = 0
    for e in man:
        m = trimesh.load(f"{pdir}/{e['file']}", force="mesh")
        rgba = tuple(int(round(c * 255)) for c in e["color"]) + (255,)
        colour_mesh(m, rgba)
        sc.add_geometry(m, node_name=e["label"], geom_name=e["label"]); nf += len(m.faces)
    sc.export(f"{OUT}/glb/{name}.glb")
    return nf

ORDER = ["CB-01", "CB-02", "HP-01", "HP-01M", "HP-02", "HP-03", "P-11", "P-07", "PL-01", "A-03", "A-04"]
faces = {}
for pid in ORDER:
    info = PARTS[pid]
    faces[pid] = glb_assembly(pid, info) if info.get("assembly") else glb_single(pid, info)
    sz = os.path.getsize(f"{OUT}/glb/{info['files']}.glb")
    print(f"{pid:7s} {info['files']:24s} {faces[pid]:8d} faces  {sz/1e6:6.2f} MB")

# montage of the iso views
tiles = []
for pid in ORDER:
    fn = PARTS[pid]["files"]
    png = f"/tmp/montage_{fn}.png"
    subprocess.run(["rsvg-convert", "-w", "800", "-b", "white", f"{OUT}/svg/{fn}_iso.svg", "-o", png], check=True)
    im = Image.open(png).convert("RGB")
    # crop to content with a margin
    bbox = Image.eval(im.convert("L"), lambda p: 255 - p).getbbox()
    if bbox:
        im = im.crop((max(bbox[0] - 20, 0), max(bbox[1] - 20, 0), min(bbox[2] + 20, im.width), min(bbox[3] + 20, im.height)))
    tiles.append((pid, im))
W, H, cols = 600, 380, 3
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W, rows * (H + 56) + 50), "white")
dr = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16); fontb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except Exception:
    font = fontb = ImageFont.load_default()
dr.text((16, 12), "HCSA Rev F parts, 8 Nov 2026 PROPOSAL for the 13 Nov review: iso views from the CadQuery models (parts_revF)", fill="black", font=fontb)
for i, (pid, im) in enumerate(tiles):
    r, c = divmod(i, cols)
    im = im.copy(); im.thumbnail((W - 24, H - 10))
    x0 = c * W + (W - im.width) // 2; y0 = 50 + r * (H + 56) + (H - im.height) // 2
    sheet.paste(im, (x0, y0))
    info = PARTS[pid]
    label = f"{pid}  {info['name']}"
    if len(label) > 68:
        label = label[:65] + "..."
    dr.text((c * W + 12, 50 + r * (H + 56) + H + 2), label, fill="black", font=font)
    dr.text((c * W + 12, 50 + r * (H + 56) + H + 24), f"{info['material']}, {info['mass_kg']:.2f} kg, bbox {' x '.join(str(round(b)) for b in info['bbox_mm'])}", fill=(80, 80, 80), font=font)
sheet.save(f"{OUT}/montage_parts_revF.png")
print("montage", sheet.size)

# README
lines = ["# HCSA Rev F parts library additions, 8 Nov 2026 (PROPOSAL)", "",
         "Built with CadQuery 2.8 by `build_parts_revF.py` (conventions of `parts_lib.py`: mm; z 0 outer face of the rib/frame grid, z 180 pane seat plane, z 400 cabin face of the main rib and corner block). "
         "Everything here is a proposal for the 13 November review with Marco Cross and Prof. Fleeter, not a decision. Outputs: `step/`, `stl/`, `svg/` (front, top, side, iso), `glb/`, `parts.json` (masses from model volume x nominal density), `checks.json` (bounding boxes, hole volumes, clearances, dihedrals), `montage_parts_revF.png`.", "",
         "## Parts", "", "| id | name | material | mass kg | bbox mm | status |", "|---|---|---|---|---|---|"]
for pid in ORDER:
    info = PARTS[pid]
    lines.append(f"| {pid} | {info['name']} | {info['material']} | {info['mass_kg']:.3f} | {' x '.join(str(b) for b in info['bbox_mm'])} | {info['rev']} |")
lines += ["", "Masses of the assemblies: A-03 " + ", ".join(f"{k} {v}" for k, v in PARTS["A-03"]["masses"].items()) + "; A-04 " + ", ".join(f"{k} {v}" for k, v in PARTS["A-04"]["masses"].items()) + " (kg).", ""]
lines += ["## Clashes and departures from the brief (for the review)", "",
          "1. **CB-01 / CB-02 tie columns.** The brief put the two tie columns 56 mm apart centred on the 230 mm leg (87 and 143 mm from the vertex). The main rib landing (110 wide pocket along the bisector) reaches "
          f"{CHECKS['CB-01']['landing_wall_on_inner_face']} mm (hexagon) and {CHECKS['CB-02']['landing_wall_on_inner_face']} mm (pentagon) along the legs' inner faces, so a 23.5 mm hole at 87 mm breaks into the pocket. "
          "The columns are drawn at 136 and 192 mm (pitch 56 kept), the nearest position where a 45 mm washer clears the landing on both blocks. The C1 model has them elsewhere and should be rerun.",
          f"2. **CB-01 / CB-02 landing depth.** '30 mm into the block' from the re-entrant corner (57.7 mm from the vertex on the hexagon, 61.8 on the pentagon) cannot be cut: 30 mm nearer the vertex the block is only {2*(57.74-30)*math.tan(math.radians(60)):.0f} mm (hex) / {2*(61.80-30)*math.tan(math.radians(54)):.0f} mm (pent) wide, so a 110 pocket there breaks through the joint faces. "
          f"The pocket bottom is at {CHECKS['CB-01']['landing_bottom_from_vertex']:.0f} mm (hex) / {CHECKS['CB-02']['landing_bottom_from_vertex']:.0f} mm (pent) from the vertex, the deepest position that keeps a continuous 110 mm bearing face; the walls are then 34.5 / 41.8 mm long and "
          f"{CHECKS['CB-01']['wall_to_joint_face']} / {CHECKS['CB-02']['wall_to_joint_face']} mm of metal remain between the pocket corner and the joint face (thin: for Marco). The R12 at the re-entrant corner is consumed by the landing.",
          "3. **CB-02 rows.** Tie rows at z 128.3 and 364.4 as briefed; the dowel is at z 246.3, not 240, so it meets the hexagon's z 240 dowel on the joint plane (same 256.9 mm along the leaning face).",
          f"4. **HP-01M (moved fitting, pins at z 76).** The 40 mm bore (z 56-96) does NOT overlap the seam bolt row at z 58: the nearest bolt hole (y +-88.75) is {CHECKS['HP-01M']['clearances_with_bolts_at_z58']['wall_bore_to_bolt_hole']} mm of metal from the bore, and the bore is "
          f"{CHECKS['HP-01M']['clearances']['bore_to_gland']} mm above the inner gland (z 28.5-35.5). The clash is elsewhere: the moved fitting pad (200 x 60 at z 46-106, y +-100) covers the two plain bolts at y +-88.75, z 58, so their nuts sit under the fitting and the fitting's "
          f"end fixing holes land on them. The two plain bolts are therefore moved to z {CHECKS['HP-01M']['clearances']['bolt_z']:.0f} in this variant (hole edge {CHECKS['HP-01M']['clearances']['bolt_hole_edge_above_pad']} mm above the pad, a 16 mm washer {CHECKS['HP-01M']['clearances']['washer16_above_pad']} mm); "
          f"at the brief's z 110 the hole edge would touch the pad ({CHECKS['HP-01M']['clearances_with_bolts_at_z110']['bolt_hole_edge_above_pad']} mm) and the washer overlap it by {-CHECKS['HP-01M']['clearances_with_bolts_at_z110']['washer16_above_pad']:.0f} mm. "
          "Caution: D1 showed the seal gap grows when the bolt row moves away from the seals (z 70 failed), so a deeper plain bolt is the wrong direction for the seal; the alternatives are the plain bolts moved along the seam into the 20 mm web beside the block (y +-137.5, where the HP1M run had them) or a shorter fitting. To decide on 13 Nov.",
          f"5. **HP-01 (as drawn).** Pad at z 110-170 touches the underside of the frame seat lip (z 170); bore to lip underside {CHECKS['HP-01']['clearances']['bore_to_lip_underside']} mm. Fails the HP1 seal check (hinge), kept for comparison.",
          f"6. **HP-02 fixing holes.** Two rows of three 10 mm holes cannot clear three 40 mm bores on a 60 mm deep plate; drawn as two pairs at the ends and one hole between each pair of bores ({CHECKS['HP-01M']['clearances']['wall_fitting_tap_to_bore']} mm wall to the bore in the block). The fitting bolts are in tension under the seam pull; size to check.",
          "7. **P-11 brace.** A flat 8 mm plate on the web cannot reach z 375 because the cap angle P-04A has a 12 mm vertical leg down the web from z 300 to 375; the plate is stepped out 12 mm at z 280-300 and runs up the outside of the angle's leg. Size is a proposal needing its own check.",
          "8. **PL-01 closure.** The brief's 100 mm cut-back from the rib centre lines and the frame leaves the plate seated on nothing (the ledge is 4-34 mm off the centre line, the lip 50 mm wide); drawn 10 mm back like the panes, plus the apex cut r 100 about the hub and the corner cuts to the CB-02 outline. Side of the ribs is open (Q57); drawn cabin side at z 180-190. Clash at the apex: the hub fork cheeks (4.1-14.1 mm off the rib centre line, out to r 210) cross the plate's edge line between r 100 and 210; a 15 mm cut-back there or notched cheeks, open.",
          "9. **A-03 corner node.** On the real polyhedron (edge 2,250 mm, 11,151.1 mm across) the dihedrals measured at the chosen vertex are " + "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in CHECKS['A-03']['dihedrals']) +
          " deg (138.19 and 142.62 expected). Because the blocks are drawn straight, the two joint faces at each edge are " + ", ".join(str(d['measured_from_solid_faces_deg']) for d in CHECKS['A-03']['dihedrals']) +
          " deg apart instead of coplanar on the radial plane; the straight blocks overlap in a prism about 75 mm on a side along each outer edge and the facing tie holes do not line up. The next step is the leaning joint face (20.905 / 16.472 deg) with the tie holes normal to it, as in C1.",
          "10. **A-04 pentagon.** Schematic: straight frames 1,790 mm between the block ends, five ribs from r 215 to the landings (1,639 mm), 90 plain secondary segments (node cores and star plates not drawn), five CB-02, five PL-01.", "",
          "## Fillets and chamfers", "", ("All blends succeeded." if not BLENDS else "Failed and skipped: " + "; ".join(BLENDS)), "",
          "## Checks", "", "Every part's bounding box is in `checks.json` next to the intended envelope; hole counts were checked by volume before and after the cuts (tie and dowel holes on CB-01/02, pin bores on HP-01/HP-02, brace holes on P-11), all equal to the expected cylinder volumes.", ""]
open(f"{OUT}/README.md", "w").write("\n".join(lines))
print("README written")
