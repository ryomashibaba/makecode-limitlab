#!/usr/bin/env python3
"""G4-C7 R1: a first authored urban-material study, NEVER ART PASS or safety evidence.

Authoring is code-assisted with individually specified districts and manually
composed inhabited/industrial section. It MUST NOT be called autonomous expert
GUI sculpting; one subsequent real VIEW_3D move is separately proven.
"""
import bpy, math, sys, os
from mathutils import Vector
from pathlib import Path
from math import sin, cos, pi
OUT=Path(os.environ["G4C7_R1_DIR"])
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in bpy.data.materials:
    bpy.data.materials.remove(block)
scene=bpy.context.scene
scene.name="M37P2_R1_CIVIC_ESTUARY_ART_TRIAL"
scene["P2_ART"]="HOLD"
scene["P2_OFFICIAL_ADOPTIONS"]=0
scene["P2_MINECRAFT"]="FORBIDDEN"
scene["P2_FORMAL_331_993"]="NOT_RUN"
scene["R1_STATUS"]="UNREVIEWED_SOURCE_TRIAL_NOT_ART_PASS"
scene["R1_AUTHORSHIP"]="CLOUD_CODE_ASSISTED_BESPOKE_MESH_PLUS_SEPARATE_GUI_EDIT"
scene["R1_UNITS"]="ABSTRACT_RESEARCH_UNITS_NOT_MINECRAFT_BLOCKS"
def mat(name,rgb,metal=0,rough=.5,emit=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(*rgb,1)
    p.inputs["Metallic"].default_value=metal
    p.inputs["Roughness"].default_value=rough
    if emit:
        p.inputs["Emission Color"].default_value=(*rgb,1)
        p.inputs["Emission Strength"].default_value=emit
    return m
chalk=mat("warm limestone ceramic",(.63,.57,.49),.1,.56)
ivory=mat("stony pearl",(.84,.79,.68),.1,.42)
slate=mat("deep ink titanium",(.047,.085,.112),.65,.34)
sea=mat("tinted sea-glass",(.055,.26,.30),.26,.14)
copper=mat("oxidized copper",(.29,.36,.29),.7,.4)
bronze=mat("machined warm brass",(.51,.29,.13),.75,.32)
amber=mat("occupied interior glow",(.85,.52,.22),.2,.25,.2)
ground=mat("civic stone paving",(.36,.36,.33),.0,.9)
dark=mat("recessed circulation",(.11,.15,.16),.05,.78)
green=mat("roof garden",(.1,.25,.18),.05,.78)
manufacture=mat("factory powder-coated steel",(.4,.49,.52),.6,.38)
white=mat("clean assembly envelope",(.77,.83,.8),.1,.5)
water=mat("harbor water",(.045,.13,.18),.25,.22)
mats=[chalk,ivory,slate,sea,copper,bronze,amber,ground,dark,green,manufacture,white,water]
def mesh(name,verts,faces,material,mindices=None):
    me=bpy.data.meshes.new(name+" geometry");me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);scene.collection.objects.link(o)
    if isinstance(material,list):
        for m in material:me.materials.append(m)
    else: me.materials.append(material)
    if mindices is not None:
        for p,mi in zip(me.polygons,mindices):p.material_index=mi
    return o
def box(name,loc,size,m):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object;o.name=name
    o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(m)
    return o
def segment(name,a,b,r,m,vertices=8):
    a,b=Vector(a),Vector(b);delta=b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=r, depth=delta.length, location=(a+b)*.5)
    o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler()
    o.data.materials.append(m);return o
def look(obj,point):obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
def terraced_footprint(cx,cy,rx,ry,n,phase,variation):
    return [(cx+rx*(1+.16*sin(i*2.9+variation))*cos(2*pi*i/n+phase),
             cy+ry*(1+.12*cos(i*3.3+variation))*sin(2*pi*i/n+phase)) for i in range(n)]
