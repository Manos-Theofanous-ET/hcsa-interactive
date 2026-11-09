"""HCSA Rev F parts, 8-9 Nov 2026 PROPOSAL for the 13 Nov review (Marco Cross, Prof. Fleeter).
9 Nov: CB-01 / CB-02 with leaning joint faces (corner_block.py), A-03 mated and verified on the real polyhedron, P-06H / P-06P leaning
frame members, HP-01M plain bolts back on the bolt row beside the block; HP-02 / HP-03 marked schematic. PL-01 and A-04 still use the
8 Nov straight block outline (corner_block_straight.py).
Builds CB-01, CB-02, HP-01, HP-01M, HP-02, HP-03, P-11, P-07 (21 mm), PL-01, A-03, P-06H, P-06P, A-04 with CadQuery 2.8, in the
conventions of parts_lib.py (units mm; z 0 outer face of the rib/frame grid, z 180 pane seat plane, z 400 cabin face
of the main rib and the corner block). Outputs: out/{step,stl,svg,glb}, out/parts.json, out/checks.json.

Run:  python3 build_parts_revF.py [part ids ...]      (no ids = everything)
"""
import json, math, os, sys, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadquery as cq
from cadquery import exporters
import parts_lib_revF as L
from parts_lib_revF import OUT, RHO, PARTS, REV, register
import corner_block as CB
import corner_block_straight as CBS       # the 8 Nov straight outline, still used by PL-01 and the schematic A-04

P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "hcsa_params_revF.json")))
v = lambda g, k: P[g][k][0]

CHECKS = json.load(open(f"{OUT}/checks.json")) if os.path.exists(f"{OUT}/checks.json") else {}
FAILED_BLENDS = []

def _plain(o):
    """numpy scalars to plain Python for json"""
    import numpy as np
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError(type(o))

def bbox(shape):
    bb = (shape.val() if hasattr(shape, "val") else shape).BoundingBox()
    return [round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)]

def check(pid, **kw):
    CHECKS.setdefault(pid, {}).update(kw)
    print(f"   check {pid}: " + ", ".join(f"{k}={vv}" for k, vv in kw.items()))

def box(dx, dy, dz, x0=0.0, y0=0.0, z0=0.0):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x0, y0, z0))

def cyl_x(d, x0, x1, y, z):
    return cq.Workplane("YZ").center(y, z).circle(d / 2).extrude(x1 - x0).translate((x0, 0, 0))

def cyl_y(d, y0, y1, x, z):
    return cq.Workplane("XZ").center(x, z).circle(d / 2).extrude(-(y1 - y0)).translate((0, y0, 0))

def cyl_z(d, z0, z1, x, y):
    return cq.Workplane("XY").center(x, y).circle(d / 2).extrude(z1 - z0).translate((0, 0, z0))

# ============================================================ CB-01 / CB-02 corner blocks, leaning joint faces (9 Nov)
REV9 = "9 Nov 2026 PROPOSAL"
TIE_HOLE_STR = "23.5 (7/8 in clearance)"

def _dist(a, b):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped)
    return d.Value()

def corner_block_clearances(theta, shape, g):
    """(d) metal round every hole and washer seat, (e) wall between the landing corner and the joint face; measured on solids
    in the block frame, with the closed-form value beside each one"""
    V = cq.Vector
    solid = shape.val()
    m, cosb, q = g["mitre"], g["cosb"], g["q"]
    air = CB.pocket_air(theta)
    outer = cq.Workplane("XY").box(3000, 3000, 50, centered=(True, True, False)).translate((0, 0, -50)).val()
    cabin = cq.Workplane("XY").box(3000, 3000, 50, centered=(True, True, False)).translate((0, 0, CB.DEPTH)).val()
    res = dict(hole_to_landing=[], washer_to_landing_edge=[], hole_to_outer_face=[], hole_to_cabin_face=[], washer_to_outer_face=[], washer_to_cabin_face=[],
               washer_seat_on_flat_metal=[], hole_to_leg_end=[], washer_to_leg_end=[])
    ring = lambda h, n0, n1: (cq.Solid.makeCylinder(CB.WASHER_R, n1 - n0, V(*h["centre"]) + V(*h["axis"]) * n0, V(*h["axis"]))
                              .cut(cq.Solid.makeCylinder(h["dia"] / 2 + 0.01, n1 - n0 + 2, V(*h["centre"]) + V(*h["axis"]) * (n0 - 1), V(*h["axis"]))))
    for h in g["holes"]:
        cyl = cq.Solid.makeCylinder(h["dia"] / 2, CB.THK, V(*h["centre"]), V(*h["axis"]))
        res["hole_to_landing"].append(_dist(cyl, air))
        res["hole_to_outer_face"].append(_dist(cyl, outer)); res["hole_to_cabin_face"].append(_dist(cyl, cabin))
        res["hole_to_leg_end"].append((CB.LEG - h["xs"]) * cosb - h["dia"] / 2)
        if h["kind"] == "tie":
            seat = cq.Solid.makeCylinder(CB.WASHER_R, 0.05, V(*h["centre"]) + V(*h["axis"]) * CB.THK, V(*h["axis"]))
            res["washer_to_landing_edge"].append(_dist(seat, air))
            res["washer_to_outer_face"].append(_dist(seat, outer)); res["washer_to_cabin_face"].append(_dist(seat, cabin))
            res["washer_to_leg_end"].append((CB.LEG - h["xs"]) * cosb - CB.WASHER_R)
            # the washer must sit wholly on flat metal: the ring just under the seat is all metal, the ring just above it is all air
            under = ring(h, CB.THK - 0.05, CB.THK); above = ring(h, CB.THK, CB.THK + 1.0)
            res["washer_seat_on_flat_metal"].append(abs(under.intersect(solid).Volume() - under.Volume()) < 1e-3 and above.intersect(solid).Volume() < 1e-6)
    out = {k: (round(min(x), 2) if not isinstance(x[0], bool) else all(x)) for k, x in res.items()}
    # closed form, for the nearest column and the two rows
    xs0 = min(CB.TIE_COLS); r = CB.TIE_HOLE / 2
    out["closed_form"] = dict(
        hole_to_landing=round((xs0 - g["xs_wall"]) * cosb - r, 2), washer_to_landing_edge=round((xs0 - g["xs_wall"]) * cosb - CB.WASHER_R, 2),
        hole_to_outer_face=round(CB.ROWS_ZP[0] * math.cos(m) - CB.THK * math.sin(m) - r * math.cos(m), 2),
        hole_to_cabin_face=round(CB.DEPTH - (CB.ROWS_ZP[1] + r) * math.cos(m), 2),
        washer_to_outer_face=round((CB.ROWS_ZP[0] - CB.WASHER_R) * math.cos(m) - CB.THK * math.sin(m), 2),
        washer_to_cabin_face=round(CB.DEPTH - ((CB.ROWS_ZP[1] + CB.WASHER_R) * math.cos(m) - CB.THK * math.sin(m)), 2))
    out["hole_to_hole"] = round(min(CB.TIE_COLS[1] - CB.TIE_COLS[0] - CB.TIE_HOLE, (CB.DOWEL_ZP - CB.ROWS_ZP[0]) - r - CB.DOWEL / 2, (CB.ROWS_ZP[1] - CB.DOWEL_ZP) - r - CB.DOWEL / 2), 2)
    # (e) the wall between the landing corner and the joint face, at the outer end and at the cabin end
    ex, t, nu = CB.face_frame(g)
    beyond = cq.Workplane("XY").box(3000, 3000, 3000).val().intersect(     # everything outside leg A's joint plane
        cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon([V(-1500, 0, 0) + V(*t) * (-1500), V(1500, 0, 0) + V(*t) * (-1500), V(1500, 0, 0) + V(*t) * 1500, V(-1500, 0, 0) + V(*t) * 1500], close=True)), V(*nu) * (-800)))
    wall = {}
    for label, z0, z1 in (("z0", 0.0, 1.0), ("z400", CB.DEPTH - 1.0, CB.DEPTH)):
        wall[label] = round(_dist(CB.pocket_air(theta, z0, z1), beyond), 3)
    fil = [f for f in solid.Faces() if f.geomType() == "CYLINDER" and abs(f._geomAdaptor().Cylinder().Radius() - CB.R_IN) < 1e-6
           and abs(abs(cq.Vector(f._geomAdaptor().Cylinder().Axis().Direction()).dot(V(*g["sigma"]).normalized())) - 1) < 1e-6]
    out["landing_wall_sharp_corner"] = wall
    out["landing_wall_closed_form"] = round(g["wall_min"], 3)
    out["landing_wall_at_R10_fillet"] = round(min(_dist(f, beyond) for f in fil), 3) if fil else None
    out["n_R10_fillet_faces"] = len(fil)
    out["a_vertical_landing_breaks_the_joint_face_at_z"] = round((g["d_b"] - g["d_min"]) / g["k"], 1)
    return out

def build_corner_blocks(which):
    allowed = CB.columns_allowed()
    for pid, th, name in (("CB-01", 120, "Corner block, hexagon corner (120 deg), leaning joint faces, 2219-T852"),
                          ("CB-02", 108, "Corner block, pentagon corner (108 deg), leaning joint faces, 2219-T852")):
        if not which(pid):
            continue
        s, g, log = CB.corner_block(th)
        for mm in log:
            FAILED_BLENDS.append(f"{pid}: {mm}")
        cl = corner_block_clearances(th, s, g)
        lean = g["mitre_deg"]; other = "pentagon" if th == 120 else "hexagon"
        rows_z = [round(z * math.cos(g["mitre"]), 1) for z in CB.ROWS_ZP]; dz = round(CB.DOWEL_ZP * math.cos(g["mitre"]), 1)
        xfrom = [[round(x + g["q"] * z, 1) for z in CB.ROWS_ZP] for x in CB.TIE_COLS]
        al = allowed[108]; alh = allowed[120]
        notes = (f"PROPOSAL of 9 Nov for the 13 Nov review (Marco, Rick); supersedes the straight block of 8 Nov. One solid block per panel corner, 2219-T852 hand forging, machined; "
                 f"three bolt together at a vertex (A-03). TRUE GEOMETRY: each leg's outer face IS the seam's joint plane, the radial plane through the shell edge and the sphere "
                 f"centre, which leans {lean:.3f} deg from the panel normal toward the panel interior. The two joint planes of the corner meet on the vertex line (vertex to sphere "
                 f"centre), which in this panel's frame leans {g['spine_lean_deg']:.2f} deg along the corner bisector, so the whole block is one constant outline swept along the vertex "
                 f"line (an oblique prism) and cut flat to the panel planes at z 0 (outer face) and z 400 (cabin face). Legs 230 long from the vertex line, {CB.THK:.0f} thick measured "
                 f"normal to the joint face ({g['th']:.1f} in a section parallel to the panel), inner faces parallel to the joint faces, so the tie nuts seat flat; leg end faces "
                 f"parallel to the vertex line. Along the leaning face (z') the joint face is {g['zp_joint_end']:.1f} long. "
                 f"HOLES, all normal to the joint face: four tie holes {CB.TIE_HOLE} mm per face (7/8-14 Inconel 718 studs, 198 kN preload) in rows at z' {CB.ROWS_ZP[0]} and {CB.ROWS_ZP[1]} "
                 f"(z {rows_z[0]} and {rows_z[1]} on the face) and two 20 mm dowel holes (room for 24) at z' {CB.DOWEL_ZP} (z {dz}), the same z' on both block types. Columns at "
                 f"{CB.TIE_COLS[0]:.0f} and {CB.TIE_COLS[1]:.0f} mm along the edge FROM THE VERTEX LINE at each row's depth (pitch 56), so the columns run parallel to the vertex line; "
                 f"from the z 0 vertex the holes are at {xfrom[0][0]} / {xfrom[0][1]} mm (column 1, rows 1 / 2) and {xfrom[1][0]} / {xfrom[1][1]} mm (column 2). "
                 f"WHY {CB.TIE_COLS[0]:.0f} / {CB.TIE_COLS[1]:.0f}: the rib landing's wall meets the leg's inner face {alh['pocket_edge_xs']:.1f} mm (hexagon) and {al['pocket_edge_xs']:.1f} mm "
                 f"(pentagon) from the vertex line; a {CB.TIE_HOLE} hole clears it from {al['hole_tangent']:.1f}, a 45 mm washer from {al['washer_tangent_sharp_edge']:.1f} and, clear of the 2 mm "
                 f"chamfer, from {al['washer_clear_of_chamfer']:.1f} (pentagon governs; hexagon {alh['washer_clear_of_chamfer']:.1f}). The briefed 87 / 143 is not possible; "
                 f"{CB.TIE_COLS[0]:.0f} is the nearest round position, 6 mm nearer the vertex line than the 136 of 8 Nov, the same on both blocks so the holes meet. "
                 f"MEASURED ON THIS SOLID: nearest hole to the landing {cl['hole_to_landing']} mm, washer seat to the landing's edge {cl['washer_to_landing_edge']} mm (sharp edge; 2 mm less "
                 f"to the chamfer), every washer wholly on flat metal: {cl['washer_seat_on_flat_metal']}; hole to the outer face {cl['hole_to_outer_face']} mm and to the cabin face "
                 f"{cl['hole_to_cabin_face']} mm, washer to the outer face {cl['washer_to_outer_face']} mm and to the cabin face {cl['washer_to_cabin_face']} mm; hole to the leg end "
                 f"{cl['hole_to_leg_end']} mm. "
                 f"LANDING for the main rib end: 110 wide (100 flange plus 5 a side) along the bisector, its walls and bottom parallel to the vertex line, bottom {g['d_b']:.0f} mm from "
                 f"the vertex line, walls {g['wall_len']:.1f} mm long where they cut the legs' inner faces, R10 at the two inside corners, 2 mm chamfers on every outside edge. Metal "
                 f"between the landing corner and the joint face: {cl['landing_wall_sharp_corner']['z0']} mm at z 0 and {cl['landing_wall_sharp_corner']['z400']} mm at z 400 (sharp corner; "
                 f"{cl['landing_wall_at_R10_fillet']} mm at the R10), the same at every depth because the landing follows the vertex line. It has to: a landing cut straight along "
                 f"the panel z would break out through the joint faces {cl['a_vertical_landing_breaks_the_joint_face_at_z']} mm below the outer face (the vertex line moves "
                 f"{g['k'] * CB.DEPTH:.0f} mm along the bisector over the 400 depth). So the main rib's end is cut on the same lean ({g['spine_lean_deg']:.2f} deg from square) and "
                 f"the rib is longer at its outer flange than at the cabin flange; P-04 is still drawn with square ends. "
                 f"MACHINING: every face is a plane or an R10 cylinder parallel to the vertex line, and the landing consumes the re-entrant corner between the legs, so there is no "
                 f"undercut and no sharp inside corner. The two R10 corners run {CB.DEPTH / math.cos(math.radians(g['spine_lean_deg'])):.0f} mm along the vertex line: an end mill cannot "
                 f"reach that far plunging along the line, so they are cut from the open (cabin interior) side with a 20 mm ball or R10 bull-nose cutter run along the vertex line, "
                 f"about {g['wall_len'] + 20:.0f} mm stick-out. With the vertex line on a rotary axis one set-up cuts the joint faces, inner faces, landing and all holes (the holes are "
                 f"square to the joint faces, which contain that axis); the two end cuts at z 0 and z 400 are {g['spine_lean_deg']:.1f} deg off square to the axis and take one more "
                 f"set-up each. Acute edges of {90 - lean:.1f} deg where the joint faces meet z 0 and the inner faces meet z 400, chamfered 2 mm. "
                 f"Not modelled: the rib fixing in the landing, the O10 corner seal path (the three chamfered spines leave a channel about 2 mm across down the vertex line), tie nuts and washers. "
                 f"The C1 model should be rerun with these hole positions.")
        dims = dict(legs=f"2 x 230 from the vertex line, {CB.THK:.0f} thick normal to the joint face, at {th} deg in plan", joint_face_lean=f"{lean:.3f} deg from the panel normal",
                    vertex_line_lean=f"{g['spine_lean_deg']:.2f} deg along the bisector (moves {g['k'] * CB.DEPTH:.1f} over z 400)",
                    depth="z 0 to z 400, both ends flat to the panel planes", joint_face_length_along_lean=round(g["zp_joint_end"], 1),
                    tie_hole=TIE_HOLE_STR + ", normal to the joint face", tie_columns_from_vertex_line=f"{CB.TIE_COLS[0]:.0f}, {CB.TIE_COLS[1]:.0f} (pitch 56), parallel to the vertex line",
                    tie_columns_from_z0_vertex=f"{xfrom[0][0]}, {xfrom[1][0]} (row 1); {xfrom[0][1]}, {xfrom[1][1]} (row 2)",
                    tie_rows_along_face=f"z' {CB.ROWS_ZP[0]}, {CB.ROWS_ZP[1]} (z {rows_z[0]}, {rows_z[1]})", dowel=f"20 mm (room for 24) at z' {CB.DOWEL_ZP} (z {dz})",
                    landing=f"110 wide, bottom {g['d_b']:.0f} from the vertex line, walls {g['wall_len']:.1f}, parallel to the vertex line",
                    landing_wall_to_joint_face=f"{g['wall_min']:.1f} (constant with depth)", inside_radius="R10 (landing corners)", outside_chamfer=2.0, stock="2219-T852 hand forging")
        register(pid, name, s, "2219-T852", notes, dims, rev=REV9, source="RE-06-2, Ansys C1 (5 Nov), Marco's review (7 Nov), true polyhedron geometry (9 Nov)")
        CHECKS.pop(pid, None)
        check(pid, bbox=bbox(s), valid_solid=s.val().isValid(), expected_envelope=f"oblique prism, legs 230 from the vertex line, 50 thick normal to the joint face, z 0 to 400, at {th} deg",
              joint_face_lean_deg=round(lean, 4), vertex_line_lean_deg=round(g["spine_lean_deg"], 4), tie_holes=g["n_tie_holes"], dowel_holes=g["n_dowel_holes"],
              hole_volume=round(g["hole_volume"]), hole_volume_expected=round(g["hole_volume_expected"]),
              tie_columns_xs=list(CB.TIE_COLS), tie_columns_allowed={k: round(x, 2) for k, x in allowed[th].items()}, tie_columns_brief="87/143 not possible; 136/192 on 8 Nov",
              landing_bottom_from_vertex_line=g["d_b"], landing_wall_len=round(g["wall_len"], 1), clearances=cl, blends_failed=log)

