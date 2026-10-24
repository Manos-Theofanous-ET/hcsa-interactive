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
    value: 651,
    unit: "kg",
    label: "Pentagon panel mass, base, before variant equipment (with its node and hardpoint shares)",
    display: "651 kg",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  structure_mass: {
    value: 34.0,
    unit: "t",
    label: "Structure mass, frames, ribs, L7, plates, nodes, hardpoint blocks (Rev S: 25.4 t, superseded)",
    display: "34.0 t",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  facility_mass: {
    value: 50.4,
    unit: "t",
    label: "Facility mass, 50,350 kg itemised (Rev S: 41.7 t, superseded)",
    display: "50.4 t",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 11",
  },
  test_pass_tolerance: {
    value: 10,
    unit: "%",
    label: "Test pass band: measurement within this of the digital twin's filed prediction",
    display: "10 %",
    source: "HCSA_RevD_design_spec.md (14 Oct 2026, FEA 9-12 Oct) section 12",
  },

  // ---- Rev E (decided 23 Oct 2026, drawings 8 Nov): the pane and the seal.
  // The Rev D values above (24 panes of 1,125 mm, 25.4 mm glass) stay on the
  // drawings and in the 3D scene until the 8 Nov pack. ----
  reve_pane_side: {
    value: 531,
    unit: "mm",
    label: "Pressure pane side, Rev E baseline (k 4: each 2,250 mm triangle split into 16 panes)",
    display: "531 mm",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_pane_side_upside: {
    value: 708,
    unit: "mm",
    label: "Pressure pane side, Rev E upside (k 3), if T0 gives a high Weibull m",
    display: "708 mm",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_pane_side_fallback: {
    value: 425,
    unit: "mm",
    label: "Pressure pane side, Rev E fallback (k 5), if T0 gives a low Weibull m",
    display: "425 mm",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_l7_thickness: {
    value: 22,
    unit: "mm",
    label: "L7 pressure pane thickness, BOROFLOAT 33, Rev E baseline (Rev D: 25.4 mm on 1,125 mm panes)",
    display: "22 mm",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_panes_per_hex: {
    value: 96,
    unit: "panes",
    label: "Glass panes per hexagon, Rev E baseline (Rev D: 24)",
    display: "96",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_panes_total: {
    value: 1920,
    unit: "panes",
    label: "Glass panes on the shell, Rev E baseline (Rev D: 480)",
    display: "1,920",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },
  reve_seal_rings: {
    value: 2,
    unit: "seals",
    label: "Butyl BA500 seals per seam, Rev E (closed loops; fluorosilicone out, per Parker; RTV566 kept as the third seal)",
    display: "two",
    source: "Decision 23 Oct 2026 (TRUTH Rev E in preparation); campaign findings 16 to 17 Oct",
  },

  // ---- Supplier limits (Oct 2026). What the glass makers can supply and
  // finish at each thickness. Limits, not design choices: the pane is set by
  // the Rev E decision above, and these say what fits. ----
  supremax_rolled_thickness: {
    value: 34.9,
    unit: "mm",
    label: "SUPREMAX 33, rolled, as supplied",
    display: "34.9 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },
  supremax_rolled_sheet_w: {
    value: 1000,
    unit: "mm",
    label: "SUPREMAX 33 rolled sheet, short side",
    display: "1,000 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },
  supremax_rolled_sheet_l: {
    value: 1500,
    unit: "mm",
    label: "SUPREMAX 33 rolled sheet, long side",
    display: "1,500 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },
  supremax_polished_thickness: {
    value: 29.4,
    unit: "mm",
    label: "SUPREMAX 33 ground and polished, from the 34.9 mm rolled sheet",
    display: "29.4 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026 (Swift Glass, Charlie Burke, 14 and 20 Oct: about 1.25 in, the two figures still to be reconciled)",
  },
  swift_max_square: {
    value: 787,
    unit: "mm",
    label: "Largest square part Swift Glass can grind and polish (31 in)",
    display: "787 x 787 mm",
    source: "Swift Glass, Charlie Burke, 14 and 20 Oct 2026",
  },
  borofloat_25_sheet: {
    value: 25.4,
    unit: "mm",
    label: "BOROFLOAT 33 at 25.4 mm: sheet 1,150 x 850 mm",
    display: "25.4 mm at 1,150 x 850 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },
  borofloat_21_sheet: {
    value: 21,
    unit: "mm",
    label: "BOROFLOAT 33 at 21 mm: sheet 1,700 x 1,300 mm",
    display: "21 mm at 1,700 x 1,300 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },
  borofloat_15_sheet: {
    value: 15,
    unit: "mm",
    label: "BOROFLOAT 33 at 15 mm: sheet 2,300 x 1,700 mm",
    display: "15 mm at 2,300 x 1,700 mm",
    source: "SCHOTT standard formats email, Tina Gallo, 20 Oct 2026",
  },

  // ---- Lab facts (Oct 2026): the frames and the glass in hand. ----
  t1_frame_capacity: {
    value: 100,
    unit: "kN",
    label: "Instron 5882 load frame at Brown (BH 092), for the T1 seam pulls; free after 18 Nov 2026",
    display: "100 kN",
    source: "Jerry Zani, Brown School of Engineering, 14 Oct 2026",
  },
  small_frame_capacity: {
    value: 0.5,
    unit: "kN",
    label: "Small load frame at Brown (the plan assumed 5 to 10 kN)",
    display: "0.5 kN",
    source: "Jerry Zani, Brown School of Engineering, 14 Oct 2026",
  },
  t0_bar_width_in: {
    value: 1,
    unit: "in",
    label: "T0 four-point bend bar width, as ENGN 1440 runs it",
    display: "1 in",
    source: "Jerry Zani, 14 Oct 2026; ENGN 1440 bar tests, spring 2027",
  },
  t0_bar_thickness_in: {
    value: 0.125,
    unit: "in",
    label: "T0 four-point bend bar thickness, as ENGN 1440 runs it",
    display: "1/8 in",
    source: "Jerry Zani, 14 Oct 2026; ENGN 1440 bar tests, spring 2027",
  },
  borofloat_discs_received: {
    value: 60,
    unit: "discs",
    label: "BOROFLOAT 33 discs received from SCHOTT North America",
    display: "60",
    source: "Delivery 13 Oct 2026, SCHOTT North America",
  },
  sapphire_discs_received: {
    value: 15,
    unit: "discs",
    label: "Sapphire discs received from Meller Optics",
    display: "15",
    source: "Delivery 13 Oct 2026, Meller Optics",
  },
  daq_channels: {
    value: 16,
    unit: "channels",
    label: "Dewesoft strain DAQ on loan, in 3 to 4 week batches with a month's notice",
    display: "16-channel",
    source: "Dewesoft, Trevor Gajewski, 22 Oct 2026 (loan agreed in principle)",
  },
  drawing_release: {
    value: 8,
    unit: "Nov 2026",
    label: "Drawing release for the test pieces (the Rev E pack)",
    display: "8 Nov 2026",
    source: "Fall plan 28 Sep 2026; decision 23 Oct 2026 (TRUTH Rev E in preparation)",
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