def high_fabric(tag,cx,cy,rx,ry,height,n,rotation,offset,skin):
    """Each manually sited parcel is a *single* changing solid loft, not repeated towers."""
    levels=max(3,int(height/5.5));ring=[]
    for j in range(levels+1):
        z=1+j*height/levels
        setback=1-.19*(j/levels)+.064*sin(j*1.7+offset)
        phase=rotation+.025*sin(j*.71+offset)
        pp=terraced_footprint(cx,cy,rx*setback,ry*setback,n,phase,offset+j*.2)
        ring.extend((x,y,z) for x,y in pp)
    faces=[];indices=[]
    for j in range(levels):
        for k in range(n):
            faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
            indices.append(1 if (j+k*3+int(offset*7))%5 in (0,3) else 0 if (j+k)%6 in (1,2) else 2)
    faces.append(tuple(range(levels*n,(levels+1)*n)));indices.append(3)
    building=mesh("URBAN:"+tag,ring,faces,[skin,sea,slate,copper],indices)
    for k in range(n):
        if k%2==0:
            pts=[ring[j*n+k] for j in range(levels+1)]
            for j in range(levels):
                segment(tag+" articulated mullion",pts[j],pts[j+1],.13,bronze,6)
    # Roof infrastructure and planters are readable at aerial scale.
    box(tag+" accessible roof garden",(cx,cy,1+height+.18),(rx*1.15,ry*.85,.34),green)
    return building
# Shared living city: individually sited skyline and mid-rise fabrics, never a tower array.
parcels=[
 ("North Water Court",-133,70,11,16,45,7,.31,.4,ivory),
 ("Artisans' Verge",-108,66,14,11,34,6,.18,1.1,chalk),
 ("Nacre House",-80,65,10,17,69,8,.07,2.2,ivory),
 ("North Laboratory",-53,70,13,13,51,7,.4,3.1,slate),
 ("Sailing Gardens",-9,76,12,15,59,9,.3,2.9,ivory),
 ("Lantern Co-op",20,72,9,16,36,6,.14,.8,chalk),
 ("Copper Commons",46,71,17,13,56,9,.25,1.7,copper),
 ("Night Institute",83,75,13,12,74,7,.27,2.8,slate),
 ("Lacuna Studio",115,73,11,18,50,6,.19,4.1,ivory),
 ("Harbor Exchange",150,66,17,13,39,8,.12,4.4,chalk),
 ("Museum Chambers",-144,17,18,12,31,9,.5,1.8,chalk),
 ("Sculpture School",-114,23,13,14,36,7,.25,1.9,copper),
 ("Solar Archive",-83,20,11,17,55,9,.49,2.2,ivory),
 ("Civic Tradehouse",-57,14,13,13,41,6,.24,.7,slate),
 ("Nesting Terrace",-26,57,14,12,28,8,.27,3.7,chalk),
 ("Light Workshop",4,20,12,12,46,7,.25,.3,ivory),
 ("Exchange Hall",33,13,12,19,35,9,.35,2.6,copper),
 ("South Artworks",-145,-79,13,11,42,7,.46,.2,ivory),
 ("Spice Market",-111,-80,13,15,27,8,.33,1.2,chalk),
 ("Ink Residence",-81,-78,12,13,61,7,.14,2.1,slate),
 ("Garden Steps",-53,-76,10,15,37,8,.19,1.2,ivory),
 ("Library Annex",-22,-76,12,13,50,6,.26,.8,copper),
 ("Harbor Rooms",9,-78,14,15,43,9,.35,3.9,ivory),
 ("Mosaic Cooperative",44,-80,15,13,54,7,.1,1.1,chalk),
 ("Crew Quarters",77,-78,13,15,46,8,.37,4.1,slate),
 ("Maintenance Atelier",112,-77,14,12,29,7,.18,2.2,ivory),
 ("Oceanarium 4",151,-77,12,18,40,9,.3,4.3,copper)]
for s in parcels:high_fabric(*s)
# Urban-ground continuity with transverse pedestrian crossings and explicitly linked corridors.
box("CONTEXT_ONLY garden-bearing research terrain",(0,0,-1.55),(362,199,3),ground)
box("Southern basin waterfront",(0,-119,-1.8),(380,43,2),water)
spine=[(-175,-34),(-129,-35),(-95,-34),(-58,-34),(-22,-33),(19,-33),(56,-32),(101,-32),(174,-31)]
for i in range(len(spine)-1):
    a,b=spine[i],spine[i+1];mid=((a[0]+b[0])/2,(a[1]+b[1])/2,0.08)
    box("PUBLIC: continuous inhabited esplanade "+str(i),mid,(b[0]-a[0]+.3,13.5,.18),ivory)
for x in (-120,-67,-32,15,44,125):
    box("PUBLIC: traversable north-south connector "+str(x),(x,12,.07),(9,93,.12),chalk)
for x in (-131,-96,-57,-19,24,57,92,133):
    box("PUBLIC: neighborhood transit threshold "+str(x),(x,-45,.18),(11,4,.35),dark)
