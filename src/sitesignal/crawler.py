"""Bounded public-web crawler. No browser, private-network access, or bypasses."""
from __future__ import annotations

import asyncio
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import ipaddress
import socket
import time
from typing import Awaitable, Callable
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import aiohttp
from aiohttp.abc import AbstractResolver

from .config import RunConfig
from .extract import extract_page

USER_AGENT = "SiteSignalBot/0.1 (+https://github.com/boyhoanghoi/site-signal-apify)"
ROBOTS_AGENT = "SiteSignalBot"
MAX_BYTES = 2 * 1024 * 1024


class FetchError(Exception):
    def __init__(self, status: str, message: str, http_status: int | None = None):
        super().__init__(message)
        self.status = status
        self.http_status = http_status


def public_ip(address: str) -> bool:
    try:
        ip = ipaddress.ip_address(address.split("%")[0])
        mapped = getattr(ip, "ipv4_mapped", None)
        return bool(ip.is_global and (mapped is None or mapped.is_global))
    except ValueError:
        return False


def validate_url(value: str) -> str:
    """Validate literal targets; PublicResolver also checks the actual DNS answer."""
    try:
        if not isinstance(value, str) or len(value) > 4096:
            raise ValueError("Invalid or excessively long URL.")
        p = urlsplit(value)
        if p.scheme not in {"http", "https"} or not p.hostname:
            raise ValueError("Only HTTP(S) URLs are supported.")
        if p.username is not None or p.password is not None:
            raise ValueError("URL credentials are not supported.")
        if any(c.isspace() or ord(c) < 32 for c in value):
            raise ValueError("URL contains whitespace or control characters.")
        host = p.hostname.rstrip(".").encode("idna").decode("ascii").lower()
        if p.port not in {None, 80, 443}:
            raise ValueError("Only standard web ports 80 and 443 are allowed.")
        if "%" in host or host == "localhost" or host.endswith((".localhost", ".local", ".internal", ".lan")):
            raise ValueError("Local network destinations are not allowed.")
        try:
            ipaddress.ip_address(host)
        except ValueError:
            # aiohttp treats any all-digit/dot hostname as an IP literal and
            # bypasses its resolver. Reject legacy octal/shortened spellings.
            if host.replace(".", "").isdigit():
                raise ValueError("IP addresses must use canonical public IP syntax.")
            if "." not in host or any(not label for label in host.split(".")):
                raise ValueError("A public fully qualified hostname is required.")
        else:
            if not public_ip(host):
                raise ValueError("Private or reserved network destinations are not allowed.")
        authority = f"[{host}]" if ":" in host else host
        if p.port is not None:
            authority += f":{p.port}"
        return urlunsplit((p.scheme, authority, p.path or "/", p.query, ""))
    except (ValueError, UnicodeError) as exc:
        raise FetchError("invalid_url", str(exc)) from None


