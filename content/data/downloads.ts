/**
 * What a sponsor can see, download or ask for. Shown at the top of the
 * "Our work" section. Drawings are the Rev D sheets (14 Oct 2026) in
 * public/blueprints/img (a -thumb.webp and a full .webp for each); the
 * Rev S sketches stay in the same folder for the blueprints page.
 */
import { NUMERICS as N } from "../numerics";

export type DrawingPreview = { name: string; caption: string; w: number; h: number };

/** Thumb size is 720 x 509 for every Rev D sheet (A3 landscape). */
export const DRAWING_PREVIEW: DrawingPreview[] = [
  { name: "revd-00_cover", caption: "Rev D cover: index, what changed from Rev S, conventions", w: 720, h: 509 },
  { name: "revd-02_hex_plan", caption: "One hexagon panel from the cabin side: " + N.panes_per_hex.display + " panes on main and secondary ribs", w: 720, h: 509 },
  { name: "revd-05_seam_joint", caption: "The seam joint in section: two frames, bolt, seals and the load path", w: 720, h: 509 },
  { name: "revd-06_corner_node", caption: "The corner node, where three panels meet (proposal)", w: 720, h: 509 },
  { name: "revd-07_hardpoint", caption: "The mid-seam hardpoint: lug, clevis and pin (proposal)", w: 720, h: 509 },
  { name: "revd-10_test_articles", caption: "The test articles against the facility: T0, T1, T2, T3", w: 720, h: 509 },
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
    title: "The Rev D blueprint pack",
    meta: "PDF, 13 sheets, 0.3 MB",
    body: "The baseline sized by the whole-shell stress model (14 Oct 2026): shell, hexagon and pentagon panels, ribs, seam joint, corner node, hardpoint, glazing, test articles, materials and mass, open decisions.",
    href: "/downloads/HCSA-Rev-D-blueprint-pack-14-Oct-2026.pdf",
    action: "Download",
  },
  {
    title: "The Rev D design spec",
    meta: "PDF, 6 pages, 0.1 MB",
    body: "The one source for the Rev D numbers: every value with its status, locked, from the stress model, proposal or still open.",
    href: "/downloads/HCSA-Rev-D-design-spec-14-Oct-2026.pdf",
    action: "Download",
  },
  {
    title: "Rev S drawings, explained (superseded 14 Oct 2026)",
    meta: "PDF, 53 pages, 8.6 MB",
    body: "Every sketch and render of the Rev S shell, panels, joint and tests, with dimensions and a short note on each. Kept for reference.",
    href: "/downloads/HCSA-Rev-S-drawings-explained-26-Sep-2026.pdf",
    action: "Download",
  },
  {
    title: "The blueprints page",
    meta: "Web page",
    body: "The Rev D sheets and the Rev S drawings online. Click any one to see it full size.",
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
  {
    title: "Meetings register (23 Oct 2026)",
    meta: "Google Doc",
    body: "What each October meeting changed: the load frames, the glass tests, the seal, the pane, the suppliers and the dates. Opens in Google Docs.",
    href: "https://docs.google.com/document/d/1HVu05Gn9fgm8OwNxXRq6qbaqKN4YYxC943rhsSCkQ5s/edit",
    action: "Open",
  },
];

export const ON_REQUEST: { title: string; body: string }[] = [
  { title: "CAD files (STEP)", body: "The test pieces and rigs, ready for quoting and machining." },
  { title: "The test plan", body: "The requirements, the loads and how each test is run." },
  { title: "TRUTH Rev D, the master specification", body: "The team's full engineering source of truth, for team and partners; ask." },
];
