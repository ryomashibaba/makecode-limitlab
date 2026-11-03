#!/usr/bin/env python3
"""Cloud AI-authored native bpy urban/lived scene, ART HOLD, NOT interactive GUI."""
from pathlib import Path
from math import pi,sin,cos,radians
import hashlib,json,math,sys

PARENT=Path("artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend")
PARENT_SHA="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
TAG="CLOUD_AI_BPY_NATIVE_DIRECT_EDIT_NOT_GUI_NOT_ART"
COLLECTIONS={"urban":"P2_CITY_MACRO_DIRECT_AUTHOR",
 "public":"P2_INHABITED_SECTION_DIRECT_AUTHOR",
 "factory":"P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
 "culture":"P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
 "home":"P2_HABITAT_PRIVATE_DIRECT_AUTHOR"}
CAMERAS={
 "AERIAL":((192,-186,153),(0,0,35),31),
 "PUBLIC_EYE":((24,-69,18),(54,0,18),28),
 "HABITAT_EYE":((-75,45,41),(-54,30,41),27),
 "CULTURE_EYE":((-60,-64,18),(-47,-36,16),29)}
def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()
def parent_ok():
    if not PARENT.is_file() or sha(PARENT)!=PARENT_SHA:
        raise RuntimeError("PROTECTED_V3_NATIVE_PARENT_HASH_REJECT")
def material(name,col,metal=0,rough=.55):
    import bpy
    m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(*col,1)
    p.inputs["Metallic"].default_value=metal
    p.inputs["Roughness"].default_value=rough
    return m
def make_mesh(name,vs,fs,coll,mat):
    import bpy
    d=bpy.data.meshes.new(name+"_real_mesh");d.from_pydata(vs,[],fs);d.update()
    o=bpy.data.objects.new(name,d);coll.objects.link(o);d.materials.append(mat)
    o["P2_AUTHOR_SOURCE"]=TAG
    return o
def skin(name,rings,coll,mat):
    n=len(rings[0]);assert n>=3 and len(rings)>=2
    assert all(len(row)==n for row in rings)
    vertices=[tuple(p) for row in rings for p in row]
    faces=[tuple(range(n-1,-1,-1))]
    for k in range(len(rings)-1):
        for j in range(n):
            p=k*n+j;q=k*n+(j+1)%n
            faces.append((p,q,q+n,p+n))
    faces.append(tuple((len(rings)-1)*n+j for j in range(n)))
    return make_mesh(name,vertices,faces,coll,mat)
def solid(name,poly,z0,z1,coll,mat):
    return skin(name,[[(x,y,z0) for x,y in poly],
                      [(x,y,z1) for x,y in poly]],coll,mat)
def room(name,x0,y0,z0,x1,y1,z1,c,m):
    return solid(name,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1,c,m)
def beam(name,a,b,thick,c,m):
    import bpy
    from mathutils import Vector
    x,y=Vector(a),Vector(b);axis=y-x
    if axis.length<.01:raise RuntimeError("ZERO_BEAM")
    bpy.ops.mesh.primitive_cube_add(size=1,location=(x+y)/2)
    o=bpy.context.object;o.name=name;o.dimensions=(thick,thick,axis.length)
    o.rotation_euler=axis.to_track_quat("Z","Y").to_euler()
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    for old in list(o.users_collection):old.objects.unlink(o)
    c.objects.link(o);o.data.materials.append(m)
    o["P2_AUTHOR_SOURCE"]=TAG
    return o
def walkway(name,pts,width,c,m):
    rows=[]
    for i,(x,y,z) in enumerate(pts):
        aa=pts[max(0,i-1)];bb=pts[min(len(pts)-1,i+1)]
        dx=bb[0]-aa[0];dy=bb[1]-aa[1];scale=math.hypot(dx,dy)
        nx=-dy/scale*width/2;ny=dx/scale*width/2
        rows.append(((x+nx,y+ny,z),(x-nx,y-ny,z),
                     (x-nx,y-ny,z-1),(x+nx,y+ny,z-1)))
    return skin(name,rows,c,m)
