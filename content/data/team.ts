/**
 * Team roster, Brown University, UTRA (source: project role tables).
 */
export type TeamMember = {
  name: string
  role: string
  /** Optional secondary line */
  focus?: string
}

export const projectAffiliation =
  'We are a design and engineering research project at Brown University, with students from Brown, the Rhode Island School of Design, the Moraitis School in Athens, where Marina Kouroumali leads our group, and the University of Patras. Brown supports us through its Undergraduate Teaching and Research Awards (UTRA) program, and our faculty advisors guide the work.'

export const leadership: TeamMember[] = [
  {
    name: 'Manos Theofanous',
    role: 'Project lead · Presenter, Brown Space Horizons 2026',
    focus: 'Leads the structure and materials work, brings the whole design together and is the lead author',
  },
]

export const facultyAdvisors: TeamMember[] = [
  {
    name: 'Rick Fleeter, PhD',
    role: 'Faculty advisor',
  },
]

export const collaborators: TeamMember[] = [
  { name: 'Marina Kouroumali', role: 'Head of interior · Presenter, Brown Space Horizons 2026' },
  { name: 'Gerasimos Nikolopoulos', role: 'Life support, plants and biology' },
  { name: 'Xenia Tzamalouka', role: 'Interior and shutters · Presenter, Brown Space Horizons 2026' },
  { name: 'Aris Achilleoudis', role: 'Design, shutters and interior · Presenter, Brown Space Horizons 2026' },
  { name: 'Androniki Sarra', role: 'Interior concept and physical models' },
  { name: 'Amalia', role: 'Interior CAD' },
]

/** General marketing and outreach support. */
export const outreachSupport: TeamMember[] = [
  { name: 'Estella', role: 'Marketing and outreach' },
  { name: 'Katerina Sofianou', role: 'Marketing and outreach' },
  { name: 'Nefeli Moraitini', role: 'Marketing and outreach' },
]

/** Members of the team before its September 2026 remake. */
export const earlierMembers: TeamMember[] = [
  { name: 'Katie Liu', role: 'Structure and FEA' },
  { name: 'Keren Dial', role: 'Design and outreach' },
  { name: 'Lauren Hogan', role: 'Thermal and the water loop' },
  { name: 'Marco Cross, PhD', role: 'Fabrication advisor' },
  { name: 'Skye Rosario', role: 'Thermal and life support · Presenter, Brown Space Horizons 2026' },
]
