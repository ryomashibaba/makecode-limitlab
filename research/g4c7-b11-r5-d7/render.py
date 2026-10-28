"""Photographically faithful offscreen VTK captures from saved D7 part PLYs.
No image generation or artistic paint-over."
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import vtk
from build import ROOT, COLORS

VIEWS={
 '01_macro':([490,-580,400],[-10,20,115],37),
 '02_district':([235,-275,240],[-15,25,125],43),
 '03_public_eye':([-123,115,28],[-45,-26,72],61),
 '04_fabrication_eye':([-78,-42,28],[-20,-24,91],67),
 '05_research_eye':([-19,135,119],[30,30,130],65),
 '06_upper_eye':([56,193,205],[-70,30,114],66),
 '07_north_oblique':([230,470,315],[-30,15,135],42),
}

def draw(h):
 folder=ROOT/f'clearance_{h}'
 for name,(position,target,angle) in VIEWS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(.075,.103,.15);ren.SetBackground2(.36,.46,.55);ren.GradientBackgroundOn()
  for category,rgb in COLORS.items():
   p=folder/f'{category}.ply'
   if not p.exists():continue
   reader=vtk.vtkPLYReader();reader.SetFileName(str(p));reader.Update()
   poly=reader.GetOutput();mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly);mapper.ScalarVisibilityOff()
   actor=vtk.vtkActor();actor.SetMapper(mapper)
   actor.GetProperty().SetColor(*(x/255 for x in rgb[:3]));actor.GetProperty().SetAmbient(.32)
   actor.GetProperty().SetDiffuse(.66);actor.GetProperty().SetSpecular(.2)
   actor.GetProperty().SetSpecularPower(18)
   actor.GetProperty().SetOpacity(.63 if category=='glazing' else 1)
   ren.AddActor(actor)
  camera=ren.GetActiveCamera();camera.SetPosition(*position);camera.SetFocalPoint(*target);camera.SetViewUp(0,0,1);camera.SetViewAngle(angle)
  ren.ResetCameraClippingRange()
  win=vtk.vtkRenderWindow();win.SetOffScreenRendering(True);win.SetSize(1050,720);win.SetMultiSamples(4);win.AddRenderer(ren)
  win.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(folder/f'{name}.png'));writer.SetInputConnection(f.GetOutputPort());writer.Write()
  win.Finalize();print(h,name,flush=True)
 # 3x2 key view board excluding north (7th displayed optional)
 names=list(VIEWS.keys())
 bg=Image.new('RGB',(2100,2210),(241,244,246));d=ImageDraw.Draw(bg)
 for i,name in enumerate(names[:6]):
  im=Image.open(folder/f'{name}.png').convert('RGB').resize((1050,720))
  col=i%2;row=i//2;x=col*1050;y=row*735
  bg.paste(im,(x,y));d.rectangle((x,y+696,x+1050,y+732),fill=(15,27,42))
  d.text((x+22,y+706),f'D7 / {h}m / {name} / saved PLY',fill=(255,255,255))
 bg.save(folder/'six_views.png')

if __name__=='__main__':
 vtk.vtkObject.GlobalWarningDisplayOff()
 for h in (70,90):draw(h)
