"""Rev F flight sheets RF-05 to RF-09 (8 Nov 2026), replacing the Rev E draft sheets RE-04 to RE-07 of 24 Oct.
Drawn from hcsa_params_revF.json and the parts library masses in matplotlib. Dimensioned 2D sheets, not CAD sections.
"""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, Wedge, FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(HERE, "..", "src", "hcsa_params_revF.json"))); v = lambda g, k: P[g][k][0]
A3 = (16.54, 11.69); MET = "#9aa3ad"; MET2 = "#c9ced4"; MET3 = "#e4e7ea"; GLS = "#bfe3f5"; SEAL = "#222"; RED = "#c0392b"; BLU = "#1f5f99"; ORG = "#b9770e"; GRN = "#1e8449"; TI = "#b9a37a"
EDGE = v("geometry", "edge"); K = v("geometry", "grid_k"); PITCH = EDGE / K
MH, MP = 20.905, 16.472  # mitre angles, hexagon and pentagon
D = v("frame", "depth"); WEB = v("frame", "web"); LIP_H = v("frame", "seat_lip_hex")
Z1, Z2 = v("seal", "outer_cord_z"), v("seal", "outer_cord_z") + v("seal", "centreline_spacing"); ZR, ZB = 42.0, v("seam_bolt", "row_z")
TP = v("pane", "thickness")
MASS = {"P-01": 2.53, "P-02": 1.75, "P-03": 4.38, "P-04": 33.24, "P-04A": 12.77, "P-05": 28.28, "P-05A": 14.20, "P-06": 27.86, "P-07": 5.50, "P-08": 0.19, "P-14": 0.03}

def sheet(no, title, status):
    fig = plt.figure(figsize=A3)
    fig.add_artist(Rectangle((0.01, 0.01), 0.98, 0.98, fill=False, lw=1.5, transform=fig.transFigure))
    tb = fig.add_axes([0.60, 0.012, 0.39, 0.12]); tb.axis("off"); tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=1.2))
    for y in (0.75, 0.5, 0.25): tb.plot([0, 1], [y, y], lw=0.6, c="k")
    tb.plot([0.6, 0.6], [0, 0.75], lw=0.6, c="k")
    tb.text(0.02, 0.86, f"HCSA  {no}  {title}", fontsize=10.5, weight="bold", va="center")
    tb.text(0.02, 0.62, "Rev F flight design, 8 Nov 2026. Replaces the Rev E draft sheet of 24 Oct", fontsize=6.8, va="center")
    tb.text(0.02, 0.37, f"Status: {status[:92]}", fontsize=6.2, va="center")
    tb.text(0.02, 0.12, "Drawn: Claude for M. Theofanous    Checked: -    Released: -", fontsize=8, va="center")
    tb.text(0.62, 0.62, "mm. Drawn from the parameters", fontsize=7.5, va="center")
    tb.text(0.62, 0.37, "PROPOSAL where marked", fontsize=7.5, va="center")
    tb.text(0.62, 0.12, "Not for machining", fontsize=7.5, va="center", color=RED)
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

def reflect(pts, u):
    """reflect points about a line through the origin with unit direction u"""
    u = np.asarray(u, float); R = 2 * np.outer(u, u) - np.eye(2)
    return (np.asarray(pts, float) @ R.T)

