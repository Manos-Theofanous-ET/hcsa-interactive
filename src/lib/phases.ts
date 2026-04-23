import { z } from "zod";

export const Opacities = z.object({
  hex_frame: z.number(),
  hex_glass: z.number(),
  hex_solar: z.number(),
  pent_frame: z.number(),
  pent_glass: z.number(),
  interior: z.number(),
  wireframe: z.number(),
});

export const Emissive = z.object({
  wireframe_cyan: z.number(),
  led_green: z.number(),
  water_red: z.number(),
  water_blue: z.number(),
});

export const PhaseSpec = z.object({
  phase: z.number().int().min(1).max(9),
  name: z.string(),
  scroll_range: z.tuple([z.number().min(0).max(1), z.number().min(0).max(1)]),
  camera: z.string(),
  opacities: Opacities,
  hex_translation_m: z.number(),
  pent_translation_m: z.number(),
  emissive: Emissive,
  ease: z.string(),
});

export const PhasesDoc = z.object({
  version: z.string(),
  canonical_source: z.string(),
  brief_source: z.string(),
  phases: z.array(PhaseSpec).length(9),
});

export type PhaseSpec = z.infer<typeof PhaseSpec>;
export type PhasesDoc = z.infer<typeof PhasesDoc>;
export type Opacities = z.infer<typeof Opacities>;
export type Emissive = z.infer<typeof Emissive>;

/** Returns the phase that contains a given scroll fraction [0,1]. */
export function phaseAt(phases: PhaseSpec[], scroll: number): PhaseSpec {
  const clamped = Math.max(0, Math.min(1, scroll));
  const found = phases.find(
    (p) => clamped >= p.scroll_range[0] && clamped <= p.scroll_range[1],
  );
  return found ?? phases[phases.length - 1]!;
}
