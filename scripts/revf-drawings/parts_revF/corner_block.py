"""Corner blocks CB-01 (hexagon corner, 120 deg) and CB-02 (pentagon corner, 108 deg) with LEANING joint faces,
9 Nov 2026 PROPOSAL (supersedes the straight blocks of 8 Nov, kept in corner_block_straight.py).

Frame of a block (panel-local, mm): the true polyhedron vertex at the origin, leg A along +x (a shell edge), the panel
interior on +y, z the depth into the cabin (z 0 outer face of the panel, z 400 cabin face).  Leg B is the mirror of leg A
across the vertical plane through the corner bisector.

True geometry used here
  * The joint face of a seam is the radial plane through the shell edge and the sphere centre.  Seen from the panel it leans
    toward the panel interior with depth by the mitre m (20.905 deg hexagon, 16.472 deg pentagon; computed exactly below).
  * The two joint planes of a corner meet on the VERTEX LINE (vertex to sphere centre), the spine of the block.  In the
    panel frame the vertex line leans along the corner bisector by atan(tan m / sin(theta/2)) (23.80 deg hexagon, 20.08 deg
    pentagon), so everything that belongs to the corner moves along the bisector by k z with k = tan m / sin(theta/2).
  * The block is therefore an OBLIQUE PRISM: one constant outline swept along the vertex line and cut flat at the panel
    planes z 0 and z 400.  Joint faces, leg inner faces (parallel to the joint faces, 50 mm away measured normal to them),
    leg end faces, the rib landing walls and bottom and its R10 corners are all parallel to the vertex line.
  * Positions on a joint face are given as (xs, z'): z' down the leaning face from the shell edge (z = z' cos m on the face),
    xs along the edge direction FROM THE VERTEX LINE at that depth.  From the z 0 vertex the same point is at
    x = xs + Q z', Q = sin m / tan(theta/2) = 0.20601 for both blocks (the vertex line is 11.64 deg off square to an edge).
  * Tie and dowel holes are normal to the joint face.
"""
import math
import cadquery as cq

EDGE = 2250.0
LEG, DEPTH, THK = 230.0, 400.0, 50.0     # leg length from the vertex line along the edge; depth in z; leg thickness NORMAL to the joint face
TIE_HOLE = 23.5          # clearance for the 7/8-14 Inconel 718 stud
DOWEL = 20.0             # 20 mm dowel (room for 24)
POCKET_W = 110.0         # landing for the 100 wide main rib flange, 5 mm a side
R_IN, CHAMF = 10.0, 2.0
WASHER_R = 22.5          # 7/8 in hardened washer, 45 mm OD, on the leg's inner face
TIE_COLS_BRIEF = (87.0, 143.0)
TIE_COLS_8NOV = (136.0, 192.0)
TIE_COLS = (130.0, 186.0)                # xs: see columns_allowed(); pitch 56 kept
ROWS_ZP = (133.8, 380.0)                 # tie rows, z' down the joint face (the same on both blocks so they meet)
DOWEL_ZP = 256.9

_R_CIRC = EDGE / 4.0 * math.sqrt(58.0 + 18.0 * math.sqrt(5.0))        # circumradius of the truncated icosahedron, 5575.54


def mitre(n_sides):
    """lean of the radial joint plane from the panel normal, radians (exact): tan m = apothem / distance of the face from the centre"""
    r = EDGE / (2 * math.sin(math.pi / n_sides))
    ap = EDGE / (2 * math.tan(math.pi / n_sides))
    return math.atan(ap / math.sqrt(_R_CIRC ** 2 - r ** 2))


def mirror_pt(p, alpha):
    """reflect (x, y) across the line through the origin at angle alpha (radians)"""
    c, s = math.cos(2 * alpha), math.sin(2 * alpha)
    return (c * p[0] + s * p[1], s * p[0] - c * p[1])


