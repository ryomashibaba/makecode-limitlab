"""Real Cycles-image gate tests. Synthetic PNG header is QA fixture NOT artwork."""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools"/"g4c7_m37p2_visual_feedback_gate.py"
spec=importlib.util.spec_from_file_location("g4c7_m37p2_visual_feedback_gate",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ReadOnlyArtVeto(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        # Data-only short fixtures; images are never presented as genuine art.
        report={
          "art":"HOLD","official_adoptions":0,"minecraft":"FORBIDDEN",
          "formal_331_993":"NOT_RUN","true_city":False,
          "human_gui_authorship":"NOT_PERFORMED",
          "camera_positions_author_approved":False,
          "factory_boundary":"NOT_AUTHORED",
          "research_culture":"NOT_AUTHORED",
          "habitat_living_interior":"NOT_AUTHORED",
          "original_stored_blend_sha256":"fake-in-test",
          "roles":{"city_macro":{"vertices":8,"faces":6},
                   "habitat":{"vertices":8,"faces":6}},
          "views":{}
        }
        for key in m.VIEWS:
            name=key+".png"
            blob=m.MAGIC+b"TEST_NON_IMAGE"*15
            (self.root/name).write_bytes(blob)
            report["views"][key]={"filename":name,
                 "sha256":hashlib.sha256(blob).hexdigest()}
        self.report=self.root/"report.json"
        self.report.write_text(json.dumps(report),encoding="utf-8")

    def test_two_cubes_and_missing_lived_city_are_rejected(self):
        data,images,gate=m.inspect(self.report)
        self.assertEqual(gate["outcome"],"EARLY_ART_REJECT")
        self.assertIn("TWO_CUBOIDS_8_VERTICES_6_FACES_EACH",gate["reasons"])
        self.assertIn("MISSING_HABITAT_LIVING_INTERIOR",gate["reasons"])
        self.assertEqual(len(images),3)

    def test_sha_tampering_is_rejected(self):
        (self.root/"AERIAL.png").write_bytes(m.MAGIC+b"CORRUPTED"*21)
        with self.assertRaisesRegex(ValueError,"SHA256_MISMATCH"):
            m.inspect(self.report)

    def test_bad_metadata_never_passes(self):
        z=json.loads(self.report.read_text())
        z["official_adoptions"]=1
        self.report.write_text(json.dumps(z))
        with self.assertRaisesRegex(ValueError,"CHARTER"):
            m.inspect(self.report)

    def test_no_formal_pass_route_even_if_scene_flags_improve(self):
        z=json.loads(self.report.read_text())
        z.update({"true_city":True,"factory_boundary":"AUTHORED",
                  "research_culture":"AUTHORED",
                  "habitat_living_interior":"AUTHORED",
                  "camera_positions_author_approved":True,
                  "human_gui_authorship":"DIRECT_GUI"})
        z["roles"]["city_macro"]={"vertices":300,"faces":400}
        z["roles"]["habitat"]={"vertices":230,"faces":310}
        self.report.write_text(json.dumps(z))
        _,_,gate=m.inspect(self.report)
        self.assertEqual(gate["outcome"],"ART_HOLD_VISUAL_JUDGMENT_REQUIRED")
        self.assertNotIn("PASS",gate["outcome"])

    def test_offline_report_does_not_call_vision_and_is_portable(self):
        result=m.run(self.report,self.root/"output")
        self.assertEqual(result["outcome"],"EARLY_ART_REJECT")
        self.assertEqual(result["vision"]["status"],"NOT_REQUESTED")
        self.assertEqual(len(list((self.root/"output").glob("*.png"))),3)
        page=(self.root/"output"/"OPEN_THREE_VIEW_VISUAL_FEEDBACK.html").read_text()
        self.assertIn("AERIAL.png",page)
        self.assertNotIn("file://",page)
        self.assertEqual(result["official_adoptions"],0)

if __name__=="__main__":unittest.main()
