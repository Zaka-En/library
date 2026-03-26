import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  use: {
    baseURL: "http://localhost:3000",
    screenshot: "on",
    //reuseExistingServer: true,
    video: "on-first-retry",
  },

  webServer: {
    command: "docker compose -f compose.yml -f compose.test.yml up ",
    url: "http://localhost:3000",
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
  //testMatch: '**/*.e2e.{ts,js}'
});
