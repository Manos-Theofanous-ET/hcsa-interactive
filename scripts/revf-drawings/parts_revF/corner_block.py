"""Corner blocks CB-01 (hexagon corner, 120 deg) and CB-02 (pentagon corner, 108 deg), 8 Nov 2026 PROPOSAL.
Straight (prismatic along the panel z) like P-06. Vertex at the origin, leg A along +x, panel interior on +y, z 0 outer face,
z 400 cabin face. Leg B is the mirror of leg A across the corner bisector."""
import math
import cadquery as cq

LEG, DEPTH, THK = 230.0, 400.0, 50.0
TIE_HOLE = 23.5          # clearance for the 7/8-14 Inconel 718 stud
DOWEL = 20.0             # 20 mm dowel (room for 24)
POCKET_W = 110.0         # landing for the 100 wide main rib flange, 5 mm a side
R_IN, R_VERTEX, CHAMF = 10.0, 12.0, 2.0
WASHER_R = 22.5          # 7/8 in hardened washer, 45 mm OD, on the inner face
TIE_COLS_BRIEF = (87.0, 143.0)          # two columns 56 apart centred on the 230 leg: clash with the landing (see notes)
TIE_COLS = (136.0, 192.0)               # moved outboard, pitch 56 kept, so a 45 mm washer clears the landing on both blocks


def mirror_pt(p, alpha):
    """reflect (x, y) across the line through the origin at angle alpha (radians)"""
    c, s = math.cos(2 * alpha), math.sin(2 * alpha)
    return (c * p[0] + s * p[1], s * p[0] - c * p[1])


def geometry(theta_deg):
    """all the derived numbers of a block with legs at theta_deg; d is distance along the bisector from the vertex,
    s is the offset perpendicular to the bisector (positive toward leg A)"""
    a = math.radians(theta_deg / 2)
    u = (math.cos(a), math.sin(a))              # bisector
    v = (math.sin(a), -math.cos(a))             # toward leg A
    hw = POCKET_W / 2
    d_re = THK / math.sin(a)                    # re-entrant corner between the legs' inner faces, on the bisector
    d_wall = (THK + hw * math.cos(a)) / math.sin(a)   # where the pocket wall meets a leg's inner face
    d_min = hw / math.tan(a)                    # below this the pocket breaks through the joint faces
    # pocket bottom: deepest position (toward the vertex) that keeps the 110 face continuous (d < d_re) and the wall
    # between the pocket corner and the joint face at or above 20 mm where that is possible
    d_wall20 = (20.0 / math.cos(a) + hw) / math.tan(a)
    d_b = min(round(d_re - 2.0, 0), round(d_wall20, 0))
    wall_min = (d_b * math.tan(a) - hw) * math.cos(a)        # material between pocket corner and joint face
    x_wall = (d_wall * u[0] + hw * v[0])                       # along leg A where the pocket wall meets the inner face
    return dict(alpha=a, u=u, v=v, hw=hw, d_re=d_re, d_wall=d_wall, d_min=d_min, d_b=d_b, wall_min=wall_min,
                x_wall=x_wall, wall_len=d_wall - d_b, pocket_depth_at_bisector=d_re - d_b)


def outline(theta_deg):
    g = geometry(theta_deg)
    a, u, v, hw, d_b, d_wall = g["alpha"], g["u"], g["v"], g["hw"], g["d_b"], g["d_wall"]
    P = lambda d, s: (d * u[0] + s * v[0], d * u[1] + s * v[1])
    p0 = (0.0, 0.0)
    p1 = (LEG, 0.0)
    p2 = (LEG, THK)
    p3 = P(d_wall, hw)
    p4 = P(d_b, hw)       # concave, R10
    p5 = P(d_b, -hw)      # concave, R10
    p6 = mirror_pt(p3, a)
    p7 = mirror_pt(p2, a)
    p8 = mirror_pt(p1, a)
    pts = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    convex = [p0, p1, p2, p3, p6, p7, p8]
    concave = [p4, p5]
    return pts, convex, concave, g


def _vertical_edges_at(shape, pts, tol=0.5):
    out = []
    for e in shape.edges("|Z").vals():
        c = e.Center()
        for p in pts:
            if abs(c.x - p[0]) < tol and abs(c.y - p[1]) < tol:
                out.append(e)
                break
    return out


def corner_block(theta_deg, tie_z, dowel_z, tie_cols=TIE_COLS, log=None):
    log = log if log is not None else []
    pts, convex, concave, g = outline(theta_deg)
    s = cq.Workplane("XY").polyline(pts).close().extrude(DEPTH)
    v0 = s.val().Volume()
    # 1. R10 at the two inside corners of the landing (machining-driven: an end mill of 20 mm or less)
    try:
        s = s.newObject(_vertical_edges_at(s, concave)).fillet(R_IN)
    except Exception as e:
        log.append(f"R{R_IN} pocket fillets failed: {e}")
    # 2. 2 mm chamfer on the convex vertical edges
    try:
        s = s.newObject(_vertical_edges_at(s, convex)).chamfer(CHAMF)
    except Exception as e:
        log.append(f"vertical edge chamfers failed: {e}")
    # 3. 2 mm chamfer on the outer and cabin face outlines
    for sel in (">Z", "<Z"):
        try:
            s = s.faces(sel).edges().chamfer(CHAMF)
        except Exception as e:
            log.append(f"face {sel} outline chamfer failed: {e}")
    v1 = s.val().Volume()
    # 4. holes in leg A (axis along y, through the 50 thickness), then mirrored into leg B
    cutters = []
    for x in tie_cols:
        for z in tie_z:
            cutters.append(cq.Workplane("XZ").center(x, z).circle(TIE_HOLE / 2).extrude(-(THK + 2)).translate((0, -1, 0)))
        cutters.append(cq.Workplane("XZ").center(x, dowel_z).circle(DOWEL / 2).extrude(-(THK + 2)).translate((0, -1, 0)))
    a = g["alpha"]
    nrm = (math.sin(a), -math.cos(a), 0)
    for c in cutters:
        s = s.cut(c)
        s = s.cut(c.mirror(mirrorPlane=cq.Vector(*nrm), basePointVector=(0, 0, 0)))
    v2 = s.val().Volume()
    expected = 2 * sum(math.pi * (TIE_HOLE / 2) ** 2 * THK for _ in tie_cols for _ in tie_z) + 2 * sum(math.pi * (DOWEL / 2) ** 2 * THK for _ in tie_cols)
    g.update(volume_prism=v0, volume_after_blends=v1, volume_final=v2, hole_volume=v1 - v2, hole_volume_expected=expected,
             n_tie_holes=2 * len(tie_cols) * len(tie_z), n_dowel_holes=2 * len(tie_cols))
    return s, g, log


if __name__ == "__main__":
    import json
    for th, tz, dz in ((120, (125.0, 355.0), 240.0), (108, (128.3, 364.4), 246.3)):
        s, g, log = corner_block(th, tz, dz)
        bb = s.val().BoundingBox()
        print(th, "bbox", round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1), "xmin", round(bb.xmin, 1), "ymin", round(bb.ymin, 1))
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in g.items() if k not in ("u", "v")})
        print("log", log)
