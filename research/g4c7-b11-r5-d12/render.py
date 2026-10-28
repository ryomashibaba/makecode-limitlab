"""D12 original saved-PLY renderer; generates 8 real views per case, no concept imagery."""
from pathlib import Path
import json
import vtk
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
COL={
 'land':(55,76,83),'public':(235,191,114),
 'maker':(211,133,95),'machine':(224,83,72),
 'research':(103,173,217),'culture':(236,182,126),
 'habitat':(194,218,182),'structure':(99,127,154),
 'porous_skin':(152,178,197),'glass':(74,204,215),
 'core':(88,190,189),'garden':(98,175,129)
}
CAMERAS={
 '01_whole':([760,-760,420],[0,-5,112],44),
 '02_district':([370,-470,264],[0,-8,112],49),
 '03_civic_maker_eye':([0,-20,22.1],[-150,-101,28],60),
 '04_civic_research_eye':([0,-20,22.1],[118,77,25],60),
 '05_public_valley':([0,-340,93],[0,20,140],45),
 '06_maker_inside':([-178,-151,25],[-151,-98,29],65),
 '07_research_upper':([98,142,139],[28,10,131],61),
 '08_habitat_eye':([(70+132)/2,83,223],[-25,-2,210],64),
}
W,H=1240,780
try:FONT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
except:FONT=ImageFont.load_default()
def render_case(folder):
    manifest=json.loads((folder/'manifest.json').read_text())
    geometry={}
    for name in manifest['category_files']:
        path=folder/(name+'.ply')
        rd=vtk.vtkPLYReader();rd.SetFileName(str(path));rd.Update()
        geo=rd.GetOutput()
        assert geo.GetNumberOfPolys()>0
        geometry[name]=geo
    for name,(pos,focal,fov) in CAMERAS.items():
        ren=vtk.vtkRenderer();ren.GradientBackgroundOn();ren.SetBackground(.045,.07,.11);ren.SetBackground2(.28,.35,.43)
        for role,geo in geometry.items():
            mp=vtk.vtkPolyDataMapper();mp.SetInputData(geo);mp.ScalarVisibilityOff()
            act=vtk.vtkActor();act.SetMapper(mp)
            prop=act.GetProperty()
            prop.SetColor(*[v/255 for v in COL[role]])
            prop.SetAmbient(.26);prop.SetDiffuse(.68);prop.SetSpecular(.2);prop.SetSpecularPower(18)
            if role=='glass':prop.SetOpacity(.47)
            ren.AddActor(act)
        cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*focal);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange()
        window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(W,H);window.SetMultiSamples(4)
        window.AddRenderer(ren);window.Render()
        filt=vtk.vtkWindowToImageFilter();filt.SetInput(window);filt.Update()
        writer=vtk.vtkPNGWriter();writer.SetFileName(str(folder/(name+'.png')));writer.SetInputConnection(filt.GetOutputPort());writer.Write()
        window.Finalize()
        print('rendered',folder.name,name,flush=True)
    imgs=[]
    for name in CAMERAS:
        im=Image.open(folder/(name+'.png')).convert('RGB');im.thumbnail((610,385))
        tile=Image.new('RGB',(640,438),(18,27,38));tile.paste(im,((640-im.width)//2,12))
        draw=ImageDraw.Draw(tile);draw.text((18,398),name.replace('_',' '),font=FONT,fill=(240,242,239))
        imgs.append(tile)
    sheet=Image.new('RGB',(1280,438*4),(11,17,25))
    for n,im in enumerate(imgs):sheet.paste(im,((n%2)*640,(n//2)*438))
    sheet.save(folder/'eight_views.png')
if __name__=='__main__':
    for n in ('height_70','height_90','height_70_no_housing'):
        render_case(ROOT/n)