# ============================================================ HP-01 / HP-01M / HP-02 / HP-03 hardpoint
HP_L, HP_T, STUB_L = 240.0, 50.0, 60.0
FD, FWEB = L.FD, L.FWEB                               # 180, 20; joint face at x = 20, panel side x < 0 (P-06 convention)
GW, GD = v("seal", "gland_width"), v("seal", "gland_depth")    # 7.1 x 4.0
Z_G1 = v("seal", "outer_cord_z"); Z_G2 = Z_G1 + v("seal", "centreline_spacing")   # 18, 32
Z_BOLT = v("seam_bolt", "row_z")                      # 58
D_BOLT = 8.5
PIN_D, PIN_PITCH, PIN_L = 40.0, 60.0, 160.0
FIT_L, FIT_D, FIT_T = 200.0, 60.0, 30.0               # fitting half: along seam x deep (z) x thick (x)
FIT_HOLE, FIT_TAP = 10.0, 8.5                         # 10 mm clearance in the fitting, 8.5 tap drill (M10) 35 deep in the block
Z_PIN_AS_DRAWN, Z_PIN_MOVED = 140.0, 76.0
BOLT_Y = (-(HP_L / 2 - 31.25), HP_L / 2 - 31.25)      # +-88.75: inside the block. An artefact of the 8 Nov solid, kept on HP-01 only
BOLT_Y_WEB = (-137.5, 137.5)                           # 9 Nov, HP-01M: the plain bolts beside the block, in the 20 mm web, where the HP1M model had them
WASHER_SEAM = 16.0
HP_BLEND = 10.0
FLIGHT_BOLTS_FROM_HP = (131.25, 141.25)                # nearest seam bolts to a hardpoint centre in the 3-5-5-3 flight layout (sheets_flight_revF.py)

def fitting_hole_pattern(zc):
    """six fixing holes clear of the three 40 bores: two columns of two at the ends, one each between the bores"""
    return [(-90.0, zc - 20), (-90.0, zc + 20), (90.0, zc - 20), (90.0, zc + 20), (-30.0, zc), (30.0, zc)]

def hardpoint_clearances(zc, bolt_z, bolt_y=BOLT_Y):
    bores = [(k * PIN_PITCH, zc) for k in (-1, 0, 1)]
    bolts = [(y, bolt_z) for y in bolt_y]
    d_bore_bolt = min(math.hypot(b[0] - q[0], b[1] - q[1]) - PIN_D / 2 - D_BOLT / 2 for b in bores for q in bolts)
    d_bore_gland = (zc - PIN_D / 2) - (Z_G2 + GW / 2)
    d_bore_lip = (FD - 10) - (zc + PIN_D / 2)
    pad = (zc - FIT_D / 2, zc + FIT_D / 2)
    bolt_edge_vs_pad = (bolt_z - D_BOLT / 2) - pad[1]          # positive: hole clear above the pad
    washer_vs_pad = (bolt_z - 8.0) - pad[1]                    # 16 mm washer
    fit_holes = fitting_hole_pattern(zc)
    d_fithole_bolt = min(math.hypot(f[0] - q[0], f[1] - q[1]) - FIT_TAP / 2 - D_BOLT / 2 for f in fit_holes for q in bolts)
    d_fithole_bore = min(math.hypot(f[0] - b[0], f[1] - b[1]) - FIT_TAP / 2 - PIN_D / 2 for f in fit_holes for b in bores)
    bolt_under_pad = (pad[0] - 8.0 < bolt_z < pad[1] + 8.0) and abs(bolt_y[1]) - 8.0 < FIT_L / 2
    yb = abs(bolt_y[1]); w = WASHER_SEAM / 2
    beside = None
    if yb > HP_L / 2:      # the bolt is in the 20 mm web beside the block
        over = (HP_L / 2 + HP_BLEND) - (yb - w)                      # how far the washer reaches onto the blend's run-out on the web face
        beside = dict(bolt_y=yb, in_web_20mm=True, washer16_to_block_end_face=round(yb - w - HP_L / 2, 2), washer16_to_R10_blend_runout=round(-over, 2),
                      blend_height_under_washer_edge=round(HP_BLEND - math.sqrt(HP_BLEND ** 2 - max(over, 0.0) ** 2), 4), largest_blend_radius_that_clears=round(yb - w - HP_L / 2, 2),
                      washer16_to_fitting_pad_end_along_seam=round(yb - w - FIT_L / 2, 2), hole_edge_to_block_end_face=round(yb - D_BOLT / 2 - HP_L / 2, 2),
                      hole_edge_to_stub_end=round(HP_L / 2 + STUB_L - yb - D_BOLT / 2, 2), flight_layout_nearest_bolts_from_hp_centre=list(FLIGHT_BOLTS_FROM_HP),
                      washer16_to_blend_runout_at_flight_positions=[round(f - w - HP_L / 2 - HP_BLEND, 2) for f in FLIGHT_BOLTS_FROM_HP])
    return dict(pin_z=zc, bolt_z=bolt_z, bolt_y=list(bolt_y), plain_bolts_beside_the_block=beside, pad_z=list(pad), wall_bore_to_bolt_hole=round(d_bore_bolt, 1), bore_to_gland=round(d_bore_gland, 1),
                bore_to_lip_underside=round(d_bore_lip, 1), bolt_hole_edge_above_pad=round(bolt_edge_vs_pad, 2), washer16_above_pad=round(washer_vs_pad, 1),
                bolt_nut_under_fitting_pad=bolt_under_pad, wall_fitting_tap_to_bolt=round(d_fithole_bolt, 1), wall_fitting_tap_to_bore=round(d_fithole_bore, 1))

def hardpoint_block(zc, bolt_z, log, bolt_y=BOLT_Y):
    blk = box(HP_T, HP_L, FD, FWEB - HP_T, -HP_L / 2, 0)                       # x -30 .. 20
    stub = box(FWEB, HP_L + 2 * STUB_L, FD, 0, -(HP_L / 2 + STUB_L), 0)         # web stubs, one box through (y -180 .. 180)
    s = blk.union(stub)
    try:   # R10 blend block -> web at the two inside corners (x 0, y +-120)
        edges = [e for e in s.edges("|Z").vals() if abs(e.Center().x) < 0.5 and abs(abs(e.Center().y) - HP_L / 2) < 0.5]
        s = s.newObject(edges).fillet(10.0)
    except Exception as e:
        log.append(f"HP block R10 blends failed: {e}")
    v0 = s.val().Volume()
    cuts = []
    for zg in (Z_G1, Z_G2):   # glands on the joint face, full length
        cuts.append(box(GD + 1, HP_L + 2 * STUB_L + 2, GW, FWEB - GD, -(HP_L / 2 + STUB_L + 1), zg - GW / 2))
    for y in bolt_y:
        cuts.append(cyl_x(D_BOLT, FWEB - HP_T - 1, FWEB + 1, y, bolt_z))
    for k in (-1, 0, 1):
        cuts.append(cyl_x(PIN_D, FWEB - HP_T - 1, FWEB + 1, k * PIN_PITCH, zc))
    for (y, z) in fitting_hole_pattern(zc):
        cuts.append(cyl_x(FIT_TAP, FWEB - HP_T - 1, FWEB - HP_T + 35, y, z))
    vols = []
    for c in cuts:
        before = s.val().Volume()
        s = s.cut(c)
        vols.append(round(before - s.val().Volume()))
    return s, v0, vols

def build_hardpoint(which):
    for pid, zc, bolt_z, name in (("HP-01", Z_PIN_AS_DRAWN, Z_BOLT, "Hardpoint block in the frame, 50 thick, as drawn (pins at z 140)"),
                                  ("HP-01M", Z_PIN_MOVED, Z_BOLT, "Hardpoint block, moved fitting (pins at z 76), plain bolts beside the block")):
        if not which(pid):
            continue
        log = []
        by = BOLT_Y_WEB if pid == "HP-01M" else BOLT_Y
        s, v0, vols = hardpoint_block(zc, bolt_z, log, by)
        for m in log:
            FAILED_BLENDS.append(f"{pid}: {m}")
        cl = hardpoint_clearances(zc, bolt_z, by)
        cl_brief = cl_110 = None
        common = (f"PROPOSAL for the 13 Nov review. The frame web thickened from 20 to {HP_T:.0f} mm over {HP_L:.0f} mm of the seam at a hardpoint (three per seam at the quarter "
                  f"points), joint face flat at x 20 (P-06 convention, panel side toward -x), modelled alone with a 60 mm stub of the 20 mm web at each end and R10 "
                  f"blends from the block to the web. The two 7.1 x 4.0 butyl glands at z 18 and 32 run through on the joint face (the fitting must not cover them: "
                  f"it sits on the panel side). Three 40 mm pin bores at 60 mm pitch through the thickness, two 8.5 mm seam bolt holes (the plain bolts beside the "
                  f"fitting, {'in the 20 mm web 17.5 mm beyond each end face of the block' if pid == 'HP-01M' else '31.25 mm inside each end face'}) and six 8.5 mm tap-drill holes 35 deep (M10) from the panel face for the fitting HP-02 (two pairs at the ends, "
                  f"one each between the bores; the brief's two rows of three cannot clear the three bores). The frame flange and lip (z 0-10 and 170-180) are not in "
                  f"this solid. SUPERSEDED IN CONCEPT (9 Nov): the three pin bores across the joint and the six tap holes belong to the schematic fitting of 8 Nov. The real TP3 fitting from the C3 "
                  f"model (HP-02A lug, HP-02B clevis, HP-03 pins along the depth; assembly A-05) bores nothing through the frame: its base blocks seat on the web's inner face and replace this local block, and "
                  f"the frame's only feature at a hardpoint is the slot for the lug. This entry is kept for the 13 Nov comparison of the two fitting depths and for the plain-bolt position.")
        if zc == Z_PIN_AS_DRAWN:
            notes = common + (f" AS DRAWN (RE-06-1): pins at z 140, fitting pads z 110 to 170; the pad touches the underside of the seat lip at z 170. "
                              f"Clearances: bore to seam bolt hole {cl['wall_bore_to_bolt_hole']} mm, bore to the inner gland {cl['bore_to_gland']} mm, bore to the lip underside "
                              f"{cl['bore_to_lip_underside']} mm. The HP1 run of 6-7 Nov shows this position fails: the fitting sits 64 mm below the line of the pull and acts as a hinge, "
                              f"the seals open at 0.22 to 0.47 atm. Kept so both positions can be compared on 13 Nov.")
        else:
            bs = cl["plain_bolts_beside_the_block"]
            notes = common + (f" MOVED (HP1M study of 7 Nov, passes): pins at z 76, fitting envelope z 46 to 106, on the line of the pull. Drawn straight, so z here is z' along the joint face. "
                              f"CORRECTED 9 Nov: the two plain seam bolts stay ON THE BOLT ROW at z' {Z_BOLT:.0f} and sit beside the block along the seam at y = +-{by[1]} mm from the hardpoint "
                              f"centre, in the 20 mm frame web, which is where the HP1M model had them; none is under the fitting pad (y +-100). The 8 Nov solid had put them inside the block "
                              f"at y +-88.75, found that the moved pad covered them, and moved them deeper to z 118: that clash was an artefact of the solid, not of the design, and the "
                              f"deeper position was wrong for the seal (D1: the seal gap grows when the bolt row moves away from the seals). The flight layout (3-5-5-3 at 75 pitch) has the "
                              f"nearest seam bolts {FLIGHT_BOLTS_FROM_HP[0]} and {FLIGHT_BOLTS_FROM_HP[1]} mm from the hardpoint centre, so +-137.5 is 6.25 / 3.75 mm off the drawn bays; one of the "
                              f"two has to move to the other (P-06H and P-06P are drawn with the flight bays). "
                              f"CLEARANCES: a 16 mm washer at y {by[1]} is {bs['washer16_to_block_end_face']} mm from the block's end face and {bs['washer16_to_fitting_pad_end_along_seam']} mm along "
                              f"the seam from the end of the fitting pad (which is also 30 mm further into the panel), the hole edge {bs['hole_edge_to_block_end_face']} mm from the end face. "
                              f"ONE THING DOES NOT CLEAR: the R10 blend from the block to the web runs out on the web face at y 130 and the washer's edge is at y 129.5, so the washer rides "
                              f"{-bs['washer16_to_R10_blend_runout']} mm onto the blend ({bs['blend_height_under_washer_edge']} mm proud there). A blend of R{bs['largest_blend_radius_that_clears']:.1f} "
                              f"or smaller clears, or the bolt at the flight position 141.25 ({bs['washer16_to_blend_runout_at_flight_positions'][1]} mm clear; at 131.25 the washer is "
                              f"{-bs['washer16_to_blend_runout_at_flight_positions'][0]} mm onto an R10). The blend is left at R10 here for the review. "
                              f"The 40 mm bore at z 76 (edges z 56 to 96) is {cl['bore_to_gland']} mm above the inner gland (z 28.5-35.5) and {cl['wall_bore_to_bolt_hole']} mm of metal from the "
                              f"nearest plain bolt hole; bore to the fitting tap holes {cl['wall_fitting_tap_to_bore']} mm, tap holes to the plain bolts {cl['wall_fitting_tap_to_bolt']} mm.")
        dims = dict(block=f"{HP_L:.0f} along the seam x {FD:.0f} deep x {HP_T:.0f} thick", web_stubs=f"20 x {STUB_L:.0f} each end, R10 blend", glands=f"2 x {GW} x {GD} at z {Z_G1:.0f} and {Z_G2:.0f}",
                    pin_bores=f"3 x {PIN_D:.0f} at {PIN_PITCH:.0f} pitch, z {zc:.0f}", seam_bolts=f"2 x {D_BOLT} at y +-{by[1]}, z' {bolt_z:.0f}" + (" (in the 20 mm web beside the block)" if pid == "HP-01M" else " (inside the block, 8 Nov artefact)"), fitting_fixing="6 x 8.5 tap drill (M10) 35 deep from the panel face",
                    fitting_pad_z=f"{zc - 30:.0f} to {zc + 30:.0f}")
        register(pid, name, s, "6061-T6", notes, dims, source="RE-06-1, Ansys HP1/HP1M (6-7 Nov), C3 (Oct)", **(dict(rev=REV9) if pid == "HP-01M" else {}))
        CHECKS.pop(pid, None)
        exp_bores = 3 * math.pi * (PIN_D / 2) ** 2 * HP_T
        check(pid, bbox=bbox(s), expected_envelope="50 x 360 x 180 (block 240 plus two 60 stubs)", cut_volumes=vols, pin_bore_volume_expected=round(exp_bores),
              pin_bore_volume=sum(vols[4:7]), seam_bolt_hole_volumes=vols[2:4], seam_bolt_hole_volume_expected=round(math.pi * (D_BOLT / 2) ** 2 * (FWEB if pid == "HP-01M" else HP_T)), n_holes=dict(glands=2, seam_bolts=2, pin_bores=3, fitting_taps=6), clearances=cl,
              clearances_with_bolts_at_z58=cl_brief, clearances_with_bolts_at_z110=cl_110, blends_failed=log)

