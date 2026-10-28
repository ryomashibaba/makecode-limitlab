"""D10 independent audit of persisted PLY, OBJ and GLB.
Does not import the generator. Reports failed design gates without rewriting history.
All results remain research-only, not S1/G1/G2/G3, not engineering certification.
"""
from pathlib import Path
from math import hypot, dist, sqrt
import hashlib,json
import vtk
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
ROLES=('terrain','fabrication','research','habitat','city_body','public','glass','frame','service','vegetation')
E1=(-445,120);E2=(155,165)

def pl(filename):
    reader=vtk.vtkPLYReader();reader.SetFileName(str(filename));reader.Update()
    poly=reader.GetOutput()
    assert poly.GetNumberOfPolys()>0,filename
    return poly

def tree(poly):
    t=vtk.vtkOBBTree();t.SetDataSet(poly);t.BuildLocator();return t

def hits(t,a,b):
    pts=vtk.vtkPoints();ids=vtk.vtkIdList()
    t.IntersectWithLine(a,b,pts,ids)
    return [tuple(pts.GetPoint(i)) for i in range(pts.GetNumberOfPoints())]

def closest_point(poly,p):
    t=vtk.vtkCellLocator();t.SetDataSet(poly);t.BuildLocator()
    closest=[0.,0.,0.];cell=vtk.vtkGenericCell();cid=vtk.mutable(0);sid=vtk.mutable(0);d2=vtk.mutable(0.)
    t.FindClosestPoint(p,closest,cell,cid,sid,d2)
    return {'distance_m':float(sqrt(d2)), 'nearest_xyz':list(map(float,closest))}

def route_to_xy(q,r):
    def ds(a,b,c):
        dx,dy=b[0]-a[0],b[1]-a[1]
        n=dx*dx+dy*dy;t=max(0.,min(1.,((c[0]-a[0])*dx+(c[1]-a[1])*dy)/n))
        return hypot(c[0]-a[0]-t*dx,c[1]-a[1]-t*dy)
    return min(ds(a,b,q) for a,b in zip(r,r[1:]))

def run(name):
    folder=ROOT/name
    m=json.loads((folder/'manifest.json').read_text())
    assert hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest()==m['sha256_obj']
    assert hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest()==m['sha256_glb']
    tri=trimesh.load(folder/'study.obj',force='mesh',process=False)
    assert len(tri.faces)==m['triangles']
    shapes={};loc={}
    for role,c in m['categories'].items():
        p=folder/f'{role}.ply'
        assert hashlib.sha256(p.read_bytes()).hexdigest()==c['sha256_ply']
        shapes[role]=pl(p);loc[role]=tree(shapes[role])
    r=m['civic_path_points'];public=loc['public'];terrain=loc['terrain']
    route_witness=[]
    for x,y,z in r:
        ps=hits(public,(x,y,z+2.0),(x,y,z-4))
        ps=[p for p in ps if abs(p[2]-z)<.25]
        route_witness.append({'xy':[x,y],'has_planned_public_floor':bool(ps)})
    test={}
    # Sightlines are evaluated from immutable saved PLY, not speculative visual labels.
    lines={
      'civic_to_maker':((-220,70,22),(-420,-35,24)),
      'maker_view_to_activity':((-440,32,21),(-460,-25,24)),
      'civic_to_research':((55,112,21.7),(160,116,122)),
      'research_court_to_activity':((72,128,21.7),(180,120,124)),
    }
    for k,(a,b) in lines.items():
        obstruct=[]
        for role in ('city_body','habitat','fabrication','research','frame','service'):
            for p in hits(loc[role],a,b) if role in loc else []:
                # Do not interpret intersections at target surfaces as open sightlines.
                if dist(p,a)>1.5 and dist(p,b)>1.5:obstruct.append({'role':role,'xyz':p})
        test[k]={'unobstructed':not bool(obstruct),'opaque_intersections':obstruct[:12]}
    core_info={}
    for namecore,(x,y) in {'E1':E1,'E2':E2}.items():
        ground_gap=route_to_xy((x,y),r)
        # direct actual minimum distance to actual research mesh from upper transfer
        upper=closest_point(shapes['research'],(x,y,112)) if 'research' in shapes else None
        ground=closest_point(shapes['public'],(x,y,18))
        core_info[namecore]={'public_ground_centerline_distance_m':ground_gap,
            'distance_112m_landing_to_research_mesh':upper,
            'distance_18m_landing_to_public_mesh':ground}
    # research mesh nearest point need not be a WALKABLE floor. Even zero is not PASS.
    test['fault_blocker']=bool(hits(tree(_blocker()),(-220,70,22),(-420,-35,24)))
    return {'variant':name,'faces':len(tri.faces),'obj_sha_ok':True,'glb_sha_ok':True,
      'route_samples':len(r),'route_centerline_surface_witnesses':sum(x['has_planned_public_floor'] for x in route_witness),
      'route_witness':route_witness,'public_sightlines':test,'core_landings':core_info,
      'hard_gates':{
        'two_cores_ground_connected_within_8m':all(v['public_ground_centerline_distance_m']<=8 for v in core_info.values()),
        'two_cores_research_access_within_8m':all(v['distance_112m_landing_to_research_mesh'] is not None and v['distance_112m_landing_to_research_mesh']['distance_m']<=8 for v in core_info.values()),
        'maker_and_research_both_visible_from_public_eye':test['civic_to_maker']['unobstructed'] and test['civic_to_research']['unobstructed'],
        'negative_fault_detection':test['fault_blocker'],
        'route_centerline_floor_all_sampled':all(x['has_planned_public_floor'] for x in route_witness)
      },
      'status':{'art':'G0 ART REJECT','formal_safety':'NOT_RUN','minecraft':'FORBIDDEN','adopted':0},
      'limitations':['cell distance is not an actual doorway','route point witness not swept body',
        'no true lifts or structural loads','no validated room sun/egress']}

def _blocker():
    cube=vtk.vtkCubeSource();cube.SetBounds(-330,-310,12,30,16,41);cube.Update()
    return cube.GetOutput()

if __name__=='__main__':
    rs=[run('all_70'),run('no_research_70')]
    assert rs[0]['obj_sha_ok'] and rs[1]['obj_sha_ok']
    assert rs[0]['faces']>rs[1]['faces']
    assert all(x['public_sightlines']['fault_blocker'] for x in rs)
    (ROOT/'audit.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2))
    for d in rs:
        print(d['variant'],d['faces'],d['route_centerline_surface_witnesses'],d['hard_gates'],flush=True)