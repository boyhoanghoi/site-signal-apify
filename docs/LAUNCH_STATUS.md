# Launch handover

Checked 15 October 2026.

## Built and tested

- Repository: https://github.com/boyhoanghoi/site-signal-apify
- Actor owner: `reliable_quatrain`
- Actor ID: `KgxuXmLMsWUuA8Jkw`
- Actor Console: https://console.apify.com/actors/KgxuXmLMsWUuA8Jkw
- Public Actor: https://apify.com/reliable_quatrain/business-website-contact-tech-scraper
- Release build: `0.1.3`, successful live cloud run and saved exports.
- Website demo: https://sitesignal-business-enricher.yxinhhh18.chatgpt.site (owner-private preview).
- Local project: `apify_tools/site-signal`.
- Tests and benchmarks: [VALIDATION.md](VALIDATION.md).

## Published and monetized

The authenticated official API confirms **`isPublic: true`** for this Actor.
The owner's latest Console screenshot also shows **The Actor is published** and
**Monetization: Active**. The Store listing above can now be shared.

Pay-per-event pricing is active at **$0.003 per successful website**
(**$3/1,000**), using the single event **`website-enriched`**. Paid-mode cloud
smoke testing passed. Publication and billing are no longer setup blockers.
There is **no verified customer revenue yet**; owner-run tests are not sales.

## Payout verification remains pending

Payout billing details have been saved. The owner has submitted identity
verification; the latest Console screenshot shows **identity verification pending**,
with an indicated review time of **1–2 business days**. This is the review estimate
shown by Console, not a guaranteed completion date. Submission is not approval,
and payouts remain unavailable until verification is approved.

Official path to change payout details: Development → Insights → Payouts →
Billing details → Edit. If the verification profile cannot be changed, contact
Apify support to reset the profile as an individual developer. Review any future
account or terms notices in Console; the earlier publication blocker is resolved.

The current published payout guide lists a **$20 PayPal/Wise minimum** and
normally issues payouts on **days 21–25** of the month. Verification approval,
eligible profit and the minimum threshold are separate from publication.

Reference: https://docs.apify.com/actors/publishing/monetize/monthly-payouts

## Reproducing deployment and checking future releases

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
Publishing → Monetization. Check the active price and public Store page after
any authorized configuration change. Paid-mode cloud run `ovMKN7v00twIRmfj0`
succeeded: two inputs, one saved
website, one invalid/private URL diagnostic, and exactly one `website-enriched`
charged event. This owner test is not customer revenue. The earlier
`store-terms-not-accepted` response has been resolved; a subsequent authenticated
official API check confirms publication.

The website remains an **owner-private preview**. Its configuration and price
copy now link to the verified public Actor at the active price. Hosting retains
the same website and audience. Do not describe that preview as publicly
accessible until its hosting visibility changes and is checked independently.
Store publication does not change website visibility.

Acquisition drafts and the first-revenue plan are in [LAUNCH_COPY.md](LAUNCH_COPY.md)
and [FIRST_5_DOLLARS.md](FIRST_5_DOLLARS.md). No promotional messages have been sent.
