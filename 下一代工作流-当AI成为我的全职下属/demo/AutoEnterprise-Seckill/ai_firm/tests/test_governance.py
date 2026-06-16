from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cheat_detector import scan
from context_pruner import JavaContextPruner


class GovernanceTest(unittest.TestCase):
    def test_detector_finds_weakened_assertion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "BrokenTest.java").write_text("assertTrue(true);", encoding="utf-8")
            self.assertTrue(any("ALWAYS_TRUE" in item for item in scan(root)))

    def test_pruner_follows_project_import(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "com/example/A.java"
            dependency = root / "com/example/B.java"
            target.parent.mkdir(parents=True)
            target.write_text("package com.example;\nimport com.example.B;\nclass A {}", encoding="utf-8")
            dependency.write_text("package com.example;\nclass B {}", encoding="utf-8")
            result = JavaContextPruner(root, max_depth=1).prune(target)
            self.assertEqual(2, result["file_count"])


if __name__ == "__main__":
    unittest.main()

