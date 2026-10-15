import asyncio
import csv
import io
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sitesignal.config import RunConfig
from sitesignal.crawler import FetchError, Page, PublicResolver, crawl_sites, public_ip, same_site, validate_url
from sitesignal.output import results_csv


class SecurityTests(unittest.TestCase):
    def test_reject_private_literal_urls_and_credentials(self):
        for url in ["http://127.0.0.1/", "http://[::1]/", "http://169.254.169.254/", "http://10.1.2.3/", "http://localhost/", "https://a.local/", "http://100.64.0.1/", "https://user:pass@example.com/", "file:///etc/passwd", "http://example.com:3000/"]:
            with self.subTest(url=url), self.assertRaises(FetchError):
                validate_url(url)

    def test_public_ip_and_scope(self):
        self.assertTrue(public_ip("8.8.8.8"))
        self.assertFalse(public_ip("::ffff:127.0.0.1"))
        self.assertTrue(same_site("https://www.example.com/", "https://example.com/about"))
        self.assertFalse(same_site("https://example.com", "https://example.com.attacker.net"))

    def test_csv_formula_escape(self):
        row = {"url": "https://example.com", "companyName": "  =HYPERLINK(\"bad\")", "phones": ["+123456789"]}
        exported = list(csv.DictReader(io.StringIO(results_csv([row]))))[0]
        self.assertTrue(exported["companyName"].startswith("'"))
        self.assertEqual(row["companyName"], "  =HYPERLINK(\"bad\")")


class FakeClient:
    def __init__(self, config):
        self.requests = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def fetch(self, url, **kwargs):
        self.requests += 1
        if "blocked" in url:
            raise FetchError("blocked", "Denied", 403)
        if url.endswith("/contact"):
            return Page(url, '<a href="mailto:hello@acme-business.co">Email</a><a href="tel:+12025550123">Phone</a>', 200, "text/html")
        return Page(url, '<title>Acme</title><a href="/contact">Contact us</a>', 200, "text/html")


class CrawlerTests(unittest.IsolatedAsyncioTestCase):
    async def test_merge_dedupe_failures_and_page_limit(self):
        config = RunConfig.from_dict({"websites": ["https://acme.example", "https://www.acme.example/path", "https://blocked.example"], "maxPagesPerSite": 2})
        report = await crawl_sites(config, client_factory=FakeClient)
        self.assertEqual(len(report["results"]), 1)
        self.assertEqual(report["summary"]["duplicateDomainsSkipped"], 1)
        self.assertEqual(report["diagnostics"][0]["status"], "blocked")
        row = report["results"][0]
        self.assertEqual(row["pagesChecked"], 2)
        self.assertEqual(row["emails"], ["hello@acme-business.co"])
        self.assertTrue(any(e["sourceUrl"].endswith("/contact") for e in row["evidence"]))

    async def test_result_callback_can_stop_before_billing(self):
        config = RunConfig.from_dict({"websites": ["https://one.example", "https://two.example", "https://three.example"], "concurrency": 1, "maxPagesPerSite": 1})
        saved = []
        async def save(row):
            if saved:
                return False
            saved.append(row)
            return True
        report = await crawl_sites(config, save, client_factory=FakeClient)
        self.assertEqual(len(report["results"]), 1)
        self.assertEqual(report["summary"]["requests"], 2)
        self.assertEqual(report["summary"]["unprocessedAfterLimit"], 2)
        self.assertTrue(report["summary"]["stoppedByResultLimit"])

    async def test_resolver_rejects_mixed_dns_answers(self):
        resolver = PublicResolver()
        original = resolver._resolver
        class FakeDNS:
            async def resolve(self, *args):
                return [{"host": "8.8.8.8"}, {"host": "127.0.0.1"}]
        resolver._resolver = FakeDNS()
        with self.assertRaises(OSError):
            await resolver.resolve("example.com")
        await original.close()


if __name__ == "__main__":
    unittest.main()
