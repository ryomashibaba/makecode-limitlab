"""Read persisted GLB, not the author state. Render 8 fixed cameras using VTK."""
from pathlib import Path
import numpy as np
import trimesh, vtk
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent
scene=trimesh.load(R/'CIVIC_CANYON_PILOT.glb',force='scene')
meshes=list(scene.geometry.items())

def vtk_poly(mesh):
 p=vtk.vtkPoints();p.SetNumberOfPoints(len(mesh.vertices))
 for i,v in enumerate(mesh.vertices):p.SetPoint(i,*map(float,v))
 tris=vtk.vtkCellArray()
 for face in mesh.faces:
  cell=vtk.vtkTriangle()
  for k,t in enumerate(face):cell.GetPointIds().SetId(k,int(t))
  tris.InsertNextCell(cell)
 poly=vtk.vtkPolyData();poly.SetPoints(p);poly.SetPolys(tris)
 return poly
ren=vtk.vtkRenderer();ren.SetBackground(.073,.112,.156);ren.SetBackground2(.16,.22,.28);ren.GradientBackgroundOn()
w=vtk.vtkRenderWindow();w.SetOffScreenRendering(1);w.SetSize(1050,660);w.AddRenderer(ren)
for name,mesh in meshes:
 a=vtk.vtkActor();mp=vtk.vtkPolyDataMapper();mp.SetInputData(vtk_poly(mesh));a.SetMapper(mp)
 if hasattr(mesh.visual,'face_colors'):
  color=np.mean(mesh.visual.face_colors[:,:3],axis=0)/255.
 else:color=np.array([.7,.7,.75])
 a.GetProperty().SetColor(*map(float,color));a.GetProperty().SetOpacity(1.0)
 a.GetProperty().SetSpecular(.2);a.GetProperty().SetSpecularPower(22)
 a.GetProperty().SetAmbient(.22);a.GetProperty().SetDiffuse(.78)
 ren.AddActor(a)
light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(-430,-520,700);light.SetFocalPoint(0,0,70);light.SetIntensity(1.0);ren.AddLight(light)
light2=vtk.vtkLight();light2.SetLightTypeToSceneLight();light2.SetPosition(350,200,570);light2.SetFocalPoint(0,0,40);light2.SetIntensity(.65);ren.AddLight(light2)
# XYZ coordinate X east, Y north, Z up. Camera VTK view up always approximated +Z.
views={
 '01_CITY_SOUTH':((360,-710,360),(0,0,110),35),
 '02_CITY_NORTH':((-380,750,390),(0,0,105),35),
 '03_AERIAL':((0,-200,890),(0,0,70),38),
 '04_EAST_OBLIQUE':((570,220,410),(0,0,90),34),
 '05_CIVIC_EYE':((-6,-170,25),(-15,70,44),56),
 '06_MARKET_EYE':((67,-125,25),(-30,5,27),55),
 '07_FORGE_EYE':((-92,-118,27),(-50,45,47),50),
 '08_HIGH_GALLERY':((115,55,137),(-55,20,115),53)
}
for name,(pos,focal,angle) in views.items():
 cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*focal);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle);ren.ResetCameraClippingRange()
 w.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(w);f.ReadFrontBufferOff();f.Update()
 import vtk.util.numpy_support as nps
 arr=nps.vtk_to_numpy(f.GetOutput().GetPointData().GetScalars());h=660;ww=1050
 pix=np.flipud(arr.reshape(h,ww,-1))[:,:,:3]
 Image.fromarray(pix).save(R/f'{name}.png')
 print(name,round(np.mean(pix),1))
# 4 storyboard comps as real saved model images only.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for n,keys in [('FOUR_VIEWS',list(views)[:4]),('EIGHT_VIEWS',list(views))]:
 sheet=Image.new('RGB',(2100,700*(len(keys)//2)),(14,28,44));d=ImageDraw.Draw(sheet)
 for i,name in enumerate(keys):
  x=(i%2)*1050;y=(i//2)*700
  frame=Image.open(R/f'{name}.png').convert('RGB');sheet.paste(frame,(x,y+32))
  d.rectangle((x,y,x+1050,y+32),fill=(7,17,28));d.text((x+20,y+7),name,fill=(240,244,245),font=font)
 sheet.save(R/f'SAVED_GLB_{n}.jpg',quality=88)