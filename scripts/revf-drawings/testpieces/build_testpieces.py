"""HCSA test pieces at Rev F (180 mm frame), CadQuery 2.8. 7-8 Nov 2026.

Builds the T1 seam slices (75, 150, 225), the 550 mm seal article with its grip legs and dummy hardpoint
(RE-03 rev B), and the 4140 pull blocks (rev B lug rows, one M24 for run 1), as STEP, STL and SVG views,
plus an assembly STEP per article. Units mm.

Coordinates (test slice, flat: z equals z'):
  x across the joint. The joint plane is x = 0. Frame B (glands) lies at x <= 0, frame A (flat face) at x >= 0.
  y along the seam, 0 .. L.
  z depth: 0 = outer (space) face, 180 = cabin face = pane seat plane (P-06 convention).

Sources: RE-01-1/2/3 and RE-02 (24 Oct), RE-03 rev B (2 Nov), RF-03 (5 Nov), hcsa_params_revF.json, parts_lib.py (P-06).
Everything marked DFM below is a proposal for Marco's review on 13 Nov, not a decision.
"""
import json, math, os, sys
import cadquery as cq
from cadquery import exporters

P = json.load(open(os.path.join(os.path.dirname(__file__), "..", "src", "hcsa_params_revF.json")))
v = lambda g, k: P[g][k][0]

OUT = os.path.join(os.path.dirname(__file__), "out")
for d in ("step", "stl", "svg", "asm"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

RHO = {"6061-T651": 2.70e-6, "4140 QT": 7.85e-6, "A286": 7.94e-6, "butyl": 1.2e-6}

# ---- parameters ----
D       = v("frame", "depth")            # 180
WEB     = v("frame", "web")              # 20
FL_T    = v("frame", "flange_thickness") # 10 (flange and lip)
LEG     = 200.0                          # grip legs as drawn (RE-01). DFM variant: 120 (see LEG_DFM)
LEG_DFM = 120.0
GW, GD  = v("seal", "gland_width"), v("seal", "gland_depth")   # 7.1 x 4.0
Z_G1    = v("seal", "outer_cord_z")      # 18
Z_G2    = Z_G1 + v("seal", "centreline_spacing")               # 32
Z_RTV   = 42.0; R_RTV = 3.0
Z_PORT  = 25.0; D_PORT = 2.0; D_M5_DRILL = 4.2; M5_DEPTH = 8.0
Z_BOLT  = v("seam_bolt", "row_z")        # 58
PITCH   = v("seam_bolt", "pitch")        # 75
D_BOLT_HOLE = 8.5                        # drilled (RE-01 had 8.4 reamed); a clamp bolt, not a shear pin
R_IN    = 6.0                            # inside corners web/flange, web/lip (TRUTH 10.4, OPEN-5)
LEG_HOLE = 14.0                          # drilled; M12 screws need play to find the block threads (was 13.5)
BLK_X   = 80.0                           # block along the leg
BLK_Z0, BLK_Z1 = FL_T, D - FL_T          # block between the legs: z 10 .. 170 (160 tall)
M12_DRILL, M12_DEPTH = 10.2, 31.0        # tapped M12 from each bearing face, 26 mm full thread
M24_DRILL, M24_DEPTH = 21.0, 40.0        # run 1: M24 x 3 in the pull face at the block centre
LUG_Z = (42.0, 74.0)                     # RE-03 rev B lug screw rows (relative to the outer flange, unchanged)
LUG_DY = 30.0                            # +-30 from mid-length (150, 225, 550); 25 on the 75 block
HP_W, HP_PIN_D, HP_PITCH = 200.0, 40.0, 60.0   # TP3 dummy hardpoint on the 550 article
HP_Z_AS_DRAWN = 140.0                    # fitting centre as drawn (RE-06-1: 110 to 170 deep)
HP_Z_MOVED    = 76.0                     # HP1M study: pads 46 to 106 deep, on the line of the pull

def box(dx, dy, dz, x0=0.0, y0=0.0, z0=0.0):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x0, y0, z0))

