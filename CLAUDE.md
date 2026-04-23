# HCSA Interactive — Site Rules

## Mission
Ship a single-page, scroll-driven WebGL teardown of the HCSA habitat.
Nine chapters. The model is the storyteller. The information rides on
the spectacle, not alongside it.

Visual reference: [Igloo.inc](https://www.igloo.inc) — cinematic
scroll-driven R3F, GSAP ScrollTrigger as the absolute source of truth,
fullscreen canvas with HTML overlay.

## Relationship to sibling repos
- **`../blender-automation/`** produces the canonical geometry:
  `HCSA_MAIN.glb`, `cameras.json`, `phase_metadata.json`. Do **not**
  author geometry in this repo. Run `pnpm sync:geometry` to pull the
  pinned artifacts; the script fails if the GLB sha256 drifts
  (forces an intentional re-pin).
- **`../internal_release_revB/`** is the team's engineering source of
  truth. Cited numerics live in `content/numerics.ts` with source file
  paths attached — update values there, not in copy.
- **`../archive/`** holds the six prior site attempts (see
  `archive/ARCHIVE_INDEX.md` §"2026-04-21 — Website consolidation").
  Mine from archive with direct copy only; do not resurrect an archived
  folder as live.

## Stack (locked — do not swap without updating `WEB_ASSET_BRIEF.md`)
- **Vite 5 + React 19 + TypeScript** (strict, `noUncheckedIndexedAccess`)
- **@react-three/fiber + drei + postprocessing** for the 3D scene
- **GSAP ScrollTrigger** as the one source of truth for scroll
  choreography. No Framer Motion, no Theatre.js, no Motion One. Lenis is
  allowed for smooth scroll if wired with ScrollTrigger compat.
- **Tailwind v4** via `@tailwindcss/vite`
- **MDX** for chapter body copy (`content/chapters/0{1-9}-*.mdx`)
- **Howler** for subtle SFX (opt-in; default muted)
- **zod** to parse `cameras.json` + `phase_metadata.json` at runtime
- **Fraunces** (serif) + **Space Mono** (mono) via `@fontsource/*`
- Deploy: **Vercel** → `hcsa-site.vercel.app`

## Hard rules
- **No React state updates inside `useFrame` or ScrollTrigger
  `onUpdate`.** Mutate Three.js refs directly.
- **No camera positions hardcoded in TypeScript.** Always read from
  `public/3d/cameras.json` (the file synced from blender-automation).
- **No geometry authored in the browser.** Import only.
- **Pixel ratio capped at 2** — `renderer.setPixelRatio(Math.min(dpr, 2))`.
- **Materials in the GLB are Principled BSDF + image texture only.**
  The site layers post-processing (bloom, chromatic aberration, fog)
  on top; it does not rebuild materials client-side.
- **Every number in copy traces to `content/numerics.ts`.** If a value
  lives only in a chapter's MDX, move it to numerics.ts.
- **Font licensing:** only self-hosted free fonts via `@fontsource/*`.

## Nine-chapter narrative (merged from teardown brief + sponsor plan)
| # | Chapter | Scroll % | 3D beat | Sponsor message |
|---|---|---|---|---|
| 1 | Hero | 0–10 | Closed shell vs Earth, slow orbit | "Living the good life in space" |
| 2 | The Habitat | 10–20 | Cyan wireframes fade in | 11.151 m · 32 faces · 629 m³ |
| 3 | Earth-Built, Orbit-Assembled | 20–35 | Hex +0.30 m, pent +0.15 m push | Fabricate → stack → launch → weld |
| 4 | Inside the Shell | 35–50 | Ghost cage, interior visible | ~520 m³, 8 zones |
| 5 | The Panel | 50–65 | One hex teardown, 7 layers | v3 joint, 1332 kN, NAS9306C-06 |
| 6 | Living Systems | 65–75 | PENT_02 hinges, trays glow | Bioregenerative ECLSS |
| 7 | Thermal & Water | 75–85 | Beam splits, loops pulse | 15 L/day distillation |
| 8 | Coupon → Habitat | 85–92 | Reassembly snap back | P5 coupon current, P1–P7 roadmap |
| 9 | Get Involved | 92–100 | Wide orbital shot | Brown, team, contact |

## Repo layout
```
hcsa-interactive/
  CLAUDE.md                       this file
  index.html                      minimal shell, preloads GLB
  vite.config.ts                  plugins: react-swc, tailwind, mdx
  tsconfig.json                   strict, path aliases @/ @content/
  package.json
  .claude/                        (session scaffolding)
  scripts/
    sync-geometry.ts              pulls GLB + JSONs from blender-automation
  public/
    3d/
      HCSA_MAIN.glb               synced, pinned sha256
      cameras.json                9 phase camera matrices
      phase_metadata.json         per-phase opacities/translations/emissive
      manifest.json               generated hash/size record
    assets/
      images/                     renders + concepts (28 png/jpeg/svg)
      blueprints/                 15 engineering blueprint PNGs
      renders/                    internal_release_revB canonical renders
      prototype/                  physical-prototype photos
  src/
    main.tsx                      root render
    App.tsx                       Experience + Overlay
    index.css                     Tailwind v4 + theme tokens
    mdx.d.ts                      MDX module declaration
    experience/                   R3F side
      Experience.tsx              Canvas wrapper
      Scene.tsx                   GLB + stars + lights
      CameraRig.tsx               reads cameras.json, sets hero camera
    overlay/
      Overlay.tsx                 HTML overlay layout; imports MDX chapters
    chapters/
      HeroChapter.tsx             hero with MDX body
      ChapterStub.tsx             generic chapter section with MDX children
    lib/
      cameras.ts                  zod schema + focalToFov util
      phases.ts                   zod schema + phaseAt util
  content/
    numerics.ts                   every cited number, sourced
    data/
      team.ts                     team roster
    chapters/
      01-hero.mdx … 09-contact.mdx
  tests/                          (Playwright + axe, to add)
```

## Scripts
- `pnpm dev` — Vite dev server (reads PORT env var, default 5173)
- `pnpm build` — tsc + vite build
- `pnpm preview` — serve build output
- `pnpm sync:geometry` — pull GLB + JSONs from `../blender-automation`
- `pnpm typecheck` — `tsc -b --noEmit`
- `pnpm test` — Vitest
- `pnpm test:e2e` — Playwright
- `pnpm test:a11y` — axe-core via Playwright
- `pnpm lint` — ESLint

## Validation gates (to enforce in CI)
- **Typecheck:** `tsc -b` passes with zero errors
- **Lighthouse:** Performance ≥ 90 desktop / ≥ 75 mobile, LCP < 2.5 s,
  CLS < 0.05
- **Runtime 3D:** Hero scene holds ≥ 55 fps for 30 s on M1 Air baseline
- **Draw calls:** ≤ 120 in phase 1, ≤ 300 at any peak phase
- **Heap:** ≤ 500 MB after a full scroll-through
- **a11y:** `axe-core` zero errors, keyboard path through every chapter
- **Reduced motion:** `prefers-reduced-motion: reduce` swaps to poster
  fallback (`reports/renders/web_preview/hcsa_teardown_preview.mp4`)
- **GLB contract:** All expected node names resolve (static check
  against `content/numerics.ts` contract names)
- **Camera drift:** Playwright reads live camera; position vs
  `cameras.json` ≤ 1e-3 m
- **React state:** dev-only assert: no `useState` setter fires during
  scroll event dispatch
- **Bundle:** first-load JS ≤ 250 KB gzipped outside the R3F chunk

## Banned
- React state updates inside `useFrame` / ScrollTrigger `onUpdate`
- Camera positions hardcoded in TypeScript
- Geometry authored in-browser
- Theatre.js / Framer Motion / Motion One for scroll
- Materials in GLB that aren't Principled BSDF + image texture
- Pixel ratio > 2
- Blocking fonts on critical render path (`font-display: swap`)
- Autoplaying audio without mute-by-default
- Tracking scripts that block page load

## Working mode
- Scripts are idempotent. `pnpm sync:geometry` run twice is a no-op.
- Typecheck before committing. `pnpm typecheck` in < 10 s is the bar.
- Keep chapters' MDX short — body copy is ≤ 4 short paragraphs.
  Anything longer belongs in a linked resource, not inline.
- If a chapter needs new numerics, add them to `content/numerics.ts`
  with source, then reference in MDX.
- Post-processing (bloom, chromatic aberration, DOF) is allowed once
  the 3D scene itself reads correctly. Never use post to hide a
  material or camera issue.
