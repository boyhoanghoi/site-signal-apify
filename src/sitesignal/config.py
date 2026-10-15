"""Validated limits for both the local CLI and the Apify Actor."""

from dataclasses import dataclass
import math
from typing import Any
from urllib.parse import urlsplit, urlunsplit


def _url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Each website must be a non-empty URL string or an object with a url field.")
    value = value.strip()
    if "://" not in value:
        value = "https://" + value
    try:
        parts = urlsplit(value)
        port = parts.port
        hostname = parts.hostname
        if parts.scheme.lower() not in {"http", "https"} or not hostname:
            raise ValueError("Only HTTP(S) website URLs are supported.")
        if parts.username is not None or parts.password is not None:
            raise ValueError("Website URLs must not contain credentials.")
        if any(c.isspace() or ord(c) < 32 for c in value):
            raise ValueError("Website URLs must not contain whitespace or control characters.")
        hostname = hostname.encode("idna").decode("ascii").lower()
        # Preserve IPv6 syntax here. The crawler separately rejects non-public IPs.
        authority = f"[{hostname}]" if ":" in hostname else hostname
        if port is not None:
            authority += f":{port}"
        return urlunsplit((parts.scheme.lower(), authority, parts.path or "/", parts.query, ""))
    except (UnicodeError, ValueError) as exc:
        raise ValueError(f"Invalid website URL {value!r}: {exc}") from None


def _pick(data: dict[str, Any], camel: str, snake: str, default: Any) -> Any:
    return data.get(camel, data.get(snake, default))


def _number(value: Any, name: str, low: float, high: float, *, integer: bool = False) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be {'an integer' if integer else 'a number'} between {low:g} and {high:g}.")
    if not math.isfinite(value) or not low <= value <= high or (integer and int(value) != value):
        raise ValueError(f"{name} must be {'an integer' if integer else 'a number'} between {low:g} and {high:g}.")
    return int(value) if integer else float(value)


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be true or false.")
    return value


@dataclass(frozen=True)
class RunConfig:
    websites: tuple[str, ...]
    max_pages_per_site: int = 3
    max_sites: int = 100
    concurrency: int = 5
    timeout_seconds: float = 20.0
    respect_robots: bool = True
    min_delay_seconds: float = 0.5
    include_technology: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RunConfig":
        if not isinstance(data, dict):
            raise ValueError("Input must be a JSON object.")
        supported = {
            "websites", "webUrls", "startUrls", "maxPagesPerSite", "max_pages_per_site",
            "maxSites", "max_sites", "concurrency", "timeoutSeconds", "timeout_seconds",
            "respectRobots", "respect_robots", "minDelaySeconds", "min_delay_seconds",
            "includeTechnology", "include_technology",
        }
        unknown = [str(key) for key in data if key not in supported and not str(key).startswith("__")]
        if unknown:
            raise ValueError("Unknown input field(s): " + ", ".join(sorted(unknown)))
        websites = data.get("websites", data.get("webUrls", data.get("startUrls")))
        if not isinstance(websites, list) or not websites:
            raise ValueError("websites must be a non-empty list of URLs or {url: ...} objects.")
        if len(websites) > 1000:
            raise ValueError("Provide at most 1,000 websites per run.")
        normalized = tuple(dict.fromkeys(_url(item.get("url") if isinstance(item, dict) else item) for item in websites))
        return cls(
            websites=normalized,
            max_pages_per_site=_number(_pick(data, "maxPagesPerSite", "max_pages_per_site", 3), "maxPagesPerSite", 1, 5, integer=True),
            max_sites=_number(_pick(data, "maxSites", "max_sites", 100), "maxSites", 1, 1000, integer=True),
            concurrency=_number(data.get("concurrency", 5), "concurrency", 1, 10, integer=True),
            timeout_seconds=_number(_pick(data, "timeoutSeconds", "timeout_seconds", 20), "timeoutSeconds", 5, 45),
            respect_robots=_boolean(_pick(data, "respectRobots", "respect_robots", True), "respectRobots"),
            min_delay_seconds=_number(_pick(data, "minDelaySeconds", "min_delay_seconds", 0.5), "minDelaySeconds", 0.25, 10),
            include_technology=_boolean(_pick(data, "includeTechnology", "include_technology", True), "includeTechnology"),
        )