def cyl_x(d, x0, x1, y, z):
    """cylinder along X from x0 to x1"""
    return cq.Workplane("YZ").center(y, z).circle(d / 2).extrude(x1 - x0).translate((x0, 0, 0))

def cyl_z(d, z0, z1, x, y):
    return cq.Workplane("XY").center(x, y).circle(d / 2).extrude(z1 - z0).translate((0, 0, z0))

def cyl_y(d, y0, y1, x, z):
    return cq.Workplane("XZ").center(x, z).circle(d / 2).extrude(-(y1 - y0)).translate((0, y0, 0))

def bolt_positions(L, hardpoint):
    if hardpoint:  # RF-03: 2 + 2 bolts in the two bays beside the 200 mm dummy fitting, centred in each bay
        bay = L / 2 - HP_W / 2
        n = int((bay - 60) // PITCH) + 1
        f0 = (bay - (n - 1) * PITCH) / 2
        return [f0 + i * PITCH for i in range(n)] + [L - f0 - i * PITCH for i in range(n)]
    nb = int(round(L / PITCH))
    return [L / 2 + (i - (nb - 1) / 2) * PITCH for i in range(nb)]

def leg_hole_ys(L):
    """RE-01-3: 75 mm pitch along the slice; the 75 slice has its outer row moved to 16.5 / 58.5 (OPEN-6)."""
    if L == 75:
        return {"inner": [18.75, 56.25], "outer": [16.5, 58.5]}
    n = int(L // PITCH)
    ys = [L / 2 + (i - (n - 1) / 2) * PITCH for i in range(n)]
    return {"inner": ys, "outer": ys}

def leg_rows_x(leg):
    """block sits at the leg end: x from -(WEB+leg) to -(WEB+leg)+BLK_X; rows 20 mm in from the block edges"""
    x0 = -(WEB + leg)
    return {"outer": x0 + 20, "inner": x0 + BLK_X - 20}, x0

def frame(L, grooved, leg=LEG, hardpoint_z=None, side=-1):
    """side -1: frame B at x<=0 (joint face at x=0). side +1: frame A mirrored to x>=0."""
    web = box(WEB, L, D, -WEB, 0, 0)
    fl = box(leg, L, FL_T, -(WEB + leg), 0, 0)
    lip = box(leg, L, FL_T, -(WEB + leg), 0, D - FL_T)
    s = web.union(fl).union(lip)
    # R6 inside corners (edges parallel to Y at x=-WEB, z=FL_T and z=D-FL_T)
    try:
        s = s.edges(cq.selectors.BoxSelector((-WEB - 0.5, -1, FL_T - 0.5), (-WEB + 0.5, L + 1, FL_T + 0.5))).fillet(R_IN)
        s = s.edges(cq.selectors.BoxSelector((-WEB - 0.5, -1, D - FL_T - 0.5), (-WEB + 0.5, L + 1, D - FL_T + 0.5))).fillet(R_IN)
    except Exception as e:
        print("  fillet skipped:", e)
    rows, bx0 = leg_rows_x(leg)
    lys = leg_hole_ys(L)
    for row in ("inner", "outer"):
        for y in lys[row]:
            s = s.cut(cyl_z(LEG_HOLE, -1, FL_T + 1, rows[row], y))
            s = s.cut(cyl_z(LEG_HOLE, D - FL_T - 1, D + 1, rows[row], y))
    for y in bolt_positions(L, hardpoint_z is not None):
        s = s.cut(cyl_x(D_BOLT_HOLE, -WEB - 1, 1, y, Z_BOLT))
    if hardpoint_z is not None:
        for k in (-1, 0, 1):
            s = s.cut(cyl_x(HP_PIN_D, -WEB - 1, 1, L / 2 + k * HP_PITCH, hardpoint_z))
    if grooved:
        for zc in (Z_G1, Z_G2):
            g = box(GD + 1, L + 2, GW, -GD, -1, zc - GW / 2)
            try:
                g = g.edges(cq.selectors.BoxSelector((-GD - 0.5, -2, zc - GW / 2 - 0.5), (-GD + 0.5, L + 2, zc + GW / 2 + 0.5))).fillet(0.7)
            except Exception as e:
                print("  gland bottom radius skipped:", e)
            s = s.cut(g)
        s = s.cut(cyl_y(2 * R_RTV, -1, L + 1, 0, Z_RTV))
        s = s.cut(cyl_x(D_PORT, -WEB - 1, 1, L / 2, Z_PORT))
        s = s.cut(cyl_x(D_M5_DRILL, -WEB - 1, -WEB + M5_DEPTH, L / 2, Z_PORT))
    if side > 0:
        s = s.mirror("YZ")
    return s

def pull_block(L, leg=LEG, lug_dy=LUG_DY):
    rows, bx0 = leg_rows_x(leg)
    b = box(BLK_X, L, BLK_Z1 - BLK_Z0, bx0, 0, BLK_Z0)
    lys = leg_hole_ys(L)
    for row in ("inner", "outer"):
        for y in lys[row]:
            b = b.cut(cyl_z(M12_DRILL, BLK_Z1 - M12_DEPTH, BLK_Z1 + 1, rows[row], y))   # from the top bearing face (lip side)
            b = b.cut(cyl_z(M12_DRILL, BLK_Z0 - 1, BLK_Z0 + M12_DEPTH, rows[row], y))   # from the bottom bearing face (flange side)
    zc = (BLK_Z0 + BLK_Z1) / 2
    b = b.cut(cyl_x(M24_DRILL, bx0 - 1, bx0 + M24_DEPTH, L / 2, zc))                    # run 1, straight pull
    for z in LUG_Z:
        for dy in (-lug_dy, lug_dy):
            b = b.cut(cyl_x(M12_DRILL, bx0 - 1, bx0 + 20, L / 2 + dy, z))              # run 2 lug screws (rev B)
    b = b.edges("|Y").chamfer(1.0)
    return b, bx0

def seam_bolt(grip=43.0):
    head = cq.Workplane("YZ").polygon(6, 12.7 / math.cos(math.radians(30))).extrude(4.9)
    shank = cq.Workplane("YZ").circle(7.94 / 2).extrude(grip).translate((4.9, 0, 0))
    thread = cq.Workplane("YZ").circle(7.94 / 2 - 0.3).extrude(12).translate((4.9 + grip, 0, 0))
    return head.union(shank).union(thread)

def mass(shape, material):
    return shape.val().Volume() * RHO[material]

def export(shape, name, views=True):
    exporters.export(shape, f"{OUT}/step/{name}.step")
    exporters.export(shape, f"{OUT}/stl/{name}.stl", tolerance=0.2, angularTolerance=0.2)
    if views:
        for view, d in dict(front=(0, -1, 0), top=(0, 0, 1), side=(1, 0, 0), iso=(1, -1.2, 0.8)).items():
            exporters.export(shape, f"{OUT}/svg/{name}_{view}.svg", opt=dict(width=640, height=440, marginLeft=12, marginTop=12,
                             projectionDir=d, strokeWidth=0.6, strokeColor=(30, 30, 30), hiddenColor=(170, 170, 170),
                             showHidden=view != "iso", showAxes=False, focus=None))

def article(L, hardpoint_z=None, leg=LEG, tag=""):
    name = f"T1-{L:03d}" if L != 550 else "SA-550"
    name += tag
    lug_dy = 25.0 if L == 75 else LUG_DY
    fb = frame(L, True, leg, hardpoint_z, -1)
    fa = frame(L, False, leg, hardpoint_z, +1)
    blk, bx0 = pull_block(L, leg, lug_dy)
    blk2 = blk.mirror("YZ")
    bom = []
    def add(pid, desc, shape, material, qty):
        m = mass(shape, material)
        bom.append(dict(id=pid, desc=desc, material=material, qty=qty, mass_kg=round(m, 3), volume_mm3=round(shape.val().Volume()))); return m
    add(f"{name}-FB", f"Frame B (glands, RTV recess, leak port), {L} mm, 180 deep, legs {leg:.0f}", fb, "6061-T651", 1)
    add(f"{name}-FA", f"Frame A (flat joint face), {L} mm, 180 deep, legs {leg:.0f}", fa, "6061-T651", 1)
    add(f"{name}-PB", f"Pull block {BLK_Z1-BLK_Z0:.0f} x {BLK_X:.0f} x {L}, M12 from both bearing faces, M24 run 1, lug rows run 2", blk, "4140 QT", 2)
    export(fb, f"{name}-FB"); export(fa, f"{name}-FA"); export(blk, f"{name}-PB")
    # assembly: frames face to face, blocks on both legs, seam bolts
    asm = cq.Assembly(name=name)
    asm.add(fb, name="frame_B", color=cq.Color(0.72, 0.75, 0.78))
    asm.add(fa, name="frame_A", color=cq.Color(0.85, 0.87, 0.89))
    asm.add(blk, name="block_B", color=cq.Color(0.35, 0.35, 0.38))
    asm.add(blk2, name="block_A", color=cq.Color(0.35, 0.35, 0.38))
    for i, y in enumerate(bolt_positions(L, hardpoint_z is not None)):
        b = seam_bolt().translate((-WEB - 4.9 - 1.6, y, Z_BOLT))
        asm.add(b, name=f"bolt_{i}", color=cq.Color(0.5, 0.5, 0.55))
    for zc in (Z_G1, Z_G2):
        cord = cyl_y(5.33, 0, L, -GD / 2, zc)
        asm.add(cord, name=f"cord_{zc:.0f}", color=cq.Color(0.1, 0.1, 0.1))
    asm.save(f"{OUT}/asm/{name}_assembly.step")
    # checks: bounding boxes, hole counts
    bb = fb.val().BoundingBox()
    chk = dict(frame_B_bbox=[round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)],
               expected=[WEB + leg, L, D],
               bolts=len(bolt_positions(L, hardpoint_z is not None)),
               leg_holes_per_leg=sum(len(vv) for vv in leg_hole_ys(L).values()),
               hardpoint_z=hardpoint_z, lug_dy=lug_dy)
    print(name, chk, "masses:", [(r["id"], r["mass_kg"]) for r in bom])
    return dict(name=name, L=L, leg=leg, hardpoint_z=hardpoint_z, bom=bom, checks=chk)

if __name__ == "__main__":
    out = []
    for L in (75, 150, 225):
        out.append(article(L))
    out.append(article(550, hardpoint_z=HP_Z_AS_DRAWN))
    out.append(article(550, hardpoint_z=HP_Z_MOVED, tag="-HPmoved"))
    # DFM variant: short legs on the 150 slice, to show the stock saving
    out.append(article(150, leg=LEG_DFM, tag="-DFMlegs120"))
    json.dump(dict(parameters=dict(D=D, WEB=WEB, FL_T=FL_T, LEG=LEG, GW=GW, GD=GD, Z_G1=Z_G1, Z_G2=Z_G2, Z_RTV=Z_RTV, Z_PORT=Z_PORT, Z_BOLT=Z_BOLT,
                                   PITCH=PITCH, D_BOLT_HOLE=D_BOLT_HOLE, R_IN=R_IN, LEG_HOLE=LEG_HOLE, BLK_X=BLK_X, BLK_Z=[BLK_Z0, BLK_Z1],
                                   HP=dict(W=HP_W, pin=HP_PIN_D, pitch=HP_PITCH, z_as_drawn=HP_Z_AS_DRAWN, z_moved=HP_Z_MOVED)),
                   articles=out), open(f"{OUT}/testpieces.json", "w"), indent=1)
    print("done")
