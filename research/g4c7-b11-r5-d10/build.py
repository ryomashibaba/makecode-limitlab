"""D10: authored civic fault-section, 2 variants; no mining, no safety claim.
Not derived from D7/D8/D9 primitive generator; spatial program in same scene.
"""
from pathlib import Path
import numpy as np, trimesh, hashlib, json, math, argparse
ROOT=Path(__file__).resolve().parent
PAL={'terrain':(56,76,87,255),'fabrication':(202,150,116,255),'research':(101,168,191,255),
     'habitat':(171,195,168,255),'city_body':(145,166,179,255),
     'public':(239,207,141,255),'glass':(90,211,215,180),
     'frame':(104,129,154,255),'service':(183,103,98,255),'vegetation':(105,162,136,255)}
parts={k:[] for k in PAL}
E1=(-445,120);E2=(155,165)

def add(mesh,role):
    assert np.isfinite(mesh.vertices).all() and len(mesh.faces)>0
    mesh.visual.vertex_colors=np.tile(PAL[role],(len(mesh.vertices),1));parts[role].append(mesh)
def box(c,d,role):
    mesh=trimesh.creation.box(extents=d);mesh.apply_translation(c);add(mesh,role)
def rod(a,b,r,role):
    add(trimesh.creation.cylinder(radius=r,segment=[a,b],sections=9),role)
def polyprism(p,zlo,zhi,role,top_shift=(0,0)):
    p=np.array(p,float);n=len(p);assert n>=3 and zhi>zlo
    q=p+np.array(top_shift,float)
    v=np.vstack([np.c_[p,np.full(n,zlo)],np.c_[q,np.full(n,zhi)]])
    f=[]
    for j in range(1,n-1):f.extend([[0,j+1,j],[n,n+j,n+j+1]])
    for j in range(n):k=(j+1)%n;f.extend([[j,k,n+k],[j,n+k,n+j]])
    add(trimesh.Trimesh(vertices=v,faces=f,process=False),role)
def loft_section(stations,role):
    """Loft angular 6-vertex section along y. Each station [(x,z)*6] has its own y."""
    vv=[]
    for y,section in stations:
        assert len(section)==6
        vv.extend([[x,y,z] for x,z in section])
    f=[];m=len(stations)
    for i in range(m-1):
        a=i*6;b=(i+1)*6
        for j in range(6):k=(j+1)%6;f.extend([[a+j,b+j,b+k],[a+j,b+k,a+k]])
    for i in range(1,5):f.append([0,i,i+1]);f.append([(m-1)*6,(m-1)*6+i+1,(m-1)*6+i])
    add(trimesh.Trimesh(vertices=np.array(vv),faces=np.array(f),process=False),role)
def walk(points,width,role):
    """Physically meshed walk surface (not validated safe access)."""
    for a,b in zip(points,points[1:]):
        a=np.array(a,float);b=np.array(b,float);d=b-a;n=np.linalg.norm(d[:2]);assert n>1
        u=np.array([-d[1],d[0],0])/n*width*.5
        top=[a-u,a+u,b+u,b-u];vs=np.array(top+[p-[0,0,.8] for p in top]);f=[]
        for j in range(1,3):f.append([0,j,j+1]);f.append([4,4+j+1,4+j])
        for j in range(4):k=(j+1)%4;f.extend([[j,k,k+4],[j,k+4,j+4]])
        add(trimesh.Trimesh(vertices=vs,faces=f,process=False),role)
def maker(h):
    # Huge tool-and-space hall with long side physically open to shared square.
    polyprism([(-710,-245),(-230,-240),(-196,-28),(-352,36),(-700,16)],9,17,'terrain')
    box((-463,-126,18),(380,200,3),'fabrication')
    for x in (-625,-520,-415,-308):
        box((x,-130,24),(27,22,11),'service')
        rod((x,-115,29),(x+6,-82,43),2.0,'frame')
    # Split roof is physically absent over public presentation area; no solid cliff wall.
    z=18+h
    polyprism([(-680,-260),(-310,-236),(-290,-82),(-660,-116)],z,z+8,'city_body',top_shift=(26,22))
    polyprism([(-610,-80),(-410,-55),(-300,-32),(-540,-15)],z+13,z+20,'city_body',top_shift=(18,26))
    # Distinct structural counterforts at perimeter, not a repeat of ceiling slabs.
    for a,b in [((-630,-210,17),(-623,-125,z)),((-340,-225,17),(-314,-99,z)),((-585,-18,17),(-540,-40,z+15))]:rod(a,b,4.2,'frame')
    # Broad two-sided public exposure to actual fabrication (not occluded by solid north wall).
    walk([(-670,41,17.7),(-540,53,17.7),(-410,58,17.7),(-260,62,17.7)],11,'public')
    box((-460,-8,20),(98,52,4),'public')
    for x in (-520,-460,-390):box((x,-25,22.5),(14,9,3),'service')
    return z

