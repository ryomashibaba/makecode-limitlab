#!/usr/bin/env python3
"""Independent triangle-mesh G0 audit for A82. NOT a swept-agent or building certification."""
import importlib.util,json,math
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('a82',P/'a82_shared_section.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
M,topo=a.build()

def ray_t(origin,direction,p0,p1,p2):
 # Moller-Trumbore; use bounded positive forward ray distance < 1000m.
 o=np.asarray(origin,float);d=np.asarray(direction,float);v0=np.asarray(p0,float);v1=np.asarray(p1,float);v2=np.asarray(p2,float)
 e1=v1-v0;e2=v2-v0;h=np.cross(d,e2);den=float(np.dot(e1,h))
 if abs(den)<1e-9:return None
 inv=1/den;s=o-v0;u=inv*np.dot(s,h)
 if u<-1e-8 or u>1+1e-8:return None
 q=np.cross(s,e1);v=inv*np.dot(d,q)
 if v<-1e-8 or u+v>1+1e-8:return None
 t=inv*np.dot(e2,q)
 return float(t) if 1e-7<t<1000 else None

def hits(parts,origin,direction):
 result=[]
 for label,v,faces,mat in parts:
  for f in faces:
   t=ray_t(origin,direction,*v[f])
   if t is not None:result.append((t,label))
 return sorted(result)

def only(parts,prefix):return [v for v in parts if v[0].startswith(prefix)]
def require(ok,msg):
 if not ok:raise AssertionError(msg)

portal_checks=[]
def portals(parts):
 checks=[]
 for name,p in a.PORTALS.items():
  wall=only(parts,name+'_PUBLIC_OPENING')
  assert len(wall)==3
  z=0 if p['level']==0 else 24
  cx=p['door'];start=(cx,4,z+1.7)
  check1=not hits(wall,start,(0,1,0))
  check2=bool(hits(wall,(cx-12,4,z+1.7),(0,1,0)))
  check3=bool(hits(wall,(cx+12,4,z+1.7),(0,1,0)))
  check4=bool(hits(wall,(cx,4,z+6.4),(0,1,0)))
  checks.append({'room':name,'actual_center_open':check1,'left_wall':check2,'right_wall':check3,'real_lintel':check4})
  require(all((check1,check2,check3,check4)),'PORTAL_TRIANGLE_RAY_FAILED_'+name)
 for label,z in [('LOW',0),('UP',24)]:
  wall=only(parts,'SHARED_PARTITION_'+label)
  require(len(wall)==3,'MISSING_SHARED_PARTITION_'+label)
  check1=not hits(wall,(-28,73,z+1.7),(1,0,0))
  check2=bool(hits(wall,(-28,57,z+1.7),(1,0,0)))
  check3=bool(hits(wall,(-28,73,z+6.4),(1,0,0)))
  checks.append({'room':'SHARED_'+label,'actual_center_open':check1,'solid_next_to_opening':check2,'real_lintel':check3})
  require(all((check1,check2,check3)),'SHARED_PARTITION_RAY_FAILED_'+label)
 return checks

def floors(parts):
  # One and only one slab: lower ceiling / upper floor, shared physical vertices.
  slab=only(parts,'SHARED_UPPER_LOWER_SLAB');require(len(slab)==1,'NO_SINGLE_SHARED_SLAB')
  q=hits(slab,(0,68,48),(0,0,-1))
  require(q and abs(q[0][0]-24)<1e-5,'UPPER_SHARED_SLAB_RAY_BAD')
  f=only(parts,'SHARED_BASE_ROOM_FLOOR');require(len(f)==1,'LOWER_FLOOR_MISSING')
  q=hits(f,(-90,68,17),(0,0,-1));require(q and abs(q[0][0]-17)<1e-5,'LOWER_FLOOR_RAY_BAD')
  r=only(parts,'MONO_SHARED_TOP_ROOF');require(len(r)==1,'MISSING_SHARED_ROOF')
  for x,y in ((-150,30),(-10,75),(120,115)):
   q=hits(r,(x,y,20),(0,0,1))
   require(q and q[0][0]>40,'REAL_ROOF_TRIANGLE_MISSING')
  return True

def ramp(parts):
  surf=only(parts,'RAMP_ACTUAL_FLOOR');require(len(surf)==1,'NO_TRUE_RAMP')
  count=0;max_err=0
  for t in np.linspace(.025,.975,49):
   x=-205+410*float(t);expected=24*float(t)
   for y in (-40.,-29.,-18.):
    q=hits(surf,(x,y,expected+7),(0,0,-1))
    require(q,'RAMP_TRIANGLE_HOLE')
    err=abs((expected+7)-q[0][0]-expected)
    max_err=max(max_err,err)
    require(err<1e-4,'RAMP_TRIANGLE_WRONG_HEIGHT')
    count+=1
  lower=only(parts,'LOWER_ROUTE_JUNCTION');upper=only(parts,'UPPER_ROUTE_JUNCTION')
  require(lower and upper,'MISSING_ROUTE_JUNCTION')
  for prefix,level in [('LOWER',0),('UPPER',24)]:
   parts2=only(parts,prefix+'_PUBLIC_GALLERY')
   require(parts2,'MISSING_PUBLIC_GALLERY_'+prefix)
   for xx in (-120,0,120):
    q=hits(parts2,(xx,0,level+5),(0,0,-1))
    require(q and abs((level+5)-q[0][0]-level)<1e-5,'GALLERY_FLOOR_MISSING_'+prefix)
  return {'ramp_triangles_samples':count,'sample_position_wrong_height':0,'max_height_error_m':max_err}

def cap_alignment(parts):
  pieces=[(n,verts) for n,verts,fs,mat in parts if n.startswith(('END_UP_','FAR_UP_','READING_PUBLIC_OPENING','RESIDENCE_PUBLIC_OPENING','SHARED_PARTITION_UP'))]
  verified=0
  for name,points in pieces:
   for x,y,z in points:
    if z>50:
     # All high upper-wall boundary vertices MUST lie on roof edge equations.
     require(abs(float(z)-a.roof_height(x,y))<1e-6,'ROOF_FACADE_REAL_VERTEX_GAP_'+name)
     verified+=1
  require(verified>=28,'INSUFFICIENT_COHERENT_ROOF_EDGES')
  return verified

pchecks=portals(M.parts)
slab_valid=floors(M.parts)
rcheck=ramp(M.parts)
ncaps=cap_alignment(M.parts)

neg={}
def should_reject(label,parts,which):
 try:
  which(parts)
 except AssertionError:neg[label]=True
 else:neg[label]=False

should_reject('triangles_block_actual_market_door',M.parts+[("MARKET_PUBLIC_OPENING_BLOCK",np.array([(-104,20,0),(-96,20,0),(-96,20,5),(-104,20,5)],float),np.array([[0,1,2],[0,2,3]]),'wall')],portals)
should_reject('remove_physically_shared_slab',[p for p in M.parts if p[0]!='SHARED_UPPER_LOWER_SLAB'],floors)
should_reject('remove_real_ramp_mesh',[p for p in M.parts if p[0]!='RAMP_ACTUAL_FLOOR'],ramp)
should_reject('remove_partition_door_lintel',[p for p in M.parts if p[0]!='SHARED_PARTITION_UP_LINTEL'],portals)
should_reject('remove_roof_real_mesh',[p for p in M.parts if p[0]!='MONO_SHARED_TOP_ROOF'],floors)
changed=[]
for label,verts,faces,mat in M.parts:
 if label=='READING_PUBLIC_OPENING_LEFT':
  v=verts.copy();v[2,2]-=8;changed.append((label,v,faces,mat))
 else:changed.append((label,verts,faces,mat))
should_reject('mutate_roof_facade_joint_real_vertex',changed,cap_alignment)
require(all(neg.values()),'NEGATIVE_CONTROL_NOT_CAUGHT')

report={
 'stage':'A82_G0_INDEPENDENT_TRIANGLE_CHECK_NOT_S1_G2',
 'shared_mid_slab_mesh_once':slab_valid,
 'rays_into_real_wall_mesh':pchecks,
 'portal_count_checked':4,'shared_partition_portal_levels':2,
 'upper_roof_to_facade_matching_vertices':ncaps,
 **rcheck,
 'broken_geometry_caught':neg,
 'full_human_swept_volume':'NOT_TESTED','bridge_junction_continuous_collision':'NOT_TESTED',
 'real_structural_support_or_load':'NOT_TESTED','whole_shell_watertight':'NOT_TESTED',
 'art':'NOT_APPROVED','formal':a.GATES,'construction':'FORBIDDEN',
}
out=P/'a82-output';out.mkdir(exist_ok=True)
(out/'a82_independent_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
