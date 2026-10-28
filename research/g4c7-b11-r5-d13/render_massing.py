"""Render genuine categorical PLY from D13 author_massing, no concept CGI or imagegen."""
from pathlib import Path
import json
import vtk
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
COLORS={'earth':(75,93,99),'inhabited':(158,184,191),'fabrication':(214,139,100),
        'cultural':(229,188,120),'research':(100,176,202),'habitat':(189,211,172),
        'public_route':(233,193,115),'light':(123,211,218),'core':(92,166,174)}
CAMERAS={
 '01_distant':([1030,-1140,710],[0,-15,145],41),
 '02_district':([400,-670,360],[0,-30,110],49),
 '03_public_eye':([0,-20,26],[0,105,80],68),
 '04_culture_eye':([78,60,60],[-125,-140,100],68)}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for variant in ('canyon','braided','courts'):
 f=ROOT/variant;j=json.loads((f/'manifest.json').read_text())
 geos={}
 for tag in j['roles']:
  reader=vtk.vtkPLYReader();reader.SetFileName(str(f/f'{tag}.ply'));reader.Update()
  geos[tag]=reader.GetOutput()
 imgs=[]
 for name,(pos,target,angle) in CAMERAS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(.052,.07,.105);ren.SetBackground2(.24,.32,.41);ren.GradientBackgroundOn()
  for tag,geo in geos.items():
   mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(geo);mapper.ScalarVisibilityOff()
   actor=vtk.vtkActor();actor.SetMapper(mapper)
   prop=actor.GetProperty();prop.SetColor(*[c/255 for c in COLORS[tag]])
   prop.SetAmbient(.35);prop.SetDiffuse(.64);prop.SetSpecular(.16)
   ren.AddActor(actor)
  cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
  ren.ResetCameraClippingRange()
  window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(1024,680);window.SetMultiSamples(4);window.AddRenderer(ren)
  window.Render();flt=vtk.vtkWindowToImageFilter();flt.SetInput(window);flt.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(f/f'{name}.png'));writer.SetInputConnection(flt.GetOutputPort());writer.Write();window.Finalize()
  im=Image.open(f/f'{name}.png').convert('RGB');im.thumbnail((580,383))
  tile=Image.new('RGB',(610,420),(13,22,32));tile.paste(im,((610-im.width)//2,8))
  ImageDraw.Draw(tile).text((15,392),f'{variant} / {name}',font=font,fill=(237,241,240))
  imgs.append(tile)
 sheet=Image.new('RGB',(1220,840),(10,16,24))
 for i,tile in enumerate(imgs):sheet.paste(tile,((i%2)*610,(i//2)*420))
 sheet.save(f/'four_views.png')
 print('rendered',variant,flush=True)