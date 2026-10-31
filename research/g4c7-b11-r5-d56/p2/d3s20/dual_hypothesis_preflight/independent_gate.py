"""Independent, non-construction morphology / route preflight.
Reads SAVED and RELOADED GLB and authors' semantic JSON, not Python source.
This is intentionally NOT the formal 331/993 or human-width/swept-volume QA.
"""
import json,math
from pathlib import Path
import numpy as np, trimesh
from shapely.geometry import box,MultiPoint
from shapely.ops import unary_union
R=Path(__file__).resolve().parent
report={}
def point_polyline_distance_z(point,segments):
 p=np.asarray(point,dtype=float);best=(float('inf'),None,None)
 for _,path in segments:
  pts=np.asarray(path['points'],float)
  for a,b in zip(pts[:-1],pts[1:]):
   v=b[:2]-a[:2];den=np.dot(v,v)
   if den<1e-8:continue
   t=float(np.clip(np.dot(p[:2]-a[:2],v)/den,0,1))
   q=a+t*(b-a);delta=float(np.linalg.norm(p[:2]-q[:2]));
   if delta<best[0]:best=(delta,float(q[2]),path['width'])
 return best
for name in ('A_INHABITED_CANYON','B_BRAIDED_RIDGES'):
 data=json.loads((R/(name+'.json')).read_text());s=trimesh.load(R/(name+'.glb'),force='scene');assert len(s.geometry)==data['geometries']
 bounds=s.bounds
 public=[(k,v) for k,v in data['functional_paths'].items()]
 portal=[]
 for key,room in data['rooms'].items():
  d,z,width=point_polyline_distance_z(room['door_center'],public)
  gap=max(0,d-width/2)
  delta=abs(z-room['floor_z'])
  portal.append({'room':key,'lane_edge_gap_m':round(gap,2),'z_mismatch_m':round(delta,2),'preflight_near':gap<=2 and delta<=3})
 floor_geoms=[(key,m) for key,m in s.geometry.items() if data['components'].get(key,{}).get('role') in ('room_floor','continuous_slope_walkway_candidate')]
 # bounded projected convex-hull union, OVERestimates area for rotated/concave geometry; useful only for detecting sparse coverage.
 shapes=[]
 for key,m in floor_geoms:
  try:
   poly=MultiPoint(m.vertices[:,:2]).convex_hull
   if poly.area>0:shapes.append(poly)
  except:pass
 aabb_area=(bounds[1,0]-bounds[0,0])*(bounds[1,1]-bounds[0,1]);area=sum(x.area for x in shapes);union=unary_union(shapes).area
 ratio=union/aabb_area
 slopes={k:round(v['slope_max'],5) for k,v in public};too_steep=[k for k,v in public if v['slope_max']>1/12]
 report[name]={'saved_glb_sha256':data['glb_sha256'],'geometry_count':len(s.geometry),'bounds':bounds.tolist(),'room_like_cavities':len(data['rooms']),'public_paths':len(public),'route_slope_ratios':slopes,'above_1_in_12':too_steep,'door_point_proximity_only':{'near_within_2m_horizontal_3m_vertical':sum(p['preflight_near'] for p in portal),'total':len(portal),'individual':portal},'projected_candidate_floor_and_path_coverage_over_aabb':round(float(ratio),5),'footprint_model':'Convex hulls of each floor or ribbon GLB node; broad estimate, NOT supported contiguous floor, exact usable area, or Minecraft blocks','formal_qa':'NOT_RUN','art_gate':'REJECT: isolated room modules plus ribbons; not integrated macro urban space'}
 print(name,'ROOMS',len(portal),'NEAR',sum(p['preflight_near'] for p in portal),'MAX-SLOPE',max(slopes.values()),'COVERAGE',ratio,'STEEP',too_steep)
 print('DOOR GAPS',[(p['room'],p['lane_edge_gap_m'],p['z_mismatch_m']) for p in portal])
(R/'INDEPENDENT_GATE.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
