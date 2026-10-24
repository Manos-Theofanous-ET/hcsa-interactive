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
    id: "concepts",
    title: "Interior concept",
    blurb: "These are Marina Kouroumali's working images for the interior. Look at these when we talk about the inside. Some were made with AI image tools, and they show the working concept, not a final design.",
    items: [
      { file: "prototype-whatsapp-image-2026-04-03-at-3-17-43-pm", caption: "People float, climb and cycle around the garden column (Marina Kouroumali)", w: 720, h: 720 },
      { file: "prototype-whatsapp-image-2026-04-03-at-3-18-17-pm", caption: "The track and the garden column, with Earth below (Marina Kouroumali)", w: 691, h: 720 },
      { file: "images-facility-render-night", caption: "Two pods beside the garden column, with the ramp spiralling round it (Marina Kouroumali)", w: 720, h: 480 },
      { file: "images-facility-annotated-dimensions", caption: "Marina's sketch with the first sizes for the ramp, the pods and the column", w: 720, h: 473 },
      { file: "images-facility-render-day", caption: "The same pods and ramp by day (Marina Kouroumali)", w: 720, h: 480 },
    ],
  },
  {
    id: "earlier-concepts",
    title: "Earlier concepts",
    blurb: "These mood images come from before the working concept. They show ideas we explored, not the current design.",
    items: [
      { file: "images-concept-observatory", caption: "Walkways and gardens under a glass sky", w: 480, h: 720 },
      { file: "images-concept-plants", caption: "Terraced gardens along the inner wall", w: 583, h: 720 },
      { file: "images-concept-interior", caption: "Ropes in a garden corner at night", w: 720, h: 720 },
    ],
  },
  {
    id: "blueprints",
    title: "Blueprints",
    blurb: "These are the Rev S drawings from September 2026, taken from the CAD model, with dimensions in millimetres. Rev D replaced Rev S on 14 October 2026. The Rev D sheets and every Rev S drawing, each with a plain explanation, are on the blueprints page.",
    link: { href: "/blueprints/", label: "Open all the blueprints" },
    items: [
      { file: "revs-3d_render-01_shell_exterior", caption: "The whole shell, 11,151 mm across, with " + N.hex_count.display + " glass hexagons and " + N.pent_count.display + " solid pentagons", w: 720, h: 480 },
      { file: "revs-3d_render-02_shell_cutaway", caption: "The shell cut in half, with the parts the cut goes through in orange", w: 720, h: 480 },
      { file: "revs-3d_render-03_hex_panel_cabin_side", caption: "One hexagon panel seen from the cabin side, with its frames, ribs and six glass panes. This is Rev S, and Rev D has " + N.panes_per_hex.display + " panes.", w: 720, h: 529 },
      { file: "revs-2d_sketch-01_simple_joint_section", caption: "The joint between two panels, cut through a bolt", w: 720, h: 480 },
      { file: "revs-3d_render-07_seam_closeup_cut", caption: "A piece of seam cut through a bolt, with two frames, two O-rings and a bead of sealant", w: 720, h: 480 },
      { file: "revs-3d_render-09_corner_node_inside", caption: "A corner where three panels meet, from inside", w: 720, h: 480 },
      { file: "revs-3d_render-18_T0_ring_on_ring_cut", caption: "Test T0 as first planned, with a 50 mm glass disc in the ring-on-ring fixture", w: 720, h: 535 },
      { file: "revs-3d_render-10_T1_slice_150", caption: "Test T1, a full-size 150 mm slice of the seam, ready to be pulled apart", w: 720, h: 480 },
      { file: "revs-3d_render-14_T2_rig_pinned", caption: "Test T2, one panel at quarter scale in its water rig", w: 720, h: 480 },
    ],
  },
  {
    id: "model",
    title: "3D model",
    blurb: "This is the CAD model of Rev S from September 2026, with all " + N.face_count.display + " panels and " + N.edges.display + " seams. The Rev D sizes are on the blueprints page. The 3D scene at the top of this page is built from this model.",
    items: [
      { file: "revs-clean-3d-01_shell_exterior", caption: "The whole shell, " + N.diameter.display + " across, with " + N.hex_count.display + " glass hexagons and " + N.pent_count.display + " solid pentagons", w: 720, h: 480 },
      { file: "revs-clean-3d-02_shell_cutaway", caption: "The shell cut in half, with the parts the cut goes through in orange", w: 720, h: 480 },
      { file: "revs-clean-2d-01_shell_elevation", caption: "The shell from the side", w: 720, h: 480 },
      { file: "revs-clean-2d-02_shell_plan_top", caption: "The shell from above", w: 720, h: 480 },
      { file: "revs-clean-3d-08_corner_node_outside", caption: "A corner where three panels meet, from outside", w: 720, h: 480 },
      { file: "revs-clean-3d-09_corner_node_inside", caption: "The same corner from inside", w: 720, h: 480 },
      { file: "revs-clean-3d-07_seam_closeup_cut", caption: "A piece of seam cut through a bolt, with two frames, two O-rings and a bead of sealant", w: 720, h: 480 },
    ],
  },
  {
    id: "panels",
    title: "Panels",
    blurb: "The panels are the building blocks of the station, and every panel connects the same way. The six-sided panels are the windows. The five-sided ones are solid and hold the solar panels and the fold-out shields.",
    items: [
      { file: "revs-clean-3d-03_hex_panel_cabin_side", caption: "One hexagon panel seen from the cabin side, with its edge frames, six ribs and glass panes. This is Rev S, and Rev D splits each bay into four.", w: 720, h: 480 },
      { file: "revs-clean-3d-04_hex_panel_exterior_side", caption: "The same panel from outside", w: 720, h: 480 },
      { file: "revs-clean-3d-05_pent_panel_cabin_side", caption: "One pentagon panel. It is solid, and so far the model shows only its frames, ribs and plate.", w: 720, h: 480 },
      { file: "revs-clean-2d-03_hex_panel_plan_exterior", caption: "A hexagon panel, seen flat from outside", w: 720, h: 480 },
      { file: "revs-clean-2d-05_pent_panel_plan_exterior", caption: "A pentagon panel, seen flat from outside", w: 720, h: 480 },
      { file: "revs-clean-2d-06_seam_section", caption: "The seam between two panels, cut through a bolt", w: 720, h: 480 },
    ],
  },
  {
    id: "prototype",
    title: "Physical model",
    blurb: "We built this scale model of the shell and the garden column by hand.",
    items: [
      { file: "images-prototype-photo-1", caption: "The scale model with the garden column inside", w: 540, h: 720 },
      { file: "images-prototype-photo-2", caption: "Light passing through the model", w: 540, h: 720 },
      { file: "images-prototype-photo-3", caption: "The model's clear panels and frame", w: 540, h: 720 },
    ],
  },
  {
    id: "sheets",
    title: "Earlier sheets",
    blurb: "These are our technical sheets from March 2026. Some numbers have changed since then, and the current drawings are in the Blueprints tab.",
    items: [
      { file: "blueprints-page-01", caption: "Project overview", w: 720, h: 402 },
      { file: "blueprints-page-02", caption: "Why a glass sphere instead of metal tubes", w: 720, h: 402 },
      { file: "blueprints-page-03", caption: "The shape and its main measurement", w: 720, h: 402 },
      { file: "blueprints-page-04", caption: "How hard the air pushes on each panel", w: 720, h: 402 },
      { file: "blueprints-page-05", caption: "The seven panel layers", w: 720, h: 402 },
      { file: "blueprints-page-06", caption: "How the panel joint keeps the air in", w: 720, h: 402 },
      { file: "blueprints-page-07", caption: "Three design options compared", w: 720, h: 402 },
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
