"""Extract observed public contacts and their provenance from a single HTML page.

This module deliberately performs no network calls and never infers addresses from
people's names. Returned contacts have not been verified for reachability.
"""

import json
import re
from collections import Counter
from typing import Any, Iterator
from urllib.parse import parse_qs, unquote, urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup

from .models import PageResult
from .tech import detect_technologies


_EMAIL = re.compile(r"(?<![\w.!#$%&'*+/=?^`{|}~-])([A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9](?:[A-Z0-9.-]*[A-Z0-9])?\.[A-Z]{2,63})(?![\w-])", re.I)
_PLACEHOLDER_DOMAINS = {"example.com", "example.org", "example.net", "test.com", "test.org", "test.net", "domain.com", "yourdomain.com", "yourcompany.com", "company.com", "email.example", "website.com"}
_ASSET_SUFFIXES = {"png", "jpg", "jpeg", "gif", "svg", "webp", "ico", "css", "js", "map", "woff", "woff2", "ttf"}
_ORG_TYPES = {"organization", "localbusiness", "corporation", "store", "restaurant", "professionalservice", "medicalorganization", "educationalorganization", "ngo", "onlinebusiness", "onlinestore", "automotivebusiness", "financialservice", "realestateagent", "travelagency", "lodgingbusiness", "hotel", "legalservice", "dentist", "homeandconstructionbusiness", "sportsactivitylocation", "foodestablishment", "entertainmentbusiness", "healthandbeautybusiness", "employmentagency", "drycleaningorlaundry", "internetcafe", "library", "shoppingcenter", "hairsalon", "beautysalon", "day spa", "bakery", "barorpub", "cafeorcoffeeshop", "accountingservice", "insuranceagency", "electrician", "generalcontractor", "plumber", "roofingcontractor", "locksmith", "movingcompany", "hvacbusiness", "autorepair", "autodealer", "pharmacy", "hospital", "childcare", "preschool", "school", "collegeoruniversity"}

MAX_EMAILS = 100
MAX_PHONES = 50
MAX_SOCIALS_PER_PLATFORM = 10
MAX_CONTACT_PAGES = 50
MAX_CONTACT_FORMS = 50
MAX_EVIDENCE = 500


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _public_url(raw: str, base: str) -> str | None:
    if not isinstance(raw, str) or any(ord(c) < 32 for c in raw):
        return None
    try:
        parsed = urlsplit(urljoin(base, raw.strip()))
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            return None
        _ = parsed.port
        return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))
    except ValueError:
        return None


def _same_site(left: str, right: str) -> bool:
    try:
        a, b = urlsplit(left).hostname, urlsplit(right).hostname
        return bool(a and b and a.lower().removeprefix("www.") == b.lower().removeprefix("www."))
    except ValueError:
        return False


def normalize_email(raw: str) -> str | None:
    """Normalize domains while preserving the observed local-part spelling."""
    raw = unquote(raw).strip().strip("<>\"'.,; ")
    if not _EMAIL.fullmatch(raw) or len(raw) > 254:
        return None
    local, domain = raw.rsplit("@", 1)
    domain = domain.lower()
    if len(local) > 64 or local.startswith(".") or local.endswith(".") or ".." in raw:
        return None
    if domain in _PLACEHOLDER_DOMAINS or domain.endswith((".example", ".invalid", ".test", ".localhost", ".sentry.io")) or domain == "sentry.io":
        return None
    if any(not label or label.startswith("-") or label.endswith("-") for label in domain.split(".")):
        return None
    if domain.rsplit(".", 1)[-1] in _ASSET_SUFFIXES:
        return None
    return f"{local}@{domain}"


