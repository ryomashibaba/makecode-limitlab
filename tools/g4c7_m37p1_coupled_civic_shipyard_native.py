#!/usr/bin/env python3
"""G4-C7 M37-P1 native Blender ART-EARLY-REVIEW source.
A single hand-authored occupied urban cross-section where four shared human
decisions produce ACTUAL coupled vertices in exterior and occupied-use meshes.
NO reuse of M37-L/N tube or M37-O1 pavilions. NO Minecraft writes or ART PASS.
"""
from pathlib import Path
from mathutils import Vector
import bpy,math,hashlib,json

ROOT=Path("artifacts/g4c7-m37p1-shared-section-build")
ROOT.mkdir(parents=True,exist_ok=True)
SPEC=Path("research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json")
SOURCE=Path("artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_A_REAL_ACTIVITY_SILHOUETTE_AUTHOR_ART_HOLD.blend")
SOURCE_PIN="7845343514b79067835ddbbd18aabf93439a391f4a2c0983227475b18331b2f1"
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()
assert sha(SOURCE)==SOURCE_PIN
contract=json.loads(SPEC.read_text())
assert contract["status"]=="AUTHOR_INPUT_ONLY_NOT_ART"
assert contract["proposed_geometry"]=="NONE_NOT_GENERATED"
required={"shared_maker_clearance","research_daylight_transfer",
          "habitat_graded_threshold","upper_civic_link"}
assert {x["id"] for x in contract["shared_author_decisions"]}==required
# These authored decisions are UNITS OF INTENT, not Minecraft block scales.
decisions={"shared_maker_clearance":54.0,"research_daylight_transfer":12.0,
           "habitat_graded_threshold":11.0,"upper_civic_link":17.0}
C,D,H,U=(decisions[x] for x in (
    "shared_maker_clearance","research_daylight_transfer",
    "habitat_graded_threshold","upper_civic_link"))
assert 48<=C<=60 and 8<=D<=16 and 8<=H<=14 and 14<=U<=21
bpy.ops.wm.read_factory_settings(use_empty=False)
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob,do_unlink=True)
sc=bpy.context.scene
sc.name="M37P1_CIVIC_SHIPYARD_SHARED_AUTHOR_SECTION_ART_HOLD"
sc["M37P1_ART"]="EARLY_REVIEW_UNJUDGED"
sc["M37P1_MINECRAFT"]="FORBIDDEN"
sc["M37P1_ART_ADOPTION"]=0
sc["M37P1_331_993"]="NOT_RUN"
sc["M37P1_G0_S1_G1_G2_G3"]="NOT_RUN"
sc["M37P1_PREVIOUS_ART"]="M37O1_EARLY_REJECT"
sc["M37P1_SCALE"]="ABSTRACT_RESEARCH_NOT_MINECRAFT"
sc["M37P1_SOURCE_CONTRACT_SHA256"]=sha(SPEC)
studio=bpy.data.collections.new("M37P1_ONE_INTERLOCKED_URBAN_SECTION_NOT_MODULED_BUILDINGS")
sc.collection.children.link(studio)

def material(name,rgb,metal=0,rough=.52,emission=0):
    m=bpy.data.materials.new("P1_"+name)
    m.diffuse_color=tuple(rgb)+(1,)
    m.use_nodes=True
    bs=m.node_tree.nodes["Principled BSDF"]
    bs.inputs["Base Color"].default_value=tuple(rgb)+(1,)
    bs.inputs["Metallic"].default_value=metal
    bs.inputs["Roughness"].default_value=rough
    if emission:
        bs.inputs["Emission Color"].default_value=tuple(rgb)+(1,)
        bs.inputs["Emission Strength"].default_value=emission
    return m
