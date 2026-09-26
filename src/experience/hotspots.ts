import { NUMERICS as N } from "@content/numerics";
import type { HotspotLabelProps } from "./HotspotLabel";

/** Hotspot definitions for Phase 3/5/6/7. Labels are plain language for
 *  sponsors; every number comes from content/numerics.ts (which carries
 *  the CANONICAL.md / SOURCE_OF_TRUTH citation).
 *
 *  Positions use world-space coordinates in metres. For shell-surface
 *  hotspots we pick points at roughly the outer radius (5.58 m) along
 *  approximate canonical face directions. For interior hotspots we use
 *  camera-target neighbourhoods from `cameras.json` (near the corresponding
 *  phase camera's focus point). These are approximations — fine-tune once
 *  the live site shows where they actually land.
 *
 *  scroll_range phase-mapping (from phase_metadata.json):
 *    Phase 3: 0.20 – 0.35
 *    Phase 5: 0.50 – 0.65
 *    Phase 6: 0.65 – 0.75
 *    Phase 7: 0.75 – 0.85
 */
export type HotspotDef = Omit<HotspotLabelProps, "progressRef">;

export const HOTSPOTS: readonly HotspotDef[] = [
  // --- Phase 3: Geometry Reveal (20–35 %) ---
  {
    position: [5.58, 0.0, 0.0],
    label: `${N.diameter.display} across`,
    source: "Width of the whole station",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [2.8, 3.4, 3.4],
    label: `${N.edge.display} edges`,
    source: `Every frame edge is the same length, ${N.edges.display} edges in total`,
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [0.0, 5.4, 0.8],
    label: `${N.hex_count.display} six-sided, ${N.pent_count.display} five-sided`,
    source: `${N.face_count.display} panels make up the shell`,
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [-3.8, 0.0, 4.0],
    label: "Docking port",
    source: "One five-sided panel is where spacecraft connect",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },

  // --- Phase 5: Panel Teardown (50–65 %) ---
  // The seven teardown slabs stack radially outward from world origin along
  // a single face normal. Place labels near that stack.
  {
    position: [0.0, 0.0, 2.6],
    label: `${N.frame_depth.display} thick`,
    source: "Total thickness of one window panel",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [0.5, 0.3, 2.0],
    label: `${N.panel_layers.display} layers, space to cabin`,
    source: "Shield, frame, solar cells, tint, gas layer, shade, inner frame",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [-0.6, 0.0, 2.4],
    label: "Aluminium frame",
    source: "Carries the air pressure load so the glass does not have to",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [-0.4, -1.1, 1.4],
    label: "Locking bolts",
    source: "Aerospace bolts join each panel to its neighbours",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [0.8, 0.0, 1.8],
    label: "Triple air seal",
    source: "Two rubber seals plus a sealant layer keep the air in",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },

  // --- Phase 6: Pentagon Greenhouse (65–75 %) ---
  // Camera target is [-5.03, 0, 3.26]; the hinge opens PENT_02 90° outward.
  {
    position: [-5.0, 0.0, 4.0],
    label: "Five-sided panel",
    source: "Solid, not a window: it houses solar panels and a fold-out shield",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },
  {
    position: [-4.4, 0.8, 3.2],
    label: "Plants clean the air",
    source: "Garden trays under grow lights make oxygen and food",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },
  {
    position: [-5.5, -0.9, 2.4],
    label: "Shields for the windows",
    source: "Every window borders three five-sided panels, so a shield can fold out over it",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },

  // --- Phase 7: Systems Core (75–85 %) ---
  // Camera target [0, 0, 1.5] — near the axial trunk.
  {
    position: [0.4, 0.6, 2.4],
    label: "Central column",
    source: "Carries air, water, power and storage through the station",
    phaseRange: [0.75, 0.85],
    tone: "orange",
  },
  {
    position: [-0.8, 0.0, 1.8],
    label: "Clean water loop",
    source: `About ${N.water_distill_per_day.display} of clean water made with sunlight`,
    phaseRange: [0.75, 0.85],
    tone: "blue",
  },
  {
    position: [1.0, -0.4, 1.2],
    label: "Heat out, water back",
    source: "Red pipes carry heat out, blue pipes bring clean water back",
    phaseRange: [0.75, 0.85],
    tone: "orange",
  },
  {
    position: [0.0, 0.8, 0.6],
    label: "Station core",
    source: "The main axis that runs through the middle of the station",
    phaseRange: [0.75, 0.85],
    tone: "cyan",
  },
];
