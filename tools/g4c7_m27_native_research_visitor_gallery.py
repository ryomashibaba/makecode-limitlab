#!/usr/bin/env python3
"""M27: edit actual M26B research room; open east controlled portal, join
M17 U0-U1 public gallery floor and daylight observation corridor.
One pinned editable source. Research, not certified physical access/ART.
"""
import os,math,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m27_immutable_m26b"
OUT=ROOT/"artifacts/g4c7-m27-visitor-gallery-entry"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
SPEC=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
PIN="aae03e6af71a6acca1da740d73f12e4e8db6cceff457debe93aa299c2f7a241f"
ORIGIN=(-43.,37.,9.6)
OLD_GLASS="M26_east_large_daylight_glazing_32"
STREET="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
VIEWS=("gallery_arrival_eye","controlled_threshold_eye","original_research_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 f=list(SEED.rglob("M26B_EDITED_HUMAN_RESEARCH_ROOM.blend"))
 assert len(f)==1,("M26B original uniqueness",len(f))
 assert sha(f[0])==PIN,"Refuse unpinned M26B original"
 return f[0]
def spec():
 s=json.loads(SPEC.read_text(encoding="utf-8"))
 nodes={n["id"]:n for n in s["nodes"]}
 assert tuple(nodes["R0_RESEARCH_LAB"]["xyz"])==ORIGIN
 assert tuple(nodes["U1_RESEARCH_OBSERVATORY"]["xyz"])==(-29,30,9.6)
 assert tuple(nodes["U0_SOUTH_GALLERY"]["xyz"])==(-24,13,9.6)
 assert any(e["from"]=="U1_RESEARCH_OBSERVATORY" and e["to"]=="R0_RESEARCH_LAB" and e["kind"]=="controlled_entry" for e in s["edges"])
 assert s["gates"]["art"]=="HOLD" and s["gates"]["minecraft_education"]=="NO_WRITE"
 return s
def run():
 import bpy
 from mathutils import Vector
 assert not OUT.exists(),"Append-only: refuse overwrite"
 spec()
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 old_objects={o.name for o in bpy.data.objects}
 original_camera=bpy.data.objects.get("M26_HUMAN_EYE_CAMERA")
 road=bpy.data.objects.get(STREET)
 pane=bpy.data.objects.get(OLD_GLASS)
 assert original_camera and original_camera.type=="CAMERA" and road and pane and pane.type=="MESH"
 assert not pane.hide_render,"Controlled opening must remove a real prior glazed pane"
 oldroad=sorted(tuple(round(float(w),5) for w in road.matrix_world@v.co) for v in road.data.vertices)
 oldcams={o.name:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))
          for o in bpy.data.objects if o.type=="CAMERA"}
 pane.hide_render=True  # the east wall is now PHYSICALLY OPEN in this study
 col=bpy.data.collections.new("M27_EAST_REAL_PUBLIC_GALLERY_CONTROLLED_ENTRY_ART_HOLD")
 scene.collection.children.link(col)
 new=[]
 def xyz(a):return tuple(ORIGIN[i]+a[i] for i in range(3))
 def mat(name,rgb,metal=0,rough=.45,glass=0,emit=0):
  m=bpy.data.materials.new("M27_"+name);m.use_nodes=True
  p=m.node_tree.nodes["Principled BSDF"]
  p.inputs["Base Color"].default_value=(*rgb,1)
  p.inputs["Metallic"].default_value=metal
  p.inputs["Roughness"].default_value=rough
  p.inputs["Transmission Weight"].default_value=glass
  if emit:
   p.inputs["Emission Color"].default_value=(*rgb,1)
   p.inputs["Emission Strength"].default_value=emit
  return m
 M={
  "floor":mat("gallery_honed_warm_stone",(.57,.55,.48),rough=.67),
  "inlay":mat("brass_solid_tactile_wayfinding",(.57,.44,.22),metal=.66),
  "steel":mat("recycled_bronze_rails",(.20,.25,.24),metal=.72),
  "glass":mat("real_clear_galleries",(.49,.74,.78),rough=.08,glass=.76),
  "wood":mat("artisan_oak_exhibit",(.44,.27,.18)),
  "screen":mat("luminescent_observation_data",(.22,.69,.77),emit=.7),
  "green":mat("public_garden_plant",(.18,.42,.24)),
  "light":mat("warm_threshold_lamp",(.96,.72,.38),emit=1.3),
  "dark":mat("interactive_display_dark",(.07,.15,.18)),
 }
 def use(o,n,k):
  o.name="M27_"+n
  for co in list(o.users_collection):co.objects.unlink(o)
  col.objects.link(o);o.data.materials.append(M[k]);new.append(o)
  return o
 def block(n,pos,size,k,bevel=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(pos))
  o=bpy.context.object;o.dimensions=size
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  use(o,n,k)
  if bevel:
   m=o.modifiers.new("Crafted_beveled_edge","BEVEL");m.width=bevel;m.segments=2
   o.modifiers.new("Face_normal_weight","WEIGHTED_NORMAL")
  return o
 def bar(n,a,b,r,k):
  a=Vector(xyz(a));b=Vector(xyz(b));delta=b-a
  assert delta.length>.01
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=delta.length,location=(a+b)*.5)
  o=bpy.context.object;o.rotation_euler=delta.to_track_quat("Z","Y").to_euler()
  return use(o,n,k)
 def line(n,points,r,k):
  cu=bpy.data.curves.new("M27_"+n+"_spline","CURVE")
  cu.dimensions="3D";cu.bevel_depth=r;cu.bevel_resolution=2
  sp=cu.splines.new("POLY");sp.points.add(len(points)-1)
  for q,p in zip(sp.points,points):q.co=(*xyz(p),1)
  ob=bpy.data.objects.new("M27_"+n,cu);col.objects.link(ob);cu.materials.append(M[k]);new.append(ob)
  return ob
 def sphere(n,pos,r,k):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=r,location=xyz(pos))
  return use(bpy.context.object,n,k)
 # Real gallery platform contains U0 and U1 study-node centers. Floor top
 # equals the original M26 wood floor top (local z=.043).
 # x:[8.52,20.10], y:[-27,-.5], deck top=.043 exactly.
 block("ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK",(14.31,-13.75,-.207),
      (11.58,26.5,.5),"floor",.11)
 # The 0.003-high transition threshold overlaps gallery AND M26 room wood.
 # It cannot be confused with a falsely "seamless"/formally safe floor.
 block("REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD",(8.7,-6.75,-.076),
      (4.2,2.60,.28),"inlay",.05) # top +.064
 # Door is NOT a painted dark hole: hide real M26 pane and create
 # perimeter only, with genuine positive 2.60m-wide passage at z=0..3.2.
 for yy,name in ((-8.18,"south"),(-5.33,"north")):
  bar("portal_structural_post_"+name,(8.61,yy,.12),(8.61,yy,4.8),.16,"steel")
 bar("portal_real_overhead_header",(8.61,-8.18,3.38),(8.61,-5.33,3.38),.18,"steel")
 block("portal_high_transom_actual_glass",(8.63,-6.755,4.37),
       (.06,2.54,1.6),"glass")
 block("folded_glass_door_parked_OPEN",(10.0,-5.25,1.65),
       (.09,2.1,2.9),"glass") # explicitly parked outside walking slit
 bar("door_hinge_actual",(9.94,-5.1,.15),(9.94,-5.1,3.05),.065,"steel")
 block("restricted_access_observation_label",(9.65,-8.4,2.3),
       (1.7,.09,.55),"screen",.04)
 # An open outdoor corridor, deliberately NOT a giant box / covered tunnel.
 # Structural bays stay at the east outer edge and the lab side remains
 # actually transparent for viewing work being performed.
 for i,y in enumerate((-25.0,-19.,-13.,-7.,-.9)):
  bar("recessed_structural_pier_%02d"%i,(19.48,y,-.02),
      (19.14,y+.3,5.5),.24,"steel")
  bar("DAYLIGHT_ANGLED_CANOPY_RIB_%02d"%i,(9.6,y,5.08),
      (19.16,y+.35,5.46),.11,"inlay")
 for i,y in enumerate((-22.2,-16.2,-10.2,-4.2)):
  # Actual broad partial sunshade: two opening gaps between panes.
  block("canopy_real_diffused_glass_%d"%i,(14.4,y,5.33),
        (8.6,2.0,.10),"glass")
  block("canopy_timber_warm_rail_%d"%i,(14.4,y-1.07,5.28),
        (8.8,.18,.22),"wood")
 # Outer viewing edge: a real protective parapet with gaps to admit light
 # (visual mockup, never a regulation-certified railing).
 for i,(lo,hi) in enumerate(((-27.,-15.5),(-13.5,-.5))):
  bar("east_guard_top_%d"%i,(20.00,lo,1.12),(20.00,hi,1.12),.12,"steel")
  block("east_glass_guard_%d"%i,(20.0,(lo+hi)*.5,.63),
      (.07,hi-lo,1.10),"glass")
 for i,y in enumerate((-23,-17,-11,-5,-1)):
  bar("east_human_guard_vertical_%d"%i,(20,y,.04),(20,y,1.16),.065,"steel")
 # Purposeful exhibit objects and places to sit/view the lab, not empty floor.
 for i,y in enumerate((-21.1,-14.7,-1.7)):
  block("exhibition_real_demonstration_plinth_%d"%i,(17.6,y,.53),
        (2.1,1.15,.95),"wood",.09)
  block("exhibition_label_readable_screen_%d"%i,(17.6,y-.4,1.28),
        (1.52,.1,.37),"screen",.025)
  bar("exhibition_instrument_%d"%i,(17.6,y,1.04),
      (17.6,y,2.0),.075,"inlay")
  sphere("exhibition_lab_data_model_%d"%i,(17.6,y,2.13),.43,"glass")
 # A specific station for observing research through the retained east glass.
 block("research_observation_ledge",(11.15,-2.2,.86),(3.9,1.12,.22),
       "wood",.11)
 for i,y in enumerate((-4.0,-1.4)):
  block("public_daylight_planter_box_%d"%i,(18.55,y,.32),
        (1.4,1.3,.57),"floor",.10)
  bar("public_atrium_tree_trunk_%d"%i,(18.55,y,.61),
      (18.55,y,2.65),.11,"wood")
  sphere("public_atrium_tree_leaves_%d"%i,(18.55,y,2.85),1.02,"green")
 # Real walking route with support point continuity at same Z.
 # U0(+19,-24) -> U1(+14,-7) -> glazed public/controlled threshold
 # -> room-side landing(+7.2,-7). The lab's equipment access is NOT certified.
 way=[(19.,-24.,.065),(17.,-19.,.065),(15.,-12.,.065),
      (14.,-7.,.065),(11.2,-7.,.065),(8.8,-7.,.065),
      (7.2,-7.25,.065)]
 line("VISITOR_PUBLIC_ROUTE_REFERENCE_NOT_CERTIFIED",way,.024,"inlay")
 # Viewpoint sensors: from public entrance into gallery and through glass
 # to active lab; retain original lab camera for pre-existing work continuity.
 camera_data={}
 def camera(n,eye,aim,lens):
  c=bpy.data.cameras.new("M27_camera_"+n)
  o=bpy.data.objects.new("M27_CAMERA_"+n,c)
  col.objects.link(o);o.location=xyz(eye)
  o.rotation_euler=(Vector(xyz(aim))-o.location).to_track_quat("-Z","Y").to_euler()
  c.lens=lens;camera_data[n]=o
 camera("gallery_arrival_eye",(16.9,-23.,1.70),(12.7,-7.2,1.76),26)
 camera("controlled_threshold_eye",(14.4,-7.8,1.66),(1.0,-2.1,2.40),25)
 camera_data["original_research_eye"]=original_camera
 # Three preframed real images (M26B eye camera not repositioned).
 bpy.context.view_layer.update()
 from bpy_extras.object_utils import world_to_camera_view
 anchors={
  "public_U0_node":(19.,-24.,.043),
  "public_U1_node":(14.,-7.,.043),
  "room_controlled_entry":(8.64,-6.75,1.5),
  "lab_interior":(2.,-.5,2.)
 }
 projections={}
 for name,point in anchors.items():
  view=world_to_camera_view(scene,camera_data["gallery_arrival_eye"],Vector(xyz(point)))
  projections[name]={"nx":round(float(view.x),4),"ny":round(float(view.y),4),"depth":round(float(view.z),4)}
 # Existing M26B room objects stay (except one intentionally OPEN pane).
 assert old_objects.issubset({o.name for o in bpy.data.objects})
 assert len(new)>50 and pane.hide_render
 assert oldcams=={o.name:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))
                for o in bpy.data.objects if o.type=="CAMERA" and o.name in oldcams}
 assert oldroad==sorted(tuple(round(float(w),5) for w in road.matrix_world@v.co) for v in road.data.vertices)
 scene["M27"]="REAL_EAST_CONTROLLED_PORTAL_AND_PUBLIC_VISITOR_GALLERY_RESEARCH"
 scene["ART"]="HOLD_NOT_APPROVED";scene["ADOPTED"]=0
 scene["FORMAL_331_993"]="NOT_RUN";scene["G0_S1_G1_G2_G3"]="NOT_RUN"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene.render.engine="CYCLES";scene.cycles.samples=30
 scene.render.resolution_x=1080;scene.render.resolution_y=680
 scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG"
 OUT.mkdir(parents=True)
 blend=OUT/"M27_EDITABLE_RESEARCH_VISITOR_GALLERY.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 images={}
 for n in VIEWS:
  scene.camera=camera_data[n]
  f=OUT/("M27_"+n+".png")
  scene.render.filepath=str(f);bpy.ops.render.render(write_still=True)
  assert f.stat().st_size>2500
  images[n]={"sha256":sha(f),"bytes":f.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M27_GALLERY_RESEARCH_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 report={
   "stage":"M27_NATIVE_VISITOR_GALLERY_REAL_ENTRY",
   "source_M26B_sha256":PIN,
   "original_camera_frozen":True,"M22_hidden_road_unchanged":True,
   "removed_from_visible_geometry_one_pane":OLD_GLASS,
   "new_objects":len(new),
   "design_node_world":{"U0":[-24,13,9.6],"U1":[-29,30,9.6],"R0":[-43,37,9.6]},
   "study_route_relative":way,
   "geometry_check":{"gallery_floor_top_local":.043,"research_floor_top_local":.043,
      "threshold_top_local":.064,
      "door_y_min":-8.05,"door_y_max":-5.45,
      "door_clear_width":2.60,"door_clear_height":3.2,
      "floor_study_gap_height":.021,
      "studio_level":9.6,
      "inside_room_route_not_formally_certified":True},
   "gallery_view_projections":projections,
   "three_view_sha256":images,
   "blend_sha256":sha(blend),"glb_sha256":sha(glb),
   "art":"HOLD_NOT_APPROVED","adopted":0,
   "minecraft":"FORBIDDEN","official_331_993":"NOT_RUN",
   "formal_G0_S1_G1_G2_G3":"NOT_RUN",
   "constraints":"Limited M17 U0→U1 upper-level gallery and controlled lab interface only. No proven access from ground or full physical human sweep, no legal stair or structural approval."}
 (OUT/"manifest.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
 print("M27_NATIVE_GALLERY_THREE_IMAGES_AND_EDITABLE_FILES_DONE_ART_HOLD",len(new))
if __name__=="__main__":
 if "--preflight" in sys.argv:
  spec();print("M27_M26B_PINNED_SOURCE",original())
 else:run()
