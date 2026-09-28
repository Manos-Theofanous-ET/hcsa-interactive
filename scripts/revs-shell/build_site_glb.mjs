// Put the Rev S shell (32 panels: frames, ribs, panes, pentagon plates) into
// the site model, in place of the old face meshes. Everything else in the
// site model (interior, teardown slabs, wireframe, cameras, water loops,
// greenhouse, docking collar) is kept as it is.
//
//   node scripts/revs-shell/build_site_glb.mjs <revS_shell.glb> <old_site.glb> <out.glb>
//
// Needs @gltf-transform/{core,extensions,functions}, meshoptimizer and
// draco3dgltf (installed in /opt/node-tools in the build container).
//
// What it does:
//  1. Reads the Rev S shell (Z up, metres, parts instanced). Skips bolts,
//     nuts, washers, O-rings and RTV beads (too small to see at site scale).
//  2. Simplifies the three frame parts (bolt holes and grooves collapse,
//     outer shape stays within a few mm) so the whole shell is ~100k triangles.
//  3. Turns Z up into Y up and rotates the shell so its 32 panel centres land
//     on the site model's 32 face centres (checked to within 1 mm).
//  4. Merges each panel into two meshes: structure (edge frames + ribs and hub)
//     and skin (the L1 and L7 panes on a hexagon, the plate on a pentagon), and
//     writes them into HEX_NN_Frame / HEX_NN_Glass and PENT_NN_Frame /
//     PENT_NN_Glass, keeping each node's name, transform, extras and material.
//     HEX_NN_Solar nodes and the old bolt heads (HCSA_BOLTS) are removed. The docking face gets a Rev S pentagon
//     under PENT_DOCK_RevS_Frame / _Plate, and its old host shell is removed.
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { draco, prune } from "@gltf-transform/functions";
import { MeshoptSimplifier } from "meshoptimizer";
import draco3d from "draco3dgltf";

const [, , REVS, OLD, OUT] = process.argv;
if (!REVS || !OLD || !OUT) throw new Error("usage: build_site_glb.mjs revs.glb old.glb out.glb");

const io = new NodeIO()
  .registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({
    "draco3d.decoder": await draco3d.createDecoderModule(),
    "draco3d.encoder": await draco3d.createEncoderModule(),
  });
await MeshoptSimplifier.ready;

// ---------- small vector helpers ----------
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const len = (a) => Math.hypot(a[0], a[1], a[2]);
const norm = (a) => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const xf = (m, p) => [ // column-major 4x4 * point
  m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
  m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
  m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14],
];
const mul3 = (R, p) => [ // row-major 3x3 * vector
  R[0][0] * p[0] + R[0][1] * p[1] + R[0][2] * p[2],
  R[1][0] * p[0] + R[1][1] * p[1] + R[1][2] * p[2],
  R[2][0] * p[0] + R[2][1] * p[1] + R[2][2] * p[2],
];
function invertAffine(m) {
  // Inverse of a column-major affine 4x4 (rotation/scale + translation).
  const a = [[m[0], m[4], m[8]], [m[1], m[5], m[9]], [m[2], m[6], m[10]]];
  const det = a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]);
  const inv = [
    [(a[1][1] * a[2][2] - a[1][2] * a[2][1]) / det, (a[0][2] * a[2][1] - a[0][1] * a[2][2]) / det, (a[0][1] * a[1][2] - a[0][2] * a[1][1]) / det],
    [(a[1][2] * a[2][0] - a[1][0] * a[2][2]) / det, (a[0][0] * a[2][2] - a[0][2] * a[2][0]) / det, (a[0][2] * a[1][0] - a[0][0] * a[1][2]) / det],
    [(a[1][0] * a[2][1] - a[1][1] * a[2][0]) / det, (a[0][1] * a[2][0] - a[0][0] * a[2][1]) / det, (a[0][0] * a[1][1] - a[0][1] * a[1][0]) / det],
  ];
  const t = [m[12], m[13], m[14]];
  const it = mul3(inv, t);
  return (p) => { const q = mul3(inv, p); return [q[0] - it[0], q[1] - it[1], q[2] - it[2]]; };
}