# (the 8 Nov schematic fitting half HP-02 and 160 mm pin HP-03 were removed on 9 Nov: see build_hardpoint_fitting, from the C3 model)

# ============================================================ P-11 main rib lateral brace
def brace_plate():
    prof = [(4, 180), (12, 180), (12, 280), (24, 280), (24, 367), (76, 367), (76, 375), (16, 375), (16, 300), (4, 300)]
    s = cq.Workplane("XZ").polyline(prof).close().extrude(90).translate((0, 45, 0))
    try:   # inside corners for the cutter
        edges = [e for e in s.edges("|Y").vals() if (abs(e.Center().x - 12) < 0.5 and abs(e.Center().z - 280) < 0.5) or (abs(e.Center().x - 24) < 0.5 and abs(e.Center().z - 367) < 0.5)]
        s = s.newObject(edges).fillet(3.0)
    except Exception as e:
        FAILED_BLENDS.append(f"P-11 R3 inside corners failed: {e}")
    v0 = s.val().Volume()
    for z in (210.0, 260.0):
        s = s.cut(cyl_x(9.6, -20, 40, 0, z))
    return s, v0 - s.val().Volume()

def build_brace(which):
    if not which("P-11"):
        return
    a, hv = brace_plate()
    b = a.mirror("YZ")
    pair = cq.Workplane("XY").newObject([cq.Compound.makeCompound([a.val(), b.val()])])
    notes = (f"PROPOSAL, the size needs its own check. Requirement from the 4 Nov survival check: the 400 x 100 x 25 main rib buckles sideways if unbraced over 2.25 m "
             f"(0.79 of its load) and has 8.4 times margin braced at every secondary rib crossing (562.5 mm). This bracket holds the rib's cabin flange sideways at the node "
             f"where the secondary grid meets the main rib: a pair of 7075-T7351 plates, 8 mm thick and 90 mm wide, one each side of the 8 mm web, from z 180 (the "
             f"secondary grid's cabin face) to z 375 (the cap angles), with a 60 x 8 leg under the cap angle's horizontal leg, bolted through the web with two 3/8-24 A286 "
             f"bolts (9.6 mm holes at z 210 and 260, common to both plates). CHANGE AGAINST THE BRIEF: the cap angle P-04A has a 12 mm vertical leg down the web from z 300 to "
             f"375, so a flat 8 mm plate against the web cannot reach z 375; the plate is stepped out 12 mm at z 280-300 (20 thick there) and runs up the outside of the "
             f"angle's vertical leg (x 16-24) to the flange. R3 at the two machined inside corners; the notch corner at z 300 is left sharp for the angle. The foot at z 180 "
             f"stands on the main rib's seat ledge (z 170-180, 30 wide) beside the secondary rib's end and is not fixed to it here; whether the brace also needs a tie into the node star plate P-02 is open (Q95). The holes at z 210 and 260 clear the rib's cap bolt holes at z 360. One pair "
             f"at every secondary rib crossing: 3 per main rib on a hexagon, 2 or 3 on a pentagon.")
    dims = dict(plates="2 x 90 wide x 8 thick, z 180 to 375", step="12 mm out at z 280-300 to pass the cap angle's vertical leg", top_leg="60 x 8 under the cap angle, z 367-375",
                bolts="2 x 3/8-24 A286 through the web, 9.6 holes at z 210 and 260", material="7075-T7351")
    register("P-11", "Main rib lateral brace at a node, 7075-T7351 (pair)", pair, "7075-T7351", notes, dims, source="Does option B at 0.8 atm survive (4 Nov), Q95")
    check("P-11", bbox=bbox(pair), expected_envelope="152 x 90 x 195 (two plates, x -76 to 76)", hole_volume_per_plate=round(hv), hole_volume_expected=round(2 * math.pi * 4.8 ** 2 * 8))

# ============================================================ P-07 pane at 21 mm
def build_pane(which):
    if not which("P-07"):
        return
    s = L.pane()
    notes = ("Equilateral 531 mm (k 4 cut, 9.09 mm short of each rib centre line). Corners truncated 60 mm for the node star plates and clamp screws. Edges ground and polished, "
             "1 mm chamfers. Rests on the cabin face of the secondary rib inner flanges; pressure seats it. 21 mm since 5 November 2026 (SCHOTT's standard 1,700 x 1,300 sheet; 22 mm "
             "would need container loads); regenerated at 21 mm on 8 November, so the model, drawing views, STEP and GLB are now at 21 mm. 96 per hexagon.")
    register("P-07", "Pressure pane L7, 531 mm, 21 mm BOROFLOAT 33", s, "BOROFLOAT 33", notes, dict(side=L.PANE_SIDE, thickness=L.PANE_T, corner_cut=L.CORNER_CUT, bite_on_60mm_flange=20.9),
             rev="DECIDED 5 Nov 2026 (21 mm), regenerated 8 Nov", source="Rev E restack (24 Oct), rib study (2 Nov), Glass at 21 mm (4 Nov)")
    check("P-07", bbox=bbox(s), expected_envelope="531 x 459.9 x 21 before corner cuts", thickness=L.PANE_T)

# ============================================================ PL-01 pentagon closure triangle, and the pentagon geometry
EDGE = v("geometry", "edge")                                   # 2250
R_PENT = EDGE / (2 * math.sin(math.radians(36)))               # 1913.9 circumradius
A_PENT = EDGE / (2 * math.tan(math.radians(36)))               # 1548.4 apothem
PENT_V = [(R_PENT * math.cos(math.radians(-54 + 72 * k)), R_PENT * math.sin(math.radians(-54 + 72 * k))) for k in range(5)]   # V0 (-126 deg), V1 (-54 deg) make the bottom edge
PL_T = 10.0
CUT_RIB, CUT_FRAME, CUT_HUB = 10.0, 10.0, 100.0                 # see notes: brief said 100 and 100

def poly_wp(pts, h, z0=0.0):
    return cq.Workplane("XY").polyline(pts).close().extrude(h).translate((0, 0, z0))

def offset_line_poly(a, b, c, cut_ab, cut_bc, cut_ca):
    """triangle a-b-c (ccw) with each side moved inward by its cut: returns the three new corners"""
    import numpy as np
    pts = [np.array(a, float), np.array(b, float), np.array(c, float)]
    cuts = [cut_ab, cut_bc, cut_ca]
    lines = []
    for i in range(3):
        p, q = pts[i], pts[(i + 1) % 3]
        d = q - p; d /= np.linalg.norm(d)
        n = np.array([-d[1], d[0]])          # inward normal for a ccw triangle
        lines.append((p + n * cuts[i], d))
    out = []
    for i in range(3):   # corner between line i-1 and line i
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
        t = np.linalg.solve(A, p2 - p1)
        out.append(tuple(p1 + d1 * t[0]))
    return out

def pent_block_outline_at(k):
    """CB-02 outline placed at pentagon vertex k (legs along the two edges meeting there)"""
    pts, _, _, _ = CBS.outline_straight(108)
    vk = PENT_V[k]; vn = PENT_V[(k + 1) % 5]
    ang = math.atan2(vn[1] - vk[1], vn[0] - vk[0])
    c, s = math.cos(ang), math.sin(ang)
    return [(vk[0] + c * x - s * y, vk[1] + s * x + c * y) for (x, y) in pts]

def closure_triangle(k=0):
    """one of the five triangles: centre O, vertices V_k, V_k+1; ccw order O, V_k, V_k+1 -> sides O-Vk (rib), Vk-Vk+1 (frame), Vk+1-O (rib)"""
    O = (0.0, 0.0); a = PENT_V[k]; b = PENT_V[(k + 1) % 5]
    tri = offset_line_poly(O, a, b, CUT_RIB, CUT_FRAME, CUT_RIB)
    s = poly_wp(tri, PL_T, 180.0)
    v0 = s.val().Volume()
    s = s.cut(cyl_z(2 * CUT_HUB, 170, 200, 0, 0))                                   # clear the hub core (160 dia) by 20
    for kk in (k, (k + 1) % 5):                                                     # clear the two corner blocks
        s = s.cut(poly_wp(pent_block_outline_at(kk), 40, 170))
    return s, v0

def build_closure(which):
    if not which("PL-01"):
        return
    s, v0 = closure_triangle(0)
    area = s.val().Volume() / PL_T
    notes = (f"PROPOSAL. The pentagon's pressure closure: a 10 mm 6061-T6 plate cut as five triangles sealed at the five main ribs, one triangle shown (the bottom one of A-04, "
             f"centre to the two corners of a 2,250 mm edge). Which side of the ribs it goes on is OPEN (register Q57); drawn on the cabin side at the seat plane, z 180 to 190, "
             f"where the glass sits on a hexagon, so it rests on the secondary rib flanges (z 170-180), the main rib ledges and the frame web top and lip, like the panes. "
             f"Edges: {CUT_RIB:.0f} mm from each main rib centre line (24 mm bite on the 30 mm ledge, which runs from 4 to 34 mm off the centre line) and {CUT_FRAME:.0f} mm from the frame "
             f"joint face (60 mm seat on the web top and lip), a 20 mm wide seal land along all three edges (RTV or a butyl cord in a gland in the rib ledge, to decide). "
             f"The apex is cut back {CUT_HUB:.0f} mm from the centre to clear the 160 mm hub core, and the two outer corners are cut to the CB-02 corner block outline. "
             f"CHANGE AGAINST THE BRIEF: it said 100 mm from the rib centre lines and 100 mm from the frame, but a 100 mm cut-back leaves the plate 66 mm clear of the 30 mm ledge "
             f"and 30 mm clear of the lip, so it would seat on nothing; 10 mm is the pane rule (9.09). Confirm. Fixing (screws into the ribs through the land, or clamps) is not drawn. "
             f"CLASH AT THE APEX: the hub's fork cheeks (P-05, 4.1 to 14.1 mm off each main rib centre line, out to r 210, between z 54 and 346) cross the plate's edge line (10 mm off the centre line) between r 100 and r 210, so each triangle's two rib edges need a 15 mm cut-back over that 110 mm, or the cheeks notched at the seat plane; the same applies to the hexagon's innermost panes. Open.")
    dims = dict(thickness=PL_T, sides=f"rib edges {R_PENT:.0f} nominal, frame edge {EDGE:.0f} nominal, cut back {CUT_RIB:.0f}/{CUT_FRAME:.0f}", apex_cut=f"r {CUT_HUB:.0f} about the hub",
                corner_cuts="to the CB-02 outline", seal_land=20, area_m2=round(area / 1e6, 3), per_pentagon=5)
    register("PL-01", "Pentagon closure plate, one of five triangles, 10 mm 6061-T6", s, "6061-T6", notes, dims, source="TRUTH Rev F draft (5 Nov) pentagon, Q57", hidden=False)
    check("PL-01", bbox=bbox(s), expected_envelope=f"about {EDGE - 2*CUT_FRAME/math.tan(math.radians(54)):.0f} wide x {A_PENT - CUT_FRAME - 20:.0f} tall x 10", area_m2=round(area / 1e6, 3),
          uncut_triangle_area_m2=round(v0 / PL_T / 1e6, 3))

# ============================================================ A-03 corner node assembly on the real truncated icosahedron
PHI = (1 + 5 ** 0.5) / 2

def even_perms(t):
    a, b, c = t
    return [(a, b, c), (b, c, a), (c, a, b)]

def signs(t):
    out = set()
    for sa in (1, -1):
        for sb in (1, -1):
            for sc in (1, -1):
                out.add((sa * t[0], sb * t[1], sc * t[2]))
    return out

def truncated_icosahedron(edge):
    import numpy as np
    base = [(0, 1, 3 * PHI), (1, 2 + PHI, 2 * PHI), (PHI, 2, 2 * PHI + 1)]
    V = set()
    for b in base:
        for s in signs(b):
            for p in even_perms(s):
                V.add(tuple(round(x, 9) for x in p))
    V = np.array(sorted(V)) * (edge / 2.0)            # unit edge is 2 in these coordinates
    assert len(V) == 60, len(V)
    # face normals: pentagons along the icosahedron vertices, hexagons along the dodecahedron vertices
    pent_n = set()
    for s in signs((0, 1, PHI)):
        for p in even_perms(s):
            pent_n.add(p)
    hex_n = set(signs((1, 1, 1)))
    for s in signs((0, PHI, 1 / PHI)):          # dodecahedron vertices dual to the (0, 1, phi) icosahedron
        for p in even_perms(s):
            hex_n.add(p)
    faces = []
    for kind, ns, cnt in (("pent", pent_n, 5), ("hex", hex_n, 6)):
        for n in ns:
            n = np.array(n, float); n /= np.linalg.norm(n)
            d = V @ n
            idx = np.argsort(-d)[:cnt]
            assert abs(d[idx].max() - d[idx].min()) < 1e-6, (kind, d[idx])
            c = V[idx].mean(axis=0)
            # order around the centre
            e1 = V[idx[0]] - c; e1 -= n * (e1 @ n); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
            ang = [math.atan2((V[i] - c) @ e2, (V[i] - c) @ e1) for i in idx]
            order = [i for _, i in sorted(zip(ang, idx))]
            faces.append(dict(kind=kind, verts=order, normal_out=n, centre=c))
    assert len(faces) == 32
    return V, faces

def place_matrix(origin, ex, ey, ez):
    return cq.Matrix([[ex[0], ey[0], ez[0], origin[0]], [ex[1], ey[1], ez[1], origin[1]], [ex[2], ey[2], ez[2], origin[2]], [0, 0, 0, 1]])

def export_assembly(name, parts, colors, pid):
    """parts: list of (label, cq shape); writes STEP (cq.Assembly), merged STL, 4 SVG views; returns the compound"""
    asm = cq.Assembly(name=name)
    for (label, shp), col in zip(parts, colors):
        asm.add(shp, name=label, color=cq.Color(*col))
    asm.export(f"{OUT}/step/{name}.step")
    comp = cq.Compound.makeCompound([s.val() if hasattr(s, "val") else s for _, s in parts])
    exporters.export(comp, f"{OUT}/stl/{name}.stl", tolerance=0.3, angularTolerance=0.3)
    # per-part meshes for the coloured GLB (postprocess.py)
    pdir = f"{OUT}/stl/_parts/{name}"
    os.makedirs(pdir, exist_ok=True)
    for f in os.listdir(pdir):
        os.remove(os.path.join(pdir, f))
    manifest = []
    for i, ((label, shp), col) in enumerate(zip(parts, colors)):
        fn = f"{i:03d}_{label}.stl"
        exporters.export(shp, f"{pdir}/{fn}", tolerance=0.3, angularTolerance=0.3)
        manifest.append(dict(file=fn, label=label, color=list(col)))
    json.dump(manifest, open(f"{pdir}/manifest.json", "w"), indent=1)
    for view, d in dict(front=(0, -1, 0), top=(0, 0, 1), side=(1, 0, 0), iso=(1, -1.2, 0.8)).items():
        try:
            exporters.export(comp, f"{OUT}/svg/{name}_{view}.svg", opt=dict(width=520, height=380, marginLeft=12, marginTop=12, projectionDir=d, strokeWidth=0.5,
                             strokeColor=(30, 30, 30), hiddenColor=(160, 160, 160), showHidden=False, showAxes=False, focus=None))
        except Exception as e:
            print("   svg failed", name, view, e)
    return comp

