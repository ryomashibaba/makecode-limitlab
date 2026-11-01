#!/usr/bin/env python3
"""M37-O1: activity-to-city-section native Blender AUTHOR STUDY, not ART PASS.
A single hand-authored inhabited cross-section and coarse district exterior.
Does NOT use M37-L/N tube art. No Minecraft/MakeCode/world writes.
"""
import bpy, json, hashlib, math
from pathlib import Path
from mathutils import Vector

OUT=Path("artifacts/g4c7-m37o-activity-section-build")
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=Path("artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/M37N_MAKER_SHELL_DIRECT_EDIT_ART_HOLD.blend")
PIN="0817bf8a9681e9380b8167e75ddc236dbcab18920b01298c5e405ed46752bdff"
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
assert SOURCE.is_file() and sha(SOURCE)==PIN,"M37-N native parent not pinned"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
sc.name="M37O_A_INHABITED_SHIPYARD_SEAM_COARSE_ART_HOLD"
for k,v in {
 "M37O_ART":"EARLY_REVIEW_REQUIRED_NOT_PASSED",
 "M37O_FORMAL_331_993":"NOT_RUN",
 "M37O_USER_ADOPTION":0,
 "M37O_MINECRAFT":"FORBIDDEN",
 "M37O_PRIOR_TUBE_ART":"NOT_IMPORTED",
 "M37O_MODEL_UNIT":"ABSTRACT_RESEARCH_NOT_MINECRAFT_BLOCK",
 "M37O_SOURCE_M37N_SHA256":PIN,
 "M37O_TECH":"NATIVE_SOURCE_WITHOUT_SAFETY_OR_ROUTE_CERTIFICATION"
}.items():sc[k]=v
col=bpy.data.collections.new("M37O_A_AUTHOR_PROGRAM_AND_CITY_COHERENT")
sc.collection.children.link(col)
def material(name,rgba,metallic=0):
    m=bpy.data.materials.new("M37O_"+name)
    m.diffuse_color=tuple(rgba)+(1,)
    m.use_nodes=True
    bs=m.node_tree.nodes["Principled BSDF"]
    bs.inputs["Base Color"].default_value=tuple(rgba)+(1,)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=.48
    return m
