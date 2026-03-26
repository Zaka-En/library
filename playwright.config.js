import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  use: {
    baseURL: "http://frontend.ezaka.es",
    screenshot: "on",
    //reuseExistingServer: true,
    video: "on-first-retry",
  },

  webServer: {
    command: "docker compose -f compose.yml -f compose.test.yml up ",
    url: "http://frontend.ezaka.es",
    reuseExistingServer: true,
    timeout: 120 * 1000,
  },
  //testMatch: '**/*.e2e.{ts,js}'
});
