# Verification record — 15 October 2026

This records observed tests, not a claim that all websites work.

- 35 Python tests passed: extraction, technology evidence, validation, DNS/IP boundaries, redirects, robots handling, spreadsheet CSV safety and Actor billing limits.
- 7 Node tests passed: URL normalization, domain deduplication, input errors, export safety and demo evidence consistency.
- 13 browser workflow assertions passed in installed Chrome via Playwright: filters, empty state, JSON inspection, CSV download, configuration generation, rejection of local URLs, EN/VI switching, mobile menu and no page overflow at 390px.
- Apify's CLI validated input, dataset and output schemas.
- Local live test: 6 public websites completed, 19 HTTP requests, 3 with public email findings. Completion can have no email; it means the permitted pages were processed.
- Cloud run `6V8zcKKSDkanE3J5L` succeeded with exit code 0: 3 completed domains, 9 requests, 3 saved result rows. Observed platform cost: USD 0.0023162062. Runtime about 96 seconds; the crawler honored a site's published crawl delay.
- A run by the owner's account before paid pricing was enabled is not customer revenue. No first sale or income is claimed.

Release build `0.1.3` (`67xwhBwwFcVgK9gFK`) includes extraction caps, the Klaviyo signature and redirect/deduplication fixes. Its cloud run `xmIFy4g8olUI0ktzo` succeeded with 3 saved websites in approximately 4.45 seconds, with observed platform cost USD 0.0004479478. This faster sample uses Django, Plausible and Ghost rather than a site with a long crawl delay. Both runs used the owner's account before paid pricing; neither represents revenue. Tests and costs from this small sample do not predict all-site costs, success rates, or sales.

GitHub Actions was triggered but no jobs started: GitHub returned "The job was not started because your account is locked due to a billing issue." Local checks above passed; remote CI is unverified until the account restriction is resolved.

## Run the checks

After payout details were saved, Apify accepted the launch event price of
USD 0.003. Paid-mode cloud run `ovMKN7v00twIRmfj0` succeeded in about 4.10 seconds:
one public website was saved and recorded one `website-enriched` charge event;
one private IP input was rejected before network access and produced only a
nonbillable diagnostic. Observed platform cost was USD 0.0004252951. This is an
owner-run integration test, not proof of a sale or earned revenue.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests/web.test.mjs
npx apify-cli validate-schema
```

For browser QA, install Playwright and run `node scripts/browser-check.mjs` against a server serving `dist/`. The script accepts `PREVIEW_URL`, `PLAYWRIGHT_ENTRY`, and `CHROME_PATH`; screenshots and report go to ignored `artifacts/browser/`.
