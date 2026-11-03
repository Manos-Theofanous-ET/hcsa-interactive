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
  { name: 'Amalia', role: 'Interior CAD' },
  { name: 'Androniki', role: 'Interior concept and physical models' },
  { name: 'Gerasimos Nikolopoulos', role: 'Life support, plants and biology' },
  { name: 'Marina Kouroumali', role: 'Head of interior · Presenter, Brown Space Horizons 2026' },
  { name: 'Xenia Tzamalouka', role: 'Interior and shutters · Presenter, Brown Space Horizons 2026' },
]

/** Members of the team before its September 2026 remake. */
export const earlierMembers: TeamMember[] = [
  { name: 'Aris Achilleoudis', role: 'Design, shutters and interior · Presenter, Brown Space Horizons 2026' },
  { name: 'Estella', role: 'Research team' },
  { name: 'Katerina Sofianou', role: 'Design and marketing' },
  { name: 'Katie Liu', role: 'Structure and FEA' },
  { name: 'Keren Dial', role: 'Design and outreach' },
  { name: 'Lauren Hogan', role: 'Thermal and the water loop' },
  { name: 'Marco Cross, PhD', role: 'Fabrication advisor' },
  { name: 'Nefeli Moraitini', role: 'Design' },
  { name: 'Skye Rosario', role: 'Thermal and life support · Presenter, Brown Space Horizons 2026' },
]
