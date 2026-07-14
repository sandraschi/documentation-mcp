import { defineConfig } from "@playwright/test"

export default defineConfig({
  testDir: "./e2e",
  timeout: 60000,
  retries: 1,
  use: {
    baseURL: "http://localhost:11032",
    headless: true,
    screenshot: "only-on-failure",
  },
  webServer: [
    {
      command: "uv run uvicorn docs_mcp.server:app --host 127.0.0.1 --port 11033 --log-level warning",
      port: 11033,
      cwd: "../",
      timeout: 30000,
      reuseExistingServer: false,
    },
    {
      command: "npm run dev -- --port 11032 --host",
      port: 11032,
      cwd: ".",
      timeout: 30000,
      reuseExistingServer: false,
    },
  ],
})
