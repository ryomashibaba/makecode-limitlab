"""Offline fail-closed QA for M37-P2 local AI JSON; NOT an ART city fixture."""
import copy
import math
import unittest

from tools.g4c7_m37p2_local_vertex_author import validate

ROLES = ("city_macro", "inhabited", "factory_boundary", "research_culture", "habitat")


def structural_test_only():
    meshes = []
    for i in range(10):
        vertices = []
        faces = []
        for layer in range(3):
            for k in range(6):
                a = math.pi * k / 3 + layer * .15 + i * .05
                cx = ((i % 5) - 2) * 28 + layer * 1.4
                cy = ((i // 5) - .5) * 45 + layer * 2.5
                vertices.append([
                    round(cx + (3.5 + layer * .5) * math.cos(a), 4),
                    round(cy + (4.1 - layer * .3) * math.sin(a), 4),
                    round(3 + layer * 7 + (i % 3) * 2 + math.sin(a) * 2, 4),
                ])
        for layer in range(2):
            for k in range(6):
                a = layer * 6 + k
                c = layer * 6 + (k + 1) % 6
                d = (layer + 1) * 6 + (k + 1) % 6
                e = (layer + 1) * 6 + k
                faces.extend([[a, c, d], [a, d, e]])
        meshes.append({
            "name": "CI_EPHEMERAL_NOT_CITY_" + str(i),
            "role": ROLES[i % 5],
            "why": "NON ART throwaway fixture with only numeric vertex validation",
            "vertices": vertices,
            "faces": faces,
        })
    return {
        "title": "CI geometry fixture NEVER ART",
        "design_intent": "Only validates safe geometry transport; never an art pass.",
        "meshes": meshes,
    }


class FailClosedNativeVertexTrial(unittest.TestCase):
    def test_positive_structural_fixture_only(self):
        self.assertEqual(validate(structural_test_only()), [])

    def test_duplicate_detected_despite_bad_face_count(self):
        plan = structural_test_only()
        plan["meshes"][4]["vertices"] = copy.deepcopy(plan["meshes"][0]["vertices"])
        plan["meshes"][4]["faces"] = [list(range(18))]
        failures = validate(plan)
        self.assertIn("MESH_4_BAD_TOPOLOGY_SIZE", failures)
        self.assertIn("MESH_4_DUPLICATED_VERTEX_GEOMETRY_OF_0", failures)

    def test_25_index_ngon_is_rejected(self):
        plan = structural_test_only()
        plan["meshes"][0]["faces"] = [list(range(18)), list(range(18))]
        failures = validate(plan)
        self.assertIn("MESH_0_INVALID_FACE_0", failures)
        self.assertIn("MESH_0_INVALID_FACE_1", failures)

    def test_no_meshes_is_rejected(self):
        self.assertIn("OBJECT_COUNT_OUTSIDE_10_TO_65", validate({"design_intent": "a" * 25, "meshes": []}))

    def test_reused_roles_do_not_equal_real_geometry(self):
        plan = structural_test_only()
        plan["meshes"][7]["vertices"] = copy.deepcopy(plan["meshes"][2]["vertices"])
        failures = validate(plan)
        self.assertIn("MESH_7_DUPLICATED_VERTEX_GEOMETRY_OF_2", failures)


if __name__ == "__main__":
    unittest.main()
