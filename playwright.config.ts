import { defineConfig, devices } from "@playwright/test";

/** Playwright config — one project per target device, pointed at the Vite
 *  dev server by default. `pnpm test:a11y` runs only the a11y specs;
 *  `pnpm test:e2e` will run everything under tests/ when we add more.
 *
 *  Preview URL: override with PLAYWRIGHT_BASE_URL to run against Vercel
 *  preview deploys instead of localhost (useful in CI after a PR opens). */
export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? "github" : "list",
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost:5173",
    trace: "on-first-retry",
  },
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: "pnpm dev",
        url: "http://localhost:5173",
        reuseExistingServer: !process.env.CI,
        timeout: 60_000,
      },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 13"] } },
  ],
});
