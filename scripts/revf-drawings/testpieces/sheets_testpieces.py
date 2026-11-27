"""Drawing sheets for the HCSA test pieces at Rev F (180 mm frame): TP-00 to TP-04, issue of 27 Nov 2026.

First drawn 8 Nov 2026 and corrected 9 Nov; laid out again on 27 Nov with the shared sheet style (src/drawing_kit.py). Drawn
from the same parameters as build_testpieces.py (read back from out/testpieces.json), with the CadQuery views embedded.
Run build_testpieces.py first. The STEP files govern the geometry; where a sheet and a solid differed, the sheet was
corrected to the solid. Clashes found in the solids on 27 Nov are marked CHECK and are not changed here.
"""
import json, math, os, subprocess, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Wedge, Ellipse
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import drawing_kit as K
from drawing_kit import dim, leader, label, note, heading, table, view, cl, MET, MET2, MET3, STEEL, SEAL, RED, BLU, ORG, GRN, GREY

PARTS_SVG = os.path.normpath(os.path.join(HERE, "..", "..", "..", "public", "parts", "svg"))   # F-01 to F-03 views (parts library)
T = json.load(open(f"{OUT}/testpieces.json")); PR = T["parameters"]
D, WEB, FLT, LEG = PR["D"], PR["WEB"], PR["FL_T"], PR["LEG"]
GW, GD, Z1, Z2, ZR, ZP, ZB = PR["GW"], PR["GD"], PR["Z_G1"], PR["Z_G2"], PR["Z_RTV"], PR["Z_PORT"], PR["Z_BOLT"]
BX = PR["BLK_X"]; BZ0, BZ1 = PR["BLK_Z"]; HP = PR["HP"]
LUG_Z = (42.0, 74.0); M12_DEPTH = 31.0
ORDER = ["RF-00", "RF-01", "RF-02", "RF-03", "RF-04", "RF-05", "RF-06", "RF-07", "RF-08", "RF-09", "TP-00", "TP-01", "TP-02", "TP-03", "TP-04"]
of = lambda no: f"{ORDER.index(no) + 1} of {len(ORDER)}"
BANNER = "FOR QUOTATION. NOT FOR MACHINING UNTIL CHECKED"
MAT_FRAME = "6061-T651 plate (frames); 4140 QT 28-32 HRC (blocks)"
FIN = "Joint face and glands Ra 0.8; elsewhere Ra 3.2"
TOL = "General tolerances ISO 2768-m unless stated (proposal on TP-00). To be confirmed with the shop."


def png(name, src_dir=None, width=1100):
    svg = os.path.join(src_dir or f"{OUT}/svg", f"{name}.svg"); out = f"{OUT}/svg/{name}.png"
    if not os.path.exists(out):
        subprocess.run(["rsvg-convert", "-w", str(width), "-b", "white", svg, "-o", out], check=True)
    return mpimg.imread(out)


def sheet(no, title, status, part, scale, material=MAT_FRAME, finish=FIN):
    return K.new_sheet(no, title, status=status, part=part, material=material, finish=finish, scale=scale, banner=BANNER, banner_col=ORG,
                       sheet_of=of(no), tol=TOL)


def image(fig, rect, img, title):
    x, y, w, h = rect
    ax = fig.add_axes([x / K.A3[0], y / K.A3[1], w / K.A3[0], h / K.A3[1]]); ax.axis("off"); ax.imshow(img)
    fig.text(x / K.A3[0], (y + h + 1.0) / K.A3[1], title, fontsize=8, weight="bold", va="bottom")
    return ax


