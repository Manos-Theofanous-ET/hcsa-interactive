/**
 * Sponsor-facing copy: what support pays for, what sponsors get, and how
 * to reach the team. Edit here, not in the components.
 */
import { NUMERICS as N } from "../numerics";

/** Public contact address shown in the "Get in touch" block. Leave empty
 *  to show the Brown University fallback line instead. */
export const CONTACT_EMAIL = "";

export const nowWorkingOn: string[] = [
  "Testing the seam between two panels: full-size slices of the joint pulled apart in a load frame, and a " + N.coupon_size.display + " piece of it checked for air leaks.",
  "Sizing the corner node and the mid-seam hardpoint that the whole-shell stress model (9 to 12 Oct) showed carry the seam pull, so the November test pieces are the Rev D seam.",
  "Measuring how strong our glass really is, on borosilicate bars bent to breaking in a small load frame (spring 2027), then testing one panel at quarter scale, with " + N.panes_per_hex.display + " panes, under water pressure.",
];

export const fundingUses: { title: string; body: string }[] = [
  {
    title: "Joint test pieces",
    body: "Aluminium frames, steel pull blocks, bolts, O-rings and sealant for full-size slices of the seam between two panels.",
  },
  {
    title: "Machining",
    body: "CNC machining of eight joint frames and a quarter-scale panel, so the test pieces match the drawings.",
  },
  {
    title: "Glass for strength tests",
    body: "Borosilicate glass bars, 30 or more per edge finish, bent to breaking to measure how strong the glass really is and how much it scatters.",
  },
  {
    title: "A water pressure rig",
    body: "A steel tub and rings to load one panel at quarter scale up to twice normal air pressure.",
  },
];

export const sponsorBenefits: { title: string; body: string }[] = [
  {
    title: "Your name on the project",
    body: "Your name or logo on this website and in our talks and posters.",
  },
  {
    title: "Progress updates",
    body: "Photos, test results and short reports as each step is finished.",
  },
  {
    title: "Direct access",
    body: "Meet the student team and our faculty advisors, and see the hardware in person.",
  },
  {
    title: "Early look at talent",
    body: "Get to know Brown students working across engineering, architecture, biology and design.",
  },
];

export const waysToHelp: { title: string; body: string }[] = [
  { title: "Funding", body: "Pays for test pieces, machining and pressure tests." },
  { title: "Workshop time", body: "Machining, sealing and glass work on real parts." },
  { title: "Materials", body: "Aluminium, glass, gaskets and fasteners." },
  { title: "Expert advice", body: "Reviews from people who know structures, life support or human comfort." },
];