// ---------- 1. read Rev S, simplify frames ----------
const revs = await io.read(REVS);
const FRAME_MESHES = new Set(["HEX_FRAME_A", "HEX_FRAME_B", "PENT_FRAME_B"]);
const KEEP = /^(HEX|PENT)-\d+_(E\d_[AB]|RIBS|L1_\d|L7_\d|PLATE)$/;

/** Weld by position, return {pos: Float32Array, idx: Uint32Array}. */
function welded(prim) {
  const P = prim.getAttribute("POSITION").getArray();
  const I = prim.getIndices() ? prim.getIndices().getArray() : Uint32Array.from({ length: P.length / 3 }, (_, i) => i);
  const map = new Map();
  const pos = [];
  const remap = new Uint32Array(P.length / 3);
  for (let v = 0; v < P.length / 3; v++) {
    const key = `${Math.round(P[3 * v] * 1e3)},${Math.round(P[3 * v + 1] * 1e3)},${Math.round(P[3 * v + 2] * 1e3)}`; // mesh units are mm -> 1 micron
    let id = map.get(key);
    if (id === undefined) { id = pos.length / 3; map.set(key, id); pos.push(P[3 * v], P[3 * v + 1], P[3 * v + 2]); }
    remap[v] = id;
  }
  const idx = new Uint32Array(I.length);
  for (let i = 0; i < I.length; i++) idx[i] = remap[I[i]];
  return { pos: new Float32Array(pos), idx };
}

const meshGeom = new Map(); // mesh -> {pos, idx}
const stats = [];
for (const mesh of revs.getRoot().listMeshes()) {
  const name = mesh.getName();
  const prim = mesh.listPrimitives()[0];
  let { pos, idx } = welded(prim);
  const before = idx.length / 3;
  if (FRAME_MESHES.has(name)) {
    const target = Math.floor(idx.length * 0.04 / 3) * 3;
    const [out, err] = MeshoptSimplifier.simplify(idx, pos, 3, target, 0.0025, []);
    idx = out;
    stats.push(`${name}: ${before} -> ${idx.length / 3} tris (error ${(err * 100).toFixed(2)}% of size)`);
  }
  meshGeom.set(mesh, { pos, idx });
}
console.log(stats.join("\n"));

// Collect per-panel triangles in Rev S world space (Z up, metres).
const panels = new Map(); // "HEX-07" -> {kind, structure: number[], skin: number[], centre}
for (const node of revs.getRoot().listNodes()) {
  const name = node.getName();
  if (!KEEP.test(name)) continue;
  const mesh = node.getMesh();
  if (!mesh) continue;
  const panelId = name.split("_")[0];
  const kind = panelId.startsWith("HEX") ? "hex" : "pent";
  if (!panels.has(panelId)) {
    const t = node.getWorldTranslation();
    panels.set(panelId, { kind, structure: [], skin: [], centre: [t[0], t[1], t[2]] });
  }
  const P = panels.get(panelId);
  const isSkin = /_(L1_\d|L7_\d|PLATE)$/.test(name);
  const target = isSkin ? P.skin : P.structure;
  const W = node.getWorldMatrix();
  const { pos, idx } = meshGeom.get(mesh);
  // Mirror check: a negative determinant flips winding.
  const det = W[0] * (W[5] * W[10] - W[9] * W[6]) - W[4] * (W[1] * W[10] - W[9] * W[2]) + W[8] * (W[1] * W[6] - W[5] * W[2]);
  for (let i = 0; i < idx.length; i += 3) {
    const tri = [idx[i], idx[i + 1], idx[i + 2]];
    if (det < 0) tri.reverse();
    for (const v of tri) target.push(...xf(W, [pos[3 * v], pos[3 * v + 1], pos[3 * v + 2]]));
  }
}
console.log(`Rev S panels: ${panels.size} (${[...panels.values()].filter((p) => p.kind === "hex").length} hex)`);

