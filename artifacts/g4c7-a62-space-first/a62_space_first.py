#!/usr/bin/env python3
"""A62 G0: real open-front rooms, floors, furnishing and four upper dwelling sketches.

Build the *usable destinations first*. NOT a metropolis; no unverified cliff,
roof, tube, bridge or macro skyline. VTK/OpenGL, not Blender/Cycles, and no G2/G3.
"""
import argparse, hashlib, json, math
from pathlib import Path
import vtk
HERE=Path(__file__).resolve().parent
PLAN=HERE/'scene_plan.json'
OUT=HERE/'output'

def validate(p):
    errors=[]
    if p['stage']!='A62' or p['construction']!='FORBIDDEN' or p.get('city_claim') is not False:errors.append('locked scope')
    rs=p['rooms']
    if [x['id'] for x in rs] != ['market','culture','research']:errors.append('roles')
    if len(p['housing'])<3:errors.append('housing')
    if {r['id'] for r in p['public_routes']} != {'to_market','to_culture','to_research'}:errors.append('route graph')
    for r in rs:
        if r['door_width']<4 or min(r['xmax']-r['xmin'],r['ymax']-r['ymin'])<14:errors.append('fake room '+r['id'])
        axis=r['ymin'] if r['entrance_side']=='south' else (r['xmin'] if r['entrance_side']=='west' else r['xmax'])
        if not (r['xmin']<r['xmax'] and r['ymin']<r['ymax']):errors.append('bad footprint')
        if r['entrance_side'] in ('east','west') and not r['ymin']+r['door_width']/2<r['door_center']<r['ymax']-r['door_width']/2:errors.append('door outside')
        if r['entrance_side']=='south' and not r['xmin']+r['door_width']/2<r['door_center']<r['xmax']-r['door_width']/2:errors.append('door outside')
    if errors:raise ValueError('A62 invalid G0 plan '+','.join(errors))
    return {'stage':'A62','plan':'PASS','rooms':3,'dwellings':len(p['housing']),'actual_daylight':'NOT_MEASURED','S1':'NOT_ASSESSED','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN'}

def negative_controls(p):
    import copy
    edits=[('room_depth',lambda x:x['rooms'][0].__setitem__('xmax',-28)),
           ('door_width',lambda x:x['rooms'][1].__setitem__('door_width',0.4)),
           ('missing_housing',lambda x:x.__setitem__('housing',[])),
           ('construction_unlock',lambda x:x.__setitem__('construction','ALLOWED')),
           ('wrong_route',lambda x:x['public_routes'].pop())]
    for name,edit in edits:
        bad=copy.deepcopy(p);edit(bad)
        try:validate(bad)
        except ValueError:pass
        else:raise AssertionError('NEGATIVE_MISSED '+name)
    print('A62_NEGATIVE_CONTROLS_5_OF_5_PASS')