mat={
 "CIVIC":material("CIVIC_CERAMIC",(.64,.59,.49)),
 "MAKER":material("MAKER_ALLOY",(.22,.36,.43),.5),
 "RESEARCH":material("RESEARCH_BRONZE",(.58,.47,.27),.25),
 "HABITAT":material("RESIDENTIAL_STONE",(.72,.65,.53)),
 "CULTURE":material("CULTURAL_STONE",(.36,.53,.50)),
 "PUBLIC":material("PUBLIC_PATH",(.46,.49,.42)),
 "GUARD":material("GUARD",(.16,.23,.28),.4),
 "CRAFT":material("CRAFT",(.81,.77,.63),.55)
}
def geometry(name,vertices,faces,role,material_key,program):
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata(vertices,[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    col.objects.link(ob)
    ob.data.materials.append(mat[material_key])
    ob["M37O_ROLE"]=role
    ob["M37O_PROGRAM"]=program
    return ob
def footprint(name,poly,z0,z1,role,material_key,program):
    # No repeating city envelope primitive: every 2D outline below is authored
    # from a use-specific spatial section, not inferred from a parametric tube.
    n=len(poly)
    assert n>=4 and z0<z1
    vs=[(x,y,z) for z in (z0,z1) for x,y in poly]
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return geometry(name,vs,faces,role,material_key,program)
def segment(name,a,b,z0,z1,thick,role,material_key,program):
    dx,dy=b[0]-a[0],b[1]-a[1]
    l=math.hypot(dx,dy);assert l>0.1
    nx=-dy/l*thick/2;ny=dx/l*thick/2
    poly=[(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),
          (b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)]
    return footprint(name,poly,z0,z1,role,material_key,program)
# These seven contours/altitudes are individually authored with citizen uses.
# They create both the actual horizontal room footprint and the visible roof
# outline in the SAME native scene; all have real wall gaps at named entries.
PROGRAMS=[
 {"id":"ARRIVAL","use":"CIVIC","z":3,"h":8,"door":2,
  "outline":[(-82,-56),(-56,-61),(-47,-42),(-58,-25),(-87,-32)]},
 {"id":"COMMONS","use":"CIVIC","z":7,"h":11,"door":3,
  "outline":[(-55,-37),(-20,-44),(-8,-25),(-21,-3),(-49,-11),(-65,-24)]},
 {"id":"SHIPYARD","use":"MAKER","z":0,"h":32,"door":4,
  "outline":[(-46,-85),(1,-96),(30,-73),(19,-38),(-6,-31),(-45,-49)]},
 {"id":"RESEARCH","use":"RESEARCH","z":18,"h":23,"door":4,
  "outline":[(5,-26),(36,-38),(55,-17),(43,17),(18,22),(-2,1)]},
 {"id":"HABITAT","use":"HABITAT","z":33,"h":19,"door":3,
  "outline":[(-33,18),(-3,8),(21,25),(8,58),(-22,63),(-44,42)]},
 {"id":"CULTURE","use":"CULTURE","z":44,"h":15,"door":0,
  "outline":[(40,13),(79,9),(91,35),(72,59),(43,51),(28,33)]},
 {"id":"SKY","use":"PUBLIC","z":61,"h":5,"door":5,
  "outline":[(70,47),(98,40),(115,57),(103,78),(75,84),(62,64)]}
]
# A physical public/private factory separation exists, but performance is not
# certified. The actual roof voids expose uses instead of a giant common shell.
for p in PROGRAMS:
    id=p["id"];poly=p["outline"];z=p["z"];h=p["h"];use=p["use"]
    footprint("M37O_"+id+"_OCCUPIED_FLOOR",poly,z-.7,z,"REAL_PROGRAM_FLOOR",use,id)
    footprint("M37O_"+id+"_ROOF_SILHOUETTE",poly,z+h,z+h+.8,
              "PROGRAM_DETERMINES_CITY_SILHOUETTE",use,id)
    for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
        if i==p["door"]:
            ax=(a[0]*.63+b[0]*.37,a[1]*.63+b[1]*.37)
            bx=(a[0]*.37+b[0]*.63,a[1]*.37+b[1]*.63)
            segment("M37O_"+id+"_DOOR_LEFT",a,ax,z,z+h,.8,
                    "SOLID_WALL_LEFT_OF_REAL_OPENING",use,id)
            segment("M37O_"+id+"_DOOR_RIGHT",bx,b,z,z+h,.8,
                    "SOLID_WALL_RIGHT_OF_REAL_OPENING",use,id)
            segment("M37O_"+id+"_DOOR_HEADER",ax,bx,z+4,z+h,.8,
                    "REAL_OPENING_ABOVE_FLOOR_BELOW_HEADER",use,id)
        elif not (id=="SHIPYARD" and i==1):
            segment("M37O_"+id+"_WALL_"+str(i),a,b,z,z+h,.8,
                    "EXTERIOR_ENCLOSURE",use,id)
    # Shipyard east wall is deliberately not glazed over: its job is a huge
    # working aperture; public approach must still be isolated elsewhere.
# Fixed route is author-specified PUBLIC sequence, not a passable certification.
# Stations intentionally fold across the city rather than a giant straight road.
STATIONS=[
 ("ARRIVAL",(-62,-43,4)),("CIVIC",(-42,-24,8)),
 ("VIEW",(-12,-32,12)),("RESEARCH",(16,-8,19)),
 ("HABITAT",(-2,24,34)),("CULTURE",(45,32,45)),
 ("SKY",(80,61,62))
]
for i,((na,a),(nb,b)) in enumerate(zip(STATIONS,STATIONS[1:])):
    d=Vector(b)-Vector(a)
    n=Vector((-d.y,d.x,0));n.normalize();n*=2.2
    va,vb=Vector(a),Vector(b)
    coords=[tuple(va+n),tuple(vb+n),tuple(vb-n),tuple(va-n),
            tuple(va+n-Vector((0,0,.6))),tuple(vb+n-Vector((0,0,.6))),
            tuple(vb-n-Vector((0,0,.6))),tuple(va-n-Vector((0,0,.6)))]
    geometry("M37O_ROUTE_"+str(i)+"_"+na+"_TO_"+nb,coords,
       [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],
       "ACTUAL_ROUTE_SURFACE_WITHOUT_HUMAN_SWEEP", "PUBLIC","PUBLIC_ROUTE")
# Maker scene contains an actual spacecraft assembly subject (not a city tube)
# and a staffed/public interface materialized as independent 3D objects.
# The vehicle is local to the factory; it does not define the city's envelope.
cx,cy=-3,-63
rings=[(5,1.0),(10,5.5),(23,8),(32,7.5),(40,4.5),(45,.6)]
verts=[]
for z,r in rings:
    verts += [(cx+r*math.cos(2*math.pi*j/16),
               cy+r*math.sin(2*math.pi*j/16),z) for j in range(16)]
faces=[]
for j in range(len(rings)-1):
    for k in range(16):
        faces.append((j*16+k,j*16+(k+1)%16,(j+1)*16+(k+1)%16,(j+1)*16+k))
faces += [tuple(range(15,-1,-1)),tuple((len(rings)-1)*16+k for k in range(16))]
geometry("M37O_SHIPYARD_REAL_VEHICLE_MASS",verts,faces,
         "SPACECRAFT_UNDER_ASSEMBLY_RESEARCH_GEOMETRY_NOT_FLIGHT_READY",
         "CRAFT","SHIPYARD")
# Actual opaque industrial exclusion wall between worksite and public lookout.
segment("M37O_MAKER_PUBLIC_SECURITY_PARTITION",
        (-42,-48),(-3,-32),9,17,1.1,"ACTUAL_IMPASSABLE_STAFF_PUBLIC_BARRIER",
        "GUARD","SHIPYARD")
# View bridge: separate physical space, never assert continuous accessible walk.
footprint("M37O_PUBLIC_FABRICATION_VIEW_BAY",
          [(-36,-45),(-4,-43),(5,-32),(-31,-28)],11.5,12.3,
          "ACTUAL_OBSERVATION_BAY_ACCESS_NOT_PROVEN","CIVIC","COMMONS")
# Design authoring makes the public narrative and silhouette share geometry;
# it is not a universal procedural generator and NOT an aesthetic acceptance.
def camera(key,location,target,lens):
    d=bpy.data.cameras.new("M37O_"+key+"_DATA")
    ob=bpy.data.objects.new("M37O_CAMERA_"+key,d)
    col.objects.link(ob)
    ob.location=location
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
    d.lens=lens
    return ob
cams={
 "SOUTH":camera("SOUTH",(0,-245,120),(6,-15,26),32),
 "NORTH":camera("NORTH",(12,220,130),(0,-30,25),32),
 "AERIAL":camera("AERIAL",(165,-155,185),(0,-10,32),34),
 "PUBLIC_EYE":camera("PUBLIC_EYE",(-61,-53,7),(-8,-24,15),25),
 "MAKER_EYE":camera("MAKER_EYE",(-36,-56,14),(-3,-63,23),27),
 "RESEARCH_EYE":camera("RESEARCH_EYE",(24,-17,24),(45,-6,33),27),
 "HABITAT_EYE":camera("HABITAT_EYE",(-20,38,39),(25,20,46),29),
 "CULTURE_EYE":camera("CULTURE_EYE",(49,30,49),(85,58,61),29),
 "UPPER_EYE":camera("UPPER_EYE",(80,64,66),(8,-20,32),27)
}
world=bpy.data.worlds.new("M37O_DAYLIGHT")
world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.57,.66,.77,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.8
sc.world=world
light=bpy.data.lights.new("M37O_SUNLIGHT","SUN")
light.energy=2
sun=bpy.data.objects.new("M37O_SUN",light);col.objects.link(sun)
sun.rotation_euler=(.48,-.65,.4)
sc.camera=cams["AERIAL"]
sc.render.engine="CYCLES"
sc.cycles.samples=8
sc.render.resolution_x=760
sc.render.resolution_y=480
sc.render.resolution_percentage=100
sc.render.image_settings.file_format="PNG"
native=OUT/"M37O_A_REAL_ACTIVITY_SILHOUETTE_AUTHOR_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(native.resolve()))
renders={}
for key in ("AERIAL","PUBLIC_EYE","MAKER_EYE","HABITAT_EYE","UPPER_EYE"):
    sc.camera=cams[key]
    png=OUT/("M37O_"+key+".png")
    sc.render.filepath=str(png.resolve())
    bpy.ops.render.render(write_still=True,scene=sc.name)
    assert png.stat().st_size>3000
    renders[key]={"file":png.name,"sha256":sha(png)}
    print("M37O_NATIVE_RENDER",key,flush=True)
manifest={
 "schema":"g4c7-m37o1-activity-silhouette-author-art-hold-v1",
 "concept":"A_INHABITED_SHIPYARD_SEAM","art":"EARLY_REVIEW_REQUIRED",
 "official_adoption":0,"formal_331_993":"NOT_RUN",
 "S1_G1_G2_G3":"NOT_RUN","Minecraft":"FORBIDDEN",
 "MakeCode":"NOT_EVALUATED_NO_WRITES",
 "user_work_approval":"NOT_REQUESTED_NOT_USED",
 "old_native_parent_sha256":PIN,"old_tube_meshes_imported":0,
 "scene":sc.name,"programs":PROGRAMS,
 "physical_public_route_stations":STATIONS,
 "path_walkability":"NOT_CERTIFIED",
 "factory_staff_public_barrier":"GEOMETRY_ONLY_NOT_SAFETY_CERTIFIED",
 "seven_interiors":"WALL_OPENINGS_PRESENT_BUT_ACCESS_NOT_CERTIFIED",
 "cameras":list(cams),
 "native_blend":{"file":native.name,"sha256":sha(native),"bytes":native.stat().st_size},
 "same_native_blend_renders":renders,
 "assessor_instruction":"Review macro, city density, ground eye, factory activity, habitat privacy and upper eye absolutely. If simple disconnected pavilions or elevated road dominate, EARLY ART REJECT, do not extend this A.",
 "limit":"One authored spatial study; not proven cohesive city, buildability, structure, egress, privacy, pedestrian route, or visual quality."
}
(OUT/"M37O_AUTHOR_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print("M37O_SAVED_UNREVIEWED",sha(native),flush=True)
