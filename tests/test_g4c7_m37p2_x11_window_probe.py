"""The X11 diagnostic must never be confused with real Blender VIEW_3D art."""
import importlib.util
from pathlib import Path
import os
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from types import SimpleNamespace

p = Path(__file__).resolve().parents[1] / 'tools' / 'g4c7_m37p2_x11_window_probe.py'
spec = importlib.util.spec_from_file_location('g4c7_m37p2_x11_probe', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

TREE = '''
  Root window id: 0x123
     3 children:
     0x420001 "Blender 4.5 [G4C7_P2.blend]": ("blender" "Blender") 1600x900+0+0 +0+0
     0x630002 "XTerm": ("xterm" "XTerm") 800x600+0+0 +0+0
     0x730003 "Unrelated": ("other" "Other") 200x200+0+0 +0+0
'''


class TestX11WindowProbe(unittest.TestCase):
    def test_exact_named_window_id(self):
        self.assertEqual(m.matching_x11_windows(TREE), [
            {'id': '0x420001', 'title': 'Blender 4.5 [G4C7_P2.blend]'}])

    def test_other_apps_never_misidentified_as_blender(self):
        self.assertEqual(m.matching_x11_windows(TREE, 'Nonexistent'), [])
        self.assertEqual(len(m.matching_x11_windows(TREE, 'xterm')), 1)

    def test_multiple_blender_windows_fail_closed(self):
        two = TREE + '     0x830004 "Blender additional": ("blender" "Blender") 800x600+0+0 +0+0\n'
        with TemporaryDirectory() as d, patch.dict(os.environ, {'DISPLAY': ':99'}), \
             patch.object(m.shutil, 'which', side_effect=lambda x: '/usr/bin/' + x), \
             patch.object(m.subprocess, 'run', return_value=SimpleNamespace(returncode=0, stdout=two.encode(), stderr=b'')):
            res=m.probe(d)
            self.assertEqual(res['status'], 'X11_BLENDER_WINDOW_AMBIGUOUS_NO_IMAGE')
            self.assertFalse(res['blender_editor_visual_proven'])
            self.assertEqual(res['official_adoptions'], 0)

    def test_missing_x11_display_stays_unverified(self):
        with TemporaryDirectory() as d, patch.dict(os.environ, {'DISPLAY': ''}):
            res=m.probe(d)
            self.assertEqual(res['status'], 'X11_DISPLAY_MISSING')
            self.assertEqual(res['mode'], 'X11_FULL_WINDOW_DIAGNOSTIC_ONLY_NOT_VIEW3D_NOT_ART')
            with self.assertRaisesRegex(FileExistsError, 'APPEND_ONLY'):
                m.probe(d)

    def test_image_magic_not_accepted_as_editor_evidence(self):
        with TemporaryDirectory() as d, patch.dict(os.environ, {'DISPLAY': ':99'}), \
             patch.object(m.shutil, 'which', side_effect=lambda x: '/usr/bin/' + x):
            def subprocess_fake(argv, **kw):
                if argv[0].endswith('xwininfo'):
                    return SimpleNamespace(returncode=0, stdout=TREE.encode(), stderr=b'')
                Path(argv[-1]).write_bytes(b'NOT_A_PNG' * 130)
                return SimpleNamespace(returncode=0, stdout=b'', stderr=b'')
            with patch.object(m.subprocess, 'run', side_effect=subprocess_fake):
                res=m.probe(d)
            self.assertEqual(res['status'], 'X11_BLENDER_FULL_WINDOW_BAD_IMAGE')
            self.assertFalse(res['blender_editor_visual_proven'])
            self.assertEqual(res['art'], 'HOLD')

if __name__=='__main__': unittest.main()
