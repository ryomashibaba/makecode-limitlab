#!/usr/bin/env python3
"""M34: Blender-native editability and lived/urban same-scene GATE. Never construction."""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector

OUT=Path("artifacts/g4c7-m34-native-authoring").resolve()
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != "Collection" and c.users == 0:
        bpy.data.collections.remove(c)

def collection(name):
    c=bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c

groups={n:collection(n) for n in (
 "M34_01_PUBLIC_SPINE","M34_02_MAKER_INTERIOR",
 "M34_03_RESEARCH_INTERIOR","M34_04_CIVIC_CANOPY",
 "M34_05_CAMERAS","M34_06_VISUAL_CONTEXT")}
def regroup(o,name):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    groups[name].objects.link(o)
    return o

def mat(name,color,metal=0,rough=0.7):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(*color,1)
    p.inputs["Metallic"].default_value=metal
    p.inputs["Roughness"].default_value=rough
    return m

stone=mat("M34_Light_Mineral",(0.63,0.67,0.66))
streetmat=mat("M34_Civic_Public_Stone",(0.29,0.38,0.43))
bronze=mat("M34_Warm_Bronze",(0.45,0.31,0.21),.35)
glazing=mat("M34_Clear_Observation_Glass",(0.26,0.5,0.57),.35,.22)
timber=mat("M34_Warm_Interior",(0.49,0.36,0.24))
garden=mat("M34_Garden_Green",(0.19,0.38,0.24))
def box(name,loc,size,material,group):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object
    o.name=name
    o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    regroup(o,group)
    return o
def solid(name,verts,faces,material,group):
    mesh=bpy.data.meshes.new(name+"_Mesh")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    o=bpy.data.objects.new(name,mesh)
    groups[group].objects.link(o)
    o.data.materials.append(material)
    return o
def slope(name,x0,x1,y0,y1,z0,z1,thickness,material,group):
    V=[(x0,y0,z0),(x0,y1,z0),(x1,y1,z1),(x1,y0,z1),
       (x0,y0,z0-thickness),(x0,y1,z0-thickness),
       (x1,y1,z1-thickness),(x1,y0,z1-thickness)]
    return solid(name,V,[(0,3,2,1),(4,5,6,7),(0,1,5,4),
          (3,7,6,2),(0,4,7,3),(1,2,6,5)],material,group)
