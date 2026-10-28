"""B6 source-narrow independent actual OBJ regression. Never a formal safety test."""
import unittest, sys, copy, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit import mesh_from_obj,report,blocked_door_negative,deleted_shared_floor_negative

class B6Geometry(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.base=mesh_from_obj()
 def test_real_obj_has_true_door_evidence(self):
  r=report(self.base);self.assertTrue(r['limited_triangle_gate'],r)
  self.assertEqual(len(r['door_rays']),8)
  for k,v in r['door_rays'].items():self.assertTrue(all(v.values()),(k,v))
 def test_both_upper_stair_approaches_not_only_a_route_label(self):
  a=report(self.base)['stair_terminal_rays'];self.assertEqual(len(a),6)
  self.assertEqual(a['-48:final'],8.0);self.assertEqual(a['48:landing'],8.0)
  self.assertAlmostEqual(a['-48:penultimate'],7.833333,places=5)
 def test_actual_shared_upper_plane_not_two_separate_roofs(self):
  a=report(self.base)['shared_upper_floor_rays'];self.assertEqual(len(a),4)
  self.assertTrue(all(z==8.0 for z in a.values()))
 def test_false_door_rejected(self):
  m=blocked_door_negative(self.base)
  r=report(m)
  self.assertFalse(r['door_rays']['-16:L0']['clear_center']);self.assertFalse(r['limited_triangle_gate'])
 def test_missing_shared_floor_rejected(self):
  m=deleted_shared_floor_negative(self.base)
  r=report(m)
  self.assertNotEqual(r['shared_upper_floor_rays']['-16:upper'],8.0)
  self.assertFalse(r['limited_triangle_gate'])
 def test_not_formal_safety_or_art_certification(self):
  r=report(self.base)
  self.assertEqual(r['full_human_sweep'] if 'full_human_sweep' in r else r['human_331_foot_993'],'NOT_RUN')
  self.assertEqual(r['occupied_rooms_certified'],'NOT_TESTED')
  self.assertEqual(r['structural_load'],'NOT_TESTED')
  self.assertEqual(r['minecraft_construction'],'FORBIDDEN')
  self.assertEqual(r['formal_s1_g1_g2_g3'],'NOT_RUN')
if __name__=='__main__':unittest.main()
