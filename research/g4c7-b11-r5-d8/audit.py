"""Independent persisted PLY/OBJ/GLB comparison and local route witness.
Never imports builder. NOT formal 331/993 or certified human access.
"""
from pathlib import Path
import json,hashlib,math
import numpy as np
import vtk, trimesh
ROOT=Path(__file__).resolve().parent
SAMPLE_N=81
SCENE_PARTS=['urban_body','urban_warm','maker','research','habitat','support','civic','transport','landscape']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def get_mesh(path):
    m=trimesh.load(path,process=False,force='mesh')
    assert isinstance(m,trimesh.Trimesh) and np.isfinite(m.vertices).all()
    return m

def locator(path):
    r=vtk.vtkPLYReader();r.SetFileName(str(path));r.Update()
    t=vtk.vtkOBBTree();t.SetDataSet(r.GetOutput());t.BuildLocator();return t

def intersections(t,a,b):
    points=vtk.vtkPoints();cells=vtk.vtkIdList();t.IntersectWithLine(a,b,points,cells)
    return [points.GetPoint(i) for i in range(points.GetNumberOfPoints())]

def route_samples(pts,num=81):
    pts=np.asarray(pts,dtype=float);seg=np.linalg.norm(np.diff(pts[:,:2],axis=0),axis=1)
    l=np.r_[0,np.cumsum(seg)];q=np.linspace(0,l[-1],num)
    return np.column_stack([np.interp(q,l,pts[:,i]) for i in range(3)]),seg,l[-1]

def run(variant):
    folder=ROOT/variant;manifest=json.loads((folder/'manifest.json').read_text())
    assert sha(folder/'study.obj')==manifest['sha256_obj']
    assert sha(folder/'study.glb')==manifest['sha256_glb']
    scene=trimesh.load(folder/'study.glb',force='scene')
    assert isinstance(scene,trimesh.Scene)
    m=get_mesh(folder/'study.obj')
    assert len(m.faces)==manifest['faces'],(len(m.faces),manifest['faces'])
    assert np.allclose(m.bounds,np.asarray(manifest['bounds_m']),atol=.03)
    route=np.asarray(json.loads((folder/'route_ground_author.json').read_text()),float)
    samples,dist,total=route_samples(route)
    slope=np.abs(np.diff(route[:,2]))/dist
    count=0;missing_floor=[];intruding=[];clearance=[]
    for cat,d in manifest['categories'].items():
        if cat in ('urban_body','urban_warm','maker','research','habitat','support'):
            mm=get_mesh(folder/(cat+'.ply'))
            count+=len(mm.faces)
    # Re-read persisted third-party PLY, never the intended building plot metadata.
    occupied=[(tag,locator(folder/f'{tag}.ply')) for tag in ('urban_body','urban_warm','maker','research','habitat')]
    walking=locator(folder/'circulation.ply')
    for i,p in enumerate(samples):
        x,y,z=map(float,p)
        floor=intersections(walking,(x,y,z+1),(x,y,z-4))
        if not any(abs(q[2]-z)<.035 for q in floor):missing_floor.append(i)
        for tag,t in occupied:
            # A cross-sectional center+edge witness, NOT an actual solid body sweep.
            for d in (-.65,0,.65):
                hit=intersections(t,(x+d,y,z+.15),(x+d,y,z+3.25))
                if hit:
                    intruding.append({'sample':i,'category':tag,'offset_x':d,'hits':len(hit)});break
    # Negative control: insert a virtual opaque screen 15m wide at sample midpoint.
    q=samples[len(samples)//2];plane=vtk.vtkCubeSource();plane.SetBounds(q[0]-7.5,q[0]+7.5,q[1]-7.5,q[1]+7.5,q[2],q[2]+4);plane.Update()
    block=vtk.vtkOBBTree();block.SetDataSet(plane.GetOutput());block.BuildLocator()
    # Cast from OUTSIDE both cube faces; VTK OBBTree inside-start can return -1.
    assert intersections(block,(q[0],q[1],q[2]+8.0),(q[0],q[1],q[2]-3.0))
    comp_count=len(m.split(only_watertight=False))
    return {'variant':variant,'mesh_sha256':manifest['sha256_obj'],'glb_sha256':manifest['sha256_glb'],
      'faces':len(m.faces),'vertices':len(m.vertices),'occupied_plots':manifest['occupied_plot_count'],
      'study_domain_bounds_m':np.round(m.bounds,3).tolist(),
      'obj_topological_components':comp_count,
      'route_schematic_length_m':round(total,2),'route_max_segment_grade_percent':round(float(max(slope))*100,3),
      'route_81_centerline_floor_witnesses':len(samples)-len(missing_floor),
      'route_81_missing_floor_sample_indices':missing_floor,
      'route_partial_edge_occupied_ray_hits':intruding[:30],
      'route_occupied_hits_total':len(intruding),
      'fault_injection_blocker_detected':True,
      'formal_QA':'NOT_RUN','G0_art':'NOT_ADOPTED',
      'limitations':['S1/G1/G2/G3 and 331/993 NOT RUN','not continuous edge-swept human collision',
      'mesh topological components do not prove structural support','no fully functional vertical routes',
      'plots have no true living room interiors','full study-domain is not 10km city']}

if __name__=='__main__':
    vtk.vtkObject.GlobalWarningDisplayOff()
    r=[run(v) for v in ('inhabited','depopulated')]
    assert r[0]['occupied_plots']>r[1]['occupied_plots']*3
    assert r[0]['mesh_sha256']!=r[1]['mesh_sha256']
    (ROOT/'audit.json').write_text(json.dumps(r,indent=2,ensure_ascii=False))
    for x in r:print(x['variant'],'plots',x['occupied_plots'],'faces',x['faces'],'route_m',x['route_schematic_length_m'], 'floors',x['route_81_centerline_floor_witnesses'],'hits',x['route_occupied_hits_total'],'components',x['obj_topological_components'],flush=True)