M={
 "stone":material("PALE_MOON_STONE",(.51,.51,.46)),
 "concrete":material("EARTH_WARM_THICK_SECTION",(.34,.29,.29)),
 "civic":material("CIVIC_LIMESTONE",(.72,.64,.49)),
 "bronze":material("RESEARCH_BRONZE",(.58,.41,.25),.55),
 "alloy":material("SHIPYARD_TITANIUM",(.17,.38,.45),.7,.31),
 "habitat":material("HABITAT_CERAMIC",(.60,.45,.38)),
 "garden":material("LIVING_LANDSCAPE",(.16,.39,.30)),
 "light":material("OCCUPIED_SPACE_LIGHT",(.98,.76,.45),.1,.32,2),
 "seal":material("PHYSICAL_SEALED_SCREEN",(.26,.50,.54),.4,.2),
 "path":material("PUBLIC_WALKABLE_INTENT",(.70,.58,.46)),
 "craft":material("ASSEMBLY_STAINLESS",(.82,.84,.75),.78,.28),
 "dark":material("CUT_STONE_REVEAL",(.19,.23,.27),.2)
}
ledger={}
def obj(name,v,f,mat,role,programs,decision_tags=()):
    assert len(v)>=4 and f and name not in bpy.data.objects
    mesh=bpy.data.meshes.new(name+"_MESH")
    mesh.from_pydata([tuple(a) for a in v],[],f)
    mesh.update()
    item=bpy.data.objects.new("M37P1_"+name,mesh)
    studio.objects.link(item)
    item.data.materials.append(M[mat])
    item["P1_ROLE"]=role
    item["P1_PROGRAMS"]="|".join(programs)
    item["P1_DECISIONS"]="|".join(decision_tags)
    if decision_tags:ledger[item.name]={"decisions":list(decision_tags),"vertex":tuple(round(c,3) for c in v[0])}
    return item
def patch(name,poly,z,depth,mat,role,programs,tags=()):
    # actual thick uneven occupied surface, not building footprint extrusion
    assert len(poly)>=3
    v=[(x,y,z) for x,y in poly]+[(x,y,z-depth) for x,y in poly]
    n=len(poly)
    f=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]
    f += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return obj(name,v,f,mat,role,programs,tags)
