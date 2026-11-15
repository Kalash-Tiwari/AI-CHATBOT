import asyncio
import unittest

from app.api.routes import _is_valid_key, list_models


class ProviderConfigTests(unittest.TestCase):
    def test_placeholder_api_keys_are_rejected(self):
        self.assertFalse(_is_valid_key("your_key_here"))
        self.assertFalse(_is_valid_key("dummy"))
        self.assertTrue(_is_valid_key("a_valid_api_key_12345"))

    def test_model_listing_returns_all_supported_providers(self):
        payload = asyncio.run(list_models())
        self.assertIn("providers", payload)
        names = {provider["name"] for provider in payload["providers"]}
        self.assertTrue({"gemini", "openai", "claude"}.issubset(names))


if __name__ == "__main__":
    unittest.main()
