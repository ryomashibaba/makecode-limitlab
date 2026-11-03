#!/usr/bin/env python3
import importlib.util,json,tempfile,unittest
from pathlib import Path
from PIL import Image

SRC=Path(__file__).resolve().parents[1]/"tools/g4c7_r1_negative_only_vision_gate.py"
spec=importlib.util.spec_from_file_location("g4c7_negative",SRC)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class NegativeOnlyHistoricalControls(unittest.TestCase):
 def test_uniform_black_eye_is_not_visible(self):
  with tempfile.TemporaryDirectory() as dir:
   p=Path(dir)/"HABITAT_EYE_CYCLES_TRUE_NATIVE.png"
   Image.new("RGB",(960,600),(2,3,4)).save(p)
   result=module.metrics(p)
   self.assertEqual(result["center_dark_ratio"],1.0)
   self.assertLess(result["sample_distinct_colors"],48)

 def test_synthetic_bright_image_cannot_be_certified_as_art(self):
  with tempfile.TemporaryDirectory() as dir:
   p=Path(dir)/"AERIAL_CYCLES_TRUE_NATIVE.png"
   Image.new("RGB",(960,600),(140,160,180)).save(p)
   result=module.metrics(p)
   self.assertEqual(result["center_dark_ratio"],0)
   # A completely bland image with many bright pixels is *still* bad art.
   self.assertEqual(result["sample_distinct_colors"],1)

 def test_missing_independent_manifest_fails_closed(self):
  with tempfile.TemporaryDirectory() as dir:
   with self.assertRaisesRegex(ValueError,"MANIFEST"):
    module.audit(dir)

 def test_bad_native_file_fails_closed(self):
  with tempfile.TemporaryDirectory() as dir:
   p=Path(dir)/"INDEPENDENT_SAME_NATIVE_FIVE_TRUE_CYCLES_AUDIT.json"
   p.write_text(json.dumps({
    "schema":"g4c7-r1-civic-braid-single-native-reopen-art-review-v1",
    "art":"HOLD","official_art_adoptions":0,"minecraft":"FORBIDDEN",
    "formal_331_body_993_foot":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
    "native_file":"not-real.blend","native_sha256":"f"*64
   }))
   with self.assertRaisesRegex(ValueError,"NATIVE_SOURCE_HASH_MISMATCH"):
    module.audit(dir)

 def test_authentic_rejected_blend_triggers_habitat_flag(self):
  base=Path("artifacts/g4c7-r1-civic-braid-authorial-section-ART-UNREVIEWED")
  if not base.is_dir():self.skipTest("Saved-native fixture only present on GitHub Actions")
  report=module.audit(base)
  self.assertEqual(report["result"],"BLOCK_VISUAL_OBSERVABILITY")
  self.assertTrue(report["never_proves_visual_art_acceptance"])
  self.assertEqual(report["art"],"HOLD")
  flagged=[f["view"] for f in report["blocking_evidence"]]
  self.assertIn("HABITAT_EYE",flagged)
  self.assertEqual(report["views"]["HABITAT_EYE"]["center_dark_ratio"],1.0)

if __name__=="__main__":unittest.main()
