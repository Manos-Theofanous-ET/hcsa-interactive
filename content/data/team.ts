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
  { name: 'Finn', role: 'Panels and glazing' },
  { name: 'Marina', role: 'Head of interior' },
  { name: 'Androniki', role: 'Interior concept and physical models' },
  { name: 'Amalia', role: 'Interior CAD' },
]

/** Members of the team before its September 2026 remake, credited on the concept work. */
export const earlierTeam =
  'Katie, Keren, Jake, Aris, Katerina, Xenia, Nefeli, Gerasimos, Skye, Lauren, Padelis and Marco Cross, PhD'
