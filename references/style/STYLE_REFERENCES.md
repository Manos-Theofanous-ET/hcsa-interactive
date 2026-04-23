# HCSA Interactive — Style References (Leading Authority)

**Purpose.** Five reference images define the realism bar for the
scroll-driven WebGL teardown. These supersede any prior aesthetic
guidance when the two conflict. Before proposing a render change,
compare the current state against the relevant reference in this doc
and report the delta in concrete terms.

**Source.** Attached by the user 2026-04-21 during the "it looks like
just a CAD/Blender model" iteration. See commit diff for the conversation
where they were introduced.

**Where the actual image files should live.**
If the images are saved to disk, place them at:

```
hcsa-interactive/references/style/reference-01.jpg   ISS interior cutaway
hcsa-interactive/references/style/reference-02.jpg   Axiom Station external
hcsa-interactive/references/style/reference-03.jpg   Bigelow BA-330 inflatables
hcsa-interactive/references/style/reference-04.jpg   Sierra Nevada greenhouse interior
hcsa-interactive/references/style/reference-05.jpg   BEAM module docked
```

(Claude Code cannot write binary image files; a human needs to drop
them in. The textual analysis below captures the visual language in
case the files are not present.)

---

## Reference 1 — Interior cutaway (NASA/Axiom-style)

**Content.** Two astronauts in full suits working at consoles inside a
cylindrical pressurized module. The module is cut away on one side,
revealing Earth through the opening. Heavy equipment racks, exposed
fasteners, fabric surfaces.

**Palette.**
- Interior: near-white panels (`~#e8e8ea`) with mid-grey accents
  (`#8a8e94`), warm fluorescent ambient (`~#fff2d0`)
- Suits: pure white with orange/grey detail
- Earth through window: warm-lit ocean blue + cloud white
- Accent: small amber/red console LEDs

**Lighting.**
- Three sources: harsh sun spill through the open port (~4500K, direct),
  overhead fluorescent fill (~3200K, soft), subtle Earth-shine ambient
  from below.
- Hard shadows under equipment ledges; no global ambient wash.
- Specular reads on every metal edge — bolts, hinges, rail ends.

**Detail density.** Every surface has something: panel seams, cable
runs, velcro patches, instrument faces, fastener heads. Nothing is a
blank plate.

**Takeaway for HCSA.** Phase 4 (Inside the Shell), Phase 6 (Greenhouse),
and Phase 7 (Systems Core) must read at this detail density or they
will feel CAD-empty. Requires texture maps + detail geometry on
interior assets — a Blender-side task, not a site-side one.

---

## Reference 2 — Axiom Station external (cinematic hero)

**Content.** Full Axiom Station assembly: stacked cylindrical modules,
solar wings, docking ports. 3/4 angle. Earth horizon fills the bottom
third of frame.

**Palette.**
- Hull: WHITE (`~#eef0f3`), subtle cream shift on sunlit faces,
  cool-shadowed on shadow side
- Solar arrays: DARK MAROON-BROWN (`#3a2820` mid-tone, `#1a0f08` shadow)
- Visible markings: "AXIOM SPACE" in black, stripes, fastener rows
- Earth: ocean blue/teal body (`#1a4a8a`), cream/white cloud bands,
  bright cyan atmospheric limb (`#a8e0ff` → white at horizon edge)
- Background space: TRUE BLACK (`#000000`) with sparse white stars

**Lighting.**
- Single hard key from camera-left (sun). Clipped whites on hull edges.
- Earth-shine fill from below adds subtle cool on the shadow side of
  modules.
- Zero ambient. Shadow side goes to near-black with only Earth bounce.
- Atmospheric limb acts as a secondary soft backlight on the lower
  portion of the station.

**Composition.**
- Station at ~50% frame height, centered horizontally.
- Earth curve occupies bottom 35% of frame — HERO element, not backdrop.
- Stars sparse (~1 per 10,000 pixels), sized sub-pixel to 2px.
- Grain visible — reads as "captured" image, not CG.

