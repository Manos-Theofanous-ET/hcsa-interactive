import { collaborators, earlierTeam, facultyAdvisors, leadership, projectAffiliation } from "@content/data/team";
import { SectionHeader } from "./SectionHeader";

export function TeamSection() {
  const leads = [...leadership, ...facultyAdvisors];
  return (
    <section id="team" aria-labelledby="team-title" className="hcsa-section">
      <SectionHeader id="team" eyebrow="The team" title="Who is building it." intro={projectAffiliation} />
      <ul className="mb-12 grid gap-4 sm:grid-cols-3">
        {leads.map((m) => (
          <li key={m.name} className="rounded-sm border border-white/10 bg-white/[0.03] p-5">
            <p className="font-serif text-xl text-white">{m.name}</p>
            <p className="data mt-1 text-[11px] uppercase tracking-[0.2em] text-[color:var(--color-accent-cyan)]">
              {m.role}
            </p>
            {m.focus ? <p className="mt-2 text-sm text-white/65">{m.focus}</p> : null}
          </li>
        ))}
      </ul>
      <ul className="grid gap-x-8 gap-y-4 sm:grid-cols-2 lg:grid-cols-3">
        {collaborators.map((m) => (
          <li key={m.name} className="border-t border-white/10 pt-3">
            <p className="text-lg text-white">{m.name}</p>
            <p className="text-sm text-white/60">{m.role}</p>
          </li>
        ))}
      </ul>
      <p className="mt-10 max-w-3xl text-sm leading-relaxed text-white/50">
        Earlier team members, credited on the concept art and models: {earlierTeam}.
      </p>
    </section>
  );
}
