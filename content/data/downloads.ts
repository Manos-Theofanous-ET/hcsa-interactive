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
  { name: "revd-00_cover", caption: "The Rev D cover sheet, with the index, what changed from Rev S and how to read the drawings", w: 720, h: 509 },
  { name: "revd-02_hex_plan", caption: "One hexagon panel seen from the cabin side, with " + N.panes_per_hex.display + " panes on main and secondary ribs", w: 720, h: 509 },
  { name: "revd-05_seam_joint", caption: "The seam joint cut open, with the two frames, a bolt, the seals and the path the load takes", w: 720, h: 509 },
  { name: "revd-06_corner_node", caption: "The corner node, where three panels meet, which is still a proposal", w: 720, h: 509 },
  { name: "revd-07_hardpoint", caption: "The hardpoint in the middle of a seam, with its lug, clevis and pin, which is still a proposal", w: 720, h: 509 },
  { name: "revd-10_test_articles", caption: "The four test pieces, T0 to T3, drawn against the full facility", w: 720, h: 509 },
];

export const drawingThumb = (name: string) => `/blueprints/img/${name}-thumb.webp`;
export const drawingFull = (name: string) => `/blueprints/img/${name}.webp`;

export type DownloadItem = { title: string; meta: string; body: string; href: string; action: string };

export const DOWNLOADS: DownloadItem[] = [
  {
    title: "The tests, as a film",
    meta: "Web page, 23 minutes",
    body: "A film that goes through every test step by step. It shows how each piece is made, what the test tells us, our plan B, what it costs and when it happens. You can jump between chapters, and the words are written out under the film.",
    href: "/tests/",
    action: "Watch",
  },
  {
    title: "The Rev D blueprint pack",
    meta: "PDF, 13 sheets, 0.3 MB",
    body: "The drawings of Rev D, the design we signed on 14 October 2026 after a stress model of the whole shell set its sizes. They cover the shell, the hexagon and pentagon panels, the ribs, the seam joint, the corner node, the hardpoint, the glass, the test pieces, the materials and mass, and the decisions still open.",
    href: "/downloads/HCSA-Rev-D-blueprint-pack-14-Oct-2026.pdf",
    action: "Download",
  },
  {
    title: "The Rev D design spec",
    meta: "PDF, 6 pages, 0.1 MB",
    body: "This is the one source for the Rev D numbers. Each value is marked as locked, set by the stress model, a proposal, or still open.",
    href: "/downloads/HCSA-Rev-D-design-spec-14-Oct-2026.pdf",
    action: "Download",
  },
  {
    title: "Rev S drawings, explained (out of date)",
    meta: "PDF, 53 pages, 8.6 MB",
    body: "Rev S was our design until Rev D replaced it on 14 October 2026. This file has every sketch and render of the Rev S shell, panels, joint and tests, with dimensions and a short note on each. We keep it for reference.",
    href: "/downloads/HCSA-Rev-S-drawings-explained-26-Sep-2026.pdf",
    action: "Download",
  },
  {
    title: "The blueprints page",
    meta: "Web page",
    body: "See the Rev D sheets and the Rev S drawings online. Click any one to see it full size.",
    href: "/blueprints/",
    action: "Open",
  },
  {
    title: "The parts list",
    meta: "Web page",
    body: "It lists every part and material for the tests, with sizes, quantities and the date we need each one.",
    href: "/plan/#need",
    action: "Open",
  },
  {
    title: "Meetings register (23 October 2026)",
    meta: "Google Doc",
    body: "It records what each meeting in October changed about the load frames, the glass tests, the seal, the pane, the suppliers and the dates. It opens in Google Docs.",
    href: "https://docs.google.com/document/d/1HVu05Gn9fgm8OwNxXRq6qbaqKN4YYxC943rhsSCkQ5s/edit",
    action: "Open",
  },
];

export const ON_REQUEST: { title: string; body: string }[] = [
  { title: "CAD files (STEP)", body: "CAD models of the test pieces and rigs, ready for quotes and machining." },
  { title: "The test plan", body: "It sets out the requirements, the loads and how each test is run." },
  { title: "TRUTH Rev D, the master specification", body: "TRUTH is our master spec, the one document every drawing and model has to agree with. We share it with the team and with partners who ask for it." },
];
