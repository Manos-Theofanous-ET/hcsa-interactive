"""Drawing sheets for the HCSA test pieces at Rev F (180 mm frame), 8 Nov 2026. Matplotlib, drawn from the same
parameters as build_testpieces.py, with the CadQuery views embedded. Sheets TP-00 to TP-04 in one PDF.
"""
import json, math, os, subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
T = json.load(open(f"{OUT}/testpieces.json")); PR = T["parameters"]
A3 = (16.54, 11.69); MET = "#9aa3ad"; MET2 = "#c9ced4"; STEEL = "#8a8f96"; SEAL = "#222"; RED = "#c0392b"; BLU = "#1f5f99"; ORG = "#b9770e"
D, WEB, FLT, LEG = PR["D"], PR["WEB"], PR["FL_T"], PR["LEG"]
GW, GD, Z1, Z2, ZR, ZP, ZB = PR["GW"], PR["GD"], PR["Z_G1"], PR["Z_G2"], PR["Z_RTV"], PR["Z_PORT"], PR["Z_BOLT"]
BX = PR["BLK_X"]; BZ0, BZ1 = PR["BLK_Z"]; HP = PR["HP"]

def png(name):
    svg = f"{OUT}/svg/{name}.svg"; out = f"{OUT}/svg/{name}.png"
    if not os.path.exists(out):
        subprocess.run(["rsvg-convert", "-w", "1100", svg, "-o", out], check=True)
    return mpimg.imread(out)

def sheet(no, title, status):
    fig = plt.figure(figsize=A3)
    fig.add_artist(Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, lw=1.5, transform=fig.transFigure))
    tb = fig.add_axes([0.60, 0.012, 0.39, 0.12]); tb.axis("off"); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=1.2))
    for y in (0.75, 0.5, 0.25): tb.plot([0, 1], [y, y], lw=0.6, c="k")
    tb.plot([0.6, 0.6], [0, 0.75], lw=0.6, c="k")
    tb.text(0.02, 0.86, f"HCSA  {no}  {title}", fontsize=10.5, weight="bold", va="center")
    tb.text(0.02, 0.62, "Test pieces, Rev F (180 frame), 8 Nov 2026. Replaces RE-01/02/03B, RF-03", fontsize=6.8, va="center")
    tb.text(0.02, 0.37, f"Status: {status[:92]}", fontsize=6.2, va="center")
    tb.text(0.02, 0.12, "Drawn: Claude for M. Theofanous    Checked: -    Released: -", fontsize=8, va="center")
    tb.text(0.62, 0.62, "mm. ISO 2768-m unless stated", fontsize=7.5, va="center")
    tb.text(0.62, 0.37, "STEP files govern the geometry", fontsize=7.5, va="center")
    tb.text(0.62, 0.12, "For quotation. Not for machining until checked", fontsize=7.5, va="center", color=RED)
    return fig

def dim(ax, p0, p1, txt, off=0.0, horiz=True, fs=7.5, col="k"):
    (x0, y0), (x1, y1) = p0, p1
    if horiz:
        y = y0 + off; ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.7, color=col))
        ax.plot([x0, x0], [y0, y], lw=0.4, c=col); ax.plot([x1, x1], [y1, y], lw=0.4, c=col)
        ax.text((x0 + x1) / 2, y, txt, ha="center", va="bottom", fontsize=fs, color=col, backgroundcolor="white")
    else:
        x = x0 + off; ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", lw=0.7, color=col))
        ax.plot([x0, x], [y0, y0], lw=0.4, c=col); ax.plot([x1, x], [y1, y1], lw=0.4, c=col)
        ax.text(x, (y0 + y1) / 2, txt, ha="center", va="center", rotation=90, fontsize=fs, color=col, backgroundcolor="white")

def art(name):
    return next(a for a in T["articles"] if a["name"] == name)

