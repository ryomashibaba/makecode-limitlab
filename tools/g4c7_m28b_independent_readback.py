#!/usr/bin/env python3
"""Verify exact M28B sign-only 3 mesh transformations, 3 benched removals,
and no floor/threshold changes in saved glTF. Bounded geometry, not formal QA.
"""
from pathlib import Path
import os,json,hashlib,struct
import trimesh,numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
ROOT=Path("artifacts/m28b_pinned_m28")
OUT=Path("artifacts/g4c7-m28b-gallery-sign-occlusion-correction")/("run_"+os.environ["GITHUB_SHA"][:12])
SIGN={"M28_CINEMATIC_WELCOME_SIGN","M28_CENTRAL_SIGN_HEAD","M28_CENTRAL_SIGN_SUB"}
HIDE={"M28_VIEWING_SEAT_WARM_LOW_BENCH","M28_VIEWING_SEAT_CUSHION","M28_VIEWING_SEAT_BACK"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(s,n):
 t,key=s.graph.get(n)
 return trimesh.transform_points(s.geometry[key].vertices,t),s.geometry[key].faces
def top(s,n):
 v,f=mesh(s,n);z=float(v[:,1].max())
 arr=[Polygon(v[t][:,(0,2)]) for t in f if np.allclose(v[t,1],z,atol=1e-5)]
 p=unary_union(arr)
 assert p.is_valid and p.area>2
 return p,z
def run():
 m=json.loads((OUT/"manifest.json").read_text())
 assert m["art"]=="HOLD_NOT_APPROVED" and m["adopted"]==0
 assert m["minecraft"]=="FORBIDDEN" and m["official_331_993"]=="NOT_RUN"
 assert m["original_frozen_cameras"] and set(m["hidden_exact_three_bench_objects"])==HIDE
 assert set(m["changed_exact_three_existing_sign_objects"])==SIGN
 old=list(ROOT.rglob("M28_VISITOR_GALLERY_ART_REVIEW_NOT_APPROVED.glb"))
 assert len(old)==1 and sha(old[0])==m["source_GLB_SHA256"]
 a=trimesh.load(old[0],file_type="glb",force="scene")
 new=OUT/"M28B_GALLERY_REFINEMENT_ART_HOLD.glb"
 assert sha(new)==m["glb_sha256"]
 b=trimesh.load(new,file_type="glb",force="scene")
 aa=set(a.graph.nodes_geometry);bb=set(b.graph.nodes_geometry)
 assert aa-bb==HIDE and bb-aa==set()
 kept=0
 for name in sorted(aa-SIGN-HIDE):
  va,fa=mesh(a,name);vb,fb=mesh(b,name)
  assert np.array_equal(fa,fb) and va.shape==vb.shape,(name,va.shape,vb.shape)
  assert np.allclose(va,vb,atol=1e-5),name
  kept+=1
 sign_changes=[]
 for name in SIGN:
  va,fa=mesh(a,name);vb,fb=mesh(b,name)
  assert np.linalg.norm(va.mean(axis=0)-vb.mean(axis=0))>.1,name
  sign_changes.append(name)
 fa,ha=top(a,"M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK")
 fb,hb=top(b,"M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK")
 ta,ya=top(a,"M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD")
 tb,yb=top(b,"M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD")
 assert fa.symmetric_difference(fb).area<1e-4 and ta.symmetric_difference(tb).area<1e-4
 assert abs(ha-hb)<1e-5 and abs(ya-yb)<1e-5
 assert fb.intersection(tb).area>5.9
 for n,meta in m["views"].items():
  raw=(OUT/("M28B_"+n+".png")).read_bytes()
  assert raw[:8]==b"\x89PNG\r\n\x1a\n"
  assert struct.unpack(">II",raw[16:24])==(1080,680)
  assert sha(OUT/("M28B_"+n+".png"))==meta["sha256"]
 blend=OUT/"M28B_EDITED_HUMAN_GALLERY_SIGHTLINE.blend"
 assert blend.read_bytes().startswith(b"BLENDER") and sha(blend)==m["blend_sha256"]
 result={"status":"M28B_SAVED_NATIVE_SIGN_ONLY_EDITS_AND_FLOOR_PRESERVATION_PASS",
  "unchanged_GLTF_meshes":kept,
  "sign_geometry_changes":sign_changes,
  "removed_gallery_benches":len(HIDE),
  "new_meshes":0,
  "gallery_floor_area_preserved":fb.area,
  "portal_positive_contact_area":fb.intersection(tb).area,
  "two_fixed_camera_png_sha256_pass":True,
  "art":"HOLD_NOT_APPROVED","formal_331_993":"NOT_RUN",
  "remark":"Geometric tech pass; no city-scale art, human 3D sweep, or construction certification"}
 (OUT/"readback.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps(result,indent=2))
if __name__=="__main__":run()
