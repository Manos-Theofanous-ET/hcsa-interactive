import { useEffect } from "react";

/** Quiet entrance motion for the overlay.
 *
 *  - Each chapter's text fades up when its chapter fills the screen and
 *    fades away as the next one arrives (data-inview on the section).
 *  - Blocks marked data-reveal in the reading sections fade up once.
 *
 *  The hidden starting state only applies once this runs (html.hcsa-js),
 *  so nothing is ever hidden if scripts fail. CSS handles reduced motion. */
export function RevealController() {
  useEffect(() => {
    const root = document.documentElement;
    if (!("IntersectionObserver" in window)) return;
    root.classList.add("hcsa-js");

    const chapters = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          (e.target as HTMLElement).dataset.inview = String(e.isIntersecting);
        }
      },
      { threshold: 0.45 },
    );
    document.querySelectorAll<HTMLElement>(".hcsa-corner-chapter").forEach((el) => chapters.observe(el));

    const blocks = new IntersectionObserver(
      (entries, obs) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            (e.target as HTMLElement).dataset.revealed = "true";
            obs.unobserve(e.target);
          }
        }
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 },
    );
    const observeBlocks = () =>
      document
        .querySelectorAll<HTMLElement>("[data-reveal]:not([data-revealed])")
        .forEach((el) => blocks.observe(el));
    observeBlocks();
    // The gallery swaps its items when a tab changes; pick up new blocks.
    const mo = new MutationObserver(observeBlocks);
    const overlay = document.querySelector(".hcsa-after-film");
    if (overlay) mo.observe(overlay, { childList: true, subtree: true });

    return () => {
      chapters.disconnect();
      blocks.disconnect();
      mo.disconnect();
      root.classList.remove("hcsa-js");
    };
  }, []);
  return null;
}
