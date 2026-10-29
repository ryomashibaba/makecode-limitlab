"""Author-built native meshes. Blender 5.2, no downloaded/generated assets.
Usage: blender -b --factory-startup -t 8 -P build_p2b.py -- B1 [render]
Research metres, Z up. All five cameras use identical coordinates across studies.
"""
import bpy, math, json, sys, random
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['B1']
VAR=args[0]; OUT=ROOT/VAR; OUT.mkdir(exist_ok=False)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
random.seed(56)

def mat(name, color, metallic=0, rough=.62):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metallic
    return m
M={
 'stone':mat('Ivory mineral composite',(.60,.58,.48)),
 'floor':mat('Warm civic terrazzo',(.37,.32,.25)),
 'copper':mat('Weathered copper ceramic',(.13,.29,.28),.35),
 'blue':mat('Indigo research ceramic',(.10,.18,.27),.25),
 'warm':mat('Amber timber',(.40,.16,.065)),
 'dark':mat('Recessed charcoal',(.035,.055,.065)),
 'green':mat('Garden canopy',(.09,.20,.11)),
 'people':mat('People terracotta',(.63,.20,.09)),
 'paper':mat('Work surface',(.77,.69,.49)),
 'ground':mat('Coastal mineral ground',(.18,.22,.22)),
 'water':mat('Still water',(.09,.19,.23),.45,.2),
}
class Geo:
    def __init__(self): self.v=[]; self.f=[]
    def poly(self, pts):
        a=len(self.v); self.v.extend(pts); self.f.append(tuple(range(a,a+len(pts))))
    def prism(self,pts,z0,z1):
        n=len(pts); a=len(self.v)
        self.v.extend([(x,y,z) for z in (z0,z1) for x,y in pts])
        self.f.extend([tuple(a+i for i in range(n-1,-1,-1)),tuple(a+n+i for i in range(n))])
        for i in range(n): j=(i+1)%n; self.f.append((a+i,a+j,a+n+j,a+n+i))
    def box(self,x0,x1,y0,y1,z0,z1): self.prism([(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z0,z1)
    def finish(self,name,material):
        mesh=bpy.data.meshes.new(name); mesh.from_pydata(self.v,[],self.f); mesh.update()
        ob=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(ob)
        ob.data.materials.append(M[material]); return ob
def box(name,bounds,material='stone'):
    g=Geo(); g.box(*bounds); return g.finish(name,material)
def beam(g,a,b,width,z0,z1):
    d=Vector((b[0]-a[0],b[1]-a[1])); d.normalize(); n=Vector((-d.y,d.x))*width/2
    g.prism([(a[0]+n.x,a[1]+n.y),(a[0]-n.x,a[1]-n.y),(b[0]-n.x,b[1]-n.y),(b[0]+n.x,b[1]+n.y)],z0,z1)
def linewall(name,a,b,z0,z1,thick=.65,material='stone'):
    g=Geo(); beam(g,a,b,thick,z0,z1); return g.finish(name,material)

# A real inhabited section, not three separate boxes. A common 0.65m material
# layer supports research and roofs making; a second roofs research/supports home.
core=Geo(); core.prism([(-28,-2),(24,-2),(30,28),(10,38),(-28,30)],-.65,0)
core.finish('CORE_MAKING_FLOOR','floor')
g=Geo()
for bounds in [(-28,-27,-2,30,9.35,10),(-23,-2,-2,30,9.35,10),(-27,-23,-2,0,9.35,10),(-27,-23,16.8,30,9.35,10),(-2,24,-2,4,9.35,10),(-2,24,24,30,9.35,10),(18,24,4,24,9.35,10)]: g.box(*bounds)
g.finish('SHARED_MAKING_ROOF_RESEARCH_FLOOR','stone')
g=Geo()
for bounds in [(-28,-27,-2,30,15.35,16),(-23,-2,-2,30,15.35,16),(-27,-23,-2,18,15.35,16),(-27,-23,28.2,30,15.35,16)]: g.box(*bounds)
g.finish('SHARED_RESEARCH_ROOF_HOME_FLOOR','stone')
g=Geo(); g.box(-28,-2,-2,20,21.5,22); g.finish('HOME_ROOF','stone')
# Apertures are gaps between solids. Doors and windows are never painted holes.
g=Geo()
for xa,xb in [(-28,-8),(8,24)]: g.box(xa,xb,-2.65,-2,0,9.35)
g.box(-8,8,-2.65,-2,7,9.35); g.finish('MAKING_REAL_ENTRY_JAMBS_LINTEL','stone')
g=Geo()
for y0,y1 in [(0,7),(12,19),(24,30)]: g.box(-28.65,-28,y0,y1,0,15.35)
g.box(-28.65,-28,-2,30,7.5,9.35); g.box(-28.65,-28,-2,30,14.2,15.35)
g.finish('CORE_WEST_WINDOWED_ENVELOPE','stone')
linewall('CORE_NORTH_SHARED_PRIVACY_WALL',(-28,30),(10,38),0,16)
linewall('MAKING_EAST_FACET',(24,-2),(30,28),0,8.5)
linewall('MAKING_NORTH_EAST_FACET',(30,28),(10,38),0,10)
# Research is a room with a large east observation opening, not an exposed deck.
g=Geo(); g.box(-28,-2,-2.6,-2,10,10.9); g.box(-28,-2,-2.6,-2,14.5,15.35)
for x in [-28,-17,-3]: g.box(x,x+.6,-2.6,-2,10,15.35)
g.finish('RESEARCH_FRONT_REAL_WINDOWS','copper')
g=Geo(); g.box(-2.6,-2,4,24,10,10.9); g.box(-2.6,-2,4,24,14.7,15.35)
g.box(-2.6,-2,-2,4,10,15.35); g.box(-2.6,-2,24,30,10,15.35)
g.finish('RESEARCH_TO_MAKING_REAL_OBSERVATION_OPENING','stone')
# Residence integrated into same structural section. Real outer window and door.
g=Geo(); g.box(-28,-2,-2.6,-2,16,16.75); g.box(-28,-2,-2.6,-2,20.8,21.5)
for x in [-28,-18,-3]: g.box(x,x+.6,-2.6,-2,16,21.5)
g.box(-28.6,-28,-2,20,16,21.5)
g.box(-2.6,-2,-2,20,16,17.1); g.box(-2.6,-2,-2,20,20.8,21.5)
g.box(-28,-24,19.4,20,16,21.5); g.box(-20,-2,19.4,20,16,21.5)
g.box(-24,-20,19.4,20,19.6,21.5)
g.finish('HOME_ENVELOPE_WITH_REAL_DOOR_AND_TWO_VIEW_DIRECTIONS','stone')
box('HOME_PRIVATE_SCREEN',(-20,-19.5,10,17,16,20),'warm')
# Two real flights, tread rise <= .18, full width 4.0. Limited geometry only.
for name,x0,x1,y0,run,z0,rise in [('STAIR_M_R',-27,-23,0,16.8,0,10),('STAIR_R_L',-27,-23,18,10.2,10,6)]:
    g=Geo(); steps=math.ceil(rise/.18)
    for i in range(steps): g.box(x0,x1,y0+i*run/steps,y0+(i+1)*run/steps,z0-.4,z0+(i+1)*rise/steps)
    g.finish(name,'floor')
box('HOME_PRIVATE_LANDING',(-28,-19,27.8,30,15.35,16),'stone')
# Route to home door from north landing, in the same upper section.
# Floor is already part of the shared layer; do not refill the stair aperture.
box('HOME_REAR_LOBBY_ROOF',(-28,-2,20,30,21.5,22),'stone')
linewall('HOME_REAR_LOBBY_WALL',(-28,30),(-2,30),16,21.5)

# Furniture is actual geometry within the rooms, sufficient for human scale.
for i,(x,y) in enumerate([(0,9),(10,15),(4,28)]):
    box(f'MAKING_WORKBENCH_{i}',(x-2.4,x+2.4,y-1,y+1,0,1),'warm')
    box(f'MAKING_WORKPIECE_{i}',(x-.7,x+.7,y-.5,y+.5,1,2.2),'copper')
for i,y in enumerate([4,19,26]):
    box(f'RESEARCH_DESK_{i}',(-17,-11,y,y+1.4,10,10.78),'paper')
    box(f'RESEARCH_INSTRUMENT_{i}',(-15.5,-14.3,y+.2,y+.9,10.78,11.4),'blue')
box('HOME_SOFA',(-18,-13,7,9,16,16.8),'warm')
box('HOME_TABLE',(-14,-11,3,5,16,16.6),'paper')
box('HOME_SLEEP_ALCOVE',(-18,-11,13,16,16,16.6),'warm')

# Actual empty civic axes: no emission strokes. Surrounding districts are
# generated around their cross streets, not opaque mass painted as negative space.
def clear_axis(x,y,margin=0):
    return abs(y+32)<17+margin or abs(x-.55*y-34)/math.sqrt(1+.55**2)<15+margin

DISTRICTS={
 'B1':[
 ('MAKER', [(-225,-95,24),(-185,-135,48),(-130,-125,72),(-80,-85,96),(-65,-5,78),(-95,55,42)],26,'warm'),
 ('RESEARCH',[(95,0,66),(140,50,108),(163,112,168),(115,169,144),(55,170,96)],32,'blue'),
 ('LIVING',[(-196,100,54),(-150,162,108),(-83,184,198),(-40,146,168),(-59,93,96),(-104,72,54)],34,'copper')],
 'B2':[
 ('MAKER',[(-228,-105,36),(-178,-128,60),(-123,-100,102),(-77,-65,72),(-60,0,54),(-99,55,42)],30,'warm'),
 ('RESEARCH',[(92,3,84),(133,53,132),(159,113,198),(112,161,150),(59,155,96)],36,'blue'),
 ('LIVING',[(-205,98,60),(-153,153,114),(-91,176,174),(-41,139,144),(-61,88,90),(-110,67,48)],38,'copper')]
}

def district(name,knots,width,material):
    floors=Geo(); walls=Geo(); trim=Geo(); roof=Geo(); supports=Geo()
    # Subdivide authored curved plan: each bay has usable depth, real floor and
    # opposite window openings. No thin fin or external decorative box.
    samples=[]
    for ia in range(len(knots)-1):
        a,b=knots[ia],knots[ia+1]; n=4
        for j in range(n):
            t=j/n
            samples.append((a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t))
    samples.append(knots[-1])
    for i in range(len(samples)-1):
        a,b=samples[i],samples[i+1]
        x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
        if clear_axis(x,y,width*.6): continue
        d=Vector((b[0]-a[0],b[1]-a[1])); d.normalize(); normal=Vector((-d.y,d.x))
        # Broad B2 courts interrupt the upper mass, rather than windows in cliffs.
        h=int((a[2]+b[2])/12)*6
        if VAR=='B2' and i%7 in [3,4]: h=max(18,h-42)
        w=width*(1+.12*math.sin(i*.9))
        p=[(a[0]+normal.x*w/2,a[1]+normal.y*w/2),(a[0]-normal.x*w/2,a[1]-normal.y*w/2),(b[0]-normal.x*w/2,b[1]-normal.y*w/2),(b[0]+normal.x*w/2,b[1]+normal.y*w/2)]
        for z in range(0,h+1,6):
            floors.prism(p,z-.55,z)
            if z==h: roof.prism(p,z,z+.25); continue
            for j,k in [(0,3),(1,2)]:
                beam(walls,p[j],p[k],.75,z,z+1.15)
                beam(walls,p[j],p[k],.75,z+4.8,z+5.45)
                # Asymmetric real window piers, visible across the full room depth.
                for t in [0,.48,.94]:
                    u=(p[j][0]*(1-t)+p[k][0]*t,p[j][1]*(1-t)+p[k][1]*t)
                    v=(u[0]+d.x*.8,u[1]+d.y*.8)
                    beam(trim,u,v,.9,z+1.15,z+4.8)
            # Local cross walls make inhabited cells; leave a 4m doorway.
            mid=((p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2)
            for s in [-1,1]:
                near=(mid[0]+normal.x*s*2,mid[1]+normal.y*s*2)
                end=p[0] if s==1 else p[1]
                beam(walls,near,end,.45,z,z+5.45)
        # Deep service cores are functional room partitions, not facade stripes.
        if i%4==0:
            mid=((p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2)
            beam(supports,mid,(mid[0]+d.x*4,mid[1]+d.y*4),5,-.6,h+2)
    floors.finish(name+'_ACTUAL_FLOORS','floor'); walls.finish(name+'_WINDOWED_INHABITED_WALLS','stone')
    trim.finish(name+'_CERAMIC_WINDOW_PIERS',material); roof.finish(name+'_ROOF_TERRACES','copper')
    supports.finish(name+'_SERVICE_CORES',material)

def courtyard_district(name,knots,width,material):
    """Swept deep streets with a tower/court rhythm, no continuous tall wall.
    Ground floors bend towards the civic section; upper courts fracture the skyline.
    Each band encloses actual multi-use floor volume with real facade apertures.
    """
    floors,walls,ceramic,roofs=Geo(),Geo(),Geo(),Geo()
    samples=[]
    # Catmull-Rom passes through authored points: curved streets rather than facets
    # of a wall made by linear interpolation. The topology remains editable mesh.
    for k in range(len(knots)-1):
        p0=knots[max(0,k-1)]; p1=knots[k]; p2=knots[k+1]; p3=knots[min(len(knots)-1,k+2)]
        for j in range(5):
            t=j/5
            samples.append(tuple(.5*((2*p1[q])+(-p0[q]+p2[q])*t+(2*p0[q]-5*p1[q]+4*p2[q]-p3[q])*t*t+(-p0[q]+3*p1[q]-3*p2[q]+p3[q])*t*t*t) for q in range(3)))
    samples.append(knots[-1])
    for i in range(len(samples)-1):
        a,b=samples[i],samples[i+1]; mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
        if clear_axis(mx,my,width*.54): continue
        d=Vector((b[0]-a[0],b[1]-a[1])); d.normalize(); n=Vector((-d.y,d.x))
        peak=(a[2]+b[2])/2
        # Five urban rooms in each wave: low inner courts and slender high accents.
        rhythm=[.50,.72,1.0,.94,.62,.35,.34,.60,.86,1.0][i%10]
        h=max(18,int(peak*rhythm/6)*6)
        for z in range(0,h+1,6):
            taper=1-.30*(z/max(1,h))
            off=6*math.sin(z/36+i*.13)
            w=width*taper
            p=[(a[0]+n.x*(off+w/2),a[1]+n.y*(off+w/2)),(a[0]+n.x*(off-w/2),a[1]+n.y*(off-w/2)),(b[0]+n.x*(off-w/2),b[1]+n.y*(off-w/2)),(b[0]+n.x*(off+w/2),b[1]+n.y*(off+w/2))]
            floors.prism(p,z-.65,z)
            if z==h: roofs.prism(p,z,z+.4); continue
            # Alternating floor setbacks are the edge of occupied rooms, not fins.
            for j,k in [(0,3),(1,2)]:
                beam(walls,p[j],p[k],.8,z,z+1)
                beam(walls,p[j],p[k],.8,z+4.5,z+5.35)
                # Nonuniform wide and narrow apertures. Solid panels form actual
                # enclosed room frontage and vertical visual continuity.
                for ta,tb in ([(0,.16),(.72,.95)] if (i+z//6)%3 else [(0,.52),(.87,1)]):
                    aa=tuple(p[j][q]*(1-ta)+p[k][q]*ta for q in (0,1))
                    bb=tuple(p[j][q]*(1-tb)+p[k][q]*tb for q in (0,1))
                    beam(ceramic,aa,bb,.85,z+1,z+4.5)
            # Partition with real through-door.
            mid=((p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2)
            for s,end in [(1,p[0]),(-1,p[1])]:
                near=(mid[0]+s*n.x*2,mid[1]+s*n.y*2)
                beam(walls,near,end,.5,z,z+5.35)
    floors.finish(name+'_DEEP_OCCUPIED_FLOORS','floor'); walls.finish(name+'_ACTUAL_WINDOW_WALLS','stone')
    ceramic.finish(name+'_OCCUPIED_FACADE_PANELS',material); roofs.finish(name+'_COURT_ROOFS','copper')

DISTRICTS['B2']=[
 ('MAKER',[(-230,-105,36),(-175,-132,78),(-113,-100,126),(-63,-64,84),(-57,10,60),(-35,37,24)],34,'warm'),
 ('RESEARCH',[(43,39,30),(93,73,96),(144,107,186),(127,171,222),(64,181,132)],38,'blue'),
 ('LIVING',[(-36,38,24),(-77,77,96),(-140,103,132),(-132,164,210),(-72,176,180),(-30,127,90)],40,'copper')]
district=courtyard_district
for name,knots,width,material in DISTRICTS[VAR]:
    district(name,knots,width,material)
    # B2 uses inhabited finger branches, not more facade decoration.
    if VAR=='B2':
        if name=='MAKER': branch=[(-155,-120,66),(-180,-183,48),(-233,-192,24)]
        elif name=='RESEARCH': branch=[(127,155,156),(201,166,96),(232,109,48)]
        else: branch=[(-128,154,132),(-207,173,96),(-236,121,42)]
        district(name+'_COURT_BRANCH',branch,width*.78,material)

# The two streets are at grade. Two broad urban axes have 0% grade in this study;
# upper district circulation is not claimed connected or safe.
g=Geo(); beam(g,(-285,-32),(285,-32),26,-.24,0); g.finish('CIVIC_AXIS_A_ACTUAL_STREET','floor')
g=Geo(); beam(g,(-99,-242),(166,240),24,-.24,0); g.finish('CIVIC_AXIS_B_ACTUAL_STREET','stone')
g=Geo(); beam(g,(0,-32),(0,2),16,-.25,0); g.finish('STREET_ENTRY_CONTINUOUS_FLOOR','floor')
# Small city trees and people are scale cues, not false occupancy evidence.
people=Geo()
for x,y,z in [(0,-12,0),(-4,-7,0),(3,4,0),(12,25,0),(-9,5,10),(-9,20,10),(-7,5,16),(-36,-30,0),(70,-32,0),(-90,-32,0)]:
    people.box(x-.22,x+.22,y-.18,y+.18,z,z+1.35)
    people.box(x-.17,x+.17,y-.16,y+.16,z+1.35,z+1.72)
people.finish('SCALE_FIGURES_1_72M_NOT_BODY_QA','people')
for i,(x,y) in enumerate([(-42,-5),(39,2),(-70,-54),(63,-60),(-145,-60),(102,-50),(-50,44)]):
    box(f'TREE_TRUNK_{i}',(x-.5,x+.5,y-.5,y+.5,0,4),'warm')
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=3,location=(x,y,5)); o=bpy.context.object
    o.name=f'TREE_CANOPY_{i}'; o.scale=(1,1,1.4); o.data.materials.append(M['green'])
box('CONTEXT_GROUND',(-18000,18000,-18000,18000,-1.8,-.7),'ground')
box('CONTEXT_WATER',(-1000,1000,-650,-290,-.68,-.65),'water')

CAMERAS={
 '01_CITY':((490,-650,340),(-15,35,65),48),
 '02_REVERSE':((-490,600,315),(-10,40,75),48),
 '03_STREET_TO_MAKING':((0,-24,1.65),(0,17,6.5),23),
 '04_RESEARCH_TO_MAKING':((-8,12,11.65),(10,17,4),21),
 '05_HOME':((-12,8,17.65),(0,-12,17.8),19),
}
for name,(loc,target,lens) in CAMERAS.items():
    bpy.ops.object.camera_add(location=loc); c=bpy.context.object; c.name=name
    c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler()
    c.data.lens=lens; c.data.clip_end=5000; c.data.clip_start=.08
scene=bpy.context.scene
scene.world.color=(.25,.25,.25); scene.world.use_nodes=True
bg=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND')
bg.inputs['Color'].default_value=(.49,.65,.75,1); bg.inputs['Strength'].default_value=.5
bpy.ops.object.light_add(type='SUN',location=(100,-200,300)); sun=bpy.context.object
sun.name='LATE_AFTERNOON_SUN'; sun.rotation_euler=(math.radians(28),math.radians(-25),math.radians(-32)); sun.data.energy=2.2; sun.data.angle=.10
for name,loc,power,size,color in [
 ('PORTAL_SKY',(0,-6,19),15000,30,(.73,.83,1)),
 ('MAKING_BOUNCE',(0,16,8),1200,12,(1,.73,.43)),
 ('RESEARCH_BOUNCE',(-17,15,14),700,9,(1,.83,.62)),
 ('HOME_BOUNCE',(-14,9,20),500,8,(1,.76,.52))]:
    bpy.ops.object.light_add(type='AREA',location=loc); ob=bpy.context.object; ob.name=name
    ob.data.energy=power; ob.data.shape='DISK'; ob.data.size=size; ob.data.color=color
scene.render.engine='CYCLES'; scene.cycles.samples=24; scene.cycles.use_denoising=True
scene.render.resolution_x=1100; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1
scene.camera=bpy.data.objects['01_CITY']
scene['study']=VAR; scene['art']='UNREVIEWED_HOLD'; scene['formal_331_993']='NOT RUN'
scene['artificial_fill_lights']='Yes: four area lights. Images do not prove daylight performance.'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(VAR+'.blend')),compress=True)
# Export geometry only. Context ground/water are explicitly excluded from GLB.
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
    if o.type=='MESH' and not o.name.startswith('CONTEXT'): o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/(VAR+'.glb')),use_selection=True,export_format='GLB',export_yup=True)
manifest={'study':VAR,'blender':bpy.app.version_string,'cameras':CAMERAS,'seed':56,'render':{'resolution':[1100,720],'samples':24,'engine':'Cycles CPU','artificial_fill_lights':True},'axes':[[[-285,-32,0],[285,-32,0]],[[-99,-242,0],[166,240,0]]],'formal_331_993':'NOT RUN','formal_G0_S1_G1_G2_G3':'NOT RUN','upper_district_circulation':'NOT VERIFIED','art':'HOLD pending actual image review'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('SAVED',VAR,len(scene.objects),flush=True)
if 'render' in args:
    for name in CAMERAS:
        scene.camera=bpy.data.objects[name]; scene.render.filepath=str(OUT/(name+'.png'))
        bpy.ops.render.render(write_still=True); print('RENDERED',VAR,name,flush=True)
