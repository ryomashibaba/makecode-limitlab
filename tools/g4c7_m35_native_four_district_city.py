#!/usr/bin/env python3
"""G4-C7 M35: new scene, lived urban floors and skyline in one editable Blender file.
No M34 visual geometry imported. Research units != Minecraft metres.
"""
import bpy,math,hashlib,json
from pathlib import Path
from mathutils import Vector
P=Path("artifacts/g4c7-m35-author-scene").resolve()
P.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
groups={}
for k in ("PUBLIC_SPINES","FABRICATION","HABITAT","RESEARCH","CULTURE","STAIRS_AND_BRIDGE","AUTHOR_SKYLINE","CAMERAS","LIGHTS"):
    c=bpy.data.collections.new("M35_"+k);bpy.context.scene.collection.children.link(c);groups[k]=c
def material(k,color,metal=0):
    m=bpy.data.materials.new("M35_"+k);m.diffuse_color=(*color,1);m.use_nodes=True
    n=m.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value=(*color,1)
    n.inputs["Metallic"].default_value=metal
    return m
mineral=material("Stone",(.65,.70,.70));warm=material("Warm_Ceramic",(.57,.34,.19),.1)
street=material("Public_Stone",(.48,.54,.51));bronze=material("Structure_Copper",(.52,.30,.18),.45)
green=material("Garden",(.2,.43,.26));research=material("Blue_Research",(.18,.46,.58),.35)
dark=material("Market",(.24,.31,.36));wood=material("Interior",(.49,.39,.28))
def box(n,loc,size,mat,group):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name="M35_"+n;o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    for c in list(o.users_collection):c.objects.unlink(o)
    groups[group].objects.link(o)
    return o
def mesh(n,verts,faces,mat,group):
    me=bpy.data.meshes.new("M35_"+n+"_data")
    me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new("M35_"+n,me)
    groups[group].objects.link(o);me.materials.append(mat);return o
def wall(n,a,b,lo,hi,mat,g):
    x0,y0=a;x1,y1=b
    length=math.hypot(x1-x0,y1-y0)
    ob=box(n,((x0+x1)*.5,(y0+y1)*.5,(lo+hi)*.5),
        (length,.7,hi-lo),mat,g)
    ob.rotation_euler[2]=math.atan2(y1-y0,x1-x0)
    return ob
def openroom(prefix,x0,x1,y0,y1,doorx,mat,group,roof=False):
    box(prefix+"_REAL_FLOOR",((x0+x1)/2,(y0+y1)/2,0),(x1-x0,y1-y0,.4),wood,group)
    wall(prefix+"_BACK",(x0,y1),(x1,y1),.2,24,mat,group)
    wall(prefix+"_WEST",(x0,y0),(x0,y1),.2,24,mat,group)
    wall(prefix+"_EAST",(x1,y0),(x1,y1),.2,24,mat,group)
    wall(prefix+"_FRONT_LEFT",(x0,y0),(doorx-8,y0),.2,24,mat,group)
    wall(prefix+"_FRONT_RIGHT",(doorx+8,y0),(x1,y0),.2,24,mat,group)
    box(prefix+"_DOOR_HEADER",(doorx,y0,21),(16,.7,6),bronze,group)
def roof(n,rings,mat):
    # Hand-authored asymmetric skyline cross-sections; no enclosing false blocks.
    verts=[v for pair in rings for v in pair]
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(rings)-1)]
    return mesh(n,verts,faces,mat,"AUTHOR_SKYLINE")
# Intersecting public X/Y axes and 4 street-level entrances, z top=0.2.
for n,x,y,w,d in [
 ("CIVIC_CROSS",0,0,94,64),("EAST_AXIS",111,0,134,20),
 ("WEST_AXIS",-111,0,134,20),("NORTH_AXIS",0,106,24,163),
 ("SOUTH_AXIS",0,-106,24,163),
 ("FAB_ENTRANCE_STREET",-96,-15,13,30),
 ("RESEARCH_ENTRANCE_STREET",96,15,13,30),
 ("HABITAT_ENTRANCE_STREET",-90,15,13,30),
 ("CULTURE_ENTRANCE_STREET",90,-15,13,30),
 ("HABITAT_BASE_APPROACH",-69,35,46,18),
 ("RESEARCH_BASE_APPROACH",69,35,46,18)]:
    box(n,(x,y,0),(w,d,.4),street,"PUBLIC_SPINES")