# Occupied small storefronts; these are narrow typological rooms, not the city massing.
for i,(x,y,w) in enumerate([(-127,-22,10),(-110,-21,12),(-88,-20,9),(-70,-18,12),(-50,-20,11),(-8,-20,12),(11,-21,10),(32,-20,12),(50,-19,10)]):
    box("STREET: commercial awning "+str(i),(x,y,5.3),(w,4,.35),bronze)
    box("STREET: visible commercial window "+str(i),(x,y-2.4,2.65),(w*.73,.12,4.15),sea)
    box("STREET: illuminated shop entrance reveal "+str(i),(x+w*.35,y-2.25,1.8),(1.65,.13,3.5),amber)
# Public plazas are rooms between buildings, not a colossal roof or isolated sculpture.
for i,(x,y,r) in enumerate([(-119,-10,4.2),(-59,1,3.3),(-2,-7,4.9),(41,-3,4.1),(124,-9,4.5)]):
    box("CIVIC: public gathering stair terrace "+str(i),(x,y,.4),(r*2,r*1.4,.7),chalk)
    box("CIVIC: planted terrace "+str(i),(x,y+1,.92),(r*1.6,r*.65,.32),green)
    for j in range(3):
        segment("CIVIC: branching tree trunk "+str(i),(x+(j-1)*r*.38,y+1,1),(x+(j-1)*r*.38,y+1,5+j*.35),.16,copper,7)
# Working spacecraft factory, publicly visible through a clear safety-separated gallery.
box("FACTORY: nonpublic machine hall structural floor",(108,20,.08),(99,50,.3),slate)
for i,(xc,shift,height) in enumerate([(77,-.7,31),(105,2.2,40),(135,.8,34)]):
    xs=[-14,-8,0,8,14]
    verts=[]
    for yy,zz in [(-2,0),(9,0),(26,0),(39,0),(47,0)]:
        pass
    # Distinct curved section roof ribs; open gables show interior equipment.
    for t in range(13):
        y=-4+4*t
        z=11+height*sin(pi*t/12)**.7
        segment("FACTORY: articulated soaring roof structural spine "+str(i)+"-"+str(t),
                (xc-15,y,z),(xc+14,y,z+shift),.27,manufacture,8)
    for xx in (xc-14,xc+13):
        for y in (-3,18,41):
            segment("FACTORY: load column "+str(i),(xx,y,.2),(xx,y,12),.32,manufacture,8)
    # Rocket tank in an actual suspended assembly fixture rather than abstract colored cylinder.
    segment("PRODUCTION: orbital vehicle hull core "+str(i),(xc-9,19,14),(xc+10,19,14),2.25,white,24)
    segment("PRODUCTION: nose adapter "+str(i),(xc+10,19,14),(xc+14,19,14),1.2,bronze,20)
    for t in (-7,1,8):
        segment("PRODUCTION: circumferential fixture "+str(i),(xc+t,19,11.5),(xc+t,19,16.5),.29,copper,8)
    for x in (xc-12,xc+12):
        segment("PRODUCTION: overhead gantry leg "+str(i),(x,30,1),(x,30,22),.4,manufacture,8)
    segment("PRODUCTION: gantry cross rail "+str(i),(xc-12,30,22),(xc+12,30,22),.48,bronze,8)
# Actual physical transparency barrier with no walk-through on public side.
box("FACTORY: public observation gallery floor",(106,-13,2.15),(98,7,.38),chalk)
box("FACTORY: continuous transparent safety partition",(106,-7,6.45),(98,.42,10.7),sea)
for x in range(59,157,7):
    segment("FACTORY: partition safety mullion "+str(x),(x,-7,1.1),(x,-7,12),.19,slate,6)
box("FACTORY: visitor entry portal with recess",(59,-15,3.3),(7,1.4,6.1),copper)
box("FACTORY: controlled worker-only corridor",(104,50,.3),(80,4,.55),dark)
# Research and culture: real viewing/laboratory and exhibition-level floor, not tags.
box("RESEARCH: open review laboratory floor",(-95,12,8.3),(30,17,.34),ivory)
box("RESEARCH: instrument bench",(-93,13,9.2),(17,2,1.5),manufacture)
for i in range(5):
    box("RESEARCH: inspection light rig "+str(i),(-101+i*4,15,12),(1.4,.5,2.2),amber)
box("CULTURE: civic gallery public entry threshold",(-141,-12,2.0),(9,1.2,4),sea)
box("CULTURE: public gallery exhibition wall",(-130,-4,5.6),(15,.4,7.5),ivory)
for x in (-136,-131,-126):
    box("CULTURE: lit exhibition panel "+str(x),(x,-4.38,6.1),(3.1,.12,4),amber)
