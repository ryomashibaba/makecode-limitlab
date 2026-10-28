"""A83-B6 local G0 shared inhabited edge. Research only: NOT S1/G1/G2/G3, no Minecraft construction.
World units: metres, z vertical. Public field, curvilinear shared facade, 8 room candidates on two floors, 2 stair approaches.
"""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
OUT.mkdir(parents=True, exist_ok=True)
components=[]
meta=[]

def color(hex):
    return tuple(int(hex[i:i+2],16) for i in (1,3,5))+(255,)
COLORS={'plaza':color('#567d83'),'floor':color('#c5c3a6'),'roof':color('#739c92'),
        'frontage':color('#b5d0c9'),'partition':color('#a5b6b2'),'support':color('#be906c'),
        'stair':color('#d5b98b'),'landing':color('#d8b88c'),'furnish':color('#d7ae72'),
        'parapet':color('#597977'),'garden':color('#527b64')}

def add(name,vs,faces,category):
    vs=np.asarray(vs,float);faces=np.asarray(faces,int)
    mesh=trimesh.Trimesh(vertices=vs,faces=faces,process=False)
    mesh.visual.face_colors=np.tile(COLORS[category],(len(faces),1))
    components.append(mesh)
    meta.append({'name':name,'category':category,'vertices':len(vs),'triangles':len(faces)})

def quad(name,p,q,r,s,cat):add(name,[p,q,r,s],[[0,1,2],[0,2,3]],cat)

def cube(name,x0,x1,y0,y1,z0,z1,cat):
    verts=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],
           [x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]]
    faces=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],
           [1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]
    add(name,verts,faces,cat)

def curve(x):return 8.7*math.sin(math.pi*x/72) + 3.6*math.sin(2.6*math.pi*x/72+0.2)

# Single common ground, including exterior civic place and all occupied frontages.
cube('one_shared_ground',-78,78,-55,58,-.50,0,'plaza')
# One uninterrupted inhabited upper floor, generated from the same curvilinear front edge as the rooms,
# rather than individual buildings/floor shelves. Separate panels abut exactly, all in one surface.
xs=np.linspace(-64,64,129)
for i,(x0,x1) in enumerate(zip(xs[:-1],xs[1:])):
    y0,y1=curve(x0),curve(x1)
    # frontage ground floor and upper shared floor. upper deck face is also lower room ceiling.
    quad(f'shared_upper_floor_{i}',(x0,y0,8),(x1,y1,8),(x1,y1+24,8),(x0,y0+24,8),'floor')
    quad(f'shared_roof_{i}',(x0,y0,16),(x1,y1,16),(x1,y1+24,16),(x0,y0+24,16),'roof')
    quad(f'backwall_ground_{i}',(x0,y0+24,0),(x1,y1+24,0),(x1,y1+24,8),(x0,y0+24,8),'frontage')
    quad(f'backwall_upper_{i}',(x0,y0+24,8),(x1,y1+24,8),(x1,y1+24,16),(x0,y0+24,16),'frontage')
    # deep solid parapet creates upper roof pedestrian edge where needed, but no giant outer wall.
    quad(f'roof_edge_{i}',(x0,y0,16),(x1,y1,16),(x1,y1,16.7),(x0,y0,16.7),'parapet')

# Integrate main shared curved public facade: door clearances are actual missing triangle patches.
DOORS=[-48,-16,16,48]
breaks={-64,64}
for x in np.arange(-64,64.0001,1):breaks.add(round(float(x),5))
for x in DOORS:breaks.add(x-2);breaks.add(x+2)
breaks=sorted(breaks)
for i,(x0,x1) in enumerate(zip(breaks[:-1],breaks[1:])):
    y0,y1=curve(x0),curve(x1)
    door=any(x0>=cx-2-1e-8 and x1<=cx+2+1e-8 for cx in DOORS)
    for level in (0,8):
        z0=level+4.8 if door else level
        quad(f'frontage_L{level}_seg{i}',(x0,y0,z0),(x1,y1,z0),(x1,y1,level+8),(x0,y0,level+8),'frontage')