**Detail.** Panel seams every ~30cm of hull, bolt rows, antenna array,
thermal blanket quilting visible at close range, logo/callsigns.

**Takeaway for HCSA.** This is the template for phases 1, 3, 8, 9
(exterior cinematic). Our current render violates it on three axes:
1. **Earth is not a HERO.** Ref: Earth fills 35% of frame. HCSA: Earth
   is a 450m sphere positioned below the habitat, often off-frame.
2. **No surface detail on hull.** Ref: hull has visible seams, bolts,
   logos, stripes every ~30cm. HCSA: hex/pent panels are smooth
   flat-shaded with only the frame ring bezel for detail.
3. **Star density wrong.** Ref: ~100 visible stars in a wide shot.
   HCSA: 10,000 stars = overly busy, reads as "starry night sky" not
   "low-orbit photograph".

---

## Reference 3 — Bigelow BA-330 inflatables (clean external)

**Content.** Two cylindrical inflatable modules with orange fabric
reinforcement bands, docked to Dragon capsule and Orion-style capsule.
Solar panels. Earth below.

**Palette.**
- Hull: WHITE fabric with visible diagonal quilting pattern
- Orange longitudinal bands (`#e8713c`) — structural reinforcement
- Solar: dark navy-blue rectangles (`#1a2850`), subtle cell grid
- Earth: daylit side, warm brown surfaces (deserts), white cloud
  systems, thin cyan atmospheric limb
- Space: true black, very few stars

**Lighting.**
- Overhead key (sun above frame). Hard shadow below modules.
- Earth provides strong bounce — the underside of modules is cool-lit
  from the blue-white Earth.
- Atmospheric limb rim-lights the silhouette where hull meets black sky.

**Composition.**
- Modules fill middle third horizontally, spanning ~70% of frame width.
- Earth fills bottom 40%, with hard cyan-white limb defining the top
  boundary of Earth.
- Dark space above takes the top 25%.

**Takeaway for HCSA.** The orange-band detail is the kind of single
chromatic accent that breaks "monotone white hull" syndrome. HCSA's
equivalent would be the cyan wireframe (already planned), but it
currently reads as "pasted on" rather than "integrated into the hull"
because it lacks material thickness/specular. Possible fix: turn the
WIREFRAME mesh into a slightly raised cylindrical tube geometry with
emissive cyan + specular clearcoat.

---

## Reference 4 — Sierra Nevada greenhouse interior

**Content.** Cutaway of multi-deck inflatable module interior. Top
deck: greenhouse with purple grow lights on leafy plants. Middle deck:
exercise/workspace. Bottom deck: crew quarters + console. Crew members
in each deck.

**Palette.**
- Interior panels: crisp white with mid-grey detail (`#cfd2d6` base)
- Grow-light accent: saturated **magenta/purple** (`#a040c8`) — this
  is THE emotional color of the phase
- Warm console LEDs on lower deck (amber, blue)
- Plants: healthy green (`#4a8a32`) under the purple LED wash — reads
  as muted olive-green, not vivid green

**Lighting.**
- Top deck: dominant purple LED grow lights, high intensity, hard
  falloff — purple bounces onto white panels making them read lavender
- Middle deck: neutral fluorescent fill (~4500K white)
- Bottom deck: warm console illumination (~2800K amber) with cool accent
  screens

**Takeaway for HCSA.** This is the template for phase 6 (Pentagon
Greenhouse). The brief already calls for `led_green` emissive, but
this reference says **purple/magenta grow lights** are what reads as
"real bioregenerative ECLSS" — horticulture LEDs are purple because
plants absorb red+blue and reflect green. If we shift our grow-light
color from `#00FF66` (neon green) to `#a040c8` (purple) the scene
will read as engineering-accurate instead of video-game accurate.

**Contradiction with existing brief.** WEB_ASSET_BRIEF §7 specifies
`#00FF66` emissive green for "Biology" and `led_green` emissive in
phase_metadata.json targets 2.5 at phase 6. Per the "references
supersede prior guidance" rule of this doc, purple/magenta should win
— but this should be flagged with the user before changing because it
also affects the palette system (data labels, hotspots).

