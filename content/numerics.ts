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
    label: "v3 frame depth",
    display: "140 mm",
    source: "SOURCE_OF_TRUTH/structure_baselines/Panels.md",
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
} as const satisfies Record<string, Numeric>;

export type NumericId = keyof typeof NUMERICS;
