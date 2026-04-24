import { useGLTF, Stars, Environment } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useEffect, useMemo, useRef } from "react";
import {
  AdditiveBlending,
  BackSide,
  MeshPhysicalMaterial,
  MeshStandardMaterial,
  Quaternion,
  Vector3,
  type Object3D,
  type Mesh,
  type Group,
} from "three";
import type { SceneRegistry } from "./sceneRegistry";

/** Upgrade a MeshStandardMaterial to MeshPhysicalMaterial, preserving
 *  all PBR properties and adding clearcoat so painted aluminum gets its
 *  second-surface gloss. Wrapped in try/catch at the call site — a
 *  single bad source material cannot take down the scene.
 *
 *  Why not `phys.copy(std)`: MeshPhysicalMaterial.copy assumes the source
 *  also has physical-only fields (clearcoatNormalScale, attenuationColor,
 *  sheenColor, etc.) and crashes on `undefined.x` when copying Vector2/Color
 *  properties. We instead use MeshStandardMaterial.copy for the Standard
 *  subset, then keep the Physical defaults for the physical-only fields. */
function upgradeToPhysical(
  std: MeshStandardMaterial,
  options: {
    clearcoat?: number;
    clearcoatRoughness?: number;
    reflectivity?: number;
    tintR?: number;
    tintG?: number;
    tintB?: number;
    metalnessBoost?: number;
    roughnessScale?: number;
    /** KHR_materials_transmission: true see-through glass (0 = opaque, 1 = full transmission). */
    transmission?: number;
    /** Index of refraction. 1.45 matches soda-lime / fused silica. */
    ior?: number;
    /** Physical thickness (m) of the transmissive layer. Tunes refraction feel. */
    thickness?: number;
    /** Roughness override (not a scale). Used when the source roughness is
     *  incorrect for the target material (e.g. matte paint → mirror glass). */
    roughnessAbsolute?: number;
    /** Metalness override (not a boost). Used when switching materials. */
    metalnessAbsolute?: number;
  } = {},
): MeshPhysicalMaterial {
  const phys = new MeshPhysicalMaterial();
  (MeshStandardMaterial.prototype.copy as (this: MeshStandardMaterial, s: MeshStandardMaterial) => MeshStandardMaterial)
    .call(phys as unknown as MeshStandardMaterial, std);
  phys.envMapIntensity = std.envMapIntensity;
  if (options.clearcoat !== undefined) phys.clearcoat = options.clearcoat;
  if (options.clearcoatRoughness !== undefined)
    phys.clearcoatRoughness = options.clearcoatRoughness;
  if (options.reflectivity !== undefined) phys.reflectivity = options.reflectivity;
  if (options.metalnessBoost !== undefined) {
    phys.metalness = Math.min(1, phys.metalness + options.metalnessBoost);
  }
  if (options.roughnessScale !== undefined) {
    phys.roughness = Math.max(0.02, phys.roughness * options.roughnessScale);
  }
  if (options.metalnessAbsolute !== undefined) phys.metalness = options.metalnessAbsolute;
  if (options.roughnessAbsolute !== undefined) phys.roughness = options.roughnessAbsolute;
  if (options.tintR !== undefined || options.tintG !== undefined || options.tintB !== undefined) {
    phys.color.setRGB(
      options.tintR ?? phys.color.r,
      options.tintG ?? phys.color.g,
      options.tintB ?? phys.color.b,
    );
  }
  if (options.transmission !== undefined) phys.transmission = options.transmission;
  if (options.ior !== undefined) phys.ior = options.ior;
  if (options.thickness !== undefined) phys.thickness = options.thickness;
  return phys;
}

// (Removed: applyPVCellGrid world-space PV cell grid shader.)
// The earlier implementation tiled cells in world space across the whole
// pentagon surface, but every pent in the GLB is already geometrically
// subdivided into 5 triangular panes separated by radial mullions — the
// subdivision is part of the frame geometry, not a texture effect. Tiling
// cells on top crossed triangle boundaries and broke that read. Each pent
// pane now renders as a discrete clean solar tile; mullions in _Frame do
// the cell boundaries. If we ever need visible PV sub-cell pattern per
// triangle, reintroduce using per-face UVs (not world space).

