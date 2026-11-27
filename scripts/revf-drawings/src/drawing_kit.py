"""Shared sheet style for the HCSA Rev F drawings (27 Nov 2026).

Every Rev F sheet (RF-00 to RF-09, TP-00 to TP-04) is drawn with these helpers, so the sheets share one title block,
one set of lettering sizes and one way of stating scale:

- A3 landscape, 420 x 297 mm, frame 10 mm in from the edge, zone marks 1-8 across and A-F down.
- Title block (bottom right, 180 x 62 mm): project, sheet number, revision, issue date, sheet n of N, title, part,
  material, finish, scale, units, third-angle projection symbol, general tolerance note, status, drawn / checked /
  approved, and the use banner (not for machining, or for quotation).
- Everything on the paper is placed in millimetres through one full-page "paper" axes; each drawing view gets its own
  axes at an exact scale (1:n on A3 printed at 100 %), so the scale written on a view is the scale it is drawn at.
- No lettering below 7.5 pt (capitals about 1.9 mm high on A3); notes are wrapped to the space they are given, so no
  text runs off the page or under the title block.
"""
import math, os
from functools import lru_cache
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse, Arc, FancyBboxPatch
from matplotlib.textpath import TextToPath

# ---------------------------------------------------------------- fonts
_INTER = "/usr/share/fonts/opentype/inter"
for _f in ("Inter-Regular.otf", "Inter-Bold.otf", "Inter-SemiBold.otf", "Inter-Italic.otf"):
    _p = os.path.join(_INTER, _f)
    if os.path.exists(_p):
        font_manager.fontManager.addfont(_p)
FONT = "Inter" if any(f.name == "Inter" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": FONT, "font.size": 8.0, "pdf.compression": 6, "axes.unicode_minus": False,
                     "hatch.linewidth": 0.4, "savefig.facecolor": "white"})

# ---------------------------------------------------------------- the sheet
A3 = (420.0, 297.0)                     # mm, landscape
FIGSIZE = (A3[0] / 25.4, A3[1] / 25.4)
MARGIN = 10.0                           # frame line, mm from the paper edge
TB_W, TB_H = 180.0, 62.0                # title block
ISSUE = "27 Nov 2026"                   # date of this issue of every sheet
REV = "F"
DRAWN = "HCSA team"
GENERAL_TOL = "General tolerances ISO 2768-m unless stated. To be confirmed with the shop before any part is made."
FS_MIN = 7.5                            # smallest lettering on any sheet, pt
FS = 8.0                                # notes
FS_LABEL = 8.0                          # labels and dimensions
FS_VIEW = 9.5                           # view titles
PT_MM = 25.4 / 72.0                     # one point in mm

# colours (as on the earlier sheets)
MET, MET2, MET3 = "#9aa3ad", "#c9ced4", "#e4e7ea"
STEEL = "#8a8f96"; GLS = "#bfe3f5"; SEAL = "#222222"
RED = "#b03a2e"; BLU = "#1f5f99"; ORG = "#a8650c"; GRN = "#1e7a44"; TI = "#c9b28a"; GREY = "#555555"


