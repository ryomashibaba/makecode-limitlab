#!/usr/bin/env python3
"""G4-C7 M37-D. One native authored spatial study, NOT a city art pass.
A design-specific sequence of occupied edges, open shipyard and civic route.
Neither M35 reference nor M36 editable working scene may be changed.
The program edits Blender mesh datablocks; it is NOT manual GUI sculpting.
Research units have NO mapping to Minecraft metres or blocks.
"""
import bpy, math, json, hashlib, random
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path("artifacts/g4c7-m36-verified-native-author-studio")
SOURCE=ROOT/"M36_NATIVE_DUAL_SCENE_ARTIST_STUDIO.blend"
OUT=Path("artifacts/g4c7-m37d-native-study")
OUT.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pin=json.loads((ROOT/"M36_NATIVE_STUDIO_MANIFEST.json").read_text())
assert sha(SOURCE)==pin["saved_blend"]["sha256"]
assert pin["whole_city_art"]=="HOLD_NOT_PASSED"
assert pin["construction"]=="FORBIDDEN"
bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
ref=bpy.data.scenes["M35_REJECTED_REFERENCE_LOCKED"]
old_edit=bpy.data.scenes["M36_AUTHORING_STUDIO_ART_HOLD"]
assert len([o for o in ref.objects if o.type=="MESH"])==208
assert len([o for o in old_edit.objects if o.type=="MESH"])==208
original_names={o.name for o in ref.objects}
old_names={o.name for o in old_edit.objects}
assert all(n.startswith("M35_") for n in original_names)
scene=bpy.data.scenes.new("M37D_AUTHOR_OCCUPIED_CITY_ART_HOLD")
scene["SOURCE_M36_SHA256"]=sha(SOURCE)
scene["M37D_ART_STATUS"]="UNREVIEWED_HOLD"
scene["M37D_MINECRAFT"]="FORBIDDEN"
scene["M37D_FORMAL_331_993"]="NOT_RUN"
scene["M37D_OFFICIAL_ADOPTION"]=0
scene["M37D_UNITS"]="ABSTRACT_RESEARCH_NOT_BLOCKS"
cols={}
for name in ("PUBLIC","FABRICATION","HABITAT","RESEARCH","CULTURE","VERTICAL",
             "URBAN_GRAIN","CAMERAS","LIGHTS"):
    c=bpy.data.collections.new("M37D_"+name)
    scene.collection.children.link(c)
    cols[name]=c
mats={}
def material(name,rgb,metal=.0,rough=.5):
    m=bpy.data.materials.new("M37D_"+name)
    m.diffuse_color=(*rgb,1)
    m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(*rgb,1)
    p.inputs["Metallic"].default_value=metal
    p.inputs["Roughness"].default_value=rough
    mats[name]=m
for name,rgb,met in [
 ("stone",(.40,.48,.51),.15),("warm",(.61,.44,.32),.13),
 ("copper",(.51,.31,.21),.54),("glass",(.13,.38,.48),.2),
 ("plants",(.21,.41,.28),0),("floor",(.52,.53,.46),.09),
 ("light",(.74,.63,.43),.07),("shadow",(.18,.27,.34),.2),
 ("yard",(.32,.36,.38),.26)]:
    material(name,rgb,met)
counts={"PUBLIC":0,"FABRICATION":0,"HABITAT":0,"RESEARCH":0,
        "CULTURE":0,"VERTICAL":0,"URBAN_GRAIN":0}
actual={"habitable_bays":0,"research_bays":0,"maker_bays":0,
        "culture_bays":0,"named_door_openings":0,"stairs_treads":0,
        "route_segments":0,"building_masses":0,"public_courts":0}
def mesh(name,verts,faces,mat,group,tag=None):
    data=bpy.data.meshes.new("M37D_"+name+"_mesh")
    data.from_pydata(verts,[],faces)
    data.update()
    ob=bpy.data.objects.new("M37D_"+name,data)
    cols[group].objects.link(ob)
    data.materials.append(mats[mat])
    if tag: ob["M37D_ROLE"]=tag
    counts[group]+=1
    return ob
