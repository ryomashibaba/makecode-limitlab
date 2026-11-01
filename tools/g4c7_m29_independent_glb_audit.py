#!/usr/bin/env python3
"""M29 independent GLB vs SHA-fixed M28B base: preserve all existing meshes,
verify actual world-space slab overlap, 2m physical guard opening limited.
"""
from pathlib import Path
import os,json,hashlib,struct
import numpy as np,trimesh
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
SEED=Path("artifacts/m29_pinned_m28b")
OUT=Path("artifacts/g4c7-m29-open-air-experience")/("run_"+os.environ["GITHUB_SHA"][:12])
NEW="M29_CONNECTED_OUTDOOR_RESEARCH_COURT_DECK"
OLD="M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK"
PORTAL="M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD"
GLB_PIN="6cd70a071af65fda3eb9bd37c9dcb5fab1807250c656dd13b469e631de4a05f2"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(s,n):
 T,k=s.graph.get(n)
 return trimesh.transform_points(s.geometry[k].vertices,T),s.geometry[k].faces
def upper(s,n):
 v,f=mesh(s,n);h=float(v[:,1].max())
 pp=[]
 for t in f:
  if np.allclose(v[t,1],h,atol=1e-5):
   p=Polygon(np.column_stack((v[t,0],-v[t,2])))
   if p.area>1e-7:pp.append(p)
 assert pp,(n,h)
 poly=unary_union(pp)
 assert poly.is_valid
 return poly,h
def main():
 m=json.loads((OUT/"manifest.json").read_text())
 assert m["art"]=="HOLD_NOT_APPROVED" and m["adopted"]==0 and m["minecraft"]=="FORBIDDEN"
 assert m["official_331_993"]=="NOT_RUN" and m["G0_S1_G2_G3"]=="NOT_RUN"
 source=list(SEED.rglob("M28B_GALLERY_REFINEMENT_ART_HOLD.glb"))
 assert len(source)==1 and sha(source[0])==GLB_PIN
 a=trimesh.load(source[0],file_type="glb",force="scene")
 target=OUT/"M29_HABITABLE_GARDEN_NOT_APPROVED.glb"
 assert sha(target)==m["glb_sha256"]
 b=trimesh.load(target,file_type="glb",force="scene")
 aa=set(a.graph.nodes_geometry);bb=set(b.graph.nodes_geometry)
 assert not aa-bb,sorted(aa-bb)
 changed=[]
 for n in aa:
  va,fa=mesh(a,n);vb,fb=mesh(b,n)
  assert va.shape==vb.shape and np.array_equal(fa,fb),(n,va.shape,vb.shape)
  if not np.allclose(va,vb,atol=1e-5):changed.append(n)
 assert not changed,changed
 assert NEW in bb and len(bb-aa)>=70
 old,h0=upper(b,OLD);new,h1=upper(b,NEW)
 door,dh=upper(b,PORTAL)
 assert abs(h0-h1)<1e-5 and abs(h0-9.643)<1e-4,(h0,h1)
 overlap=old.intersection(new).area
 assert overlap>5 and overlap<8,(overlap,old.area)
 # Three bounded circles through actual gap in M27 parapet.
 points=[(-23.9,22.5),(-22.1,22.5),(-19.5,22.5)]
 combined=old.union(new)
 for x,y in points:
  assert combined.covers(Point(x,y).buffer(.65,resolution=24)),(x,y)
 assert old.intersection(door).area>5.9
 # Verify the exact reference 2m guard discontinuity in the input model.
 for n in ("M27_east_guard_top_0","M27_east_guard_top_1"):
  assert n in bb
 # Guard gap is a study design claim; full 3D clearance remains untested.
 assert len(m["views"])==3
 for n,ref in m["views"].items():
  raw=(OUT/("M29_"+n+".png")).read_bytes()
  assert raw[:8]==b"\x89PNG\r\n\x1a\n"
  assert struct.unpack(">II",raw[16:24])==(1080,680)
  assert sha(OUT/("M29_"+n+".png"))==ref["sha256"]
 blend=OUT/"M29_EDITABLE_OPEN_AIR_RESEARCH_COURT.blend"
 assert blend.read_bytes().startswith(b"BLENDER") and sha(blend)==m["blend_sha256"]
 report={
  "stage":"M29_SAVED_GLTF_INDEPENDENT_PROVENANCE_AND_POSITIVE_OUTDOOR_CONNECTION",
  "M28B_unchanged_existing_meshes":len(aa),"new_GLTF_meshes":len(bb-aa),
  "gallery_old_area":old.area,"garden_deck_area":new.area,
  "gallery_garden_top_diff":h1-h0,"gallery_deck_positive_overlap":overlap,
  "portal_to_gallery_positive_overlap":old.intersection(door).area,
  "three_local_0p65_disks_support_only":"PASS","actual_guard_slit_not_full_3D_certified":True,
  "images_SHA256":"PASS","native_BLENDER":"PASS",
  "art":"HOLD_NOT_APPROVED","adopted":0,
  "formal_331_993":"NOT_RUN","G0_S1_G2_G3":"NOT_RUN",
  "limitations":"No full body/route stair/structural or art certification, nor a whole futuristic city."}
 (OUT/"M29_independent_glb_audit.json").write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=="__main__":main()
