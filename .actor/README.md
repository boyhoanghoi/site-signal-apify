# Website Contact & Tech Scraper | SiteSignal

Turn a list of business websites into structured contact and technology
profiles, with source links you can check. One row per domain, ready for CRM
enrichment, partner research or spreadsheet review.

![SiteSignal preview: public contact fields, technology signals and source evidence. Fictional sample data.](https://raw.githubusercontent.com/boyhoanghoi/site-signal-apify/main/assets/brand/sitesignal-store-preview.png)

## What SiteSignal extracts

- Public email addresses from mailto links, visible text and Organization JSON-LD.
- Published phone links and Organization JSON-LD telephone fields.
- Social profile links grouped by platform.
- Published business name, title, description and relevant contact pages.
- Contact forms observed on the fetched pages.
- Recognizable CMS, ecommerce, analytics and payment technology signatures.
- Evidence containing the observed value, source URL and extraction method.

Emails are observed addresses; mailbox existence and deliverability are not
verified. Phones are published observations. SiteSignal does not guess either
from company or person names.

Technology detection identifies signatures in fetched HTML. It is not a complete
or verified inventory of a company's software.

## How to use it

1. Add business website URLs in the Input tab.
2. Start with a few domains and the default three-page budget.
3. Run the Actor and inspect the contacts and evidence dataset views.
4. Export JSON, CSV or Excel using Apify's dataset tools. For a flat,
   spreadsheet-safe file, choose **Download spreadsheet-safe CSV** in the outputs.

The prefilled sample uses Python, Django and the Electronic Frontier Foundation.
These are real public websites, not paying customers or endorsements. Some pages
contain social links or contact forms without publishing an email; empty fields
are valid observations.

```json
{
  "websites": [
    {"url": "https://www.python.org/"},
    {"url": "https://www.djangoproject.com/"},
    {"url": "https://www.eff.org/"}
  ],
  "maxSites": 3,
  "maxPagesPerSite": 3,
  "respectRobots": true,
  "includeTechnology": true
}
```

Plain URL strings are also accepted. Duplicate domains are processed once.
The maximum is 1,000 input websites and five HTML pages per site. Set concurrency,
request timeout and per-site delay under Crawl limits. For remote API access,
use the generated examples in this Actor's API tab and keep your token private.

## Output

The default dataset contains one row per successfully processed website:

| Field | Meaning |
| --- | --- |
| `url`, `finalUrl`, `domain` | Requested website, final landing URL and normalized domain |
| `companyName`, `title`, `description` | Published organization and page metadata when available |
| `emails`, `phones`, `socials` | Observed contacts and normalized social profiles |
| `contactPageUrls`, `contactFormUrls` | Relevant contact pages and pages containing contact forms |
| `technologies` | Technology names, categories, evidence and source URLs |
| `evidence` | Contact values, source URLs and extraction methods |
| `pagesVisited`, `pagesChecked`, `observedAt` | Observation scope and time |
| `status`, `warnings` | Result status and crawl limitations |

Failed websites are separate, nonbillable diagnostics. The Output tab includes a
run summary, diagnostics, a complete JSON report and spreadsheet-safe CSV.
Statuses can include `blocked`, `timeout`, `robots_disallowed`, `http_error` and
`network_error`. Check diagnostics when reconciling an input list.

## Pricing and limits

The Actor's **Pricing tab** shows the current tariff. In pay-per-event mode, one
`website-enriched` event is recorded when a successful website result is saved to
the dataset. Failed or blocked websites do not create this event. The Actor
respects the run's spending limit and exports only saved results.

The unit is a successfully enriched website, not an email address. An accessible
site with no published email can still yield a completed result containing
metadata, social links or empty contact arrays. No contact count is guaranteed.

## Limitations

SiteSignal reads public HTML with ordinary HTTP requests. It does not execute
JavaScript, log in, solve CAPTCHAs, bypass blocked access or use a private contact
database. JavaScript-rendered details, externally embedded forms and obfuscated
addresses may be missed. A detected contact form must have email and message
fields and no password field. Its containing page is returned; form actions are
never submitted or fetched, including actions hosted by an external provider.

Per HTML page, output is capped at 100 emails, 50 phone numbers, 10 social
profiles per platform, 50 contact-page links, 50 contact-form page links and 500
evidence entries. Values are retained in deterministic discovery order, and
redundant evidence methods may be omitted to retain evidence for each contact.

Robots.txt is respected by default. Requests are bounded and paced. Only process
sites and data you are allowed to use. The Actor extracts information; it does
not send messages or submit contact forms. Review source evidence before using
the output in a business workflow.

## Support

Open an issue in the Actor's Issues tab. Include the public website URL, run ID,
expected field and observed behavior. Remove tokens and private customer data
from your report.

