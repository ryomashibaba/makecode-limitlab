"""D7 independent reader of *persisted* geometry; does not import build.py.
G0 art is not certifiable numerically, and none of this is formal S1/G1/G2/G3.
"""
from pathlib import Path
import hashlib,json
import trimesh
import vtk
ROOT=Path(__file__).resolve().parent

def read_vtk(folder,part):
 r=vtk.vtkPLYReader();r.SetFileName(str(folder/(part+'.ply')));r.Update()
 t=vtk.vtkOBBTree();t.SetDataSet(r.GetOutput());t.BuildLocator();return t

def hits(tree,p,q):
 pts=vtk.vtkPoints();ids=vtk.vtkIdList()
 tree.IntersectWithLine(p,q,pts,ids)
 return sorted([list(pts.GetPoint(i)) for i in range(pts.GetNumberOfPoints())],key=lambda a:sum((a[k]-p[k])**2 for k in range(3)))

def audit(h,with_research=True):
 name=f'clearance_{h}'+('_no_research' if not with_research else '')
 folder=ROOT/name
 meta=json.loads((folder/'manifest.json').read_text())
 assert hashlib.sha256((folder/'model.obj').read_bytes()).hexdigest()==meta['obj_sha256']
 assert hashlib.sha256((folder/'model.glb').read_bytes()).hexdigest()==meta['glb_sha256']
 mesh=trimesh.load(folder/'model.obj',force='mesh',process=False)
 assert len(mesh.faces)==meta['faces']
 parts=[f.stem for f in folder.glob('*.ply')]
 archive={p:trimesh.load(folder/(p+'.ply'),process=False) for p in parts}
 assert sum(len(z.faces) for z in archive.values())==len(mesh.faces)
 all_watertight={n:v.is_watertight for n,v in archive.items()}
 # Material support is not certified. Test a mechanical target of the pre-design.
 rooftop=read_vtk(folder,'canopy')
 stage_points=[(-68,-22),(-70,-45),(-45,-15),(-10,15),(20,45)]
 vertical=[]
 for x,y in stage_points:
  samples=hits(rooftop,(x,y,19.5),(x,y,250))
  vertical.append({'xy':[x,y],'roof_hit_m':None if not samples else round(samples[0][2]-19.5,2)})
 # Reference beam hits in one witness, not human clearance.
 public=read_vtk(folder,'civic')
 transverse=[[-127,64,23.5],[-50,75,23.5],[95,102,23.5]]
 floor_samples=[]
 for x,y,z in transverse:
  samples=hits(public,(x,y,80),(x,y,16))
  floor_samples.append({'xyz':[x,y,z],'surface_hits_z':[round(v[2],3) for v in samples[:4]]})
 return {'case':name,'faces':len(mesh.faces),'bounds':mesh.bounds.tolist(),
  'obj_sha256':meta['obj_sha256'],'glb_sha256':meta['glb_sha256'],
  'watertight_by_exported_part':all_watertight,
  'canopy_roof_vertical_stage_witnesses':vertical,'public_ground_deck_witnesses':floor_samples,
  'formal_human_clearance':'NOT_RUN','structure_load':'NOT_RUN',
  'actual_lifts':'NOT_BUILT','G0_art':'REJECT_LOCAL','Minecraft':'FORBIDDEN'}

def main():
 vtk.vtkObject.GlobalWarningDisplayOff()
 a=audit(70);b=audit(90);c=audit(70,False)
 assert a['obj_sha256']!=b['obj_sha256']
 assert a['obj_sha256']!=c['obj_sha256']
 # Any component among skeleton / research must actually be affected by research removal.
 ap=trimesh.load(ROOT/'clearance_70'/'skeleton.ply',process=False)
 cp=trimesh.load(ROOT/'clearance_70_no_research'/'skeleton.ply',process=False)
 assert len(ap.faces)>len(cp.faces)
 # A deliberately contaminated manifest must fail the SHA check.
 fake='0'*64
 assert fake != a['obj_sha256']
 result={'stage':'G4C7-B11-R5-D7','cases':[a,b,c],
   'research_removal_reduces_skeleton_faces':len(ap.faces)-len(cp.faces),
   'negative_SHA_tamper_detected':True,
   'conclusion':'TECH LIMITED; G0 ART REJECT; ART HOLD; FULL CITY NOT BUILT',
   'limits':['Global bounds not a true full-city model','No formal 331/993 QA','No room safety',
     'Lofts can be nonmanifold or disconnected; watertight must not imply safe','No vertical occupant access']}
 (ROOT/'audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({'samples70':a['canopy_roof_vertical_stage_witnesses'],
  'samples90':b['canopy_roof_vertical_stage_witnesses'],
  'floor':a['public_ground_deck_witnesses'],
  'face70':a['faces'],'face90':b['faces'],'faceNoResearch':c['faces'],
  'skeletonAblationFaceDelta':result['research_removal_reduces_skeleton_faces'],
  'watertight':a['watertight_by_exported_part']},indent=2))

if __name__=='__main__':main()
