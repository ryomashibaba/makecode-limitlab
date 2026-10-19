"""G3 evidence packaging tests: no private material leaves local archive."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from g3_evidence import pack, MAX_CSV_BYTES
from qa_p24 import CSV_NAME
from test_p23_tools import B, H, completed

REPO = Path(__file__).resolve().parents[1]
CLOCK = datetime(2026, 10, 19, 9, 0, tzinfo=timezone.utc)


class G3EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "output"

    def latch(self, value: bytes = b"USED_P23"):
        f = self.root / "logs" / "P23_ONCE.txt"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(value)
        return f

    def csv(self, value: bytes):
        f = self.root / "results" / CSV_NAME
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(value)
        return f

    def make(self, uid="test0001"):
        return pack(REPO, self.root, clock=CLOCK, uid=uid)

    def test_no_files_created_with_missing_inputs(self):
        self.assertEqual(self.make()["state"], "BLOCKED")
        self.assertFalse(self.root.exists())

    def test_ready_latch_does_not_write_archive(self):
        self.latch(b"READY_P23")
        self.csv(completed().encode())
        self.assertEqual(self.make()["reason"], "NO_USED_LATCH")
        self.assertFalse((self.root / "private_results").exists())

    def test_missing_csv_does_not_write_archive(self):
        self.latch()
        self.assertEqual(self.make()["reason"], "CSV_UNAVAILABLE")

    def test_sampled_pass_bundle_contents_and_input_preservation(self):
        latch = self.latch()
        csv = self.csv(completed().encode())
        original = (latch.read_bytes(), csv.read_bytes())
        result = self.make()
        self.assertEqual(result["state"], "BUNDLED")
        self.assertFalse(result["whole_district_exact"])
        with zipfile.ZipFile(result["path"]) as z:
            self.assertEqual(set(z.namelist()),
                             {CSV_NAME, "G3_EVIDENCE_MANIFEST.json", "READ_ME_JA.txt"})
            self.assertEqual(z.read(CSV_NAME), original[1])
            manifest = json.loads(z.read("G3_EVIDENCE_MANIFEST.json"))
            self.assertEqual(manifest["verdict"], "FAST_COMPLETED_SAMPLED_NOT_EXACT")
            self.assertEqual(manifest["csv_sha256"], hashlib.sha256(original[1]).hexdigest())
            self.assertFalse(manifest["whole_district_exact"])
            self.assertFalse(manifest["minecraft_live_verified_by_this_tool"])
        self.assertEqual((latch.read_bytes(), csv.read_bytes()), original)

    def test_incomplete_valid_csv_bundles_as_incomplete(self):
        self.latch()
        self.csv((H + B).encode())
        result = self.make()
        self.assertEqual(result["state"], "BUNDLED")
        self.assertEqual(result["verdict"], "INCOMPLETE")

    def test_invalid_csv_fails_closed(self):
        self.latch()
        self.csv(b"invalid")
        self.assertEqual(self.make()["reason"], "CSV_NOT_PARSEABLE")

    def test_too_large_csv_fails_closed(self):
        self.latch()
        self.csv(b"x" * (MAX_CSV_BYTES + 1))
        self.assertEqual(self.make()["reason"], "CSV_TOO_LARGE")

    def test_existing_bundle_not_overwritten(self):
        self.latch()
        self.csv(completed().encode())
        first = self.make()
        self.assertEqual(first["state"], "BUNDLED")
        snapshot = Path(first["path"]).read_bytes()
        second = self.make()
        self.assertEqual(second["state"], "ERROR")
        self.assertEqual(Path(first["path"]).read_bytes(), snapshot)

    def test_separate_archive_ids_do_not_overwrite(self):
        self.latch()
        self.csv(completed().encode())
        self.assertEqual(self.make(uid="one")["state"], "BUNDLED")
        self.assertEqual(self.make(uid="two")["state"], "BUNDLED")

    def test_output_path_does_not_contain_source_directory_in_bundle(self):
        self.latch()
        self.csv(completed().encode())
        result = self.make()
        with zipfile.ZipFile(result["path"]) as z:
            data = z.read("G3_EVIDENCE_MANIFEST.json")
        self.assertNotIn(str(self.root).encode(), data)

    def test_unknown_source_blocks(self):
        self.latch()
        self.csv(completed().encode())
        other = Path(self.tmp.name) / "invalid_repo"
        result = pack(other, self.root, clock=CLOCK, uid="fake")
        self.assertEqual(result["reason"], "SOURCE_NOT_PINNED")

    def test_redirected_output_blocks(self):
        self.latch()
        self.csv(completed().encode())
        folder = self.root / "private_results"
        target = Path(self.tmp.name) / "elsewhere"
        target.mkdir()
        try:
            folder.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("requires symlink support")
        self.assertEqual(self.make()["reason"], "REDIRECTED_OUTPUT")


if __name__ == "__main__":
    unittest.main()
