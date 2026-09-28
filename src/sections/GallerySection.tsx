import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { GALLERY, type GalleryItem } from "@content/data/gallery";
import { DRAWING_PREVIEW, drawingFull } from "@content/data/downloads";
import { BlueprintPreview } from "./BlueprintPreview";
import { EditorialSection, SubHeading } from "./SectionHeader";

const src = (file: string, thumb = false) => `/assets/web/${file}${thumb ? "-thumb" : ""}.webp`;

type ViewItem = { key: string; src: string; caption: string };
const PREVIEW_VIEW: ViewItem[] = DRAWING_PREVIEW.map((d) => ({ key: d.name, src: drawingFull(d.name), caption: d.caption }));

/** All project work in one place: tabs per category, a thumbnail grid and
 *  a native <dialog> viewer (Esc closes, arrow keys step through). State
 *  here only changes on clicks and key presses, never during scroll. */
export function GallerySection() {
  const [tab, setTab] = useState(GALLERY[0]?.id ?? "");
  // The viewer shows either the blueprint preview or the current tab.
  const [viewer, setViewer] = useState<{ items: ViewItem[]; index: number } | null>(null);
  const dialogRef = useRef<HTMLDialogElement>(null);

  const category = useMemo(() => GALLERY.find((c) => c.id === tab) ?? GALLERY[0], [tab]);
  const items: GalleryItem[] = category?.items ?? [];
  const current = viewer ? viewer.items[viewer.index] : undefined;
  const isOpen = viewer !== null;

  useEffect(() => {
    const d = dialogRef.current;
    if (!d) return;
    if (isOpen && !d.open) d.showModal();
    if (!isOpen && d.open) d.close();
  }, [isOpen]);

  const close = useCallback(() => setViewer(null), []);
  const step = useCallback(
    (dir: number) =>
      setViewer((v) => (v ? { ...v, index: (v.index + dir + v.items.length) % v.items.length } : v)),
    [],
  );
  const openTab = (i: number) =>
    setViewer({ items: items.map((it) => ({ key: it.file, src: src(it.file), caption: it.caption })), index: i });

  return (
    <EditorialSection
      id="work"
      index="02"
      label="Our work"
      title="Everything we have made so far."
      intro="Concept art, the current blueprints, the 3D model, the panels, our physical model and our earlier technical sheets. Click any image to see it larger."
    >
      <BlueprintPreview onOpen={(i) => setViewer({ items: PREVIEW_VIEW, index: i })} />

      <div className="mt-20" data-reveal>
        <SubHeading>All our work</SubHeading>
      </div>
      <div role="tablist" aria-label="Gallery categories" className="hcsa-tabs">
        {GALLERY.map((c) => (
          <button
            key={c.id}
            role="tab"
            type="button"
            aria-selected={c.id === tab}
            aria-controls="work-panel"
            onClick={() => setTab(c.id)}
            className="hcsa-tab"
          >
            {c.title} <span className="hcsa-tab-count">{c.items.length}</span>
          </button>
        ))}
      </div>

      <div id="work-panel" role="tabpanel" aria-label={category?.title}>
        {category ? <p className="mb-6 max-w-2xl text-base text-white/65">{category.blurb}</p> : null}
        {category?.link ? (
          <p className="-mt-3 mb-6">
            <a
              href={category.link.href}
              className="hcsa-textlink"
            >
              {category.link.label} <span aria-hidden>→</span>
            </a>
          </p>
        ) : null}
        <ul className="columns-1 gap-4 sm:columns-2 lg:columns-3">
          {items.map((item, i) => (
            <li key={item.file} className="mb-4 break-inside-avoid">
              <button
                type="button"
                onClick={() => openTab(i)}
                className="group block w-full text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-accent-cyan)]"
              >
                <img
                  src={src(item.file, true)}
                  alt=""
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
        onClose={close}
        onClick={(e) => {
          // Clicks on the dark area around the image close the viewer.
          const t = e.target as HTMLElement;
          if (t === e.currentTarget || t.tagName === "FIGURE") close();
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
              key={current.key}
              src={current.src}
              alt={current.caption}
              className="hcsa-viewer-img max-h-[80vh] max-w-full object-contain"
            />
            <figcaption className="flex w-full max-w-4xl items-center justify-between gap-4 text-white/80">
              <button type="button" onClick={() => step(-1)} className="hcsa-viewer-btn" aria-label="Previous image">
                ←
              </button>
              <span className="text-center text-base">
                {current.caption}
                <span className="ml-3 text-xs text-white/65 tabular-nums">
                  {(viewer?.index ?? 0) + 1} / {viewer?.items.length ?? 0}
                </span>
              </span>
              <button type="button" onClick={() => step(1)} className="hcsa-viewer-btn" aria-label="Next image">
                →
              </button>
            </figcaption>
            <button
              type="button"
              onClick={close}
              className="hcsa-viewer-btn absolute right-4 top-4"
              aria-label="Close image viewer"
            >
              ✕
            </button>
          </figure>
        ) : null}
      </dialog>
    </EditorialSection>
  );
}
