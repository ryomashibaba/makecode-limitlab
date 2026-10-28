"""G4-C7 B11-R5 D13 art-first THREE candidate 3D massing negatives.
Non-adoptable early forms. Explicit program anchors, not a certified building.
Creates consistent GLB/OBJ/categorical PLY for independent image review.
Not Minecraft code. No safety certification or model art approval.
"""
from pathlib import Path
import hashlib, json
import numpy as np
import trimesh
from skimage.measure import marching_cubes
ROOT=Path(__file__).resolve().parent
COLORS={'earth':(75,93,99,255),'inhabited':(158,184,191,255),'fabrication':(214,139,100,255),
        'cultural':(229,188,120,255),'research':(100,176,202,255),'habitat':(189,211,172,255),
        'public_route':(233,193,115,255),'light':(123,211,218,255),'core':(92,166,174,255)}
X=np.arange(-490,491,7,dtype='f4');Y=np.arange(-400,401,7,dtype='f4');Z=np.arange(0,310,7,dtype='f4')
x=X[:,None,None]; y=Y[None,:,None];z=Z[None,None,:]

def carve(shape):
    # Author's shared physically anchored public culture: fabrication Z20, research Z122, culture Z56,
    # housing Z205. Shifted escarpment shoulders, NOT a tube/ring/rows of towers.
    s_edge=-78+23*np.sin((x+80)/175)+12*np.sin(x/51)
    n_edge=95+38*np.sin((x-90)/210)+14*np.cos(x/76)
    south_top=187+53*np.sin((x+145)/158)+27*np.cos(x/69)
    north_top=240+39*np.cos((x-120)/177)+17*np.sin(x/56)
    south=(y < s_edge + .13*z) & (y > -365+18*np.cos(x/127)) & (z>10)&(z<south_top)
    north=(y > n_edge - .09*z) & (y < 345+25*np.sin(x/161)) & (z>10)&(z<north_top)
    # Three urban access plazas set back from the canyon face; creates genuine outdoor voids.
    void1=((x+250)/122)**2+((y+123)/119)**2+((z-62)/80)**2<1
    void2=((x+20)/155)**2+((y-103)/125)**2+((z-114)/92)**2<1
    void3=((x-240)/141)**2+((y-74)/131)**2+((z-181)/81)**2<1
    mass=(south|north)&(~void1)&(~void2)&(~void3)
    if shape=='canyon':
        pass
    elif shape=='braided':
        # Break the two cliffs into differentiated deep rifts; avoid regular fenestration.
        rift1=(np.abs(x+135+0.52*z)<22+0.025*z)&(y < -75)&(z>32)
        rift2=(np.abs(x-187-0.28*z)<24+0.021*z)&(y > 78)&(z>38)
        rift3=(np.abs(x+316-0.20*z)<18)&(y > 82)&(z>78)
        mass &= ~(rift1|rift2|rift3)
    elif shape=='courts':
        # Deep *open to sky* public cultivation terraces; function shapes upper edge.
        for cx,cy,z0,rx,ry in [(-275,-155,116,125,145),(26,184,145,149,139),(276,173,181,135,141)]:
            court=((x-cx)/rx)**2+((y-cy)/ry)**2 < 1
            mass &= ~(court & (z>z0))
    else:raise ValueError(shape)
    return mass

def add_box(parts,tag,center,extent):
    m=trimesh.creation.box(extents=extent);m.apply_translation(center);parts.setdefault(tag,[]).append(m)

def slab_footprint(parts,tag,xy,zlo,zhi):
    xy=np.asarray(xy,float);n=len(xy)
    verts=np.vstack([np.c_[xy,np.full(n,zlo)],np.c_[xy,np.full(n,zhi)]])
    fs=[]
    for i in range(1,n-1):fs.extend([(0,i+1,i),(n,n+i,n+i+1)])
    for j in range(n):k=(j+1)%n;fs.extend([(j,k,n+k),(j,n+k,n+j)])
    parts.setdefault(tag,[]).append(trimesh.Trimesh(vertices=verts,faces=fs,process=False))

def make(name):
    folder=ROOT/name;folder.mkdir(exist_ok=True)
    vox=carve(name).astype('u1')
    vertices,faces,_,_=marching_cubes(vox,0.5,spacing=(7,7,7))
    vertices+=np.array([X[0],Y[0],Z[0]])
    main=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
    parts={'inhabited':[main]}
    # One actual program scene, deliberately not pretending construction viability.
    add_box(parts,'fabrication',(-188,-92,22),(130,88,4))
    add_box(parts,'fabrication',(-182,-80,27),(60,37,8))
    # Theater cut near canyon, physically inhabitable surface; not just role labels.
    slab_footprint(parts,'cultural',[(0,16),(72,23),(142,3),(182,50),(121,89),(42,80)],54,57)
    # Research and dwelling balconies are not separate towers; recessed into shoulders.
    slab_footprint(parts,'research',[(-76,88),(25,90),(72,120),(-12,165),(-78,144)],120,124)
    slab_footprint(parts,'research',[(135,115),(250,130),(266,181),(145,174)],147,151)
    slab_footprint(parts,'habitat',[(-338,-116),(-180,-120),(-144,-199),(-297,-232)],201,206)
    slab_footprint(parts,'habitat',[(198,195),(292,194),(326,265),(177,263)],218,222)
    # One prominent public cut through the canyon remains genuinely uncovered.
    slab_footprint(parts,'public_route',[(-290,-30),(-186,-17),(-45,15),(128,19),(243,24),(304,18),(320,32),(231,38),(111,33),(-48,30),(-208,-2),(-296,-13)],20,22)
    # E1/E2 are only modelled envelopes, not functional lifts; no claims of access.
    for x0,y0 in [(-350,-91),(309,102)]:
        for dx in [-11,11]:
            for dy in [-11,11]:
                add_box(parts,'core',(x0+dx,y0+dy,118),(3,3,215))
    scene=trimesh.Scene();out=[];metadata={}
    for tag,arr in parts.items():
        m=trimesh.util.concatenate(arr)
        m.visual.vertex_colors=np.tile(COLORS[tag],(len(m.vertices),1))
        m.export(folder/f'{tag}.ply');scene.add_geometry(m,geom_name=tag);out.append(m)
        metadata[tag]={'faces':len(m.faces),'sha256':hashlib.sha256((folder/f'{tag}.ply').read_bytes()).hexdigest()}
    unified=trimesh.util.concatenate(out);unified.export(folder/'study.obj');scene.export(folder/'study.glb')
    report={'stage':'B11-R5 D13','variant':name,'scope':'art-first 3D massing only, not full city or safe interior',
        'faces':len(unified.faces),'bounds_m':np.round(unified.bounds,2).tolist(),'roles':metadata,
        'sha256_obj':hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest(),
        'sha256_glb':hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest(),
        'actual_lifts':False,'safe_habitat':False,'full_331_993':'NOT_RUN',
        'formal_S1_G1_G2_G3':'NOT_RUN','G0_ART':'NOT_RUN','art_adopted':0,'Minecraft':'FORBIDDEN'}
    (folder/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(name,len(unified.faces),flush=True)
    return report

if __name__=='__main__':
    for n in ('canyon','braided','courts'):make(n)