def geometry(theta_deg):
    """derived numbers.  d = distance along the bisector from the vertex line, s = offset perpendicular to the bisector plane
    (positive toward leg A); both are the same at every depth because the block is a prism along the vertex line."""
    n_sides = 6 if abs(theta_deg - 120) < 1e-6 else 5
    a = math.radians(theta_deg / 2)
    m = mitre(n_sides)
    th = THK / math.cos(m)                       # leg thickness in a section parallel to the panel plane
    k = math.tan(m) / math.sin(a)                # shift of the vertex line along the bisector per mm of z
    q = math.sin(m) / math.tan(a)                # shift of the vertex line along the edge per mm of z' (0.20601)
    u = (math.cos(a), math.sin(a)); v = (math.sin(a), -math.cos(a))
    hw = POCKET_W / 2
    d_re = th / math.sin(a)                                        # re-entrant corner between the two inner faces
    d_wall = (th + hw * math.cos(a)) / math.sin(a)                 # where the pocket wall meets a leg's inner face
    d_min = hw / math.tan(a)                                       # below this a 110 pocket breaks through the joint faces
    wall = lambda d: (d * math.sin(a) - hw * math.cos(a)) * math.cos(m)     # metal, normal to the joint face, pocket sharp corner to joint face
    d_wall20 = (20.0 / math.cos(m) + hw * math.cos(a)) / math.sin(a)
    # pocket bottom: the deepest position toward the vertex line that keeps a continuous 110 mm bearing face (2 mm short of the
    # re-entrant corner) and, where that allows it, 20 mm of metal to the joint face
    d_b = min(math.floor(d_re - 2.0), math.ceil(d_wall20))
    sigma = (k * math.cos(a), k * math.sin(a), 1.0)                # vertex line direction per unit z
    xs_wall = (hw + THK * math.cos(m) * math.cos(a)) / math.sin(a) # pocket wall edge on the leg inner face, as xs
    cosb = 1.0 / math.hypot(1.0, q)                                # the vertex line is atan(q) off square to the edge, in the joint face
    return dict(n_sides=n_sides, alpha=a, mitre=m, mitre_deg=math.degrees(m), th=th, k=k, q=q, u=u, v=v, hw=hw, d_re=d_re, d_wall=d_wall,
                d_min=d_min, d_b=d_b, wall_min=wall(d_b), wall_len=d_wall - d_b, pocket_depth_at_bisector=d_re - d_b, sigma=sigma,
                spine_lean_deg=math.degrees(math.atan(k)), xs_wall=xs_wall, cosb=cosb,
                zp_joint_end=DEPTH / math.cos(m),                                   # z' where the joint face meets z 400
                zp_inner=(THK * math.tan(m), (DEPTH + THK * math.sin(m)) / math.cos(m)))   # z' range of the inner face between z 0 and z 400


def columns_allowed():
    """nearest tie column (xs, mm from the vertex line along the edge) at which a 45 mm washer seats clear of the main rib landing"""
    out = {}
    for th in (120, 108):
        g = geometry(th)
        out[th] = dict(pocket_edge_xs=g["xs_wall"], hole_tangent=g["xs_wall"] + TIE_HOLE / 2 / g["cosb"],
                       washer_tangent_sharp_edge=g["xs_wall"] + WASHER_R / g["cosb"],
                       washer_clear_of_chamfer=g["xs_wall"] + (WASHER_R + CHAMF) / g["cosb"])
    return out


def outline(theta_deg, z=0.0):
    """outline of the block in the plane at depth z (parallel to the panel): the z 0 outline moved k z along the bisector"""
    g = geometry(theta_deg)
    a, u, v, hw, d_b, d_wall, th = g["alpha"], g["u"], g["v"], g["hw"], g["d_b"], g["d_wall"], g["th"]
    sh = (g["sigma"][0] * z, g["sigma"][1] * z)
    P = lambda d, s: (d * u[0] + s * v[0], d * u[1] + s * v[1])
    p0 = (0.0, 0.0); p1 = (LEG, 0.0); p2 = (LEG, th)
    p3 = P(d_wall, hw); p4 = P(d_b, hw); p5 = P(d_b, -hw)       # p4, p5 concave (R10)
    p6 = mirror_pt(p3, a); p7 = mirror_pt(p2, a); p8 = mirror_pt(p1, a)
    mv = lambda p: (p[0] + sh[0], p[1] + sh[1])
    pts = [mv(p) for p in (p0, p1, p2, p3, p4, p5, p6, p7, p8)]
    convex = [pts[i] for i in (0, 1, 2, 3, 6, 7, 8)]
    concave = [pts[4], pts[5]]
    return pts, convex, concave, g


def face_frame(g):
    """unit vectors of leg A's joint face: ex along the edge, t down the face (z'), nu the normal pointing INTO the leg"""
    m = g["mitre"]
    return (1.0, 0.0, 0.0), (0.0, math.sin(m), math.cos(m)), (0.0, math.cos(m), -math.sin(m))


def hole_table(theta_deg, tie_cols=TIE_COLS):
    """every hole of leg A and leg B: kind, diameter, a point on the joint face, the axis (into the leg), xs and z'"""
    g = geometry(theta_deg)
    ex, t, nu = face_frame(g)
    a = g["alpha"]; c2, s2 = math.cos(2 * a), math.sin(2 * a)
    mir = lambda p: (c2 * p[0] + s2 * p[1], s2 * p[0] - c2 * p[1], p[2])
    out = []
    for xs in tie_cols:
        for kind, dia, zp in [("tie", TIE_HOLE, z) for z in ROWS_ZP] + [("dowel", DOWEL, DOWEL_ZP)]:
            x = xs + g["q"] * zp
            c = (x, zp * t[1], zp * t[2])
            out.append(dict(leg="A", kind=kind, dia=dia, xs=xs, zp=zp, x_from_z0_vertex=x, centre=c, axis=nu))
            out.append(dict(leg="B", kind=kind, dia=dia, xs=xs, zp=zp, x_from_z0_vertex=x, centre=mir(c), axis=mir(nu)))
    return out


