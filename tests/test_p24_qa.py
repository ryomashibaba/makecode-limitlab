"""G1 safety regression: no Minecraft or persistent state mutations."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from qa_p24 import (
    CSV_NAME, EXPECTED_P23_BLOB, csv_check, fingerprint, fresh_and_stable,
    git_blob_sha, inspect, latch_check, source_check,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_p23_tools import completed


class G1ReadOnlyTests(unittest.TestCase):
    def test_pinned_source_is_exact_repo_file(self):
        repo = Path(__file__).resolve().parents[1]
        result = source_check(repo)
        self.assertEqual(result["state"], "PINNED_SOURCE_OK")
        self.assertEqual(result["actual_git_blob"], EXPECTED_P23_BLOB)

    def test_source_mismatch_fail_closed(self):
        with TemporaryDirectory() as d:
            repo = Path(d)
            file = repo / "makecode" / "limitlab_p2_3.ts"
            file.parent.mkdir()
            file.write_text("untrusted script", encoding="utf8")
            self.assertEqual(source_check(repo)["state"], "SOURCE_MISMATCH")

    def test_crlf_sha_normalization(self):
        self.assertEqual(git_blob_sha(b"a\r\nb\r\n"), git_blob_sha(b"a\nb\n"))

    def test_latch_never_created(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(latch_check(root)["state"], "LATCH_MISSING")
            self.assertEqual(list(root.iterdir()), [])

    def test_ready_and_used_latches_preserved(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            logs = root / "logs"
            logs.mkdir()
            latch = logs / "P23_ONCE.txt"
            latch.write_text("READY_P23", encoding="utf8")
            self.assertEqual(latch_check(root)["state"], "READY_NOT_PROOF_OF_SAFE_SITE")
            latch.write_text("USED_P23", encoding="utf8")
            before = latch.read_bytes()
            self.assertEqual(latch_check(root)["state"], "USED_DO_NOT_RESET")
            self.assertEqual(latch.read_bytes(), before)

    def test_unknown_latch_is_not_reset(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "logs").mkdir()
            latch = root / "logs" / "P23_ONCE.txt"
            latch.write_text("CORRUPTED")
            self.assertEqual(latch_check(root)["state"], "LATCH_UNKNOWN_DO_NOT_CHANGE")
            self.assertEqual(latch.read_text(), "CORRUPTED")

    def test_missing_csv(self):
        with TemporaryDirectory() as d:
            self.assertEqual(csv_check(Path(d) / CSV_NAME)["state"], "CSV_MISSING")

    def test_complete_is_sampled_not_exact(self):
        with TemporaryDirectory() as d:
            path = Path(d) / CSV_NAME
            path.write_text(completed(), encoding="utf8")
            report = csv_check(path)
            self.assertEqual(report["state"], "FAST_COMPLETED_SAMPLED_NOT_EXACT")
            self.assertTrue(report["sampled_only"])
            self.assertFalse(report["whole_district_exact"])

    def test_invalid_csv_never_success(self):
        with TemporaryDirectory() as d:
            path = Path(d) / CSV_NAME
            path.write_text("broken csv", encoding="utf8")
            self.assertEqual(csv_check(path)["state"], "CSV_INVALID_OR_PARTIAL")

    def test_existing_csv_not_fresh(self):
        with TemporaryDirectory() as d:
            path = Path(d) / CSV_NAME
            path.write_text(completed(), encoding="utf8")
            original = fingerprint(path)
            self.assertFalse(fresh_and_stable(original, original, original))

    def test_changed_unstable_csv_not_reported(self):
        with TemporaryDirectory() as d:
            path = Path(d) / CSV_NAME
            path.write_text(completed(), encoding="utf8")
            baseline = fingerprint(path)
            path.write_text(completed() + "\n", encoding="utf8")
            current = fingerprint(path)
            self.assertFalse(fresh_and_stable(baseline, baseline, current))
            self.assertTrue(fresh_and_stable(baseline, current, current))

    def test_fingerprint_absent_no_files_created(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            self.assertIsNone(fingerprint(root / CSV_NAME))
            self.assertEqual(list(root.iterdir()), [])

    def test_inspect_preserves_existing_bytes(self):
        with TemporaryDirectory() as d:
            root = Path(d)
            (root / "results").mkdir()
            (root / "logs").mkdir()
            csv = root / "results" / CSV_NAME
            latch = root / "logs" / "P23_ONCE.txt"
            csv.write_text(completed(), encoding="utf8")
            latch.write_text("USED_P23", encoding="utf8")
            before = (csv.read_bytes(), latch.read_bytes())
            report = inspect(Path(__file__).resolve().parents[1], root)
            self.assertEqual(report["csv"]["state"], "FAST_COMPLETED_SAMPLED_NOT_EXACT")
            self.assertEqual((csv.read_bytes(), latch.read_bytes()), before)


if __name__ == "__main__":
    unittest.main()
