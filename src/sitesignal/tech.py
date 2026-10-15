"""Conservative HTML technology signatures; no requests or script execution."""

import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup

from .models import Technology


def detect_technologies(html: str, url: str, *, soup: BeautifulSoup | None = None) -> list[Technology]:
    soup = soup or BeautifulSoup(html, "html.parser")
    found: dict[str, Technology] = {}

    def add(name: str, category: str, evidence: str) -> None:
        if name not in found:
            found[name] = {"name": name, "category": category, "evidence": evidence[:300], "sourceUrl": url}

    for meta in soup.find_all("meta"):
        if str(meta.get("name", "")).casefold() != "generator":
            continue
        generator = str(meta.get("content", "")).strip()
        lower = generator.casefold()
        for marker, name, category in [
            ("wordpress", "WordPress", "CMS"), ("woocommerce", "WooCommerce", "E-commerce"),
            ("shopify", "Shopify", "E-commerce"), ("webflow", "Webflow", "CMS"),
            ("wix", "Wix", "CMS"), ("squarespace", "Squarespace", "CMS"),
            ("magento", "Magento", "E-commerce"), ("ghost", "Ghost", "CMS"),
        ]:
            if re.search(r"\b" + marker + r"\b", lower):
                add(name, category, f"meta generator: {generator}")

    if soup.find(attrs={"data-wf-site": True}) or soup.find(attrs={"data-wf-page": True}):
        add("Webflow", "CMS", "HTML data-wf-site/data-wf-page attribute")

    resources: list[tuple[str, str]] = []
    for element in soup.find_all(["script", "link", "img", "iframe", "a"]):
        attribute = "href" if element.name in {"link", "a"} else "src"
        raw = element.get(attribute)
        if not isinstance(raw, str):
            continue
        try:
            parsed = urlsplit(urljoin(url, raw))
        except ValueError:
            continue
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            continue
        resources.append((parsed.hostname.casefold(), parsed.path.casefold() + "?" + parsed.query))
        host, path = resources[-1]
        evidence = f"{element.name}[{attribute}]: {raw}"

        def host_is(domain: str) -> bool:
            return host == domain or host.endswith("." + domain)

        # Links to a vendor's marketing site alone do not identify the site's stack.
        is_asset = element.name != "a"
        if is_asset and ("/wp-content/" in path or "/wp-includes/" in path):
            add("WordPress", "CMS", evidence)
        if is_asset and ("/plugins/woocommerce/" in path or "/woocommerce/assets/" in path):
            add("WooCommerce", "E-commerce", evidence)
        if is_asset and (host_is("cdn.shopify.com") or host_is("shopifycdn.com") or host_is("myshopify.com")):
            add("Shopify", "E-commerce", evidence)
        if is_asset and (host_is("website-files.com") or host_is("webflow.com") and "/js/" in path):
            add("Webflow", "CMS", evidence)
        if is_asset and (host_is("wixstatic.com") or host_is("parastorage.com")):
            add("Wix", "CMS", evidence)
        if is_asset and host_is("squarespace.com") and (host.startswith("static") or "/universal/" in path):
            add("Squarespace", "CMS", evidence)
        if is_asset and ("/magento_" in path or "/mage/" in path):
            add("Magento", "E-commerce", evidence)
        if is_asset and host_is("googletagmanager.com"):
            if path.startswith("/gtm.js?") and re.search(r"(?:[?&])id=GTM-[A-Z0-9]+", path, re.I):
                add("Google Tag Manager", "Tag manager", evidence)
            if path.startswith("/gtag/js?") and re.search(r"(?:[?&])id=G-[A-Z0-9]+", path, re.I):
                add("Google Analytics 4", "Analytics", evidence)
        if is_asset and host_is("plausible.io") and ("/js/" in path):
            add("Plausible", "Analytics", evidence)
        if is_asset and re.search(r"/(?:matomo|piwik)\.js(?:\?|$)", path):
            add("Matomo", "Analytics", evidence)
        if element.name == "script" and (
            host == "static.klaviyo.com" and path.startswith("/onsite/js/")
            or host == "a.klaviyo.com" and path.startswith(("/onsite?", "/onsite/"))
        ):
            add("Klaviyo", "Marketing", evidence)
        if host_is("js.stripe.com") and is_asset or host_is("checkout.stripe.com"):
            add("Stripe", "Payments", evidence)

    for script in soup.find_all("script"):
        if script.get("src"):
            continue
        text = script.string or script.get_text()
        if re.search(r"\bShopify\.shop\s*=", text):
            add("Shopify", "E-commerce", "inline script assigns Shopify.shop")
        if re.search(r"\bgtag\s*\(\s*['\"]config['\"]\s*,\s*['\"]G-[A-Z0-9]+['\"]", text, re.I):
            add("Google Analytics 4", "Analytics", "inline script: gtag config with G- measurement ID")
        if "_paq.push" in text and ("matomo.php" in text or "piwik.php" in text):
            add("Matomo", "Analytics", "inline script: _paq.push with Matomo/Piwik endpoint")

    return sorted(found.values(), key=lambda item: item["name"].casefold())