def normalize_phone(raw: str) -> str | None:
    raw = unquote(raw).strip()
    if raw.lower().startswith("tel:"):
        raw = raw[4:]
    raw = raw.split("?", 1)[0]
    extension = re.search(r"(?:;ext=|\bext\.?\s*|\bx\s*)(\d{1,6})\s*$", raw, re.I)
    suffix = ""
    if extension:
        suffix = " ext. " + extension.group(1)
        raw = raw[:extension.start()].strip()
    if not re.fullmatch(r"\+?[\d\s().-]+", raw):
        return None
    digits = re.sub(r"\D", "", raw)
    if not 7 <= len(digits) <= 15 or len(set(digits)) == 1:
        return None
    return ("+" if raw.startswith("+") else "") + digits + suffix


def normalize_social(raw: str, base: str) -> tuple[str, str] | None:
    absolute = _public_url(raw, base)
    if not absolute:
        return None
    parts = urlsplit(absolute)
    host = (parts.hostname or "").lower().removeprefix("www.").removeprefix("m.")
    path = [part for part in parts.path.split("/") if part]
    if not path:
        return None
    first = path[0].lower()
    query = ""
    platform: str
    if host in {"facebook.com", "fb.com"}:
        platform, host = "facebook", "www.facebook.com"
        if first in {"sharer.php", "sharer", "share.php", "share", "dialog", "plugins", "login", "l.php", "watch", "reel", "reels", "story.php", "photo.php", "permalink.php", "groups", "events"}:
            return None
        if first == "profile.php":
            identifier = parse_qs(parts.query).get("id", [""])[0]
            if not identifier.isdigit():
                return None
            query = "id=" + identifier
            path = ["profile.php"]
        elif first == "pages":
            if len(path) < 3:
                return None
            path = path[:3]
        else:
            path = path[:1]
    elif host in {"linkedin.com", "uk.linkedin.com", "vn.linkedin.com"}:
        platform, host = "linkedin", "www.linkedin.com"
        if first not in {"company", "school", "in"} or len(path) < 2:
            return None
        path = path[:2]
    elif host in {"twitter.com", "x.com", "mobile.twitter.com"}:
        platform, host = "x", "x.com"
        if first in {"intent", "share", "compose", "messages", "notifications", "search", "home", "i", "login", "signup", "explore", "hashtag", "settings", "tos", "privacy"} or not re.fullmatch(r"[A-Za-z0-9_]{1,15}", path[0]):
            return None
        path = path[:1]
    elif host == "instagram.com":
        platform, host = "instagram", "www.instagram.com"
        if first in {"p", "reel", "reels", "stories", "share", "web", "explore", "accounts", "direct", "about", "developer", "legal"}:
            return None
        path = path[:1]
    elif host in {"youtube.com", "youtube-nocookie.com"}:
        platform, host = "youtube", "www.youtube.com"
        if path[0].startswith("@") and len(path[0]) > 1:
            path = path[:1]
        elif first in {"channel", "c", "user"} and len(path) >= 2:
            path = path[:2]
        else:
            return None
    elif host == "tiktok.com":
        platform, host = "tiktok", "www.tiktok.com"
        if not path[0].startswith("@") or len(path[0]) < 2:
            return None
        path = path[:1]
    elif host == "github.com":
        platform = "github"
        if first in {"login", "signup", "features", "enterprise", "marketplace", "topics", "explore", "settings", "about", "pricing", "orgs", "sponsors", "collections", "security", "site", "readme", "customer-stories", "contact"}:
            return None
        path = path[:1]
    elif host in {"pinterest.com", "pinterest.co.uk"}:
        platform, host = "pinterest", "www.pinterest.com"
        if first in {"pin", "search", "ideas", "login", "signup", "business", "settings", "today"}:
            return None
        path = path[:1]
    else:
        return None
    # Social profiles are case-insensitive on these services; preserve handles on
    # YouTube, whose channel IDs are case-sensitive.
    if platform != "youtube":
        path = [part.lower() for part in path]
    return platform, urlunsplit(("https", host, "/" + "/".join(path), query, ""))


def _ld_nodes(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, list):
        for item in value:
            yield from _ld_nodes(item)
    elif isinstance(value, dict):
        yield value
        for key, child in value.items():
            if key != "@context" and isinstance(child, (dict, list)):
                yield from _ld_nodes(child)


