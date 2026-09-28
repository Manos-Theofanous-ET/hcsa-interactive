/** Maps raw scroll progress through the #film wrapper to the scene's phase
 *  timeline, so the 3D phase on screen always matches the chapter text.
 *
 *  The nine chapter sections are each one viewport tall, so chapter k
 *  (0-based) fills the screen at raw progress k/8. The phase ranges in
 *  phase_metadata.json are not evenly spaced (phases 3 to 5 are longer,
 *  8 and 9 shorter), so without this map the Gardens text sat over the
 *  window panel scene, and Heat and Water over the gardens.
 *
 *  Knots: raw k/8 lands on the middle of phase k+1; the first and last
 *  knots stay at 0 and 1 so the hero opens on phase 1 and the film ends
 *  on phase 9. Linear in between, strictly increasing. */
const KNOTS: readonly (readonly [number, number])[] = [
  [0, 0],
  [1 / 8, 0.15], // The Station     (phase 2: 0.10 to 0.20)
  [2 / 8, 0.275], // How it gets built (phase 3: 0.20 to 0.35)
  [3 / 8, 0.425], // Inside          (phase 4: 0.35 to 0.50)
  [4 / 8, 0.575], // Window panel    (phase 5: 0.50 to 0.65)
  [5 / 8, 0.7], // Gardens          (phase 6: 0.65 to 0.75)
  [6 / 8, 0.8], // Heat and water   (phase 7: 0.75 to 0.85)
  [7 / 8, 0.885], // Testing         (phase 8: 0.85 to 0.92)
  [1, 1], //       Get involved     (phase 9: 0.92 to 1.00)
];

export function sceneProgress(raw: number): number {
  const t = raw < 0 ? 0 : raw > 1 ? 1 : raw;
  for (let i = 1; i < KNOTS.length; i += 1) {
    const [x1, y1] = KNOTS[i]!;
    if (t <= x1) {
      const [x0, y0] = KNOTS[i - 1]!;
      return y0 + ((t - x0) / (x1 - x0)) * (y1 - y0);
    }
  }
  return 1;
}

/** Raw progress at which chapter `idx` (1-based, 1 = hero) fills the screen. */
export function chapterRawProgress(idx: number): number {
  return Math.min(1, Math.max(0, (idx - 1) / 8));
}
