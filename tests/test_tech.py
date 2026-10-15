import unittest

from sitesignal.tech import detect_technologies


URL = "https://acme-business.co/"


class TechnologyTests(unittest.TestCase):
    def names(self, html):
        return {row["name"] for row in detect_technologies(html, URL)}

    def test_text_and_vendor_marketing_links_do_not_identify_stack(self):
        self.assertEqual(self.names('''<p>We used to use WordPress, Shopify and Stripe.</p>
            <a href="https://wordpress.org/">WordPress</a><a href="https://www.shopify.com/">Shopify</a>
            <a href="https://stripe.com/">Stripe</a>'''), set())

    def test_cms_specific_assets_and_generator(self):
        self.assertEqual(self.names('<meta name="generator" content="WordPress 6.8"><script src="/wp-content/plugins/woocommerce/assets/js/cart.js"></script>'), {"WordPress", "WooCommerce"})
        self.assertIn("Shopify", self.names('<script src="https://cdn.shopify.com/s/files/theme.js"></script>'))
        self.assertIn("Wix", self.names('<script src="https://static.parastorage.com/services/editor.js"></script>'))
        self.assertIn("Squarespace", self.names('<script src="https://static1.squarespace.com/static/site.js"></script>'))
        self.assertIn("Webflow", self.names('<html data-wf-site="abc"><body></body></html>'))
        self.assertIn("Ghost", self.names('<meta name="generator" content="Ghost 5.0">'))
        self.assertIn("Magento", self.names('<script src="/static/frontend/Shop/default/en_US/Magento_Catalog/js/product.js"></script>'))

    def test_analytics_tag_manager_payments_have_source_and_evidence(self):
        html = '''<script src="https://www.googletagmanager.com/gtm.js?id=GTM-ABC123"></script>
            <script src="https://www.googletagmanager.com/gtag/js?id=G-ABC123"></script>
            <script defer data-domain="acme-business.co" src="https://plausible.io/js/script.js"></script>
            <script src="/analytics/matomo.js"></script><script src="https://js.stripe.com/v3/"></script>'''
        result = detect_technologies(html, URL)
        self.assertEqual({row["name"] for row in result}, {"Google Tag Manager", "Google Analytics 4", "Plausible", "Matomo", "Stripe"})
        self.assertTrue(all(row["sourceUrl"] == URL and row["evidence"] and row["category"] for row in result))

    def test_host_lookalikes_do_not_match(self):
        self.assertEqual(self.names('<script src="https://cdn.shopify.com.attacker.net/script.js"></script><script src="https://plausible.io.evil.net/js/script.js"></script>'), set())

    def test_repeated_signatures_return_one_technology(self):
        result = detect_technologies('<meta name="generator" content="WordPress"><script src="/wp-includes/js/x.js"></script>', URL)
        self.assertEqual(len(result), 1)

    def test_inline_ga4_specific_config(self):
        self.assertEqual(self.names("<script>gtag('config', 'G-ABC123');</script>"), {"Google Analytics 4"})
        self.assertEqual(self.names("<script>console.log('Google Analytics');</script>"), set())

    def test_klaviyo_requires_specific_script_host_and_onsite_path(self):
        self.assertEqual(self.names('<script src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id=abc"></script>'), {"Klaviyo"})
        self.assertEqual(self.names('<script src="https://a.klaviyo.com/onsite?company_id=abc"></script>'), {"Klaviyo"})
        self.assertEqual(self.names('<p>Our Klaviyo guide</p><a href="https://www.klaviyo.com/">Klaviyo</a><script src="https://static.klaviyo.com.evil.net/onsite/js/fake.js"></script>'), set())
        self.assertEqual(self.names('<img src="https://static.klaviyo.com/onsite/js/fake.js"><script src="https://static.klaviyo.com/marketing.js"></script>'), set())


if __name__ == "__main__":
    unittest.main()

