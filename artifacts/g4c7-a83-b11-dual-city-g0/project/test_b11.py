import unittest,hashlib,json
from pathlib import Path
from PIL import Image,ImageStat
import trimesh
P=Path(__file__).resolve().parent
class B11Native(unittest.TestCase):
 def test_both_real_objs_exact_mesh(self):
  for k,nf,nv in [('A',3480,2228),('B',5848,3624)]:
   p=P/k;m=json.loads((p/'manifest.json').read_text());f=p/'city_coarse.obj'
   self.assertEqual(m['obj_sha256'],hashlib.sha256(f.read_bytes()).hexdigest())
   mesh=trimesh.load(f,force='mesh',process=False)
   self.assertEqual((len(mesh.faces),len(mesh.vertices)),(nf,nv))
 def test_two_distinct_coarse_hypotheses(self):
  a=json.loads((P/'A'/'manifest.json').read_text())
  b=json.loads((P/'B'/'manifest.json').read_text())
  self.assertGreater(b['bounds_m'][1][2],2*a['bounds_m'][1][2])
  self.assertNotEqual(len(a['districts']),len(b['districts']))
 def test_eight_true_vtk_renders(self):
  for k in ('A','B'):
   for name in ('macro','district','public_eye','upper_public'):
    with self.subTest(k=k,name=name):
     with Image.open(P/k/(name+'.png')) as im:
      self.assertEqual(im.format,'PNG')
      self.assertEqual(im.size,(1350,870))
      self.assertGreater(max(ImageStat.Stat(im.convert('RGB')).stddev),8)
 def test_no_room_or_path_certified(self):
  for k in ('A','B'):
   m=json.loads((P/k/'manifest.json').read_text())
   self.assertEqual(m['real_enclosed_rooms'],'NOT_TESTED')
   self.assertTrue(m['modelled_route_not_human_walkable'])
   self.assertEqual(m['safe_entry_and_stairs'],'NOT_TESTED')
   self.assertEqual(m['load_support'],'NOT_TESTED')
   self.assertEqual(len(m['candidate_public_routes']),2)
 def test_formal_art_and_construction_locked(self):
  for k in ('A','B'):
   m=json.loads((P/k/'manifest.json').read_text())
   self.assertEqual(m['formal_human_331_foot_993'],'NOT_RUN')
   self.assertEqual(m['formal_s1_g1_g2_g3'],'NOT_RUN')
   self.assertEqual(m['minecraft_construction'],'FORBIDDEN')
   self.assertEqual(m['art_approval'],'NOT_GRANTED')
 def test_negative_control_false_unlock_refused(self):
  a=json.loads((P/'A'/'manifest.json').read_text())
  def ok(x):return x['art_approval']=='NOT_GRANTED' and x['minecraft_construction']=='FORBIDDEN'
  self.assertTrue(ok(a));a['art_approval']='APPROVED';self.assertFalse(ok(a))
  a['art_approval']='NOT_GRANTED';a['minecraft_construction']='ALLOWED';self.assertFalse(ok(a))
if __name__=='__main__':unittest.main()
