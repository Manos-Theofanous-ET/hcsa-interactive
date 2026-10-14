/**
 * Canonical numerics — every value the site cites should come from here,
 * and every entry carries its source file. If a number changes, update
 * it here and the source, not in the copy.
 *
 * Source of truth lives in
 * `../blender-automation/references/geometry_truth/CANONICAL.md`
 * and the team's `internal_release_revB/SOURCE_OF_TRUTH/`.
 */

export type Numeric = {
  value: number;
  unit: string;
  label: string;
  /** Publish-quality rounded form, used in copy. */
  display: string;
  source: string;
};

export const NUMERICS = {
  diameter: {
    value: 11.151083966,
    unit: "m",
    label: "Outer diameter",
    display: "11.15 m",
    source: "SOURCE_OF_TRUTH/structure_baselines/HCSA-BASELINE-001.md",
  },
  edge: {
    value: 2.25,
    unit: "m",
    label: "Edge length",
    display: "2.25 m",
    source: "SOURCE_OF_TRUTH/structure_baselines/HCSA-BASELINE-001.md",
  },
  volume_enclosed: {
    value: 629.762,
    unit: "m³",
    label: "Enclosed volume",
    display: "629.8 m³",
    source: "SHARED_DOCS/HCSA_Key_Calculations.md",
  },
  volume_habitable_min: {
    value: 520,
    unit: "m³",
    label: "Habitable volume (min)",
    display: "~520 m³",
    source: "SOURCE_OF_TRUTH/HCSA_Architectural_Zones.md",
  },
  volume_habitable_max: {
    value: 560,
    unit: "m³",
    label: "Habitable volume (max)",
    display: "~560 m³",
    source: "SOURCE_OF_TRUTH/HCSA_Architectural_Zones.md",
  },
  surface_area: {
    value: 367.574,
    unit: "m²",
    label: "External surface area",
    display: "367.6 m²",
    source: "SOURCE_OF_TRUTH/structure_baselines/HCSA-BASELINE-001.md",
  },
  face_count: {
    value: 32,
    unit: "faces",
    label: "Total faces",
    display: "32",
    source: "CANONICAL.md",
  },
  hex_count: {
    value: 20,
    unit: "faces",
    label: "Hex panels",
    display: "20",
    source: "CANONICAL.md",
  },
  pent_count: {
    value: 12,
    unit: "faces",
    label: "Pent panels",
    display: "12",
    source: "CANONICAL.md",
  },
  edges: {
    value: 90,
    unit: "edges",
    label: "Frame edges",
    display: "90",
    source: "CANONICAL.md",
  },
  vertices: {
    value: 60,
    unit: "nodes",
    label: "Joint nodes",
    display: "60",
    source: "CANONICAL.md",
  },
  hex_area: {
    value: 13.1528,
    unit: "m²",
    label: "Hex panel area",
    display: "13.15 m²",
    source: "SHARED_DOCS/HCSA_Key_Calculations.md",
  },
  hex_force_1atm: {
    value: 1332.703,
    unit: "kN",
    label: "Hex pressure load @ 1 atm",
    display: "1332 kN",
    source: "SHARED_DOCS/HCSA_Key_Calculations.md",
  },
  pent_area: {
    value: 8.7099,
    unit: "m²",
    label: "Pent panel area",
    display: "8.71 m²",
    source: "SHARED_DOCS/HCSA_Key_Calculations.md",
  },
  pent_force_1atm: {
    value: 882.532,
    unit: "kN",
    label: "Pent pressure load @ 1 atm",
    display: "883 kN",
    source: "SHARED_DOCS/HCSA_Key_Calculations.md",
  },
  frame_depth: {
    value: 140,
    unit: "mm",
    label: "Edge frame depth (unchanged in Rev D)",
    display: "140 mm",
    source: "SOURCE_OF_TRUTH/structure_baselines/Panels.md; HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 4",
  },
  cabin_pressure: {
    value: 101.325,
    unit: "kPa",
    label: "Cabin pressure",
    display: "101.3 kPa (1 atm)",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/BIO-LS.md",
  },
  o2_per_crew: {
    value: 0.84,
    unit: "kg/day",
    label: "O₂ consumption / crew",
    display: "0.84 kg/day",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/BIO-LS.md",
  },
  co2_per_crew: {
    value: 1.0,
    unit: "kg/day",
    label: "CO₂ production / crew",
    display: "1.0 kg/day",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/BIO-LS.md",
  },
  water_distill_per_day: {
    value: 15,
    unit: "L/day",
    label: "Thermal distillation rate",
    display: "15 L/day",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/Distillation_Water_Calculations.md",
  },
  water_loop_per_day: {
    value: 600,
    unit: "L/day",
    label: "Closed water loop",
    display: "480–720 L/day",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/Distillation_Water_Calculations.md",
  },
  crew_min: {
    value: 4,
    unit: "crew",
    label: "Design crew (min)",
    display: "4",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/BIO-LS.md",
  },
  crew_max: {
    value: 10,
    unit: "crew",
    label: "Design crew (max)",
    display: "10",
    source: "BIO_LIFE_SUPPORT_PLANTS/core_design/BIO-LS.md",
  },
  panel_layers: {
    value: 7,
    unit: "layers",
    label: "Layers in each window panel",
    display: "7",
    source: "SOURCE_OF_TRUTH/structure_baselines/Panels.md",
  },
  coupon_size: {
    value: 550,
    unit: "mm",
    label: "Physical joint test piece (T1 joint article)",
    display: "550 mm",
    source: "public/assets/blueprints/page-14.png (Validation Roadmap)",
  },
  roadmap_current: {
    value: 4,
    unit: "step",
    label: "Current roadmap step",
    display: "4",
    source: "content/chapters/08-validation.mdx; HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 12",
  },
  roadmap_total: {
    value: 7,
    unit: "steps",
    label: "Roadmap steps",
    display: "7",
    source: "content/chapters/08-validation.mdx; HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 12",
  },

  // ---- Rev D (14 Oct 2026): the FEA-sized baseline. Rev S values that these
  // replace: 6 panes of 2.19 m2 per hexagon, 31 mm L7, 1,650 kg hexagon,
  // 40.9 t facility, bolts carrying the whole seam tension. ----
  panes_per_hex: {
    value: 24,
    unit: "panes",
    label: "Glass panes per hexagon (Rev S: 6, superseded)",
    display: "24",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 2",
  },
  panes_total: {
    value: 480,
    unit: "panes",
    label: "Glass panes on the shell (Rev S: 120, superseded)",
    display: "480",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 2",
  },
  pane_side: {
    value: 1.125,
    unit: "m",
    label: "Pane side (equilateral triangle, the span the FEA models)",
    display: "1.125 m",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 2",
  },
  pane_area: {
    value: 0.548,
    unit: "m²",
    label: "Pane area (Rev S: 2.19 m², superseded)",
    display: "0.548 m²",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 2",
  },
  l7_thickness: {
    value: 25.4,
    unit: "mm",
    label: "L7 pressure pane thickness, BOROFLOAT 33 (Rev S: 31 mm, superseded)",
    display: "25.4 mm",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 7",
  },
  main_rib_depth: {
    value: 375,
    unit: "mm",
    label: "Main rib depth, hexagon (I-section; Rev S: 103 mm, superseded)",
    display: "375 mm",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 3",
  },
  secondary_rib_depth: {
    value: 160,
    unit: "mm",
    label: "Secondary rib depth (I-section; 200 mm if the hardpoint is moment-carrying, OPEN)",
    display: "160 mm",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 3",
  },
  corner_node_mass: {
    value: 5.8,
    unit: "kg",
    label: "Corner node block mass, per vertex (PROPOSAL)",
    display: "5.8 kg",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 5",
  },
  seam_tension: {
    value: 623,
    unit: "kN",
    label: "Seam tension at 1 atm, per 2.25 m seam",
    display: "623 kN",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 1",
  },
  bolt_stations_per_seam: {
    value: 29,
    unit: "stations",
    label: "Bolt stations per seam at 75 mm pitch",
    display: "29",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 4",
  },
  bolts_per_seam: {
    value: 26,
    unit: "bolts",
    label: "Seal-clamp bolts per seam (stations not taken by the corner blocks and the hardpoint; PROPOSAL)",
    display: "26",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 4",
  },
  bolts_total: {
    value: 2340,
    unit: "bolts",
    label: "Seal-clamp bolts on the shell (Rev S: 2,610, superseded)",
    display: "2,340",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 4",
  },
  bolt_service_load: {
    value: 12,
    unit: "kN",
    label: "Seam bolt service load at 1 atm, upper end of the 2 to 12 kN range",
    display: "12 kN",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 4",
  },
  hex_panel_mass: {
    value: 1838,
    unit: "kg",
    label: "Hexagon panel mass (Rev S: 1,650 kg, superseded)",
    display: "1,838 kg",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  pentagon_base_mass: {
    value: 621,
    unit: "kg",
    label: "Pentagon panel mass, base, before variant equipment",
    display: "621 kg",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  structure_mass: {
    value: 33.3,
    unit: "t",
    label: "Structure mass, frames, ribs, L7, plates, nodes (Rev S: 25.4 t, superseded)",
    display: "33.3 t",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  facility_mass: {
    value: 50.9,
    unit: "t",
    label: "Facility mass (Rev S: 41.7 t, superseded)",
    display: "50.9 t",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  test_pass_tolerance: {
    value: 10,
    unit: "%",
    label: "Test pass band: measurement within this of the digital twin's filed prediction",
    display: "10 %",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 12",
  },
} as const satisfies Record<string, Numeric>;

export type NumericId = keyof typeof NUMERICS;

/** Plain-language comparisons derived from the values above, so copy for
 *  non-engineers still traces back to a cited number. */
export const PLAIN = {
  /** Hex pressure load expressed as a weight (kN / g → tonnes). */
  hex_force_tonnes: Math.round(NUMERICS.hex_force_1atm.value / 9.81),
  /** Enclosed volume as a fraction of a 2,500 m³ Olympic pool (50 × 25 × 2 m). */
  pool_fraction: NUMERICS.volume_enclosed.value / 2500,
} as const;