COL = dict(al=(0.67, 0.70, 0.73), forging=(0.72, 0.66, 0.58), forging2=(0.60, 0.66, 0.74), forging3=(0.62, 0.72, 0.62), ti=(0.55, 0.59, 0.65), steel=(0.47, 0.51, 0.59), glass=(0.63, 0.82, 0.94), plate=(0.75, 0.78, 0.70), brace=(0.60, 0.62, 0.68))

def _cyl_axes(shape, radius, tol=1e-4):
    """axes (point, direction) of the cylindrical faces of this radius, in the shape's placed coordinates"""
    import numpy as np
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    out = []
    for f in shape.Faces():
        if f.geomType() != "CYLINDER":
            continue
        c = BRepAdaptor_Surface(f.wrapped).Cylinder()
        if abs(c.Radius() - radius) < tol:
            ax = c.Axis(); p = ax.Location(); d = ax.Direction()
            out.append((np.array([p.X(), p.Y(), p.Z()]), np.array([d.X(), d.Y(), d.Z()])))
    return out

def build_corner_node(which):
    if not which("A-03"):
        return
    import numpy as np
    from itertools import combinations
    V, faces = truncated_icosahedron(EDGE)
    vi = int(np.argmax(V[:, 2] * 1000 + V[:, 0]))          # the vertex with the largest z, deterministic
    fs = [f for f in faces if vi in f["verts"]]
    assert len(fs) == 3 and sorted(f["kind"] for f in fs) == ["hex", "hex", "pent"], [f["kind"] for f in fs]
    Vv = V[vi]
    nbrs = {}
    for f in fs:
        k = f["verts"].index(vi); n = len(f["verts"])
        for j in (f["verts"][(k - 1) % n], f["verts"][(k + 1) % n]):
            nbrs.setdefault(j, []).append(f)
    assert len(nbrs) == 3 and all(len(x) == 2 for x in nbrs.values())
    edge_lengths = [float(np.linalg.norm(V[j] - Vv)) for j in nbrs]
    hexblk, ghex, _ = CB.corner_block(120)
    pentblk, gpent, _ = CB.corner_block(108)
    tup = lambda a: tuple(float(x) for x in a)
    blocks, frames = [], []
    for f in fs:
        n_in = -f["normal_out"]                             # depth z goes inward
        k = f["verts"].index(vi); n = len(f["verts"])
        cand = [V[f["verts"][(k + 1) % n]] - Vv, V[f["verts"][(k - 1) % n]] - Vv]
        e1 = cand[0] / np.linalg.norm(cand[0]); e2 = cand[1] / np.linalg.norm(cand[1])
        ey = np.cross(n_in, e1)
        if ey @ e2 < 0:                                      # leg A must have the interior (leg B) on its +y side
            e1, e2 = e2, e1; ey = np.cross(n_in, e1)
        blk = hexblk if f["kind"] == "hex" else pentblk
        loc = cq.Location(cq.Plane(origin=tup(Vv), xDir=tup(e1), normal=tup(n_in)))
        blocks.append((f"{f['kind']}_block_{len(blocks)}", blk.val().moved(loc)))
        frames.append(dict(kind=f["kind"], face=f, e1=e1, e2=e2, ey=ey, n=n_in, interior_angle=math.degrees(math.acos(float(e1 @ e2)))))
    # ---- (a) pairwise interference of the three blocks
    interference = {}
    for (la, sa), (lb, sb) in combinations(blocks, 2):
        try:
            interference[f"{la} x {lb}"] = round(float(sa.intersect(sb).Volume()), 6)
        except Exception as e:
            interference[f"{la} x {lb}"] = f"boolean failed: {e}"
    # control: the same boolean must see an overlap when one block is pushed 0.5 mm into its neighbour across their shared joint face
    _e = [j for j, fp in nbrs.items() if any(fp_ is frames[0]["face"] for fp_ in fp) and any(fp_ is frames[1]["face"] for fp_ in fp)][0]
    _ed = (V[_e] - Vv) / np.linalg.norm(V[_e] - Vv); _ri = -Vv - (_ed @ -Vv) * _ed; _ri /= np.linalg.norm(_ri); _jn = np.cross(_ed, _ri)
    _sgn = float(np.sign((np.array(blocks[1][1].Center().toTuple()) - np.array(blocks[0][1].Center().toTuple())) @ _jn))
    control = round(float(blocks[0][1].moved(cq.Location(cq.Vector(*tup(_jn * 0.5 * _sgn)))).intersect(blocks[1][1]).Volume()), 1)
    # ---- the three seams at this vertex
    r_v = -Vv / np.linalg.norm(Vv)                           # vertex line, toward the sphere centre
    Q = math.sin(ghex["mitre"]) / math.tan(ghex["alpha"])   # the vertex line's slope along an edge, per mm of z'
    TIE_L, TIE_D, DOWEL_L = 300.0, 22.2, 100.0
    ties, dowels, seams = [], [], []
    raw = dict(axis_offset_mm=0.0, axis_angle_deg=0.0, offset_from_true_position_mm=0.0, joint_face_off_radial_plane_mm=0.0)
    for j, fpair in nbrs.items():
        e = V[j] - Vv; e /= np.linalg.norm(e)
        r_in = -Vv - (e @ -Vv) * e; r_in /= np.linalg.norm(r_in)       # in the radial plane, square to the edge, toward the centre (z')
        jn = np.cross(e, r_in)                                           # normal of the radial joint plane
        fa, fb = fpair
        dih = 180.0 - math.degrees(math.acos(float(np.clip(fa["normal_out"] @ fb["normal_out"], -1, 1))))
        leans = [math.degrees(math.acos(float(np.clip(r_in @ -f["normal_out"], -1, 1)))) for f in fpair]
        assert abs(Q - (r_v @ e) / (r_v @ r_in)) < 1e-9          # the vertex line in this joint plane
        # (b) the two blocks' joint faces against the true radial plane
        jf = []
        for (label, shp), fr in zip(blocks, frames):
            if not any(fr["face"] is f for f in fpair):
                continue
            best = None
            for f in shp.Faces():
                if f.geomType() != "PLANE" or f.Area() < 20000:
                    continue
                nrm = f.normalAt(); nrm = np.array([nrm.x, nrm.y, nrm.z])
                if abs(abs(nrm @ jn) - 1) > 1e-6:
                    continue
                dev = max(abs((np.array([p.X, p.Y, p.Z]) - Vv) @ jn) for p in f.Vertices())
                if best is None or dev < best[0]:
                    best = (dev, math.degrees(math.acos(min(1.0, abs(float(nrm @ jn))))), f.Area(), float(np.sign(nrm @ jn)), label)
            jf.append(best)
        assert len(jf) == 2 and all(x is not None for x in jf), jf
        raw["joint_face_off_radial_plane_mm"] = max(raw["joint_face_off_radial_plane_mm"], jf[0][0], jf[1][0])
        assert jf[0][3] * jf[1][3] < 0                            # the two faces look at each other
        # (c) holes: the expected axis of each tie and dowel, then the real cylindrical faces of the two blocks
        pairs = []
        for xs in CB.TIE_COLS:
            for kind, dia, zp in [("tie", CB.TIE_HOLE, z) for z in CB.ROWS_ZP] + [("dowel", CB.DOWEL, CB.DOWEL_ZP)]:
                c = Vv + e * (xs + Q * zp) + r_in * zp
                found = []
                for (label, shp), fr in zip(blocks, frames):
                    if not any(fr["face"] is f for f in fpair):
                        continue
                    cands = [(float(np.linalg.norm(np.cross(c - p, d))), p, d) for p, d in _cyl_axes(shp, dia / 2) if abs(abs(d @ jn) - 1) < 1e-3]
                    cands = [x for x in cands if x[0] < 5.0]
                    assert len(cands) >= 1, (label, kind, xs, zp)
                    _, p, d = min(cands, key=lambda x: x[0])
                    hit = p + d * (((Vv - p) @ jn) / (d @ jn))        # where this hole's axis crosses the joint plane
                    found.append((hit, d * np.sign(d @ jn)))
                assert len(found) == 2
                off = float(np.linalg.norm(found[0][0] - found[1][0]))
                ang = math.degrees(math.acos(float(np.clip(found[0][1] @ found[1][1], -1, 1))))
                off_c = max(float(np.linalg.norm(h - c)) for h, _ in found)
                raw["axis_offset_mm"] = max(raw["axis_offset_mm"], off); raw["axis_angle_deg"] = max(raw["axis_angle_deg"], ang); raw["offset_from_true_position_mm"] = max(raw["offset_from_true_position_mm"], off_c)
                pairs.append(dict(kind=kind, xs=xs, zp=zp, axis_offset_at_joint_plane=off, axis_angle_deg=ang, offset_from_true_position=off_c,
                                  worst_offset_over_the_100_grip=off + 50.0 * math.sin(math.radians(ang))))
                if kind == "tie":
                    ties.append(cq.Solid.makeCylinder(TIE_D / 2, TIE_L, cq.Vector(*tup(c - jn * TIE_L / 2)), cq.Vector(*tup(jn))))
                else:
                    dowels.append(cq.Solid.makeCylinder(CB.DOWEL / 2, DOWEL_L, cq.Vector(*tup(c - jn * DOWEL_L / 2)), cq.Vector(*tup(jn))))
        seams.append(dict(edge_to_vertex=int(j), faces=f"{fa['kind']}-{fb['kind']}", dihedral_between_panels=round(dih, 3),
                          expected=138.19 if fa["kind"] == fb["kind"] == "hex" else 142.623, joint_plane_lean_from_each_panel_normal_deg=[round(x, 3) for x in leans],
                          edge_length=round(float(np.linalg.norm(V[j] - Vv)), 3),
                          joint_faces_off_the_radial_plane_mm=[round(x[0], 6) for x in jf], joint_faces_angle_to_radial_plane_deg=[round(x[1], 6) for x in jf],
                          joint_faces_coplanar_within_mm=round(jf[0][0] + jf[1][0], 6), joint_face_areas_mm2=[round(x[2]) for x in jf],
                          tie_pairs_max_axis_offset_mm=round(max(p["axis_offset_at_joint_plane"] for p in pairs if p["kind"] == "tie"), 6),
                          dowel_pairs_max_axis_offset_mm=round(max(p["axis_offset_at_joint_plane"] for p in pairs if p["kind"] == "dowel"), 6),
                          max_axis_angle_deg=round(max(p["axis_angle_deg"] for p in pairs), 6),
                          max_offset_over_the_grip_mm=round(max(p["worst_offset_over_the_100_grip"] for p in pairs), 6),
                          max_offset_from_true_position_mm=round(max(p["offset_from_true_position"] for p in pairs), 6), n_pairs=len(pairs)))
    # ---- ties and dowels through the mated holes: none may touch a block (22.2 in 23.5; the dowel is line to line, so it is tested 0.02 under size) or each other
    tie_hits = [round(float(t.intersect(s).Volume()), 6) for t in ties for _, s in blocks]
    dowel_hits = []
    for d in dowels:
        ax = BRepAdaptorAxis(d)
        thin = cq.Solid.makeCylinder(CB.DOWEL / 2 - 0.01, DOWEL_L, ax[0], ax[1])
        dowel_hits += [round(float(thin.intersect(s).Volume()), 6) for _, s in blocks]
    fasteners = ties + dowels
    fast_hits = [round(float(a.intersect(b).Volume()), 6) for a, b in combinations(fasteners, 2)]
    # wedge angle of each block at the vertex line (the three must close the full turn)
    wedge = []
    for fr in frames:
        ns = []
        for e in (fr["e1"], fr["e2"]):
            r_in = -Vv - (e @ -Vv) * e; r_in /= np.linalg.norm(r_in)
            w = e - (e @ r_v) * r_v; w /= np.linalg.norm(w)            # direction of this joint plane seen along the vertex line
            ns.append(w)
        wedge.append(round(math.degrees(math.acos(float(np.clip(ns[0] @ ns[1], -1, 1)))), 3))
    # ---- node frame: vertex at the origin, +z inward along the vertex line, x along the hex-hex edge
    hexhex = [j for j, fp in nbrs.items() if fp[0]["kind"] == fp[1]["kind"] == "hex"][0]
    ex = V[hexhex] - Vv; ex -= r_v * (ex @ r_v); ex /= np.linalg.norm(ex)
    inv = cq.Location(cq.Plane(origin=tup(Vv), xDir=tup(ex), normal=tup(r_v))).inverse
    W = lambda s: cq.Workplane("XY").newObject([s.moved(inv)])
    parts = [(label, W(s)) for label, s in blocks] + [(f"tie_{i}", W(s)) for i, s in enumerate(ties)] + [(f"dowel_{i}", W(s)) for i, s in enumerate(dowels)]
    colors = [COL["forging"], COL["forging2"], COL["forging3"]] + [COL["steel"]] * (len(ties) + len(dowels))
    name = "A-03_corner_node"
    comp = export_assembly(name, parts, colors, "A-03")
    m_blocks = [round(s.Volume() * RHO["2219-T852"], 3) for _, s in blocks]
    masses = dict(blocks_kg=round(sum(s.Volume() for _, s in blocks) * RHO["2219-T852"], 2), ties_kg=round(sum(s.Volume() for s in ties) * RHO["Inconel 718"], 2),
                  dowels_kg=round(sum(s.Volume() for s in dowels) * RHO["A286"], 2))
    total = masses["blocks_kg"] + masses["ties_kg"] + masses["dowels_kg"]
    worst = dict(block_interference_mm3=max(x if isinstance(x, float) else 1e9 for x in interference.values()),
                 joint_faces_coplanar_mm=max(s["joint_faces_coplanar_within_mm"] for s in seams),
                 tie_axis_offset_mm=max(s["tie_pairs_max_axis_offset_mm"] for s in seams), dowel_axis_offset_mm=max(s["dowel_pairs_max_axis_offset_mm"] for s in seams),
                 axis_angle_deg=max(s["max_axis_angle_deg"] for s in seams), offset_over_grip_mm=max(s["max_offset_over_the_grip_mm"] for s in seams),
                 tie_through_block_mm3=max(tie_hits), dowel_through_block_mm3=max(dowel_hits), fastener_to_fastener_mm3=max(fast_hits))
    passed = dict(a_no_interference=worst["block_interference_mm3"] < 1.0, b_coplanar=worst["joint_faces_coplanar_mm"] < 0.01,
                  c_ties_coaxial=worst["tie_axis_offset_mm"] < 0.05 and worst["offset_over_grip_mm"] < 0.05, c_dowels_coaxial=worst["dowel_axis_offset_mm"] < 0.05,
                  ties_and_dowels_pass_through=worst["tie_through_block_mm3"] < 1e-3 and worst["dowel_through_block_mm3"] < 1e-3 and worst["fastener_to_fastener_mm3"] < 1e-3)
    notes = (f"PROPOSAL of 9 Nov, rebuilt with the leaning corner blocks. The three corner blocks of one vertex of the real truncated icosahedron (edge 2,250 mm, 11,151 mm across; the 60 "
             f"vertices from the standard coordinates, scaled): two hexagon blocks CB-01 and one pentagon block CB-02, each placed in its own panel plane with its vertex at the shared "
             f"vertex, its legs along the two panel edges meeting there and its depth along the panel's inward normal. Panel dihedrals measured at this vertex: "
             + "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in seams) + " deg; the radial joint plane of each seam leans "
             + "; ".join(f"{d['faces']} {d['joint_plane_lean_from_each_panel_normal_deg'][0]} and {d['joint_plane_lean_from_each_panel_normal_deg'][1]}" for d in seams) +
             f" deg from the two panel normals. WHAT WAS CHECKED ON THE PLACED SOLIDS: (a) the three blocks do not overlap: pairwise common volume "
             + ", ".join(f"{x}" for x in interference.values()) + f" mm3, and the same test reports {control:.0f} mm3 when one block is pushed 0.5 mm into its neighbour (the straight blocks of 8 Nov overlapped in a 75 mm prism along each edge); (b) on each seam the two blocks' "
             f"joint faces lie on the radial plane, off it by at most {max(max(s['joint_faces_off_the_radial_plane_mm']) for s in seams):.6f} mm and coplanar with each other within "
             f"{worst['joint_faces_coplanar_mm']:.6f} mm; (c) all 12 facing tie hole pairs and 6 dowel hole pairs are coaxial: axes apart by at most {worst['tie_axis_offset_mm']:.6f} mm "
             f"(ties) and {worst['dowel_axis_offset_mm']:.6f} mm (dowels) at the joint plane, {worst['axis_angle_deg']:.6f} deg between axes. The 12 ties ({TIE_D} x {TIE_L:.0f}, the "
             f"7/8-14 Inconel 718 studs with their nut length) and 6 dowels (20 x {DOWEL_L:.0f}) are drawn through the mated holes, normal to the joint planes, rows at z' "
             f"{CB.ROWS_ZP[0]} and {CB.ROWS_ZP[1]}, dowels at z' {CB.DOWEL_ZP}, columns {CB.TIE_COLS[0]:.0f} and {CB.TIE_COLS[1]:.0f} mm from the vertex line; none touches a block or another "
             f"fastener (common volumes {worst['tie_through_block_mm3']}, {worst['dowel_through_block_mm3']}, {worst['fastener_to_fastener_mm3']} mm3; the 300 mm stud length is carried "
             f"from 8 Nov and is not a sized part). The three blocks' wedge angles about the vertex line are {wedge[0]}, {wedge[1]} and {wedge[2]} deg, {sum(wedge):.3f} in all. "
             f"The 2 mm chamfers on the three spines leave a three-sided channel about 2 mm across down the vertex line: it is the path the O10 corner seal has to close, not modelled. "
             f"Exported in a node frame: vertex at the origin, +z inward along the vertex line, x along the hex-hex edge; the vertex sat at {[round(float(x), 1) for x in Vv]} in the "
             f"polyhedron frame. Masses: blocks {masses['blocks_kg']} kg ({', '.join(str(x) for x in m_blocks)}), ties {masses['ties_kg']} kg, dowels {masses['dowels_kg']} kg.")
    PARTS["A-03"] = dict(id="A-03", name="Corner node assembly: two hexagon blocks and one pentagon block mated at a vertex, with 12 ties and 6 dowels through the mated holes",
                         material="2219-T852 + Inconel 718 + A286", mass_kg=round(total, 3), notes=notes,
                         dims=dict(blocks=3, ties=len(ties), dowels=len(dowels), edge=EDGE, seams=seams, interference_mm3=interference, worst=worst, passed=passed, wedge_angles_deg=wedge,
                                   vertex_xyz=[round(float(x), 1) for x in Vv]),
                         rev=REV9, source="Truncated icosahedron coordinates; RE-06-2; C1 (5 Nov)", files=name, bbox_mm=bbox(comp), masses=masses, assembly=True)
    CHECKS.pop("A-03", None)
    check("A-03", bbox=bbox(comp), n_ties=len(ties), n_dowels=len(dowels), a_block_interference_mm3=interference, seams=seams, worst=worst, passed=passed,
          control_overlap_when_one_block_is_pushed_0p5mm_into_its_neighbour_mm3=control, raw_unrounded={k: (f"{float(x):.3e}" if not isinstance(x, str) else x) for k, x in raw.items()},
          tie_through_block_mm3_max=max(tie_hits), dowel_through_block_mm3_max=max(dowel_hits), fastener_to_fastener_mm3_max=max(fast_hits),
          wedge_angles_about_vertex_line_deg=wedge, block_interior_angles=[round(f["interior_angle"], 3) for f in frames], block_masses_kg=m_blocks,
          edge_lengths_at_vertex=[round(x, 3) for x in edge_lengths], polyhedron_diameter=round(2 * float(np.linalg.norm(V, axis=1).max()), 1))
    print("   A-03 passed:", passed)
    return parts, colors

