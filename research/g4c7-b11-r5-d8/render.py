"""Persisted PLY -> true VTK views, same scene for panorama and close human views."""
from pathlib import Path
import json
import vtk
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
PALETTE={
    'landscape':(59,78,83),'urban_body':(172,190,193),'urban_warm':(201,184,161),
    'civic':(230,197,136),'maker':(231,144,114),'research':(122,174,212),
    'habitat':(202,211,189),'circulation':(242,214,148),
    'garden':(111,171,134),'glazing':(107,212,210),
    'support':(114,130,152),'transport':(97,147,178)}
VIEWS={
'macro':([-2880,-3850,1850],[0,120,100],32),
'cross_district':([1690,-1680,990],[0,85,93],41),
'civic_confluence':([-700,-710,390],[10,55,45],60),
'maker_public_eye':([-360,-130,30],[-250,-239,38],72),
'research_public_eye':([220,80,34],[260,155,35],70),
'high_residential_eye':([-620,700,118],[-170,240,72],65),
}
def render(variant):
    folder=ROOT/variant
    for name,(pos,target,fov) in VIEWS.items():
        r=vtk.vtkRenderer();r.SetBackground(.07,.095,.13);r.SetBackground2(.30,.37,.44);r.GradientBackgroundOn()
        for role,c in PALETTE.items():
            path=folder/(role+'.ply')
            if not path.exists():continue
            source=vtk.vtkPLYReader();source.SetFileName(str(path));source.Update()
            mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(source.GetOutput());mapper.ScalarVisibilityOff()
            actor=vtk.vtkActor();actor.SetMapper(mapper)
            prop=actor.GetProperty();prop.SetColor(*(x/255 for x in c));prop.SetAmbient(.31);prop.SetDiffuse(.67)
            prop.SetSpecular(.22);prop.SetSpecularPower(15);prop.SetOpacity(.82 if role=='glazing' else 1.0)
            r.AddActor(actor)
        c=r.GetActiveCamera();c.SetPosition(*pos);c.SetFocalPoint(*target);c.SetViewUp(0,0,1);c.SetViewAngle(fov)
        r.ResetCameraClippingRange()
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1350,850);win.SetMultiSamples(4);win.AddRenderer(r)
        win.Render();f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update()
        w=vtk.vtkPNGWriter();w.SetInputConnection(f.GetOutputPort());w.SetFileName(str(folder/(name+'.png')));w.Write();win.Finalize()
        print('RENDER',variant,name,flush=True)

def montage(variant):
    folder=ROOT/variant
    canvas=Image.new('RGB',(1990,1430),(16,22,32));d=ImageDraw.Draw(canvas)
    labels=['01 / macro whole-domain','02 / crossed districts','03 / civic confluence','04 / maker eye','05 / research eye','06 / residence viewpoint']
    for i,(name,label) in enumerate(zip(VIEWS,labels)):
        pic=Image.open(folder/(name+'.png')).convert('RGB');pic.thumbnail((980,410))
        x=15+(i%2)*995;y=15+(i//2)*466
        canvas.paste(pic,(x,y+31));d.text((x+6,y+6),label,fill=(235,239,241))
    canvas.save(folder/'six_views.png')
if __name__=='__main__':
    vtk.vtkObject.GlobalWarningDisplayOff()
    for v in ('inhabited','depopulated'):render(v);montage(v)