/** Inject procedural surface-detail variation into a Standard/Physical
 *  material via onBeforeCompile. The GLB ships no UVs or tangents on the
 *  shell panels, which blocks the normal-map/texture-map path entirely.
 *  This is the only site-side lever left for "panels don't look like
 *  painted ping-pong balls": inject a cell-noise hash on world position
 *  and use it to perturb diffuse color and roughness per cell.
 *
 *  Noise cells at ~0.7 m → ~3–4 cells across each ~2.25 m panel face, so
 *  each panel has within-face tonal variation (paint unevenness) plus
 *  panel-to-panel variation (different batches of paint, thermal aging).
 *  Effect is subtle on purpose — ±6 % diffuse, ±15 % roughness — enough
 *  to break the uniform look, not enough to read as noise. */
function applyProceduralDetail(
  mat: MeshStandardMaterial | MeshPhysicalMaterial,
  colorJitter = 0.12,
  roughnessJitter = 0.3,
): void {
  // Idempotent: HMR / re-registration should not stack injections.
  const tagged = mat as unknown as { __hcsaDetailApplied?: boolean };
  if (tagged.__hcsaDetailApplied) return;
  tagged.__hcsaDetailApplied = true;

  const prevHook = mat.onBeforeCompile;
  mat.onBeforeCompile = (shader, renderer) => {
    if (prevHook) {
      try { prevHook.call(mat, shader, renderer); } catch { /* ignore */ }
    }
    try {
      // Vertex: pass world position to fragment as our own varying so we
      // never collide with three.js built-ins like `worldPosition`.
      shader.vertexShader = shader.vertexShader
        .replace(
          "#include <common>",
          `#include <common>
           varying vec3 vHcsaWorldPos;`,
        )
        .replace(
          "#include <project_vertex>",
          `#include <project_vertex>
           vHcsaWorldPos = (modelMatrix * vec4(transformed, 1.0)).xyz;`,
        );

      // Fragment: hash-based cell noise, modulate diffuse + roughness.
      shader.fragmentShader = shader.fragmentShader
        .replace(
          "#include <common>",
          `#include <common>
           varying vec3 vHcsaWorldPos;
           float hcsaHash(vec3 p) {
             return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453);
           }
           float hcsaCell(vec3 p) { return hcsaHash(floor(p)); }`,
        )
        .replace(
          "#include <color_fragment>",
          `#include <color_fragment>
           float hcsaC = hcsaCell(vHcsaWorldPos * 1.4);
           diffuseColor.rgb *= (1.0 - ${colorJitter.toFixed(3)} * 0.5 + hcsaC * ${colorJitter.toFixed(3)});`,
        )
        .replace(
          "#include <roughnessmap_fragment>",
          `#include <roughnessmap_fragment>
           float hcsaR = hcsaCell(vHcsaWorldPos * 1.1 + vec3(7.31, 2.17, 5.63));
           roughnessFactor *= (1.0 - ${roughnessJitter.toFixed(3)} * 0.5 + hcsaR * ${roughnessJitter.toFixed(3)});`,
        );
    } catch (e) {
      console.error("[hcsa] shader injection failed:", e);
      tagged.__hcsaDetailApplied = false;
    }
  };
  mat.needsUpdate = true;
}

useGLTF.preload("/3d/HCSA_MAIN.glb");

/** Per-layer PBR spec for the Phase 5 teardown slabs. Mirrors the
 *  authored layer table in blender-automation/scripts/blender/hcsa_web_export.py
 *  (_build_staged_panel_teardown, lines 590–599). The GLB ships a single
 *  shared `HCSA_V3_WebStructural` material for all 7 slabs (likely a
 *  Blender slot-assignment quirk: obj.data.materials.append adds at slot
 *  1, but faces stay on slot 0). We clone per slab so each can fade
 *  independently, and we reapply the intended color / roughness /
 *  metalness / alpha so the teardown reads as 7 distinct engineering
 *  surfaces — silica → aluminum → perovskite → electrochromic → gas →
 *  opaque PV → inner aluminum — not 7 identical greys. */
