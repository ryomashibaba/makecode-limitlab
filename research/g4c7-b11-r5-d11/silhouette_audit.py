"""Category visibility pixels from REAL persisted D11 PLY (not image concepts).
A visual diagnostic, not an aesthetic scoring system or automated art acceptance.
VTK renders unlit flat-semantic-color scene and counts pixels by visible mesh role.
"""
from pathlib import Path
import vtk, numpy as np, json
from PIL import Image
from vtk.util.numpy_support import vtk_to_numpy
ROOT=Path(__file__).resolve().parent
ROLES=('terrain','fault_mass','ceramic','dark_skin','public','maker','research','habitat','garden','structural','glass','core','light')
COLORS={name:(i*17+20,i*11+50,i*13+70) for i,name in enumerate(ROLES)}
VIEWS={
'far':((1030,-920,540),(0,10,121),37),
'public_maker':((0,-94,23.1),(-135,38,32),63),
'public_research':((0,-94,23.1),(130,65,34),63),
'inner_canyon':((22,-145,39),(0,115,139),63),
}
def perform(case='full_70'):
 root=ROOT/case;results={}
 for name,(pos,target,fov) in VIEWS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(0,0,0)
  for cat in ROLES:
   p=root/(cat+'.ply')
   if not p.exists():continue
   r=vtk.vtkPLYReader();r.SetFileName(str(p));r.Update()
   mp=vtk.vtkPolyDataMapper();mp.SetInputData(r.GetOutput());mp.ScalarVisibilityOff()
   act=vtk.vtkActor();act.SetMapper(mp)
   act.GetProperty().LightingOff();act.GetProperty().SetColor(*[v/255 for v in COLORS[cat]]);act.GetProperty().SetOpacity(1.)
   ren.AddActor(act)
  cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov);ren.ResetCameraClippingRange()
  win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1000,700);win.SetMultiSamples(0);win.AddRenderer(ren);win.Render()
  grab=vtk.vtkWindowToImageFilter();grab.SetInput(win);grab.SetInputBufferTypeToRGB();grab.Update()
  im=grab.GetOutput();dims=im.GetDimensions();a=vtk_to_numpy(im.GetPointData().GetScalars()).reshape(dims[1],dims[0],3)
  # Black background; category pixels are fully flat colored; no light / antialias.
  classified={k:int(np.all(a==rgb,axis=2).sum()) for k,rgb in COLORS.items()}
  total=int(sum(classified.values()));assert total>2000,(name,total)
  results[name]={'visible_scene_pixels':total,'share_of_rendered_occupied_pixels':{k:round(v/total,5) for k,v in classified.items()},
   'massive_outer_cliff_share':round(sum(classified.get(k,0) for k in ('fault_mass','ceramic','dark_skin'))/total,5),
   'activity_share':round(sum(classified.get(k,0) for k in ('maker','research','habitat'))/total,5)}
  # Exposes masking provenance in locally saved PNGs; they're diagnostic segmentation, not beauty images.
  Image.fromarray(np.flipud(a)).save(root/(name+'_semantic.png'))
  win.Finalize()
  print(case,name,'outer_share',results[name]['massive_outer_cliff_share'],'activity_share',results[name]['activity_share'],flush=True)
 return results
if __name__=='__main__':
 r={'full_70':perform('full_70'),'without_research_70':perform('without_research_70')}
 (ROOT/'silhouette_audit.json').write_text(json.dumps(r,indent=2))
