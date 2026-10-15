# Launch handover

Checked 15 October 2026.

## Built and tested

- Repository: https://github.com/boyhoanghoi/site-signal-apify
- Actor owner: `reliable_quatrain`
- Actor ID: `KgxuXmLMsWUuA8Jkw`
- Actor Console: https://console.apify.com/actors/KgxuXmLMsWUuA8Jkw
- Release build: `0.1.3`, successful live cloud run and saved exports.
- Website demo: https://sitesignal-business-enricher.yxinhhh18.chatgpt.site (owner-private preview).
- Local project: `apify_tools/site-signal`.
- Tests and benchmarks: [VALIDATION.md](VALIDATION.md).

## Still required before selling

The Actor is currently **private**, with **no active paid price**. The Store
listing URL is not advertised as live. The owner needs to complete accurate
payout billing details and any required identity verification directly in Apify.
If a company was entered accidentally, correct the legal-entity details before
verification; do not submit documents for a nonexistent company.

Official path to change payout details: Development → Insights → Payouts →
Billing details → Edit. If the verification profile cannot be changed, contact
Apify support to reset the profile as an individual developer. The owner must
also read/accept any Store terms that Apify presents.

Reference: https://docs.apify.com/actors/publishing/monetize/monthly-payouts

## Activation after account details are correct

The configured proposal is `$0.003` per successful website ($3/1,000), one
`website-enriched` event only. Files `.actor/launch-settings.json`,
`.actor/launch-pricing.json` and `.actor/launch-public.json` contain the reviewed
metadata, proposed price and publication flag. Do not enable an additional paid
dataset/start event. Failed/blocked/duplicate-redirect websites are diagnostics.

The authenticated deployment helper can apply these JSON files; it uses the
official CLI's OS-keyring login and never stores a token in this repository:

```text
python scripts/apify_control.py configure --file .actor/launch-settings.json
python scripts/apify_control.py configure --file .actor/launch-pricing.json
python scripts/apify_control.py configure --file .actor/launch-public.json
```

For that helper, `APIFY_CLI_ENTRY` selects the installed official Apify CLI's
`dist/apify.js` entrypoint and Node must be on PATH. Alternatively use Console
Publishing → Monetization. Check the actual accepted price and public Store
page; re-run a one-site spending-limit smoke test in paid mode. The existing
unit tests exercise billing limits, but paid platform billing has not been
verified while account setup is incomplete.

Only after Store publication succeeds, set `actorUrl` in `dist/config.js` to
the verified public listing and redeploy the website. Keep its proposed-price
language until the real price is accepted. Owner-run tests are not sales.

Acquisition drafts and the first-revenue plan are in [LAUNCH_COPY.md](LAUNCH_COPY.md)
and [FIRST_5_DOLLARS.md](FIRST_5_DOLLARS.md). No promotional messages have been sent.
