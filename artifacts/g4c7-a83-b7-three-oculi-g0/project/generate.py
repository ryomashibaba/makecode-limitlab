"""A83-B7: branched inhabited courtyards - strictly G0 architectural hypothesis, NOT construction."""
import json, math, hashlib
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
parts=[]; records=[]; doors=[]; floor_witnesses=[]
COL={
 'plaza':(42,73,79,255),'concourse':(85,121,117,255), 'floor':(161,177,161,255),
 'facade':(201,212,202,255),'inner':(120,167,173,255),'roof':(78,135,145,255),
 'structure':(178,130,87,255),'light':(226,189,116,255),'garden':(82,140,103,255),
 'glass':(98,164,179,255),'gallery':(194,175,131,255),'stair':(226,194,133,255),
 'core':(111,117,129,255), 'parapet':(78,129,129,255), 'terrace':(114,154,141,255)}
def add(name,verts,faces,kind,semantic=None):
    v=np.asarray(verts,dtype=float);f=np.asarray(faces,dtype=int)
    m=trimesh.Trimesh(vertices=v,faces=f,process=False)
    m.visual.face_colors=np.tile(np.array(COL[kind]),(len(f),1))
    parts.append(m)
    records.append({'name':name,'class':kind,'semantic':semantic or kind,'triangles':len(f),'vertices':len(v)})

def quad(name,a,b,c,d,kind,semantic=None):add(name,[a,b,c,d],[[0,1,2],[0,2,3]],kind,semantic)
def box(name,cx,cy,z0,w,d,h,kind):
    x,y=cx,cy
    z1=z0+h
    v=[(x-w/2,y-d/2,z0),(x+w/2,y-d/2,z0),(x+w/2,y+d/2,z0),(x-w/2,y+d/2,z0),
       (x-w/2,y-d/2,z1),(x+w/2,y-d/2,z1),(x+w/2,y+d/2,z1),(x-w/2,y+d/2,z1)]
    f=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]
    add(name,v,f,kind)
def pt(c,r,t,z):return (c[0]+r*math.cos(t),c[1]+r*math.sin(t),z)

def sector_poly(name,c,ri,ro,a,b,z,kind,n=12,with_hole=False):
    # Flat corridor ring sector: two concentric arcs, no interior fillers.
    angles=np.linspace(a,b,n+1)
    vs=[pt(c,ri,t,z) for t in angles]+[pt(c,ro,t,z) for t in angles]
    faces=[]
    for k in range(n):
        faces.extend([[k,k+1,n+1+k+1],[k,n+1+k+1,n+1+k]])
    add(name,vs,faces,kind)

def radial_face(name,c,a,ri,ro,z0,z1,kind):
    quad(name,pt(c,ri,a,z0),pt(c,ro,a,z0),pt(c,ro,a,z1),pt(c,ri,a,z1),kind)

def ring_wall(name,c,r,a,b,z0,z1,kind,segments=10):
    angles=np.linspace(a,b,segments+1)
    for k in range(segments):
        t0,t1=angles[k:k+2]
        quad(f'{name}_{k}',pt(c,r,t0,z0),pt(c,r,t1,z0),pt(c,r,t1,z1),pt(c,r,t0,z1),kind)

def fill_ground_path(name,p,q,width):
    a=np.array(p);b=np.array(q);unit=(b-a)/np.linalg.norm(b-a)
    n=np.array([-unit[1],unit[0]])*width/2
    pts=[a+n,b+n,b-n,a-n]
    quad(name,(*pts[0],0),(*pts[1],0),(*pts[2],0),(*pts[3],0),'concourse')

