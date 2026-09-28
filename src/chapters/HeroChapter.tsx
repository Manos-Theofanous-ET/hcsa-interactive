import Intro from "@content/chapters/01-hero.mdx";

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

/** Hero — igloo-style edge-anchored title page. The old top nav was broken
 *  (hrefs pointed at section IDs that no longer existed after the chapter
 *  rename) and fought the scroll-driven film; the PhaseRail on the right
 *  carries navigation now. Subtitle trimmed to a single mono fragment per
 *  the audit's §D-15. */
export function HeroChapter() {
  return (
    <section
      id="hero"
      data-chapter="1"
      className="relative flex min-h-screen flex-col justify-between px-6 py-8 md:px-10 md:py-10"
    >
      {/* TL: site mark */}
      <header className="flex items-start justify-between gap-6">
        <div className="data text-[11px] uppercase tracking-[0.1em] text-white/90">
          HCSA
          <span className="mx-2 text-white/40">/</span>
          <span className="text-white/70">Brown University</span>
        </div>
        {/* Sponsors land here first: give them a direct path to the
            gallery and the sponsor section below the 3D story. */}
        <nav aria-label="Quick links" className="data flex flex-wrap items-center justify-end gap-x-5 gap-y-2 text-[11px] uppercase tracking-[0.1em]">
          <a href="/plan/" className="text-white/85 hover:text-white">The plan</a>
          <a href="/blueprints/" className="text-white/85 hover:text-white">Blueprints</a>
          <a href="#work" className="hidden text-white/85 hover:text-white sm:inline">Our work</a>
          <a
            href="#sponsor"
            className="rounded-full border border-[color:var(--color-accent-cyan)] px-3 py-1.5 text-[color:var(--color-accent-cyan)] hover:bg-[color:var(--color-accent-cyan)] hover:text-black"
          >
            Sponsor us
          </a>
        </nav>
      </header>

      {/* Display title, anchored low-left. The canvas behind is the subject. */}
      <div className="pointer-events-none flex flex-1 items-end pb-8">
        <div className="hcsa-hero-text max-w-md space-y-4">
          <p
            className="hcsa-rise data text-[10px] uppercase tracking-[0.1em] text-[color:var(--color-accent-cyan)]"
            style={{ ["--stagger" as string]: "0ms" }}
          >
            Human-Centric Space Architecture
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
          <div
            className="hcsa-rise hcsa-hero-intro max-w-sm text-base leading-relaxed text-white/75"
            style={{ ["--stagger" as string]: "1100ms" }}
          >
            <Intro />
          </div>
        </div>
      </div>

      {/* BL: scroll cue. BR: phase count (decorative, mirrors igloo corner chrome). */}
      <footer className="flex items-end justify-between">
        <div className="flex items-center gap-3 text-white/75">
          <span className="data text-[11px] uppercase tracking-[0.1em]">Scroll to explore</span>
          <span className="block h-[1px] w-10 bg-white/30">
            <span className="block h-full w-full origin-left scale-x-0 bg-[color:var(--color-accent-cyan)] [animation:hcsa-scroll-cue_2.4s_ease-in-out_infinite]" />
          </span>
        </div>
        <div className="data hidden text-right text-[10px] uppercase tracking-[0.1em] text-white/55 md:block">
          01 / 09
        </div>
      </footer>
    </section>
  );
}
