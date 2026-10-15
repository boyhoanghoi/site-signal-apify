# Deploying and selling SiteSignal on Apify

SiteSignal accepts business website URLs and writes one dataset row per website
whose public HTML was successfully read. Contacts are observed, not inferred or
verified. A successful website with no contacts still produces a useful row with
its title, source pages and empty contact arrays; the charge is for website
enrichment, not for finding a guaranteed number of emails.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[actor]"
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Use the CLI for local work. The Actor entry point is `python -m sitesignal.actor`.
With the [Apify CLI](https://docs.apify.com/cli), `apify run` provides local Actor
storage and loads `storage/key_value_stores/default/INPUT.json`. Without the CLI,
create that input file before running the module directly.

```json
{
  "websites": [{"url": "https://www.python.org/"}],
  "maxSites": 1,
  "maxPagesPerSite": 3,
  "respectRobots": true,
  "includeTechnology": true
}
```

The input is bounded: 1–1,000 websites, 1–5 pages per site, 1–10 concurrent sites,
5–45 seconds per request and a minimum per-site pause of 0.25–10 seconds.
`startUrls` and `webUrls` are accepted aliases for programmatic input.

## Cloud build and smoke test

1. Authenticate with `apify login` in your own terminal.
2. From this project's root, run `apify push` to create/update the Actor and build
   its container. The `.actor/actor.json` file references the root Dockerfile,
   schemas and README; it contains no account token.
3. Set the Actor's default run timeout to **300 seconds** and memory to **512 MB**
   in Apify Console. Actor metadata sets the memory range; the platform run
   options control timeout. Increase timeout only when a measured batch needs it.
4. Run a one-site input you own or are allowed to access. Confirm a successful
   dataset row and accessible CSV/JSON outputs before increasing the batch.
5. Test a failed URL and a robots-blocked URL: they must appear in diagnostics
   without a billable website row.

The [Actor definition documentation](https://docs.apify.com/actors/development/actor-definition/actor-json)
describes schema and build metadata. Successful deployment does not by itself
publish the Actor to the Store or configure monetization.

## Output

The default dataset contains successful results. The default key-value store has:

| Key | Content |
| --- | --- |
| `RESULTS` | JSON list of saved successful website rows |
| `results.csv` | Spreadsheet-safe CSV of those same rows |
| `SUMMARY` | Counts, budget-stop state and billing information |
| `DIAGNOSTICS` | Failed/skipped websites and request diagnostics |
| `OUTPUT` | Complete report including the above result rows |

The output schema links these files in the Actor run's Output tab. The dataset
has contact and evidence/technology views. CSV escapes formula-like values;
JSON preserves source observations. Protect any exported contacts appropriately.

## Optional pay-per-event setup

The code uses the event key **`website-enriched`**, once per persisted successful
website row. A proposed launch price is **$0.003 per website** ($3 per 1,000).
This is a pricing proposal, not a live tariff, an earnings forecast or a promise
of demand. Configure and verify the actual price in Apify Console before launch.

In the Actor's Monetization settings choose pay-per-event and create:

| Field | Proposed value |
| --- | --- |
| Event key | `website-enriched` |
| Display title | Business website enriched |
| Unit price | `$0.003` |
| Billing trigger | Successful website result saved to the default dataset |

Do not add an initialization fee or duplicate dataset-item fee accidentally.
The supplied code does not charge for failed requests or diagnostics. Keep any
platform synthetic event price at zero unless you deliberately disclose a
different pricing model to customers. Apify's current platform terms, your
eligibility and Console settings determine whether selling is available.

The implementation uses `Actor.push_data(...,
charged_event_name='website-enriched')` in pay-per-event runs. The SDK persists
the permitted row before recording its explicit charge, including the run's
remaining spending allowance. It preflights the combined explicit/dataset-event
budget, reduces the crawl's site limit, and stops scheduling after a limit signal.
Only rows saved through this callback are included in exported results. A few
already-started requests may finish; they do not create additional charged rows.
Other pricing modes use plain dataset writes without explicit event charges.

See the official [Python SDK pay-per-event guide](https://docs.apify.com/sdk/python/docs/concepts/pay-per-event)
and [monetization documentation](https://docs.apify.com/actors/monetize).
For local billing simulation only, use `ACTOR_TEST_PAY_PER_EVENT=true` and set
`ACTOR_MAX_TOTAL_CHARGE_USD`. The SDK uses a **$1 default simulated event price**
when no platform pricing is supplied, so this does not simulate the proposed
$0.003 price. Do not set the test flag in cloud production. Inspect the local
charging-log dataset and confirm dataset item count matches explicit events.

## Before public launch

Measure results on a small set of varied business sites, inspect each source
URL and test very small spending caps. Static HTML parsing cannot execute
JavaScript or bypass login/CAPTCHA. Technology signatures are incomplete, and
a published contact is not proof of ownership, consent or deliverability.
The Actor does not crawl social networks for personal profiles or circumvent
access controls. Use it for legitimate business research on sites you may access.

Store publication, a screenshot, clear limitations, a realistic sample output,
support responsiveness and repeatable quality matter more than just uploading
code. Revenue requires customers and leaves platform costs, platform revenue
share, receiving fees and taxes to account for. No revenue has been generated by
the project merely being built or deployed.

