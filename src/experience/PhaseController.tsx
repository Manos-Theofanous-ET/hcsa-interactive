import { useFrame, useThree } from "@react-three/fiber";
import { useEffect, useMemo, useRef } from "react";
import { Quaternion, Vector3 } from "three";
import camerasJson from "../3d/cameras.json";
import phasesJson from "../3d/phase_metadata.json";
import { CamerasDoc, focalToFov } from "@/lib/cameras";
import { PhasesDoc, type PhaseSpec } from "@/lib/phases";
import type { SceneRegistry } from "./sceneRegistry";

const HINGE_MAX_DEG = 90;
const BEAM_TRUNK_MAX_SCALE = 3.0;
/** Water-loop pulse rate (Hz) layered on top of the JSON emissive value
 *  during Phase 7 so the red/blue loops read as flowing, not static glow. */
const WATER_PULSE_HZ = 1.25;
/** Shared scratch objects so per-frame math doesn't allocate. */
const _scratchQuat = new Quaternion();
const _scratchVec = new Vector3();

const cameras = CamerasDoc.parse(camerasJson);
const phases = PhasesDoc.parse(phasesJson);

/** Per-phase tuning for cinematic impact. The blender-automation export
 *  optimizes for preview-render composition; these overrides bring the
 *  camera closer for hero/closing and pull it back on the interior beats
 *  so the viewer can read spatial context. Values > 1 push the camera
 *  OUT; < 1 push it IN (multiplied against cameras.json position). */
const PHASE_CAM_ZOOM: Partial<Record<number, number>> = {
  1: 0.48, // hero: habitat at ~40% of frame width, dominant silhouette
  5: 2.0,  // panel teardown: was 5 m from shell → 10 m so the 7 layers
           //                  read as a stack, not a zoomed-in mess.
  6: 1.45, // greenhouse: was 3.5 m from pivot → 5 m so the hinged
           //             pent + adjacent pentagons all read in-frame.
  9: 0.56, // closing: slightly wider than hero so earth limb reads at exit
};

/** Cinematic opacity overrides layered on top of phase_metadata.json so the
 *  website can tune what-the-viewer-sees without rewriting the contract. */
const PHASE_OPACITY_OVERRIDES: Partial<
  Record<number, Partial<PhaseSpec["opacities"]>>
> = {
  // Hero hides the deployable PV so the glass shell reads as glass
  // (brief §Phase 1: "glass reflections, shell reads as glazed").
  // Also raise wireframe to 0.25 so the polyhedral edges read as
  // INTENTIONAL design — without any wireframe glow the 32 flat faces
  // read as "low-poly", with it they read as "engineered polyhedron".
  1: { hex_solar: 0, wireframe: 0.25 },
  // Mission breath and closing both keep the wireframe at ~0.2 for the
  // same reason — the shell needs the edge signal to not look faceted.
  2: { wireframe: 0.55 },
  9: { wireframe: 0.22 },
  // Panel teardown: raise the wireframe to 0.55 (was 0.1) so the viewer
  // sees the 32-face shell outline even as the solid panel fades to 0.03.
  // Without this the central hex+layers read as "floating debris", not
  // "one panel breaking apart with the shell context holding around it".
  5: { wireframe: 0.55 },
};

type Props = {
  registry: React.MutableRefObject<SceneRegistry>;
  progressRef: React.MutableRefObject<number>;
};

