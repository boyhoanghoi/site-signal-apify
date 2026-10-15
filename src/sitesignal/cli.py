"""Small, explicit CLI; local runs never involve Apify billing."""
import argparse
import asyncio
import json
from pathlib import Path
import sys

from .config import RunConfig
from .crawler import crawl_sites
from .output import export_results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="sitesignal", description="Public company website contacts and technology evidence.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run = subparsers.add_parser("run", help="Enrich websites from an input JSON file.")
    run.add_argument("--input", type=Path, required=True, help="JSON with a websites array.")
    run.add_argument("--output", type=Path, default=Path("output"), help="Output directory, default: output.")
    args = parser.parse_args(argv)
    try:
        config = RunConfig.from_dict(json.loads(args.input.read_text(encoding="utf-8-sig")))
        report = asyncio.run(crawl_sites(config))
        export_results(report, args.output)
    except (ValueError, OSError) as exc:
        print(f"SiteSignal: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("SiteSignal: interrupted.", file=sys.stderr)
        return 130
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Exports: {args.output.resolve()}")
    return 0 if report["results"] else 1

