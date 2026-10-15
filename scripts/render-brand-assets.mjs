import { access, mkdir, readFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';

// Optional development helper. Runtime code has no dependency on Playwright.
// Set PLAYWRIGHT_MODULE and CHROME_PATH when using a different workstation.
const playwrightPath = process.env.PLAYWRIGHT_MODULE || 'C:/Users/ADMIN/.cache/codex-tools/browser-check/node_modules/playwright/index.mjs';
const executablePath = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
await access(playwrightPath);
const { chromium } = await import(pathToFileURL(playwrightPath).href);
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const brand = resolve(root, 'assets', 'brand');
await mkdir(brand, { recursive: true });
const svg = await readFile(resolve(brand, 'sitesignal-icon.svg'), 'utf8');
const browser = await chromium.launch({ executablePath, headless: true });
try {
  for (const size of [512, 1024]) {
    const page = await browser.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
    await page.setContent(`<html><head><style>html,body{margin:0;width:${size}px;height:${size}px;background:transparent}svg{display:block;width:${size}px;height:${size}px}</style></head><body>${svg}</body></html>`);
    await page.screenshot({ path: resolve(brand, `sitesignal-icon-${size}.png`), omitBackground: true });
    await page.close();
  }
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(resolve(brand, 'store-preview.html')).href, { waitUntil: 'load' });
  await page.screenshot({ path: resolve(brand, 'sitesignal-store-preview.png') });
  await page.close();
  console.log('Created SiteSignal icon PNGs (512, 1024) and Store preview (1600×900) in assets/brand.');
} finally { await browser.close(); }