/** Lerp a scroll fraction [0,1] onto the 9-phase timeline and mutate refs. */
export function PhaseController({ registry, progressRef }: Props) {
  const { camera } = useThree();
  const targetRef = useRef(new Vector3(0, 0, 0));

  // Build a flat lookup: each phase → its camera + scroll range.
  const timeline = useMemo(
    () =>
      phases.phases.map((p) => {
        const cam = cameras.cameras.find((c) => c.name === p.camera);
        if (!cam) throw new Error(`Camera ${p.camera} not found in cameras.json`);
        return { phase: p, cam };
      }),
    [],
  );

  // One-shot camera init at phase 1.
  useEffect(() => {
    const first = timeline[0]!;
    const zoom = PHASE_CAM_ZOOM[first.phase.phase] ?? 1;
    camera.position.set(
      first.cam.position[0] * zoom,
      first.cam.position[1] * zoom,
      first.cam.position[2] * zoom,
    );
    targetRef.current.set(...first.cam.target);
    camera.lookAt(targetRef.current);
    if ("fov" in camera) {
      camera.fov = focalToFov(first.cam.focal_length_mm, first.cam.sensor_width_mm);
      camera.near = first.cam.clip_start;
      camera.far = first.cam.clip_end;
      camera.updateProjectionMatrix();
    }
  }, [camera, timeline]);

  useFrame(() => {
    const t = clamp(progressRef.current, 0, 1);
    // Find the two phases the scroll sits between.
    const { a, b, u } = bracket(timeline, t);

    // Interpolate camera position, target, and FOV (with per-phase zoom).
    const zoomA = PHASE_CAM_ZOOM[a.phase.phase] ?? 1;
    const zoomB = PHASE_CAM_ZOOM[b.phase.phase] ?? 1;
    const posA = new Vector3(...a.cam.position).multiplyScalar(zoomA);
    const posB = new Vector3(...b.cam.position).multiplyScalar(zoomB);
    camera.position.lerpVectors(posA, posB, u);
    targetRef.current.lerpVectors(
      new Vector3(...a.cam.target),
      new Vector3(...b.cam.target),
      u,
    );
    camera.lookAt(targetRef.current);

    if ("fov" in camera) {
      const fovA = focalToFov(a.cam.focal_length_mm, a.cam.sensor_width_mm);
      const fovB = focalToFov(b.cam.focal_length_mm, b.cam.sensor_width_mm);
      camera.fov = lerp(fovA, fovB, u);
      camera.updateProjectionMatrix();
    }

    // Interpolate phase opacity + translation values.
    const p = interpPhase(a.phase, b.phase, u);

    // Phase 2 breath: override the default lerp with one sine period of
    // ±0.02 m radial pulse. JSON ships static 0.02 baseline; here we layer
    // the oscillation and land at 0 so the Phase 3 push starts from closed.
    if (a.phase.phase === 2) {
      const [pStart, pEnd] = a.phase.scroll_range;
      const uRaw = (t - pStart) / Math.max(pEnd - pStart, 1e-6);
      const breath = Math.sin(uRaw * Math.PI * 2) * 0.02;
      p.hex_translation_m = breath;
      p.pent_translation_m = breath;
    }

    // Phase 5 shell-hold: JSON lerps shell opacity from 0.03 (phase 5)
    // toward 0.35/0.10/0.15 (phase 6) across phase 5's scroll range,
    // which would re-reveal the shell OVER the teardown slabs that sit
    // at world origin. Hold the shell near-invisible for the first 85%
    // of phase 5, then blend to phase 6 values in the final 15%.
    if (a.phase.phase === 5) {
      const [pStart, pEnd] = a.phase.scroll_range;
      const uRaw = (t - pStart) / Math.max(pEnd - pStart, 1e-6);
      const uShell = clamp((uRaw - 0.85) / 0.15, 0, 1);
      const eShell = easeInOut(uShell);
      const aO = a.phase.opacities;
      const bO = b.phase.opacities;
      p.opacities.hex_frame = lerp(aO.hex_frame, bO.hex_frame, eShell);
      p.opacities.hex_glass = lerp(aO.hex_glass, bO.hex_glass, eShell);
      p.opacities.hex_solar = lerp(aO.hex_solar, bO.hex_solar, eShell);
      p.opacities.pent_frame = lerp(aO.pent_frame, bO.pent_frame, eShell);
      p.opacities.pent_glass = lerp(aO.pent_glass, bO.pent_glass, eShell);
      p.opacities.wireframe = lerp(aO.wireframe, bO.wireframe, eShell);
    }

    applyPhase(p, registry.current);
    applyTeardown(t, a.phase.phase, a.phase.scroll_range, registry.current);
    applyHinge(t, a.phase.phase, a.phase.scroll_range, registry.current);
    applyBeamTrunk(t, a.phase.phase, a.phase.scroll_range, registry.current);
    applyWaterPulse(p.emissive.water_red, p.emissive.water_blue, registry.current);
  });

  return null;
}

type PhaseLike = {
  opacities: PhaseSpec["opacities"];
  emissive: PhaseSpec["emissive"];
  hex_translation_m: number;
  pent_translation_m: number;
};

