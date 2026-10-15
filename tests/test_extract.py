import json
import unittest

from sitesignal.config import RunConfig
from sitesignal.extract import extract_page, normalize_social


BASE = "https://acme-business.co/"


class ExtractTests(unittest.TestCase):
    def test_visible_and_mailto_contacts_have_evidence_and_deduplicate(self):
        result = extract_page('''<html lang="en"><head><title> Acme | Welcome </title>
            <meta name="description" content="A local business"></head><body>
            <p>Sales@ACME-BUSINESS.CO</p>
            <a href="mailto:Sales%40acme-business.co?subject=Hello">Email</a>
            <a href="tel:+1 (202) 555-0143;ext=42">Call</a>
            <p>Order 1234567890, number 2025550999</p></body></html>''', BASE)
        self.assertEqual(result["emails"], ["Sales@acme-business.co"])
        self.assertEqual(result["phones"], ["+12025550143 ext. 42"])
        self.assertEqual(result["language"], "en")
        self.assertEqual(result["description"], "A local business")
        self.assertEqual(result["title"], "Acme | Welcome")
        methods = {item["method"] for item in result["evidence"] if item["type"] == "email"}
        self.assertEqual(methods, {"mailto", "visible-text"})
        self.assertTrue(all(item["sourceUrl"] == BASE for item in result["evidence"]))

    def test_script_hidden_placeholder_and_assets_are_not_contacts(self):
        result = extract_page('''<html><head><script>const test = "secret@acme-business.co";</script>
            <style>.x{background:url(a@asset.png)}</style></head><body>
            <div hidden>hidden@acme-business.co</div><p aria-hidden="true">aria@acme-business.co</p>
            <p style="display: none">css@acme-business.co</p><template>template@acme-business.co</template>
            <code>fake@acme-business.co</code><pre>sample@acme-business.co</pre>
            test@example.com user@test.com x@a.sentry.io picture@logo.webp
            <a href="mailto:hello@acme-business.co">Email us</a>
            </body></html>''', BASE)
        self.assertEqual(result["emails"], ["hello@acme-business.co"])

    def test_jsonld_graph_type_arrays_and_contacts(self):
        result = extract_page('''<html><head><meta property="og:site_name" content="Fallback">
            <script type="application/ld+json">{"@context":"https://schema.org","@graph":[
            {"@type":"WebSite","name":"Website"},
            {"@type":["Organization","LocalBusiness"],"name":"Acme Ltd",
             "email":"info@ACME-BUSINESS.CO","telephone":"+84 28 3822 5555",
             "sameAs":["https://www.linkedin.com/company/acme-business/?tracking=1"],
             "contactPoint":{"@type":"ContactPoint","telephone":"+1 202 555 0115","email":"help@acme-business.co"}}]}</script>
            <script type="application/ld+json">invalid json</script></head><body>Hi</body></html>''', BASE)
        self.assertEqual(result["companyName"], "Acme Ltd")
        self.assertEqual(result["emails"], ["info@acme-business.co", "help@acme-business.co"])
        self.assertEqual(result["phones"], ["+842838225555", "+12025550115"])
        self.assertIn("LocalBusiness", result["jsonLdTypes"])
        self.assertEqual(result["socials"]["linkedin"], ["https://www.linkedin.com/company/acme-business"])

    def test_non_organization_jsonld_does_not_extract_person_email(self):
        result = extract_page('''<script type="application/ld+json">{"@type":"Person","name":"A Person","email":"person@acme-business.co","telephone":"2025550143"}</script>''', BASE)
        self.assertEqual(result["emails"], [])
        self.assertEqual(result["phones"], [])

    def test_contact_forms_require_email_and_message_with_http_action(self):
        result = extract_page('''<a href="/contact-us#form">Contact</a><a href="https://external.co/contact">Contact us</a>
            <a href="javascript:alert(1)">Contact</a><a href="/support">Support</a>
            <form action="/send"><input type="email"><textarea name="message"></textarea></form>
            <form action="https://external.co/send"><textarea name="message"></textarea></form>
            <form action="/search"><input name="q"></form>''', BASE)
        self.assertEqual(result["contactPageUrls"], [BASE + "contact-us", BASE + "support"])
        self.assertEqual(result["contactFormUrls"], [BASE])
        external = extract_page('<form action="https://formspree.io/f/public"><input type="email"><textarea name="message"></textarea></form>', BASE)
        self.assertEqual(external["contactFormUrls"], [BASE])
        self.assertTrue(any(item["type"] == "contact-form" and item["sourceUrl"] == BASE for item in external["evidence"]))

    def test_login_newsletter_and_script_forms_are_not_contacts(self):
        for form in [
            '<form><input type="email"><input type="password"><textarea></textarea></form>',
            '<form><input type="email"></form>',
            '<form><textarea></textarea></form>',
            '<form action="javascript:send()"><input type="email"><textarea></textarea></form>',
            '<form action="data:text/html,fake"><input type="email"><textarea></textarea></form>',
        ]:
            with self.subTest(form=form):
                self.assertEqual(extract_page(form, BASE)["contactFormUrls"], [])

    def test_social_profiles_canonicalize_and_share_endpoints_rejected(self):
        html = '''<a href="https://twitter.com/AcmeBusiness/status/123?ref=footer">X</a>
            <a href="https://x.com/AcmeBusiness">Again</a>
            <a href="https://www.facebook.com/sharer/sharer.php?u=x">Share</a>
            <a href="https://www.facebook.com/profile.php?id=12345&ref=x">Facebook</a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url=x">Share</a>
            <a href="https://www.youtube.com/@AcmeBusiness/videos">YouTube</a>
            <a href="https://www.instagram.com/p/abcdef">Post</a>
            <a href="https://www.instagram.com/AcmeBusiness/?igsh=x">Instagram</a>
            <a href="https://github.com/acmebusiness/project">GitHub</a>
            <a href="https://instagram.com.evil.net/attacker">Fake domain</a>'''
        result = extract_page(html, BASE)
        self.assertEqual(result["socials"]["x"], ["https://x.com/acmebusiness"])
        self.assertEqual(result["socials"]["facebook"], ["https://www.facebook.com/profile.php?id=12345"])
        self.assertNotIn("linkedin", result["socials"])
        self.assertEqual(result["socials"]["youtube"], ["https://www.youtube.com/@AcmeBusiness"])
        self.assertEqual(result["socials"]["instagram"], ["https://www.instagram.com/acmebusiness"])
        self.assertEqual(result["socials"]["github"], ["https://github.com/acmebusiness"])
        self.assertIsNone(normalize_social("javascript:alert(1)", BASE))

    def test_empty_html_is_valid_and_input_not_mutated(self):
        html = "<p>No contacts available</p>"
        result = extract_page(html, BASE)
        self.assertEqual(html, "<p>No contacts available</p>")
        self.assertEqual(result["emails"], [])
        self.assertEqual(result["phones"], [])
        self.assertEqual(extract_page("", BASE)["title"], "")

    def test_sentence_punctuation_and_comments(self):
        result = extract_page("<p>Write to us at hello@acme-business.co.</p><!-- internal@acme-business.co -->", BASE)
        self.assertEqual(result["emails"], ["hello@acme-business.co"])

    def test_public_output_caps_are_deterministic_and_keep_contact_evidence(self):
        emails = [f"team{i}@acme-business.co" for i in range(120)]
        phones = [f"+1202555{i:04}" for i in range(60)]
        socials = [f"https://instagram.com/acme{i}" for i in range(15)]
        organization = {"@type": "Organization", "email": emails, "telephone": phones, "sameAs": socials,
                        "contactPoint": {"email": emails, "telephone": phones}}
        html = '<script type="application/ld+json">' + json.dumps(organization) + '</script>'
        html += ''.join(f'<a href="mailto:{email}">{email}</a>' for email in emails)
        html += ''.join(f'<a href="tel:{phone}">Phone</a>' for phone in phones)
        html += ''.join(f'<a href="{social}">Social</a>' for social in socials)
        html += ''.join(f'<a href="/contact/{i}">Contact</a>' for i in range(60))
        html += '<script src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id=abc"></script>'
        result = extract_page(html, BASE)
        self.assertEqual(result["emails"], emails[:100])
        self.assertEqual(result["phones"], phones[:50])
        self.assertEqual(len(result["socials"]["instagram"]), 10)
        self.assertEqual(len(result["contactPageUrls"]), 50)
        self.assertLessEqual(len(result["contactFormUrls"]), 50)
        self.assertEqual(len(result["evidence"]), 500)
        self.assertEqual(result, extract_page(html, BASE))
        identities = {(item["type"], item["value"]) for item in result["evidence"]}
        for kind, values in [("email", result["emails"]), ("phone", result["phones"]),
                             ("contact-page", result["contactPageUrls"]),
                             ("social", result["socials"]["instagram"])]:
            self.assertTrue(all((kind, value) in identities for value in values))
        self.assertIn(("technology", "Klaviyo"), identities)


