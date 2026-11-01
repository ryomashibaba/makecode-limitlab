#!/usr/bin/env python3
"""M28 independent comparison on saved M27 vs M28 GLBs (not formality QA)."""
import os,json,hashlib,struct
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Point,Polygon
from shapely.ops import unary_union
OLD=Path("artifacts/m28_immutable_m27")
OUT=Path("artifacts/g4c7-m28-gallery-visual-art-edit")/("run_"+os.environ["GITHUB_SHA"][:12])
FLOOR="M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK"
THRESHOLD="M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD"
HIDDEN={"M27_exhibition_real_demonstration_plinth_0",
"M27_exhibition_label_readable_screen_0",
"M27_exhibition_instrument_0",
"M27_exhibition_lab_data_model_0"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def geometry(s,n):
 T,key=s.graph.get(n)
 a=trimesh.transform_points(s.geometry[key].vertices,T)
 return a,s.geometry[key].faces
def xy(a):return np.column_stack((a[:,0],-a[:,2]))
def footprint(s,n):
 v,f=geometry(s,n);h=float(v[:,1].max())
 faces=[Polygon(xy(v[t])) for t in f if np.allclose(v[t,1],h,atol=1e-5)]
 p=unary_union(faces)
 assert p.is_valid and p.area>2
 return p,h
def main():
 m=json.loads((OUT/"manifest.json").read_text())
 assert m["art"]=="HOLD_NOT_APPROVED" and m["minecraft"]=="FORBIDDEN" and m["adopted"]==0
 assert m["official_331_993"]=="NOT_RUN" and m["original_cameras_frozen"]
 old=list(OLD.rglob("M27_GALLERY_RESEARCH_UNAPPROVED.glb"))
 assert len(old)==1
 a=trimesh.load(old[0],file_type="glb",force="scene")
 now=OUT/"M28_VISITOR_GALLERY_ART_REVIEW_NOT_APPROVED.glb"
 assert sha(now)==m["glb_sha256"]
 b=trimesh.load(now,file_type="glb",force="scene")
 aa=set(a.graph.nodes_geometry);bb=set(b.graph.nodes_geometry)
 assert aa-bb==HIDDEN,(aa-bb)
 assert len([n for n in bb-aa if n.startswith("M28_")])>=35
 kept=0
 for n in aa-HIDDEN:
  x,fx=geometry(a,n);y,fy=geometry(b,n)
  assert x.shape==y.shape and fx.shape==fy.shape
  assert np.allclose(x,y,atol=1e-5) and np.array_equal(fx,fy),n
  kept+=1
 deck_a,ha=footprint(a,FLOOR);deck_b,hb=footprint(b,FLOOR)
 t_a,ta=footprint(a,THRESHOLD);t_b,tb=footprint(b,THRESHOLD)
 assert abs(deck_a.symmetric_difference(deck_b).area)<1e-4
 assert abs(t_a.symmetric_difference(t_b).area)<1e-4
 assert abs(ha-hb)<1e-5 and abs(ta-tb)<1e-5
 assert deck_b.intersection(t_b).area>5
 # Public route reference for M17 U0->U1: verify support center+0.65m disk
 # at 3 bounded samples. This DOES NOT replace official QA.
 for x,y in ((-24,13),(-29,30),(-28,18)):
  assert deck_b.covers(Point(x,y).buffer(.65,resolution=24)),(x,y)
 # Physical display should not interrupt center of public route in a
 # conservative 2D horizontal disc near its intended local point.
 display=np.array([-43+11.38,37-11.15])
 public=np.array([[-24,13],[-28,18],[-29,30]],dtype=float)
 assert float(np.min(np.linalg.norm(public-display,axis=1)))>1.1
 import PIL.Image as Image
 im={}
 for n,info in m["views"].items():
  f=OUT/("M28_"+n+".png")
  raw=f.read_bytes();assert raw[:8]==b"\x89PNG\r\n\x1a\n"
  assert struct.unpack(">II",raw[16:24])==(1080,680)
  assert sha(f)==info["sha256"]
  im[n]=dict(size=len(raw))
 blend=OUT/"M28_EDITABLE_ORBITAL_GALLERY.blend"
 assert blend.read_bytes().startswith(b"BLENDER") and sha(blend)==m["blend_sha256"]
 result={
  "status":"M28_FIXED_CAMERA_REAL_GLB_PRESERVATION_AND_LOCAL_ROUTE_SUPPORT_TECH_PASS",
  "preserved_M27_meshes":kept,
  "retired_occluding_display_meshes":len(HIDDEN),
  "new_M28_meshes":len(bb-aa),
  "gallery_original_area":deck_a.area,"gallery_M28_area":deck_b.area,
  "gallery_threshold_overlap_M28":deck_b.intersection(t_b).area,
  "gallery_and_threshold_height_unchanged":True,
  "route_support_three_centers":"PASS_LIMITED_ONLY",
  "images":im,"art":"HOLD_NOT_APPROVED","formal_safety":"NOT_RUN",
  "warning":"Screen-space improvement to be assessed visually, never via mesh count or image hashes alone."
 }
 (OUT/"M28_independent_readback.json").write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
