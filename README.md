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
    HeroChapter.tsx            phase 1 (implemented)
    ChapterStub.tsx            placeholder for phases 2–9
  overlay/
    Overlay.tsx                HTML overlay above the canvas
    PhaseRail.tsx              left-side phase indicator
  lib/
    cameras.ts                 zod schema + loader for cameras.json
    phases.ts                  zod schema + loader for phase_metadata.json
content/
  chapters/                    MDX copy per phase
  data/                        structured data
  numerics.ts                  canonical numeric citations
public/
  3d/
    HCSA_MAIN.glb              habitat geometry (~2.3 MB, Draco-compressed)
    cameras.json               9 phase cameras
    phase_metadata.json        per-phase opacity / translation / emissive
  assets/                      renders, blueprints, concept images
scripts/
  sync-geometry.ts             pulls updated GLB + JSONs from the
                               blender-automation repo
```

---

## The nine-phase scroll timeline

| # | Phase | Scroll % | Section id |
|---|---|---|---|
| 1 | Hero / Launch | 0–10 | `#hero` |
| 2 | Mission / Breath | 10–20 | `#mission` |
| 3 | Geometry Reveal | 20–35 | `#topology` |
| 4 | Interior Architecture | 35–50 | `#architecture` |
| 5 | Panel Teardown | 50–65 | `#panel-v3` |
| 6 | Pentagon Greenhouse | 65–75 | `#eclss-plants` |
| 7 | Systems Core | 75–85 | `#eclss-water` |
| 8 | Reassembly | 85–92 | `#prototyping` |
| 9 | Closing | 92–100 | `#footer` |

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