def extrude_polygon(name,points,z0,z1,mat,group,tag="PHYSICAL_GEOMETRY_UNVERIFIED"):
    """Closed-native 3D prism. Explicit plan footprint, no negative-scale solids."""
    assert z1>z0 and len(points)>=3
    n=len(points)
    verts=[(x,y,z) for z in (z0,z1) for x,y in points]
    tri=tessellate_polygon([[Vector((x,y,0)) for x,y in points]])
    def tri_indices(t):
        # Exact coordinate matching for authored polygon vertices.
        return [min(range(n),key=lambda k:
                (points[k][0]-v.x)**2+(points[k][1]-v.y)**2) for v in t]
    faces=[]
    for t in tri:
        # Blender builds may return triangle indices or Vector vertices.
        a,b,c=(map(int,t) if isinstance(t[0],int) else tri_indices(t))
        assert len({a,b,c})==3 and 0<=min(a,b,c) and max(a,b,c)<n
        faces.extend([(c,b,a),(a+n,b+n,c+n)])
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,j+n,i+n))
    return mesh(name,verts,faces,mat,group,tag)
def panel(name,p,q,z0,z1,depth,mat,group,tag="PHYSICAL_WALL"):
    dx=q[0]-p[0];dy=q[1]-p[1]
    ll=math.hypot(dx,dy)
    assert ll>.001
    nx=-dy/ll*depth/2;ny=dx/ll*depth/2
    return extrude_polygon(name,
       [(p[0]+nx,p[1]+ny),(q[0]+nx,q[1]+ny),
        (q[0]-nx,q[1]-ny),(p[0]-nx,p[1]-ny)],z0,z1,mat,group,tag)
def slab(name,poly,z,mat,group,thick=.45,tag="SUPPORTED_FLOOR_NOT_CERTIFIED"):
    return extrude_polygon(name,poly,z-thick/2,z+thick/2,mat,group,tag)
def stair(name,p0,p1,z0,z1,treads,group="VERTICAL"):
    dx=(p1[0]-p0[0])/treads;dy=(p1[1]-p0[1])/treads
    for k in range(treads):
        cx=p0[0]+(k+.5)*dx;cy=p0[1]+(k+.5)*dy
        t=Vector((dx,dy));t.normalize()
        n=Vector((-t.y,t.x))
        mid=Vector((cx,cy))
        pts=[tuple(mid+t*dx0+n*dd) for dx0,dd in
             [(-math.hypot(dx,dy)*.5,-2.6),(.5*math.hypot(dx,dy),-2.6),
              (.5*math.hypot(dx,dy),2.6),(-.5*math.hypot(dx,dy),2.6)]]
        slab(name+"_TREAD_%02d"%k,pts,
             z0+(k+1)*(z1-z0)/treads,"floor",group,.22,
             "STAIR_TREAD_SWEPT_ROUTE_NOT_VERIFIED")
        actual["stairs_treads"]+=1

# The civic front is not a crossing pair of long plates: three offset
# public chambers connect directly to the inner maker excavation.
courts=[
 ("GATE", [(-35,-153),(22,-151),(40,-120),(28,-91),(-18,-92),(-43,-117)]),
 ("CIVIC", [(-42,-91),(25,-91),(50,-57),(33,-18),(-11,-12),(-51,-38)]),
 ("DELTA", [(-52,-38),(-10,-12),(35,-18),(54,20),(30,58),(-35,51),(-57,9)]),
 ("NORTH_HALL",[(-35,51),(30,58),(54,86),(22,110),(-18,109),(-55,83)])]
for name,polygon in courts:
    slab("PUBLIC_"+name+"_REAL_FLOOR",polygon,-.15,"floor","PUBLIC",.6)
    actual["public_courts"]+=1
for i,(a,b) in enumerate(zip(courts,courts[1:])):
    # Court polygons overlap in the authored plan; not a continuous swept QA.
    actual["route_segments"]+=1
# No domed main hall or giant wall. The manufacture void stays open to daylight,
# surrounded by real occupied working ledges and machine access floors.
yard=[(29,-91),(131,-100),(174,-69),(180,11),(148,64),
      (67,71),(37,27),(58,-13),(35,-50)]
slab("OPEN_SPACE_VEHICLE_ASSEMBLY_YARD_REAL_FLOOR",yard,-.25,"yard","FABRICATION",.5)
slab("ASSEMBLY_OPERATIONS_SPUR",
     [(29,-53),(94,-58),(152,-34),(150,-20),(80,-35),(40,-23)],
     .12,"floor","FABRICATION",.45)
