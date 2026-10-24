/**
 * Team roster — Brown University · UTRA (source: project role tables).
 */
export type TeamMember = {
  name: string
  role: string
  /** Optional secondary line */
  focus?: string
}

export const projectAffiliation =
  'An interdisciplinary design and engineering research initiative at Brown University, supported through the Undergraduate Teaching and Research Awards (UTRA) program and faculty mentorship.'

export const leadership: TeamMember[] = [
  {
    name: 'Manos Theofanous',
    role: 'Project lead',
    focus: 'Structure and materials, brings the whole design together, lead author',
  },
]

export const facultyAdvisors: TeamMember[] = [
  {
    name: 'Rick Fleeter, PhD',
    role: 'Faculty advisor',
  },
]

export const collaborators: TeamMember[] = [
  { name: 'Finn Jolly', role: 'Panels and glazing' },
  { name: 'Marina Kouroumali', role: 'Head of interior' },
  { name: 'Androniki', role: 'Interior concept and physical models' },
  { name: 'Amalia', role: 'Interior CAD' },
  { name: 'Skye', role: 'Thermal and life support' },
  { name: 'Gerasimos Nikolopoulos', role: 'Life support, plants and biology' },
]

/** Members of the team before its September 2026 remake. Gerasimos and
 *  Skye were on it then and are on the current team too. */
export const earlierTeam =
  'Katie, Keren, Jake, Aris, Katerina, Xenia, Nefeli, Lauren, Padelis and Marco Cross, PhD'