def BRepAdaptorAxis(cyl_solid):
    """axis (point, direction) of a plain cylinder solid"""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    for f in cyl_solid.Faces():
        if f.geomType() == "CYLINDER":
            ax = BRepAdaptor_Surface(f.wrapped).Cylinder().Axis()
            d = cq.Vector(ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z())
            ends = [fc.Center() for fc in cyl_solid.Faces() if fc.geomType() == "PLANE"]
            p0 = min(ends, key=lambda p: p.dot(d))
            return p0, d

# ============================================================ P-06H / P-06P leaning frame members (9 Nov)
Z_RTV, R_RTV = 42.0, 3.0                       # RTV recess, as on the test-piece frame B (build_testpieces.py)
D_SEAM_HOLE = 8.4
FRAME_FL_W, FRAME_FL_T = v("frame", "flange_width"), v("frame", "flange_thickness")     # 50 x 10

def seam_bolt_positions():
    """16 bolts per seam, mm from the z 0 vertex along the edge: bays between the corner blocks (230) and the three 200-wide fittings (as sheets_flight_revF.py)"""
    pitch = v("seam_bolt", "pitch"); q = EDGE / 4
    pos = []
    for a, b in ((230, q - 100), (q + 100, 2 * q - 100), (2 * q + 100, 3 * q - 100), (3 * q + 100, EDGE - 230)):
        n = int((b - a - 30) // pitch) + 1
        f0 = (b - a - (n - 1) * pitch) / 2
        pos += [a + f0 + i * pitch for i in range(n)]
    return pos

def leaning_frame(theta):
    """built in the corner block's frame (vertex at the origin, edge along +x, panel interior +y, z depth), so it can be tested against the block"""
    V = cq.Vector
    g = CB.geometry(theta); m = g["mitre"]; t_ = math.tan(m)
    wh = FWEB / math.cos(m)                                 # web thickness in a section parallel to the panel
    yi = lambda z: z * t_ + wh                              # the web's inner face
    prof = [(0, 0), (yi(0) + FRAME_FL_W, 0), (yi(0) + FRAME_FL_W, FRAME_FL_T), (yi(FRAME_FL_T), FRAME_FL_T), (yi(FD - FRAME_FL_T), FD - FRAME_FL_T),
            (yi(FD) + FRAME_FL_W, FD - FRAME_FL_T), (yi(FD) + FRAME_FL_W, FD), (FD * t_, FD)]
    s = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon([V(-200, y, z) for y, z in prof], close=True)), V(EDGE + 400, 0, 0))
    # ends: the corner blocks' leg end planes, 230 mm from each vertex line and parallel to it (x = 230 + kc z at this end)
    kc = g["sigma"][0]
    keep = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon(
        [V(CB.LEG + kc * -50, -100, -50), V(EDGE - CB.LEG - kc * -50, -100, -50), V(EDGE - CB.LEG - kc * 250, -100, 250), V(CB.LEG + kc * 250, -100, 250)], close=True)), V(0, 500, 0))
    s = s.intersect(keep)
    v0 = s.Volume()
    # seam features in joint-face coordinates (X along the edge, Y = z' down the face, Z out of the face; metal at Z < 0), then moved onto the leaning face
    ex, tt, nu = CB.face_frame(g)
    loc = cq.Location(cq.Plane(origin=(0, 0, 0), xDir=ex, normal=tuple(-c for c in nu)))
    assert (loc.plane.yDir - V(*tt)).Length < 1e-12 if hasattr(loc, "plane") else True
    to_face = lambda shp: (shp.val() if hasattr(shp, "val") else shp).moved(loc)
    vols = {}
    cut = lambda sh, key: vols.__setitem__(key, vols.get(key, 0.0) + (s.Volume() - s.cut(sh).Volume()))
    blend_log = []
    for zc in (Z_G1, Z_G2):
        gl = box(EDGE + 400, GW, GD + 1, -200, zc - GW / 2, -GD)
        try:
            gl = gl.edges(cq.selectors.BoxSelector((-201, zc - GW / 2 - 0.5, -GD - 0.5), (EDGE + 201, zc + GW / 2 + 0.5, -GD + 0.5))).fillet(0.7)
        except Exception as e:
            blend_log.append(f"gland bottom R0.7 at z' {zc} skipped: {e}")
        sh = to_face(gl); cut(sh, "glands"); s = s.cut(sh)
    sh = to_face(cq.Workplane("YZ").center(Z_RTV, 0).circle(R_RTV).extrude(EDGE + 400).translate((-200, 0, 0))); cut(sh, "rtv_recess"); s = s.cut(sh)
    bolts = seam_bolt_positions()
    for x in bolts:
        sh = to_face(cyl_z(D_SEAM_HOLE, -FWEB - 2, 2, x, Z_BOLT)); cut(sh, "bolt_holes"); s = s.cut(sh)
    return s, g, dict(prof=prof, v0=v0, vols=vols, bolts=bolts, kc=kc, wh=wh, blend_log=blend_log)

def build_frames(which):
    for pid, th, kind, blk_id in (("P-06H", 120, "hexagon", "CB-01"), ("P-06P", 108, "pentagon", "CB-02")):
        if not which(pid):
            continue
        s, g, info = leaning_frame(th)
        for mm in info["blend_log"]:
            FAILED_BLENDS.append(f"{pid}: {mm}")
        m = g["mitre"]; lean = g["mitre_deg"]
        # does the end meet the corner block?  same frame: the block at the origin vertex
        blk, _, _ = CB.corner_block(th)
        gap = _dist(s, blk.val()); common = float(s.intersect(blk.val()).Volume())
        # both the member's end face and the block's leg end face must lie on the plane x - kc z = 230 (through the leg end, parallel to the vertex line)
        nrm = cq.Vector(1, 0, -info["kc"]).normalized()
        on_plane = lambda shp: [max(abs((cq.Vector(*vx.toTuple()) - cq.Vector(CB.LEG, 0, 0)).dot(nrm)) for vx in f.Vertices())
                                for f in shp.Faces() if f.geomType() == "PLANE" and abs(abs(f.normalAt().dot(nrm)) - 1) < 1e-9 and f.Center().x < 600]
        dev_frame, dev_block = on_plane(s), on_plane(blk.val())
        assert len(dev_frame) == 1 and len(dev_block) == 1, (dev_frame, dev_block)
        coplanar = dev_frame[0] + dev_block[0]
        len0 = EDGE - 2 * CB.LEG; len180 = len0 - 2 * info["kc"] * FD
        jf_len = FD / math.cos(m)
        bolts = info["bolts"]; end_at_bolt = CB.LEG + g["q"] * Z_BOLT
        exp_bolts = len(bolts) * math.pi * (D_SEAM_HOLE / 2) ** 2 * FWEB
        # to the P-06 convention: along Y, centred on the edge's mid-point, joint face through x 20 at z 0, panel side toward -x
        out = cq.Workplane("XY").newObject([s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90).translate(cq.Vector(FWEB, -EDGE / 2, 0))])
        notes = (f"PROPOSAL of 9 Nov. The edge frame member of a {kind} panel with its web LEANING {lean:.3f} deg, so that the web's joint face lies on the seam's radial plane (through the "
                 f"shell edge and the sphere centre). DEPTH CONVENTION: the 180 mm is panel depth z, outer face z 0 to the pane seat plane z 180, both cut flat to the panel planes; the "
                 f"joint face is therefore {jf_len:.1f} mm long down the lean (z'). Web {FWEB:.0f} thick measured normal to the joint face ({info['wh']:.1f} in a section parallel to the "
                 f"panel); outer flange {FRAME_FL_W:.0f} x {FRAME_FL_T:.0f} at z 0-10 and seat lip {FRAME_FL_W:.0f} x {FRAME_FL_T:.0f} at z 170-180, both parallel to the panel planes on the "
                 f"panel side, their 50 mm measured from the web's inner face at z 0 and at z 180. SEAM FEATURES are placed along the joint face by z' and cut normal to it: two butyl "
                 f"glands {GW} x {GD} (bottom R0.7) at z' {Z_G1:.0f} and {Z_G2:.0f}, the RTV recess (R{R_RTV:.0f} half-round) at z' {Z_RTV:.0f}, and {len(bolts)} seam bolt holes {D_SEAM_HOLE} mm at z' "
                 f"{Z_BOLT:.0f} through the web, 75 pitch in bays of 3, 5, 5, 3, the first {bolts[0]} mm from the vertex (positions from the vertex: "
                 f"{', '.join(f'{b:g}' for b in bolts[:8])} and mirrored). This is the gland-carrying member (frame B of the test pieces); its mate across the seam is the same member with a flat "
                 f"joint face. ENDS: cut on the corner block {blk_id}'s leg end plane, 230 mm from the vertex line and parallel to it, so the member is {len0:.0f} mm long at z 0 and "
                 f"{len180:.1f} mm at z 180 (each end leans {math.degrees(math.atan(info['kc'])):.2f} deg from square in the panel's side view, {math.degrees(math.atan(g['q'])):.2f} deg in the "
                 f"joint face). Checked against the {blk_id} solid in the same frame: gap {gap:.4f} mm, common volume {common:.4f} mm3, end face coplanar with the block's leg end within "
                 f"{coplanar:.6f} mm. The first bolt hole's edge is {bolts[0] - end_at_bolt - D_SEAM_HOLE / 2:.1f} mm from the end. "
                 f"NOT IN THIS SOLID: the three hardpoint blocks (web thickened to 50 over 240 mm at {EDGE / 4:g}, {EDGE / 2:g}, {3 * EDGE / 4:g}; HP-01M), the gland loop corners at the corner "
                 f"blocks (the glands simply run out at the ends; R16 minimum loop, Q92), the leak port, inside radii at the web (R6 on the test pieces), and how the member is fixed to the "
                 f"corner block. " + ("The parameter file carries a 56.6 mm seat lip for the hexagon (OPEN-17, proposal); 50 is drawn here as briefed. " if th == 120 else "") +
                 f"The straight P-06 stays in the library as a schematic.")
        dims = dict(depth="180 (panel z 0 to 180)", joint_face_length_along_lean=round(jf_len, 1), web_lean=f"{lean:.3f} deg", web_t=f"{FWEB:.0f} normal to the joint face",
                    flange=f"{FRAME_FL_W:.0f} x {FRAME_FL_T:.0f} at z 0-10", lip=f"{FRAME_FL_W:.0f} x {FRAME_FL_T:.0f} at z 170-180", glands=f"2 x {GW} x {GD} at z' {Z_G1:.0f} and {Z_G2:.0f}",
                    rtv_recess=f"R{R_RTV:.0f} at z' {Z_RTV:.0f}", seam_bolts=f"{len(bolts)} x {D_SEAM_HOLE} at z' {Z_BOLT:.0f}, 75 pitch, bays 3-5-5-3, first {bolts[0]} from the vertex",
                    length_at_z0=len0, length_at_z180=round(len180, 1), ends=f"on the {blk_id} leg end planes, parallel to the vertex line")
        register(pid, f"Frame member, {kind}, web leaning {lean:.3f} deg, 180 deep", out, "6061-T6", notes, dims, rev=REV9,
                 source="P-06 (Rev E sizing, 24 Oct), RF-05 (5 Nov), true polyhedron geometry (9 Nov)")
        CHECKS.pop(pid, None)
        check(pid, bbox=bbox(out), valid_solid=s.isValid(), web_lean_deg=round(lean, 4), joint_face_length=round(jf_len, 2), length_at_z0=len0, length_at_z180=round(len180, 2),
              n_bolts=len(bolts), bolt_positions_from_vertex=bolts, bolt_hole_volume=round(info["vols"]["bolt_holes"]), bolt_hole_volume_expected=round(exp_bolts),
              gland_volume=round(info["vols"]["glands"]), rtv_recess_volume=round(info["vols"]["rtv_recess"]),
              end_to_corner_block_gap_mm=round(gap, 6), end_to_corner_block_common_volume_mm3=round(common, 6), end_face_coplanar_with_block_leg_end_mm=coplanar,
              first_bolt_hole_edge_to_end=round(bolts[0] - end_at_bolt - D_SEAM_HOLE / 2, 2), blends_failed=info["blend_log"])

