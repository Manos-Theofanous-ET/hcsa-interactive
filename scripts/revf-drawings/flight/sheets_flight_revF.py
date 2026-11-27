"""Rev F flight sheets RF-00 to RF-09, issue of 27 Nov 2026.

RF-00 (new): sheet index, revision history, conventions, the baseline and the open items.
RF-01 to RF-04: first drawn on 5 Nov by a script that is not in this repository; redrawn here from the parameter file on
27 Nov so that every Rev F sheet comes from one place.
RF-05 to RF-09: the sheets of 8 Nov (reissued 17 Nov, corner ties 180 kN), corrected and laid out again on 27 Nov.

Everything is drawn from src/hcsa_params_revF.json, the parts library masses and the corner block builder
(parts_revF/corner_block.py, for the block outline and hole table). Dimensioned 2D sheets, not CAD sections; the STEP files
of the parts library govern where they differ. No design value is changed on these sheets: where a sheet disagreed with
the parameter file or with the solids it was corrected, and where something needs a decision it is marked OPEN.

    python flight/sheets_flight_revF.py            (from scripts/revf-drawings; writes flight/out/)
"""
import json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Ellipse, Wedge
from matplotlib.backends.backend_pdf import PdfPages

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, "..", "src")); sys.path.insert(0, os.path.join(HERE, "..", "parts_revF"))
import drawing_kit as K
from drawing_kit import dim, leader, label, note, heading, table, view, cl, MET, MET2, MET3, STEEL, GLS, SEAL, RED, BLU, ORG, GRN, TI, GREY
import corner_block as CB           # the builder of CB-01 / CB-02: outline, hole table and the exact mitres

P = json.load(open(os.path.join(HERE, "..", "src", "hcsa_params_revF.json"))); v = lambda g, k: P[g][k][0]
EDGE = v("geometry", "edge"); KGRID = v("geometry", "grid_k"); PITCH = EDGE / KGRID
DIAM = v("geometry", "diameter")
MH, MP = math.degrees(CB.mitre(6)), math.degrees(CB.mitre(5))          # 20.905, 16.472
D = v("frame", "depth"); WEB = v("frame", "web"); FL_W = v("frame", "flange_width"); FL_T = v("frame", "flange_thickness")
LIP_H, LIP_P = v("frame", "seat_lip_hex"), v("frame", "seat_lip_pent")
Z1 = v("seal", "outer_cord_z"); Z2 = Z1 + v("seal", "centreline_spacing"); ZR = 42.0; ZPORT = 25.0; ZB = v("seam_bolt", "row_z")
GW, GD = v("seal", "gland_width"), v("seal", "gland_depth"); CORD = 5.334
TP = v("pane", "thickness"); CUT = v("pane", "cut"); SHORT = v("pane", "cut_short_of_rib_centreline"); BITE_MIN = v("pane", "bite_rule_min")
MR = dict(d=v("main_rib", "depth"), bf=v("main_rib", "flange_width"), tf=v("main_rib", "flange_thickness"), tw=v("main_rib", "web"))
SR = dict(d=v("secondary_rib", "depth"), bf=v("secondary_rib", "flange_width"), tf=v("secondary_rib", "flange_thickness"), tw=v("secondary_rib", "web"))
LEDGE_W, LEDGE_T, CAP_H, CAP_V, CAP_T = 30.0, 10.0, 46.0, 100.0, 12.0     # P-04 seat ledges and P-04A cap angles (parts library, 2 Nov)
BOLT_HOLE = 8.4                                                          # P-06H seam bolt hole (the test pieces use 8.5 drilled)
TIE_PRE, TIE_LIM = v("corner", "tie_preload_kN"), v("corner", "tie_limit_kN")
PRE = P["cabin"]
MASS = {"P-01": 2.53, "P-02": 1.75, "P-03": 4.38, "P-04": 33.24, "P-04A": 12.77, "P-05": 28.28, "P-05A": 14.20, "P-06": 27.86,
        "P-07": 5.50, "P-08": 0.19, "P-14": 0.03}

ORDER = ["RF-00", "RF-01", "RF-02", "RF-03", "RF-04", "RF-05", "RF-06", "RF-07", "RF-08", "RF-09", "TP-00", "TP-01", "TP-02", "TP-03", "TP-04"]
of = lambda no: f"{ORDER.index(no) + 1} of {len(ORDER)}"


def bolts_on_seam():
    """16 seam bolts from a vertex: bays between the corner blocks (230) and the three 200-wide hardpoint fittings"""
    pos = []
    bays = [(230, PITCH - 100), (PITCH + 100, 2 * PITCH - 100), (2 * PITCH + 100, 3 * PITCH - 100), (3 * PITCH + 100, EDGE - 230)]
    for a, b in bays:
        n = int((b - a - 30) // 75) + 1
        f0 = (b - a - (n - 1) * 75) / 2
        pos += [a + f0 + i * 75 for i in range(n)]
    return pos


def reflect(pts, u):
    u = np.asarray(u, float); R = 2 * np.outer(u, u) - np.eye(2)
    return np.asarray(pts, float) @ R.T


def poly(ax, pts, fc, ec="k", lw=0.7, **kw):
    ax.add_patch(Polygon(np.asarray(pts, float), closed=True, fc=fc, ec=ec, lw=lw, **kw))


def rect(ax, x, y, w, h, fc, ec="k", lw=0.7, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, **kw))


# =====================================================================================================================
# RF-00 sheet index, revision history, conventions
# =====================================================================================================================
SHEETS = [
    ("RF-00", "Sheet index, revision history, conventions, baseline, open items", "27 Nov", "New on 27 Nov"),
    ("RF-01", "Main rib B and secondary rib, sections with the panes", "5 Nov; redrawn 27 Nov", "Ribs DECIDED 2 and 4 Nov"),
    ("RF-02", "Seam frame 180, glands, seam bolt, seal loop corners", "5 Nov; redrawn 27 Nov", "Frame, glands, bolt DECIDED 5 Nov; loop corners OPEN"),
    ("RF-03", "T1 test articles, overview", "5 Nov; 27 Nov", "Superseded for manufacture by TP-00 to TP-04 (8 Nov)"),
    ("RF-04", "Docking transfer lock, concept", "5 Nov; redrawn 27 Nov", "Concept, not sized"),
    ("RF-05", "Seam cross-section, hexagon to hexagon, true mitre", "8 Nov; 17 Nov; 27 Nov", "Seam DECIDED; outer glass layers OPEN-11"),
    ("RF-06", "Hexagon panel, general arrangement and parts list", "8 Nov; 17 Nov; 27 Nov", "Ribs, frame DECIDED; blocks, hardpoints PROPOSAL"),
    ("RF-07", "Seam hardpoint, the TP3 fitting at the moved position", "9 Nov; 17 Nov; 27 Nov", "Position DECIDED 10 Nov; part OPEN, to redesign"),
    ("RF-08", "Corner node: blocks, ties, dowels, results, machining", "9 Nov; 17 Nov; 27 Nov", "Block PROPOSAL; ties 180 kN DECIDED 17 Nov"),
    ("RF-09", "Pentagon panel, general arrangement, roles, docking", "8 Nov; 17 Nov; 27 Nov", "Ribs, frame DECIDED; plate side OPEN (Q57)"),
    ("TP-00", "Test pieces: cover, notes, tolerances, parts list", "8 Nov; 9 Nov; 27 Nov", "For quotation; tolerances proposed to Marco"),
    ("TP-01", "T1 frame B (glands), 180 deep", "8 Nov; 9 Nov; 27 Nov", "For quotation"),
    ("TP-02", "T1 frame A and the slice as assembled", "8 Nov; 9 Nov; 27 Nov", "For quotation"),
    ("TP-03", "550 mm seal article with the dummy hardpoint", "8 Nov; 9 Nov; 27 Nov", "For quotation; make the moved version"),
    ("TP-04", "Pull blocks and the fixture F-01 to F-03", "8 Nov; 9 Nov; 27 Nov", "For quotation; two clashes to settle first"),
]

HISTORY = [
    ("1", "5 Nov 2026", "RF-01 to RF-04", "First Rev F sheets: option B ribs, the 180 mm seam, the T1 pieces at 180 deep, the transfer lock. They replace the Rev E drafts of 24 Oct."),
    ("2", "8 Nov 2026", "RF-05 to RF-09, TP-00 to TP-04", "Seam section with the z' table, hexagon and pentagon panels, hardpoint, corner node; the five test-piece sheets and their STEP files."),
    ("3", "9 Nov 2026", "RF-06 to RF-08, TP-00 to TP-04", "Independent check: corner blocks with leaning joint faces (three fit at a vertex), hardpoint redrawn from the C3 model, test-piece solids rebuilt with drilled holes."),
    ("4", "17 Nov 2026", "RF-05 to RF-09", "Corner tie preload 180 kN (decided 17 Nov; was 198 kN). RF-08 results at 180 kN."),
    ("5", "27 Nov 2026", "All sheets", "Drawing review. No design value changed. One title block on every sheet (sheet, revision, issue date, scale, units, third-angle symbol, material, finish, tolerance note); RF-00 added; RF-01 to RF-04 redrawn from the parameter file; errors against the parameter file and the solids corrected; open items marked. Details below and in the review of 27 Nov."),
]

CHANGES_27NOV = [
    ("RF-01", "The main rib panes now sit on the P-04 seat ledges at z 170-180 (they were drawn under the cabin flange at z 400); glass bite on the main rib 24.9, not 40.9."),
    ("RF-02", "Frame section matches P-06 / P-06H: seat lip at the cabin face (z 170-180). The Rev E third flange and the 10 x 10 conduit (dropped in Rev S) removed."),
    ("RF-03", "Marked superseded by TP-00 to TP-04; names and bolt positions now match the STEP files (bolts 50 mm from the dummy fitting, not 31.25)."),
    ("RF-05", "Web drawn at its true 180 mm panel depth (joint face 192.7 long), so it meets the lip; detail A at 2:1; notes kept inside the sheet."),
    ("RF-06", "Scale stated is the scale drawn (1:25; it said 1:20); bite on the main rib 24.9; masses use each part's own material, not 6061."),
    ("RF-07", "Joint face turned so the space side is at the top, as on RF-05; fitting bodies at z' -6.5 to 123.5 as in the solids (drawn 11 to 141)."),
    ("RF-08", "Block plan from the CB-01 builder; joint face drawn true (leans 11.64 deg); dowels in the tie columns at 130 / 186, as in the solid (drawn at 50 / 210); 198 kN results labelled as the earlier value."),
    ("RF-09", "Scale 1:25 as drawn; docking label moved off the hatching; text kept inside the sheet."),
    ("TP-00 to 04", "TP-01 leg holes dimensioned from the joint face (160 / 200); the section scale is 1:2 (it said 1:1). TP-03 leak port at mid-length as in the STEP. TP-04 lug-screw rows dimensioned from the block (32 / 64; they were 42 / 74 measured from the block edge). Clashes marked."),
]

OPEN_ITEMS = [
    "Hardpoint fitting: redesign it to fit the 180 mm frame; it runs into the outer flange and the secondary ribs and its pins cannot be put in (RF-07).",
    "Seal loop corners at the seam ends: drawn R4.3 on the test pieces, Parker asks R16 at least (R32 target); the bolt row cannot move to make room (RF-02, Q92).",
    "Corner tie tightening tolerance: hold 180 kN or just above (160 kN opens the faces 0.81 mm); the band and the stretch method are not set (RF-08).",
    "Corner block stress limit: 236 MPa (95th percentile) at the earlier 198 kN, and no allowable set for the block (RF-08).",
    "Found on 27 Nov: TP-04 lug-screw holes break into the leg-screw holes on the 75 and 150 blocks, and F-01's M12 x 45 screws are longer than the 20 mm tapped holes (TP-04).",
    "Found on 27 Nov: frame-side pane bite with the 56.6 mm hexagon lip (OPEN-17): the old note says 20.0 mm, the pane as drawn has 46.6 mm; the rule for where frame-side panes are cut is not in the parameter file (RF-05).",
    "Found on 27 Nov: the P-04A cap angle solid is 58 mm per leg (inner flange 124 wide, not 100); the parameter file calls P-04A the pentagon main rib, the library calls it the cap angle.",
]


