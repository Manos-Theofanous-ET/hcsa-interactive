import type { ReactNode } from "react";

type SectionProps = {
  id: string;
  /** Two-digit section number shown in the margin, e.g. "01". */
  index: string;
  /** Short margin label in sentence case, e.g. "About the project". */
  label: string;
  title: string;
  intro?: string;
  children: ReactNode;
};

/** Editorial section for the reading part of the page: a numbered label in
 *  the left margin (sticky on wide screens), the serif title and the
 *  content in the main column. No boxed eyebrows. */
export function EditorialSection({ id, index, label, title, intro, children }: SectionProps) {
  return (
    <section id={id} aria-labelledby={`${id}-title`} className="hcsa-section">
      <div className="hcsa-ed-grid">
        <p className="hcsa-ed-label" data-reveal>
          <span className="hcsa-ed-num">{index}</span>
          {label}
        </p>
        <div className="min-w-0">
          <header className="mb-12 max-w-3xl" data-reveal>
            <h2
              id={`${id}-title`}
              className="font-serif text-[clamp(1.9rem,3.6vw,3rem)] leading-[1.08] tracking-tight text-white"
            >
              {title}
            </h2>
            {intro ? <p className="mt-5 max-w-2xl text-lg leading-relaxed text-white/72">{intro}</p> : null}
          </header>
          {children}
        </div>
      </div>
    </section>
  );
}

/** Small sentence-case heading inside a section. */
export function SubHeading({ children }: { children: ReactNode }) {
  return <h3 className="hcsa-ed-sub">{children}</h3>;
}

/** Items separated by hairlines instead of boxed cards. */
export function RuledList({
  items,
  columns = 2,
}: {
  items: { title: string; body?: string; meta?: string }[];
  columns?: 1 | 2 | 3 | 4;
}) {
  return (
    <ul className={`hcsa-ruled hcsa-ruled-${columns}`}>
      {items.map((it) => (
        <li key={it.title} data-reveal>
          <p className="font-serif text-[1.3rem] leading-snug text-white">{it.title}</p>
          {it.meta ? <p className="hcsa-ruled-meta">{it.meta}</p> : null}
          {it.body ? <p className="mt-2 text-[1.02rem] leading-relaxed text-white/68">{it.body}</p> : null}
        </li>
      ))}
    </ul>
  );
}

/** A full-width link row: title, one line, and an arrow that moves on hover. */
export function LinkRow({ href, title, body }: { href: string; title: string; body: string }) {
  return (
    <a href={href} className="hcsa-linkrow" data-reveal>
      <span>
        <span className="hcsa-linkrow-title">{title}</span>
        <span className="mt-1 block text-base text-white/65">{body}</span>
      </span>
      <span aria-hidden className="hcsa-linkrow-arrow">
        →
      </span>
    </a>
  );
}
