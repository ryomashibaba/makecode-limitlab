import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p15 import evaluate

HEADER = "Version,Stage,Completed,Total,Status,Detail\n"
BASE = "P1.5,RUN,0,0,BEGIN,segmented_only_no_endurance\n"
SOURCE = "P1.5,SOURCE,32768,32768,PASS,64_tiles_exact_to_verified_seed\n"
FILL = "P1.5,FILL32768,32768,32768,PASS,64_tiles_full_exact_comparison\n"
CLONE = "P1.5,CLONE32768,32768,32768,PASS,64_tiles_full_exact_comparison\n"
FINISH = "P1.5,RUN,1,1,PASS,32768_SOURCE_FILL_CLONE_EXACT\n"

class AnalyzerTests(unittest.TestCase):
    def evaluate_text(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.csv"
            path.write_text(content, encoding="utf-8")
            return evaluate(path)

    def test_complete(self):
        v = self.evaluate_text(HEADER + BASE + SOURCE + FILL + CLONE + FINISH)
        self.assertEqual(v["verdict"], "PASS")
        self.assertTrue(all(v["stage_pass"].values()))

    def test_partial_never_claims_success(self):
        v = self.evaluate_text(HEADER + BASE + SOURCE + FILL)
        self.assertEqual(v["verdict"], "INCOMPLETE")

    def test_stop(self):
        v = self.evaluate_text(HEADER + BASE + SOURCE +
                               "P1.5,RUN,4,8,STOP,USER_STOP\n")
        self.assertEqual(v["verdict"], "STOPPED")

    def test_inconsistent_final_without_stages(self):
        v = self.evaluate_text(HEADER + BASE + FINISH)
        self.assertEqual(v["verdict"], "INCOMPLETE")

    def test_invalid_csv_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate_text("Bad,Header\nfoo,bar\n")

    def test_non_p15_rejected(self):
        with self.assertRaises(ValueError):
            self.evaluate_text(HEADER + "P1.4,RUN,1,1,PASS,x\n")

if __name__ == "__main__":
    unittest.main()