def new_sheet(no, title, *, status, part="-", material="-", finish="-", scale="NTS", banner="NOT FOR MACHINING",
              banner_col=RED, sheet_of=None, tol=GENERAL_TOL, issue=ISSUE, rev=REV):
    """Make an A3 sheet. Returns (fig, P) where P is the paper axes in millimetres (0..420 x 0..297, origin bottom left)."""
    fig = plt.figure(figsize=FIGSIZE)
    P = fig.add_axes([0, 0, 1, 1]); P.set_xlim(0, A3[0]); P.set_ylim(0, A3[1]); P.axis("off"); P.patch.set_alpha(0)
    P.set_zorder(0)
    # frame and zones
    x0, y0, x1, y1 = MARGIN, MARGIN, A3[0] - MARGIN, A3[1] - MARGIN
    P.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=1.1, ec="k"))
    P.add_patch(Rectangle((5, 5), A3[0] - 10, A3[1] - 10, fill=False, lw=0.3, ec="#999"))
    for i in range(8):
        xm = x0 + (i + 0.5) * (x1 - x0) / 8
        for yy in (7.5, A3[1] - 7.5):
            P.text(xm, yy, str(i + 1), ha="center", va="center", fontsize=7.5, color="#666")
        if i:
            xb = x0 + i * (x1 - x0) / 8
            P.plot([xb, xb], [5, y0], lw=0.3, c="#999"); P.plot([xb, xb], [y1, A3[1] - 5], lw=0.3, c="#999")
    for j, L in enumerate("ABCDEF"):
        ym = y1 - (j + 0.5) * (y1 - y0) / 6
        for xx in (7.5, A3[0] - 7.5):
            P.text(xx, ym, L, ha="center", va="center", fontsize=7.5, color="#666")
        if j:
            yb = y1 - j * (y1 - y0) / 6
            P.plot([5, x0], [yb, yb], lw=0.3, c="#999"); P.plot([x1, A3[0] - 5], [yb, yb], lw=0.3, c="#999")
    _title_block(P, no, title, status, part, material, finish, scale, banner, banner_col, sheet_of, tol, issue, rev)
    fig._hcsa = dict(no=no, title=title)
    return fig, P


