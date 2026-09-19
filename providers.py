"""Provider adapters, including an optional Claude HTTP integration."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    """Raised when a model provider cannot return a usable response."""


def demo_provider(prompt: str) -> str:
    """Return deterministic responses so the evaluator can be tried offline."""
    lowered = prompt.casefold()
    if "password" in lowered:
        return "Use the password reset link, then check your email and follow the secure instructions."
    if "refund" in lowered:
        return "I can help with your refund. Please share the order number, but no payment details."
    return "I understand your request. Here are clear, safe next steps and a way to get more help."


def claude_provider(prompt: str) -> str:
    """Call Anthropic's Messages API using only the Python standard library."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ProviderError("ANTHROPIC_API_KEY is required for the Claude provider")

    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    payload = json.dumps(
        {
            "model": model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise ProviderError(f"Claude API returned HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise ProviderError(f"Could not reach the Claude API: {error.reason}") from error

    blocks = body.get("content", [])
    text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
    if not text:
        raise ProviderError("Claude API returned no text content")
    return text


PROVIDERS = {"demo": demo_provider, "claude": claude_provider}
