"""Actual-mesh destructive negative controls, not a formal construction/safety QA."""
import unittest
from generate import build
from audit import audit
class TestTrueB9(unittest.TestCase):
 def test_real_complete_mesh_has_two_level_crossing(self):
  mesh,_=build()
  r=audit(mesh)
  self.assertTrue(r['limited_source_true_triangle_gate'],r)
  self.assertEqual(len(r['portal_witnesses']),4)
  self.assertEqual(len(r['ground_and_upper_slab_witnesses']),6)
  self.assertEqual(r['room_enclosure'],'NOT_TESTED')
  self.assertEqual(r['continuous_body_sweep'],'NOT_TESTED')
 def test_real_wall_blockage_rejected(self):
  mesh,_=build(door_block=True)
  r=audit(mesh)
  self.assertFalse(r['limited_source_true_triangle_gate'])
  self.assertFalse(next(p for p in r['portal_witnesses'] if p['district']=='W' and p['level']=='ground')['clear_three_lanes'])
 def test_shared_upper_floor_removed_rejected(self):
  mesh,_=build(upper=False)
  r=audit(mesh)
  self.assertFalse(r['limited_source_true_triangle_gate'])
  self.assertFalse(next(p for p in r['ground_and_upper_slab_witnesses'] if p['z']==10)['triangle_at_level'])
 def test_shared_ground_removed_rejected(self):
  mesh,_=build(ground=False)
  r=audit(mesh)
  self.assertFalse(r['limited_source_true_triangle_gate'])
  self.assertFalse(next(p for p in r['ground_and_upper_slab_witnesses'] if p['z']==0)['triangle_at_level'])
 def test_never_art_or_construction_approval(self):
  a=audit(build()[0])
  self.assertEqual(a['art'],'HOLD_PENDING_TRUE_IMAGE_REVIEW')
  self.assertEqual(a['formal_s1_g1_g2_g3'],'NOT_RUN')
  self.assertEqual(a['minecraft_construction'],'FORBIDDEN')
if __name__=='__main__':unittest.main()