function applyPhase(p: PhaseLike, reg: SceneRegistry) {
  // Material opacities.
  if (reg.materials.hexFrame) reg.materials.hexFrame.opacity = p.opacities.hex_frame;
  if (reg.materials.hexGlass) reg.materials.hexGlass.opacity = p.opacities.hex_glass;
  if (reg.materials.hexSolar) reg.materials.hexSolar.opacity = p.opacities.hex_solar;
  if (reg.materials.pentFrame) reg.materials.pentFrame.opacity = p.opacities.pent_frame;
  if (reg.materials.pentGlass) reg.materials.pentGlass.opacity = p.opacities.pent_glass;
  if (reg.materials.wireframe) reg.materials.wireframe.opacity = p.opacities.wireframe;

  // Emissive strength (cyan wireframe + water loops + plant LEDs).
  const wf = reg.materials.wireframe;
  if (wf && "emissiveIntensity" in wf) {
    wf.emissiveIntensity = p.emissive.wireframe_cyan;
  }
  // Plant-tray grow LEDs (Phase 6 greenhouse reveal). Applied to every tray
  // material we collected; water loops get their pulse in applyWaterPulse.
  for (const mat of reg.plantLedMaterials) {
    if ("emissiveIntensity" in mat) mat.emissiveIntensity = p.emissive.led_green;
  }

  // Interior meshes (ramps, pods, aerogarden, figures) fade in on Phase 4.
  // Multiplicative against baseOpacity so authored translucent parts
  // (glass domes, etc.) keep their intended alpha.
  for (const entry of reg.interiorMeshes) {
    entry.material.opacity = entry.baseOpacity * p.opacities.interior;
    entry.mesh.visible = p.opacities.interior > 0.001;
  }

  // Face outward translation (the Phase 3 "aha" moment + Phase 4 ghost cage).
  for (const f of reg.hexFaces) {
    f.node.position
      .copy(f.initialPosition)
      .addScaledVector(f.faceNormal, p.hex_translation_m);
  }
  for (const f of reg.pentFaces) {
    f.node.position
      .copy(f.initialPosition)
      .addScaledVector(f.faceNormal, p.pent_translation_m);
  }
}

/** Phase 6 pentagon greenhouse: rotate PENT_02 around its hinge pivot
 *  from 0° → 90° as scroll advances through the phase. Uses world-space
 *  pivot math (no reparenting), so the scene graph stays identical to
 *  what Blender exported and HMR reloads don't stack transforms.
 *
 *  Outside phase 6 we snap every mesh back to its captured initial pose
 *  so re-entering the phase starts from a clean 0° state. */
function applyHinge(
  t: number,
  phase: number,
  range: readonly [number, number],
  reg: SceneRegistry,
): void {
  const hinge = reg.pent02Hinge;
  if (!hinge) return;

  const angleDeg = phase === 6 ? easedAngle(t, range) * HINGE_MAX_DEG : 0;
  const angleRad = (angleDeg * Math.PI) / 180;
  _scratchQuat.setFromAxisAngle(hinge.axisWorld, angleRad);

  for (let i = 0; i < hinge.meshes.length; i += 1) {
    const m = hinge.meshes[i]!;
    const pose = hinge.initialPoses[i]!;
    // Rotate initial position around the world pivot by the scratch quat.
    _scratchVec.copy(pose.position).sub(hinge.pivotWorld).applyQuaternion(_scratchQuat).add(hinge.pivotWorld);
    m.position.copy(_scratchVec);
    m.quaternion.copy(pose.quaternion).premultiply(_scratchQuat);
    m.updateMatrix();
  }
}

/** Phase 7 systems core: scale BEAM_TRUNK from its initial size to 3× along
 *  the Y axis as scroll advances through the phase, snapping back to the
 *  initial scale outside phase 7. JSON ships `scale_factor: 3.0`; we apply
 *  it only to Y so the beam reads as "extending" rather than ballooning. */
function applyBeamTrunk(
  t: number,
  phase: number,
  range: readonly [number, number],
  reg: SceneRegistry,
): void {
  const trunk = reg.beamTrunk;
  if (!trunk) return;
  const u = phase === 7 ? easedAngle(t, range) : 0;
  const scaleY = lerp(1, BEAM_TRUNK_MAX_SCALE, u);
  trunk.node.scale.set(
    trunk.initialScale.x,
    trunk.initialScale.y * scaleY,
    trunk.initialScale.z,
  );
}

/** Phase 7 water loops: layer a sine pulse on top of the JSON's static
 *  water_red / water_blue emissive so the loops read as flowing, not
 *  glowing-constant. Runs every frame; emissive magnitude already accounts
 *  for whatever the JSON asked for this scroll fraction. */
function applyWaterPulse(waterRedEmi: number, waterBlueEmi: number, reg: SceneRegistry) {
  const now = performance.now() * 0.001;
  const pulse = 0.35 + 0.35 * Math.sin(now * Math.PI * 2 * WATER_PULSE_HZ);
  const wr = reg.materials.waterRed;
  if (wr && "emissiveIntensity" in wr) {
    wr.emissiveIntensity = waterRedEmi * (0.65 + pulse);
  }
  const wb = reg.materials.waterBlue;
  if (wb && "emissiveIntensity" in wb) {
    // Offset blue by a half-period so red/blue loops alternate, not sync.
    const pulseB = 0.35 + 0.35 * Math.sin(now * Math.PI * 2 * WATER_PULSE_HZ + Math.PI);
    wb.emissiveIntensity = waterBlueEmi * (0.65 + pulseB);
  }
}

