import type { ReactNode } from "react";

/** Igloo-style corner chapter: section fills the viewport, 3D scene is
 *  the subject, and text sits at edge corners as tiny anchored labels.
 *  On narrow viewports the corners collapse into a single left-aligned
 *  stack so nothing gets clipped.
 *
 *  Layout (md+):
 *    TL: part eyebrow (PART 02 / THE STATION)
 *    TR: display statement (Fraunces serif, 1–2 lines)
 *    BL: spec table (passed via children — usually a tiny MDX <table>)
 *    BR: why-it-matters one-liner + optional micro-nav
 *
 *  Mobile: TL → statement → spec → why, stacked. */
type Props = {
  id: string;
  index: number;
  /** Short phase name, shown next to the chapter number. */
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
        <p className="data text-[13px] text-[color:var(--color-accent-cyan)]">
          <span className="tabular-nums">{phaseCode}</span>
          <span className="ml-3 text-white/85">{title}</span>
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
          <p className="max-w-[34ch] text-[15px] leading-snug text-white/90 md:text-right">
            {why}
          </p>
        </div>
      ) : null}
    </section>
  );
}
