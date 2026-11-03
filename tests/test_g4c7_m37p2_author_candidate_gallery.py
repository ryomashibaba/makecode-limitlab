"""Offline authentic-image/Blender hash binding tests. NOT art or Blender QA."""
import importlib.util
import json
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from PIL import Image

SCRIPT = Path(__file__).resolve().parents[1] / 'tools/g4c7_m37p2_author_candidate_gallery.py'
spec = importlib.util.spec_from_file_location('g4c7_gallery', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestGallery(unittest.TestCase):
    def setUp(self):
        t = TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.d = Path(t.name)
        self.blend = self.d / 'DIRECT_ARTIST_SOURCE_UNAPPROVED.blend'
        self.blend.write_bytes(b'BLENDER_native_sample_fixture_only')
        self.data = {
            'schema': 'g4c7-m37p2-artist-native-early-review-v1',
            'source_blend': self.blend.name,
            'source_sha256_before_and_after': m.digest(self.blend),
            'official_adoption': 0, 'Minecraft': 'FORBIDDEN',
            'formal_331_993': 'NOT_RUN', 'G0_S1_G1_G2_G3': 'NOT_RUN',
            'absolute_art': 'NOT_ASSESSED_HUMAN_ABSOLUTE_REVIEW_REQUIRED',
            'early_native_three_view_renders': {},
        }
        for name in m.VIEWS:
            fn = 'M37P2_' + name + '.png'
            Image.new('RGB', (480, 300), (108, 124, 140)).save(self.d / fn)
            self.data['early_native_three_view_renders'][name] = dict(name=fn, sha256=m.digest(self.d/fn))
        self.save()

    def save(self):
        (self.d/m.MANIFEST).write_text(json.dumps(self.data), encoding='utf-8')

    def test_gallery_exact_three_render_images_embedded_and_bound_to_blend(self):
        before = m.digest(self.blend)
        result = m.build(self.d, self.blend)
        self.assertEqual(result['result'], 'ART_HOLD_HUMAN_CRITIQUE_REQUIRED')
        self.assertFalse(result['human_accepted_art'])
        self.assertFalse(result['geometry_generated'])
        self.assertEqual(before, m.digest(self.blend))
        self.assertEqual(result['official_adoptions'], 0)
        self.assertEqual((self.d/m.HTML).read_text().count('data:image/png;base64,'), 3)
        self.assertEqual((self.d/m.README).read_text().count('![Blender'), 3)
        with self.assertRaises(FileExistsError): m.build(self.d, self.blend)

    def test_black_one_view_yields_art_reject_but_does_not_hide_image(self):
        path = self.d/'M37P2_HABITAT_EYE.png'
        Image.new('RGB', (480, 300), (0, 0, 0)).save(path)
        self.data['early_native_three_view_renders']['HABITAT_EYE']['sha256'] = m.digest(path)
        self.save()
        result = m.build(self.d, self.blend)
        self.assertEqual(result['result'], 'EARLY_ART_REJECT_BLACK_VIEW')
        self.assertEqual(result['official_adoptions'], 0)

    def test_reject_source_blend_changed_after_render(self):
        self.blend.write_bytes(b'UNEXPECTED_AUTHOR_SOURCE_CHANGE')
        with self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED'):
            m.build(self.d, self.blend)

    def test_reject_tampered_png_even_if_valid_png(self):
        path = self.d/'M37P2_AERIAL.png'
        Image.new('RGB',(480,300),(250,120,40)).save(path)
        with self.assertRaisesRegex(ValueError,'PNG_SHA_MISMATCH'):
            m.build(self.d,self.blend)

    def test_reject_false_official_art_and_minecraft(self):
        self.data['official_adoption'] = 1
        self.save()
        with self.assertRaisesRegex(ValueError,'CHARTER'):
            m.build(self.d,self.blend)
        self.data['official_adoption'] = 0
        self.data['Minecraft'] = 'ALLOWED'
        self.save()
        with self.assertRaisesRegex(ValueError,'CHARTER'):
            m.build(self.d,self.blend)

    def test_reject_missing_or_inconsistent_three_images(self):
        del self.data['early_native_three_view_renders']['PUBLIC_EYE']
        self.save()
        with self.assertRaisesRegex(ValueError,'THREE_GENUINE'):
            m.build(self.d,self.blend)

if __name__ == '__main__': unittest.main()