/** Eased 0→1 progress within a phase's scroll range, matching the global
 *  power2.inOut used for camera lerps. Shared by hinge + beam scale. */
function easedAngle(t: number, range: readonly [number, number]): number {
  const [s, e] = range;
  return easeInOut(clamp((t - s) / Math.max(e - s, 1e-6), 0, 1));
}

/** Phase 5 "peak technical flex": stagger-fade the 7 authored teardown
 *  slabs (vacuum→crew) as scroll advances through 0.50–0.65, then wash
 *  them out again before phase 6 begins. Hidden entirely outside phase 5. */
function applyTeardown(
  t: number,
  phase: number,
  range: readonly [number, number],
  reg: SceneRegistry,
): void {
  const layers = reg.teardownLayers;
  if (layers.length === 0) return;

  if (phase !== 5) {
    for (const l of layers) l.material.opacity = 0;
    return;
  }

  const [pStart, pEnd] = range;
  const uRaw = (t - pStart) / Math.max(pEnd - pStart, 1e-6);
  const stepStart = 0.1; // each next layer begins 10% of the phase later
  const stepSpan = 0.2;  // each layer takes 20% of the phase to reach full
  const exitStart = 0.85; // fade all back out in the final 15%

  for (const layer of layers) {
    const i = layer.index - 1; // 1-indexed → 0-indexed
    const appear = clamp((uRaw - i * stepStart) / stepSpan, 0, 1);
    const fadeOut = clamp((1 - uRaw) / (1 - exitStart), 0, 1);
    layer.material.opacity = layer.baseOpacity * appear * fadeOut;
  }
}

function interpPhase(a: PhaseSpec, b: PhaseSpec, u: number): PhaseLike {
  const oA = { ...a.opacities, ...(PHASE_OPACITY_OVERRIDES[a.phase] ?? {}) };
  const oB = { ...b.opacities, ...(PHASE_OPACITY_OVERRIDES[b.phase] ?? {}) };
  return {
    opacities: {
      hex_frame: lerp(oA.hex_frame, oB.hex_frame, u),
      hex_glass: lerp(oA.hex_glass, oB.hex_glass, u),
      hex_solar: lerp(oA.hex_solar, oB.hex_solar, u),
      pent_frame: lerp(oA.pent_frame, oB.pent_frame, u),
      pent_glass: lerp(oA.pent_glass, oB.pent_glass, u),
      interior: lerp(oA.interior, oB.interior, u),
      wireframe: lerp(oA.wireframe, oB.wireframe, u),
    },
    emissive: {
      wireframe_cyan: lerp(a.emissive.wireframe_cyan, b.emissive.wireframe_cyan, u),
      led_green: lerp(a.emissive.led_green, b.emissive.led_green, u),
      water_red: lerp(a.emissive.water_red, b.emissive.water_red, u),
      water_blue: lerp(a.emissive.water_blue, b.emissive.water_blue, u),
    },
    hex_translation_m: lerp(a.hex_translation_m, b.hex_translation_m, u),
    pent_translation_m: lerp(a.pent_translation_m, b.pent_translation_m, u),
  };
}

type TimelineEntry = { phase: PhaseSpec; cam: (typeof cameras.cameras)[number] };

function bracket(
  timeline: TimelineEntry[],
  t: number,
): { a: TimelineEntry; b: TimelineEntry; u: number } {
  // Find the phase whose [start,end] contains t; interpolate within it.
  for (let i = 0; i < timeline.length; i += 1) {
    const entry = timeline[i]!;
    const [start, end] = entry.phase.scroll_range;
    if (t >= start && t <= end) {
      const span = Math.max(end - start, 1e-6);
      const u = easeInOut((t - start) / span);
      const nextEntry = timeline[i + 1] ?? entry;
      return { a: entry, b: nextEntry, u };
    }
  }
  return { a: timeline[0]!, b: timeline[0]!, u: 0 };
}

function lerp(a: number, b: number, u: number): number {
  return a + (b - a) * u;
}

function clamp(v: number, min: number, max: number): number {
  return v < min ? min : v > max ? max : v;
}

/** Power2 ease-in-out — matches most of the brief's "power2.inOut" phases. */
function easeInOut(u: number): number {
  return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
}
