type Props = { eyebrow: string; title: string; intro?: string; id: string };

/** Shared heading block for the sections after the 3D film. */
export function SectionHeader({ eyebrow, title, intro, id }: Props) {
  return (
    <header className="mb-10 max-w-2xl">
      <p className="data mb-3 text-[11px] uppercase tracking-[0.1em] text-[color:var(--color-accent-cyan)]">
        {eyebrow}
      </p>
      <h2 id={`${id}-title`} className="font-serif text-[clamp(1.75rem,3.4vw,2.75rem)] leading-[1.1] tracking-tight text-white">
        {title}
      </h2>
      {intro ? <p className="mt-4 text-lg leading-relaxed text-white/75">{intro}</p> : null}
    </header>
  );
}
