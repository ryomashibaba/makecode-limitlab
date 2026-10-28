"""Independent D13 pre-art negative-control audit from stored categorical PLY.
Distinct from D12 formal safety; used solely for comparing the three failed art hypotheses.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import vtk
from PIL import Image
ROOT=Path(__file__).resolve().parent
CAMS={'distant':([1030,-1140,710],[0,-15,145],41),
      'district':([400,-670,360],[0,-30,110],49),
      'public_eye':([0,-20,26],[0,105,80],68),
      'culture_eye':([78,60,60],[-125,-140,100],68)}
COLORS={'inhabited':(240,50,60), 'fabrication':(30,180,230), 'cultural':(250,200,20),
        'research':(65,255,100),'habitat':(240,120,255),
        'public_route':(240,245,180),'core':(100,190,230)}
SUMMARY=[]
for name in ('canyon','braided','courts'):
 folder=ROOT/name;m=json.loads((folder/'manifest.json').read_text())
 assert hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest()==m['sha256_obj']
 assert hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest()==m['sha256_glb']
 geos={}
 for role,s in m['roles'].items():
  p=folder/f'{role}.ply';assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256']
  rd=vtk.vtkPLYReader();rd.SetFileName(str(p));rd.Update()
  assert rd.GetOutput().GetNumberOfPolys()==s['faces']
  geos[role]=rd.GetOutput()
 assert sum(x['faces'] for x in m['roles'].values())==m['faces']
 views={}
 for label,(pos,focal,angle) in CAMS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(0,0,0)
  for role,data in geos.items():
   mp=vtk.vtkPolyDataMapper();mp.SetInputData(data);mp.ScalarVisibilityOff()
   a=vtk.vtkActor();a.SetMapper(mp);prop=a.GetProperty()
   prop.SetLighting(False);prop.SetColor(*[c/255 for c in COLORS[role]])
   ren.AddActor(a)
  cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*focal);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
  ren.ResetCameraClippingRange()
  win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(720,480);win.SetMultiSamples(0);win.AddRenderer(ren)
  win.Render()
  flt=vtk.vtkWindowToImageFilter();flt.SetInput(win);flt.Update()
  path=folder/f'{label}_roles.png'
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(path));writer.SetInputConnection(flt.GetOutputPort());writer.Write();win.Finalize()
  data=np.array(Image.open(path).convert('RGB'))
  occupied=np.any(data>0,axis=2)
  mass=np.all(data==COLORS['inhabited'],axis=2)
  roles={k:int(np.all(data==c,axis=2).sum()) for k,c in COLORS.items()}
  role_total=sum(v for k,v in roles.items() if k!='inhabited')
  filled=int(occupied.sum())
  views[label]={'visible_pixels':filled,'inhabited_mass_pixels':int(mass.sum()),
         'mass_visible_fraction':round(int(mass.sum())/max(filled,1),4),
         'program_visible_fraction':round(role_total/max(filled,1),4),
         'role_pixels':roles}
 summary={'variant':name,'faces':m['faces'],'body_faces':m['roles']['inhabited']['faces'],
          'form_invariant_if_research_floors_removed':True, # no branch in generator's mass using program roles
          'g0':'PRE_ART_REJECT','formal_qa':'NOT_RUN','minecraft':'FORBIDDEN','views':views}
 SUMMARY.append(summary)
 print(name,'faces',m['faces'],'mass ratio',[views[t]['mass_visible_fraction'] for t in CAMS],flush=True)
assert all(x['views']['distant']['mass_visible_fraction']>0.85 for x in SUMMARY)
assert all(x['views']['public_eye']['mass_visible_fraction']>0.3 for x in SUMMARY)
(ROOT/'audit.json').write_text(json.dumps({'stage':'D13','cases':SUMMARY,
 'interpretation':'role colors quantify composition but not aesthetic quality; authored pre-art REJECT by visual inspection',
 'ablation_caveat':'mass is generated before activity floors and does not depend on activity toggles; negative design result',
 'formal_S1_G1_G2_G3':'NOT_RUN','art_adopted':0,'minecraft':'FORBIDDEN'},indent=2,ensure_ascii=False))