"""G4-C7 A83-B3: spatial prototype, NOT approved artwork, safety, or MakeCode construction.
A single authored 3D mesh of three differently sized occupied pavilions connected by
one ground-level civic landscape. Each contains two truly layered spaces, open portals,
a shared floor slab and a physically touching external stair. Research only.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.ops import triangulate

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
objects=[]
COLORS={
'earth':(0.18,0.26,0.31), 'ground':(0.19,0.29,0.32),
'slab':(0.25,0.44,0.48),'facade':(0.56,0.69,0.69), 'roof':(0.72,0.64,0.50),
'frame':(0.72,0.45,0.28), 'glass':(0.16,0.51,0.59), 'stair':(0.61,0.73,0.72),
'market':(0.91,0.58,0.31), 'workshop':(0.69,0.49,0.28), 'garden':(0.37,0.58,0.43),
'rail':(0.83,0.80,0.63), 'activity':(0.81,0.63,0.48)
}

def add(name,typ,triangles):
    a=np.asarray(triangles,dtype=float).reshape(-1,3,3)
    assert len(a)>0 and np.isfinite(a).all(),name
    areas=np.linalg.norm(np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]),axis=1)/2
    assert (areas>1e-7).all(), (name,float(areas.min()))
    objects.append({'name':name,'material':typ,'triangles':a})

def quad(a,b,c,d):return [[a,b,c],[a,c,d]]

def box(name,typ,x0,x1,y0,y1,z0,z1):
    assert x1>x0 and y1>y0 and z1>z0,(name,x0,x1,y0,y1,z0,z1)
    v=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
       (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    add(name,typ,sum((quad(*[v[i] for i in face]) for face in f),[]))

def flat_polygon(name,typ,points,z):
    poly=Polygon(points)
    assert poly.is_valid and poly.area>1
    tris=[]
    for t in triangulate(poly):
        if not poly.covers(t.representative_point()):continue
        p=list(t.exterior.coords)[:3]
        tris.append([(x,y,z) for x,y in p])
    add(name,typ,tris)

def walls_between(name,typ,points,z0,z1,door_edge=None,door_width=9.0,door_h=7.0):
    """Lateral bounding triangles, never a solid wall where a true doorway is requested."""
    tris=[]
    for i,(a,b) in enumerate(zip(points,points[1:]+points[:1])):
        ax,ay=a;bx,by=b
        if i!=door_edge:
            tris+=quad((ax,ay,z0),(bx,by,z0),(bx,by,z1),(ax,ay,z1));continue
        length=math.dist(a,b)
        assert length>door_width+8
        t0=(length-door_width)/2/length;t1=1-t0
        p0=(ax+(bx-ax)*t0,ay+(by-ay)*t0)
        p1=(ax+(bx-ax)*t1,ay+(by-ay)*t1)
        tris+=quad((ax,ay,z0),(p0[0],p0[1],z0),(p0[0],p0[1],z1),(ax,ay,z1))
        tris+=quad((p1[0],p1[1],z0),(bx,by,z0),(bx,by,z1),(p1[0],p1[1],z1))
        tris+=quad((p0[0],p0[1],z0+door_h),(p1[0],p1[1],z0+door_h),
                    (p1[0],p1[1],z1),(p0[0],p0[1],z1))
    add(name,typ,tris)

# 3 asymmetric inhabited nuclei: still deliberately judged on image, not named as a finished city.
regions=[
    dict(id='W',cx=-210,cy=0,sx=1.00,sy=.86,dy=0,facade='market',roof_z=38),
    dict(id='C',cx=0,cy=26,sx=1.20,sy=1.10,dy=6,facade='workshop',roof_z=43),
    dict(id='E',cx=225,cy=-12,sx=.91,sy=1.00,dy=0,facade='garden',roof_z=35),
]
# Ground connections: directly overlapping sections (no standalone disconnected district).
box('continuous_civic_ground','ground',-390,380,-53,156,-1.0,-0.1)
for x in np.arange(-360,355,28):
    box(f'civic_ground_paving_{int(x)}','slab',float(x),float(x)+.65,-34,16,-.08,.02)

manifest={'stage':'A83_B3_G0_TRUE3D_PROTOTYPE_ONLY','regions':[],
          'actual_completed_minecraft_city':False,
          'true_images':[], 'formal_safety':'NOT_RUN','art_acceptance':'NOT_APPROVED',
          'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN'}
for d in regions:
    x=d['cx']; y=d['cy']; sx=d['sx']; sy=d['sy']; id=d['id']
    points=[(x+dx*sx,y+dy*sy) for dx,dy in [(-44,8),(46,8),(68,37),(53,91),(-56,91),(-70,41)]]
    zmid=16+d['dy']*.17; top=30+d['dy']*.23
    flat_polygon(id+'_true_lower_floor','slab',points,0.05)
    flat_polygon(id+'_true_shared_mid_floor','slab',points,zmid)
    # The same polygon as bottom ceiling AND upper floor, not two offset overlapping meshes.
    # Ground portal on edge 0 faces a plaza. Upper portal is on edge 3 at rear terrace.
    walls_between(id+'_lower_facade_true_open','facade',points,.05,zmid,door_edge=0,door_width=12,door_h=8)
    walls_between(id+'_upper_facade_true_open','facade',points,zmid,top,door_edge=3,door_width=12,door_h=7)
    # Roof is non-horizontal; physically touches side wall top in this prototype at all boundaries.
    flat_polygon(id+'_continuous_upper_roof','roof',points,top)
    # Formal roof's skyline fins would be an exterior ornament: deliberately excluded.
    # Two bands of framed program windows on each side, touching real envelope faces visually.
    for q in range(1,3):
        a,b=points[q],points[q+1]
        for h in (zmid*.5,zmid+(top-zmid)*.6):
            # purely surface glazing, not a verified open ventilation window
            aa=np.array(a); bb=np.array(b); mid=(aa+bb)*.5
            nn=np.array([-(bb-aa)[1],(bb-aa)[0]],dtype=float);nn/=np.linalg.norm(nn)
            u=mid+nn*.15; length=np.linalg.norm(bb-aa)
            box(f'{id}_inhabited_facade_luminaire_{q}_{int(h)}','glass',float(u[0]-1.0),float(u[0]+1.0),
                float(u[1]-1),float(u[1]+1),h-2.1,h+2.1)
    # direct eye-height public activities: counter stalls and reading screens inside actual lower rooms
    for s in [-1,0,1]:
        box(f'{id}_lower_market_station_{s}',d['facade'],x+s*16-5,x+s*16+5,y+30,y+35,.05,2.3)
        box(f'{id}_upper_activity_shelf_{s}','activity',x+s*14-6,x+s*14+6,y+44,y+48,zmid,zmid+2.7)
    # external stairs along west side; 80 defined treads reach exact zmid without a vertical discontinuity
    # 80*0.2 rise, each tread 0.75 horizontal; no claim of accessible ramp or human safety
    n=80;rise=zmid/n;startx=x-125;back_y=y+91*sy;starty=back_y+8
    for i in range(n):
        a=startx+i*.75;b=a+.75; z=(i+1)*rise
        box(f'{id}_actual_stair_tread_{i}','stair',a,b,starty,starty+5,z-.16,z)
    # Continuous gallery of zmid, attached to last tread and to rear-room upper opening.
    # stairs end at x-65; gallery extends across rear facade to central entrance.
    box(id+'_upper_gallery','slab',x-66,x+42,back_y-.4,back_y+23,zmid-.16,zmid)
    # landing in stair's first 1m at ground, not an airborne entry
    box(id+'_stair_start_ground','slab',startx-3,startx+2,starty-2,starty+7,-.05,.05)
    # Separate upper-floor corner footings/columns, painted as structure but load not certified
    for j,(ox,oy) in enumerate([(-48,22),(48,22),(-45,74),(44,74)]):
        box(f'{id}_upper_slab_ground_column_{j}','frame',x+ox-1.4,x+ox+1.4,
            y+oy-1.4,y+oy+1.4,0,zmid)
    manifest['regions'].append({'id':id,'lower_z':0.05,'shared_mid_floor_z':zmid,
       'upper_roof_z':top,'ground_entry_edge':0,'upper_entry_edge':3,
       'stairs':n,'stair_rise':rise,'stairs_last_height':zmid,
       'ground_room':'TRUE_FACE_BOUNDING_ONLY_PARTIAL_OPENING',
       'upper_room':'TRUE_FACE_BOUNDING_ONLY_PARTIAL_OPENING',
       'valid_human_access':'NOT_TESTED', 'real_structural_load':'NOT_TESTED'})

# Open-air planted strips leave visible urban plaza program separation without false rooms
for k in range(18):
    x=-350+k*39
    if min(abs(x-d['cx']) for d in regions)<82:continue
    box('urban_growth_planter_'+str(k),'garden',x-8,x+8,-46,-30,.02,1.3)

# Write triangles once, all down-stream readers must reopen OBJ, not use objects() silently.
obj=OUT/'a83_b3_integrated_civic_study.obj';mtl=OUT/'a83_b3_integrated_civic_study.mtl'
with open(mtl,'w') as f:
    for name,(r,g,b) in COLORS.items():f.write(f'newmtl {name}\nKd {r:.3f} {g:.3f} {b:.3f}\nKa .15 .15 .15\nKs .08 .08 .08\nNs 8\n\n')
with open(obj,'w') as f:
    f.write(f'mtllib {mtl.name}\n')
    v=1
    for item in objects:
        f.write('o '+item['name']+'\nusemtl '+item['material']+'\n')
        for tri in item['triangles']:
            for xyz in tri:f.write('v %.6f %.6f %.6f\n'%tuple(xyz))
            f.write(f'f {v} {v+1} {v+2}\n');v+=3
ntri=sum(len(o['triangles']) for o in objects)
manifest['mesh']={'objects':len(objects),'triangles':ntri,'vertices':3*ntri,
                 'obj_sha256':hashlib.sha256(obj.read_bytes()).hexdigest()}
manifest['limits']={'full_human_swept_volume':'NOT_TESTED','real_load_path':'NOT_TESTED',
    'watertight_room_check':'NOT_TESTED','full_interdistrict_evacuation':'NOT_TESTED',
    '331_human_993_foot_samples':'NOT_RUN'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