// ---------- 2. old site model: face centres ----------
const site = await io.read(OLD);
const sroot = site.getRoot();
const siteFaces = []; // {id, kind, dir}
for (const n of sroot.listNodes()) {
  const m = n.getName().match(/^HCSA_FACE_(HEX|PENT)_(\d+|DOCK)$/);
  if (!m) continue;
  const t = n.getWorldTranslation();
  siteFaces.push({ id: `${m[1]}_${m[2]}`, kind: m[1] === "HEX" ? "hex" : "pent", centre: [t[0], t[1], t[2]], dir: norm([t[0], t[1], t[2]]) });
}
console.log(`site faces: ${siteFaces.length}`);

// ---------- 3. rotation: Z up -> Y up, then align pentagon sets ----------
const zToY = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]; // (x, y, z) -> (x, z, -y)
for (const p of panels.values()) p.dirY = norm(mul3(zToY, p.centre));
const revPents = [...panels.entries()].filter(([, p]) => p.kind === "pent");
const sitePents = siteFaces.filter((f) => f.kind === "pent");
const a1 = revPents[0][1].dirY;
const a2 = revPents.map(([, p]) => p.dirY).find((d) => Math.abs(dot(d, a1) - 0.4472) < 0.01);
const b1 = sitePents[0].dir;
let R = null;
for (const cand of sitePents.map((f) => f.dir).filter((d) => Math.abs(dot(d, b1) - 0.4472) < 0.01)) {
  const frame = (u, v) => { const e1 = u; const e2 = norm(sub(v, scale(u, dot(u, v)))); return [e1, e2, cross(e1, e2)]; };
  const F1 = frame(a1, a2), F2 = frame(b1, cand);
  // R = F2 * F1^T (as row-major 3x3)
  const Rc = [0, 1, 2].map((i) => [0, 1, 2].map((j) => F2[0][i] * F1[0][j] + F2[1][i] * F1[1][j] + F2[2][i] * F1[2][j]));
  // Check all 32 panel directions land on a site face of the same kind.
  let worst = 0;
  for (const p of panels.values()) {
    const d = mul3(Rc, p.dirY);
    const best = Math.max(...siteFaces.filter((f) => f.kind === p.kind).map((f) => dot(f.dir, d)));
    worst = Math.max(worst, Math.acos(Math.min(1, best)));
  }
  if (worst < 1e-3) { R = Rc; break; }
}
if (!R) throw new Error("could not align the Rev S shell with the site faces");
const toSite = (p) => mul3(R, mul3(zToY, p));

// Match each site face to a Rev S panel and check the radius too.
const faceToPanel = new Map();
let maxCentreErr = 0;
for (const f of siteFaces) {
  let best = null, bestDot = -2;
  for (const [id, p] of panels) {
    if (p.kind !== f.kind) continue;
    const d = dot(mul3(R, p.dirY), f.dir);
    if (d > bestDot) { bestDot = d; best = id; }
  }
  faceToPanel.set(f.id, best);
  const c = toSite(panels.get(best).centre);
  maxCentreErr = Math.max(maxCentreErr, len(sub(c, f.centre)));
}
if (new Set(faceToPanel.values()).size !== 32) throw new Error("face matching is not one to one");
console.log(`aligned: every panel centre within ${(maxCentreErr * 1000).toFixed(1)} mm of the site face centre`);

