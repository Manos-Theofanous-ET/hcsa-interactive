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
    focus: 'Brings the whole design together, panel design, lead author',
  },
]

export const facultyAdvisors: TeamMember[] = [
  {
    name: 'Rick Fleeter, PhD',
    role: 'Head faculty advisor',
  },
  {
    name: 'Marco Cross, PhD',
    role: 'Fabrication / prototyping advisor',
  },
]

export const collaborators: TeamMember[] = [
  { name: 'Katie', role: 'Strength checks, materials, docking and shading' },
  { name: 'Marina', role: 'Concept development, visuals lead and interior layout' },
  { name: 'Keren', role: 'Architectural concept model and layout visuals' },
  { name: 'Jake', role: 'Fabrication lead' },
  { name: 'Aris', role: '3D model and interior layout visuals' },
  { name: 'Katerina', role: 'Funding and outreach' },
  { name: 'Xenia', role: '3D model and interior layout visuals' },
  { name: 'Nefeli', role: 'Paper scale model and interior layout visuals' },
  { name: 'Gerasimos', role: 'Life support and plant life' },
  { name: 'Skye', role: 'Life support and plant life' },
  { name: 'Lauren', role: 'Life support and water treatment' },
  { name: 'Padelis', role: 'VR interior environment' },
]
