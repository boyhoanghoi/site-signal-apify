"""Apify entry point. Billing is attached only to persisted successful results."""

import asyncio
from dataclasses import replace
from typing import Any

from .config import RunConfig


BILLABLE_EVENT = "website-enriched"


async def run_actor() -> None:
    # Apify is an optional dependency for the local CLI and pure extraction code.
    from apify import Actor

    from .crawler import crawl_sites
    from .output import contact_records, contacts_csv, crm_company_records, crm_companies_csv, results_csv

    async with Actor:
        raw_input = await Actor.get_input() or {}
        try:
            config = RunConfig.from_dict(raw_input)
        except ValueError as exc:
            message = f"Invalid input: {exc}"
            Actor.log.error(message)
            await Actor.set_value("OUTPUT", {"error": message, "results": [], "diagnostics": []})
            Actor.exit_code = 1
            Actor.status_message = message
            return

        manager = Actor.get_charging_manager()
        pricing = manager.get_pricing_info()
        is_ppe = pricing.is_pay_per_event
        if is_ppe and Actor.configuration.is_at_home and BILLABLE_EVENT not in pricing.per_event_prices:
            message = f"Billing event {BILLABLE_EVENT!r} is missing from the Actor's pay-per-event configuration."
            Actor.log.error(message)
            await Actor.set_value("OUTPUT", {"error": message, "results": [], "diagnostics": []})
            Actor.exit_code = 1
            Actor.status_message = message
            return
        saved: list[dict[str, Any]] = []
        budget_reached = False

        # Avoid starting an expensive full run if the declared budget cannot fund
        # even one persisted website result. The SDK also checks every write.
        if is_ppe:
            available = manager.compute_push_data_limit(
                config.max_sites, BILLABLE_EVENT, is_default_dataset=True,
            )
            if available < config.max_sites:
                budget_reached = available == 0
                config = replace(config, max_sites=max(available, 1))

        async def save_result(row: dict[str, Any]) -> bool:
            nonlocal budget_reached
            if is_ppe and manager.compute_push_data_limit(1, BILLABLE_EVENT, is_default_dataset=True) < 1:
                budget_reached = True
                return False
            # The SDK persists the dataset row before charging, and coordinates
            # synthetic dataset events and the explicit event under one lock.
            if is_ppe:
                charge = await Actor.push_data(row, charged_event_name=BILLABLE_EVENT)
                # charge_count is 1 for a successfully saved explicit event,
                # including zero-priced events. A zero count means no paid row.
                if charge.charged_count > 0:
                    saved.append(row)
                if charge.event_charge_limit_reached or charge.charged_count == 0:
                    budget_reached = True
                    # The crawler's False means "this row was not saved".
                    # Preserve the final affordable row; a subsequent callback
                    # will fail the preflight before writing anything else.
                    return charge.charged_count > 0
            else:
                await Actor.push_data(row)
                saved.append(row)
            return True

        if budget_reached:
            report = {"results": [], "diagnostics": [], "summary": {
                "inputCount": len(config.websites), "completedDomains": 0,
                "failedDomains": 0, "requests": 0, "stoppedByResultLimit": True,
            }}
        else:
            report = await crawl_sites(config, on_result=save_result)

        # Only dataset rows actually saved through the charging-aware callback
        # appear in downloadable results. Failed URLs stay in diagnostics.
        report["results"] = saved
        summary = dict(report.get("summary", {}))
        summary.update({
            "savedResults": len(saved),
            "budgetLimitReached": budget_reached,
            "billingEvent": BILLABLE_EVENT if is_ppe else None,
            "chargedResults": manager.get_charged_event_count(BILLABLE_EVENT) if is_ppe else 0,
        })
        report["summary"] = summary
        await Actor.set_value("SUMMARY", summary)
        await Actor.set_value("DIAGNOSTICS", report.get("diagnostics", []))
        await Actor.set_value("RESULTS", saved)
        await Actor.set_value("results.csv", results_csv(saved), content_type="text/csv; charset=utf-8")
        # These are alternate views of saved websites, never extra billed items.
        contacts = contact_records(saved)
        companies = crm_company_records(saved)
        await Actor.set_value("CONTACTS", contacts)
        await Actor.set_value("CRM_COMPANIES", companies)
        await Actor.set_value("contacts.csv", contacts_csv(contacts), content_type="text/csv; charset=utf-8")
        await Actor.set_value("crm-companies.csv", crm_companies_csv(companies), content_type="text/csv; charset=utf-8")
        await Actor.set_value("OUTPUT", report)
        ending = " Budget limit reached." if budget_reached else ""
        Actor.status_message = f"Saved {len(saved)} enriched websites.{ending}"
        Actor.log.info(Actor.status_message)


def main() -> None:
    asyncio.run(run_actor())


if __name__ == "__main__":
    main()