type TeardownSpec = {
  color: readonly [number, number, number];
  rough: number;
  metal: number;
  alpha: number;
};

const TEARDOWN_SPEC: readonly TeardownSpec[] = [
  { color: [0.96, 0.98, 1.0], rough: 0.06, metal: 0.0, alpha: 0.58 },   // L1 Debris Pane (fused silica)
  { color: [0.62, 0.66, 0.72], rough: 0.3, metal: 1.0, alpha: 1.0 },    // L2 Outer Frame (6061-T6)
  { color: [0.06, 0.28, 0.78], rough: 0.18, metal: 0.15, alpha: 0.88 }, // L3 Transparent PV (perovskite)
  { color: [0.45, 0.08, 0.7], rough: 0.06, metal: 0.0, alpha: 0.94 },   // L4 Electrochromic (violet WO3)
  { color: [0.88, 0.94, 1.0], rough: 0.02, metal: 0.0, alpha: 0.58 },   // L5 Gas Gap (dry N2/Ar)
  { color: [0.01, 0.02, 0.05], rough: 0.18, metal: 0.15, alpha: 1.0 },  // L6 Sliding Solar (opaque PV)
  { color: [0.58, 0.62, 0.68], rough: 0.34, metal: 1.0, alpha: 1.0 },   // L7 Inner Frame (aluminum)
];

type Props = { registry: React.MutableRefObject<SceneRegistry> };

