/**
 * Gallery of the project's work. Files live in public/assets/web/ and are
 * generated from the originals in public/assets/{images,blueprints,prototype}
 * by `python scripts/optimize-images.py`. Each entry has a full-size
 * `<file>.webp` and a `<file>-thumb.webp`.
 *
 * Renders that failed to shade (cutaway, exterior hero, shield family,
 * docking family) and blueprint page 15 (still has a placeholder line)
 * are left out on purpose; see SKIP in the script.
 */
import { NUMERICS as N } from "../numerics";

export type GalleryCategory = {
  id: string;
  title: string;
  blurb: string;
  /** Optional link shown under the blurb (for example to the static pages). */
  link?: { href: string; label: string };
  items: GalleryItem[];
};

export type GalleryItem = {
  file: string;
  /** Short caption shown under the thumbnail and in the viewer. */
  caption: string;
  /** Pixel size of the thumbnail, so the grid reserves space (no layout shift). */
  w: number;
  h: number;
};

export const GALLERY: GalleryCategory[] = [
  {
    id: "master-model",
    title: "The station, Rev E (master 3D model)",
    blurb: "Stills from the master 3D model of 30 October 2026, built on the Rev E design: all 32 panels, the 96-pane glass hexagons, the solar pentagons and shields, the column, greenhouses and Marina's pods. The model itself opens in the browser, with a walk-through, the systems, shields and pressure, the 90-minute visit and the station's whole life.",
    link: { href: "/model/", label: "Open the 3D model" },
    items: [
      { file: "master-approach", caption: "The station 400 km above the Earth: 20 glass hexagons and 12 solar pentagons, 11.151 m across", w: 720, h: 405 },
      { file: "master-inside", caption: "Inside: the column, the greenhouses and the Earth through the glass", w: 720, h: 405 },
      { file: "master-pods", caption: "Marina's two pods hang from the column (cutaway)", w: 720, h: 405 },
      { file: "master-systems", caption: "Systems X-ray: power from the solar pentagons to the bus in the column", w: 720, h: 405 },
      { file: "master-shields", caption: "Shields inflated over the windows, seams carrying the pressure load", w: 720, h: 405 },
      { file: "master-visit-night", caption: "The visit, night side: a small concert by the column, streamed to Earth", w: 720, h: 405 },
      { file: "master-assembly", caption: "Assembling in orbit: panels come off the launch stack one by one", w: 720, h: 405 },
    ],
  },
  {
    id: "concepts",
    title: "Interior concept",
    blurb: "Marina Kouroumali's working images for the interior, the ones to look at when we talk about the inside. Some were made with AI image tools; they show the working concept, not a final design.",
    items: [
      { file: "prototype-whatsapp-image-2026-04-03-at-3-17-43-pm", caption: "Moving freely: people float, climb and cycle around the garden column (Marina Kouroumali)", w: 720, h: 720 },
      { file: "prototype-whatsapp-image-2026-04-03-at-3-18-17-pm", caption: "The track and the garden column, with Earth below (Marina Kouroumali)", w: 691, h: 720 },
      { file: "images-facility-render-night", caption: "Two pods beside the garden column, with the ramp spiralling round it (Marina Kouroumali)", w: 720, h: 480 },
      { file: "images-facility-annotated-dimensions", caption: "Marina's sketch with first sizes for the ramp, the pods and the column", w: 720, h: 473 },
      { file: "images-facility-render-day", caption: "The same pods and ramp by day (Marina Kouroumali)", w: 720, h: 480 },
    ],
  },
  {
    id: "earlier-concepts",
    title: "Earlier concepts",
    blurb: "Mood images from before the working concept. They show ideas we explored, not the current design.",
    items: [
      { file: "images-concept-observatory", caption: "Walkways and gardens under a glass sky", w: 480, h: 720 },
      { file: "images-concept-plants", caption: "Terraced gardens along the inner wall", w: 583, h: 720 },
      { file: "images-concept-interior", caption: "Ropes in a garden corner at night", w: 720, h: 720 },
    ],
  },
  {
    id: "blueprints",
    title: "Blueprints",
    blurb: "The Rev S drawings (September 2026, superseded by Rev D on 14 October 2026), taken from the CAD model, with dimensions in millimetres. The Rev D sheets and every Rev S drawing, with a plain explanation of each, are on the blueprints page.",
    link: { href: "/blueprints/", label: "Open all the blueprints" },
    items: [
      { file: "revs-3d_render-01_shell_exterior", caption: "The whole shell, 11,151 mm across: 20 glass hexagons and 12 solid pentagons", w: 720, h: 480 },
      { file: "revs-3d_render-02_shell_cutaway", caption: "The shell cut in half; the parts the cut goes through are orange", w: 720, h: 480 },
      { file: "revs-3d_render-03_hex_panel_cabin_side", caption: "One hexagon panel from the cabin side: frames, ribs and six glass panes (Rev S; Rev D has " + N.panes_per_hex.display + ")", w: 720, h: 529 },
      { file: "revs-2d_sketch-01_simple_joint_section", caption: "The joint between two panels, cut through a bolt", w: 720, h: 480 },
      { file: "revs-3d_render-07_seam_closeup_cut", caption: "A piece of seam cut through a bolt: two frames, two O-rings and a sealant bead", w: 720, h: 480 },
      { file: "revs-3d_render-09_corner_node_inside", caption: "A corner where three panels meet, from inside", w: 720, h: 480 },
      { file: "revs-3d_render-18_T0_ring_on_ring_cut", caption: "Test T0: a 50 mm glass disc in the ring-on-ring fixture", w: 720, h: 535 },
      { file: "revs-3d_render-10_T1_slice_150", caption: "Test T1: a full-size 150 mm slice of the seam, ready to be pulled apart", w: 720, h: 480 },
      { file: "revs-3d_render-14_T2_rig_pinned", caption: "Test T2: one panel at quarter scale in its water rig", w: 720, h: 480 },
    ],
  },
  {
    id: "model",
    title: "3D model",
    blurb: "The CAD model (Rev S, September 2026; the Rev D sizes are on the blueprints page): all 32 panels and 90 seams. The 3D scene at the top of this page is built from it.",
    items: [
      { file: "revs-clean-3d-01_shell_exterior", caption: "The whole shell, 11.15 m across: 20 glass hexagons and 12 solid pentagons", w: 720, h: 480 },
      { file: "revs-clean-3d-02_shell_cutaway", caption: "The shell cut in half; the parts the cut goes through are orange", w: 720, h: 480 },
      { file: "revs-clean-2d-01_shell_elevation", caption: "The shell from the side", w: 720, h: 480 },
      { file: "revs-clean-2d-02_shell_plan_top", caption: "The shell from above", w: 720, h: 480 },
      { file: "revs-clean-3d-08_corner_node_outside", caption: "A corner where three panels meet, from outside", w: 720, h: 480 },
      { file: "revs-clean-3d-09_corner_node_inside", caption: "The same corner from inside", w: 720, h: 480 },
      { file: "revs-clean-3d-07_seam_closeup_cut", caption: "A piece of seam cut through a bolt: two frames, two O-rings and a sealant bead", w: 720, h: 480 },
    ],
  },
  {
    id: "panels",
    title: "Panels",
    blurb: "The building block of the station. Every panel connects the same way. The six-sided panels are the windows; the five-sided ones are solid and house the solar panels and fold-out shields.",
    items: [
      { file: "revs-clean-3d-03_hex_panel_cabin_side", caption: "One hexagon panel from the cabin side: edge frames, six ribs and the glass panes (Rev S; Rev D splits each bay into four)", w: 720, h: 480 },
      { file: "revs-clean-3d-04_hex_panel_exterior_side", caption: "The same panel from outside", w: 720, h: 480 },
      { file: "revs-clean-3d-05_pent_panel_cabin_side", caption: "One pentagon panel. It is solid; the model shows its frames, ribs and plate so far", w: 720, h: 480 },
      { file: "revs-clean-2d-03_hex_panel_plan_exterior", caption: "Hexagon panel, flat view from outside", w: 720, h: 480 },
      { file: "revs-clean-2d-05_pent_panel_plan_exterior", caption: "Pentagon panel, flat view from outside", w: 720, h: 480 },
      { file: "revs-clean-2d-06_seam_section", caption: "The seam between two panels, cut through a bolt", w: 720, h: 480 },
    ],
  },
  {
    id: "prototype",
    title: "Physical model",
    blurb: "A hand-built scale model of the shell and garden column.",
    items: [
      { file: "images-prototype-photo-1", caption: "Scale model with the garden column inside", w: 540, h: 720 },
      { file: "images-prototype-photo-2", caption: "Light passing through the model", w: 540, h: 720 },
      { file: "images-prototype-photo-3", caption: "The model's clear panels and frame", w: 540, h: 720 },
    ],
  },
  {
    id: "sheets",
    title: "Earlier sheets",
    blurb: "Our technical sheets from March 2026. Some numbers have changed since; the current drawings are in the Blueprints tab.",
    items: [
      { file: "blueprints-page-01", caption: "Project overview", w: 720, h: 402 },
      { file: "blueprints-page-02", caption: "Why a glass sphere instead of metal tubes", w: 720, h: 402 },
      { file: "blueprints-page-03", caption: "The shape and its key measurement", w: 720, h: 402 },
      { file: "blueprints-page-04", caption: "How hard the air pushes on each panel", w: 720, h: 402 },
      { file: "blueprints-page-05", caption: "The seven panel layers", w: 720, h: 402 },
      { file: "blueprints-page-06", caption: "How the panel joint keeps the air in", w: 720, h: 402 },
      { file: "blueprints-page-07", caption: "Comparing three design options", w: 720, h: 402 },
      { file: "blueprints-page-08", caption: "How docking forces spread through the frame", w: 720, h: 402 },
      { file: "blueprints-page-09", caption: "Getting around inside", w: 720, h: 402 },
      { file: "blueprints-page-10", caption: "Garden alcoves", w: 720, h: 402 },
      { file: "blueprints-page-11", caption: "The central column", w: 720, h: 402 },
      { file: "blueprints-page-12", caption: "Making clean water with sunlight", w: 720, h: 402 },
      { file: "blueprints-page-13", caption: "How people, plants and machines work together", w: 720, h: 402 },
      { file: "blueprints-page-14", caption: "How it gets built and tested", w: 720, h: 402 },
    ],
  },
];