def rf00(pdf):
    fig, Pp = K.new_sheet("RF-00", "Sheet index, revision history and conventions", status="Index of the Rev F drawing set as issued 27 Nov 2026. No design value is changed in this issue.",
                          part="Rev F drawing set, 15 sheets", material="-", finish="-", scale="No views", banner="INDEX. FLIGHT SHEETS NOT FOR MACHINING", sheet_of=of("RF-00"))
    x0, y = 15.0, 284.0
    y = heading(Pp, x0, y, "Sheets in the Rev F set")
    y = table(Pp, x0, y, (15, 82, 36, 72), [("Sheet", "Title", "Issued", "Status")] + [s for s in SHEETS], fs=7.5)
    y -= 5
    y = heading(Pp, x0, y, "Revision history (all Rev F; the design baseline did not change between issues 4 and 5)")
    y = table(Pp, x0, y, (11, 21, 40, 133), [("Issue", "Date", "Sheets", "What changed")] + HISTORY, fs=7.5)
    y -= 5
    y = heading(Pp, x0, y, "Corrections in issue 5 (27 Nov)")
    y = table(Pp, x0, y, (20, 185), [("Sheet", "Correction")] + CHANGES_27NOV, fs=7.5, header=True)
    # right column
    xr, yr, wr = 228.0, 284.0, 177.0
    yr = heading(Pp, xr, yr, "The Rev F baseline (from hcsa_params_revF.json)")
    base = (f"- Shell: truncated icosahedron, {DIAM:,.0f} mm across, edge {EDGE:,.0f} mm; 32 panels (20 glass hexagons, 12 pentagons), 90 seams, 60 corner nodes.\n"
            f"- Cabin {PRE['pressure_atm'][0]} atm, {PRE['o2_fraction'][0]*100:.0f} % oxygen; design pressure {PRE['design_pressure_psia'][0]} psia with our own relief valve; hatch-open case 15.2 psia. Factors {1.5} at proof, {PRE['ultimate_factor'][0]} at ultimate.\n"
            f"- Pressure pane {TP:g} mm BOROFLOAT 33, {CUT:g} mm, {v('pane', 'per_hexagon')} per hexagon, on 2 mm setting strips.\n"
            f"- Edge frame {D:g} deep, web {WEB:g}, flange {FL_W:g} x {FL_T:g}, seat lip {LIP_H:g} (hexagon, OPEN-17) / {LIP_P:g} (pentagon) at the cabin face.\n"
            f"- Main rib option B, I {MR['d']:g} x {MR['bf']:g} x {MR['tf']:g}, web {MR['tw']:g}; secondary rib I {SR['d']:g} x {SR['bf']:g} x {SR['tf']:g}, web {SR['tw']:g}; k {KGRID} grid at {PITCH:g} mm.\n"
            f"- Seam: two loops of Parker BA500 butyl in {GW:g} x {GD:g} glands at z' {Z1:g} and {Z2:g}, RTV566 bead at z' {ZR:g}; NAS6705U27 bolt with KFN670 nut at {v('seam_bolt','preload_kN'):g} kN, one row at z' {ZB:g}, {v('seam_bolt','per_seam')} per seam.\n"
            f"- Corner ties 7/8-14 Inconel 718, four per face, {TIE_PRE:g} kN (decided 17 Nov; 198 kN is the earlier value), limit {TIE_LIM:g} kN.\n"
            f"- Hardpoints: three per seam at the quarter points; the fitting on the line of the pull, z' 46 to 106 (decided 10 Nov).")
    yr = note(Pp, xr, yr, wr, base, fs=7.5) - 3
    yr = heading(Pp, xr, yr, "Conventions")
    conv = ("- Units mm, angles in degrees, Ø diameter. Third-angle projection.\n"
            "- z is panel depth, square to the panel: z 0 the outer (space) face, z 180 the pane seat plane, z 400 the cabin face of the main rib and corner block.\n"
            f"- z' is depth along the leaning joint face from the shell edge: z = z' x cos(mitre), {math.cos(math.radians(MH)):.4f} on a hexagon (mitre {MH:.3f} deg), {math.cos(math.radians(MP)):.4f} on a pentagon ({MP:.3f} deg).\n"
            "- Frame A has the flat joint face, frame B the glands. A pentagon is always B; between two hexagons the lower number is A.\n"
            "- Status: LOCKED spec; DECIDED by Manos (dated); PROPOSAL drawn to carry a load from the models, not yet tested or signed; OPEN not decided, default stated; STUDY studied, not drawn.\n"
            "- A superseded value shown for comparison is labelled as the earlier value.\n"
            "- Flight sheets are not for machining. Test-piece sheets are for quotation: the STEP files govern the geometry.")
    yr = note(Pp, xr, yr, wr, conv, fs=7.5) - 3
    yr = heading(Pp, xr, yr, "Open items that need a decision", color=RED)
    note(Pp, xr, yr, wr, "\n".join(f"- {t}" for t in OPEN_ITEMS), fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-00_index.png")


# =====================================================================================================================
# RF-01 main rib B and the secondary rib, sections with the panes
# =====================================================================================================================
def _pane_pair(ax, half, xc=0.0, z0=180.0):
    """two panes cut SHORT from the rib centre line, 2 mm setting strips, 21 mm glass (z 180-203), out to +-half"""
    for s in (-1, 1):
        a, b = xc + s * SHORT, xc + s * half
        rect(ax, min(a, b), z0, abs(b - a), 2.0, "#444", ec="none")
        rect(ax, min(a, b), z0 + 2.0, abs(b - a), TP, GLS, ec=BLU, lw=0.6)


def rf01(pdf):
    fig, Pp = K.new_sheet("RF-01", "Main rib B and secondary rib, sections with the panes", status="Main rib option B DECIDED 4 Nov; secondary rib DECIDED 2 Nov; pane 21 mm DECIDED 5 Nov; rib brace P-11 PROPOSAL; launch restraint of the panes OPEN.",
                          part="P-04 + 2 x P-04A main rib; P-01 secondary rib; P-07 pane", material="6061-T6 ribs; BOROFLOAT 33 panes",
                          finish="As extruded / machined; Ra 3.2 on seats", scale="1:2; plan 1:25", sheet_of=of("RF-01"))
    tw, tf, bf, d = MR["tw"], MR["tf"], MR["bf"], MR["d"]
    # ---- main rib, section across, z down the page
    ax = view(fig, (14, 50, 182, 220), 2.0, (-22, 207), flip_y=True, title="Section B-B across the main rib, option B, with the panes  (1:2)")
    rect(ax, -bf / 2, 0, bf, tf, MET2)                                   # outer flange
    rect(ax, -tw / 2, tf, tw, d - tf, MET2)                              # web to the cabin face
    for s_ in (-1, 1):
        rect(ax, (tw / 2 if s_ > 0 else -tw / 2 - LEDGE_W), 180 - LEDGE_T, LEDGE_W, LEDGE_T, MET2)        # seat ledges z 170-180
        poly(ax, [(s_ * tw / 2, d - CAP_V), (s_ * (tw / 2 + CAP_T), d - CAP_V), (s_ * (tw / 2 + CAP_T), d - tf), (s_ * (tw / 2 + CAP_H), d - tf),
                  (s_ * (tw / 2 + CAP_H), d), (s_ * tw / 2, d)], "#b0b7be")                              # P-04A
    ax.add_patch(Rectangle((-tw / 2 - CAP_T, 360 - 4.8), 2 * CAP_T + tw, 9.6, fc="none", ec="k", lw=0.4, ls="--"))
    _pane_pair(ax, 150)
    cl(ax, (0, -12), (0, d + 14))
    dim(ax, (-bf / 2, 0), (bf / 2, 0), f"{bf:g}", off=7)
    dim(ax, (bf / 2, 0), (bf / 2, tf), f"{tf:g}", off=6, inside=False)
    dim(ax, (-bf / 2, 0), (-bf / 2, d), f"{d:g}", off=-57.5, text_side=-30)
    dim(ax, (-bf / 2, 0), (-bf / 2, 180), "180 seat plane", off=-18)
    dim(ax, (-tw / 2, 100), (tw / 2, 100), f"web {tw:g}", off=0, inside=False, text_side=9)
    dim(ax, (tw / 2, 170), (tw / 2 + LEDGE_W, 170), f"{LEDGE_W:g}", off=6)
    dim(ax, (tw / 2 + LEDGE_W, 170), (tw / 2 + LEDGE_W, 180), f"{LEDGE_T:g}", off=4, inside=False)
    dim(ax, (SHORT, 203), (tw / 2 + LEDGE_W, 203), f"bite {tw/2 + LEDGE_W - SHORT:.1f}", off=-7, inside=False, text_side=14)
    dim(ax, (0, 203), (SHORT, 203), f"{SHORT:g}", off=-14, inside=False, text_side=-9)
    dim(ax, (150, 182), (150, 203), f"{TP:g}", off=6, inside=False)
    dim(ax, (tw / 2, d), (tw / 2 + CAP_H, d), f"{CAP_H:g}", off=-7)
    dim(ax, (tw / 2 + CAP_T, d - CAP_V), (tw / 2 + CAP_T, d), f"{CAP_V:g}", off=26)
    dim(ax, (tw / 2 + CAP_H, d - tf), (tw / 2 + CAP_H, d), f"{tf:g}", off=5, inside=False)
    dim(ax, (-tw / 2 - CAP_T, d - 50), (-tw / 2, d - 50), f"{CAP_T:g}", off=0, inside=False, text_side=-9)
    leader(ax, (-tw / 2 - CAP_T / 2, 320), (-160, 290), "cap angle P-04A (two make the\n100 wide inner flange)", ha="left")
    leader(ax, (-10, 360), (-160, 345), "3/8-24 A286 cap bolts at z 360,\n90 pitch, fitted after the glass", ha="left")
    leader(ax, (-25, 175), (-160, 140), "seat ledge 30 x 10, one piece\nwith the P-04 web", ha="left")
    leader(ax, (90, 192), (60, 255), "21 mm BOROFLOAT 33 pane on a 2 mm\nsetting strip, cut 9.09 short of the\nrib centre line", ha="left")
    label(ax, (-160, -8), "space side (z 0)", col=GREY, ha="left"); label(ax, (-160, d + 6), "cabin side (z 400)", col=GREY, ha="left")
    # ---- secondary rib
    ax2 = view(fig, (204, 146, 130, 118), 2.0, (-5, 104), flip_y=True, title="Section C-C across a secondary rib, with the panes, space side at the top  (1:2)")
    d2, b2, t2, w2 = SR["d"], SR["bf"], SR["tf"], SR["tw"]
    rect(ax2, -b2 / 2, 0, b2, t2, MET2); rect(ax2, -w2 / 2, t2, w2, d2 - 2 * t2, MET2); rect(ax2, -b2 / 2, d2 - t2, b2, t2, MET2)
    _pane_pair(ax2, 110)
    cl(ax2, (0, -10), (0, 215))
    dim(ax2, (-b2 / 2, 0), (b2 / 2, 0), f"{b2:g}", off=6)
    dim(ax2, (-b2 / 2, 0), (-b2 / 2, d2), f"{d2:g}", off=-10)
    dim(ax2, (b2 / 2, 0), (b2 / 2, t2), f"{t2:g}", off=5, inside=False)
    dim(ax2, (-w2 / 2, 90), (w2 / 2, 90), f"web {w2:g}", off=0, inside=False, text_side=9)
    dim(ax2, (SHORT, 203), (b2 / 2, 203), f"bite {b2/2 - SHORT:.1f}", off=-7, inside=False, text_side=13)
    dim(ax2, (b2 / 2, 170), (b2 / 2, 180), f"{t2:g}", off=5, inside=False)
    # ---- plan of the main rib's cabin flange: the brace stations
    ax3 = view(fig, (40, 20, 110, 16), 25.0, (1125, 0), title="Main rib, plan of the cabin flange (1:25): a brace at every secondary rib crossing")
    ax3.plot([0, EDGE], [0, 0], lw=3.0, c="#7f8a94", solid_capstyle="butt")
    for i in range(5):
        ax3.add_patch(Rectangle((i * PITCH - 30, -45), 60, 90, fc=TI if 0 < i < 4 else STEEL, ec="k", lw=0.4))
    for i, t in enumerate(("corner block", "P-11", "P-11", "P-11", "hub")):
        label(ax3, (i * PITCH, -125), t, fs=7.5, bg=False)
    dim(ax3, (0, 50), (PITCH, 50), f"{PITCH:g}", off=2)
    # ---- notes
    nt = (f"- Glass bite at least {BITE_MIN:g} mm on every seat: secondary rib {SR['bf']/2 - SHORT:.1f}, main rib {tw/2 + LEDGE_W - SHORT:.1f} on the 30 mm ledges. "
          f"The pane edge clears the web by {SHORT - SR['tw']/2:.1f} (secondary) and {SHORT - tw/2:.1f} (main).\n"
          "- Option A (I 450 x 150 x 25, web 10, parts P-10 / P-10A) is superseded and kept for the record only.\n"
          "- Main rib B yields at 1.96 atm; at the 0.8 atm cabin the ultimate case is 1.67 atm (factor 2.0 on 12.3 psia). Open glass straight on, with these ribs and a 60 mm frame band: 60.9 % of a hexagon.\n"
          "- REQUIREMENT (survival check, 4 Nov): unbraced over 2.25 m the main rib buckles sideways at 0.79 of the load it must carry; braced every 562.5 mm it has 8.4 times margin. "
          "The P-11 brace pair (RF-08) holds the cabin flange sideways at every secondary rib crossing.\n"
          "- LAUNCH (OPEN): packed outer face down at 6 g each pane pulls off its seat with about 0.35 kN. Pack the panels outer face up, or rate the P-08 pane clamps for 6 g plus random vibration.\n"
          "- Corrected 27 Nov: the 5 Nov sheet drew the main-rib panes under the cabin flange at z 400 with 40.9 mm of bite. In the decided P-04 the panes sit on the seat ledges at z 170-180, "
          "level with the secondary ribs, and the bite is 24.9 mm. The library solid of P-04A has 58 mm horizontal legs (124 wide in all); drawn here at 46 (100 wide), the decided section.")
    y = heading(Pp, 204, 140, "Notes")
    note(Pp, 204, y, 202, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-01_ribs.png")


# =====================================================================================================================
# RF-02 seam frame 180, glands, seam bolt, seal loop corners (straight section)
# =====================================================================================================================
def _frame_straight(ax, side, lip, glands, fc):
    """frame member drawn straight (mitre not shown). side -1: frame A at x <= 0; side +1: frame B at x >= 0."""
    s = side
    rect(ax, min(0, s * WEB), 0, WEB, D, fc)
    xi = s * WEB
    rect(ax, min(xi, xi + s * FL_W), 0, FL_W, FL_T, fc)
    rect(ax, min(xi, xi + s * lip), D - FL_T, lip, FL_T, fc)
    for zz, sg in ((FL_T, 1), (D - FL_T, -1)):                          # R6 inside corners, as on the test pieces (OPEN-5)
        cx = xi + s * 6; cy = zz + sg * 6
        ax.add_patch(Rectangle((min(xi, xi + s * 6), min(zz, zz + sg * 6)), 6, 6, fc=fc, ec="none"))
        ax.add_patch(Wedge((cx, cy), 6, 0, 360, fc="white", ec="none"))
        th1 = {(1, 1): 180, (1, -1): 90, (-1, 1): 270, (-1, -1): 0}[(s, sg)]
        ax.add_patch(Arc((cx, cy), 12, 12, theta1=th1, theta2=th1 + 90, lw=0.7, color="k"))
    if glands:
        for zc in (Z1, Z2):
            rect(ax, 0, zc - GW / 2, GD, GW, "white", lw=0.5)
            ax.add_patch(Ellipse((GD / 2, zc), 4.0, 6.6, fc=SEAL, ec="none"))
        ax.add_patch(Wedge((0, ZR), 3.0, -90, 90, fc="#7a5", ec="k", lw=0.4))
        rect(ax, 0, ZPORT - 1, WEB, 2, "white", lw=0.4)
        rect(ax, WEB - 8, ZPORT - 2.1, 8, 4.2, "white", lw=0.4)


def _bolt_through(ax, zb=None):
    zb = ZB if zb is None else zb
    rect(ax, -WEB, zb - BOLT_HOLE / 2, 2 * WEB, BOLT_HOLE, "white", lw=0.5)
    rect(ax, -WEB - 1.6 - 9.0, zb - 3.97, 2 * WEB + 3.2 + 9.0 + 4.9, 7.94, "#666", lw=0.4)
    rect(ax, WEB + 1.6, zb - 7.35, 4.9, 14.7, "#888", lw=0.4)                 # head on frame B
    rect(ax, -WEB - 1.6 - 9.0, zb - 7.35, 9.0, 14.7, "#888", lw=0.4)          # KFN670 nut on frame A
    for xw in (WEB, -WEB - 1.6):
        rect(ax, xw, zb - 8.0, 1.6, 16.0, "#bbb", lw=0.3)


def rf02(pdf):
    fig, Pp = K.new_sheet("RF-02", "Seam frame 180, glands, seam bolt, seal loop corners", status="Frame 180, glands 7.1 x 4.0 and bolt NAS6705U27 at 4 kN DECIDED 5 Nov; bolt row z' 58 kept 5 Nov; seal loop corners OPEN (Q92); flight alloy OPEN.",
                          part="P-06H / P-06P frame members at a seam, drawn straight", material="6061-T651 (tests); flight alloy OPEN (checks at 6061-T6)",
                          finish="Joint face and gland faces Ra 0.8; elsewhere Ra 3.2", scale="1:1; loop ends 1:2", sheet_of=of("RF-02"))
    ax = view(fig, (14, 36, 200, 236), 1.0, (0, 92), flip_y=True, title="Section D-D through a seam bolt, normal to the joint plane, drawn straight (the mitre is on RF-05)  (1:1)")
    _frame_straight(ax, -1, LIP_H, False, MET3)
    _frame_straight(ax, +1, LIP_H, True, MET2)
    _bolt_through(ax)
    cl(ax, (0, -14), (0, D + 14), col=RED)
    label(ax, (-45, -16), "frame A (flat joint face)", fs=8, bg=False); label(ax, (45, -16), "frame B (glands)", fs=8, bg=False)
    label(ax, (0, D + 19), "joint plane (radial)", col=RED, fs=8, bg=False)
    # ordinate dimensions of z' from the shell edge, on the left
    xo = -84
    ax.plot([xo, xo], [0, D], lw=0.5, c="k")
    for zz, t in ((0, "0"), (Z1, f"{Z1:g}"), (ZPORT, f"{ZPORT:g}"), (Z2, f"{Z2:g}"), (ZR, f"{ZR:g}"), (ZB, f"{ZB:g}"), (D - FL_T, f"{D - FL_T:g}"), (D, f"{D:g}")):
        ax.plot([xo - 3, -1 if zz not in (0, D, D - FL_T) else -WEB - (LIP_H if zz != 0 else FL_W) - 1], [zz, zz], lw=0.3, c="k")
        label(ax, (xo - 4, zz), t, fs=7.5, ha="right", bg=False)
    label(ax, (xo - 4, -8), "z'", fs=7.5, ha="right", bg=False)
    dim(ax, (WEB, 0), (WEB + FL_W, 0), f"{FL_W:g}", off=7)
    dim(ax, (WEB + FL_W, 0), (WEB + FL_W, FL_T), f"{FL_T:g}", off=5, inside=False)
    dim(ax, (WEB, D), (WEB + LIP_H, D), f"{LIP_H:g} hexagon lip ({LIP_P:g} pentagon), OPEN-17", off=-8)
    dim(ax, (0, D), (WEB, D), f"{WEB:g}", off=-8, inside=False, text_side=-9)
    leader(ax, (GD, Z1 - 2), (54, 14), f"two glands {GW:g} x {GD:g},\nbottom R0.5-0.9; BA500 butyl\ncord {CORD:.2f}, 25 % squeeze", ha="left", fs=7.5)
    leader(ax, (WEB - 4, ZPORT), (54, 33), "leak port Ø2, M5 x 8\nfrom the back", ha="left", fs=7.5)
    leader(ax, (2.5, ZR), (54, 47), "RTV566 bead, R3 recess", ha="left", fs=7.5)
    leader(ax, (WEB + 6.5, ZB + 5), (54, 68), f"NAS6705U27 + KFN670 nut,\nA286, {v('seam_bolt','preload_kN'):g} kN by torque; hole\nØ{BOLT_HOLE:g} (tests: Ø8.5 drilled)", ha="left", fs=7.5)
    leader(ax, (WEB + 2.5, D - FL_T - 2.5), (54, 98), "inside corners R6, as on\nthe test pieces (OPEN-5)", ha="left", fs=7.5)
    leader(ax, (WEB + 40, D - 5), (54, 140), "seat lip at the cabin face,\nz 170-180; the pane sits on\nits cabin side on a 2 mm strip", ha="left", fs=7.5)
    # ---- seal loop ends (three options)
    xL, w, gapx = 222.0, 58.0, 5.0
    note(Pp, xL, 272, 184, "Seal loop ends on frame B's joint face, at a corner block or a fitting  (1:2). Which layout we build waits on Parker's 'two loops' answer.", fs=8.5, bold=True)
    opts = [("As drawn on the test pieces:\none racetrack, cords 14 apart,\ninner R 4.3", RED, 4.33, ZB, "bolt z' 58"),
            ("Inner R16, Parker minimum\n(3 x cord section)", ORG, 16.0, 69.0, "bolt z' 69: fails D1\n(z' 70 tested 5 Nov)"),
            ("Inner R32, Parker target\n(6 x cord section)", GRN, 32.0, 101.0, "bolt z' 101: fails D1\n(z' 70 tested 5 Nov)")]
    for i, (ttl, colr, r_in, zbolt, btxt) in enumerate(opts):
        axo = view(fig, (xL + i * (w + gapx), 160, w, 92), 2.0, (-40, 70), flip_y=True)
        rect(axo, -100, 0, 100, 175, MET3, lw=0.5)
        axo.plot([0, 0], [0, 175], lw=1.4, c="k")
        rc = r_in + CORD / 2                       # cord centre-line radius
        z_top, z_bot = Z1, Z1 + 2 * rc
        xc = -rc - 8
        axo.plot([-100, xc], [z_top, z_top], lw=CORD * 0.55, c=SEAL, solid_capstyle="butt")
        axo.plot([-100, xc], [z_bot, z_bot], lw=CORD * 0.55, c=SEAL, solid_capstyle="butt")
        axo.add_patch(Arc((xc, (z_top + z_bot) / 2), 2 * rc, 2 * rc, theta1=-90, theta2=90, lw=CORD * 0.55, color=SEAL))
        axo.add_patch(Circle((-48, zbolt), BOLT_HOLE / 2 + 2.5, fc="#888", ec="k", lw=0.4))
        label(axo, (-48, zbolt + 14), btxt, fs=7.5, col=colr if i else "k")
        label(axo, (-50, -8), ttl, fs=7.5, col=colr, va="bottom", bg=False)
        label(axo, (-4, 162), "seam end", fs=7.5, ha="right", bg=False)
    Pp.text(xL, 152, "z' runs down the page; the vertical line on the right is the seam end (corner block or fitting face).", fontsize=7.5, va="top", color=GREY)
    nt = ("What the check says\n"
          "- If each seam's two cords are one racetrack joined at the seam ends, the ends turn at an inner radius of 4.3 mm. That breaks Parker's rule of R16 minimum.\n"
          "- A racetrack with an inner R16 end needs its legs 37.3 mm apart, which pushes the bolt row from z' 58 to z' 70 or more (z' 102 for R32). "
          "The D1 run of 5 Nov says no: at z' 70 the seal gap is 0.111 mm at 2.48 kN per bolt, on the 0.11 limit (3.75 kN at z' 58). The bolt row stays at z' 58.\n"
          "- If each cord is its own closed loop round the whole panel (the Rev B intent), the turns are at the vertices, 60 deg on a hexagon and 72 deg on a pentagon, "
          "through the corner block and the O10 corner seal. That needs the block's CAD and is not checked here.\n"
          "- Next: draw the loop path through the corner block (turn the loop round the end bolt, or widen the frame flange locally at the panel corners) after Parker answers.\n"
          "Corrected 27 Nov: the 5 Nov sheet drew a third flange with the seat lip at mid-depth and a 10 x 10 conduit. That was the Rev E stack; the conduit was dropped in Rev S. "
          "The section is now the P-06 / P-06H section: outer flange at z 0-10 and the seat lip at the cabin face, z 170-180.")
    note(Pp, xL, 145, 185, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-02_seam_frame.png")


# =====================================================================================================================
# RF-03 T1 test articles, overview (superseded for manufacture by TP-00 to TP-04)
# =====================================================================================================================
def _tp_bolts(L, hardpoint):
    if hardpoint:
        bay = L / 2 - 100.0; n = int((bay - 60) // 75) + 1; f0 = (bay - (n - 1) * 75) / 2
        return [f0 + i * 75 for i in range(n)] + [L - f0 - i * 75 for i in range(n)]
    nb = int(round(L / 75)); return [L / 2 + (i - (nb - 1) / 2) * 75 for i in range(nb)]


def rf03(pdf):
    fig, Pp = K.new_sheet("RF-03", "T1 test articles at 180 deep, overview", status="SUPERSEDED for manufacture by TP-00 to TP-04 and the STEP files (8 and 9 Nov). Kept so the set is complete.",
                          part="T1-075, T1-150, T1-225, SA-550 (frame B joint faces)", material="6061-T651", finish="See TP-00",
                          scale="1:5", banner="SUPERSEDED: USE TP-00 TO TP-04", banner_col=ORG, sheet_of=of("RF-03"))
    names = [("T1-075", 75, False), ("T1-150", 150, False), ("T1-225", 225, False), ("SA-550-HPmoved", 550, True)]
    x = 18.0
    for nm, L, hp in names:
        w = L / 5 + 14
        ax = view(fig, (x, 150, w, 60), 5.0, (L / 2, 90), flip_y=True)
        rect(ax, 0, 0, L, D, MET2, lw=0.7)
        for zc in (Z1, Z2): ax.plot([0, L], [zc, zc], lw=1.0, c=SEAL)
        ax.plot([0, L], [ZR, ZR], lw=0.5, c="k", ls=":")
        for yb in _tp_bolts(L, hp): ax.add_patch(Circle((yb, ZB), 4.25, fc="white", ec="k", lw=0.5))
        if hp:
            for j in (-1, 0, 1): ax.add_patch(Circle((L / 2 + 60 * j, 76), 20, fc="white", ec="k", lw=0.6))
            ax.add_patch(Rectangle((L / 2 - 100, 46), 200, 60, fill=False, ec=GRN, ls="--", lw=0.7))
        ax.add_patch(Circle((L / 2, ZPORT), 1.5, fc="white", ec="k", lw=0.4))
        bl = sorted(_tp_bolts(L, hp))
        Pp.text(x + w / 2, 202, nm, fontsize=8, weight="bold", ha="center", va="bottom")
        Pp.text(x + w / 2, 159, f"{len(bl)} seam bolt{'s' if len(bl) > 1 else ''} at\n" + ", ".join(f"{b:g}" for b in bl), fontsize=7.5, ha="center", va="top")
        x += w + 8
    Pp.text(18, 228, "Joint faces of frame B, space side (z 0) at the top: glands z' 18 and 32, RTV recess z' 42 (dotted), leak port z' 25 at mid-length, seam bolts z' 58. "
            "SA-550 drawn with the dummy fitting moved onto the pull line (bores Ø40 at z 76, envelope z 46-106, dashed).", fontsize=8, va="top")
    Pp.add_patch(Rectangle((18, 238), 300, 28, fc="#fff4e0", ec=ORG, lw=1.0))
    Pp.text(24, 258, "SUPERSEDED FOR MANUFACTURE", fontsize=14, weight="bold", color=ORG, va="center")
    Pp.text(24, 246, "Make the test pieces from TP-00 to TP-04 and the STEP files (zip of 9 Nov). This overview stays in the set so the sheet numbers run on.",
            fontsize=8.5, va="center")
    nt = ("What changed from the Rev E draft sheets RE-01 and RE-02\n"
          "- Frame depth 140 to 180 on every T1 frame, so the test matches the station frame (decided 5 Nov). Stock 6061-T651 plate; check the blank with the shop.\n"
          "- Glands 7.1 x 4.0 (decided 5 Nov). The cord ends at the slice ends follow RF-02: no tight racetrack end; use R16 at least or dam the ends.\n"
          "- Bolts NAS6705U27 + KFN670 at 4 kN by torque (decided 5 Nov), row at z' 58.\n"
          "- The 550 article carries the dummy hardpoint of RE-03 rev B: no bolt inside the 200 mm fitting, 2 + 2 bolts at 75 pitch in the two 175 mm bays, centred, 50 mm from the fitting's faces. It is pulled through pinned lugs.\n"
          "- The pull blocks keep the RE-03 rev B interface; their holes move with the 40 mm deeper frame (TP-04).\n"
          "Corrected 27 Nov: the 5 Nov sheet called the pieces RE-01-75 to RE-02-550 and put the 550 article's bolts 31.25 mm off the fitting. The names and positions above are the ones in the STEP files and on TP-00 to TP-04.")
    note(Pp, 18, 128, 210, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-03_T1_overview.png")


# =====================================================================================================================
# RF-04 docking transfer lock, concept
# =====================================================================================================================
def rf04(pdf):
    fig, Pp = K.new_sheet("RF-04", "Docking transfer lock, concept", status="Concept, Rick to agree; volumes, valve sizes and the hatch are not sized; the host operator has to agree to a hatch-shut interface.",
                          part="Transfer lock between HCSA and the host station", material="-", finish="-", scale="Not to scale (schematic)", banner="CONCEPT. NOT A DESIGN", banner_col=ORG,
                          sheet_of=of("RF-04"))
    from matplotlib.patches import FancyBboxPatch
    def box(x, y, w, h, fc, ec, txt, ls="-"):
        Pp.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12", fc=fc, ec=ec, lw=1.2, ls=ls))
        Pp.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=10, linespacing=1.4)
    box(25, 130, 140, 100, "#e8f2fa", BLU, f"HCSA facility (module)\n{PRE['pressure_atm'][0]} atm (11.8 psia), {PRE['o2_fraction'][0]*100:.0f} % oxygen\ndesign pressure {PRE['design_pressure_psia'][0]} psia")
    Pp.add_patch(Rectangle((186, 155), 70, 50, fc="#fdf1e1", ec=ORG, lw=1.0, ls="--"))
    Pp.text(221, 180, "transfer lock\nabout 2 m³, concept", ha="center", va="center", fontsize=9)
    box(277, 130, 125, 100, "#eeeeee", "#555", "host station\nOrbital Reef class\n1 atm, about 15.2 psia")
    for xh, nm, sub in ((168, "hatch A", "shut whenever the\npressures differ"), (260, "hatch B", "host side")):
        Pp.add_patch(Rectangle((xh, 158), 8 if xh == 168 else 7, 44, fc="#444", ec="k", lw=0.5))
        Pp.text(xh + 4, 222, nm, ha="center", va="bottom", fontsize=8, weight="bold")
        Pp.text(xh + 4, 220.5, sub, ha="center", va="top", fontsize=7.5)
    Pp.add_patch(Circle((60, 230), 5, fc=RED, ec="k", lw=0.5))
    Pp.annotate("module relief valve, cracks at 12.0-12.3 psid, sized for the worst inflow\nfrom the host side (a valve stuck open, a leaking hatch seal)", (60, 235), (30, 262), fontsize=8,
                arrowprops=dict(arrowstyle="-|>", lw=0.5, mutation_scale=6))
    Pp.annotate("equalising valve, flow-limited,\nbleeds into the module", (190, 157), (150, 105), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.5, mutation_scale=6))
    Pp.annotate("equalising valve, host side", (252, 157), (290, 105), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-|>", lw=0.5, mutation_scale=6))
    nt = ("Rules this concept has to keep (from the 3 Nov lower-pressure note)\n"
          "- The module has its own relief valve, cracking at about 12.0-12.3 psid, big enough for the worst inflow from the 1 atm side.\n"
          "- Hatch A stays shut whenever the pressures differ, held by the pressure difference and by an interlock.\n"
          "- The lock does the stepping through flow-limited valves: about 6-10 minutes at 0.3-0.5 psi per minute, slowest on the way back up to 1 atm.\n"
          "- The module never takes its air from the host. Volumes, valve sizes and the hatch are not sized; the host operator has to agree to a hatch-shut interface.\n"
          "- The hatch-open case (cabin at 1 atm, 15.2 psia) is the case the corner node and seams are checked against (RF-08). The docking pentagon is on RF-09.")
    note(Pp, 25, 85, 200, nt, fs=8)
    K.save(fig, pdf, f"{OUT}/RF-04_transfer_lock.png")


# =====================================================================================================================
# RF-05 seam cross-section, true mitre
# =====================================================================================================================
def _seam_geometry(m_deg, lip):
    """panel-B frame section with the true leaning web: x across (panel B at -x), y = panel depth z (down the page)"""
    m = math.radians(m_deg); tm, cm, sm = math.tan(m), math.cos(m), math.sin(m)
    wh = WEB / cm                                            # web thickness in a section parallel to the panel
    xin = lambda z: -wh - z * tm                             # web inner face at depth z
    web = [(0, 0), (-D * tm, D), (xin(D), D), (xin(0), 0)]
    fl = [(xin(0), 0), (xin(0) - FL_W, 0), (xin(0) - FL_W, FL_T), (xin(FL_T), FL_T)]
    lp = [(xin(D - FL_T), D - FL_T), (xin(D - FL_T) - (xin(D - FL_T) - xin(D)) - lip, D - FL_T), (xin(D) - lip, D), (xin(D), D)]
    lp = [(xin(D - FL_T), D - FL_T), (xin(D) - lip, D - FL_T), (xin(D) - lip, D), (xin(D), D)]
    u = np.array([-sm, cm]); nB = np.array([-cm, -sm])      # along the joint face (z' down), and into panel B
    jp = lambda s, off=0.0: s * u + off * nB
    return dict(m=m, tm=tm, cm=cm, sm=sm, wh=wh, xin=xin, web=web, fl=fl, lp=lp, u=u, nB=nB, jp=jp)


def rf05(pdf):
    fig, Pp = K.new_sheet("RF-05", "Seam cross-section, hexagon to hexagon, true mitre", status="Frame 180, glands, bolt DECIDED 5 Nov; hardpoint position DECIDED 10 Nov; outer glass layers L1-L6 OPEN-11; hexagon lip 56.6 OPEN-17.",
                          part="P-06H frame members at a hexagon-hexagon seam", material="6061-T651 (tests); flight alloy OPEN",
                          finish="Joint face and glands Ra 0.8; elsewhere Ra 3.2", scale="1:2; detail A 2:1", sheet_of=of("RF-05"))
    G = _seam_geometry(MH, LIP_H); u, nB, jp, xin = G["u"], G["nB"], G["jp"], G["xin"]
    ax = view(fig, (12, 131, 262, 149), 2.0, (-40, 109), flip_y=True,
              title="Section E-E normal to a hexagon-hexagon seam at the first bolt, 271.25 from the vertex; space side at the top  (1:2)")
    TB = lambda p: np.asarray(p, float); TA = lambda p: reflect(p, u)
    for T, col in ((TB, MET2), (TA, MET3)):
        for part in (G["web"], G["fl"], G["lp"]):
            poly(ax, T(part), col, lw=0.7)
    xe = -250
    layers = [(12, 18, 8, "#dff1fa", BLU, 0.5), (40, 43.3, 8, "#e8f4fb", BLU, 0.4), (50, 53.3, 8, "#e8f4fb", BLU, 0.4), (95, 115, 8, "#f3f3f3", "#888", 0.4),
              (180, 182, 10, "#444", "none", 0), (182, 182 + TP, 10, GLS, BLU, 0.7), (230, 236, 10, "#fff6e0", "#aa8", 0.5)]
    for z0, z1, gap, fc, ec, lw in layers:
        xa = min(xin(z0), xin(z1)) - gap if z0 < 180 else xin(180) - gap
        pts = [(xa, z0), (xe, z0), (xe, z1), (xa, z1)]
        for T in (TB, TA):
            poly(ax, T(pts), fc, ec=ec, lw=lw)
    for s_ in (Z1, Z2):
        poly(ax, [jp(s_ - GW / 2), jp(s_ + GW / 2), jp(s_ + GW / 2, GD), jp(s_ - GW / 2, GD)], "white", lw=0.3)
        ax.add_patch(Ellipse(jp(s_, GD / 2), 6.6, 4.0, angle=math.degrees(math.atan2(u[1], u[0])), fc=SEAL, ec="none"))
    ax.add_patch(Circle(jp(ZR, 0), 3.0, fc="#7a5", ec="k", lw=0.3))
    a_, b_ = jp(ZB, WEB + 2), reflect([jp(ZB, WEB + 2)], u)[0]
    ax.plot([a_[0], b_[0]], [a_[1], b_[1]], c="#555", lw=2.2, solid_capstyle="butt")
    env = {}
    for key, (za, zb, col, ls) in (("new", (46, 106, GRN, "--")), ("old", (110, 170, ORG, ":"))):
        e = [jp(za, WEB), jp(zb, WEB), jp(zb, WEB + 30), jp(za, WEB + 30)]
        ax.add_patch(Polygon(e, fill=False, ec=col, lw=0.9, ls=ls)); ax.add_patch(Polygon(reflect(e, u), fill=False, ec=col, lw=0.9, ls=ls))
        env[key] = reflect([jp((za + zb) / 2, WEB + 30)], u)[0]
    p0, p1 = jp(-25), jp(D / G["cm"] + 40)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], ls=(0, (9, 2, 1.5, 2)), lw=0.5, c=RED)
    label(ax, jp(D / G["cm"] + 50), "joint plane (radial)", col=RED, fs=7.5)
    ax.annotate("", (0, -4), (0, -30), arrowprops=dict(arrowstyle="-|>", lw=0.5, mutation_scale=6))
    label(ax, (-4, -26), "panel B normal", fs=7.5, ha="right", bg=False)
    ax.plot([0, 0], [0, 78], lw=0.4, c=RED, ls=(0, (6, 2)))
    ax.add_patch(Arc((0, 0), 140, 140, theta1=90, theta2=90 + MH, lw=0.6, color=RED))
    label(ax, (8, 84), f"mitre {MH:.3f}°", col=RED, fs=7.5, ha="left")
    # dimensions of the true section (frame B)
    dim(ax, (xin(0), 0), (0, 0), f"{G['wh']:.1f}", off=6, fs=7.5, inside=False, text_side=-8)
    dim(ax, (xin(0) - FL_W, 0), (xin(0), 0), f"{FL_W:g}", off=6, fs=7.5)
    dim(ax, (xin(D) - LIP_H, D), (xin(D), D), f"{LIP_H:g} (OPEN-17)", off=-7, fs=7.5)
    dim(ax, (xin(0) - FL_W, 0), (xin(0) - FL_W, D), f"{D:g} panel depth z", off=-12, fs=7.5)
    dim(ax, (xin(0) - FL_W, 0), (xin(0) - FL_W, FL_T), f"{FL_T:g}", off=-4, fs=7.5, inside=False)
    dim(ax, (0, 0), tuple(jp(D / G["cm"])), f"joint face {D / G['cm']:.1f} (z')", off=14, fs=7.5)
    # balloons
    B = [(1, tuple(jp(140, 12)), (-150, 150)), (2, tuple(reflect([jp(140, 12)], u)[0]), (100, 80)),
         (3, (-200, 15), (-235, -12)), (4, (-200, 41.6), (-220, 30)), (5, (-180, 51.6), (-200, 72)), (6, (-200, 105), (-230, 128)),
         (7, (-200, 192), (-235, 160)), (8, (-200, 233), (-235, 252)), (9, tuple(env["new"]), (60, 20)), (10, tuple(env["old"]), (115, 170)),
         (11, tuple(jp(ZB, -12)), (40, -20)), (12, tuple(jp(30, 0)), (-105, -22))]
    for n, tgt, at in B:
        K.balloon(ax, tgt, at, n)
    # ---- detail A, 2:1, in the joint-face frame: x normal to the face (+ into A), y = z' down
    axd = view(fig, (284, 134, 120, 136), 0.5, (2, 33), flip_y=True, title="Detail A, the joint face drawn square to it; flanges not shown  (2:1)")
    top = WEB * G["tm"]
    for sgn, col in ((-1, MET2), (1, MET3)):
        poly(axd, [(0, 0), (sgn * WEB, top), (sgn * WEB, 64), (0, 64)], col, lw=0.6)
        axd.plot([sgn * WEB, sgn * WEB * 1.18], [64, 67], lw=0.4, c="k")
    for s_ in (Z1, Z2):
        rect(axd, -GD, s_ - GW / 2, GD, GW, "white", lw=0.5)
        axd.add_patch(Ellipse((-GD / 2, s_), 4.0, 6.6, fc=SEAL, ec="none"))
    axd.add_patch(Wedge((0, ZR), 3.0, 90, 270, fc="#7a5", ec="k", lw=0.4))
    rect(axd, -WEB, ZPORT - 1, WEB, 2, "white", lw=0.4); rect(axd, -WEB, ZPORT - 2.1, 8, 4.2, "white", lw=0.4)
    rect(axd, -WEB, ZB - BOLT_HOLE / 2, 2 * WEB, BOLT_HOLE, "white", lw=0.5)
    rect(axd, -WEB - 1.6 - 4.9, ZB - 3.97, 2 * WEB + 3.2 + 4.9 + 11, 7.94, "#666", lw=0.4)
    rect(axd, -WEB - 1.6 - 4.9, ZB - 7.35, 4.9, 14.7, "#888", lw=0.4); rect(axd, WEB + 1.6, ZB - 7.35, 9.0, 14.7, "#888", lw=0.4)
    for xw in (-WEB - 1.6, WEB): rect(axd, xw, ZB - 8.0, 1.6, 16.0, "#bbb", lw=0.3)
    cl(axd, (0, -5), (0, 66), col=RED)
    for i, (zz, t) in enumerate(((Z1, f"{Z1:g}"), (ZPORT, f"{ZPORT:g}"), (Z2, f"{Z2:g}"), (ZR, f"{ZR:g}"), (ZB, f"{ZB:g}"))):
        dim(axd, (0, 0), (WEB, zz) if False else (0, zz), t, off=24 + 7 * i, fs=7.5)
    dim(axd, (-GD, Z2 + GW / 2 + 0.2), (0, Z2 + GW / 2 + 0.2), f"{GD:g}", off=-3, fs=7.5, inside=False, text_side=-6)
    dim(axd, (-GD, Z1 - GW / 2), (-GD, Z1 + GW / 2), f"{GW:g}", off=-5, fs=7.5, inside=False)
    dim(axd, (-WEB, ZB - BOLT_HOLE / 2), (-WEB, ZB + BOLT_HOLE / 2), f"Ø{BOLT_HOLE:g}", off=-3.5, fs=7.5, inside=False)
    label(axd, (-12, 3), "frame B", fs=7.5, bg=False); label(axd, (13, 3), "frame A", fs=7.5, bg=False)
    leader(axd, (-GD + 0.5, Z1 + 2.5), (-27, 9), "glands, bottom\nR0.5-0.9", fs=7.5, ha="left")
    leader(axd, (-14, ZPORT), (-27, 31), "port Ø2; M5 x 8\nfrom the back", fs=7.5, ha="left")
    leader(axd, (-1.5, ZR + 1.5), (-27, 47), "RTV566 in R3", fs=7.5, ha="left")
    # ---- key, z' table and notes
    key = ("1  Frame B, P-06H, with the glands (web 20 normal to the joint face, 21.4 in this section)\n"
           "2  Frame A, P-06H, flat joint face\n"
           "3  L1 outer pane, 6 mm fused silica, gap vented to space (position: Rev E proposal, OPEN-11)\n"
           "4  L4 solar layer, 3.3 mm substrate (OPEN-11)\n"
           "5  L5 tint layer, 3.3 mm substrate (OPEN-11)\n"
           "6  L6 shade, envelope z 95-115 (OPEN-11)\n"
           f"7  L7 pressure pane, 21 mm BOROFLOAT 33 on a 2 mm setting strip; edge 10 mm clear of the web, so {LIP_H - 10:.1f} on the {LIP_H:g} lip (OPEN-17)\n"
           "8  Cabin scratch pane, cast acrylic, unloaded (envelope)\n"
           "9  Hardpoint fitting envelope on the line of the pull, z' 46-106: DECIDED 10 Nov (RF-07)\n"
           "10 Hardpoint envelope as first drawn, z' 110-170: superseded, it fails the HP1 seal check\n"
           f"11 Seam bolt NAS6705U27 + KFN670 nut at z' {ZB:g}, {v('seam_bolt','preload_kN'):g} kN by torque\n"
           "12 Detail A: glands, leak port, RTV recess, bolt hole")
    y = heading(Pp, 14, 126, "Key to the balloons")
    yk = note(Pp, 14, y, 130, key, fs=7.5, ls=1.15)
    y = heading(Pp, 150, 126, "Joint-face features, placed along the joint plane by z'")
    rows = [("Feature", "z'", "Hexagon z", "Pentagon z")]
    ch, cp = math.cos(math.radians(MH)), math.cos(math.radians(MP))
    for lab, s_ in (("Outer gland", Z1), ("Leak port (frame B)", ZPORT), ("Inner gland", Z2), ("RTV recess (frame B)", ZR), ("Seam bolt row", ZB),
                    ("Hardpoint fitting, DECIDED", (46, 106)), ("Hardpoint, first drawn", (110, 170)), ("Corner tie rows", (133.8, 380.0)), ("Corner dowels", (256.9,))):
        if isinstance(s_, tuple):
            sep = "-" if lab.startswith("Hardpoint") else ", "
            rows.append((lab, sep.join(f"{x:g}" for x in s_), sep.join(f"{x*ch:.1f}" for x in s_), sep.join(f"{x*cp:.1f}" for x in s_)))
        else:
            rows.append((lab, f"{s_:g}", f"{s_*ch:.2f}", f"{s_*cp:.2f}"))
    rows.append(("Frame cabin face", f"{D/ch:.1f} / {D/cp:.1f}", "180", "180"))
    yb = table(Pp, 150, y, (36, 18, 13 + 4, 15 + 4), rows, fs=7.5, ls=1.1, pad=0.6)
    note(Pp, 150, yb - 2, 76, f"z = z' x cos(mitre): hexagon {ch:.4f}, pentagon {cp:.4f}. Both frames of a seam share the joint plane, so holes and glands line up on hexagon-pentagon seams too (OPEN-9).", fs=7.5)
    nt = (f"Seal: two loops of Parker BA500 butyl, {CORD:.2f} mm cord, in {GW:g} x {GD:g} glands (25 % squeeze, 79 % fill); RTV566 bead cured on the ground (Q80). Loop corners: R16 minimum at the corner block, OPEN (Q92).\n"
          f"Bolt: NAS6705U27 A286 with KFN670 nut, {v('seam_bolt','preload_kN'):g} kN by torque, 16 per seam at 75 pitch in bays of 3, 5, 5, 3; the two beside each hardpoint at 6 kN, measured (proposed 14 Nov). "
          "Shear along the seam goes to the hardpoint pins and the corner dowels; there is no shear key (OPEN-15, FEA of 24 Oct).\n"
          "Changed from RE-04 (24 Oct): frame 140 to 180; pane 22 to 21 mm; bolt NAS6705U27 at 4 kN (was NAS9306C-06, a rivet standard); the lip and seat moved to the cabin face, z 170-180 (Q78).\n"
          "Corrected 27 Nov: the web is drawn at its true depth, z 0 to 180 square to the panel, so its joint face is 192.7 long and it meets the lip (it was drawn 180 along the face and stopped short of the lip). "
          f"Bite on the lip as drawn: {LIP_H - 10:.1f} mm; the earlier note gave 20.0 mm for the {LIP_H:g} lip, which does not fit this stack: needs the rule for the frame-side pane edge (OPEN-17). "
          "The P-06H solid has a 50 mm lip.")
    note(Pp, 246, 126, 160, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-05_seam_section.png")


# =====================================================================================================================
# hexagon / pentagon helpers
# =====================================================================================================================
def grid_segments(c, a, b, k=KGRID):
    """secondary rib segments inside the triangle (c, a, b): lines parallel to each side at i = 1 .. k-1"""
    segs = []
    Pt = lambda i, j: c + (a - c) * (i / k) + (b - c) * (j / k)
    for i in range(1, k):
        for j in range(0, k - i):
            segs.append((Pt(i, j), Pt(i, j + 1)))
            segs.append((Pt(j, i), Pt(j + 1, i)))
    for s in range(1, k):
        for t in range(0, s):
            segs.append((Pt(s - t, t), Pt(s - t - 1, t + 1)))
    return segs


def _panel(ax, V, glass, hatch=False):
    C = np.zeros(2); n = len(V)
    ax.add_patch(Polygon(V, fc="#f4f6f8", ec="k", lw=1.0))
    for i in range(n):
        A, B = V[i], V[(i + 1) % n]; mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        ax.add_patch(Polygon([A, B, B + inward * 120, A + inward * 120], fc=MET2, ec="k", lw=0.5))
    if glass:
        for i in range(n):
            A, B = V[i], V[(i + 1) % n]
            p = lambda i_, j_: C + (A - C) * (i_ / KGRID) + (B - C) * (j_ / KGRID)
            for ii in range(KGRID):
                for jj in range(KGRID - ii):
                    ax.add_patch(Polygon([p(ii, jj), p(ii + 1, jj), p(ii, jj + 1)], fc=GLS, ec=BLU, lw=0.3))
                    if jj < KGRID - ii - 1:
                        ax.add_patch(Polygon([p(ii + 1, jj), p(ii + 1, jj + 1), p(ii, jj + 1)], fc=GLS, ec=BLU, lw=0.3))
    if hatch:
        for i in range(n):
            tri = np.array([C, V[i], V[(i + 1) % n]]); cen = tri.mean(axis=0)
            ax.add_patch(Polygon(cen + (tri - cen) * 0.86, fc="#eef2f5", ec="#888", lw=0.4, hatch="////"))
    nseg = 0
    for i in range(n):
        for a, b in grid_segments(C, V[i], V[(i + 1) % n]):
            ax.plot([a[0], b[0]], [a[1], b[1]], c=MET, lw=1.6, solid_capstyle="butt"); nseg += 1
    for i in range(n):
        ax.plot([0, V[i][0]], [0, V[i][1]], c="#7f8a94", lw=3.2, solid_capstyle="butt")
    ax.add_patch(Circle((0, 0), 90, fc="#777", ec="k", lw=0.6))
    for i in range(n):
        A = V[i]
        for B in (V[(i - 1) % n], V[(i + 1) % n]):
            d = (B - A) / np.linalg.norm(B - A); inward = (C - A) / np.linalg.norm(C - A); nn = np.array([-d[1], d[0]])
            if np.dot(nn, inward) < 0: nn = -nn
            ax.add_patch(Polygon([A, A + d * 230, A + d * 230 + nn * 50, A + nn * 50], fc=STEEL, ec="k", lw=0.5))
        B = V[(i + 1) % n]; d = (B - A) / np.linalg.norm(B - A); mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        for q in (1, 2, 3):
            hc = A + d * (q * PITCH)
            ax.add_patch(Polygon([hc - d * 100, hc + d * 100, hc + d * 100 + inward * 50, hc - d * 100 + inward * 50], fc=TI, ec="k", lw=0.5))
    return nseg


# =====================================================================================================================
# RF-06 hexagon general arrangement
# =====================================================================================================================
def rf06(pdf):
    fig, Pp = K.new_sheet("RF-06", "Hexagon panel, general arrangement and parts list", status="Ribs and frame DECIDED; corner blocks, hardpoints, nodes and P-11 braces PROPOSAL; masses from the models, not reconciled with the 36.1 t shell model.",
                          part="Hexagon panel (A-02B), 20 per station", material="See parts list", finish="-", scale="1:25; sections 1:5", sheet_of=of("RF-06"))
    V = [np.array([EDGE * math.cos(math.radians(60 * i)), EDGE * math.sin(math.radians(60 * i))]) for i in range(6)]
    C = np.zeros(2)
    ax = view(fig, (12, 74, 208, 198), 25.0, (110, -130), title="Hexagon from the cabin side: frames, main ribs, k 4 secondary grid, hub, nodes, corner blocks, hardpoints, 96 panes  (1:25)")
    nseg = _panel(ax, V, True)
    A, Bv = V[0], V[1]; dvec = (Bv - A) / np.linalg.norm(Bv - A); mid = (A + Bv) / 2; inward = -mid / np.linalg.norm(mid)
    bolts = bolts_on_seam()
    for s_ in bolts: ax.add_patch(Circle(A + dvec * s_ + inward * ZB * math.cos(math.radians(MH)), 14, fc="#333", ec="none"))
    for q in (1, 2, 3):
        hc = A + dvec * (q * PITCH) - inward * 170; label(ax, hc, f"HP{q}", fs=7.5, col=ORG, bg=False)
    yF = EDGE * math.sin(math.radians(60))
    dim(ax, (V[3][0], 0), (V[0][0], 0), f"{2*EDGE:,.0f} across corners", off=-86)
    dim(ax, (V[1][0], -yF), (V[1][0], yF), f"{2*yF:,.1f} across flats", off=52)
    dim(ax, tuple(V[2]), tuple(V[1]), f"edge {EDGE:,.0f}", off=8)
    # item balloons (numbers as in the parts list)
    def at(p, d): return (p[0] + d[0], p[1] + d[1])
    node = (V[0] + V[1]) / 4                                  # a six-way node
    pane_c = (C + (V[4] - C) * 0.5 + (V[5] - C) * 0.25 + (C + (V[4] - C) * 0.75 + (V[5] - C) * 0.25) + (C + (V[4] - C) * 0.5 + (V[5] - C) * 0.5)) / 3
    seg = C + (V[3] - C) * 0.5 + (V[4] - C) * 0.125 + (V[3] - C) * 0.0
    crossing = V[3] * 0.25
    hp2 = V[4] + (V[5] - V[4]) * 0.5
    items = [(1, (V[3] + V[4]) / 2 + np.array([60, 30]), (-2350, -1350)), (2, V[2] * 0.62, (-1950, 1250)), (3, V[2] * 0.42, (-1700, 780)),
             (4, C + np.array([30, 30]), (420, 700)), (5, C + np.array([-40, 20]), (-450, 700)), (6, seg, (-1000, -1450)),
             (7, node, (1250, 1550)), (8, node + np.array([20, -20]), (1500, 1250)), (9, pane_c, (300, -1350)), (10, node + np.array([-25, 25]), (900, 1750)),
             (11, A + dvec * bolts[-3] + inward * 55, (2620, 1650)), (12, V[0] + np.array([-60, 40]), (2620, 500)), (13, hp2 + np.array([-40, 25]), (-500, -1550)),
             (14, hp2 + np.array([40, 25]), (-150, -1500)), (15, hp2 + np.array([0, 25]), (300, -1550)), (16, crossing, (-1150, 450))]
    for n, tgt, pos in items:
        K.balloon(ax, tuple(tgt), pos, n)
    # sections at 1:5
    axs = view(fig, (226, 182, 180, 92), 5.0, (190, 205), flip_y=True, title="Sections B-B and C-C through the ribs, space side at the top  (1:5; full size on RF-01)")
    tw, tf, bf, d = MR["tw"], MR["tf"], MR["bf"], MR["d"]
    rect(axs, -bf / 2, 0, bf, tf, MET2); rect(axs, -tw / 2, tf, tw, d - tf, MET2)
    for s_ in (-1, 1):
        rect(axs, (tw / 2 if s_ > 0 else -tw / 2 - LEDGE_W), 170, LEDGE_W, 10, MET2)
        poly(axs, [(s_ * tw / 2, d - CAP_V), (s_ * (tw / 2 + CAP_T), d - CAP_V), (s_ * (tw / 2 + CAP_T), d - tf), (s_ * (tw / 2 + CAP_H), d - tf), (s_ * (tw / 2 + CAP_H), d), (s_ * tw / 2, d)], "#b0b7be")
    _pane_pair(axs, 150)
    xc = 430
    rect(axs, xc - 30, 0, 60, 10, MET2); rect(axs, xc - 2.5, 10, 5, 160, MET2); rect(axs, xc - 30, 170, 60, 10, MET2)
    _pane_pair(axs, 130, xc=xc)
    label(axs, (0, 425), "B-B main rib: I 400 x 100 x 25, web 8", fs=7.5, bg=False)
    label(axs, (xc, 232), "C-C secondary rib: I 180 x 60 x 10, web 5", fs=7.5, bg=False)
    label(axs, (95, 228), f"bite {tw/2 + LEDGE_W - SHORT:.1f} on the 30 ledge", fs=7.5, col=BLU, bg=False, ha="left")
    label(axs, (xc + 70, 192), f"bite {SR['bf']/2 - SHORT:.1f}", fs=7.5, col=BLU, bg=False, ha="left")
    label(axs, (95, 390), "cap angles P-04A, z 375-400", fs=7.5, bg=False, ha="left")
    label(axs, (95, 160), "seat ledges z 170-180", fs=7.5, bg=False, ha="left")
    # parts list
    y = heading(Pp, 228, 177, "Parts list, one hexagon (masses from the models)")
    rows = [("P-06H frame member, 1,790 between the blocks", 6, 22.55), ("P-04 main rib B", 6, MASS["P-04"]), ("P-04A cap angle (see note)", 12, MASS["P-04A"]),
            ("P-05 hub core", 1, MASS["P-05"]), ("P-05A hub star plate", 2, MASS["P-05A"]), ("P-01 secondary rib segment", 108, MASS["P-01"]),
            ("P-02 node star plate", 36, MASS["P-02"]), ("P-03 node web core", 18, MASS["P-03"]), ("P-07 pane, 21 mm", 96, MASS["P-07"]),
            ("P-08 pane corner clamp (six-way nodes)", 18, MASS["P-08"]), ("P-14 seam bolt (half of 16 x 6)", 48, MASS["P-14"]),
            ("CB-01 corner block, leaning faces", 6, 22.86), ("HP-02A lug body, Ti-6Al-4V (half of 18)", 9, 9.69),
            ("HP-02B clevis body, Ti-6Al-4V (other half)", 9, 6.77), ("HP-03 pin 40 x 95, A286 (3 per hardpoint)", 27, 0.948), ("P-11 main rib brace pair, 7075", 18, 1.12)]
    tot = sum(q * e for _, q, e in rows)
    tab = [("Item", "Part", "Qty", "Each kg", "Total kg")] + [(str(i + 1), n, str(q), f"{e:.2f}", f"{q*e:.0f}") for i, (n, q, e) in enumerate(rows)] + [("", "Listed parts, one hexagon", "", "", f"{tot:,.0f}")]
    yb = table(Pp, 228, y, (10, 100, 14, 22, 30), tab, fs=7.5, ls=1.05, pad=0.5)
    nt = (f"Listed parts {tot:,.0f} kg per hexagon with its glass ({96*MASS['P-07']:.0f} kg) and its half share of the hardpoints. Masses: model volume x the nominal density of each part's own material. "
          "Shell model 36.1 t: to reconcile. Item 3: the library solid has 58 mm legs (124 wide); at the decided 46 mm it is about 11.1 kg. Item 10 counts the six-way nodes only; the library also puts clamps at the main rib and frame nodes.")
    note(Pp, 228, yb - 1.5, 176, nt, fs=7.5)
    nt2 = (f"k 4 grid: {PITCH:g} mm pitch, {nseg} secondary rib segments, 96 panes (48 full triangles, 48 cut back at the frame and the hub), 18 six-way nodes, 18 crossings on the main ribs (P-11 braces), "
           "18 hardpoints, each shared with the neighbouring panel. 16 seam bolts per edge (dots on one edge), 75 pitch in bays of 3, 5, 5, 3, the first 271.25 from the vertex; hardpoints HP1-HP3 at 562.5, 1125 and 1687.5.\n"
           "Corrected 27 Nov: the sheet said 1:20; the view is drawn at 1:25. The main rib bite is 24.9 on the 30 mm ledges (it said 40.9). The masses are per material (it said 6061 density).")
    note(Pp, 14, 66, 206, nt2, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-06_hexagon_GA.png")


# =====================================================================================================================
# RF-07 hardpoint
# =====================================================================================================================
def rf07(pdf):
    fig, Pp = K.new_sheet("RF-07", "Seam hardpoint: the TP3 fitting at the moved position", status="Position on the line of the pull DECIDED 10 Nov with Rick. The part is a PROPOSAL and not buildable: it must be redesigned for the 180 mm frame (OPEN).",
                          part="HP-02A lug, HP-02B clevis, 3 x HP-03 pin; slot in P-06H", material="Ti-6Al-4V bodies; A286 pins", finish="-",
                          scale="1:2", sheet_of=of("RF-07"))
    LUG0, LUG1 = 56.5, 95.5; CH = ((33.5, 56.0), (96.0, 118.5)); PIN0, PIN1 = 28.5, 123.5; BASE0, BASE1 = -6.5, 123.5
    Lh = 460; x0 = -Lh / 2
    ax = view(fig, (12, 150, 244, 118), 2.0, (0, 88), flip_y=True,
              title="Joint face of frame B at a hardpoint (HP1 of a seam), z' down from the shell edge. Only the lug crosses the joint, through the slot  (1:2)")
    rect(ax, x0, 0, Lh, D / math.cos(math.radians(MH)), MET2, lw=0.8)
    for zc in (Z1, Z2): ax.plot([x0, x0 + Lh], [zc, zc], c=SEAL, lw=1.4)
    ax.plot([x0, x0 + Lh], [ZR, ZR], c="k", lw=0.5, ls=":")
    rect(ax, -101, LUG0 - 1, 202, LUG1 - LUG0 + 2, "white", ec=GRN, lw=1.1)
    for j in (-1, 0, 1): ax.add_patch(Rectangle((j * 60 - 20, PIN0), 40, PIN1 - PIN0, fill=False, ec="#555", lw=0.6, ls="--"))
    for xb in (-141.25, 131.25, -141.25 - 75, 131.25 + 75): ax.add_patch(Circle((xb, ZB), BOLT_HOLE / 2, fc="white", ec="k", lw=0.6))
    label(ax, (0, 76), "slot 202 x 41, R5, z' 55.5 to 96.5", col=GRN, fs=7.5)
    label(ax, (0, PIN1 + 9), "three pins Ø40 x 95 behind the web (dashed), axes along z', 60 pitch", fs=7.5, col=GREY)
    dim(ax, (-141.25, ZB), (-101, ZB), "40.25", off=-12, fs=7.5); dim(ax, (101, ZB), (131.25, ZB), "30.25", off=-12, fs=7.5)
    dim(ax, (-101, 0), (101, 0), "202 slot (200 lug)", off=8, fs=7.5)
    dim(ax, (80, PIN0), (80, PIN1), "pins z' 28.5-123.5", off=40, fs=7.5)
    dim(ax, (x0, 0), (x0, ZB), f"z' {ZB:g}", off=10, fs=7.5); dim(ax, (x0, 0), (x0, LUG0 - 1), "55.5", off=19, fs=7.5)
    for zc, t in ((Z1, "butyl z' 18"), (Z2, "butyl z' 32"), (ZR, "RTV z' 42")):
        label(ax, (x0 + Lh + 4, zc), t, fs=7.5, ha="left", bg=False)
    label(ax, (x0 + Lh + 4, ZB), "seam bolts z' 58", fs=7.5, ha="left", bg=False)
    label(ax, (x0 + 4, -9), "shell edge, z' 0 (space side)", fs=7.5, ha="left", bg=False, col=GREY)
    # section across the seam, drawn straight
    ax2 = view(fig, (262, 112, 144, 156), 2.0, (-30, 95), flip_y=True, title="Section F-F across the seam, drawn straight, space side at the top  (1:2)")
    rect(ax2, 0, 0, 20, D, MET3); rect(ax2, -20, 0, 20, D, MET2)
    for sgn in (-1, 1):
        rect(ax2, 20 if sgn > 0 else -70, 0, 50, 10, MET3 if sgn > 0 else MET2, lw=0.6)
        rect(ax2, 20 if sgn > 0 else -20 - LIP_H, 170, 50 if sgn > 0 else LIP_H, 10, MET3 if sgn > 0 else MET2, lw=0.6)
    rect(ax2, 20, BASE0, 48, BASE1 - BASE0, TI, lw=0.8, alpha=0.9)
    rect(ax2, -120, LUG0, 140, LUG1 - LUG0, TI, lw=0.8, alpha=0.9)
    rect(ax2, -152, BASE0, 30, BASE1 - BASE0, "#a9c0a0", lw=0.8, alpha=0.9)
    for (c0, c1) in CH: rect(ax2, -122, c0, 102, c1 - c0, "#a9c0a0", lw=0.8, alpha=0.9)
    rect(ax2, -80, PIN0, 40, PIN1 - PIN0, "#777", lw=0.6, alpha=0.75)
    ax2.plot([0, 0], [-14, D + 12], ls=(0, (9, 2, 1.5, 2)), lw=0.5, c=RED)
    for s in (Z1, Z2): ax2.add_patch(Ellipse((-2.0, s), 4.0, 6.6, fc=SEAL, ec="none"))
    label(ax2, (44, 40), "HP-02A\nlug body", fs=7.5, bg=False); label(ax2, (-137, 60), "HP-02B\nclevis", fs=7.5, bg=False, rotation=90)
    label(ax2, (-60, 140), "HP-03 pins", fs=7.5, bg=False)
    label(ax2, (-12, -20), "panel B", fs=7.5, ha="right", bg=False); label(ax2, (12, -20), "panel A", fs=7.5, ha="left", bg=False)
    leader(ax2, (40, 4), (-60, -26), "base blocks start at z' -6.5: they\nrun into the outer flange (both sides)", fs=7.5, col=RED, ha="right")
    leader(ax2, (-60, 172), (-150, 205), "pins cannot be put in: the lip and\nthe pane are in the way (cabin side)", fs=7.5, col=RED, ha="left")
    dim(ax2, (68, BASE0), (68, BASE1), "z' -6.5 to 123.5", off=6, fs=7.5)
    # notes
    nt = ("What the fitting is. Measured from the October C3 model (the run that gave 2.876 million N/mm): a Ti-6Al-4V lug 39 thick and 200 wide on panel A reaches across the joint into a clevis of two 22.5 mm cheeks on panel B; "
          "three A286 pins, Ø40 x 95, at 60 pitch, run along the panel depth with no clearance and work in double shear. The 8 Nov solids (pins across the joint, a pad of 200 x 60) were wrong and are withdrawn.\n"
          "What the models say (HP1, 6-7 Nov). Where sheet RE-06-1 put it, 64 mm deeper than the line of the pull, the frames hinge about the fitting and the seal gap reaches 0.11 mm at 0.22 atm (0.47 with the frames held), against the 1.93 atm required. "
          "On the line of the pull (lug mid-plane at z' 76) the gap at the hardpoint is 0.064 mm at 1.93 atm; the plain bolt beside it reaches 0.11 mm at 1.87 atm at 4 kN, 3 % short. "
          "Moved closer (115 mm) that bolt is worse, 1.76 atm (13 Nov); at 6 kN it clears, about 1.95 atm (14 Nov), so the two bolts beside each hardpoint go to 6 kN, measured (proposed). These runs model the fitting as a spring between rigid pads of 200 x 60, not this part.\n"
          "What the solid found (9 Nov, leaning hexagon frame). Good: the slot is 10.5 mm from the RTV recess, 20 mm from the inner gland and 32 mm from the nearest bolt hole; the seam bolts on the flight layout (131.25 and 141.25 mm from the hardpoint centre) are clear of it. "
          "Not good: (1) to sit behind the 20 mm webs the bodies had to move 38 mm apart, so the lug is 140 long, not 102, and the pin line is 60 mm from the joint, not 40: the C3 stiffness no longer applies. "
          "(2) The base blocks and pin ends run into the outer flange, and both bodies and the pins run into the two secondary ribs that land on the hardpoint. "
          "(3) The pins cannot be put in: the seat lip and the pane are in the way from the cabin side, the flange from the space side. "
          "(4) The web is cut through over 202 mm at the bolt row's depth, and nothing yet says how the base blocks fasten to the frame. The old 50 mm local block (HP-01) has no job left.\n"
          "So the position is right and the part is not yet a design: redraw it for the 180 mm frame (a shallower stack, pins put in from the side or along the seam, the ribs landing on the base blocks) and rerun C3 and HP1. "
          "Load 108.7 kN per atm on the worst hardpoint; one hardpoint is 19.3 kg.\n"
          "Corrected 27 Nov: the joint face is turned so the space side is at the top, as on RF-05; the fitting bodies are drawn at z' -6.5 to 123.5 as in the solids HP-02A / HP-02B (the sheet had 11 to 141, which hid the flange clash).")
    note(Pp, 14, 140, 244, nt, fs=7.5)
    bolts = bolts_on_seam()
    y = heading(Pp, 262, 104, "The three hardpoints on a 2,250 mm seam, from the vertex")
    rows = [("", "Centre", "Slot", "Nearest seam bolts (from the centre)")]
    for i, hp in enumerate((562.5, 1125.0, 1687.5)):
        lo = max(b for b in bolts if b < hp); hi = min(b for b in bolts if b > hp)
        rows.append((f"HP{i+1}", f"{hp:g}", f"{hp-101:g} to {hp+101:g}", f"{lo:g} ({hp-lo:g}) and {hi:g} ({hi-hp:g})"))
    table(Pp, 262, y, (12, 20, 38, 74), rows, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-07_hardpoint.png")


# =====================================================================================================================
# RF-08 corner node
# =====================================================================================================================
def rf08(pdf):
    fig, Pp = K.new_sheet("RF-08", "Corner node: blocks, ties, dowels, what the model says, machining", status="Block PROPOSAL; tie preload 180 kN DECIDED 17 Nov (was 198 kN); R10 inside corners per Marco; O10 corner seal, rib landing, tightening tolerance and block stress limit OPEN.",
                          part="CB-01 hexagon block (CB-02 pentagon); node A-03", material="2219-T852 or 7050-T7451 (OPEN); ties Inconel 718",
                          finish="Joint faces Ra 0.8; elsewhere Ra 3.2", scale="Plan 1:2; joint face 1:5", sheet_of=of("RF-08"))
    pts, convex, concave, g = CB.outline(120)
    th = g["th"]; a_ = g["alpha"]
    ax = view(fig, (12, 140, 188, 130), 2.0, (60, 100), title="CB-01 plan section, square to the panel (the same at every depth)  (1:2)")
    ax.add_patch(Polygon(pts, closed=True, fc=STEEL, ec="k", lw=0.8))
    for p_ in concave:
        ax.add_patch(Circle(p_, 3.0, fc="none", ec=RED, lw=0.7))
    for xs in CB.TIE_COLS:
        ax.add_patch(Rectangle((xs - 11.75, 0), 23.5, th, fc="none", ec="k", lw=0.5, ls="--"))
        q_ = [CB.mirror_pt(pp, a_) for pp in ((xs - 11.75, 0), (xs + 11.75, 0), (xs + 11.75, th), (xs - 11.75, th))]
        ax.add_patch(Polygon(q_, closed=True, fill=False, ec="k", lw=0.5, ls="--"))
    cl(ax, (0, 0), (g["u"][0] * 200, g["u"][1] * 200), col=GREY)
    dim(ax, (0, 0), (230, 0), "230 from the vertex line", off=-20)
    dim(ax, (0, 0), (CB.TIE_COLS[0], 0), f"{CB.TIE_COLS[0]:g}", off=-6, fs=7.5)
    dim(ax, (0, 0), (CB.TIE_COLS[1], 0), f"{CB.TIE_COLS[1]:g}", off=-13, fs=7.5)
    dim(ax, (230, 0), (230, th), f"{th:.1f}", off=5, fs=7.5, inside=False)
    ax.add_patch(Arc((0, 0), 60, 60, theta1=0, theta2=120, lw=0.6, color=RED)); label(ax, (36, 26), "120°", col=RED, fs=7.5, bg=False)
    leader(ax, ((pts[4][0] + pts[5][0]) / 2, (pts[4][1] + pts[5][1]) / 2), (120, 205), "main rib landing: 110 wide, bottom 57 from the\nvertex line, walls 36.6, R10 at both inside corners\n(circled); it leans with the vertex line, 23.8°", fs=7.5, ha="left")
    leader(ax, (175, th), (150, 120), "tie holes Ø23.5, normal to the joint face\n(dashed), in columns 130 / 186", fs=7.5, ha="left")
    label(ax, (-8, -6), "vertex line", fs=7.5, ha="right", bg=False, col=GREY)
    label(ax, (110, -55), f"Legs 50 thick normal to the joint face ({th:.1f} in this section). The legs' outer faces are the joint faces.", fs=7.5, bg=False)
    # joint face of leg A, true shape: z' down, x along the edge from the z' 0 vertex
    zj = g["zp_joint_end"]; q = g["q"]
    ax2 = view(fig, (204, 112, 98, 158), 5.0, (140, 205), flip_y=True, title="Joint face of a leg, true shape  (1:5)")
    ax2.add_patch(Polygon([(0, 0), (230, 0), (230 + q * zj, zj), (q * zj, zj)], closed=True, fc=STEEL, ec="k", lw=0.8))
    for zp in CB.ROWS_ZP:
        for xs in CB.TIE_COLS: ax2.add_patch(Circle((xs + q * zp, zp), 11.75, fc="white", ec="k", lw=0.6))
    for xs in CB.TIE_COLS: ax2.add_patch(Circle((xs + q * CB.DOWEL_ZP, CB.DOWEL_ZP), 10, fc="white", ec="k", lw=0.6, ls="--"))
    ax2.plot([0, q * zj], [0, zj], lw=0.5, c=GREY, ls=(0, (9, 2, 1.5, 2)))
    xo = -40                                                      # ordinate dimensions of z'
    ax2.plot([xo, xo], [0, zj], lw=0.5, c="k")
    for zz, t in ((0, "0"), (CB.ROWS_ZP[0], f"{CB.ROWS_ZP[0]:g}"), (CB.DOWEL_ZP, f"{CB.DOWEL_ZP:g}"), (CB.ROWS_ZP[1], f"{CB.ROWS_ZP[1]:g}"), (zj, f"{zj:.1f}")):
        xr = q * zz
        ax2.plot([xo - 6, xr - 3], [zz, zz], lw=0.35, c="k")
        label(ax2, (xo - 9, zz), t, fs=7.5, ha="right", bg=False)
    label(ax2, (xo - 8, -26), "z'", fs=7.5, ha="right", bg=False)
    dim(ax2, (0, 0), (230, 0), "230", off=6, fs=7.5)
    zr = CB.ROWS_ZP[1]
    dim(ax2, (q * zr, zr), (CB.TIE_COLS[0] + q * zr, zr), f"{CB.TIE_COLS[0]:g}", off=-9, fs=7.5)
    dim(ax2, (CB.TIE_COLS[0] + q * zr, zr), (CB.TIE_COLS[1] + q * zr, zr), "56", off=-9, fs=7.5)
    label(ax2, (q * 60 + 8, 62), "vertex line, 11.64°\noff square to the edge", fs=7.5, ha="left", bg=False, col=GREY)
    label(ax2, (140, zj + 44), "4 ties 7/8-14 Inconel 718 in Ø23.5;\n2 dowels Ø20 (room for 24), dashed.\nHexagon z 125 / 240 / 355; pentagon\nface 417.1, z 128.3 / 246.4 / 364.4", fs=7.5, bg=False, va="top")
    # results
    xr0 = 306; y = heading(Pp, xr0, 270, "What the corner model says")
    res = ("Model C1, 5 to 17 Nov.\n"
           f"- Tie preload {TIE_PRE:g} kN by measured stretch, decided 17 Nov (198 kN is the earlier value).\n"
           f"- At {TIE_PRE:g} kN, proof, 0.8 atm: worst tie 198.9 kN (limit {TIE_LIM:g}); faces open 0.57 mm (0.55 with the pentagon 15 K warmer).\n"
           f"- At {TIE_PRE:g} kN, hatch open, 1 atm: worst tie 212.0 kN; faces open 0.773 mm (limit 0.8).\n"
           "- Pentagon 15 K warmer: 197.0 kN at 0.8 atm, 208.6 kN hatch open.\n"
           "- Not below 180 kN: at 160 kN the faces open 0.813 mm with the hatch open.\n"
           "- Earlier value, 198 kN (before 17 Nov): 214.5 kN at 0.8 atm and 226.3 kN hatch open, 0.7 kN from the limit.\n"
           "- Block stress at the earlier 198 kN, 95th percentile: 236 MPa (255 at 1 atm). No stress limit is set for the block: OPEN.\n"
           "- Worst corner load 235 kN at 0.8 atm, 290 kN at 1 atm.\n"
           "- Tightening tolerance: held at 180 kN or just above; the band is OPEN.")
    note(Pp, xr0, y, 100, res, fs=7.5)
    nt = ("Making it (Marco, 7 Nov). As first drawn the node could not be machined: every inside corner needs a radius a cutter can reach (R10 here; the landing takes up the re-entrant corner). Our position (9 Nov): "
          "machine it from 7050-T7451 or 2219-T851 plate, not a casting (seal faces) and not a die forging (180 parts). The main rib's flanges enter the block at the landing (PROPOSAL); the two frame members run into the legs' inner faces; "
          "the tie-to-web-fillet clash (Q29), the O10 corner seal and the loop corners R16 (Q27, Q92) are open.\n"
          "The ties are tightened by measured stretch, because a torque wrench scatters about 25 % and the hatch-open faces leave only 0.03 mm. Marco called the force 'achievable but unreasonable': "
          "about 590-820 N m per tie if torqued (650-900 at the earlier 198 kN). 12 ties per node, 720 on the station.\n"
          "Solids of 9 Nov with the real leaning joint faces (CB-01 22.9 kg, CB-02 21.6 kg, node A-03 80.2 kg): three blocks at a real vertex share no volume, the joint faces are coplanar, and the 12 tie holes and "
          "6 dowel holes meet on axis. The block is one outline swept along the vertex line, which leans 23.8° (20.1° pentagon), so the main rib end is mitred to match. Tie columns 130 / 186 from the vertex line "
          "(87 / 143 cannot clear the landing). Metal from the landing to the joint face 20.4 mm (17.1 pentagon); washer seat to the landing edge 14.3 mm (3.4 pentagon, tight). The R10 corners are about 430 mm long: "
          "cut from the open side with a ball or bull-nose cutter.\n"
          "Main rib lateral brace (requirement of 4 Nov): unbraced over 2.25 m the main rib buckles sideways at 0.79 of its load; braced every 562.5 mm it has 8.4 times margin. "
          "P-11 (PROPOSAL): a pair of 8 mm 7075 plates on the main rib web from z 180 to z 375 at every secondary rib crossing, bolted through the web. Size to be checked.\n"
          "Corrected 27 Nov: the plan is the CB-01 builder's outline (it was a sketch with round holes); the joint face is drawn true, leaning with the vertex line; the dowels are in the tie columns at 130 / 186, "
          "as in the solid (the sheet had them at 50 / 210); results at 198 kN are labelled as the earlier value.")
    note(Pp, 14, 124, 186, nt, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-08_corner_node.png")


# =====================================================================================================================
# RF-09 pentagon
# =====================================================================================================================
def rf09(pdf):
    fig, Pp = K.new_sheet("RF-09", "Pentagon panel, general arrangement, roles, docking", status="Ribs and frame DECIDED; closure plate side OPEN (Q57); roles PROPOSAL (25 Oct); docking hatch and IDSS ring concept.",
                          part="Pentagon panel (A-04), 12 per station", material="6061-T6; closure plate 10 mm 6061-T6", finish="-", scale="1:25", sheet_of=of("RF-09"))
    Rc = EDGE / (2 * math.sin(math.radians(36)))
    V = [np.array([Rc * math.cos(math.radians(90 + 72 * i)), Rc * math.sin(math.radians(90 + 72 * i))]) for i in range(5)]
    ax = view(fig, (12, 74, 200, 196), 25.0, (0, -150), title="Pentagon from the cabin side: the hexagon's frame and rib parts, no glass, a 10 mm closure plate  (1:25)")
    nseg = _panel(ax, V, False, hatch=True)
    ax.add_patch(Circle((0, 0), 400, fill=False, ec=ORG, lw=1.1, ls="--")); ax.add_patch(Circle((0, 0), 620, fill=False, ec=ORG, lw=0.8, ls=":"))
    ri = Rc * math.cos(math.radians(36))
    dim(ax, (V[2][0], -ri), (V[3][0], -ri), f"edge {EDGE:,.0f}", off=-10)
    dim(ax, (V[1][0], -ri), (V[1][0], Rc), f"{Rc + ri:,.1f} vertex to flat", off=-12)
    ax.plot([V[1][0] - 14 * 25, 0], [Rc, Rc], lw=0.3, c="k"); ax.plot([V[1][0] - 14 * 25, V[2][0]], [-ri, -ri], lw=0.3, c="k")
    C = np.zeros(2)
    items = [(1, (V[3] + V[4]) / 2 + np.array([-40, 60]), (2250, -900)), (2, V[4] * 0.6, (2250, 300)), (3, (C + (V[0] - C) * 0.5 + (V[4] - C) * 0.25 + C + (V[0] - C) * 0.5) / 2, (1300, 1500)),
             (4, C + np.array([40, -40]), (900, -700)), (5, V[0] + np.array([60, -150]), (900, 1950)), (6, V[2] + (V[3] - V[2]) * 0.5 + np.array([0, 25]), (-300, -2150)),
             (7, (C + V[2] + V[3]) / 3, (-900, -1350)), (8, (400 * math.cos(math.radians(200)), 400 * math.sin(math.radians(200))), (-1300, -400))]
    for n, tgt, pos in items:
        K.balloon(ax, tuple(tgt), pos, n, col=ORG if n == 8 else "k")
    xr, y = 228, 268
    y = heading(Pp, xr, y, "What the twelve pentagons do")
    roles = ("Set by Manos on 25 Oct (PROPOSAL for TRUTH; the model and the earlier TRUTH split still show shield, service, docking and greenhouse pentagons).\n"
             "- Eleven identical pentagons: inside, a greenhouse alcove and a service panel connected to the central mast; outside, solar panels on standoffs over an insulating blanket, and a stowed inflatable shield that cuts UV, takes heavy MMOD strikes and can act as a repair balloon (Q89).\n"
             "- One docking pentagon: IDSS ring, 800 mm hatch, the transfer lock and relief valve (RF-04); the hatch stays shut whenever the pressures differ.\n"
             "- Stabilising thrusters, if ever added, live in the pentagons (Q90). Which way the mast runs is open (Q88).\n"
             "- The closure plate carries pressure only; a thin stressed skin would see 190 to 680 MPa. At 3.6 m across it is wider than plate comes, so it is five triangles sealed at the main ribs. Which side of the ribs, and how it is held, is OPEN with Marco (Q57). Drawn on the cabin side at the seat plane, where the glass sits on a hexagon.\n"
             "- Solar cells must stand off the structure: on bare pentagons in full sun the hexagon-pentagon difference could reach about 100 K (about 380 kN on a corner); on a blanket it is 2 to 15 K (model of 1 Nov).\n"
             "- The greenhouses get no daylight: 6 to 9 kW of LED per TRUTH 4; the arrays and batteries for that are not sized.")
    y = note(Pp, xr, y, 176, roles, fs=7.5) - 3
    y = heading(Pp, xr, y, "Key to the balloons")
    parts = ("1  P-06P frame member, 180 deep, with the 50 mm lip (pentagons carry no glass)\n"
             "2  P-04 main rib B (five)\n"
             f"3  P-01 secondary rib segment ({nseg} on the k 4 grid)\n"
             "4  P-05 hub with five arms, a variant of the hexagon hub\n"
             "5  CB-02 corner block, 108°, tie rows z 128.3 / 364.4 (RF-08)\n"
             "6  Hardpoint fitting, three per edge, 15 per pentagon (RF-07)\n"
             "7  PL-01 closure plate, one of five 10 mm 6061-T6 triangles, sealed at the main ribs (hatched)\n"
             "8  Docking pentagon only: 800 mm hatch and IDSS ring (phantom), the transfer lock behind it (RF-04)\n"
             f"Mitre {MP:.3f}°; joint-face features by z' (RF-05 table). The parts library carries the pentagon assembly A-04 and PL-01 (PROPOSAL, 8 Nov; not yet redrawn with the leaning blocks).\n"
             "Corrected 27 Nov: the sheet said 1:20; the view is drawn at 1:25. The callouts are numbered so no text lies on the hatching or runs off the sheet.")
    note(Pp, xr, y, 176, parts, fs=7.5)
    K.save(fig, pdf, f"{OUT}/RF-09_pentagon_GA.png")


PDF_A = "HCSA_RevF_sheets_RF-00_to_RF-04_27Nov2026.pdf"
PDF_B = "HCSA_RevF_flight_sheets_RF-05_to_RF-09_27Nov2026.pdf"

if __name__ == "__main__":
    with PdfPages(f"{OUT}/{PDF_A}") as pdf:
        rf00(pdf); rf01(pdf); rf02(pdf); rf03(pdf); rf04(pdf)
    with PdfPages(f"{OUT}/{PDF_B}") as pdf:
        rf05(pdf); rf06(pdf); rf07(pdf); rf08(pdf); rf09(pdf)
    print("flight sheets ok; bolts per seam:", len(bolts_on_seam()), bolts_on_seam()[:4], "mitres", round(MH, 3), round(MP, 3))
