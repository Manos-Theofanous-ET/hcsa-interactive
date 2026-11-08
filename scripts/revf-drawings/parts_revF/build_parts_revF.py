"""HCSA Rev F parts, 8 Nov 2026 PROPOSAL for the 13 Nov review (Marco Cross, Prof. Fleeter).
Builds CB-01, CB-02, HP-01, HP-01M, HP-02, HP-03, P-11, P-07 (21 mm), PL-01, A-03, A-04 with CadQuery 2.8, in the
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

P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "hcsa_params_revF.json")))
v = lambda g, k: P[g][k][0]

CHECKS = json.load(open(f"{OUT}/checks.json")) if os.path.exists(f"{OUT}/checks.json") else {}
FAILED_BLENDS = []

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

# ============================================================ CB-01 / CB-02 corner blocks
TIE_Z_HEX = (125.0, 355.0)
TIE_Z_PENT = (128.3, 364.4)
DOWEL_Z_HEX = 240.0
DOWEL_Z_PENT = round(240.0 / math.cos(math.radians(20.905)) * math.cos(math.radians(16.472)), 1)   # 246.3, same depth along the joint plane

def build_corner_blocks(which):
    for pid, th, tz, dz, name in (("CB-01", 120, TIE_Z_HEX, DOWEL_Z_HEX, "Corner block, hexagon corner (120 deg), 2219-T852, R10 inside corners"),
                                  ("CB-02", 108, TIE_Z_PENT, DOWEL_Z_PENT, "Corner block, pentagon corner (108 deg)")):
        if not which(pid):
            continue
        s, g, log = CB.corner_block(th, tz, dz)
        for m in log:
            FAILED_BLENDS.append(f"{pid}: {m}")
        shape = s
        lean = 20.905 if th == 120 else 16.472
        notes = (f"PROPOSAL for the 13 Nov review (Marco, Rick). One solid block per panel corner, 2219-T852 hand forging, machined; three bolt together at a vertex "
                 f"(A-03). Two legs 230 x 400 x 50 at {th} deg, the joint face on each leg's outer face, z 0 outer face to z 400 cabin face. "
                 f"Four tie holes 23.5 mm per joint face (clearance for the 7/8-14 Inconel 718 studs, 198 kN preload) in two columns 56 mm apart at "
                 f"z {tz[0]} and z {tz[1]}, and two 20 mm dowel holes (room for 24) at z {dz} in the same columns. "
                 f"Landing for the main rib end at the vertex along the corner bisector: a pocket 110 wide (100 flange plus 5 a side) x 400 deep whose "
                 f"flat bottom is {g['d_b']:.0f} mm from the vertex, the walls {g['wall_len']:.1f} mm long where they cut the legs' inner faces, "
                 f"{g['wall_min']:.1f} mm of metal between the pocket corner and the joint face. "
                 f"Machining-driven features, after Marco's review of 7 Nov: R10 at the two inside corners of the landing (a 20 mm end mill or smaller), "
                 f"2 mm chamfers on every outside edge, no sharp inside corner anywhere; the block could be cast instead (material would change). "
                 f"Drawn straight (prismatic along the panel z) like P-06; the real joint face lies on the radial plane through the edge and leans "
                 f"{lean} deg to the panel normal, so the real section is a parallelogram and the tie holes are normal to that face. "
                 f"CHANGES AGAINST THE BRIEF, to be confirmed: (1) the tie columns are at 136 and 192 mm from the vertex, not 87 and 143 (centred on the "
                 f"leg): at 87 the inner hole breaks into the rib landing, whose wall reaches {g['x_wall']:.0f} mm along the inner face; 136 is the "
                 f"nearest position where a 45 mm washer clears the landing on both block types. The C1 model should be rerun at these positions. "
                 f"(2) The landing cannot be '30 mm into the block' from the re-entrant corner: the block is only {2*g['d_min']*math.tan(g['alpha']):.0f} mm wide "
                 f"{g['d_min']:.0f} mm from the vertex and a 110 pocket there breaks through the joint faces; the bottom is put {g['d_b']:.0f} mm from the vertex, "
                 f"the deepest position that keeps a continuous 110 mm bearing face, which makes the walls {g['wall_len']:.1f} long. The R12 at the re-entrant "
                 f"corner is consumed by the landing (the pocket bottom lies {g['pocket_depth_at_bisector']:.1f} mm beyond it). "
                 f"Not modelled: how the two 180 mm frame members end at the legs, the rib fixing in the landing, the O10 corner seal path, the tie nuts and washers.")
        if th == 108:
            notes += (f" Pentagon: tie rows at z 128.3 and 364.4 (the same 133.8 and 380.0 mm along the leaning joint face as the hexagon's 125 and 355); the dowel "
                      f"is at z {dz} for the same reason (the brief's 240 would miss the hexagon's dowel by 6.3 mm along the joint face).")
        dims = dict(legs=f"2 x 230 x 400 x 50 at {th} deg", tie_hole=TIE_HOLE_STR, tie_columns_from_vertex="136, 192 (pitch 56)",
                    tie_rows_z=f"{tz[0]}, {tz[1]}", dowel=f"20 mm (room for 24) at z {dz}", landing=f"110 wide x 400, bottom {g['d_b']:.0f} from the vertex, walls {g['wall_len']:.1f}",
                    inside_radius="R10 (landing corners)", outside_chamfer=2.0, stock="2219-T852 hand forging")
        register(pid, name, shape, "2219-T852", notes, dims, source="RE-06-2, Ansys C1 (5 Nov), Marco's review (7 Nov)")
        check(pid, bbox=bbox(shape), expected_envelope=f"legs 230 long, 50 thick, 400 deep at {th} deg",
              tie_holes=g["n_tie_holes"], dowel_holes=g["n_dowel_holes"], hole_volume=round(g["hole_volume"]), hole_volume_expected=round(g["hole_volume_expected"]),
              landing_bottom_from_vertex=g["d_b"], wall_to_joint_face=round(g["wall_min"], 1), landing_wall_on_inner_face=round(g["x_wall"], 1),
              brief_tie_columns_clash=f"columns at 87/143 would break into the landing (wall at {g['x_wall']:.0f} mm); moved to 136/192", blends_failed=log)

TIE_HOLE_STR = "23.5 (7/8 in clearance)"

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
BOLT_Y = (-(HP_L / 2 - 31.25), HP_L / 2 - 31.25)      # +-88.75
Z_BOLT_MOVED = 118.0                                   # see hardpoint_clearances()

def fitting_hole_pattern(zc):
    """six fixing holes clear of the three 40 bores: two columns of two at the ends, one each between the bores"""
    return [(-90.0, zc - 20), (-90.0, zc + 20), (90.0, zc - 20), (90.0, zc + 20), (-30.0, zc), (30.0, zc)]

def hardpoint_clearances(zc, bolt_z):
    bores = [(k * PIN_PITCH, zc) for k in (-1, 0, 1)]
    bolts = [(y, bolt_z) for y in BOLT_Y]
    d_bore_bolt = min(math.hypot(b[0] - q[0], b[1] - q[1]) - PIN_D / 2 - D_BOLT / 2 for b in bores for q in bolts)
    d_bore_gland = (zc - PIN_D / 2) - (Z_G2 + GW / 2)
    d_bore_lip = (FD - 10) - (zc + PIN_D / 2)
    pad = (zc - FIT_D / 2, zc + FIT_D / 2)
    bolt_edge_vs_pad = (bolt_z - D_BOLT / 2) - pad[1]          # positive: hole clear above the pad
    washer_vs_pad = (bolt_z - 8.0) - pad[1]                    # 16 mm washer
    fit_holes = fitting_hole_pattern(zc)
    d_fithole_bolt = min(math.hypot(f[0] - q[0], f[1] - q[1]) - FIT_TAP / 2 - D_BOLT / 2 for f in fit_holes for q in bolts)
    d_fithole_bore = min(math.hypot(f[0] - b[0], f[1] - b[1]) - FIT_TAP / 2 - PIN_D / 2 for f in fit_holes for b in bores)
    bolt_under_pad = (pad[0] - 8.0 < bolt_z < pad[1] + 8.0) and abs(BOLT_Y[1]) - 8.0 < FIT_L / 2
    return dict(pin_z=zc, bolt_z=bolt_z, pad_z=list(pad), wall_bore_to_bolt_hole=round(d_bore_bolt, 1), bore_to_gland=round(d_bore_gland, 1),
                bore_to_lip_underside=round(d_bore_lip, 1), bolt_hole_edge_above_pad=round(bolt_edge_vs_pad, 2), washer16_above_pad=round(washer_vs_pad, 1),
                bolt_nut_under_fitting_pad=bolt_under_pad, wall_fitting_tap_to_bolt=round(d_fithole_bolt, 1), wall_fitting_tap_to_bore=round(d_fithole_bore, 1))

def hardpoint_block(zc, bolt_z, log):
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
    for y in BOLT_Y:
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
                                  ("HP-01M", Z_PIN_MOVED, Z_BOLT_MOVED, "Hardpoint block, moved fitting (pins at z 76)")):
        if not which(pid):
            continue
        log = []
        s, v0, vols = hardpoint_block(zc, bolt_z, log)
        for m in log:
            FAILED_BLENDS.append(f"{pid}: {m}")
        cl = hardpoint_clearances(zc, bolt_z)
        cl_brief = hardpoint_clearances(zc, Z_BOLT) if zc == Z_PIN_MOVED else None
        cl_110 = hardpoint_clearances(zc, 110.0) if zc == Z_PIN_MOVED else None
        common = (f"PROPOSAL for the 13 Nov review. The frame web thickened from 20 to {HP_T:.0f} mm over {HP_L:.0f} mm of the seam at a hardpoint (three per seam at the quarter "
                  f"points), joint face flat at x 20 (P-06 convention, panel side toward -x), modelled alone with a 60 mm stub of the 20 mm web at each end and R10 "
                  f"blends from the block to the web. The two 7.1 x 4.0 butyl glands at z 18 and 32 run through on the joint face (the fitting must not cover them: "
                  f"it sits on the panel side). Three 40 mm pin bores at 60 mm pitch through the thickness, two 8.5 mm seam bolt holes (the plain bolts beside the "
                  f"fitting, 31.25 mm from each end face) and six 8.5 mm tap-drill holes 35 deep (M10) from the panel face for the fitting HP-02 (two pairs at the ends, "
                  f"one each between the bores; the brief's two rows of three cannot clear the three bores). The frame flange and lip (z 0-10 and 170-180) are not in "
                  f"this solid. Pins are A286, dry-film lubricated (HP-03); the fitting is Ti-6Al-4V (HP-02).")
        if zc == Z_PIN_AS_DRAWN:
            notes = common + (f" AS DRAWN (RE-06-1): pins at z 140, fitting pads z 110 to 170; the pad touches the underside of the seat lip at z 170. "
                              f"Clearances: bore to seam bolt hole {cl['wall_bore_to_bolt_hole']} mm, bore to the inner gland {cl['bore_to_gland']} mm, bore to the lip underside "
                              f"{cl['bore_to_lip_underside']} mm. The HP1 run of 6-7 Nov shows this position fails: the fitting sits 64 mm below the line of the pull and acts as a hinge, "
                              f"the seals open at 0.22 to 0.47 atm. Kept so both positions can be compared on 13 Nov.")
        else:
            notes = common + (f" MOVED (HP1M study of 7 Nov, passes): pins at z 76, pads z 46 to 106, on the line of the pull. CLEARANCE CHECK: a 40 mm bore at z 76 (edges z 56 to 96) "
                              f"does not overlap the seam bolt row at z 58: the nearest bolt hole (y 88.75) is {cl_brief['wall_bore_to_bolt_hole']} mm of metal away from the bore, and the bore is "
                              f"{cl['bore_to_gland']} mm above the inner gland (z 28.5-35.5). THE CLASH IS ELSEWHERE: the moved fitting pad (200 x 60, y +-100, z 46-106) covers the two plain "
                              f"bolts at y +-88.75 z 58, so their nuts would sit under the fitting, and the fitting's own end fixing holes (y +-90, z 56) land on them. So in this variant the two "
                              f"plain bolts are moved to z {Z_BOLT_MOVED:.0f}: the hole edge is {cl['bolt_hole_edge_above_pad']} mm above the pad and a 16 mm washer {cl['washer16_above_pad']} mm; "
                              f"at the brief's z 110 the hole edge would be {cl_110['bolt_hole_edge_above_pad']} mm from the pad and the washer {-cl_110['washer16_above_pad']:.0f} mm over it. "
                              f"CAUTION: D1 showed the seal gap grows when the bolt row moves away from the seals (z 70 failed), so a deeper plain bolt is the wrong direction for the seal; the "
                              f"alternatives are the plain bolts moved along the seam into the 20 mm web beside the block (y +-137.5, z 58, which is where the HP1M run had them) or a "
                              f"shorter fitting (160 long). To decide on 13 Nov. Bore to the tap holes {cl['wall_fitting_tap_to_bore']} mm, tap holes to the moved bolts {cl['wall_fitting_tap_to_bolt']} mm.")
        dims = dict(block=f"{HP_L:.0f} along the seam x {FD:.0f} deep x {HP_T:.0f} thick", web_stubs=f"20 x {STUB_L:.0f} each end, R10 blend", glands=f"2 x {GW} x {GD} at z {Z_G1:.0f} and {Z_G2:.0f}",
                    pin_bores=f"3 x {PIN_D:.0f} at {PIN_PITCH:.0f} pitch, z {zc:.0f}", seam_bolts=f"2 x {D_BOLT} at y +-88.75, z {bolt_z:.0f}", fitting_fixing="6 x 8.5 tap drill (M10) 35 deep from the panel face",
                    fitting_pad_z=f"{zc - 30:.0f} to {zc + 30:.0f}")
        register(pid, name, s, "6061-T6", notes, dims, source="RE-06-1, Ansys HP1/HP1M (6-7 Nov), C3 (Oct)")
        exp_bores = 3 * math.pi * (PIN_D / 2) ** 2 * HP_T
        check(pid, bbox=bbox(s), expected_envelope="50 x 360 x 180 (block 240 plus two 60 stubs)", cut_volumes=vols, pin_bore_volume_expected=round(exp_bores),
              pin_bore_volume=sum(vols[4:7]), n_holes=dict(glands=2, seam_bolts=2, pin_bores=3, fitting_taps=6), clearances=cl,
              clearances_with_bolts_at_z58=cl_brief, clearances_with_bolts_at_z110=cl_110, blends_failed=log)

def fitting_half(zc):
    s = box(FIT_T, FIT_L, FIT_D, FWEB - HP_T - FIT_T, -FIT_L / 2, zc - FIT_D / 2)   # x -60 .. -30, mounted as drawn
    v0 = s.val().Volume()
    for k in (-1, 0, 1):
        s = s.cut(cyl_x(PIN_D, -100, 100, k * PIN_PITCH, zc))
    v1 = s.val().Volume()
    for (y, z) in fitting_hole_pattern(zc):
        s = s.cut(cyl_x(FIT_HOLE, -100, 100, y, z))
    v2 = s.val().Volume()
    try:
        s = s.edges("|X").chamfer(1.0)
    except Exception as e:
        FAILED_BLENDS.append(f"HP-02 1 mm edge chamfers failed: {e}")
    return s, (v0, v1, v2)

def build_fitting(which):
    if which("HP-02"):
        s, (v0, v1, v2) = fitting_half(Z_PIN_AS_DRAWN)
        notes = (f"PROPOSAL. One of the pair of titanium fittings (TP3), one in each panel, bolted to the panel side of HP-01 (x -60 to -30) with six 10 mm holes "
                 f"(M10 A286 into the block's tap holes; two pairs at the ends, one each between the bores). 200 along the seam x 60 deep x 30 thick with three 40 mm "
                 f"bores at 60 pitch for the HP-03 pins, no clearance (the pins cross the joint plane into the mirror fitting of the neighbour panel). Measured stiffness "
                 f"2.876 million N/mm (Ansys C3). Drawn at the AS DRAWN height, z 110 to 170 (pins at z 140); the MOVED variant HP-02M is the same part mounted 64 mm "
                 f"higher (pads z 46 to 106, pins at z 76), so one STEP serves both. At the as-drawn height the pad touches the underside of the frame seat lip (z 170). "
                 f"The end holes sit 10 mm from the plate's end and edges (5 mm edge distance): thin, for review. The fixing bolts are in tension under the seam pull (108.7 kN per atmosphere on a hardpoint, so about 15 kN per bolt at 0.8 atm): size and count to check against the C3 model. Open: the bore chamfer stress at 1.5 x proof (Q18: accept, bush or thicken) and the C3 stiffness at the moved position.")
        dims = dict(size=f"{FIT_L:.0f} x {FIT_D:.0f} x {FIT_T:.0f}", bores=f"3 x {PIN_D:.0f} H7 at {PIN_PITCH:.0f}", fixing=f"6 x {FIT_HOLE:.0f} for M10 A286", mounted_as_drawn="z 110-170", mounted_moved="z 46-106 (HP-02M)")
        register("HP-02", "Hardpoint fitting half, Ti-6Al-4V (TP3), as drawn", s, "Ti-6Al-4V", notes, dims, source="RE-06-1, Ansys C3 (Oct), HP1M (7 Nov)")
        check("HP-02", bbox=bbox(s), expected_envelope="30 x 200 x 60", bore_volume=round(v0 - v1), bore_volume_expected=round(3 * math.pi * 400 * FIT_T),
              fixing_hole_volume=round(v1 - v2), fixing_hole_volume_expected=round(6 * math.pi * 25 * FIT_T))
    if which("HP-03"):
        pin = cq.Workplane("YZ").circle(PIN_D / 2).extrude(PIN_L).translate((FWEB - HP_T - FIT_T, 0, Z_PIN_AS_DRAWN))
        try:
            pin = pin.faces("<X or >X").chamfer(1.0)
        except Exception as e:
            FAILED_BLENDS.append(f"HP-03 chamfers failed: {e}")
        notes = (f"PROPOSAL. Hardpoint pin 40 h6 x 160, A286, 1 mm chamfers, dry-film lubricant (MoS2 type) on the shank; three per hardpoint. 160 = fitting 30 + block 50 + "
                 f"block 50 + fitting 30 across the joint plane. Drawn on the as-drawn bore line (z 140, middle bore), from x -60 to 100 in the HP-01 frame. 119 MPa at 1 atm "
                 f"against 655 in C3.")
        register("HP-03", "Hardpoint pin, 40 mm, 160 long, A286, dry-film lubricated", pin, "A286", notes, dict(diameter="40 h6", length=160, chamfer=1.0, quantity_per_hardpoint=3), source="Ansys C3 (Oct)")
        check("HP-03", bbox=bbox(pin), expected_envelope="160 x 40 x 40")

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
    pts, _, _, _ = CB.outline(108)
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

COL = dict(al=(0.67, 0.70, 0.73), forging=(0.72, 0.66, 0.58), ti=(0.55, 0.59, 0.65), steel=(0.47, 0.51, 0.59), glass=(0.63, 0.82, 0.94), plate=(0.75, 0.78, 0.70), brace=(0.60, 0.62, 0.68))

def build_corner_node(which):
    if not which("A-03"):
        return
    import numpy as np
    V, faces = truncated_icosahedron(EDGE)
    # the vertex: pick the one with the largest z, deterministic
    vi = int(np.argmax(V[:, 2] * 1000 + V[:, 0]))
    fs = [f for f in faces if vi in f["verts"]]
    assert len(fs) == 3 and sorted(f["kind"] for f in fs) == ["hex", "hex", "pent"], [f["kind"] for f in fs]
    Vv = V[vi]
    # edges at the vertex: each face contributes its two neighbours of vi; the three distinct neighbours
    nbrs = {}
    for f in fs:
        k = f["verts"].index(vi); n = len(f["verts"])
        for j in (f["verts"][(k - 1) % n], f["verts"][(k + 1) % n]):
            nbrs.setdefault(j, []).append(f)
    assert len(nbrs) == 3 and all(len(x) == 2 for x in nbrs.values())
    edge_lengths = [float(np.linalg.norm(V[j] - Vv)) for j in nbrs]
    hexblk, _, _ = CB.corner_block(120, TIE_Z_HEX, DOWEL_Z_HEX)
    pentblk, _, _ = CB.corner_block(108, TIE_Z_PENT, DOWEL_Z_PENT)
    parts, colors, frames = [], [], []
    for f in fs:
        n_in = -f["normal_out"]                       # depth z goes inward
        k = f["verts"].index(vi); n = len(f["verts"])
        cand = [V[f["verts"][(k + 1) % n]] - Vv, V[f["verts"][(k - 1) % n]] - Vv]
        e1 = cand[0] / np.linalg.norm(cand[0]); e2 = cand[1] / np.linalg.norm(cand[1])
        ey = np.cross(n_in, e1)
        if ey @ e2 < 0:                                # leg A must have the interior (leg B) on its +y side
            e1, e2 = e2, e1; ey = np.cross(n_in, e1)
        blk = hexblk if f["kind"] == "hex" else pentblk
        loc = cq.Location(cq.Plane(origin=tuple(float(x) for x in Vv), xDir=tuple(float(x) for x in e1), normal=tuple(float(x) for x in n_in)))
        shp = cq.Workplane("XY").newObject([blk.val().moved(loc)])
        pl = cq.Plane(origin=tuple(float(x) for x in Vv), xDir=tuple(float(x) for x in e1), normal=tuple(float(x) for x in n_in))
        assert (pl.yDir - cq.Vector(*[float(x) for x in ey])).Length < 1e-9
        parts.append((f"{f['kind']}_block_{len(parts)}", shp)); colors.append(COL["forging"])
        frames.append(dict(kind=f["kind"], e1=e1, ey=ey, n=n_in, interior_angle=math.degrees(math.acos(float(e1 @ e2)))))
    # ties and dowels on the three joint (radial) planes
    tie_ds = [125.0 / math.cos(math.radians(20.905)), 355.0 / math.cos(math.radians(20.905))]      # 133.8, 380.0 along the joint plane
    dowel_d = 240.0 / math.cos(math.radians(20.905))                                                # 256.9
    dihedrals = []
    for j, fpair in nbrs.items():
        e = V[j] - Vv; e /= np.linalg.norm(e)
        r_in = -Vv - (e @ -Vv) * e; r_in /= np.linalg.norm(r_in)       # in the radial plane, perpendicular to the edge, toward the centre
        jn = np.cross(e, r_in)                                           # normal of the joint plane
        # dihedral between the two faces at this edge, and between the two blocks' joint faces (their in-plane perpendiculars)
        fa, fb = fpair
        dih_faces = 180.0 - math.degrees(math.acos(float(np.clip(fa["normal_out"] @ fb["normal_out"], -1, 1))))
        ta = np.cross(fa["normal_out"], e); ta *= np.sign(ta @ (fa["centre"] - Vv))
        tb = np.cross(fb["normal_out"], e); tb *= np.sign(tb @ (fb["centre"] - Vv))
        dih_blocks = math.degrees(math.acos(float(np.clip(ta @ tb, -1, 1))))
        dihedrals.append(dict(edge_to_vertex=int(j), faces=f"{fa['kind']}-{fb['kind']}", dihedral_between_panels=round(dih_faces, 3), angle_between_block_joint_faces=round(dih_blocks, 3),
                              expected=138.19 if fa["kind"] == fb["kind"] == "hex" else 142.62, edge_length=round(float(np.linalg.norm(V[j] - Vv)), 3)))
        for x in CB.TIE_COLS:
            for d in tie_ds:
                c = Vv + e * x + r_in * d
                tie = cq.Workplane("XY").newObject([cq.Solid.makeCylinder(22.2 / 2, 300.0, cq.Vector(*(c - jn * 150.0)), cq.Vector(*jn))])
                parts.append((f"tie_{len(parts)}", tie)); colors.append(COL["steel"])
            c = Vv + e * x + r_in * dowel_d
            dw = cq.Workplane("XY").newObject([cq.Solid.makeCylinder(20.0 / 2, 100.0, cq.Vector(*(c - jn * 50.0)), cq.Vector(*jn))])
            parts.append((f"dowel_{len(parts)}", dw)); colors.append(COL["steel"])
    # measure the dihedrals from the placed solids: the joint faces are the large planar faces through the vertex whose normal is in the panel plane
    def joint_faces(shp, fr):
        out = []
        for f in shp.faces().vals():
            if f.geomType() != "PLANE" or f.Area() < 50000:
                continue
            nrm = f.normalAt(); nrm = np.array([nrm.x, nrm.y, nrm.z])
            c = f.Center(); c = np.array([c.x, c.y, c.z])
            if abs(nrm @ fr["n"]) < 1e-4 and abs((c - Vv) @ nrm) < 1e-2:
                out.append((nrm, c))
        return out
    measured = []
    blocks = [(p, fr) for (p, fr) in zip([q for q in parts if "block" in q[0]], frames)]
    for j in nbrs:
        e = V[j] - Vv; e /= np.linalg.norm(e)
        ns = []
        for (label, shp), fr in blocks:
            for nrm, c in joint_faces(shp, fr):
                if abs(nrm @ e) < 1e-4:   # the face plane contains the vertex (checked above) and is parallel to the edge, so it contains the edge line
                    ns.append(nrm)
        if len(ns) == 2:
            measured.append(round(math.degrees(math.acos(float(np.clip(abs(ns[0] @ ns[1]), -1, 1)))), 3))
        else:
            measured.append(f"{len(ns)} faces found")
    for d, m in zip(dihedrals, measured):
        d["measured_from_solid_faces_deg"] = m
        d["measured_from_solid_faces_supplement_deg"] = round(180 - m, 3) if isinstance(m, float) else m
    # re-express in a node frame: vertex at the origin, +z inward along the vertex radial (the parts' z convention), x along the hex-hex edge
    r_in_v = -Vv / np.linalg.norm(Vv)
    hexhex = [j for j, fp in nbrs.items() if fp[0]["kind"] == fp[1]["kind"] == "hex"][0]
    ex = V[hexhex] - Vv; ex -= r_in_v * (ex @ r_in_v); ex /= np.linalg.norm(ex)
    node_loc = cq.Location(cq.Plane(origin=tuple(map(float, Vv)), xDir=tuple(map(float, ex)), normal=tuple(map(float, r_in_v))))
    inv = node_loc.inverse
    parts = [(label, cq.Workplane("XY").newObject([shp.val().moved(inv)])) for label, shp in parts]
    # how far apart the straight blocks' hole mouths are for the same tie: each mouth is z along its own (non-radial) joint face
    mouth_offsets = []
    for j, fpair in nbrs.items():
        fa, fb = fpair
        za = TIE_Z_HEX if fa["kind"] == "hex" else TIE_Z_PENT; zb = TIE_Z_HEX if fb["kind"] == "hex" else TIE_Z_PENT
        la = 20.905 if fa["kind"] == "hex" else 16.472; lb = 20.905 if fb["kind"] == "hex" else 16.472
        mouth_offsets.append([round(za[i] * math.sin(math.radians(la)) + zb[i] * math.sin(math.radians(lb)), 1) for i in range(2)])
    for d, mo in zip(dihedrals, mouth_offsets):
        d["straight_block_hole_mouths_apart_mm"] = mo
    name = "A-03_corner_node"
    comp = export_assembly(name, parts, colors, "A-03")
    n_ties = sum(1 for p, _ in parts if p.startswith("tie")); n_dowels = sum(1 for p, _ in parts if p.startswith("dowel"))
    masses = dict(blocks_kg=round(sum(p[1].val().Volume() for p in parts if "block" in p[0]) * RHO["2219-T852"], 2),
                  ties_kg=round(sum(p[1].val().Volume() for p in parts if p[0].startswith("tie")) * RHO["Inconel 718"], 2),
                  dowels_kg=round(sum(p[1].val().Volume() for p in parts if p[0].startswith("dowel")) * RHO["A286"], 2))
    total = masses["blocks_kg"] + masses["ties_kg"] + masses["dowels_kg"]
    notes = (f"PROPOSAL. The three corner blocks of one vertex of the real truncated icosahedron (edge 2,250 mm, 11,151 mm across; the 60 vertices from the standard "
             f"coordinates, scaled), two hexagon blocks CB-01 and one pentagon block CB-02, each placed in its own panel plane with its vertex at the shared vertex, "
             f"its legs along the two panel edges meeting there and its depth along the panel's inward normal; 12 ties (22.2 x 300, the 7/8-14 Inconel 718 studs with their "
             f"nut length) and 6 dowels (20 x 100) drawn normal to the three radial joint planes at 133.8, 380.0 (ties) and 256.9 mm (dowels) along those planes from the "
             f"edge, which is where the z 125/355/240 (hexagon) and z 128.3/364.4/246.3 (pentagon) holes meet. Measured here: panel dihedral angles "
             + "; ".join(f"{d['faces']} {d['dihedral_between_panels']}" for d in dihedrals) +
             f" deg against 138.19 and 142.62. Measured on the placed solids, the two blocks' joint faces at each edge are "
             + ", ".join(f"{d['measured_from_solid_faces_deg']}" for d in dihedrals) +
             f" deg apart (the supplements of the dihedrals): on the real part both faces lie on the radial plane and that angle is zero. The assembly is exported in a node "
             f"frame, vertex at the origin, +z inward along the vertex radial, x along the hex-hex edge; the vertex sat at {[round(float(x), 1) for x in Vv]} in the "
             f"polyhedron frame. WHAT THE ASSEMBLY SHOWS: because the blocks are drawn straight "
             f"(joint faces normal to their own panel) while the real joint face is the radial plane, each pair of neighbouring blocks overlaps in a prism about 75 mm on a side "
             f"along the outer edge, and the facing tie holes do not line up: for the same tie the two blocks' hole mouths sit "
             + "; ".join(f"{d['faces']} {d['straight_block_hole_mouths_apart_mm'][0]} and {d['straight_block_hole_mouths_apart_mm'][1]} mm" for d in dihedrals) +
             f" apart (rows 1 and 2, z x sin of the lean on each side) with their axes {', '.join(str(d['measured_from_solid_faces_deg']) for d in dihedrals)} deg apart; the ties are drawn where the real "
             f"holes meet on the radial plane, not through these straight blocks' holes. The next step is "
             f"the block with its joint face leaning 20.905 deg (hexagon) or 16.472 deg (pentagon) and the tie holes normal to it; the C1 model has it that way. "
             f"Masses: blocks {masses['blocks_kg']} kg, ties {masses['ties_kg']} kg, dowels {masses['dowels_kg']} kg.")
    PARTS["A-03"] = dict(id="A-03", name="Corner node assembly: two hexagon blocks and one pentagon block at a vertex, with 12 ties and 6 dowels", material="2219-T852 + Inconel 718 + A286",
                         mass_kg=round(total, 3), notes=notes, dims=dict(blocks=3, ties=n_ties, dowels=n_dowels, edge=EDGE, dihedrals=dihedrals, vertex_xyz=[round(float(x), 1) for x in Vv]),
                         rev=REV, source="Truncated icosahedron coordinates; RE-06-2; C1 (5 Nov)", files=name, bbox_mm=bbox(comp), masses=masses, assembly=True)
    check("A-03", bbox=bbox(comp), n_ties=n_ties, n_dowels=n_dowels, dihedrals=dihedrals, block_interior_angles=[round(f["interior_angle"], 3) for f in frames],
          edge_lengths_at_vertex=[round(x, 3) for x in edge_lengths], polyhedron_diameter=round(2 * float(np.linalg.norm(V, axis=1).max()), 1))
    print("   dihedrals:", dihedrals)
    return parts, colors

# ============================================================ A-04 pentagon panel assembly (schematic)
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
    frame_len = EDGE - 2 * CB.LEG                      # 1790: the frames run between the corner blocks' leg ends
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
    blk, _, _ = CB.corner_block(108, TIE_Z_PENT, DOWEL_Z_PENT)
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
    for fn in (build_corner_blocks, build_hardpoint, build_fitting, build_brace, build_pane, build_closure, build_corner_node, build_pentagon):
        try:
            fn(which)
        except Exception:
            traceback.print_exc()
            FAILED_BLENDS.append(f"{fn.__name__} crashed: {traceback.format_exc().splitlines()[-1]}")
        json.dump(PARTS, open(f"{OUT}/parts.json", "w"), indent=1)
        json.dump(CHECKS, open(f"{OUT}/checks.json", "w"), indent=1)
    json.dump(dict(failed_blends=FAILED_BLENDS), open(f"{OUT}/blend_log.json", "w"), indent=1)
    print("failed blends:", FAILED_BLENDS)
    print(f"done in {time.time() - t0:.0f} s")