def _title_block(P, no, title, status, part, material, finish, scale, banner, banner_col, sheet_of, tol, issue, rev):
    W, H = TB_W, TB_H
    x0 = A3[0] - MARGIN - W; y0 = MARGIN
    lw = 0.6
    P.add_patch(Rectangle((x0, y0), W, H, fc="white", ec="k", lw=1.1, zorder=5))
    line = lambda xa, ya, xb, yb, w=lw: P.plot([xa, xb], [ya, yb], lw=w, c="k", zorder=6)
    # rows from the top: project (8), title (11), part/material (8), finish/scale (8), tolerance (6), status (9), people (7), banner (5)
    ys = [y0 + H]
    for h in (8.0, 11.0, 8.0, 8.0, 6.5, 8.5, 7.0):
        ys.append(ys[-1] - h)
    for yy in ys[1:]:
        line(x0, yy, x0 + W, yy)
    xr = x0 + W - 34.0                                      # right column: sheet number and revision
    line(xr, ys[0], xr, ys[2])
    t = lambda x, y, s, **k: P.text(x, y, s, zorder=7, **{"fontsize": FS_MIN, "va": "center", **k})
    t(x0 + 2, (ys[0] + ys[1]) / 2 + 1.6, "HCSA  Human-Centric Space Architecture", fontsize=8.5, weight="bold")
    t(x0 + 2, (ys[0] + ys[1]) / 2 - 1.9, "Brown University and RISD student design study, low Earth orbit observation facility", fontsize=7.5)
    t(xr + 2, (ys[0] + ys[1]) / 2 + 1.6, "SHEET", fontsize=7.5, color="#444")
    t(xr + 2, ys[1] - 4.5, no, fontsize=14, weight="bold")
    t(xr + 22.5, (ys[0] + ys[1]) / 2 + 1.6, "REV", fontsize=7.5, color="#444")
    t(xr + 22.5, ys[1] - 4.5, rev, fontsize=14, weight="bold")
    t(xr + 2, ys[2] + 1.8, f"Sheet {sheet_of}" if sheet_of else "", fontsize=7.5, color="#444")
    ttl = _wrap(title, 11.5, xr - x0 - 4, bold=True)
    if len(ttl) > 2:
        ttl = _wrap(title, 9.5, xr - x0 - 4, bold=True)[:2]
        t(x0 + 2, (ys[1] + ys[2]) / 2, "\n".join(ttl), fontsize=9.5, weight="bold", linespacing=1.05)
    else:
        t(x0 + 2, (ys[1] + ys[2]) / 2, "\n".join(ttl), fontsize=11.5 if len(ttl) == 1 else 9.5, weight="bold", linespacing=1.05)
    # part and material
    xm = x0 + W * 0.5
    line(xm, ys[2], xm, ys[4])
    def cell(xa, ya, yb, wdt, label, value):
        lab = label + "  "
        t(xa + 1.5, (ya + yb) / 2, lab, fontsize=7.5, color="#444")
        lw_ = _text_width(lab, 7.5) + 1.5
        val = _fit(value, wdt - lw_ - 3, 7.5)
        t(xa + lw_ + 1.5, (ya + yb) / 2, val, fontsize=7.5)
    cell(x0, ys[2], ys[3], W * 0.5, "Part", part)
    cell(xm, ys[2], ys[3], W * 0.5, "Material", material)
    cell(x0, ys[3], ys[4], W * 0.5, "Finish", finish)
    # scale, units, projection
    xs = xm
    t(xs + 1.5, (ys[3] + ys[4]) / 2, "Scale", fontsize=7.5, color="#444")
    t(xs + 10.5, (ys[3] + ys[4]) / 2, _fit(scale, 31, 7.5), fontsize=7.5, weight="bold")
    t(xs + 44, (ys[3] + ys[4]) / 2, "Units mm", fontsize=7.5, weight="bold")
    third_angle(P, x0 + W - 13.5, (ys[3] + ys[4]) / 2, h=5.2)
    t(x0 + 1.5, (ys[4] + ys[5]) / 2, _fit(tol, W - 4, 7.5), fontsize=7.5)
    st = _wrap("Status: " + status, 7.5, W - 4)
    if len(st) > 2:
        st = st[:2]; st[1] = _fit(st[1] + " ...", W - 4, 7.5)
    t(x0 + 1.5, (ys[5] + ys[6]) / 2, "\n".join(st), fontsize=7.5, linespacing=1.1)
    # people and issue
    cw = W / 4
    for i in range(1, 4):
        line(x0 + i * cw, ys[6], x0 + i * cw, ys[7])
    for i, (a, b) in enumerate((("Drawn", DRAWN), ("Checked", "-"), ("Approved", "-"), ("Issued", issue))):
        t(x0 + i * cw + 1.5, ys[6] - 2.2, a, fontsize=7.5, color="#444")
        t(x0 + i * cw + 1.5, ys[7] + 2.1, b, fontsize=7.5, weight="bold" if i in (0, 3) else "normal")
    # banner
    P.add_patch(Rectangle((x0, y0), W, ys[7] - y0, fc="#fbeaea" if banner_col == RED else "#fff4e0", ec="k", lw=lw, zorder=6))
    t(x0 + W / 2, (y0 + ys[7]) / 2, banner, fontsize=8, weight="bold", color=banner_col, ha="center")


def third_angle(P, xc, yc, h=5.0):
    """ISO 5456-2 third-angle projection symbol: the frustum's side view (trapezoid) on the left, its end view (two
    circles) on the right; in third angle the trapezoid's small end points toward the circles."""
    D, d, L, gap = h, h / 2, h * 1.1, h * 0.55
    xt0 = xc - (L + gap + D) / 2
    P.add_patch(Polygon([(xt0, yc - D / 2), (xt0 + L, yc - d / 2), (xt0 + L, yc + d / 2), (xt0, yc + D / 2)], closed=True,
                        fill=False, lw=0.6, ec="k", zorder=7))
    xcirc = xt0 + L + gap + D / 2
    P.add_patch(Circle((xcirc, yc), D / 2, fill=False, lw=0.6, ec="k", zorder=7))
    P.add_patch(Circle((xcirc, yc), d / 2, fill=False, lw=0.6, ec="k", zorder=7))
    P.plot([xt0 - 1, xcirc + D / 2 + 1], [yc, yc], lw=0.35, c="k", ls=(0, (4, 1, 1, 1)), zorder=7)
    P.plot([xcirc, xcirc], [yc - D / 2 - 1, yc + D / 2 + 1], lw=0.35, c="k", ls=(0, (4, 1, 1, 1)), zorder=7)


