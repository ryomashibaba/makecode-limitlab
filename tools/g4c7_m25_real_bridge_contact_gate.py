#!/usr/bin/env python3
"""M25 independent negative control: height alignment != walking contact.
Do not certify M25; this test must demonstrate that the general contact gate
REJECTS the known detached M25 bridge/pocket geometry.
"""
import json,os,hashlib
from pathlib import Path
import numpy as np,trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union
SEED=Path("artifacts/m25_immutable_native_for_negative_control")
PIN="826befc37288458e1fdaf59d14bea234116fd728878ac63925f8222b98c0bc12"
OUT=Path("artifacts/g4c7-m25-bridge-contact-negative-gate")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
def original():
 fs=list(SEED.rglob("M25_SECTION_HERO_GEOMETRY_UNAPPROVED.glb"))
 assert len(fs)==1
 assert hashlib.sha256(fs[0].read_bytes()).hexdigest()==PIN
 return fs[0]
def geometry(scene,name):
 mat,key=scene.graph.get(name)
 mesh=scene.geometry[key]
 world=trimesh.transform_points(mesh.vertices,mat)
 polys=[Polygon([(world[i,0],-world[i,2]) for i in face])
           for face in mesh.faces]
 return world,unary_union(polys)
def contact_required(room,bridge,max_z_difference=.05,min_overlap_area=.10):
 # This reusable GATE is necessary, but not sufficient for safe human travel:
 # it only checks overlap of the horizontal surface projections and height.
 rw,rp=room;bw,bp=bridge
 zroom=float(np.max(rw[:,1]))
 zbridge=float(np.max(bw[:,1]))
 gap=float(rp.distance(bp));overlap=float(rp.intersection(bp).area)
 elevation=abs(zroom-zbridge)
 assert elevation<=max_z_difference,("HEIGHT_MISMATCH",elevation)
 assert overlap>=min_overlap_area,("BRIDGE_NOT_TOUCHING_POCKET",gap,overlap)
 return {"overlap_area":overlap,"height_delta":elevation}
def main():
 scene=trimesh.load(str(original()),force="scene")
 assert len(scene.graph.nodes_geometry)==225
 details=[]
 for k in (1,2):
  bridge=geometry(scene,"M25_true_level_matched_bridge_"+str(k))
  for side in ("west","east"):
   room=geometry(scene,"M25_"+side+"_carved_occupied_pocket_"+str(k))
   z=float(abs(np.max(room[0][:,1])-np.max(bridge[0][:,1])))
   gap=float(room[1].distance(bridge[1]))
   area=float(room[1].intersection(bridge[1]).area)
   assert z<=.05 and 0<gap<3 and area<1e-6
   rejected=False
   try:contact_required(room,bridge)
   except AssertionError as e:
    rejected=True
    assert "BRIDGE_NOT_TOUCHING_POCKET" in str(e)
   assert rejected,"Known unsafe sample must be rejected"
   details.append({"level":k,"side":side,"height_delta":z,
       "horizontal_gap_design_units":gap,"overlap_area":area,
       "validated_as_connected":False})
 assert len(details)==4
 OUT.mkdir(parents=True,exist_ok=False)
 result={"source_sha256":PIN,
  "status":"M25_NEGATIVE_CONTACT_GATE_PASS_BY_REJECTING_DISCONNECTED_BRIDGES",
  "tested_bridge_ends":4,"rejected_ends":4,
  "details":details,
  "reason":"M25 bridge decks are level but do NOT intersect floor pockets in plan",
  "art":"REJECT","adopted":0,"formal_331_993":"NOT_RUN",
  "G0_S1_G1_G2_G3":"NOT_RUN","minecraft":"FORBIDDEN"}
 (OUT/"manifest.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
