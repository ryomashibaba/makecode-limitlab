#!/usr/bin/env python3
"""M21 independent GLB 331/993 sampling. NOT formal safety QA.
No Minecraft operations, no artistically accepted building or route.
"""
import hashlib,json,math,os
from collections import Counter
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Polygon,Point,LineString
from shapely.ops import unary_union
from shapely.prepared import prep

ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m21_pinned_m20_source"
GRAPH=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
OUT=ROOT/"artifacts/g4c7-m21-real-mesh-support-diagnostic"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
GLB_SHA="e89949cc783a073ef55c51f0e475edb3b9aff6993c27d483142ace70f8e3b9b5"
FLOOR="M20_ONE_REAL_STREET_HOLE_AWARE"
BODY_RADIUS=.65
BODY_Y_RANGE=(.15,3.25)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def get_seed():
 files=list(SEED.rglob("M20_UNIONED_PUBLIC_FLOOR_ART_HOLD.glb"))
 assert len(files)==1,("M20 source must be unique",len(files))
 assert sha(files[0])==GLB_SHA,"Pinned source mismatch"
 return files[0]
def world(scene,name):
 transform,key=scene.graph.get(name)
 mesh=scene.geometry[key]
 return trimesh.transform_points(mesh.vertices,transform),mesh.faces
def footprint(tri):
 xy=tri[:,(0,2)].copy()
 xy[:,1]*=-1
 p=Polygon(xy)
 if p.area>1e-7:return p
 unique=np.unique(np.round(xy,6),axis=0)
 return LineString([tuple(v) for v in unique[:2]]) if len(unique)>=2 else None
def main():
 original=get_seed()
 assert not OUT.exists(),"No overwrite on research artifact"
 scene=trimesh.load(original,force="scene",file_type="glb")
 assert len(scene.graph.nodes_geometry)==154,"Unexpected M20 mesh count"
 v,faces=world(scene,FLOOR)
 assert len(faces)==25,"Unexpected street triangles"
 assert np.ptp(v[:,1])<1e-6,"Road is not level"
 ground=unary_union([footprint(v[f]) for f in faces])
 assert ground.geom_type=="Polygon" and ground.is_valid
 assert abs(ground.area-2495.2731511717707)<.001
 graph=json.loads(GRAPH.read_text(encoding="utf-8"))
 assert graph["gates"]["art"]=="HOLD" and graph["gates"]["minecraft_education"]=="NO_WRITE"
 nodes={n["id"]:n for n in graph["nodes"]}
 links=graph["edges"][:7]
 assert len(links)==7 and all(e["access"]=="public" for e in links)
 assert [e["kind"] for e in links]==["street","street","street","street","entry","entry","street"]
 foot_missing=[];disk_missing=[];body=[]
 erosion=ground.buffer(-BODY_RADIUS)
 for idx,e in enumerate(links):
  a=np.array(nodes[e["from"]]["xyz"][:2],dtype=float)
  b=np.array(nodes[e["to"]]["xyz"][:2],dtype=float)
  u=(b-a)/np.linalg.norm(b-a)
  perp=np.array([-u[1],u[0]])
  nsamples=48 if idx<2 else 47
  for j in range(nsamples):
   t=(j+.5)/nsamples
   center=a+(b-a)*t
   site={"route_index":idx,"sample_index":j,
         "point":[round(float(center[0]),6),round(float(center[1]),6)]}
   for offset in (-BODY_RADIUS,0,BODY_RADIUS):
    sample=center+perp*offset
    if not ground.covers(Point(sample)):
     foot_missing.append({**site,"lateral_offset":offset,
       "foot":[float(sample[0]),float(sample[1])]})
   margin=float(ground.boundary.distance(Point(center)))
   if not erosion.covers(Point(center)):
    disk_missing.append({**site,"edge_clearance":round(margin,6)})
   body.append((site,center))
 assert len(body)==331
 assert 331*3==993
 assert not ground.covers(Point(1000,1000)),"Negative control failed"
 # Conservative 2D silhouette, height-restricted to body interval.
 # Not a valid exact body collision test: classify as proximity only.
 obstacles=[]
 for name in scene.graph.nodes_geometry:
  if name==FLOOR:continue
  verts,triangles=world(scene,name)
  if verts[:,1].max()<BODY_Y_RANGE[0] or verts[:,1].min()>BODY_Y_RANGE[1]:continue
  projections=[]
  for f in triangles:
   tri=verts[f]
   if np.max(tri[:,1])<BODY_Y_RANGE[0] or np.min(tri[:,1])>BODY_Y_RANGE[1]:continue
   shape=footprint(tri)
   if shape is not None:projections.append(shape)
  if projections:obstacles.append((name,unary_union(projections).buffer(BODY_RADIUS)))
 hits=[];names=Counter()
 for site,center in body:
  obstacle_names=[name for name,region in obstacles if region.covers(Point(center))]
  if obstacle_names:
   hits.append({**site,"objects":obstacle_names})
   names.update(obstacle_names)
 assert len(foot_missing)==0,"Unexpected ground point support regression"
 # These are expected diagnostic failures and must never be labeled SAFE.
 assert len(disk_missing)>0 and len(hits)>0,"Potential unsupported body edge or obstruction was concealed"
 result={
  "status":"DIAGNOSTIC_ONLY_NOT_FORMAL_SAFETY_APPROVAL",
  "stage":"M21_GLB_REAL_MESH_STREET",
  "source_sha256":GLB_SHA,"source_real_meshes":154,
  "road_triangle_count":len(faces),"road_area":ground.area,
  "test":"331 route sample centers, 3 lateral feet per center, body-radius disk and conservative obstruction footprint",
  "samples":{"body_centers":len(body),"three_point_foot_samples":993,
    "point_foot_unsupported":len(foot_missing),
    "disk_radius":BODY_RADIUS,
    "disk_not_fully_supported_count":len(disk_missing),
    "conservative_near_obstacle_count":len(hits),
    "obstacle_meshes_considered":len(obstacles)},
  "per_route":[{"from":e["from"],"to":e["to"],"body_samples":48 if i<2 else 47,
    "unsupported_feet":sum(x["route_index"]==i for x in foot_missing),
    "disk_uncovered":sum(x["route_index"]==i for x in disk_missing),
    "near_obstacle":sum(x["route_index"]==i for x in hits)}
    for i,e in enumerate(links)],
  "disk_missing_locations":disk_missing,
  "obstacle_proximity_locations":hits,
  "obstacle_objects":names.most_common(),
  "negative_control_far_outside_support_pass":True,
  "limitations":[
    "993 three-point feet are not the official 993-foot sampling standard",
    "A full radius-.65 disk is a stronger local coverage diagnostic than three feet but not a validated human-body model",
    "3D obstacle proximity conservatively uses projected triangles and height AABB, not exact continuous human sweep",
    "Reference scale figures and stairs are included as proximity objects, not counted as proven safety contacts",
    "Only seven ground-level route edges were sampled; actual stair flights and upper galleries were not certified",
    "No Minecraft Education writes; G0/S1/G1/G2/G3 and official 331/993 remain NOT RUN"],
  "art":"HOLD","adopted":0,"minecraft":"FORBIDDEN",
  "official_body_331_foot_993":"NOT_RUN","official_gates":"NOT_RUN",
  "safety_decision":"HOLD_NOT_SAFE_TO_CONSTRUCT"
 }
 OUT.mkdir(parents=True)
 (OUT/"M21_independent_real_GLB_diagnostic.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({"status":result["status"],"samples":result["samples"],"per_route":result["per_route"]},indent=2))
if __name__=="__main__":main()
