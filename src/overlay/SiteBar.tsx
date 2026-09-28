import { useEffect, useRef } from "react";

/** Slim top bar so visitors can always reach the plan, the blueprints and
 *  the sponsor section without scrolling back to the hero.
 *
 *  It stays out of the way of the film: hidden in the hero, shown when the
 *  reader scrolls up anywhere past it, and always shown once the film is
 *  over (the reading sections). DOM mutation only, no React state in the
 *  scroll path. */
export function SiteBar() {
  const barRef = useRef<HTMLElement>(null);

  useEffect(() => {
    let lastY = window.scrollY;
    let raf = 0;

    const update = () => {
      raf = 0;
      const bar = barRef.current;
      if (!bar) return;
      const y = window.scrollY;
      const film = document.getElementById("film");
      const filmEnd = film ? film.offsetTop + film.offsetHeight - window.innerHeight : Infinity;
      const pastHero = y > window.innerHeight * 0.85;
      const afterFilm = y > filmEnd + window.innerHeight * 0.4;
      const scrollingUp = y < lastY - 2;
      const scrollingDown = y > lastY + 2;
      let show = bar.dataset.show === "true";
      if (!pastHero) show = false;
      else if (afterFilm) show = true;
      else if (scrollingUp) show = true;
      else if (scrollingDown) show = false;
      bar.dataset.show = String(show);
      bar.inert = !show;
      lastY = y;
    };

    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };
    // In-page links (#work, #sponsor, #hero) glide instead of jumping.
    // Done in JS rather than CSS scroll-behavior, which fights ScrollTrigger.
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    const onClick = (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = (e.target as Element | null)?.closest?.("a[href^='#']") as HTMLAnchorElement | null;
      if (!a) return;
      const id = a.getAttribute("href")!.slice(1);
      const target = id ? document.getElementById(id) : null;
      if (!target) return;
      e.preventDefault();
      const top = id === "hero" ? 0 : target.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top, behavior: reduce.matches ? "auto" : "smooth" });
      history.pushState(null, "", `#${id}`);
    };
    document.addEventListener("click", onClick);

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    update();
    return () => {
      document.removeEventListener("click", onClick);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <nav ref={barRef} aria-label="Site" className="hcsa-sitebar" data-show="false">
      <div className="hcsa-sitebar-inner data">
        <a href="#hero" className="hcsa-sitebar-brand">
          HCSA
        </a>
        <a href="/plan/">The plan</a>
        <a href="/blueprints/">Blueprints</a>
        <a href="#work" className="hcsa-sitebar-wide">
          Our work
        </a>
        <a href="#sponsor" className="hcsa-sitebar-cta">
          Sponsor us
        </a>
      </div>
    </nav>
  );
}
