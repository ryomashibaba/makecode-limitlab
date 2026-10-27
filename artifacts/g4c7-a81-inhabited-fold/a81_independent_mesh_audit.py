#!/usr/bin/env python3
"""A81 independent G0 triangle-surface ray audit; NOT G2/Navmesh/structural acceptance."""
import importlib.util,json
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g4c7_a81_native',D/'a81_inhabited_fold.py')
src=importlib.util.module_from_spec(spec);spec.loader.exec_module(src)

def ray_tri(origin,vec,tri):
 p0,p1,p2=np.asarray(tri,float)
 e1=p1-p0;e2=p2-p0;h=np.cross(vec,e2);den=float(np.dot(e1,h))
 if abs(den)<1e-10:return None
 f=1/den;s=origin-p0;u=f*float(np.dot(s,h))
 if u<-1e-7 or u>1.0000001:return None
 q=np.cross(s,e1);v=f*float(np.dot(vec,q))
 if v<-1e-7 or u+v>1.0000001:return None
 t=f*float(np.dot(e2,q))
 return t if t>1e-7 else None

def first_hit(parts,origin,vec,max_t=100):
 origin=np.array(origin,float);vec=np.array(vec,float)
 hits=[]
 for name,p,faces,mat in parts:
  for f in faces:
   t=ray_tri(origin,vec,p[f])
   if t is not None and t<max_t:
    hits.append((t,name))
 return sorted(hits)[:1]

def actual_check(mesh):
 report={'rooms':{},'stair_treads_detected':0,'centerline_continuous_at_world_mesh':True}
 parts={n:(n,p,faces,mat) for n,p,faces,mat in mesh.parts}
 for label,a,b,side,depth,height in src.PROGRAM:
  A=src.point(a,src.NODES);B=src.point(b,src.NODES)
  length=np.linalg.norm((B-A)[:2]);mid=length/2;sgn=float(side)
  vn=sgn*src.ROUTE_WIDTH/2;vo=sgn*(src.ROUTE_WIDTH/2+depth)
  def P(u,v,z):return src.param_plane(A,B,(u,v,z))
  sidewalls=[v for n,v in parts.items() if n.startswith(label+'_DOOR_')]
  assert len(sidewalls)==3
  along=np.array([0.,0.,0.]);along[:2]=src.unit2(A,B)[1]*sgn
  def wallhit(u,z):
   origin=P(u,vn-sgn*2,z)
   hit=first_hit(sidewalls,origin,along,5)
   return hit[0][1] if hit else None
  assert wallhit(mid,1.7) is None, f'{label}: door physically obstructed'
  assert wallhit(mid-7,1.7)==f'{label}_DOOR_LEFT',f'{label}: left wall missing'
  assert wallhit(mid+7,1.7)==f'{label}_DOOR_RIGHT',f'{label}: right wall missing'
  assert wallhit(mid,5.2)==f'{label}_DOOR_LINTEL',f'{label}: lintel missing'
  floor_part=[parts[f'{label}_ACTUAL_ROOM_FLOOR']]
  fc=P(mid,sgn*(src.ROUTE_WIDTH/2+depth/2),0)
  downhit=first_hit(floor_part,fc+np.array([0,0,2]),np.array([0.,0.,-1]),4)
  assert downhit and abs(downhit[0][0]-2)<1e-6,f'{label}: missing floor'
  roof_part=[parts[f'{label}_COVERED_ROOF']]
  uphit=first_hit(roof_part,fc+np.array([0,0,2]),np.array([0.,0.,1]),height+6)
  assert uphit and uphit[0][0]>4,f'{label}: missing roof'
  outer=[parts[f'{label}_OUTER_FACADE']]
  outerhit=first_hit(outer,P(mid,sgn*(src.ROUTE_WIDTH/2+depth/2),1.7),along,depth+5)
  assert outerhit,f'{label}: no exterior facade'
  report['rooms'][label]={'door_mid_at_body_z':'RAY_UNBLOCKED','door_left_wall':'RAY_BLOCKED',
     'door_right_wall':'RAY_BLOCKED','head_height_lintel':'RAY_BLOCKED',
     'real_floor':'RAY_HIT','real_roof':'RAY_HIT','far_facade':'RAY_HIT',
     'certified_walkable':'NOT_TESTED'}
 # world-coordinate centerline surface intersections for every segment (not just self-reported vertices)
 street=[x for x in mesh.parts if x[0].startswith('STREET_')]
 for a,b in zip(src.PATH,src.PATH[1:]):
  A=src.point(a,src.NODES);B=src.point(b,src.NODES)
  for t in (.02,.17,.5,.83,.98):
   C=(1-t)*A+t*B
   hit=first_hit(street,C+np.array([0,0,3.]),np.array([0.,0.,-1]),6)
   assert hit and abs(hit[0][0]-3.)<1e-5,(a,b,t,hit)
  # exact joining vertices at segment boundaries, subject to this limited check
 report['centerline_ray_hits']=len(src.PATH[:-1])*5
 stairs=[x for x in mesh.parts if x[0].startswith('STAIR_')]
 assert len(stairs)==140
 for i,(n,p,fs,mat) in enumerate(stairs):
  a,b=n.split('_')[1][:2]
  # world horizontal tread test at representative triangles' midpoint
  assert np.max(p[:,2])-np.min(p[:,2])<1e-7,n
  hit=first_hit([(n,p,fs,mat)],np.mean(p,axis=0)+np.array([0,0,1]),np.array([0.,0.,-1]),2)
  assert hit and abs(hit[0][0]-1)<1e-5,n
 report['stair_treads_detected']=len(stairs)
 return report

