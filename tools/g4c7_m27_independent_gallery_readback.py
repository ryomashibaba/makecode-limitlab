#!/usr/bin/env python3
"""M27 independent readback from ACTUAL exported GLBs; bounded access test only."""
import os,json,hashlib,struct
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Polygon,Point,LineString
SEED=Path("artifacts/m27_immutable_m26b")
OUT=Path("artifacts/g4c7-m27-visitor-gallery-entry")/("run_"+os.environ["GITHUB_SHA"][:12])
ROAD="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
PANE="M26_east_large_daylight_glazing_32"
FLOOR="M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK"
THRESHOLD="M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def world_mesh(scene,name):
 tx,key=scene.graph.get(name)
 return trimesh.transform_points(scene.geometry[key].vertices,tx),scene.geometry[key].faces
def xy(v):return np.stack([v[:,0],-v[:,2]],axis=1)
def main():
 m=json.loads((OUT/"manifest.json").read_text())
 assert m["art"]=="HOLD_NOT_APPROVED" and m["adopted"]==0 and m["minecraft"]=="FORBIDDEN"
 assert m["official_331_993"]=="NOT_RUN" and m["formal_G0_S1_G1_G2_G3"]=="NOT_RUN"
 assert m["removed_from_visible_geometry_one_pane"]==PANE
 original=list(SEED.rglob("M26B_INTERIOR_ART_REVIEW_UNAPPROVED.glb"))
 assert len(original)==1
 before=trimesh.load(str(original[0]),file_type="glb",force="scene")
 afterfile=OUT/"M27_GALLERY_RESEARCH_UNAPPROVED.glb"
 assert sha(afterfile)==m["glb_sha256"]
 after=trimesh.load(str(afterfile),file_type="glb",force="scene")
 oldset=set(before.graph.nodes_geometry);newset=set(after.graph.nodes_geometry)
 # Glazed wall segment must be truly absent in exported geometry.
 assert PANE in oldset and PANE not in newset
 assert FLOOR in newset and THRESHOLD in newset
 assert len(oldset-newset)==1,(oldset-newset)
 untouched=0
 for n in sorted(oldset-{PANE}):
  a,fa=world_mesh(before,n);b,fb=world_mesh(after,n)
  assert a.shape==b.shape and fa.shape==fb.shape and np.allclose(a,b,atol=1e-5),(n,a.shape,b.shape)
  untouched+=1
 v,f=world_mesh(after,FLOOR)
 # exported glTF is y-up, room +z world -> +y
 assert np.ptp(v[:,1])<1e-5
 deck_height=float(v[:,1].max())
 # mesh top is planar top polygon, bottom polygon is separate.
 # glTF cubes have top/bottom faces: recover top triangles.
 top_polys=[Polygon(xy(v[face])) for face in f if np.allclose(v[face,1],deck_height,atol=1e-5)]
 from shapely.ops import unary_union
 footprint=unary_union(top_polys)
 assert footprint.area>300 and footprint.is_valid
 # Relative local to M17 lab origin: U0=(+19,-24), U1=(+14,-7).
 for xy_local in [(19,-24),(14,-7),(14.5,-19)]:
  target=Point(-43+xy_local[0],37+xy_local[1])
  assert footprint.covers(target.buffer(.65,resolution=24)),xy_local
 threshold_v,threshold_f=world_mesh(after,THRESHOLD)
 t_top=float(threshold_v[:,1].max())
 local_gallery_top=9.6+m["geometry_check"]["gallery_floor_top_local"]
 local_threshold_top=9.6+m["geometry_check"]["threshold_top_local"]
 assert abs(deck_height-local_gallery_top)<1e-4
 assert abs(t_top-local_threshold_top)<1e-4
 assert abs(t_top-deck_height)<.05
 threshold_top=[Polygon(xy(threshold_v[face])) for face in threshold_f if np.allclose(threshold_v[face,1],t_top,atol=1e-5)]
 threshold_area=unary_union(threshold_top)
 assert footprint.intersection(threshold_area).area>1.0,"Gallery/doorway positive floor overlap missing"
 # M26B wood floor planks are explicit, all original meshes unchanged.
 room_floor=[]
 for n in oldset:
  if not n.startswith("M26_oak_floor_interior_plank_"):continue
  w,faces=world_mesh(after,n)
  zz=float(w[:,1].max())
  top=[Polygon(xy(w[face])) for face in faces if np.allclose(w[face,1],zz,atol=1e-5)]
  room_floor+=top
 oak=unary_union(room_floor)
 assert oak.intersection(threshold_area).area>.5,"Door threshold fails to contact existing room wood floor"
 assert abs(float(9.6+.043)-float(deck_height))<1e-4
 # Strictly limited access: elevated U0↔U1 + threshold. Do NOT assert the
 # entire M17 city, stairs, head-height or all lab furniture routes.
 views=m["three_view_sha256"]
 assert set(views)=={"gallery_arrival_eye","controlled_threshold_eye","original_research_eye"}
 for n,entry in views.items():
  raw=(OUT/("M27_"+n+".png")).read_bytes()
  assert raw[:8]==b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",raw[16:24])==(1080,680)
  assert hashlib.sha256(raw).hexdigest()==entry["sha256"]
 blend=OUT/"M27_EDITABLE_RESEARCH_VISITOR_GALLERY.blend"
 assert blend.read_bytes().startswith(b"BLENDER") and sha(blend)==m["blend_sha256"]
 result={"status":"M27_REAL_GLTF_LOCAL_PORTAL_AND_GALLERY_CONTACT_TECH_PASS",
 "original_meshes_preserved":untouched,"removed_obstructing_glazed_pane":PANE,
 "new_meshes":len(newset-oldset),
 "U0_U1_disk_support_diagnostic":"PASS_FOR_THREE_SAMPLE_CENTERS_ONLY",
 "positive_gallery_threshold_area":footprint.intersection(threshold_area).area,
 "positive_threshold_existing_lab_floor_area":oak.intersection(threshold_area).area,
 "local_floor_height_difference":t_top-deck_height,
 "gallery_floor_area":footprint.area,
 "camera_and_shas":"PASS",
 "conclusion":"ART HOLD; NO FORMAL 331/993, STEP, STAIR, 3D SWEEP OR CONSTRUCTION APPROVAL",
 "minecraft":"FORBIDDEN","adopted":0}
 (OUT/"independent_glb_readback.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
