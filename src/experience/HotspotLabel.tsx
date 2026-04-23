import { Html } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useRef } from "react";
import type { CSSProperties } from "react";

/** A drei `<Html>`-anchored label placed at a 3D point in the habitat.
 *  Fades in during `phaseRange` and out elsewhere so the hotspot only reads
 *  when the relevant chapter is on-screen. Mutates opacity via a DOM ref
 *  inside `useFrame` — never React state, per the no-setState-during-scroll
 *  rule in CLAUDE.md.
 *
 *  Each hotspot renders as a small cyan dot + a short connector line to a
 *  labelled chip. The chip is keyboard-focusable (tabIndex=0) so it sits
 *  inside the a11y tree; the content citation (`source`) becomes the
 *  aria-label so screen readers announce the engineering reference, not
 *  just the display number. */
export type HotspotLabelProps = {
  /** World-space position to anchor the dot marker. */
  position: [number, number, number];
  /** Short display text — e.g. "11.15 m". */
  label: string;
  /** Longer context — e.g. "Outer diameter · CANONICAL §Dimensions". */
  source: string;
  /** Scroll range [start, end] during which this hotspot is fully visible.
   *  Outside the range it fades with `edgeFadeFraction` at each end. */
  phaseRange: readonly [number, number];
  /** Shared scroll progress ref (0..1) from the root ScrollProgress trigger. */
  progressRef: React.MutableRefObject<number>;
  /** How much of the phase range is used for the fade in/out on each end.
   *  Default 0.15 means first 15% fades in, last 15% fades out. */
  edgeFadeFraction?: number;
  /** Optional tone — tints the dot + chip border. Defaults to cyan. */
  tone?: "cyan" | "green" | "orange" | "blue";
};

const TONE_HEX: Record<NonNullable<HotspotLabelProps["tone"]>, string> = {
  cyan: "var(--color-accent-cyan)",
  green: "var(--color-accent-biology)",
  orange: "var(--color-accent-thermal)",
  blue: "var(--color-accent-water)",
};

export function HotspotLabel({
  position,
  label,
  source,
  phaseRange,
  progressRef,
  edgeFadeFraction = 0.15,
  tone = "cyan",
}: HotspotLabelProps) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const [start, end] = phaseRange;
  const accent = TONE_HEX[tone];

  useFrame(() => {
    const t = progressRef.current;
    const fade = edgeFadeFraction * (end - start);
    let alpha: number;
    if (t < start - fade || t > end + fade) {
      alpha = 0;
    } else if (t < start) {
      alpha = (t - (start - fade)) / Math.max(fade, 1e-6);
    } else if (t > end) {
      alpha = 1 - (t - end) / Math.max(fade, 1e-6);
    } else {
      alpha = 1;
    }
    const clamped = alpha < 0 ? 0 : alpha > 1 ? 1 : alpha;
    const el = wrapRef.current;
    if (el) {
      el.style.opacity = String(clamped);
      // Pointer events off when invisible so the hotspot doesn't trap focus
      // or tooltips while outside its phase.
      el.style.pointerEvents = clamped > 0.05 ? "auto" : "none";
    }
  });

  const wrapStyle: CSSProperties = {
    transformOrigin: "center left",
    pointerEvents: "none",
    opacity: 0,
    transition: "none",
    willChange: "opacity",
  };

  const dotStyle: CSSProperties = {
    width: 8,
    height: 8,
    borderRadius: "50%",
    background: accent,
    boxShadow: `0 0 8px ${accent}`,
    flex: "0 0 auto",
  };

  const lineStyle: CSSProperties = {
    width: 28,
    height: 1,
    background: accent,
    opacity: 0.55,
    flex: "0 0 auto",
  };

  const chipStyle: CSSProperties = {
    padding: "4px 8px",
    background: "rgba(0, 0, 0, 0.72)",
    border: `1px solid ${accent}`,
    borderRadius: 2,
    fontFamily: "var(--font-mono)",
    fontSize: 10,
    letterSpacing: "0.08em",
    textTransform: "uppercase",
    color: "#f4f5f7",
    backdropFilter: "blur(4px)",
    WebkitBackdropFilter: "blur(4px)",
    whiteSpace: "nowrap",
  };

  return (
    <Html position={position} center={false} distanceFactor={10} zIndexRange={[10, 0]}>
      <div
        ref={wrapRef}
        style={wrapStyle}
        role="note"
        aria-label={`${label} — ${source}`}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 0,
            transform: "translate(-4px, -4px)",
          }}
        >
          <span aria-hidden style={dotStyle} />
          <span aria-hidden style={lineStyle} />
          <span tabIndex={0} style={chipStyle}>
            {label}
          </span>
        </div>
      </div>
    </Html>
  );
}
