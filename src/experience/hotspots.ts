import type { HotspotLabelProps } from "./HotspotLabel";

/** Hotspot definitions for Phase 3/5/6/7. Every number is cited to
 *  CANONICAL.md or the shipped data JSONs so nothing is invented.
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
    label: "11.15 m Ø",
    source: "Outer diameter · CANONICAL §Dimensions",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [2.8, 3.4, 3.4],
    label: "2.25 m edge",
    source: "Canonical edge length · 90 edges · CANONICAL §Dimensions",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [0.0, 5.4, 0.8],
    label: "20 HEX · 12 PENT",
    source: "Truncated icosahedron · 32 faces · CANONICAL §Shell Topology",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },
  {
    position: [-3.8, 0.0, 4.0],
    label: "1 docking face",
    source: "Exactly one pent is the dock · CANONICAL §Docking Face",
    phaseRange: [0.2, 0.35],
    tone: "cyan",
  },

  // --- Phase 5: Panel Teardown (50–65 %) ---
  // The seven teardown slabs stack radially outward from world origin along
  // a single face normal. Place labels near that stack.
  {
    position: [0.0, 0.0, 2.6],
    label: "140 mm depth",
    source: "v3 frame · CANONICAL §Hex Face Stackup",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [0.5, 0.3, 2.0],
    label: "7 layers · vacuum → crew",
    source: "Sacrificial → solar → tint → gas → shade → frame · CANONICAL",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [-0.6, 0.0, 2.4],
    label: "6061-T6 aluminium",
    source: "Frame material · CANONICAL §Joint / Section Values",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [0.0, -0.4, 1.4],
    label: "NAS9306C-06 · Ø 4.83 mm",
    source: "Lockbolt hole basis · 39 mm pitch · CANONICAL",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },
  {
    position: [0.8, 0.0, 1.8],
    label: "Dual fluorosilicone · 1.6 mm",
    source: "Gasket stack · RTV tertiary seal · CANONICAL",
    phaseRange: [0.5, 0.65],
    tone: "cyan",
  },

  // --- Phase 6: Pentagon Greenhouse (65–75 %) ---
  // Camera target is [-5.03, 0, 3.26]; the hinge opens PENT_02 90° outward.
  {
    position: [-5.0, 0.0, 4.0],
    label: "PENT_02 · 90° hinge",
    source: "Greenhouse bloom · phase_metadata §pentagon_hinge",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },
  {
    position: [-4.4, 0.8, 3.2],
    label: "Bioregenerative ECLSS",
    source: "Plant trays · biology-green LEDs · WEB_ASSET_BRIEF §Phase 6",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },
  {
    position: [-5.5, -0.9, 2.4],
    label: "Plant-lit pentagon",
    source: "Pent module family · CANONICAL §Pent Face Module Types",
    phaseRange: [0.65, 0.75],
    tone: "green",
  },

  // --- Phase 7: Systems Core (75–85 %) ---
  // Camera target [0, 0, 1.5] — near the axial trunk.
  {
    position: [0.4, 0.6, 2.4],
    label: "BEAM_TRUNK · 3× extend",
    source: "Systems longitudinal split · phase_metadata §phase 7",
    phaseRange: [0.75, 0.85],
    tone: "orange",
  },
  {
    position: [-0.8, 0.0, 1.8],
    label: "Closed-loop distillate",
    source: "15 L/day water · WEB_ASSET_BRIEF §Phase 7",
    phaseRange: [0.75, 0.85],
    tone: "blue",
  },
  {
    position: [1.0, -0.4, 1.2],
    label: "Thermal · 1.25 Hz pulse",
    source: "Red/blue water loops · alternating · scene.phase 7",
    phaseRange: [0.75, 0.85],
    tone: "orange",
  },
  {
    position: [0.0, 0.8, 0.6],
    label: "Axial core",
    source: "Habitat principal axis · CANONICAL §Axial Core",
    phaseRange: [0.75, 0.85],
    tone: "cyan",
  },
];
