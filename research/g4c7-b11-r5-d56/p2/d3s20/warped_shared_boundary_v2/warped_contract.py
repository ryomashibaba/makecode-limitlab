"""G4C7 experimental nonorthogonal shared-surface author contract V2.
Not an aesthetic city proposal, not construction instructions, NOT formal safety QA.
The v1 SpatialLedger remains immutable in its original research directory.
"""
from __future__ import annotations
import sys, json, math, copy
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
# Resolve the append-only v1 contract from a local evidence package or the
# sibling GitHub research directory; the /mnt/data path is only a fallback.
CANDIDATES=[ROOT,ROOT.parent/'shared_boundary_contract_v1',Path('/mnt/data/D3S20_SHARED_BOUNDARY_CONTRACT')]
V1=next((d for d in CANDIDATES if (d/'spatial_contract.py').is_file()),None)
if V1 is None:raise ImportError('v1 shared-boundary contract source is required')
if str(V1) not in sys.path:sys.path.insert(0,str(V1))
from spatial_contract import make_fixture,norm_edge,shift_market_frontage,SpatialLedger

ROOT=Path(__file__).resolve().parent
LEVEL=3.2
WALL=0.16
FLOOR=.20
PORTAL_WIDTH=2.45
PORTAL_HEIGHT=2.45
COLOR={'PUBLIC':(174,191,179,255),'FORGE':(215,128,95,255),'RESEARCH':(108,176,217,255),'MARKET':(230,188,111,255),'CULTURE':(179,152,222,255),'HABITAT':(145,193,163,255),'UPPER':(213,221,238,255),'STAIR':(248,210,141,255)}

@dataclass(frozen=True)
class Warp:
    x_shear:float=.45
    y_shear:float=.30
    quadratic:float=.035
    cross:float=.04
    def xy(self,u,v):
        # Global nonaffine yet continuous map; shared edges reuse *identical* points.
        return np.array([4*u+self.x_shear*v+self.cross*u*v,
                         4*v+self.y_shear*u+self.quadratic*u*u],dtype=float)
    def cell(self,i,j):
        return np.array([self.xy(i,j),self.xy(i+1,j),self.xy(i+1,j+1),self.xy(i,j+1)])
    def area(self,i,j):
        p=self.cell(i,j);return float(.5*abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1))))

def make_ledger():
    s=make_fixture()
    for y in (1,2):
        s.spaces[(5,y,0)]='STAIR'
        s.spaces[(5,y,1)]='STAIR'
    s.portals[norm_edge((5,0,0),(5,1,0))]='interface'
    s.portals[norm_edge((5,2,1),(5,3,1))]='interface'
    return s

@dataclass(frozen=True)
class StairSpec:
    x:int=5
    start_y:int=1
    end_y:int=3
    steps:int=8
    height:float=LEVEL
    min_clear:float=2.1
    min_width:float=2.3
    def sample(self,k,warp):
        v=self.start_y+(k+.5)*(self.end_y-self.start_y)/self.steps
        p=.5*(warp.xy(self.x,v)+warp.xy(self.x+1,v))
        return np.array([p[0],p[1],(k+1)*self.height/self.steps])

def validate_model(ledger,warp=Warp(),stair=StairSpec()):
    errors=[];g=ledger.validate()
    if not g['ok']:errors+=['V1_'+e for e in g['errors']]
    if stair.steps<1 or stair.steps>48:errors.append('STEP_COUNT_INVALID')
    if stair.height<=0:errors.append('NONPOSITIVE_VERTICAL_RISE')
    if norm_edge((5,0,0),(5,1,0)) not in ledger.portals:errors.append('STAIR_LOWER_PORTAL_MISSING')
    if norm_edge((5,2,1),(5,3,1)) not in ledger.portals:errors.append('STAIR_UPPER_PORTAL_MISSING')
    for y in (1,2):
        for z in (0,1):
            if ledger.spaces.get((5,y,z))!='STAIR':errors.append('STAIR_SHAFT_AIR_MISSING')
    if ledger.spaces.get((5,3,1))!='UPPER':errors.append('UPPER_LANDING_MISSING')
    if stair.height/stair.steps > .5:errors.append('EXCESS_RISER_DESIGN')
    widths=[];step_runs=[]
    for k in range(stair.steps):
        va=stair.start_y+k*(stair.end_y-stair.start_y)/stair.steps
        vb=stair.start_y+(k+1)*(stair.end_y-stair.start_y)/stair.steps
        p=warp.xy(stair.x,va);q=warp.xy(stair.x+1,va)
        widths.append(float(np.linalg.norm(p-q)))
        r=.5*(warp.xy(stair.x,va)+warp.xy(stair.x+1,va))
        s=.5*(warp.xy(stair.x,vb)+warp.xy(stair.x+1,vb))
        step_runs.append(float(np.linalg.norm(s-r)))
    if min(widths)<stair.min_width:errors.append('STAIR_TOO_NARROW')
    if min(step_runs)<.78:errors.append('STAIR_TREAD_TOO_SHORT')
    if LEVEL<stair.height/stair.steps+stair.min_clear:errors.append('STAIR_INSUFFICIENT_NOMINAL_CLEARANCE')
    # The top stair matches upper landing, not a detached bridge segment.
    if abs(stair.height-LEVEL)>1e-8:errors.append('STAIR_UPPER_LANDING_Z_MISMATCH')
    return {'ok':not errors,'errors':sorted(set(errors)),'v1_horizontal_ok':g['ok'],
            'lower_upper_shared_air':all(ledger.spaces.get((5,y,z))=='STAIR' for y in (1,2) for z in (0,1)),
            'stair_width_min':min(widths),'tread_run_min':min(step_runs),
            'riser':stair.height/stair.steps,'upper_landing_level':LEVEL,
            'meaning':'nominal author topology only; never ART or formal swept-body QA'}

