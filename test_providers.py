import os
import unittest
from unittest.mock import patch

from model_eval.providers import ProviderError, claude_provider, demo_provider


class ProviderTests(unittest.TestCase):
    def test_demo_provider_is_deterministic(self):
        prompt = "Help me reset my password"
        self.assertEqual(demo_provider(prompt), demo_provider(prompt))

    def test_claude_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ProviderError, "ANTHROPIC_API_KEY"):
                claude_provider("Hello")


if __name__ == "__main__":
    unittest.main()
