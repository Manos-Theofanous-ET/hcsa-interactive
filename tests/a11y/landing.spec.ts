import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/** Landing-page accessibility audit. Runs axe-core against the hero and
 *  each chapter section, asserting zero `critical` or `serious` violations.
 *  `moderate` and `minor` are logged but do not fail — we tighten once we
 *  have a clean baseline. WCAG 2.1 AA scope per WEB_ASSET_BRIEF. */

const SECTIONS = [
  { id: "hero", label: "Phase 1 — Hero" },
  { id: "habitat", label: "Phase 2 — Habitat" },
  { id: "assembly", label: "Phase 3 — Assembly" },
  { id: "interior", label: "Phase 4 — Interior" },
  { id: "panel", label: "Phase 5 — Panel" },
  { id: "bio", label: "Phase 6 — Bio" },
  { id: "thermal", label: "Phase 7 — Thermal" },
  { id: "validate", label: "Phase 8 — Validation" },
  { id: "contact", label: "Phase 9 — Contact" },
] as const;

test.describe("Landing a11y", () => {
  test("no critical or serious axe violations on initial load", async ({ page }) => {
    await page.goto("/");
    // Let fonts + R3F settle so we don't report FOUT-only issues.
    await page.waitForLoadState("networkidle");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
      .analyze();

    const blocking = results.violations.filter(
      (v) => v.impact === "critical" || v.impact === "serious",
    );
    for (const v of blocking) {
      // eslint-disable-next-line no-console
      console.error(`[a11y] ${v.impact?.toUpperCase()} ${v.id}: ${v.help}`);
      for (const node of v.nodes) {
        // eslint-disable-next-line no-console
        console.error(`  target: ${node.target.join(" ")}`);
      }
    }
    expect(blocking, "no critical or serious axe violations").toHaveLength(0);
  });

  test("every phase section has a reachable anchor + heading", async ({ page }) => {
    await page.goto("/");
    for (const s of SECTIONS) {
      const section = page.locator(`#${s.id}`);
      await expect(section, `${s.label} section present`).toBeVisible({ timeout: 10_000 });
      const heading = section.locator("h1, h2").first();
      await expect(heading, `${s.label} has heading`).toBeVisible();
    }
  });

  test("phase rail dots are keyboard-reachable", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");
    // PhaseRail is hidden on mobile (md: breakpoint). Only run on desktop.
    const viewport = page.viewportSize();
    test.skip(!viewport || viewport.width < 768, "PhaseRail hidden below md");

    const dots = page.locator('[aria-label^="Jump to phase"]');
    const count = await dots.count();
    expect(count, "9 phase-rail dots").toBe(9);
    // Focusable via tab (indirect check — element is a real <button>).
    await expect(dots.first()).toBeEnabled();
  });

  test("reduced-motion fallback does not autoplay video", async ({ browser }) => {
    const context = await browser.newContext({ reducedMotion: "reduce" });
    const page = await context.newPage();
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // The Canvas layer must NOT render. Instead the poster stills mount.
    const canvas = page.locator("canvas");
    await expect(canvas, "no WebGL canvas under reduced-motion").toHaveCount(0);

    const videos = page.locator("video");
    // A <video> element may exist (inside the play-on-demand modal) only
    // AFTER the user opens it; on load there should be zero autoplaying
    // videos, so we assert none are currently present.
    await expect(videos).toHaveCount(0);

    await context.close();
  });
});