# ============================================================ HP-02A / HP-02B / HP-03 hardpoint fitting from the C3 model, A-05 (9 Nov)
# Joint frame J of a hexagon-to-hexagon seam at a hardpoint: X along the seam (0 at the hardpoint centre), Y normal to the joint plane
# (panel A at +Y, panel B at -Y), Z = z' down the leaning joint face from the shell edge.  C3 gives the fitting in (x seam, y normal, z depth).
C3 = dict(half_w=100.0, pin_d=40.0, pin_x=(-60.0, 0.0, 60.0), pin_y=-40.0, pin_len=95.0, pin_z=(45.0, 140.0),
          baseA_y=(2.0, 50.0), base_z=(10.0, 140.0), lug_z=(73.0, 112.0), lug_tip_y=-100.0, tip_chamfer=8.0, root_R=10.0,
          baseB_y=(-132.0, -102.0), cheek_z=((50.0, 72.5), (112.5, 135.0)), cheek_top_y=0.0, slot_floor_y=-102.0, relief_y=8.0, R_small=4.0)
FIT_MID_MOVED, FIT_MID_AS_DRAWN = 76.0, 140.0
DZ_MOVED = FIT_MID_MOVED - sum(C3["lug_z"]) / 2            # -16.5: shift of the whole C3 depth stack
# The C3 model has no frame webs: its bodies meet at y 0..2.  Here each body sits on the INNER face of its own 20 mm web, so
# body A moves +18 (base face from y 2 to the web's inner face y 20) and everything on side B moves -20 (cheek tops from y 0 to y -20).
DY_A = FWEB - C3["baseA_y"][0]            # +18
DY_B = -FWEB - C3["cheek_top_y"]          # -20
SLOT_CLR, SLOT_R, WEB_RELIEF = 1.0, 5.0, 11.0
BOLT_X_HP = 137.5
A05_LEN = 360.0

def _wp(s):
    return cq.Workplane("XY").newObject([s.val() if hasattr(s, "val") else s])

def _edges(s, pred):
    return [e for e in s.val().Edges() if pred(e)]

def _try(s, op, edges, size, what, log):
    try:
        if not edges:
            raise ValueError("no edges selected")
        return _wp(s.val().fillet(size, edges) if op == "fillet" else s.val().chamfer(size, None, edges))
    except Exception as e:
        log.append(f"{what} skipped: {e}")
        return s

def _par(e, axis):
    d = e.endPoint() - e.startPoint()
    return e.geomType() == "LINE" and d.Length > 1 and abs(abs(d.normalized().dot(cq.Vector(*axis))) - 1) < 1e-9

def fitting_bodies(dz, dy_a=DY_A, dy_b=DY_B, log=None):
    """HP-02A (lug), HP-02B (clevis) and the three pins in the joint frame J, C3 depth stack shifted by dz"""
    log = log if log is not None else []
    hw = C3["half_w"]; r = C3["pin_d"] / 2
    bz0, bz1 = C3["base_z"][0] + dz, C3["base_z"][1] + dz
    lz0, lz1 = C3["lug_z"][0] + dz, C3["lug_z"][1] + dz
    py = C3["pin_y"] + dy_b; tip = C3["lug_tip_y"] + dy_b
    ya0, ya1 = C3["baseA_y"][0] + dy_a, C3["baseA_y"][1] + dy_a
    # ---- body A: base block and lug
    a = box(2 * hw, ya1 - ya0, bz1 - bz0, -hw, ya0, bz0).union(box(2 * hw, ya0 - tip, lz1 - lz0, -hw, tip, lz0))
    a = _try(a, "fillet", _edges(a, lambda e: _par(e, (1, 0, 0)) and abs(e.Center().y - ya0) < 1e-6 and min(abs(e.Center().z - lz0), abs(e.Center().z - lz1)) < 1e-6), C3["root_R"], "HP-02A lug root R10", log)
    a = _try(a, "chamfer", _edges(a, lambda e: _par(e, (1, 0, 0)) and abs(e.Center().y - tip) < 1e-6), C3["tip_chamfer"], "HP-02A tip chamfer 8 x 8", log)
    va0 = a.val().Volume()
    for x in C3["pin_x"]:
        a = a.cut(cyl_z(C3["pin_d"], lz0 - 1, lz1 + 1, x, py))
    bore_a = va0 - a.val().Volume()
    a = _try(a, "chamfer", _edges(a, lambda e: e.geomType() == "CIRCLE" and abs(e.radius() - r) < 1e-6), 1.0, "HP-02A bore chamfers 1 x 1", log)
    # ---- body B: base block and two cheeks
    yb0, yb1 = C3["baseB_y"][0] + dy_b, C3["baseB_y"][1] + dy_b; top = C3["cheek_top_y"] + dy_b; floor = C3["slot_floor_y"] + dy_b
    b = box(2 * hw, yb1 - yb0, bz1 - bz0, -hw, yb0, bz0)
    cz = [(z0 + dz, z1 + dz) for z0, z1 in C3["cheek_z"]]
    for z0, z1 in cz:
        b = b.union(box(2 * hw, top - floor, z1 - z0, -hw, floor, z0))
    on_floor = lambda e: _par(e, (1, 0, 0)) and abs(e.Center().y - floor) < 1e-6
    b = _try(b, "fillet", _edges(b, lambda e: on_floor(e) and min(abs(e.Center().z - cz[0][1]), abs(e.Center().z - cz[1][0])) < 1e-6), C3["root_R"], "HP-02B slot floor R10", log)
    b = _try(b, "fillet", _edges(b, lambda e: on_floor(e) and abs(e.Center().z - cz[0][0]) < 1e-6), C3["root_R"], "HP-02B outer root R10", log)
    b = _try(b, "fillet", _edges(b, lambda e: on_floor(e) and abs(e.Center().z - cz[1][1]) < 1e-6), C3["R_small"], "HP-02B outer root R4", log)
    b = _try(b, "chamfer", _edges(b, lambda e: _par(e, (1, 0, 0)) and abs(e.Center().y - top) < 1e-6 and min(abs(e.Center().z - cz[0][1]), abs(e.Center().z - cz[1][0])) < 1e-6), C3["relief_y"], "HP-02B cheek top relief 8 x 8", log)
    vb0 = b.val().Volume()
    for x in C3["pin_x"]:
        b = b.cut(cyl_z(C3["pin_d"], cz[0][0] - 1, cz[1][1] + 1, x, py))
    bore_b = vb0 - b.val().Volume()
    b = _try(b, "chamfer", _edges(b, lambda e: e.geomType() == "CIRCLE" and abs(e.radius() - r) < 1e-6), 1.0, "HP-02B bore chamfers 1 x 1", log)
    pz0, pz1 = C3["pin_z"][0] + dz, C3["pin_z"][1] + dz
    pins = [cyl_z(C3["pin_d"], pz0, pz1, x, py) for x in C3["pin_x"]]
    info = dict(base_z=(bz0, bz1), lug_z=(lz0, lz1), cheek_z=cz, pin_z=(pz0, pz1), pin_y=py, lug_tip_y=tip, baseA_y=(ya0, ya1), baseB_y=(yb0, yb1), cheek_y=(floor, top),
                bore_volume_A=bore_a, bore_volume_B=bore_b)
    return a, b, pins, info

def hp_frames(length=A05_LEN, slot=True):
    """two short lengths of the leaning hexagon frame (P-06H section) in the joint frame J, each as web / flange / lip, with the seam features"""
    V = cq.Vector
    g = CB.geometry(120); m = g["mitre"]; t_ = math.tan(m); lean = g["mitre_deg"]
    wh = FWEB / math.cos(m); yi = lambda z: z * t_ + wh
    polys = dict(web=[(0, 0), (wh, 0), (yi(FD), FD), (FD * t_, FD)],
                 flange=[(wh, 0), (wh + FRAME_FL_W, 0), (wh + FRAME_FL_W, FRAME_FL_T), (yi(FRAME_FL_T), FRAME_FL_T)],
                 lip=[(yi(FD - FRAME_FL_T), FD - FRAME_FL_T), (yi(FD) + FRAME_FL_W, FD - FRAME_FL_T), (yi(FD) + FRAME_FL_W, FD), (yi(FD), FD)])
    A = {}
    for k, poly in polys.items():
        s = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon([V(-length / 2, y, z) for y, z in poly], close=True)), V(length, 0, 0))
        A[k] = s.rotate(V(0, 0, 0), V(1, 0, 0), lean)             # panel frame -> joint frame: the joint face turns onto Y = 0
    bb = A["web"].BoundingBox(); assert abs(bb.ymin) < 1e-6 and abs(bb.ymax - FWEB) < 1e-6 and abs(bb.zmax - FD / math.cos(m) - FWEB * t_) < 1e-6, (bb.ymin, bb.ymax, bb.zmax)
    B = {k: s.mirror("XZ") for k, s in A.items()}
    cuts_both, cuts_A, cuts_B = [], [], []
    for x in (-BOLT_X_HP, BOLT_X_HP):
        cuts_both.append(cyl_y(D_SEAM_HOLE, -FWEB - 2, FWEB + 2, x, Z_BOLT).val())
    for zc in (Z_G1, Z_G2):
        cuts_B.append(box(length + 2, GD + 1, GW, -length / 2 - 1, -GD, zc - GW / 2).val())
    cuts_B.append(cq.Workplane("YZ").center(0, Z_RTV).circle(R_RTV).extrude(length + 2).translate((-length / 2 - 1, 0, 0)).val())
    sl = None
    if slot:
        lz0, lz1 = C3["lug_z"][0] + DZ_MOVED - SLOT_CLR, C3["lug_z"][1] + DZ_MOVED + SLOT_CLR
        hw = C3["half_w"] + SLOT_CLR
        sb = box(2 * hw, 2 * FWEB + 4, lz1 - lz0, -hw, -FWEB - 2, lz0)
        sb = _wp(sb.val().fillet(SLOT_R, [e for e in sb.val().Edges() if _par(e, (0, 1, 0))]))
        cuts_both.append(sb.val())
        # relief on web A's inner face along the slot's two long edges, so the lug's R10 root fillet clears the web
        for zc, sgn in ((lz0, -1), (lz1, 1)):
            tri = [V(-hw, FWEB + 0.5, zc - sgn * 0.5), V(-hw, FWEB + 0.5, zc + sgn * WEB_RELIEF), V(-hw, FWEB - WEB_RELIEF, zc - sgn * 0.5)]
            cuts_A.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon(tri, close=True)), V(2 * hw, 0, 0)))
        sl = dict(x=(-hw, hw), z=(lz0, lz1))
    for c in cuts_both + cuts_A:
        A["web"] = A["web"].cut(c)
    for c in cuts_both + cuts_B:
        B["web"] = B["web"].cut(c)
    return A, B, g, sl

def secondary_rib_stubs(g, cut_back=72.0, length=320.0):
    """the two secondary ribs (I 180 x 60 x 10, web 5) that land on each frame at a hardpoint node, in J, for panel A and panel B"""
    V = cq.Vector; out = {"A": [], "B": []}
    for ang in (60.0, 120.0):
        rib = L.I_section(L.D2, L.BF2, L.TF2, L.TW2).extrude(length).translate((0, length / 2, 0)).val()       # along Y, centred
        rib = rib.translate(V(0, cut_back + length / 2, 0)).rotate(V(0, 0, 0), V(0, 0, 1), ang - 90.0)           # from the node on the edge line, in the panel frame
        ribJ = rib.rotate(V(0, 0, 0), V(1, 0, 0), g["mitre_deg"])
        out["A"].append(ribJ); out["B"].append(ribJ.mirror("XZ"))
    return out

def _common(a, b):
    a = a.val() if hasattr(a, "val") else a; b = b.val() if hasattr(b, "val") else b
    try:
        return round(float(a.intersect(b).Volume()), 1)
    except Exception as e:
        return f"boolean failed: {e}"

def _zmax_panel(shape, m, side):
    """largest panel depth z reached by a shape given in J (side +1 panel A, -1 panel B)"""
    return max(-side * math.sin(m) * vx.Y + math.cos(m) * vx.Z for vx in (shape.val() if hasattr(shape, "val") else shape).Vertices() if side * vx.Y >= FWEB - 1e-6)

def fitting_clash_report(dz, A, B, g, with_ribs=True):
    m = g["mitre"]; log = []
    a, b, pins, info = fitting_bodies(dz, log=log)
    ribs = secondary_rib_stubs(g) if with_ribs else {"A": [], "B": []}
    rep = {}
    for name, body, fr, side in (("HP-02A", a, A, "A"), ("HP-02B", b, B, "B"), ("pins", _wp(cq.Compound.makeCompound([p.val() for p in pins])), B, "B")):
        rep[name] = {f"common_volume_with_frame_{side}_{k}_mm3": _common(body, fr[k]) for k in ("web", "flange", "lip")}
        if with_ribs:
            rep[name][f"common_volume_with_the_two_secondary_ribs_of_panel_{side}_mm3"] = sum(_common(body, r) for r in ribs[side])
        rep[name]["largest_panel_depth_z_reached"] = round(_zmax_panel(body, m, 1 if side == "A" else -1), 1)
    rep["lug_with_frame_B_mm3"] = sum(_common(a, B[k]) for k in ("web", "flange", "lip"))
    rep["HP-02A_with_HP-02B_mm3"] = _common(a, b)
    return rep, (a, b, pins, info, log)

