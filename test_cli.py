import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from model_eval.cli import main


class CliTests(unittest.TestCase):
    def test_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as directory:
            suite = Path(directory) / "suite.json"
            report = Path(directory) / "report.json"
            suite.write_text(json.dumps({"name": "Test", "cases": []}), encoding="utf-8")
            argv = ["model-eval", "run", str(suite), "--output", str(report)]
            with patch.object(sys, "argv", argv):
                self.assertEqual(main(), 0)
            self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["suite"], "Test")


if __name__ == "__main__":
    unittest.main()
