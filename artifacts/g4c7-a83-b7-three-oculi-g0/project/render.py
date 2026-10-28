"""Render actual saved PLY with VTK. All views share exactly one source geometry."""
from pathlib import Path
import vtk
R=Path(__file__).resolve().parent/'output'
reader=vtk.vtkPLYReader();reader.SetFileName(str(R/'b7_civic_oculi_source.ply'));reader.Update()
poly=reader.GetOutput();print('vtk polygons',poly.GetNumberOfPolys(),'pts',poly.GetNumberOfPoints())
views={
 'macro':((530,-550,380),(0,-4,8),(0,0,1),40),
 'district':((155,-210,160),(-15,0,10),(0,0,1),46),
 'public_eye':((10,-20,2.0),(0,25,9),(0,0,1),74),
 'court_eye':((-145,-18,2.1),(-135,-80,11),(0,0,1),72),
}
for name,(loc,focal,up,angle) in views.items():
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(reader.GetOutputPort());mapper.SetScalarVisibility(True)
 if poly.GetCellData().GetScalars():mapper.SetScalarModeToUseCellData()
 actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetAmbient(.45);actor.GetProperty().SetDiffuse(.55)
 ren=vtk.vtkRenderer();ren.SetBackground(.022,.047,.067);ren.SetBackground2(.13,.20,.24);ren.GradientBackgroundOn();ren.AddActor(actor)
 light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(-120,140,400);light.SetFocalPoint(0,0,0);light.SetIntensity(.95);ren.AddLight(light)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1300,850);win.SetMultiSamples(4)
 camera=ren.GetActiveCamera();camera.SetPosition(*loc);camera.SetFocalPoint(*focal);camera.SetViewUp(*up);camera.SetViewAngle(angle)
 ren.ResetCameraClippingRange();win.Render()
 filt=vtk.vtkWindowToImageFilter();filt.SetInput(win);filt.Update()
 png=vtk.vtkPNGWriter();png.SetFileName(str(R/(name+'.png')));png.SetInputConnection(filt.GetOutputPort());png.Write()
 win.Finalize();print(name,'rendered')
