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
export type GalleryCategory = {
  id: string;
  title: string;
  blurb: string;
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
    title: "Concept art",
    blurb: "What life inside the station could look and feel like.",
    items: [
      { file: "images-concept-exterior", caption: "The station in orbit, filled with gardens", w: 480, h: 720 },
      { file: "prototype-whatsapp-image-2026-04-03-at-3-17-43-pm", caption: "People floating, climbing and cycling inside", w: 720, h: 720 },
      { file: "prototype-whatsapp-image-2026-04-03-at-3-18-17-pm", caption: "The ring track and garden column above Earth", w: 691, h: 720 },
      { file: "images-concept-observatory", caption: "Walkways and gardens under a glass sky", w: 480, h: 720 },
      { file: "images-concept-plants", caption: "Terraced gardens along the inner wall", w: 583, h: 720 },
      { file: "images-concept-interior", caption: "A quiet garden corner at night", w: 720, h: 720 },
      { file: "images-facility-render-day", caption: "Garden column, ramp and seating pods", w: 720, h: 480 },
      { file: "images-facility-render-night", caption: "The same layout at night", w: 720, h: 480 },
      { file: "images-facility-annotated-dimensions", caption: "Early sketch with the sizes of the ramp and pods", w: 720, h: 473 },
    ],
  },
  {
    id: "model",
    title: "3D model",
    blurb: "The engineering model the scroll story above is built from.",
    items: [
      { file: "images-hcsa_buckyball_revg_outreach_web", caption: "The full shell: 20 six-sided and 12 five-sided panels", w: 720, h: 720 },
      { file: "images-hcsa_exterior_technical_nominal", caption: "Outside view of the frame and window panels", w: 720, h: 477 },
      { file: "images-hcsa_exploded_assembly_technical", caption: "The shell with one panel lifted out", w: 720, h: 468 },
      { file: "images-hcsa_interior_facility_reva_hero", caption: "Cut-away showing the layout inside", w: 720, h: 720 },
      { file: "images-hcsa_interior_revd_hero", caption: "The inside structure seen through the panels", w: 720, h: 720 },
      { file: "images-hcsa_interior_view_orbit", caption: "Looking along the central column", w: 720, h: 455 },
      { file: "images-diagram_of_assembly", caption: "The shell unfolded flat", w: 624, h: 610 },
    ],
  },
  {
    id: "panels",
    title: "Window panels",
    blurb: "The building block of the station. Every panel connects the same way.",
    items: [
      { file: "images-hcsa_single_hex_panel_revg_outreach_web", caption: "One six-sided panel", w: 720, h: 720 },
      { file: "images-hcsa_single_pent_panel_revg_outreach_web", caption: "One five-sided panel", w: 720, h: 720 },
      { file: "images-hcsa_single_hex_panel_exploded", caption: "Six-sided panel with its layers pulled apart", w: 720, h: 480 },
      { file: "images-hcsa_single_hex_panel_top_orthographic", caption: "Six-sided panel seen from above", w: 720, h: 720 },
      { file: "images-hcsa_single_hex_panel_section", caption: "A slice through the panel edge", w: 720, h: 480 },
      { file: "images-hcsa_panel_closeup_realistic", caption: "Close-up of the joint between two panels", w: 720, h: 520 },
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
    title: "Engineering sheets",
    blurb: "Our detailed technical sheets, for readers who want the full numbers.",
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
