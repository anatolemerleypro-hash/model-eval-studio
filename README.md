# Model Eval Studio

A small, transparent evaluation toolkit for comparing LLM responses against reusable test cases and scoring rubrics. It runs locally, works without an API key in demo mode, and exports auditable JSON reports.

## Why this project?

LLM comparisons are often based on a handful of subjective prompts. Model Eval Studio turns those comparisons into a repeatable workflow:

- test cases live in version-controlled JSON files;
- scoring rules are explicit and deterministic;
- providers are adapters, so Claude or another API can be added without changing the evaluator;
- reports preserve every response and score for later review;
- the included demo provider makes the full workflow testable offline.

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/YOUR_USERNAME/model-eval-studio.git
cd model-eval-studio
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
model-eval run examples/customer-support.json --output report.json
model-eval summary report.json
```

To evaluate real Claude responses, provide an Anthropic API key through the environment:

```bash
export ANTHROPIC_API_KEY="your-key-here"
export ANTHROPIC_MODEL="claude-sonnet-4-5"  # optional
model-eval run examples/customer-support.json --provider claude --output claude-report.json
```

The key is read at runtime, is never written to a report, and `.env` files are excluded from Git.

Example output:

```text
Provider: demo
Cases: 3
Average score: 0.83
Passed: 2/3
```

## Evaluation format

Each case contains a prompt plus simple, inspectable expectations:

```json
{
  "name": "Password reset",
  "prompt": "Help a customer reset a forgotten password.",
  "must_include": ["reset", "email"],
  "must_not_include": ["password is"],
  "min_length": 40
}
```

The score is the fraction of rules satisfied. A case passes at `0.75` by default. This deliberately simple baseline is useful for regression tests and can be extended with model-graded or human review.

## Project layout

```text
src/model_eval/       evaluator, providers, CLI
examples/              sample evaluation suite
tests/                 unit and CLI tests
.github/workflows/     continuous integration
```

## Roadmap

- Claude Messages API adapter with streaming and rate-limit handling
- side-by-side HTML report
- latency and token-cost tracking
- pairwise blind review
- dataset import from CSV and JSONL

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Development

Run the test suite without any third-party test runner:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Responsible use

Scores are indicators, not universal judgments of model quality. Use representative test data, review edge cases manually, and never place secrets or personal customer data in fixtures.

## License

MIT © 2026