# Genuine rooms with door-sized openings on their own public-facing edges.
# Fabrication south-west (door faces north, y=-30).
box("FAB_REAL_FLOOR",(-99,-73,0),(118,86,.4),wood,"FABRICATION")
wall("FAB_BACK",(-158,-116),(-40,-116),.2,24,mineral,"FABRICATION")
wall("FAB_WEST",(-158,-116),(-158,-30),.2,24,mineral,"FABRICATION")
wall("FAB_EAST",(-40,-116),(-40,-30),.2,24,mineral,"FABRICATION")
wall("FAB_FRONT_L",(-158,-30),(-104,-30),.2,24,mineral,"FABRICATION")
wall("FAB_FRONT_R",(-88,-30),(-40,-30),.2,24,mineral,"FABRICATION")
box("FAB_GATE_HEADER",(-96,-30,21),(16,.7,6),bronze,"FABRICATION")
for i,(x,y) in enumerate([(-130,-81),(-101,-83),(-68,-78),(-117,-55),(-72,-55)]):
    box("FAB_ACTIVE_BAY_"+str(i),(x,y,1.3),(10,5,2.6),bronze,"FABRICATION")
roof("FAB_ACTIVITY_ROOF",[
 [(-165,-120,33),(-165,-25,38)],[(-140,-120,40),(-140,-25,50)],
 [(-105,-120,49),(-105,-25,63)],[(-68,-120,42),(-68,-25,54)],
 [(-34,-120,28),(-34,-25,41)]],warm)
# Research north-east; street-to-door y=0..30 and exact physical floor inside y=30..
openroom("RESEARCH",34,162,30,116,96,research,"RESEARCH")
for i,(x,y) in enumerate([(64,77),(91,80),(123,76),(82,51),(121,52)]):
    box("RESEARCH_OCCUPIED_WORK_"+str(i),(x,y,1.1),(10,6,2.2),research,"RESEARCH")
roof("RESEARCH_CIVIC_COVER",[
 [(27,22,38),(27,123,43)],[(57,22,50),(57,123,68)],
 [(106,22,76),(106,123,82)],[(145,22,52),(145,123,65)],
 [(170,22,39),(170,123,46)]],research)
# Residence north-west, ground entrance at (-90,30). Real mid-level living floor and garden.
box("HABITAT_GROUND",(-108,79,0),(112,98,.4),wood,"HABITAT")
wall("HAB_WEST",(-164,30),(-164,128),.2,18,warm,"HABITAT")
wall("HAB_EAST",(-52,30),(-52,128),.2,18,warm,"HABITAT")
wall("HAB_NORTH",(-164,128),(-52,128),.2,18,warm,"HABITAT")
wall("HAB_SOUTH_L",(-164,30),(-98,30),.2,12,warm,"HABITAT")
wall("HAB_SOUTH_R",(-82,30),(-52,30),.2,12,warm,"HABITAT")
box("HAB_DOOR_HEADER",(-90,30,10),(16,.7,4),warm,"HABITAT")
box("HAB_ACTUAL_UPPER_LIVING",(-112,92,18),(98,60,.4),warm,"HABITAT")
box("HAB_GARDEN",(-131,96,18.45),(34,24,.5),green,"HABITAT")
roof("HAB_INHABITED_SKYLINE",[
 [(-169,34,24),(-169,132,28)],[(-145,34,38),(-145,132,45)],
 [(-112,34,49),(-112,132,61)],[(-77,34,51),(-77,132,57)],
 [(-47,34,32),(-47,132,40)]],warm)
# Culture south-east genuinely attached to ground civic access.
box("CULTURE_GROUND",(101,-78,0),(128,100,.4),dark,"CULTURE")
for i,(y,z,w) in enumerate([(-120,5,90),(-108,4,96),(-96,3,104),(-84,2,110)]):
    box("CULTURE_OCCUPIED_TIER_"+str(i),(101,y,z),(w,10,.5),warm,"CULTURE")
box("CULTURE_STAGE",(99,-58,.5),(52,25,.7),wood,"CULTURE")
for i,x in enumerate((55,76,121,142)):
    box("MARKET_WORK_KIOSK_"+str(i),(x,-38,1),(10,7,2),bronze,"CULTURE")
roof("CULTURE_CANOPY",[
 [(31,-125,17),(31,-31,23)],[(64,-125,30),(64,-31,41)],
 [(108,-125,43),(108,-31,53)],[(144,-125,26),(144,-31,37)],
 [(170,-125,15),(170,-31,25)]],bronze)