export function Scene({ registry }: Props) {
  const gltf = useGLTF("/3d/HCSA_MAIN.glb");
  const habitatRef = useRef<Group>(null);

  const scene = useMemo(() => gltf.scene.clone(true), [gltf]);

  useEffect(() => {
    const reg = registry.current;
    reg.root = scene;

    const hexFaceNodes: Record<string, Object3D> = {};
    const pentFaceNodes: Record<string, Object3D> = {};
    const teardownNodes: Array<{ node: Object3D; mesh: Mesh; index: number }> = [];
    /** Nodes flagged during the traverse for post-traverse hinge assembly. */
    const pent02Meshes: Object3D[] = [];
    let pent02PivotNode: Object3D | null = null;
    /** Unmatched mesh names collected so the interior heuristic can be
     *  verified once the site runs — if nothing lands in `interiorMeshes`,
     *  this list tells the user which node names Blender actually exports. */
    const unmatchedInteriorCandidates: string[] = [];

    scene.traverse((node: Object3D) => {
      const name = node.name;

      const hexMatch = name.match(/^HEX_(\d+)_(Frame|Glass|Solar)$/);
      if (hexMatch) {
        const [, nn] = hexMatch;
        if (!hexFaceNodes[nn!]) hexFaceNodes[nn!] = node;
      }

      const pentMatch = name.match(/^PENT_(\d+)_(Frame|Glass)$/);
      if (pentMatch) {
        const [, nn] = pentMatch;
        if (!pentFaceNodes[nn!]) pentFaceNodes[nn!] = node;
      }

      // Phase 6 hinge collection. PENT_02_HINGE_PIVOT is a Blender empty
      // whose +X axis is the hinge axis per phase_metadata.json; the meshes
      // named PENT_02_Frame / PENT_02_Glass are what we rotate around it.
      if (name === "PENT_02_HINGE_PIVOT") {
        pent02PivotNode = node;
      } else if (name === "PENT_02_Frame" || name === "PENT_02_Glass") {
        pent02Meshes.push(node);
      }

      const mesh = node as Mesh;
      if (mesh.isMesh && mesh.material) {
        const mat = mesh.material as MeshStandardMaterial;
        if (name.startsWith("HEX_") && name.endsWith("_Frame") && !reg.materials.hexFrame) {
          reg.materials.hexFrame = mat;
          mat.transparent = true;
          // Aluminum bezel: crank env reflections so the rim edges pick
          // up the sunset HDR highlights — reads as metal, not painted.
          mat.envMapIntensity = 3.5;
          mat.roughness = Math.max(0.15, mat.roughness * 0.75);
          mat.metalness = Math.min(1, mat.metalness + 0.15);
        } else if (name.startsWith("HEX_") && name.endsWith("_Glass") && !reg.materials.hexGlass) {
          reg.materials.hexGlass = mat;
          mat.transparent = true;
          // Pass F satin white panel skin: leave it matte but give the
          // HDR just enough grip that panel-to-panel shadow reads.
          mat.envMapIntensity = 2.8;
        } else if (name.startsWith("HEX_") && name.endsWith("_Solar") && !reg.materials.hexSolar) {
          reg.materials.hexSolar = mat;
          mat.transparent = true;
          mat.envMapIntensity = 1.5;
        } else if (name.startsWith("PENT_") && name.endsWith("_Frame") && !name.startsWith("PENT_DOCK") && !reg.materials.pentFrame) {
          reg.materials.pentFrame = mat;
          mat.transparent = true;
          mat.envMapIntensity = 3.5;
          mat.roughness = Math.max(0.15, mat.roughness * 0.75);
          mat.metalness = Math.min(1, mat.metalness + 0.15);
        } else if (name.startsWith("PENT_") && name.endsWith("_Glass") && !reg.materials.pentGlass) {
          reg.materials.pentGlass = mat;
          mat.transparent = true;
          mat.envMapIntensity = 2.8;
        } else if (name === "WIREFRAME" && !reg.materials.wireframe) {
          reg.materials.wireframe = mat;
          mat.transparent = true;
          mat.opacity = 0;
          reg.wireframeMesh = mesh;
        } else if (name.startsWith("BEAM_WATER_RED") && !reg.materials.waterRed) {
          reg.materials.waterRed = mat;
        } else if (name.startsWith("BEAM_WATER_BLUE") && !reg.materials.waterBlue) {
          reg.materials.waterBlue = mat;
        } else if (name === "BEAM_TRUNK") {
          // Phase 7 systems core: BEAM_TRUNK scales 3× longitudinally.
          // We capture the initial scale so the tween can interpolate from it
          // rather than assuming identity (Blender may export non-identity).
          reg.beamTrunk = { node, initialScale: node.scale.clone() };
        } else if (/^PLANT_TRAY_\d+/.test(name)) {
          // Phase 6 greenhouse: each tray carries its own grow-LED material.
          // Collect each unique material once so the `led_green` emissive
          // tween writes to one value per tray, not every instance.
          if (!reg.plantLedMaterials.includes(mat)) {
            reg.plantLedMaterials.push(mat);
          }
        } else {
          // PANEL_TEARDOWN_L{1..7}_{suffix} — each layer is a unique mesh
          // with its own authored PBR material (silica, 6061-T6, perovskite,
          // electrochromic, gas, black PV, inner aluminum). Each node has a
          // Blender custom prop hcsa_panel_layer_index (1..7).
          const teardownMatch = name.match(/^PANEL_TEARDOWN_L(\d+)_/);
          if (teardownMatch) {
            const idx = Number(teardownMatch[1]);
            teardownNodes.push({ node, mesh, index: idx });
          } else if (
            /^(INT_|INTERIOR_|RAMP_|POD_|FIGURE_|AEROGARDEN)/i.test(name)
          ) {
            // Phase 4 interior reveal: ramps, pods, aerogarden, figures.
            // Blender export names are not yet pinned in the contract, so we
            // use a broad prefix heuristic and log unmatched mesh names below.
            mat.transparent = true;
            mat.depthWrite = true;
            const baseOpacity = mat.opacity > 0 ? mat.opacity : 1.0;
            mat.opacity = 0;
            reg.interiorMeshes.push({ mesh, material: mat, baseOpacity });
          } else if (
            // Record every other mesh for post-traverse diagnostics so we can
            // extend the interior heuristic when the node-name convention
            // shifts. Skip infrastructure that we've already matched above.
            !name.startsWith("HEX_") &&
            !name.startsWith("PENT_") &&
            !name.startsWith("BEAM_") &&
            !name.startsWith("PANEL_TEARDOWN_") &&
            !name.startsWith("PLANT_TRAY_") &&
            name !== "WIREFRAME" &&
            name !== "BEAM_TRUNK"
          ) {
            unmatchedInteriorCandidates.push(name);
          }
        }
      }
    });

    const extractFace = (node: Object3D) => {
      const rawNormal = (node.userData?.["hcsa_face_normal"] ?? null) as
        | [number, number, number]
        | null;
      if (!rawNormal) return null;
      const faceNormal = new Vector3(...rawNormal).normalize();
      const initialPosition = node.position.clone();
      return { node, faceNormal, initialPosition };
    };

    reg.hexFaces = Object.values(hexFaceNodes)
      .map(extractFace)
      .filter((f): f is NonNullable<ReturnType<typeof extractFace>> => f !== null);

    reg.pentFaces = Object.values(pentFaceNodes)
      .map(extractFace)
      .filter((f): f is NonNullable<ReturnType<typeof extractFace>> => f !== null);

    // Register Phase 5 teardown slabs in authored vacuum→crew order.
    // CRITICAL: all 7 slabs share a single material in the GLB
    // (HCSA_V3_WebStructural at material_index 0), so we MUST clone per
    // slab — otherwise opacity writes collide and the stagger does
    // nothing. We also reapply the per-layer PBR from TEARDOWN_SPEC so
    // each slab reads as its distinct engineering surface.
    reg.teardownLayers = teardownNodes
      .sort((a, b) => a.index - b.index)
      .map(({ node, mesh, index }) => {
        const sharedMat = mesh.material as MeshStandardMaterial;
        const material = sharedMat.clone();
        mesh.material = material;
        const spec = TEARDOWN_SPEC[index - 1];
        if (spec) {
          material.color.setRGB(spec.color[0], spec.color[1], spec.color[2]);
          material.roughness = spec.rough;
          material.metalness = spec.metal;
        }
        material.transparent = true;
        material.depthWrite = false;
        material.opacity = 0;
        const baseOpacity = spec ? spec.alpha : 1.0;
        return { node, material, index, baseOpacity };
      });

    // --- Phase 6 hinge assembly ---
    // Given PENT_02_HINGE_PIVOT (a Blender empty) and the PENT_02 meshes,
    // capture each mesh's initial pose plus the pivot point and hinge axis
    // in WORLD space. PhaseController then rotates each mesh around the
    // world-space pivot by up to 90° without reparenting — keeps the scene
    // graph identical to what Blender exported.
    if (pent02PivotNode && pent02Meshes.length > 0) {
      const pivot = pent02PivotNode as Object3D;
      pivot.updateWorldMatrix(true, false);
      const pivotWorld = new Vector3();
      const pivotQuat = new Quaternion();
      const pivotScale = new Vector3();
      pivot.matrixWorld.decompose(pivotWorld, pivotQuat, pivotScale);
      // Hinge axis = pivot's local +X in world coordinates.
      const axisWorld = new Vector3(1, 0, 0).applyQuaternion(pivotQuat).normalize();
      const initialPoses = pent02Meshes.map((m) => {
        m.updateWorldMatrix(true, false);
        const p = new Vector3();
        const q = new Quaternion();
        const s = new Vector3();
        m.matrixWorld.decompose(p, q, s);
        return { position: p, quaternion: q };
      });
      reg.pent02Hinge = {
        meshes: pent02Meshes,
        initialPoses,
        pivotWorld,
        axisWorld,
      };
    } else if (import.meta.env.DEV) {
      console.info(
        `[hcsa] Phase 6 hinge: pivotNode=${!!pent02PivotNode}, meshes=${pent02Meshes.length} (need pivot + ≥1 mesh)`,
      );
    }

    if (import.meta.env.DEV) {
      console.info(
        `[hcsa] phase-6/7 nodes: beamTrunk=${!!reg.beamTrunk}, plantLEDs=${reg.plantLedMaterials.length}, pent02Hinge=${!!reg.pent02Hinge}, interior=${reg.interiorMeshes.length}`,
      );
      if (reg.interiorMeshes.length === 0 && unmatchedInteriorCandidates.length > 0) {
        // Log up to 30 candidate names so the interior-heuristic regex can
        // be tightened once the user names-pattern is known. Keeps signal
        // from drowning in long lists.
        console.info(
          `[hcsa] interior heuristic matched 0 meshes. Unmatched candidates (first 30):`,
          unmatchedInteriorCandidates.slice(0, 30),
        );
      }
    }

    // --- Frame-only material upgrade ---
    // Promote ONLY the hex/pent frame materials to MeshPhysicalMaterial
    // so the aluminum bezel rings read as metal (clearcoat + higher
    // metalness) while the panel skin stays on the original Pass F
    // Principled BSDF. This gives us the material boundary the orbital
    // references rely on: silver-grey metal frame, painted-white skin.
    // Wrapped in try/catch — if any source material has a malformed
    // state, we log and skip rather than blank the page.
    const frameSwaps = new Map<MeshStandardMaterial, MeshPhysicalMaterial>();
    const upgradeFrame = (
      slot: MeshStandardMaterial | null,
      label: string,
    ): MeshPhysicalMaterial | null => {
      if (!slot) return null;
      try {
        const phys = upgradeToPhysical(slot, {
          clearcoat: 0.55,
          clearcoatRoughness: 0.18,
          reflectivity: 0.6,
          metalnessBoost: 0.3,
          roughnessScale: 0.65,
          // Cool steel-silver tint so the frame visually separates from
          // the slightly warm panel skin. References: Axiom Station
          // hull — bezels read cooler/metallic vs warmer painted body.
          tintR: 0.78,
          tintG: 0.81,
          tintB: 0.86,
        });
        frameSwaps.set(slot, phys);
        if (import.meta.env.DEV) {
          console.info(`[hcsa] upgraded ${label} → MeshPhysicalMaterial`);
        }
        return phys;
      } catch (e) {
        console.error(`[hcsa] failed to upgrade ${label}:`, e);
        return null;
      }
    };
    const newHexFrame = upgradeFrame(reg.materials.hexFrame, "hex frame");
    if (newHexFrame) reg.materials.hexFrame = newHexFrame;
    const newPentFrame = upgradeFrame(reg.materials.pentFrame, "pent frame");
    if (newPentFrame) reg.materials.pentFrame = newPentFrame;

    // --- Hex glass upgrade: real transmissive glass ---
    // The hex face's `_Glass` slot is what the user sees through. Upgrade
    // to MeshPhysicalMaterial with KHR transmission so the shell reads as
    // an engineered glass aperture, not a painted panel. Pale cool tint so
    // it still feels cold-vacuum glass, not living-room window.
    const glassSwaps = new Map<MeshStandardMaterial, MeshPhysicalMaterial>();
    if (reg.materials.hexGlass && !(reg.materials.hexGlass as MeshPhysicalMaterial).isMeshPhysicalMaterial) {
      try {
        const glass = upgradeToPhysical(reg.materials.hexGlass, {
          // Previously transmission=0.92 made the glass ~invisible — each
          // of the 6 triangular panes per hex blurred into the background,
          // so the triangular subdivision was lost. User reference shows
          // each triangle reading as a discrete tinted pane. Drop to 0.72
          // so the glass has BODY — you see each triangle, lit blue, with
          // reflections catching across its surface.
          transmission: 0.72,
          ior: 1.45,
          thickness: 0.05,
          roughnessAbsolute: 0.06,
          metalnessAbsolute: 0,
          reflectivity: 0.65,
          // Cooler, more saturated blue so the triangles read as tinted
          // glass rather than clear window — closer to the reference.
          tintR: 0.62,
          tintG: 0.82,
          tintB: 1.0,
        });
        glass.envMapIntensity = 2.8;
        glassSwaps.set(reg.materials.hexGlass, glass);
        reg.materials.hexGlass = glass;
        if (import.meta.env.DEV) console.info(`[hcsa] upgraded hex glass → transmissive MeshPhysicalMaterial`);
      } catch (e) {
        console.error(`[hcsa] failed to upgrade hex glass:`, e);
      }
    }

    // Swap the upgraded materials in on every mesh that referenced the
    // old MeshStandardMaterial. Skip non-mesh nodes, multi-material
    // meshes, and meshes whose material isn't in the swap map (that
    // includes the teardown slab clones, which stay on MeshStandard).
    const allSwaps = new Map<MeshStandardMaterial, MeshPhysicalMaterial>();
    for (const [k, v] of frameSwaps) allSwaps.set(k, v);
    for (const [k, v] of glassSwaps) allSwaps.set(k, v);
    if (allSwaps.size > 0) {
      scene.traverse((node: Object3D) => {
        const m = node as Mesh;
        if (!m.isMesh) return;
        if (Array.isArray(m.material)) return;
        const swap = allSwaps.get(m.material as MeshStandardMaterial);
        if (swap) {
          try {
            m.material = swap;
          } catch (e) {
            console.error(`[hcsa] failed to swap material on ${m.name}:`, e);
          }
        }
      });
    }

    // --- Pent glass → solar panel exterior ---
    // Per user direction: hexagons are glass, pentagons are solar panels on
    // the outside. IMPORTANT: each pent is already 5 triangular panes
    // separated by radial mullions in the GLB (see sync-geometry.ts —
    // "every face is now 6 (hex) or 5 (pent) triangular glass panes"), so
    // the subdivision is GEOMETRIC — handled by the _Frame material's
    // mullion ribs. We deliberately do NOT apply a world-space cell-grid
    // shader on top because it would tile across triangle boundaries,
    // breaking the "5 discrete solar tiles" read.
    //
    // Styling is just dark-navy silicon PV surface with moderate metalness
    // so grazing sunlight rims the edges. The mullions alone give the grid.
    if (reg.materials.pentGlass) {
      const pv = reg.materials.pentGlass;
      pv.color.setRGB(0.03, 0.05, 0.12);
      pv.metalness = 0.55;
      pv.roughness = 0.22;
      pv.envMapIntensity = 1.2;
      if ("emissive" in pv) pv.emissive.setRGB(0.0, 0.01, 0.03);
      pv.needsUpdate = true;
    }

    // --- Procedural surface detail (tuned down) ---
    // Previous intensities read as "dusty / weathered / deteriorating" when
    // the camera was close (Phase 5 teardown, Phase 6 greenhouse). User
    // direction is "clean and porous", not weathered metal. Keep a whisper
    // of cell-to-cell variation on frames only so they don't look plastic,
    // drop variation entirely on glass/PV surfaces — those should read as
    // engineered panels, not painted metal.
    if (reg.materials.hexFrame) applyProceduralDetail(reg.materials.hexFrame, 0.02, 0.08);
    if (reg.materials.pentFrame) applyProceduralDetail(reg.materials.pentFrame, 0.02, 0.08);
    if (reg.materials.hexSolar) applyProceduralDetail(reg.materials.hexSolar, 0.04, 0.1);

    if (import.meta.env.DEV) {
      console.info(
        `[hcsa] scene: hex=${reg.hexFaces.length}/20, pent=${reg.pentFaces.length}/11, teardown=${reg.teardownLayers.length}/7`,
      );
      const w = window as unknown as { __hcsa?: Record<string, unknown> };
      w.__hcsa = { ...(w.__hcsa ?? {}), scene };
    }
  }, [scene, registry]);

  // Slow constant orbital drift — gives life even before the user scrolls.
  useFrame((_, dt) => {
    if (habitatRef.current) habitatRef.current.rotation.y += dt * 0.035;
  });

  return (
    <>
      {/* HDR env drives reflections on aluminum + glass. Sunset preset gives
          warm golden highlights + cool shadow side — reads as orbital dawn. */}
      <Environment preset="sunset" environmentIntensity={1.05} background={false} />

      {/* Harsh sun key — vacuum sunlight. Pushed to 5.2 (from 4.0) so
          the sunlit faces clip into ACES pure white the way the Axiom
          Station reference photographs do. Near-daylight white
          (#fff8e8) instead of warm yellow so the "photograph" reads
          as midday orbit, not sunset. */}
      <directionalLight
        position={[22, 10, 14]}
        intensity={5.2}
        color="#fff8e8"
      />
      {/* Earth-shine rim. Dropped from 0.8 → 0.45 so the shadow side of
          the habitat goes nearly black — that terminator split is what
          separates orbital hardware from a CAD render. */}
      <directionalLight
        position={[-18, -12, -10]}
        intensity={0.45}
        color="#4d80ff"
      />

      {/* Visible sun disc at the key-light direction. High emissive pushes
          it into the bloom threshold so it glows without us faking a lens
          flare. Placed well outside the habitat's clip volume (<far: 1200). */}
      <mesh position={[220, 100, 140]}>
        <sphereGeometry args={[6, 32, 32]} />
        <meshBasicMaterial color="#fff6e0" toneMapped={false} />
      </mesh>

      <Stars radius={280} depth={120} count={10000} factor={4.0} saturation={0} fade speed={0.12} />

      <EarthLimb />

      <group ref={habitatRef}>
        <primitive object={scene} />
      </group>
    </>
  );
}