def tower(name,x,y,height,r,twist,c,metal,glass):
    # Unique interlocking city elevations, no rectangular facade arrays.
    n=9;levels=(0,.26,.58,.82,1)
    radii=(r,r*1.12,r*.86,r*1.03,r*.49)
    rings=[]
    for k,t in enumerate(levels):
        row=[]
        for i in range(n):
            a=2*pi*i/n+twist+t*(.24 if twist>.3 else -.21)
            f=1+.11*sin(1.7*i+k*.45+twist)
            row.append((x+2.2*t*cos(twist)+radii[k]*f*cos(a),
                        y+2.0*t*sin(twist)+radii[k]*f*sin(a),
                        height*t+.3*sin(i+twist)))
        rings.append(row)
    skin(name+"_ARTICULATED_CITY_MASS",rings,c,metal)
    for j in (1,2,3):
        for i in (0,3,6):
            a,b=rings[j][i],rings[j][(i+1)%n]
            beam(name+"_READABLE_GLAZED_FRAME_"+str(j)+"_"+str(i),
                 (a[0],a[1],a[2]-4),(a[0],a[1],a[2]+4),.38,c,glass)
def ship(name,c,iron,copper):
    cx,cz=55,17
    rings=[]
    for y,s in ((-37,.2),(-30,.60),(-19,.93),(-3,1),(14,.94),(30,.53),(42,.04)):
        rings.append([(cx+9*s*cos(2*pi*i/16),y,cz+6*s*sin(2*pi*i/16))
                     for i in range(16)])
    skin(name+"_HULL_IN_ACTIVE_ASSEMBLY",rings,c,iron)
    for k,(dx,dz) in enumerate(((-4,-2),(4,-2),(0,2.6))):
        rows=[]
        for y,r in ((-40,2.8),(-37,2.4),(-34,1.5),(-31,1.6)):
            rows.append([(cx+dx+r*cos(2*pi*i/12),y,
                          cz+dz+r*sin(2*pi*i/12)) for i in range(12)])
        skin(name+"_ACTUAL_ENGINE_BELL_"+str(k),rows,c,copper)
    for k,y in enumerate((-24,-5,22)):
        for x in (47,63):
            beam(name+"_HULL_ALIGNMENT_CRADLE_"+str(k)+"_"+str(x),
                 (x,y,3),(x+(55-x)*.2,y,11),1.4,c,copper)
