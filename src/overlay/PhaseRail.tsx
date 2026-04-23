import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useEffect, useRef } from "react";

gsap.registerPlugin(ScrollTrigger);

/** Vertical scroll-progress rail pinned to the right edge. Nine phase dots
 *  evenly spaced along a 1 px column; a cyan fill scales top-down as the
 *  user scrolls; the dot whose scroll range contains the current progress
 *  pulses cyan.
 *
 *  Why not React state per tick? Same rule as PhaseController — no
 *  useState in the scroll path. We mutate DOM refs directly inside the
 *  ScrollTrigger onUpdate callback. */
const PHASES = [
  { idx: 1, label: "Hero", start: 0.0, end: 0.1 },
  { idx: 2, label: "Habitat", start: 0.1, end: 0.2 },
  { idx: 3, label: "Assembly", start: 0.2, end: 0.35 },
  { idx: 4, label: "Interior", start: 0.35, end: 0.5 },
  { idx: 5, label: "Panel", start: 0.5, end: 0.65 },
  { idx: 6, label: "Bio", start: 0.65, end: 0.75 },
  { idx: 7, label: "Thermal", start: 0.75, end: 0.85 },
  { idx: 8, label: "Validation", start: 0.85, end: 0.92 },
  { idx: 9, label: "Closing", start: 0.92, end: 1.0 },
] as const;

export function PhaseRail() {
  const fillRef = useRef<HTMLSpanElement>(null);
  const dotsRef = useRef<Array<HTMLButtonElement | null>>([]);
  const labelRef = useRef<HTMLSpanElement>(null);
  const currentPhaseRef = useRef(1);

  useEffect(() => {
    const st = ScrollTrigger.create({
      start: 0,
      end: "max",
      scrub: true,
      onUpdate: (self) => {
        const p = self.progress;
        if (fillRef.current) {
          fillRef.current.style.transform = `scaleY(${p})`;
        }
        // Find the active phase by range containment; swap the pulse
        // styling only when it changes (cheap attribute mutation).
        const active = PHASES.find((ph) => p >= ph.start && p <= ph.end) ?? PHASES[PHASES.length - 1]!;
        if (active.idx !== currentPhaseRef.current) {
          for (let i = 0; i < dotsRef.current.length; i += 1) {
            const dot = dotsRef.current[i];
            const phase = PHASES[i];
            if (dot && phase) dot.dataset.active = String(phase.idx === active.idx);
          }
          if (labelRef.current) labelRef.current.textContent = active.label;
          currentPhaseRef.current = active.idx;
        }
      },
    });
    // Prime initial state.
    const initial = PHASES[0];
    if (initial && labelRef.current) labelRef.current.textContent = initial.label;
    const firstDot = dotsRef.current[0];
    if (firstDot) firstDot.dataset.active = "true";
    return () => st.kill();
  }, []);

  // Smooth-scroll to a phase's scroll-range midpoint on dot click.
  const jumpTo = (start: number, end: number) => {
    const target = document.documentElement.scrollHeight - window.innerHeight;
    const mid = (start + end) / 2;
    window.scrollTo({ top: target * mid, behavior: "smooth" });
  };

  return (
    <nav
      aria-label="Phase navigation"
      className="pointer-events-none fixed right-6 top-1/2 z-20 hidden -translate-y-1/2 flex-col items-end gap-3 md:flex"
    >
      <span
        ref={labelRef}
        className="data pointer-events-none text-[9px] uppercase tracking-[0.35em] text-white/70"
      >
        Hero
      </span>
      <div className="pointer-events-auto relative flex h-[46vh] w-[12px] items-stretch justify-center">
        {/* Vertical rail + scroll-linked fill */}
        <span aria-hidden className="absolute left-1/2 top-0 h-full w-px -translate-x-1/2 bg-white/15" />
        <span
          aria-hidden
          ref={fillRef}
          className="hcsa-rail-fill absolute left-1/2 top-0 h-full w-px -translate-x-1/2 bg-[color:var(--color-accent-cyan)]"
        />
        {/* 9 dots, evenly spaced along the rail */}
        {PHASES.map((ph, i) => (
          <button
            key={ph.idx}
            ref={(el) => {
              dotsRef.current[i] = el;
            }}
            type="button"
            aria-label={`Jump to phase ${ph.idx}: ${ph.label}`}
            onClick={() => jumpTo(ph.start, ph.end)}
            className="hcsa-rail-dot absolute left-1/2 h-[6px] w-[6px] -translate-x-1/2 rounded-full bg-white/30 hover:bg-white/80 focus:outline-none focus-visible:ring-1 focus-visible:ring-[color:var(--color-accent-cyan)]"
            style={{ top: `calc(${(i / (PHASES.length - 1)) * 100}% - 3px)` }}
          />
        ))}
      </div>
      <span className="data pointer-events-none text-[9px] uppercase tracking-[0.35em] text-white/30">
        {PHASES.length} / 9
      </span>
    </nav>
  );
}
