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
  'We are a design and engineering research project at Brown University, with students from several fields. Brown supports us through its Undergraduate Teaching and Research Awards (UTRA) program, and our faculty advisors guide the work.'

export const leadership: TeamMember[] = [
  {
    name: 'Manos Theofanous',
    role: 'Project lead',
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
  { name: 'Marina Kouroumali', role: 'Head of interior' },
  { name: 'Androniki', role: 'Interior concept and physical models' },
  { name: 'Amalia', role: 'Interior CAD' },
  { name: 'Gerasimos Nikolopoulos', role: 'Life support, plants and biology' },
]

/** Members of the team before its September 2026 remake. Gerasimos was
 *  on it then and is on the current team too. */
export const earlierMembers: TeamMember[] = [
  { name: 'Katie Liu', role: 'Structure and FEA' },
  { name: 'Lauren Hogan', role: 'Thermal and the water loop' },
  { name: 'Skye Rosario', role: 'Thermal and life support' },
  { name: 'Gerasimos Nikolopoulos', role: 'Plants and biology' },
  { name: 'Aris Achilleoudis', role: 'Design, shutters and interior' },
  { name: 'Xenia Tzamalouka', role: 'Design, the moon-phase shutters' },
  { name: 'Nefeli Moraitini', role: 'Design' },
  { name: 'Katerina Sofianou', role: 'Design and marketing' },
  { name: 'Keren Dial', role: 'Design and outreach' },
  { name: 'Estella', role: 'Research team' },
  { name: 'Marco Cross, PhD', role: 'Fabrication advisor' },
]
