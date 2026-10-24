/**
 * Sponsor-facing copy: what support pays for, what sponsors get, and how
 * to reach the team. Edit here, not in the components.
 */
import { NUMERICS as N } from "../numerics";

/** Public contact address shown in the "Get in touch" block. Leave empty
 *  to show the Brown University fallback line instead. */
export const CONTACT_EMAIL = "";

export const nowWorkingOn: string[] = [
  "Building the seam test pieces this fall: full-size slices of the joint between two panels, and a " + N.coupon_size.display + " piece of it for air leaks. Drawings are released on " + N.drawing_release.display + ". The slices are pulled apart in a " + N.t1_frame_capacity.display + " load frame at Brown in January and February 2027, with a " + N.daq_channels.display + " strain recorder on loan from Dewesoft.",
  "Sizing the corner node and the mid-seam hardpoint that the whole-shell stress model (9 to 12 Oct) showed carry the seam pull, so the test pieces are the Rev D seam.",
  "Measuring how strong our glass really is, on borosilicate bars " + N.t0_bar_width_in.display + " wide and " + N.t0_bar_thickness_in.display + " thick, bent to breaking the way ENGN 1440 does it (spring 2027). That number picks the final pane size. Then one panel at quarter scale under water pressure.",
  "Every physical test runs on the computer first. Nothing is machined before its digital twin has a signed sheet.",
];

export const fundingUses: { title: string; body: string }[] = [
  {
    title: "Joint test pieces",
    body: "Aluminium frames, steel pull blocks, bolts, butyl seals and sealant for full-size slices of the seam between two panels.",
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

/** Companies that have given parts, loans, discounts, advice or software so
 *  far (Oct 2026). `kind` is shown as the label so a loan or a discount is
 *  never read as a gift. `href` is the company's main site only; MEPLA Pro's
 *  link is a condition of the student licence. Loans and discounts stay here
 *  while they run. */
export type Supporter = {
  name: string;
  kind: "Donation" | "Offer" | "Loan" | "Discount" | "Advice" | "Software licence";
  body: string;
  href?: string;
};

export const supporters: Supporter[] = [
  { name: "SCHOTT North America", kind: "Donation", body: N.borofloat_discs_received.display + " BOROFLOAT 33 glass discs for the glass tests, received 13 Oct 2026.", href: "https://www.schott.com" },
  { name: "Meller Optics", kind: "Donation", body: N.sapphire_discs_received.display + " sapphire discs for the glass tests, received 13 Oct 2026.", href: "https://www.melleroptics.com" },
  { name: "Precision Glass & Optics", kind: "Offer", body: "30 to 40 Borofloat discs offered for the glass tests.", href: "https://www.pgo.com" },
  { name: "Bolt Depot", kind: "Donation", body: "Bolts for the test pieces and rigs.", href: "https://www.boltdepot.com" },
  { name: "MEPLA Pro", kind: "Software licence", body: "A student licence of SJ MEPLA, the structural glass analysis program, for the pane calculations.", href: "https://www.mepla.net" },
  { name: "Dewesoft", kind: "Loan", body: "A " + N.daq_channels.display + " strain recorder and its software, lent in 3 to 4 week batches for the tests. Agreed in principle.", href: "https://dewesoft.com" },
  { name: "OSH Cut", kind: "Discount", body: "Half price on laser-cut parts until 31 Dec 2026.", href: "https://www.oshcut.com" },
  { name: "PCBWay", kind: "Discount", body: "Half price on CNC machining, 3D printing and circuit boards under the Future Innovators Program, capped at $2,000 for the project.", href: "https://www.pcbway.com" },
  // Heintges (Advice, "A glazing review of the pane and its seat.", https://www.heintges.com):
  // held off the public list until Dan Vos confirms the credit wording (open question Q74, 23 Oct 2026).
  { name: "Parker", kind: "Advice", body: "Seal advice: butyl BA500 loops in place of fluorosilicone cord.", href: "https://www.parker.com" },
];

export const waysToHelp: { title: string; body: string }[] = [
  { title: "Funding", body: "Pays for test pieces, machining and pressure tests." },
  { title: "Workshop time", body: "Machining, sealing and glass work on real parts." },
  { title: "Materials", body: "Aluminium, glass, gaskets and fasteners." },
  { title: "Expert advice", body: "Reviews from people who know structures, life support or human comfort." },
];