def create():
    centers={'W':(-148,-35),'C':(0,38),'E':(164,-22)}
    box('shared_public_ground',0,0,-.8,480,280,.8,'plaza')
    # At-grade broad public connectors: unverified as complete human routes.
    fill_ground_path('western_intercourt_public_ground',(-126,-18),(-27,26),22)
    fill_ground_path('eastern_intercourt_public_ground',(24,25),(142,-9),26)
    for dist,c in centers.items():
        number={'W':4,'C':5,'E':4}[dist]
        start={'W':-2.6,'C':-2.7,'E':-2.45}[dist]
        anglewidth={'W':.48,'C':.44,'E':.49}[dist]
        ri=29 if dist=='C' else 25
        ro=69 if dist=='C' else 63
        sector_poly(f'{dist}_lower_public_annulus',c,ri-6,ri,start-.19,start+(number-1)*anglewidth+.19,0,'concourse',32)
        # Real occupied sectors: each is an arc-bounded wedge, not a rectangular box or an external wall.
        for i in range(number):
            a=start+i*anglewidth; b=a+anglewidth
            mid=(a+b)/2
            code=f'{dist}{i}'
            h=13 if dist=='C' else 11.5
            sector_poly(f'{code}_inhabited_floor',c,ri,ro,a,b,0,'floor',10)
            # Roof shares the exact footprint, no huge planar facade around the city.
            sector_poly(f'{code}_inhabited_roof',c,ri,ro,a,b,h,'roof',10)
            # Outer face and radial party walls physically bound the sector.
            ring_wall(f'{code}_outer_enclosure',c,ro,a,b,0,h,'facade',10)
            radial_face(f'{code}_side_A',c,a,ri,ro,0,h,'inner')
            radial_face(f'{code}_side_B',c,b,ri,ro,0,h,'inner')
            # Actual facade aperture at inner arc: a 0.14rad opening up to z=4.8,
            # with solid left-right and upper lintel on same real mesh.
            da=.078
            ring_wall(f'{code}_portal_left',c,ri,a,mid-da,0,h,'inner',4)
            ring_wall(f'{code}_portal_right',c,ri,mid+da,b,0,h,'inner',4)
            ring_wall(f'{code}_portal_lintel',c,ri,mid-da,mid+da,4.8,h,'inner',3)
            doors.append({'id':code,'center':list(c),'radius':ri,'theta':mid,'width_angle':da,'height':4.8,
                          'height_top':h,'district':dist,'type':'real_missing_inner_facade_mesh_patch'})
            # A double-height occupied front edge presents activity to an open sky court.
            for j in range(3):
                ta=a+(j+.5)*anglewidth/3
                q=pt(c,ri+16,ta,.4)
                box(f'{code}_activity_island_{j}',q[0],q[1],.2,5,3,1.8,'light' if j==1 else 'garden')
            # Roof lips and selective exterior ribs are tied to occupied roof sectors.
            for j in (0,1,2):
                ta=a+(j+.5)*anglewidth/3
                x,y,_=pt(c,ri+23,ta,0)
                # 3 grounded supports, terminating exactly at the inhabited roof surface.
                box(f'{code}_rooted_support_{j}',x,y,0,1.8,1.8,h,'structure')
            # Lower roof clerestory: a smaller raised canopy is part of room roof, not floating artwork.
            t0=a+.07;t1=b-.07
            for j in range(6):
                t=t0+(t1-t0)*j/6;t2=t0+(t1-t0)*(j+1)/6
                z0=h+3*math.sin((t-a)/(b-a)*math.pi)
                z1=h+3*math.sin((t2-a)/(b-a)*math.pi)
                quad(f'{code}_monitor_{j}',pt(c,ro-13,t,h),pt(c,ro-13,t2,h),
                     pt(c,ro-22,t2,z1),pt(c,ro-22,t,z0),'glass')
        # Deliberately no generic full ring bridges. Upper wayfinding/stairs tested as a separate layer.
        # A short upper public crescent resides in the same footprint as the floors below.
        nupper=number-1
        upper_a=start+.08; upper_b=start+anglewidth*(nupper+.65)
        sector_poly(f'{dist}_upper_shared_gallery',c,ri-5,ri+2,upper_a,upper_b,13 if dist=='C' else 11.5,'gallery',32)
        # two tall inhabited spires grow out of rooms as occupiable extensions,
        # not unrooted tower frames: no claim of real vertical access to these volumes.
        for k in range(2):
            i=1 if k==0 else number-2
            t=start+(i+.5)*anglewidth; x,y,_=pt(c,ri+35,t,0)
            base=13 if dist=='C' else 11.5
            # Tapered folded atrium fins: anchored physically at roof with continuous triangulated sides.
            h=35+12*k+(9 if dist=='C' else 0)
            w=12 if k==0 else 10
            verts=[(x-w/2,y-8,base),(x+w/2,y-8,base),(x+w/2,y+8,base),(x-w/2,y+8,base),
                   (x-w/3+5,y-4,base+h),(x+w/3+6,y-5,base+h+3),(x+w/3+10,y+4,base+h+6),(x-w/3+5,y+6,base+h+1)]
            faces=[[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7],[4,5,6],[4,6,7]]
            add(f'{dist}_roof_built_lightwell_{k}',verts,faces,'glass','unoccupied_lightwell_not_real_room')
        # Two physically drafted public stairs out of common court, toward the first and last gallery portals.
        for k,t in enumerate((start+.25*anglewidth,start+(number-.25)*anglewidth)):
            h=13 if dist=='C' else 11.5
            n=52
            for j in range(n):
                # Radially outward approach: first tread near r=ri-18, last near r=ri-3.
                r0=ri-19+j*(16/n);r1=ri-19+(j+1)*(16/n)
                z=h*(j+1)/n
                ta=t-.032;tb=t+.032
                quad(f'{dist}_stair_{k}_{j}',pt(c,r0,ta,z),pt(c,r1,ta,z),pt(c,r1,tb,z),pt(c,r0,tb,z),'stair')
            # No claim that this is a real code-compliant stair; tread depth is inadequate.
    mesh=trimesh.util.concatenate(parts)
    mesh.export(OUT/'b7_civic_oculi_source.obj')
    mesh.export(OUT/'b7_civic_oculi_source.ply')
    meta={'stage':'A83_B7_TRUE_GEOMETRY_ANTI_SCULPTURE_TEST','hypothesis':'THREE_INTERLOCKED_PUBLIC_OCULI',
          'parts':len(parts),'vertices':len(mesh.vertices),'triangles':len(mesh.faces),
          'domains':list(centers),'room_candidates':len(doors),'portals':doors,
          'completed_rooms':'NOT_TESTED','real_continuous_routes':'NOT_TESTED',
          'stair_tread_safety':'NOT_TESTED','structural_load':'NOT_TESTED',
          'formal_s1_g1_g2_g3':'NOT_RUN','art':'HOLD_REQUIRES_IMAGE_REVIEW',
          'minecraft_construction':'FORBIDDEN',
          'sha256_obj':hashlib.sha256((OUT/'b7_civic_oculi_source.obj').read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
    print(json.dumps({k:meta[k] for k in ['parts','vertices','triangles','room_candidates','sha256_obj']},indent=2))
if __name__=='__main__':create()
