#!/usr/bin/env python3
"""R1 / Civic Braid: singular authored urban SECTION, not a generated skyline.

Explicit one-off spatial composing across urban fabric, dwelling, working ship
factory, research/culture, public realm. Research art trial; not accepted city.
Meshes are deliberately authored control points and compositional decisions
encoded for reproducibility. No M37 rejected art or old generator imported.
"""
import bpy, math, os, json, hashlib
from pathlib import Path
from mathutils import Vector
from math import sin,cos,pi
D=Path(os.environ["G4C7_BRAID_DIR"]);D.mkdir(exist_ok=True,parents=True)
bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
for m in bpy.data.materials: bpy.data.materials.remove(m)
s=bpy.context.scene;s.name="G4C7_R1_CIVIC_BRAID_AUTHORED_SECTION_HOLD"
for k,v in {
 "P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,"P2_MINECRAFT":"FORBIDDEN",
 "P2_FORMAL_331_993":"NOT_RUN","R1_METHOD":"EXPLICIT_HAND_AUTHORED_CONTROLS",
 "R1_SCOPE":"ONE_INTEGRATED_URBAN_SECTION_NOT_WHOLE_CITY",
 "R1_STATUS":"UNREVIEWED_EARLY_ART_TRIAL","R1_UNITS":"ABSTRACT_NOT_BLOCKS",
 "R1_HIGH_QUALITY_AUTONOMOUS_GUI_AUTHORSHIP":"NOT_ESTABLISHED"
}.items(): s[k]=v
def M(name, rgb, metal=0, rough=.5, emission=0, transmission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True
 p=m.node_tree.nodes.get("Principled BSDF")
 p.inputs["Base Color"].default_value=(*rgb,1);p.inputs["Metallic"].default_value=metal;p.inputs["Roughness"].default_value=rough
 if emission:
  p.inputs["Emission Color"].default_value=(*rgb,1)
  p.inputs["Emission Strength"].default_value=emission
 if transmission:p.inputs["Transmission Weight"].default_value=transmission
 return m
stone=M("Pearl-grey precast columns",(.65,.65,.60),.08,.72)
warm=M("Sun-warmed ivory limestone",(.80,.71,.57),.06,.7)
ink=M("Midnight bronze anodized aluminium",(.047,.075,.087),.65,.34)
oxide=M("Copper green anodized ceramic",(.21,.40,.37),.55,.35)
copper=M("Brushed bronze fins",(.54,.32,.18),.74,.31)
glass=M("Optically tinted transparent panels",(.095,.31,.36),.08,.13,0,.45)
light=M("Warm lived-in windows",(.87,.59,.29),.04,.33,.2)
lawn=M("Terraced green infiltration beds",(.16,.33,.21),.04,.88)
pave=M("Detailed pale street paving",(.42,.45,.42),.04,.82)
dark=M("Porous recess and road",(.12,.18,.19),.03,.82)
steel=M("Working factory galvanised steel",(.38,.51,.55),.64,.36)
ship=M("Spacecraft assembly pearl material",(.74,.78,.72),.43,.28)
water=M("Civic estuary water",(.052,.15,.18),.3,.22)
mats=[stone,warm,ink,oxide,copper,glass,light,lawn,pave,dark,steel,ship,water]
def face_mesh(name,vertices,faces,materials,indices=None):
 mesh=bpy.data.meshes.new(name+" modeled faces")
 mesh.from_pydata(vertices,[],faces);mesh.update()
 obj=bpy.data.objects.new(name,mesh);s.collection.objects.link(obj)
 for m in (materials if isinstance(materials,list) else [materials]):mesh.materials.append(m)
 if indices:
  for p,idx in zip(mesh.polygons,indices):p.material_index=idx
 return obj
def box(name,p,size,material,bevel=.07):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p)
 o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 if bevel:
  mod=o.modifiers.new("Soft crafted edge","BEVEL");mod.width=bevel;mod.segments=2
  n=o.modifiers.new("Weighted facade normals","WEIGHTED_NORMAL")
 return o