def build_hardpoint_fitting(which):
    ids = ("HP-02A", "HP-02B", "HP-03", "A-05")
    if not any(which(i) for i in ids):
        return
    for old in ("HP-02",):                       # the 8 Nov schematic fitting half is superseded
        PARTS.pop(old, None); CHECKS.pop(old, None)
        for f in [f"step/{old}.step", f"stl/{old}.stl", f"glb/{old}.glb"] + [f"svg/{old}_{vw}.svg" for vw in ("front", "top", "side", "iso")]:
            if os.path.exists(f"{OUT}/{f}"):
                os.remove(f"{OUT}/{f}")
    A, B, g, sl = hp_frames()
    m = g["mitre"]; sm, cm = math.sin(m), math.cos(m)
    rep, (a, b, pins, info, log) = fitting_clash_report(DZ_MOVED, A, B, g)
    for mm in log:
        FAILED_BLENDS.append(f"HP-02: {mm}")
    # the as-drawn position (lug mid-plane z' 140), as a check only
    dz_ad = FIT_MID_AS_DRAWN - sum(C3["lug_z"]) / 2
    A0, B0, _, _ = hp_frames(slot=False)
    rep_ad, (a_ad, b_ad, pins_ad, info_ad, _) = fitting_clash_report(dz_ad, A0, B0, g, with_ribs=False)
    rep_ad.pop("lug_with_frame_B_mm3", None)                  # no slot is cut for this check, so the lug-through-web volumes mean nothing
    for k in rep_ad:
        if isinstance(rep_ad[k], dict):
            rep_ad[k] = {kk: vv for kk, vv in rep_ad[k].items() if "_web_" not in kk}
    as_drawn = dict(lug_mid_plane_zp=FIT_MID_AS_DRAWN, lug_zp=list(info_ad["lug_z"]), cheeks_zp=[list(c) for c in info_ad["cheek_z"]], pins_zp=list(info_ad["pin_z"]), base_blocks_zp=list(info_ad["base_z"]),
                    straight_convention_z_equals_zp=dict(cheeks_beyond_180=round(info_ad["cheek_z"][1][1] - FD, 1), pins_beyond_180=round(info_ad["pin_z"][1] - FD, 1), base_blocks_beyond_180=round(info_ad["base_z"][1] - FD, 1),
                                                         cheeks_into_the_lip_zone_170_180=round(info_ad["cheek_z"][1][1] - (FD - FRAME_FL_T), 1), pins_into_the_lip_zone=round(info_ad["pin_z"][1] - (FD - FRAME_FL_T), 1),
                                                         base_blocks_into_the_lip_zone=round(info_ad["base_z"][1] - (FD - FRAME_FL_T), 1)),
                    leaning_hexagon_frame=rep_ad, joint_face_length=round(FD / cm, 1))
    # ---- slot clearances
    slot_chk = dict(slot_x=list(sl["x"]), slot_zp=list(sl["z"]), corner_radius=SLOT_R, clearance_all_round=SLOT_CLR,
                    to_rtv_recess_edge=round(sl["z"][0] - (Z_RTV + R_RTV), 2), to_inner_gland_edge=round(sl["z"][0] - (Z_G2 + GW / 2), 2),
                    to_plain_bolt_hole_at_137p5=round(BOLT_X_HP - D_SEAM_HOLE / 2 - sl["x"][1], 2),
                    to_flight_bay_bolt_holes_at_131p25_and_141p25=[round(f - D_SEAM_HOLE / 2 - sl["x"][1], 2) for f in FLIGHT_BOLTS_FROM_HP],
                    bolt_row_zp_58_is_inside_the_slot_depth_range=sl["z"][0] < Z_BOLT < sl["z"][1],
                    web_left_between_slot_and_joint_face_outer_end=round(sl["z"][0], 1), web_left_between_slot_and_cabin_end_of_joint_face=round(FD / cm - sl["z"][1], 1),
                    lug_square_corner_into_R5_slot_corner_mm=round((SLOT_R - SLOT_CLR) * math.sqrt(2) - SLOT_R, 2), largest_slot_corner_radius_that_clears_a_square_lug=round(SLOT_CLR * math.sqrt(2) / (math.sqrt(2) - 1), 2),
                    lug_with_web_A_mm3=rep["HP-02A"]["common_volume_with_frame_A_web_mm3"], lug_with_web_B_mm3=rep["lug_with_frame_B_mm3"])
    # ---- reach against the 50 x 10 flange and lip widths (panel-interior direction, measured in each panel's own plane)
    wh = FWEB / cm
    reach = lambda body, side: max(side * cm * vx.Y + sm * vx.Z for vx in body.val().Vertices())
    widths = dict(flange_tip_panel_y=round(wh + FRAME_FL_W, 1), lip_tip_panel_y=round(FD * math.tan(m) + wh + FRAME_FL_W, 1),
                  HP_02A_reach_panel_y=round(reach(a, 1), 1), HP_02B_reach_panel_y=round(reach(b, -1), 1), pins_reach_panel_y=round(max(reach(p, -1) for p in pins) + 0.0, 1))
    # ---- can the pins go in?  95 mm along z', from the cabin side or from the space side
    py = info["pin_y"]; r = C3["pin_d"] / 2; plen = C3["pin_len"]
    drive_cabin = [cyl_z(C3["pin_d"], info["pin_z"][1], info["pin_z"][1] + plen, x, py) for x in C3["pin_x"]]
    drive_space = [cyl_z(C3["pin_d"], info["pin_z"][0] - plen, info["pin_z"][0], x, py) for x in C3["pin_x"]]
    ya = abs(py) - r                                                     # the pin's edge nearest the web
    lip_first = ((FD - FRAME_FL_T) + ya * sm) / cm                       # z' where that edge meets the lip's upper face (panel z 170)
    lip_tip_normal = (FD * math.tan(m) + wh + FRAME_FL_W) * cm - FD * sm # normal distance of the lip's tip from the joint plane
    insertion = dict(pin_length=plen, pin_zp=list(info["pin_z"]), pin_line_from_joint_plane=abs(py),
                     cabin_side=dict(travel_needed=plen, free_travel_before_the_seat_lip=round(lip_first - info["pin_z"][1], 1), short_by=round(plen - (lip_first - info["pin_z"][1]), 1),
                                     common_volume_of_the_drive_path_with_frame_B_lip_mm3=sum(_common(d, B["lip"]) for d in drive_cabin),
                                     lip_reaches_normal_distance=round(lip_tip_normal, 1), pane_seat_plane="z 180: the pane and its seal lie on the lip, across the drive path"),
                     space_side=dict(common_volume_of_the_drive_path_with_frame_B_flange_mm3=sum(_common(d, B["flange"]) for d in drive_space),
                                     pin_as_installed_with_flange_mm3=rep["pins"]["common_volume_with_frame_B_flange_mm3"]),
                     possible=False)
    # ---- what C3's own y positions would do against the 20 mm webs (no shift): why the bodies were moved
    a_v, b_v, pins_v, info_v = fitting_bodies(DZ_MOVED, dy_a=0.0, dy_b=0.0)[:4]
    verbatim = dict(base_A_with_web_A_mm3=_common(a_v, A0["web"]), cheeks_and_base_B_with_web_B_mm3=_common(b_v, B0["web"]),
                    pin_to_web_B_inner_face=round(abs(C3["pin_y"]) - r - FWEB, 2), note="C3 y positions kept as modelled: the bodies overlap the two 20 mm webs and the pins touch web B")
    # ---- parts
    ti = RHO["Ti-6Al-4V"]
    mA, mB, mP = a.val().Volume() * ti, b.val().Volume() * ti, pins[0].val().Volume() * RHO["A286"]
    total = mA + mB + 3 * mP
    ch = lambda k: rep[k]
    placement = (f"PLACEMENT (moved position): the C3 depth stack is shifted {DZ_MOVED:+.1f} so the lug's mid-plane is at z' {FIT_MID_MOVED:.0f} on the joint face: lug z' {info['lug_z'][0]} to {info['lug_z'][1]}, "
                 f"cheeks {info['cheek_z'][0][0]} to {info['cheek_z'][0][1]} and {info['cheek_z'][1][0]} to {info['cheek_z'][1][1]}, pins {info['pin_z'][0]} to {info['pin_z'][1]}, base blocks "
                 f"{info['base_z'][0]} to {info['base_z'][1]}. DEPARTURE FROM C3 in the pull direction: C3 has no frame webs (its bodies meet at y 0 to 2). Kept at C3's y, base A would overlap web A "
                 f"({verbatim['base_A_with_web_A_mm3']:.0f} mm3), the cheeks would overlap web B ({verbatim['cheeks_and_base_B_with_web_B_mm3']:.0f} mm3) and the pins would touch web B. So each body is seated on the inner "
                 f"face of its own 20 mm web: body A's base face moved from y 2 to y 20, everything on side B moved 20 mm further in (cheek tops y -20, pin line y {info['pin_y']:.0f}, lug tip y {info['lug_tip_y']:.0f}, "
                 f"slot floor y {info['cheek_y'][0]:.0f}, base B y {info['baseB_y'][0]:.0f} to {info['baseB_y'][1]:.0f}). The lug is therefore {DY_A - DY_B:.0f} mm longer than in C3 (140 from base face to tip, not 102) and the pin "
                 f"line is 60 mm from the joint plane, not 40; every other dimension is C3's. The 2.876 million N/mm of C3 does not apply to this longer lug: to rerun. ")
    clash = (f"CLASHES FOUND with the leaning hexagon frame (P-06H section, common volumes in mm3): HP-02A with frame A flange {ch('HP-02A')['common_volume_with_frame_A_flange_mm3']}, lip "
             f"{ch('HP-02A')['common_volume_with_frame_A_lip_mm3']}, web {ch('HP-02A')['common_volume_with_frame_A_web_mm3']} (only the lug's four corners in the slot's R5 corners); HP-02B with frame B flange {ch('HP-02B')['common_volume_with_frame_B_flange_mm3']}, lip "
             f"{ch('HP-02B')['common_volume_with_frame_B_lip_mm3']}, web {ch('HP-02B')['common_volume_with_frame_B_web_mm3']}; pins with frame B flange {ch('pins')['common_volume_with_frame_B_flange_mm3']}, lip "
             f"{ch('pins')['common_volume_with_frame_B_lip_mm3']}; with the two secondary ribs that land on the hardpoint node (I 180 x 60, cut back 72): HP-02A "
             f"{ch('HP-02A')['common_volume_with_the_two_secondary_ribs_of_panel_A_mm3']}, HP-02B {ch('HP-02B')['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']}, pins "
             f"{ch('pins')['common_volume_with_the_two_secondary_ribs_of_panel_B_mm3']}. The base blocks start at z' {info['base_z'][0]}, above the shell edge, and run under the outer flange (z 0-10). ")
    notes_A = (f"PROPOSAL of 9 Nov, from the C3 finite element model (TP3, the run that gave 2.876 million N/mm); replaces the schematic fitting half HP-02 of 8 Nov. Body A, the LUG, Ti-6Al-4V, on panel A: base "
               f"block 200 wide x 48 x 130 deep, and a lug the full 200 width, 39 thick, reaching through the slot in both frame webs across the joint plane to its tip; tip chamfer 8 x 8 on both faces, root "
               f"fillets R10 on both faces, three 40 mm bores with 1 x 1 chamfers, 60 from bore centre to the tip and 40 to the side faces. The pins run ALONG THE DEPTH (z'), in double shear between this lug "
               f"and the two cheeks of HP-02B. Drawn in the joint frame: X along the seam, Y normal to the joint plane (panel A at +Y), Z = z' down the joint face. " + placement + clash +
               f"How the base block fastens to the frame is NOT in the C3 model: it is drawn seated on the web's inner face and the fastening is OPEN. See A-05.")
    notes_B = (f"PROPOSAL of 9 Nov, from the C3 model; replaces the schematic fitting half HP-02 of 8 Nov. Body B, the CLEVIS, Ti-6Al-4V, on panel B: base block 200 wide x 30 x 130 deep and two cheeks the full "
               f"width, each 22.5 thick, 102 tall, with a 40 mm slot between them (0.5 mm each side of the 39 lug); slot floor with R10 fillets, outer root R10 on one side and R4 on the side where only 5 mm "
               f"of base remains, cheek top inner edges relieved 8 x 8 (in C3 this cleared the lug's root fillet; with the webs between, the root is now 40 mm away and the relief is not needed), three 40 mm "
               f"bores with 1 x 1 chamfers. " + placement + clash + f"Fastening of the base block to the frame: OPEN, not in C3. See A-05.")
    ins = insertion["cabin_side"]
    notes_P = (f"PROPOSAL of 9 Nov, from the C3 model; replaces the 160 mm pin of 8 Nov. Hardpoint pin 40.0 x 95, A286, three per hardpoint at X -60, 0, +60, axes along the depth (z'), zero clearance in C3, in double "
               f"shear between the lug (39) and the two cheeks (22.5 each); drawn plain, without chamfers or retention. In the moved position it lies at z' {info['pin_z'][0]} to {info['pin_z'][1]}, "
               f"{abs(info['pin_y']):.0f} mm from the joint plane on panel B's side. CAN IT BE INSERTED? Not as drawn. From the cabin side it needs 95 mm of travel below z' {info['pin_z'][1]}; the seat lip of frame B "
               f"is met after {ins['free_travel_before_the_seat_lip']} mm ({ins['short_by']} mm short), and the pane lies on that lip. From the space side the outer flange is in the way, and the installed pin itself "
               f"overlaps the flange ({insertion['space_side']['pin_as_installed_with_flange_mm3']} mm3). A notch in the lip or the flange over the 160 mm of the three pins, or pins put in before the panel is glazed "
               f"through a notched lip, is needed: OPEN.")
    register("HP-02A", "Hardpoint fitting body A, lug, Ti-6Al-4V (TP3, from the C3 model)", a, "Ti-6Al-4V", notes_A,
             dict(base_block="200 x 48 x 130 deep", lug="200 wide x 39 thick, 140 from base face to tip (102 in C3)", tip_chamfer="8 x 8, both faces", root_fillet="R10, both faces",
                  bores="3 x 40 at 60 pitch, 1 x 1 chamfers, 60 to the tip, 40 to the sides", lug_zp=f"{info['lug_z'][0]} to {info['lug_z'][1]} (mid-plane z' 76)", base_zp=f"{info['base_z'][0]} to {info['base_z'][1]}"),
             rev=REV9, source="Ansys C3 (TP3), geometry as measured from the model; HP1M (7 Nov)")
    register("HP-02B", "Hardpoint fitting body B, clevis, Ti-6Al-4V (TP3, from the C3 model)", b, "Ti-6Al-4V", notes_B,
             dict(base_block="200 x 30 x 130 deep", cheeks="2 x 200 wide x 22.5 thick x 102 tall, 40 slot between", slot_floor="R10", outer_roots="R10 and R4", cheek_top_relief="8 x 8",
                  bores="3 x 40 at 60 pitch, 1 x 1 chamfers", cheeks_zp=f"{info['cheek_z'][0][0]} to {info['cheek_z'][0][1]} and {info['cheek_z'][1][0]} to {info['cheek_z'][1][1]}", base_zp=f"{info['base_z'][0]} to {info['base_z'][1]}"),
             rev=REV9, source="Ansys C3 (TP3), geometry as measured from the model; HP1M (7 Nov)")
    register("HP-03", "Hardpoint pin, 40 x 95, A286, along the depth, double shear (from the C3 model)", pins[1], "A286", notes_P,
             dict(diameter=40.0, length=95.0, quantity_per_hardpoint=3, axis="along the depth z'", shear="double: lug 39 between two 22.5 cheeks", pin_zp=f"{info['pin_z'][0]} to {info['pin_z'][1]}"),
             rev=REV9, source="Ansys C3 (TP3)")
    for pid, body in (("HP-02A", a), ("HP-02B", b), ("HP-03", pins[1])):
        CHECKS.pop(pid, None)
    check("HP-02A", bbox=bbox(a), valid_solid=a.val().isValid(), bore_volume=round(info["bore_volume_A"]), bore_volume_expected=round(3 * math.pi * 400 * 39), mass_kg=round(mA, 3), clashes=rep["HP-02A"], blends_failed=[x for x in log if "HP-02A" in x])
    check("HP-02B", bbox=bbox(b), valid_solid=b.val().isValid(), bore_volume=round(info["bore_volume_B"]), bore_volume_expected=round(3 * math.pi * 400 * 45), mass_kg=round(mB, 3), clashes=rep["HP-02B"], blends_failed=[x for x in log if "HP-02B" in x])
    check("HP-03", bbox=bbox(pins[1]), expected_envelope="40 x 40 x 95", mass_kg=round(mP, 3), clashes=rep["pins"], insertion=insertion)
    # ---- A-05
    frameA = _wp(A["web"].fuse(A["flange"]).fuse(A["lip"]).clean()); frameB = _wp(B["web"].fuse(B["flange"]).fuse(B["lip"]).clean())
    bolts = []
    for x in (-BOLT_X_HP, BOLT_X_HP):
        bolts.append(cyl_y(7.94, -FWEB - 8.0, FWEB, x, Z_BOLT).union(cyl_y(14.0, FWEB, FWEB + 5.0, x, Z_BOLT)).union(cyl_y(14.0, -FWEB - 7.0, -FWEB, x, Z_BOLT)))
    parts = [("frame_A_P-06H_flat_face", frameA), ("frame_B_P-06H_glands", frameB), ("HP-02A_lug", a), ("HP-02B_clevis", b)] + [(f"HP-03_pin_{i}", p) for i, p in enumerate(pins)] + [(f"seam_bolt_{i}", bb_) for i, bb_ in enumerate(bolts)]
    colors = [COL["al"], COL["al"], COL["ti"], COL["forging2"]] + [COL["steel"]] * 3 + [COL["brace"]] * 2
    name = "A-05_hardpoint_moved"
    comp = export_assembly(name, parts, colors, "A-05")
    masses = dict(HP_02A_kg=round(mA, 3), HP_02B_kg=round(mB, 3), pin_each_kg=round(mP, 3), hardpoint_2_bodies_3_pins_kg=round(total, 3),
                  frame_lengths_kg=round((frameA.val().Volume() + frameB.val().Volume()) * RHO["6061-T6"], 3))
    bolt_clash = sum(_common(bb_, x) for bb_ in bolts for x in (a, b))
    verdict = ("The base blocks replace the local block. The 8 Nov HP-01 / HP-01M block (web thickened to 50 over 240 mm, three 40 mm bores ACROSS the joint, six tap holes) belongs to the schematic "
               "fitting and no longer makes sense: in the C3 geometry nothing is bored through the frame, the pins run along the depth inside the fitting, and the frame's only feature at a hardpoint is the "
               "202 x 41 slot for the lug. What the web needs round that slot (a doubler or a thicker web, since the slot removes the web over 202 mm exactly on the bolt row) and how the two base blocks are "
               "fastened are open.")
    notes = (f"PROPOSAL of 9 Nov. The hardpoint in the MOVED position (lug mid-plane at z' {FIT_MID_MOVED:.0f}), from the C3 model's real fitting: two {A05_LEN:.0f} mm lengths of the leaning hexagon frame P-06H "
             f"(panel A with the flat joint face, panel B with the glands and RTV recess) on a hexagon-to-hexagon seam, drawn in the joint frame (X along the seam, Y normal to the joint plane, Z = z' down the "
             f"joint face, so the two panels' flanges and lips lean away at 20.905 deg); the slot for the lug through both webs, {sl['x'][1] * 2:.0f} x {sl['z'][1] - sl['z'][0]:.0f} at z' {sl['z'][0]} to {sl['z'][1]} "
             f"(1 mm clear of the lug all round, R5 corners, and an 11 x 11 relief on web A's inner face so the lug's R10 root fillet clears). The R5 corners and the 1 mm clearance do not go together with a "
             f"square-edged lug: each lug corner is {slot_chk['lug_square_corner_into_R5_slot_corner_mm']} mm into the slot's corner radius ({slot_chk['lug_with_web_A_mm3']} and {slot_chk['lug_with_web_B_mm3']} mm3 in the two webs); "
             f"R{slot_chk['largest_slot_corner_radius_that_clears_a_square_lug']} or less, or a 2 mm break on the lug's four long edges, clears. Drawn as specified. Also in the assembly: HP-02A (lug) on panel A, HP-02B (clevis) on panel B, three HP-03 "
             f"pins along the depth, and the two plain seam bolts at X +-{BOLT_X_HP} on the bolt row z' {Z_BOLT:.0f}. Both base blocks and the cheeks sit on the inner (panel-interior) side of the frame webs, "
             f"not in the joint face. " + placement +
             f"SLOT CLEARANCES: {slot_chk['to_rtv_recess_edge']} mm to the RTV recess (z' 42), {slot_chk['to_inner_gland_edge']} mm to the inner gland (z' 32), {slot_chk['to_plain_bolt_hole_at_137p5']} mm to the "
             f"plain bolt holes at +-137.5 ({slot_chk['to_flight_bay_bolt_holes_at_131p25_and_141p25'][0]} / {slot_chk['to_flight_bay_bolt_holes_at_131p25_and_141p25'][1]} mm to the flight bay bolts at 131.25 / 141.25). "
             f"The bolt row z' 58 lies inside the slot's depth range, so the seam has no clamp bolt and no web over the 202 mm of the slot; the seals above it (z' 18, 32, 42) keep {sl['z'][0]} mm of web. "
             + clash +
             f"WIDTH: the flange tip is {widths['flange_tip_panel_y']} mm and the lip tip {widths['lip_tip_panel_y']} mm into the panel from the edge line; HP-02A reaches {widths['HP_02A_reach_panel_y']} mm and HP-02B "
             f"{widths['HP_02B_reach_panel_y']} mm, so the clevis stands {widths['HP_02B_reach_panel_y'] - widths['lip_tip_panel_y']:.0f} mm beyond the lip into the first pane bay. "
             f"PINS: cannot be inserted as drawn: from the cabin side the seat lip is met after {ins['free_travel_before_the_seat_lip']} of the 95 mm ({ins['short_by']} mm short) and the pane lies on the lip; from the "
             f"space side the flange is in the way. "
             f"AS-DRAWN POSITION (lug mid-plane z' 140, check only, not drawn): cheeks to z' {info_ad['cheek_z'][1][1]}, pins and base blocks to z' {info_ad['pin_z'][1]}; taking z = z' (straight frame) that is "
             f"{as_drawn['straight_convention_z_equals_zp']['cheeks_beyond_180']} mm (cheeks) and {as_drawn['straight_convention_z_equals_zp']['pins_beyond_180']} mm (pins, base blocks) beyond the 180 frame depth. "
             f"OPEN: the fastening of the base blocks to the frame (not in C3), the web round the slot, the flange and lip cut-outs, the secondary rib ends at the node, pin insertion and retention, and a check that the slot, which lies on the cabin side "
             f"of the three seals (z' 18, 32, 42) and so joins cabin to cabin, leaves the seals enough web ({slot_chk['to_rtv_recess_edge']} mm below the RTV recess). "
             + verdict + f" Masses: HP-02A {mA:.3f} kg, HP-02B {mB:.3f} kg, pin {mP:.3f} kg each, the hardpoint (two bodies and three pins) {total:.3f} kg.")
    PARTS["A-05"] = dict(id="A-05", name="Hardpoint, moved position: two lengths of leaning hexagon frame, lug HP-02A, clevis HP-02B, three pins, two plain seam bolts",
                         material="6061-T6 + Ti-6Al-4V + A286", mass_kg=round(total + masses["frame_lengths_kg"], 3), notes=notes,
                         dims=dict(frame_lengths=f"2 x {A05_LEN:.0f} of P-06H", slot=f"{sl['x'][1] * 2:.0f} x {sl['z'][1] - sl['z'][0]:.0f} at z' {sl['z'][0]} to {sl['z'][1]}, R5", lug_mid_plane_zp=FIT_MID_MOVED,
                                   pins="3 x 40 x 95 along the depth", plain_bolts=f"2 at X +-{BOLT_X_HP}, z' {Z_BOLT:.0f}", slot_clearances=slot_chk, widths=widths),
                         rev=REV9, source="Ansys C3 (TP3), HP1M (7 Nov), P-06H (9 Nov)", files=name, bbox_mm=bbox(comp), masses=masses, assembly=True)
    CHECKS.pop("A-05", None)
    check("A-05", bbox=bbox(comp), slot=slot_chk, clashes_moved_position=rep, widths=widths, pin_insertion=insertion, as_drawn_position_lug_mid_plane_zp_140=as_drawn,
          c3_y_positions_kept_without_shift=verbatim, shift_applied=dict(depth_stack=DZ_MOVED, body_A_y=DY_A, side_B_y=DY_B, lug_longer_than_C3_by=DY_A - DY_B),
          seam_bolts_with_fitting_bodies_mm3=bolt_clash, masses=masses, local_block_verdict=verdict, blends_failed=log)
    print("   A-05 clashes:", json.dumps(rep, default=_plain))