def build(dest):
    import bpy
    from mathutils import Vector
    parent_ok()
    dest=Path(dest).resolve()
    if dest.exists() or dest==PARENT.resolve():
        raise RuntimeError("CLOUD_NEW_NATIVE_OUTPUT_MUST_BE_APPEND_ONLY")
    bpy.ops.wm.open_mainfile(filepath=str(PARENT.resolve()))
    s=bpy.context.scene
    if any(o.type=="MESH" for o in s.objects):raise RuntimeError("V3_NOT_EMPTY")
    if s.get("P2_ART")!="HOLD" or s.get("P2_OFFICIAL_ADOPTIONS")!=0:
        raise RuntimeError("ART_CHARTER_INVALID")
    coll={k:bpy.data.collections.get(v) for k,v in COLLECTIONS.items()}
    if any(v is None for v in coll.values()):raise RuntimeError("FIVE_GROUPS_MISSING")
    basalt=material("CLOUD_WEST_EAST_BASALT",(.11,.15,.20))
    bone=material("CLOUD_CIVIC_BONE",(.67,.66,.57))
    glass=material("CLOUD_REFLECTIVE_SAPPHIRE",(.11,.40,.48),.4,.15)
    iron=material("CLOUD_SPACECRAFT_TITANIUM",(.57,.66,.71),.72,.24)
    copper=material("CLOUD_LIFTING_AMBER",(.72,.34,.09),.7,.28)
    navy=material("CLOUD_CIVIC_BLUE",(.035,.10,.15),.7)
    wood=material("CLOUD_WARM_HABITAT",(.48,.28,.16))
    cloth=material("CLOUD_PRIVATE_BLUE",(.14,.24,.38))
    foliage=material("CLOUD_COMMUNITY_GARDEN",(.16,.39,.22))
    water=material("CLOUD_HARBOUR_WATER",(.04,.22,.29),.55,.17)
    # City-specific asymmetric banks / a clear harbor rather than disconnected campus.
    solid("WEST_URBAN_TOPOGRAPHIC_BANK",
          [(-135,-116),(-37,-116),(-31,-68),(-41,-8),(-33,55),(-40,118),(-135,118)],
          -4,0,coll["urban"],basalt)
    solid("EAST_URBAN_TOPOGRAPHIC_BANK",
          [(23,-116),(140,-116),(140,118),(27,118),(25,62),(18,9),(26,-59)],
          -4,0,coll["urban"],basalt)
    solid("HARBOR_WATER_REAL_DEPTH_CONTEXT",
          [(-30,-114),(21,-114),(21,114),(-30,114)],-3,-1.6,coll["urban"],water)
    # Unlike failed homogeneous boxes, each authored neighborhood has a unique
    # warped section, nonidentical height, occupancy silhouette, and linkage.
    districts=[
      ("CIVIC_GATE",-106,-87,47,13,.12),("MAKER_LOFTS",-79,-78,59,14,.66),
      ("CULTURE_LANTERN",-113,-30,68,15,.32),("SCIENCE_TERRACE",-89,-6,78,13,.24),
      ("INHABITED_SKY",-110,47,94,12,.52),("EDUCATION_RISE",-86,88,61,14,.18),
      ("STREET_MOUTH",-47,90,52,12,.83),("MAKER_GATE",92,-87,79,14,.11),
      ("PORT_DWELLINGS",118,-33,65,14,.62),("SHIPWRIGHT_HOMES",108,15,89,13,.71),
      ("HIGH_LAB",91,62,84,15,.45),("PUBLIC_ARCHIVE",127,99,55,12,.38)]
    for vals in districts:
        tower(*vals,coll["urban"],bone,glass)
    walkway("WEST_DENSE_CITY_PEDESTRIAN_AXIS",
        [(-132,-106,3),(-106,-83,5),(-91,-55,7),(-84,-25,9),(-77,5,12),
         (-84,44,16),(-87,80,11),(-61,107,9)],8,coll["urban"],bone)
    walkway("EAST_DENSE_CITY_WORKING_STREET",
        [(135,-107,4),(111,-80,5),(96,-49,6),(91,-15,9),
         (89,23,11),(92,60,9),(117,106,8)],8,coll["urban"],bone)
    # Directly model actual spacecraft manufacture and separable visitors.
    room("SHIPYARD_ACTUAL_FABRICATION_FLOOR",35,-57,1,76,49,3,coll["factory"],bone)
    ship("SPACECRAFT",coll["factory"],iron,copper)
    for i,y in enumerate((-35,0,35)):
        for x in (35,76):
            beam("GANTRY_REAL_LEG_%s_%s"%(i,x),(x,y,3),(x,y,45),1.3,coll["factory"],navy)
        beam("GANTRY_TRANSFER_CRANE_"+str(i),(35,y,45),(76,y,45),1.3,coll["factory"],copper)
        beam("GANTRY_CHAIN_"+str(i),(54,y,45),(54,y,25),.37,coll["factory"],iron)
    for i,(a,b,d) in enumerate((
        ((75,-24,5),(69,-15,17),(61,-11,20)),
        ((36,18,5),(41,14,21),(47,12,20)),
        ((71,33,5),(65,25,20),(60,22,21)))):
        beam("ACTIVE_ROBOT_SHOULDER_"+str(i),a,b,1.4,coll["factory"],copper)
        beam("ACTIVE_ROBOT_ELBOW_"+str(i),b,d,.76,coll["factory"],iron)
    room("PUBLIC_VISITOR_REAL_GALLERY",21,-57,8,30,48,10,coll["factory"],wood)
    for y in (-49,-38,-27,-16,-5,6,17,28,39):
        room("PUBLIC_STAFF_REAL_GLASS_BARRIER_"+str(y),
             30,y,10,30.24,y+9,23,coll["factory"],glass)
        beam("PUBLIC_STAFF_RAIL_"+str(y),(30,y,10),(30,y,23),.24,
             coll["factory"],copper)
    walkway("WORKERS_PROTECTED_TRANSFER_ROUTE",
        [(73,-54,5),(80,-30,5),(82,4,5),(80,34,6)],4,coll["factory"],bone)
    # Research AND culture are physically furnished, not just usage labels.
    room("RESEARCH_CULTURE_ACTUAL_OCCUPIED_FLOOR",-74,-59,10,-27,-16,11,
         coll["culture"],wood)
    room("RESEARCH_DAYLIGHT_SKYLIGHT",-71,-19,32,-32,-18.6,35,
         coll["culture"],glass)
    for k,(x,y) in enumerate(((-67,-54),(-54,-53),(-41,-51),(-67,-38),(-54,-36),(-41,-35))):
        room("RESEARCH_REAL_BENCH_"+str(k),x,y,11,x+7,y+2.6,13,
             coll["culture"],bone)
        room("RESEARCH_COMPUTER_"+str(k),x+2,y+1,13,x+3.3,y+1.4,15,
             coll["culture"],navy)
        room("RESEARCH_WORKER_CHAIR_"+str(k),x+2,y-2,11,x+4,y-1,12,
             coll["culture"],cloth)
    for i in range(5):
        yy=-22+i*4
        room("PUBLIC_CULTURE_REAL_BOOKSHELF_"+str(i),
             -69,yy,11,-67,yy+3,20,coll["culture"],wood)
        room("PUBLIC_CULTURE_READING_TABLE_"+str(i),
             -61,yy,11,-55,yy+2.5,12.3,coll["culture"],bone)
    walkway("LEARNING_ACCESS_TO_SEPARATE_FACTORY_GALLERY",
      [(-58,-29,13),(-38,-34,13),(-18,-51,12),(4,-61,11),(25,-57,10)],
      4,coll["public"],wood)
    # A genuinely occupied home: entrance -> vestibule -> dining/living,
    # private bed, kitchen, window towards the harbour, shared sky threshold.
    room("HOME_LIVEABLE_REAL_FLOOR",-84,20,35,-45,56,36,coll["home"],wood)
    room("HOME_REAL_ENTRY_THRESHOLD",-84,51,36,-76,51.6,44,coll["home"],bone)
    room("HOME_REAL_PRIVATE_VESTIBULE_SCREEN",-76,40,36,-75.6,52,44,
         coll["home"],cloth)
    room("HOME_KITCHEN_REAL_COUNTER",-68,21,36,-52,25,39,coll["home"],bone)
    room("HOME_KITCHEN_SINK",-57,23,39,-54,24,39.2,coll["home"],navy)
    room("HOME_ACTUAL_DINING_TABLE",-70,31,36,-61,36,38,coll["home"],wood)
    for i,(x,y) in enumerate(((-73,30),(-60,30),(-73,36),(-60,36))):
        room("HOME_DINING_CHAIR_"+str(i),x,y,36,x+2,y+1.5,37.4,
             coll["home"],cloth)
    room("HOME_ACTUAL_LIVING_SOFA",-57,44,36,-46,49,39,coll["home"],cloth)
    room("HOME_REAL_BED",-83,21,36,-72,29,38,coll["home"],cloth)
    room("HOME_SLEEPING_PRIVACY_PARTITION",-70,20,36,-69.5,33,45,
         coll["home"],wood)
    for i,y in enumerate((21,30,39,48)):
        room("HOME_HARBOR_VIEW_ACTUAL_WINDOW_"+str(i),
             -45.6,y,36,-45.3,y+7.2,46,coll["home"],glass)
    room("HOME_CEILING",-84,20,47,-47,56,47.7,coll["home"],bone)
    walkway("SAME_CITY_SHARED_RESIDENTIAL_SKY_TERRACE",
       [(-88,84,26),(-80,66,30),(-70,55,35),(-60,53,36),(-43,47,32),(-24,32,24)],
       5,coll["public"],bone)
    for k,(x,y) in enumerate(((-79,65),(-65,53),(-44,46))):
        room("ACTUAL_RESIDENT_COMMUNITY_PLANTED_BED_"+str(k),
             x-2.8,y-1.8,36,x+2.8,y+1.8,36.5,coll["public"],foliage)
    s.world.use_nodes=True
    bg=s.world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value=(.30,.40,.54,1)
    bg.inputs["Strength"].default_value=.75
    sun=bpy.data.lights.new("ART_HOLD_STUDY_TRUE_SUN","SUN");sun.energy=2
    lamp=bpy.data.objects.new("ART_HOLD_STUDY_TRUE_SUN",sun);s.collection.objects.link(lamp)
    lamp.rotation_euler=(radians(35),radians(-25),radians(-40))
    for name,pos,power in (("HANGAR",(47,-2,64),7500),
                           ("LIVED_HOME",(-65,27,54),2400),
                           ("CULTURE",(-48,-34,45),2600)):
        l=bpy.data.lights.new(name,"AREA");l.energy=power;l.size=38
        o=bpy.data.objects.new(name,l);s.collection.objects.link(o);o.location=pos
        o.rotation_euler=(Vector((0,0,12))-o.location).to_track_quat("-Z","Y").to_euler()
    for name,(pos,target,lens) in CAMERAS.items():
        ob=bpy.data.objects.get("P2_CAMERA_"+name)
        if ob is None:
            d=bpy.data.cameras.new("P2_CAMERA_"+name+"_DATA")
            ob=bpy.data.objects.new("P2_CAMERA_"+name,d)
            bpy.data.collections["P2_CAMERA_RIG_NOT_ART"].objects.link(ob)
        ob.location=pos
        ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
        ob.data.lens=lens
        ob["P2_CAMERA_STATUS"]="CLOUD_AI_POSITIONED_NOT_HUMAN_APPROVED"
    s.camera=bpy.data.objects["P2_CAMERA_AERIAL"]
    s["P2_SOURCE_KIND"]=TAG
    s["P2_STUDIO_STAGE"]="CLOUD_BPY_AI_AUTHORED_ACTUAL_SPATIAL_STUDY_UNAPPROVED"
    s["P2_PARENT_SOURCE_SHA256"]=PARENT_SHA
    s["P2_CLOUD_AUTHOR_NOT_GUI"]=True
    s["P2_CAMERA_VIEWS_AUTHOR_APPROVED"]=False
    s["P2_ART"]="HOLD";s["P2_OFFICIAL_ADOPTIONS"]=0
    s["P2_FORMAL_331_993"]="NOT_RUN";s["P2_MINECRAFT"]="FORBIDDEN"
    s["P2_MAKECODE_COST"]="NOT_EVALUATED"
    s.render.engine="CYCLES";s.render.resolution_x=960;s.render.resolution_y=600
    s.render.resolution_percentage=100
    bpy.data.texts.new("CLOUD_BPY_DIRECT_EDIT_NOT_GUI_ART_HOLD_JA.txt").write(
      "Cloud AI wrote the explicit 3D composition; Blender bpy executed real "
      "native modifications of an immutable v3 source COPY. This was NOT a GUI "
      "mouse-operated artist, NOT human-approved art, NOT safety certified. "
      "Formal 331/993 and G0/S1/G1/G2/G3 NOT RUN; Minecraft FORBIDDEN.")
    dest.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
    if sha(PARENT)!=PARENT_SHA:raise RuntimeError("PROTECTED_PARENT_CHANGED")
    print("GENUINE_CLOUD_BPY_EDIT_SAVED_NOT_ART",sha(dest),flush=True)