# Two separate 72-tread access flights, not painted ramps; top landing at z=18.2.
for kind,x in (("HAB",-51),("RESEARCH",51)):
    for i in range(72):
        box(kind+"_TREAD_%03d"%(i+1),(x,35+i+.5,(i+1)*.25-.1),
            (7,1,.2),street,"STAIRS_AND_BRIDGE")
    box(kind+"_LANDING",(x,113,18),(14,14,.4),street,"STAIRS_AND_BRIDGE")
box("UPPER_CITY_PUBLIC_BRIDGE",(0,113,18),(108,9,.4),bronze,"STAIRS_AND_BRIDGE")
# Physical upper bridge to upper living and research observation floor.
box("HAB_UPPER_BRIDGE_JOIN",(-59,113,18),(13,9,.4),street,"STAIRS_AND_BRIDGE")
box("RESEARCH_UPPER_GALLERY",(107,110,18),(104,16,.4),wood,"RESEARCH")
roof("UPPER_CIVIC_BRIDGE_SHELTER",[
 [(-55,108,25),(-55,120,29)],[(-20,108,32),(-20,120,36)],
 [(22,108,34),(22,120,36)],[(55,108,26),(55,120,29)]],research)
# Fixed genuine cameras (model images, not AI visualizations).
cams={}
def cam(n,xyz,target,lens):
    d=bpy.data.cameras.new("M35_"+n+"_lens");o=bpy.data.objects.new("M35_CAMERA_"+n,d)
    groups["CAMERAS"].objects.link(o);o.location=xyz
    o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
    d.lens=lens;cams[n]=o
cam("SOUTH",(0,-275,123),(0,0,13),34)
cam("NORTH",(0,250,105),(0,0,17),37)
cam("AERIAL",(-245,-225,242),(0,0,16),35)
cam("PUBLIC_EYE",(-15,-18,2),(8,16,4),22)
cam("FAB_EYE",(-104,-68,2),(-95,-30,7),25)
cam("RESEARCH_EYE",(94,67,2),(100,30,10),25)
cam("HAB_EYE",(-118,94,20),(-84,112,23),24)
cam("CULTURE_EYE",(96,-81,2),(100,-36,10),25)
cam("UPPER_BRIDGE_EYE",(0,113,20),(40,69,32),22)
world=bpy.context.scene.world;world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.43,.51,.57,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.7
for i,(pos,power,size) in enumerate([
 ((-240,-240,250),28000,105),((210,140,220),24000,105),
 ((-60,-60,80),4000,40),((90,70,82),4500,45)]):
    d=bpy.data.lights.new("M35_LIGHT_"+str(i),"AREA");d.energy=power;d.shape="DISK";d.size=size
    o=bpy.data.objects.new("M35_LIGHT_"+str(i),d);groups["LIGHTS"].objects.link(o);o.location=pos
    o.rotation_euler=(Vector((0,0,15))-o.location).to_track_quat("-Z","Y").to_euler()
scene=bpy.context.scene
scene.render.engine="CYCLES";scene.cycles.samples=9
scene.render.resolution_x=850;scene.render.resolution_y=510
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.camera=cams["SOUTH"]
blend=P/"M35_NATIVE_CITY_ART_HOLD.blend"
glb=P/"M35_SAVED_CITY_ART_HOLD.glb"
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",export_cameras=False,export_lights=False)
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
im={}
for name,c in cams.items():
    scene.camera=c;p=P/("M35_"+name+".png")
    scene.render.filepath=str(p);bpy.ops.render.render(write_still=True)
    im[name]={"file":p.name,"sha256":sha(p)}
    print("M35_REAL_CAMERA",name,flush=True)
m={"study":"M35_FOUR_INHABITED_DISTRICTS_AND_TWO_PUBLIC_AXES",
 "art":"HOLD_NOT_ADOPTED","minecraft":"NO_WRITES",
 "formal_safety":"331_993_NOT_RUN",
 "full_body_sweep":"NOT_RUN","structure":"NOT_CERTIFIED",
 "scale":"ABSTRACT_RESEARCH_UNITS_NOT_MINECRAFT_METERS",
 "street_floor_z":0.2,"upper_stair_z":18.2,
 "doors":{"fabrication":[-96,-30,.2],"research":[96,30,.2],
    "habitat":[-90,30,.2],"culture":[90,-30,.2]},
 "cameras":im,"blend":{"file":blend.name,"sha256":sha(blend)},
 "glb":{"file":glb.name,"sha256":sha(glb)},
 "full_city_art":"NOT_EVALUATED_BY_AUTOMATION",
 "official_adoption":0}
(P/"M35_MANIFEST.json").write_text(json.dumps(m,indent=2))
print("M35_REAL_NATIVE_SCENE_ART_HOLD",flush=True)
