"""P2.4 G2 read-only preparation gate; no Minecraft side effects."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from qa_p24_g2 import gate, main, LATCH_NAME

REPO = Path(__file__).resolve().parents[1]


class P24G2GateTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / "out"

    def guard(self):
        return gate(REPO, self.root)

    def make_latch(self, contents: bytes):
        p = self.root / "logs" / LATCH_NAME
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(contents)
        return p

    def make_csv(self, contents: bytes = b"older evidence"):
        p = self.root / "results" / "USER_UPLOAD_THIS_P23_STATUS.csv"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(contents)
        return p

    def test_fresh_root_safely_allows_local_prep_without_writing(self):
        self.assertFalse(self.root.exists())
        r = self.guard()
        self.assertEqual(r["decision"], "ALLOW_PREPARE")
        self.assertEqual(r["reason"], "FIRST_TIME_NO_P23_EVIDENCE")
        self.assertFalse(self.root.exists())

    def test_ready_existing_latch_allows_prep_without_changing_it(self):
        latch = self.make_latch(b"READY_P23")
        before = latch.read_bytes()
        r = self.guard()
        self.assertEqual(r["reason"], "EXISTING_UNUSED_READY_LATCH")
        self.assertEqual(latch.read_bytes(), before)

    def test_used_latch_fails_closed_and_retained(self):
        latch = self.make_latch(b"USED_P23")
        self.assertEqual(self.guard()["reason"], "USED_LATCH_NEVER_RESET")
        self.assertEqual(latch.read_bytes(), b"USED_P23")

    def test_corrupt_latch_fails_closed(self):
        latch = self.make_latch(b"BROKEN")
        self.assertEqual(self.guard()["decision"], "REFUSE")
        self.assertEqual(latch.read_bytes(), b"BROKEN")

    def test_ready_latch_with_extra_newline_fails_closed(self):
        self.make_latch(b"READY_P23\n")
        self.assertEqual(self.guard()["reason"], "UNKNOWN_LATCH_PRESERVE")

    def test_bom_latch_fails_closed(self):
        self.make_latch(b"\xef\xbb\xbfREADY_P23")
        self.assertEqual(self.guard()["decision"], "REFUSE")

    def test_existing_csv_fails_even_if_latch_missing(self):
        csv = self.make_csv()
        self.assertEqual(self.guard()["reason"], "P23_CSV_EXISTS_PRESERVE_HISTORY")
        self.assertEqual(csv.read_bytes(), b"older evidence")

    def test_existing_empty_csv_fails(self):
        self.make_csv(b"")
        self.assertEqual(self.guard()["decision"], "REFUSE")

    def test_ready_plus_old_csv_fails(self):
        self.make_latch(b"READY_P23")
        self.make_csv(b"evidence")
        self.assertEqual(self.guard()["decision"], "REFUSE")

    def test_root_not_directory_fails(self):
        self.root.write_bytes(b"not a directory")
        self.assertEqual(self.guard()["reason"], "OUTPUT_ROOT_IS_NOT_DIRECTORY")

    def test_logs_file_not_directory_fails(self):
        self.root.mkdir()
        (self.root / "logs").write_bytes(b"not a directory")
        self.assertEqual(self.guard()["reason"], "OUTPUT_SUBDIR_NOT_DIRECTORY")

    def test_results_file_not_directory_fails(self):
        self.root.mkdir()
        (self.root / "results").write_bytes(b"not a directory")
        self.assertEqual(self.guard()["decision"], "REFUSE")

    def test_unpinned_source_fails(self):
        other = Path(self.t.name) / "badrepo"
        (other / "makecode").mkdir(parents=True)
        (other / "makecode" / "limitlab_p2_3.ts").write_bytes(b"tampered")
        r = gate(other, self.root)
        self.assertEqual(r["reason"], "SOURCE_NOT_PINNED")
        self.assertFalse(self.root.exists())

    def test_missing_source_fails(self):
        other = Path(self.t.name) / "badrepo"
        r = gate(other, self.root)
        self.assertEqual(r["decision"], "REFUSE")

    def test_linked_root_fails_when_supported(self):
        original = Path(self.t.name) / "original"
        original.mkdir()
        try:
            self.root.symlink_to(original, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink requires platform permissions")
        self.assertEqual(self.guard()["reason"], "REDIRECTED_PATH_NOT_ALLOWED")

    def test_linked_logs_fails_when_supported(self):
        self.root.mkdir()
        target = Path(self.t.name) / "logs-source"
        target.mkdir()
        try:
            (self.root / "logs").symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink requires platform permissions")
        self.assertEqual(self.guard()["decision"], "REFUSE")

    def test_no_files_written_when_used(self):
        latch = self.make_latch(b"USED_P23")
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob("*") if p.is_file()}
        self.guard()
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(latch.read_bytes(), b"USED_P23")

    def test_cli_preflight_blocks_but_inspect_returns_zero(self):
        import subprocess
        code = REPO / "tools" / "qa_p24_g2.py"
        blocked = self.make_latch(b"USED_P23")
        cmd = [sys.executable, str(code), "preflight", "--repo", str(REPO),
               "--output-root", str(self.root)]
        check = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        self.assertEqual(check.returncode, 3)
        self.assertIn("USED_LATCH_NEVER_RESET", check.stdout)
        cmd[2] = "inspect"
        check = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        self.assertEqual(check.returncode, 0)
        self.assertEqual(blocked.read_bytes(), b"USED_P23")


if __name__ == "__main__":
    unittest.main()