def seam_bolt_positions():
    """16 bolts per seam from a vertex: bays between the corner blocks (230) and the three 200-wide fittings"""
    pos = []
    bays = [(230, PITCH - 100), (PITCH + 100, 2 * PITCH - 100), (2 * PITCH + 100, 3 * PITCH - 100), (3 * PITCH + 100, EDGE - 230)]
    for a, b in bays:
        n = int((b - a - 30) // 75) + 1
        f0 = (b - a - (n - 1) * 75) / 2
        pos += [a + f0 + i * 75 for i in range(n)]
    return pos

# ---------------- RF-05 seam cross-section of the flight design ----------------
def rf05(pdf):
    fig = sheet("RF-05", "Seam cross-section, hexagon to hexagon, at the first bolt", "frame 180, gland, bolt decided 5 Nov; hardpoint position open; outer layers OPEN-11")
    ax = fig.add_axes([0.03, 0.17, 0.60, 0.76]); ax.set_aspect("equal"); ax.axis("off")
    m = math.radians(MH); u = np.array([-math.sin(m), math.cos(m)])          # joint plane direction, from the outer edge inward
    nrm = np.array([-math.cos(m), -math.sin(m)])                               # into the left panel, normal to the joint plane
    def jp(s, off=0.0): return s * u + off * nrm                                 # point at z' = s, offset into the left panel
    def draw_panel(mirror, col, grooved):
        T = (lambda p: reflect(p, u)) if mirror else (lambda p: np.asarray(p, float))
        web = np.array([jp(0), jp(D), jp(D, WEB), jp(0, WEB)])
        ax.add_patch(Polygon(T(web), fc=col, ec="k", lw=0.8))
        # flange (z 0-10) and seat lip (z 170-180), horizontal in the panel, from the web's back face
        xb0 = -WEB / math.cos(m)   # web back face at z = 0, panel x
        def strip(z0, z1, w):
            xb = lambda z: xb0 - z * math.tan(m)
            pts = np.array([[xb(z0), z0], [xb(z0) - w, z0], [xb(z1) - w, z1], [xb(z1), z1]])
            ax.add_patch(Polygon(T(pts), fc=col, ec="k", lw=0.8))
        strip(0, 10, 50); strip(170, 180, LIP_H)
        # glass stack in the panel (positions of L1, L4, L5, L6 are the Rev E stack proposal, OPEN-11)
        xb = lambda z: xb0 - z * math.tan(m)
        def layer(z0, z1, x0off, w, fc, ec, lw=0.7):
            pts = np.array([[xb(z0) - x0off, z0], [xb(z0) - x0off - w, z0], [xb(z1) - x0off - w, z1], [xb(z1) - x0off, z1]])
            ax.add_patch(Polygon(T(pts), fc=fc, ec=ec, lw=lw))
        layer(182, 182 + TP, 10, 200, GLS, BLU)          # L7 pressure pane on the seat, 2 mm strip, 10 mm clear of the web
        layer(180, 182, 10, 200, "#555", "none")          # setting strip
        layer(12, 18, 8, 200, "#dff1fa", BLU, 0.5)        # L1 outer pane, 6 mm fused silica (proposal position)
        layer(40, 43.3, 8, 200, "#e8f4fb", BLU, 0.4)      # L4 solar substrate
        layer(50, 53.3, 8, 200, "#e8f4fb", BLU, 0.4)      # L5 tint substrate
        layer(95, 115, 8, 200, "#f3f3f3", "#888", 0.4)    # L6 shade envelope
        layer(230, 236, 10, 200, "#fff6e0", "#aa8", 0.5)  # cabin scratch pane, acrylic, unloaded
        # secondary rib (I 180 x 60 x 10) 562.5 mm in from the seam is off the sheet; the main-rib cap angles sit at z 375-400 (not on this section)
        return T
    TL = draw_panel(False, MET2, True); TR = draw_panel(True, MET3, False)
    # seals, port, RTV, bolt on the joint plane (frame B side)
    for s in (Z1, Z2):
        g = np.array([jp(s - 3.55), jp(s + 3.55), jp(s + 3.55, 4.0), jp(s - 3.55, 4.0)]); ax.add_patch(Polygon(g, fc="white", ec="k", lw=0.5))
        c = jp(s, 2.0); ax.add_patch(Circle(c, 2.67, fc=SEAL, ec="none"))
    c = jp(ZR, 1.5); ax.add_patch(Circle(c, 3, fc="#7a5", ec="k", lw=0.4))
    b0, b1 = jp(ZB, WEB + 8), reflect(jp(ZB, WEB + 8), u)
    ax.plot([b0[0], b1[0]], [b0[1], b1[1]], c="#555", lw=5, solid_capstyle="butt")
    for p, w in ((jp(ZB, WEB + 1.6), 5), (reflect(jp(ZB, WEB + 1.6), u), 6)): ax.add_patch(Circle(p, 6.5, fc="#777", ec="k", lw=0.4))
    # hardpoint envelopes (dashed) on the panel side of the web, both positions
    for (za, zb, col, lab) in ((110, 170, ORG, "TP3 fitting as drawn, z' 110-170"), (46, 106, GRN, "TP3 moved onto the pull line, z' 46-106 (HP1M)")):
        e = np.array([jp(za, WEB), jp(zb, WEB), jp(zb, WEB + 30), jp(za, WEB + 30)]); ax.add_patch(Polygon(e, fill=False, ec=col, lw=1.0, ls="--"))
        ax.add_patch(Polygon(reflect(e, u), fill=False, ec=col, lw=1.0, ls="--"))
        ax.annotate(lab, jp((za + zb) / 2, WEB + 30), (-250, 150 if col == ORG else 125), fontsize=6.8, color=col, arrowprops=dict(arrowstyle="->", lw=0.6, color=col))
    # joint plane and panel normal
    p0, p1 = jp(-30), jp(D + 60); ax.plot([p0[0], p1[0]], [p0[1], p1[1]], ls="-.", lw=0.6, c=RED); ax.text(*(jp(D + 70)), "joint plane (radial)", fontsize=7, color=RED, ha="center")
    ax.plot([-20, -20], [-40, -5], lw=0.5, c="k"); ax.annotate("", (-20, -5), (-20, -40), arrowprops=dict(arrowstyle="->", lw=0.6)); ax.text(-24, -45, "panel normal", fontsize=6.5, ha="right")
    ax.add_patch(Arc((0, 0), 90, 90, theta1=90, theta2=90 + MH, lw=0.6, color=RED)); ax.text(-30, 52, f"{MH} deg", fontsize=7, color=RED)
    # dims along the joint plane
    for s, lab, zt in ((Z1, "z' 18 outer gland, 7.1 x 4.0", 28), (Z2, "z' 32 inner gland", 62), (ZR, "z' 42 RTV566 bead, R3 recess", 76), (ZB, "z' 58 seam bolt NAS6705U27, 4 kN", 90)):
        ax.annotate(lab, jp(s, 2), (-250, zt), fontsize=6.8, va="center", ha="left", arrowprops=dict(arrowstyle="->", lw=0.5, color="#333"))
    pA, pB = jp(0, -60), jp(D, -60); ax.annotate("", pA, pB, arrowprops=dict(arrowstyle="<->", lw=0.7)); ax.text(*(jp(D / 2, -74)), "180 along the joint plane", fontsize=7, rotation=90 - MH, ha="center", va="center")
    ax.text(-250, 212, "L7: 21 mm BOROFLOAT 33 on a 2 mm strip, 10 mm clear of the web at its cabin face;\nthe 56.6 lip gives 20.0 mm of bite (OPEN-17)", fontsize=6.8, color=BLU, va="top")
    ax.text(-250, 248, "cabin scratch pane, cast acrylic, unloaded (envelope)", fontsize=6.5, color="#886")
    ax.text(-250, 4, "L1 6 mm fused silica, gap vented to space (position: Rev E stack proposal)", fontsize=6.5, color=BLU)
    ax.text(-250, 44, "L4 solar and L5 tint, 3.3 mm substrates; L6 shade envelope at z 95-115 (OPEN-11)", fontsize=6.5, color=BLU)
    ax.set_xlim(-260, 300); ax.set_ylim(275, -70)   # z down the page
    ax.set_title("Section normal to a hexagon-to-hexagon seam at the first bolt (271.25 mm from the vertex). Space side at the top. Frame B (left) carries the glands.", fontsize=9)
    # z' table
    ax2 = fig.add_axes([0.65, 0.45, 0.33, 0.46]); ax2.axis("off"); ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
    ax2.text(0, 1.0, "Joint-face features, placed along the joint plane (z')", fontsize=9.5, weight="bold", va="top")
    ax2.text(0, 0.95, "Panel depth = z' x cos(mitre): hexagon 0.9342, pentagon 0.9590. Both frames of a seam share the plane, so holes and glands line up on hexagon-to-pentagon seams too (OPEN-9).", fontsize=6.8, va="top", wrap=True)
    rows = [("Feature", "z'", "Hexagon z", "Pentagon z")]
    for lab, s in (("Outer gland", Z1), ("Leak port", 25), ("Inner gland", Z2), ("RTV recess", ZR), ("Seam bolt row", ZB), ("TP3 pads, as drawn", "110-170"), ("TP3 pads, moved (HP1M)", "46-106"), ("Corner tie rows", "133.8, 380.0")):
        if isinstance(s, str):
            a = [float(x) for x in s.replace("-", ",").split(",")]
            rows.append((lab, s, ", ".join(f"{x*math.cos(math.radians(MH)):.1f}" for x in a).replace(", ", "-" if "-" in s else ", "), ", ".join(f"{x*math.cos(math.radians(MP)):.1f}" for x in a).replace(", ", "-" if "-" in s else ", ")))
        else:
            rows.append((lab, f"{s:.0f}", f"{s*math.cos(math.radians(MH)):.2f}", f"{s*math.cos(math.radians(MP)):.2f}"))
    for i, r in enumerate(rows):
        y = 0.80 - i * 0.065
        for c, t in zip((0, 0.42, 0.62, 0.82), r): ax2.text(c, y, t, fontsize=7.4, weight="bold" if i == 0 else "normal", va="top")
        if i == 0: ax2.plot([0, 1], [y - 0.03, y - 0.03], lw=0.6, c="k")
    ax2.text(0, 0.20, "Seal: two loops of Parker BA500 butyl 5.33 mm in 7.1 x 4.0 glands (25 % squeeze, 79 % fill), RTV566 bead cured on the ground (Q80).\nBolt: NAS6705U27 A286 with KFN670 nut, 4 kN by torque, 16 per seam at 75 pitch in bays of 3, 5, 5, 3.\nLoop corners: R16 minimum at the corner block, OPEN (Q92).", fontsize=7.2, va="top")
    fig.text(0.03, 0.14, "What changed from RE-04 (24 Oct): frame 140 to 180; pane 22 to 21 mm; bolt NAS6705U27 at 4 kN (was NAS9306C-06, a rivet standard); the lip and seat moved to the cabin face (z 170-180, P-06) for the restack (Q78);\n"
             "the hardpoint shown in both positions because the fitting as drawn fails the HP1 seal check (0.22 atm free) and the moved fitting holds (0.064 mm at 1.93 atm); Rick decides on 10 Nov. Shear along the seam goes to the hardpoint pins and the\n"
             "vertex dowels, no shear key (OPEN-15, confirmed by FEA 24 Oct). Secondary ribs (I 180 x 60 x 10) and the main rib cap angles (z 375-400) are off this section: see RF-01 and RF-06.", fontsize=7.4, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/RF-05_seam_section.png", dpi=130); plt.close(fig)

# ---------------- hexagon geometry helpers ----------------
def hex_vertices(R=EDGE):
    return [np.array([R * math.cos(math.radians(60 * i)), R * math.sin(math.radians(60 * i))]) for i in range(6)]

def grid_segments(c, a, b, k=K):
    """secondary rib segments inside triangle (c, a, b): lines parallel to each side at i = 1..k-1"""
    segs = []
    P_ = lambda i, j: c + (a - c) * (i / k) + (b - c) * (j / k)
    for i in range(1, k):
        for j in range(0, k - i):      # parallel to side cb: from P(i, j) to P(i, j+1)
            segs.append((P_(i, j), P_(i, j + 1)))
            segs.append((P_(j, i), P_(j + 1, i)))   # parallel to side ca
        for j in range(0, i):          # parallel to side ab: points with i+j = const = k - (k - i)... use P(k - i + ... )
            pass
    # lines parallel to ab: i + j = s for s = 1..k-1, from P(s - t, t) to P(s - t - 1, t + 1)
    for s in range(1, k):
        for t in range(0, s):
            segs.append((P_(s - t, t), P_(s - t - 1, t + 1)))
    return segs

# ---------------- RF-06 hexagon general arrangement ----------------
def rf06(pdf):
    fig = sheet("RF-06", "Hexagon panel, general arrangement and parts list", "ribs and frame decided; blocks, hardpoints, nodes PROPOSAL; model masses")
    ax = fig.add_axes([0.02, 0.14, 0.60, 0.80]); ax.set_aspect("equal"); ax.axis("off")
    V = hex_vertices(); C = np.zeros(2)
    ax.add_patch(Polygon(V, fc="#f4f6f8", ec="k", lw=1.0))
    # frames: 120 wide band inside the edge
    for i in range(6):
        A, B = V[i], V[(i + 1) % 6]; mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        band = np.array([A, B, B + inward * 120, A + inward * 120]); ax.add_patch(Polygon(band, fc=MET2, ec="k", lw=0.5))
    # panes
    for i in range(6):
        A, B = V[i], V[(i + 1) % 6]
        for ii in range(K):
            for jj in range(K - ii):
                p = lambda i_, j_: C + (A - C) * (i_ / K) + (B - C) * (j_ / K)
                t1 = [p(ii, jj), p(ii + 1, jj), p(ii, jj + 1)]; ax.add_patch(Polygon(t1, fc=GLS, ec=BLU, lw=0.3))
                if jj < K - ii - 1:
                    t2 = [p(ii + 1, jj), p(ii + 1, jj + 1), p(ii, jj + 1)]; ax.add_patch(Polygon(t2, fc=GLS, ec=BLU, lw=0.3))
    # secondary ribs
    nseg = 0
    for i in range(6):
        for a, b in grid_segments(C, V[i], V[(i + 1) % 6]):
            ax.plot([a[0], b[0]], [a[1], b[1]], c=MET, lw=2.2, solid_capstyle="butt"); nseg += 1
    # main ribs
    for i in range(6): ax.plot([0, V[i][0]], [0, V[i][1]], c="#7f8a94", lw=4.5, solid_capstyle="butt")
    ax.add_patch(Circle((0, 0), 90, fc="#777", ec="k", lw=0.6))
    # corner blocks and hardpoint blocks
    for i in range(6):
        A = V[i]; prev, nxt = V[(i - 1) % 6], V[(i + 1) % 6]
        for B in (prev, nxt):
            d = (B - A) / np.linalg.norm(B - A); inward = (C - A) / np.linalg.norm(C - A)
            nn = np.array([-d[1], d[0]]);
            if np.dot(nn, inward) < 0: nn = -nn
            ax.add_patch(Polygon([A, A + d * 230, A + d * 230 + nn * 50, A + nn * 50], fc="#8a8f96", ec="k", lw=0.5))
        B = nxt; d = (B - A) / np.linalg.norm(B - A); mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        for q in (1, 2, 3):
            hc = A + d * (q * PITCH); ax.add_patch(Polygon([hc - d * 120, hc + d * 120, hc + d * 120 + inward * 50, hc - d * 120 + inward * 50], fc=TI, ec="k", lw=0.5))
    # seam bolts on edge 0 (from V0 to V1)
    A, B = V[0], V[1]; d = (B - A) / np.linalg.norm(B - A); mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
    bolts = seam_bolt_positions()
    for s in bolts: ax.add_patch(Circle(A + d * s + inward * 58 * 0.9342, 14, fc="#444", ec="none"))
    # dimensions
    dim(ax, (V[3][0], -2500), (V[0][0], -2500), f"{2*EDGE:.0f} across corners", off=0, fs=8)
    ax.plot([V[3][0], V[3][0]], [V[3][1], -2500], lw=0.4, c="k"); ax.plot([V[0][0], V[0][0]], [V[0][1], -2500], lw=0.4, c="k")
    yF = EDGE * math.sin(math.radians(60))
    dim(ax, (2850, -yF), (2850, yF), f"{2*yF:.1f} across flats", off=0, horiz=False, fs=8)
    ax.plot([V[1][0], 2850], [yF, yF], lw=0.4, c="k"); ax.plot([V[5][0], 2850], [-yF, -yF], lw=0.4, c="k")
    for q in (1, 2, 3):
        hc = A + d * (q * PITCH) + inward * (-110); ax.text(hc[0], hc[1], f"HP{q}", fontsize=6.5, ha="center", color=ORG)
    ax.text(0, 2420, "16 seam bolts per edge at 75 pitch in bays of 3, 5, 5, 3 (dots on the upper right edge); the first bolt 271.25 from the vertex; hardpoints HP at 562.5, 1125, 1687.5", fontsize=6.8, ha="center", color="#444")
    ax.text(0, -2650 - 200, f"k 4 grid: {PITCH:.1f} mm pitch, {nseg} secondary rib segments, 96 panes (48 full triangles, 48 cut back at the frame and the hub), 18 six-way nodes, 18 crossings on the main ribs, 18 hardpoints", fontsize=7.5, ha="center")
    ax.set_xlim(-2800, 3150); ax.set_ylim(-3000, 2600)
    ax.set_title("Hexagon from the cabin side (schematic, 1:20 on A3): frames, six main ribs, the k 4 secondary grid, hub, corner blocks (grey), hardpoint blocks (gold), 96 panes", fontsize=9)
    # sections inset
    axs = fig.add_axes([0.63, 0.55, 0.35, 0.37]); axs.set_aspect("equal"); axs.axis("off")
    def ibeam(xc, d, bf, tf, tw, col=MET2):
        axs.add_patch(Rectangle((xc - bf / 2, -tf), bf, tf, fc=col, ec="k", lw=0.7)); axs.add_patch(Rectangle((xc - tw / 2, -d + tf), tw, d - 2 * tf, fc=col, ec="k", lw=0.7))
        axs.add_patch(Rectangle((xc - bf / 2, -d), bf, tf, fc=col, ec="k", lw=0.7))
    ibeam(0, 400, 100, 25, 8); axs.add_patch(Rectangle((-50, -400), 100, 25, fc="#b0b7be", ec="k", lw=0.7))
    axs.add_patch(Rectangle((-34, -180), 30, 10, fc=MET2, ec="k", lw=0.5)); axs.add_patch(Rectangle((4, -180), 30, 10, fc=MET2, ec="k", lw=0.5))
    for s in (-1, 1): axs.add_patch(Rectangle((min(s * 9.09, s * 150), -180 - 2 - TP), abs(150 - 9.09), TP, fc=GLS, ec=BLU, lw=0.6))
    ibeam(320, 180, 60, 10, 5)
    for s in (-1, 1): axs.add_patch(Rectangle((320 + min(s * 9.09, s * 120), -180 - 2 - TP), abs(120 - 9.09), TP, fc=GLS, ec=BLU, lw=0.6))
    axs.text(0, 40, "Main rib B: I 400 x 100 x 25, web 8\nseat ledges at z 170-180, cap angles P-04A at z 375-400", fontsize=6.8, ha="center")
    axs.text(320, 40, "Secondary rib: I 180 x 60 x 10, web 5\npane seat on the cabin face z 180", fontsize=6.8, ha="center")
    axs.text(160, -440, "21 mm panes on 2 mm setting strips, cut 9.09 mm short of the rib centre lines; bite 40.9 (main) and 20.9 (secondary); P-11 brace at every crossing (RF-08 note)", fontsize=6.4, ha="center")
    axs.set_xlim(-170, 470); axs.set_ylim(-470, 90)
    # parts list
    axp = fig.add_axes([0.63, 0.14, 0.35, 0.40]); axp.axis("off"); axp.set_xlim(0, 1); axp.set_ylim(0, 1)
    axp.text(0, 1.0, "Parts list, one hexagon (model masses)", fontsize=9.5, weight="bold", va="top")
    rows = [("Part", "Qty", "Each kg", "Total kg"),
            ("P-06 frame member, 180 deep", 6, MASS["P-06"]), ("P-04 main rib B", 6, MASS["P-04"]), ("P-04A cap angle", 12, MASS["P-04A"]),
            ("P-05 hub core", 1, MASS["P-05"]), ("P-05A hub star plate", 2, MASS["P-05A"]), ("P-01 secondary rib segment", 108, MASS["P-01"]),
            ("P-02 node star plate", 36, MASS["P-02"]), ("P-03 node web core", 18, MASS["P-03"]), ("P-07 pane, 21 mm", 96, MASS["P-07"]),
            ("P-08 pane corner clamp", 18, MASS["P-08"]), ("P-14 seam bolt (half of 16 x 6)", 48, MASS["P-14"]),
            ("CB-01 corner block, 2219 (see parts library)", 6, None), ("HP-01/02/03 hardpoint block, fittings, pins", 18, None), ("P-11 main rib brace pair", 18, None)]
    tot = 0.0
    for i, r in enumerate(rows):
        y = 0.92 - i * 0.058
        if i == 0:
            for c, t in zip((0, 0.62, 0.74, 0.88), r): axp.text(c, y, t, fontsize=7.2, weight="bold", va="top")
            axp.plot([0, 1], [y - 0.028, y - 0.028], lw=0.6, c="k"); continue
        nm, q, e = r; t = (q * e) if e else None; tot += t or 0
        for c, s in zip((0, 0.62, 0.74, 0.88), (nm, str(q), f"{e:.2f}" if e else "-", f"{t:.0f}" if t else "-")): axp.text(c, y, s, fontsize=6.9, va="top")
    axp.text(0, 0.04, f"Listed parts: {tot:.0f} kg; with the corner blocks, hardpoints and braces the model panel is about 1.7 t (shell model: 36.1 t for 32 panels).", fontsize=7, va="top", color="#444")
    pdf.savefig(fig); fig.savefig(f"{OUT}/RF-06_hexagon_GA.png", dpi=130); plt.close(fig)

# ---------------- RF-07 hardpoint ----------------
def rf07(pdf):
    fig = sheet("RF-07", "Seam hardpoint: block, TP3 fitting, both positions", "PROPOSAL; as drawn fails HP1, moved passes; decision Tue 10 Nov")
    # plan of the seam at a hardpoint (looking at the joint face)
    ax = fig.add_axes([0.03, 0.50, 0.58, 0.42]); ax.set_aspect("equal"); ax.axis("off")
    L = 500; x0 = -L / 2
    ax.add_patch(Rectangle((x0, 0), L, D, fc=MET2, ec="k", lw=0.8))
    ax.add_patch(Rectangle((-120, 0), 240, D, fc="#b0b7be", ec="k", lw=0.8)); ax.text(0, D + 12, "local block in the frame, 50 thick over 240 (web 20 elsewhere)", ha="center", fontsize=7)
    for zc in (Z1, Z2): ax.plot([x0, x0 + L], [zc, zc], c=SEAL, lw=1.6)
    ax.plot([x0, x0 + L], [ZR, ZR], c="k", lw=0.5, ls=":")
    for xb in (-120 - 31.25, 120 + 31.25, -120 - 31.25 - 75, 120 + 31.25 + 75): ax.add_patch(Circle((xb, ZB), 4.25, fc="white", ec="k", lw=0.6))
    for (zc, col, lab) in ((140, ORG, "as drawn: pads z' 110-170"), (76, GRN, "moved: pads z' 46-106")):
        for j in (-1, 0, 1): ax.add_patch(Circle((j * 60, zc), 20, fill=False, ec=col, lw=1.2, ls="-" if col == ORG else "--"))
        ax.add_patch(Rectangle((-100, zc - 30), 200, 60, fill=False, ec=col, lw=0.8, ls="--")); ax.text(140, zc, lab, fontsize=7, color=col, va="center")
    dim(ax, (-60, 76), (60, 76), "2 x 60", off=-40, fs=6.5); dim(ax, (-120, 0), (-120 - 31.25, 0), "31.25", off=-12, fs=6.5)
    dim(ax, (-120, D), (120, D), "240 block", off=30, fs=6.5); dim(ax, (-100, D), (100, D), "200 fitting", off=46, fs=6.5)
    ax.set_xlim(x0 - 20, x0 + L + 150); ax.set_ylim(-60, D + 70)
    ax.set_title("Joint face at a hardpoint: the 50 mm block, the three 40 mm pin bores at 60 pitch, the two seam bolts beside the fitting (31.25 from its faces)", fontsize=8.5)
    # section across the seam
    ax2 = fig.add_axes([0.62, 0.50, 0.36, 0.42]); ax2.set_aspect("equal"); ax2.axis("off")
    for sgn, col in ((-1, MET2), (1, MET3)):
        ax2.add_patch(Rectangle((0 if sgn > 0 else -50, 0), 50, D, fc=col, ec="k", lw=0.8))
    for (zc, col) in ((140, ORG), (76, GRN)):
        ax2.add_patch(Rectangle((-80, zc - 20), 160, 40, fc="#ddd", ec=col, lw=1.0, ls="-" if col == ORG else "--"))   # pin through both blocks and both fittings
        for sgn in (-1, 1): ax2.add_patch(Rectangle((50 if sgn > 0 else -80, zc - 30), 30, 60, fill=False, ec=col, lw=1.0, ls="-" if col == ORG else "--"))
        ax2.text(95, zc, "fitting 30 thick\n(Ti-6Al-4V)", fontsize=6.5, va="center", color=col)
    ax2.add_patch(Rectangle((-50, ZB - 4), 100, 8, fc="#555", ec="k", lw=0.5)); ax2.text(55, ZB, "seam bolt z' 58", fontsize=6.5, va="center")
    for s in (Z1, Z2): ax2.add_patch(Circle((-2, s), 2.67, fc=SEAL, ec="none"))
    ax2.plot([0, 0], [-10, D + 10], ls="-.", lw=0.6, c=RED)
    ax2.set_xlim(-130, 170); ax2.set_ylim(D + 20, -20)
    ax2.set_title("Section across the seam (space side at the top): pin 40 x 160 through fitting, block, block, fitting", fontsize=8)
    fig.text(0.03, 0.46, "What the models say (HP1, 6-7 Nov). As drawn, the fitting sits 64 mm deeper than the line of the pull (about 76 mm), so the two frames hinge about it and the seals open: the gap between the cords\n"
             "reaches 0.11 mm at 0.22 atm with the frames free to turn and 0.47 atm with them held, against the 1.93 atm required; the two plain bolts beside the fitting carry about 60 kN at 1.96 atm, nearly twice\n"
             "their breaking load, and the frame yields round their holes from about 0.5 atm. With the fitting moved onto the line of the pull (pads 46 to 106), the hardpoint seal gap is 0.064 mm at 1.93 atm and stays\n"
             "under 0.11 mm to 2.5 atm; the plain bolts stay at 13 kN. One place is marginal in the moved case: the seal band at the plain bolt next to the fitting reaches 0.11 mm at 1.87 atm. The fitting in the model is\n"
             "a spring between rigid pads, not pins and bores, so the real part has to be drawn and rerun. The 2 Nov figures of 2.9 to 3.4 atm are withdrawn.\n\n"
             "Clash to resolve in the moved position: a 40 mm bore at z' 76 spans z' 56 to 96 and crosses the bolt row at z' 58. Either the two bolts beside the fitting move deeper (about z' 110), or the pins shrink to 32 mm\n"
             "at z' 80 (z' 64-96), or the bolt row near the fitting is dropped and the fitting takes the clamping too. Also open: the fitting's fixing to the aluminium block, the bore chamfers at 1.5 x proof\n"
             "(194-197 MPa against 160, Q18, about 19 % lower at 0.8 atm), galling (dry-film lubricant on the pins), and the seal loops passing the fitting. Fitting stiffness 2.876 million N/mm (C3). Load 108.7 kN per atm on the worst hardpoint.", fontsize=7.2, va="top")
    axt = fig.add_axes([0.03, 0.14, 0.55, 0.12]); axt.axis("off"); axt.set_xlim(0, 1); axt.set_ylim(0, 1)
    axt.text(0, 1, "The three hardpoints on a 2,250 mm seam, from the vertex", fontsize=8.5, weight="bold", va="top")
    for i, (hp, b1, b2) in enumerate(((562.5, 421.25, 693.75), (1125.0, 993.75, 1256.25), (1687.5, 1556.25, 1818.75))):
        axt.text(0, 0.68 - i * 0.22, f"HP{i+1} at {hp:.1f}: fitting faces {hp-100:.1f} and {hp+100:.1f}; nearest bolts {b1} (41.25 off the outer face) and {b2} (31.25 off the inner face)", fontsize=7.2, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/RF-07_hardpoint.png", dpi=130); plt.close(fig)

# ---------------- RF-08 corner node ----------------
def rf08(pdf):
    fig = sheet("RF-08", "Corner node: blocks, ties, dowels, what the model says, machining", "PROPOSAL; ties, preload decided; radii per Marco; O10 seal, rib landing open")
    ax = fig.add_axes([0.03, 0.50, 0.40, 0.42]); ax.set_aspect("equal"); ax.axis("off")
    # plan of a hexagon corner block: legs 230 x 50 at 120 deg, vertex at origin, leg A along +x, interior on +y
    a2 = math.radians(120); dB = np.array([math.cos(a2), math.sin(a2)])
    legA = np.array([[0, 0], [230, 0], [230, 50], [50 / math.tan(a2 / 2), 50]]);
    legB = np.array([[0, 0], 230 * dB, 230 * dB + 50 * np.array([math.sin(a2), -math.cos(a2)]), [50 / math.tan(a2 / 2), 50]])
    ax.add_patch(Polygon(legA, fc="#8a8f96", ec="k", lw=0.8)); ax.add_patch(Polygon(legB, fc="#8a8f96", ec="k", lw=0.8))
    ax.add_patch(Polygon([[50 / math.tan(a2 / 2), 50], [50 / math.tan(a2 / 2) + 60, 50 + 60 * math.tan(math.radians(60))], [50 / math.tan(a2 / 2) + 60 - 110 * math.sin(math.radians(60)), 50 + 60 * math.tan(math.radians(60)) + 110 * math.cos(math.radians(60))]], fill=False, ec=ORG, lw=0.8, ls="--"))
    ax.text(70, 140, "main rib landing (notch 110 x 30, R10)", fontsize=6.5, color=ORG)
    ax.add_patch(Arc((50 / math.tan(a2 / 2) + 12, 62), 24, 24, theta1=120, theta2=240, lw=0.8, color=RED)); ax.text(20, 95, "R12", fontsize=7, color=RED)
    for xc in (118, 174): ax.add_patch(Circle((xc, 25), 11.75, fc="white", ec="k", lw=0.5))
    ax.text(146, -22, "tie columns 56 apart (2 rows in depth)", fontsize=6.5, ha="center")
    dim(ax, (0, 0), (230, 0), "230", off=-45, fs=7); dim(ax, (230, 0), (230, 50), "50", off=20, horiz=False, fs=7)
    ax.add_patch(Arc((0, 0), 120, 120, theta1=0, theta2=120, lw=0.6, color=RED)); ax.text(40, 75, "120 deg (108 on a pentagon block)", fontsize=6.5, color=RED)
    ax.text(0, -70, "joint faces: the legs' outer faces, on the radial joint planes", fontsize=6.5)
    ax.set_xlim(-150, 300); ax.set_ylim(-90, 280); ax.set_title("Plan of one hexagon corner block (CB-01), looking at the cabin face", fontsize=8.5)
    # joint face view
    ax2 = fig.add_axes([0.45, 0.50, 0.25, 0.42]); ax2.set_aspect("equal"); ax2.axis("off")
    ax2.add_patch(Rectangle((0, 0), 230, 400, fc="#8a8f96", ec="k", lw=0.8))
    for z in (125, 355):
        for xc in (118, 174): ax2.add_patch(Circle((xc, z), 11.75, fc="white", ec="k", lw=0.6))
    for xc in (50, 210): ax2.add_patch(Circle((xc, 240), 10, fc="white", ec="k", lw=0.5, ls="--"))
    dim(ax2, (0, 0), (0, 125), "125", off=-20, horiz=False, fs=6.5); dim(ax2, (0, 0), (0, 355), "355", off=-38, horiz=False, fs=6.5)
    dim(ax2, (118, 400), (174, 400), "56", off=12, fs=6.5); dim(ax2, (230, 0), (230, 400), "400", off=16, horiz=False, fs=6.5)
    ax2.text(115, -40, "4 ties 7/8-14 Inconel 718 (23.5 holes), 2 dowels 20 (24 room)\nhexagon rows z 125 / 355, pentagon rows z 128.3 / 364.4", fontsize=6.3, ha="center", va="top")
    ax2.set_xlim(-60, 290); ax2.set_ylim(-110, 440); ax2.set_title("Joint face of a leg (z' 133.8 and 380 along the plane)", fontsize=8)
    # results and notes
    axr = fig.add_axes([0.72, 0.50, 0.27, 0.42]); axr.axis("off"); axr.set_xlim(0, 1); axr.set_ylim(0, 1)
    axr.text(0, 1, "What the corner model says (C1, 5 Nov)", fontsize=8.5, weight="bold", va="top")
    for i, t in enumerate(["Tie preload 198 kN, held to 196.5-198.1 kN, by stretch", "Worst tie at proof, 0.8 atm: 214.5 kN (limit 227)", "Pentagon 15 K warmer: 213.3 kN", "Hatch open, 1 atm: 226.3 kN, 0.7 kN under the limit", "Faces open at proof: 0.55 mm (0.74 at 1 atm), limit 0.8", "Block stress, 95th percentile: 236 MPa (255 at 1 atm), no limit set yet", "Worst corner load 235 kN at 0.8 atm, 290 at 1 atm"]):
        axr.text(0, 0.90 - i * 0.1, "- " + t, fontsize=7.0, va="top")
    fig.text(0.03, 0.46, "Making it (Marco, 7 Nov). As drawn the node cannot be machined: every inside corner needs a radius an end mill can cut (R10 here, R12 at the re-entrant vertex corner), and the part could be cast instead\n"
             "of machined from a 2219-T852 hand forging (about 300 mm of stock for the 400 mm deep block), which may change the alloy. Both routes are open for Friday. The main rib's flanges enter the block at the\n"
             "vertex landing (notch, PROPOSAL); the two frame members run into the legs' inner faces; the tie-to-web-fillet clash (Q29), the O10 maze-patch corner seal and the loop corners R16 (Q27, Q92) are open.\n"
             "The ties are tightened by measured stretch, because a torque wrench scatters about 25 % and the hatch-open case leaves only 0.7 kN. Forces Marco called 'achievable but unreasonable': 198 kN per tie\n"
             "(about 650-900 N m if torqued), 12 ties per node, 720 on the station. The corner node assembly A-03 (two hexagon blocks and one pentagon block at a real vertex, dihedral 138.19 / 142.62 deg) is in the parts library.\n\n"
             "Main rib lateral brace (new requirement, 4 Nov): the main rib buckles sideways if unbraced over 2.25 m (0.79 of its load) and has 8.4 times margin braced every 562.5 mm. P-11 (PROPOSAL): a pair of 8 mm\n"
             "7075 plates on the main rib web from z 180 to z 375 at every secondary rib crossing, bolted through the web, tying the cabin flange to the grid. Size to be checked.", fontsize=7.2, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/RF-08_corner_node.png", dpi=130); plt.close(fig)

# ---------------- RF-09 pentagon GA ----------------
def rf09(pdf):
    fig = sheet("RF-09", "Pentagon panel, general arrangement, roles, docking", "ribs and frame decided; closure plate side OPEN (Q57); roles PROPOSAL (25 Oct)")
    ax = fig.add_axes([0.02, 0.14, 0.56, 0.80]); ax.set_aspect("equal"); ax.axis("off")
    Rc = EDGE / (2 * math.sin(math.radians(36))); V = [np.array([Rc * math.cos(math.radians(90 + 72 * i)), Rc * math.sin(math.radians(90 + 72 * i))]) for i in range(5)]; C = np.zeros(2)
    ax.add_patch(Polygon(V, fc="#f4f6f8", ec="k", lw=1.0))
    for i in range(5):
        A, B = V[i], V[(i + 1) % 5]; mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        ax.add_patch(Polygon([A, B, B + inward * 120, A + inward * 120], fc=MET2, ec="k", lw=0.5))
    # closure plate as five triangles, hatched, cut back 100 from the main ribs and the frame
    for i in range(5):
        A, B = V[i], V[(i + 1) % 5]
        tri = np.array([C, A, B]); cen = tri.mean(axis=0); shrunk = cen + (tri - cen) * 0.86
        ax.add_patch(Polygon(shrunk, fc="#e9eef2", ec="#666", lw=0.5, hatch="///"))
    nseg = 0
    for i in range(5):
        for a, b in grid_segments(C, V[i], V[(i + 1) % 5]):
            ax.plot([a[0], b[0]], [a[1], b[1]], c=MET, lw=2.0, solid_capstyle="butt"); nseg += 1
    for i in range(5): ax.plot([0, V[i][0]], [0, V[i][1]], c="#7f8a94", lw=4.5, solid_capstyle="butt")
    ax.add_patch(Circle((0, 0), 90, fc="#777", ec="k", lw=0.6))
    ax.add_patch(Circle((0, 0), 400, fill=False, ec=ORG, lw=1.2, ls="--")); ax.add_patch(Circle((0, 0), 620, fill=False, ec=ORG, lw=0.8, ls=":"))
    ax.text(0, -470, "docking pentagon only: 800 mm hatch and IDSS ring (phantom), transfer lock behind", fontsize=6.8, ha="center", color=ORG)
    a2 = math.radians(108)
    for i in range(5):
        A = V[i]
        for B in (V[(i - 1) % 5], V[(i + 1) % 5]):
            d = (B - A) / np.linalg.norm(B - A); inward = (C - A) / np.linalg.norm(C - A); nn = np.array([-d[1], d[0]])
            if np.dot(nn, inward) < 0: nn = -nn
            ax.add_patch(Polygon([A, A + d * 230, A + d * 230 + nn * 50, A + nn * 50], fc="#8a8f96", ec="k", lw=0.5))
        B = V[(i + 1) % 5]; d = (B - A) / np.linalg.norm(B - A); mid = (A + B) / 2; inward = (C - mid) / np.linalg.norm(C - mid)
        for q in (1, 2, 3):
            hc = A + d * (q * PITCH); ax.add_patch(Polygon([hc - d * 120, hc + d * 120, hc + d * 120 + inward * 50, hc - d * 120 + inward * 50], fc=TI, ec="k", lw=0.5))
    ri = Rc * math.cos(math.radians(36))
    dim(ax, (-Rc * math.sin(math.radians(72)) - 300, -ri), (-Rc * math.sin(math.radians(72)) - 300, Rc), f"{Rc + ri:.1f} vertex to flat", off=0, horiz=False, fs=7.5)
    dim(ax, (V[2][0], -ri - 300), (V[3][0], -ri - 300), f"{EDGE:.0f} edge", off=0, fs=7.5)
    ax.text(0, -ri - 650, f"k 4 grid: {nseg} secondary rib segments, 5 main ribs, 5 corner blocks, 15 hardpoints; closure plate 10 mm 6061-T6 as five triangles (hatched), sealed at the main ribs", fontsize=7.3, ha="center")
    ax.set_xlim(-2700, 2500); ax.set_ylim(-2700, 2300)
    ax.set_title("Pentagon from the cabin side (schematic, 1:20 on A3): the same frame, main rib and secondary rib parts as the hexagon, no glass, a 10 mm closure plate", fontsize=9)
    axt = fig.add_axes([0.60, 0.42, 0.38, 0.50]); axt.axis("off"); axt.set_xlim(0, 1); axt.set_ylim(0, 1)
    axt.text(0, 1, "What the twelve pentagons do", fontsize=9.5, weight="bold", va="top")
    axt.text(0, 0.95, "Set by Manos on 25 Oct (PROPOSAL for TRUTH; the model and the earlier TRUTH split still show shield, service, docking and greenhouse pentagons):", fontsize=7, va="top", wrap=True)
    for i, t in enumerate(["Eleven identical pentagons: inside, a greenhouse alcove and a service panel connected to the central mast; outside, solar panels on standoffs over an insulating blanket, and a stowed inflatable shield that cuts UV, takes heavy MMOD strikes and can act as a repair balloon (Q89).",
                           "One docking pentagon: IDSS ring, 800 mm hatch, the transfer lock and relief valve (RF-04); the hatch stays shut whenever the pressures differ.",
                           "Stabilising thrusters, if ever added, live in the pentagons (Q90). Which way the mast runs is open (Q88).",
                           "The closure plate carries pressure only; a thin stressed skin would see 190 to 680 MPa. At 3.6 m across it is wider than plate comes, so it is five triangles sealed at the main ribs. Which side of the ribs, and how it is held, is OPEN with Marco (Q57). Drawn here on the cabin side at the seat plane, where the glass sits on a hexagon.",
                           "Solar cells must stand off the structure: on bare pentagons in full sun the hexagon-pentagon difference could reach about 100 K (about 380 kN on a corner); on a blanket it is 2 to 15 K (1 Nov model).",
                           "The greenhouses get no daylight: 6 to 9 kW of LED per TRUTH 4; the arrays and batteries for that are not sized."]):
        axt.text(0, 0.84 - i * 0.135, "- " + "\n  ".join(__import__("textwrap").wrap(t, 100)), fontsize=6.6, va="top")
    fig.text(0.60, 0.38, "Pentagon frame: P-06 at 180 deep with the 50 mm lip (pentagons carry no glass). Main ribs P-04 (five), hub P-05 with five arms (variant of the hexagon hub).\n"
             "Corner blocks CB-02 (108 deg, tie rows z 128.3 / 364.4). Hardpoints as RF-07. Mitre 16.472 deg; joint-face features by z' (RF-05 table).\nThe parts library carries the pentagon assembly A-04 and the closure triangle PL-01 (PROPOSAL, 8 Nov).", fontsize=7.2, va="top")
    pdf.savefig(fig); fig.savefig(f"{OUT}/RF-09_pentagon_GA.png", dpi=130); plt.close(fig)

if __name__ == "__main__":
    with PdfPages(f"{OUT}/HCSA_RevF_flight_sheets_RF-05_to_RF-09_8Nov2026.pdf") as pdf:
        rf05(pdf); rf06(pdf); rf07(pdf); rf08(pdf); rf09(pdf)
    print("flight sheets ok; bolts per seam:", len(seam_bolt_positions()), seam_bolt_positions()[:4])
