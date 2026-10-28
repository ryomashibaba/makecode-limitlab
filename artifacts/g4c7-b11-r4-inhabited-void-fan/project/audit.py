"""Independent re-import and ray validation. This is NOT human accessibility or room certification."""
from pathlib import Path
import json,hashlib,math
import numpy as np
import trimesh
OUT=Path(__file__).resolve().parent/'output'

def intersect(tris,origin,vector,length=100):
  origin=np.asarray(origin,float);d=np.asarray(vector,float);d=d/np.linalg.norm(d)
  a,b,c=tris[:,0,:],tris[:,1,:],tris[:,2,:]
  e1=b-a;e2=c-a;h=np.cross(np.broadcast_to(d,e2.shape),e2)
  det=np.einsum('ij,ij->i',e1,h)
  with np.errstate(invalid='ignore',divide='ignore'):
    inv=np.where(np.abs(det)>1e-9,1/det,0)
    s=origin-a;u=inv*np.einsum('ij,ij->i',s,h)
    q=np.cross(s,e1);v=inv*(q@d)
    t=inv*np.einsum('ij,ij->i',e2,q)
  mask=(np.abs(det)>1e-9)&(u>=-1e-6)&(v>=-1e-6)&(u+v<=1+1e-6)&(t>1e-5)&(t<=length)
  return float(t[mask].min()) if np.any(mask) else None

def mesh():
  m=json.loads((OUT/'manifest.json').read_text())
  meshes=[]
  for cat,p in m['parts'].items():
    f=OUT/(cat+'.ply')
    assert hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'],cat
    mm=trimesh.load(f,force='mesh',process=False)
    assert len(mm.faces)==p['faces'],cat
    meshes.append(np.asarray(mm.triangles,float))
  return m,np.concatenate(meshes)

def audit():
  data,tris=mesh();res=[]
  for room in data['rooms']:
    dirs={'inward':-np.array(room['radial']), 'outward':np.array(room['radial']),
      'left':-np.array(room['tangent']), 'right':np.array(room['tangent']),
      'down':np.array([0,0,1]), 'up':np.array([0,0,1])}
    dirs['down']=-dirs['down']
    hits={k:intersect(tris,room['point'],d,45) for k,d in dirs.items()}
    doorvec=np.array(room['door_b'])-np.array(room['door_a'])
    clear=intersect(tris,room['door_a'],doorvec,float(np.linalg.norm(doorvec))) is None
    publicfloor=intersect(tris,room['door_b'],[0,0,-1],4) is not None
    res.append({'id':room['id'],'six_direction_room_boundary_witness':all(v is not None for v in hits.values()),
      'real_door_local_ray_clear':bool(clear),'adjacent_public_floor_triangle':bool(publicfloor),
      'directions':{k:round(v,3) if v is not None else None for k,v in hits.items()}})
  out={'stage':'B11-R4','triangles_independently_reimported':len(tris),'room_sample_count':len(res),
   'samples_with_6_direction_witness':sum(i['six_direction_room_boundary_witness'] for i in res),
   'door_centre_rays_clear':sum(i['real_door_local_ray_clear'] for i in res),
   'adjacent_public_floor_witnesses':sum(i['adjacent_public_floor_triangle'] for i in res),
   'witnesses':res,'true_rooms':'NOT_CERTIFIED',
   'continuous_human_walk_and_stairs':'NOT_TESTED','structural_load':'NOT_TESTED',
   'formal_S1_G1_G2_G3':'NOT_RUN','minecraft_construction':'FORBIDDEN',
   'formal_art_adoptions':0,'art_G0':'REJECT__REPEATED_STACKED_RINGS_AND_DARK_VOID'}
  (OUT/'independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
  return out
if __name__=='__main__':
  x=audit();print({k:v for k,v in x.items() if k!='witnesses'})
