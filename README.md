# HCSA Interactive

Scroll-driven WebGL teardown of the **Human-Centric Space Architecture** (HCSA)
habitat. The 3D model is the storyteller — as the user scrolls, the habitat
physically deconstructs and reassembles, proving the design is a rigorously
engineered machine, not just a render.

**Live site:** https://hcsa-cinematic-site.vercel.app/

---

## Stack

- **Build:** Vite 5 + TypeScript
- **UI:** React 19
- **3D:** Three.js + `@react-three/fiber` + `@react-three/drei` + `@react-three/postprocessing`
- **Scroll choreography:** GSAP ScrollTrigger (source of truth — no Framer Motion, no Theatre.js)
- **Smooth scroll:** Lenis
- **Styling:** Tailwind CSS v4
- **Content:** MDX for chapter copy, TypeScript for numerics

---

## Getting started

Requires **Node 20+** and **pnpm 9+**.

```bash
pnpm install
pnpm dev          # starts Vite on http://localhost:5173
pnpm build        # production build → dist/
pnpm preview      # serve the production build locally
pnpm typecheck    # tsc --noEmit
```

---

## Project layout

```
src/
  App.tsx                      root component
  main.tsx                     Vite entry
  index.css                    Tailwind + globals
  experience/
    Experience.tsx             wires Scene + Overlay + ScrollProgress
    Scene.tsx                  R3F <Canvas>, loads GLB
    PhaseController.tsx        reads phase_metadata.json, drives tweens
    ScrollProgress.tsx         ScrollTrigger wiring
    sceneRegistry.ts           named mesh lookup table
  chapters/
    HeroChapter.tsx            part 1 (title + intro)
    ChapterStub.tsx            corner layout for parts 2–9
  overlay/
    Overlay.tsx                HTML overlay above the canvas (#film + sections)
    PhaseRail.tsx              right-side chapter indicator
  sections/                    reading sections after the 3D film
    AboutSection.tsx           plain-language project summary
    GallerySection.tsx         all project images, tabs + full-screen viewer
    SponsorSection.tsx         what support pays for, what sponsors get, contact
    TeamSection.tsx            team roster from content/data/team.ts
  lib/
    cameras.ts                 zod schema + loader for cameras.json
    phases.ts                  zod schema + loader for phase_metadata.json
content/
  chapters/                    MDX copy per phase
  data/                        team.ts, gallery.ts, sponsors.ts (edit copy here)
  numerics.ts                  canonical numeric citations
src/
  3d/                          bundled at build time — zod-validated on import
    cameras.json               9 phase cameras
    phase_metadata.json        per-phase opacity / translation / emissive
public/
  3d/
    HCSA_MAIN.glb              habitat geometry (~2.3 MB, Draco-compressed)
    manifest.json              hash + size for drift detection
  assets/                      renders, blueprints, concept images (originals)
    web/                       WebP copies used by the gallery (generated)
  draco/                       self-hosted Draco decoder for the GLB
  hdri/                        self-hosted lighting map (no CDN dependency)
  fallback/                    reduced-motion poster stills + 9s MP4
scripts/
  sync-geometry.ts             pulls updated GLB + JSONs from the
                               blender-automation repo
  optimize-images.py           rebuilds public/assets/web/ from the originals
                               (pip install pillow; python scripts/optimize-images.py)
```

---

## The nine-phase scroll timeline

| # | Phase | Scroll % | Section id |
|---|---|---|---|
| 1 | Intro | 0–10 | `#hero` |
| 2 | The Station | 10–20 | `#habitat` |
| 3 | How It Gets Built | 20–35 | `#assembly` |
| 4 | Inside | 35–50 | `#interior` |
| 5 | The Window Panel | 50–65 | `#panel` |
| 6 | Gardens | 65–75 | `#bio` |
| 7 | Heat and Water | 75–85 | `#thermal` |
| 8 | Testing | 85–92 | `#validate` |
| 9 | Get Involved | 92–100 | `#contact` |

The scroll percentages are measured over the `#film` wrapper only. After the
film come the reading sections: `#about`, `#work` (gallery), `#sponsor` and
`#team`. They have a solid background and do not move the 3D timeline.

### Adding new work to the gallery

1. Drop the original image into `public/assets/images/` (or `blueprints/`).
2. Run `python scripts/optimize-images.py`.
3. Add an entry to `content/data/gallery.ts` with a short plain caption.

---

## Non-negotiable rules

- **Never update React state during scroll.** Mutate Three.js refs directly
  inside ScrollTrigger `onUpdate`.
- **Cap pixel ratio at 2:** `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- **No camera positions hardcoded in TypeScript.** Read from `cameras.json`.
  If a camera needs adjusting, fix it in Blender and re-export.
- **No geometry authored in-browser.** GLB is imported, never mutated.
- **Scroll choreography = GSAP ScrollTrigger only.** No Framer Motion, no
  Theatre.js, no Motion One.

Full constitution: [`CLAUDE.md`](./CLAUDE.md).

---

## Where does the 3D asset come from?

The GLB and JSON files in `public/3d/` are produced by the sibling repo
`blender-automation` (deterministic Blender export pipeline).

To pull the latest export:

```bash
pnpm sync:geometry
```

The script reads from a local path (configured in `scripts/sync-geometry.ts`).
If you don't have the `blender-automation` repo checked out, skip this — the
committed files in `public/3d/` are the current shipped version.

---

## Deployment

Deploys to Vercel. `vercel.json` is committed. Preview URLs generated per branch.

---

## Performance budgets (hard gates)

- Lighthouse Performance ≥ 90 desktop, ≥ 75 mobile
- LCP < 2.5 s, TTI < 4 s, CLS < 0.05
- ≥ 55 fps sustained for 30 s on M1 Air baseline
- WebGL draw calls ≤ 120 in phase 1, ≤ 300 at any peak
- First-load JS ≤ 250 KB gzipped (outside the R3F chunk)

---

## Contributing

1. Create a branch off `main`.
2. `pnpm typecheck` must pass.
3. For scroll/3D changes, test with reduced-motion enabled too.
4. Open a PR — Vercel will auto-deploy a preview URL.
