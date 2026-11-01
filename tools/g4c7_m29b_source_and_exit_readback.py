#!/usr/bin/env python3
"""M29B honest two-phase independent readback. Pinned prior native/GLB output
is fully checked without re-rendering 3 heavy images. Camera-only re-render
is checked separately. No false formal body/access/ART pass.
"""
from pathlib import Path
import hashlib,json,os,sys,struct
S29=Path("artifacts/m29b_immutable_m29")
S28=Path("artifacts/m29b_immutable_m28b")
OUT=Path("artifacts/g4c7-m29b-exit-human-eye")/("run_"+os.environ["GITHUB_SHA"][:12])
M29_BLEND="eae814098136f291c2d0c01fd327a711fbaf97296ec9d9e31527927641044cdc"
M29_GLB="28d2bfb9b7a870108036edbee988a5f0f5e8f8d07fd1af17a4acc4c00af6d822"
M28B_GLB="6cd70a071af65fda3eb9bd37c9dcb5fab1807250c656dd13b469e631de4a05f2"
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def sole(root,n):
 p=list(root.rglob(n))
 assert len(p)==1,(root,n,len(p))
 return p[0]
def original():
 import numpy as np,trimesh
 from shapely.geometry import Polygon,Point
 from shapely.ops import unary_union
 old=sole(S28,"M28B_GALLERY_REFINEMENT_ART_HOLD.glb")
 new=sole(S29,"M29_HABITABLE_GARDEN_NOT_APPROVED.glb")
 assert sha(old)==M28B_GLB and sha(new)==M29_GLB
 original_scene=trimesh.load(old,file_type="glb",force="scene")
 newer=trimesh.load(new,file_type="glb",force="scene")
 oa=set(original_scene.graph.nodes_geometry)
 na=set(newer.graph.nodes_geometry)
 assert not oa-na and len(na-oa)==92
 def verts(s,n):
  T,k=s.graph.get(n)
  return trimesh.transform_points(s.geometry[k].vertices,T),s.geometry[k].faces
 for n in oa:
  a,f=verts(original_scene,n);b,g=verts(newer,n)
  assert a.shape==b.shape and np.array_equal(f,g) and np.allclose(a,b,atol=1e-5),(n,a.shape,b.shape)
 def top(n):
  w,f=verts(newer,n)
  h=float(w[:,1].max())
  ps=[Polygon(np.column_stack((w[i,0],-w[i,2]))) for i in f if np.allclose(w[i,1],h,atol=1e-5)]
  p=unary_union(ps);assert p.is_valid and p.area>3
  return p,h
 p,h=top("M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK")
 q,g=top("M29_CONNECTED_OUTDOOR_RESEARCH_COURT_DECK")
 door,d=top("M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD")
 overlap=p.intersection(q).area
 assert 5.5<overlap<6 and abs(h-g)<1e-5
 assert p.intersection(door).area>5.9
 for c in ((-23.9,22.5),(-22.1,22.5),(-19.5,22.5)):
  assert p.union(q).covers(Point(*c).buffer(.65,resolution=24)),c
 mf=sole(S29,"manifest.json")
 m=json.loads(mf.read_text())
 assert m["G0_S1_G1_G2_G3"]=="NOT_RUN" and m["official_331_993"]=="NOT_RUN"
 assert m["art"]=="HOLD_NOT_APPROVED" and m["adopted"]==0 and m["minecraft"]=="FORBIDDEN"
 assert sha(sole(S29,"M29_EDITABLE_OPEN_AIR_RESEARCH_COURT.blend"))==M29_BLEND
 for n,x in m["views"].items():
  f=sole(S29,"M29_"+n+".png")
  assert sha(f)==x["sha256"]
  assert struct.unpack(">II",f.read_bytes()[16:24])==(1080,680)
 result={"status":"M29_ACTUAL_SAVED_GLTF_TECH_LOCAL_PASS_FORMAL_HOLD",
  "M28B_meshes_preserved":len(oa),"M29_new_meshes":len(na-oa),
  "real_deck_positive_overlap":overlap,
  "deck_top_height_delta":g-h,
  "original_gallery_portal_overlap":p.intersection(door).area,
  "bounded_3_disk_diagnostic":"PASS",
  "source_sha256":"MATCH","saved_M29_real_3_Cycles_images":"MATCH",
  "formal_body_331_feet_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "art":"HOLD_NOT_APPROVED","minecraft":"FORBIDDEN",
  "caveat":"Positive local contact is not complete human path or construction-safe elevated exterior."}
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/"M29_SOURCE_SAVED_GLTF_INDEPENDENT_AUDIT.json").write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
def camera():
 m=json.loads((OUT/"manifest.json").read_text())
 assert m["pinned_M29_native_SHA256"]==M29_BLEND and m["geometry_edit_count"]==0
 assert m["art"]=="HOLD_NOT_APPROVED" and m["formal_331_993"]=="NOT_RUN"
 assert set(m["frozen_comparison_cameras"])=={
  "M27_CAMERA_gallery_arrival_eye","M27_CAMERA_controlled_threshold_eye"}
 blend=OUT/"M29B_EDITABLE_HUMAN_EXIT_VIEW_ONLY.blend"
 png=OUT/"M29B_OPEN_AIR_FROM_GALLERY_EXIT.png"
 assert blend.read_bytes().startswith(b"BLENDER") and sha(blend)==m["blend_sha256"]
 raw=png.read_bytes()
 assert raw[:8]==b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",raw[16:24])==(1080,680)
 assert sha(png)==m["png_sha256"]
 print("M29B_CAMERA_ONLY_NATIVE_TECH_PASS_ART_HOLD")
if __name__=="__main__":
 if "--original" in sys.argv:original()
 elif "--camera" in sys.argv:camera()
 else:raise SystemExit("Specify --original or --camera")
