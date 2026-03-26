import { test, expect } from "@playwright/test";

test.describe("Home page || Mi biblioteca", () => {
  // test.beforeEach(async ({ page }) => {
  //   await page.goto("/");
  // });

  // test("Should display the three static categories", async ({ page }) => {
  //   const categories = page.locator(".category-card");
  //   await expect(categories).toHaveCount(3);

  //   await expect(page.getByText("Ciencia Ficción")).toBeVisible();
  //   await expect(page.getByText("Filosofía")).toBeVisible();
  //   await expect(page.getByText("Desarrollo Web")).toBeVisible();
  // });

  test("Should load one reading progress from the api", async ({ page }) => {
    page.on("console", (msg) => console.log("BROWSER LOG:", msg.text()));
    page.on("requestfailed", (req) =>
      console.log("FAILED:", req.url(), req.failure()?.errorText),
    );

    await page.goto("/");
    const progresses = page.locator(".reading-progress");
    await expect(progresses).toHaveCount(1);

    const firstProgress = progresses.first();
    await expect(firstProgress).toBeVisible({ timeout: 10000 });
    await expect(firstProgress).toContainText("%");
  });
});
