"""Render from D10 persisted PLY. CI visualization, not aesthetic certification.
A geometry source is always rebuilt before calling this renderer.
"""
from pathlib import Path
import vtk
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
COLORS={
'terrain':(.19,.27,.31),'fabrication':(.78,.57,.41),'research':(.38,.69,.76),
'habitat':(.66,.78,.59),'city_body':(.54,.64,.71),'public':(.95,.77,.43),
'glass':(.18,.88,.83),'frame':(.34,.46,.58),'service':(.79,.36,.31),
'vegetation':(.33,.68,.45),
'ground':(.20,.28,.34),'floor':(.94,.77,.49),'maker':(.84,.50,.38),
'structure':(.48,.60,.70),'machine':(.90,.36,.27),'core':(.40,.70,.77)}
A={
'01_macro':([2220,-2100,1150],[20,180,110],34),
'02_district':([-1150,-800,430],[-165,155,100],39),
'03_public':([-220,70,22],[90,150,44],65),
'04_maker':([-420,-35,25],[18,85,32],65),
'05_research':([72,128,31],[230,178,96],65),
'06_upper':([585,630,380],[280,230,120],56),
'07_north':([600,1630,650],[95,205,105],40)}
B={
'01_district':([440,-340,300],[0,10,92],45),
'02_common_eye':([-20,20,21.7],[20,-25,30],74),
'03_maker_eye':([-70,12,23],[-154,-123,26],67),
'04_research_eye':([50,12,22],[108,92,26],67),
'05_upper_study':([100,60,121],[0,20,112],67),
'06_terrace':([100,70,216],[0,20,208],68),
'07_north':([250,350,270],[0,0,90],46)}
def run(folder,cameras):
    path=ROOT/folder
    vtk.vtkObject.GlobalWarningDisplayOff()
    for name,(pos,target,fov) in cameras.items():
        ren=vtk.vtkRenderer()
        ren.SetBackground(.07,.09,.14)
        ren.SetBackground2(.29,.36,.44)
        ren.GradientBackgroundOn()
        for category,color in COLORS.items():
            candidate=path/f'{category}.ply'
            if not candidate.is_file():continue
            reader=vtk.vtkPLYReader()
            reader.SetFileName(str(candidate))
            reader.Update()
            mapper=vtk.vtkPolyDataMapper()
            mapper.SetInputData(reader.GetOutput())
            mapper.ScalarVisibilityOff()
            actor=vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*color)
            actor.GetProperty().SetAmbient(.3)
            if category=='glass':actor.GetProperty().SetOpacity(.7)
            ren.AddActor(actor)
        cam=ren.GetActiveCamera()
        cam.SetPosition(*pos)
        cam.SetFocalPoint(*target)
        cam.SetViewUp(0,0,1)
        cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange()
        win=vtk.vtkRenderWindow()
        win.SetOffScreenRendering(True)
        win.SetSize(1080,680)
        win.AddRenderer(ren)
        win.Render()
        fil=vtk.vtkWindowToImageFilter()
        fil.SetInput(win)
        fil.Update()
        png=vtk.vtkPNGWriter()
        png.SetFileName(str(path/f'{name}.png'))
        png.SetInputConnection(fil.GetOutputPort())
        png.Write()
        win.Finalize()
        print(folder,name,flush=True)
    pics=sorted(path.glob('0?_*.png'))
    assert len(pics)==7,(folder,len(pics))
    out=Image.new('RGB',(1440,478*4),(20,27,39))
    draw=ImageDraw.Draw(out)
    for i,pic in enumerate(pics):
        x=(i%2)*720;y=(i//2)*478
        frame=Image.open(pic).convert('RGB').resize((720,450))
        out.paste(frame,(x,y+28))
        draw.text((x+10,y+6),pic.stem.upper().replace('_',' '),fill=(240,240,240))
    out.save(path/'seven_views.png')
if __name__=='__main__':
    for name in ('all_70','no_research_70'):run(name,A)
    run('d10b',B)
