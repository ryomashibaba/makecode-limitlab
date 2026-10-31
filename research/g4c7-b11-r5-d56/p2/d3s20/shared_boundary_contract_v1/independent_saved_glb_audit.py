"""Independent persisted-GLB AABB inclusion, door negative control.
For this specific fixture every reloaded component MUST be an axis-aligned box.
This has NO claim to arbitrary mesh triangle certification or human swept safety.
"""
from pathlib import Path
import json,hashlib, numpy as np, trimesh
from spatial_contract import make_fixture, CELL, PORTAL_HEIGHT,PORTAL_WIDTH
from render_fixture import slab
R=Path(__file__).resolve().parent


def loaded_aabbs(path):
 s=trimesh.load(path,force='scene')
 assert len(s.geometry)>0
 for m in s.geometry.values():
  if len(m.faces)!=12 or len(m.vertices)!=8:
   raise AssertionError('AABB test fixture expects individually saved boxes ONLY')
  v=np.round(m.vertices,5)
  axes=[set(v[:,i]) for i in range(3)]
  if any(len(aa)!=2 for aa in axes):raise AssertionError('Saved mesh is not axis-aligned box')
 return np.array([m.bounds for m in s.geometry.values()]),len(s.geometry)

def portal_test_points(led):
 points=[];origin=[]
 for edge,tag in sorted(led.portals.items()):
  a,b=edge
  # exterior entrance is also sampled; points offset into the public cell
  axis=0 if a[0]!=b[0] else 1
  p=np.array([(a[i]+.5)*CELL for i in range(3)],float)
  p[axis]=max(a[axis],b[axis])*CELL
  for across in (-.25,0,.25):
   for side in (-.6,0,.6):
    for height in (.4,1.8,3.25):
     q=p.copy();q[axis]+=across;q[1-axis]+=side;q[2]=a[2]*CELL+height
     points.append(q);origin.append(str(edge))
 return np.array(points),origin

def points_inside(aabb,pts):
 # exact for saved-axis-aligned box meshes, strict interior excludes surface
 p=pts[:,None,:];b=aabb[None,:,:,:]
 return np.any(np.all((p>b[:,:,0,:]+1e-5)&(p<b[:,:,1,:]-1e-5),axis=2),axis=1)

if __name__=='__main__':
 led=make_fixture();path=R/'SHARED_BOUNDARY_TEST_FIXTURE.glb'
 aabb,count=loaded_aabbs(path);pts,orig=portal_test_points(led)
 hits=points_inside(aabb,pts)
 assert not hits.any(), {'blocked':[(orig[i],pts[i].tolist()) for i in np.where(hits)[0][:10]]}
 # Change saved GLB for *negative-control* only, never modify baseline model.
 sc=trimesh.load(path,force='scene')
 ca,cb=led.entrance
 axis=0 if ca[0]!=cb[0] else 1
 center=np.array([(ca[i]+.5)*CELL for i in range(3)],float)
 center[axis]=max(ca[axis],cb[axis])*CELL
 blocker=slab([center[0],center[1],1.8],[1.2,3.3,3.6] if axis==0 else [3.3,1.2,3.6],(225,35,40,255))
 sc.add_geometry(blocker,geom_name='NEGATIVE_CONSTRUCTION_BLOCKER')
 neg=R/'NEGATIVE_BLOCKED_ENTRANCE.glb';neg.write_bytes(sc.export(file_type='glb'))
 negbb,negcount=loaded_aabbs(neg);blocked=points_inside(negbb,pts)
 assert blocked.any(), 'INTENTIONAL_BLOCKER_NOT_FOUND'
 # Verify the blocker actually covers test points of the exterior gate.
 gate=str(tuple(sorted(led.entrance)))
 exterior=sum(blocked[i] for i,o in enumerate(orig) if o==gate)
 assert exterior>0,(gate,exterior)
 report={'base_glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'persisted_geometry_count':count,'baseline_door_samples':len(pts),'baseline_blocked':int(hits.sum()),
         'negative_glb_sha256':hashlib.sha256(neg.read_bytes()).hexdigest(),
         'negative_blocked_samples':int(blocked.sum()),'negative_external_gate_blocked':int(exterior),
         'scope':'AABB exact for this fixture boxes only; NOT triangulated swept-body QA; not MakeCode'}
 (R/'INDEPENDENT_SAVED_GLB_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,indent=2))