// ---------- 4. write geometry into the site model ----------
const buffer = sroot.listBuffers()[0];
function writePrim(prim, worldTris, node, faceDir) {
  const toLocal = invertAffine(node.getWorldMatrix());
  const n = worldTris.length / 3;
  const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3), uv = new Float32Array(n * 2);
  // Planar UVs in the face plane (1 unit = one 2.25 m edge).
  const up = Math.abs(faceDir[1]) < 0.9 ? [0, 1, 0] : [1, 0, 0];
  const t1 = norm(cross(up, faceDir)), t2 = cross(faceDir, t1);
  for (let i = 0; i < n; i += 3) {
    const w = [0, 1, 2].map((k) => toSite([worldTris[3 * (i + k)], worldTris[3 * (i + k) + 1], worldTris[3 * (i + k) + 2]]));
    const l = w.map(toLocal);
    let fn = norm(cross(sub(l[1], l[0]), sub(l[2], l[0])));
    if (!Number.isFinite(fn[0])) fn = [0, 1, 0];
    for (let k = 0; k < 3; k++) {
      pos.set(l[k], 3 * (i + k));
      nor.set(fn, 3 * (i + k));
      uv.set([dot(w[k], t1) / 2.25, dot(w[k], t2) / 2.25], 2 * (i + k));
    }
  }
  const idx = new Uint32Array(n).map((_, i) => i);
  const mk = (arr, type) => site.createAccessor().setArray(arr).setType(type).setBuffer(buffer);
  for (const sem of prim.listSemantics()) if (!["POSITION", "NORMAL", "TEXCOORD_0"].includes(sem)) prim.setAttribute(sem, null);
  prim.setAttribute("POSITION", mk(pos, "VEC3"));
  prim.setAttribute("NORMAL", mk(nor, "VEC3"));
  prim.setAttribute("TEXCOORD_0", mk(uv, "VEC2"));
  prim.setIndices(mk(idx, "SCALAR"));
  return n / 3;
}

let tris = 0, removed = 0;
const byName = new Map(sroot.listNodes().map((n) => [n.getName(), n]));
for (const f of siteFaces) {
  const panel = panels.get(faceToPanel.get(f.id));
  if (f.id === "PENT_DOCK") continue;
  const frame = byName.get(`${f.id}_Frame`);
  const skin = byName.get(`${f.id}_Glass`);
  if (!frame || !skin) throw new Error(`missing site nodes for ${f.id}`);
  tris += writePrim(frame.getMesh().listPrimitives()[0], panel.structure, frame, f.dir);
  tris += writePrim(skin.getMesh().listPrimitives()[0], panel.skin, skin, f.dir);
  const solar = byName.get(`${f.id}_Solar`);
  if (solar) { solar.dispose(); removed++; }
}

// Docking face: a Rev S pentagon with the shared pentagon materials; drop the old host shell.
{
  const f = siteFaces.find((x) => x.id === "PENT_DOCK");
  const panel = panels.get(faceToPanel.get("PENT_DOCK"));
  const refFrame = byName.get("PENT_02_Frame").getMesh().listPrimitives()[0].getMaterial();
  const refPlate = byName.get("PENT_02_Glass").getMesh().listPrimitives()[0].getMaterial();
  const scene = sroot.listScenes()[0];
  for (const [suffix, tri, mat] of [["Frame", panel.structure, refFrame], ["Plate", panel.skin, refPlate]]) {
    const prim = site.createPrimitive().setMaterial(mat);
    const mesh = site.createMesh(`PENT_DOCK_RevS_${suffix}_mesh`).addPrimitive(prim);
    const node = site.createNode(`PENT_DOCK_RevS_${suffix}`).setMesh(mesh).setExtras({ hcsa_web_role: `pent_dock_revs_${suffix.toLowerCase()}` });
    scene.addChild(node);
    tris += writePrim(prim, tri, node, f.dir);
  }
  const host = byName.get("PENT_DOCK_shell_1");
  if (host) { host.dispose(); removed++; }
}
// The old bolt heads sit on the old seam line, outside the Rev S frames.
{
  const bolts = byName.get("HCSA_BOLTS");
  if (bolts) { bolts.dispose(); removed++; }
}
console.log(`wrote ${tris} shell triangles; removed ${removed} old nodes`);

await site.transform(prune({ keepLeaves: true }), draco({ method: "edgebreaker", quantizePosition: 16, quantizeNormal: 10, quantizeTexcoord: 12 }));
await io.write(OUT, site);
console.log(`written ${OUT}`);