def _proj(pt, g):
    """slide a point along the vertex line to z 0"""
    return (pt.x - g["sigma"][0] * pt.z, pt.y - g["sigma"][1] * pt.z)


def _spine_edges_at(solid, pts, g, tol=0.3):
    sg = cq.Vector(*g["sigma"]).normalized()
    out = []
    for e in solid.Edges():
        if e.geomType() != "LINE":
            continue
        d = (e.endPoint() - e.startPoint())
        if d.Length < 5 or abs(abs(d.normalized().dot(sg)) - 1) > 1e-6:
            continue
        p = _proj(e.startPoint(), g)
        if any(abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol for q in pts):
            out.append(e)
    return out


def prism(pts, g, z0, z1):
    """the outline (given at z 0) swept along the vertex line from depth z0 to z1"""
    sg = g["sigma"]
    w = cq.Wire.makePolygon([cq.Vector(p[0] + sg[0] * z0, p[1] + sg[1] * z0, z0) for p in pts], close=True)
    f = cq.Face.makeFromWires(w)
    return cq.Solid.extrudeLinear(f, cq.Vector(*sg) * (z1 - z0))


def pocket_air(theta_deg, z0=-40.0, z1=DEPTH + 40.0, reach=400.0):
    """the open space of the rib landing (sharp corners), for clearance measurements"""
    g = geometry(theta_deg); u, v, hw, d_b = g["u"], g["v"], g["hw"], g["d_b"]
    P = lambda d, s: (d * u[0] + s * v[0], d * u[1] + s * v[1])
    return prism([P(d_b, hw), P(d_b + reach, hw), P(d_b + reach, -hw), P(d_b, -hw)], g, z0, z1)


def corner_block(theta_deg, tie_cols=TIE_COLS, log=None, holes=True):
    log = log if log is not None else []
    pts, convex, concave, g = outline(theta_deg)
    over = 60.0
    s = prism(pts, g, -over, DEPTH + over)
    v0 = prism(pts, g, 0.0, DEPTH).Volume()
    # 1. R10 at the two inside corners of the landing: true R10 (a 20 mm ball or bull-nose cutter run along the vertex line)
    try:
        s = s.fillet(R_IN, _spine_edges_at(s, concave, g))
    except Exception as e:
        log.append(f"R{R_IN} pocket fillets failed: {e}")
    # 2. 2 mm chamfer on the convex edges that run along the vertex line (the spine itself, the leg ends, the landing mouth)
    try:
        s = s.chamfer(CHAMF, None, _spine_edges_at(s, convex, g))
    except Exception as e:
        log.append(f"chamfers along the vertex line failed: {e}")
    # 3. cut flat to the panel planes z 0 and z 400
    slab = cq.Workplane("XY").box(2000, 2000, DEPTH, centered=(True, True, False)).val()
    s = s.intersect(slab)
    # 4. 2 mm chamfer round the outer and cabin face outlines
    for zc, name in ((0.0, "outer"), (DEPTH, "cabin")):
        try:
            edges = [e for e in s.Edges() if abs(e.startPoint().z - zc) < 1e-6 and abs(e.endPoint().z - zc) < 1e-6 and abs(e.Center().z - zc) < 1e-6]
            s = s.chamfer(CHAMF, None, edges)
        except Exception as e:
            log.append(f"{name} face outline chamfer failed: {e}")
    v1 = s.Volume()
    # 5. holes normal to the joint faces, through the 50 mm legs
    table = hole_table(theta_deg, tie_cols)
    if holes:
        for h in table:
            c = cq.Vector(*h["centre"]); ax = cq.Vector(*h["axis"])
            s = s.cut(cq.Solid.makeCylinder(h["dia"] / 2, THK + 4.0, c - ax * 2.0, ax))
    v2 = s.Volume()
    expected = sum(math.pi * (h["dia"] / 2) ** 2 * THK for h in table)
    g.update(volume_prism=v0, volume_after_blends=v1, volume_final=v2, hole_volume=v1 - v2, hole_volume_expected=expected,
             n_tie_holes=sum(1 for h in table if h["kind"] == "tie"), n_dowel_holes=sum(1 for h in table if h["kind"] == "dowel"), holes=table)
    return cq.Workplane("XY").newObject([s]), g, log


if __name__ == "__main__":
    print({k: {kk: round(vv, 2) for kk, vv in d.items()} for k, d in columns_allowed().items()})
    for th in (120, 108):
        s, g, log = corner_block(th)
        bb = s.val().BoundingBox()
        print(th, "bbox", round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1), "valid", s.val().isValid(), "kg", round(s.val().Volume() * 2.84e-6, 3))
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in g.items() if k not in ("u", "v", "holes", "sigma", "zp_inner")}, g["zp_inner"])
        print("log", log)
