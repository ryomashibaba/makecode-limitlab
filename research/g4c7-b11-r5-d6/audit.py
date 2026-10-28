"""Independent persisted-PLY audit for D6. Does not import build.py.
VTK uses exported triangles, not source program labels. This is limited technical QA.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import trimesh
import vtk
ROOT=Path(__file__).resolve().parent
PARTS=['ground','studio','structure','skin','glazing','visitor','research','learning','core','machinery']

def tree(folder,tag):
    r=vtk.vtkPLYReader();r.SetFileName(str(folder/f'{tag}.ply'));r.Update()
    t=vtk.vtkOBBTree();t.SetDataSet(r.GetOutput());t.BuildLocator();return t

def crossings(t,a,b):
    p=vtk.vtkPoints();ids=vtk.vtkIdList()
    n=t.IntersectWithLine(a,b,p,ids)
    return sorted([tuple(p.GetPoint(i)) for i in range(p.GetNumberOfPoints())], key=lambda x: sum((x[k]-a[k])**2 for k in range(3)))

def audit(h):
    folder=ROOT/f'case_{h}'
    manifest=json.loads((folder/'manifest.json').read_text())
    assert hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest()==manifest['sha256_obj']
    assert hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest()==manifest['sha256_glb']
    exported=trimesh.load(folder/'study.glb')
    assert isinstance(exported,trimesh.Scene)
    trees={k:tree(folder,k) for k in PARTS}
    # Through real façade opening from visitor eye to visible product. Ignore end 1m.
    eye=(-40,65,21.65);target=(-40,35,23.92)
    roadblock=[]
    for cat,t in trees.items():
        if cat in ('ground','visitor','glazing','machinery'):continue
        hits=crossings(t,eye,target)
        if hits:roadblock.append({'part':cat,'hit':hits[0]})
    # Actual vertical roof clearance at x=30,y=0, no intended crane apparatus.
    origin=(30,0,19.05)
    hit=crossings(trees['skin'],origin,(30,0,155))
    roof_z=hit[0][2] if hit else None
    # Ramp is measured from mesh; shallow slope at x=-40; avoid base-floor overlap.
    ramp=[]
    for y,expected in [(95,18.7),(79,19.42),(65,20)]:
        hits=crossings(trees['visitor'],(-38.5,y,60),(-38.5,y,16))
        top=max([p[2] for p in hits]) if hits else None
        ramp.append({'y':y,'expected_z':expected,'measured_z':top,
                     'within_0_03m':top is not None and abs(top-expected)<.03})
    # Reference to zero formal QA; no claims about wall occupancy.
    # Inject a temporary occluding rectangle into a separate VTK dataset; verify
    # that the witness genuinely detects a blocked optical path, not an empty check.
    blocker=vtk.vtkCubeSource()
    blocker.SetBounds(-45,-35,49,52,18,37);blocker.Update()
    blocker_tree=vtk.vtkOBBTree();blocker_tree.SetDataSet(blocker.GetOutput());blocker_tree.BuildLocator()
    negative_hit=crossings(blocker_tree,eye,target)
    assert negative_hit,"Negative control failed to detect blocking façade"
    result={'height_case':h,'obj_sha256':manifest['sha256_obj'],'glb_sha256':manifest['sha256_glb'],
      'model_bound_m':manifest['bounds_m'],'faces':manifest['faces'],
      'opaque_intersections_on_proposed_visitor_to_product_ray':roadblock,
      'roof_hit_z_m':roof_z,'roof_clearance_at_x30_y0_m':None if roof_z is None else round(roof_z-19.05,3),
      'expected_clearance_at_x30_y0_m':h,
      'floor_mesh_ramp_witnesses':ramp,
      'injected_opaque_screen_is_detected':bool(negative_hit),
      'warnings':['single ray cannot certify viewing aperture over person width','measured visible path is not a certified human route',
         'research level has no certified vertical travel mechanism',
         'facade is architecturally primitive; no real city skyline','S1/G1/G2/G3 NOT RUN'],
      'status':'LIMITED_GEOMETRY_WITNESS_NOT_ART_PASS'}
    assert not roadblock,roadblock
    assert roof_z is not None and abs(roof_z-(19.05+h))<.01
    assert all(x['within_0_03m'] for x in ramp),ramp
    return result

if __name__=='__main__':
    all_cases=[audit(h) for h in [70,90]]
    assert all_cases[0]['obj_sha256']!=all_cases[1]['obj_sha256']
    assert abs(all_cases[1]['roof_hit_z_m']-all_cases[0]['roof_hit_z_m']-20)<1e-3
    (ROOT/'audit.json').write_text(json.dumps(all_cases,indent=2,ensure_ascii=False))
    print(json.dumps(all_cases,indent=2,ensure_ascii=False))
