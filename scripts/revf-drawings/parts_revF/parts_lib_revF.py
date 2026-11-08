"""HCSA parts library, CadQuery 2.8. Rev F copy of parts_lib.py (2 Nov 2026) made 8 Nov 2026 for the Rev F parts
(corner blocks, hardpoint, main rib brace, pentagon closure, corner node assembly, P-07 at 21 mm). Units mm. z is the
outward normal of a panel: z 0 = outer face of the rib/frame grid (space side), z 180 = cabin face of the secondary rib
inner flange = the pressure pane seat plane; z 400 = cabin face of the main rib and the corner block.
Changes against parts_lib.py: OUT, STL into out/stl, Ti-6Al-4V in RHO, PANE_T 21, default rev, and main_rib(),
cap_angle(), rib_segment() take a length so the pentagon assembly can use them."""
import math, json, os
import cadquery as cq
from cadquery import exporters

OUT = "/home/claude/package/parts_revF/out"
RHO = {"6061-T6": 2.70e-6, "7075-T7351": 2.81e-6, "2219-T852": 2.84e-6, "A286": 7.94e-6, "BOROFLOAT 33": 2.23e-6,
       "Inconel 718": 8.19e-6, "Ti-6Al-4V": 4.43e-6}
PARTS = json.load(open(f"{OUT}/parts.json")) if os.path.exists(f"{OUT}/parts.json") else {}
REV = "8 Nov 2026 PROPOSAL"

def _solid(shape):
    return shape.val() if hasattr(shape, "val") else shape

def register(pid, name, shape, material, notes, dims, rev=REV, source="", views=True, hidden=True, fname=None):
    vol = _solid(shape).Volume()
    mass = vol * RHO[material]
    bb = _solid(shape).BoundingBox()
    fname = fname or pid
    PARTS[pid] = dict(id=pid, name=name, material=material, mass_kg=round(mass, 3), volume_mm3=round(vol), notes=notes, dims=dims, rev=rev, source=source,
                      bbox_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)], files=fname)
    exporters.export(shape, f"{OUT}/step/{fname}.step")
    exporters.export(shape, f"{OUT}/stl/{fname}.stl", tolerance=0.2, angularTolerance=0.2)
    if views:
        for view, d in dict(front=(0, -1, 0), top=(0, 0, 1), side=(1, 0, 0), iso=(1, -1.2, 0.8)).items():
            exporters.export(shape, f"{OUT}/svg/{fname}_{view}.svg", opt=dict(width=520, height=380, marginLeft=12, marginTop=12,
                             projectionDir=d, strokeWidth=0.6, strokeColor=(30, 30, 30), hiddenColor=(160, 160, 160),
                             showHidden=(view != "iso") and hidden, showAxes=False, focus=None))
    print(f"{pid}  {name}: {mass:.3f} kg   bbox {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f}")
    return shape

# ---------- sections ----------
def I_section(d, bf, tf, tw):
    """I profile in the XZ plane, extruded along Y. z from 0 (outer face) to d."""
    return (cq.Workplane("XZ").moveTo(-bf/2, 0).lineTo(bf/2, 0).lineTo(bf/2, tf).lineTo(tw/2, tf).lineTo(tw/2, d-tf)
            .lineTo(bf/2, d-tf).lineTo(bf/2, d).lineTo(-bf/2, d).lineTo(-bf/2, d-tf).lineTo(-tw/2, d-tf).lineTo(-tw/2, tf)
            .lineTo(-bf/2, tf).close())