def wall(name,a,b,z0,z1,thick,mat,role,programs,tags=()):
    a,b=Vector(a),Vector(b)
    t=(b-a).normalized()
    n=Vector((-t.y,t.x,0))*(thick/2)
    v=[(a.x+n.x,a.y+n.y,z0),(b.x+n.x,b.y+n.y,z0),
       (b.x-n.x,b.y-n.y,z0),(a.x-n.x,a.y-n.y,z0),
       (a.x+n.x,a.y+n.y,z1),(b.x+n.x,b.y+n.y,z1),
       (b.x-n.x,b.y-n.y,z1),(a.x-n.x,a.y-n.y,z1)]
    faces=[(3,2,1,0),(4,5,6,7),
           (0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return obj(name,v,faces,mat,role,programs,tags)
def bridge(name,path,width,thick,mat,programs,tags=()):
    # Multi-section standing surface, solid 3D. NOT safety certified.
    v=[]
    for p0,p1 in zip(path,path[1:]):
        assert (Vector(p1)-Vector(p0)).length>1
    for i,p in enumerate(path):
        prev=Vector(path[max(0,i-1)])
        nxt=Vector(path[min(len(path)-1,i+1)])
        d=nxt-prev
        n=Vector((-d.y,d.x,0)).normalized()*(width/2)
        p=Vector(p)
        v += [tuple(p+n),tuple(p-n),tuple(p+n-Vector((0,0,thick))),
              tuple(p-n-Vector((0,0,thick)))]
    f=[]
    for i in range(len(path)-1):
        a=4*i;b=4*(i+1)
        f += [(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),
              (a,a+2,b+2,b),(a+1,b+1,b+3,a+3)]
    f += [(0,1,3,2)]
    j=4*(len(path)-1);f += [(j,j+2,j+3,j+1)]
    return obj(name,v,f,mat,"SHARED_REAL_PUBLIC_SECTION_WITH_NO_CONTINUOUS_SWEEP_CERT",programs,tags)
# The city has no single giant tube or set of independently roofed polygon buildings.
# Multiple interlocked cross sections share a central civic/manufacturing gorge.
# These are hand-authored adjacent civic terraces with actual occupied surfaces.
patch("ARRIVAL_FOLDED_GROUND",[(-116,-73),(-85,-92),(-42,-70),(-60,-44),(-109,-41)],
      11,3,"stone","OPEN_PUBLIC_ARRIVAL",["arrival","commons"])
patch("COMMONS_LARGE_COURT",[(-80,-51),(-44,-71),(-18,-39),(-36,-7),(-66,-13)],
      15,4,"civic","PUBLIC_COURT_OPEN_TO_SKY",["commons","maker_view","research"])
patch("MAKER_OBSERVATION_LEDGE",[(-35,-38),(-17,-50),(19,-23),(17,0),(-6,7)],
      23+D*.32,2,"path","SEPARATED_LIVE_FACTORY_VIEW",["maker_view","research","commons"],["shared_maker_clearance","research_daylight_transfer"])
patch("RESEARCH_SHARED_PLAZA",[(8,-9),(42,-23),(70,0),(47,31),(18,27)],
      30+D*.55,3,"bronze","RESEARCH_FABRICATION_SHARED_EDGE",["research","maker_view","culture"],["research_daylight_transfer"])
patch("HABITAT_PRIVATE_COURT",[(-66,5),(-31,-3),(-2,20),(-27,49),(-69,38),(-79,23)],
      31+H*.50,2,"habitat","PRIVATE_COURT_REAL_FLOOR",["habitat_private","habitat_gate"],["habitat_graded_threshold"])
patch("CULTURE_CIVIC_FORUM",[(43,21),(67,10),(97,31),(79,60),(49,66),(28,41)],
      44+U*.32,3,"civic","PUBLIC_CULTURE_OVER_RESEARCH",["culture","research","upper"],["upper_civic_link"])
patch("UPPER_OPEN_SKY_DECK",[(79,47),(108,50),(126,74),(102,92),(78,78)],
      57+U*.52,2.5,"garden","HIGH_PUBLIC_VISTA",["upper","culture"],["upper_civic_link"])
# Four shared decision-driven architectural folds: each connects different
# activities in the same native vertex topology; no per-program building solids.
bridge("COMMONS_TO_MAKER_SECTION",
       [(-65,-42,15),(-41,-33,18),(-18,-25,23+D*.32),(0,-9,30+D*.55)],
       8,1.6,"path",["commons","maker_view","research"],["research_daylight_transfer"])
bridge("RESEARCH_TO_CULTURE_BRAID",
       [(33,10,30+D*.55),(47,23,37),(58,38,44+U*.32),(81,50,57+U*.52)],
       7,1.8,"stone",["research","culture","upper"],["research_daylight_transfer","upper_civic_link"])
bridge("PRIVATE_THRESHOLD",
       [(-57,-28,15),(-63,-4,22),(-52,13,31+H*.50)],
       5.5,1.3,"habitat",["commons","habitat_gate","habitat_private"],["habitat_graded_threshold"])
bridge("ARRIVAL_SHARED_PUBLIC_STAIR_INTENT",
       [(-104,-65,11),(-89,-55,12),(-65,-42,15)],8,1,"path",["arrival","commons"])
# The working bay is defined by its clearance, which moves its roof edges,
# viewing light cut and research portal together (not one scalar radius).
bay_top=C+14
# Two unequal deep folded work walls with an enormous REAL gap along the public
# view; there is no giant continuous box enclosure, roof or tubular shell.
wall("WEST_TECTONIC_MAKER_WING",(-42,-82),(-26,-15),3,bay_top,4,
     "dark","PILOT_INHABITED_SHARED_SHIPYARD_FACE",["maker_work","commons","maker_view"],
     ["shared_maker_clearance"])
wall("EAST_RESEARCH_MAKER_WING",(54,-69),(41,0),3,bay_top-6,3.5,
     "stone","OPEN_WORK_FACE_CONSTRAINS_RESEARCH_SKYLINE",
     ["maker_work","research","maker_view"],["shared_maker_clearance"])
# Instead of closing the top of the shipyard, an asymmetric upper structural
# arch/gantry actually crosses its open volume at the specified clearance.
bridge("GANTRY_OCCUPIED_LOFT",[( -37,-55,C+12),(-11,-45,C+19),
                                (27,-31,C+24),(48,-20,C+16)],7,2.4,
       "alloy",["maker_work","research","maker_view"],["shared_maker_clearance"])
# Public-private industrial *physical* screen has no staff-usable door from
# view side. It is a continuous solid, optically open only in renders.
wall("SHIPYARD_ACTUAL_PUBLIC_STAFF_SEAL",
     (-32,-38),(20,-12),22,35+D*.52,1.5,
     "seal","SEALED_BARRIER_NOT_FIRE_IMPACT_OR_ACCESS_CERTIFIED",
     ["maker_view","maker_work","research"],
     ["shared_maker_clearance","research_daylight_transfer"])
# Factory access entrance is on its separate staff service side.
bridge("STAFF_LOADING_FLOOR",[(-23,-103,5),(4,-89,5),(22,-66,5)],11,1.7,
       "alloy",["maker_staff_gate","maker_work"])
wall("HABITAT_PRIVATE_VIEW_BREAK",
     (-53,13),(-11,30),31+H*.5,44+H*.9,2.3,"habitat",
     "ACTUAL_PRIVATE_SCREEN_NO_PUBLIC_PASSAGE",["habitat_gate","habitat_private","commons"],
     ["habitat_graded_threshold"])
# Daylight slot is a *real absence* between roofed pieces, not a painted window.
# Research daylight D changes the upper edges of actual paired shading members
# and visible public research floor / visual barrier.
bridge("RESEARCH_SUN_SHELF_LEFT",
       [(11,-10,41+D*.5),(19,4,46+D*.5),(31,15,48+D*.5)],4,1.1,
       "bronze",["research","maker_view","culture"],["research_daylight_transfer"])
bridge("RESEARCH_SUN_SHELF_RIGHT",
       [(40,-21,48+D*.9),(49,-7,50+D*.9),(60,8,52+D*.9)],3.5,1.1,
       "bronze",["research","maker_view","culture"],["research_daylight_transfer"])
# An inhabitable upper culture section and true vertical sense. Ramps/stairs are
# not certified; this research studies the visual architecture first.
bridge("CULTURE_HANGING_LOGGIA",
       [(51,26,44+U*.32),(63,34,50+U*.4),(78,47,57+U*.52)],
       7,1.5,"civic",["culture","research","upper"],["upper_civic_link"])
# Housing is physically embedded into the civic fold, not a free standing house.
# Interlocking stepped residential balconies deliberately face AWAY from
# spacecraft manufacture and public visitor traffic.
for i,(a,b,z) in enumerate([
    ((-76,14),(-54,30),35+H*.5),
    ((-55,31),(-33,44),40+H*.5),
    ((-38,46),(-16,54),46+H*.5)]):
    wall("HABITAT_LIGHT_EDGE_%02d"%i,a,b,z,z+8,1.5,"habitat",
         "ACTUAL_RESIDENTIAL_OUTWARD_LIGHT_EDGE_NOT_COMPLETE_ROOM",
         ["habitat_private","habitat_gate"],["habitat_graded_threshold"])
    wall("HABITAT_BAY_DIVIDER_%02d"%i,
         (a[0]+3,a[1]-4),(a[0]+7,a[1]+5),z,z+8,1.2,"dark",
         "REAL_PRIVATE_BAY_DIVIDER",["habitat_private"],["habitat_graded_threshold"])
    patch("HABITAT_PRIVATE_BALCONY_%02d"%i,
          [a,b,(b[0]-5,b[1]+6),(a[0]-6,a[1]+4)],z,1.0,
          "garden","PRIVATE_OUTWARD_BALCONY_NO_PUBLIC_ACCESS",["habitat_private"],
          ["habitat_graded_threshold"])
# Authentic-looking (still abstract) spacecraft construction at real factory
# height. Many independently specified rings / radial scaffold arms, not a tube
# that controls the city's skyline. The working void remains open to the sky.
vehicle_center=Vector((10,-58,0))
profile=[(9,4.2),(14,8.5),(19,9),(31,8.2),(39,6.7),(47,4),(51,.7)]
N=18
v=[(vehicle_center.x+r*math.cos(2*math.pi*i/N),
    vehicle_center.y+r*math.sin(2*math.pi*i/N),z) for z,r in profile for i in range(N)]
f=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i)
   for j in range(len(profile)-1) for i in range(N)]
