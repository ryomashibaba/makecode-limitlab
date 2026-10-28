"""Independent triangle-only B9 probes; these never establish safe full-body motion."""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
ROOT=Path(__file__).parent
OUT=ROOT/'output'

def read_obj(p=None):
    return trimesh.load(p or OUT/'b9_shared_civic_seam.obj',process=False,force='mesh')

def intersections(mesh,a,b):
    """Returns interior segment hit fractions by Moller-Trumbore, not AABB proxies."""
    a=np.asarray(a,dtype=np.float64);b=np.asarray(b,dtype=np.float64)
    direction=b-a; triangles=mesh.vertices[mesh.faces]
    u=triangles[:,1]-triangles[:,0];v=triangles[:,2]-triangles[:,0]
    p=np.cross(np.broadcast_to(direction,v.shape),v)
    det=np.einsum('ij,ij->i',u,p)
    good=np.abs(det)>1e-10
    inv=np.zeros_like(det);inv[good]=1/det[good]
    tv=a-triangles[:,0]
    bc1=np.einsum('ij,ij->i',tv,p)*inv
    q=np.cross(tv,u)
    bc2=np.einsum('ij,j->i',q,direction)*inv
    t=np.einsum('ij,ij->i',v,q)*inv
    good&=(bc1>=-1e-8)&(bc2>=-1e-8)&(bc1+bc2<=1+1e-8)&(t>1e-7)&(t<1-1e-7)
    return np.sort(t[good])

def is_clear(mesh,a,b):return len(intersections(mesh,a,b))==0

def is_horizontal_solid(mesh,x,y,z):
    a=(x,y,z+.15);b=(x,y,z-.15)
    return len(intersections(mesh,a,b))>0

def audit(mesh=None):
    m=mesh if mesh is not None else read_obj()
    # Portals open in BOTH district boundary walls on TWO levels, checking
    # center and two lateral offsets. True unblocked air witness, not human QA.
    portals=[]
    for level,z in [('ground',2.0),('upper',12.0)]:
      for district,x in [('W',-12.0),('E',12.0)]:
        clear=[is_clear(m,(x-1.7,y,z),(x+1.7,y,z)) for y in (-.65,0,.65)]
        blocked_side=[not is_clear(m,(x-1.7,y,z),(x+1.7,y,z)) for y in (-7.0,7.0)]
        lintel=not is_clear(m,(x-1.7,0,z+4.4),(x+1.7,0,z+4.4))
        portals.append({'level':level,'district':district,'clear_three_lanes':all(clear),
                        'two_wall_sides':all(blocked_side),'solid_lintel':lintel})
    path_samples=[]
    for level,z in [('ground',1.7),('upper',11.7)]:
      for y in (-.65,0,.65):
        path_samples.append({'level':level,'y':y,
            'no_triangle_on_crossing':is_clear(m,(-18,y,z),(18,y,z))})
    floors=[]
    for z in (0,10):
       for x in (-20,0,20):
         floors.append({'z':z,'x':x,'y':0,'triangle_at_level':is_horizontal_solid(m,x,0,z)})
    # Not proof of full stair access; only physically placed last tread / slab edge.
    stair_end=[{'entrance':side,'last_step_height':10.0,'end_y':y,
                'upper_landing_height':10.0,'endpoint_geometry_expected':True}
              for side,y in [('S',-14.11),('N',14.11)]]
    gated=all(v['clear_three_lanes'] and v['two_wall_sides'] and v['solid_lintel'] for v in portals) \
       and all(v['no_triangle_on_crossing'] for v in path_samples) \
       and all(f['triangle_at_level'] for f in floors)
    r={'stage':'A83_B9_G0_INDEPENDENT_REAL_TRIANGLE_AUDIT',
       'obj_sha256':hashlib.sha256((OUT/'b9_shared_civic_seam.obj').read_bytes()).hexdigest() if mesh is None else 'IN_MEMORY_NEGATIVE',
       'vertices':len(m.vertices),'triangles':len(m.faces),
       'portal_witnesses':portals,'narrow_air_lanes':path_samples,'ground_and_upper_slab_witnesses':floors,
       'stair_endpoint_design_only':stair_end,'limited_source_true_triangle_gate':gated,
       'room_enclosure':'NOT_TESTED','continuous_body_sweep':'NOT_TESTED',
       'stair_full_body_and_egress':'NOT_TESTED','district_scale_city':'NOT_TESTED',
       'structural_load':'NOT_TESTED','formal_s1_g1_g2_g3':'NOT_RUN',
       'art':'HOLD_PENDING_TRUE_IMAGE_REVIEW','minecraft_construction':'FORBIDDEN'}
    return r

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    a=audit()
    (OUT/'independent_audit.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:a[k] for k in ('vertices','triangles','limited_source_true_triangle_gate')},indent=2))
    if not a['limited_source_true_triangle_gate']:raise SystemExit(2)
