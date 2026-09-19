import unittest

from model_eval.evaluator import evaluate_case, run_suite


class EvaluatorTests(unittest.TestCase):
    def test_evaluate_case_scores_each_rule(self):
        case = {
            "name": "Example",
            "prompt": "Say hello",
            "must_include": ["hello"],
            "must_not_include": ["secret"],
            "min_length": 5,
        }
        result = evaluate_case(case, "Hello there")
        self.assertEqual(result["score"], 1.0)
        self.assertTrue(result["passed"])

    def test_run_suite_aggregates_results(self):
        suite = {"name": "Tiny", "cases": [{"name": "One", "prompt": "Hi"}]}
        report = run_suite(suite, lambda prompt: prompt)
        self.assertEqual(report["summary"], {"cases": 1, "passed": 1, "average_score": 1.0})


if __name__ == "__main__":
    unittest.main()