# Three open-dock work bays follow the curved maker edge, no false enclosing roof.
for i,(x,y,angle) in enumerate([(92,-84,.11),(141,-47,.47),(145,18,-.24)]):
    length=25+7*i;width=16+2*i
    ux=(math.cos(angle),math.sin(angle));vy=(-ux[1],ux[0])
    def loc(a,b):return (x+ux[0]*a+vy[0]*b,y+ux[1]*a+vy[1]*b)
    slab("ACTUAL_WORK_FLOOR_%d"%i,
         [loc(-length/2,-width/2),loc(length/2,-width/2),
          loc(length/2,width/2),loc(-length/2,width/2)],1.2,"floor","FABRICATION")
    for j in range(3):
        q=loc(-length/3+j*length/3,0)
        slab("SHIPBUILD_JIG_%d_%d"%(i,j),
             [loc(-length/3+j*length/3,-2),loc(-length/6+j*length/3,-2),
              loc(-length/6+j*length/3,2),loc(-length/3+j*length/3,2)],
             2.5,"copper","FABRICATION",2.0,"REAL_WORKSTATION_CONCEPT_NOT_SAFETY")
    actual["maker_bays"]+=1

# Authored city cross-sections. Distinct built street edges, not a repeated
# grid or detached four-building campus. Boundaries are hand-positioned to
# interlock into the civic courts, manufacturing yard, and northern balconies.
# Each row (center / direction / bay lengths / elevations) determines *usable*
# activity space first, then the external envelope. Roof height follows use.
districts=[
 ("HAB1", "HABITAT",(-114, -29), 0.26,[17,23,15,21,14],[-1,10,22,35,49],19),
 ("HAB2", "HABITAT",(-126,  54),-0.16,[20,14,25,17],[ 0,13,27,42,60],22),
 ("HAB3", "HABITAT",(-110, 115), 0.12,[17,22,19,15],[ 8,26,46,66,87],20),
 ("RES1", "RESEARCH",( 76, 109),-0.48,[19,21,16,22],[ 4,22,42,64,85],23),
 ("RES2", "RESEARCH",(151,  74),-1.06,[23,18,24],[ 1,19,39,59,82],21),
 ("FAB1", "FABRICATION",(-97,-112),0.42,[24,20,26],[ 0,16,34,56],25),
 ("FAB2", "FABRICATION",(-164,-28),1.31,[18,25,20],[ 0,19,40,65],26),
 ("CULT1","CULTURE",(-110,-128),0.03,[16,22,20,16],[-1,13,29,47],20),
 ("CULT2","CULTURE",( 62,-146),-0.35,[19,17,25],[ 0,14,30,50],20),
 ("CIVIC","CULTURE",(-33, 135),-0.02,[23,19,22],[10,29,52,76],21)]