def wall(name,x0,x1,y0,y1,z0,z1,material,group):
    return box(name,((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),
       (x1-x0,y1-y0,z1-z0),material,group)
# Real floor surfaces. A single 5/50 (0.10) rise, not a claimed all-person route.
box("M34_PUBLIC_LOWER_STREET",( -27,0,0),(75,12,.4),streetmat,"M34_01_PUBLIC_SPINE")
slope("M34_PUBLIC_REAL_RISE",10,60,-5,5,.2,5.2,.4,streetmat,"M34_01_PUBLIC_SPINE")
box("M34_PUBLIC_UPPER_LANDING",(74,0,5),(28,12,.4),streetmat,"M34_01_PUBLIC_SPINE")
box("M34_MAKER_FLOOR",(-30,-18,0),(30,24,.4),timber,"M34_02_MAKER_INTERIOR")
# Maker room with a genuinely missing doorway section in the street-facing wall (Y=-6).
wall("M34_MAKER_BACK",-45,-15,-30,-29.5,.2,8.6,stone,"M34_02_MAKER_INTERIOR")
wall("M34_MAKER_LEFT",-45,-44.5,-30,-6,.2,8.6,stone,"M34_02_MAKER_INTERIOR")
wall("M34_MAKER_RIGHT",-15.5,-15,-30,-6,.2,8.6,stone,"M34_02_MAKER_INTERIOR")
wall("M34_MAKER_FRONT_W",-45,-32,-6.5,-6,.2,8.6,stone,"M34_02_MAKER_INTERIOR")
wall("M34_MAKER_FRONT_E",-28,-15,-6.5,-6,.2,8.6,stone,"M34_02_MAKER_INTERIOR")
wall("M34_MAKER_DOOR_HEAD",-32,-28,-6.5,-6,5,8.6,stone,"M34_02_MAKER_INTERIOR")
box("M34_MAKER_WORKTABLE",(-32,-21,1.1),(10,3.2,1.4),bronze,"M34_02_MAKER_INTERIOR")
box("M34_MAKER_ACTIVE_WORKSTATION",(-32,-21,2.3),(3.5,1.7,.8),timber,"M34_02_MAKER_INTERIOR")
# Roof is separated from room walls for actual interior inspection; no fictitious top slab.
box("M34_MAKER_UPPER_ROOF",(-30,-19,8.85),(30,22,.5),stone,"M34_04_CIVIC_CANOPY")
# Upper research front-door opens toward the public upper landing, not through a solid slab.
box("M34_RESEARCH_ACTUAL_FLOOR",(73,19,5),(30,25,.4),timber,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_BACK",58,88,31,31.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_SIDE_E",87.5,88,6,31.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_SIDE_W",58,58.5,6,31.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_FRONT_W",58,71,6,6.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_FRONT_E",75,88,6,6.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_DOOR_HEAD",71,75,6,6.5,10.0,14.2,stone,"M34_03_RESEARCH_INTERIOR")
# A real 4x4 window opening in a side wall rather than painting a false window.
# Side E is opaque; the room's back includes a 4m observation gap at X=71..75.
for ob in list(bpy.data.objects):
    if ob.name=="M34_RESEARCH_BACK":
        bpy.data.objects.remove(ob,do_unlink=True)
wall("M34_RESEARCH_BACK_W",58,69,31,31.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_BACK_E",77,88,31,31.5,5.2,14.2,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_BACK_LOWER",69,77,31,31.5,5.2,6.5,stone,"M34_03_RESEARCH_INTERIOR")
wall("M34_RESEARCH_BACK_UPPER",69,77,31,31.5,11.5,14.2,stone,"M34_03_RESEARCH_INTERIOR")
box("M34_RESEARCH_ACTUAL_DESK",(75,21,6.15),(8,3,1.5),bronze,"M34_03_RESEARCH_INTERIOR")
box("M34_RESEARCH_LIVING_GARDEN",(82,26,5.4),(7,6,.7),garden,"M34_03_RESEARCH_INTERIOR")
# Make an editable artist canopy, not a 100m fake wall or generic slab.
# Only this canopy mesh is altered AFTER reopening the saved native .blend.
canopy=solid("M34_HAND_EDITABLE_SKYLINE_CANOPY",
 [(-49,-31,9.2),(-44,-4,10.3),(-24,-3,12.7),(-9,-30,11.8),
  (-49,-31,9.65),(-44,-4,10.75),(-24,-3,13.15),(-9,-30,12.25)],
 [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],
 bronze,"M34_04_CIVIC_CANOPY")
# Native editable Bézier geometry records the master art axis, does NOT claim a floor.
cv=bpy.data.curves.new("M34_Editable_Urban_Experience_Spine","CURVE")
cv.dimensions="3D"; cv.resolution_u=12;cv.bevel_depth=.15;cv.bevel_resolution=2
sp=cv.splines.new("BEZIER");sp.bezier_points.add(4)
for p,co in zip(sp.bezier_points,[(-58,0,.5),(-25,0,.5),(8,0,.5),(38,0,3.5),(76,0,5.5)]):
    p.co=co;p.handle_left_type="AUTO";p.handle_right_type="AUTO"
guide=bpy.data.objects.new("M34_NATIVE_EDITABLE_CIVIC_SPINE",cv)
groups["M34_01_PUBLIC_SPINE"].objects.link(guide)
cv.materials.append(bronze)
# Native camera objects are preserved in BLEND and reused after an actual mesh edit.
def camera(name,point,target,lens):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d)
    groups["M34_05_CAMERAS"].objects.link(o)
    o.location=point
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
    d.lens=lens
    return o
