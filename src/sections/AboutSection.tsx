import { NUMERICS as N } from "@content/numerics";
import { nowWorkingOn } from "@content/data/sponsors";
import { ArrowIcon, EditorialSection, SubHeading } from "./SectionHeader";

export function AboutSection() {
  return (
    <EditorialSection
      id="about"
      index="01"
      label="About the project"
      title="A space station designed around the people who visit it."
    >
      <div className="grid gap-14 lg:grid-cols-[1.35fr_1fr]">
        <div className="space-y-5 text-lg leading-relaxed text-white/80" data-reveal>
          <p>
            Most space stations are rows of metal tubes with a few small windows. Human-Centric Space
            Architecture (HCSA) is a round station whose walls are mostly windows, so the people inside
            can always see Earth and the stars.
          </p>
          <p>
            It is a facility with many uses, built for short visits, and it has no sleeping quarters.
            The station is one open room where people watch Earth, move freely, relax among living plants,
            meet and do research. It is made from {N.face_count.display} panels that all connect the same way.
            That means it can be built in factories on Earth, launched in pieces and put together in orbit.
          </p>
          <p>
            We are a student team at Brown University, supported by Brown's UTRA research program and by
            our faculty advisors. We are on step {N.roadmap_current.display} of {N.roadmap_total.display}.
            A stress model of the whole shell set the sizes in Rev D, the version of our design that we
            signed on 14 October 2026. Now we are building the seam between two panels at full size, so we
            can test it on real hardware.
          </p>
        </div>
        <div data-reveal>
          <SubHeading>What we are working on now</SubHeading>
          <ol className="hcsa-numbered">
            {nowWorkingOn.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ol>
          <p className="mt-8 flex flex-wrap gap-x-8 gap-y-3">
            <a href="/plan/" className="hcsa-textlink">
              The fall plan <span aria-hidden><ArrowIcon /></span>
            </a>
            <a href="/blueprints/" className="hcsa-textlink">
              The blueprints <span aria-hidden><ArrowIcon /></span>
            </a>
          </p>
        </div>
      </div>
    </EditorialSection>
  );
}
