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
  'We are a design and engineering research project at Brown University. The lead researcher, Manos Theofanous, is a student at Brown University and the Rhode Island School of Design. The head designer is Marina Kouroumali, Head of Visual Arts, IB, at the Moraitis School in Athens, Greece. The project supervisor is Professor Rick Fleeter of Brown University. The rest of the group is made up of students from Brown University and the University of Patras, and IB Visual Arts students in Greece. Brown supports us through its Undergraduate Teaching and Research Awards (UTRA) program.'

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
  { name: 'Marina Kouroumali', role: 'Head designer · Head of Visual Arts, IB, Moraitis School, Athens · Presenter, Brown Space Horizons 2026' },
  { name: 'Gerasimos Nikolopoulos', role: 'Life support, plants and biology' },
  { name: 'Xenia Tzamalouka', role: 'Interior and shutters · Presenter, Brown Space Horizons 2026' },
  { name: 'Aris Achilleoudis', role: 'Design, shutters and interior · Presenter, Brown Space Horizons 2026' },
  { name: 'Androniki Sarra', role: 'Interior concept and physical models' },
  { name: 'Amalia', role: 'Interior CAD' },
  { name: 'Nefeli Moraitini', role: 'Design' },
]

/** General marketing and outreach support. */
export const outreachSupport: TeamMember[] = [
  { name: 'Estella', role: 'Marketing and outreach' },
  { name: 'Katerina Sofianou', role: 'Marketing and outreach' },
]

/** Members of the team before its September 2026 remake. */
export const earlierMembers: TeamMember[] = [
  { name: 'Katie Liu', role: 'Structure and FEA' },
  { name: 'Keren Dial', role: 'Design and outreach' },
  { name: 'Lauren Hogan', role: 'Thermal and the water loop' },
  { name: 'Marco Cross', role: 'Fabrication advisor' },
  { name: 'Skye Rosario', role: 'Thermal and life support · Presenter, Brown Space Horizons 2026' },
]
