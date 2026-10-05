/**
 * What a sponsor can see, download or ask for. Shown at the top of the
 * "Our work" section. Drawings are the Rev S dimensioned sketches in
 * public/blueprints/img (a -thumb.webp and a full .webp for each).
 */
export type DrawingPreview = { name: string; caption: string; w: number; h: number };

export const DRAWING_PREVIEW: DrawingPreview[] = [
  { name: "2d_sketch-04_shell_elevation", caption: "The whole shell, 11,151 mm across", w: 720, h: 480 },
  { name: "2d_sketch-03_hex_panel_plan", caption: "One hexagon panel, from the cabin side", w: 720, h: 480 },
  { name: "2d_sketch-01_simple_joint_section", caption: "The joint between two panels, in section", w: 720, h: 480 },
  { name: "2d_sketch-06_T1_slice_section", caption: "Test T1: a 150 mm slice of the seam, pulled apart", w: 720, h: 480 },
  { name: "2d_sketch-07_T2_rig_section", caption: "Test T2: a quarter-scale panel on its water rig", w: 720, h: 480 },
  { name: "2d_sketch-08_T0_section", caption: "Test T0: a glass disc on the ring-on-ring fixture", w: 720, h: 480 },
];

export const drawingThumb = (name: string) => `/blueprints/img/${name}-thumb.webp`;
export const drawingFull = (name: string) => `/blueprints/img/${name}.webp`;

export type DownloadItem = { title: string; meta: string; body: string; href: string; action: string };

export const DOWNLOADS: DownloadItem[] = [
  {
    title: "The tests, as a film",
    meta: "Web page, 23 min",
    body: "Every test step by step: how each piece is made, what it tells us, plan B, what it costs and when. Chapter buttons, and the words written out underneath.",
    href: "/tests/",
    action: "Watch",
  },
  {
    title: "The drawings, explained",
    meta: "PDF, 53 pages, 8.6 MB",
    body: "Every sketch and render of the shell, the panels, the joint and the three tests, with dimensions and a short note on each.",
    href: "/downloads/HCSA-Rev-S-drawings-explained-26-Sep-2026.pdf",
    action: "Download",
  },
  {
    title: "The blueprints page",
    meta: "Web page",
    body: "The same drawings online. Click any one to see it full size.",
    href: "/blueprints/",
    action: "Open",
  },
  {
    title: "The parts list",
    meta: "Web page",
    body: "Every part and material for the tests, with sizes, quantities and the date we need it by.",
    href: "/plan/#need",
    action: "Open",
  },
];

export const ON_REQUEST: { title: string; body: string }[] = [
  { title: "CAD files (STEP)", body: "The test pieces and rigs, ready for quoting and machining." },
  { title: "The test plan", body: "The requirements, the loads and how each test is run." },
];