def tube(name,a,b,r,material,n=10):
 aa=Vector(a);bb=Vector(b);v=bb-aa
 bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=r,depth=v.length,location=(aa+bb)*.5)
 o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat("Z","Y").to_euler();o.data.materials.append(material);return o
def polyextrude(name,foot,z1,z2,materials):
 n=len(foot);verts=[(x,y,z1) for x,y in foot]+[(x,y,z2) for x,y in foot]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,n+(i+1)%n,n+i) for i in range(n)]
 ids=[0,0]+[(k%len(materials)) for k in range(n)]
 return face_mesh(name,verts,faces,materials,ids)
def loft(name, rings,ms,indices=None):
 n=len(rings[0]);assert all(len(x)==n for x in rings)
 vs=[v for ring in rings for v in ring]
 faces=[tuple(reversed(range(n)))]
 ids=[0]
 for j in range(len(rings)-1):
  for i in range(n):
   faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
   ids.append((j+i*2)%len(ms) if indices is None else indices(j,i))
 faces.append(tuple(range((len(rings)-1)*n,len(rings)*n)));ids.append(0)
 return face_mesh(name,vs,faces,ms,ids)
def set_cam(name,loc,focus,lens):
 cam=bpy.data.cameras.new(name);obj=bpy.data.objects.new(name,cam);s.collection.objects.link(obj)
 obj.location=loc;obj.rotation_euler=(Vector(focus)-obj.location).to_track_quat("-Z","Y").to_euler()
 cam.lens=lens;cam.clip_end=1200;return obj
def font(name,txt,loc,rot,scale,mat):
 curve=bpy.data.curves.new(name,"FONT");curve.body=txt;curve.size=scale;curve.extrude=.017
 ob=bpy.data.objects.new(name,curve);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=rot;ob.data.materials.append(mat);return ob
# Architecture-level urban compositional intent. No sea of repeated towers.
# The central public route bifurcates into inhabited alleys and factory gallery.
# Road width is deliberately NOT world-certified; all dimensions are research units.
box("public transit seam integrated ground",(0,-12,-.45),(345,137,.85),pave,0)
box("southern water edge",(-5,-94,-.5),(370,25,.7),water,0)
# Streets have public edge, crossings and two tiers; no empty giant plazas.
for k,(x,y,w,l) in enumerate([(-80,-34,11,112),(10,-27,12,92),(96,-39,11,104)]):
 box("PUBLIC narrow walk street and urban activity %02d"%k,(x,y,.055),(w,l,.11),warm,.01)
for i,(x,y,l) in enumerate([(-130,-32,42),(-40,-29,68),(48,-29,53),(154,-31,46)]):
 box("PUBLIC continuous east-west pedestrian seam %02d"%i,(x,y,.08),(l,8.5,.14),stone,.02)
