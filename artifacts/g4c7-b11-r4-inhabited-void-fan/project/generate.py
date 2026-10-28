"""B11-R4: authored inhabited civic fan research. Never Minecraft construction.
Three staggered, occupied radial gallery sections with actual room boundary triangles
and door apertures oriented toward one shared civic void. Local topology research only.
"""
from pathlib import Path
import json, hashlib, math
import numpy as np
import trimesh

OUT=Path(__file__).resolve().parent/'output'
OUT.mkdir(exist_ok=True)
parts={k:[] for k in ['public','room','envelope','structure','detail']}
rooms=[]
def v(r,a,z,cx=0,cy=0):return np.array([cx+r*np.cos(a),cy+r*np.sin(a),z],float)
def quad(a,b,c,d,category):
    mesh=trimesh.Trimesh(vertices=np.array([a,b,c,d]),faces=np.array([[0,1,2],[0,2,3]]),process=False)
    parts[category].append(mesh)
def box(x,y,z,dim,cat,angle=0):
    m=trimesh.creation.box(extents=dim);R=trimesh.transformations.rotation_matrix(angle,[0,0,1]);m.apply_transform(R);m.apply_translation([x,y,z]);parts[cat].append(m)
def wedge_floor(r0,r1,a0,a1,z,cat):
    quad(v(r0,a0,z),v(r1,a0,z),v(r1,a1,z),v(r0,a1,z),cat)
def rwall(r,a0,a1,z0,z1,cat):
    quad(v(r,a0,z0),v(r,a1,z0),v(r,a1,z1),v(r,a0,z1),cat)
def twall(r0,r1,a,z0,z1,cat):
    quad(v(r0,a,z0),v(r1,a,z0),v(r1,a,z1),v(r0,a,z1),cat)

# Angles are intentionally overlapping and each civic terrace is a different radius/level.
strands=[
  dict(name='lower',start=-130,end=54,z=10,r0=43,rroom=57,rout=89,n=10),
  dict(name='middle',start=15,end=210,z=36,r0=49,rroom=64,rout=100,n=11),
  dict(name='upper',start=158,end=366,z=66,r0=56,rroom=72,rout=112,n=11),
]
for g,band in enumerate(strands):
    s=np.deg2rad(band['start']);e=np.deg2rad(band['end']);n=band['n'];r0=band['r0'];r1=band['rroom'];r2=band['rout'];z=band['z'];dz=(e-s)/n
    for k in range(n):
        a=s+dz*k;b=a+dz;c=(a+b)/2
        # Each room's floor is structurally shared with the public gallery at exactly the same z.
        wedge_floor(r0,r1,a,b,z,'public')
        wedge_floor(r1,r2,a,b,z,'room')
        wedge_floor(r1,r2,a,b,z+8.3,'envelope')
        # Facade: actual two side segments and lintel, 43%-width clear opening from z to z+4.
        cuta=a+.30*(b-a);cutb=a+.70*(b-a)
        rwall(r1,a,cuta,z,z+8.3,'room')
        rwall(r1,cutb,b,z,z+8.3,'room')
        rwall(r1,cuta,cutb,z+4.2,z+8.3,'room')
        rwall(r2,a,b,z,z+8.3,'room')
        twall(r1,r2,a,z,z+8.3,'room')
        twall(r1,r2,b,z,z+8.3,'room')
        # Public lower rail and inhabited deep roof terraces; rhythmic structural arches.
        if k%2==0:
            rwall(r0,a,a+dz*.10,z,z+1.35,'detail')
            rwall(r0,b-dz*.10,b,z,z+1.35,'detail')
        # Roof ridges break the flat shelf into a triangulated sloping family of occupied roofs.
        j=(k+.3*g);lift=4.5+4*abs(math.sin(1.25*j))
        apex=v(r2-6,c,z+8.3+lift)
        quad(v(r1,a,z+8.3),v(r2,a,z+8.3),apex,v(r1,c,z+8.3),'envelope')
        quad(v(r1,c,z+8.3),apex,v(r2,b,z+8.3),v(r1,b,z+8.3),'envelope')
        # Supports: exterior columns up to elevated gallery, not certified structure.
        if k in (0,n-1) or k%3==0:
            pos=v(r2-5,c,z*.5)
            box(pos[0],pos[1],z*.5,[3.2,4.0,max(0.5,z)],'structure',angle=c)
        room_pt=v((r1+r2)/2,c,z+5.7)
        door_start=v(r1+3,c,z+2.0)
        door_end=v(r1-3,c,z+2.0)
        rooms.append(dict(id=f'{band["name"]}-{k:02d}',band=band['name'],angle_deg=float(np.rad2deg(c)),level_m=z,point=room_pt.tolist(),door_a=door_start.tolist(),door_b=door_end.tolist(),radial=[np.cos(c),np.sin(c),0.],tangent=[-np.sin(c),np.cos(c),0.],outer_r=r2,inner_r=r1,theta_width=dz))
    # One continuous promenade per strand; no fake ramps or city-wide safe connection claim.
    for k in range(n):
        aa=s+(e-s)*k/n;bb=s+(e-s)*(k+1)/n
        # Continuous parapet beyond room back facade, different heights.
        rwall(r2+1.5,aa,bb,z+8.3,z+9.2,'detail')

