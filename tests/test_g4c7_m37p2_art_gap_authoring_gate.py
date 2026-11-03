"""Quality-first: a real 3-view two-cuboid report cannot authorize another cheap repair."""
import importlib.util
from pathlib import Path
import unittest

SRC=Path(__file__).resolve().parents[1]/"tools"/"g4c7_m37p2_art_gap_authoring_gate.py"
spec=importlib.util.spec_from_file_location("art_gap_authoring_gate",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
DIGESTS={x: str(i)*64 for i,x in enumerate(mod.VIEWS,start=1)}
BLEND="f"*64

def native():
    return {
        "art":"HOLD","official_adoptions":0,"minecraft":"FORBIDDEN",
        "formal_331_993":"NOT_RUN",
        "original_stored_blend_sha256":BLEND,
        "views":{x:{"sha256":h} for x,h in DIGESTS.items()},
        "true_city":False,
        "factory_boundary":"NOT_AUTHORED",
        "research_culture":"NOT_AUTHORED",
        "habitat_living_interior":"NOT_AUTHORED",
        "roles":{"city_macro":{"vertices":8,"faces":6},
                 "habitat":{"vertices":8,"faces":6}},
    }

def feedback():
    return {
        "outcome":"EARLY_ART_REJECT","art":"HOLD",
        "official_adoptions":0,"minecraft":"FORBIDDEN",
        "formal_331_993":"NOT_RUN",
        "original_stored_blend_sha256":BLEND,
        "verified_images_sha256":dict(DIGESTS),
        "reasons":["TWO_CUBOIDS_8_VERTICES_6_FACES_EACH",
                   "MISSING_HABITAT_LIVING_INTERIOR"],
    }

class QualityGate(unittest.TestCase):
    def test_actual_previous_reject_requires_direct_artist_content(self):
        z=mod.decide(native(),feedback())
        self.assertEqual(z["decision"],"REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT")
        self.assertIn("WHOLE_DENSE_CITY_NOT_AUTHORED",z["reason_codes"])
        self.assertIn("ONLY_TWO_TECHNICAL_CUBOIDS",z["reason_codes"])
        self.assertIn("UNAUTHORED_HABITAT_LIVING_INTERIOR",z["reason_codes"])
        self.assertEqual(z["permitted_model_calls"],0)
        self.assertFalse(z["automatic_geometry_repair_allowed"])
        self.assertEqual(z["official_adoptions"],0)

    def test_extra_polygons_still_do_not_repair_absent_city(self):
        n=native()
        for role in n["roles"].values():
            role["vertices"]=1200
            role["faces"]=1800
        f=feedback()
        f["reasons"]=["MISSING_HABITAT_LIVING_INTERIOR"]
        z=mod.decide(n,f)
        self.assertEqual(z["decision"],"REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT")
        self.assertIn("WHOLE_DENSE_CITY_NOT_AUTHORED",z["reason_codes"])
        self.assertNotIn("ONLY_TWO_TECHNICAL_CUBOIDS",z["reason_codes"])

    def test_wrong_image_digest_prevents_any_call(self):
        f=feedback()
        f["verified_images_sha256"]["AERIAL"]="0"*64
        z=mod.decide(native(),f)
        self.assertEqual(z["decision"],"EVIDENCE_INVALID_SAFE_STOP")
        self.assertIn("IMAGE_DIGEST_MISMATCH_AERIAL",z["reason_codes"])
        self.assertEqual(z["permitted_model_calls"],0)

    def test_report_from_different_scene_refused(self):
        f=feedback()
        f["original_stored_blend_sha256"]="a"*64
        z=mod.decide(native(),f)
        self.assertEqual(z["decision"],"EVIDENCE_INVALID_SAFE_STOP")

    def test_unsafe_world_write_metadata_refused(self):
        n=native()
        n["minecraft"]="ALLOWED"
        self.assertEqual(mod.decide(n,feedback())["decision"],
                         "EVIDENCE_INVALID_SAFE_STOP")

    def test_formal_art_adoption_not_possible(self):
        n=native()
        n["official_adoptions"]=1
        self.assertEqual(mod.decide(n,feedback())["decision"],
                         "EVIDENCE_INVALID_SAFE_STOP")

    def test_structurally_sound_scene_still_requires_human_visual_review(self):
        n=native()
        n["true_city"]=True
        for field in mod.UNAUTHORED_FLAGS:
            n[field]="AUTHORED"
        n["roles"]={"city_macro":{"vertices":300,"faces":280},
                    "habitat":{"vertices":240,"faces":300}}
        f=feedback()
        f["outcome"]="ART_HOLD_VISUAL_JUDGMENT_REQUIRED"
        f["reasons"]=[]
        z=mod.decide(n,f)
        self.assertEqual(z["decision"],"ART_HOLD_HUMAN_VISUAL_REVIEW_REQUIRED")
        self.assertEqual(z["art"],"HOLD")
        self.assertTrue(z["human_art_approval_required"])
        self.assertFalse(z["automatic_geometry_repair_allowed"])

if __name__=="__main__":
    unittest.main()
