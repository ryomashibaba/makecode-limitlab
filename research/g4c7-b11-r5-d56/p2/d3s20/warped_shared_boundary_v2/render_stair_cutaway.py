"""Diagnostic visualization of actual saved GLB stair treads, with other meshes hidden.
Does not insert any unsupported stairs into the geometry.
"""
from pathlib import Path
import numpy as np,trimesh,vtk
from PIL import Image,ImageDraw
from vtk.util.numpy_support import vtk_to_numpy
from warped_contract import ROOT
loaded=trimesh.load(ROOT/'V2_WARPED_STAIRS_BASE.glb',force='scene')
rr=vtk.vtkRenderer();rr.SetBackground(.06,.09,.13);rr.SetBackground2(.23,.28,.34);rr.GradientBackgroundOn()
count=0
for name,mesh in loaded.geometry.items():
 if not name.startswith('STAIR_TREAD_') and not ('FLOOR_ROOF_' in name and ('(5,3,1)' in name or '(5,0,0)' in name)):
  continue
 points=vtk.vtkPoints()
 for p in mesh.vertices:points.InsertNextPoint(*map(float,p))
 polys=vtk.vtkCellArray()
 for f in mesh.faces:
  tri=vtk.vtkTriangle()
  for j,id in enumerate(f):tri.GetPointIds().SetId(j,int(id))
  polys.InsertNextCell(tri)
 data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(polys)
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(data)
 actor=vtk.vtkActor();actor.SetMapper(mapper)
 if name.startswith('STAIR_TREAD_'):actor.GetProperty().SetColor(.95,.66,.34)
 else:actor.GetProperty().SetColor(.55,.78,.72)
 actor.GetProperty().SetAmbient(.35);rr.AddActor(actor);count+=1
cam=vtk.vtkCamera();cam.SetPosition(47,3,15);cam.SetFocalPoint(27,14,1.7);cam.SetViewUp(0,0,1);cam.SetViewAngle(27);rr.SetActiveCamera(cam)
rr.ResetCameraClippingRange()
rw=vtk.vtkRenderWindow();rw.SetOffScreenRendering(1);rw.SetSize(1200,810);rw.AddRenderer(rr);rw.Render()
wf=vtk.vtkWindowToImageFilter();wf.SetInput(rw);wf.Update()
img=wf.GetOutput();arr=vtk_to_numpy(img.GetPointData().GetScalars()).reshape(img.GetDimensions()[1],img.GetDimensions()[0],-1)
im=Image.fromarray(np.flipud(arr)).convert('RGB');d=ImageDraw.Draw(im)
d.text((20,20),'CUTAWAY: ONLY SAVED STAIR TREAD MESHES SHOWN',fill='white')
d.text((20,43),'Other GLB walls and roofs temporarily hidden for inspection',fill='white')
im.save(ROOT/'STAIR_SAVED_GLB_CUTAWAY.jpg',quality=92)
print('shown',count)
rw.Finalize()
