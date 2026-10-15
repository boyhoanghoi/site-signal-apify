"""Local and Actor export helpers. JSON is lossless; spreadsheet CSV is escaped."""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path


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
    stream = io.StringIO(newline="")
    fields = ["url", "finalUrl", "domain", "companyName", "title", "description", "emails", "phones",
              "socials", "contactFormUrls", "technologies", "pagesChecked", "pagesVisited", "observedAt", "status", "evidence", "warnings"]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    for row in results:
        writer.writerow({key: spreadsheet_cell(row.get(key)) for key in fields})
    return stream.getvalue()


def export_results(report: dict, directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, data in (("results", report["results"]), ("diagnostics", report["diagnostics"]), ("summary", report["summary"])):
        (directory / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (directory / "results.csv").write_text("\ufeff" + results_csv(report["results"]), encoding="utf-8", newline="")

