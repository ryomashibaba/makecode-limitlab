"""Independent persisted-PLY geometry audit, not imported from D11 build.py.
A successful diagnostic is NOT positive art, safety, structural or MakeCode acceptance.
"""
from pathlib import Path
import json, hashlib
import numpy as np, vtk
import trimesh
ROOT=Path(__file__).resolve().parent
OPAQUE=['fault_mass','ceramic','dark_skin','structural','maker','research','habitat']

def load(folder,role):
 p=folder/(role+'.ply')
 if not p.exists(): return None
 r=vtk.vtkPLYReader();r.SetFileName(str(p));r.Update();return r.GetOutput()

def inside(poly,pt):
 if poly is None:return False
 s=vtk.vtkSelectEnclosedPoints();s.SetSurfaceData(poly);s.SetTolerance(1e-5);s.Initialize(poly)
 try:return bool(s.IsInsideSurface(*[float(x) for x in pt]))
 finally:s.Complete()

def hit(poly,a,b):
 if poly is None:return []
 tree=vtk.vtkOBBTree();tree.SetDataSet(poly);tree.BuildLocator()
 points=vtk.vtkPoints();ids=vtk.vtkIdList()
 tree.IntersectWithLine([float(v) for v in a],[float(v) for v in b],points,ids)
 return [[round(v,4) for v in points.GetPoint(i)] for i in range(points.GetNumberOfPoints())]

def study(h=70,research=True):
 folder=ROOT/(('full' if research else 'without_research')+'_'+str(h));m=json.loads((folder/'manifest.json').read_text())
 assert m['formal_S1_G1_G2_G3']=='NOT_RUN' and m['minecraft']=='FORBIDDEN'
 assert hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest()==m['sha256_obj']
 assert hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest()==m['sha256_glb']
 mesh=trimesh.load(folder/'study.obj');assert len(mesh.faces)==m['faces']
 poly={k:load(folder,k) for k in m['categories']}
 assert all(hashlib.sha256((folder/(cat+'.ply')).read_bytes()).hexdigest()==meta['sha256_ply'] for cat,meta in m['categories'].items())
 # These are core *interior candidate* points, at intended visitor levels.
 core_pts=[[-285,55,132.9],[283,55,132.9],[-285,55,220.9],[283,55,220.9]]
 core=[{'xyz':p,'within_opaque':{c:inside(poly.get(c),p) for c in ('fault_mass','ceramic','dark_skin')},
        'inside_core_cage_frame':inside(poly.get('core'),p)} for p in core_pts]
 # Sample upper public-bridge centerline; a floor might exist beneath but volume may be occupied.
 research_p=[(-285,55),(-216,86),(-138,124),(-45,146),(45,144),(119,127),(199,89),(283,55)]
 research_audit=[]
 for x,y in research_p:
  z=133.5
  research_audit.append({'xyz':[x,y,z],'solid_interiors':[c for c in ('fault_mass','ceramic','dark_skin') if inside(poly.get(c),(x,y,z))]})
 # Public eye is away from the canyon-side volume; witness is one ray to selected equipment point.
 # A wider cone is needed to know if production and science are truly perceptible.
 eye=(0,-94,22.1)
 rays={ 'fabrication':(-143,39,23),'science':(132,73,26) }
 sight={}
 for name,target in rays.items():
  hits={cat:hit(poly.get(cat),eye,target) for cat in OPAQUE if hit(poly.get(cat),eye,target)}
  sight[name]={'from':eye,'to':target,'opaque_category_hits':hits}
 # Wide radial visibility to activity zones: nine independent endpoints each.
 cone={}
 for name,target in rays.items():
  visible=0;by_role={}
  for dx in [-7,0,7]:
   for dz in [-2,0,2]:
    test=(target[0]+dx,target[1],target[2]+dz)
    # A ray intentionally terminates INSIDE the target activity object.
    # Intersecting the target itself is the expected surface witness, not occlusion.
    self_role='maker' if name=='fabrication' else 'research'
    blocks=[c for c in OPAQUE if c!=self_role and hit(poly.get(c),eye,test)]
    if not blocks:visible+=1
    for c in blocks:by_role[c]=by_role.get(c,0)+1
  cone[name]={'clear_rays_of_9':visible,'category_block_counts':by_role}
 # Roof over the fabrication stage at x=-125, y=25; this might hit maker glass before roof.
 root=(-125,25,20); up=(-125,25,180)
 roof=hit(poly.get('dark_skin'),root,up)
 roof_clearance=min((p[2]-20 for p in roof if p[2]>=20),default=None)
 # Test fault injection with in-memory cube, not a saved mesh mutation.
 brick=vtk.vtkCubeSource();brick.SetBounds(-75,-67,-36,-24,18,38);brick.Update()
 neg=hit(brick.GetOutput(),eye,(-143,39,23))
 result={'stage':'D11','variant':folder.name,'obj_sha256':m['sha256_obj'],'faces':len(mesh.faces),
  'core_and_landings_occupied':core,'upper_bridge_samples':research_audit,
  'sightline_rays':sight,'vision_cone':cone,'maker_roof_bottom_ray_m':roof_clearance,
  'synthetic_barrier_detected':bool(neg),
  'core_4_of_4_in_opaque_urban_mass':sum(any(x['within_opaque'].values()) for x in core)==4,
  'independent_qa_scope':'stored PLY geometry witnesses; DOES NOT certify any human route, structural support or visual quality',
  'ART':'NOT_ADOPTED','G0':'REVIEW_REQUIRED','formal_S1_G1_G2_G3':'NOT_RUN','minecraft':'FORBIDDEN'}
 assert result['synthetic_barrier_detected']
 assert result['core_4_of_4_in_opaque_urban_mass'] if research else True
 assert roof_clearance is not None and abs(roof_clearance-h)<1e-3,(roof_clearance,h)
 return result

if __name__=='__main__':
 d=[study(70,True),study(90,True),study(70,False)]
 assert d[0]['obj_sha256']!=d[2]['obj_sha256']
 assert len(d[0]['upper_bridge_samples'])==8
 assert d[0]['faces']>d[2]['faces']
 assert d[0]['maker_roof_bottom_ray_m']==70 and d[1]['maker_roof_bottom_ray_m']==90
 (ROOT/'audit.json').write_text(json.dumps(d,indent=2,ensure_ascii=False))
 for r in d:
  print(r['variant'],'faces',r['faces'],'roof_m',r['maker_roof_bottom_ray_m'],
    'core_opaque',[(x['xyz'],x['within_opaque']) for x in r['core_and_landings_occupied']],
    'research_bridge_opaque',[(q['xyz'],q['solid_interiors']) for q in r['upper_bridge_samples']],
    'visibility',r['vision_cone'],flush=True)
 print('D11 deterministic persisted-PLY diagnostics PASS. ARCHITECTURE ART REJECT/HOLD, NO CONSTRUCTION.')
