import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useEffect } from "react";

gsap.registerPlugin(ScrollTrigger);

type Props = { progressRef: React.MutableRefObject<number> };

/** Binds a ScrollTrigger to the document so scroll [0..1] writes `progressRef.current`.
 *  No React state — refs only, to honor the "no setState during scroll" rule.
 *
 *  NOTE on `end: "max"`: the site CSS sets `html, body, #root { height: 100% }`,
 *  so `document.body.getBoundingClientRect().height === window.innerHeight`.
 *  That makes `end: "bottom bottom"` resolve to the SAME scroll position as
 *  `start: "top top"` — progress jumps 0→1 in a single pixel of scroll.
 *  `end: "max"` binds the end to the scroller's maximum scroll position
 *  (document scrollHeight minus viewport), giving us a proper 0→1 range
 *  across the full overlay height. */
export function ScrollProgress({ progressRef }: Props) {
  useEffect(() => {
    const st = ScrollTrigger.create({
      trigger: document.body,
      start: "top top",
      end: "max",
      scrub: true,
      onUpdate: (self) => {
        progressRef.current = self.progress;
      },
    });

    // Sync progressRef with any existing scroll on mount.
    progressRef.current = st.progress;

    // Refresh once after first paint so ScrollTrigger measures the final
    // overlay height (MDX + images + fonts may still be settling).
    const raf = requestAnimationFrame(() => ScrollTrigger.refresh());

    return () => {
      cancelAnimationFrame(raf);
      st.kill();
    };
  }, [progressRef]);

  return null;
}
