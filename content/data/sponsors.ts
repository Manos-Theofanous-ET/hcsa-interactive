/**
 * Sponsor-facing copy: what support pays for, what sponsors get, and how
 * to reach the team. Edit here, not in the components.
 */
import { NUMERICS as N } from "../numerics";

/** Public contact address shown in the "Get in touch" block. Leave empty
 *  to show the Brown University fallback line instead. */
export const CONTACT_EMAIL = "";

export const nowWorkingOn: string[] = [
  "This fall we are building the seam test pieces. They are full-size slices of the joint between two panels, plus a " + N.coupon_size.display + " length of it to check for air leaks. The drawings come out on " + N.drawing_release.display + ". In late January and February 2027 we pull the slices apart in a " + N.t1_frame_capacity.display + " load frame at Brown, with a " + N.daq_channels.display + " strain recorder on loan from Dewesoft.",
  "We are sizing the corner node and the hardpoint in the middle of each seam. The stress model of the whole shell, run from 9 to 12 October, showed that these two parts carry the pull across the seam. So our test pieces copy the Rev D seam.",
  "In spring 2027 we measure how strong our glass really is. We bend borosilicate bars, " + N.t0_bar_width_in.display + " wide and " + N.t0_bar_thickness_in.display + " thick, until they break, the way the ENGN 1440 class does it. That result picks the final pane size. After that we test one panel at quarter scale under water pressure.",
  "Every physical test runs on the computer first. Nothing is machined until its digital twin, the computer model of that test, has a signed test sheet.",
];

export const fundingUses: { title: string; body: string }[] = [
  {
    title: "Joint test pieces",
    body: "This buys the aluminium frames, steel pull blocks, bolts, butyl seals and sealant for full-size slices of the seam between two panels.",
  },
  {
    title: "Machining",
    body: "This pays a shop to machine eight joint frames and a quarter-scale panel on CNC machines, so the test pieces match the drawings.",
  },
  {
    title: "Glass for strength tests",
    body: "We bend borosilicate glass bars until they break, 30 or more for each edge finish. That tells us how strong the glass really is and how much its strength varies.",
  },
  {
    title: "A water pressure rig",
    body: "A steel tub and rings let us load one panel at quarter scale with water, up to twice normal air pressure.",
  },
];

export const sponsorBenefits: { title: string; body: string }[] = [
  {
    title: "Your name on the project",
    body: "We show your name or logo on this website and in our talks and posters.",
  },
  {
    title: "Progress updates",
    body: "We send you photos, test results and short reports as each step is finished.",
  },
  {
    title: "Direct access",
    body: "You can meet the student team and our faculty advisors, and see the hardware in person.",
  },
  {
    title: "Early look at talent",
    body: "You get to know Brown students who work in engineering, architecture, biology and design.",
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
  { name: "SCHOTT North America", kind: "Donation", body: "They gave us " + N.borofloat_discs_received.display + " BOROFLOAT 33 glass discs for the glass tests. The discs arrived on 13 October 2026.", href: "https://www.schott.com" },
  { name: "Meller Optics", kind: "Donation", body: "They gave us " + N.sapphire_discs_received.display + " sapphire discs for the glass tests. The discs arrived on 13 October 2026.", href: "https://www.melleroptics.com" },
  { name: "Precision Glass & Optics", kind: "Offer", body: "They offered 30 to 40 Borofloat discs for the glass tests.", href: "https://www.pgo.com" },
  { name: "Bolt Depot", kind: "Donation", body: "They gave us bolts for the test pieces and rigs.", href: "https://www.boltdepot.com" },
  { name: "MEPLA Pro", kind: "Software licence", body: "They gave us a student licence of SJ MEPLA, a program that analyses structural glass. We use it for the pane calculations.", href: "https://www.mepla.net" },
  { name: "Dewesoft", kind: "Loan", body: "They will lend us a " + N.daq_channels.display + " strain recorder and its software for the tests, in batches of 3 to 4 weeks. They have agreed to this in principle.", href: "https://dewesoft.com" },
  { name: "OSH Cut", kind: "Discount", body: "They give us half price on laser-cut parts until 31 December 2026.", href: "https://www.oshcut.com" },
  { name: "PCBWay", kind: "Discount", body: "Under their Future Innovators Program, they give us half price on CNC machining, 3D printing and circuit boards, up to $2,000 for the project.", href: "https://www.pcbway.com" },
  // Heintges (Advice, "A glazing review of the pane and its seat.", https://www.heintges.com):
  // held off the public list until Dan Vos confirms the credit wording (open question Q74, 23 Oct 2026).
  { name: "Parker", kind: "Advice", body: "They advised us to seal the joints with loops of butyl BA500 in place of fluorosilicone cord.", href: "https://www.parker.com" },
];

export const waysToHelp: { title: string; body: string }[] = [
  { title: "Funding", body: "It pays for test pieces, machining and pressure tests." },
  { title: "Workshop time", body: "Your shop can machine, seal and work glass on real parts." },
  { title: "Materials", body: "We need aluminium, glass, gaskets and fasteners." },
  { title: "Expert advice", body: "We want reviews from people who know structures, life support or human comfort." },
];
