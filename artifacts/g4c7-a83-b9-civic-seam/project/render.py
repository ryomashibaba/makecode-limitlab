"""VTK true renders from the saved B9 PLY; images are NOT art approval."""
from pathlib import Path
import json,hashlib
import vtk
R=Path(__file__).parent/'output'
r=vtk.vtkPLYReader();r.SetFileName(str(R/'b9_shared_civic_seam.ply'));r.Update()
p=r.GetOutput()
assert p.GetNumberOfPolys()>0 and p.GetNumberOfPoints()>0
views={
 'macro':((130,-150,94),(0,0,7),(0,0,1),43),
 'district':((66,-66,37),(-5,0,8),(0,0,1),48),
 'public_eye':((0,-26,1.7),(0,8,5),(0,0,1),75),
 'upper_eye':((0,-4,11.7),(0,13,11.7),(0,0,1),71),
}
hashes={}
for name,(loc,focal,up,angle) in views.items():
 mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(r.GetOutputPort());mapper.SetScalarVisibility(True)
 if p.GetCellData().GetScalars():mapper.SetScalarModeToUseCellData()
 actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetAmbient(.5);actor.GetProperty().SetDiffuse(.5)
 ren=vtk.vtkRenderer();ren.SetBackground(.023,.048,.07);ren.SetBackground2(.17,.23,.27);ren.GradientBackgroundOn();ren.AddActor(actor)
 light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(-100,-80,170);light.SetFocalPoint(0,0,5);light.SetIntensity(1.0);ren.AddLight(light)
 win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1200,780);win.SetMultiSamples(0)
 cam=ren.GetActiveCamera();cam.SetPosition(*loc);cam.SetFocalPoint(*focal);cam.SetViewUp(*up);cam.SetViewAngle(angle)
 ren.ResetCameraClippingRange();win.Render()
 f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update()
 w=vtk.vtkPNGWriter();w.SetFileName(str(R/(name+'.png')));w.SetInputConnection(f.GetOutputPort());w.Write()
 hashes[name]=hashlib.sha256((R/(name+'.png')).read_bytes()).hexdigest()
 win.Finalize()
print(json.dumps({'true_vtk_ply_images':hashes,'poly_count':p.GetNumberOfPolys()},indent=2))
(R/'render_manifest.json').write_text(json.dumps({'stage':'A83_B9_TRUE_VTK_REJECTABLE','source':'b9_shared_civic_seam.ply','images':hashes,'art':'HOLD','formal_safety':'NOT_RUN'},indent=2)+'\n')