def bolt_ys(L, hardpoint):
    pitch = PR["PITCH"]
    if hardpoint:
        bay = L / 2 - HP["W"] / 2; n = int((bay - 60) // pitch) + 1; f0 = (bay - (n - 1) * pitch) / 2
        return sorted([f0 + i * pitch for i in range(n)] + [L - f0 - i * pitch for i in range(n)])
    nb = int(round(L / pitch)); return [L / 2 + (i - (nb - 1) / 2) * pitch for i in range(nb)]


def leg_ys(L):
    if L == 75: return {"inner": [18.75, 56.25], "outer": [16.5, 58.5]}
    n = int(L // 75); ys = [L / 2 + (i - (n - 1) / 2) * 75 for i in range(n)]; return {"inner": ys, "outer": ys}


def rect(ax, x, y, w, h, fc, ec="k", lw=0.7, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, **kw))


# leg-hole rows across the leg (from build_testpieces.leg_rows_x): block at the leg end, rows 20 mm in from its edges
ROW_OUT = WEB + LEG - 20.0          # 200 from the joint face (180 from the web's back face)
ROW_IN = WEB + LEG - BX + 20.0      # 160 from the joint face (140 from the web's back face)

CHECKS = [
    "CHECK 1 (found 27 Nov, in the solids): on the 75 and 150 pull blocks the M12 lug-plate holes of the z 42 row (from the pull face, drilled 20 deep) "
    "break into the outer-row M12 leg-screw holes (from the flange-side bearing face, 31 deep): 157 mm³ (75 block) and 34 mm³ (150 block) of common volume. "
    "The 225 and 550 blocks are clear. Move the lug rows, shorten the leg-screw holes or move the leg holes before quoting: a decision, not changed here.",
    "CHECK 2: F-01 has 12 mm deep Ø20 counterbores over 8 mm of plate, so an M12 x 45 screw reaches about 37 mm into the block, whose lug holes are drilled 20 deep; "
    "and an ISO 7089 M12 washer (Ø24) does not fit a Ø20 counterbore. Choose the screw length (about M12 x 25) or the hole depth, and drop the washers there.",
    "CHECK 3: the F-01 pin hole is 24 mm from the plate's lower edge in the STEP (14 mm of steel below the Ø20 hole); RE-03 rev B said 40 (2d), and the 720 kN tear-out check assumed 30 mm. "
    "Still ample for a 50 kN fixture load, but the check should be redone on the STEP.",
]


# ---------------- TP-00 cover: sheets, notes, tolerances, parts list ----------------
def tp00(pdf):
    fig, Pp = sheet("TP-00", "Test pieces: cover, notes, tolerances, parts list", "For quotation. Tolerances and DFM items are proposals for Marco (17 Nov); three CHECK items to settle before quoting.",
                    "T1 slices, SA-550 article, pull blocks, F-01 to F-03", "No views")
    x0, y = 14.0, 282.0
    Pp.text(x0, y, "HCSA test pieces, Rev F (180 mm frame)", fontsize=14, weight="bold", va="top")
    y = note(Pp, x0, y - 8, 200, "The T1 seam slices (75, 150, 225 mm), the 550 mm seal article with its grip legs and dummy hardpoint, and the pull blocks, all at the 180 mm frame. "
             "First issued 8 Nov 2026, solids rebuilt 9 Nov, sheets reissued 27 Nov. Drawn from hcsa_params_revF.json. What changed from the 24 Oct Rev E draft: frame depth 140 to 180, glands 7.1 x 4.0, "
             "seam bolt NAS6705U27 at 4 kN, pull blocks 160 tall to span the legs, run 2 pulled through pinned lugs (RE-03 rev B), the 550 article with legs and a dummy hardpoint (2 + 2 bolts).", fs=8) - 3
    y = heading(Pp, x0, y, "Sheets")
    y = table(Pp, x0, y, (18, 182), [("Sheet", "Contents"), ("TP-00", "Cover: sheets, general notes, tolerances, parts list, CHECK items"),
                                     ("TP-01", "T1 frame B (glands): section 1:2, joint face of the 150, leg holes; 75 / 150 / 225 table"),
                                     ("TP-02", "T1 frame A and the slice as assembled, the two pull lines, screws, lug plate F-01"),
                                     ("TP-03", "550 mm seal article with legs and the dummy hardpoint: the moved one to make, the first one for comparison"),
                                     ("TP-04", "Pull blocks (rev B interface) and the lug, fork and pin F-01 to F-03"),
                                     ("STEP", "HCSA-Rev-F-test-pieces-STEP-9-Nov-2026.zip: one STEP per part (out/step) and one assembly per article (out/asm)")], fs=7.5) - 4
    y = heading(Pp, x0, y, "General notes")
    notes = ("1. Material: frames 6061-T651 plate (keeps the FEA twins valid). Pull blocks 4140 quenched and tempered, 28-32 HRC. DFM option for Marco: blocks in 6061-T651 (one material, 65 % lighter: 19 kg instead of 55 kg each on the 550 article).\n"
             "2. Machining order for the frames: rough, rest 24 h, finish; the joint face is the last cut (fly-cut), so the part is flat once the stress is out. The joint face is the datum for every dimension across the frame.\n"
             "3. Inside corners web-to-flange and web-to-lip R6. Every hole 1 x 45° at both ends. Other edges 0.5 mm break. Gland edges deburred only, no break.\n"
             "4. Surface finish: joint face and gland faces Ra 0.8 µm; elsewhere Ra 3.2.\n"
             "5. Hardware (McMaster-Carr or equal): ISO 4762 M12 x 35 class 12.9 socket head cap screws with ISO 7089 hardened washers through the legs into the blocks; "
             "lug-plate screws ISO 4762 M12 class 12.9, length to suit (CHECK 2: M12 x 45 is too long for the 20 mm holes), no washers in the Ø20 counterbores; "
             "seam bolts in the test pieces: McMaster-Carr 5/16-24 alloy steel bolts and nuts as stand-ins (Marco, 7-9 Nov), two hardened washers each; the flight part is NAS6705U27 with a KFN670 nut, A286.\n"
             "6. Seals: Parker BA500-70 butyl cord 0.210 in (5.33 mm), two per article; RTV566 bead with SS4155 primer. End dams on the slices (M8 rod, fabrication plan 2.3).\n"
             "7. Quantities: one of each slice (75, 150, 225) and one 550 article, the moved version (SA-550-HPmoved): 8 frames, 8 blocks. Fixture parts F-01 to F-03 are shared: 2 lugs, 2 forks, 2 pins + 1 spare each.\n"
             "8. All sizes at 20 °C. 7 °C of difference moves 550 mm of aluminium by 0.09 mm (23.6e-6 per K), so the long parts are measured at 20 °C (Marco, 7 Nov).")
    note(Pp, x0, y, 200, notes, fs=7.5)
    # tolerance table
    xr = 222.0; y = heading(Pp, xr, 282, "Tolerances: tight only where the seal or a fit needs it (proposal for Marco)")
    tol = [("Feature", "Drawn 24 Oct", "Proposed", "Why"),
           ("Joint face flatness", "0.05 over the length", "0.10 per 150 mm, 0.15 over 550", "0.1 mm of gap moves the squeeze 2 points of 25 %"),
           ("Joint face finish", "Ra 0.8", "Ra 0.8 (keep)", "Parker face-seal finish"),
           ("Gland depth 4.0", "±0.05", "±0.05 (keep)", "sets the 25 % squeeze"),
           ("Gland width 7.1", "±0.05", "±0.10", "fill 78.7 % moves 1 point per 0.1 mm"),
           ("Gland position z 18, 32", "±0.05", "±0.15", "the cords only have to meet frame A's flat face"),
           ("Seam bolt holes", "8.4 reamed", "Ø8.5 drilled, position ±0.2", "a clamp bolt, not a shear pin, in the tests"),
           ("Leg holes", "13.5", "Ø14.0 drilled, pattern ±0.2", "M12 screws need play to find the block threads"),
           ("Hardpoint bores (550)", "Ø40 H7", "Ø40 +0.10 / 0", "the dummy pins are fitted loose"),
           ("Block bearing faces", "parallel 0.05", "parallel 0.10, height 160 ±0.1", "the legs must not be sprung by the screws"),
           ("Everything else", "ISO 2768-f", "ISO 2768-m", "nothing seals on legs, lengths, block outline")]
    y = table(Pp, xr, y, (36, 30, 46, 72), tol, fs=7.5, ls=1.1, pad=0.6) - 3
    y = heading(Pp, xr, y, "CHECK before quoting (found 27 Nov)", color=RED)
    note(Pp, xr, y, 184, "\n".join(CHECKS), fs=7.5, color=RED)
    # parts list (bottom left, above the title block's height on the left)
    rows = []
    for a in T["articles"]:
        if "DFM" in a["name"] or a["name"] == "SA-550":
            continue
        L = a["L"]
        for b in a["bom"]:
            blank = f"190 x 230 x {L+6}" if b["id"].endswith(("FB", "FA")) else f"165 x 85 x {L+6}"
            rows.append((b["id"], b["desc"].replace("Frame B (glands, RTV recess, leak port)", "Frame B, glands, RTV recess, leak port").replace(", M12 from both bearing faces, M24 run 1, lug rows run 2", ""),
                         b["material"], str(b["qty"]), f"{b['mass_kg']:.2f}", blank))
    rows += [("F-01", "Lug plate 80 x 100 x 20 (RE-03 rev B)", "4140 QT", "2", "1.05", "parts library STEP"),
             ("F-02", "Fork with M24 x 3 for the Instron adapter", "4140 QT", "2", "1.80", "parts library STEP"),
             ("F-03", "Pin 20 h6 x 70 with shoulder and E-clip groove", "17-4PH H900 or 4140 QT", "2", "0.20", "parts library STEP")]
    Pp.text(x0, 103, "Parts list (masses from the solids). SA-550 = the moved version, SA-550-HPmoved, bores at z 76 (the first version, bores at z 140, is not made).",
            fontsize=7.5, weight="bold", va="top")
    table(Pp, x0, 98.5, (32, 98, 30, 8, 16, 26), [("Part", "Description", "Material", "Qty", "kg each", "Stock blank")] + rows, fs=7.5, ls=1.0, pad=0.45)
    K.save(fig, pdf, f"{OUT}/TP-00_cover.png")


# ---------------- TP-01 frame B ----------------
def tp01(pdf):
    fig, Pp = sheet("TP-01", "T1 frame B (glands), 180 deep: section, joint face, legs", "For quotation. Geometry from build_testpieces.py; 75 / 150 / 225 in one table. The joint face is the datum.",
                    "T1-075-FB, T1-150-FB, T1-225-FB", "1:2", material="6061-T651 plate")
    ax = view(fig, (14, 112, 196, 156), 2.0, (-118, 88), title="Section G-G through a bolt station, looking along the seam; space side (z 0) at the bottom  (1:2)")
    rect(ax, -WEB, 0, WEB, D, MET2)
    rect(ax, -(WEB + LEG), 0, LEG, FLT, MET2); rect(ax, -(WEB + LEG), D - FLT, LEG, FLT, MET2)
    for zz, sg in ((FLT, 1), (D - FLT, -1)):
        cx, cy = -WEB - 6, zz + sg * 6
        ax.add_patch(Rectangle((-WEB - 6, min(zz, zz + sg * 6)), 6, 6, fc=MET2, ec="none"))
        ax.add_patch(Wedge((cx, cy), 6, 0, 360, fc="white", ec="none"))
        ax.add_patch(Arc((cx, cy), 12, 12, theta1=0 if sg > 0 else 270, theta2=90 if sg > 0 else 360, lw=0.7, color="k"))
    for zc in (Z1, Z2):
        rect(ax, -GD, zc - GW / 2, GD, GW, "white", lw=0.5); ax.add_patch(Ellipse((-GD / 2, zc), 4.0, 6.6, fc=SEAL, ec="none"))
    ax.add_patch(Wedge((0, ZR), 3.0, 90, 270, fc="white", ec="k", lw=0.6))
    rect(ax, -WEB, ZP - 1, WEB, 2, "white", lw=0.4); rect(ax, -WEB, ZP - 2.1, 8, 4.2, "white", lw=0.4)
    rect(ax, -WEB, ZB - 4.25, WEB, 8.5, "white", lw=0.5)
    bx0 = -(WEB + LEG); ax.add_patch(Rectangle((bx0, BZ0), BX, BZ1 - BZ0, fill=False, ec=STEEL, lw=0.8, ls="--"))
    for xr_ in (-ROW_OUT, -ROW_IN):
        rect(ax, xr_ - 7.0, 0, 14.0, FLT, "white", lw=0.5); rect(ax, xr_ - 7.0, D - FLT, 14.0, FLT, "white", lw=0.5)
        cl(ax, (xr_, -6), (xr_, FLT + 6)); cl(ax, (xr_, D - FLT - 6), (xr_, D + 6))
    ax.plot([0, 0], [-12, D + 12], ls=(0, (9, 2, 1.5, 2)), lw=0.5, c=RED)
    dim(ax, (-WEB, D), (0, D), f"{WEB:g}", off=8)
    dim(ax, (-(WEB + LEG), D), (0, D), f"{WEB + LEG:g} (DFM option: 140)", off=16)
    dim(ax, (-ROW_IN, 0), (0, 0), f"{ROW_IN:g}", off=-8)
    dim(ax, (-ROW_OUT, 0), (0, 0), f"{ROW_OUT:g}", off=-15)
    dim(ax, (bx0, BZ1), (bx0 + BX, BZ1), f"block {BX:g}", off=-6, col=STEEL)
    dim(ax, (0, 0), (0, D), f"{D:g}", off=26)
    for i, (zz, t) in enumerate(((Z1, Z1), (Z2, Z2), (ZB, ZB))):
        dim(ax, (0, 0), (0, zz), f"{t:g}", off=8 + 6 * i, fs=7.5)
    dim(ax, (-(WEB + LEG), 0), (-(WEB + LEG), FLT), f"{FLT:g}", off=-5, inside=False)
    leader(ax, (-WEB + 2, ZB), (-150, 74), "seam bolt holes Ø8.5 drilled,\n75 pitch, centred, z 58", fs=7.5, ha="left")
    leader(ax, (-WEB + 3, ZP), (-150, 48), "leak port Ø2 through, M5 x 8 deep\nfrom the leg side, one per slice\nat mid-length, z 25", fs=7.5, ha="left")
    leader(ax, (-GD, Z1), (-150, 22), f"2 glands {GW:g} x {GD:g}, bottom R0.5-0.9,\nrun through, dammed at the ends;\nRTV recess R3 at z {ZR:g}", fs=7.5, ha="left")
    leader(ax, (-WEB - 2.5, D - FLT - 2.5), (-150, 150), "inside corners R6 (both)", fs=7.5, ha="left")
    leader(ax, (-ROW_IN - 5, 2), (-150, -48), "leg holes Ø14 drilled, 2 rows, through both legs; the block threads match (TP-04)", fs=7.5, ha="left")
    label(ax, (12, D / 2), "joint face\n(datum)", col=RED, fs=7.5, ha="left", bg=False)
    label(ax, (-(WEB + LEG), D + 50), "the seat lip (z 170-180) is the second grip leg", fs=7.5, ha="left", bg=False, col=GREY)
    # joint face of the 150
    L = 150
    ax2 = view(fig, (226, 158, 110, 110), 2.0, (75, 90), title="Joint face of the 150 slice, frame B; space side at the bottom  (1:2)")
    rect(ax2, 0, 0, L, D, MET2)
    for zc in (Z1, Z2): rect(ax2, 0, zc - GW / 2, L, GW, "white", lw=0.4); ax2.plot([0, L], [zc, zc], c=SEAL, lw=1.4)
    ax2.plot([0, L], [ZR, ZR], c="k", lw=0.5, ls=":")
    for yb in bolt_ys(L, False): ax2.add_patch(Circle((yb, ZB), 4.25, fc="white", ec="k", lw=0.6))
    ax2.add_patch(Circle((L / 2, ZP), 1.0, fc="white", ec="k", lw=0.5))
    dim(ax2, (0, D), (L, D), f"{L}", off=6)
    dim(ax2, (0, ZB), (bolt_ys(L, False)[0], ZB), "37.5", off=12, fs=7.5)
    dim(ax2, (bolt_ys(L, False)[0], ZB), (bolt_ys(L, False)[1], ZB), "75", off=12, fs=7.5)
    dim(ax2, (L, 0), (L, D), f"{D:g}", off=6, fs=7.5)
    leader(ax2, (L / 2, ZP - 1), (L / 2 + 10, -10), "leak port Ø2, mid-length, z 25", fs=7.5, ha="left")
    # table
    y = heading(Pp, 226, 150, "Holes by slice: seam bolts and leg holes along the seam, from the slice end")
    tab = [("Slice", "Seam bolts", "Leg holes, inner row\n(160 from the joint face)", "Leg holes, outer row\n(200 from the joint face)", "Threads per block face"),
           ("75", "37.5", "18.75, 56.25", "16.5, 58.5 (OPEN-6)", "4"),
           ("150", "37.5, 112.5", "37.5, 112.5", "37.5, 112.5", "4"),
           ("225", "37.5, 112.5, 187.5", "37.5, 112.5, 187.5", "37.5, 112.5, 187.5", "6"),
           ("550 (TP-03)", "50, 125, 425, 500", "7 at 75 pitch, 50 to 500", "the same", "14")]
    y = table(Pp, 226, y, (20, 32, 42, 42, 44), tab, fs=7.5) - 3
    note(Pp, 226, y, 180, "Frame A (TP-02) is the mirror image without the glands, the RTV recess and the port. Stock 6061-T651 plate 190 x 230 x (L + 6); with the DFM 120 legs, 190 x 150 x (L + 6). "
         "The slice is flat, so z equals the joint-plane coordinate z' of the flight frame: the test measures the same joint face the station has.\n"
         "Corrected 27 Nov: the leg-hole rows are dimensioned from the joint face, 160 and 200 (the table said 140 and 180, which are from the web's back face). "
         "The section is drawn at 1:2; it said 1:1.", fs=7.5)
    image(fig, (14, 18, 120, 82), png("T1-150-FB_iso"), "T1-150-FB from the STEP (legs toward the viewer, joint face at the back)")
    K.save(fig, pdf, f"{OUT}/TP-01_frame_B.png")


# ---------------- TP-02 frame A and the slice assembled ----------------
def tp02(pdf):
    fig, Pp = sheet("TP-02", "T1 frame A and the slice as assembled, pull lines, screws", "For quotation. Block 160 tall; run 1 M24 at z 90; run 2 through the lugs at z 24 (RE-03 rev B).",
                    "T1-150-FA, T1-150-PB (x2), F-01 (x2); slice assembly", "1:2")
    ax = view(fig, (14, 120, 268, 150), 2.0, (0, 92), title="Section H-H through a bolt station: frame B (left, glands), frame A (right), pull blocks, lug plates F-01 (phantom); space side at the bottom  (1:2)")
    def frame_side(sgn, col, grooved):
        rect(ax, 0 if sgn > 0 else -WEB, 0, WEB, D, col)
        rect(ax, WEB if sgn > 0 else -(WEB + LEG), 0, LEG, FLT, col)
        rect(ax, WEB if sgn > 0 else -(WEB + LEG), D - FLT, LEG, FLT, col)
        bx0 = WEB + LEG - BX if sgn > 0 else -(WEB + LEG)
        rect(ax, bx0, BZ0, BX, BZ1 - BZ0, STEEL)
        for xr_ in (bx0 + 20, bx0 + BX - 20):
            for z0, z1 in ((0, FLT + 31), (D - FLT - 31, D)):
                rect(ax, xr_ - 5.1, z0, 10.2, z1 - z0, "white", lw=0.4)
            rect(ax, xr_ - 9, D, 18, 2.5, "#666", lw=0.4); rect(ax, xr_ - 9, -2.5, 18, 2.5, "#666", lw=0.4)
        zc = (BZ0 + BZ1) / 2
        rect(ax, bx0 if sgn < 0 else bx0 + BX - 40, zc - 10.5, 40, 21, "white", lw=0.5)
        for z in LUG_Z: rect(ax, bx0 if sgn < 0 else bx0 + BX - 20, z - 5.1, 20, 10.2, "white", lw=0.4)
        xo = -(WEB + LEG) - 20 if sgn < 0 else WEB + LEG                     # F-01, 20 thick, z 0-100, pin at z 24
        ax.add_patch(Rectangle((xo, 0), 20, 100, fill=False, ec=ORG, lw=0.8, ls="--"))
        ax.add_patch(Circle((xo + 10, 24), 10, fill=False, ec=ORG, lw=0.7, ls="--"))
        if grooved:
            for zz in (Z1, Z2): rect(ax, -GD, zz - GW / 2, GD, GW, "white", lw=0.5); ax.add_patch(Ellipse((-GD / 2, zz), 4.0, 6.6, fc=SEAL, ec="none"))
            ax.add_patch(Wedge((0, ZR), 3.0, 90, 270, fc="#7a5", ec="k", lw=0.4))
    frame_side(-1, MET2, True); frame_side(1, MET3, False)
    rect(ax, -WEB - 3.2, ZB - 3.97, 2 * WEB + 6.4, 7.94, "#555", lw=0.5)
    rect(ax, -WEB - 4.9 - 1.6, ZB - 6.3, 4.9, 12.7, "#777", lw=0.5); rect(ax, WEB + 1.6, ZB - 6.3, 6.8, 12.7, "#777", lw=0.5)
    for z, lab, c in ((90, "run 1: straight pull, M24 x 3 at the block centre, z 90", BLU), (24, "run 2: prying pull at z 24 through the lug plate, fork and pin (RE-03 rev B)", ORG)):
        ax.annotate("", (-(WEB + LEG) - 28, z), (WEB + LEG + 28, z), arrowprops=dict(arrowstyle="<|-|>", lw=1.2, color=c, mutation_scale=8))
        label(ax, (0, z + 7), lab, col=c, fs=7.5)
    ax.plot([0, 0], [-10, D + 10], ls=(0, (9, 2, 1.5, 2)), lw=0.5, c=RED)
    dim(ax, (-(WEB + LEG), D), (WEB + LEG, D), f"{2*(WEB+LEG):g} over the legs", off=10)
    dim(ax, (-(WEB + LEG), BZ0), (-(WEB + LEG), BZ1), f"block {BZ1-BZ0:g}", off=-15)
    dim(ax, (WEB + LEG + 20, 0), (WEB + LEG + 20, 24), "z 24", off=4, fs=7.5, inside=False)
    label(ax, (WEB + LEG + 10, 108), "F-01", col=ORG, fs=7.5, bg=False); label(ax, (-(WEB + LEG) - 10, 108), "F-01", col=ORG, fs=7.5, bg=False)
    note(Pp, 14, 113, 268, "M12 x 35 class 12.9 screws with hardened washers through the Ø14 leg holes into the block threads (4 to 14 per face). The screws carry the pull in shear; "
         "the washers keep the head pressure on the 6061 leg under 132 MPa (RE-01-2 check). The lug plates F-01 screw to the pull faces on the z 42 and z 74 rows (see CHECK 2 on TP-00 for their screw length).", fs=7.5)
    image(fig, (292, 196, 110, 72), png("T1-150-FA_iso"), "T1-150-FA (flat joint face), from the STEP")
    image(fig, (300, 110, 95, 72), png("T1-150-PB_iso"), "Pull block, 160 x 80 x 150 (TP-04)")
    nt = ("Why the block grew. On the 140 frame the block spanned the flange and the lip, 83 mm apart. On the 180 frame the lip is at the cabin face (z 170-180, P-06), so the span is 160 mm. "
          "The single M24 for run 1 sits at the block centre, which puts the straight pull at z 90; the D1 and HP1 twins pull at the frame middle (76 mm), so run 1's pull line is 14 mm off the twins'. "
          "Run 2 (the one the seal design turns on) is unchanged at z 24. The thin walls round the two M24 threads of the 24 Oct blocks are gone: rev B has one M24 and the z 24 pull goes through the lugs.\n"
          "DFM questions for Marco: blocks in 6061-T651 instead of 4140 (19 kg instead of 55 kg for each 550 block; the M12 and M24 threads in aluminium carry the 100 kN frame load with margin); "
          "legs 120 instead of 200 (stock 190 x 150 instead of 190 x 230; the block moves in; the twins' fixture legs change).")
    note(Pp, 14, 96, 206, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/TP-02_assembled.png")


# ---------------- TP-03 the 550 article ----------------
def tp03(pdf):
    fig, Pp = sheet("TP-03", "550 mm seal article with legs and the dummy hardpoint", "For quotation. Make the moved version, bores at z 76 (fitting on the pull line, agreed 10 Nov); the first version is shown for comparison only.",
                    "SA-550-HPmoved-FB, -FA, -PB (x2)", "1:2; comparison view 1:5")
    L = 550
    def face(ax, hz, col):
        rect(ax, 0, 0, L, D, MET2, lw=0.8)
        for zc in (Z1, Z2): ax.plot([0, L], [zc, zc], c=SEAL, lw=1.3)
        ax.plot([0, L], [ZR, ZR], c="k", lw=0.5, ls=":")
        ax.add_patch(Rectangle((L / 2 - HP["W"] / 2, hz - 30), HP["W"], 60, fill=False, ec=col, lw=0.9, ls="--"))
        for j in (-1, 0, 1): ax.add_patch(Circle((L / 2 + j * HP["pitch"], hz), HP["pin"] / 2, fc="white", ec="k", lw=0.7))
        for yb in bolt_ys(L, True): ax.add_patch(Circle((yb, ZB), 4.25, fc="white", ec="k", lw=0.6))
        ax.add_patch(Circle((L / 2, ZP), 1.0, fc="white", ec="k", lw=0.5))
    ax = view(fig, (14, 142, 292, 124), 2.0, (283, 85), title="SA-550-HPmoved, joint face of frame B, dummy fitting on the pull line (bores at z 76, envelope z 46 to 106); space side at the bottom  (1:2)")
    face(ax, HP["z_moved"], GRN)
    bl = bolt_ys(L, True)
    dim(ax, (0, D), (L, D), f"{L}", off=6)
    dim(ax, (0, ZB), (bl[0], ZB), f"{bl[0]:g}", off=-14, fs=7.5); dim(ax, (bl[0], ZB), (bl[1], ZB), "75", off=-14, fs=7.5)
    dim(ax, (bl[1], ZB), (L / 2 - HP["W"] / 2, ZB), f"{L/2 - HP['W']/2 - bl[1]:g}", off=-14, fs=7.5)
    dim(ax, (L / 2 - HP["pitch"], HP["z_moved"]), (L / 2, HP["z_moved"]), "60", off=27, fs=7.5)
    dim(ax, (L / 2, HP["z_moved"]), (L / 2 + HP["pitch"], HP["z_moved"]), "60", off=27, fs=7.5)
    dim(ax, (L / 2 - HP["W"] / 2, HP["z_moved"] + 30), (L / 2 + HP["W"] / 2, HP["z_moved"] + 30), "fitting envelope 200", off=6, fs=7.5, col=GRN)
    dim(ax, (L, 0), (L, HP["z_moved"]), f"z {HP['z_moved']:g}", off=7, fs=7.5)
    dim(ax, (L, 0), (L, ZB), f"z {ZB:g}", off=15, fs=7.5)
    leader(ax, (L / 2 + HP["pitch"] + 14, HP["z_moved"] + 14), (440, 128), "3 bores Ø40 +0.10/0 through both webs, 60 pitch;\npins fitted loose; the fitting pads bolt to the leg side\nof the web (pocket depth from the C3 drawing)", fs=7.5, ha="left")
    leader(ax, (L / 2, ZP), (330, 12), "leak port Ø2 at mid-length, z 25 (as in the STEP)", fs=7.5, ha="left")
    leader(ax, (bl[0], ZB), (20, 98), "seam bolt holes Ø8.5, z 58: 2 + 2 in the two\n175 mm bays beside the fitting, none inside it", fs=7.5, ha="left")
    ax2 = view(fig, (318, 200, 86, 46), 5.0, (275, 90), title="SA-550, first version, bores at z 140: do not make  (1:5)")
    face(ax2, HP["z_as_drawn"], ORG)
    image(fig, (318, 128, 86, 60), png("SA-550-FB_iso"), "SA-550-FB from the STEP (legs, 14 + 14 leg holes)")
    nt = ("What the article does (RE-03 rev B, 2 Nov): assembled dry, the faces checked with a 0.05 feeler; cords in, bolts tightened from the middle out, squeeze read against torque; "
          "bead cured 24 h; end dams fitted; the space between the cords pressurised to 1 and 2 atm and logged (LC5, January 2027 at the earliest, once funded). Then pulled in prying through the lugs while the leak rate is read against the gap, "
          "which measures the gap at which the butyl stops sealing: the number the whole seal design turns on. Afterwards it stays assembled as the ageing sample.\n"
          "Leg holes: 7 positions at 75 pitch (50 to 500), two rows, both legs. Pull blocks: 160 x 80 x 550 (TP-04), 55 kg each in 4140; 19 kg each in 6061-T651 (DFM option). "
          "The seam model reaches the 0.11 mm gap at 3.75 kN per plain bolt. D1-550 ran on 14 Nov: 0.11 mm at about 11.8 kN of pull (computer result). Fixture rated 50 kN.\n"
          "Corrected 27 Nov: the leak port is drawn at mid-length, z 25, where the STEP has it (the sheet had it 137.5 mm off centre); the leak-test date and the D1-550 result are brought up to date; the note text no longer runs over the part; "
          "the version to make (moved, z 76) is the large view.")
    note(Pp, 14, 126, 206, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/TP-03_550.png")


# ---------------- TP-04 pull blocks and fixture ----------------
def tp04(pdf):
    fig, Pp = sheet("TP-04", "Pull blocks (rev B interface) and the lug, fork and pin", "For quotation after CHECK 1 and 2 are settled. Block 160 x 80 x L; M12 from both bearing faces; M24 for run 1; lug rows 32 / 64 from the flange-side face.",
                    "T1-075/150/225-PB, SA-550-HPmoved-PB; F-01, F-02, F-03", "1:2", material="4140 QT 28-32 HRC (DFM option 6061-T651)",
                    finish="Ra 3.2 all over (TP-00 note 4)")
    L = 150; H = BZ1 - BZ0
    ax = view(fig, (14, 156, 132, 112), 2.0, (85, 80), title="Pull face (the face away from the joint) of the 150 block  (1:2)")
    rect(ax, 0, 0, L, H, STEEL, lw=0.8)
    zc = H / 2
    ax.add_patch(Circle((L / 2, zc), 10.5, fc="white", ec="k", lw=0.7))
    for z in LUG_Z:
        for dy in (-30, 30): ax.add_patch(Circle((L / 2 + dy, z - BZ0), 5.1, fc="white", ec="k", lw=0.6))
    cl(ax, (L / 2, -8), (L / 2, H + 8))
    dim(ax, (0, H), (L, H), f"L ({L})", off=6)
    dim(ax, (0, 0), (0, H), f"{H:g}", off=-22)
    dim(ax, (0, 0), (0, LUG_Z[0] - BZ0), f"{LUG_Z[0] - BZ0:g}", off=-8, fs=7.5)
    dim(ax, (0, 0), (0, LUG_Z[1] - BZ0), f"{LUG_Z[1] - BZ0:g}", off=-15, fs=7.5)
    dim(ax, (L, 0), (L, zc), f"{zc:g}", off=6, fs=7.5)
    dim(ax, (L / 2 - 30, -4), (L / 2 + 30, -4), "60 (50 on the 75 block)", off=-6, fs=7.5)
    leader(ax, (L / 2 + 8, zc + 8), (160, 150), "M24 x 3, 40 deep (run 1), at the centre:\nz 90 in the assembly", fs=7.5, ha="left")
    leader(ax, (L / 2 + 34, LUG_Z[1] - BZ0 + 3), (160, 110), "4 x M12 x 1.75, drill Ø10.2 x 20 deep\n(lug plate F-01, run 2); rows z 42 and 74\nin the assembly = 32 and 64 from the\nflange-side bearing face", fs=7.5, ha="left")
    label(ax, (L / 2, -24), "flange-side bearing face (z 10 in the assembly)", fs=7.5, bg=False, col=GREY)
    # bearing face
    ax2 = view(fig, (152, 156, 112, 112), 2.0, (60, 75), title="Bearing face (either) of the 150 block  (1:2)")
    rect(ax2, 0, 0, BX, L, STEEL, lw=0.8)
    for x in (20, 60):
        for y in leg_ys(L)["inner" if x == 60 else "outer"]: ax2.add_patch(Circle((x, y), 5.1, fc="white", ec="k", lw=0.6))
    dim(ax2, (0, L), (BX, L), f"{BX:g}", off=6)
    dim(ax2, (0, L), (20, L), "20", off=13, fs=7.5); dim(ax2, (20, L), (60, L), "40", off=13, fs=7.5)
    dim(ax2, (BX, 0), (BX, L), f"L ({L})", off=20)
    dim(ax2, (BX, 0), (BX, 37.5), "37.5", off=7, fs=7.5); dim(ax2, (BX, 37.5), (BX, 112.5), "75", off=7, fs=7.5)
    label(ax2, (-4, L / 2), "pull face", fs=7.5, ha="right", rotation=90, bg=False, col=GREY)
    label(ax2, (BX + 4, -10), "joint side", fs=7.5, ha="left", bg=False, col=GREY)
    note(Pp, 270, 266, 136, "4 x M12 x 1.75 from each bearing face (drill Ø10.2 x 31 deep, 26 full thread), at the leg-hole positions of TP-01: "
         "the outer row 20 from the pull face, the inner row 60. Holes from the two faces line up; 160 - 2 x 31 leaves 98 mm of steel between them. "
         "Rows along L as TP-01: 75 block 16.5, 58.5 (outer) and 18.75, 56.25 (inner); 225 block 37.5, 112.5, 187.5; 550 block 50 to 500 at 75.\n"
         "All edges parallel to L chamfered 1 x 45°.\n"
         "Corrected 27 Nov: the lug rows were dimensioned 42 and 74 from the block's bottom edge; those are assembly heights from the frame's outer face. "
         "On the block they are 32 and 64 from the flange-side bearing face.", fs=7.5)
    y = heading(Pp, 270, 192, "CHECK before quoting", color=RED)
    note(Pp, 270, y, 136, "\n".join(c.split(": ", 1)[0] + ": " + c.split(": ", 1)[1] for c in CHECKS[:2]), fs=7.5, color=RED)
    for k, (nm, cap) in enumerate((("F-01", "F-01 lug plate 80 x 100 x 20, Ø20 H7 pin hole on the z 24 line, 4 x M12 counterbored (Ø20 x 12)"),
                                   ("F-02", "F-02 fork: two 15 mm cheeks, 21 mm gap, Ø20 H8 holes, M24 x 3 female for the adapter"),
                                   ("F-03", "F-03 pin Ø20 h6 x 70, Ø28 shoulder, E-clip groove, greased"))):
        image(fig, (16 + k * 70, 84, 56, 50), png(f"{nm}_iso", PARTS_SVG, 700), "")
        note(Pp, 14 + k * 70, 148, 66, cap, fs=7.5)
    note(Pp, 14, 76, 210, "Load train for run 2: crosshead, adapter, M24 stud, fork F-02, pin F-03, lug F-01, block, legs, frame, joint, and the mirror image below. Both pins are parallel to the seam, so each end is free to turn. "
         "Checks (RE-03 rev B, 50 kN fixture load): pin double shear 377 kN; lug tear-out 720 kN (with 30 mm of edge; CHECK 3 on TP-00); worst lug screw 39 kN against an 83 kN proof load.", fs=7.5)
    K.save(fig, pdf, f"{OUT}/TP-04_blocks_fixture.png")


PDF = "HCSA_test_pieces_RevF_TP-00_to_TP-04_27Nov2026.pdf"

if __name__ == "__main__":
    with PdfPages(f"{OUT}/{PDF}") as pdf:
        tp00(pdf); tp01(pdf); tp02(pdf); tp03(pdf); tp04(pdf)
    print("sheets ok")
