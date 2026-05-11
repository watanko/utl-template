import { expect, test } from "@playwright/test";

test("A should show the template shell", async ({ page }) => {
  await page.route("**/health", async (route) => {
    await route.fulfill({
      json: {
        service_id: "00000000-0000-4000-8000-000000000001",
        name: "utl-template",
        healthy: true,
      },
    });
  });

  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "UTL Template" }),
  ).toBeVisible();
  await expect(page.getByText("Healthy")).toBeVisible();
});