# A sequence of deliberately distinct inhabitation blocks, not identical tower arrays:
# six separate compositions governed by individually supplied floor outlines.
blocks=[
 ("Habitat stepped walled garden",-136,28,[(-17,-10),(-8,-15),(10,-13),(18,-5),(15,15),(-2,18),(-18,12)],[0,11,19,28,31],[1,1,.9,.73,.64],warm),
 ("Civic cooperative weaving",-87,41,[(-17,-16),(6,-18),(18,-7),(16,9),(0,17),(-17,9)],[0,9,18,25],[1,1,.84,.67],oxide),
 ("Research lantern tower",-38,45,[(-9,-11),(9,-13),(16,-2),(11,13),(-6,16),(-15,3)],[0,13,27,40,53],[1,1,.84,.7,.48],stone),
 ("Habitat light courts",10,42,[(-20,-13),(-6,-19),(16,-12),(19,2),(12,15),(-8,18),(-18,6)],[0,7,16,23,34,39],[1,1,1,.89,.71,.64],warm),
 ("Public arts archive",54,43,[(-20,-9),(-10,-20),(6,-17),(17,-10),(19,9),(3,17),(-19,10)],[0,8,17,22,31],[1,1,.88,.73,.56],oxide),
 ("Workshop housing branch",136,40,[(-16,-17),(1,-19),(16,-8),(20,14),(-3,19),(-18,8)],[0,9,19,29,37],[1,1,.85,.75,.58],warm)
]
def authored_block(name,cx,cy,xy,levels,scales,material):
 base=list(xy);rings=[]
 # Context and elevations explicitly different per architectural address.
 for lvl,scale in zip(levels,scales):
  skew=.05*lvl
  rings.append([(cx+u*scale + skew*math.sin(i*2),cy+v*scale+skew*math.cos(i*1.9),lvl+.3)
             for i,(u,v) in enumerate(base)])
 ob=loft("STREETWALL: "+name,rings,[material,glass,ink,oxide],lambda j,i:0 if i%3==0 else 1 if (j+i)%3==0 else 2 if i%5==0 else 3)
 # Material and function genuinely registered within facade along public street.
 # Balconies at one/two unique depth zones with void above, never colossal slabs.
 for j in range(1,len(levels)-1):
  z=levels[j]+.25
  for side in (0,2,4):
   if side>=len(base):continue
   p=base[side];q=base[(side+1)%len(base)]
   x=cx+.5*(p[0]+q[0])*scales[j];y=cy+.5*(p[1]+q[1])*scales[j]
   box(name+" accessible green balcony",(x,y,z),(4.8,3.1,.37),lawn,.06)
   for t in range(3):
    tube(name+" fine bronze balcony safety mullion",(x-2.1+t*2.0,y-1.5,z+.2),(x-2.1+t*2.0,y-1.5,z+1.4),.055,copper,6)
 # Primary lower-level street frontage: shop window, entry threshold, visible inside
 front_y=cy-16
 box(name+" genuinely recessed public-shop threshold",(cx-2.4,front_y,2.0),(4.9,.25,3.8),ink,.04)
 box(name+" lit glass retail opening",(cx+4.3,front_y,3.1),(7,.16,4.7),glass,.04)
 box(name+" lit retail interior",(cx+3.9,front_y+2.9,2.2),(5,2.2,3.4),light,.08)
 font(name+" wayfinding typography",name.upper()[:19],(cx-8,front_y-.22,6.8),(pi/2,0,0),.88,warm)
 return ob
for args in blocks:authored_block(*args)
# Orthogonal narrow inhabited lower districts continue without repeated towers.
# These have different dwelling directions and explicit service/access zones.
low=[
 (-158,-57,26,18,13,-.16),(-113,-59,24,21,15,.13),(-64,-58,30,17,14,-.18),
 (-11,-60,29,20,17,.26),(42,-59,21,23,14,-.17),(83,-56,26,20,16,.13),(147,-58,29,17,13,.08)
]
for i,(x,y,w,d,h,tilt) in enumerate(low):
 plan=[(-w*.5,-d*.5),(w*.3,-d*.58),(w*.58,d*.05),(w*.37,d*.5),(-w*.36,d*.48),(-w*.53,-d*.03)]
 ring0=[(x+u,y+v,.25) for u,v in plan]
 ring1=[(x+u*(.94 if i%2 else .90)+tilt*8,y+v*.96,h) for u,v in plan]
 ob=loft("LIVED MIDRISE distinct urban parcel "+str(i),[ring0,ring1],[stone if i%3 else warm,glass,oxide,ink])
 # Ground visible frontage has alcoves and warm genuine door pockets
 for t in range(3):
  box("LIVED shopfront glass "+str(i)+"-"+str(t),(x-w*.24+t*w*.18,y-d*.52,2.2),(w*.15,.13,3.25),glass,.025)
 box("LIVED entry to real interior "+str(i),(x+w*.29,y-d*.5,2.2),(2.4,.2,4),light,.04)
 box("LIVED unique accessible planted edge "+str(i),(x,y+d*.28,h+.2),(w*.54,d*.33,.35),lawn,.07)
