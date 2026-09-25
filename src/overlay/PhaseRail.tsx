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
  { idx: 1, label: "Intro", start: 0.0, end: 0.1 },
  { idx: 2, label: "The Station", start: 0.1, end: 0.2 },
  { idx: 3, label: "How It Gets Built", start: 0.2, end: 0.35 },
  { idx: 4, label: "Inside", start: 0.35, end: 0.5 },
  { idx: 5, label: "Window Panel", start: 0.5, end: 0.65 },
  { idx: 6, label: "Gardens", start: 0.65, end: 0.75 },
  { idx: 7, label: "Heat and Water", start: 0.75, end: 0.85 },
  { idx: 8, label: "Testing", start: 0.85, end: 0.92 },
  { idx: 9, label: "Get Involved", start: 0.92, end: 1.0 },
] as const;

export function PhaseRail() {
  const fillRef = useRef<HTMLSpanElement>(null);
  const dotsRef = useRef<Array<HTMLButtonElement | null>>([]);
  const labelRef = useRef<HTMLSpanElement>(null);
  const countRef = useRef<HTMLSpanElement>(null);
  const currentPhaseRef = useRef(1);
  const navRef = useRef<HTMLElement>(null);

  useEffect(() => {
    // Same range as ScrollProgress: the #film wrapper. The rail fades out
    // once the reader leaves the film for the gallery and sponsor sections.
    const film = document.getElementById("film");
    const setVisible = (v: boolean) => {
      if (!navRef.current) return;
      navRef.current.style.opacity = v ? "1" : "0";
      // Hidden rail must not catch clicks or keyboard focus.
      navRef.current.inert = !v;
    };
    const st = ScrollTrigger.create({
      trigger: film ?? document.body,
      start: "top top",
      end: film ? "bottom bottom" : "max",
      scrub: true,
      onLeave: () => setVisible(false),
      onEnterBack: () => setVisible(true),
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
          if (countRef.current) countRef.current.textContent = String(active.idx);
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
    const film = document.getElementById("film");
    const target = (film?.offsetHeight ?? document.documentElement.scrollHeight) - window.innerHeight;
    const mid = (start + end) / 2;
    window.scrollTo({ top: target * mid, behavior: "smooth" });
  };

  return (
    <nav
      ref={navRef}
      aria-label="Chapter navigation"
      className="pointer-events-none fixed right-6 top-1/2 z-20 hidden -translate-y-1/2 flex-col items-end gap-3 transition-opacity duration-500 md:flex"
    >
      <span
        ref={labelRef}
        className="data pointer-events-none text-[9px] uppercase tracking-[0.35em] text-white/70"
      >
        Intro
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
            aria-label={`Jump to part ${ph.idx}: ${ph.label}`}
            onClick={() => jumpTo(ph.start, ph.end)}
            className="hcsa-rail-dot absolute left-1/2 h-[6px] w-[6px] -translate-x-1/2 rounded-full bg-white/30 hover:bg-white/80 focus:outline-none focus-visible:ring-1 focus-visible:ring-[color:var(--color-accent-cyan)]"
            style={{ top: `calc(${(i / (PHASES.length - 1)) * 100}% - 3px)` }}
          />
        ))}
      </div>
      <span className="data pointer-events-none text-[9px] uppercase tracking-[0.35em] text-white/30">
        <span ref={countRef}>1</span> / {PHASES.length}
      </span>
    </nav>
  );
}
