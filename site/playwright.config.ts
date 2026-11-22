import { defineConfig, devices } from "@playwright/test";

// Runs against the static build (npm run build first), served like GitHub Pages by e2e/serve.mjs.
export default defineConfig({
  testDir: "e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
  webServer: {
    command: "node e2e/serve.mjs dist 4322",
    port: 4322,
    reuseExistingServer: !process.env.CI,
  },
  use: { baseURL: "http://localhost:4322" },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 900 } } },
    { name: "phone", use: { ...devices["Desktop Chrome"], viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true } },
  ],
});
