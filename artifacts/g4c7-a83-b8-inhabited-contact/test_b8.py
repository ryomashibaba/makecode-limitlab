import unittest,copy
from b8_source import SEEDS,audit
class TestSourceContact(unittest.TestCase):
 def setUp(self):self.s=copy.deepcopy(SEEDS)
 def test_source_positive_overlap_is_not_real_pass(self):
  r=audit(self.s)
  self.assertTrue(r["source_geometry_constraints_satisfied"],r["violations"])
  self.assertEqual(len(r["contacts"]),2)
  self.assertGreater(min(x["SOURCE_overlap_m3"] for x in r["contacts"]),10000)
  self.assertEqual(r["actual_shared_walking_air"],"NOT_TESTED")
 def test_move_east_breaks_actual_source_contact(self):
  self.s[2]["polygon"]=[[x+110,y] for x,y in self.s[2]["polygon"]]
  self.assertIn("SOURCE_CONTACT_DISCONNECTED:C-E",audit(self.s)["violations"])
 def test_move_centre_up_breaks_vertical_contact(self):
  self.s[1]["bottom"]=23;self.s[1]["top"]=48
  self.assertIn("SOURCE_CONTACT_DISCONNECTED:W-C",audit(self.s)["violations"])
 def test_single_use_rejected(self):
  self.s[1]["uses"]=["market"]
  self.assertIn("NOT_MULTIUSE:C",audit(self.s)["violations"])
 def test_art_and_construction_never_unlocked(self):
  r=audit(self.s)
  self.assertEqual(r["pre3d_art"],"REJECT__THREE_OVERLAPPING_POLYGON_MASSES")
  self.assertEqual(r["real_3d"],"NOT_RUN")
  self.assertEqual(r["s1_g1_g2_g3"],"NOT_RUN")
  self.assertEqual(r["art_adoptions"],0)
  self.assertEqual(r["minecraft_construction"],"FORBIDDEN")
if __name__=="__main__":unittest.main()