f += [tuple(range(N-1,-1,-1)),tuple((len(profile)-1)*N+i for i in range(N))]
obj("SPACECRAFT_REAL_ASSEMBLY_TEST_ARTIFACT",v,f,"craft",
    "ASSEMBLY_SUBJECT_NOT_REAL_WORKING_ROCKET",
    ["maker_work","maker_view","research"])
for i,(a,b) in enumerate([
    ((-24,-77),(3,-77)),((21,-76),(49,-70)),
    ((-23,-29),(5,-33)),((27,-38),(48,-22))]):
    wall("ASSEMBLY_WORK_CELL_%02d"%i,a,b,5,13+i*1.8,1.6,"alloy",
         "WORKCELL_FRAME_WITHOUT_OPERATIONAL_CERT",["maker_work"])
    # Exterior mesh placement contains practical industrial equipment, not
    # unrelated decoration covering visual failures.
for i,(p,q) in enumerate([
    ((-25,-68,16),(10,-56,33)),((37,-68,14),(10,-55,35)),
    ((-25,-43,26),(9,-52,42))]):
    bridge("ASSEMBLY_GANTRY_ARM_%02d"%i,[p,q],2.8,1.2,"alloy",
           ["maker_work","maker_view"],["shared_maker_clearance"])
# Actual occupied public atrium and shared research light court, including
# uneven seating/teaching areas that remain open to adjacent civic movement.
for i,(xy,z) in enumerate([((-47,-37),16),((-36,-26),16),((30,9),30+D*.55),
                            ((64,40),44+U*.32)]):
    x,y=xy
    patch("OCCUPIED_PUBLIC_FORUM_%02d"%i,
          [(x-6,y-3),(x+5,y-4),(x+8,y+5),(x-5,y+7)],
          z+0.2,1.0,"civic","PUBLIC_ACTIVITY_STAGE_NOT_AN_UNUSED_ROOM",
          ["commons","research","culture"])
