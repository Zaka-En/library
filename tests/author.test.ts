import { test, expect } from "@playwright/test";

const AUTHORS_COUNT = 4;

test.describe("Authors page ", () => {
  test(`Should load ${AUTHORS_COUNT} authors`, async ({ page }) => {
    await page.goto("/authors");

    const authors = page.getByRole("heading", { level: 2 });
    const verLinks = page.getByRole("link", { name: "Ver" });

    // the +1 is for the h2 title of the Header
    await expect(authors).toHaveCount(AUTHORS_COUNT + 1);
    await expect(verLinks).toHaveCount(AUTHORS_COUNT);
  });

  test("Should click on the Ver link and navigate to the author page", async ({
    page,
  }) => {
    await page.goto("/authors");
    const verLinks = page.getByRole("link", { name: "Ver" });

    await verLinks.first().click();
    await expect(page).toHaveURL(/\/authors\/[A-Za-z0-9+/]+=*$/);

    const AuthorNameTitle = page.getByRole("heading", { level: 1 });
    await expect(AuthorNameTitle).toBeVisible();
  });

  test("Should update the author correctly", async ({ page }) => {
    await page.goto("/authors");

    const editLinks = page.getByRole("link", { name: /Editar/ });

    await editLinks.first().click();
    await expect(page).toHaveURL(/\/authors\/[A-Za-z0-9+/]+=*\/edit$/);

    // input: Biografía
    const idInputField = page.getByRole("textbox", { name: "ID del Autor" });
    await expect(idInputField).toBeVisible();
    await expect(idInputField).toBeDisabled();

    // Fill: Biografía
    const biographyField = page.getByLabel("Biografía");
    await biographyField.fill("TRES TRISTES TIGRES COMEN TRIGO EN UN TRIGAAAL");

    // Save Button
    const saveButton = page.getByRole("button", { name: "Guardar Cambios" });
    await saveButton.click();

    //await expect(saveButton).toBeDisabled();
    await expect(page.getByText(/Cargando/)).toBeVisible();
    await expect(page).toHaveURL(/\/authors$/);
  });
});
