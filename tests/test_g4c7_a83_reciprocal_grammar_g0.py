"""A83-0 source-only falsification; no formal approvals."""
import sys
from pathlib import Path
import unittest
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import g4c7_a83_reciprocal_grammar_g0 as a

class A83G0ReciprocalTests(unittest.TestCase):
 def test_three_regions_and_unapproved_geometry(self):
  p=a.witness()
  self.assertEqual(len(p['stations']),12)
  self.assertEqual(p['districts'],['west','center','east'])
  self.assertEqual(len(p['vertices']),48)
  self.assertEqual(len(p['triangles']),36)
  self.assertGreater(p['span_m'][0],1800)
  self.assertEqual(p['real_rooms'],0)
  self.assertEqual(p['rendered_3d'],'NOT_RUN')
  self.assertEqual(p['full_3d_walkability'],'NOT_TESTED')
 def test_actual_vertices_change_both_directions(self):
  c=a.counterfactuals()
  self.assertTrue(all(c['checks'].values()))
  self.assertNotEqual(c['program_edit_outer_sha256'],c['baseline_outer_coordinate_sha256'])
  self.assertNotEqual(c['exterior_edit_inner_sha256'],c['baseline_inner_coordinate_sha256'])
 def test_one_common_control_not_frozen_shell(self):
  s=a.STATIONS[5]
  b=a.solve(s)
  p=a.solve(replace(s,requested_depth_m=s.requested_depth_m+10))
  e=a.solve(replace(s,authored_exterior_m=s.authored_exterior_m+10))
  self.assertGreater(p['offset_m'],b['offset_m'])
  self.assertGreater(e['depth_m'],b['depth_m'])
  self.assertNotEqual(p['outer'],b['outer'])
  self.assertNotEqual(e['inner'],b['inner'])
 def test_reject_invalid_design_and_false_gates(self):
  self.assertEqual(len(a.refuse_negative_controls()),9)
 def test_never_claim_formal_safety_or_art(self):
  p=a.witness()
  self.assertEqual(p['gate'],'A83_0_SOURCE_ONLY')
  self.assertEqual(p['art'],'NOT_APPROVED')
  self.assertEqual(p['load_safety'],'NOT_TESTED')
  self.assertEqual(a.PROTECTED['formal_body_samples'],331)
  self.assertEqual(a.PROTECTED['formal_foot_samples'],993)
  self.assertEqual(a.PROTECTED['foot_relative_m'],(0.15,3.25))

if __name__=='__main__':unittest.main()
