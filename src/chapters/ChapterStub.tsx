import type { ReactNode } from "react";

type Props = {
  id: string;
  index: number;
  title: string;
  kicker: string;
  children?: ReactNode;
};

export function ChapterStub({ id, index, title, kicker, children }: Props) {
  return (
    <section
      id={id}
      data-chapter={index}
      className="relative flex min-h-screen flex-col justify-center px-8 md:px-16"
    >
      <div className="max-w-2xl">
        <p className="data text-xs uppercase tracking-[0.3em] text-[color:var(--color-accent-cyan)]">
          Phase {String(index).padStart(2, "0")}
        </p>
        <h2 className="mt-3 font-serif text-[clamp(2rem,5vw,4rem)] font-normal leading-tight tracking-tight">
          {title}
        </h2>
        <p className="mt-5 data text-sm uppercase tracking-[0.2em] text-white/60">{kicker}</p>
        {children ? (
          <div className="mt-8 space-y-4 text-base leading-relaxed text-white/80 md:text-lg [&_strong]:font-semibold [&_strong]:text-white">
            {children}
          </div>
        ) : (
          <p className="mt-6 text-white/40">Copy pending — placeholder stub.</p>
        )}
      </div>
    </section>
  );
}