---

## Reference 5 — BEAM module docked (iconic minimal)

**Content.** Single white inflatable module docked to a node. Simple
shape, visible fabric surface. Earth curving below with bright
atmospheric halo.

**Palette.**
- Hull: matte white fabric, subtle shading on quilt pattern
- Earth: grey-blue ocean, bright white atmospheric limb
  (almost clipped, `#d0e8ff` → white)
- Background: deep black, zero stars visible

**Lighting.**
- Hard sun from upper-left, near-black shadow on lower-right of module.
- Earth limb acts as secondary fill — the underside of the module
  catches a subtle cyan-white bounce.

**Composition.**
- Module dead-centered, fills ~25% frame.
- Earth curve in lower third, with THE atmosphere being the brightest
  thing on screen.
- This is the "all about the silhouette" composition. Minimal detail,
  maximum mood.

**Takeaway for HCSA.** This is the template for phase 9 (Closing) and
possibly phase 1 (Hero) in "cinematic" mode. Our current hero is
closer to this already — just needs bigger Earth + brighter limb.

---

## Distilled principles (the rubric)

Any time we propose a render change, check against this list:

### Earth
- [ ] Earth fills **20–40% of frame** on every exterior phase
  (currently: visible only at phase 6 composition)
- [ ] Earth body has **surface color variation** — not uniform
  dark blue (currently: uniform `#040c20`)
- [ ] Atmospheric halo is **bright cyan-white**, reaches near-white at
  the extreme limb (currently: `rgba(0.26,0.52,1.0)` — too dim)
- [ ] Limb acts as a **secondary light source** — gives cool rim on
  the underside of the habitat (currently: rim light is a separate
  directional, not a bounce from Earth)

### Sunlight
- [x] Hard directional key, one dominant source ✓
- [x] ACES filmic tone map to clip cleanly into white ✓
- [ ] Clipped whites on sunlit metal edges (currently: not quite
  punching through)
- [x] Near-black on shadow side, no global ambient ✓

### Hull
- [ ] **Surface detail** (seams, bolts, fasteners, bands) — our panels
  are smooth and featureless
- [ ] **Material differentiation** — metal bezel vs painted skin vs
  glass vs solar should read as four distinct surfaces
  (currently: three materials but they read similar)
- [ ] **One accent color** breaking the monotone (currently: cyan
  wireframe, but it floats rather than integrates)

### Stars
- [ ] **Sparse** — not a starfield. ~100–300 visible at a time, not
  10,000 (currently: 10,000 — too busy)
- [ ] Sized mostly sub-pixel, with a few brighter 2px-3px accents
- [ ] Not saturated — pure white, maybe 1% cyan tint

### Post-process
- [x] Subtle bloom on highlights only ✓
- [x] Film grain ✓
- [x] Vignette ✓
- [ ] Tone curve should preserve Earth's daylit side brightness without
  blowing it out

### Interior (Phases 4, 6, 7)
- [ ] Surface detail density matches Ref 1 / Ref 4 (requires Blender
  re-authoring — out of site-repo scope)
- [ ] Phase 6 grow lights should be **purple/magenta**, not green —
  needs user decision before changing

---

## Current render vs target — explicit delta

