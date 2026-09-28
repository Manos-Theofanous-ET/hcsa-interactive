import { DOWNLOADS, DRAWING_PREVIEW, ON_REQUEST, drawingThumb } from "@content/data/downloads";
import { RuledList, SubHeading } from "./SectionHeader";

/** A look at the blueprints before the gallery tabs, so a sponsor sees
 *  what exists, what they can download now and what they can ask for.
 *  Clicking a drawing opens it in the gallery's viewer. */
export function BlueprintPreview({ onOpen }: { onOpen: (index: number) => void }) {
  return (
    <div className="hcsa-bp">
      <h3 id="bp-preview-title" className="font-serif text-[clamp(1.45rem,2.4vw,1.9rem)] leading-tight text-white" data-reveal>
        Blueprints you can download or ask for
      </h3>
      <p className="mt-3 max-w-2xl text-base leading-relaxed text-white/65" data-reveal>
        Drawn from the CAD model (Rev S, September 2026), with dimensions in millimetres. Click a drawing to see it full size.
      </p>

      <ul className="mt-8 grid grid-cols-2 gap-x-4 gap-y-6 lg:grid-cols-3">
        {DRAWING_PREVIEW.map((d, i) => (
          <li key={d.name} data-reveal>
            <button type="button" onClick={() => onOpen(i)} className="hcsa-bp-thumb group">
              <img
                src={drawingThumb(d.name)}
                alt=""
                width={d.w}
                height={d.h}
                loading="lazy"
                decoding="async"
                className="h-auto w-full"
              />
              <span className="mt-2 block text-sm leading-snug text-white/70">{d.caption}</span>
            </button>
          </li>
        ))}
      </ul>

      <div className="mt-12 grid gap-x-14 gap-y-10 lg:grid-cols-[1.4fr_1fr]">
        <div>
          <SubHeading>Download now</SubHeading>
          <ul className="hcsa-files">
            {DOWNLOADS.map((f) => (
              <li key={f.title} data-reveal>
                <a href={f.href} className="hcsa-file">
                  <span className="min-w-0">
                    <span className="hcsa-file-title">{f.title}</span>
                    <span className="hcsa-file-meta">{f.meta}</span>
                    <span className="mt-1 block text-[0.98rem] leading-relaxed text-white/68">{f.body}</span>
                  </span>
                  <span className="hcsa-file-action">
                    {f.action} <span aria-hidden="true">→</span>
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <SubHeading>Ask us for</SubHeading>
          <RuledList items={ON_REQUEST} columns={1} />
          <p className="mt-6" data-reveal>
            <a href="#contact-us" className="hcsa-textlink">
              How to reach us <span aria-hidden="true">→</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
