import { collaborators, earlierMembers, outreachSupport, facultyAdvisors, leadership, projectAffiliation } from "@content/data/team";
import { EditorialSection, RuledList, SubHeading } from "./SectionHeader";

export function TeamSection() {
  const leads = [...leadership, ...facultyAdvisors].map((m) => ({
    title: m.name,
    meta: m.role,
    body: m.focus,
  }));
  const team = collaborators.map((m) => ({ title: m.name, meta: m.role }));
  const outreach = outreachSupport.map((m) => ({ title: m.name, meta: m.role }));
  const earlier = earlierMembers.map((m) => ({ title: m.name, meta: m.role }));
  return (
    <EditorialSection id="team" index="04" label="The team" title="Who is building it." intro={projectAffiliation}>
      <RuledList items={leads} columns={2} />
      <div className="mt-12">
        <SubHeading>Team</SubHeading>
        <RuledList items={team} columns={2} />
      </div>
      <div className="mt-12">
        <SubHeading>Marketing and outreach support</SubHeading>
        <RuledList items={outreach} columns={2} />
      </div>
      <div className="mt-12">
        <SubHeading>Earlier members</SubHeading>
        <RuledList items={earlier} columns={2} />
      </div>
      <p className="mt-10 max-w-3xl text-sm leading-relaxed text-white/82" data-reveal>
        These people were on the team before we remade it in September 2026. The interior concept is Marina’s. The plants are Marina’s and Manos’s idea, and Gerasimos is in charge of the plant system. The moon-phase shutters were Xenia’s idea.
      </p>
    </EditorialSection>
  );
}