# ---------- P-01 secondary rib segment ----------
D2, BF2, TF2, TW2 = 180.0, 60.0, 10.0, 5.0
PITCH = 562.5; CORE = 90.0; TONGUE = 10.0; GAP = 2.0
SEG_L = PITCH - CORE - 2*GAP          # 468.5 mm flange to flange
BOLT = 7.94; HOLE = 8.03               # 5/16 close tolerance, reamed
def rib_segment(SEG_L=SEG_L):
    s = I_section(D2, BF2, TF2, TW2).extrude(SEG_L).translate((0, SEG_L/2, 0))   # along Y, centred (XZ normal is -Y)
    # web cut back TONGUE at each end: the web is left as a tongue only between the flanges? No: the tongue enters the
    # fork, so the web stays full length and the FLANGES are cut back by the fork cheek length... keep it simple and
    # true to the note: flanges stop at the segment end, web tongue continues 90 mm beyond each end.
    tongue = cq.Workplane("XZ").rect(TW2, D2 - 2*TF2 - 2).extrude(TONGUE).translate((0, SEG_L/2 + TONGUE, D2/2))
    tongue2 = cq.Workplane("XZ").rect(TW2, D2 - 2*TF2 - 2).extrude(TONGUE).translate((0, -SEG_L/2, D2/2))
    s = s.union(tongue).union(tongue2)
    # flange holes: 2 rows of 3 at each end, 32 mm pitch, rows at x +-15
    pts = []
    for ye in (SEG_L/2 - 16, -(SEG_L/2 - 16)):
        sgn = -1 if ye > 0 else 1
        for k in range(3):
            for x in (-18, 18):
                pts.append((x, ye + sgn*k*32))
    s = s.faces(">Z").workplane(origin=(0, 0, D2)).pushPoints(pts).hole(HOLE)
    s = s.faces("<Z").workplane(origin=(0, 0, 0)).pushPoints([(x, -y) for x, y in pts]).hole(HOLE)   # mirrored workplane
    # web holes: 2 columns x 3 rows in each tongue
    wpts = []
    for yc in (SEG_L/2 - 25, SEG_L/2 - 57, -(SEG_L/2 - 25), -(SEG_L/2 - 57)):
        for z in (D2/2 - 50, D2/2, D2/2 + 50):
            wpts.append((yc, z))
    s = s.faces(">X").workplane(origin=(TW2/2, 0, 0)).pushPoints([(-y, z) for y, z in wpts]).hole(HOLE)
    return s

# ---------- P-02 star plate ----------
ARM_W, PLATE_T, ARM_R = 60.0, 12.0, 175.0
def star_plate():
    s = None
    for i in range(6):
        a = math.radians(60*i)
        arm = cq.Workplane("XY").rect(ARM_R, ARM_W).extrude(PLATE_T).translate((ARM_R/2, 0, 0)).rotate((0,0,0), (0,0,1), 60*i)
        s = arm if s is None else s.union(arm)
    s = s.union(cq.Workplane("XY").polygon(6, CORE/math.cos(math.radians(30)) + 4).extrude(PLATE_T))
    pts = []
    for i in range(6):
        a = math.radians(60*i)
        for k in range(3):
            r = CORE/2 + GAP + 16 + k*32
            for off in (-18, 18):
                pts.append((r*math.cos(a) - off*math.sin(a), r*math.sin(a) + off*math.cos(a)))
    s = s.faces(">Z").workplane().pushPoints(pts).hole(HOLE)
    return s

# ---------- P-03 web core ----------
CHEEK_T, FORK_L = 6.0, 90.0
def web_core():
    h = D2 - 2*TF2 - 2*PLATE_T - 2      # sits between the two star plates inside the section: 180-20-24-2 = 134
    core = cq.Workplane("XY").polygon(6, CORE/math.cos(math.radians(30))).extrude(h)
    for i in range(6):
        for side in (-1, 1):
            cheek = (cq.Workplane("XY").rect(FORK_L, CHEEK_T).extrude(h - 4)
                     .translate((CORE/2 - 10 + FORK_L/2, side*(TW2/2 + 0.1 + CHEEK_T/2), 2)).rotate((0,0,0), (0,0,1), 60*i))
            core = core.union(cheek)
    # the slot between the cheeks is open (the rib web tongue goes in); cut the core back so the tongue reaches 90 mm
    for i in range(6):
        slot = cq.Workplane("XY").rect(FORK_L + 20, TW2 + 0.2).extrude(h + 2).translate((CORE/2 - 8 + (FORK_L+20)/2, 0, -1)).rotate((0,0,0),(0,0,1),60*i)
        core = core.cut(slot)
    # fork holes: 2 columns x 3 rows, through both cheeks
    for i in range(6):
        for yc in (CORE/2 + GAP + 25, CORE/2 + GAP + 57):
            for z in (h/2 - 50, h/2, h/2 + 50):
                hole = cq.Workplane("XZ").center(yc, z).circle(HOLE/2).extrude(60, both=True).rotate((0,0,0),(0,0,1),60*i + 90)
                core = core.cut(hole)
    return core

