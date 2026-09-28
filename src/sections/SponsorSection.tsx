import { fundingUses, sponsorBenefits, waysToHelp, CONTACT_EMAIL } from "@content/data/sponsors";
import { EditorialSection, LinkRow, RuledList, SubHeading } from "./SectionHeader";

export function SponsorSection() {
  return (
    <EditorialSection
      id="sponsor"
      index="03"
      label="Sponsor the project"
      title="Help turn a design into hardware."
      intro="The design is drawn in full, down to every bolt. The next steps need real parts, real machining and real tests. That is where your support goes."
    >
      <div className="grid gap-x-14 gap-y-12 xl:grid-cols-2">
        <div>
          <SubHeading>What your support pays for</SubHeading>
          <RuledList items={fundingUses} columns={1} />
        </div>
        <div>
          <SubHeading>What you get</SubHeading>
          <RuledList items={sponsorBenefits} columns={1} />
        </div>
      </div>

      <div className="mt-16">
        <SubHeading>Ways to help</SubHeading>
        <RuledList items={waysToHelp} columns={4} />
      </div>

      <div className="mt-16">
        <LinkRow
          href="/plan/#need"
          title="The plan, and exactly what we need"
          body="Every part, material and size for the three tests, with the date we need it by."
        />
        <LinkRow
          href="/blueprints/"
          title="The blueprints"
          body="The shell, the panels, the joint, a corner and every test piece, each with dimensions and a plain explanation."
        />
      </div>

      <div id="contact-us" className="hcsa-contact" data-reveal>
        <h3 className="font-serif text-[clamp(1.6rem,2.8vw,2.2rem)] leading-tight text-white">Get in touch</h3>
        {CONTACT_EMAIL ? (
          <p className="mt-3 max-w-2xl text-lg leading-relaxed text-white/78">
            Email{" "}
            <a className="hcsa-textlink" href={`mailto:${CONTACT_EMAIL}`}>
              {CONTACT_EMAIL}
            </a>{" "}
            and we will reply with a short sponsor pack and a time to talk.
          </p>
        ) : (
          <p className="mt-3 max-w-2xl text-lg leading-relaxed text-white/78">
            Reach Manos Theofanous, project lead, through the Brown University School of Engineering.
            We will reply with a short sponsor pack and a time to talk.
          </p>
        )}
      </div>
    </EditorialSection>
  );
}