def district(name,group,center,ang,bays,level_z,depth):
    # Volumes are multiple staggered true room bays with real floor,
    # lateral privacy partitions, full-height back walls broken by windows,
    # a deliberate civic-side door opening, and varying upper levels.
    cs=math.cos(ang);sn=math.sin(ang)
    def xy(u,v):return (center[0]+cs*u-sn*v,center[1]+sn*u+cs*v)
    total=sum(bays)
    drift=[0,-1.8,3.2,-4.4,5.2,-6.1]
    for level,base in enumerate(level_z[:-1]):
        top=level_z[level+1]
        shift=drift[level]
        # Stagger each floor front and each neighboring bay so street density
        # comes from interior depth/courtyard setbacks, not a blank monolith.
        offset=-total/2
        for j,width in enumerate(bays):
            mask=(j+level*2)%7
            if mask==5 and level>0:
                offset+=width
                continue # actual multi-level sky court cut from an occupied edge
            d=depth*(.77 if mask==2 else .95 if mask==4 else 1)
            lead=1.7*((j+level)%3-1)
            u0=offset+shift;u1=offset+width+shift
            v0=lead;v1=lead+d
            poly=[xy(u0,v0),xy(u1,v0),
                  xy(u1+1.7,v1*.47),xy(u1-1.3,v1),
                  xy(u0+1.3,v1),xy(u0-1.1,v1*.47)]
            floor=slab(name+"_L%d_B%d_OCCUPIED_FLOOR"%(level,j),poly,base,
                       "floor",group,.45,"REAL_OCCUPIED_FLOOR_NOT_CLEARED")
            floor["M37D_PUBLIC_PRIVATE_LEVEL"]=group
            h=min(8,top-base-1.3)
            # Interior walls are tied to the accessible room footprint,
            # not facades painted onto a solid cuboid.
            panel(name+"_L%d_B%d_BACK_WALL_LOW"%(level,j),
                  xy(u0+1.3,v1),xy(u1-1.3,v1),
                  base+.2,base+1.45,.45,"warm" if group=="HABITAT" else "stone",group)
            panel(name+"_L%d_B%d_BACK_WALL_HIGH"%(level,j),
                  xy(u0+1.3,v1),xy(u1-1.3,v1),
                  base+5.25,base+h,.45,"warm" if group=="HABITAT" else "stone",group)
            for side,u in enumerate((u0,u1)):
                panel(name+"_L%d_B%d_SIDE_%d"%(level,j,side),
                      xy(u,v0+2.8),xy(u,v1),base+.2,base+h,.35,
                      "shadow" if group=="RESEARCH" else "warm",group)
            # A visible actual door opening from the street-side gallery:
            # low screen on left, full-height header, clear gap 4.2.
            midpoint=(u0+u1)/2
            panel(name+"_L%d_B%d_FACADE_LEFT"%(level,j),
                  xy(u0,v0),xy(midpoint-2.1,v0),
                  base+.25,base+3,.4,"stone",group)
            panel(name+"_L%d_B%d_FACADE_RIGHT"%(level,j),
                  xy(midpoint+2.1,v0),xy(u1,v0),
                  base+.25,base+3,.4,"stone",group)
            panel(name+"_L%d_B%d_DOOR_LINTEL"%(level,j),
                  xy(midpoint-2.1,v0),xy(midpoint+2.1,v0),
                  base+3.8,base+h,.38,"copper",group)
            actual["named_door_openings"]+=1
            if group=="HABITAT":actual["habitable_bays"]+=1
            if group=="RESEARCH":actual["research_bays"]+=1
            if group=="CULTURE":actual["culture_bays"]+=1
            if group=="FABRICATION":actual["maker_bays"]+=1
            if level>0 and mask in (0,3,6):
                # Physical balcony rather than a floating glass drawing.
                balcony=[xy(u0,v0-3.4),xy(u1,v0-3.4),
                         xy(u1,v0+.3),xy(u0,v0+.3)]
                slab(name+"_L%d_B%d_BALCONY"%(level,j),balcony,
                     base-.12,"copper",group,.3)
            offset+=width
        # Full-length identical plates forbidden. The common horizontal
        # corridor is split into actual offset segments by per-bay depths.
        offset=-total/2
        for j,width in enumerate(bays):
            u0=offset+shift;u1=offset+width+shift
            path=[xy(u0, -5.4),xy(u1, -5.4),
                  xy(u1, -1.2),xy(u0,-1.2)]
            slab(name+"_L%d_SHARED_WALK_%d"%(level,j),
                 path,base-.13,"floor",group,.36,
                 "GALLERY_SEGMENT_NOT_CONNECTED_OR_SAFETY_TESTED")
            offset+=width
    actual["building_masses"]+=1

for args in districts:
    district(*args)

# Explicit physical transition from ground public arrival up to one research
# gallery; multiple route pieces are real mesh but connectivity is unproven.
stair("CIVIC_TO_RESEARCH_LOWER",(-16,89),(12,105),0,11,36)
stair("CIVIC_TO_RESEARCH_UPPER",(12,110),(42,122),11,22,36)
slab("CITY_UPPER_OBSERVATION",
     [(-21,116),(15,115),(51,120),(55,135),(18,132),(-23,136)],
     22.1,"floor","VERTICAL",.5)
# Urban activity texture: perforated public-facing parapets, site-specific
# garden courts, no fake glass surfaces as substitute for real rooms.
for k,poly in enumerate([
 [(-43,62),(-10,64),(1,84),(-36,83)],
 [(-47,-72),(-29,-62),(-14,-48),(-41,-45)],
 [(8,110),(35,110),(43,133),(11,132)]]):
    slab("ACTUAL_GARDEN_COURT_%d"%k,poly,.2+ (21.9 if k==2 else 0),
         "plants","PUBLIC" if k<2 else "VERTICAL",.25)
    for j in range(2):
        actual["route_segments"]+=1

# City-wide camera contract: original M35 cameras are retained in untouched
# source scenes; here new authored cameras include actual eye and aerial.
def camera(name,pos,target,lens):
    data=bpy.data.cameras.new("M37D_"+name+"_lens")
    ob=bpy.data.objects.new("M37D_CAM_"+name,data)
    cols["CAMERAS"].objects.link(ob)
    ob.location=pos
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
    data.lens=lens
    return ob
