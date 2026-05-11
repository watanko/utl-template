import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "../e2e",
  testMatch: "**/*.e2e.ts",
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "on-first-retry",
  },
  webServer: {
    command: "corepack pnpm dev --host 127.0.0.1 --port 5173",
    reuseExistingServer: true,
    url: "http://127.0.0.1:5173",
  },
  projects: [
    {
      name: "chromium",
      use: devices["Desktop Chrome"],
    },
  ],
});