# One elevated public viewing platform in the shared central void. No pretend walkable link.
for a,b in [(-.5,.25),(.25,.7)]:wedge_floor(20,37,a,b,52,'public')
# Asymmetric open-edged diagonal spines supporting landscape depth as form study.
for angle,length,zend in [(-.45,90,76),(2.0,115,104),(4.12,104,89)]:
    start=v(22,angle,10);end=v(length,angle+.10,zend)
    direction=end-start
    link=trimesh.creation.box(extents=[3.4,4.2,np.linalg.norm(direction)])
    rot=trimesh.geometry.align_vectors([0,0,1],direction)
    link.apply_transform(rot);link.apply_translation((start+end)/2)
    parts['structure'].append(link)

combined=[];info={}
colors={'public':[110,195,193,255],'room':[223,190,142,255],'envelope':[161,178,211,255],'structure':[84,107,131,255],'detail':[233,165,119,255]}
for key,meshes in parts.items():
    assert meshes
    m=trimesh.util.concatenate(meshes)
    m.visual.vertex_colors=colors[key]
    m.export(OUT/(key+'.ply'))
    combined.append(m)
    info[key]={'faces':len(m.faces),'vertices':len(m.vertices),'sha256':hashlib.sha256((OUT/(key+'.ply')).read_bytes()).hexdigest()}
allm=trimesh.util.concatenate(combined)
allm.export(OUT/'model.obj')
meta={'stage':'B11-R4','character':'local_only_real_room_and_civic_void_form_study',
  'rooms':rooms,'parts':info,'faces':len(allm.faces),'vertices':len(allm.vertices),
  'obj_sha256':hashlib.sha256((OUT/'model.obj').read_bytes()).hexdigest(),
  'bounds_m':allm.bounds.tolist(),'real_room_certification':'NOT_CERTIFIED',
  'door_local_witness':'NOT_YET_TESTED','floor_and_structural_load':'NOT_TESTED',
  'continuous_human_walk':'NOT_TESTED','formal_331_993':'NOT_RUN',
  'S1_G1_G2_G3':'NOT_RUN','art_approval':'NOT_GRANTED','minecraft':'FORBIDDEN',
  'warning':'Bands have independent elevations: continuous vertical walk and structural support NOT PROVEN'}
(OUT/'manifest.json').write_text(json.dumps(meta,indent=2))
print('faces',len(allm.faces),'verts',len(allm.vertices),'bounds',allm.bounds,'rooms',len(rooms))
