"""Inspect immutable output from REAL imported PLY, not just authored intentions.
No tests certify a safe walker, usable room, load bearing or city artwork.
"""
import hashlib,json,unittest
from pathlib import Path
import numpy as np
import trimesh
from coupled_section import GROUPS,XS
ROOT=Path(__file__).parent/'output'

def read(k):return json.loads((ROOT/k/'manifest.json').read_text())
def mesh(k,part):return trimesh.load(ROOT/k/(part+'.ply'),force='mesh',process=False)

class TestSource3DDependency(unittest.TestCase):
 def test_authentic_mesh_by_reimport(self):
  for k in ('baseline','public_change','housing_change','cut'):
   a=read(k)
   for group in GROUPS:
    f=ROOT/k/(group+'.ply');m=mesh(k,group)
    self.assertGreater(len(m.faces),0)
    self.assertEqual(len(m.faces),a['parts'][group]['faces'])
    self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),a['parts'][group]['file_sha256'])
 def test_public_space_requirement_changes_real_public_occupied_and_outer_geometry(self):
  a,b=read('baseline'),read('public_change')
  for group in ('public','occupied','envelope'):
   self.assertNotEqual(a['parts'][group]['triangle_digest'],b['parts'][group]['triangle_digest'])
   ma,mb=mesh('baseline',group),mesh('public_change',group)
   self.assertGreater(np.max(np.abs(ma.vertices-mb.vertices)),.3)
  self.assertGreater(b['profile']['outer_halfspan_max_m'],a['profile']['outer_halfspan_max_m']+2)
  self.assertGreater(b['profile']['roof_max_height_m'],a['profile']['roof_max_height_m'])
  self.assertGreater(b['profile']['min_clear_void_width_m'],a['profile']['min_clear_void_width_m'])
 def test_occupied_room_need_changes_real_atrium_and_silhouette_not_just_use_label(self):
  a,b=read('baseline'),read('housing_change')
  for group in ('public','occupied','envelope'):
   self.assertNotEqual(a['parts'][group]['file_sha256'],b['parts'][group]['file_sha256'])
  self.assertLess(b['profile']['min_clear_void_width_m'],a['profile']['min_clear_void_width_m'])
  self.assertGreater(b['profile']['outer_halfspan_max_m'],a['profile']['outer_halfspan_max_m'])
  self.assertGreater(b['profile']['roof_max_height_m'],a['profile']['roof_max_height_m'])
 def test_real_mesh_narrow_cut_fails_source_only_gate(self):
  a,b=read('baseline'),read('cut')
  self.assertEqual(a['source_void_width_gate'],'PASS_SOURCE_ONLY')
  self.assertEqual(b['source_void_width_gate'],'REJECT_NARROW_SOURCE_VOID')
  self.assertEqual(b['profile']['min_clear_void_width_m'],.5)
  m=mesh('cut','public')
  x=XS[np.argmin(abs(XS-35))]
  verts=m.vertices[np.isclose(m.vertices[:,0],x,atol=.01)]
  self.assertGreater(len(verts),0)
  self.assertLess(float(np.ptp(verts[:,1])),1.)
  self.assertNotEqual(a['parts']['public']['file_sha256'],b['parts']['public']['file_sha256'])
 def test_source_study_always_locks_formal_safety_construction_and_adoption(self):
  for k in ('baseline','public_change','housing_change','cut'):
   a=read(k)
   self.assertEqual(a['official_art'],'HOLD')
   self.assertEqual(a['formal_adoptions'],0)
   self.assertEqual(a['real_enclosed_rooms'],'NOT_TESTED')
   self.assertEqual(a['actual_safe_walk'],'NOT_TESTED')
   self.assertEqual(a['human_331_foot_993'],'NOT_RUN')
   self.assertEqual(a['formal_s1_g1_g2_g3'],'NOT_RUN')
   self.assertEqual(a['structural_load'],'NOT_TESTED')
   self.assertEqual(a['minecraft_construction'],'FORBIDDEN')
 def test_renders_are_real_png_not_mechanical_art_pass(self):
  from PIL import Image,ImageStat
  for k in ('baseline','public_change'):
   for v in ('macro','public_eye'):
    with Image.open(ROOT/k/(v+'.png')) as im:
     self.assertEqual(im.format,'PNG')
     self.assertEqual(im.size,(1300,840))
     self.assertGreater(max(ImageStat.Stat(im.convert('RGB')).stddev),8.)
 def test_negative_control_tampered_manifest_false_unlock_rejected(self):
  a=read('baseline')
  def accepted(m):return m['minecraft_construction']=='FORBIDDEN' and m['formal_adoptions']==0 and m['official_art']=='HOLD'
  self.assertTrue(accepted(a))
  a['minecraft_construction']='ALLOWED'
  self.assertFalse(accepted(a))
  a['minecraft_construction']='FORBIDDEN';a['formal_adoptions']=1
  self.assertFalse(accepted(a))
if __name__=='__main__':unittest.main()
