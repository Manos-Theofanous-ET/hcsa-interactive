import { useEffect, useRef, useState } from "react";

/** Swaps the live WebGL scene for a static poster sequence when the user
 *  has opted out of motion. Two modes:
 *
 *  1. Scroll-indexed still: the appropriate phase PNG crossfades in based
 *     on scroll position. Zero kinetic energy on the page.
 *  2. A short looped MP4 (9 s) as an alternative, behind a "Play teardown"
 *     button so motion is user-initiated, not auto-playing.
 *
 *  Follows WCAG 2.1 `prefers-reduced-motion: reduce` and WEB_ASSET_BRIEF
 *  §Accessibility: reduced-motion must swap to the poster fallback.
 *
 *  The component reads scroll progress via a ref (no React state during
 *  scroll — same rule the rest of the scene follows) so the phase index
 *  can change without triggering React re-renders. */
type Props = {
  progressRef: React.MutableRefObject<number>;
};

/** Scroll-range → phase-index map, matching phase_metadata.json ranges so
 *  the still frame always matches what the live scene would be showing. */
const PHASE_RANGES: readonly [number, number, number][] = [
  [1, 0.0, 0.1],
  [2, 0.1, 0.2],
  [3, 0.2, 0.35],
  [4, 0.35, 0.5],
  [5, 0.5, 0.65],
  [6, 0.65, 0.75],
  [7, 0.75, 0.85],
  [8, 0.85, 0.92],
  [9, 0.92, 1.0],
];

export function ReducedMotionFallback({ progressRef }: Props) {
  const imgRefs = useRef<Array<HTMLImageElement | null>>([]);
  const currentPhase = useRef(1);
  const [videoOpen, setVideoOpen] = useState(false);

  // Drive the crossfade between the 9 poster stills from scroll progress.
  // `requestAnimationFrame` loop — no useState, no scroll listener.
  useEffect(() => {
    let raf = 0;
    const tick = () => {
      const t = progressRef.current;
      let active = 1;
      for (const [phase, s, e] of PHASE_RANGES) {
        if (t >= s && t <= e) {
          active = phase;
          break;
        }
      }
      if (active !== currentPhase.current) {
        currentPhase.current = active;
        for (let i = 0; i < imgRefs.current.length; i += 1) {
          const img = imgRefs.current[i];
          if (img) img.style.opacity = i === active - 1 ? "1" : "0";
        }
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [progressRef]);

  return (
    <div
      className="hcsa-canvas-layer"
      aria-label="HCSA habitat — reduced-motion poster view"
      role="img"
    >
      {PHASE_RANGES.map(([phase], i) => (
        <img
          key={phase}
          ref={(el) => {
            imgRefs.current[i] = el;
          }}
          src={`/fallback/phase_${phase}.png`}
          alt={`Phase ${phase} — reduced-motion still`}
          loading={phase === 1 ? "eager" : "lazy"}
          style={{
            position: "fixed",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: phase === 1 ? 1 : 0,
            transition: "opacity 420ms ease",
            pointerEvents: "none",
          }}
        />
      ))}

      {/* Manual play-on-demand teardown video. Behind a button so it does
          NOT auto-play — only user-initiated motion is allowed when the
          prefers-reduced-motion media query is active. */}
      <div
        style={{
          position: "fixed",
          bottom: 24,
          right: 24,
          pointerEvents: "auto",
          zIndex: 20,
        }}
      >
        {!videoOpen ? (
          <button
            type="button"
            onClick={() => setVideoOpen(true)}
            className="data"
            style={{
              padding: "8px 14px",
              background: "rgba(0,0,0,0.65)",
              border: "1px solid var(--color-accent-cyan)",
              borderRadius: 2,
              color: "#f4f5f7",
              fontSize: 10,
              letterSpacing: "0.25em",
              textTransform: "uppercase",
              cursor: "pointer",
              backdropFilter: "blur(4px)",
              WebkitBackdropFilter: "blur(4px)",
            }}
            aria-label="Play the 9-second teardown video"
          >
            Play teardown ·&nbsp;9 s
          </button>
        ) : (
          <div
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(0,0,0,0.9)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: 24,
            }}
            role="dialog"
            aria-modal="true"
            aria-label="Teardown video"
          >
            <video
              src="/fallback/hcsa_teardown_preview.mp4"
              controls
              autoPlay
              style={{
                maxWidth: "min(100%, 1280px)",
                maxHeight: "100%",
                outline: "1px solid var(--color-accent-cyan)",
              }}
            />
            <button
              type="button"
              onClick={() => setVideoOpen(false)}
              className="data"
              style={{
                position: "absolute",
                top: 24,
                right: 24,
                padding: "8px 14px",
                background: "rgba(0,0,0,0.65)",
                border: "1px solid #fff",
                borderRadius: 2,
                color: "#fff",
                fontSize: 10,
                letterSpacing: "0.25em",
                textTransform: "uppercase",
                cursor: "pointer",
              }}
              aria-label="Close teardown video"
            >
              Close
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

/** React hook: returns true if the current user has requested reduced
 *  motion. Updates live if they change the OS setting while the page is
 *  open (common on iOS / macOS). */
export function usePrefersReducedMotion(): boolean {
  const [reduced, setReduced] = useState(() => {
    if (typeof window === "undefined") return false;
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handler = (ev: MediaQueryListEvent) => setReduced(ev.matches);
    // Safari < 14 uses the deprecated addListener signature.
    if (mq.addEventListener) {
      mq.addEventListener("change", handler);
      return () => mq.removeEventListener("change", handler);
    }
    mq.addListener(handler);
    return () => mq.removeListener(handler);
  }, []);

  return reduced;
}