# One physically modelled inhabited apartment frontage, actual doorway/vestibule/living room/window.
# Building contains a 12x13 representative corner unit at z=8.5; no solid front wall across portal.
bx,by,bz=-26,38,9.3
box("HABITAT: inhabitable floor",(bx,by,bz-.28),(13,14,.55),ivory)
box("HABITAT: rear private wall",(bx,by+6.9,bz+2.75),(13,.34,5.5),chalk)
box("HABITAT: east wall",(bx+6.5,by,bz+2.75),(.28,14,5.5),ivory)
box("HABITAT: west wall",(bx-6.5,by,bz+2.75),(.28,14,5.5),ivory)
box("HABITAT: front wall left of usable entrance",(bx-4.6,by-6.9,bz+2.75),(3.9,.31,5.5),chalk)
box("HABITAT: doorway-height lintel",(bx-1.4,by-6.9,bz+4.65),(2.45,.3,1.65),chalk)
box("HABITAT: front entrance door with physical swing clearance",(bx-1.35,by-6.85,bz+1.5),(1.9,.1,3.0),bronze)
box("HABITAT: actual exterior city window",(bx+3.9,by-6.86,bz+2.8),(4.9,.12,4.1),sea)
box("HABITAT: private vestibule divider",(bx-3.8,by-2.5,bz+2.2),(4.7,.28,4.4),chalk)
box("HABITAT: living couch",(bx+1,by+1,bz+.42),(4,1.7,.88),copper)
box("HABITAT: low reading table",(bx+2.1,by-1,bz+.4),(2.3,1,.8),bronze)
box("HABITAT: book niche",(bx-4.8,by+3.4,bz+1.25),(1.8,.7,2.5),slate)
box("HABITAT: internal inhabited ceiling",(bx,by,bz+5.6),(13,14,.34),ivory)
# Hand-authored public lantern: selected for a *real GUI* elevation edit, not a skyscraper or sculpture.
lantern=mesh("R1_PUBLIC_LANTERN",[(13,-32,5),(27,-32,5),(29,-25,5),(16,-23,5),(15,-31,8),(26,-31,8.6),(27,-26,9),(18,-24,7.9)],
             [(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],[copper,sea,bronze],[0,1,0,1,2])
lantern["R1_HUMAN_TACTILE_ROOF"]="public threshold weather protection"
# lighting / view / scene pass
world=bpy.data.worlds.new("cloud-lit estuary atmosphere");scene.world=world;world.use_nodes=True
bg=world.node_tree.nodes.get("Background");bg.inputs["Color"].default_value=(.47,.55,.64,1);bg.inputs["Strength"].default_value=.55
sun_data=bpy.data.lights.new("north-warm afternoon","SUN");sun=bpy.data.objects.new("sun",sun_data);scene.collection.objects.link(sun);sun.rotation_euler=(math.radians(35),math.radians(-26),math.radians(-20));sun_data.energy=2.1
def area(name,loc,power,size,point):
    d=bpy.data.lights.new(name,"AREA");d.energy=power;d.shape="DISK";d.size=size
    o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;look(o,point)
area("factory practical skylight",(105,8,60),2300,70,(105,17,4))
area("apartment warm lamp",(-28,39,12),450,9,(-26,37,9))
def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);scene.collection.objects.link(o)
    o.location=loc;look(o,target);d.lens=lens;d.clip_end=2000;return o
camera("R1_CAMERA_AERIAL",(244,-307,240),(0,3,27),33)
camera("R1_CAMERA_PUBLIC_EYE",(19,-44,6.2),(110,-12,14.2),24)
camera("R1_CAMERA_HABITAT_EYE",(-26,41,11.0),(-23,31,11.2),19)
scene.render.engine="CYCLES"
scene.cycles.samples=18
scene.cycles.use_denoising=True
scene.render.resolution_x=840;scene.render.resolution_y=560;scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
scene.render.film_transparent=False
scene.view_settings.view_transform="AgX"
# Select the real architectural lantern for an additional genuine Blender GUI edit.
bpy.ops.object.select_all(action='DESELECT')
lantern.select_set(True);bpy.context.view_layer.objects.active=lantern
for screen in bpy.data.screens:
    for region in screen.areas:
        if region.type=="CONSOLE":region.type="VIEW_3D"
saved=OUT/"R1_CIVIC_ESTUARY_CODE_ASSISTED_INITIAL_NOT_ART.blend"
assert not saved.exists()
assert "FINISHED" in bpy.ops.wm.save_as_mainfile(filepath=str(saved),compress=True)
print("R1_NATIVE_INITIAL_CODE_ASSISTED_SAVED",saved,flush=True)
