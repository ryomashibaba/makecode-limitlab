"""D11 real VTK camera captures from independently loaded persisted role PLYs.
NOT image-generation; no manual drawing of the city/model.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import vtk,argparse
ROOT=Path(__file__).resolve().parent
COLORS={
 'terrain':(43,60,71),'fault_mass':(116,135,149),'ceramic':(191,198,189),
 'dark_skin':(53,75,90),'public':(229,187,110),'maker':(228,125,91),
 'research':(97,177,205),'habitat':(164,200,151),'garden':(75,159,120),
 'structural':(101,143,164),'glass':(101,207,225),'core':(68,167,181),'light':(247,215,140)
}
VIEWS={
 '01_far':((1030,-920,540),(0,10,121),37),
 '02_district':((-635,-680,345),(0,10,130),54),
 '03_public_maker':((0,-94,23.1),(-135,38,32),63),
 '04_public_research':((0,-94,23.1),(130,65,34),63),
 '05_inner_urban_canyon':((22,-145,39),(0,115,139),63),
 '06_sky_habitat':((-20,167,224),(170,125,207),67),
 '07_rear_oblique':((680,540,428),(0,-30,145),42),
}

def render(folder):
 vtk.vtkObject.GlobalWarningDisplayOff()
 for name,(camera,target,angle) in VIEWS.items():
  ren=vtk.vtkRenderer();ren.SetBackground(.075,.108,.150);ren.SetBackground2(.34,.43,.52);ren.GradientBackgroundOn()
  for cat,col in COLORS.items():
   fp=folder/f'{cat}.ply'
   if not fp.exists():continue
   reader=vtk.vtkPLYReader();reader.SetFileName(str(fp));reader.Update()
   mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(reader.GetOutputPort());mapper.ScalarVisibilityOff()
   actor=vtk.vtkActor();actor.SetMapper(mapper)
   actor.GetProperty().SetColor(*[x/255 for x in col]);actor.GetProperty().SetAmbient(.29);actor.GetProperty().SetDiffuse(.71)
   actor.GetProperty().SetSpecular(.17);actor.GetProperty().SetSpecularPower(25)
   actor.GetProperty().SetOpacity(.75 if cat=='glass' else 1.)
   ren.AddActor(actor)
  light=vtk.vtkLight();light.SetPosition(-500,-500,800);light.SetFocalPoint(0,0,0)
  light.SetIntensity(.9);ren.AddLight(light)
  cam=ren.GetActiveCamera();cam.SetPosition(*camera);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(angle)
  ren.ResetCameraClippingRange()
  win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1280,850);win.SetMultiSamples(6);win.AddRenderer(ren)
  win.Render();flt=vtk.vtkWindowToImageFilter();flt.SetInput(win);flt.SetInputBufferTypeToRGB();flt.ReadFrontBufferOff();flt.Update()
  writer=vtk.vtkPNGWriter();writer.SetFileName(str(folder/(name+'.png')));writer.SetInputConnection(flt.GetOutputPort());writer.Write();win.Finalize()
  print('rendered',folder.name,name,flush=True)
 # montage 2 cols, 4 rows, compressed for review
 pics=[]
 for name in VIEWS:
  im=Image.open(folder/(name+'.png')).convert('RGB');im.thumbnail((720,480))
  tile=Image.new('RGB',(734,510),(19,30,42));tile.paste(im,((734-im.width)//2,26));
  ImageDraw.Draw(tile).text((15,8),name,fill='white');pics.append(tile)
 out=Image.new('RGB',(734*2,510*4),(16,22,34))
 for i,img in enumerate(pics):out.paste(img,((i%2)*734,(i//2)*510))
 out.save(folder/'seven_views.png',optimize=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',default='full_70');a=ap.parse_args();render(ROOT/a.case)
