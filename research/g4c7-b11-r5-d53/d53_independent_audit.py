"""Independent D53 saved-GLB audit. Does not import D53 generator.
All results are candidate-specific local geometry only; no G0, S1, G1-G3 or 331/993 claims.
"""
import json, hashlib
from pathlib import Path
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent

def intersections(p, vec, triangles, ray_max=1.0):
    # Vectorised Moller-Trumbore ray/triangle hits, independently implemented.
    t=np.asarray(triangles,dtype=float)
    if len(t)==0:return np.array([])
    e1=t[:,1]-t[:,0];e2=t[:,2]-t[:,0];a=np.broadcast_to(vec,e2.shape)
    h=np.cross(a,e2); det=np.einsum('ij,ij->i',e1,h)
    good=np.abs(det)>1e-9
    inv=np.zeros_like(det);inv[good]=1/det[good]
    s=np.broadcast_to(p,t[:,0].shape)-t[:,0]
    u=inv*np.einsum('ij,ij->i',s,h)
    q=np.cross(s,e1);v=inv*np.einsum('ij,ij->i',a,q)
    d=inv*np.einsum('ij,ij->i',e2,q)
    return np.sort(d[good&(u>=-1e-8)&(v>=-1e-8)&(u+v<=1+1e-8)&(d>1e-6)&(d<ray_max-1e-6)])

def contains_point(p,tri):
    # Cast a non-axis-aligned ray to reduce coincident-face ambiguity.
    ray=np.array([1.0,.135,.239]);dist=intersections(np.asarray(p,float),ray,tri,1000)
    unique=[]
    for d in dist:
        if not unique or abs(d-unique[-1])>1e-5:unique.append(float(d))
    return len(unique)%2==1

def audit(kind):
    path=ROOT/kind/f'd53_{kind}.glb'
    sc=trimesh.load(path,force='scene',process=False)
    meshes={n:sc.geometry[sc.graph.get(n)[1]] for n in sc.graph.nodes_geometry}
    solid={n:m for n,m in meshes.items() if 'fold' in n or 'fault' in n or 'splice' in n or 'interlock' in n}
    tri={n:np.asarray(m.triangles) for n,m in solid.items()}
    core=np.concatenate(list(tri.values()),axis=0)
    treads=sorted([(n,m.centroid) for n,m in meshes.items() if n.startswith('rising_path_')])
    # Footstep centre +1.62m is a representative head probe, not body volume sweep.
    hitheads=[]
    for n,mid in treads:
        head=mid+[0,0,1.62]
        for sn,t in tri.items():
            if contains_point(head,t):hitheads.append({'stair':n,'solid':sn});break
    floor=meshes['living_floor'].bounds
    end=meshes['rising_path_b_23'].centroid
    xy_gap=np.linalg.norm(np.maximum(floor[0,:2]-end[:2],np.maximum(end[:2]-floor[1,:2],0)))
    vertical_delta=float(floor[1,2]-end[2])
    # Hard-coded designated sightlines are independent of the generator file.
    observers={
    'arrival_to_maker':([0,-30,2.0],[-7,-9,2]),
    'maker_to_research':([-7,-9,3],[7,0,3]),
    'research_to_maker':([7,0,3],[-7,-9,3]),
    'living_to_maker':(([-2,18,19] if kind=='A' else [2,18,18]),[-7,-9,3]),
    }
    lines={}
    for label,(start,endp) in observers.items():
        start=np.asarray(start,float);d=np.asarray(endp,float)-start
        hits=intersections(start,d,core)
        lines[label]={'solid_intersections':len(hits),'clear_direct_segment':len(hits)==0}
    diagnostics={
        'subject':f'D53 {kind}', 'only_saved_glb':True,
        'glb_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'nodes':len(meshes), 'triangles':int(sum(len(m.faces) for m in meshes.values())),
        'primary_mass_watertight':{n:bool(m.is_watertight) for n,m in solid.items()},
        'tread_count':len(treads),
        'sample_head_inside_primary_mass_count':len(hitheads),
        'sample_head_examples':hitheads[:12],
        'final_tread_to_living_floor_min_XY_gap':round(float(xy_gap),3),
        'living_floor_top_minus_last_tread_centroid_z':round(vertical_delta,3),
        'life_floor_connection_not_proven':True,
        'sightlines_on_primary_solids_only':lines,
        'official_331_993':'NOT RUN',
        'formal_G0_S1_G1_G2_G3':'NOT RUN',
        'art':'NOT AUTOMATICALLY JUDGED; human visual review required',
    }
    (ROOT/kind/'independent_audit.json').write_text(json.dumps(diagnostics,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(diagnostics,ensure_ascii=False,indent=2))

if __name__=='__main__':
    for kind in ['A','B']:audit(kind)
