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

The Actor is currently **private**, with active pay-per-event pricing of
**$0.003 per successful website**. Paid-mode cloud smoke testing passed.
Publication is blocked by the API error **store-terms-not-accepted**: the owner
must personally read and accept Store terms in Publishing. The Store listing
URL is not advertised as live.

Payout billing details have been saved. The owner reports completing identity
verification; Console shows **identity verification pending**, with an indicated
review time of 1–2 business days. Submission is not approval, and payouts remain
unavailable until verification is approved.

Official path to change payout details: Development → Insights → Payouts →
Billing details → Edit. If the verification profile cannot be changed, contact
Apify support to reset the profile as an individual developer. The owner must
also read/accept any Store terms that Apify presents.

Reference: https://docs.apify.com/actors/publishing/monetize/monthly-payouts

## Activation after account details are correct

The accepted platform price is `$0.003` per successful website ($3/1,000), one
`website-enriched` event only. Files `.actor/launch-settings.json`,
`.actor/launch-pricing.json` and `.actor/launch-public.json` contain the reviewed
metadata, launch price and publication flag. Pricing is already active: do not
reapply or change pricing merely to publish. Do not enable an additional paid
dataset/start event. Failed/blocked/duplicate-redirect websites are diagnostics.

The authenticated deployment helper can apply these JSON files; it uses the
official CLI's OS-keyring login and never stores a token in this repository:

```text
python scripts/apify_control.py configure --file .actor/launch-settings.json
python scripts/apify_control.py configure --file .actor/launch-public.json
```

For that helper, `APIFY_CLI_ENTRY` selects the installed official Apify CLI's
`dist/apify.js` entrypoint and Node must be on PATH. Alternatively use Console
Publishing → Monetization. Check the actual accepted price and public Store
page. Paid-mode cloud run `ovMKN7v00twIRmfj0` succeeded: two inputs, one saved
website, one invalid/private URL diagnostic, and exactly one `website-enriched`
charged event. This owner test is not customer revenue. The API publication
attempt returned HTTP 403 with `store-terms-not-accepted`; it was not bypassed.

Only after Store publication succeeds, set `actorUrl` in `dist/config.js` to
the verified public listing and redeploy the website. Keep its proposed-price
language until the real price is accepted. Owner-run tests are not sales.

Acquisition drafts and the first-revenue plan are in [LAUNCH_COPY.md](LAUNCH_COPY.md)
and [FIRST_5_DOLLARS.md](FIRST_5_DOLLARS.md). No promotional messages have been sent.
