"""Authentic VTK renders from exported PLY, not procedural paint or image-generation."""
from pathlib import Path
import vtk
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
C={
'ground':(54,65,78,255),'studio':(218,159,104,255),'structure':(115,147,169,255),
'skin':(160,183,197,255),'glazing':(111,214,213,125),'visitor':(246,207,136,255),
'research':(132,178,209,255),'learning':(224,192,134,255),'core':(69,156,177,255),
'machinery':(224,100,79,255),'residential':(213,215,193,255)}
VIEWS={
'01_district':([330,-340,245],[5,100,72],43),
'02_public_eye':([-40,105,21.5],[-39,28,28],62),
'03_learning_eye':([49,107,22],[65,190,36],66),
'04_workshop_interior':([18,-22,23],[-38,32,42],67),
'05_research_overlook':([63,180,138],[10,112,32],67),
'06_north':([300,330,250],[10,70,80],45),
}

def run(h):
    folder=ROOT/f'case_{h}'
    vtk.vtkObject.GlobalWarningDisplayOff()
    for name,(pos,target,fov) in VIEWS.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.065,.085,.12);ren.SetBackground2(.31,.38,.49);ren.GradientBackgroundOn()
        for cat,rgba in C.items():
            p=folder/f'{cat}.ply'
            if not p.exists():continue
            reader=vtk.vtkPLYReader();reader.SetFileName(str(p));reader.Update()
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(reader.GetOutput());mapper.ScalarVisibilityOff()
            a=vtk.vtkActor();a.SetMapper(mapper)
            a.GetProperty().SetColor(*(x/255 for x in rgba[:3]))
            a.GetProperty().SetAmbient(.34);a.GetProperty().SetDiffuse(.64)
            a.GetProperty().SetSpecular(.2);a.GetProperty().SetSpecularPower(20)
            a.GetProperty().SetOpacity(.47 if cat=='glazing' else 1)
            ren.AddActor(a)
        cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange()
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1350,900);win.SetMultiSamples(6);win.AddRenderer(ren)
        win.Render();flt=vtk.vtkWindowToImageFilter();flt.SetInput(win);flt.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(folder/f'{name}.png'));writer.SetInputConnection(flt.GetOutputPort());writer.Write();win.Finalize()
        print('RENDERED',h,name,flush=True)

if __name__=='__main__':
    for h in (70,90):run(h)