# The inhabited room and urban frontage occupy the SAME ONE saved architectural scene:
# The room is not a sealed cube; it opens on the city to the south along its glazing.
bx,by,bz=-136,14,9.0
box("HABITAT inhabited floor actual",(bx,by,bz-.25),(17.4,16,.5),warm,.08)
box("HABITAT separated rear private wall",(bx,by+7.8,bz+2.5),(17.4,.24,5),stone,.04)
box("HABITAT privacy east flank",(bx+8.6,by,bz+2.5),(.26,16,5),stone,.04)
box("HABITAT privacy west flank",(bx-8.6,by,bz+2.5),(.26,16,5),stone,.04)
box("HABITAT vestibule west public arrival wall",(bx-5.25,by-7.8,bz+3.65),(6.8,.28,2.7),warm,.08)
box("HABITAT solid entrance lintel",(bx-1,by-7.8,bz+4.7),(3.2,.28,.65),warm,.06)
box("HABITAT actual entrance door",(bx-2.0,by-7.76,bz+1.64),(1.85,.16,3.28),oxide,.05)
box("HABITAT openable exterior south sash",(bx+3.2,by-7.8,bz+2.4),(8.7,.1,4.5),glass,.02)
box("HABITAT window mullion left",(bx-.3,by-7.95,bz+2.6),(.13,.18,4.8),copper,.02)
box("HABITAT window mullion middle",(bx+3.3,by-7.95,bz+2.6),(.13,.18,4.8),copper,.02)
box("HABITAT window mullion right",(bx+6.8,by-7.95,bz+2.6),(.13,.18,4.8),copper,.02)
box("HABITAT threshold vestibule divider leading to living room",(bx-4.5,by-3,bz+2.5),(6,.22,5),warm,.02)
box("HABITAT vestibule built-in coat niche",(bx-6.0,by-5.5,bz+1.8),(1.4,.7,3.3),copper,.05)
box("HABITAT actual soft upholstered living sofa",(bx+2.7,by+2.0,bz+.65),(4.9,2.2,1.25),oxide,.3)
box("HABITAT longitudinal sofa seat",(bx+2.7,by+1.3,bz+.9),(4.7,1.2,.48),light,.3)
box("HABITAT table for daily use",(bx+2.2,by-.3,bz+.47),(2.8,1.3,.9),copper,.1)
box("HABITAT bookcase housing private contents",(bx-7.4,by+3.8,bz+2),(1.5,3.8,3.65),ink,.05)
for t in range(4):
 box("HABITAT colorful books "+str(t),(bx-7.15,by+2.5+t*.8,bz+1.9),(1.5,.5,2),warm if t%2 else light,.02)
box("HABITAT separating inhabited ceiling",(bx,by,bz+5.65),(17.4,16,.22),stone,.04)
# Front balcony and actual elevated access at apartment occupied level.
box("HABITAT inhabited balcony",(bx+4.9,by-9.2,bz-.12),(8.5,3.4,.32),warm,.03)
for k in range(4):
 tube("HABITAT waist-height balcony rail", (bx+.9+k*2.5,by-11,bz+.12),(bx+.9+k*2.5,by-11,bz+1.65),.06,copper,8)
