"""GLB files from the STL meshes (trimesh), the iso-view montage PNG, and out/README.md. 8 Nov 2026, README rewritten 9 Nov
(leaning corner blocks, mated node, leaning frame members, HP-01M bolts). The corner node montage is montage_corner.py.
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

ORDER = ["CB-01", "CB-02", "P-06H", "P-06P", "HP-01", "HP-01M", "HP-02A", "HP-02B", "HP-03", "P-11", "P-07", "PL-01", "A-03", "A-05", "A-04"]
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
dr.text((16, 12), "HCSA Rev F parts, 8-9 Nov 2026 PROPOSAL for the 13 Nov review: iso views from the CadQuery models (parts_revF)", fill="black", font=fontb)
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
C1, C2, A3, HM = CHECKS["CB-01"], CHECKS["CB-02"], CHECKS["A-03"], CHECKS["HP-01M"]
c1, c2 = C1["clearances"], C2["clearances"]; w = A3["worst"]; raw = A3["raw_unrounded"]; bs = HM["clearances"]["plain_bolts_beside_the_block"]
al1, al2 = C1["tie_columns_allowed"], C2["tie_columns_allowed"]
FH, FP = CHECKS["P-06H"], CHECKS["P-06P"]
A5 = CHECKS["A-05"]; sl = A5["slot"]; cm = A5["clashes_moved_position"]; wd = A5["widths"]; pi_ = A5["pin_insertion"]; ad = A5["as_drawn_position_lug_mid_plane_zp_140"]; ms = A5["masses"]
cols = C1["tie_columns_xs"]
lines = ["# HCSA Rev F parts library additions, 8-9 Nov 2026 (PROPOSAL)", "",
         "Built with CadQuery 2.8 by `build_parts_revF.py` (with `corner_block.py`, `parts_lib_revF.py`; `postprocess.py` for GLB, montage and this file; `montage_corner.py`; `site_update.py` for the parts page). "
         "Everything here is a proposal for the 13 November review with Marco Cross and Prof. Fleeter, not a decision. Outputs: `step/`, `stl/`, `svg/` (front, top, side, iso), `glb/`, `parts.json` (masses from model volume x nominal density), `checks.json` (bounding boxes, hole volumes, clearances, the node verification), `montage_parts_revF.png`, `montage_corner_node_9nov.png`.", "",
         "## Depth convention (read this first)", "",
         "Units mm. **z is panel depth**, square to the panel: z 0 the outer (space) face of the rib and frame grid, z 180 the pane seat plane, z 400 the cabin face of the main rib and the corner block. "
         "The 180 mm frame depth is panel depth z (z 0 to z 180, the same as the straight secondary ribs), not length along the leaning joint face. "
         "The joint face of every seam lies on the radial plane through the shell edge and the sphere centre; seen from a panel it leans toward the panel interior with depth, "
         f"{C1['joint_face_lean_deg']:.3f} deg from the panel normal on a hexagon and {C2['joint_face_lean_deg']:.3f} deg on a pentagon. **z' is depth along that leaning face** from the shell edge (z = z' cos(lean) on the face). "
         f"The frame's joint face is therefore 180 / cos(lean) long: {FH['joint_face_length']:.1f} mm on a hexagon, {FP['joint_face_length']:.1f} mm on a pentagon. "
         "Features that belong to the seam are placed along the joint face by z' and cut normal to it: glands at z' 18 and 32, RTV recess z' 42, seam bolt row z' 58, hardpoint fitting envelope z' 46-106, corner tie rows z' 133.8 and 380.0, dowel z' 256.9. "
         f"At a corner the two joint planes meet on the **vertex line** (vertex to sphere centre), which leans {C1['vertex_line_lean_deg']:.2f} deg (hexagon) / {C2['vertex_line_lean_deg']:.2f} deg (pentagon) along the corner bisector in the panel frame and 11.64 deg off square to an edge in the joint face (0.2060 mm along the edge per mm of z'). "
         "Parts still drawn straight (z = z'): P-06, HP-01, HP-01M, PL-01, A-04. HP-02A, HP-02B, HP-03 and A-05 are drawn in the joint frame (X along the seam, Y normal to the joint plane, Z = z').", "",
         "## Parts", "", "| id | name | material | mass kg | bbox mm | status |", "|---|---|---|---|---|---|"]
for pid in ORDER:
    info = PARTS[pid]
    lines.append(f"| {pid} | {info['name']} | {info['material']} | {info['mass_kg']:.3f} | {' x '.join(str(b) for b in info['bbox_mm'])} | {info['rev']} |")
lines += ["", "Masses of the assemblies: A-03 " + ", ".join(f"{k} {v}" for k, v in PARTS["A-03"]["masses"].items()) + f" (blocks {', '.join(str(x) for x in A3['block_masses_kg'])}); A-04 " + ", ".join(f"{k} {v}" for k, v in PARTS["A-04"]["masses"].items()) + " (kg). "
          "The straight P-06 (27.86 kg at 2,250 long) stays on the parts page as 'schematic, straight'; its files come from the older `parts_lib.py`.", ""]
lines += ["## Corner node verification (A-03, 9 Nov)", "",
          "Two CB-01 and one CB-02 placed on a vertex of the real truncated icosahedron (60 vertices from the standard coordinates, edge 2,250, 11,151.1 across), each in its own panel frame. Measured on the placed solids:", "",
          "| check | result | limit |", "|---|---|---|",
          f"| (a) pairwise common volume of the three blocks | {', '.join(str(x) for x in A3['a_block_interference_mm3'].values())} mm3 (control: {A3['control_overlap_when_one_block_is_pushed_0p5mm_into_its_neighbour_mm3']:.0f} mm3 when one block is pushed 0.5 mm into its neighbour) | < 1 mm3 |",
          f"| (b) joint faces off the true radial plane / coplanar with each other | {raw['joint_face_off_radial_plane_mm']} mm / {w['joint_faces_coplanar_mm']:.6f} mm | 0.01 mm |",
          f"| (c) 12 facing tie hole pairs, axes apart at the joint plane | {raw['axis_offset_mm']} mm worst, {w['axis_angle_deg']:.6f} deg between axes | 0.05 mm |",
          f"| (c) 6 facing dowel hole pairs | {w['dowel_axis_offset_mm']:.6f} mm worst (all 18 pairs within {raw['offset_from_true_position_mm']} mm of the true position) | 0.05 mm |",
          f"| 12 ties (22.2 x 300) and 6 dowels through the mated holes | common volume with any block {w['tie_through_block_mm3']} / {w['dowel_through_block_mm3']} mm3, with each other {w['fastener_to_fastener_mm3']} mm3 | 0 |",
          f"| (d) nearest tie or dowel hole to the rib landing | {c1['hole_to_landing']} mm hexagon, {c2['hole_to_landing']} mm pentagon | |",
          f"| (d) washer seat (45 mm) to the landing's edge | {c1['washer_to_landing_edge']} mm hexagon, {c2['washer_to_landing_edge']} mm pentagon (sharp edge; 2 mm less to the chamfer); all washers wholly on flat metal: {c1['washer_seat_on_flat_metal'] and c2['washer_seat_on_flat_metal']} | > 0 |",
          f"| (d) hole to the outer face z 0 / cabin face z 400 | {c1['hole_to_outer_face']} / {c1['hole_to_cabin_face']} mm hexagon, {c2['hole_to_outer_face']} / {c2['hole_to_cabin_face']} mm pentagon | |",
          f"| (d) washer seat to the outer face / cabin face | {c1['washer_to_outer_face']} / {c1['washer_to_cabin_face']} mm hexagon, {c2['washer_to_outer_face']} / {c2['washer_to_cabin_face']} mm pentagon | |",
          f"| (d) hole to the leg end, washer to the leg end, hole to hole | {c1['hole_to_leg_end']}, {c1['washer_to_leg_end']}, {c1['hole_to_hole']} mm (both blocks) | |",
          f"| (e) wall, landing corner to joint face, at z 0 and at z 400 | hexagon {c1['landing_wall_sharp_corner']['z0']} and {c1['landing_wall_sharp_corner']['z400']} mm (at the R10: {c1['landing_wall_at_R10_fillet']}); pentagon {c2['landing_wall_sharp_corner']['z0']} and {c2['landing_wall_sharp_corner']['z400']} mm (at the R10: {c2['landing_wall_at_R10_fillet']}) | |",
          "", f"Dihedrals at the vertex: " + "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in A3["seams"]) + f" deg. Wedge angles of the three blocks about the vertex line: {', '.join(str(x) for x in A3['wedge_angles_about_vertex_line_deg'])} deg (sum {sum(A3['wedge_angles_about_vertex_line_deg']):.3f}). The wall in (e) does not change with depth because the landing follows the vertex line (item 2).", ""]
lines += ["## Clashes and departures from the brief (for the review)", "",
          f"1. **CB-01 / CB-02 tie columns.** Columns at {cols[0]:.0f} and {cols[1]:.0f} mm (pitch 56) measured along the edge **from the vertex line at each row's depth**, so the columns run parallel to the vertex line; from the z 0 vertex the holes are at {cols[0] + 0.20601 * 133.8:.1f} / {cols[0] + 0.20601 * 380.0:.1f} mm (column 1, rows 1 / 2) and {cols[1] + 0.20601 * 133.8:.1f} / {cols[1] + 0.20601 * 380.0:.1f} mm (column 2); the dowels are in the same columns. "
          f"What the true geometry allows: the landing's wall meets the leg's inner face {al1['pocket_edge_xs']} mm (hexagon) / {al2['pocket_edge_xs']} mm (pentagon) from the vertex line; a 23.5 hole clears it from {al1['hole_tangent']} / {al2['hole_tangent']}, a 45 mm washer from {al1['washer_tangent_sharp_edge']} / {al2['washer_tangent_sharp_edge']}, and clear of the 2 mm chamfer from {al1['washer_clear_of_chamfer']} / {al2['washer_clear_of_chamfer']}. "
          f"So the briefed 87 / 143 is not possible; the pentagon governs at {al2['washer_clear_of_chamfer']}; {cols[0]:.0f} is drawn (2 mm of flat seat beyond the chamfer on the pentagon), 6 mm nearer the vertex line than the 136 of 8 Nov, the same on both blocks. Columns square to the edge instead (fixed distance from the z 0 vertex) do not fit: at the z' 380 row the landing's edge is already {al2['pocket_edge_xs'] + 0.20601 * 380:.0f} mm from the z 0 vertex on the pentagon. The C1 model should be rerun at these positions.",
          f"2. **CB-01 / CB-02 shape and landing.** Each block is one outline swept along the vertex line (an oblique prism) and cut flat to the panel planes z 0 and z 400: joint faces on the radial planes, leg inner faces parallel to them 50 mm away (measured normal; flat nut seats), leg ends and the landing all parallel to the vertex line. Legs are 230 from the vertex line at every depth. "
          f"The landing is 110 wide with its bottom {C1['landing_bottom_from_vertex_line']} mm (hexagon) / {C2['landing_bottom_from_vertex_line']} mm (pentagon) from the vertex line (2 mm short of the re-entrant corner, and 20 mm of wall where that is possible), walls {C1['landing_wall_len']} / {C2['landing_wall_len']} mm long; wall to the joint face {c1['landing_wall_closed_form']} / {c2['landing_wall_closed_form']} mm (pentagon below 20: for Marco). "
          f"Departure: the landing leans with the vertex line, it is not straight along z. A landing straight along z would break out through the joint faces {c1['a_vertical_landing_breaks_the_joint_face_at_z']} mm (hexagon) / {c2['a_vertical_landing_breaks_the_joint_face_at_z']} mm (pentagon) below the outer face, because the vertex line moves 176 / 146 mm along the bisector over the 400 depth. Consequence: the main rib's end has to be cut on that lean (23.80 / 20.08 deg from square); P-04 is still drawn square-ended. "
          f"Machining: every face is a plane or an R10 cylinder parallel to the vertex line, no undercut. The two R10 landing corners are 437 mm (hexagon) / 426 mm (pentagon) long, too deep for an end mill plunging along the vertex line; they are cut from the open side with a 20 mm ball or R10 bull-nose cutter run along the line. With the vertex line on a rotary axis one set-up does the joint faces, inner faces, landing and all holes; the z 0 and z 400 end cuts take one more set-up each. Acute 69.1 deg (hexagon) / 73.5 deg (pentagon) edges at the end cuts, chamfered. The three chamfered spines leave a channel about 2 mm across down the vertex line (corner seal O10, not modelled).",
          "3. **Rows.** Tie rows at z' 133.8 and 380.0 and dowels at z' 256.9 on both blocks (z 125.0, 355.0, 240.0 on the hexagon's face; 128.3, 364.4, 246.4 on the pentagon's). The hexagon's joint face is 428.2 mm long down the lean and the pentagon's 417.1, so on a hexagon-pentagon seam the two cabin ends are 11.1 mm apart along the face.",
          f"4. **HP-01M (moved fitting, pins at z 76). Corrected.** There is no clash between the moved fitting pad and the plain seam bolts. The 8 Nov solid had put the two plain bolts inside the block at y +-88.75, where the pad (y +-100, z 46-106) covered them, and then moved them deeper to z 118; that was an artefact of the solid. The flight layout has the nearest seam bolts 131.25 or 141.25 mm from the hardpoint centre and the HP1M model had them at 137.5. HP-01M now has the two plain bolts on the bolt row at z' 58, at y +-137.5, in the 20 mm web beside the block, none under the pad. "
          f"Clearances: 16 mm washer to the block's end face {bs['washer16_to_block_end_face']} mm, to the end of the fitting pad along the seam {bs['washer16_to_fitting_pad_end_along_seam']} mm, hole edge to the end face {bs['hole_edge_to_block_end_face']} mm, bolt hole to the nearest 40 bore {HM['clearances']['wall_bore_to_bolt_hole']} mm. "
          f"One thing does not clear: the R10 blend from block to web runs out at y 130 and the washer's edge is at y 129.5, so the washer rides {-bs['washer16_to_R10_blend_runout']} mm onto the blend ({bs['blend_height_under_washer_edge']} mm proud). R{bs['largest_blend_radius_that_clears']} or smaller clears; so does the bolt at 141.25 ({bs['washer16_to_blend_runout_at_flight_positions'][1]} mm), not at 131.25 ({bs['washer16_to_blend_runout_at_flight_positions'][0]} mm). Left at R10 for the review. "
          "Also to settle: +-137.5 is 3.75 / 6.25 mm off the 3-5-5-3 bay bolts (141.25 / 131.25). HP-01 (as drawn) still shows its bolts at y +-88.75 and was not touched.",
          f"5. **HP-01 (as drawn).** Pad at z 110-170 touches the underside of the frame seat lip (z 170); bore to lip underside {CHECKS['HP-01']['clearances']['bore_to_lip_underside']} mm. Fails the HP1 seal check (hinge), kept for comparison.",
          f"6. **Hardpoint fitting from the C3 model: HP-02A (lug), HP-02B (clevis), HP-03 (pin 40 x 95), assembly A-05 (new, 9 Nov).** They replace the schematic fitting half HP-02 and the 160 mm pin of 8 Nov, which had the pins across the joint (removed). The real TP3 fitting is a lug on panel A passing through a slot in both frame webs into a clevis on panel B, three pins along the depth in double shear. "
          f"Placement, moved position: C3 depth stack shifted {A5['shift_applied']['depth_stack']} so the lug's mid-plane is at z' 76 (lug z' 56.5-95.5, cheeks 33.5-56 and 96-118.5, pins 28.5-123.5, base blocks -6.5 to 123.5). "
          f"Departure from C3 in the pull direction: C3 has no frame webs; at C3's own y the bodies overlap the two 20 mm webs ({A5['c3_y_positions_kept_without_shift']['base_A_with_web_A_mm3']:.0f} and {A5['c3_y_positions_kept_without_shift']['cheeks_and_base_B_with_web_B_mm3']:.0f} mm3) and the pins touch web B, so body A is moved +18 and side B -20 to seat on the webs' inner faces: the lug is {A5['shift_applied']['lug_longer_than_C3_by']:.0f} mm longer than in C3 (140, not 102) and the pin line is 60 mm from the joint plane, not 40. The C3 stiffness does not apply to this; to rerun. "
          f"Slot {sl['slot_x'][1] * 2:.0f} x {sl['slot_zp'][1] - sl['slot_zp'][0]:.0f} at z' {sl['slot_zp'][0]}-{sl['slot_zp'][1]}, R5: {sl['to_rtv_recess_edge']} mm to the RTV recess, {sl['to_inner_gland_edge']} mm to the inner gland, {sl['to_plain_bolt_hole_at_137p5']} mm to the plain bolt holes at +-137.5; the bolt row z' 58 is inside the slot's depth range, so the seam has no bolt and no web over 202 mm there. R5 with 1 mm clearance fouls the square lug corners by {sl['lug_square_corner_into_R5_slot_corner_mm']} mm (R{sl['largest_slot_corner_radius_that_clears_a_square_lug']} or less clears, or a 2 mm break on the lug). An 11 x 11 relief on web A lets the lug's R10 root fillet in. "
          f"Clashes with the leaning hexagon frame (common volume, mm3): lug body with frame A flange {cm['HP-02A']['common_volume_with_frame_A_flange_mm3']}, clevis with frame B flange {cm['HP-02B']['common_volume_with_frame_B_flange_mm3']}, pins with frame B flange {cm['pins']['common_volume_with_frame_B_flange_mm3']}; none with the seat lips; with the two secondary ribs that land on the node: {cm['HP-02A']['common_volume_with_the_two_secondary_ribs_of_panel_A_mm3']} (lug body), {cm['HP-02B']['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']} (clevis), {cm['pins']['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']} (pins). The base blocks start at z' -6.5, above the shell edge. "
          f"Width: flange tip {wd['flange_tip_panel_y']} and lip tip {wd['lip_tip_panel_y']} mm into the panel; the lug body reaches {wd['HP_02A_reach_panel_y']} and the clevis {wd['HP_02B_reach_panel_y']} mm. "
          f"Pins cannot be inserted as drawn: from the cabin side the seat lip is met after {pi_['cabin_side']['free_travel_before_the_seat_lip']} of the 95 mm ({pi_['cabin_side']['short_by']} short) and the pane lies on the lip; from the space side the flange is in the way. "
          f"As-drawn position (lug mid-plane z' 140, check only): cheeks to z' 182.5, pins and base blocks to z' 187.5, i.e. {ad['straight_convention_z_equals_zp']['cheeks_beyond_180']} and {ad['straight_convention_z_equals_zp']['pins_beyond_180']} mm beyond the 180 depth if z = z' (straight frame); in the leaning hexagon frame they stay inside (largest panel z {ad['leaning_hexagon_frame']['HP-02A']['largest_panel_depth_z_reached']}, 2 mm under the lip) because parts further into the panel are shallower in z. "
          f"Masses: HP-02A {ms['HP_02A_kg']} kg, HP-02B {ms['HP_02B_kg']} kg, pin {ms['pin_each_kg']} kg, the hardpoint (two bodies, three pins) {ms['hardpoint_2_bodies_3_pins_kg']} kg. "
          f"**Does the HP-01 local block still make sense? No.** " + A5["local_block_verdict"] + " Fastening of the base blocks to the frame is not in C3: OPEN.",
          "7. **P-11 brace.** A flat 8 mm plate on the web cannot reach z 375 because the cap angle P-04A has a 12 mm vertical leg down the web from z 300 to 375; the plate is stepped out 12 mm at z 280-300 and runs up the outside of the angle's leg. Size is a proposal needing its own check.",
          "8. **PL-01 closure.** The brief's 100 mm cut-back from the rib centre lines and the frame leaves the plate seated on nothing; drawn 10 mm back like the panes, plus the apex cut r 100 about the hub and the corner cuts. Side of the ribs is open (Q57); drawn cabin side at z 180-190. Clash at the apex with the hub fork cheeks, open. NOT redrawn on 9 Nov: its corner cuts still follow the straight CB-02 outline of 8 Nov; on the leaning block the outline at z 180 sits 65.8 mm further along the bisector.",
          "9. **A-03 corner node.** Rebuilt with the leaning blocks; the three blocks now fit (table above). The 8 Nov straight blocks overlapped in a prism about 75 mm on a side along each edge and their facing holes did not meet. Ties (22.2 x 300, length carried from 8 Nov, not a sized part) and dowels (20 x 100) pass through the mated holes. Not checked: the 300 mm studs against the main rib ends in the landings, nuts, washers, wrench access.",
          f"10. **P-06H / P-06P leaning frame members (new).** Web leaning {FH['web_lean_deg']:.3f} / {FP['web_lean_deg']:.3f} deg with its joint face on the radial plane, 180 deep in z, web 20 normal to the joint face, flange 50 x 10 at z 0-10 and lip 50 x 10 at z 170-180 parallel to the panel planes; glands, RTV recess (R3 half-round, as on the test pieces) and 16 bolt holes 8.4 at z' 58 placed by z' and cut normal to the joint face; bays 3-5-5-3, first bolt 271.25 from the vertex. "
          f"Ends on the corner blocks' leg end planes (parallel to the vertex line): {FH['length_at_z0']:.0f} long at z 0, {FH['length_at_z180']:.1f} (hexagon) / {FP['length_at_z180']:.1f} (pentagon) at z 180. Against the block solid: gap {FH['end_to_corner_block_gap_mm']} mm, common volume {FH['end_to_corner_block_common_volume_mm3']} mm3. First bolt hole edge {FH['first_bolt_hole_edge_to_end']} mm from the end. "
          "Departures: the gland-carrying hand is drawn (the mate has a flat face); the glands run out at the ends (loop corners Q92 not drawn); hardpoint blocks, leak port and inside radii not in the solid; hexagon lip drawn 50 as briefed although the parameter file carries 56.6 (OPEN-17).",
          "11. **A-04 pentagon.** Schematic, NOT redrawn on 9 Nov: straight frames 1,790 mm, straight 8 Nov CB-02 blocks, five ribs, 90 plain secondary segments, five PL-01. Its mass still counts the straight blocks (20.69 kg each against 21.55).", "",
          "## Fillets and chamfers", "", ("All blends succeeded." if not BLENDS else "Failed and skipped: " + "; ".join(BLENDS)), "",
          "## Checks", "", "Every part's bounding box is in `checks.json`; hole counts were checked by volume before and after the cuts (tie and dowel holes on CB-01/02, bolt holes on P-06H/P and HP-01M, pin bores on HP-01, HP-02A and HP-02B, brace holes on P-11), all equal to the expected cylinder volumes within 3 mm3.", ""]
open(f"{OUT}/README.md", "w").write("\n".join(lines))
print("README written")
