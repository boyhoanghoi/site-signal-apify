"""Local and Actor export helpers. JSON is lossless; spreadsheet CSV is escaped."""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path


SOCIAL_PLATFORMS = ("linkedin", "facebook", "instagram", "x", "youtube", "tiktok", "github", "pinterest")


def contact_records(results: list[dict]) -> list[dict]:
    """Flatten retained contacts without inventing sources or merging businesses.

    Contacts shared by two domains intentionally remain two observations. Email
    identity follows the extractor's case-insensitive deduplication policy; the
    spelling retained on the website result is preserved in the export.
    """
    records = []
    for website in results:
        # Index once per website: the capped crawl can contain thousands of
        # evidence entries, so rescanning it for every contact is avoidable.
        evidence_index: dict[tuple[str, str], tuple[set[str], set[str]]] = {}
        for item in website.get("evidence", []):
            kind, value = item.get("type"), item.get("value", "")
            if kind not in {"email", "phone", "social", "contact-form"}:
                continue
            identity = value.casefold() if kind == "email" else value
            sources, methods = evidence_index.setdefault((kind, identity), (set(), set()))
            if item.get("sourceUrl"):
                sources.add(item["sourceUrl"])
            if item.get("method"):
                methods.add(item["method"])
        candidates = [("email", "", value) for value in website.get("emails", [])]
        candidates += [("phone", "", value) for value in website.get("phones", [])]
        candidates += [("social", platform, value)
                       for platform, values in sorted(website.get("socials", {}).items()) for value in values]
        candidates += [("contact-form", "", value) for value in website.get("contactFormUrls", [])]
        seen = set()
        for kind, platform, value in candidates:
            identity = value.casefold() if kind == "email" else value
            marker = kind, platform, identity
            if marker in seen:
                continue
            seen.add(marker)
            sources, methods = evidence_index.get((kind, identity), (set(), set()))
            records.append({
                "website": website.get("finalUrl", website.get("url", "")),
                "domain": website.get("domain", ""), "companyName": website.get("companyName", ""),
                "type": kind, "platform": platform, "value": value,
                "sourceUrls": sorted(sources), "methods": sorted(methods),
                "observedAt": website.get("observedAt", ""), "verificationStatus": "not_verified",
            })
    return records


def crm_company_records(results: list[dict]) -> list[dict]:
    """One flat record per saved website for user-controlled CRM field mapping."""
    records = []
    for website in results:
        final_url = website.get("finalUrl", website.get("url", ""))
        company_contacts = contact_records([website])
        emails = sorted({item["value"] for item in company_contacts if item["type"] == "email"},
                        key=lambda value: (value.casefold(), value))
        phones = sorted({item["value"] for item in company_contacts if item["type"] == "phone"})
        email = emails[0] if emails else ""
        phone = phones[0] if phones else ""

        def source_urls(kind: str, value: str) -> str:
            return "; ".join(sorted({source for contact in company_contacts
                                     if contact["type"] == kind and contact["value"] == value
                                     for source in contact["sourceUrls"]}))

        row = {
            "companyName": website.get("companyName", ""), "domain": website.get("domain", ""),
            "website": final_url, "email": email, "emailSourceUrls": source_urls("email", email),
            "phone": phone, "phoneSourceUrls": source_urls("phone", phone),
            "emailCount": len(emails), "phoneCount": len(phones),
            "contactPageUrl": next(iter(website.get("contactPageUrls", [])), ""),
            "contactFormUrl": next(iter(website.get("contactFormUrls", [])), ""),
            "technologyNames": "; ".join(sorted({item["name"] for item in website.get("technologies", [])})),
            "observedAt": website.get("observedAt", ""),
            "contactVerification": "not_verified",
        }
        for platform in SOCIAL_PLATFORMS:
            row[platform] = next(iter(sorted(website.get("socials", {}).get(platform, []))), "")
        records.append(row)
    return records


def spreadsheet_cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    value = str(value)
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value


def results_csv(results: list[dict]) -> str:
    fields = ["url", "finalUrl", "domain", "companyName", "title", "description", "emails", "phones",
              "socials", "contactPageUrls", "contactFormUrls", "technologies", "pagesChecked", "pagesAttempted",
              "contactPageLimitReached", "pagesVisited", "pageDiagnostics", "observedAt", "status", "evidence", "warnings"]
    return _csv(results, fields)


def _csv(records: list[dict], fields: list[str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    for row in records:
        writer.writerow({key: spreadsheet_cell(row.get(key)) for key in fields})
    return stream.getvalue()


def crm_companies_csv(records: list[dict]) -> str:
    return _csv(records, ["companyName", "domain", "website", "email", "emailSourceUrls", "phone", "phoneSourceUrls",
                          *SOCIAL_PLATFORMS, "contactPageUrl", "contactFormUrl", "technologyNames", "emailCount",
                          "phoneCount", "observedAt", "contactVerification"])


def contacts_csv(records: list[dict]) -> str:
    # CSV uses readable multi-value cells; JSON keeps these as arrays.
    flat = [{**row, "sourceUrls": "; ".join(row["sourceUrls"]), "methods": "; ".join(row["methods"])}
            for row in records]
    return _csv(flat, ["website", "domain", "companyName", "type", "platform", "value", "sourceUrls",
                        "methods", "observedAt", "verificationStatus"])


def export_results(report: dict, directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    contacts = contact_records(report["results"])
    companies = crm_company_records(report["results"])
    for name, data in (("results", report["results"]), ("diagnostics", report["diagnostics"]),
                       ("summary", report["summary"]), ("contacts", contacts), ("crm-companies", companies)):
        (directory / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name, csv_text in (("results", results_csv(report["results"])), ("contacts", contacts_csv(contacts)),
                           ("crm-companies", crm_companies_csv(companies))):
        (directory / f"{name}.csv").write_text("\ufeff" + csv_text, encoding="utf-8", newline="")

