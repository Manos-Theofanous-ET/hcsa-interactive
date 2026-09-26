import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { GALLERY, type GalleryItem } from "@content/data/gallery";
import { SectionHeader } from "./SectionHeader";

const src = (file: string, thumb = false) => `/assets/web/${file}${thumb ? "-thumb" : ""}.webp`;

/** All project work in one place: tabs per category, a thumbnail grid and
 *  a native <dialog> viewer (Esc closes, arrow keys step through). State
 *  here only changes on clicks and key presses, never during scroll. */
export function GallerySection() {
  const [tab, setTab] = useState(GALLERY[0]?.id ?? "");
  const [open, setOpen] = useState<number | null>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);

  const category = useMemo(() => GALLERY.find((c) => c.id === tab) ?? GALLERY[0], [tab]);
  const items: GalleryItem[] = category?.items ?? [];
  const current = open === null ? undefined : items[open];

  useEffect(() => {
    const d = dialogRef.current;
    if (!d) return;
    if (open !== null && !d.open) d.showModal();
    if (open === null && d.open) d.close();
  }, [open]);

  const step = useCallback(
    (dir: number) => setOpen((i) => (i === null ? i : (i + dir + items.length) % items.length)),
    [items.length],
  );

  return (
    <section id="work" aria-labelledby="work-title" className="hcsa-section">
      <SectionHeader
        id="work"
        eyebrow="Our work"
        title="Everything we have made so far."
        intro="Concept art, the current blueprints, the 3D model, the panels, our physical model and our earlier technical sheets. Click any image to see it larger."
      />

      <div role="tablist" aria-label="Gallery categories" className="mb-8 flex flex-wrap gap-2">
        {GALLERY.map((c) => (
          <button
            key={c.id}
            role="tab"
            type="button"
            aria-selected={c.id === tab}
            aria-controls="work-panel"
            onClick={() => setTab(c.id)}
            className="data rounded-full border px-4 py-2 text-[11px] uppercase tracking-[0.2em] transition-colors aria-selected:border-[color:var(--color-accent-cyan)] aria-selected:text-[color:var(--color-accent-cyan)] border-white/20 text-white/70 hover:text-white"
          >
            {c.title} <span className="text-white/40">{c.items.length}</span>
          </button>
        ))}
      </div>

      <div id="work-panel" role="tabpanel" aria-label={category?.title}>
        {category ? <p className="mb-6 max-w-2xl text-base text-white/65">{category.blurb}</p> : null}
        {category?.link ? (
          <p className="-mt-3 mb-6">
            <a
              href={category.link.href}
              className="data text-[12px] uppercase tracking-[0.2em] text-[color:var(--color-accent-cyan)] underline underline-offset-4"
            >
              {category.link.label}
            </a>
          </p>
        ) : null}
        <ul className="columns-1 gap-4 sm:columns-2 lg:columns-3">
          {items.map((item, i) => (
            <li key={item.file} className="mb-4 break-inside-avoid">
              <button
                type="button"
                onClick={() => setOpen(i)}
                className="group block w-full text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-accent-cyan)]"
              >
                <img
                  src={src(item.file, true)}
                  alt={item.caption}
                  width={item.w}
                  height={item.h}
                  loading="lazy"
                  decoding="async"
                  className="h-auto w-full rounded-sm bg-white/5 transition-opacity group-hover:opacity-85"
                />
                <span className="mt-2 block text-sm leading-snug text-white/70">{item.caption}</span>
              </button>
            </li>
          ))}
        </ul>
      </div>

      <dialog
        ref={dialogRef}
        aria-label={current?.caption ?? "Image viewer"}
        onClose={() => setOpen(null)}
        onClick={(e) => {
          // Clicks on the dark area around the image close the viewer.
          const t = e.target as HTMLElement;
          if (t === e.currentTarget || t.tagName === "FIGURE") setOpen(null);
        }}
        onKeyDown={(e) => {
          if (e.key === "ArrowRight") step(1);
          if (e.key === "ArrowLeft") step(-1);
        }}
        className="hcsa-viewer"
      >
        {current ? (
          <figure className="flex h-full flex-col items-center justify-center gap-4 p-4 md:p-10">
            <img
              src={src(current.file)}
              alt={current.caption}
              className="max-h-[80vh] max-w-full object-contain"
            />
            <figcaption className="flex w-full max-w-4xl items-center justify-between gap-4 text-white/80">
              <button type="button" onClick={() => step(-1)} className="hcsa-viewer-btn" aria-label="Previous image">
                ←
              </button>
              <span className="text-center text-base">
                {current.caption}
                <span className="data ml-3 text-xs text-white/40">
                  {(open ?? 0) + 1} / {items.length}
                </span>
              </span>
              <button type="button" onClick={() => step(1)} className="hcsa-viewer-btn" aria-label="Next image">
                →
              </button>
            </figcaption>
            <button
              type="button"
              onClick={() => setOpen(null)}
              className="hcsa-viewer-btn absolute right-4 top-4"
              aria-label="Close image viewer"
            >
              ✕
            </button>
          </figure>
        ) : null}
      </dialog>
    </section>
  );
}
