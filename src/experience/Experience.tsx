import { Canvas } from "@react-three/fiber";
import { EffectComposer, Bloom, ChromaticAberration, Noise, Vignette } from "@react-three/postprocessing";
import { Suspense, useEffect, useRef } from "react";
import { ACESFilmicToneMapping, Vector2 } from "three";
import { Scene } from "./Scene";
import { PhaseController } from "./PhaseController";
import { ScrollProgress } from "./ScrollProgress";
import { emptyRegistry, type SceneRegistry } from "./sceneRegistry";

// Memoized outside render so postprocessing doesn't re-allocate on each frame.
// Halved from 0.0006 — at hero the title copy was picking up a color fringe.
const CHROMA_OFFSET = new Vector2(0.0003, 0.0003);

export function Experience() {
  const registry = useRef<SceneRegistry>(emptyRegistry());
  const progressRef = useRef(0);

  // Dev-only: expose stable refs on window for in-browser diagnosis.
  // Merges with whatever Scene.tsx later writes (scene + populated registry).
  useEffect(() => {
    if (import.meta.env.DEV) {
      const w = window as unknown as { __hcsa?: Record<string, unknown> };
      w.__hcsa = { ...(w.__hcsa ?? {}), progressRef, registry };
    }
  }, []);

  return (
    <>
      <ScrollProgress progressRef={progressRef} />
      <div className="hcsa-canvas-layer">
        <Canvas
          dpr={[1, 2]}
          gl={{
            antialias: true,
            alpha: false,
            powerPreference: "high-performance",
            // ACES Filmic + exposure 1.15: single biggest lever for
            // "cinema" feel vs raw Blender-preview look. Compresses the
            // highlight shoulder instead of clipping, gives richer
            // mid-tones. Default three.js toneMapping (Linear) is why
            // PBR scenes look flat "CAD" out of the box.
            toneMapping: ACESFilmicToneMapping,
            toneMappingExposure: 1.15,
          }}
          camera={{ fov: 40, near: 0.05, far: 1200, position: [22, -15, 8] }}
        >
          {/* True black space — was #02040a (slight blue tint) which made
              the earth backdrop fight the void instead of sitting in it. */}
          <color attach="background" args={["#000000"]} />
          {/* No fog: space has none. Fog was smearing the habitat into the
              background and killing the crisp specular reads. */}
          <Suspense fallback={null}>
            <Scene registry={registry} />
            <PhaseController registry={registry} progressRef={progressRef} />
            <EffectComposer multisampling={0}>
              {/* Bloom tuned for the new visible Sun mesh + specular rim
                  highlights on the aluminum bezels. Threshold 0.9 catches
                  the sun (emissive, toneMapped=false pushes it past 1.0)
                  and strong sun-lit panel edges, but not the matte skin. */}
              <Bloom
                intensity={0.48}
                luminanceThreshold={0.9}
                luminanceSmoothing={0.35}
                radius={0.85}
                mipmapBlur
              />
              <ChromaticAberration
                offset={CHROMA_OFFSET}
                radialModulation={false}
                modulationOffset={0}
              />
              {/* Film grain — the cue that turns a CG render into a
                  "captured" image. Opacity kept low so it reads as sensor
                  noise, not stylized VHS. */}
              <Noise opacity={0.035} premultiply />
              <Vignette eskil={false} offset={0.18} darkness={0.55} />
            </EffectComposer>
          </Suspense>
        </Canvas>
      </div>
    </>
  );
}
