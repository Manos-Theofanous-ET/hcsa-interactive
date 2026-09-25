/**
 * Sponsor-facing copy: what support pays for, what sponsors get, and how
 * to reach the team. Edit here, not in the components.
 */
import { NUMERICS as N } from "../numerics";

/** Public contact address shown in the "Get in touch" block. Leave empty
 *  to show the Brown University fallback line instead. */
export const CONTACT_EMAIL = "";

export const nowWorkingOn: string[] = [
  `Building a ${N.coupon_size.display} test piece of the panel joint and checking that it holds air under pressure.`,
  "Running computer stress tests on the panel for air pressure, docking and heat.",
  `Updating the life support plan for the full ${N.volume_enclosed.display} of the station.`,
];

export const fundingUses: { title: string; body: string }[] = [
  {
    title: "Test pieces",
    body: "Aluminium, glass, seals and bolts for full-size samples of the panel joint.",
  },
  {
    title: "Machining",
    body: "Precision cutting of frame parts so the test pieces match the design.",
  },
  {
    title: "Pressure testing",
    body: "Lab time to fill the test pieces with air and prove they do not leak or break.",
  },
  {
    title: "Next prototype",
    body: "A larger structural model of the shell, the step after the current tests.",
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