def closed_prism(poly,z0,z1,rgba):
    p=np.asarray(poly,float)
    # Clockwise/CCW normalized to positive XY winding.
    signed=np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1))
    if signed<0:p=p[::-1]
    n=len(p)
    verts=np.vstack([np.c_[p,np.full(n,z0)],np.c_[p,np.full(n,z1)]])
    fs=[]
    for k in range(1,n-1):fs.append([0,k+1,k]);fs.append([n,n+k,n+k+1])
    for k in range(n):
        j=(k+1)%n;fs.extend([[k,j,n+j],[k,n+j,n+k]])
    mesh=trimesh.Trimesh(vertices=verts,faces=fs,process=False)
    mesh.fix_normals();mesh.visual.face_colors=rgba
    return mesh

def strip(a,b,thick):
    v=np.array(b)-np.array(a);v/=np.linalg.norm(v)
    normal=np.array([-v[1],v[0]])*thick/2
    return np.array([np.array(a)+normal,np.array(b)+normal,np.array(b)-normal,np.array(a)-normal])

def face_segment(a,b,axis,warp):
    x=max(a[0],b[0]);y=max(a[1],b[1])
    if axis==0:return warp.xy(x,y),warp.xy(x,y+1)
    if axis==1:return warp.xy(x,y),warp.xy(x+1,y)
    raise ValueError(axis)

def add_wall(scene,pa,pb,z0,z1,owner,door,name):
    col=COLOR.get(owner,(158,164,166,255));v=np.array(pb)-np.array(pa);length=float(np.linalg.norm(v))
    if not door:
        scene.add_geometry(closed_prism(strip(pa,pb,WALL),z0,z1,col),geom_name='WALL_'+name)
        return
    if PORTAL_WIDTH>=length:raise ValueError('portal wider than shared non-orthogonal edge')
    t=(length-PORTAL_WIDTH)/2/length
    left=np.array(pa)+t*v;right=np.array(pb)-t*v
    for n,u,w,low,high in [('LEFT',pa,left,z0,z1),('RIGHT',right,pb,z0,z1),
                             ('LINTEL',left,right,z0+PORTAL_HEIGHT,z1)]:
        if high>low:
            scene.add_geometry(closed_prism(strip(u,w,WALL),low,high,col),geom_name='PORTAL_'+n+'_'+name)

def make_scene(ledger=None,warp=Warp(),stair=StairSpec(),missing_step=None,block_stair=False):
    ledger=ledger or make_ledger();v=validate_model(ledger,warp,stair)
    if not v['ok']:raise ValueError(v['errors'])
    scene=trimesh.Scene()
    # Faces are owned once; no disconnected, independently rendered road or doorway.
    for key,f in sorted(ledger.face_inventory().items(),key=lambda t:str(t[0])):
        a,b=key;axis=f['axis'];kind=f['kind'];z=min(a[2],b[2])*LEVEL
        name=f'{a}_{b}'.replace(' ','')
        owner=f['owner'];col=COLOR.get(owner,(160,160,160,255))
        if axis==2:
            # An interlevel slab is intentionally omitted for the double-height STAIR shaft.
            x,y=max(a[0],b[0]),max(a[1],b[1]);q=warp.cell(x,y)
            height=max(a[2],b[2])*LEVEL
            scene.add_geometry(closed_prism(q,height-FLOOR,height,col),geom_name='FLOOR_ROOF_'+name)
        else:
            pa,pb=face_segment(a,b,axis,warp)
            if not f['door'] and f['kind']=='envelope_wall' and owner=='STAIR' and a[2]==1:
                col=(124,181,195,255)
            add_wall(scene,pa,pb,z,z+LEVEL,owner,bool(f['door']),name)
    # Derived approach apron from original external interface, not an independently drawn road.
    entrance=ledger.entrance;outside=next(c for c in entrance if c not in ledger.spaces)
    scene.add_geometry(closed_prism(warp.cell(outside[0],outside[1]),-FLOOR,0,COLOR['PUBLIC']),geom_name='DERIVED_EXTERNAL_APRON_UNVERIFIED_SUPPORT')
    # Closed, physically stair-shaped supported step prisms. No floating nominal route lines.
    for k in range(stair.steps):
        if k==missing_step:continue
        va=stair.start_y+k*(stair.end_y-stair.start_y)/stair.steps
        vb=stair.start_y+(k+1)*(stair.end_y-stair.start_y)/stair.steps
        q=[warp.xy(stair.x,va),warp.xy(stair.x+1,va),warp.xy(stair.x+1,vb),warp.xy(stair.x,vb)]
        rise=(k+1)*stair.height/stair.steps
        scene.add_geometry(closed_prism(q,0,rise,(224,166,104,255)),geom_name=f'STAIR_TREAD_{k:02d}')
    if block_stair:
        k=3;v=stair.start_y+(k+.5)*(stair.end_y-stair.start_y)/stair.steps
        center=.5*(warp.xy(stair.x,v)+warp.xy(stair.x+1,v))
        # true closed body obstructing head space above selected tread, not only an audit annotation
        poly=[center+[-.65,-.55],center+[.65,-.55],center+[.65,.55],center+[-.65,.55]]
        scene.add_geometry(closed_prism(poly,2.15,3.6,(235,58,51,255)),geom_name='NEGATIVE_BLOCKED_HEADSPACE')
    return scene

if __name__=='__main__':
    a=make_ledger();print(json.dumps(validate_model(a),indent=2))
    f=ROOT/'V2_WARPED_STAIRS_BASE.glb';f.write_bytes(make_scene(a).export(file_type='glb'))
    print('saved',f)
