# Verification record — 15 October 2026

This records observed tests, not a claim that all websites work.

- 35 Python tests passed: extraction, technology evidence, validation, DNS/IP boundaries, redirects, robots handling, spreadsheet CSV safety and Actor billing limits.
- 7 Node tests passed: URL normalization, domain deduplication, input errors, export safety and demo evidence consistency.
- 13 browser workflow assertions passed in installed Chrome via Playwright: filters, empty state, JSON inspection, CSV download, configuration generation, rejection of local URLs, EN/VI switching, mobile menu and no page overflow at 390px.
- Apify's CLI validated input, dataset and output schemas.
- Local live test: 6 public websites completed, 19 HTTP requests, 3 with public email findings. Completion can have no email; it means the permitted pages were processed.
- Cloud run `6V8zcKKSDkanE3J5L` succeeded with exit code 0: 3 completed domains, 9 requests, 3 saved result rows. Observed platform cost: USD 0.0023162062. Runtime about 96 seconds; the crawler honored a site's published crawl delay.
- A run by the owner's account before paid pricing was enabled is not customer revenue. No first sale or income is claimed.

The source changed after the first cloud test to add extraction caps and a Klaviyo signature; the release is rebuilt and rechecked before handover. Tests and costs from this small sample do not predict all-site costs, success rates, or sales.

## Run the checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests/web.test.mjs
npx apify-cli validate-schema
```

For browser QA, install Playwright and run `node scripts/browser-check.mjs` against a server serving `dist/`. The script accepts `PREVIEW_URL`, `PLAYWRIGHT_ENTRY`, and `CHROME_PATH`; screenshots and report go to ignored `artifacts/browser/`.