| Axis | Ref target | HCSA now | Gap |
|---|---|---|---|
| Earth prominence in frame | 20–40% | ~0% at most phases | **HIGH** — reposition and scale Earth |
| Earth surface variation | Clouds + continents + oceans | Uniform dark blue | **HIGH** — procedural texture or shader |
| Atmospheric halo brightness | Near-clipped white at limb | Dim blue | **MEDIUM** — boost halo shader |
| Star density | ~100–300 per frame | 10,000 total | **MEDIUM** — reduce count |
| Hull surface detail | Panel seams, bolts, markings | Smooth flat faces | **HIGH** — requires Blender re-export |
| Hull material variety | 4+ distinct surfaces | 3 similar-reading materials | **MEDIUM** — targeted MeshPhysical upgrade |
| Sunlit clipped highlights | Pure white peaks | Still slightly beige | **LOW** — push sun to ~5.0 |
| Shadow side darkness | Near-black + Earth bounce | OK, slightly flat | **LOW** — already close |
| Interior detail (phase 4/6/7) | Dense, industrial | Low-poly primitives | **HIGH** — Blender scope |
| Phase 6 grow light color | Purple/magenta | Neon green | Pending user decision |
| Phase 5 teardown readability | (no direct ref) | Working with 7 distinct colors | OK |

---

## Prioritized next changes (site-repo scope only)

In order of impact-per-effort:

1. **Earth as hero** — reposition to `[0, -450, -50]`, scale radius to
   550, boost halo brightness (`glowColor` → `[0.55, 0.85, 1.0]`,
   `power` → 1.8 for a brighter crescent). Expected: Earth becomes the
   bottom-of-frame horizon in hero, phase 3, phase 8, phase 9 — matches
   Ref 2 and Ref 5 composition.

2. **Star density down** — `count={10000}` → `count={800}`,
   `radius={280}` → `radius={320}`, `factor={4.0}` → `factor={5.5}`
   for fewer but slightly brighter stars. Matches Ref 2's sparse sky.

3. **Earth surface variation** — swap the `meshStandardMaterial` for a
   custom shader with procedural cloud bands + continental color shift.
   Expected: Earth reads as a real planet, not a dark-blue ball.

4. **Cyan atmosphere brightness** — increase the halo shader's output
   to clip into white at the crescent. Acts as a secondary light
   source visually.

5. **Re-attempt `MeshPhysicalMaterial` upgrade** with a `try/catch`
   around the mesh-material swap, so a single problem material doesn't
   blank the page. Targets the "metal reads as metal" bar from Ref 2
   (visible specular on bezels).

6. **Phase 6 grow-light color flip** — only after user approval.
   Requires editing `phase_metadata.json` and this repo's palette
   tokens (the `--color-accent-biology` CSS variable).

## Out-of-scope gaps (require Blender-side work)

- Hull surface seams/bolts/logos (Ref 2)
- Interior detail density (Ref 1, Ref 4)
- Textured Earth map (optional — can procedurally fake)

These would be next-round deliverables from `blender-automation`.

---

## Process rule

Before any visible render change, add a line to the bottom of this
file under "Changes made":

```
YYYY-MM-DD  [change summary]  [which rubric checkbox it ticks]
```

This keeps the references as the active authority instead of drifting.

## Changes made

- **2026-04-21** — Frame-only `MeshPhysicalMaterial` upgrade (hex + pent
  frames only; skin/glass/solar stay on MeshStandardMaterial). Adds
  clearcoat 0.55, reflectivity 0.6, metalness +0.3, roughness × 0.65,
  cool steel tint (0.78, 0.81, 0.86). Wrapped in try/catch with
  per-swap guard. Ticks rubric items: "Hull material variety" →
  frame/skin/solar now three distinct surfaces. Leaves "Hull surface
  detail" (seams, bolts, markings) still open — Blender scope.
- **2026-04-21** — Sun intensity 4.0 → 5.2, color `#fff0d8` →
  `#fff8e8` (less warm, more noon-orbit). Rim intensity 0.8 → 0.45.
  Ticks rubric items: "Clipped whites on sunlit metal edges",
  "Near-black on shadow side".
- **2026-04-21** — Panel skin (hex/pent Glass) tinted to warm-white
  `(0.97, 0.95, 0.92)` so it separates chromatically from the cool
  steel frame. Ticks rubric item: "Material differentiation".
