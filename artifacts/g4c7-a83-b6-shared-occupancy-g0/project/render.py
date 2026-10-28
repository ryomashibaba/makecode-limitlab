from pathlib import Path
import json
import vtk
R=Path(__file__).resolve().parent/'output'
reader=vtk.vtkPLYReader();reader.SetFileName(str(R/'b6_shared_occupied_boundary.ply'));reader.Update()
poly=reader.GetOutput()
print('vtk triangles',poly.GetNumberOfPolys(),'points',poly.GetNumberOfPoints(), 'cells colors',bool(poly.GetCellData().GetScalars()),'point colors',bool(poly.GetPointData().GetScalars()))
views={
 'macro':((245,-280,205),(0,6,7),(0,0,1),35),
 'district':((134,-140,92),(0,8,8),(0,0,1),41),
 'public_eye':((22,-42,2.2),(10,8,6),(0,0,1),68),
 'upper_gallery':((-48,-15,10.3),(-14,23,10.1),(0,0,1),72),
}
for name,(loc,focal,up,angle) in views.items():
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(reader.GetOutputPort())
 mapper.SetScalarVisibility(True)
 if poly.GetCellData().GetScalars():mapper.SetScalarModeToUseCellData()
 actor=vtk.vtkActor();actor.SetMapper(mapper)
 actor.GetProperty().SetAmbient(.35);actor.GetProperty().SetDiffuse(.68)
 ren=vtk.vtkRenderer();ren.SetBackground(.022,.05,.075);ren.SetBackground2(.10,.15,.19);ren.GradientBackgroundOn()
 ren.AddActor(actor)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1500,950)
 win.SetMultiSamples(4)
 camera=ren.GetActiveCamera();camera.SetPosition(*loc);camera.SetFocalPoint(*focal);camera.SetViewUp(*up);camera.SetViewAngle(angle)
 ren.ResetCameraClippingRange()
 win.Render()
 filt=vtk.vtkWindowToImageFilter();filt.SetInput(win);filt.Update()
 png=vtk.vtkPNGWriter();png.SetFileName(str(R/(name+'.png')));png.SetInputConnection(filt.GetOutputPort());png.Write()
 win.Finalize()
 print(name,'rendered')
