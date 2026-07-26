import { test } from "@playwright/test";
import path from "path";
import config from "./config.json";

const OUT_DIR = path.resolve(__dirname, config.output_dir || "../../docs/screenshots");

test.describe("Screenshot capture", () => {
  for (const page of config.pages) {
    test(page.name, async ({ page: p }) => {
      await p.goto(page.route);
      if (page.selector) await p.waitForSelector(page.selector);
      await p.screenshot({ path: `${OUT_DIR}/${page.name.toLowerCase().replace(/\s+/g, "-")}.png`, fullPage: true });
    });
  }
});
