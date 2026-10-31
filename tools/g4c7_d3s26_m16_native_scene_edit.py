#!/usr/bin/env python3
"""M16: directly edit saved M15C Blender original after observed 8-view critique."""
import os,json,hashlib,sys
from pathlib import Path
ROOT=Path("artifacts")
SEED=ROOT/"m16_immutable_m15c_seed"
OUT=ROOT/"g4c7-d3s26-m16-native-revision"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
OLD_SHA="4b17686607764fbfcddd54e32b132c2a8bea04f21a5c46ae0ff7525955bc9132"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def find_seed():
 found=list(SEED.rglob("M15C_EDITABLE_PUBLIC_INTERIOR.blend"))
 assert len(found)==1,("expected single original",found)
 assert sha(found[0])==OLD_SHA,"original M15C altered"
 return found[0]
def run():
 import bpy
 from mathutils import Vector
 src=find_seed()
 assert not OUT.exists(),"append-only safeguard"
 bpy.ops.wm.open_mainfile(filepath=str(src.resolve()))
 scene=bpy.context.scene
 expected=("MARKET_EAST_END_WALL","MAKER_BACK_THICK_WALL","RESEARCH_NORTH_WALL",
 "RESIDENTIAL_APPROACH_BACK_WALL","MAKER_PARTIAL_DAYLIGHT_ROOF")
 assert all(bpy.data.objects.get(n) for n in expected)
 assert all(bpy.data.objects.get("M15C_CAMERA_"+n) for n in VIEWS)
 count_before=len(bpy.data.objects)
 col=bpy.data.collections.new("M16_REAL_REVIEW_DRIVEN_NATIVE_REVISIONS")
 scene.collection.children.link(col)
 def mat(n,c,metal=0,trans=0):
  m=bpy.data.materials.new("M16_"+n);m.use_nodes=True
  p=m.node_tree.nodes.get("Principled BSDF")
  p.inputs["Base Color"].default_value=(*c,1);p.inputs["Roughness"].default_value=.38
  p.inputs["Metallic"].default_value=metal
  p.inputs["Transmission Weight"].default_value=trans
  return m
 M={"stone":mat("inhabited_light_mineral",(.59,.65,.60)),
 "bronze":mat("metal_reveals",(.45,.36,.24),.48),
 "glass":mat("daylight_clear_glazing",(.77,.86,.87),.05,.85),
 "wood":mat("human_touch_wood",(.44,.29,.17)),
 "plant":mat("private_garden",(.12,.32,.21)),
 "seat":mat("resident_upholstery",(.30,.41,.47))}
 def cube(n,loc,dims,kind):
  bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
  o=bpy.context.object;o.name=n;o.dimensions=dims
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for old in list(o.users_collection):old.objects.unlink(o)
  col.objects.link(o);o.data.materials.append(M[kind])
  return o
 def sheet(n,pts,kind,th=.10):
  data=bpy.data.meshes.new(n+"_mesh")
  data.from_pydata(pts,[],[tuple(range(len(pts)))]);data.update()
  o=bpy.data.objects.new(n,data);col.objects.link(o)
  data.materials.append(M[kind])
  if th:
   mod=o.modifiers.new("Physical_Thickness","SOLIDIFY");mod.thickness=th
  return o
 def remove(n):
  o=bpy.data.objects.get(n)
  assert o and o.type=="MESH",n
  bpy.data.objects.remove(o,do_unlink=True)
 # Worker's view was blocked by large solid maker wall: replace with real windows.
 remove("MAKER_BACK_THICK_WALL")
 for i,y in enumerate((-12,-2,8,20)):
  cube("M16_MAKER_DAYLIT_PIER_%d"%i,(-36,y,7.65),(1.1,1.45,15.3),"stone")
 cube("M16_MAKER_WINDOW_HEADER",(-36,4,14.8),(1.2,32,.9),"bronze")
 cube("M16_MAKER_REAR_SILL",(-36,4,1.1),(1.0,32,2.2),"stone")
 for i,(a,b) in enumerate(((-11.2,-2.8),(-1.2,7.2),(8.8,19.2))):
  sheet("M16_MAKER_TRUE_DAYLIGHT_BAY_%d"%i,
   [(-35.96,a,2.3),(-35.96,b,2.3),(-35.96,b,14.3),(-35.96,a,14.3)],"glass")
 # Market frontage should read as public, not a giant blank rectangular wall.
 remove("MARKET_EAST_END_WALL")
 for i,y in enumerate((-27,-13,0,15)):
  cube("M16_MARKET_PUBLIC_PIER_%d"%i,(38,y,5.7),(1.4,1.3,11.4),"stone")
 cube("M16_MARKET_CLERESTORY_BAND",(38,-6,10.7),(1.4,42,1.1),"bronze")
 cube("M16_MARKET_HUMAN_SILL",(38,-6,.85),(1.2,42,1.7),"stone")
 for i,(a,b) in enumerate(((-26,-13.8),(-12.2,-.8),(.8,14.2))):
  sheet("M16_MARKET_WINDOW_%d"%i,
   [(37.95,a,1.8),(37.95,b,1.8),(37.95,b,10.1),(37.95,a,10.1)],"glass")
 # Research upper public destination must have sky visibility.
 remove("RESEARCH_NORTH_WALL")
 for i,x in enumerate((-23,-10,3,15,23)):
  cube("M16_RESEARCH_NORTH_PIER_%d"%i,(x,37,13.0),(1.25,1.1,11.5),"stone")
 cube("M16_RESEARCH_SILL",(0,37,8.4),(46,1.1,2.1),"stone")
 cube("M16_RESEARCH_ROOFLINE",(0,37,18.5),(46,1.1,.95),"bronze")
 for i,(a,b) in enumerate(((-22,-10.7),(-9.3,2.3),(3.7,14.3),(15.7,22.3))):
  sheet("M16_RESEARCH_GLASS_LIGHTWELL_%d"%i,
   [(a,36.95,9.4),(b,36.95,9.4),(b,36.95,18),(a,36.95,18)],"glass")
 # Former single maker roof was a blank view-blocking slab.
 remove("MAKER_PARTIAL_DAYLIGHT_ROOF")
 sheet("M16_MAKER_SPLIT_ROOF_WEST",
  [(-37,-14,16),(-28,-14,16),(-25,17,19),(-37,20,18)],"stone",.48)
 sheet("M16_MAKER_SPLIT_ROOF_EAST",
  [(-16,-14,16.5),(-9,-14,17),(-7,13,21),(-14,15,20.1)],"stone",.48)
 sheet("M16_MAKER_REAL_SKYLIGHT",
  [(-26,-14,16.2),(-17,-14,16.6),(-15,14,20),(-25,16,19)],"glass",.08)
 # A true private room: saved walls, furniture, floor and portal, not a label.
 remove("RESIDENTIAL_APPROACH_BACK_WALL")
 cube("M16_HOME_ENTRY_LEFT",(31.5,22.3,10.7),(1.1,2.3,7),"stone")
 cube("M16_HOME_ENTRY_RIGHT",(31.5,29.8,10.7),(1.1,2.3,7),"stone")
 cube("M16_HOME_PORTAL_HEADER",(31.5,26.0,14.1),(1.1,5.9,.55),"bronze")
 cube("M16_HOME_REAL_FLOOR",(38.0,25.9,7.1),(13.6,14,.5),"wood")
 cube("M16_HOME_OCCUPIED_WORKDESK",(38.5,23,8.0),(3.4,1.9,1.15),"wood")
 cube("M16_HOME_SEATING",(41,29,7.85),(3.8,1.8,.9),"seat")
 cube("M16_HOME_LIVING_PLANTER",(43,21,7.85),(2.5,1.8,1.2),"plant")
 cube("M16_HOME_BACK_WALL_LOW",(44.7,25.8,9.5),(.8,13,5),"stone")
 sheet("M16_HOME_PANORAMIC_UPPER_WINDOW",
  [(44.2,20,10),(44.2,31,10),(44.2,31,14.5),(44.2,20,14.5)],"glass")
 # Same camera IDs, targeted corrections to unviewable research/resident eye heights.
 for name,eye,target in (
   ("research_eye",(-7,26,9.6),(-22,5,6.6)),
   ("resident_eye",(40,26.5,9.1),(14,14,7.5))):
  cam=bpy.data.objects["M15C_CAMERA_"+name]
  cam.location=eye
  cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
  cam.data.lens=27
 assert bpy.data.objects.get("M16_HOME_REAL_FLOOR")
 assert bpy.data.objects.get("M16_RESEARCH_GLASS_LIGHTWELL_0")
 assert len(bpy.data.objects)>count_before+20
 scene["M16"]="NATIVE_EDIT_NOT_NEW_CITY"
 scene["FORMAL_GATES"]="NOT_RUN"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene.cycles.samples=15
 OUT.mkdir(parents=True)
 blend=OUT/"M16_EDITED_M15C_NATIVE_SCENE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in VIEWS:
  scene.camera=bpy.data.objects["M15C_CAMERA_"+name]
  img=OUT/("M16_"+name+".png")
  scene.render.filepath=str(img)
  bpy.ops.render.render(write_still=True)
  assert img.stat().st_size>2000
  views[name]={"sha256":sha(img),"bytes":img.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for obj in bpy.data.objects:
  if obj.type=="MESH" and not obj.hide_render:obj.select_set(True)
 glb=OUT/"M16_M15C_GEOMETRY_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={
  "original_sha256":OLD_SHA,"native_blend_sha256":sha(blend),"glb_sha256":sha(glb),
  "views":views,"new_objects_min":20,
  "art":"HOLD","adopted":0,"minecraft":"FORBIDDEN",
  "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "review_scope":"targeted native M15C edit not city-scale ART acceptance"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
 print("M16_8_VIEWS_DIRECT_NATIVE_EDIT_DONE",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("SHA_MATCH",find_seed(),OLD_SHA)
 else:run()
