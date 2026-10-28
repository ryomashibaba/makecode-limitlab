"""B11-R3: independent triangle-ray audit of existing B11-R2 rejected PLY.
Only eight intended-use sample points, not a full room or human safety test.
"""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image,ImageDraw

PARTS=('public','occupied','envelope','supports','activity')
NODES=(-132.,-36.,64.,143.)
RAYS={'east':([1,0,0],16.),'west':([-1,0,0],16.),
      'north':([0,1,0],37.),'south':([0,-1,0],37.),
      'up':([0,0,1],25.),'down':([0,0,-1],12.)}

def original_sites():
    out=[]
    for x in NODES:
        activity=(np.exp(-((x+116)/48)**2)+1.2*np.exp(-((x-35)/71)**2)
                  +.75*np.exp(-((x-136)/39)**2))
        centre=14*np.sin(x/95)+4*np.sin(x/31)
        void=11+6+5.5*activity-1.8
        depth=10+8+2*activity+.8
        for side in (-1,1):
            out.append({'site':f'{int(x)}_{"north" if side>0 else "south"}',
              'point':[float(x),float(centre+side*(void+.5*depth)),8.]})
    return out

def import_authentic_triangles(folder):
    folder=Path(folder)
    manifest=json.loads((folder/'manifest.json').read_text())
    tris=[];identity={}
    for name in PARTS:
        f=folder/(name+'.ply')
        digest=hashlib.sha256(f.read_bytes()).hexdigest()
        if digest!=manifest['parts'][name]['file_sha256']:
            raise ValueError('ORIGINAL_PLY_SHA_MISMATCH:'+name)
        mesh=trimesh.load(f,force='mesh',process=False)
        if len(mesh.faces)!=manifest['parts'][name]['faces']:
            raise ValueError('ORIGINAL_PLY_FACE_COUNT_MISMATCH:'+name)
        tris.append(np.asarray(mesh.triangles,dtype=float))
        identity[name]={'sha256':digest,'faces':int(len(mesh.faces))}
    return np.concatenate(tris),identity

def wall_hit(tris,point,direction,limit):
    p=np.asarray(point,dtype=float);d=np.asarray(direction,dtype=float)
    v0,v1,v2=tris[:,0,:],tris[:,1,:],tris[:,2,:]
    e1=v1-v0;e2=v2-v0
    normal=np.cross(e1,e2);length=np.linalg.norm(normal,axis=1)
    facing=np.abs(normal@d)>.72*length
    h=np.cross(np.broadcast_to(d,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,h)
    with np.errstate(divide='ignore',invalid='ignore'):
        inv=np.where(np.abs(det)>1e-10,1/det,0)
        s=p-v0;u=inv*np.einsum('ij,ij->i',s,h)
        q=np.cross(s,e1);v=inv*(q@d)
        t=inv*np.einsum('ij,ij->i',e2,q)
    ok=facing&(np.abs(det)>1e-10)&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(t>1e-4)&(t<=limit)
    return float(np.min(t[ok])) if np.any(ok) else None

def check(tris,sites):
    result=[]
    for s in sites:
        rays={}
        for name,(vec,limit) in RAYS.items():
            dist=wall_hit(tris,s['point'],vec,limit)
            rays[name]={'hit':dist is not None,'distance_m':round(dist,3) if dist is not None else None}
        result.append({'site':s['site'],'point_m':s['point'],'rays':rays,
                       'six_direction_local_witness':all(r['hit'] for r in rays.values())})
    return result

def audit(folder):
    triangles,identities=import_authentic_triangles(folder)
    probes=check(triangles,original_sites())
    return {'study':'B11_R3_REAL_TRIANGLE_ROOM_CLOSURE_DIAGNOSTIC',
      'original':'B11-R2 baseline PLY unchanged','faces':len(triangles),
      'original_sha256':identities,'probes':probes,'probed_sites':len(probes),
      'six_direction_local_witnesses':sum(p['six_direction_local_witness'] for p in probes),
      'interpretation':'Six directional walls are necessary, never sufficient, for a usable room; conclusions only concern these eight samples',
      'real_room_certification':'NOT_CERTIFIED','art':'G0_ART_REJECT',
      's1_g1_g2_g3':'NOT_RUN','human_331_foot_993':'NOT_RUN',
      'load_and_egress':'NOT_TESTED','formal_art_adoptions':0,'minecraft':'FORBIDDEN'}

def chart(result,path):
    im=Image.new('RGB',(1060,900),(15,25,39));d=ImageDraw.Draw(im)
    d.text((22,22),'B11-R3 / REAL B11-R2 PLY / SIX DIRECTIONAL ROOM WITNESSES',fill='white')
    d.text((22,55),'Not a room or human safety certificate; missing end walls remain missing.',fill='#c5ccd8')
    for i,n in enumerate(RAYS):d.text((250+i*130,125),n,fill='white')
    for j,p in enumerate(result['probes']):
        y=165+j*87;d.text((22,y+20),p['site'],fill='white')
        for i,name in enumerate(RAYS):
            hit=p['rays'][name]['hit'];x=250+i*130
            d.rectangle((x,y,x+101,y+56),fill='#437f6b' if hit else '#a65054')
            d.text((x+10,y+20),'HIT' if hit else 'MISSING',fill='white')
    im.save(path)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--baseline',required=True)
    parser.add_argument('--out',required=True);a=parser.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    result=audit(a.baseline)
    (out/'room_witness_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    chart(result,out/'directional_room_witness.png')
    print('B11_R3_REAL_MESH_SIX_DIRECTIONAL_ROOM_WITNESSES',result['six_direction_local_witnesses'],'/',result['probed_sites'])
