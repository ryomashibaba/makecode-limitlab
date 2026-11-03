"""Hash-bound, one-revision-only native Blender ART HOLD gate tests."""
import copy
import importlib.util
import hashlib
from pathlib import Path
import tempfile
import unittest

PATH=Path(__file__).resolve().parents[1]/"tools"/"g4c7_m37p2_feedback_to_native_revision.py"
spec=importlib.util.spec_from_file_location("p2_feedback_native_revision",PATH)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SRC="a"*64
FEED="b"*64

def fixture_feedback():
    return {
        "outcome":"EARLY_ART_REJECT","art":"HOLD",
        "official_adoptions":0,"minecraft":"FORBIDDEN",
        "original_stored_blend_sha256":SRC,
        "reasons":["TWO_CUBOIDS_8_VERTICES_6_FACES_EACH",
                   "MISSING_HABITAT_LIVING_INTERIOR"],
    }

def fixture_revision():
    return {
        "source_sha256":SRC,
        "feedback_sha256":FEED,
        "purpose":"SINGLE_TECH_REVISION_NOT_ART",
        "responds_to":["TWO_CUBOIDS_8_VERTICES_6_FACES_EACH"],
        "art_intent":"ART-HOLD topology modification only, small scoped city/habitat sample; not real city.",
        "actions":[
            {"role":"city_macro","op":"inset_facing_face","face":"TOP","inset":0.14,
             "why":"Test a visible surface recess on a selected face, not the entire object."},
            {"role":"habitat","op":"extrude_facing_face","face":"FRONT","delta":[0,0.6,0],
             "why":"Test a different face depth profile without introducing repeated object seeds."},
        ],
    }

class NativeFeedbackPlanSafety(unittest.TestCase):
    def test_valid_single_study_only(self):
        self.assertEqual(m.validate(fixture_revision(),fixture_feedback(),SRC,FEED),[])

    def test_require_actual_feedback_reject(self):
        f=fixture_feedback()
        f["outcome"]="ART_HOLD_VISUAL_JUDGMENT_REQUIRED"
        self.assertIn("FEEDBACK_MUST_BE_GENUINE_REJECT_HOLD",
                      m.validate(fixture_revision(),f,SRC,FEED))

    def test_protected_blend_hash_required(self):
        p=fixture_revision()
        p["source_sha256"]="fake"
        self.assertIn("PLAN_SOURCE_SHA_MISMATCH",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_hash_for_actual_three_image_feedback_required(self):
        p=fixture_revision()
        p["feedback_sha256"]="wrong"
        self.assertIn("PLAN_FEEDBACK_SHA_MISMATCH",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_unproven_repair_claim(self):
        p=fixture_revision()
        p["responds_to"]=["AI_says_city_is_beautiful"]
        self.assertIn("NO_VERIFIED_EARLY_REJECT_REASON_BINDING",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_untrusted_generated_code(self):
        p=fixture_revision()
        p["actions"][0]["python"]="import os"
        self.assertIn("ACTION_0_UNKNOWN_ARGUMENT",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_new_objects_and_world_modifications(self):
        p=fixture_revision()
        p["actions"][0]["op"]="begin_surface"
        p["world_write"]=True
        errors=m.validate(p,fixture_feedback(),SRC,FEED)
        self.assertIn("ACTION_0_OP_FORBIDDEN",errors)
        self.assertIn("UNKNOWN_TOP_LEVEL_CONTROL",errors)

    def test_reject_missing_both_existing_roles(self):
        p=fixture_revision()
        p["actions"][1]["role"]="city_macro"
        self.assertIn("MUST_EDIT_BOTH_EXISTING_ROLES",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_excessive_move(self):
        p=fixture_revision()
        p["actions"][1]["delta"]=[0,100,0]
        self.assertIn("ACTION_1_BAD_DELTA",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_unbounded_loop_actions(self):
        p=fixture_revision()
        p["actions"]=p["actions"]*5
        self.assertIn("ACTION_COUNT_NOT_2_TO_8",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_reject_art_promote(self):
        p=fixture_revision()
        p["promote_art"]=True
        self.assertIn("UNKNOWN_TOP_LEVEL_CONTROL",
                      m.validate(p,fixture_feedback(),SRC,FEED))

    def test_real_three_image_digest_binding_and_tamper_rejection(self):
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d)
            report=fixture_feedback()
            report["verified_images_sha256"]={}
            magic=bytes.fromhex("89504e470d0a1a0a")
            for view in ("AERIAL","PUBLIC_EYE","HABITAT_EYE"):
                name="P2_PAIRED_NATIVE_"+view+"_NO_ART.png"
                raw=magic+b"QA_IMAGE_PAYLOAD_NOT_ART"*6
                (directory/name).write_bytes(raw)
                report["verified_images_sha256"][view]=hashlib.sha256(raw).hexdigest()
            self.assertTrue(m.verify_visual_evidence_files(directory/"feedback.json",report))
            (directory/"HABITAT_EYE.png").write_bytes(b"unused")
            changed=directory/"P2_PAIRED_NATIVE_HABITAT_EYE_NO_ART.png"
            changed.write_bytes(magic+b"TAMPERED_DIFFERENT_PIXELS"*6)
            with self.assertRaisesRegex(ValueError,"VISUAL_SOURCE_CHANGED"):
                m.verify_visual_evidence_files(directory/"feedback.json",report)

    def test_missing_image_set_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,"THREE_VERIFIED_REAL_IMAGE"):
                m.verify_visual_evidence_files(Path(d)/"f.json",fixture_feedback())


if __name__=="__main__":
    unittest.main()
