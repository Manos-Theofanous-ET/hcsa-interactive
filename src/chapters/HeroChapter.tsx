/** Split a string into word-spans, each receiving an incremental
 *  animation-delay so the line unfolds word-by-word. Whitespace is
 *  preserved with non-breaking spaces between spans. */
function RiseWords({
  text,
  baseDelayMs = 0,
  stepMs = 70,
  className = "",
}: {
  text: string;
  baseDelayMs?: number;
  stepMs?: number;
  className?: string;
}) {
  const words = text.split(/\s+/).filter(Boolean);
  return (
    <span className={className}>
      {words.map((w, i) => (
        <span key={`${w}-${i}`}>
          <span
            className="hcsa-rise"
            style={{ ["--stagger" as string]: `${baseDelayMs + i * stepMs}ms` }}
          >
            {w}
          </span>
          {i < words.length - 1 && " "}
        </span>
      ))}
    </span>
  );
}

export function HeroChapter() {
  return (
    <section
      id="hero"
      data-chapter="1"
      className="relative flex min-h-screen flex-col justify-between px-6 py-8 md:px-10 md:py-10"
    >
      <header className="flex items-start justify-between gap-6">
        <div className="data text-[10px] uppercase tracking-[0.35em] text-white/75">
          HCSA Interactive
          <span className="mx-2 text-white/30">/</span>
          <span className="text-white/50">Brown University</span>
        </div>
        <nav className="data hidden gap-5 text-[10px] uppercase tracking-[0.3em] text-white/55 md:flex">
          <a href="#architecture" className="transition hover:text-white">Interior</a>
          <a href="#panel-v3" className="transition hover:text-white">Panel</a>
          <a href="#prototyping" className="transition hover:text-white">Validation</a>
          <a href="#footer" className="transition hover:text-white">Contact</a>
        </nav>
      </header>

      <div className="pointer-events-none flex flex-1 items-end">
        <div className="max-w-md space-y-3">
          <p
            className="hcsa-rise data text-[10px] uppercase tracking-[0.35em] text-[color:var(--color-accent-cyan)]"
            style={{ ["--stagger" as string]: "0ms" }}
          >
            Phase 01 · Hero
          </p>
          <h1 className="font-serif text-[clamp(1.75rem,3.6vw,3.25rem)] font-normal leading-[1.05] tracking-tight text-white">
            <RiseWords text="Living the good life" baseDelayMs={180} stepMs={90} />
            <br />
            <RiseWords
              text="in space."
              baseDelayMs={180 + 4 * 90 + 120}
              stepMs={90}
              className="italic text-white/90"
            />
          </h1>
          <p
            className="hcsa-rise max-w-sm text-sm leading-relaxed text-white/60"
            style={{ ["--stagger" as string]: "1100ms" }}
          >
            A mostly transparent orbital habitat built from 32 panels.
            Scroll to watch it come apart.
          </p>
        </div>
      </div>

      <footer className="flex items-end justify-between">
        <div className="flex items-center gap-3 text-white/45">
          <span className="data text-[10px] uppercase tracking-[0.35em]">Scroll</span>
          <span className="block h-[1px] w-10 bg-white/30">
            <span className="block h-full w-full origin-left scale-x-0 bg-[color:var(--color-accent-cyan)] [animation:hcsa-scroll-cue_2.4s_ease-in-out_infinite]" />
          </span>
        </div>
        <div className="data hidden text-right text-[9px] uppercase tracking-[0.35em] text-white/25 md:block">
          32 panels · 9 phases
        </div>
      </footer>
    </section>
  );
}
