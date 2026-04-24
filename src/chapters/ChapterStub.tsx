import type { ReactNode } from "react";

/** Igloo-style corner chapter: section fills the viewport, 3D scene is
 *  the subject, and text sits at edge corners as tiny anchored labels.
 *  On narrow viewports the corners collapse into a single left-aligned
 *  stack so nothing gets clipped.
 *
 *  Layout (md+):
 *    TL: phase eyebrow (PHASE 02 · HABITAT)
 *    TR: display statement (Fraunces serif, 1–2 lines)
 *    BL: spec table (passed via children — usually a tiny MDX <table>)
 *    BR: why-it-matters one-liner + optional micro-nav
 *
 *  Mobile: TL → statement → spec → why, stacked. */
type Props = {
  id: string;
  index: number;
  /** Short phase name, rendered uppercase in the eyebrow. */
  title: string;
  /** 1–2 line display headline. Can contain `\n` for a manual break. */
  statement: string;
  /** One-line "why it matters", shown bottom-right in mono. */
  why?: string;
  /** MDX body, usually a single minimal spec table. */
  children?: ReactNode;
};

export function ChapterStub({ id, index, title, statement, why, children }: Props) {
  const phaseCode = String(index).padStart(2, "0");
  return (
    <section
      id={id}
      data-chapter={index}
      className="hcsa-corner-chapter relative min-h-screen"
    >
      {/* TL: phase eyebrow */}
      <div className="hcsa-corner hcsa-corner-tl">
        <p className="data text-[10px] uppercase tracking-[0.35em] text-[color:var(--color-accent-cyan)]">
          Phase&nbsp;{phaseCode}
          <span className="mx-2 text-white/25">/</span>
          <span className="text-white/70">{title}</span>
        </p>
      </div>

      {/* TR: statement (display serif, opinionated line-height) */}
      <div className="hcsa-corner hcsa-corner-tr">
        <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2.6rem)] font-normal leading-[1.05] tracking-tight text-white">
          {statement.split("\n").map((line, i) => (
            <span key={i} className="block">
              {line}
            </span>
          ))}
        </h2>
      </div>

      {/* BL: spec table (MDX body) */}
      <div className="hcsa-corner hcsa-corner-bl">{children}</div>

      {/* BR: why + micro-nav */}
      {why ? (
        <div className="hcsa-corner hcsa-corner-br">
          <p className="data max-w-[32ch] text-right text-[10px] uppercase tracking-[0.18em] leading-relaxed text-white/55">
            {why}
          </p>
        </div>
      ) : null}
    </section>
  );
}
