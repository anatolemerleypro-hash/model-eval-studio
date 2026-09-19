"""Command-line interface for Model Eval Studio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluator import run_suite
from .providers import PROVIDERS, ProviderError


def _run(args: argparse.Namespace) -> int:
    suite = json.loads(Path(args.suite).read_text(encoding="utf-8"))
    try:
        report = run_suite(suite, PROVIDERS[args.provider], args.provider)
    except ProviderError as error:
        print(f"Provider error: {error}")
        return 2
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = report["summary"]
    print(f"Provider: {report['provider']}")
    print(f"Cases: {summary['cases']}")
    print(f"Average score: {summary['average_score']:.2f}")
    print(f"Passed: {summary['passed']}/{summary['cases']}")
    return 0


def _summary(args: argparse.Namespace) -> int:
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    summary = report["summary"]
    print(f"{report['suite']} — {report['provider']}")
    print(f"{summary['passed']}/{summary['cases']} passed; average {summary['average_score']:.2f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="model-eval", description="Evaluate LLM responses")
    commands = parser.add_subparsers(required=True)
    run = commands.add_parser("run", help="run an evaluation suite")
    run.add_argument("suite")
    run.add_argument("--provider", choices=PROVIDERS, default="demo")
    run.add_argument("--output", default="report.json")
    run.set_defaults(handler=_run)
    summary = commands.add_parser("summary", help="print a saved report summary")
    summary.add_argument("report")
    summary.set_defaults(handler=_summary)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
