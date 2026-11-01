#!/usr/bin/env python3
"""M17 editable native 3-D diagram, NOT the architectural artwork or Minecraft build."""
import json,sys,os,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
OUT=ROOT/"artifacts/g4c7-m17-authoring-guide"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate(s):
 nodes={n["id"]:n for n in s["nodes"]};edges=s["edges"]
 assert len(nodes)==18 and len(edges)==18 and len({tuple(n["xyz"]) for n in nodes.values()})==18
 assert s["gates"]["art"]=="HOLD" and s["gates"]["adopted"]==0 and s["gates"]["minecraft_education"]=="NO_WRITE"
 def walk(skip=()):
  adj={k:set() for k,n in nodes.items() if n["access"]=="public"}
  for e in edges:
   a,b=e["from"],e["to"]
   assert a in nodes and b in nodes and e["width"]>0
   if e["kind"]=="stair_design_only": assert nodes[a]["xyz"][2]!=nodes[b]["xyz"][2]
   else: assert nodes[a]["xyz"][2]==nodes[b]["xyz"][2]
   if e["access"]=="public" and tuple(sorted((a,b))) not in skip:
    assert a in adj and b in adj
    adj[a].add(b);adj[b].add(a)
  seen=set(["P0_GATE"]);todo=["P0_GATE"]
  while todo:
   for v in adj[todo.pop()]:
    if v not in seen: seen.add(v);todo.append(v)
  return seen
 public={k for k,n in nodes.items() if n["access"]=="public"}
 assert walk()==public,"Public network must be one connected component"
 for k in ("P5_MARKET_INTERIOR","P6_MAKER_HALL","U1_RESEARCH_OBSERVATORY","U2_SKY_GARDEN","G0_UPPER_GREENHOUSE"): assert k in walk()
 for k in ("R1_HOME","R0_RESEARCH_LAB","S0_SERVICE"):assert k not in walk()
 cut=[tuple(sorted(p)) for p in (("P7_STAIR_SOUTH","U0_SOUTH_GALLERY"),("P8_STAIR_NORTH","U3_NORTH_GALLERY"))]
 assert "U1_RESEARCH_OBSERVATORY" not in walk(cut),"negative: stair closure must disconnect gallery"
 assert min(e["width"] for e in edges if e["access"]=="public")>=6
 return {"nodes":18,"edges":18,"public_nodes":len(public),"public_connected":True,
   "negative_private_service_and_stairs":True,"min_public_design_width":6,"art":"HOLD","minecraft":"FORBIDDEN"}
def make():
 import bpy
 from mathutils import Vector
 spec=json.loads(SPEC.read_text(encoding="utf-8"))
 report=validate(spec)
 assert not OUT.exists()
 OUT.mkdir(parents=True)
 bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene
 col=bpy.data.collections.new("M17_TOPOLOGY_AUTHORING_GUIDE_NOT_CITY")
 scene.collection.children.link(col)
 palette={"public":(.07,.56,.66),"semiprivate":(.72,.49,.21),
          "restricted":(.67,.25,.32),"private":(.67,.25,.32),"service":(.35,.38,.43)}
 mats={}
 for role,rgb in palette.items():
  m=bpy.data.materials.new("M17_"+role);m.diffuse_color=(*rgb,1)
  m.use_nodes=True;m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*rgb,1)
  mats[role]=m
 def join_col(o):
  for prev in list(o.users_collection):prev.objects.unlink(o)
  col.objects.link(o)
  o.show_name=True
 def build_link(name,a,b,role):
  p,q=Vector(a),Vector(b);v=q-p
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.42 if role=="public" else .25,depth=v.length,location=(p+q)*.5)
  o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat("Z","Y").to_euler()
  join_col(o);o.data.materials.append(mats[role])
 nd={n["id"]:n for n in spec["nodes"]}
 for i,e in enumerate(spec["edges"]):
  build_link("GUIDE_EDGE_%02d_%s"%(i,e["kind"]),nd[e["from"]]["xyz"],nd[e["to"]]["xyz"],e["access"])
 for n in spec["nodes"]:
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1.4,location=n["xyz"])
  o=bpy.context.object;o.name="GUIDE_NODE_"+n["id"];join_col(o);o.data.materials.append(mats[n["access"]])
  curve=bpy.data.curves.new("LABEL_"+n["id"],type="FONT");curve.body=n["id"].replace("_"," ");curve.size=1.55
  label=bpy.data.objects.new("LABEL_"+n["id"],curve);col.objects.link(label)
  label.location=tuple(c+[2.2] if False else (n["xyz"][0]+2,n["xyz"][1],n["xyz"][2]+2))
 camdata=bpy.data.cameras.new("M17_AUTHOR_CAMERA");camera=bpy.data.objects.new("M17_AUTHOR_CAMERA",camdata)
 col.objects.link(camera);camera.location=(-185,-195,145)
 camera.rotation_euler=(Vector((0,-10,4))-camera.location).to_track_quat("-Z","Y").to_euler()
 camdata.lens=44;scene.camera=camera
 lamp=bpy.data.lights.new("M17_SUN","SUN");lamp.energy=2.8
 lampobj=bpy.data.objects.new("M17_SUN",lamp);col.objects.link(lampobj);lampobj.rotation_euler=(.5,-.7,.3)
 world=bpy.data.worlds.new("M17_Sky") if not scene.world else scene.world
 scene.world=world;world.use_nodes=True
 world.node_tree.nodes["Background"].inputs["Color"].default_value=(.65,.73,.82,1)
 world.node_tree.nodes["Background"].inputs["Strength"].default_value=.8
 scene.render.engine="CYCLES";scene.cycles.samples=8
 scene.render.resolution_x=1050;scene.render.resolution_y=680;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 scene["M17_STATUS"]="SPATIAL_TOPOLOGY_NOT_ARCHITECTURAL_CITY"
 scene["ART"]="HOLD";scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["G0_S1_G1_G2_G3"]="NOT_RUN";scene["FORMAL_331_993"]="NOT_RUN"
 native=OUT/"M17_EDITABLE_TOPOLOGY_GUIDE_NOT_CITY.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(native),check_existing=False)
 png=OUT/"M17_NATIVE_TOPOLOGY_PREVIEW.png";scene.render.filepath=str(png)
 bpy.ops.render.render(write_still=True)
 assert png.is_file() and png.stat().st_size>1024
 manifest={"status":report,"native_sha256":digest(native),"png_sha256":digest(png),
   "source_sha256":digest(SPEC),"scope":"guide only, not building/art or human safety"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
 print("M17_NATIVE_GUIDE_COMPLETE_ART_HOLD",OUT)
if __name__=="__main__":
 s=json.loads(SPEC.read_text(encoding="utf-8"))
 if "--preflight" in sys.argv: print(json.dumps(validate(s),indent=2))
 else: make()
