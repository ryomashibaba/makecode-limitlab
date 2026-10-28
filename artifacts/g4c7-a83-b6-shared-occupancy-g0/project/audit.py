"""Independent triangle-level G0 audit. No claims about whole-body clearance or structural capacity."""
from pathlib import Path
import json, math, hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'output'

def facade_y(x):return 8.7*math.sin(math.pi*x/72) + 3.6*math.sin(2.6*math.pi*x/72+0.2)

# Moller-Trumbore ray triangle intersection, independent from shape labels, no rtree.
def hits(mesh, o, d, maxdist=30):
    T=mesh.vertices[mesh.faces]
    a,b,c=T[:,0,:],T[:,1,:],T[:,2,:]
    e1=b-a;e2=c-a
    P=np.cross(np.broadcast_to(d,e2.shape),e2)
    det=np.einsum('ij,ij->i',e1,P)
    valid=np.abs(det)>1e-9
    inv=np.divide(1,det,out=np.zeros_like(det),where=valid)
    tv=np.broadcast_to(o,a.shape)-a
    u=np.einsum('ij,ij->i',tv,P)*inv
    valid &= (u>=-1e-7)&(u<=1+1e-7)
    q=np.cross(tv,e1)
    v=np.einsum('j,ij->i',d,q)*inv
    valid &= (v>=-1e-7)&(u+v<=1+1e-7)
    distances=np.einsum('ij,ij->i',e2,q)*inv
    return np.sort(distances[valid & (distances>1e-7)&(distances<=maxdist)])

def mesh_from_obj(p=None):
    return trimesh.load(p or OUT/'b6_shared_occupied_boundary.obj',force='mesh',process=False)

def doorway(mesh,cx,z):
    cy=facade_y(cx)
    y0=cy-5.0; d=np.array([0.,1.,0.]);
    def blocked(x,height):return len(hits(mesh,np.array([x,facade_y(x)-5,height]),d,10))>0
    return {
      'clear_center':not blocked(cx,z+2.2),
      'left_wall':blocked(cx-2.9,z+2.2),
      'right_wall':blocked(cx+2.9,z+2.2),
      'solid_lintel':blocked(cx,z+6.3)
    }

def height_at(mesh,x,y,start=19):
    h=hits(mesh,np.array([x,y,start]),np.array([0.,0.,-1.]),start+2)
    return round(start-float(h[0]),6) if len(h) else None

def canonical_triangles_sha(mesh):
    # Order- and triangle-winding-independent hash of quantized geometric faces.
    tris=np.round(mesh.vertices[mesh.faces],4)
    quant=np.rint(tris*10000).astype(np.int64)
    items=sorted(tuple(sorted(tuple(int(v) for v in xyz) for xyz in face)) for face in quant)
    return hashlib.sha256(json.dumps(items,separators=(',',':')).encode()).hexdigest()

def report(mesh=None):
    obj=OUT/'b6_shared_occupied_boundary.obj'; m=mesh if mesh is not None else mesh_from_obj()
    door_results={f'{cx}:L{level}':doorway(m,cx,level) for cx in [-48,-16,16,48] for level in [0,8]}
    floors={f'{cx}:upper':height_at(m,cx,facade_y(cx)+10,9.5) for cx in [-48,-16,16,48]}
    stair={f'{cx}:penultimate':height_at(m,cx,facade_y(cx)-.70,8.4) for cx in [-48,48]}
    stair.update({f'{cx}:final':height_at(m,cx,facade_y(cx)-.20,8.4) for cx in [-48,48]})
    stair.update({f'{cx}:landing':height_at(m,cx,facade_y(cx)+1.0,8.4) for cx in [-48,48]})
    # False if exposed floor is not truly at z=8.0; plan sources alone cannot fake this check.
    return {'source':'independent_OBJ_triangle_intersections',
            'obj_sha256':hashlib.sha256(obj.read_bytes()).hexdigest() if mesh is None else 'MUTATED_NEGATIVE_CONTROL',
            'canonical_face_digest':canonical_triangles_sha(m),
            'geometry':{'vertices':len(m.vertices),'triangles':len(m.faces),'bbox':np.round(m.bounds,4).tolist()},
            'door_rays':door_results,'shared_upper_floor_rays':floors,'stair_terminal_rays':stair,
            'limited_triangle_gate':all(all(v.values()) for v in door_results.values())
               and all(z==8.0 for z in floors.values()) and all(abs(z-7.833333)<1e-5 for k,z in stair.items() if k.endswith('penultimate'))
               and all(z==8.0 for k,z in stair.items() if not k.endswith('penultimate')),
            'occupied_rooms_certified':'NOT_TESTED','human_331_foot_993':'NOT_RUN',
            'human_half_width':0.65,'formal_s1_g1_g2_g3':'NOT_RUN',
            'structural_load':'NOT_TESTED','continuous_walk':'NOT_TESTED',
            'architectural_art':'HOLD_AWAITING_HUMAN_REVIEW','minecraft_construction':'FORBIDDEN'}

def blocked_door_negative(m,cx=-16,z=0):
    # Inject a distinct true triangle exactly in formerly open doorway.
    y=facade_y(cx)
    o=np.array([[cx-1.7,y, z+.25],[cx+1.7,y,z+.25],[cx,y,z+4.]])
    verts=np.vstack([m.vertices,o]);faces=np.vstack([m.faces,[[len(verts)-3,len(verts)-2,len(verts)-1]]])
    return trimesh.Trimesh(vertices=verts,faces=faces,process=False)

def deleted_shared_floor_negative(m,cx=-16):
    # Strip all z=8 triangles supporting this frontage, leaving other mesh intact.
    tri=m.vertices[m.faces]
    cent=np.mean(tri,axis=1)
    flat=np.all(abs(tri[:,:,2]-8)<1e-5,axis=1)
    region=(cent[:,0]>cx-6)&(cent[:,0]<cx+6)&(cent[:,1]>facade_y(cx)+7)&(cent[:,1]<facade_y(cx)+22)
    newfaces=m.faces[~(flat&region)]
    return trimesh.Trimesh(vertices=m.vertices,faces=newfaces,process=False)

if __name__=='__main__':
    r=report();(OUT/'independent_audit.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'limited_triangle_gate':r['limited_triangle_gate'],'doors':r['door_rays'],'floors':r['shared_upper_floor_rays'],'stair':r['stair_terminal_rays']},indent=2))
