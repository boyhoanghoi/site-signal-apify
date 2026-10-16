"""Customer export checks: lossless evidence, company boundaries and safe CSV."""

import copy
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from sitesignal.output import contact_records, contacts_csv, crm_company_records, crm_companies_csv, export_results


def website(domain="acme-business.co"):
    return {
        "url": f"https://{domain}/", "finalUrl": f"https://{domain}/", "domain": domain,
        "companyName": "=Acme", "emails": ["Sales@acme-business.co", "sales@acme-business.co", "help@acme-business.co"],
        "phones": ["+12025550123"], "socials": {"linkedin": ["https://www.linkedin.com/company/acme-business"]},
        "contactFormUrls": [f"https://{domain}/contact"], "contactPageUrls": [f"https://{domain}/contact"],
        "technologies": [{"name": "WordPress"}, {"name": "WordPress"}],
        "observedAt": "2026-10-16T00:00:00Z",
        "evidence": [
            {"type": "email", "value": "sales@acme-business.co", "sourceUrl": f"https://{domain}/", "method": "mailto"},
            {"type": "email", "value": "Sales@acme-business.co", "sourceUrl": f"https://{domain}/contact", "method": "visible-text"},
            {"type": "email", "value": "help@acme-business.co", "sourceUrl": f"https://{domain}/contact", "method": "mailto"},
            {"type": "phone", "value": "+12025550123", "sourceUrl": f"https://{domain}/contact", "method": "tel"},
            {"type": "email", "value": "not-retained@acme-business.co", "sourceUrl": f"https://{domain}/", "method": "mailto"},
        ],
    }


class ExportTests(unittest.TestCase):
    def test_contact_records_dedupe_case_keep_all_sources_and_never_invent_evidence(self):
        original = website()
        before = copy.deepcopy(original)
        contacts = contact_records([original])
        self.assertEqual(original, before)
        self.assertEqual(len(contacts), 5)
        sales = next(row for row in contacts if row["value"] == "Sales@acme-business.co")
        self.assertEqual(sales["sourceUrls"], ["https://acme-business.co/", "https://acme-business.co/contact"])
        self.assertEqual(sales["methods"], ["mailto", "visible-text"])
        self.assertEqual(sales["verificationStatus"], "not_verified")
        social = next(row for row in contacts if row["type"] == "social")
        self.assertEqual(social["sourceUrls"], [])
        self.assertFalse(any(row["value"] == "not-retained@acme-business.co" for row in contacts))

    def test_shared_contact_is_not_merged_across_company_websites(self):
        contacts = contact_records([website(), website("second-business.co")])
        sales = [row for row in contacts if row["value"] == "Sales@acme-business.co"]
        self.assertEqual({row["domain"] for row in sales}, {"acme-business.co", "second-business.co"})
        self.assertEqual(sales[1]["sourceUrls"], ["https://second-business.co/", "https://second-business.co/contact"])

    def test_company_mapping_has_flat_contacts_and_sources_and_no_inferred_business_name(self):
        original = website()
        records = crm_company_records([original, {"url": "https://empty-business.co/"}])
        self.assertEqual(records[0]["email"], "help@acme-business.co")
        self.assertEqual(records[0]["emailSourceUrls"], "https://acme-business.co/contact")
        self.assertEqual(records[0]["phone"], "+12025550123")
        self.assertEqual(records[0]["linkedin"], "https://www.linkedin.com/company/acme-business")
        self.assertEqual(records[0]["technologyNames"], "WordPress")
        self.assertEqual(records[0]["emailCount"], 2)
        self.assertTrue(all(not isinstance(value, (dict, list)) for value in records[0].values()))
        self.assertEqual(records[1]["companyName"], "")
        self.assertEqual(records[1]["email"], "")

    def test_csv_formula_safety_does_not_mutate_lossless_json(self):
        companies = crm_company_records([website()])
        exported = list(csv.DictReader(io.StringIO(crm_companies_csv(companies))))[0]
        self.assertEqual(exported["companyName"], "'=Acme")
        self.assertEqual(exported["phone"], "'+12025550123")
        self.assertEqual(companies[0]["phone"], "+12025550123")
        contacts = contact_records([website()])
        flat = list(csv.DictReader(io.StringIO(contacts_csv(contacts))))
        self.assertEqual(next(row for row in flat if row["type"] == "phone")["value"], "'+12025550123")
        self.assertEqual(next(row for row in contacts if row["type"] == "phone")["value"], "+12025550123")

    def test_local_exports_have_same_saved_website_scope_and_empty_exports_have_headers(self):
        report = {"results": [website()], "diagnostics": [{"url": "https://failed-business.co/", "status": "blocked"}], "summary": {}}
        with tempfile.TemporaryDirectory() as directory:
            export_results(report, directory)
            files = {file.name for file in Path(directory).iterdir()}
            self.assertTrue({"crm-companies.json", "crm-companies.csv", "contacts.json", "contacts.csv"} <= files)
            contacts = json.loads((Path(directory) / "contacts.json").read_text(encoding="utf-8"))
            self.assertEqual(len(contacts), 5)
            self.assertNotIn("failed-business.co", (Path(directory) / "contacts.csv").read_text(encoding="utf-8-sig"))
        self.assertEqual(len(list(csv.DictReader(io.StringIO(crm_companies_csv([]))))), 0)
        self.assertIn("sourceUrls", contacts_csv([]).splitlines()[0])


if __name__ == "__main__":
    unittest.main()