# ============================================================ A-04 pentagon panel assembly (schematic)
TIE_Z_PENT_8NOV, DOWEL_Z_PENT_8NOV = (128.3, 364.4), 246.3
def rib_plain(Lseg):
    return L.I_section(L.D2, L.BF2, L.TF2, L.TW2).extrude(Lseg).translate((0, Lseg / 2, 0))

def along(shape, p, q, cut_p, cut_q):
    """place a y-extruded, y-centred member from point p to q (2D), shortened by cut_p at p and cut_q at q"""
    import numpy as np
    p = np.array(p, float); q = np.array(q, float); d = q - p; Lfull = np.linalg.norm(d); d /= Lfull
    Lseg = Lfull - cut_p - cut_q
    mid = p + d * (cut_p + Lseg / 2)
    ang = math.degrees(math.atan2(d[1], d[0])) - 90.0
    return shape(Lseg).rotate((0, 0, 0), (0, 0, 1), ang).translate((mid[0], mid[1], 0)), Lseg

def build_pentagon(which):
    if not which("A-04"):
        return
    import numpy as np
    parts, colors = [], []
    # frames: joint face (local x = 20) on the edge line, flanges inward
    frame_len = EDGE - 2 * CBS.LEG                      # 1790: the frames run between the corner blocks' leg ends
    frame = L.frame_member(frame_len)
    for k in range(5):
        a = np.array(PENT_V[k]); b = np.array(PENT_V[(k + 1) % 5]); mid = (a + b) / 2
        n_out = mid / np.linalg.norm(mid)
        psi = math.degrees(math.atan2(n_out[1], n_out[0]))
        pos = mid - n_out * L.FWEB
        parts.append((f"frame_{k}", frame.rotate((0, 0, 0), (0, 0, 1), psi).translate((pos[0], pos[1], 0)))); colors.append(COL["al"])
    # main ribs with cap angles, from r 215 (past the hub cheeks) to the block landing at R - 60
    r0, r1 = 215.0, R_PENT - 60.0
    rib_len = r1 - r0
    rib = L.main_rib(rib_len); capA = L.cap_angle(rib_len); capB = capA.mirror("YZ")
    for k in range(5):
        th = -54 + 72 * k
        d = np.array([math.cos(math.radians(th)), math.sin(math.radians(th))]); mid = d * (r0 + r1) / 2
        for label, shp, col in ((f"main_rib_{k}", rib, COL["al"]), (f"cap_angle_{k}a", capA, COL["al"]), (f"cap_angle_{k}b", capB, COL["al"])):
            parts.append((label, shp.rotate((0, 0, 0), (0, 0, 1), th - 90).translate((mid[0], mid[1], 0)))); colors.append(col)
    # hub: five-fork core between the two star plates
    a0 = -54.0
    parts.append(("hub_core", L.hub(5, a0).translate((0, 0, 51)))); colors.append(COL["forging"])
    parts.append(("hub_star_outer", L.hub_star_plate(5, a0).translate((0, 0, 25)))); colors.append(COL["forging"])
    parts.append(("hub_star_inner", L.hub_star_plate(5, a0).translate((0, 0, 350)))); colors.append(COL["forging"])
    # secondary ribs: k 4 lattice in each of the five triangles, interior segments only
    O = np.zeros(2); seg_lengths = []; n_sec = 0
    cut_for = lambda kind: {"node": 47.0, "rib": 55.0, "frame": 72.0}[kind]
    def kind(i, j):
        if i + j == 4: return "frame"
        if i == 0 or j == 0: return "rib"
        return "node"
    for k in range(5):
        A = np.array(PENT_V[k]); B = np.array(PENT_V[(k + 1) % 5])
        Pt = lambda i, j: O + (i / 4) * (A - O) + (j / 4) * (B - O)
        edges = set()
        for i in range(5):
            for j in range(5 - i):
                for (i2, j2) in ((i + 1, j), (i, j + 1)):
                    if i2 + j2 <= 4:
                        edges.add(((i, j), (i2, j2)))
                if i + 1 + j <= 4 and j + 1 <= 4 and i + (j + 1) <= 4:
                    edges.add(((i + 1, j), (i, j + 1)))
        for (p, q) in sorted(edges):
            on_boundary = ((p[1] == 0 and q[1] == 0) or (p[0] == 0 and q[0] == 0) or (p[0] + p[1] == 4 and q[0] + q[1] == 4))
            if on_boundary:
                continue
            shp, Lseg = along(rib_plain, Pt(*p), Pt(*q), cut_for(kind(*p)), cut_for(kind(*q)))
            parts.append((f"sec_rib_{k}_{p[0]}{p[1]}_{q[0]}{q[1]}", shp)); colors.append(COL["al"]); n_sec += 1; seg_lengths.append(round(Lseg, 1))
    # corner blocks
    blk, _, _ = CBS.corner_block_straight(108, TIE_Z_PENT_8NOV, DOWEL_Z_PENT_8NOV)     # the 8 Nov straight block: A-04 is schematic and was not redrawn
    for k in range(5):
        vk = np.array(PENT_V[k]); vn = np.array(PENT_V[(k + 1) % 5])
        ang = math.degrees(math.atan2(vn[1] - vk[1], vn[0] - vk[0]))
        parts.append((f"corner_block_{k}", blk.rotate((0, 0, 0), (0, 0, 1), ang).translate((vk[0], vk[1], 0)))); colors.append(COL["forging"])
    # closure plate, five triangles
    tri, _ = closure_triangle(0)
    for k in range(5):
        parts.append((f"closure_{k}", tri.rotate((0, 0, 0), (0, 0, 1), 72 * k))); colors.append(COL["plate"])
    name = "A-04_pentagon_panel"
    comp = export_assembly(name, parts, colors, "A-04")
    counts = dict(frames=5, main_ribs=5, cap_angles=10, hub=3, secondary_ribs=n_sec, corner_blocks=5, closure_triangles=5)
    mass = dict(frames=5 * frame.val().Volume() * RHO["6061-T6"], main_ribs=5 * (rib.val().Volume() + 2 * capA.val().Volume()) * RHO["6061-T6"],
                hub=(L.hub(5, a0).val().Volume() + 2 * L.hub_star_plate(5, a0).val().Volume()) * RHO["2219-T852"],
                secondary=sum(p[1].val().Volume() for p in parts if p[0].startswith("sec_rib")) * RHO["6061-T6"],
                blocks=5 * blk.val().Volume() * RHO["2219-T852"], closure=5 * tri.val().Volume() * RHO["6061-T6"])
    mass = {k: round(x, 1) for k, x in mass.items()}
    total = round(sum(mass.values()), 1)
    notes = (f"PROPOSAL, schematic. One of the 12 pentagons: five 180 mm frame members (P-06 section, straight, {frame_len:.0f} long between the corner blocks' leg ends; the real webs lean 16.472 deg), five 400 x 100 x 25 main ribs with "
             f"their cap angles from the hub to the corner block landings ({rib_len:.0f} mm, schematic ends), the hub (five-fork P-05 core and two five-arm P-05A star "
             f"plates), the {n_sec} secondary rib segments of the k 4 grid as plain I 180 x 60 x 10 sections (18 per triangle; segment lengths {min(seg_lengths)} to "
             f"{max(seg_lengths)}, cut back 47 mm at a node, 55 at a main rib, 72 at the frame; the node cores and star plates are not drawn), five CB-02 corner blocks and the "
             f"10 mm closure plate as five PL-01 triangles on the cabin side at the seat plane (Q57 open). Counts and positions are right; joints, holes, hardpoints, seals, shutters "
             f"and the pentagon kit (greenhouse, solar, shield, dock) are not in it. Masses from the model: frames {mass['frames']}, main ribs and caps {mass['main_ribs']}, hub {mass['hub']}, "
             f"secondary ribs {mass['secondary']}, corner blocks {mass['blocks']}, closure {mass['closure']} kg; {total} kg in all for the structure drawn.")
    PARTS["A-04"] = dict(id="A-04", name="Pentagon panel assembly, schematic: five frames, five main ribs, hub, 90 secondary ribs, five corner blocks, closure plate",
                         material="6061-T6 + 2219-T852", mass_kg=total, notes=notes, dims=dict(edge=EDGE, circumradius=round(R_PENT, 1), apothem=round(A_PENT, 1), **counts),
                         rev=REV, source="TRUTH Rev F draft (5 Nov); parts_lib.py primitives", files=name, bbox_mm=bbox(comp), masses=mass, assembly=True)
    check("A-04", bbox=bbox(comp), expected_envelope=f"{2*R_PENT*math.cos(math.radians(18)):.0f} x {R_PENT + A_PENT:.0f} x 400", counts=counts, secondary_segment_lengths=sorted(set(seg_lengths)),
          main_rib_length=round(rib_len, 1))
    return parts, colors

# ============================================================ run
if __name__ == "__main__":
    which_ids = sys.argv[1:]
    which = lambda k: (not which_ids) or (k in which_ids)
    t0 = time.time()
    for fn in (build_corner_blocks, build_hardpoint, build_brace, build_pane, build_closure, build_corner_node, build_frames, build_hardpoint_fitting, build_pentagon):
        try:
            fn(which)
        except Exception:
            traceback.print_exc()
            FAILED_BLENDS.append(f"{fn.__name__} crashed: {traceback.format_exc().splitlines()[-1]}")
        json.dump(PARTS, open(f"{OUT}/parts.json", "w"), indent=1, default=_plain)
        json.dump(CHECKS, open(f"{OUT}/checks.json", "w"), indent=1, default=_plain)
    json.dump(dict(failed_blends=FAILED_BLENDS), open(f"{OUT}/blend_log.json", "w"), indent=1)
    print("failed blends:", FAILED_BLENDS)
    print(f"done in {time.time() - t0:.0f} s")