# ---------------------------------------------------------------- text measuring and wrapping
_T2P = TextToPath()


@lru_cache(maxsize=200000)
def _text_width(s, fs, bold=False):
    """width of a single line of text in mm at font size fs (pt)"""
    if not s:
        return 0.0
    prop = FontProperties(family=FONT, size=fs, weight="bold" if bold else "normal")
    w, h, d = _T2P.get_text_width_height_descent(s, prop, ismath=False)
    return w * PT_MM


def _fit(s, width_mm, fs, bold=False):
    s = str(s)
    if _text_width(s, fs, bold) <= width_mm:
        return s
    while s and _text_width(s + "...", fs, bold) > width_mm:
        s = s[:-1]
    return s.rstrip() + "..."


def _wrap(text, fs, width_mm, bold=False):
    """greedy word wrap to a width in mm; keeps explicit line breaks"""
    out = []
    for para in str(text).split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if _text_width(cand, fs, bold) <= width_mm or not cur:
                cur = cand
            else:
                out.append(cur); cur = w
        out.append(cur)
    return out


def note(P, x, y, w, text, fs=FS, color="k", bold=False, ls=1.22, indent=0.0, **kw):
    """Wrapped text block with its top-left corner at (x, y) mm, w mm wide. Returns the y of its bottom edge.
    Paragraphs separated by '\\n'. A line that starts with '- ' is a bullet with a hanging indent."""
    lh = fs * PT_MM * ls
    yy = y
    for para in str(text).split("\n"):
        if para.startswith("- "):
            lines = _wrap(para[2:], fs, w - 3.2, bold)
            for i, ln in enumerate(lines):
                if i == 0:
                    P.text(x + indent, yy, "-", fontsize=fs, va="top", color=color, weight="bold" if bold else "normal", **kw)
                P.text(x + indent + 3.2, yy, ln, fontsize=fs, va="top", color=color, weight="bold" if bold else "normal", **kw)
                yy -= lh
        elif para == "":
            yy -= lh * 0.5
        else:
            for ln in _wrap(para, fs, w - indent, bold):
                P.text(x + indent, yy, ln, fontsize=fs, va="top", color=color, weight="bold" if bold else "normal", **kw)
                yy -= lh
    return yy


def heading(P, x, y, text, fs=9.5, color="k"):
    P.text(x, y, text, fontsize=fs, weight="bold", va="top", color=color)
    return y - fs * PT_MM * 1.55


def table(P, x, y, widths, rows, fs=FS, header=True, ls=1.18, pad=0.9, colors=None, bold_first_col=False, rule_every=True):
    """Table with wrapped cells. widths in mm. rows: list of tuples of strings. Returns the y of the bottom rule."""
    lh = fs * PT_MM * ls
    W = sum(widths)
    yy = y
    P.plot([x, x + W], [yy, yy], lw=0.8 if header else 0.5, c="k")
    for i, r in enumerate(rows):
        is_h = header and i == 0
        cells = [_wrap(str(c), fs, wd - 2 * pad, is_h) for c, wd in zip(r, widths)]
        n = max(len(c) for c in cells)
        h = n * lh + 2 * pad
        xx = x
        for j, (c, wd) in enumerate(zip(cells, widths)):
            col = (colors[i] if colors and colors[i] else "k")
            for k_, ln in enumerate(c):
                P.text(xx + pad, yy - pad - k_ * lh, ln, fontsize=fs, va="top",
                       weight="bold" if (is_h or (bold_first_col and j == 0)) else "normal", color=col)
            xx += wd
        yy -= h
        if is_h:
            P.plot([x, x + W], [yy, yy], lw=0.8, c="k")
        elif rule_every:
            P.plot([x, x + W], [yy, yy], lw=0.25, c="#999")
    P.plot([x, x + W], [yy, yy], lw=0.6, c="k")
    return yy