cameras={
 "south":camera("M34_CAMERA_SOUTH",(-5,-110,42),(25,2,6),33),
 "north":camera("M34_CAMERA_NORTH",(70,95,37),(25,0,6),37),
 "urban_oblique":camera("M34_CAMERA_URBAN_OBLIQUE",(-45,-90,95),(24,0,7),34),
 "public_approach":camera("M34_CAMERA_PUBLIC_APPROACH",(-57,-3,1.9),(-24,0,3),24),
 "maker_eye":camera("M34_CAMERA_MAKER_EYE",(-32,-23,1.9),(-30,-6,3),28),
 "research_eye":camera("M34_CAMERA_RESEARCH_EYE",(75,24,6.9),(73,6,9.3),26)}
# Soft world and physical lights; renders are model screenshots, never AI reference images.
world=bpy.context.scene.world
world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.60,.72,.81,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.65
for i,(loc,power,size) in enumerate([
 ((-10,-30,65),5000,35),((78,60,46),4200,27),((-31,-16,7),1200,12),
 ((73,18,13),1300,10)]):
    data=bpy.data.lights.new("M34_Light_%02d"%i,"AREA")
    ob=bpy.data.objects.new("M34_Light_%02d"%i,data)
    groups["M34_06_VISUAL_CONTEXT"].objects.link(ob)
    ob.location=loc;data.energy=power;data.shape="DISK";data.size=size
    ob.rotation_euler=(Vector((24,0,5))-ob.location).to_track_quat("-Z","Y").to_euler()
scene=bpy.context.scene
scene.render.engine="CYCLES"
scene.cycles.samples=14
scene.render.resolution_x=760
scene.render.resolution_y=460
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.camera=cameras["south"]
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def export(label):
    blend=OUT/("M34_NATIVE_"+label+".blend")
    glb=OUT/("M34_NATIVE_"+label+".glb")
    scene.camera=cameras["south"]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_cameras=False,export_lights=False)
    im={}
    for k,c in cameras.items():
        scene.camera=c
        path=OUT/("M34_"+label+"_"+k+".png")
        scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        im[k]=sha(path)
    return {"blend":blend.name,"blend_sha256":sha(blend),"glb":glb.name,
            "glb_sha256":sha(glb),"images":im}
before=export("BASE")
# Crucial: OPEN the saved native BLEND and directly edit EXISTING MESH VERTICES.
bpy.ops.wm.open_mainfile(filepath=str(OUT/"M34_NATIVE_BASE.blend"))
mesh_obj=bpy.data.objects["M34_HAND_EDITABLE_SKYLINE_CANOPY"]
base_verts=[tuple(v.co) for v in mesh_obj.data.vertices]
for index in (2,6):
    mesh_obj.data.vertices[index].co.z+=2.25
mesh_obj.data.update()
assert any(abs(mesh_obj.data.vertices[i].co.z-base_verts[i][2]-2.25)<1e-6 for i in (2,6))
# The exact same named exterior and human cameras must survive reopening.
cameras={key:bpy.data.objects["M34_CAMERA_"+key.upper()] for key in cameras}
scene=bpy.context.scene
after=export("DIRECT_EDIT")
summary={"study":"M34_NATIVE_AUTHORING_METHOD_ONLY",
 "art":"HOLD_NO_ART_ADOPTION","city":"NOT_BUILT",
 "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
 "minecraft_education":"CONSTRUCTION_FORBIDDEN",
 "actual_native_reopen_and_existing_mesh_edit":True,
 "edited_object":"M34_HAND_EDITABLE_SKYLINE_CANOPY",
 "edited_vertex_indices":[2,6],"vertex_delta_z":2.25,
 "shared_saved_cameras":list(cameras),"native_collections":list(groups),
 "base":before,"direct_edit":after}
(OUT/"M34_NATIVE_AUTHORING_MANIFEST.json").write_text(json.dumps(summary,indent=2))
print("M34_NATIVE_FILE_SAVED_REOPENED_AND_EDITED_NO_ART_PASS")