# Radiating party walls at 3 room boundaries: actual structural room divisions with a small service doorway gap.
for i,x in enumerate([-32,0,32]):
    yf=curve(x)
    for level in (0,8):
        # doorway inside shared gallery at y_front+10..16, up to 4.5m
        for a,b in [(yf,yf+10),(yf+16,yf+24)]:
            quad(f'party_{i}_{level}_{a:.1f}',(x,a,level),(x,b,level),(x,b,level+8),(x,a,level+8),'partition')
        quad(f'party_lintel_{i}_{level}',(x,yf+10,level+4.5),(x,yf+16,level+4.5),
             (x,yf+16,level+8),(x,yf+10,level+8),'partition')
# Side walls close both ends. Four contiguous occupied bands per floor, no detached buildings.
for x in (-64,64):
    yf=curve(x)
    for level in (0,8):
        quad(f'sidewall_{x}_L{level}',(x,yf,level),(x,yf+24,level),
             (x,yf+24,level+8),(x,yf,level+8),'frontage')
# 8 visible room use witnesses; these are real solids but not certified furnished habitable rooms.
for j,cx in enumerate(DOORS):
    for level in (0,8):
        yf=curve(cx)
        cube(f'activity_counter_{j}_L{level}',cx-5.8,cx+5.8,yf+14,yf+16.3,level+.1,level+1.4,'furnish')
        cube(f'activity_display_{j}_L{level}',cx-6,cx+6,yf+18,yf+18.9,level+1.7,level+5.8,'garden' if (j+level//8)%2 else 'furnish')
# Two long independent stair systems (48 treads each), ending at actual upper door lip.
# The stair is on civic field rather than a long elevated bridge. Each tread spans 0.35m, rise=8/48m.
for k,cx in enumerate((-48,48)):
    start=curve(cx)-18.0
    for i in range(48):
        y0=start+i*.375;y1=y0+.375
        z=(i+1)*(8/48.)
        cube(f'stair_{k}_{i}',cx-1.75,cx+1.75,y0,y1,z-.15,z,'stair')
    # lip abuts door plane and the single 8m roof-floor plane. Not a certified complete human sweep.
    cube(f'upper_door_landing_{k}',cx-2,cx+2,curve(cx)-.55,curve(cx)+2.0,7.78,8,'landing')
    # A low-side handrail simulation is not a human-safety proof; left out of occupancy gate.
# Substantial ground-rooted support under shared upper floor, distributed in ways matched to occupancy bands.
for x in [-60,-35,-8,21,55,61]:
    yf=curve(x)
    cube(f'grounded_support_{x}',x-1.2,x+1.2,yf+19,yf+21,0,8,'support')

# Actual mesh for inspection (face colours used in VTK PLY read, OBJ is independent source of truth).
combined=trimesh.util.concatenate(components)
combined.export(OUT/'b6_shared_occupied_boundary.obj',file_type='obj',include_color=True)
combined.export(OUT/'b6_shared_occupied_boundary.ply',file_type='ply')
metaout={'stage':'A83_B6_LOCAL_TRUE_3D_RESEARCH','scene':'SHARED_PUBLIC_FRONTAGE_SIX_DISTRICTS_NOT_CLAIMED',
 'program_seeds':8,'actual_door_intentions':8,'actual_stair_treads':96,
 'two_access_systems':2,'one_shared_upper_floor':True,
 'source_parts':len(meta),'mesh':{'triangles':len(combined.faces),'vertices':len(combined.vertices)},
 'doors':DOORS,'model_sha256':hashlib.sha256((OUT/'b6_shared_occupied_boundary.obj').read_bytes()).hexdigest(),
 'formal_s1_g1_g2_g3':'NOT_RUN','full_human_sweep':'NOT_TESTED','structural_load':'NOT_TESTED',
 'geometry_room_enclosure':'NOT_YET_VERIFIED','city_scale_form':'NOT_TESTED',
 'art':'HOLD_REQUIRES_REAL_IMAGE_REVIEW','minecraft_construction':'FORBIDDEN'}
(OUT/'manifest.json').write_text(json.dumps(metaout,indent=2))
print(json.dumps(metaout,indent=2))
