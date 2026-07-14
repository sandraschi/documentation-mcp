import { test, expect } from "@playwright/test"

const BE = "http://127.0.0.1:11033"

test.describe("Fleet Audit", () => {
  test("Backend health", async ({ request }) => {
    const resp = await request.get(BE + "/api/health")
    expect(resp.status()).toBe(200)
    const body = await resp.json()
    expect(body.status).toBe("ok")
    expect(body.tool_count).toBeGreaterThan(0)
  })

  test("Backend diagnostics", async ({ request }) => {
    const resp = await request.get(BE + "/api/v1/diagnostics")
    expect(resp.status()).toBe(200)
    const body = await resp.json()
    expect(body.tool_count).toBeGreaterThan(0)
    expect(body.system.windows).toBe(true)
  })

  test("Frontend loads", async ({ page }) => {
    await page.goto("/", { timeout: 15000 })
    await page.waitForTimeout(3000)
    await expect(page.locator("#root")).toBeAttached()
  })

  test("No console errors", async ({ page }) => {
    const errors: string[] = []
    page.on("console", (msg) => {
      if (msg.type() === "error") errors.push(msg.text())
    })
    await page.goto("/", { timeout: 15000 })
    await page.waitForTimeout(3000)
    expect(errors).toEqual([])
  })

  test("Dashboard loads with KPIs", async ({ page }) => {
    await page.goto("/dashboard", { timeout: 15000 })
    await page.waitForTimeout(3000)
    await expect(page.locator('[data-testid="kpi-chunks"]')).toBeAttached()
    await expect(page.locator('[data-testid="kpi-apps"]')).toBeAttached()
  })

  test("Tools hub loads", async ({ page }) => {
    await page.goto("/tools", { timeout: 15000 })
    await page.waitForTimeout(3000)
    await expect(page.locator("#root")).toBeAttached()
  })
})