# ---------------------------------------------------------------- views at an exact scale
def view(fig, rect_mm, scale, centre, flip_y=False, title=None, title_fs=FS_VIEW, frame=False):
    """Axes for a drawing view placed at rect_mm = (x, y, w, h) on the paper, drawn at 1:scale (scale = data mm per paper
    mm; 0.5 means 2:1). centre = data point at the middle of the rectangle. flip_y puts +y down the page."""
    x, y, w, h = rect_mm
    ax = fig.add_axes([x / A3[0], y / A3[1], w / A3[0], h / A3[1]])
    ax.set_aspect("equal"); ax.axis("off"); ax.patch.set_alpha(0)
    cx, cy = centre
    ax.set_xlim(cx - w * scale / 2, cx + w * scale / 2)
    if flip_y:
        ax.set_ylim(cy + h * scale / 2, cy - h * scale / 2)
    else:
        ax.set_ylim(cy - h * scale / 2, cy + h * scale / 2)
    ax._k = scale                     # data mm per paper mm
    ax._flip = flip_y
    if frame:
        ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False, lw=0.4, ec="#999"))
    if title:
        fig.text((x) / A3[0], (y + h + 1.5) / A3[1], title, fontsize=title_fs, weight="bold", va="bottom")
    return ax


def scale_text(scale):
    if scale >= 1:
        return f"1:{scale:g}"
    return f"{1 / scale:g}:1"


def _u(ax, d_mm):
    """paper mm to data units in this view"""
    return d_mm * getattr(ax, "_k", 1.0)


def dim(ax, p0, p1, text, off=8.0, fs=FS_LABEL, col="k", ext=1.5, gap=1.0, text_side=0.0, inside=True, lw=0.5):
    """Aligned dimension between p0 and p1, its line off paper-mm away from the measured points. A positive off puts it
    ABOVE a horizontal dimension and to the RIGHT of a vertical one, as seen on the paper (for a sloping one: to the
    upper left of the line read left to right). Text sits on the line with a white background; text_side slides it
    along the line in paper mm."""
    p0 = (float(p0[0]), float(p0[1])); p1 = (float(p1[0]), float(p1[1]))
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L == 0:
        return
    ux, uy = dx / L, dy / L
    fy = -1.0 if getattr(ax, "_flip", False) else 1.0
    px, py = ux, uy * fy                      # direction on the paper
    if px < -1e-9 or (abs(px) <= 1e-9 and py > 0):
        px, py = -px, -py                     # read left to right; verticals read downward, so +off is to the right
    nx, ny = -py, px * fy                     # left normal on the paper, back in data units
    if abs(px) <= 1e-9:
        nx, ny = 1.0, 0.0
    o = _u(ax, off)
    a = (p0[0] + nx * o, p0[1] + ny * o); b = (p1[0] + nx * o, p1[1] + ny * o)
    s = 1 if off >= 0 else -1
    g, e = _u(ax, gap) * s, _u(ax, ext) * s
    ax.plot([p0[0] + nx * g, a[0] + nx * e], [p0[1] + ny * g, a[1] + ny * e], lw=0.35, c=col, clip_on=False)
    ax.plot([p1[0] + nx * g, b[0] + nx * e], [p1[1] + ny * g, b[1] + ny * e], lw=0.35, c=col, clip_on=False)
    if inside:
        ax.annotate("", b, a, annotation_clip=False, arrowprops=dict(arrowstyle="<|-|>", lw=lw, color=col, shrinkA=0, shrinkB=0, mutation_scale=6))
    else:
        for q, sg in ((a, -1), (b, 1)):
            tip = (q[0], q[1]); tail = (q[0] + sg * ux * _u(ax, 6), q[1] + sg * uy * _u(ax, 6))
            ax.annotate("", tip, tail, annotation_clip=False, arrowprops=dict(arrowstyle="-|>", lw=lw, color=col, shrinkA=0, shrinkB=0, mutation_scale=6))
        ax.plot([a[0], b[0]], [a[1], b[1]], lw=lw, c=col, clip_on=False)
    ang = math.degrees(math.atan2(dy, dx))
    if getattr(ax, "_flip", False):
        ang = -ang
    if ang > 90.01: ang -= 180
    if ang <= -89.99: ang += 180
    mx, my = (a[0] + b[0]) / 2 + ux * _u(ax, text_side), (a[1] + b[1]) / 2 + uy * _u(ax, text_side)
    ax.text(mx, my, text, fontsize=fs, color=col, ha="center", va="center", rotation=ang, rotation_mode="anchor",
            bbox=dict(fc="white", ec="none", pad=0.6), zorder=20)


