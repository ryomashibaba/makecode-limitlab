#!/usr/bin/env python3
"""Independent G0 falsification, NEVER a formal human swept-volume test."""
import importlib.util,json,math
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('a80',P/'a80_network_fabric.py')
a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
scene,_,_=a.sketch()
streets=[(n,pts,faces) for n,pts,faces,mat in scene.parts if n.endswith('public_surface')]
landings=[(n,pts,faces) for n,pts,faces,mat in scene.parts if n.startswith('JOINT_')]
def hit_z(xy):
 out=[]
 for n,verts,faces in streets+landings:
  for tri in faces:
   q=verts[tri];v=q[:,:2]
   mat=np.array([[v[0,0],v[1,0],v[2,0]],[v[0,1],v[1,1],v[2,1]],[1,1,1]],float)
   if abs(np.linalg.det(mat))<1e-8:continue
   l=np.linalg.solve(mat,[xy[0],xy[1],1.])
   if min(l)>=-1e-6:out.append((float(np.dot(l,q[:,2])),n))
 return out
checked=[];holes=[];errors=[]
for label,path in a.ROUTES.items():
 for i,(u,v) in enumerate(zip(path,path[1:])):
  A=np.array(a.NODES[u],float);B=np.array(a.NODES[v],float)
  tang=(B-A)[:2];tang/=np.linalg.norm(tang);normal=np.array([-tang[1],tang[0]])
  width=13 if label=='central' else 11
  for t in (.035,.10,.25,.50,.75,.9,.965):
   C=(1-t)*A+t*B
   for f in (-.45,0,.45):
    xy=C[:2]+normal*(width*f)
    zlist=hit_z(xy)
    if not zlist:holes.append((label,i,t,f))
    elif not any(abs(z-C[2])<.15 for z,n in zlist):errors.append((label,i,t,f,[(round(z,3),n) for z,n in zlist[:2]]))
    checked.append((label,i,t,f))
for key,pt in a.NODES.items():
 results=hit_z(pt[:2]);
 if not any(abs(z-pt[2])<.01 for z,n in results):errors.append(('junction',key,results))
parts=[n for n,_,_,_ in scene.parts]
# Grounded, conservative acceptance audit: a short partition face + flooring
# without a closed occupied volume, aperture with lintel, roof, and staircase
# is NOT a real habitable room; the code contains no such assembly at all.
solid_room_count=0
stairs_count=0
support_checks='NOT_RUN'
report={
 'g0_probe_name':'NARROW_TRIANGLE_SURFACE_FLOOR_SAMPLE_NOT_G2',
 'nominal_plan_graph_connected':True,
 'street_floor_samples':len(checked),
 'samples_without_public_surface':len(holes),
 'samples_with_wrong_floor_elevation':len(errors),
 'hole_examples':holes[:12], 'wrong_elevation_examples':errors[:12],
 'shared_junction_count':len(a.NODES),
 'fully_enclosed_and_serviced_real_rooms':solid_room_count,
 'real_staircases_to_programmed_upper_spaces':stairs_count,
 'verified_load_bearing_supports':support_checks,
 'qualifies_as_inhabited_future_city':False,
 'visual_grade':'G0_ART_REJECT_REQUIRES_HUMAN_REVIEW',
 'formal_gates':a.GATES,
 'construction':'FORBIDDEN', 'city_integration':'FORBIDDEN',
 'reason':'3D ribbons are physically present, but real habitable rooms, layered floor access, and structural supports remain absent; macroform is a spread-out flat deck/road network and eye view shows giant blank fins.'
}
(P/'a80-output'/'a80_critical_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
