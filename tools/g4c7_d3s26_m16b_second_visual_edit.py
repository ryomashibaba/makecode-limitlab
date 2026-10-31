#!/usr/bin/env python3
"""M16B: second native editing pass based on independently measured M16 visual occlusions."""
import hashlib,json,os,sys
from pathlib import Path
from math import radians
SEED=Path("artifacts/m16b_immutable_m16_seed")
OUT=Path("artifacts/g4c7-d3s26-m16b-second-visual-correction")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
INPUT_SHA="842ea0bc63f062eef39b6637066661c1f0d307d2b2110bb4a1d9868e91d4678b"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def find_seed():
 files=list(SEED.rglob("M16_EDITED_M15C_NATIVE_SCENE.blend"))
 assert len(files)==1,("m16b expected exactly one prior native scene",len(files))
 assert sha(files[0])==INPUT_SHA,"M16 immutable source has changed"
 return files[0]
def run():
 import bpy
 from mathutils import Vector
 original=find_seed()
 assert not OUT.exists(),"append-only no overwrite"
 bpy.ops.wm.open_mainfile(filepath=str(original.resolve()))
 scene=bpy.context.scene
 assert bpy.data.objects.get("MAKER_NORTH_THICK_WALL")
 assert bpy.data.objects.get("M16_HOME_REAL_FLOOR")
 assert bpy.data.objects.get("M16_MAKER_TRUE_DAYLIGHT_BAY_0")
 assert not bpy.data.collections.get("M16B_VISION_VERIFIED_REVISIONS")
 col=bpy.data.collections.new("M16B_VISION_VERIFIED_REVISIONS")
 scene.collection.children.link(col)
 def material(name,c,metal=0,trans=0):
  m=bpy.data.materials.new("M16B_"+name);m.use_nodes=True
  p=m.node_tree.nodes.get("Principled BSDF")
  p.inputs["Base Color"].default_value=(*c,1)
  p.inputs["Roughness"].default_value=.31
  p.inputs["Metallic"].default_value=metal
  p.inputs["Transmission Weight"].default_value=trans
  return m
 pale=material("perforated_civic_stone",(.66,.69,.61))
 copper=material("warm_structural_bronze",(.52,.39,.29),.47)
 clear=material("public_research_glass",(.81,.92,.88),0,.93)
 def cube(n,point,size,mat):
  bpy.ops.mesh.primitive_cube_add(size=1,location=point)
  ob=bpy.context.object;ob.name=n;ob.dimensions=size
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for old in list(ob.users_collection):old.objects.unlink(ob)
  col.objects.link(ob);ob.data.materials.append(mat)
 def panel(n,points,mat):
  mesh=bpy.data.meshes.new(n+"_mesh")
  mesh.from_pydata(points,[],[tuple(range(len(points)))]);mesh.update()
  ob=bpy.data.objects.new(n,mesh);col.objects.link(ob);mesh.materials.append(mat)
  mod=ob.modifiers.new("Window_thickness","SOLIDIFY");mod.thickness=.06
 # Ray cast showed research eye hits opaque MAKER_NORTH_THICK_WALL after 6.56 units.
 # Break the north wall into real structural bays and transparent daylight glazing.
 bpy.data.objects.remove(bpy.data.objects["MAKER_NORTH_THICK_WALL"],do_unlink=True)
 for i,x in enumerate((-36,-27,-18,-10)):
  cube("M16B_MAKER_NORTH_TRUE_PIER_%d"%i,(x,20,7.7),(1.05,1.25,15.4),pale)
 cube("M16B_MAKER_NORTH_REAL_SILL",(-23,20,1.15),(27,1.1,2.3),pale)
 cube("M16B_MAKER_NORTH_STRUCTURAL_HEADER",(-23,20,14.85),(27,1.1,.9),copper)
 for i,(xa,xb) in enumerate(((-35,-27.8),(-26.2,-18.8),(-17.2,-10.8))):
  panel("M16B_RESEARCH_VIEW_THRU_NORTH_BAY_%d"%i,
   [(xa,19.94,2.4),(xb,19.94,2.4),(xb,19.94,14.25),(xa,19.94,14.25)],clear)
 # User's maker view contained an opaque cyan hanging sheet: free up authentic workbench sight.
 oldpanes=[o for o in bpy.data.objects if o.name.startswith("MAKER_INSET_GLAZING_")]
 assert len(oldpanes)==2,("M16B expected two visual obstructions",len(oldpanes))
 for o in oldpanes:bpy.data.objects.remove(o,do_unlink=True)
 # Ensure the two opened service bays retain slim rail-like headers.
 cube("M16B_MAKER_VISIBLE_WORKSHOP_SIGN",(-10.6,-8,10.5),(.18,3.5,.55),copper)
 cube("M16B_MAKER_GALLERY_EDGE_MATERIAL",(-10.6,8.5,10.5),(.18,3.5,.55),copper)
 for key,eye,target in (
   ("maker_eye",(-28,-6,1.7),(-22,7,3.3)),
   ("research_eye",(-6.5,27,9.6),(-23,6,7)),
   ("resident_eye",(39,26.0,9.1),(8,24.0,7.6))):
  ob=bpy.data.objects["M15C_CAMERA_"+key]
  ob.location=eye
  ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
  ob.data.lens=28 if key!="research_eye" else 30
 assert not bpy.data.objects.get("MAKER_NORTH_THICK_WALL")
 assert not any(o.name.startswith("MAKER_INSET_GLAZING_") for o in bpy.data.objects)
 assert bpy.data.objects.get("M16_HOME_REAL_FLOOR")
 scene["M16B_CHANGE"]="MEASURED OCCLUSION CORRECTED, ART HOLD"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["FORMAL_G0_S1_G1_G2_G3"]="NOT_RUN"
 scene.cycles.samples=14
 OUT.mkdir(parents=True)
 blend=OUT/"M16B_EDITED_NATIVE_SCENE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for n in VIEWS:
  scene.camera=bpy.data.objects["M15C_CAMERA_"+n]
  p=OUT/("M16B_"+n+".png")
  scene.render.filepath=str(p)
  bpy.ops.render.render(write_still=True)
  assert p.stat().st_size>2048
  views[n]={"sha256":sha(p),"bytes":p.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M16B_SAVED_MESH_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"original_sha256":INPUT_SHA,"native_blend_sha256":sha(blend),
  "glb_sha256":sha(glb),"views":views,"art":"HOLD","adopted":0,
  "minecraft":"FORBIDDEN","formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "review_scope":"second true native edit of M16, not ART PASS",
  "actual_changed":"MAKER_NORTH_THICK_WALL deleted and replaced; 2 opaque maker panes removed"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
 print("M16B_SECOND_NATIVE_VISUAL_CORRECTION_COMPLETE",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M16B_PINNED_ORIGINAL",find_seed())
 else:run()
