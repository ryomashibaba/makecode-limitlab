import unittest,os,copy,json,tempfile,shutil
from pathlib import Path
import numpy as np,trimesh
from room_witness import audit,wall_hit,check
BASE=Path(os.environ.get('B11_R2_BASELINE',
 Path(__file__).resolve().parents[1]/'g4c7-b11-r2-causal-section'/'project'/'output'/'baseline'))
def box_without_face(missing=None):
 m=trimesh.creation.box(extents=(12,14,8));m.apply_translation((0,0,4))
 t=np.asarray(m.triangles)
 if missing is not None:
  n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.linalg.norm(n,axis=1)[:,None]
  t=t[np.abs(n@np.asarray(missing))<.9]
 return t
P=[{'site':'control','point':[0,0,3]}]
class R3(unittest.TestCase):
 def test_closed_positive_control(self):self.assertTrue(check(box_without_face(),P)[0]['six_direction_local_witness'])
 def test_missing_endcap_negative(self):
  x=check(box_without_face([1,0,0]),P)[0]
  self.assertFalse(x['six_direction_local_witness']);self.assertFalse(x['rays']['east']['hit'])
 def test_missing_ceiling_negative(self):self.assertFalse(check(box_without_face([0,0,1]),P)[0]['rays']['up']['hit'])
 def test_forged_room_label_negative(self):
  self.assertFalse(check(box_without_face([1,0,0]),[{'site':'APPROVED_ROOM','point':[0,0,3]}])[0]['six_direction_local_witness'])
 def test_real_original_ply_eight_samples_not_bounded(self):
  a=audit(BASE)
  self.assertEqual(a['faces'],3072);self.assertEqual(a['probed_sites'],8)
  self.assertEqual(a['six_direction_local_witnesses'],0)
  self.assertTrue(all(not p['rays']['east']['hit'] and not p['rays']['west']['hit'] for p in a['probes']))
  self.assertEqual(a['real_room_certification'],'NOT_CERTIFIED')
  self.assertEqual(a['s1_g1_g2_g3'],'NOT_RUN');self.assertEqual(a['minecraft'],'FORBIDDEN')
 def test_source_sha_mismatch_negative(self):
  with tempfile.TemporaryDirectory() as tmp:
   t=Path(tmp)
   for f in BASE.glob('*.ply'):shutil.copy2(f,t/f.name)
   m=json.loads((BASE/'manifest.json').read_text());m['parts']['public']['file_sha256']='0'*64
   (t/'manifest.json').write_text(json.dumps(m))
   with self.assertRaisesRegex(ValueError,'ORIGINAL_PLY_SHA_MISMATCH'):audit(t)
 def test_grazing_wall_not_endcap(self):
  a=np.array([[[5,-4,-2],[5,-4,2],[6,4,2]]],float)
  self.assertIsNone(wall_hit(a,[0,0,0],[0,1,0],20))
if __name__=='__main__':unittest.main()
