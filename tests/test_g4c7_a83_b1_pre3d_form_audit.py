import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from g4c7_a83_b1_pre3d_form_audit import audit,load,b0_components

class TestB1(unittest.TestCase):
    def setUp(self):
        self.d=copy.deepcopy(load())
    def reasons(self):
        return audit(self.d)["errors"]
    def test_falsified_b0_network_has_three_components(self):
        self.assertEqual({tuple(x) for x in b0_components()},{
            ("W0","W1"),("C0","C1"),("E0","E1")})
    def test_source_only_cannot_be_misreported_as_art_or_construction(self):
        q=audit(self.d)
        self.assertTrue(q["source_review_consistent"],q["errors"])
        self.assertEqual(q["true_3d_render"],"NOT_RUN")
        self.assertEqual(q["real_enclosed_rooms"],"NOT_TESTED")
        self.assertEqual(q["minecraft_construction"],"FORBIDDEN")
    def test_all_three_massing_studies_are_rejected(self):
        self.assertEqual([x["decision"] for x in self.d["schemes"]],["PRE_3D_REJECT"]*3)
    def test_program_outside_envelope(self):
        self.d["programs"][0]["z"]=999
        self.assertTrue(any(x.startswith("PROGRAM_OUTSIDE") for x in self.reasons()))
    def test_support_root_not_grounded(self):
        self.d["roots"][0][1]=12
        self.assertIn("UNROOTED_SUPPORT_INTENTION",self.reasons())
    def test_support_must_touch_activity_witness(self):
        self.d["roots"][0][2]+=4
        self.assertIn("SUPPORT_INTENTION_NOT_REGISTERED_TO_PROGRAM",self.reasons())
    def test_abstract_cross_district_network_disconnection(self):
        self.d["links"]=[x for x in self.d["links"] if "C-fabrication" not in x or x[0]=="C-fabrication" and x[1]=="C-library"]
        self.assertIn("DISCONNECTED_ABSTRACT_CITY",self.reasons())
    def test_labeling_claim_falsely_as_adopted_rejected(self):
        self.d["schemes"][2]["decision"]="ART_PASS"
        self.assertIn("NO_REJECTED_FORM_REVIEW",self.reasons())
    def test_bad_distribution_of_programs(self):
        self.d["programs"][5]["district"]="W"
        self.assertIn("DISTRICT_PROGRAM_BALANCE",self.reasons())

if __name__=="__main__":
    unittest.main()
