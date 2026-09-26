import { NUMERICS as N } from "@content/numerics";
import { nowWorkingOn } from "@content/data/sponsors";
import { SectionHeader } from "./SectionHeader";

export function AboutSection() {
  return (
    <section id="about" aria-labelledby="about-title" className="hcsa-section">
      <SectionHeader
        id="about"
        eyebrow="About the project"
        title="A space station designed around the people who visit it."
      />
      <div className="grid gap-12 md:grid-cols-[1.4fr_1fr]">
        <div className="space-y-5 text-lg leading-relaxed text-white/80">
          <p>
            Most space stations are rows of metal tubes with a few small windows. Human-Centric Space
            Architecture (HCSA) is a round station whose walls are mostly windows, so the people inside
            can always see Earth and the stars.
          </p>
          <p>
            It is a multi-use facility for short-stay visits. There are no sleeping quarters. Instead,
            the station is one open room for watching Earth, moving freely, relaxing among living plants,
            gatherings and research. Because it is made from {N.face_count.display} panels that all connect the same way, it
            can be built in factories on Earth, launched in pieces and put together in orbit.
          </p>
          <p>
            We are a student team at Brown University, supported by Brown's UTRA research program and
            our faculty advisors. We are on step {N.roadmap_current.display} of {N.roadmap_total.display}:
            building and testing a real piece of the panel joint.
          </p>
        </div>
        <div className="rounded-sm border border-white/10 bg-white/[0.03] p-6">
          <h3 className="data mb-4 text-[11px] uppercase tracking-[0.25em] text-white/60">
            What we are working on now
          </h3>
          <ul className="space-y-4 text-base leading-relaxed text-white/80">
            {nowWorkingOn.map((item) => (
              <li key={item} className="flex gap-3">
                <span aria-hidden className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[color:var(--color-accent-cyan)]" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
