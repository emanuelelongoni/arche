// Browser checks of the built site: accessibility, phone layout, keyboard use,
// working without JavaScript, the CSP, and that every symbol the graph uses draws.
import AxeBuilder from "@axe-core/playwright";
import { expect, test, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
import { planRoute } from "../src/lib/plan";

const data = JSON.parse(readFileSync(new URL("../.generated/site-data.json", import.meta.url), "utf-8"));
const PAGES = ["/", "/map/", "/map/npov/", "/topics/", "/topics/ts.finite-products-compact/", "/courses/ib-topological-spaces/", "/route/#to=ts.heine-borel"];

function watchErrors(page: Page) {
  const errors: string[] = [];
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  page.on("pageerror", (e) => errors.push(String(e)));
  return errors;
}

for (const scheme of ["light", "dark"] as const) {
  test.describe(`${scheme} theme`, () => {
    test.use({ colorScheme: scheme });
    for (const path of PAGES) {
      test(`${path} has no accessibility violations`, async ({ page }) => {
        await page.goto(path);
        const { violations } = await new AxeBuilder({ page }).analyze();
        expect(violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(" ")).slice(0, 3).join(", ")}`)).toEqual([]);
      });
    }
  });
}

test("pages load without console errors (including CSP violations) and never scroll sideways", async ({ page }) => {
  const errors = watchErrors(page);
  for (const path of PAGES) {
    await page.goto(path);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow, `${path} scrolls sideways`).toBeLessThanOrEqual(0);
  }
  expect(errors).toEqual([]);
});

test("every non-ASCII symbol in the graph draws with ink", async ({ page }) => {
  const text = JSON.stringify(data.nodes) + JSON.stringify(data.courses);
  const symbols = [...new Set([...text].filter((c) => c.codePointAt(0)! > 0x7e))].join("");
  await page.goto("/topics/ts.finite-products-compact/");
  const blank = await page.evaluate(async (symbols) => {
    const stack = getComputedStyle(document.body).fontFamily;
    await document.fonts.load(`64px ${stack}`, symbols);
    await document.fonts.ready;
    const c = document.createElement("canvas");
    c.width = 200; c.height = 120;
    const ctx = c.getContext("2d")!;
    return [...symbols].filter((ch) => {
      ctx.clearRect(0, 0, 200, 120);
      ctx.font = `64px ${stack}`;
      ctx.fillText(ch, 20, 90);
      const d = ctx.getImageData(0, 0, 200, 120).data;
      for (let i = 3; i < d.length; i += 4) if (d[i] > 0) return false;
      return true;
    });
  }, symbols);
  expect(blank).toEqual([]);
});

test.describe("without JavaScript", () => {
  test.use({ javaScriptEnabled: false });
  test("the map switches viewpoint and marks nPOV-only topics", async ({ page }) => {
    await page.goto("/map/");
    await expect(page.locator(".map-svg .node.only")).toHaveCount(0);
    await page.getByRole("link", { name: "nPOV", exact: true }).click();
    await expect(page).toHaveURL(/\/map\/npov\/$/);
    const onlyNpov = Object.values(data.nodes).filter((n: any) => n.only_in?.includes("npov")).length;
    await expect(page.locator(".map-svg .node.only")).toHaveCount(onlyNpov);
    await expect(page.locator(".map-svg .node.stub").first()).toBeVisible();
  });
});

test("the route tool works from the keyboard alone", async ({ page }) => {
  await page.goto("/route/");
  for (let i = 0; i < 30 && (await page.evaluate(() => document.activeElement?.id)) !== "route-target"; i++) {
    await page.keyboard.press("Tab");
  }
  await expect(page.locator("#route-target")).toBeFocused();
  const target = "ts.finite-products-compact";
  const dag = data.viewpoints.npov.dag;
  await page.keyboard.type("Finite products"); // select typeahead
  await expect(page.locator("#route-target")).toHaveValue(target);
  await page.keyboard.press("Tab"); // to the viewpoint radios
  await page.keyboard.press("ArrowRight"); // classical -> nPOV
  await expect(page.locator("#route-summary")).toHaveText(new RegExp(`^nPOV: ${planRoute(dag, [target], []).length} topics`));

  // Tick the first topic in the checklist with the space bar.
  const first = page.locator("#route-known-list input").first();
  const firstId = await first.getAttribute("value");
  await first.focus();
  await page.keyboard.press("Space");
  await expect(first).toBeFocused();
  const expected = planRoute(dag, [target], [firstId!]).length;
  await expect(page.locator("#route-summary")).toHaveText(new RegExp(`^nPOV: ${expected} topics`));
  await expect(page).toHaveURL(new RegExp(`known=${firstId!.replace(".", "\\.")}`));
});

test("the theme control overrides the system setting and is remembered", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("radio", { name: "Dark" }).check();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(page.getByRole("radio", { name: "Dark" })).toBeChecked();
});