# ---------- P-07 pressure pane ----------
PANE_SIDE, PANE_T, CORNER_CUT = 531.0, 21.0, 60.0   # 21 mm since 5 Nov 2026 (was 22)
def pane():
    r = PANE_SIDE / math.sqrt(3)
    tri = cq.Workplane("XY").polygon(3, 2*r).extrude(PANE_T)
    # truncate corners
    for i in range(3):
        cutter = cq.Workplane("XY").rect(200, 200).extrude(PANE_T + 2).translate((100 + r - CORNER_CUT*0.866, 0, -1)).rotate((0,0,0),(0,0,1), 120*i)
        tri = tri.cut(cutter)
    return tri.edges("|Z").chamfer(1.0)

# ---------- P-14 seam / splice bolt NAS6705 5/16-24 ----------
def bolt_5_16(grip=42.9):
    head = cq.Workplane("XY").polygon(6, 12.7/math.cos(math.radians(30))).extrude(4.9)
    shank = cq.Workplane("XY").circle(7.94/2).extrude(grip).translate((0, 0, 4.9))
    thread = cq.Workplane("XY").circle(7.94/2 - 0.3).extrude(12).translate((0, 0, 4.9 + grip))
    return head.union(shank).union(thread)

# ---------- P-04 main rib ----------
DM, BFM, TFM, TWM = 400.0, 100.0, 25.0, 8.0
LEDGE_W, LEDGE_T, SEAT_Z = 30.0, 10.0, 180.0
RIB_L = 2020.0
def main_rib(RIB_L=RIB_L):
    # one piece: outer flange, web, seat ledges
    prof = (cq.Workplane("XZ").moveTo(-BFM/2, 0).lineTo(BFM/2, 0).lineTo(BFM/2, TFM).lineTo(TWM/2, TFM)
            .lineTo(TWM/2, SEAT_Z - LEDGE_T).lineTo(TWM/2 + LEDGE_W, SEAT_Z - LEDGE_T).lineTo(TWM/2 + LEDGE_W, SEAT_Z).lineTo(TWM/2, SEAT_Z)
            .lineTo(TWM/2, DM).lineTo(-TWM/2, DM).lineTo(-TWM/2, SEAT_Z).lineTo(-TWM/2 - LEDGE_W, SEAT_Z).lineTo(-TWM/2 - LEDGE_W, SEAT_Z - LEDGE_T)
            .lineTo(-TWM/2, SEAT_Z - LEDGE_T).lineTo(-TWM/2, TFM).lineTo(-BFM/2, TFM).close())
    s = prof.extrude(RIB_L).translate((0, RIB_L/2, 0))
    # cap bolt holes 3/8 through the web at 90 mm pitch, 40 mm below the cabin face
    n = int(RIB_L // 90)
    pts = [(-(RIB_L/2) + 45 + k*90, DM - 40) for k in range(n)]
    s = s.faces(">X").workplane(origin=(TWM/2, 0, 0)).pushPoints([(-y, z) for y, z in pts]).hole(9.6)
    return s

def cap_angle(RIB_L=RIB_L):
    # one of the two angles: horizontal leg 46 x 25 (the inner flange), vertical leg 100 tall x 12 down the web
    prof = (cq.Workplane("XZ").moveTo(0, DM).lineTo(46 + 12, DM).lineTo(46 + 12, DM - 25).lineTo(12, DM - 25).lineTo(12, DM - 100).lineTo(0, DM - 100).close())
    s = prof.extrude(RIB_L).translate((0, RIB_L/2, 0))
    n = int(RIB_L // 90)
    pts = [(-(RIB_L/2) + 45 + k*90, DM - 40) for k in range(n)]
    s = s.faces(">X").workplane(origin=(12, 0, 0)).pushPoints([(-y, z) for y, z in pts]).hole(9.6)
    return s.translate((TWM/2, 0, 0))

# ---------- P-05 hub ----------
HUB_D = 160.0
def hub(n=6, a0=0.0):
    """n forks (6 hexagon, 5 pentagon), first fork at angle a0 (degrees)"""
    h = DM - 2*TFM - 2*25 - 2       # between two 25 mm star plates inside the section: 400-50-50-2 = 298
    step = 360.0 / n
    core = cq.Workplane("XY").circle(HUB_D/2).extrude(h)
    for i in range(n):
        for side in (-1, 1):
            cheek = (cq.Workplane("XY").rect(150, 10).extrude(h - 6).translate((HUB_D/2 - 20 + 75, side*(TWM/2 + 0.1 + 5), 3)).rotate((0,0,0),(0,0,1),a0 + step*i))
            core = core.union(cheek)
        slot = cq.Workplane("XY").rect(170, TWM + 0.2).extrude(h + 2).translate((HUB_D/2 - 20 + 85 - 10, 0, -1)).rotate((0,0,0),(0,0,1),a0 + step*i)
        core = core.cut(slot)
    for i in range(n):
        for yc in (HUB_D/2 + 30 + k*45 for k in range(2)):
            for z in (h/2 - 90, h/2 - 30, h/2 + 30, h/2 + 90):
                hole = cq.Workplane("XZ").center(yc, z).circle(13.0/2).extrude(80, both=True).rotate((0,0,0),(0,0,1),a0 + step*i + 90)
                core = core.cut(hole)
    return core

def hub_star_plate(n=6, a0=0.0):
    step = 360.0 / n
    s = cq.Workplane("XY").circle(HUB_D/2 + 10).extrude(25)
    for i in range(n):
        arm = cq.Workplane("XY").rect(330, 100).extrude(25).translate((165 + HUB_D/2 - 20, 0, 0)).rotate((0,0,0),(0,0,1),a0 + step*i)
        s = s.union(arm)
    pts = []
    for i in range(n):
        a = math.radians(a0 + step*i)
        for k in range(5):
            r = HUB_D/2 + 40 + k*52
            for off in (-30, 30):
                pts.append((r*math.cos(a) - off*math.sin(a), r*math.sin(a) + off*math.cos(a)))
    return s.faces(">Z").workplane().pushPoints(pts).hole(13.0)

# ---------- P-06 frame member ----------
FD, FWEB, FFL_W, FFL_T, LIP_W, LIP_T = 180.0, 20.0, 50.0, 10.0, 50.0, 10.0
FRAME_L = 2250.0
def frame_member(FRAME_L=FRAME_L):
    # web 20 thick, outer flange 50 x 10 toward the panel, lip 50 x 10 at the seat plane (z 170-180), both on the panel side
    web = cq.Workplane("XZ").rect(FWEB, FD).extrude(FRAME_L).translate((FWEB/2, FRAME_L/2, FD/2))
    fl = cq.Workplane("XZ").rect(FFL_W, FFL_T).extrude(FRAME_L).translate((-FFL_W/2, FRAME_L/2, FFL_T/2))
    lip = cq.Workplane("XZ").rect(LIP_W, LIP_T).extrude(FRAME_L).translate((-LIP_W/2, FRAME_L/2, FD - LIP_T/2))
    s = web.union(fl).union(lip)
    # seam bolt holes through the web, 5/16, at the Rev E pitch (two per 150 mm slice -> 75 mm), at mid-depth
    n = int(FRAME_L // 75)
    pts = [(-(FRAME_L/2) + 37.5 + k*75, FD/2) for k in range(n)]
    s = s.faces(">X").workplane(origin=(FWEB, 0, 0)).pushPoints([(-y, z) for y, z in pts]).hole(8.03)
    return s

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["all"]
    def want(k): return "all" in which or k in which
    if want("P-01"): register("P-01", "Secondary rib segment, I 180 x 60 x 10, web 5", rib_segment(), "6061-T6",
        "Custom extrusion, 468.5 mm between flange ends, the web 10 mm longer at each end to bear in the node core slot. The node fork cheeks slide inside the section beside the web over the last 78 mm. 12 flange holes (two rows of three at 32 mm, rows 36 mm apart) and 6 web holes per end, 8.03 mm reamed for 5/16-24 A286 close-tolerance bolts. Inner-flange holes countersunk at the seat face (z 180).",
        dict(depth=180, flange_width=60, flange_t=10, web_t=5, length_flange_to_flange=SEG_L, web_overhang=TONGUE, pitch_between_nodes=PITCH, bolt="5/16-24 NAS6705 family"))
    if want("P-02"): register("P-02", "Node star plate, 12 mm", star_plate(), "7075-T7351",
        "Two per node: one on the space side over the outer flanges, one inside the section under the inner flanges. Six arms 60 wide, 175 mm from the node centre. 6 holes per arm in two rows of 3 at 32 mm pitch.",
        dict(arms=6, arm_width=60, arm_reach_from_centre=ARM_R, thickness=PLATE_T, holes_per_arm=6, hole=HOLE))
    if want("P-03"): register("P-03", "Node web core, six forks", web_core(), "7075-T7351",
        "Machined hexagonal core 90 mm across flats with six forks: 6 mm cheeks 90 mm long, 134 mm tall, with a 5.2 mm slot for the rib web. The cheeks sit inside the rib section between its flanges. 6 holes per fork, two columns of three, through both cheeks (double shear).",
        dict(core_across_flats=CORE, fork_length=FORK_L, cheek_t=CHEEK_T, slot=TW2+0.2, height=D2-2*TF2-2*PLATE_T-2, holes_per_fork=6, hole=HOLE))
    if want("P-07"): register("P-07", "Pressure pane L7, 531 mm, 21 mm BOROFLOAT 33", pane(), "BOROFLOAT 33",
        "Equilateral 531 mm (k 4 cut, 9.09 mm short of each rib centre line). Corners truncated 60 mm for the node star plates and clamp screws. Edges ground and polished, 1 mm chamfers. Rests on the cabin face of the secondary rib inner flanges; pressure seats it.",
        dict(side=PANE_SIDE, thickness=PANE_T, corner_cut=CORNER_CUT, bite_on_60mm_flange=20.9), source="Rev E restack (24 Oct), rib study (2 Nov)")
    if want("P-14"): register("P-14", "Bolt 5/16-24 A286, NAS6705 family", bolt_5_16(), "A286",
        "The seam bolt (NAS6705U27, grip 42.9 mm) and the node splice bolts (shorter grips) are the same family. Close tolerance shank in reamed holes.",
        dict(diameter=7.94, grip_seam=42.9, head_across_flats=12.7), source="Third seal, seam bolt (24 Oct)")
    if want("P-04"): register("P-04", "Main rib, I 400 x 100 x 25, web 8, one piece with seat ledges", main_rib(), "6061-T6",
        "Outer flange 100 x 25, web 8, seat ledges 30 mm each side at the seat plane z 170-180. The inner flange is the two bolted angles P-04A. 3/8-24 cap bolt holes through the web at 90 mm pitch, 40 mm below the cabin face. Length 2020 mm between hub and corner block (schematic ends).",
        dict(depth=DM, flange_width=BFM, flange_t=TFM, web_t=TWM, ledge_reach=LEDGE_W, ledge_t=LEDGE_T, seat_plane=SEAT_Z, cap_bolt="3/8-24 A286 at 90 mm", length=RIB_L), source="Rev E restack (24 Oct), rib study (2 Nov)")
    if want("P-04A"): register("P-04A", "Main rib cap angle (one of two)", cap_angle(), "6061-T6",
        "Two angles make the inner flange: horizontal leg 46 x 25 each (with the 8 mm web, 100 mm wide), vertical leg 100 x 12 down the web. Bolted horizontally through the web, 3/8-24 A286 close-tolerance in reamed holes, 90 mm pitch, after the glass is in.",
        dict(horizontal_leg=46, flange_t=25, vertical_leg=100, vertical_t=12, length=RIB_L))
    if want("P-05"): register("P-05", "Hub web core, six forks", hub(), "2219-T852",
        "160 mm core with six forks for the 8 mm main rib webs, 10 mm cheeks 150 long, 8 holes per fork (13 mm for 1/2-20 A286). Sits between the two hub star plates P-05A.",
        dict(core_d=HUB_D, fork_length=150, cheek_t=10, holes_per_fork=8, hole=13.0))
    if want("P-05A"): register("P-05A", "Hub star plate, 25 mm", hub_star_plate(), "2219-T852",
        "Two per hub, outer and inner. Six arms 100 wide, 25 thick, 10 holes per arm (13 mm, 1/2-20 A286). Carries each main rib's flange force straight across to the opposite rib.",
        dict(arms=6, arm_width=100, thickness=25, holes_per_arm=10, hole=13.0))
    if want("P-06"): register("P-06", "Frame member, 180 deep", frame_member(), "6061-T6",
        "Web 20, outer flange 50 x 10 and seat lip 50 x 10 at z 170-180 (moved to the cabin face for the restack). Seam bolt holes 8.03 mm at 75 mm pitch at mid-depth (two per 150 mm D1 slice). Straight schematic: the real member's web leans 20.9 degrees to the joint plane.",
        dict(depth=FD, web_t=FWEB, flange=f"{FFL_W} x {FFL_T}", lip=f"{LIP_W} x {LIP_T}", seam_bolt_pitch=75, length=FRAME_L), source="Rev E sizing (24 Oct)")
    json.dump(PARTS, open(f"{OUT}/parts.json", "w"), indent=1)
