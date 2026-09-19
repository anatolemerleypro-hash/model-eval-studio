"""Deterministic evaluation primitives."""

from __future__ import annotations

from typing import Any, Callable


def evaluate_case(case: dict[str, Any], response: str, threshold: float = 0.75) -> dict[str, Any]:
    """Score one response against explicit rules in an evaluation case."""
    normalized = response.casefold()
    checks: list[dict[str, Any]] = []

    for phrase in case.get("must_include", []):
        checks.append({"rule": f"includes: {phrase}", "passed": phrase.casefold() in normalized})
    for phrase in case.get("must_not_include", []):
        checks.append({"rule": f"excludes: {phrase}", "passed": phrase.casefold() not in normalized})
    if "min_length" in case:
        minimum = int(case["min_length"])
        checks.append({"rule": f"length >= {minimum}", "passed": len(response) >= minimum})

    score = sum(item["passed"] for item in checks) / len(checks) if checks else 1.0
    return {
        "name": case["name"],
        "prompt": case["prompt"],
        "response": response,
        "score": round(score, 4),
        "passed": score >= threshold,
        "checks": checks,
    }


def run_suite(
    suite: dict[str, Any],
    provider: Callable[[str], str],
    provider_name: str = "demo",
) -> dict[str, Any]:
    """Run all cases and return a JSON-serializable report."""
    threshold = float(suite.get("pass_threshold", 0.75))
    results = [
        evaluate_case(case, provider(case["prompt"]), threshold)
        for case in suite["cases"]
    ]
    average = sum(item["score"] for item in results) / len(results) if results else 0.0
    return {
        "suite": suite.get("name", "Unnamed suite"),
        "provider": provider_name,
        "pass_threshold": threshold,
        "summary": {
            "cases": len(results),
            "passed": sum(item["passed"] for item in results),
            "average_score": round(average, 4),
        },
        "results": results,
    }