def domain_key(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host


def same_site(a: str, b: str) -> bool:
    return domain_key(a) == domain_key(b)


class PublicResolver(AbstractResolver):
    """Resolve once and connect only to the checked addresses (no DNS TOCTOU)."""
    def __init__(self):
        self._resolver = aiohttp.ThreadedResolver()

    async def resolve(self, host: str, port: int = 0, family: int = socket.AF_INET):
        answers = await self._resolver.resolve(host, port, family)
        if not answers or any(not public_ip(a["host"]) for a in answers):
            raise OSError("DNS returned a private or reserved address; request blocked.")
        return answers

    async def close(self):
        await self._resolver.close()


@dataclass
class Page:
    url: str
    text: str
    status: int
    content_type: str


class SafeHttpClient:
    def __init__(self, config: RunConfig):
        self.config = config
        self.session: aiohttp.ClientSession | None = None
        self._last_request: dict[str, float] = {}
        self._host_locks = defaultdict(asyncio.Lock)
        self._robots_locks = defaultdict(asyncio.Lock)
        self._robots: dict[str, RobotFileParser] = {}
        self._crawl_delays: dict[str, float] = {}
        self.requests = 0

    async def __aenter__(self):
        self._resolver = PublicResolver()
        connector = aiohttp.TCPConnector(
            resolver=self._resolver, use_dns_cache=False,
            limit=self.config.concurrency + 2, family=socket.AF_UNSPEC,
        )
        self.session = aiohttp.ClientSession(
            connector=connector, timeout=aiohttp.ClientTimeout(total=self.config.timeout_seconds),
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,text/plain;q=0.8"},
            cookie_jar=aiohttp.DummyCookieJar(), trust_env=False,
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
        await self._resolver.close()

    async def _pace(self, url: str):
        host = urlsplit(url).netloc
        async with self._host_locks[host]:
            delay = max(self.config.min_delay_seconds, self._crawl_delays.get(host, 0))
            await asyncio.sleep(max(0, self._last_request.get(host, 0) + delay - time.monotonic()))
            self._last_request[host] = time.monotonic()

    async def allowed(self, url: str) -> bool:
        p = urlsplit(url)
        origin = f"{p.scheme}://{p.netloc}"
        async with self._robots_locks[origin]:
            if origin not in self._robots:
                parser = RobotFileParser(origin + "/robots.txt")
                try:
                    page = await self.fetch(origin + "/robots.txt", check_robots=False)
                except FetchError as exc:
                    if exc.http_status in {404, 410}:
                        parser.parse([])
                    elif exc.http_status in {401, 403}:
                        parser.parse(["User-agent: *", "Disallow: /"])
                    else:
                        # Do not silently crawl when the site's rules cannot be read.
                        raise FetchError("robots_unavailable", "Could not read robots.txt; skipped conservatively.") from None
                else:
                    # Robots rules are authoritative regardless of a site's
                    # mistaken MIME type. HTML-only branded 404 lines are ignored
                    # by the robots parser without discarding valid directives.
                    parser.parse(page.text.splitlines())
                delay = parser.crawl_delay(ROBOTS_AGENT) or parser.crawl_delay("*") or 0
                if delay > 30:
                    raise FetchError("robots_disallowed", "Published crawl delay exceeds this tool's bounded runtime.")
                self._crawl_delays[p.netloc] = float(delay)
                self._robots[origin] = parser
            return self._robots[origin].can_fetch(ROBOTS_AGENT, url)

    async def fetch(self, url: str, *, check_robots: bool = True, scope_url: str | None = None) -> Page:
        assert self.session is not None
        for redirect in range(6):
            url = validate_url(url)
            if scope_url is not None and not same_site(scope_url, url):
                raise FetchError("offsite_redirect", "Contact-page redirect leaves the selected website.")
            if check_robots and self.config.respect_robots and not await self.allowed(url):
                raise FetchError("robots_disallowed", "The website's robots.txt disallows this page.")
            await self._pace(url)
            try:
                self.requests += 1
                async with self.session.get(url, allow_redirects=False) as response:
                    status = response.status
                    if status in {301, 302, 303, 307, 308}:
                        location = response.headers.get("Location")
                        if not location:
                            raise FetchError("http_error", "Redirect has no Location header.", status)
                        if not check_robots and not same_site(url, urljoin(url, location)):
                            raise FetchError("robots_unavailable", "robots.txt redirected to another website.")
                        url = urljoin(url, location)
                        continue
                    if status in {401, 403, 429}:
                        raise FetchError("blocked", "Website denied access or requested a lower request rate.", status)
                    if status >= 400:
                        raise FetchError("http_error", f"Website returned HTTP {status}.", status)
                    content_type = response.headers.get("Content-Type", "").lower()
                    if content_type and not any(t in content_type for t in ("text/", "application/xhtml+xml", "application/xml")):
                        raise FetchError("unsupported_content", "Response is not a supported text/HTML page.", status)
                    chunks: list[bytes] = []
                    size = 0
                    async for chunk in response.content.iter_chunked(65536):
                        size += len(chunk)
                        if size > MAX_BYTES:
                            raise FetchError("response_too_large", "Page exceeds the 2 MiB decoded response limit.")
                        chunks.append(chunk)
                    charset = response.charset or "utf-8"
                    try:
                        text = b"".join(chunks).decode(charset, errors="replace")
                    except LookupError:
                        text = b"".join(chunks).decode("utf-8", errors="replace")
                    return Page(str(response.url), text, status, content_type)
            except asyncio.TimeoutError:
                raise FetchError("timeout", "Website request timed out.") from None
            except (aiohttp.ClientError, OSError) as exc:
                raise FetchError("network_error", f"Public website connection failed ({type(exc).__name__}).") from None
        raise FetchError("redirect_limit", "Website exceeded five redirects.")


def merge_pages(seed: str, pages: list[tuple[Page, dict]], warnings: list[str], *, include_technology: bool) -> dict:
    first_page, first = pages[0]
    result = {
        "url": seed, "finalUrl": first_page.url, "domain": domain_key(first_page.url),
        "companyName": first.get("companyName", ""), "title": first.get("title", ""),
        "description": first.get("description", ""), "emails": [], "phones": [],
        "socials": {}, "contactFormUrls": [], "contactPageUrls": [], "technologies": [], "evidence": [],
        "language": first.get("language", ""), "jsonLdTypes": [],
        "pagesVisited": [p.url for p, _ in pages], "pagesChecked": len(pages),
        "observedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "success", "warnings": warnings,
    }
    email_spelling: dict[str, str] = {}
    for _, data in pages:
        if not result["companyName"] and data.get("companyName"):
            result["companyName"] = data["companyName"]
        for email in data.get("emails", []):
            email_spelling.setdefault(email.casefold(), email)
        for key in ("phones", "contactFormUrls", "contactPageUrls", "jsonLdTypes"):
            result[key] = sorted(set(result[key]) | set(data.get(key, [])))
        for platform, urls in data.get("socials", {}).items():
            result["socials"][platform] = sorted(set(result["socials"].get(platform, [])) | set(urls))
        for e in data.get("evidence", []):
            if not include_technology and e.get("type") == "technology":
                continue
            if e.get("type") == "email":
                e = {**e, "value": email_spelling.get(e["value"].casefold(), e["value"])}
            if e not in result["evidence"]:
                result["evidence"].append(e)
        if include_technology:
            for tech in data.get("technologies", []):
                if not any(t["name"] == tech["name"] and t["sourceUrl"] == tech["sourceUrl"] for t in result["technologies"]):
                    result["technologies"].append(tech)
    result["emails"] = sorted(email_spelling.values(), key=lambda value: (value.casefold(), value))
    result["hasPublicEmail"] = bool(result["emails"])
    result["hasContactForm"] = bool(result["contactFormUrls"])
    return result


def _check_challenge(page: Page) -> None:
    lower = page.text[:200000].lower()
    if any(s in lower for s in ("<title>just a moment", "<title>access denied", "<title>attention required!", "<title>verify you are human")):
        raise FetchError("blocked", "A browser challenge was returned; this tool does not bypass it.", page.status)


async def crawl_site(url: str, config: RunConfig, client: SafeHttpClient) -> dict:
    first = await client.fetch(url)
    _check_challenge(first)
    data = extract_page(first.text, first.url)
    pages = [(first, data)]
    pending = list(data.get("contactPageUrls", []))
    visited = {first.url, url}
    warnings: list[str] = []
    page_diagnostics = [{"url": url, "finalUrl": first.url, "status": "success", "httpStatus": first.status}]
    attempts = 1
    while pending and attempts < config.max_pages_per_site:
        candidate = pending.pop(0)
        if candidate in visited or not same_site(first.url, candidate):
            continue
        visited.add(candidate)
        attempts += 1
        page = None
        try:
            candidate = validate_url(candidate)
            # Every redirect is checked for robots and public DNS by the transport.
            page = await client.fetch(candidate, scope_url=first.url)
            visited.add(page.url)
            if not same_site(first.url, page.url):
                warnings.append("A contact page redirected outside this website and was not extracted.")
                page_diagnostics.append({"url": candidate, "finalUrl": page.url, "status": "offsite_redirect",
                                         "httpStatus": page.status, "message": warnings[-1]})
                continue
            if page.url in {p.url for p, _ in pages}:
                page_diagnostics.append({"url": candidate, "finalUrl": page.url, "status": "duplicate_page_redirect",
                                         "httpStatus": page.status, "message": "Redirect led to an already extracted page."})
                continue
            _check_challenge(page)
            extracted = extract_page(page.text, page.url)
            pages.append((page, extracted))
            page_diagnostics.append({"url": candidate, "finalUrl": page.url, "status": "success", "httpStatus": page.status})
            pending.extend(extracted.get("contactPageUrls", []))
        except FetchError as exc:
            warnings.append(f"Contact page skipped: {exc.status}.")
            diagnostic = {"url": candidate, "status": exc.status, "message": str(exc), "httpStatus": exc.http_status}
            if page is not None:
                diagnostic.update({"finalUrl": page.url, "httpStatus": page.status})
            page_diagnostics.append(diagnostic)
    result = merge_pages(url, pages, warnings, include_technology=config.include_technology)
    result["pagesAttempted"] = attempts
    result["pageDiagnostics"] = page_diagnostics
    result["contactPageLimitReached"] = attempts >= config.max_pages_per_site and any(
        candidate not in visited and same_site(first.url, candidate) for candidate in pending
    )
    return result


async def crawl_sites(
    config: RunConfig,
    on_result: Callable[[dict], Awaitable[bool]] | None = None,
    *, client_factory=SafeHttpClient,
) -> dict:
    started = time.monotonic()
    results, diagnostics = [], []
    unique, seen = [], set()
    for value in config.websites:
        key = domain_key(value)
        if key not in seen:
            seen.add(key)
            unique.append(value)
    selected = unique[:config.max_sites]
    semaphore = asyncio.Semaphore(config.concurrency)
    output_lock = asyncio.Lock()
    completed_domains: set[str] = set()
    stop = asyncio.Event()
    async with client_factory(config) as client:
        async def worker(url: str):
            async with semaphore:
                if stop.is_set():
                    return
                try:
                    row = await asyncio.wait_for(
                        crawl_site(validate_url(url), config, client),
                        timeout=min(240, (config.max_pages_per_site + 2) * config.timeout_seconds + 30),
                    )
                    async with output_lock:
                        if stop.is_set():
                            return
                        if row["domain"] in completed_domains:
                            diagnostics.append({"url": url, "status": "duplicate_redirect", "message": "Another input already produced this final website; no additional charge.", "finalUrl": row["finalUrl"]})
                            return
                        if on_result is not None and not await on_result(row):
                            stop.set()
                            return
                        results.append(row)
                        completed_domains.add(row["domain"])
                except asyncio.TimeoutError:
                    diagnostics.append({"url": url, "status": "timeout", "message": "Website processing time limit reached."})
                except FetchError as exc:
                    diagnostics.append({"url": url, "status": exc.status, "message": str(exc), "httpStatus": exc.http_status})
        await asyncio.gather(*(worker(url) for url in selected))
        requests = client.requests
    results.sort(key=lambda row: row["url"])
    diagnostics.sort(key=lambda row: row["url"])
    return {
        "results": results, "diagnostics": diagnostics,
        "summary": {
            "inputCount": len(config.websites), "uniqueDomains": len(unique),
            "selectedDomains": len(selected), "completedDomains": len(results),
            "failedDomains": len(diagnostics), "duplicateDomainsSkipped": len(config.websites) - len(unique),
            "omittedByMaxSites": max(0, len(unique) - len(selected)),
            "unprocessedAfterLimit": len(selected) - len(results) - len(diagnostics),
            "emailDomains": sum(bool(r["emails"]) for r in results),
            "duplicateFinalDomainsSkipped": sum(d["status"] == "duplicate_redirect" for d in diagnostics),
            "statusCounts": dict(Counter(d["status"] for d in diagnostics)),
            "requests": requests, "durationSeconds": round(time.monotonic() - started, 3),
            "stoppedByResultLimit": stop.is_set(),
        },
    }
