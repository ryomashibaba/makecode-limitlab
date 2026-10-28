import unittest,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from independent_audit import analyze
class TestB5(unittest.TestCase):
 def test_real_saved_obj_does_not_become_room_or_safety_certification(self):
  a=analyze()
  self.assertEqual(a['triangles'],4368)
  self.assertEqual(a['vertices'],8736)
  self.assertFalse(a['preflight_eligible'])
  self.assertEqual(a['room_enclosure_verified'],'NOT_TESTED')
  self.assertEqual(a['formal_s1_g1_g2_g3'],'NOT_RUN')
  self.assertEqual(a['minecraft_construction'],'FORBIDDEN')
 def test_unwelded_gaps_cannot_disappear_from_report(self):
  a=analyze()
  self.assertFalse(a['watertight_after_weld'])
  self.assertGreater(a['edge_welded_components'],1)
 def test_negative_control_triangle_geometry_cannot_fake_certification(self):
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'single-triangle.obj'
   f.write_text('v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n')
   r=analyze(f)
   self.assertEqual(r['triangles'],1)
   self.assertFalse(r['preflight_eligible'])
   self.assertEqual(r['room_enclosure_verified'],'NOT_TESTED')
if __name__=='__main__':unittest.main()