class ConfigTests(unittest.TestCase):
    def test_defaults_aliases_url_normalization_deduplication(self):
        result = RunConfig.from_dict({"startUrls": [{"url": "ACME-BUSINESS.CO"}, "https://acme-business.co/#section"]})
        self.assertEqual(result.websites, (BASE,))
        self.assertTrue(result.respect_robots)
        self.assertEqual(result.max_pages_per_site, 3)
        self.assertEqual(result.min_delay_seconds, 0.5)

    def test_limits_types_bad_urls(self):
        cases = [
            {"websites": []}, {"websites": "https://acme-business.co"},
            {"websites": ["ftp://acme-business.co"]}, {"websites": ["https://u:p@acme-business.co"]},
            {"websites": [BASE], "maxPagesPerSite": 6}, {"websites": [BASE], "maxSites": 1001},
            {"websites": [BASE], "concurrency": True}, {"websites": [BASE], "timeoutSeconds": 4},
            {"websites": [BASE], "minDelaySeconds": 0}, {"websites": [BASE], "respectRobots": "true"},
            {"websites": [BASE], "includeTechnology": 1}, {"websites": [BASE], "minDelaySeconds": float("nan")},
            {"websites": [BASE], "maxPagesPersite": 3},
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                RunConfig.from_dict(case)


if __name__ == "__main__":
    unittest.main()

