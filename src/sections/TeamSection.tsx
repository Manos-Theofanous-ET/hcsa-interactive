import { collaborators, earlierTeam, facultyAdvisors, leadership, projectAffiliation } from "@content/data/team";
import { EditorialSection, RuledList, SubHeading } from "./SectionHeader";

export function TeamSection() {
  const leads = [...leadership, ...facultyAdvisors].map((m) => ({
    title: m.name,
    meta: m.role,
    body: m.focus,
  }));
  const team = collaborators.map((m) => ({ title: m.name, meta: m.role }));
  return (
    <EditorialSection id="team" index="04" label="The team" title="Who is building it." intro={projectAffiliation}>
      <RuledList items={leads} columns={2} />
      <div className="mt-12">
        <SubHeading>Team</SubHeading>
        <RuledList items={team} columns={2} />
      </div>
      <p className="mt-10 max-w-3xl text-sm leading-relaxed text-white/55" data-reveal>
        Earlier team members, before the September 2026 remake: {earlierTeam}. The interior concept is Marina’s; the plants are Marina’s and Manos’s idea, with Gerasimos in charge of the plant system; the moon-phase shutters were Xenia’s idea.
      </p>
    </EditorialSection>
  );
}
