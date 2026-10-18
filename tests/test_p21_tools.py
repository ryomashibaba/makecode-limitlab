"""Mutate an actual mock transcript; never store private hardware results."""
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.analyze_p21 import evaluate

class TranscriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (Path(__file__).resolve().parents[1] / 'build/p21_mock_status.csv').read_text()

    def assess(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'test.csv'
            p.write_text(text, encoding='utf8')
            return evaluate(p)['verdict']

    def reject(self, text):
        with self.assertRaises(ValueError):
            self.assess(text)

    def test_success(self):
        self.assertEqual(self.assess(self.text), 'ALL_PASS')

    def test_negative_candidate_coordinates(self):
        self.assertEqual(self.assess(self.text.replace('candidate_1_x16_y16_z24', 'candidate_1_x-368_y16_z-360')), 'ALL_PASS')

    def test_every_truncated_prefix_is_incomplete(self):
        rows = self.text.splitlines(True)
        for n in range(2, len(rows)):
            self.assertEqual(self.assess(''.join(rows[:n])), 'INCOMPLETE')

    def test_stop_at_each_prefix_is_stopped(self):
        rows = self.text.splitlines(True)
        for n in range(2, len(rows)):
            self.assertEqual(self.assess(''.join(rows[:n]) + 'P2.1,RUN,0,0,STOP,USER_STOP\n'), 'STOPPED')

    def test_missing_pass_rejected(self):
        self.reject(''.join(r for r in self.text.splitlines(True) if ',BEFORE_PATCH,' not in r))

    def test_duplicate_pass_rejected(self):
        r = next(r for r in self.text.splitlines(True) if ',SOURCE,' in r and ',PASS,' in r)
        self.reject(self.text.replace(r, r+r))

    def test_false_finished_without_evidence(self):
        r = self.text.splitlines(True)
        self.reject(''.join(r[:2] + r[-1:]))

    def test_reordered_writes(self):
        r = self.text.splitlines(True)
        r[-4], r[-5] = r[-5], r[-4]
        self.reject(''.join(r))

    def test_wrong_volume(self):
        self.reject(self.text.replace(',39270,39270,PASS,', ',1,1,PASS,'))

    def test_wrong_plan(self):
        self.reject(self.text.replace('w35_h33_d34', 'w36_h33_d34'))

    def test_unsafe_chunk(self):
        self.reject(self.text.replace('chunk32x16x32', 'chunk32x32x32'))

    def test_unsafe_patch(self):
        self.reject(self.text.replace('patch16x16x16x16', 'patch24x16x16x16'))

    def test_rows_after_finish(self):
        self.reject(self.text+'P2.1,RUN,0,0,STOP,USER_STOP\n')

    def test_duplicate_begin(self):
        r=self.text.splitlines(True)
        self.reject(''.join(r[:2]+r[1:]))

    def test_wrong_version(self):
        self.reject(self.text.replace('P2.1', 'P2.0', 1))

    def test_extra_column(self):
        self.reject(self.text.replace('full_build_clone_patch_verified', 'full_build_clone_patch_verified,EXTRA'))

    def test_bad_counter(self):
        self.reject(self.text.replace(',0,0,BEGIN,', ',NaN,0,BEGIN,'))

    def test_empty(self):
        self.reject('Version,Stage,Units,Total,Status,Detail\n')

if __name__ == '__main__':
    unittest.main()