class Scene:
    def __init__(self):
        self.ren=vtk.vtkRenderer()
        self.ren.GradientBackgroundOn();self.ren.SetBackground(.11,.18,.28);self.ren.SetBackground2(.39,.54,.65)
        self.win=vtk.vtkRenderWindow();self.win.SetOffScreenRendering(1);self.win.SetSize(1200,800)
        self.win.SetMultiSamples(4);self.win.AddRenderer(self.ren)
        self.data=[]
    def add(self,name,source,color,opacity=1):
        m=vtk.vtkPolyDataMapper();m.SetInputConnection(source.GetOutputPort())
        a=vtk.vtkActor();a.SetMapper(m);p=a.GetProperty();p.SetColor(color);p.SetOpacity(opacity)
        p.SetInterpolationToPhong();p.SetSpecular(.3);p.SetSpecularPower(55)
        self.ren.AddActor(a)
        self.data.append(name)
        return a
    def box(self,name,bounds,color,opacity=1):
        x1,x2,y1,y2,z1,z2=bounds
        c=vtk.vtkCubeSource();c.SetBounds(x1,x2,y1,y2,z1,z2)
        return self.add(name,c,color,opacity)
    def line(self,name,pts,r,color):
        pl=vtk.vtkPoints();ln=vtk.vtkCellArray()
        for a in pts:pl.InsertNextPoint(*a)
        for i in range(len(pts)-1):l=vtk.vtkLine();l.GetPointIds().SetId(0,i);l.GetPointIds().SetId(1,i+1);ln.InsertNextCell(l)
        pd=vtk.vtkPolyData();pd.SetPoints(pl);pd.SetLines(ln)
        t=vtk.vtkTubeFilter();t.SetInputData(pd);t.SetRadius(r);t.SetNumberOfSides(7);t.Update()
        return self.add(name,t,color)
    def human(self,name,x,y,z=0):
        # tiny unobtrusive calibrated 1.75 m figures; not proof of crowd occupancy
        skin=(.86,.66,.46);out=(.25,.49,.56)
        self.box(name+'_legs',(x-.22,x+.22,y-.17,y+.17,z+.08,z+.88),out)
        self.box(name+'_torso',(x-.3,x+.3,y-.22,y+.22,z+.88,z+1.5),out)
        sp=vtk.vtkSphereSource();sp.SetCenter(x,y,z+1.65);sp.SetRadius(.16);sp.SetPhiResolution(9);sp.SetThetaResolution(10)
        self.add(name+'_head',sp,skin)
    def camera(self,eye,target,angle=65):
        c=self.ren.GetActiveCamera();c.SetPosition(*eye);c.SetFocalPoint(*target);c.SetViewUp(0,0,1);c.SetViewAngle(angle)
        self.ren.ResetCameraClippingRange()
    def save(self,name,eye,target,angle):
        self.camera(eye,target,angle);self.win.Render()
        grab=vtk.vtkWindowToImageFilter();grab.SetInput(self.win);grab.SetInputBufferTypeToRGB();grab.ReadFrontBufferOff();grab.Update()
        wr=vtk.vtkPNGWriter();wr.SetFileName(str(OUT/name));wr.SetInputConnection(grab.GetOutputPort());wr.Write()

