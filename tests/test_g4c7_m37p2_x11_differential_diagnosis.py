"""No fake GUI/ART PASS from diagnostic pixels or conflicting source reports."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/g4c7_m37p2_x11_differential_diagnosis.py'
spec = importlib.util.spec_from_file_location('p2_differential', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def pix(visible):
    if visible is None:
        return {'exists': False}
    return {'exists': True, 'size': [600, 700],
            'visible_bright_fraction': 0.6 if visible else 0.0,
            'all_black': not visible}


def stats(macro=False, lived=False, root=False, window=False):
    return dict(zip(m.LABELS, (pix(macro), pix(lived), pix(root), pix(window))))


class TestTriage(unittest.TestCase):
    def verdict(self, entries):
        d = m.classify(entries)
        self.assertEqual(d['art'], 'HOLD')
        self.assertEqual(d['official_adoptions'], 0)
        self.assertFalse(d['classification_is_root_cause_proof'])
        self.assertFalse(d['x11_window_is_editor_evidence'])
        return d['decision']

    def test_black_native_bright_blender_x11_window(self):
        self.assertEqual(self.verdict(stats(root=True, window=True)),
            'NATIVE_EDITORS_BLACK_X11_BLENDER_WINDOW_NONBLACK')

    def test_black_window_but_bright_x11_root(self):
        self.assertEqual(self.verdict(stats(root=True)),
            'NATIVE_EDITORS_AND_X11_WINDOW_BLACK_ROOT_NONBLACK')

    def test_everything_black_not_blender_root_cause_proof(self):
        self.assertEqual(self.verdict(stats()),
            'NATIVE_EDITORS_AND_X11_WINDOW_AND_ROOT_BLACK')

    def test_actual_native_pixels_do_not_certify_art(self):
        self.assertEqual(self.verdict(stats(macro=True, lived=True, root=True, window=True)),
            'NATIVE_EDITORS_NONBLACK_ONLY_NOT_VALIDATED_AS_ART')

    def test_mixed_editor_capture_is_not_called_pass(self):
        self.assertEqual(self.verdict(stats(macro=True, root=True, window=True)),
            'NATIVE_EDITOR_VISIBILITY_MIXED_INVESTIGATE')

    def test_unavailable_x11_window_is_unknown(self):
        self.assertEqual(self.verdict(stats(root=True, window=None)),
            'NATIVE_EDITORS_BLACK_X11_WINDOW_EVIDENCE_INSUFFICIENT')

    def test_missing_native_capture_refuses_classification(self):
        self.assertEqual(self.verdict(stats(macro=None, lived=False, root=True, window=True)),
            'NATIVE_EDITOR_EVIDENCE_INCOMPLETE')

    def test_conflicting_pixel_metadata_refused(self):
        case=stats(macro=True, lived=True, root=True, window=True)
        case['MACRO_EDITOR']['all_black'] = True
        self.assertEqual(self.verdict(case), 'NATIVE_EDITOR_EVIDENCE_INCOMPLETE')

    def test_missing_report_creates_explicit_unknown_without_art_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'report.json'
            r=m.diagnose(Path(tmp)/'NO_REPORT.json', dest)
            self.assertEqual(r['decision'], 'INDEPENDENT_PIXEL_REPORT_MISSING')
            self.assertIsNone(r['source_sha256'])
            self.assertEqual(json.loads(dest.read_text())['official_adoptions'], 0)
            with self.assertRaisesRegex(FileExistsError, 'APPEND_ONLY'):
                m.diagnose(Path(tmp)/'NO_REPORT.json', dest)

    def test_source_hash_integrity_and_size_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=Path(tmp)/'stats.json'
            src.write_text(json.dumps(stats(root=True,window=True)))
            r=m.diagnose(src, Path(tmp)/'report.json')
            self.assertEqual(len(r['source_sha256']), 64)
            src.write_text(' '*(m.MAX_SOURCE_BYTES + 1))
            with self.assertRaisesRegex(ValueError, 'SAFE_LIMIT'):
                m.diagnose(src,Path(tmp)/'different.json')


if __name__ == '__main__':
    unittest.main()