def caught_bad_geometry(base):
 outcomes={}
 # Actually corrupt real mesh, don't merely toggle a metadata flag.
 m=src.Mesh();m.parts=list(base.parts)
 lab,a,b,side,depth,height=src.PROGRAM[0];A=src.point(a,src.NODES);B=src.point(b,src.NODES)
 length=np.linalg.norm((B-A)[:2]);v=side*src.ROUTE_WIDTH/2
 def P(u,vv,z):return src.param_plane(A,B,(u,vv,z))
 mid=length/2
 m.quad(f'{lab}_DOOR_BLOCKER',[P(mid-3,v,0),P(mid+3,v,0),P(mid+3,v,4.6),P(mid-3,v,4.6)],'wall')
 # We must deliberately include blockers in the portal obstruction ray group below.
 wallparts=[x for x in m.parts if x[0].startswith(lab+'_DOOR_')]
 normal=np.r_[src.unit2(A,B)[1]*side,0]
 hit=first_hit(wallparts,P(mid,v-side*2,1.7),normal,5)
 outcomes['inserted_door_blocker_detected']=bool(hit and hit[0][1]==lab+'_DOOR_BLOCKER')
 for label,key in [('roof_removed',f'{lab}_COVERED_ROOF'),('floor_removed',f'{lab}_ACTUAL_ROOM_FLOOR'),('stair_step_removed','STAIR_AB_00')]:
  c=src.Mesh();c.parts=[x for x in base.parts if x[0]!=key]
  try:actual_check(c)
  except (AssertionError,KeyError):outcomes[label]=True
  else:outcomes[label]=False
 assert all(outcomes.values()),outcomes
 return outcomes

if __name__=='__main__':
 m,topo,ch=src.build()
 report=actual_check(m);report['negative_real_mesh_mutations']=caught_bad_geometry(m)
 report['note']='NARROW_EXPLICIT_RAY_TRIANGLE_PROOF_ONLY_NOT_G2_OR_HABITABILITY_CERTIFICATION'
 report['formal']={k:'NOT_RUN' for k in ('S1','G1','G2','G3')}
 report['art']='NOT_APPROVED'
 out=D/'a81-output';out.mkdir(exist_ok=True)
 (out/'a81_independent_mesh_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