def build(p):
    s=Scene()
    blue=(.68,.80,.84);low=(.27,.38,.46);floor=(.47,.53,.55);teal=(.20,.54,.55);metal=(.74,.78,.76);warm=(.81,.55,.32);wood=(.58,.42,.29);plant=(.18,.46,.33)
    # Site and walkable public court, no fake full-city footprint.
    s.box('SITE_CONTEXT',(-42,44,-28,63,-1.8,-.50),(.26,.36,.39))
    s.box('PUBLIC_COURT_TRUE_FLOOR',(-14,14,-17,24,-.48,0),floor)
    s.box('CIVIC_PATH_CORE',(-3.7,3.7,-17,22,.015,.08),metal)
    s.box('CIVIC_PATH_CROSS',(-15,15,3.4,10,.015,.08),metal)
    for r in p['rooms']:
        n=r['id'];x1,x2,y1,y2=r['xmin'],r['xmax'],r['ymin'],r['ymax'];d=r['door_width'];dc=r['door_center']
        s.box(n+'_TRUE_FLOOR',(x1,x2,y1,y2,-.43,0),floor)
        h=5.5;t=.45
        def wall(label,xlo,xhi,ylo,yhi,zlo=0,zhi=h,color=blue):
            if xhi-xlo>.0001 and yhi-ylo>.0001:s.box(n+'_'+label,(xlo,xhi,ylo,yhi,zlo,zhi),color)
        if r['entrance_side']=='east':
            wall('front_low',x2-t,x2,y1,dc-d/2)
            wall('front_high',x2-t,x2,dc+d/2,y2)
            wall('door_header',x2-t,x2,dc-d/2,dc+d/2,4.1,h,metal)
        elif r['entrance_side']=='west':
            wall('front_low',x1,x1+t,y1,dc-d/2)
            wall('front_high',x1,x1+t,dc+d/2,y2)
            wall('door_header',x1,x1+t,dc-d/2,dc+d/2,4.1,h,metal)
        else:
            wall('front_left',x1,dc-d/2,y1,y1+t)
            wall('front_right',dc+d/2,x2,y1,y1+t)
            wall('door_header',dc-d/2,dc+d/2,y1,y1+t,4.1,h,metal)
        # Other full-room walls; true openings are empty space, not decals.
        if r['entrance_side']!='east':wall('east_side',x2-t,x2,y1,y2)
        if r['entrance_side']!='west':wall('west_side',x1,x1+t,y1,y2)
        if r['entrance_side']!='south':wall('south_side',x1,x2,y1,y1+t)
        wall('north_rear',x1,x2,y2-t,y2)
        # Rooftop: two separate strips leave an actual open-air strip; this is an OPEN public room and NOT a closed airtight building.
        # Behind actual occupied room is a second floor datum for housing studies, supported by wall edges.
        s.box(n+'_LEFT_ROOF', (x1,x1+3.9,y1+3,y2-1,5.6,6.0),low)
        s.box(n+'_RIGHT_ROOF',(x2-3.9,x2,y1+3,y2-1,5.6,6.0),low)
        # Varied equipment placed in the actual room at real depth; no labels over the doorway.
        if n=='market':
            for i,(yy,xx) in enumerate([(0,-25),(7,-24),(13,-25),(19,-24)]):
                s.box(f'MARKET_COUNTER_{i}',(xx-1.25,xx+1.25,yy-1.0,yy+1.0,0,1.1),wood)
                s.box(f'MARKET_PRODUCE_{i}',(xx-1.1,xx+1.1,yy-.75,yy+.75,1.1,1.38),warm)
        elif n=='culture':
            for i,yy in enumerate((27,35,42)):
                s.box(f'MAKER_BENCH_{i}',(-3.4,3.4,yy-1,yy+1,0,1.0),wood)
                s.box(f'MAKER_WORK_{i}',(-2,-.6,yy-.55,yy+.55,1.0,1.58),teal)
        else:
            for i,yy in enumerate((0,8,15,20)):
                s.box(f'RESEARCH_DESK_{i}',(20,26,yy-.7,yy+.7,0,1.1),wood)
                s.box(f'RESEARCH_BOOKCASE_{i}',(28,29.4,yy-1.35,yy+1.35,0,3.1),warm)
        # Glowing threshold frame only as detail, opening remains physically empty
        if r['entrance_side']=='east':
            s.box(n+'_door_sill',(x2-.7,x2,dc-d/2,dc+d/2,-.02,.07),teal)
        elif r['entrance_side']=='west':
            s.box(n+'_door_sill',(x1,x1+.7,dc-d/2,dc+d/2,-.02,.07),teal)
        else:s.box(n+'_door_sill',(dc-d/2,dc+d/2,y1,y1+.7,-.02,.07),teal)
    # Residential uses are ACTUAL bounded interior footprints, not facades drawn on giant shapes.
    for house in p['housing']:
        n=house['id'];x1,x2,y1,y2,z1,z2=house['bounds'];w=.35;roof=.42
        s.box(n+'_SUPPORTED_FLOOR',(x1,x2,y1,y2,z1-.5,z1),floor)
        s.box(n+'_BACK_WALL',(x1,x2,y2-w,y2,z1,z2),low)
        s.box(n+'_SIDE_A',(x1,x1+w,y1,y2,z1,z2),blue)
        s.box(n+'_SIDE_B',(x2-w,x2,y1,y2,z1,z2),blue)
        # human aperture on front wall with horizontal head and jambs; no glass sheet closing it.
        mid=(x1+x2)/2;a=min(3.4,(x2-x1)*.40)
        s.box(n+'_FRONT_L',(x1,mid-a/2,y1,y1+w,z1,z2),blue)
        s.box(n+'_FRONT_R',(mid+a/2,x2,y1,y1+w,z1,z2),blue)
        s.box(n+'_FRONT_LINTEL',(mid-a/2,mid+a/2,y1,y1+w,z1+3.1,z2),metal)
        s.box(n+'_PART_ROOF_L',(x1,x1+1.8,y1,y2,z2,z2+roof),low)
        s.box(n+'_PART_ROOF_R',(x2-1.8,x2,y1,y2,z2,z2+roof),low)
        s.box(n+'_BED',(mid-1.1,mid+1.1,y1+3.1,y1+5.6,z1,z1+.72),warm)
        s.box(n+'_DESK',(x1+1.0,x1+3.5,y2-3.6,y2-2.1,z1,z1+.7),wood)
        s.box(n+'_BALCONY',(x1,x2,y1-1.7,y1,z1-.5,z1),teal)
    # One planted outdoor area attached to the actually modelled public ground.
    s.box('GARDEN_POCKET_FLOOR',(-14,-6,-16,-8,0,.28),teal)
    for i,(x,y) in enumerate([(-12,-11),(-9,-14)]):
        s.box(f'GARDEN_PLANTER_{i}',(x-1.0,x+1.0,y-1,y+1,.28,.87),wood)
        sphere=vtk.vtkSphereSource();sphere.SetCenter(x,y,1.65);sphere.SetRadius(.85);sphere.SetThetaResolution(9);sphere.SetPhiResolution(7)
        s.add(f'GARDEN_TREE_{i}',sphere,plant)
    # A public gathering space people can stand in, not a decorative empty stadium.
    for i,(x,y) in enumerate([(-3,1),(4,6),(-2,15),(6,-2),(-12,5),(14,6),(-2,29),(-19,8),(20,8)]):
        s.human('SCALE_USER_'+str(i),x,y)
    for i,(x,y) in enumerate([(4,0),(-5,12)]):
        s.box('CIVIC_SEAT_'+str(i),(x-1.2,x+1.2,y-.5,y+.5,0,.55),wood)
    # Reference sun lighting and camera, not a physically certified daylight test.
    for xyz,brightness in [((-70,-100,160),1.25),((95,-30,65),.75)]:
        l=vtk.vtkLight();l.SetLightTypeToSceneLight();l.SetPosition(*xyz);l.SetFocalPoint(0,10,4);l.SetIntensity(brightness);s.ren.AddLight(l)
    OUT.mkdir(parents=True,exist_ok=True)
    protected=[OUT/q for q in ('public_heart.png','oblique.png','manifest.json')]
    if any(q.exists() for q in protected):
        raise FileExistsError('A62 evidence is append-only, refusing overwrites')
    s.save('public_heart.png',(0,-11,1.7),(0,19,2.8),65)
    s.save('oblique.png',(67,-79,58),(0,15,7),53)
    return s

