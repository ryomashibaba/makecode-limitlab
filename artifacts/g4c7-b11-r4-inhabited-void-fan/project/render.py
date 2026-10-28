"""Native vtkPLYReader evidence, one camera per ground truth view."""
from pathlib import Path
import vtk,json,hashlib
OUT=Path(__file__).resolve().parent/'output'
colors={'public':(0.38,0.78,0.82),'room':(0.94,0.78,0.58),'envelope':(0.58,0.70,0.86),'structure':(0.28,0.37,0.48),'detail':(0.95,0.52,0.35)}
vtk.vtkObject.GlobalWarningDisplayOff()
views={
 'macro':((345,-420,255),(0,0,43),38),
 'opposite':((-360,315,240),(0,0,43),37),
 'public_eye':((8,-31,14),(22,10,39),58),
 'high_eye':((-53,15,77),(12,5,59),62),
}
for name,(camPos,target,angle) in views.items():
  ren=vtk.vtkRenderer();ren.SetBackground(0.035,0.075,0.12);ren.SetBackground2(0.14,0.22,0.31);ren.GradientBackgroundOn()
  for part,rgb in colors.items():
    rd=vtk.vtkPLYReader();rd.SetFileName(str(OUT/(part+'.ply')));rd.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(rd.GetOutputPort())
    act=vtk.vtkActor();act.SetMapper(mapper)
    act.GetProperty().SetColor(*rgb);act.GetProperty().SetAmbient(0.45);act.GetProperty().SetDiffuse(0.65);act.GetProperty().SetSpecular(.16);act.GetProperty().SetSpecularPower(18)
    act.GetProperty().BackfaceCullingOff()
    ren.AddActor(act)
  # Only ground surface in rendering as world reference, not a structural claim.
  grid=vtk.vtkPlaneSource();grid.SetOrigin(-190,-190,-2);grid.SetPoint1(190,-190,-2);grid.SetPoint2(-190,190,-2)
  ground=vtk.vtkActor();gm=vtk.vtkPolyDataMapper();gm.SetInputConnection(grid.GetOutputPort());ground.SetMapper(gm)
  ground.GetProperty().SetColor(.09,.15,.19);ground.GetProperty().SetOpacity(.9);ren.AddActor(ground)
  light=vtk.vtkLight();light.SetPosition(50,-80,300);light.SetFocalPoint(0,0,40);light.SetIntensity(0.9);ren.AddLight(light)
  ren.GetActiveCamera().SetPosition(*camPos);ren.GetActiveCamera().SetFocalPoint(*target);ren.GetActiveCamera().SetViewUp(0,0,1);ren.GetActiveCamera().SetViewAngle(angle)
  ren.ResetCameraClippingRange()
  rw=vtk.vtkRenderWindow();rw.OffScreenRenderingOn();rw.SetSize(1350,880);rw.AddRenderer(ren);rw.SetMultiSamples(0)
  rw.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(rw);f.Update()
  write=vtk.vtkPNGWriter();write.SetInputConnection(f.GetOutputPort());write.SetFileName(str(OUT/(name+'.png')));write.Write()
  print(name, (OUT/(name+'.png')).stat().st_size)
