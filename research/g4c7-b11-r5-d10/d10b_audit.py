"""Independent D10B saved-mesh geometry audit. Does not import d10b generator.
No life-safety, load, working elevator, or formal Minecraft certification.
"""
from pathlib import Path
import vtk,hashlib,json,math,trimesh
P=Path(__file__).resolve().parent/'d10b'
def mesh(role):
 r=vtk.vtkPLYReader();r.SetFileName(str(P/f'{role}.ply'));r.Update()
 assert r.GetOutput().GetNumberOfCells()>0
 return r.GetOutput()
def obb(m):
 t=vtk.vtkOBBTree();t.SetDataSet(m);t.BuildLocator();return t
def hit(tree,a,b):
 pts=vtk.vtkPoints();ids=vtk.vtkIdList();tree.IntersectWithLine(a,b,pts,ids)
 return [tuple(pts.GetPoint(i)) for i in range(pts.GetNumberOfPoints())]
def nearest_surface_z(t,x,y,z):
 points=hit(t,(x,y,z+2),(x,y,z-3));return min((abs(p[2]-z),p[2]) for p in points) if points else (float('inf'),None)

def run():
 m=json.loads((P/'manifest.json').read_text())
 assert hashlib.sha256((P/'study.obj').read_bytes()).hexdigest()==m['sha256_obj']
 assert hashlib.sha256((P/'study.glb').read_bytes()).hexdigest()==m['sha256_glb']
 obj=trimesh.load(P/'study.obj',force='mesh',process=False)
 assert len(obj.faces)==m['faces']
 objects={k:mesh(k) for k in m['ply_sha256']}
 assert all(hashlib.sha256((P/f'{k}.ply').read_bytes()).hexdigest()==v for k,v in m['ply_sha256'].items())
 t={k:obb(v) for k,v in objects.items()}
 ro=hit(t['structure'],(-145,-126,20),(-145,-126,170))
 roof=min([z for x,y,z in ro if z>30],default=None)
 floor=hit(t['maker'],(-145,-126,30),(-145,-126,14))
 worktop=max([z for x,y,z in floor],default=None)
 # Both eye rays are from exactly one shared, PUBLIC location, not separate idealized cameras.
 eye=(-20,20,21.7);rays={'maker':(-154,-107,23),'research':(95,91,22)}
 visibility={}
 for name,target in rays.items():
  obstructions=[]
  for role in ('structure','maker','research','core','habitat','machine'):
   if role not in t:continue
   for p in hit(t[role],eye,target):
    da=math.dist(eye,p);db=math.dist(target,p)
    if da>1 and db>1:obstructions.append({'role':role,'xyz':p})
  visibility[name]={'unblocked_saved_ply':not obstructions,'opaque_intersections':obstructions[:6]}
 # Two core shafts have THREE actual horizontal platforms each; independent raster sample of saved PLY.
 landings=[]
 for x in (-120,140):
  for z in (18,112,209):
   err,actual=nearest_surface_z(t['core'],x,20,z)
   landings.append({'x':x,'y':20,'z_plan':z,'floor_z':actual,'valid':err<.05})
 # 112m public floor is a corridor from both upper cores to the research activity branch.
 upper=[(-120,20,112),(-20,20,112),(95,20,112),(140,20,112),(96,45,112),(96,65,112)]
 floor_checks=[]
 for x,y,z in upper:
  e,v=nearest_surface_z(t['floor'],x,y,z)
  floor_checks.append({'xyz':[x,y,z],'nearest_walktop_z':v,'pass':e<.05})
 # Negative control an opaque screen intentionally placed in the optical line.
 screen=vtk.vtkCubeSource();screen.SetBounds(-105,-95,-77,-57,18,33);screen.Update()
 simulated=hit(obb(screen.GetOutput()),eye,rays['maker'])
 result={'stage':'B11-R5 D10B','scope':'local_function_first_geometry_only',
  'triangle_count':len(obj.faces),'measured_maker_floor_z':worktop,'measured_roof_underside_z':roof,
  'measured_working_clearance_m':None if roof is None or worktop is None else roof-worktop,
  'single_shared_public_eye':list(eye),'visibility':visibility,
  'core_3level_platforms':landings,'upper_floor_witnesses':floor_checks,
  'art':'ART HOLD (aesthetic quality not met)','construction':'FORBIDDEN',
  'fault_injected_screen_detected':bool(simulated),
  'gates':{'70m_maker_clearance_sample':roof is not None and worktop is not None and roof-worktop>=70-.01,
   'one_eye_two_visible_activities':all(v['unblocked_saved_ply'] for v in visibility.values()),
   'two_core_three_level_platform_meshes':all(v['valid'] for v in landings),
   'research_level_walking_surface_witnesses':all(q['pass'] for q in floor_checks),
   'negative_control_detection':bool(simulated)},
  'limits':['Open optical ray does not guarantee viewed content is visually legible',
    'Upper research floor witness not a human width continuous swept volume',
    'Core shaft platforms are NOT elevator cars, stairs, access, egress, or load-rated',
    'Function-first scaffold is NOT qualifying future-city art','No 331/993 formal QA']}
 (P/'audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({k:result[k] for k in ('triangle_count','measured_working_clearance_m','gates')},indent=2))
if __name__=='__main__':run()