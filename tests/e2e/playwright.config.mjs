import { defineConfig } from '@playwright/test';

const PORT = Number(process.env.PORT || 4173);

export default defineConfig({
  testDir: '.',
  timeout: 30_000,
  expect: { timeout: 7_000 },
  fullyParallel: false,
  workers: 1,
  reporter: process.env.CI ? 'list' : [['list']],
  use: {
    baseURL: `http://localhost:${PORT}`,
    headless: true,
    trace: 'retain-on-failure',
  },
  webServer: {
    command: 'node serve.mjs',
    url: `http://localhost:${PORT}`,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    env: { PORT: String(PORT) },
  },
  projects: [{ name: 'chromium', use: { browserName: 'chromium' } }],
});
