"""Montage of the leaning corner blocks and the mated corner node (9 Nov 2026): line views from the SVG exports, a shaded view of the
three blocks mated at the vertex, and a section square to the vertex line through the first tie column.
Run after build_parts_revF.py and postprocess.py:  python3 montage_corner.py"""
import json, os, subprocess
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/claude/package/parts_revF/out"
PARTS = json.load(open(f"{OUT}/parts.json")); CHECKS = json.load(open(f"{OUT}/checks.json"))
PDIR = f"{OUT}/stl/_parts/A-03_corner_node"
MAN = json.load(open(f"{PDIR}/manifest.json"))
BLOCK_COL = {"pent": (0.86, 0.60, 0.36), "hex1": (0.42, 0.60, 0.80), "hex2": (0.50, 0.74, 0.52)}

def load():
    out = []; nh = 0
    for e in MAN:
        m = trimesh.load(f"{PDIR}/{e['file']}", force="mesh")
        if "block" in e["label"]:
            if e["label"].startswith("pent"): key, name = "pent", "CB-02 (pentagon)"
            else: nh += 1; key, name = f"hex{nh}", f"CB-01 (hexagon {nh})"
            out.append((e["label"], name, m, BLOCK_COL[key]))
        else:
            out.append((e["label"], "tie" if e["label"].startswith("tie") else "dowel", m, (0.35, 0.37, 0.42)))
    return out

def shaded(parts, path, elev, azim, title, blocks_only=True):
    fig = plt.figure(figsize=(7.5, 6.6), dpi=130); ax = fig.add_subplot(111, projection="3d")
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    allv = []
    for label, name, m, col in parts:
        if blocks_only and "block" not in label:
            continue
        tri = m.vertices[m.faces]; n = m.face_normals
        sh = 0.45 + 0.55 * np.abs(n @ light)
        fc = np.clip(np.outer(sh, np.array(col)), 0, 1)
        ax.add_collection3d(Poly3DCollection(tri, facecolors=fc, edgecolors="none", linewidths=0))
        allv.append(m.vertices)
    allv = np.vstack(allv); c = (allv.max(0) + allv.min(0)) / 2; r = (allv.max(0) - allv.min(0)).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] + r, c[2] - r)      # +z is inward (cabin), drawn downward
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
    ax.set_title(title, fontsize=10)
    fig.subplots_adjust(0, 0, 1, 0.94); fig.savefig(path); plt.close(fig)

def section(parts, path, z):
    fig, ax = plt.subplots(figsize=(7.5, 6.6), dpi=130)
    seen = set()
    for label, name, m, col in parts:
        sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None:
            continue
        p2, T = sec.to_planar(to_2D=np.eye(4)) if hasattr(sec, "to_planar") else sec.to_2D(to_2D=np.eye(4))
        for poly in p2.polygons_full:
            xy = np.array(poly.exterior.coords)
            is_block = "block" in label
            ax.fill(xy[:, 0], xy[:, 1], color=col, alpha=0.95 if is_block else 1.0, zorder=2 if is_block else 3, ec="k", lw=0.5, label=None if name in seen else name)
            seen.add(name)
            for hole in poly.interiors:
                h = np.array(hole.coords); ax.fill(h[:, 0], h[:, 1], color="white", zorder=2.5, ec="k", lw=0.4)
    ax.plot([0], [0], "k+", ms=10, zorder=5)
    ax.set_aspect("equal"); ax.legend(fontsize=7, loc="upper right"); ax.tick_params(labelsize=7)
    ax.set_title(f"Section square to the vertex line, {z:.0f} mm in from the vertex (first tie column, row 1): three blocks, no overlap", fontsize=8.5)
    ax.set_xlabel("mm (node frame, x along the hex-hex edge)", fontsize=7)
    fig.tight_layout(); fig.savefig(path); plt.close(fig)

def svg_tile(fn, path):
    subprocess.run(["rsvg-convert", "-w", "900", "-b", "white", f"{OUT}/svg/{fn}.svg", "-o", path], check=True)
    im = Image.open(path).convert("RGB")
    bb = Image.eval(im.convert("L"), lambda p: 255 - p).getbbox()
    if bb:
        im = im.crop((max(bb[0] - 20, 0), max(bb[1] - 20, 0), min(bb[2] + 20, im.width), min(bb[3] + 20, im.height)))
    im.save(path)

if __name__ == "__main__":
    parts = load()
    t = "/tmp/mc_"
    svg_tile("CB-01_iso", t + "0.png"); svg_tile("CB-02_iso", t + "1.png"); svg_tile("A-03_corner_node_iso", t + "2.png")
    shaded(parts, t + "3.png", 62, -60, "The three blocks mated at the vertex, seen from outside (space side up)")
    shaded(parts, t + "4.png", -55, 40, "The same from the cabin: the three rib landings and the leg inner faces")
    section(parts, t + "5.png", 162.8)
    w = CHECKS["A-03"]["worst"]; c1, c2 = CHECKS["CB-01"]["clearances"], CHECKS["CB-02"]["clearances"]
    caps = [f"CB-01 hexagon corner block, {PARTS['CB-01']['mass_kg']:.2f} kg: joint faces lean 20.905 deg, vertex line 23.80 deg",
            f"CB-02 pentagon corner block, {PARTS['CB-02']['mass_kg']:.2f} kg: joint faces lean 16.472 deg, vertex line 20.08 deg",
            f"A-03 node, {PARTS['A-03']['mass_kg']:.2f} kg: 12 ties and 6 dowels through the mated holes",
            f"Overlap {w['block_interference_mm3']:.3f} mm3; joint faces coplanar within {w['joint_faces_coplanar_mm']:.4f} mm",
            f"Tie holes coaxial within {w['tie_axis_offset_mm']:.4f} mm, dowels {w['dowel_axis_offset_mm']:.4f} mm",
            f"Landing wall to joint face {c1['landing_wall_sharp_corner']['z0']:.1f} (hex) / {c2['landing_wall_sharp_corner']['z0']:.1f} (pent) mm, same at z 0 and z 400"]
    W, H, cols = 760, 620, 3
    sheet = Image.new("RGB", (cols * W, 2 * (H + 34) + 54), "white"); dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15); fontb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except Exception:
        font = fontb = ImageFont.load_default()
    dr.text((16, 14), "HCSA corner blocks with leaning joint faces and the mated corner node, 9 Nov 2026 PROPOSAL (CadQuery solids, checked on the real truncated icosahedron)", fill="black", font=fontb)
    for i in range(6):
        im = Image.open(f"{t}{i}.png").convert("RGB"); im.thumbnail((W - 20, H - 10))
        r, c = divmod(i, cols)
        sheet.paste(im, (c * W + (W - im.width) // 2, 54 + r * (H + 34) + (H - im.height) // 2))
        dr.text((c * W + 12, 54 + r * (H + 34) + H + 4), caps[i], fill=(40, 40, 40), font=font)
    sheet.save(f"{OUT}/montage_corner_node_9nov.png")
    print("montage", sheet.size)