def review(path):
    import bpy
    output=Path(path)
    if output.exists():raise RuntimeError("APPEND_ONLY_REVIEW_EXISTS")
    output.mkdir(parents=True)
    parent_ok()
    s=bpy.context.scene
    native=Path(bpy.data.filepath)
    if not native.is_file() or native.resolve()==PARENT.resolve():
        raise RuntimeError("REAL_SEPARATE_SAVED_BLEND_REQUIRED")
    before=sha(native)
    req={"P2_SOURCE_KIND":TAG,"P2_PARENT_SOURCE_SHA256":PARENT_SHA,
         "P2_CLOUD_AUTHOR_NOT_GUI":True,"P2_CAMERA_VIEWS_AUTHOR_APPROVED":False,
         "P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,
         "P2_FORMAL_331_993":"NOT_RUN","P2_MINECRAFT":"FORBIDDEN"}
    for key,val in req.items():
        if s.get(key)!=val:raise RuntimeError("CHARTER_REJECT_"+key)
    counts={}
    for key,colname in COLLECTIONS.items():
        c=bpy.data.collections.get(colname)
        objs=[o for o in c.all_objects if o.type=="MESH" and len(o.data.vertices)>0]
        counts[key]={"meshes":len(objs),"vertices":sum(len(o.data.vertices) for o in objs)}
        if len(objs)<(10 if key=="urban" else 5):
            raise RuntimeError("REAL_SPATIAL_COLLECTION_INCOMPLETE_"+key)
    required=("SPACECRAFT_HULL_IN_ACTIVE_ASSEMBLY",
       "PUBLIC_VISITOR_REAL_GALLERY","PUBLIC_STAFF_REAL_GLASS_BARRIER_-49",
       "RESEARCH_REAL_BENCH_0","PUBLIC_CULTURE_REAL_BOOKSHELF_0",
       "HOME_REAL_ENTRY_THRESHOLD","HOME_ACTUAL_LIVING_SOFA","HOME_REAL_BED")
    if any(bpy.data.objects.get(name) is None for name in required):
        raise RuntimeError("REAL_LIVED_MANUFACTURING_SPACE_MISSING")
    s.render.engine="CYCLES";s.cycles.samples=16
    s.render.resolution_x=960;s.render.resolution_y=600
    s.render.resolution_percentage=100;s.render.image_settings.file_format="PNG"
    images={}
    for name in CAMERAS:
        s.camera=bpy.data.objects["P2_CAMERA_"+name]
        img=output/("M37P2_"+name+".png")
        s.render.filepath=str(img)
        bpy.ops.render.render(write_still=True)
        if not img.exists() or img.stat().st_size<5000:raise RuntimeError("RENDER_FAILED_"+name)
        # Blender ships its own Python: do not assume system python3-pil is
        # installed inside the official Blender interpreter.
        from array import array
        picture=bpy.data.images.load(str(img),check_existing=False)
        try:
            if tuple(picture.size)!=(960,600):
                raise RuntimeError("RENDER_RESOLUTION_MISMATCH_"+name)
            channels=picture.channels
            raw=array("f",[0.0])*len(picture.pixels)
            picture.pixels.foreach_get(raw)
            stride=channels*16
            samples=range(0,len(raw)-channels+1,stride)
            visible=sum(max(raw[i:i+3])>.08 for i in samples)/len(samples)
        finally:
            bpy.data.images.remove(picture)
        if visible<.04:raise RuntimeError("TRUE_RENDER_BLACK_"+name)
        images[name]={"sha256":sha(img),"visible_fraction":round(visible,4),"bytes":img.stat().st_size}
    if sha(native)!=before or sha(PARENT)!=PARENT_SHA:
        raise RuntimeError("NATIVE_ORIGINAL_MODIFIED")
    report={"schema":"g4c7-cloud-bpy-art-hold-v1",
      "technical_status":"REAL_BLENDER_REOPEN_AND_RENDER_EVIDENCE",
      "absolute_art":"HOLD_HUMAN_CRITIQUE_REQUIRED","adoptions":0,
      "provenance":"CLOUD_AI_SCRIPTED_NATIVE_BPY_DIRECT_EDIT_NOT_INTERACTIVE_GUI",
      "native_blend_sha256":before,"v3_protected_sha256":PARENT_SHA,
      "native_collections":counts,"four_genuine_cycles_views":images,
      "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
      "MakeCode":"NOT_EVALUATED","Minecraft":"FORBIDDEN"}
    (output/"M37P2_CLOUD_AUTHOR_EVIDENCE_ART_HOLD.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n","utf8")
    lines=["# M37-P2 真正Blenderクラウド作者研究 / ART HOLD","",
      "AIが設計したbpyコードで保護原本のコピーを直接編集。GUI直接操作や美術完成ではありません。","",
      "正式採用0、331/993 NOT RUN、MakeCode NOT EVALUATED、Minecraft施工禁止。",""]
    for name in CAMERAS:
        lines+=["## "+name,"","![real Cycles "+name+"](M37P2_"+name+".png)",""]
    (output/"README_ART_HOLD.md").write_text("\n".join(lines)+"\n","utf8")
    print("FOUR_GENUINE_REAL_NATIVE_CYCLES_ART_HOLD",json.dumps(images),flush=True)
def main():
    args=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    if len(args)!=2:raise SystemExit("Expected --build OUTPUT.blend or --review EMPTY_DIR")
    if args[0]=="--build":build(args[1])
    elif args[0]=="--review":review(args[1])
    else:raise SystemExit("INVALID_OPERATION")
if __name__=="__main__":main()