def bolt_ys(L, hardpoint):
    pitch = PR["PITCH"]
    if hardpoint:
        bay = L / 2 - HP["W"] / 2; n = int((bay - 60) // pitch) + 1; f0 = (bay - (n - 1) * pitch) / 2
        return [f0 + i * pitch for i in range(n)] + [L - f0 - i * pitch for i in range(n)]
    nb = int(round(L / pitch)); return [L / 2 + (i - (nb - 1) / 2) * pitch for i in range(nb)]

def leg_ys(L):
    if L == 75: return {"inner": [18.75, 56.25], "outer": [16.5, 58.5]}
    n = int(L // 75); ys = [L / 2 + (i - (n - 1) / 2) * 75 for i in range(n)]; return {"inner": ys, "outer": ys}

# ---------------- TP-00 cover: index, notes, tolerance table, BOM ----------------
def tp00(pdf):
    fig = sheet("TP-00", "Cover: sheet list, notes, tolerances, parts list", "for quotation; tolerances and DFM items are proposals for Marco, 13 Nov")
    fig.text(0.03, 0.95, "HCSA test pieces, Rev F, 8 November 2026", fontsize=15, weight="bold", va="top")
    fig.text(0.03, 0.915, "The T1 seam slices (75, 150, 225 mm), the 550 mm seal article with its grip legs and dummy hardpoint, and the pull blocks, all at the 180 mm frame.\n"
             "Drawn from hcsa_params_revF.json (5 Nov). What changed from the 24 Oct Rev E draft: frame depth 140 to 180, gland 7.1 x 4.0, seam bolt NAS6705U27 at 4 kN,\n"
             "the pull blocks grow to 160 tall to span the legs, run 2 pulls through pinned lugs (RE-03 rev B), the 550 article has legs and a dummy hardpoint (2 + 2 bolts).", fontsize=8.5, va="top")
    ax = fig.add_axes([0.03, 0.42, 0.44, 0.45]); ax.axis("off")
    rows = [("TP-00", "Cover, notes, tolerances, parts list"), ("TP-01", "T1 frame B (glands): section, joint face, legs; 75 / 150 / 225 table"),
            ("TP-02", "T1 frame A and the slice as assembled, pull lines, screws"), ("TP-03", "550 mm seal article with legs and the dummy hardpoint, both fitting depths"),
            ("TP-04", "Pull blocks (rev B interface) and the lug, fork and pin F-01 to F-03"), ("STEP", "out/step: one file per part; out/asm: one assembly per article")]
    ax.text(0, 1.0, "Sheets", fontsize=10, weight="bold", va="top")
    for i, (a, b) in enumerate(rows): ax.text(0, 0.92 - i * 0.065, a, fontsize=8.5, weight="bold", va="top"); ax.text(0.14, 0.92 - i * 0.065, b, fontsize=8.5, va="top")
    ax.text(0, 0.50, "General notes", fontsize=10, weight="bold", va="top")
    notes = ["1. Material: frames 6061-T651 plate (as drawn, keeps the FEA twins valid). Pull blocks 4140 quenched and tempered 28-32 HRC (as drawn).",
             "   DFM option for Marco: blocks in 6061-T651 (one material, 65 % lighter: 19 kg instead of 55 kg each on the 550 article).",
             "2. Machining order for the frames: rough, rest 24 h, finish; the joint face is the last cut (fly-cut), so the part is flat after the stress is out.",
             "3. Inside corners web-to-flange and web-to-lip R6. Every hole 1 x 45 deg at both ends. All other edges 0.5 mm break. Gland edges deburred only, no break.",
             "4. Surface finish: joint face and gland faces Ra 0.8 um. Elsewhere Ra 3.2.",
             "5. Hardware (test articles, McMaster-Carr or equal): ISO 4762 M12 x 35 class 12.9 socket screws + ISO 7089 hardened washers into the blocks;",
             "   M12 x 45 class 12.9 for the lug plates; seam bolts NAS6705U27 with KFN670 nuts and two hardened washers (flight part, A286).",
             "6. Seals: Parker BA500-70 butyl cord 0.210 in, two per article, RTV566 bead with SS4155 primer. End dams on the slices (M8 rod, fabrication plan 2.3).",
             "7. Quantities: one of each slice (75, 150, 225) and one 550 article: 8 frames, 8 blocks. Fixture parts F-01 to F-03 are shared: 2 lugs, 2 forks, 2 pins + 1 spare each."]
    for i, n in enumerate(notes): ax.text(0, 0.44 - i * 0.047, n, fontsize=7.3, va="top")
    # tolerance table
    ax2 = fig.add_axes([0.50, 0.47, 0.48, 0.40]); ax2.axis("off")
    ax2.text(0, 1.0, "Tolerances: tight only where the seal or the fit needs it (proposal for Marco, 13 Nov)", fontsize=10, weight="bold", va="top")
    tol = [("Feature", "As drawn 24 Oct", "Proposed", "Why"),
           ("Joint face flatness", "0.05 over the length", "0.10 per 150 mm, 0.15 over 550", "0.1 mm of gap moves the squeeze 2 points of 25 %"),
           ("Joint face finish", "Ra 0.8", "Ra 0.8 (keep)", "Parker face-seal finish"),
           ("Gland depth 4.0", "+-0.05", "+-0.05 (keep)", "sets the 25 % squeeze; a shallow groove, easy to hold"),
           ("Gland width 7.1", "+-0.05", "+-0.10", "fill 78.7 % moves 1 point per 0.1 mm"),
           ("Gland position z 18, 32", "+-0.05", "+-0.15", "the cords only have to meet the flat face of frame A"),
           ("Seam bolt holes", "8.4 reamed, pos +-0.2", "8.5 drilled, pos +-0.2", "a clamp bolt, not a shear pin, in the test articles"),
           ("Leg holes", "13.5", "14.0 drilled, pattern +-0.2", "M12 screws need play to find the block threads"),
           ("Hardpoint bores (550)", "40 H7", "40 +0.10 / 0", "the dummy pins are fitted loose by design"),
           ("Block bearing faces", "parallel 0.05", "parallel 0.10, height 160 +-0.1", "the legs must not be sprung when the screws go in"),
           ("Everything else", "ISO 2768-f", "ISO 2768-m", "legs, lengths, block outline: nothing seals on them")]
    for i, r in enumerate(tol):
        y = 0.92 - i * 0.075; w = (0, 0.21, 0.43, 0.68)
        for c, txt in zip(w, r): ax2.text(c, y, txt, fontsize=7.2 if i else 7.8, weight="bold" if i == 0 else "normal", va="top")
        if i == 0: ax2.plot([0, 1], [y - 0.03, y - 0.03], lw=0.6, c="k")
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.text(0, 0.06, "Temperature: all sizes at 20 C. 7 C of difference moves 550 mm of aluminium by 0.09 mm (23.6e-6 per K), so the long parts are measured at 20 C (Marco, 7 Nov).", fontsize=7.4, va="top", color=ORG)
    # BOM
    ax3 = fig.add_axes([0.03, 0.165, 0.95, 0.25]); ax3.axis("off")
    ax3.text(0, 1.0, "Parts list (masses from the solids)", fontsize=10, weight="bold", va="top")
    hdr = ("Part", "Description", "Material", "Qty", "Mass each kg", "Stock blank (mm)")
    rows = []
    for a in T["articles"]:
        if "DFM" in a["name"] or "HPmoved" in a["name"]: continue
        L = a["L"]
        for b in a["bom"]:
            blank = f"190 x 230 x {L+6}" if b["id"].endswith(("FB", "FA")) else f"165 x 85 x {L+6}"
            rows.append((b["id"], b["desc"], b["material"], b["qty"], f"{b['mass_kg']:.2f}", blank))
    rows += [("F-01", "Lug plate 80 x 100 x 20 (RE-03 rev B)", "4140 QT", 2, "1.05", "from the parts library STEP"),
             ("F-02", "Fork with M24 x 3 for the Instron adapter", "4140 QT", 2, "1.80", "parts library STEP"),
             ("F-03", "Pin 20 h6 x 70 with shoulder and E-clip groove", "17-4PH H900 or 4140 QT", 2, "0.20", "parts library STEP"),
             ("SA-550-HPmoved-*", "The same three 550 parts with the dummy fitting bores at z 76 instead of 140 (if Tuesday chooses the moved fitting)", "as above", "-", "same", "same")]
    cols = (0, 0.13, 0.62, 0.75, 0.80, 0.89)
    for c, h in zip(cols, hdr): ax3.text(c, 0.9, h, fontsize=7.8, weight="bold", va="top")
    ax3.plot([0, 1], [0.86, 0.86], lw=0.6, c="k")
    for i, r in enumerate(rows):
        y = 0.82 - i * 0.056
        for c, txt in zip(cols, r): ax3.text(c, y, str(txt), fontsize=6.9, va="top")
    ax3.set_xlim(0, 1); ax3.set_ylim(0, 1); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    pdf.savefig(fig); fig.savefig(f"{OUT}/TP-00_cover.png", dpi=130); plt.close(fig)

# ---------------- TP-01 frame B ----------------
def tp01(pdf):
    fig = sheet("TP-01", "T1 frame B (glands), 180 deep: section, joint face, legs", "geometry from build_testpieces.py; 75 / 150 / 225 as a table")
    # section XZ through a bolt (looking along +y). Draw frame B at x<=0, joint face x=0.
    ax = fig.add_axes([0.03, 0.30, 0.46, 0.62]); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-WEB, 0), WEB, D, fc=MET2, ec="k", lw=0.8))
    ax.add_patch(Rectangle((-(WEB + LEG), 0), LEG, FLT, fc=MET2, ec="k", lw=0.8))
    ax.add_patch(Rectangle((-(WEB + LEG), D - FLT), LEG, FLT, fc=MET2, ec="k", lw=0.8))
    for r in (FLT, D - FLT):   # R6 fillets drawn as arcs
        ax.add_patch(Arc((-WEB - 6, r + (6 if r == FLT else -6)), 12, 12, theta1=180 if r == FLT else 90, theta2=270 if r == FLT else 180, lw=0.7, color="k"))
    for zc in (Z1, Z2):
        ax.add_patch(Rectangle((-GD, zc - GW / 2), GD, GW, fc="white", ec="k", lw=0.6))
        ax.add_patch(Circle((-GD / 2 + 0.3, zc), 5.33 / 2, fc=SEAL, ec="none"))
    ax.add_patch(Arc((0, ZR), 6, 6, theta1=90, theta2=270, lw=0.8, color="k")); ax.add_patch(Rectangle((-3, ZR - 3), 3, 6, fc="white", ec="none"))
    ax.add_patch(Rectangle((-WEB, ZP - 1), WEB, 2, fc="white", ec="k", lw=0.5)); ax.add_patch(Rectangle((-WEB, ZP - 2.1), 8, 4.2, fc="white", ec="k", lw=0.5))
    ax.add_patch(Rectangle((-WEB, ZB - 4.2), WEB, 8.4, fc="white", ec="k", lw=0.6))
    # block outline and leg holes
    bx0 = -(WEB + LEG); ax.add_patch(Rectangle((bx0, BZ0), BX, BZ1 - BZ0, fill=False, ec=STEEL, lw=0.8, ls="--"))
    for xr in (bx0 + 20, bx0 + BX - 20):
        ax.add_patch(Rectangle((xr - 6.75, 0), 13.5, FLT, fc="white", ec="k", lw=0.5)); ax.add_patch(Rectangle((xr - 6.75, D - FLT), 13.5, FLT, fc="white", ec="k", lw=0.5))
    dim(ax, (-WEB, D), (0, D), f"{WEB:.0f}", off=14)
    dim(ax, (-(WEB + LEG), D), (-WEB, D), f"{LEG:.0f} (DFM: 120)", off=14)
    dim(ax, (0, 0), (0, D), f"{D:.0f}", off=36, horiz=False)
    dim(ax, (0, 0), (0, Z1), f"{Z1:.0f}", off=12, horiz=False, fs=6.5); dim(ax, (0, 0), (0, Z2), f"{Z2:.0f}", off=20, horiz=False, fs=6.5)
    dim(ax, (0, 0), (0, ZB), f"{ZB:.0f}", off=28, horiz=False, fs=6.5)
    dim(ax, (-(WEB + LEG), 0), (-(WEB + LEG), FLT), f"{FLT:.0f}", off=-12, horiz=False, fs=6.5)
    dim(ax, (bx0 + 20, 0), (bx0 + BX - 20, 0), "40 (hole rows)", off=-22, fs=6.5)
    dim(ax, (bx0, D), (bx0 + BX, D), "80 (block)", off=28, fs=6.5, col=STEEL)
    ax.annotate(f"2 glands {GW} x {GD}, bottom R0.5-0.9,\nrun through, dammed at the ends", (-GD, Z1), (-120, 60), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("RTV recess R3", (-3, ZR), (-120, 85), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("leak port dia 2 through, M5 from the leg side, 8 deep,\none per slice at mid-length", (-WEB, ZP), (-215, 118), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("seam bolt holes dia 8.5 (8.4 reamed as drawn)\nat 75 pitch, centred", (-WEB, ZB), (-215, 150), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("leg holes dia 14 (13.5 as drawn), 2 rows,\nthrough both legs; block threads match", (bx0 + 20, FLT), (-215, -40), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.annotate("R6 inside corners (both)", (-WEB - 6, FLT + 6), (-150, 30), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
    ax.text(2, D / 2, "joint face\n(x = 0)", fontsize=7, color=RED, va="center"); ax.plot([0, 0], [-10, D + 10], ls="-.", lw=0.6, c=RED)
    ax.text(-(WEB + LEG) + 5, D + 40, "space side (z 0) at the bottom, cabin side (z 180) at the top; the seat lip (z 170-180) doubles as the second grip leg", fontsize=7, color="#555")
    ax.set_xlim(-(WEB + LEG) - 40, 60); ax.set_ylim(-50, D + 60); ax.set_title("Section through a bolt station, looking along the seam (1:1 on A3)", fontsize=9.5)
    # joint face elevation for the 150
    ax2 = fig.add_axes([0.52, 0.56, 0.46, 0.36]); ax2.set_aspect("equal"); ax2.axis("off")
    L = 150
    ax2.add_patch(Rectangle((0, 0), L, D, fc=MET2, ec="k", lw=0.8))
    for zc in (Z1, Z2): ax2.add_patch(Rectangle((0, zc - GW / 2), L, GW, fc="white", ec="k", lw=0.5)); ax2.plot([0, L], [zc, zc], c=SEAL, lw=1.4)
    ax2.plot([0, L], [ZR, ZR], c="k", lw=0.5, ls=":")
    for y in bolt_ys(L, False): ax2.add_patch(Circle((y, ZB), 4.25, fc="white", ec="k", lw=0.6))
    ax2.add_patch(Circle((L / 2, ZP), 1, fc="white", ec="k", lw=0.5))
    dim(ax2, (0, D), (L, D), f"{L}", off=10); dim(ax2, (bolt_ys(L, False)[0], ZB), (bolt_ys(L, False)[1], ZB), "75", off=-16, fs=6.5)
    dim(ax2, (0, 0), (bolt_ys(L, False)[0], 0), "37.5", off=-12, fs=6.5)
    ax2.set_xlim(-30, L + 30); ax2.set_ylim(-35, D + 30); ax2.set_title("Joint face of the 150 slice (frame B)", fontsize=9)
    # leg plan and table
    ax3 = fig.add_axes([0.52, 0.30, 0.46, 0.24]); ax3.axis("off")
    ax3.text(0, 1.0, "Leg holes (both legs, through), measured from the slice end along the seam and from the joint face across the leg", fontsize=8.5, weight="bold", va="top")
    tab = [("Slice", "Seam bolts (from the end)", "Leg holes, inner row x 140", "Leg holes, outer row x 180", "Threads / face"),
           ("75", "37.5", "18.75, 56.25", "16.5, 58.5 (OPEN-6, moved for the M24 wall)", "4"),
           ("150", "37.5, 112.5", "37.5, 112.5", "37.5, 112.5", "4"),
           ("225", "37.5, 112.5, 187.5", "37.5, 112.5, 187.5", "37.5, 112.5, 187.5", "6"),
           ("550 (TP-03)", "50, 125, 425, 500", "7 at 75 pitch, 50 to 500", "same", "14")]
    for i, r in enumerate(tab):
        y = 0.8 - i * 0.16; cols = (0, 0.11, 0.33, 0.56, 0.86)
        for c, txt in zip(cols, r): ax3.text(c, y, txt, fontsize=7.2, weight="bold" if i == 0 else "normal", va="top")
    # iso view
    axi = fig.add_axes([0.03, 0.03, 0.55, 0.26]); axi.axis("off"); axi.imshow(png("T1-150-FB_iso")); axi.set_title("T1-150-FB, from the STEP (legs toward the viewer, joint face at the back)", fontsize=8)
    fig.text(0.60, 0.26, "Frame A (TP-02) is the mirror image without the glands, the recess and the port.\nStock 6061-T651 plate 190 x 230 x (L + 6); with 120 mm legs, 190 x 150 x (L + 6).\n"
             "The slice is flat, so z equals the joint-plane coordinate z' of the flight frame: the test measures the same joint face the station has.", fontsize=7.6, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/TP-01_frame_B.png", dpi=130); plt.close(fig)

# ---------------- TP-02 frame A and the slice assembled ----------------
def tp02(pdf):
    fig = sheet("TP-02", "T1 frame A and the slice as assembled, pull lines, screws", "block 160 tall; run 1 M24 at z 90; run 2 through the lugs at z 24 (rev B)")
    ax = fig.add_axes([0.03, 0.30, 0.6, 0.62]); ax.set_aspect("equal"); ax.axis("off")
    def frame_side(sgn, col, grooved):
        ax.add_patch(Rectangle((0 if sgn > 0 else -WEB, 0), WEB, D, fc=col, ec="k", lw=0.8))
        ax.add_patch(Rectangle((WEB if sgn > 0 else -(WEB + LEG), 0), LEG, FLT, fc=col, ec="k", lw=0.8))
        ax.add_patch(Rectangle((WEB if sgn > 0 else -(WEB + LEG), D - FLT), LEG, FLT, fc=col, ec="k", lw=0.8))
        bx0 = WEB + LEG - BX if sgn > 0 else -(WEB + LEG)
        ax.add_patch(Rectangle((bx0, BZ0), BX, BZ1 - BZ0, fc=STEEL, ec="k", lw=0.8))
        for xr in (bx0 + 20, bx0 + BX - 20):
            for z0, z1 in ((0, FLT + 31), (D - FLT - 31, D)):
                ax.add_patch(Rectangle((xr - 5.1, z0), 10.2, z1 - z0, fc="white", ec="k", lw=0.4))
            ax.add_patch(Rectangle((xr - 9, D), 18, 2.5, fc="#666", ec="k", lw=0.4)); ax.add_patch(Rectangle((xr - 9, -2.5), 18, 2.5, fc="#666", ec="k", lw=0.4))
        zc = (BZ0 + BZ1) / 2
        ax.add_patch(Rectangle((bx0 if sgn < 0 else bx0 + BX - 40, zc - 10.5), 40, 21, fc="white", ec="k", lw=0.5))
        for z in (42, 74): ax.add_patch(Rectangle((bx0 if sgn < 0 else bx0 + BX - 20, z - 5.1), 20, 10.2, fc="white", ec="k", lw=0.4))
        if grooved:
            for zz in (Z1, Z2): ax.add_patch(Rectangle((-GD, zz - GW / 2), GD, GW, fc="white", ec="k", lw=0.5)); ax.add_patch(Circle((-GD / 2 + 0.3, zz), 2.6, fc=SEAL, ec="none"))
            ax.add_patch(Circle((0, ZR), 3, fc="#7a5", ec="k", lw=0.4))
    frame_side(-1, MET2, True); frame_side(1, "#e4e7ea", False)
    ax.add_patch(Rectangle((-WEB - 3.2, ZB - 3.97), 2 * WEB + 6.4, 7.94, fc="#555", ec="k", lw=0.5))
    ax.add_patch(Rectangle((-WEB - 4.9 - 1.6, ZB - 6.3), 4.9, 12.7, fc="#777", ec="k", lw=0.5)); ax.add_patch(Rectangle((WEB + 1.6, ZB - 6.3), 6.8, 12.7, fc="#777", ec="k", lw=0.5))
    for z, lab, c in ((90, "run 1: straight pull, M24 x 3 at the block centre (z 90)", BLU), (24, "run 2: prying pull at z 24 through the lug, fork and pin (rev B)", ORG)):
        ax.annotate("", (-(WEB + LEG) - 60, z), (WEB + LEG + 60, z), arrowprops=dict(arrowstyle="<->", lw=1.4, color=c)); ax.text(0, z + 5, lab, ha="center", fontsize=7.5, color=c)
    ax.plot([0, 0], [-10, D + 10], ls="-.", lw=0.6, c=RED)
    dim(ax, (-(WEB + LEG), D), (WEB + LEG, D), f"{2*(WEB+LEG):.0f} over the legs", off=30)
    dim(ax, (WEB + LEG, BZ0), (WEB + LEG, BZ1), f"{BZ1-BZ0:.0f}", off=30, horiz=False)
    ax.text(-(WEB + LEG), -40, "M12 x 35 class 12.9 screws with hardened washers through the 14 mm leg holes into the block threads (4 to 14 per face).\nThe screws carry the pull in shear; the washers keep the head pressure on the 6061 leg under 132 MPa (RE-01-2 check).", fontsize=7.3, va="top")
    ax.set_xlim(-(WEB + LEG) - 80, WEB + LEG + 80); ax.set_ylim(-70, D + 50); ax.set_title("Section through a bolt station: frame B (left, glands), frame A (right), the two pull blocks and the seam bolt", fontsize=9.5)
    axi = fig.add_axes([0.64, 0.56, 0.34, 0.36]); axi.axis("off"); axi.imshow(png("T1-150-FA_iso")); axi.set_title("T1-150-FA (flat face), from the STEP", fontsize=8)
    axj = fig.add_axes([0.64, 0.30, 0.34, 0.24]); axj.axis("off"); axj.imshow(png("T1-150-PB_iso")); axj.set_title("Pull block, 160 x 80 x 150 (TP-04)", fontsize=8)
    fig.text(0.03, 0.26, "Why the block grew. On the 140 frame the block spanned the flange and the lip, 83 mm apart. On the 180 frame the lip is at the cabin face\n"
             "(z 170-180, P-06), so the span is 160 mm. The single M24 for run 1 sits at the block centre, which puts the straight pull at z 90; the D1 and HP1 twins\n"
             "pull at the frame middle (76 mm), so run 1's pull line is 14 mm off the twin's. Run 2 (the one the seal design turns on) is unchanged at z 24.\n"
             "The 2.0 and 3.5 mm walls round the two M24 threads of the 24 Oct blocks are gone: rev B has one M24 and the z 24 pull goes through the lugs.\n"
             "DFM questions for Marco: block in 6061-T651 instead of 4140 (19 kg instead of 55 kg on the 550 pair; the M12 and M24 threads in aluminium carry\n"
             "the 100 kN frame load with margin); legs 120 instead of 200 (stock 190 x 150 instead of 190 x 230; the block moves in; the twins' fixture legs change).", fontsize=7.6, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/TP-02_assembled.png", dpi=130); plt.close(fig)

# ---------------- TP-03 the 550 article ----------------
def tp03(pdf):
    fig = sheet("TP-03", "550 mm seal article with legs and the dummy hardpoint", "dummy fitting at z 140 (as drawn) or z 76 (moved): decision Tue 10 Nov; both STEPs")
    L = 550
    for k, (hz, lab, name) in enumerate(((HP["z_as_drawn"], "as drawn (RE-06-1: fitting 110 to 170 deep)", "SA-550"), (HP["z_moved"], "moved onto the pull line (HP1M study: 46 to 106 deep)", "SA-550-HPmoved"))):
        ax = fig.add_axes([0.03, 0.62 - k * 0.3, 0.6, 0.28]); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((0, 0), L, D, fc=MET2, ec="k", lw=0.8))
        for zc in (Z1, Z2): ax.plot([0, L], [zc, zc], c=SEAL, lw=1.4)
        ax.plot([0, L], [ZR, ZR], c="k", lw=0.5, ls=":")
        ax.add_patch(Rectangle((L / 2 - HP["W"] / 2, hz - 30), HP["W"], 60, fill=False, ec=ORG, lw=0.9, ls="--"))
        for j in (-1, 0, 1): ax.add_patch(Circle((L / 2 + j * HP["pitch"], hz), HP["pin"] / 2, fc="white", ec="k", lw=0.7))
        for y in bolt_ys(L, True): ax.add_patch(Circle((y, ZB), 4.25, fc="white", ec="k", lw=0.6))
        ax.add_patch(Circle((L / 2 + 100 + 37.5, ZP), 1, fc="white", ec="k", lw=0.5))
        dim(ax, (0, D), (L, D), f"{L}", off=10)
        dim(ax, (L / 2 - HP["pitch"], hz), (L / 2 + HP["pitch"], hz), "2 x 60", off=-32, fs=6.5)
        dim(ax, (0, 0), (0, hz), f"z {hz:.0f}", off=-16, horiz=False, fs=6.5, col=ORG)
        dim(ax, (0, 0), (bolt_ys(L, True)[0], 0), "50", off=-12, fs=6.5); dim(ax, (bolt_ys(L, True)[0], 0), (bolt_ys(L, True)[1], 0), "75", off=-12, fs=6.5)
        ax.text(L / 2, D + 28, f"Joint face of frame B, dummy hardpoint {lab}", ha="center", fontsize=8.5, color=ORG if k else "k")
        ax.text(L / 2, hz + 38, "3 bores dia 40 (+0.10/0) through both webs, 60 pitch; pins fitted loose; fitting pads bolt to the leg side of the web (pocket depth from the C3 drawing)", ha="center", fontsize=6.6)
        ax.set_xlim(-30, L + 30); ax.set_ylim(-35, D + 40)
    axi = fig.add_axes([0.64, 0.50, 0.34, 0.40]); axi.axis("off"); axi.imshow(png("SA-550-FB_iso")); axi.set_title("SA-550-FB from the STEP: legs, 14 + 14 leg holes, 4 seam bolts, 3 pin bores", fontsize=7.5)
    fig.text(0.03, 0.30, "What the article does (RE-03 rev B, 2 Nov): assembled dry, the faces checked with a 0.05 feeler; cords in, bolts tightened from the middle out, squeeze read against torque;\n"
             "bead cured 24 h; end dams fitted; the space between the cords pressurised to 1 and 2 atm and logged (LC5, 7-14 Dec). Then pulled in prying through the lugs while the\n"
             "leak rate is read against the gap, which measures the gap at which the butyl stops sealing, the number the whole seal design turns on. Afterwards it stays assembled as the ageing sample.\n"
             "Bolts: 2 + 2 at 75 pitch in the two 175 mm bays beside the 200 mm dummy fitting (RF-03), none inside it. Leg holes: 7 positions at 75 pitch (50 to 500), two rows, both legs.\n"
             "Pull blocks: 160 x 80 x 550 (TP-04), 55 kg each in 4140; 19 kg each in 6061-T651 (DFM option). Expected pulls: about 3.3 kN per bolt to a 0.11 mm gap, so about 60 kN on the article.", fontsize=7.5, va="top")
    axj = fig.add_axes([0.64, 0.14, 0.34, 0.33]); axj.axis("off"); axj.imshow(png("SA-550-PB_iso")); axj.set_title("SA-550-PB, 160 x 80 x 550", fontsize=7.5)
    pdf.savefig(fig); fig.savefig(f"{OUT}/TP-03_550.png", dpi=130); plt.close(fig)

# ---------------- TP-04 pull blocks and fixture ----------------
def tp04(pdf):
    fig = sheet("TP-04", "Pull blocks (rev B interface) and the lug, fork and pin", "block 160 x 80 x L; M12 from both faces; M24 run 1; lug rows z 42/74; F-01..03 as 2 Nov")
    ax = fig.add_axes([0.03, 0.42, 0.44, 0.5]); ax.set_aspect("equal"); ax.axis("off")
    L = 150; H = BZ1 - BZ0
    # pull face view (YZ): y along, z up (block from z 10 to 170; z shown absolute)
    ax.add_patch(Rectangle((0, BZ0), L, H, fc=STEEL, ec="k", lw=0.8))
    ax.add_patch(Circle((L / 2, (BZ0 + BZ1) / 2), 10.5, fc="white", ec="k", lw=0.7)); ax.text(L / 2 + 14, (BZ0 + BZ1) / 2, "M24 x 3, 40 deep (run 1)", fontsize=7, va="center")
    for z in (42, 74):
        for dy in (-30, 30): ax.add_patch(Circle((L / 2 + dy, z), 5.1, fc="white", ec="k", lw=0.6))
    ax.text(L / 2 + 42, 58, "4 x M12 x 1.75, 20 deep\n(lug plate F-01, run 2)\nrows z 42 and 74 from the\nframe's outer face; +-30\n(+-25 on the 75 block)", fontsize=6.8, va="center")
    dim(ax, (0, BZ1), (L, BZ1), f"L ({L})", off=10); dim(ax, (0, BZ0), (0, BZ1), f"{H:.0f}", off=-14, horiz=False)
    dim(ax, (0, BZ0), (0, 42), "42", off=-26, horiz=False, fs=6.5); dim(ax, (0, BZ0), (0, 74), "74", off=-38, horiz=False, fs=6.5)
    ax.set_xlim(-50, L + 110); ax.set_ylim(BZ0 - 25, BZ1 + 25); ax.set_title("Pull face (the face away from the joint), z measured from the frame's outer face", fontsize=9)
    ax2 = fig.add_axes([0.50, 0.42, 0.48, 0.5]); ax2.set_aspect("equal"); ax2.axis("off")
    # bearing face view (XY): x across (80), y along (L)
    ax2.add_patch(Rectangle((0, 0), BX, L, fc=STEEL, ec="k", lw=0.8))
    for x in (20, 60):
        for y in leg_ys(L)["inner" if x == 60 else "outer"]: ax2.add_patch(Circle((x, y), 5.1, fc="white", ec="k", lw=0.6))
    dim(ax2, (0, L), (BX, L), f"{BX:.0f}", off=8); dim(ax2, (20, L), (60, L), "40", off=-14, fs=6.5)
    dim(ax2, (BX, 0), (BX, L), f"L ({L})", off=12, horiz=False)
    ax2.text(BX + 25, L / 2, "4 x M12 x 1.75 from each bearing face\n(10.2 drill 31 deep, 26 full thread),\nat the leg hole positions of TP-01.\nHoles from the two faces line up;\n160 - 2 x 31 leaves 98 mm of steel between.\nThe outer row sits 20 from the pull face.", fontsize=7, va="center")
    ax2.set_xlim(-20, BX + 150); ax2.set_ylim(-20, L + 25); ax2.set_title("Bearing face (either), the leg screws' threads", fontsize=9)
    for k, (nm, cap) in enumerate((("F-01", "Lug plate 80 x 100 x 20, 20 H7 pin hole on the z 24 line, 4 x M12 x 45 counterbored"), ("F-02", "Fork: two 15 mm cheeks, 21 mm gap, 20 H8 holes, M24 x 3 female for the adapter"), ("F-03", "Pin 20 h6 x 70, 28 shoulder, E-clip groove, greased"))):
        axk = fig.add_axes([0.03 + k * 0.32, 0.13, 0.30, 0.26]); axk.axis("off")
        p = f"/home/claude/manos-theofanous-et/hcsa-interactive/public/parts/svg/{nm}_iso.svg"; o = f"{OUT}/svg/{nm}_iso.png"
        if not os.path.exists(o): subprocess.run(["rsvg-convert", "-w", "700", p, "-o", o], check=True)
        axk.imshow(mpimg.imread(o)); axk.set_title(f"{nm}: {cap}", fontsize=7)
    fig.text(0.03, 0.11, "Load train for run 2: crosshead, adapter, M24 stud, fork F-02, pin F-03, lug F-01, block, legs, frame, joint, and the mirror image below. Both pins parallel to the seam, so each end is free to turn.\n"
             "Checks (RE-03 rev B, 50 kN fixture load): pin double shear 377 kN; lug tear-out 720 kN; worst lug screw 39 kN against an 83 kN proof load. Material 4140 QT 28-32 HRC as drawn.", fontsize=7.4, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/TP-04_blocks_fixture.png", dpi=130); plt.close(fig)

if __name__ == "__main__":
    with PdfPages(f"{OUT}/HCSA_test_pieces_RevF_TP-00_to_TP-04_8Nov2026.pdf") as pdf:
        tp00(pdf); tp01(pdf); tp02(pdf); tp03(pdf); tp04(pdf)
    print("sheets ok")