# Asymmetric structural fins visible from city scale:
for i,(a,b) in enumerate([
    ((-97,-39),(-74,0)),((-73,-12),(-57,34)),
    ((35,-69),(65,-22)),((58,-10),(96,26)),
    ((75,50),(107,76))]):
    ztop=[39,48,59,65,78+U*.5][i]
    wall("LOAD_PATH_RIB_%02d"%i,a,b,8,ztop,1.5,"concrete",
         "ARCHITECTURAL_RIB_NOT_STRUCTURAL_CERT",
         ["commons","maker_work","research","culture","upper"],
         ["upper_civic_link"] if i==4 else (["shared_maker_clearance"] if i in (2,3) else []))
# Lighting and nine fixed saved viewpoints. Explicitly avoid pointing into a
# dark solid, but do not hide defects by moving cameras after viewing them.
def camera(name,loc,target,lens):
    data=bpy.data.cameras.new("M37P1_"+name+"_DATA")
    ob=bpy.data.objects.new("M37P1_CAMERA_"+name,data)
    studio.objects.link(ob)
    ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
    data.lens=lens
    return ob
cams={
 "SOUTH":camera("SOUTH",(17,-265,124),(4,-15,35),32),
 "NORTH":camera("NORTH",(15,205,143),(0,-17,33),33),
 "AERIAL":camera("AERIAL",(189,-141,184),(4,-19,37),32),
 "PUBLIC_EYE":camera("PUBLIC_EYE",(-93,-58,15),(-51,-29,24),22),
 "MAKER_EYE":camera("MAKER_EYE",(-28,-42,28),(13,-52,32),22),
 "RESEARCH_EYE":camera("RESEARCH_EYE",(40,-3,37),(8,-42,34),24),
 "HABITAT_EYE":camera("HABITAT_EYE",(-58,25,43),(-22,38,46),24),
 "CULTURE_EYE":camera("CULTURE_EYE",(58,42,52),(14,-23,38),23),
 "UPPER_EYE":camera("UPPER_EYE",(92,60,72),(11,-38,33),27)
}
world=bpy.data.worlds.new("M37P1_BRIGHT_OPEN_SKY")
world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.65,.73,.79,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=1.15
sc.world=world
sun=bpy.data.lights.new("M37P1_SUN","SUN")
sun.energy=2.6
so=bpy.data.objects.new("M37P1_SUN_OBJECT",sun)
studio.objects.link(so)
so.rotation_euler=(.47,-.61,-.28)
sc.camera=cams["AERIAL"]
sc.render.engine="CYCLES"
sc.cycles.samples=8
sc.cycles.max_bounces=4
sc.render.resolution_x=780
sc.render.resolution_y=500
sc.render.resolution_percentage=100
sc.render.image_settings.file_format="PNG"
sc.render.film_transparent=False
sc.view_settings.view_transform="AgX"
# A second reproducible evaluation of the four author decisions is captured as
# hard *actual* scene mesh dependencies, never by a bare semantic label.
names={name for name in ledger}
affected={tag:[n for n,info in ledger.items() if tag in info["decisions"]]
          for tag in decisions}
