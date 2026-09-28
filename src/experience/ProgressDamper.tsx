import { useFrame } from "@react-three/fiber";
import { useRef } from "react";

type Props = {
  /** Scroll position mapped to the phase timeline, written by ScrollProgress. */
  targetRef: React.MutableRefObject<number>;
  /** What the scene reads: follows the target with a short ease. */
  progressRef: React.MutableRefObject<number>;
};

/** Eases the scene toward the scroll position instead of following it
 *  frame for frame, so the camera glides between chapters and a flick of
 *  the trackpad does not jerk the model. Mounted before PhaseController so
 *  it runs first in each frame. Refs only, no React state. */
export function ProgressDamper({ targetRef, progressRef }: Props) {
  const primed = useRef(false);
  useFrame((_, dt) => {
    const target = targetRef.current;
    if (!primed.current) {
      // First frame (or a reload halfway down the page): start in place.
      progressRef.current = target;
      primed.current = true;
      return;
    }
    const diff = target - progressRef.current;
    if (Math.abs(diff) < 1e-5) {
      progressRef.current = target;
      return;
    }
    // About 0.2 s time constant; frame-rate independent.
    const k = 1 - Math.exp(-Math.min(dt, 0.25) * 5.5);
    progressRef.current += diff * k;
  });
  return null;
}
