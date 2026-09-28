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
        Previous work from {earlierTeam}, credited on the concept art and models.
      </p>
    </EditorialSection>
  );
}