def write_report(p,scene):
    h={}
    for fn in ('public_heart.png','oblique.png'):
        raw=(OUT/fn).read_bytes();h[fn]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    result={'stage':'A62','renderer':'VTK_OPENGL_NOT_BLENDER_CYCLES','new_scene':True,
        'scope':'three real room footprints and true wall apertures, four elevated housing room sketches, one shared outdoor court',
        'city_claim':False,'minecraft_construction':'FORBIDDEN',
        'rooms':3,'housing':4,'ground_route_intent':3,'scene_objects':len(scene.data),
        'visual_art':'NOT_ASSESSED','G0':'RESEARCH_ONLY','S1':'NOT_RUN',
        'G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN','outputs':h,
        'caveats':['Not a city skyline','Doors/floors are real polygons but walkability not path-certified','Upper housing access not certified','Daylight physically not measured','Visual art verdict must be set from image review']}
    (OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

def main():
    q=argparse.ArgumentParser();q.add_argument('--build',action='store_true');q.add_argument('--negative',action='store_true')
    a=q.parse_args();p=json.loads(PLAN.read_text());print(json.dumps(validate(p)))
    if a.negative:negative_controls(p)
    if a.build:
        s=build(p);print(json.dumps(write_report(p,s),indent=2))
if __name__=='__main__':main()
