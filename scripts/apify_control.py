"""Operate our Actor through the authenticated official Apify CLI.

No tokens are read, printed, or passed as arguments. APIFY_CLI_ENTRY optionally
selects a local apify-cli JS entrypoint; otherwise `apify` must be on PATH.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ACTOR = "KgxuXmLMsWUuA8Jkw"


def request(method, endpoint, body=None, params=None):
    entry = os.environ.get("APIFY_CLI_ENTRY")
    if entry:
        node = shutil.which("node")
        if not node:
            raise RuntimeError("Node.js is required by Apify CLI.")
        command = [node, str(Path(__file__).with_name("apify-api.mjs"))]
        process = subprocess.run(command, input=json.dumps({"method": method, "endpoint": endpoint, "body": body, "params": params}),
                                 capture_output=True, encoding="utf-8", errors="replace", timeout=90)
        if process.returncode:
            raise RuntimeError((process.stderr or process.stdout)[-6000:])
        data = json.loads(process.stdout)
        return data.get("data", data) if isinstance(data, dict) else data
    else:
        executable = shutil.which("apify")
        if not executable:
            raise RuntimeError("Install Apify CLI and run `apify login` first.")
        command = [executable]
    command += ["api", method, endpoint]
    if body is not None:
        command += ["--body", "-"]
    if params:
        command += ["--params", json.dumps(params)]
    process = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                             capture_output=True, encoding="utf-8", errors="replace", timeout=90)
    if process.returncode:
        # API error text never includes the OS-keyring credential in this flow.
        raise RuntimeError((process.stderr or process.stdout)[-6000:])
    data = json.loads(process.stdout)
    return data.get("data", data) if isinstance(data, dict) else data


def brief(data, keys):
    return {key: data.get(key) for key in keys}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["actor", "configure", "run", "run-status", "build-status", "sample", "record"])
    parser.add_argument("--id", default=ACTOR)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--key", default="SUMMARY")
    args = parser.parse_args()
    if args.action in {"actor", "configure"}:
        actor = request("PUT" if args.action == "configure" else "GET", f"actors/{args.id}",
                        json.loads(args.file.read_text(encoding="utf-8")) if args.action == "configure" else None)
        data = brief(actor, ["id", "name", "username", "title", "isPublic", "categories", "pricingInfos", "defaultRunOptions", "taggedBuilds", "pictureUrl"])
    elif args.action == "run":
        run = request("POST", f"actors/{args.id}/runs", json.loads(args.file.read_text(encoding="utf-8")),
                      {"memory": 512, "timeout": 180, "maxTotalChargeUsd": 0.05})
        data = brief(run, ["id", "status", "defaultDatasetId", "defaultKeyValueStoreId", "buildId", "options"])
    elif args.action == "run-status":
        data = brief(request("GET", f"actor-runs/{args.id}"), ["id", "status", "statusMessage", "exitCode", "defaultDatasetId", "defaultKeyValueStoreId", "usageTotalUsd", "chargedEventCounts", "stats", "pricingInfo"])
    elif args.action == "build-status":
        data = brief(request("GET", f"actor-builds/{args.id}"), ["id", "status", "statusMessage", "usageTotalUsd", "finishedAt"])
    elif args.action == "sample":
        data = request("GET", f"datasets/{args.id}/items", params={"limit": 5, "clean": True})
    elif args.action == "record":
        data = request("GET", f"key-value-stores/{args.id}/records/{args.key}")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"saved": str(args.out), "type": type(data).__name__}))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