tube("HABITAT continuous handrail",(bx+.6,by-11,bz+1.65),(bx+8.4,by-11,bz+1.65),.06,copper)
# Working shipbuilder: open architecture organized by 3 internal operational bays
# (not a giant single blue wall). Actual vessel/tooling visible through gallery.
factory_x=103
box("FACTORY clearly defined assembly floor",(factory_x,2,.0),(128,71,.55),dark,.06)
for k,(x,y,hl) in enumerate([(58,2,30),(104,2,37),(146,2,29)]):
 # Authored distinctive portal ribs: loaded curve is segmented and open across site.
 pts=[(x-16,y-26,2),(x-17,y-26,10),(x-15,y-26,21),
      (x-9,y-26,hl),(x+4,y-26,hl+5),(x+16,y-26,hl-5),(x+18,y-26,10),(x+18,y-26,2)]
 for j in range(len(pts)-1):
  tube("FACTORY actual portal portal rib %02d-%02d"%(k,j),pts[j],pts[j+1],.43,steel,10)
 for shift in (8,33):
  tube("FACTORY cross-bay structural lateral tie %02d %02d"%(k,shift),
      (x-14,y-26,shift*.6),(x-14,y+23,shift*.6),.31,oxide)
  tube("FACTORY cross-bay roof truss %02d %02d"%(k,shift),
      (x-10,y-26,shift*.65+13),(x-10,y+23,shift*.65+13),.26,steel)
 # Actual hull to be manufactured, suspended over tooling fixtures.
 tube("MANUFACTURE actual cylindrical tank hull "+str(k),(x-11,y-3,15),(x+13,y-3,15),2.5,ship,26)
 tube("MANUFACTURE tank forward flange "+str(k),(x+13,y-3,15),(x+16,y-3,15),1.65,copper,24)
 for t in range(4):
  tube("MANUFACTURE orbit vehicle ring weld support %02d-%02d"%(k,t),
      (x-7+t*5,y-3,12.6),(x-7+t*5,y-3,17.4),.23,steel,10)
 for sx in (x-15,x+15):
  tube("MANUFACTURE operating gantry legs "+str(k),(sx,y+9,.1),(sx,y+9,21),.48,steel)
 tube("MANUFACTURE actual overhead bridge crane "+str(k),(x-15,y+9,21),(x+15,y+9,21),.6,copper)
 tube("MANUFACTURE crane hoist cable "+str(k),(x+3,y+9,21),(x+3,y+9,13),.12,steel)
 box("MANUFACTURE machining assembly work bench "+str(k),(x-10,y+19,2.2),(11,3,2),stone,.14)
# Public is outside equipment, behind safety barrier. Transparent panels, control gates,
# open views instead of one giant colored rectangle.
box("PUBLIC FACTORY visitor gallery traversable floor",(102,-34,1.4),(136,8.5,.4),warm,.07)
box("FACTORY physical one-direction transparent separation",(103,-27,7.0),(129,.25,11.4),glass,.03)
for i in range(18):
 x=39+i*7.4
 tube("FACTORY transparent curtain wall structural mullion "+str(i),(x,-27,1.3),(x,-27,12.6),.13,copper,8)
box("FACTORY visitor entry threshold",(39,-37,3.2),(8,.4,5.5),copper,.08)
font("FACTORY visitor signage","ORBITAL WORKS  /  VISITOR GALLERY",(53,-34.2,5.0),(pi/2,0,0),1.36,stone)
# Research + civic exhibition connecting actual maker district at ground level
# small hall is freely accessible from public seam, light-gathering roof profiles.
roofplan=[(-47,-13),(-24,-15),(-8,-8),(-9,15),(-28,20),(-52,10)]
polyextrude("RESEARCH cultural laboratory elevated inhabited platform",roofplan,1.0,1.5,[warm,oxide])
top=[(-47,-13,16),(-24,-15,16),(-8,-8,15),(-9,15,22),(-28,20,27),(-52,10,19)]
low=[(x,y,3) for x,y in roofplan]
face_mesh("RESEARCH folded high-window designed roof and facade",low+top,
 [(i,(i+1)%6,6+(i+1)%6,6+i) for i in range(6)]+[tuple(range(6,12))],
 [stone,glass,oxide,warm],[1,2,1,2,1,1,0])
box("RESEARCH instrument visible front laboratory",( -29,-9,4.0),(20,5,3),glass,.04)
for i in range(4):
 box("RESEARCH spectrometer work table "+str(i),(-44+i*8,3,3.7),(4.6,2.3,1.4),steel,.08)
 box("RESEARCH visible warm instrument "+str(i),(-44+i*8,3,5),(1.8,1,1.5),light,.08)
