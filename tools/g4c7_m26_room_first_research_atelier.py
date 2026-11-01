#!/usr/bin/env python3
"""M26 first-room-first native 3D art gate.
One occupied research room with visible human activity; no giant exterior.
Never promotes aesthetics or foot/structural safety from a render.
"""
from pathlib import Path
import os,math,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m26_immutable_m22"
SPEC=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
OUT=ROOT/"artifacts/g4c7-m26-inhabited-research-room"/("run_"+os.environ.get("GITHUB_SHA","local")[:12])
PIN="22473a0d17fb59470049fb22b508dcfc294316185d38878b5563e213246af9df"
STREET="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
ORIGIN=(-43.0,37.0,9.6)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pinned():
 candidates=list(SEED.rglob("M22_EDITABLE_REVISED_PUBLIC_ROUTE.blend"))
 assert len(candidates)==1,("expected a unique immutable M22",len(candidates))
 assert sha(candidates[0])==PIN,"original SHA256 changed"
 return candidates[0]
def preflight():
 d=json.loads(SPEC.read_text(encoding="utf-8"))
 assert d["schema"]=="g4c7.m17.design_reference.v1"
 assert len(d["nodes"])==len(d["edges"])==18
 lab=next(x for x in d["nodes"] if x["id"]=="R0_RESEARCH_LAB")
 assert tuple(lab["xyz"])==ORIGIN
 assert d["gates"]["art"]=="HOLD" and d["gates"]["minecraft_education"]=="NO_WRITE"
 assert not OUT.exists(),"No overwrites of earlier research runs"
 return {"source":str(pinned()),"room_origin":ORIGIN,"program":"Research workshop plus quiet habitat nook",
 "candidate_gate":"ONE HUMAN-EYE FRAME ONLY, FORMAL SAFETY NOT RUN"}