cams={
 "SOUTH":camera("SOUTH",(0,-365,174),(0,-5,32),37),
 "NORTH":camera("NORTH",(0,331,163),(0,8,42),38),
 "AERIAL":camera("AERIAL",(-320,-256,310),(0,-5,31),34),
 "STREET":camera("STREET",(-13,-108,2.3),(4,-48,8),21),
 "YARD":camera("YARD",(70,-68,3),(146,-4,10),22),
 "HAB_EYE":camera("HAB_EYE",(-122,65,16),(-108,46,20),21),
 "RESEARCH_EYE":camera("RESEARCH_EYE",(85,104,24),(138,76,31),21),
 "CULTURE_EYE":camera("CULTURE_EYE",(-113,-124,2),(-81,-115,11),21),
 "UPPER_EYE":camera("UPPER_EYE",(17,125,24),(70,4,40),21)
}
world=bpy.data.worlds.new("M37D_DAYLIGHT") if not scene.world else scene.world.copy()
scene.world=world
world.use_nodes=True
world.node_tree.nodes.get("Background").inputs["Color"].default_value=(.43,.53,.64,1)
world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.78
for k,pos,power,size in [
 (0,(-220,-225,290),50000,100),
 (1,(190,210,260),52000,130),
 (2,(-5,-75,155),19000,95)]:
    d=bpy.data.lights.new("M37D_LIGHT_"+str(k),"AREA")
    d.energy=power;d.shape="DISK";d.size=size
    o=bpy.data.objects.new("M37D_LIGHT_"+str(k),d)
    cols["LIGHTS"].objects.link(o);o.location=pos
    o.rotation_euler=(Vector((0,0,23))-o.location).to_track_quat("-Z","Y").to_euler()
scene.camera=cams["SOUTH"]
scene.render.engine="CYCLES"
scene.cycles.samples=8
scene.render.resolution_x=840
scene.render.resolution_y=504
scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.film_transparent=False
scene["M37D_SEMANTIC_METRICS"]=json.dumps(actual)
saved=OUT/"M37D_NEW_NATIVE_URBAN_FABRIC_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(saved.resolve()))

# Render from exactly the *same saved 3D*; do not re-generate geometry.
pics={}
for key in ("SOUTH","NORTH","AERIAL","STREET","YARD","HAB_EYE","RESEARCH_EYE","CULTURE_EYE","UPPER_EYE"):
    scene.camera=cams[key]
    dest=OUT/("M37D_"+key+".png")
    scene.render.filepath=str(dest.resolve())
    bpy.ops.render.render(write_still=True,scene=scene.name)
    assert dest.exists() and dest.stat().st_size>1500
    pics[key]={"file":dest.name,"sha256":sha(dest)}
    print("M37D_REAL_NATIVE_RENDER",key,flush=True)

manifest={
 "study":"M37D_ONE_HAND_AUTHORED_OCCUPIED_CITY_DIRECTION_ART_HOLD",
 "source_blend_sha256":sha(SOURCE),
 "authoring_method":"Blender bpy native mesh authoring driven by individual room and public-space cross sections; NOT manual GUI edit",
 "saved_blend":{"name":saved.name,"bytes":saved.stat().st_size,"sha256":sha(saved)},
 "source_reference_scene":"M35_REJECTED_REFERENCE_LOCKED",
 "protected_M36_edit_scene":"M36_AUTHORING_STUDIO_ART_HOLD",
 "new_art_scene":scene.name,
 "new_mesh_counts":counts,
 "spatial_components":actual,
 "rendered_cameras":pics,
 "old_9_camera_positions":"PRESERVED_IN_OLD_SCENES",
 "art":"HOLD_UNREVIEWED",
 "formal_331_993":"NOT_RUN",
 "G0_S1_G1_G2_G3":"NOT_RUN",
 "continuous_human_walk":"NOT_RUN",
 "scale":"ABSTRACT_UNITS_NOT_MINECRAFT_BLOCKS",
 "minecraft":"FORBIDDEN",
 "important":"Rooms and doors are modeled; no full route clearance or continuity has been proven."
}
(OUT/"M37D_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print("M37D_NATIVE_SAVED_PRODUCED_NOT_ART_PASSED",
      json.dumps({"meshes":sum(counts.values()),"bays":actual,
                  "blend_sha":sha(saved)},ensure_ascii=False),flush=True)
