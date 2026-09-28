import { fundingUses, sponsorBenefits, waysToHelp, CONTACT_EMAIL } from "@content/data/sponsors";
import { SectionHeader } from "./SectionHeader";

function CardList({ items }: { items: { title: string; body: string }[] }) {
  return (
    <ul className="grid gap-4 sm:grid-cols-2">
      {items.map((it) => (
        <li key={it.title} className="rounded-sm border border-white/10 bg-white/[0.03] p-5">
          <h4 className="mb-2 font-serif text-xl text-white">{it.title}</h4>
          <p className="text-base leading-relaxed text-white/70">{it.body}</p>
        </li>
      ))}
    </ul>
  );
}

export function SponsorSection() {
  return (
    <section id="sponsor" aria-labelledby="sponsor-title" className="hcsa-section">
      <SectionHeader
        id="sponsor"
        eyebrow="Sponsor us"
        title="Help turn a design into hardware."
        intro="The design is drawn in full, down to every bolt. The next steps need real parts, real machining and real tests. That is where your support goes."
      />

      <div className="grid gap-14 lg:grid-cols-2">
        <div>
          <h3 className="data mb-5 text-[11px] uppercase tracking-[0.25em] text-white/60">
            What your support pays for
          </h3>
          <CardList items={fundingUses} />
        </div>
        <div>
          <h3 className="data mb-5 text-[11px] uppercase tracking-[0.25em] text-white/60">
            What you get
          </h3>
          <CardList items={sponsorBenefits} />
        </div>
      </div>

      <div className="mt-14">
        <h3 className="data mb-5 text-[11px] uppercase tracking-[0.25em] text-white/60">Ways to help</h3>
        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {waysToHelp.map((w) => (
            <li key={w.title} className="border-t border-[color:var(--color-accent-cyan)]/50 pt-4">
              <h4 className="font-serif text-lg text-white">{w.title}</h4>
              <p className="mt-1 text-sm leading-relaxed text-white/65">{w.body}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-16 grid gap-6 md:grid-cols-2">
        <a href="/plan/#need" className="block rounded-sm border border-white/15 bg-white/[0.03] p-6 hover:border-[color:var(--color-accent-cyan)]">
          <p className="data mb-2 text-[11px] uppercase tracking-[0.25em] text-[color:var(--color-accent-cyan)]">The plan</p>
          <h3 className="font-serif text-2xl text-white">What we are building this fall, and exactly what we need</h3>
          <p className="mt-2 text-base text-white/70">Every part, material and size for the three tests, with the date we need it by.</p>
        </a>
        <a href="/blueprints/" className="block rounded-sm border border-white/15 bg-white/[0.03] p-6 hover:border-[color:var(--color-accent-cyan)]">
          <p className="data mb-2 text-[11px] uppercase tracking-[0.25em] text-[color:var(--color-accent-cyan)]">The blueprints</p>
          <h3 className="font-serif text-2xl text-white">Every drawing, with dimensions</h3>
          <p className="mt-2 text-base text-white/70">The shell, the panels, the joint, a corner and every test piece, each explained in plain words.</p>
        </a>
      </div>

      <div id="contact-us" className="mt-16 rounded-sm border border-[color:var(--color-accent-cyan)]/40 bg-[color:var(--color-accent-cyan)]/[0.05] p-8">
        <h3 className="font-serif text-2xl text-white">Get in touch</h3>
        {CONTACT_EMAIL ? (
          <p className="mt-3 text-lg text-white/80">
            Email{" "}
            <a className="text-[color:var(--color-accent-cyan)] underline underline-offset-4" href={`mailto:${CONTACT_EMAIL}`}>
              {CONTACT_EMAIL}
            </a>{" "}
            and we will reply with a short sponsor pack and a time to talk.
          </p>
        ) : (
          <p className="mt-3 text-lg text-white/80">
            Reach Manos Theofanous, project lead, through the Brown University School of Engineering.
            We will reply with a short sponsor pack and a time to talk.
          </p>
        )}
      </div>
    </section>
  );
}
