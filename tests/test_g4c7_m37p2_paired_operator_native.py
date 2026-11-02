"""M37-P2 native Blender editor action gate: no model-generated Python executed."""
import importlib.util
from pathlib import Path
import unittest

SRC = Path(__file__).resolve().parents[1] / "tools" / "g4c7_m37p2_native_operator_author.py"
spec = importlib.util.spec_from_file_location("g4c7_m37p2_native_operator_author", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def technical_fixture_not_art():
    return {
        "art_intent": "A technical test of paired macro and inhabited forms only; not a city design.",
        "actions": [
            {"op":"begin_surface","role":"city_macro","location":[-8,0,0],
             "intent":"Create an editable seed to test a city-related sculpt stroke."},
            {"op":"extrude_face","role":"city_macro","delta":[0,0,3],
             "intent":"Confirm one genuine native extrude operator works."},
            {"op":"inset_face","role":"city_macro","thickness":0.15,
             "intent":"Confirm a native inset can alter the selected surface."},
            {"op":"translate_selection","role":"city_macro","delta":[0.7,0,0.5],
             "intent":"Native operator translation changes mesh topology shape."},
            {"op":"begin_surface","role":"habitat","location":[4,2,0],
             "intent":"Create separate nearby lived-section mesh seed."},
            {"op":"extrude_face","role":"habitat","delta":[0,0,2],
             "intent":"Native edit makes a short spatial profile study."},
            {"op":"inset_face","role":"habitat","thickness":0.2,
             "intent":"Model directed inset for temporary private-space study."},
            {"op":"translate_selection","role":"habitat","delta":[0,1,0.4],
             "intent":"Native edit operation on habitat-scope mesh only."},
        ],
    }


class OperatorGate(unittest.TestCase):
    def test_fixture_valid_only_as_technical_input(self):
        self.assertEqual(mod.validate_actions(technical_fixture_not_art()), [])

    def test_reject_explicit_generated_python(self):
        plan = technical_fixture_not_art()
        plan["actions"][1]["python"] = "import os"
        self.assertIn("ACTION_1_UNKNOWN_PARAMETERS", mod.validate_actions(plan))

    def test_reject_unlisted_operator(self):
        plan = technical_fixture_not_art()
        plan["actions"][2]["op"] = "execute_blender_code"
        self.assertIn("ACTION_2_ROLE_OR_OPERATOR_NOT_ALLOWED", mod.validate_actions(plan))

    def test_reject_city_without_habitat(self):
        plan = technical_fixture_not_art()
        plan["actions"] = plan["actions"][:4]
        self.assertIn("PAIR_MISSING_habitat", mod.validate_actions(plan))

    def test_reject_second_seed(self):
        plan = technical_fixture_not_art()
        plan["actions"][2] = {"op":"begin_surface","role":"city_macro","location":[5,0,0],
              "intent":"A repeated seed should be blocked by the first-pair charter."}
        self.assertIn("ACTION_2_SECOND_SEED_FORBIDDEN", mod.validate_actions(plan))

    def test_reject_world_write_and_art_promotion(self):
        plan = technical_fixture_not_art()
        plan["world_write"] = True
        plan["promote_art"] = True
        self.assertIn("FORBIDDEN_PRODUCTION_ACTION", mod.validate_actions(plan))

    def test_reject_nonfinite_move(self):
        plan = technical_fixture_not_art()
        plan["actions"][1]["delta"] = [float("nan"),0,0]
        self.assertIn("ACTION_1_BAD_EDIT_DELTA", mod.validate_actions(plan))


if __name__ == "__main__":
    unittest.main()