- **2026-04-21** — Procedural surface-detail shader injection
  (`applyProceduralDetail` via `onBeforeCompile`). GLB ships no UVs or
  tangents on shell panels — forensic check via direct GLB JSON parse
  confirmed only POSITION + NORMAL attributes — which blocks the
  normal-map / texture-map path. Injection uses world-space cell-hash
  noise to modulate `diffuseColor` (±6% frames, ±14% skin) and
  `roughnessFactor` (±35% frames, ±28% skin). Cells scale ~0.7 m = 3-4
  cells per ~2.25 m panel face. Applied to hex + pent frames + glass +
  solar materials. Idempotent (tag check) and try/catch-guarded.
  Ticks rubric items (partial): "Hull surface detail" — real seams still
  require Blender-scope detail geometry, but within-panel tonal
  variation now reads as painted-unevenness rather than uniform clay.
- **2026-04-22** — Full RENDER_AUDIT_PLAN.md executed in
  `blender-automation`. New GLB sha256
  `02e629ed2a4912699a9f3b9ef8c704ccc1ff22327375c68f9dafa5c23d31802f`,
  2.6 MB. Changes:
  - **RC-1**: planar XY UVs on all shell mesh builders
    (`_make_polygon_bezel`, `_make_flat_polygon_pane`,
    `_make_flat_hex_panel`). UV coverage jumped 0/305 → 341/341 meshes.
  - **RC-2**: Metal032 PBR binding for `HCSA_V3_WebGlass`,
    `HCSA_V3_WebPentGlass`, `HCSA_V3_WebBezel`, `HCSA_V3_WebSolar` in
    `_MATERIAL_TEXTURE_MAP`; `TexCoord.Generated` → `TexCoord.UV` in
    `_rewire_material_with_pbr` so texture bindings survive glTF
    export; `apply_image_textures()` re-called after Pass-A enforcement
    so shell materials (created during Pass A) actually receive the PBR
    graph. All 5 shell materials now ship with baseColor + normal +
    metallicRoughness texture bindings. PBR images capped at 512 px to
    keep GLB under the 20 MB CLAUDE.md gate.
  - **RC-3**: widened `_fix_uvless_meshes` safe-prefix tuple from 4
    prefixes → 19 prefixes (includes `HCSA_V3_PanelTeardown` which was
    missing — that's the bug that clobbered per-layer teardown
    materials into a flat grey `HCSA_V3_WebStructural`). Added
    `_ensure_uv_layers_on_all_meshes()` blanket pass using
    bounds-based planar projection so interior meshes survive the
    UV-less safety clamp with their authored materials intact.
  - **RC-4**: wireframe rewritten from face-centre k-nearest
    adjacency (radial X-stars on each face) to true shell-edge
    topology. Reads each frame mesh's outer-ring vertices in world
    space, clusters them into the 60 canonical joint nodes, extracts
    consecutive-corner pairs → exactly 90 shell edges. Tube radius
    bumped 0.020 → 0.045 m; material upgraded from pure Emission to
    Principled BSDF (metallic 0.7, clearcoat 0.5) + Emission
    add-shader. Ticks Ref 3 takeaway.
  - **RC-5**: greenhouse LED emissive flipped from lime-yellow-green
    `(0.85, 1.00, 0.55)` to magenta `(0.63, 0.25, 0.78)` at strength
    4.5 (Ref 4 target — horticulture LEDs are magenta because plants
    reflect green). LED bars bulked 0.025 × 0.04 → 0.06 × 0.10 m.
    Plant cones densified 8 → 20 per shelf (radius 0.10 → 0.06,
    height 0.22 → 0.16) — 60 leaves per phase, packed at real
    hydroponic density.
  - **RC-6**: water pipes pushed from 0.40 m → 1.20 m from column
    axis so they clear the opaque BEAM_TRUNK silhouette. Cylinder
    radius 0.12 → 0.16 m.
  - **RC-8 option 1**: BEAM_TRUNK rebound to `HCSA_V3_Anodized_Aluminum`
    (which now carries Metal032 PBR textures) so the interior column
    reads as scratched anodised aluminium instead of flat grey.
    Detail-geometry re-author of BEAM_TRUNK still deferred (Ref 1 L
    follow-up).