/** Orbital Earth backdrop — a dark-blue sphere sitting below the habitat,
 *  wrapped in an additive fresnel halo to sell the atmosphere. This is the
 *  "subtle Earth imagery" from WEB_ASSET_BRIEF §2.1. Earth is intentionally
 *  NOT in the GLB (blender-automation excludes it from export); the website
 *  renders it so every phase reads as "in orbit", not "floating in a void".
 *
 *  Geometry: 450 m-radius sphere centered at [0, -520, -80] — below and
 *  slightly behind the scene origin. At this scale the limb fills a chunk
 *  of frame from any of the 9 phase cameras (hero to systems), and its
 *  atmospheric halo reads even when the body itself is off-frame. */
function EarthLimb() {
  const center: [number, number, number] = [0, -520, -80];
  const bodyRadius = 450;
  const haloRadius = 470;
  return (
    <group position={center}>
      {/* Body: dark ocean blue with faint emissive so the night-side still
          registers against pure-black space. High roughness, zero metal —
          Earth is NOT a mirror ball. */}
      <mesh>
        <sphereGeometry args={[bodyRadius, 96, 96]} />
        <meshStandardMaterial
          color="#050c22"
          emissive="#1a377a"
          emissiveIntensity={0.18}
          roughness={0.96}
          metalness={0}
        />
      </mesh>
      {/* Atmosphere halo: slightly larger BackSide sphere, additive blend,
          fresnel in shader so it only glows on the crescent facing the
          camera. Standard orbital-photo trick. */}
      <mesh>
        <sphereGeometry args={[haloRadius, 96, 96]} />
        <shaderMaterial
          transparent
          depthWrite={false}
          side={BackSide}
          blending={AdditiveBlending}
          uniforms={{
            glowColor: { value: [0.26, 0.52, 1.0] },
            power: { value: 2.6 },
          }}
          vertexShader={`
            varying vec3 vNormal;
            varying vec3 vViewDir;
            void main() {
              vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
              vNormal = normalize(normalMatrix * normal);
              vViewDir = normalize(-mvPosition.xyz);
              gl_Position = projectionMatrix * mvPosition;
            }
          `}
          fragmentShader={`
            varying vec3 vNormal;
            varying vec3 vViewDir;
            uniform vec3 glowColor;
            uniform float power;
            void main() {
              float rim = pow(1.0 - abs(dot(vNormal, vViewDir)), power);
              gl_FragColor = vec4(glowColor * rim, rim);
            }
          `}
        />
      </mesh>
    </group>
  );
}