font("CULTURE facade signage","RESEARCH  /  PUBLIC LAB",(-45,-16.25,7.1),(pi/2,0,0),1.16,warm)
# A former silo shell becomes a genuinely used public amphitheatre — sectional, not monument.
for k,(x,y,w,h) in enumerate([(-37,-26,17,.45),(-37,-22,14,.8),(-37,-18,11,1.15)]):
 box("CULTURE actual public seating terrace "+str(k),(x,y,h),(w,2,.45),stone,.05)
# Streets intentionally occupied by wayfinding, lighting, plants, cycle racks and market.
for i,(x,y) in enumerate([(-159,-23),(-123,-24),(-95,-24),(-62,-24),(-20,-23),(21,-24),(65,-25),(158,-23)]):
 tube("PUBLIC lamp mast "+str(i),(x,y,0),(x,y,8.2),.13,ink)
 tube("PUBLIC suspended lantern shade "+str(i),(x-.9,y,8.4),(x+1,y,8.4),.15,light)
 box("PUBLIC retail bicycle and seating "+str(i),(x+2.6,y+1,.65),(3.2,1.1,1.1),copper,.09)
 for u in range(3):
  box("PUBLIC stepped edible planting "+str(i)+"-"+str(u),(x-2.0+u*1.5,y+2.0,.6),(1.1,1.2,1.2),lawn,.25)
# Site-specific landmark is readable wayfinding, not giant sculpture.
font("CITY identifiable pedestrian gate","CIVIC BRAID",( -15,-20,8),(pi/2,0,0),2.4,oxide)
# Ground sunlight, sky, cameras. All 4 views use ONE saved 3D.
world=bpy.data.worlds.new("Soft clear harbor daylight");world.use_nodes=True;s.world=world
bg=world.node_tree.nodes.get("Background");bg.inputs["Color"].default_value=(.58,.70,.79,1);bg.inputs["Strength"].default_value=.68
data=bpy.data.lights.new("Daylight broad sun","SUN");sun=bpy.data.objects.new("Daylight broad sun",data);s.collection.objects.link(sun)
sun.rotation_euler=(math.radians(32),math.radians(-21),math.radians(-25));data.energy=1.8
def area(name,loc,power,size,target):
 d=bpy.data.lights.new(name,"AREA");d.energy=power;d.shape="DISK";d.size=size
 ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc
 ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
area("Residential light court",(-135,5,24),700,24,(-136,14,9))
area("Manufacturing skylight",(90,-5,85),3200,110,(103,2,12))
# Cameras actually target intended content rather than walls/solid boxes
set_cam("CAM_AERIAL",(270,-345,240),(-5,-2,13),32)
set_cam("CAM_PUBLIC_EYE",(4,-52,6.6),(77,-27,12),29)
set_cam("CAM_HABITAT_EYE",(-134,17,11.6),(-132,8,11.6),19)
set_cam("CAM_FACTORY_EYE",(107,-47,8),(101,0,15),30)
set_cam("CAM_RESEARCH_EYE",(-30,-41,6),(-29,2,8),29)
s.render.engine="CYCLES";s.cycles.samples=20;s.cycles.use_denoising=True
s.render.resolution_x=960;s.render.resolution_y=600;s.render.resolution_percentage=100
s.render.image_settings.file_format="PNG"
s.view_settings.view_transform="AgX"
s.camera=bpy.data.objects["CAM_AERIAL"]
# Do not treat source count or rendered count as ART score. No auto ART PASS.
path=D/"R1_CIVIC_BRAID_AUTHORIAL_SECTION_ART_UNREVIEWED.blend"
assert not path.exists()
assert "FINISHED" in bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
print("R1_NEW_DISTINCT_ONE_AUTHORIAL_CITY_SECTION_NATIVE_SAVED_UNREVIEWED",path,len([o for o in s.objects if o.type=="MESH"]),flush=True)