def _ld_types(node: dict[str, Any]) -> list[str]:
    return [kind.rstrip("/").rsplit("/", 1)[-1].rsplit("#", 1)[-1] for kind in _strings(node.get("@type"))]


def extract_page(html: str, url: str) -> PageResult:
    if not isinstance(html, str):
        raise ValueError("HTML must be text.")
    if not _public_url(url, url):
        raise ValueError("Page URL must be HTTP(S).")
    soup = BeautifulSoup(html, "html.parser")
    result: PageResult = {
        "title": _clean_text(soup.title.get_text(" ")) if soup.title else "",
        "description": "", "companyName": "", "emails": [], "phones": [],
        "socials": {}, "contactPageUrls": [], "contactFormUrls": [],
        "technologies": detect_technologies(html, url, soup=soup), "evidence": [],
        "language": _clean_text(soup.html.get("lang", "")) if soup.html else "", "jsonLdTypes": [],
    }
    for meta in soup.find_all("meta"):
        key = str(meta.get("name", meta.get("property", ""))).lower()
        content = _clean_text(meta.get("content", ""))
        if key == "description" and content:
            result["description"] = content
        elif key == "og:description" and not result["description"]:
            result["description"] = content
        elif key == "og:site_name" and not result["companyName"]:
            result["companyName"] = content

    evidence_seen: set[tuple[str, str, str]] = set()
    evidence_counts: Counter[tuple[str, str]] = Counter()
    email_seen: dict[str, str] = {}

    def evidence(kind: str, value: str, method: str) -> None:
        marker = kind, value, method
        identity = kind, value
        if marker in evidence_seen:
            return
        if len(result["evidence"]) >= MAX_EVIDENCE:
            if evidence_counts[identity]:
                return
            # Preserve a source for each retained contact/technology before
            # keeping extra methods for a contact already represented.
            for index in range(len(result["evidence"]) - 1, -1, -1):
                previous = result["evidence"][index]
                previous_identity = previous["type"], previous["value"]
                if evidence_counts[previous_identity] > 1:
                    result["evidence"].pop(index)
                    evidence_counts[previous_identity] -= 1
                    evidence_seen.discard((*previous_identity, previous["method"]))
                    break
            else:
                return
        evidence_seen.add(marker)
        evidence_counts[identity] += 1
        result["evidence"].append({"type": kind, "value": value, "sourceUrl": url, "method": method})

    def email(raw: str, method: str) -> None:
        normalized = normalize_email(raw)
        if normalized:
            if normalized.casefold() not in email_seen:
                if len(result["emails"]) >= MAX_EMAILS:
                    return
                email_seen[normalized.casefold()] = normalized
                result["emails"].append(normalized)
            evidence("email", email_seen[normalized.casefold()], method)

    def phone(raw: str, method: str) -> None:
        normalized = normalize_phone(raw)
        if normalized:
            if normalized not in result["phones"]:
                if len(result["phones"]) >= MAX_PHONES:
                    return
                result["phones"].append(normalized)
            evidence("phone", normalized, method)

    def social(raw: str, method: str) -> None:
        normalized = normalize_social(raw, url)
        if normalized:
            platform, address = normalized
            profiles = result["socials"].setdefault(platform, [])
            if address not in profiles:
                if len(profiles) >= MAX_SOCIALS_PER_PLATFORM:
                    return
                profiles.append(address)
            evidence("social", address, method)

    organization_name = ""
    for script in soup.find_all("script"):
        if str(script.get("type", "")).split(";", 1)[0].lower().strip() != "application/ld+json":
            continue
        try:
            document = json.loads(script.string or script.get_text())
        except (ValueError, TypeError, RecursionError):
            continue
        try:
            nodes = list(_ld_nodes(document))
        except RecursionError:
            continue
        for node in nodes:
            kinds = _ld_types(node)
            for kind in kinds:
                if kind not in result["jsonLdTypes"]:
                    result["jsonLdTypes"].append(kind)
            if not any(kind.casefold() in _ORG_TYPES for kind in kinds):
                continue
            if not organization_name:
                organization_name = _clean_text(node.get("name", "")) if isinstance(node.get("name"), str) else ""
            for raw in _strings(node.get("email")):
                email(raw[7:] if raw.lower().startswith("mailto:") else raw, "jsonld.email")
            for raw in _strings(node.get("telephone")):
                phone(raw, "jsonld.telephone")
            for raw in _strings(node.get("sameAs")):
                social(raw, "jsonld.sameAs")
            # contactPoint is structured publication of a business contact.
            points = node.get("contactPoint", [])
            if isinstance(points, dict):
                points = [points]
            if isinstance(points, list):
                for point in points:
                    if isinstance(point, dict):
                        for raw in _strings(point.get("email")):
                            email(raw[7:] if raw.lower().startswith("mailto:") else raw, "jsonld.contactPoint.email")
                        for raw in _strings(point.get("telephone")):
                            phone(raw, "jsonld.contactPoint.telephone")
    if organization_name:
        result["companyName"] = organization_name

    # Remove non-visible containers, including their anchors. Script/configuration
    # addresses are not public contact evidence. No JS or CSS is executed.
    for element in list(soup.find_all(["script", "style", "noscript", "template", "svg", "head", "code", "pre"])):
        if element.parent is not None:
            element.decompose()
    for element in list(soup.find_all(True)):
        if element.parent is None:
            continue
        style = str(element.get("style", ""))
        if element.has_attr("hidden") or str(element.get("aria-hidden", "")).lower() == "true" or re.search(r"(?:display\s*:\s*none|visibility\s*:\s*hidden)", style, re.I):
            element.decompose()

    for anchor in soup.find_all("a", href=True):
        raw = str(anchor.get("href", "")).strip()
        if raw.lower().startswith("mailto:"):
            recipients = unquote(raw[7:].split("?", 1)[0])
            for recipient in re.split(r"[,;]", recipients):
                email(recipient, "mailto")
        elif raw.lower().startswith("tel:"):
            phone(raw, "tel")
        else:
            social(raw, "html-link")
            address = _public_url(raw, url)
            if not address or not _same_site(address, url):
                continue
            path = unquote(urlsplit(address).path).casefold()
            text = _clean_text(anchor.get_text(" ")).casefold()
            contact_path = re.search(r"(?:^|[/_-])(?:contact(?:-us)?|get-in-touch|lien-he|lienhe|support|customer-service)(?:$|[/_.-])", path)
            if contact_path or text in {"contact", "contact us", "get in touch", "liên hệ", "liên hệ với chúng tôi"}:
                if address not in result["contactPageUrls"]:
                    if len(result["contactPageUrls"]) >= MAX_CONTACT_PAGES:
                        continue
                    result["contactPageUrls"].append(address)
                evidence("contact-page", address, "html-link")

    for form in soup.find_all("form"):
        fields = form.find_all(["input", "textarea"])
        has_email = any(
            str(field.get("type", "")).lower() == "email"
            or re.search(r"(?:^|[_-])(?:email|e-mail)(?:$|[_-])", str(field.get("name", "")), re.I)
            for field in fields
        )
        has_message = any(field.name == "textarea" for field in fields)
        has_password = any(str(field.get("type", "")).lower() == "password" for field in fields)
        if not has_email or not has_message or has_password:
            continue
        action = _public_url(str(form.get("action", "")), url)
        if action:
            # An external HTTP(S) action (e.g. Formspree) is ordinary for contact
            # forms. Record only this public page; never fetch/submit the action.
            if url not in result["contactFormUrls"]:
                if len(result["contactFormUrls"]) >= MAX_CONTACT_FORMS:
                    continue
                result["contactFormUrls"].append(url)
            evidence("contact-form", url, "html-form")

    visible_text = soup.get_text(" ", strip=True)
    for match in _EMAIL.finditer(visible_text):
        email(match.group(1), "visible-text")
    for technology in result["technologies"]:
        evidence("technology", technology["name"], technology["evidence"])
    return result