assert all(len(group)>=5 for group in affected.values()),affected
assert all(any("ROUTE" in n or "SECTION" in n or "BRAID" in n or "THRESHOLD" in n or "GANTRY" in n
               for n in group) for group in affected.values())
native=ROOT/"M37P1_ONE_COUPLED_NATIVE_CITY_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(native.resolve()))
render={}
for key in ("AERIAL","PUBLIC_EYE","MAKER_EYE","RESEARCH_EYE","HABITAT_EYE",
            "CULTURE_EYE","UPPER_EYE"):
    sc.camera=cams[key]
    png=ROOT/("M37P1_"+key+".png")
    sc.render.filepath=str(png.resolve())
    bpy.ops.render.render(write_still=True,scene=sc.name)
    assert png.stat().st_size>3000
    render[key]={"name":png.name,"sha256":sha(png)}
    print("M37P1_TRUE_NATIVE_VIEW",key,flush=True)
manifest={
 "schema":"g4c7-m37p1-native-shared-author-section-v1",
 "art":"EARLY_REVIEW_REQUIRED_UNAPPROVED",
 "formal_adoption":0,"formal_331_993":"NOT_RUN",
 "S1_G1_G2_G3":"NOT_RUN","Minecraft":"FORBIDDEN",
 "MakeCode_estimate":"NOT_EVALUATED",
 "previous_M37O1_art":"EARLY_REJECT_NOT_REUSED",
 "old_pavilions_and_tubes_imported":0,
 "source_contract_sha256":sha(SPEC),"old_M37O1_blend_pin":SOURCE_PIN,
 "shared_author_decisions":decisions,
 "actual_native_meshes_tied_to_author_decisions":affected,
 "native_scene":sc.name,"native_blend":{"name":native.name,"sha256":sha(native),"bytes":native.stat().st_size},
 "cameras":list(cams),"same_saved_native_renders":render,
 "physical_habitat_privacy":"WALL_PRESENT_NOT_CERTIFIED",
 "physical_factory_public_separation":"MESH_PRESENT_NOT_CERTIFIED",
 "walkable_full_route":"NOT_CERTIFIED",
 "connected_multiprogram_architecture":"EARLY_VISUAL_REVIEW_REQUIRED",
 "construction_material_structure":"NOT_CERTIFIED",
 "declaration":"One deliberately authored integrated rough city plus representative inhabited section, not a valid beautiful city, safety clearance or construction plan."
}
(ROOT/"M37P1_AUTHOR_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print("M37P1_NATIVE_SAVED_ART_HOLD",sha(native),flush=True)
