# SiteSignal — Business Website Enricher

Turn a list of company websites into contact and technology records with page-level evidence. Built for agencies, researchers, and CRM workflows. Python CLI, Apify Actor, and a browser-based product demo are included.

[Run on Apify Store](https://apify.com/reliable_quatrain/business-website-contact-tech-scraper) · $0.003 per successfully processed website ($3/1,000). Check the listing for current terms. Failed, blocked and duplicate-redirect websites are not charged; a completed website can have no public contacts.

Only information publicly published by the website is extracted. Email delivery is not verified. Protected or JavaScript-only pages may not yield results. Respect website rules and applicable laws; this tool does not send messages.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[actor]"
.\.venv\Scripts\python.exe -m sitesignal run --input examples/input.json --output output
```

On macOS/Linux, use `.venv/bin/python` instead. Python 3.11+ is required.

The output directory contains `results.json`, `results.csv`, `diagnostics.json`, and `summary.json`, plus `crm-companies.json`/`.csv` and `contacts.json`/`.csv` for company-field mapping and contact review. A domain that cannot be processed appears in diagnostics, not as an enriched result. CSV is protected against spreadsheet formula execution; JSON preserves original data, including the leading `+` in phone numbers.

## What it does

- Reads a homepage and a bounded number of same-site contact/about pages.
- Extracts published email addresses, linked phone numbers, social profiles, and contact forms.
- Detects supported CMS, ecommerce, and analytics signatures and records their evidence.
- Deduplicates website inputs and reports failures explicitly.
- Exports flat company fields for CRM mapping and one contact per row with its source pages and extraction methods.
- Reports each attempted page, failed contact URLs and whether discovered contact links remain beyond the page budget.
- Checks robots.txt by default, restricts requests to public Internet addresses, limits redirects and response size, and throttles requests per host.

## Apify and business setup

For a practical company-list-to-CRM workflow, see [the Vietnamese walkthrough](docs/CRM_WORKFLOW_VI.md). The exports do not write to a CRM or send messages. Contact records remain separate per website, even when the same address appears on two businesses. Export views are included in the website price; they do not create extra billable results.

See [Apify setup](docs/APIFY.md), [market research](docs/MARKET.md), and [first $5 plan](docs/FIRST_5_DOLLARS.md). The project does not guarantee buyers or earnings. Live publication and paid pricing must be confirmed in the owner's Apify account before advertising a paid Actor.

## Product demo

```powershell
.\scripts\serve.ps1
```

Open `http://127.0.0.1:8765`. The bilingual demo lets visitors inspect clearly fictional sample results, export them, and prepare validated Actor input. It does not pretend to scrape websites in the browser. The Python CLI and Apify Actor perform actual enrichment.

## Verification

See [the verification record](docs/VALIDATION.md) for unit/browser checks and actual cloud-test results. Supported signatures include WordPress, WooCommerce, Shopify, Webflow, Wix, Squarespace, Magento, Ghost, GA4, GTM, Plausible, Matomo, Stripe, and Klaviyo. They are observations from HTML, not exhaustive or definitive technology inventories.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## License

MIT. No affiliation with Apify or any technology detected by the tool.