def research():
    # Research/culture is a heavily indented inhabited rift terrace, not a tower.
    # Each section makes outer-crest and inner-terrace part of SAME solid loft.
    stations=[]
    for y,L,R,h,foot in [(-90,85,300,121,108),(-20,30,390,151,95),
            (70,65,345,191,103),(155,55,455,184,99),(260,92,405,230,120),
            (390,130,540,251,124),(505,180,590,238,118)]:
        # 6-vertex polygon: inner nose, ledge underside, lower mass foot, remote support,
        # crest, upper active depth. Skewed per station so no repeated tubes.
        pts=[(L,foot),(L+32,foot-34),(R-80,19),(R,21),(R-40,h),(L+112,h-6)]
        stations.append((y,pts))
    loft_section(stations,'city_body')
    # Public research rooms occupy actual floors inside/outside the folded city mass.
    for p,z in [([(97,75),(217,88),(233,144),(105,139)],113),
                ([(120,234),(325,226),(366,279),(151,296)],146),
                ([(198,380),(414,383),(435,430),(207,447)],182)]:
        polyprism(p,z-3,z,'research')
        # Turn each activity into readable contained volume with transparent outward interface.
        x0=min(pt[0] for pt in p)+28;y0=sum(pt[1] for pt in p)/len(p)
        box((x0+39,y0,z+8),(77,25,15),'research')
        box((x0+39,y0-13,z+8),(69,1.8,10),'glass')
        for dx in (-15,12):box((x0+39+dx,y0,z+2),(14,5,3),'public')
    # research and craft reveal stage, accessible ground in this study
    box((95,78,18.2),(103,72,2.4),'public')
    for x in (64,94,124):box((x,80,21.8),(11,9,4),'research')
    # Very deep opening between ascending activity decks, not a filled retaining wall.
    # This is an honest visual hypothesis, not a sun or structural proof.

def habitat():
    # One irregular inhabited crescent-like cliff crest with actual rooms/courts, not 69 towers.
    sections=[]
    for y,L,R,z in [(280,195,550,190),(405,178,650,227),(555,265,735,278),
                     (740,321,815,305),(900,415,780,279)]:
        sections.append((y,[(L,130),(L+30,93),(R-130,46),(R,61),(R-40,z),(L+100,z-12)]))
    loft_section(sections,'habitat')
    # Perched residential courts are built as differentiated small room volumes behind active edge
    for x,y,z,angle in [(354,423,212,0),(421,572,256,1),(525,713,287,2)]:
        polyprism([(x-51,y-34),(x+47,y-34),(x+59,y+20),(x+15,y+49),(x-66,y+28)],z-4,z,'public')
        box((x,y+15,z+12),(88,34,23),'habitat')
        box((x,y-3,z+9),(58,2,11),'glass')
        box((x+48,y+13,z+3),(10,28,6),'vegetation')

def vertical_core(x,y):
    # Two actually modelled cage shafts + 3 real landings; unmodelled lift travel mechanics.
    for dx in (-6.5,6.5):
        for dy in (-6.5,6.5):rod((x+dx,y+dy,17),(x+dx,y+dy,215),.8,'frame')
    for z in (18,112,209):
        box((x,y,z-.7),(16,16,1.4),'public')
    for z in (70,160):
        box((x-6.5,y,z),(1.0,12,1),'frame')

def create(variant='all',clearance=70):
    assert variant in ('all','no_research') and clearance in (70,90)
    for k in parts:parts[k].clear()
    # City-scale ground and public spine, not architecturally generic towers.
    polyprism([(-1400,-700),(-900,-1050),(-230,-780),(260,-680),(930,-340),(1260,430),(950,1050),(-160,1100),(-1000,620)],-22,15,'terrain')
    # 1.7-km representative human corridor, not a certified route.
    pts=[(-1080,-345,18),(-920,-230,18),(-750,-126,18),(-650,-35,18),(-540,53,18),
         (-400,88,18),(-245,97,18),(-90,108,18),(55,112,18),(155,165,18),
         (285,260,18),(420,390,18),(545,560,18)]
    walk(pts,12,'public')
    roof=maker(clearance)
    if variant=='all': research();habitat()
    else:
        # In the counterfactual, the research and habitat programmes and their
        # actual dependent cliff-forms disappear, leaving just manufacturing.
        pass
    for x,y in [E1,E2]:vertical_core(x,y)
    # Public exchange terrace / maker displays; activity not merely a text label.
    box((-152,144,19),(162,54,3),'public')
    for x in (-188,-135,-84):box((x,160,22.5),(21,17,5),'fabrication')
    # Vertical cores grounded and visible. Upper landings NOT connected to upper
    # research rooms in current geometry; this is intentionally an unpassed gate.
    folder=ROOT/f'{variant}_{clearance}';folder.mkdir(exist_ok=True)
    meshes=[];scene=trimesh.Scene();cats={}
    for role,m in parts.items():
        if not m:continue
        mesh=trimesh.util.concatenate(m)
        mesh.export(folder/f'{role}.ply');scene.add_geometry(mesh,geom_name=role);meshes.append(mesh)
        cats[role]={'triangles':len(mesh.faces),'sha256_ply':hashlib.sha256((folder/f'{role}.ply').read_bytes()).hexdigest()}
    joined=trimesh.util.concatenate(meshes)
    joined.export(folder/'study.obj');scene.export(folder/'study.glb')
    manifest={'stage':'B11-R5 D10','variant':variant,'clearance_target_m':clearance,
      'bounds_m':joined.bounds.tolist(),'triangles':len(joined.faces),'vertices':len(joined.vertices),
      'sha256_obj':hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest(),
      'sha256_glb':hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest(),
      'categories':cats,'civic_path_points':pts,'sha256_program_source':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'status':{'G0':'NOT_ADOPTED','ART':'HOLD','formal_S1_G1_G2_G3':'NOT_RUN','Minecraft':'FORBIDDEN'},
      'limits':['representative route 3D width not certified','upper landing does NOT guarantee room access',
       'no structural support calculation','not entire 10km city','no exact interior room closure or real lifts',
       '90m scenario not yet verified safe over the entire workshop']}
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return manifest
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--variant',choices=['all','no_research','both'],default='both');p.add_argument('--clearance',type=int,choices=[70,90],default=70);a=p.parse_args()
    for v in (['all','no_research'] if a.variant=='both' else [a.variant]):
        m=create(v,a.clearance);print(v,m['triangles'],m['sha256_obj'],flush=True)