def make():
 import bpy
 from mathutils import Vector
 from bpy_extras.object_utils import world_to_camera_view
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(pinned().resolve()))
 scene=bpy.context.scene
 road=bpy.data.objects.get(STREET)
 assert road and road.type=="MESH"
 oldroad=sorted(tuple(round(float(w),5) for w in road.matrix_world@v.co)
                for v in road.data.vertices)
 # Do not import rejected M23-M25. Original M22 stays serialized but is
 # hidden from this single room-only study's artistic render.
 for o in bpy.data.objects:o.hide_render=True
 col=bpy.data.collections.new("M26_ROOM_FIRST_VAULTED_RESEARCH_ATELIER_ART_HOLD")
 scene.collection.children.link(col)
 built=[];regions={}
 def world(v):return (float(v[0])+ORIGIN[0],float(v[1])+ORIGIN[1],float(v[2])+ORIGIN[2])
 def material(n,rgb,metal=0.0,rough=.42,trans=0,emit=0):
  m=bpy.data.materials.new("M26_"+n)
  m.use_nodes=True
  b=m.node_tree.nodes.get("Principled BSDF")
  b.inputs["Base Color"].default_value=(*rgb,1)
  b.inputs["Metallic"].default_value=metal
  b.inputs["Roughness"].default_value=rough
  b.inputs["Transmission Weight"].default_value=trans
  if emit:
   b.inputs["Emission Color"].default_value=(*rgb,1)
   b.inputs["Emission Strength"].default_value=emit
  return m
 M={
  "warm_ash":material("light_ash_oak",(.59,.42,.27),rough=.52),
  "stone":material("honed_cream_stone",(.64,.64,.58),rough=.65),
  "dark":material("dark_oxidized_bronze",(.13,.19,.21),metal=.7),
  "shell":material("soft_ceramic_ribbing",(.73,.72,.66),rough=.43),
  "copper":material("warm_copper",(.60,.31,.14),metal=.66),
  "glass":material("light_refractive_glass",(.55,.77,.79),trans=.72,rough=.08),
  "screen":material("soft_cyan_analytical_display",(.23,.73,.83),emit=1.45),
  "brass":material("satin_brass",(.67,.49,.25),metal=.65),
  "fabric":material("muted_honey_saffron_textile",(.66,.40,.22),rough=.80),
  "leaf":material("garden_evergreen",(.12,.31,.19),rough=.72),
  "leaf2":material("sage_accent",(.27,.48,.27),rough=.75),
  "light":material("diffused_warm_lamp",(.98,.72,.41),emit=3),
  "slate":material("dark_lab_tabletop",(.19,.25,.25),rough=.33),
  "sky":material("daylight_backdrop",(.48,.68,.72),rough=.8)
 }
 def take(ob,name,mat):
  ob.name="M26_"+name
  for co in list(ob.users_collection):co.objects.unlink(ob)
  col.objects.link(ob)
  if mat:ob.data.materials.append(M[mat])
  built.append(ob);return ob
 def cube(n,pos,dims,mat,bevel=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=world(pos))
  ob=bpy.context.object
  ob.dimensions=dims
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  take(ob,n,mat)
  if bevel:
   mod=ob.modifiers.new("Rounded_human_handmade_edges","BEVEL")
   mod.width=bevel;mod.segments=3
   ob.modifiers.new("weighted_normals","WEIGHTED_NORMAL")
  return ob
 def cylinder(n,center,radius,depth,mat,verts=20):
  bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=world(center))
  return take(bpy.context.object,n,mat)
 def link(n,a,b,r,mat):
  a,b=Vector(world(a)),Vector(world(b));delta=b-a
  assert delta.length>1e-5
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=delta.length,location=(a+b)/2)
  ob=bpy.context.object
  ob.rotation_euler=delta.to_track_quat("Z","Y").to_euler()
  return take(ob,n,mat)
 def polygon(n,points,faces,mat,solidify=0):
  mesh=bpy.data.meshes.new("M26_"+n+"_mesh")
  mesh.from_pydata([world(q) for q in points],[],faces);mesh.update()
  obj=bpy.data.objects.new("M26_"+n,mesh);col.objects.link(obj);obj.data.materials.append(M[mat]);built.append(obj)
  if solidify:
   m=obj.modifiers.new("Real_surface_thickness","SOLIDIFY");m.thickness=solidify
  return obj
 def curve_tube(n,points,r,mat):
  c=bpy.data.curves.new("M26_"+n+"_curve","CURVE");c.dimensions="3D"
  c.resolution_u=18;c.bevel_depth=r;c.bevel_resolution=3
  spline=c.splines.new("POLY");spline.points.add(len(points)-1)
  for p,q in zip(spline.points,points):p.co=(*world(q),1)
  o=bpy.data.objects.new("M26_"+n,c);col.objects.link(o);c.materials.append(M[mat])
  built.append(o);return o
 def ring(n,center,major,minor,mat,rotation=(0,0,0)):
  bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=8,
    location=world(center),rotation=rotation,major_radius=major,minor_radius=minor)
  return take(bpy.context.object,n,mat)
 def loft_arch(x):return 7.9-.046*x*x
 # FIRST define one usable real room with a vaulted clear-height envelope,
 # then place the contents. This is NOT an extra external macro shell.
 cube("real_foundation_slab",(0,0,-.32),(17.5,19.0,.65),"stone",.1)
 for i in range(21):
  x=-8.2+i*.82
  cube("oak_floor_interior_plank_%02d"%i,(x,0,.018),(.806,18.75,.05),"warm_ash")
 # Left solid wall and sculpted inset windows that admit daylight.
 for ylo,yhi in ((-9.2,-4.2),(-2.1,2.1),(4.7,9.3)):
  cube("west_research_wall_%02d"%int((ylo+10)*10),(-8.68,(ylo+yhi)/2,2.53),
      (.35,yhi-ylo,5.05),"shell",.05)
 for yy in (-3.2,3.3):
  cube("west_lightwell_window_frame_%d"%int(yy*10),(-8.69,yy,4.35),(.24,2.0,2.85),"dark",.09)
  cube("west_lightwell_glazing_%d"%int(yy*10),(-8.65,yy,4.35),(.035,1.65,2.42),"glass")
 # Right wall deliberately opalescent glass between slender masonry piers,
 # so the room reads as inhabitable light rather than a monolithic curtain.
 for y in (-9.0,-4.5,0,4.5,9.0):
  link("east_stone_mullion_%d"%int((y+10)*10),(8.6,y,.0),(8.6,y,4.9),.21,"dark")
 for y in (-6.75,-2.25,2.25,6.75):
  cube("east_large_daylight_glazing_%d"%int((y+10)*10),(8.64,y,2.8),(.07,4.3,4.6),"glass")
 # The back wall is OPEN at the central panoramic garden frame (no fake opaque backdrop).
 for x in (-7.1,7.1):
  cube("deep_garden_window_side_%d"%int((x+10)*10),(x,9.35,3.05),(2.7,.55,6.1),"shell",.08)
 cube("garden_window_sill",(0,9.32,.75),(12.5,.45,1.5),"stone",.1)
 cube("garden_window_header",(0,9.32,7.05),(12.7,.60,1.15),"shell",.09)
 for x in (-4.1,0,4.1):
  link("garden_window_mullion_%d"%int((x+5)*10),(x,9.35,1.4),(x,9.35,6.45),.12,"dark")
 # Continuous vaulted ceiling in small panels; central carved skylight actual
 # missing faces, not black texture. Camera near front sees the sculpture.
 xs=[-8.6+i*.43 for i in range(41)]
 ys=[-9.35+i*.55 for i in range(35)]
 roofpoints=[(x,y,loft_arch(x)+.018*math.sin(y*.8)) for y in ys for x in xs]
 roof_faces=[]
 for iy in range(len(ys)-1):
  for ix in range(len(xs)-1):
   x=(xs[ix]+xs[ix+1])/2;y=(ys[iy]+ys[iy+1])/2
   if abs(x)<1.1 and -1<y<5.7:continue
   roof_faces.append((iy*len(xs)+ix,iy*len(xs)+ix+1,
       (iy+1)*len(xs)+ix+1,(iy+1)*len(xs)+ix))
 polygon("single_vaulted_occupiable_shell",roofpoints,roof_faces,"shell",.23)
 for i,y in enumerate((-8.9,-3.6,2.3,8.2)):
  curve_tube("vault_structural_arch_rib_%d"%i,
    [(x,y,loft_arch(x)-.12) for x in xs[::2]],.14,"copper")
 # Skylight translucent louvers that cast actual light down to workspaces.
 for j,y in enumerate((-.7,.5,1.7,2.9,4.1,5.3)):
  link("skylight_daylight_tension_louver_%d"%j,(-1.17,y,loft_arch(-1.17)),
       (1.17,y,loft_arch(1.17)),.065,"brass")
 # Room's program: real science workspace centered on a visible suspended
 # microsatellite prototype and surrounding test benches.
 cube("central_low_experiment_plinth",(-.05,2.1,.60),(5.8,4.1,1.0),"dark",.32)
 cube("central_experiment_plinth_inlay",(-.05,2.1,1.13),(4.95,3.1,.08),"brass",.06)
 cylinder("microsatellite_core",(0,2.15,3.0),.90,1.25,"copper",24)
 cylinder("microsatellite_antenna",(0,2.15,4.05),.12,1.0,"brass",18)
 for j,angle in enumerate((.35,-.57)):
  ring("orbit_alignment_research_ring_%d"%j,(0,2.15,3.0),2.10,.045,"brass",(angle,.32,0))
 for side in (-1,1):
  cube("satellite_blue_solar_wing_%s"%("l" if side<0 else "r"),(side*2.05,2.15,3.0),
    (2.6,.13,1.0),"screen",.025)
  for j in range(3):
   link("solar_wing_rib_%s_%d"%(side,j),(side*(.95+j*.58),2.06,2.53),
       (side*(.95+j*.58),2.06,3.47),.025,"dark")
 # Human operational foreground lab with screens, actual keyboard/seat groups.
 cube("research_primary_studio_desk",(-4.3,-1.7,.93),(4.4,2.0,.18),"slate",.10)
 for x in (-5.9,-3.1):
  cylinder("research_primary_desk_leg_%d"%int(x*10),(x,-1.7,.47),.09,.91,"dark")
 cube("interactive_instrument_display",(-4.65,-1.44,1.68),(2.7,.17,1.35),"screen",.07)
 cube("instrument_display_back",(-4.65,-1.08,1.70),(2.95,.23,1.55),"dark",.07)
 for i,x in enumerate((-5.7,-5.25,-4.8,-4.35,-3.9)):
  cube("scientist_instrument_control_%d"%i,(x,-1.8,1.05),(.19,.47,.14),"brass",.04)
 cylinder("research_operator_chair",(-4.1,-4.03,.61),.65,.19,"fabric")
 cylinder("research_operator_chair_foot",(-4.1,-4.03,.26),.09,.49,"dark")
 cube("research_operator_chair_back",(-4.1,-4.56,1.25),(1.1,.21,1.3),"fabric",.12)
 # Second active wet lab east with visible equipment bottles, optic and panels.
 cube("wetlab_real_worktop",(5.0,2.4,.94),(4.7,2.15,.18),"warm_ash",.12)
 for i,x in enumerate((3.5,4.45,5.35,6.25)):
  cylinder("sample_vial_%d"%i,(x,2.55,1.38),.17,.56,"glass",14)
  cylinder("sample_bottle_lid_%d"%i,(x,2.55,1.73),.19,.12,"brass",12)
 cube("research_optic_imager",(5.65,1.8,1.7),(1.35,.9,1.2),"dark",.14)
 ring("optical_aperture",(5.65,1.12,1.73),.42,.08,"brass",(math.pi/2,0,0))
 # A separate quiet living zone within research space.
 cube("reading_terrace_rug",(4.5,-5.6,.07),(5.5,3.2,.06),"fabric",.14)
 cube("habitable_lounge_seat",(4.8,-6.0,.46),(3.15,1.25,.83),"fabric",.27)
 cube("habitable_lounge_cushion",(4.8,-6.0,.93),(2.75,1.12,.22),"fabric",.22)
 cube("habitable_lounge_back",(4.8,-6.60,1.16),(3.2,.40,1.35),"fabric",.18)
 cylinder("reading_side_table",(2.35,-6.35,.54),.49,1.0,"warm_ash")
 # Planter plus garden outside REAL panoramic rear opening.
 cube("interior_planting_trough",(-6.95,6.80,.43),(.87,3.7,.77),"stone",.14)
 for j,y in enumerate((5.8,6.9,7.95)):
  link("interior_tree_stem_%d"%j,(-6.95,y,.80),(-6.95,y,2.75),.095,"dark")
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.65,location=world((-6.95,y,2.75)))
  take(bpy.context.object,"interior_fern_canopy_%d"%j,"leaf")
 # Outdoor garden visibly carries through window into the city beyond.
 cube("botanical_atrium_visible_floor",(0,13.1,-.39),(16.8,7,.30),"stone")
 for j,(x,y) in enumerate(((-4,12.5),(-.3,13.3),(4.3,14.2))):
  link("outdoor_stem_%d"%j,(x,y,-.1),(x,y,3.1+j*.55),.16,"dark")
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1.6+j*.18,
      location=world((x,y,3.15+j*.55)))
  take(bpy.context.object,"outdoor_sapling_%d"%j,"leaf2")
 # Handcrafted hanging task lights with actual lights at eye-scaled positions.
 for j,(x,y,z) in enumerate(((-5,-.65,5.8),(5.2,1.3,5.7),(0,2.15,6.3))):
  cylinder("pendant_luminous_diffuser_%d"%j,(x,y,z),.45,.13,"light")
  link("pendant_cable_%d"%j,(x,y,z+.1),(x,y,loft_arch(x)-.1),.03,"dark")
  l=bpy.data.lights.new("M26_warm_task_lamp_%d"%j,"AREA")
  l.energy=600 if j==2 else 420;l.shape="DISK";l.size=5.2
  o=bpy.data.objects.new("M26_warm_task_lamp_%d"%j,l)
  col.objects.link(o);o.location=world((x,y,z+.18))
  o.rotation_euler=(math.pi,0,0)
 # Soft daytime exterior key without a false sky backdrop wall.
 s=bpy.data.lights.new("M26_room_sun","SUN")
 s.energy=1.65;s.angle=math.radians(9)
 sun=bpy.data.objects.new("M26_room_sun",s)
 col.objects.link(sun);sun.rotation_euler=(.56,-.32,-.58)
 area=bpy.data.lights.new("M26_wide_window_daylight","AREA")
 area.energy=1600;area.shape="RECTANGLE";area.size=9.5;area.size_y=7.1
 ao=bpy.data.objects.new("M26_wide_window_daylight",area);col.objects.link(ao)
 ao.location=world((0,12.0,5.1))
 ao.rotation_euler=(math.radians(78),0,0)
 w=bpy.data.worlds.new("M26_daylit_atrium_world")
 w.use_nodes=True;w.node_tree.nodes["Background"].inputs["Color"].default_value=(.64,.72,.77,1)
 w.node_tree.nodes["Background"].inputs["Strength"].default_value=.75
 scene.world=w
 # Framing must show lab work, central apparatus, occupied lounge and
 # daylight at the same time; no hidden-eye cam inside solid geometry.
 camera_data=bpy.data.cameras.new("M26_human_room_camera")
 camera=bpy.data.objects.new("M26_HUMAN_EYE_CAMERA",camera_data)
 col.objects.link(camera)
 camera.location=world((.8,-10.7,1.78))
 aim=Vector(world((0,2.1,2.45)))
 camera.rotation_euler=(aim-camera.location).to_track_quat("-Z","Y").to_euler()
 camera_data.lens=23.5;scene.camera=camera
 scene.render.engine="CYCLES";scene.cycles.samples=22
 scene.render.resolution_x=1200;scene.render.resolution_y=760
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 scene.render.film_transparent=False
 # Independent screen-space framing preflight, not occlusion guarantee.
 anchors={
  "central_real_satellite":(0,2.15,3.0),
  "left_occupied_workstation":(-4.65,-1.4,1.7),
  "right_real_wetlab":(5,2.4,1.1),
  "human_lounge":(4.8,-6,1.0),
  "outdoor_atrium":(0,13.1,2.7)
 }
 frame={}
 # bpy camera transform is lazy: force dependency-graph update before
 # world_to_camera_view to prevent stale view matrices and false negatives.
 bpy.context.view_layer.update()
 for n,p in anchors.items():
  q=world_to_camera_view(scene,camera,Vector(world(p)))
  frame[n]={"nx":round(float(q.x),4),"ny":round(float(q.y),4),"depth":round(float(q.z),4)}
  assert -0.15<q.x<1.15 and -.15<q.y<1.15 and q.z>0,(n,frame[n])
 assert len(built)>85,(len(built),"expected visible real room components")
 assert sorted(tuple(round(float(w),5) for w in road.matrix_world@v.co) for v in road.data.vertices)==oldroad
 scene["M26_ART"]="HOLD_NOT_APPROVED"
 scene["M26_SOURCE"]="M22_ROAD_IMMUTABLE"
 scene["M26_ACCESS"]="NOT_CERTIFIED"
 scene["M26_OFFICIAL_331_993"]="NOT_RUN"
 scene["M26_MINECRAFT_EDUCATION_WRITE"]=0
 OUT.mkdir(parents=True)
 blend=OUT/"M26_EDITABLE_ROOM_FIRST_RESEARCH_ATELIER.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 png=OUT/"M26_HUMAN_EYE_ART_GATE.png"
 scene.render.filepath=str(png)
 bpy.ops.render.render(write_still=True)
 assert png.stat().st_size>4000
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M26_INHABITED_ROOM_ART_HOLD.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"stage":"M26_ROOM_FIRST_ONE_FRAME_ART_GATE",
  "room_origin":ORIGIN,"pinned_source_sha256":PIN,
  "new_mesh_creatives":len(built),"real_room_components":len(built),
  "program":["human research bench","satellite optics demonstration","wet lab","living nook","daylight garden"],
  "image_anchor_screen_coordinates":frame,
  "one_actual_human_eye_png_sha256":sha(png),
  "source_road_unchanged":True,
  "blend_sha256":sha(blend),"glb_sha256":sha(glb),
  "art":"HOLD_NOT_APPROVED","adopted":0,
  "official_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "minecraft":"FORBIDDEN",
  "limitations":"Artwork, not validated inhabited space or public access. No formal safety/MakeCode build."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print("M26_ONE_HUMAN_EYE_TRUE_BLENDER_FRAME_COMPLETE_ART_HOLD",len(built))
if __name__=="__main__":
 if "--preflight" in sys.argv:print(json.dumps(preflight(),ensure_ascii=False))
 else:make()