def leader(ax, target, text_at, text, fs=FS_LABEL, col="k", ha=None, va="center", lw=0.45, bg=True, dot=False, **kw):
    """Leader line from a label at text_at (data coordinates) to target."""
    if ha is None:
        ha = "right" if text_at[0] < target[0] else "left"
    ax.annotate(text, target, text_at, fontsize=fs, color=col, ha=ha, va=va, zorder=21, annotation_clip=False,
                arrowprops=dict(arrowstyle="-|>" if not dot else "-", lw=lw, color=col, shrinkA=1.5, shrinkB=0, mutation_scale=6),
                bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.9) if bg else None, **kw)
    if dot:
        ax.plot([target[0]], [target[1]], marker="o", ms=2.2, c=col, zorder=22)


def balloon(ax, target, at, n, fs=7.5, r=2.6, col="k", dot=True):
    """Numbered item balloon at `at` (data) with a leader to `target`; r in paper mm."""
    rr = _u(ax, r)
    dx, dy = target[0] - at[0], target[1] - at[1]
    L = math.hypot(dx, dy)
    if L > rr:
        sx, sy = at[0] + dx / L * rr, at[1] + dy / L * rr
        ax.plot([sx, target[0]], [sy, target[1]], lw=0.45, c=col, zorder=21, clip_on=False)
    if dot:
        ax.plot([target[0]], [target[1]], marker="o", ms=2.0, c=col, zorder=22)
    ax.add_patch(Circle(at, rr, fc="white", ec=col, lw=0.6, zorder=22, clip_on=False))
    ax.text(at[0], at[1], str(n), fontsize=fs, ha="center", va="center", color=col, zorder=23, weight="bold")


def cl(ax, p0, p1, col="k", lw=0.35):
    """centre line"""
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], lw=lw, c=col, ls=(0, (9, 2, 1.5, 2)))


def label(ax, xy, text, fs=FS_LABEL, col="k", ha="center", va="center", bg=True, **kw):
    return ax.text(xy[0], xy[1], text, fontsize=fs, color=col, ha=ha, va=va, zorder=21,
                   bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.9) if bg else None, **kw)


def legend(P, x, y, items, fs=FS, sw=6.0, row=4.6):
    """swatch legend on the paper: items = [(kind, colour, text)], kind 'fill', 'line', 'dash' or 'hatch'"""
    yy = y
    for kind, colr, text in items:
        if kind == "fill":
            P.add_patch(Rectangle((x, yy - 2.6), sw, 3.2, fc=colr, ec="k", lw=0.4))
        elif kind == "hatch":
            P.add_patch(Rectangle((x, yy - 2.6), sw, 3.2, fc="#eef2f5", ec="#666", lw=0.4, hatch="////"))
        elif kind == "line":
            P.plot([x, x + sw], [yy - 1.0, yy - 1.0], lw=1.6, c=colr)
        elif kind == "dash":
            P.plot([x, x + sw], [yy - 1.0, yy - 1.0], lw=1.0, c=colr, ls="--")
        elif kind == "dot":
            P.add_patch(Circle((x + sw / 2, yy - 1.0), 1.4, fc=colr, ec="k", lw=0.3))
        P.text(x + sw + 2, yy - 1.0, text, fontsize=fs, va="center")
        yy -= row
    return yy


def save(fig, pdf, png_path, dpi=150):
    pdf.savefig(fig)
    fig.savefig(png_path, dpi=dpi)
    plt.close(fig)
