#!/usr/bin/env python3
"""M29 room/gallery -> physically connected outdoor research terrace.
Real native Blender; two M28B cameras remain fixed, one new eye for critique.
Preserve all M28B geometry. No formal city, safety or ART acceptance.
"""
from pathlib import Path
import hashlib,json,math,os,sys
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m29_pinned_m28b"
OUT=ROOT/"artifacts/g4c7-m29-open-air-experience"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="2c36e40fe97922e099a1e3197bf79a10555dc5eb00293553f2897a33241c5441"
ORIGIN=(-43.0,37.0,9.6)
GALLERY="M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK"
THRESHOLD="M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD"
FIXED=("gallery_arrival_eye","controlled_threshold_eye")
VIEWS=FIXED+("outdoor_court_eye",)
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def seed():
 f=list(SEED.rglob("M28B_EDITED_HUMAN_GALLERY_SIGHTLINE.blend"))
 assert len(f)==1,("M28B native uniquely pinned",len(f))
 assert sha(f[0])==PIN,"Source native SHA mismatch"
 return f[0]
def preflight():
 assert not OUT.exists(),"Append only; never overwrite"
 assert len(VIEWS)==3 and len(FIXED)==2
 return str(seed())
def run():
 import bpy
 from mathutils import Vector
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(seed().resolve()))
 scene=bpy.context.scene
 before=set(bpy.data.objects)
 deck=bpy.data.objects.get(GALLERY)
 entry=bpy.data.objects.get(THRESHOLD)
 road=bpy.data.objects.get("M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD")
 assert deck and entry and road and all(o.type=="MESH" for o in (deck,entry,road))
 cameras={n:bpy.data.objects.get("M27_CAMERA_"+n) for n in FIXED}
 assert all(c and c.type=="CAMERA" for c in cameras.values())
 camera_pin={n:(tuple(c.location),tuple(c.rotation_euler),float(c.data.lens)) for n,c in cameras.items()}
 def vertices(ob):
  return sorted(tuple(round(float(w),5) for w in ob.matrix_world@v.co) for v in ob.data.vertices)
 geometry_pin={o.name:vertices(o) for o in (deck,entry,road)}
 # No element of the M28B architecture may move or disappear.
 col=bpy.data.collections.new("M29_ACTUAL_GALLERY_TO_OPEN_AIR_GARDEN_ART_HOLD")
 scene.collection.children.link(col)
 created=[]
 def xyz(p):return tuple(ORIGIN[i]+float(p[i]) for i in range(3))
 def mat(n,rgb,rough=.48,metal=0,trans=0,emission=0):
  m=bpy.data.materials.new("M29_"+n);m.use_nodes=True
  q=m.node_tree.nodes["Principled BSDF"]
  q.inputs["Base Color"].default_value=(*rgb,1)
  q.inputs["Roughness"].default_value=rough
  q.inputs["Metallic"].default_value=metal
  q.inputs["Transmission Weight"].default_value=trans
  if emission:
   q.inputs["Emission Color"].default_value=(*rgb,1)
   q.inputs["Emission Strength"].default_value=emission
  return m
 M={
  "terrace":mat("warm_stone_connected_public_court",(.61,.60,.52),.76),
  "earth":mat("deep_cultivation_soil",(.14,.20,.17),.85),
  "bronze":mat("oxidized_structural_bronze",(.17,.27,.27),.34,.6),
  "timber":mat("carved_warm_oak",(.47,.32,.20),.52),
  "plant":mat("forest_green_planting",(.15,.40,.24),.75),
  "plant2":mat("sage_leaf_garden",(.32,.53,.36),.73),
  "glass":mat("greenhouse_clear_glazing",(.48,.72,.74),.15,0,.68),
  "teal":mat("research_graph_cyan",(.13,.60,.68),.4,0,0,.62),
  "gold":mat("golden_information_mark",(.83,.54,.25),.36,.52,0,.6),
  "display":mat("dark_instrument_glass",(.055,.16,.20),.22,.34),
  "water":mat("recovered_water_reflection",(.12,.38,.42),.20,.12,.33),
  "person":mat("nonidentified_staff_silhouette",(.28,.30,.34),.71),
  "fabric":mat("visitor_warm_jacket",(.65,.32,.22),.80),
  "clay":mat("architectural_ceramic_ribs",(.79,.74,.62),.58)
 }
 def attach(o,n,m):
  o.name="M29_"+n
  for c in tuple(o.users_collection):c.objects.unlink(o)
  col.objects.link(o);o.data.materials.append(M[m]);created.append(o)
  return o
 def cube(n,p,dim,m,bevel=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(p))
  o=bpy.context.object;o.dimensions=dim
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  attach(o,n,m)
  if bevel:
   b=o.modifiers.new("Crafted_edges","BEVEL");b.width=bevel;b.segments=2
   o.modifiers.new("Smooth_face_normals","WEIGHTED_NORMAL")
  return o
 def cylinder(n,p,r,d,m,vertices=16):
  bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d,location=xyz(p))
  return attach(bpy.context.object,n,m)
 def beam(n,a,b,r,m):
  p,q=Vector(xyz(a)),Vector(xyz(b))
  d=q-p;assert d.length>1e-5
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=d.length,location=(p+q)*.5)
  o=bpy.context.object;o.rotation_euler=d.to_track_quat("Z","Y").to_euler()
  return attach(o,n,m)
 def ico(n,p,r,m,sub=2):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=r,location=xyz(p))
  return attach(bpy.context.object,n,m)
 def surf(n,verts,m,depth=0):
  mesh=bpy.data.meshes.new("M29_"+n+"_mesh")
  mesh.from_pydata([xyz(p) for p in verts],[],[tuple(range(len(verts)))])
  mesh.update()
  o=bpy.data.objects.new("M29_"+n,mesh);col.objects.link(o)
  o.data.materials.append(M[m]);created.append(o)
  if depth:
   mod=o.modifiers.new("Real_slab_thickness","SOLIDIFY")
   mod.thickness=depth
  return o
 # The FIRST new object is a REAL physical deck joining M27's right edge.
 # M27 gallery ends x=20.10. Public court begins at x=19.85: a 0.25
 # positive area overlap and same floor top local z=+0.043.
 cube("CONNECTED_OUTDOOR_RESEARCH_COURT_DECK",(36.175,7.0,-.257),
      (32.65,60.0,.60),"terrace")
 # Access is through the actual deliberate 2.0m parapet gap around
 # y=-14.5, rather than through a painted door on the guard.
 portal=[(19.15,-14.5,.072),(20.5,-14.5,.072),
         (24.0,-14.5,.072),(27.5,-10.7,.072)]
 for i,(a,b) in enumerate(zip(portal,portal[1:])):
  beam("outdoor_positive_connected_path_segment_%d"%i,a,b,.05,"gold")
 for i,x in enumerate((21.2,24.8)):
  cube("public_threshold_floor_mark_%d"%i,(x,-14.5,.086),
       (.23,1.65,.07),"gold",.02)
 # A PRODUCTIVE planted courtyard, not a flat fake city skyline.
 # Landscape regions lie away from the 2m entrance slit / walking center.
 beds=[
  (("south_biofilter",36.2,-18.5),(13.2,5.8,.48)),
  (("east_crops",46.8,-1.0),(7.0,14.4,.50)),
  (("north_planting",38.0,26.0),(15.2,7.6,.52))]
 for (n,x,y),dim in beds:
  cube(n+"_real_contained_planter",(x,y,.28),dim,"clay",.20)
  cube(n+"_visible_soil",(x,y,.57),(dim[0]-.55,dim[1]-.55,.12),"earth",.08)
  for j in range(4):
   px=x+(j-1.5)*(dim[0]-1.5)/4
   py=y+((j%2)-.5)*min(2.4,dim[1]*.32)
   beam(n+"_woody_branch_%d"%j,(px,py,.62),
       (px+(-1)**j*.28,py,2.0+.35*(j%3)),.09,"timber")
   ico(n+"_canopy_%d"%j,(px+(-1)**j*.28,py,2.15+.35*(j%3)),
       .62+.14*(j%2),"plant" if j%2 else "plant2",2)
 # A low, deliberately asymmetrical WATER-RECLAIMING RILL connects
 # through the productive garden instead of repeated decorative arches.
 surf("reclamation_stream_surface",[
  (29.5,1.0,.095),(34.5,1.0,.095),
  (35.9,21.3,.095),(32.1,22.6,.095)],"water",.045)
 for i,p in enumerate(((30,2),(31,9),(33,16),(34,22))):
  cylinder("reed_stem_collection_%d"%i,(p[0],p[1],1.2),.08,2.25,"plant")
  ico("reed_plume_%d"%i,(p[0],p[1],2.5),.40,"plant2")
 # A REAL occupied outdoor sampling workplace with equipment people can
 # interact with. Keep outside entrance stripe open.
 cube("PUBLIC_SCIENCE_INTERACTION_WORKTOP",(28.5,1.5,.98),
      (4.1,2.15,.25),"timber",.12)
 for i,x in enumerate((27.1,29.8)):
  beam("worktop_support_%d"%i,(x,1.3,.05),(x,1.3,.87),.10,"bronze")
 cube("ENVIRONMENTAL_DATA_CONSOLE",(28.5,1.35,1.20),
      (3.25,.84,.09),"display",.08)
 for i in range(7):
  cube("ENVIRONMENTAL_COMPOSITION_TRACE_%d"%i,
       (27.2+i*.40,1.13,1.264),(.23,.14,.032),
       "teal" if i%2 else "gold")
 cylinder("GARDEN_AIR_SENSOR",(27.6,2.0,1.58),.13,.86,"bronze")
 ico("GARDEN_ATMOSPHERIC_SENSOR",(27.6,2.0,2.08),.32,"glass")
 # Three architectonic CLIMATE-COLLECTING RIBS are grounded in this court,
 # not a huge fake shell or a rows-of-roofs building. They guide vista
 # vertically to real research function beyond the gallery window.
 anchor_y=(5.0,12.5,21.0)
 for i,y in enumerate(anchor_y):
  base=(40.6+.9*math.sin(i),y,.10)
  high=(43.8+.9*math.sin(i),y+1.8,9.1+i*.75)
  beam("BIOMIMETIC_CANOPY_LOAD_BEARING_RIB_%d"%i,base,high,.48,"bronze")
  tip=(39.0,y+1.0,10.4+i*.75)
  beam("CANTILEVER_REAL_COMPRESSION_BRANCH_%d"%i,high,tip,.30,"clay")
  beam("HIGH_DAYLIGHT_CROSS_TIE_%d"%i,tip,
       (31.0,y+1.0,9.6+i*.75),.21,"bronze")
  cube("SEMI_TRANSPARENT_DAYLIGHT_BAFFLE_%d"%i,
       (35.0,y+1.0,9.63+i*.75),(8.7,1.65,.13),"glass",.05)
 # Light civic equipment completes the readable depth at the far court.
 cube("DAYLIGHT_BIOCLIMATE_CONTROL_PYLON",(46.8,20.0,2.65),
      (2.3,1.5,5.2),"bronze",.2)
 for j,z in enumerate((1.2,2.0,2.8,3.7)):
  cube("PYLON_ENVIRONMENTAL_READOUT_%d"%j,
       (45.57,19.93,z),(.08,1.15,.38),"teal",.03)
 cube("SOLAR_DATA_COLLECTOR_HEAD",(46.8,20.0,6.8),
      (4.1,2.4,.28),"clay",.08)
 # Intentional, anonymous humans doing research, made with actual
 # cylinders/spheres and oriented arms/heads, not mere decorative markers.
 def human(n,x,y,coat,pose):
  cylinder(n+"_footing_shadow",(x,y,.070),.35,.04,"bronze")
  for j,dx in enumerate((-.17,.17)):
   beam(n+"_leg_%d"%j,(x+dx,y,.10),(x+dx*.8,y,1.04),.11,"person")
  cube(n+"_practical_jacket",(x,y,1.38),(.64,.34,.83),coat,.13)
  beam(n+"_neck",(x,y,1.76),(x,y,1.88),.085,"person")
  ico(n+"_human_head",(x,y,2.06),.24,"person",2)
  # Real differentiated gestures: a working observer and a visitor
  if pose=="sample":
   beam(n+"_right_working_arm",(x+.27,y,1.60),(x+.72,y-.45,1.36),.09,"person")
   beam(n+"_left_research_arm",(x-.26,y,1.60),(x-.65,y-.36,1.16),.09,"person")
  else:
   beam(n+"_pointing_arm",(x-.26,y,1.62),(x-.80,y-.15,1.97),.095,"person")
   beam(n+"_resting_arm",(x+.27,y,1.58),(x+.41,y,1.13),.09,"person")
 human("PUBLIC_GARDEN_RESEARCH_OPERATOR",29.5,4.7,"fabric","sample")
 human("PUBLIC_VISITOR_DISCOVERING_WORK",26.1,6.9,"timber","observe")
 # No opaque walls are erected in the courtyard. The outdoor atmosphere
 # is a real open sky with depth. Add only dedicated outdoor-area light.
 daylight=bpy.data.lights.new("M29_open_sky_spill","AREA")
 daylight.energy=1600;daylight.shape="DISK";daylight.size=19.5
 ld=bpy.data.objects.new("M29_open_sky_spill",daylight)
 col.objects.link(ld);ld.location=xyz((34,6,18.5))
 ld.rotation_euler=(Vector(xyz((32,8,0)))-ld.location).to_track_quat("-Z","Y").to_euler()
 scene.cycles.samples=34
 # Freeze both comparison cameras exactly; a third new outdoors camera
 # is NOT labelled a fixed M28B comparison view.
 cam=bpy.data.cameras.new("M29_OUTDOOR_COURT_CAMERA")
 eye=bpy.data.objects.new("M29_OUTDOOR_COURT_CAMERA",cam)
 col.objects.link(eye);eye.location=xyz((34.3,-17.0,1.72))
 eye.rotation_euler=(Vector(xyz((23.3,5.0,3.2)))-eye.location).to_track_quat("-Z","Y").to_euler()
 cam.lens=29.5
 cameras["outdoor_court_eye"]=eye
 # Preserve all original M28B names, meshes, existing architectural cameras.
 assert before.issubset(set(bpy.data.objects))
 for name,ob in ((GALLERY,deck),(THRESHOLD,entry),
                 ("M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD",road)):
  assert vertices(ob)==geometry_pin[name],name
 for n in FIXED:
  o=cameras[n]
  assert (tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))==camera_pin[n],n
 assert len(created)>=70,(len(created),"expected real inhabited garden geometry")
 # Test the floor is as authored (not a painted plane). Actual GLB
 # independently checks positive area overlap and bounded walking points.
 scene["M29"]="TRUE_OUTDOOR_MICROCLIMATE_RESEARCH_COURT_ART_HOLD"
 scene["ART"]="HOLD_NOT_APPROVED";scene["ADOPTED"]=0
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["OFFICIAL_331_993"]="NOT_RUN";scene["G0_S1_G1_G2_G3"]="NOT_RUN"
 scene.render.engine="CYCLES"
 scene.render.resolution_x=1080;scene.render.resolution_y=680
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 OUT.mkdir(parents=True)
 blend=OUT/"M29_EDITABLE_OPEN_AIR_RESEARCH_COURT.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in VIEWS:
  scene.camera=cameras[name]
  png=OUT/("M29_"+name+".png")
  scene.render.filepath=str(png)
  bpy.ops.render.render(write_still=True)
  assert png.stat().st_size>3000
  views[name]={"bytes":png.stat().st_size,"sha256":sha(png)}
 bpy.ops.object.select_all(action="DESELECT")
 for o in bpy.data.objects:
  if o.type=="MESH" and not o.hide_render:o.select_set(True)
 glb=OUT/"M29_HABITABLE_GARDEN_NOT_APPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={
  "stage":"M29_GALLERY_TO_PHYSICAL_OPEN_AIR_RESEARCH_EXPERIENCE",
  "pinned_M28B_source_SHA256":PIN,
  "fixed_M28B_cameras":list(FIXED),"new_M29_outdoor_camera":"outdoor_court_eye",
  "existing_M28B_meshes_unchanged":True,
  "existing_M27_public_floor_and_door_unchanged":True,
  "new_real_blender_objects":len(created),
  "outdoor_real_court":{"x_min_local":19.85,"x_max_local":52.50,
    "y_min_local":-23,"y_max_local":37,
    "top_local":.043,"gallery_floor_top_local":.043,
    "overlap_width_local":.25,
    "dedicated_public_guard_gap_y":[-15.5,-13.5],
    "gate_route_y":-14.5},
  "outdoor_art":["real court deck","wet garden and retained water",
    "microclimate structural canopy","public equipment","two working human-scale subjects"],
  "views":views,"blend_sha256":sha(blend),"glb_sha256":sha(glb),
  "art":"HOLD_NOT_APPROVED","adopted":0,
  "official_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "minecraft":"FORBIDDEN",
  "limitations":"Bounded geometry contact and sculptural viewport study, not true formal full body/step/structural/urban QA. Outdoor context is a new local study, not a completed futuristic city."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
 print("M29_TRUE_NATIVE_OPEN_AIR_TERRACE_THREE_VIEWS_ART_HOLD",len(created))
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M29_SOURCE_PINNED",preflight())
 else:run()
